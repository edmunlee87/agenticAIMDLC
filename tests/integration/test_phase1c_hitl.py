"""Phase 1C integration tests: hitlsdk cross-SDK wiring.

Verifies that HITLService integrates correctly with:
- workflowsdk  (WorkflowService.start_stage invoked during create_review)
- observabilitysdk (review lifecycle events emitted to event store)
- auditsdk (decision/approval/signoff records written on action capture)

Scope per the plan (1C.4):
- Full review lifecycle (create -> build_payload -> approve)
- Escalation path (create -> escalate -> verify chain)
- Rejection -> rerun path (create -> reject -> verify status)
- Approval chain across multiple reviews for the same run
- hitlsdk <-> workflowsdk: start_stage driven by create_review
- hitlsdk <-> observabilitysdk: event types emitted per lifecycle step
- hitlsdk <-> auditsdk: audit records chained per decision

Note: policysdk integration is deferred to Phase 1D.
"""

from __future__ import annotations

from typing import Generator

import pytest

from sdk.auditsdk.audit_service import AuditService
from sdk.hitlsdk.models import EscalationReason, ReviewAction, ReviewStatus, ReviewerAssignment
from sdk.hitlsdk.service import HITLService
from sdk.observabilitysdk.observability_service import ObservabilityService
from sdk.workflowsdk.models import ReviewType
from sdk.workflowsdk.service import WorkflowService

from tests.unit.workflowsdk.conftest import minimal_bundle  # noqa: F401 re-export fixture


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

RUN_ID = "int_run_01"
PROJECT_ID = "int_proj_01"
STAGE_A = "stage_a"


@pytest.fixture()
def audit_svc() -> AuditService:
    return AuditService(run_id=RUN_ID, actor="system")


@pytest.fixture()
def obs_svc() -> ObservabilityService:
    return ObservabilityService(run_id=RUN_ID, actor="system")


@pytest.fixture()
def workflow_svc(minimal_bundle) -> WorkflowService:  # type: ignore[no-untyped-def]
    svc = WorkflowService(bundle=minimal_bundle)
    svc.initialize_run(
        run_id=RUN_ID,
        project_id=PROJECT_ID,
        first_stage=STAGE_A,
        actor_id="system",
        actor_role="developer",
    )
    return svc


@pytest.fixture()
def hitl_svc(
    minimal_bundle,  # type: ignore[no-untyped-def]
    obs_svc: ObservabilityService,
    audit_svc: AuditService,
    workflow_svc: WorkflowService,
) -> HITLService:
    return HITLService(
        bundle=minimal_bundle,
        obs=obs_svc,
        audit=audit_svc,
        workflow_service=workflow_svc,
    )


@pytest.fixture()
def open_review_id(hitl_svc: HITLService) -> str:
    """Create a review and return its ID."""
    r = hitl_svc.create_review(
        review_type=ReviewType.MODEL_SELECTION,
        stage_name=STAGE_A,
        run_id=RUN_ID,
        project_id=PROJECT_ID,
        created_by="analyst_01",
        actor_role="validator",
        summary_for_reviewer="Select best model for credit scoring.",
        reviewers=[ReviewerAssignment(reviewer_id="rev_01", reviewer_role="validator")],
    )
    assert r.is_success, f"create_review failed: {r.errors}"
    return r.data["review_id"]


# ---------------------------------------------------------------------------
# 1. Full review lifecycle (create -> build_payload -> approve)
# ---------------------------------------------------------------------------


