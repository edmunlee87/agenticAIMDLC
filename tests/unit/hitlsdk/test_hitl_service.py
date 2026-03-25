"""Unit tests for HITLService — review lifecycle, action validation, and decision capture."""

from __future__ import annotations

import pytest

from sdk.auditsdk.audit_service import AuditService
from sdk.hitlsdk.action_validator import ActionValidator
from sdk.hitlsdk.models import (
    EscalationReason,
    ReviewAction,
    ReviewRecord,
    ReviewStatus,
    ReviewerAssignment,
)
from sdk.hitlsdk.review_store import ReviewStore
from sdk.hitlsdk.service import HITLService
from sdk.observabilitysdk.observability_service import ObservabilityService
from sdk.workflowsdk.models import ReviewType


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def audit_svc() -> AuditService:
    return AuditService()


@pytest.fixture()
def obs_svc() -> ObservabilityService:
    return ObservabilityService()


@pytest.fixture()
def svc(minimal_bundle, audit_svc: AuditService, obs_svc: ObservabilityService) -> HITLService:
    return HITLService(bundle=minimal_bundle, obs=obs_svc, audit=audit_svc)


@pytest.fixture()
def open_review(svc: HITLService) -> str:
    """Create a review and return the review_id."""
    r = svc.create_review(
        review_type=ReviewType.MODEL_SELECTION,
        stage_name="stage_a",
        run_id="run_01",
        project_id="proj_01",
        created_by="analyst_01",
        actor_role="validator",
        summary_for_reviewer="Select the best model for credit scoring.",
        reviewers=[
            ReviewerAssignment(reviewer_id="rev_01", reviewer_role="validator")
        ],
    )
    assert r.is_success
    return r.data["review_id"]


# ---------------------------------------------------------------------------
# Review lifecycle
# ---------------------------------------------------------------------------


class TestCreateReview:
    def test_create_review_success(self, svc: HITLService) -> None:
        r = svc.create_review(
            review_type=ReviewType.GENERIC,
            stage_name="stage_a",
            run_id="run_01",
            project_id="proj_01",
            created_by="analyst_01",
        )
        assert r.is_success
        assert r.data["review_id"].startswith("rev_")
        assert r.data["review_type"] == "generic"

    def test_create_review_empty_stage_raises(
        self, svc: HITLService
    ) -> None:
        r = svc.create_review(
            review_type=ReviewType.GENERIC,
            stage_name="",
            run_id="run_01",
            project_id="proj_01",
            created_by="analyst_01",
        )
        assert not r.is_success

    def test_multiple_reviews_for_same_run(self, svc: HITLService) -> None:
        for i in range(3):
            svc.create_review(
                review_type=ReviewType.GENERIC,
                stage_name="stage_a",
                run_id="run_01",
                project_id="proj_01",
                created_by="analyst_01",
            )
        lr = svc.list_reviews_for_run("run_01")
        assert lr.data["count"] == 3


class TestGetReview:
    def test_get_existing_review(self, svc: HITLService, open_review: str) -> None:
        r = svc.get_review(open_review)
        assert r.is_success
        assert r.data["review"]["review_id"] == open_review
        assert r.data["status"] == ReviewStatus.PENDING_REVIEW.value

    def test_get_missing_review_is_failure(self, svc: HITLService) -> None:
        r = svc.get_review("rev_missing")
        assert not r.is_success


class TestBuildReviewPayload:
    def test_payload_has_three_panels(self, svc: HITLService, open_review: str) -> None:
        r = svc.build_review_payload(open_review)
        assert r.is_success
        payload = r.data["payload"]
        assert "panel_a" in payload
        assert "panel_b" in payload
        assert "panel_c" in payload

    def test_payload_missing_review_is_failure(self, svc: HITLService) -> None:
        r = svc.build_review_payload("rev_nope")
        assert not r.is_success


# ---------------------------------------------------------------------------
# Action validation
# ---------------------------------------------------------------------------


