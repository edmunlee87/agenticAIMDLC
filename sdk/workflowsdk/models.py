"""Workflow SDK core data models.

All event/state records use Pydantic v2 with ``frozen=True`` for immutability.
Workflow state is rebuilt by replaying :class:`WorkflowEvent` entries — no
in-place mutation anywhere in the codebase.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from sdk.platform_core.schemas.common_fragments import ActorRecord, PolicyContextRef
from sdk.platform_core.schemas.enums import StageStatusEnum


# ---------------------------------------------------------------------------
# Workflow-local enums (not in platform enums — workflow-specific semantics)
# ---------------------------------------------------------------------------


class WorkflowMode(str, Enum):
    """Overall workflow execution mode."""

    DEVELOPMENT = "development"
    VALIDATION = "validation"
    MONITORING = "monitoring"
    REMEDIATION = "remediation"
    COMMITTEE_REVIEW = "committee_review"


class UIMode(str, Enum):
    """Active UI layout mode."""

    IDLE = "idle"
    STAGE_PROGRESS = "stage_progress"
    REVIEW_3PANEL = "review_3panel"
    SELECTION_CARDS = "selection_cards"
    RECOVERY_PROMPT = "recovery_prompt"
    BOOTSTRAP = "bootstrap"


class InteractionMode(str, Enum):
    """Required interaction pattern."""

    NONE = "none"
    REVIEW_REQUIRED = "review_required"
    SELECTION_REQUIRED = "selection_required"
    RECOVERY_REQUIRED = "recovery_required"


class CandidateType(str, Enum):
    """Type of versioned candidate object."""

    BINNING_VERSION = "binning_version"
    MODEL_VERSION = "model_version"
    SCORE_VERSION = "score_version"
    FEATURE_SET = "feature_set"
    GENERIC = "generic"


class ReviewType(str, Enum):
    """Type of HITL review that preceded a selection."""

    GENERIC = "generic"
    COARSE_CLASSING = "coarse_classing"
    MODEL_SELECTION = "model_selection"
    BINNING_SELECTION = "binning_selection"
    SCORE_SCALING = "score_scaling"
    DEPLOYMENT_READINESS = "deployment_readiness"
    ANNUAL_REVIEW = "annual_review"


class WorkflowEventType(str, Enum):
    """All event types that drive workflow state mutations."""

    WORKFLOW_INITIALIZED = "workflow.initialized"
    STAGE_STARTED = "stage.started"
    STAGE_COMPLETED = "stage.completed"
    STAGE_FAILED = "stage.failed"
    STAGE_BLOCKED = "stage.blocked"
    STAGE_SKIPPED = "stage.skipped"
    REVIEW_OPENED = "review.opened"
    REVIEW_CLOSED = "review.closed"
    CANDIDATE_REGISTERED = "candidate.registered"
    CANDIDATE_SELECTED = "candidate.selected"
    SESSION_CREATED = "session.created"
    SESSION_RESUMED = "session.resumed"
    SESSION_SUSPENDED = "session.suspended"
    SESSION_CLOSED = "session.closed"
    CHECKPOINT_SAVED = "checkpoint.saved"
    RECOVERY_STARTED = "recovery.started"
    RECOVERY_COMPLETED = "recovery.completed"
    METADATA_UPDATED = "metadata.updated"


class BlockReason(str, Enum):
    """Why a stage transition was blocked."""

    REVIEW_PENDING = "review_pending"
    SELECTION_MISSING = "selection_missing"
    POLICY_BREACH = "policy_breach"
    PREREQUISITE_NOT_MET = "prerequisite_not_met"
    INVALID_TRANSITION = "invalid_transition"
    SESSION_INVALID = "session_invalid"


class RecoveryPath(str, Enum):
    """Recovery strategy choices after a stage failure."""

    RETRY = "retry"
    RERUN = "rerun"
    ROLLBACK = "rollback"
    RESUME = "resume"


class CandidateStatus(str, Enum):
    """Lifecycle status of a candidate version."""

    PENDING_REVIEW = "pending_review"
    SELECTED = "selected"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class SelectionStatus(str, Enum):
    """Status of a version selection record."""

    ACTIVE = "active"
    SUPERSEDED = "superseded"
    REVOKED = "revoked"


class SessionStatus(str, Enum):
    """Status of a UI/agent session."""

    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"
    EXPIRED = "expired"


# ---------------------------------------------------------------------------
# Governance flags (embedded in WorkflowState)
# ---------------------------------------------------------------------------


class GovernanceFlags(BaseModel):
    """Snapshot of current governance flag states.

    Args:
        requires_escalation: Escalation has been triggered.
        has_open_policy_violations: One or more policy violations are active.
        has_active_waiver: A waiver is currently active.
        is_in_remediation: Workflow is in remediation mode.
    """

    model_config = ConfigDict(frozen=True)

    requires_escalation: bool = False
    has_open_policy_violations: bool = False
    has_active_waiver: bool = False
    is_in_remediation: bool = False


# ---------------------------------------------------------------------------
# WorkflowEvent — the unit of the event log
# ---------------------------------------------------------------------------


class WorkflowEvent(BaseModel):
    """An immutable, append-only event in the workflow event log.

    Args:
        event_id: Unique event identifier.
        event_type: Type of state mutation.
        run_id: Active run at the time of the event.
        project_id: Owning project.
        session_id: Active session.
        trace_id: Distributed trace identifier.
        actor_id: Actor who triggered the event.
        actor_role: Role of the actor.
        stage_name: Active MDLC stage name.
        timestamp: UTC event timestamp.
        payload: Event-type-specific structured data.
        schema_version: Schema version.
    """

    model_config = ConfigDict(frozen=True)

    event_id: str
    event_type: WorkflowEventType
    run_id: str
    project_id: str
    session_id: str = ""
    trace_id: str = ""
    actor_id: str = "system"
    actor_role: str = "system"
    stage_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any] = Field(default_factory=dict)
    schema_version: str = "1.0"

    @field_validator("event_id", "run_id", "project_id", "stage_name", mode="before")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("event_id, run_id, project_id, stage_name must be non-empty")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dict representation."""
        d = self.model_dump()
        d["timestamp"] = self.timestamp.isoformat()
        d["event_type"] = self.event_type.value
        return d