class TestFullReviewLifecycle:
    def test_create_review_returns_review_id(self, hitl_svc: HITLService) -> None:
        r = hitl_svc.create_review(
            review_type=ReviewType.GENERIC,
            stage_name=STAGE_A,
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            created_by="analyst_01",
        )
        assert r.is_success
        assert r.data["review_id"].startswith("rev_")
        assert r.data["run_id"] == RUN_ID
        assert r.data["stage_name"] == STAGE_A

    def test_build_payload_returns_three_panels(
        self, hitl_svc: HITLService, open_review_id: str
    ) -> None:
        r = hitl_svc.build_review_payload(open_review_id)
        assert r.is_success
        payload = r.data["payload"]
        assert "panel_a" in payload
        assert "panel_b" in payload
        assert "panel_c" in payload

    def test_approve_transitions_review_to_approved(
        self, hitl_svc: HITLService, open_review_id: str
    ) -> None:
        r = hitl_svc.approve_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
        )
        assert r.is_success
        assert r.data["new_status"] == ReviewStatus.APPROVED.value

        gr = hitl_svc.get_review(open_review_id)
        assert gr.data["status"] == ReviewStatus.APPROVED.value

    def test_approve_with_conditions_transitions_correctly(
        self, hitl_svc: HITLService, open_review_id: str
    ) -> None:
        r = hitl_svc.approve_with_conditions(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
            conditions=["Must rerun stress test before deployment."],
            rationale="Gini acceptable but stress test pending.",
        )
        assert r.is_success
        assert r.data["new_status"] == ReviewStatus.APPROVED_WITH_CHANGES.value

    def test_decision_record_stored_and_retrievable(
        self, hitl_svc: HITLService, open_review_id: str
    ) -> None:
        r = hitl_svc.approve_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
        )
        decision_id = r.data["decision_id"]
        gd = hitl_svc.get_decision(decision_id)
        assert gd.is_success
        assert gd.data["decision"]["review_id"] == open_review_id
        assert gd.data["decision"]["decided_by"] == "rev_01"


# ---------------------------------------------------------------------------
# 2. Escalation path
# ---------------------------------------------------------------------------


class TestEscalationPath:
    def test_escalate_transitions_to_escalated(
        self, hitl_svc: HITLService, open_review_id: str
    ) -> None:
        r = hitl_svc.escalate_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
            escalate_to="cro_01",
            reason=EscalationReason.RISK_THRESHOLD_EXCEEDED,
            note="Model Gini below regulatory floor.",
        )
        assert r.is_success
        assert r.data["new_status"] == ReviewStatus.ESCALATED.value
        assert r.data["escalated_to"] == "cro_01"

    def test_escalation_chain_persisted(
        self, hitl_svc: HITLService, open_review_id: str
    ) -> None:
        hitl_svc.escalate_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
            escalate_to="cro_01",
            reason=EscalationReason.MANUAL,
        )
        gr = hitl_svc.get_review(open_review_id)
        chain = gr.data["review"]["escalation_chain"]
        assert len(chain) == 1
        assert chain[0]["escalated_to"] == "cro_01"
        assert chain[0]["reason"] == EscalationReason.MANUAL.value

    def test_double_escalation_builds_chain(
        self, hitl_svc: HITLService, open_review_id: str
    ) -> None:
        """A second escalation is permitted (escalate_review bypasses status check).

        `escalate_review` is not routed through `submit_action`/`ActionValidator`,
        so it can be applied even after a first escalation. This allows multi-hop
        escalation chains (e.g. analyst -> CRO -> board).
        """
        hitl_svc.escalate_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
            escalate_to="cro_01",
            reason=EscalationReason.MANUAL,
        )
        r2 = hitl_svc.escalate_review(
            review_id=open_review_id,
            actor_id="cro_01",
            actor_role="governance",
            escalate_to="board_01",
            reason=EscalationReason.AUTHORITY_INSUFFICIENT,
        )
        assert r2.is_success, f"Second escalation failed: {r2.errors}"
        gr = hitl_svc.get_review(open_review_id)
        chain = gr.data["review"]["escalation_chain"]
        assert len(chain) == 2
        assert chain[1]["escalated_to"] == "board_01"


# ---------------------------------------------------------------------------
# 3. Rejection -> rerun path
# ---------------------------------------------------------------------------