class TestActionValidator:
    def test_valid_approve(self) -> None:
        store = ReviewStore()
        rec = ReviewRecord(
            review_id="rev_1",
            review_type=ReviewType.GENERIC,
            stage_name="s",
            run_id="r",
            project_id="p",
            created_by="analyst_01",
        )
        store.put(rec)
        validator = ActionValidator()
        errors = validator.validate(
            review=rec,
            action=ReviewAction.APPROVE,
            actor_id="rev_01",
            actor_role="validator",
        )
        assert errors == []

    def test_reject_without_rationale_fails(self) -> None:
        store = ReviewStore()
        rec = ReviewRecord(
            review_id="rev_2",
            review_type=ReviewType.GENERIC,
            stage_name="s",
            run_id="r",
            project_id="p",
            created_by="analyst_01",
        )
        store.put(rec)
        validator = ActionValidator()
        errors = validator.validate(
            review=rec,
            action=ReviewAction.REJECT,
            actor_id="rev_01",
            actor_role="validator",
            rationale="",
        )
        assert any("rationale" in e.lower() for e in errors)

    def test_developer_cannot_approve(self) -> None:
        rec = ReviewRecord(
            review_id="rev_3",
            review_type=ReviewType.GENERIC,
            stage_name="s",
            run_id="r",
            project_id="p",
            created_by="dev_01",
        )
        validator = ActionValidator()
        errors = validator.validate(
            review=rec,
            action=ReviewAction.APPROVE,
            actor_id="dev_01",
            actor_role="developer",
        )
        assert any("not authorised" in e.lower() for e in errors)

    def test_action_on_closed_review_fails(self) -> None:
        rec = ReviewRecord(
            review_id="rev_4",
            review_type=ReviewType.GENERIC,
            stage_name="s",
            run_id="r",
            project_id="p",
            created_by="analyst_01",
            status=ReviewStatus.APPROVED,
        )
        validator = ActionValidator()
        errors = validator.validate(
            review=rec,
            action=ReviewAction.APPROVE,
            actor_id="rev_01",
            actor_role="validator",
        )
        assert any("not open" in e.lower() for e in errors)

    def test_unacknowledged_violations_block_finalising(self) -> None:
        rec = ReviewRecord(
            review_id="rev_5",
            review_type=ReviewType.GENERIC,
            stage_name="s",
            run_id="r",
            project_id="p",
            created_by="analyst_01",
        )
        validator = ActionValidator()
        errors = validator.validate(
            review=rec,
            action=ReviewAction.APPROVE,
            actor_id="rev_01",
            actor_role="validator",
            active_violations=["POL-001"],
            policy_acknowledgments=[],
        )
        assert any("acknowledgment" in e.lower() for e in errors)

    def test_violations_with_acknowledgment_pass(self) -> None:
        rec = ReviewRecord(
            review_id="rev_6",
            review_type=ReviewType.GENERIC,
            stage_name="s",
            run_id="r",
            project_id="p",
            created_by="analyst_01",
        )
        validator = ActionValidator()
        errors = validator.validate(
            review=rec,
            action=ReviewAction.APPROVE,
            actor_id="rev_01",
            actor_role="validator",
            active_violations=["POL-001"],
            policy_acknowledgments=["POL-001"],
        )
        assert errors == []

    def test_allowed_for_role(self) -> None:
        validator = ActionValidator()
        actions = validator.allowed_for_role("validator")
        assert ReviewAction.APPROVE in actions
        assert ReviewAction.REJECT in actions

    def test_is_finalising(self) -> None:
        validator = ActionValidator()
        assert validator.is_finalising(ReviewAction.APPROVE)
        assert validator.is_finalising(ReviewAction.REJECT)
        assert not validator.is_finalising(ReviewAction.ACKNOWLEDGE)
        assert not validator.is_finalising(ReviewAction.DEFER)


# ---------------------------------------------------------------------------
# Decision capture
# ---------------------------------------------------------------------------


