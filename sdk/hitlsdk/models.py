"""HITL SDK data models.

All review records and decisions are immutable. The review state machine
progresses: ``pending_review`` → one of: ``approved``, ``approved_with_changes``,
``rejected``, ``rerun_requested``, ``escalated``.

Escalation preserves the full escalation history chain.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import ConfigDict, Field, field_validator

from sdk.platform_core.schemas.base_model_base import BaseModelBase
from sdk.platform_core.schemas.common_fragments import ActorRecord, PolicyContextRef
from sdk.workflowsdk.models import ReviewType


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ReviewStatus(str, Enum):
    """Status machine for a HITL review."""

    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    APPROVED_WITH_CHANGES = "approved_with_changes"
    REJECTED = "rejected"
    RERUN_REQUESTED = "rerun_requested"
    ESCALATED = "escalated"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class ReviewAction(str, Enum):
    """Bounded set of actions a reviewer may take.

    Only these actions are accepted; free-text-only approval is rejected.
    """

    APPROVE = "approve"
    APPROVE_WITH_CHANGES = "approve_with_changes"
    REJECT = "reject"
    RERUN_WITH_PARAMETERS = "rerun_with_parameters"
    REQUEST_MORE_ANALYSIS = "request_more_analysis"
    ESCALATE = "escalate"
    ACKNOWLEDGE = "acknowledge"
    DEFER = "defer"


class EscalationReason(str, Enum):
    """Reason for escalating a review."""

    POLICY_BREACH = "policy_breach"
    SLA_BREACH = "sla_breach"
    REVIEWER_CONFLICT = "reviewer_conflict"
    AUTHORITY_INSUFFICIENT = "authority_insufficient"
    DISAGREEMENT = "disagreement"
    RISK_THRESHOLD_EXCEEDED = "risk_threshold_exceeded"
    MANUAL = "manual"


# ---------------------------------------------------------------------------
# ReviewerAssignment
# ---------------------------------------------------------------------------


class ReviewerAssignment(BaseModelBase):
    """Assignment of a reviewer to a review.

    Args:
        reviewer_id: Actor ID of the assigned reviewer.
        reviewer_role: Required role for this reviewer.
        assigned_at: Assignment timestamp.
        delegation_source: Actor ID who delegated (empty for direct assignment).
        is_mandatory: True if this reviewer's sign-off is mandatory.
    """

    model_config = ConfigDict(frozen=True)

    reviewer_id: str
    reviewer_role: str
    assigned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    delegation_source: str = ""
    is_mandatory: bool = True


# ---------------------------------------------------------------------------
# EscalationRecord
# ---------------------------------------------------------------------------


class EscalationRecord(BaseModelBase):
    """A single escalation step in the escalation chain.

    Args:
        escalation_id: Unique identifier for this escalation.
        escalated_by: Actor initiating the escalation.
        escalated_to: Target reviewer actor ID.
        reason: Escalation reason category.
        note: Free-text note explaining the escalation.
        escalated_at: Escalation timestamp.
    """

    model_config = ConfigDict(frozen=True)

    escalation_id: str
    escalated_by: str
    escalated_to: str
    reason: EscalationReason
    note: str = ""
    escalated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# ReviewRecord -- the core HITL review object
# ---------------------------------------------------------------------------


class ReviewRecord(BaseModelBase):
    """An immutable HITL review record.

    Represents a single governance review gate that must be cleared before
    a stage or version selection can proceed.

    Args:
        review_id: Unique review identifier.
        review_type: Type of HITL review.
        status: Current review status.
        stage_name: MDLC stage the review is attached to.
        run_id: Associated run.
        project_id: Owning project.
        session_id: Session in which the review was opened.
        trace_id: Distributed trace ID.
        created_by: Actor ID who opened the review.
        created_at: Review creation timestamp.
        sla_deadline: SLA deadline (None = no SLA).
        policy_context: Active policy context.
        reviewers: Assigned reviewers.
        escalation_chain: Ordered list of escalation steps.
        evidence_refs: Artifact/document IDs submitted as evidence.
        template_id: Review template used (loaded from YAML).
        subject_candidate_id: Candidate version under review (if applicable).
        subject_artifact_ids: Artifact IDs under review.
        summary_for_reviewer: Human-readable summary for the review UI.
        schema_version: Schema version.
    """

    model_config = ConfigDict(frozen=True)

    review_id: str
    review_type: ReviewType
    status: ReviewStatus = ReviewStatus.PENDING_REVIEW
    stage_name: str
    run_id: str
    project_id: str
    session_id: str = ""
    trace_id: str = ""
    created_by: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sla_deadline: Optional[datetime] = None
    policy_context: Optional[PolicyContextRef] = None
    reviewers: List[ReviewerAssignment] = Field(default_factory=list)
    escalation_chain: List[EscalationRecord] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)
    template_id: str = ""
    subject_candidate_id: str = ""
    subject_artifact_ids: List[str] = Field(default_factory=list)
    summary_for_reviewer: str = ""
    schema_version: str = "1.0"

    @field_validator("review_id", "stage_name", "run_id", "project_id", mode="before")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("review_id, stage_name, run_id, project_id must be non-empty")
        return v


# ---------------------------------------------------------------------------
# ReviewDecision -- the outcome of a completed review
# ---------------------------------------------------------------------------


class ReviewDecision(BaseModelBase):
    """Immutable record of the final decision on a review.

    Args:
        decision_id: Unique decision identifier.
        review_id: The review this decision resolves.
        action: The bounded action taken.
        decided_by: Actor ID making the decision.
        actor_role: Role of the deciding actor.
        decided_at: Decision timestamp.
        rationale: Decision rationale (mandatory for non-approve actions).
        audit_id: Audit record ID written at decision time.
        conditions: Approval conditions (for APPROVED_WITH_CHANGES).
        rerun_parameters: Parameters to use on rerun (for RERUN_WITH_PARAMETERS).
        policy_acknowledgments: Policy violations explicitly acknowledged.
    """

    model_config = ConfigDict(frozen=True)

    decision_id: str
    review_id: str
    action: ReviewAction
    decided_by: str
    actor_role: str = ""
    decided_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    rationale: str = ""
    audit_id: str = ""
    conditions: List[str] = Field(default_factory=list)
    rerun_parameters: Dict[str, Any] = Field(default_factory=dict)
    policy_acknowledgments: List[str] = Field(default_factory=list)