class TestRejectionPath:
    def test_reject_requires_rationale(
        self, hitl_svc: HITLService, open_review_id: str
    ) -> None:
        r = hitl_svc.submit_action(
            review_id=open_review_id,
            action=ReviewAction.REJECT,
            actor_id="rev_01",
            actor_role="validator",
            rationale="",
        )
        assert not r.is_success
        assert any("rationale" in e.lower() for e in r.errors)

    def test_reject_with_rationale_transitions_to_rejected(
        self, hitl_svc: HITLService, open_review_id: str
    ) -> None:
        r = hitl_svc.reject_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
            rationale="Gini coefficient insufficient for production deployment.",
        )
        assert r.is_success
        assert r.data["new_status"] == ReviewStatus.REJECTED.value

        gr = hitl_svc.get_review(open_review_id)
        assert gr.data["status"] == ReviewStatus.REJECTED.value

    def test_action_on_rejected_review_is_blocked(
        self, hitl_svc: HITLService, open_review_id: str
    ) -> None:
        hitl_svc.reject_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
            rationale="Gini too low.",
        )
        r2 = hitl_svc.approve_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
        )
        assert not r2.is_success


# ---------------------------------------------------------------------------
# 4. Approval chain (multiple reviews for the same run)
# ---------------------------------------------------------------------------


class TestApprovalChain:
    def test_multiple_reviews_same_run_listed(self, hitl_svc: HITLService) -> None:
        for stage in ("stage_a", "stage_b"):
            hitl_svc.create_review(
                review_type=ReviewType.GENERIC,
                stage_name=stage,
                run_id=RUN_ID,
                project_id=PROJECT_ID,
                created_by="analyst_01",
            )
        lr = hitl_svc.list_reviews_for_run(RUN_ID)
        assert lr.is_success
        assert lr.data["count"] == 2

    def test_list_open_reviews_only(self, hitl_svc: HITLService) -> None:
        r1 = hitl_svc.create_review(
            review_type=ReviewType.GENERIC,
            stage_name=STAGE_A,
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            created_by="analyst_01",
        )
        r2 = hitl_svc.create_review(
            review_type=ReviewType.GENERIC,
            stage_name="stage_b",
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            created_by="analyst_01",
        )
        # Approve the first one
        hitl_svc.approve_review(
            review_id=r1.data["review_id"],
            actor_id="rev_01",
            actor_role="validator",
        )
        lr_open = hitl_svc.list_reviews_for_run(RUN_ID, status=ReviewStatus.PENDING_REVIEW)
        assert lr_open.data["count"] == 1
        assert lr_open.data["reviews"][0]["review_id"] == r2.data["review_id"]


# ---------------------------------------------------------------------------
# 5. hitlsdk <-> observabilitysdk: events emitted
# ---------------------------------------------------------------------------


class TestObservabilityIntegration:
    def test_create_review_emits_opened_event(
        self, hitl_svc: HITLService, obs_svc: ObservabilityService, open_review_id: str
    ) -> None:
        qr = obs_svc.query_events(run_id=RUN_ID, event_type="hitl.review.opened")
        assert qr.is_success
        events = qr.data["events"]
        assert len(events) >= 1
        assert any(e["event_type"] == "hitl.review.opened" for e in events)

    def test_approve_emits_approve_event(
        self, hitl_svc: HITLService, obs_svc: ObservabilityService, open_review_id: str
    ) -> None:
        hitl_svc.approve_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
        )
        qr = obs_svc.query_events(run_id=RUN_ID, event_type="hitl.review.approve")
        assert qr.is_success
        assert len(qr.data["events"]) >= 1

    def test_escalate_emits_escalated_event(
        self, hitl_svc: HITLService, obs_svc: ObservabilityService, open_review_id: str
    ) -> None:
        hitl_svc.escalate_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
            escalate_to="cro_01",
            reason=EscalationReason.MANUAL,
        )
        qr = obs_svc.query_events(run_id=RUN_ID, event_type="hitl.review.escalated")
        assert qr.is_success
        assert len(qr.data["events"]) >= 1