class TestSubmitAction:
    def test_approve_review(self, svc: HITLService, open_review: str) -> None:
        r = svc.approve_review(
            review_id=open_review,
            actor_id="rev_01",
            actor_role="validator",
        )
        assert r.is_success
        assert "decision_id" in r.data
        assert r.data["new_status"] == ReviewStatus.APPROVED.value

    def test_approve_closes_review(self, svc: HITLService, open_review: str) -> None:
        svc.approve_review(
            review_id=open_review,
            actor_id="rev_01",
            actor_role="validator",
        )
        gr = svc.get_review(open_review)
        assert gr.data["status"] == ReviewStatus.APPROVED.value

    def test_reject_with_rationale(self, svc: HITLService, open_review: str) -> None:
        r = svc.reject_review(
            review_id=open_review,
            actor_id="rev_01",
            actor_role="validator",
            rationale="Model Gini too low — insufficient discriminatory power.",
        )
        assert r.is_success
        assert r.data["new_status"] == ReviewStatus.REJECTED.value

    def test_reject_without_rationale_fails(self, svc: HITLService, open_review: str) -> None:
        r = svc.submit_action(
            review_id=open_review,
            action=ReviewAction.REJECT,
            actor_id="rev_01",
            actor_role="validator",
            rationale="",
        )
        assert not r.is_success

    def test_approve_with_conditions(self, svc: HITLService, open_review: str) -> None:
        r = svc.approve_with_conditions(
            review_id=open_review,
            actor_id="rev_01",
            actor_role="validator",
            conditions=["Must rerun stress test before deployment."],
        )
        assert r.is_success
        assert r.data["new_status"] == ReviewStatus.APPROVED_WITH_CHANGES.value

    def test_action_on_missing_review_fails(self, svc: HITLService) -> None:
        r = svc.approve_review(
            review_id="rev_missing",
            actor_id="rev_01",
            actor_role="validator",
        )
        assert not r.is_success

    def test_second_action_on_closed_review_fails(
        self, svc: HITLService, open_review: str
    ) -> None:
        svc.approve_review(
            review_id=open_review,
            actor_id="rev_01",
            actor_role="validator",
        )
        r = svc.reject_review(
            review_id=open_review,
            actor_id="rev_01",
            actor_role="validator",
            rationale="Changing my mind.",
        )
        assert not r.is_success

    def test_get_decision(self, svc: HITLService, open_review: str) -> None:
        r = svc.approve_review(
            review_id=open_review,
            actor_id="rev_01",
            actor_role="validator",
        )
        decision_id = r.data["decision_id"]
        gd = svc.get_decision(decision_id)
        assert gd.is_success
        assert gd.data["decision"]["review_id"] == open_review


# ---------------------------------------------------------------------------
# Escalation
# ---------------------------------------------------------------------------


class TestEscalateReview:
    def test_escalate_review(self, svc: HITLService, open_review: str) -> None:
        r = svc.escalate_review(
            review_id=open_review,
            actor_id="rev_01",
            actor_role="validator",
            escalate_to="cro_01",
            reason=EscalationReason.RISK_THRESHOLD_EXCEEDED,
            note="Gini below regulatory threshold.",
        )
        assert r.is_success
        assert r.data["new_status"] == ReviewStatus.ESCALATED.value
        assert r.data["escalated_to"] == "cro_01"

    def test_escalated_review_has_chain(self, svc: HITLService, open_review: str) -> None:
        svc.escalate_review(
            review_id=open_review,
            actor_id="rev_01",
            actor_role="validator",
            escalate_to="cro_01",
            reason=EscalationReason.MANUAL,
        )
        gr = svc.get_review(open_review)
        chain = gr.data["review"]["escalation_chain"]
        assert len(chain) == 1
        assert chain[0]["escalated_to"] == "cro_01"


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


class TestHealthCheck:
    def test_health_check(self, svc: HITLService, open_review: str) -> None:
        r = svc.health_check()
        assert r.is_success
        assert r.data["n_reviews"] == 1
        assert r.data["n_open"] == 1

    def test_health_check_after_approve(
        self, svc: HITLService, open_review: str
    ) -> None:
        svc.approve_review(
            review_id=open_review,
            actor_id="rev_01",
            actor_role="validator",
        )
        r = svc.health_check()
        assert r.data["n_open"] == 0
        assert r.data["n_decisions"] == 1