# ---------------------------------------------------------------------------
# StageRecord — per-stage runtime state
# ---------------------------------------------------------------------------


class StageRecord(BaseModel):
    """Point-in-time record of a single stage's execution state.

    Args:
        stage_name: MDLC stage identifier.
        status: Current stage status.
        started_at: Stage start timestamp.
        completed_at: Stage completion timestamp.
        failed_at: Stage failure timestamp.
        block_reason: Reason the stage is blocked (if applicable).
        review_id: Active HITL review ID (if open).
        selected_candidate_id: ID of the selected candidate (if any).
        artifact_ids: Artifact IDs produced by this stage.
        error_detail: Error message if stage failed.
        attempt_count: Number of execution attempts.
    """

    model_config = ConfigDict(frozen=True)

    stage_name: str
    status: StageStatusEnum = StageStatusEnum.NOT_STARTED
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    block_reason: Optional[BlockReason] = None
    review_id: str = ""
    selected_candidate_id: str = ""
    artifact_ids: List[str] = Field(default_factory=list)
    error_detail: str = ""
    attempt_count: int = 0


# ---------------------------------------------------------------------------
# WorkflowState — rebuilt from event replay
# ---------------------------------------------------------------------------


class WorkflowState(BaseModel):
    """Reconstructed workflow state for a single run.

    Never persisted directly — always rebuilt by replaying WorkflowEvent
    entries from :class:`WorkflowStateStore`.

    Args:
        run_id: Run identifier.
        project_id: Owning project.
        workflow_mode: Active workflow mode.
        active_domain: Active domain pack.
        current_stage: Currently active stage name.
        stages: Map of stage_name -> :class:`StageRecord`.
        governance_flags: Current governance flag snapshot.
        ui_mode: Resolved UI mode for the current stage.
        interaction_mode: Resolved interaction mode.
        event_count: Number of events replayed to produce this state.
        last_event_id: Most recent event ID.
        session_id: Active session ID.
    """

    model_config = ConfigDict(frozen=True)

    run_id: str
    project_id: str
    workflow_mode: WorkflowMode = WorkflowMode.DEVELOPMENT
    active_domain: str = "generic"
    current_stage: str = ""
    stages: Dict[str, StageRecord] = Field(default_factory=dict)
    governance_flags: GovernanceFlags = Field(default_factory=GovernanceFlags)
    ui_mode: UIMode = UIMode.IDLE
    interaction_mode: InteractionMode = InteractionMode.NONE
    event_count: int = 0
    last_event_id: str = ""
    session_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dict representation."""
        return json.loads(self.model_dump_json())


# ---------------------------------------------------------------------------
# CandidateVersion
# ---------------------------------------------------------------------------


class CandidateVersion(BaseModel):
    """An immutable versioned candidate snapshot within a stage.

    Args:
        candidate_id: Unique candidate identifier (``cnd_<uuid>``).
        stage_name: Stage that produced this candidate.
        candidate_type: Type of versioned object.
        run_id: Run that produced this candidate.
        project_id: Owning project.
        created_by: Actor ID.
        created_at: Creation timestamp.
        version_label: Human-readable version label.
        summary: Human-readable summary for the HITL selection UI.
        metrics: Key performance metrics dict.
        artifact_ids: Related artifact IDs.
        status: Candidate lifecycle status.
        preceding_candidate_id: Prior version this supersedes.
        metadata: Additional metadata.
    """

    model_config = ConfigDict(frozen=True)

    candidate_id: str
    stage_name: str
    candidate_type: CandidateType
    run_id: str
    project_id: str
    created_by: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version_label: str = ""
    summary: str = ""
    metrics: Dict[str, Any] = Field(default_factory=dict)
    artifact_ids: List[str] = Field(default_factory=list)
    status: CandidateStatus = CandidateStatus.PENDING_REVIEW
    preceding_candidate_id: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dict."""
        d = self.model_dump()
        d["created_at"] = self.created_at.isoformat()
        d["candidate_type"] = self.candidate_type.value
        d["status"] = self.status.value
        return d


