"""Common fragment models shared across all SDK schemas.

These fragments are composable sub-models embedded in payloads, results, and
registry entries. All extend BaseModelBase for consistent serialization.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .base_model_base import BaseModelBase


class ActorRecord(BaseModelBase):
    """Identity record for an actor (human or system).

    Attributes:
        actor_id: Unique identifier for the actor.
        role: Actor's platform role.
        display_name: Human-readable display name.
        delegation_chain: List of actor IDs in the delegation chain, if any.
    """

    actor_id: str
    role: str
    display_name: Optional[str] = None
    delegation_chain: List[str] = []


class ArtifactRef(BaseModelBase):
    """Reference to a registered artifact.

    Attributes:
        artifact_id: Unique identifier in the artifact registry.
        artifact_type: Type/category of the artifact.
        artifact_name: Human-readable name.
        uri: Storage URI or path.
        stage_name: Stage that produced this artifact.
        version: Artifact version label.
    """

    artifact_id: str
    artifact_type: Optional[str] = None
    artifact_name: Optional[str] = None
    uri: Optional[str] = None
    stage_name: Optional[str] = None
    version: Optional[str] = None


class MetricResult(BaseModelBase):
    """A single metric measurement.

    Attributes:
        metric_name: Metric identifier.
        value: Numeric metric value.
        unit: Optional unit label (e.g. %, bps, score).
        threshold: Optional policy threshold for comparison.
        status: pass/warn/breach relative to threshold.
        description: Human-readable description of this metric.
    """

    metric_name: str
    value: float
    unit: Optional[str] = None
    threshold: Optional[float] = None
    status: Optional[str] = None
    description: Optional[str] = None


class WarningRecord(BaseModelBase):
    """A non-blocking warning.

    Attributes:
        code: Warning code.
        message: Human-readable warning message.
        severity: Warning severity (low/medium/high).
        field: Optional field name associated with this warning.
        context: Optional context dict.
    """

    code: str
    message: str
    severity: str = "medium"
    field: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ErrorRecord(BaseModelBase):
    """A blocking error.

    Attributes:
        code: Error code.
        message: Human-readable error message.
        detail: Optional additional detail or stack trace.
        field: Optional field name associated with this error.
        is_retryable: Whether this error can be retried.
    """

    code: str
    message: str
    detail: Optional[str] = None
    field: Optional[str] = None
    is_retryable: bool = False


class PolicyContextRef(BaseModelBase):
    """Reference to active policy context.

    Attributes:
        policy_mode: Active policy enforcement mode.
        environment: Deployment environment name.
        domain: Model domain.
        active_policy_pack_id: ID of the active policy pack.
    """

    policy_mode: Optional[str] = None
    environment: Optional[str] = None
    domain: Optional[str] = None
    active_policy_pack_id: Optional[str] = None


class GovernanceSummary(BaseModelBase):
    """Summary of governance evaluation results.

    Attributes:
        policy_check_result: Overall policy result (pass/warn/breach/blocked).
        open_violations: Count of open policy violations.
        blocking_reasons: List of blocking reason descriptions.
        requires_escalation: Whether escalation has been triggered.
    """

    policy_check_result: str = "pass"
    open_violations: int = 0
    blocking_reasons: List[str] = []
    requires_escalation: bool = False


class CandidateSummary(BaseModelBase):
    """Summary of a candidate version for review payloads.

    Attributes:
        candidate_version_id: Unique candidate version identifier.
        version_label: Human-readable version label.
        stage_name: Stage that produced this candidate.
        artifact_refs: Artifact IDs associated with this candidate.
        key_metrics: Key metric results for comparison.
        is_selected: Whether this candidate has been selected.
    """

    candidate_version_id: str
    version_label: Optional[str] = None
    stage_name: Optional[str] = None
    artifact_refs: List[str] = []
    key_metrics: List[MetricResult] = []
    is_selected: bool = False


class ReviewSuggestion(BaseModelBase):
    """Suggested action or consideration for a review.

    Attributes:
        suggestion_type: Type of suggestion (action/concern/info).
        text: Human-readable suggestion text.
        priority: Suggestion priority (low/medium/high).
        evidence_ref: Optional artifact or event reference for context.
    """

    suggestion_type: str = "info"
    text: str
    priority: str = "medium"
    evidence_ref: Optional[str] = None