# ---------------------------------------------------------------------------
# 6. hitlsdk <-> auditsdk: audit records written
# ---------------------------------------------------------------------------


class TestAuditIntegration:
    def test_approve_writes_audit_record(
        self, hitl_svc: HITLService, audit_svc: AuditService, open_review_id: str
    ) -> None:
        r = hitl_svc.approve_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
        )
        audit_id = r.data.get("audit_id", "")
        assert audit_id, "Expected a non-empty audit_id in result data"

        bundle = audit_svc.export_audit_bundle(run_id=RUN_ID)
        assert bundle.is_success
        records = bundle.data["bundle"]["records"]
        assert any(rec["audit_id"] == audit_id for rec in records)

    def test_reject_writes_audit_record_with_reason(
        self, hitl_svc: HITLService, audit_svc: AuditService, open_review_id: str
    ) -> None:
        rationale = "Model Gini insufficient."
        r = hitl_svc.reject_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
            rationale=rationale,
        )
        assert r.is_success
        audit_id = r.data.get("audit_id", "")
        bundle = audit_svc.export_audit_bundle(run_id=RUN_ID)
        records = bundle.data["bundle"]["records"]
        matching = [rec for rec in records if rec["audit_id"] == audit_id]
        assert len(matching) == 1
        assert rationale in matching[0]["reason"]

    def test_escalate_writes_audit_record(
        self, hitl_svc: HITLService, audit_svc: AuditService, open_review_id: str
    ) -> None:
        hitl_svc.escalate_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
            escalate_to="cro_01",
            reason=EscalationReason.RISK_THRESHOLD_EXCEEDED,
            note="Exceeded tolerance.",
        )
        bundle = audit_svc.export_audit_bundle(run_id=RUN_ID)
        assert bundle.is_success
        assert bundle.data["bundle"]["total_count"] >= 1


# ---------------------------------------------------------------------------
# 7. hitlsdk <-> workflowsdk: start_stage invoked on create_review
# ---------------------------------------------------------------------------


class TestWorkflowIntegration:
    def test_create_review_triggers_start_stage(
        self,
        hitl_svc: HITLService,
        workflow_svc: WorkflowService,
    ) -> None:
        """WorkflowService.start_stage is called when a review is opened."""
        r = hitl_svc.create_review(
            review_type=ReviewType.MODEL_SELECTION,
            stage_name=STAGE_A,
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            created_by="analyst_01",
            actor_role="developer",
        )
        assert r.is_success

        # The workflow event log should have a STAGE_STARTED event for stage_a
        events_r = workflow_svc.get_events(run_id=RUN_ID)
        assert events_r.is_success
        event_types = [e["event_type"] for e in events_r.data["events"]]
        assert "stage.started" in event_types

    def test_workflow_state_after_review_creation(
        self,
        hitl_svc: HITLService,
        workflow_svc: WorkflowService,
    ) -> None:
        hitl_svc.create_review(
            review_type=ReviewType.GENERIC,
            stage_name=STAGE_A,
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            created_by="analyst_01",
            actor_role="developer",
        )
        state_r = workflow_svc.get_state(run_id=RUN_ID, project_id=PROJECT_ID)
        assert state_r.is_success
        # Stage should be tracked in the state
        stages = state_r.data["state"]["stages"]
        assert STAGE_A in stages


# ---------------------------------------------------------------------------
# 8. Health check
# ---------------------------------------------------------------------------


class TestHealthCheck:
    def test_health_check_after_full_lifecycle(
        self, hitl_svc: HITLService, open_review_id: str
    ) -> None:
        hitl_svc.approve_review(
            review_id=open_review_id,
            actor_id="rev_01",
            actor_role="validator",
        )
        r = hitl_svc.health_check()
        assert r.is_success
        assert r.data["n_reviews"] == 1
        assert r.data["n_open"] == 0
        assert r.data["n_decisions"] == 1
