"""Pydantic payload models mirroring the JSON schemas in configs/schemas/.

Each model corresponds exactly to one JSON Schema file and extends
:class:`~platform_core.schemas.base.BaseModelBase`.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field, field_validator, model_validator

from platform_contracts.enums import (
    CandidateType,
    GovernanceSeverity,
    InteractionMode,
    InteractionType,
    PolicyCheckResult,
    StageStatus,
    TokenMode,
    UIMode,
    WorkflowMode,
)
from platform_contracts.fragments import (
    ActorRecord,
    ArtifactRef,
    GovernanceFlags,
    PolicyContextRef,
    PolicyFindingRef,
    PolicyViolationRef,
)
from platform_core.schemas.base import BaseModelBase, GovernanceAwareModelBase


# ---------------------------------------------------------------------------
# RuntimeContext  (runtime_context.schema.json)
# ---------------------------------------------------------------------------


class RuntimeContext(GovernanceAwareModelBase):
    """Input to the runtime resolver for a given controller invocation.

    Extends :class:`GovernanceAwareModelBase` with execution-specific fields
    such as active_role, workflow_mode, and governance state.
    """

    active_role: str
    active_domain: str
    workflow_mode: WorkflowMode = WorkflowMode.DEVELOPMENT
    validation_mode: bool = False
    annual_review_mode: bool = False
    remediation_mode: bool = False
    policy_mode: str = ""
    pending_review_type: str = ""
    ui_entry_point: str = ""
    selected_candidate_version_id: str = ""
    candidate_versions_present: bool = False
    failure_state: str = ""
    active_overlays: list[str] = Field(default_factory=list)
    current_refs: dict[str, str] = Field(default_factory=dict)
    token_mode: TokenMode = TokenMode.STANDARD
    pending_remediation_actions: list[str] = Field(default_factory=list)
    delegation_context: dict[str, Any] | None = None

    @field_validator("active_role", "active_domain", mode="before")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("active_role and active_domain must be non-empty")
        return v


# ---------------------------------------------------------------------------
# ResolvedStack  (resolved_stack.schema.json)
# ---------------------------------------------------------------------------

from pydantic import BaseModel as _PB  # noqa: E402


class ResolvedSkillsModel(_PB):
    """Skill resolution output from the runtime resolver."""

    model_config = {"frozen": True}

    base_skills: list[str] = Field(default_factory=list)
    role_skill: str = ""
    domain_skill: str = ""
    stage_skill: str = ""
    overlay_skills: list[str] = Field(default_factory=list)
    support_skills: list[str] = Field(default_factory=list)
    ordered_skill_ids: list[str] = Field(default_factory=list)


class UIContractModel(_PB):
    """UI contract portion of a resolved stack."""

    model_config = {"frozen": True}

    ui_mode: UIMode = UIMode.IDLE
    interaction_mode: InteractionMode = InteractionMode.NONE
    token_mode: TokenMode = TokenMode.STANDARD
    requires_human_action: bool = False
    display_sections: list[str] = Field(default_factory=list)


class GovernanceConstraintsModel(_PB):
    """Governance constraints derived from the active policy context."""

    model_config = {"frozen": True}

    blocked_actions: list[str] = Field(default_factory=list)
    mandatory_review_reasons: list[str] = Field(default_factory=list)
    mandatory_audit_reasons: list[str] = Field(default_factory=list)
    approval_required: bool = False
    auto_continue_allowed: bool = True
    review_required: bool = False


class RetryPolicyModel(_PB):
    """Retry policy resolved for the current stage."""

    model_config = {"frozen": True}

    max_retries: int = 3
    retry_on: list[str] = Field(default_factory=list)
    backoff_mode: str = "exponential"


class ResolvedStack(_PB):
    """Output of the runtime resolver.

    Carries the effective skill stack, allowlist, UI contract, and governance
    constraints for the current stage / role / domain context.

    Not a BaseModelBase subclass because it is a *resolver output*, not an
    event schema -- it has no timestamp or actor fields.
    """

    model_config = {"frozen": True}

    project_id: str
    run_id: str
    session_id: str
    trace_id: str = ""
    correlation_id: str = ""
    stage_name: str
    active_role: str
    schema_version: str = "1.0.0"
    resolved_skills: ResolvedSkillsModel = Field(default_factory=ResolvedSkillsModel)
    sdk_allowlist: list[str] = Field(default_factory=list)
    sdk_blocklist: list[str] = Field(default_factory=list)
    ui_contract: UIContractModel = Field(default_factory=UIContractModel)
    governance_constraints: GovernanceConstraintsModel = Field(
        default_factory=GovernanceConstraintsModel
    )
    retry_policy: RetryPolicyModel = Field(default_factory=RetryPolicyModel)
    access_mode: str = "BUILD_ONLY"
    policy_context: PolicyContextRef | None = None


# ---------------------------------------------------------------------------
# InteractionPayload  (interaction_payload.schema.json)
# ---------------------------------------------------------------------------


class PolicyAcknowledgment(_PB):
    """An explicit acknowledgment of a policy finding by the actor."""

    model_config = {"frozen": True}

    finding_id: str
    acknowledged_at: datetime
    comment: str = ""


class InteractionPayload(BaseModelBase):
    """Structured input from UI or agent to a controller."""

    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="allow")

    interaction_id: str
    interaction_type: InteractionType
    action: str
    review_id: str = ""
    data: dict[str, Any] = Field(default_factory=dict)
    structured_edits: dict[str, Any] = Field(default_factory=dict)
    parameters: dict[str, Any] = Field(default_factory=dict)
    user_comment: str = ""
    attachments: list[dict[str, str]] = Field(default_factory=list)
    policy_acknowledgments: list[PolicyAcknowledgment] = Field(default_factory=list)

    @field_validator("interaction_id", "action", mode="before")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("interaction_id and action must be non-empty")
        return v


# ---------------------------------------------------------------------------
# ReviewPayload  (review_payload.schema.json)
# ---------------------------------------------------------------------------


class RiskFlag(_PB):
    """A risk flag surfaced as part of a review proposal."""

    model_config = {"frozen": True}

    severity: GovernanceSeverity = GovernanceSeverity.MEDIUM
    category: str = ""
    description: str = ""
    evidence_ref: str = ""


class ProposalSummary(_PB):
    """Business and technical summary for a HITL review."""

    model_config = {"frozen": True}

    business_summary: str = ""
    technical_summary: str = ""
    recommendation: str = ""
    alternatives: list[str] = Field(default_factory=list)
    risk_flags: list[RiskFlag] = Field(default_factory=list)


class GovernanceRequirements(_PB):
    """Mandatory governance conditions that must be satisfied before review closure."""

    model_config = {"frozen": True}

    required_evidence: list[str] = Field(default_factory=list)
    required_acknowledgments: list[str] = Field(default_factory=list)
    sla_deadline: datetime | None = None
    minimum_approval_authority: str = ""


class ReviewPayload(BaseModelBase):
    """Payload presented to a human reviewer at a governance gate."""

    review_id: str
    review_type: str
    title: str = ""
    decision_required: bool = True
    proposal_summary: ProposalSummary = Field(default_factory=ProposalSummary)
    evidence: list[ArtifactRef] = Field(default_factory=list)
    allowed_actions: list[str] = Field(default_factory=list)
    structured_edit_schema: dict[str, Any] = Field(default_factory=dict)
    policy_findings: list[PolicyFindingRef] = Field(default_factory=list)
    linked_refs: dict[str, str] = Field(default_factory=dict)
    timestamps: dict[str, datetime] = Field(default_factory=dict)
    governance_requirements: GovernanceRequirements = Field(
        default_factory=GovernanceRequirements
    )


# ---------------------------------------------------------------------------
# CandidateVersion  (candidate_version.schema.json)
# ---------------------------------------------------------------------------


class CandidateProvenance(_PB):
    """Data provenance for a candidate version."""

    model_config = {"frozen": True}

    feature_set_ref: str = ""
    dataset_snapshot_ref: str = ""
    skill_version: str = ""
    tool_versions: dict[str, str] = Field(default_factory=dict)


class CandidateVersion(BaseModelBase):
    """Versioned snapshot of a model or methodology produced at a build/train stage."""

    candidate_version_id: str
    candidate_type: CandidateType
    parent_candidate_version_id: str = ""
    label: str = ""
    description: str = ""
    status: str = "draft"
    artifact_refs: list[ArtifactRef] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, float] = Field(default_factory=dict)
    comparison_delta: dict[str, Any] = Field(default_factory=dict)
    policy_findings: list[PolicyFindingRef] = Field(default_factory=list)
    provenance: CandidateProvenance = Field(default_factory=CandidateProvenance)


# ---------------------------------------------------------------------------
# VersionSelection  (version_selection.schema.json)
# ---------------------------------------------------------------------------


class VersionSelection(BaseModelBase):
    """Immutable human selection record binding a CandidateVersion to a stage."""

    selection_id: str
    selected_candidate_version_id: str
    rejected_candidate_version_ids: list[str] = Field(default_factory=list)
    rationale: str = ""
    conditions: list[str] = Field(default_factory=list)
    review_id: str = ""
    audit_ref: str
    policy_findings_acknowledged: list[str] = Field(default_factory=list)
    immutable: bool = True

    @field_validator("audit_ref", mode="before")
    @classmethod
    def _audit_ref_required(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("audit_ref is mandatory on VersionSelection")
        return v


# ---------------------------------------------------------------------------
# StandardResponseEnvelope  (standard_response_envelope.schema.json)
# ---------------------------------------------------------------------------


class ResponseWarning(_PB):
    model_config = {"frozen": True}

    code: str = ""
    message: str = ""
    severity: str = "warning"


class ResponseError(_PB):
    model_config = {"frozen": True}

    code: str = ""
    message: str = ""
    detail: str = ""


class GovernanceSummary(_PB):
    model_config = {"frozen": True}

    policy_check_result: PolicyCheckResult = PolicyCheckResult.PASS
    open_violations: int = 0
    blocking_reasons: list[str] = Field(default_factory=list)


class StandardResponseEnvelope(BaseModelBase):
    """Standard response returned by all controllers to UI/agent."""

    status: str
    message: str = ""
    current_stage: str = ""
    next_stage: str = ""
    required_human_action: str = ""
    interaction_state: str = "idle"
    warnings: list[ResponseWarning] = Field(default_factory=list)
    errors: list[ResponseError] = Field(default_factory=list)
    artifacts_created: list[ArtifactRef] = Field(default_factory=list)
    candidate_versions_created: list[str] = Field(default_factory=list)
    selected_candidate_version_id: str = ""
    updated_metrics: dict[str, Any] = Field(default_factory=dict)
    review_created: bool = False
    review_id: str = ""
    validation_updates: dict[str, Any] = Field(default_factory=dict)
    workflow_state_patch: dict[str, Any] = Field(default_factory=dict)
    audit_ref: str = ""
    event_ref: str = ""
    governance_summary: GovernanceSummary = Field(default_factory=GovernanceSummary)
    token_usage_hint: dict[str, Any] = Field(default_factory=dict)