# ---------------------------------------------------------------------------
# VersionSelection
# ---------------------------------------------------------------------------


class VersionSelection(BaseModel):
    """An immutable record of a human version selection decision.

    Args:
        selection_id: Unique selection identifier.
        stage_name: Stage for which the selection applies.
        run_id: Active run.
        project_id: Owning project.
        selected_candidate_id: ID of the chosen candidate.
        selected_by: Actor ID.
        selected_at: Selection timestamp.
        rationale: Decision rationale.
        audit_id: Audit record ID generated at selection time.
        review_type: Type of HITL review that preceded this selection.
        conditions: List of approval conditions (if any).
        status: Selection lifecycle status.
    """

    model_config = ConfigDict(frozen=True)

    selection_id: str
    stage_name: str
    run_id: str
    project_id: str
    selected_candidate_id: str
    selected_by: str
    selected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    rationale: str = ""
    audit_id: str = ""
    review_type: ReviewType = ReviewType.GENERIC
    conditions: List[str] = Field(default_factory=list)
    status: SelectionStatus = SelectionStatus.ACTIVE

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dict."""
        d = self.model_dump()
        d["selected_at"] = self.selected_at.isoformat()
        d["review_type"] = self.review_type.value
        d["status"] = self.status.value
        return d


# ---------------------------------------------------------------------------
# SessionRecord
# ---------------------------------------------------------------------------


class SessionRecord(BaseModel):
    """An active or historical UI/agent session.

    Args:
        session_id: Unique session identifier.
        run_id: Associated run.
        project_id: Owning project.
        created_by: Actor ID.
        created_at: Session creation timestamp.
        last_active_at: Last activity timestamp.
        closed_at: Session close timestamp (None if still active).
        status: Session lifecycle status.
        ui_mode: UI mode active when last seen.
        last_stage: Stage active when the session was last seen.
        checkpoint_id: Most recent checkpoint ID.
        metadata: Arbitrary session metadata.
    """

    model_config = ConfigDict(frozen=True)

    session_id: str
    run_id: str
    project_id: str
    created_by: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: Optional[datetime] = None
    status: SessionStatus = SessionStatus.ACTIVE
    ui_mode: UIMode = UIMode.IDLE
    last_stage: str = ""
    checkpoint_id: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dict."""
        d = self.model_dump()
        d["created_at"] = self.created_at.isoformat()
        d["last_active_at"] = self.last_active_at.isoformat()
        d["closed_at"] = self.closed_at.isoformat() if self.closed_at else None
        d["status"] = self.status.value
        d["ui_mode"] = self.ui_mode.value
        return d


# ---------------------------------------------------------------------------
# CheckpointRecord
# ---------------------------------------------------------------------------


class CheckpointRecord(BaseModel):
    """A serialised workflow state snapshot for recovery.

    Args:
        checkpoint_id: Unique checkpoint identifier.
        run_id: Associated run.
        project_id: Owning project.
        session_id: Session active at checkpoint time.
        taken_at: Checkpoint timestamp.
        stage_name: Stage at checkpoint time.
        event_count: Number of events in the log at checkpoint time.
        last_event_id: Last event ID at checkpoint time.
        state_json: JSON-serialised :class:`WorkflowState`.
        is_valid: False if the checkpoint has been invalidated.
    """

    model_config = ConfigDict(frozen=True)

    checkpoint_id: str
    run_id: str
    project_id: str
    session_id: str = ""
    taken_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    stage_name: str = ""
    event_count: int = 0
    last_event_id: str = ""
    state_json: str = ""
    is_valid: bool = True

    def restore_state(self) -> WorkflowState:
        """Deserialise and return the checkpointed :class:`WorkflowState`.

        Returns:
            Reconstructed :class:`WorkflowState` from the checkpoint JSON.

        Raises:
            ValueError: If ``state_json`` is empty or malformed.
        """
        if not self.state_json:
            raise ValueError(f"Checkpoint '{self.checkpoint_id}' has no state_json.")
        return WorkflowState.model_validate_json(self.state_json)
