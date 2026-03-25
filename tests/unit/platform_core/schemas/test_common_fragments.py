"""Unit tests for common fragment models."""

import pytest
from pydantic import ValidationError

from sdk.platform_core.schemas.common_fragments import (
    ActorRecord,
    ArtifactRef,
    CandidateSummary,
    ErrorRecord,
    GovernanceSummary,
    MetricResult,
    PolicyContextRef,
    ReviewSuggestion,
    WarningRecord,
)


class TestActorRecord:
    def test_minimal(self) -> None:
        actor = ActorRecord(actor_id="user_001", role="developer")
        assert actor.actor_id == "user_001"
        assert actor.display_name is None
        assert actor.delegation_chain == []

    def test_delegation_chain(self) -> None:
        actor = ActorRecord(
            actor_id="delegate",
            role="approver",
            delegation_chain=["originator", "supervisor"],
        )
        assert len(actor.delegation_chain) == 2

    def test_missing_actor_id_raises(self) -> None:
        with pytest.raises(ValidationError):
            ActorRecord(role="developer")  # type: ignore[call-arg]


class TestArtifactRef:
    def test_minimal(self) -> None:
        ref = ArtifactRef(artifact_id="art_001")
        assert ref.artifact_id == "art_001"
        assert ref.artifact_type is None

    def test_full(self) -> None:
        ref = ArtifactRef(
            artifact_id="art_002",
            artifact_type="model",
            artifact_name="LogisticScorecard_v1",
            uri="s3://bucket/models/v1",
            stage_name="model_fitting",
            version="1.0",
        )
        assert ref.uri == "s3://bucket/models/v1"


class TestMetricResult:
    def test_minimal(self) -> None:
        metric = MetricResult(metric_name="gini", value=0.72)
        assert metric.metric_name == "gini"
        assert metric.value == pytest.approx(0.72)

    def test_with_threshold(self) -> None:
        metric = MetricResult(
            metric_name="gini",
            value=0.50,
            threshold=0.55,
            status="breach",
        )
        assert metric.status == "breach"


class TestWarningRecord:
    def test_minimal(self) -> None:
        warn = WarningRecord(code="W001", message="Low sample count in segment")
        assert warn.code == "W001"

    def test_missing_message_raises(self) -> None:
        with pytest.raises(ValidationError):
            WarningRecord(code="W002")  # type: ignore[call-arg]


class TestErrorRecord:
    def test_minimal(self) -> None:
        err = ErrorRecord(code="E001", message="Feature not found")
        assert err.code == "E001"


class TestPolicyContextRef:
    def test_defaults(self) -> None:
        ref = PolicyContextRef()
        assert ref.policy_mode is None
        assert ref.environment is None

    def test_with_values(self) -> None:
        ref = PolicyContextRef(
            policy_mode="strict",
            environment="prod",
            domain="scorecard",
        )
        assert ref.policy_mode == "strict"


class TestGovernanceSummary:
    def test_defaults(self) -> None:
        summary = GovernanceSummary()
        assert summary.policy_check_result == "pass"
        assert summary.open_violations == 0
        assert summary.blocking_reasons == []
        assert summary.requires_escalation is False

    def test_with_violations(self) -> None:
        summary = GovernanceSummary(
            policy_check_result="breach",
            open_violations=2,
            blocking_reasons=["Gini below threshold", "Missing approval"],
        )
        assert summary.policy_check_result == "breach"
        assert summary.open_violations == 2
        assert len(summary.blocking_reasons) == 2


class TestCandidateSummary:
    def test_minimal(self) -> None:
        candidate = CandidateSummary(candidate_version_id="cand_001")
        assert candidate.is_selected is False

    def test_with_metrics(self) -> None:
        candidate = CandidateSummary(
            candidate_version_id="cand_002",
            version_label="v1.0",
            key_metrics=[MetricResult(metric_name="gini", value=0.72)],
        )
        assert len(candidate.key_metrics) == 1
        assert candidate.key_metrics[0].value == pytest.approx(0.72)


class TestReviewSuggestion:
    def test_minimal(self) -> None:
        suggestion = ReviewSuggestion(text="Review the Gini coefficient carefully.")
        assert suggestion.suggestion_type == "info"
        assert suggestion.priority == "medium"

    def test_action_type(self) -> None:
        suggestion = ReviewSuggestion(
            suggestion_type="action",
            text="Request additional validation data.",
            priority="high",
        )
        assert suggestion.suggestion_type == "action"
