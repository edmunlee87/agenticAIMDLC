"""Payload models: RuntimeContext, ResolvedStack, InteractionPayload, ReviewPayload, StandardResponseEnvelope.

These are the five core payload types that flow through the platform per enhancement v0.1,
enriched with governance fields per the plan.

Flow: runtime_context -> resolved_stack -> review_payload -> interaction_payload -> standard_response_envelope
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .base_model_base import BaseModelBase
from .base_result import BaseResult
from .common_fragments import (
    ActorRecord,
    ArtifactRef,
    GovernanceSummary,
    PolicyContextRef,
)


class RuntimeContext(BaseModelBase):
    """Runtime context: input to the RuntimeResolver.

    Carries actor, stage, session, governance, and delegation context.
    Enriched with governance fields per enhancement v0.1.

    Attributes:
        context_id: Unique identifier for this context.
        project_id: Associated project identifier.
        run_id: Associated run identifier.
        session_id: Active session identifier.
        trace_id: Distributed trace identifier.
        correlation_id: Links related operations.
        actor: Actor making the request.
        timestamp: ISO 8601 timestamp with timezone.
        current_stage: Current workflow stage name.
        domain: Model domain (scorecard, ecl, etc.).
        model_family: Model family within domain.
        environment: Deployment environment.
        ui_mode: Active UI mode.
        interaction_mode: Active interaction mode.
        token_mode: Active token mode.
        policy_context: Active policy context reference.
        schema_version: Schema version for backward compatibility.
        pending_reviews: Active review IDs blocking this context.
        selected_candidate_version_ids: stage -> candidate_version_id map.
        active_candidate_versions: Active unselected candidate version IDs.
        workflow_state_ref: Reference to the current workflow state document.
        governance_flags: Active governance flag overrides.
        active_policy_violations: Active unresolved policy violations.
        pending_remediation_actions: Active remediation action IDs.
        delegation_context: Delegation info if actor is acting on behalf of another.
    """

    context_id: str
    project_id: str
    run_id: str
    session_id: str
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None
    actor: ActorRecord
    timestamp: str
    current_stage: str
    stage_name: Optional[str] = None
    domain: Optional[str] = None
    model_family: Optional[str] = None
    environment: Optional[str] = None
    ui_mode: Optional[str] = None
    interaction_mode: Optional[str] = None
    token_mode: Optional[str] = None
    policy_context: Optional[PolicyContextRef] = None
    schema_version: str = "1.0.0"
    pending_reviews: List[str] = []
    selected_candidate_version_ids: Dict[str, str] = {}
    active_candidate_versions: List[str] = []
    workflow_state_ref: Optional[str] = None
    governance_flags: Dict[str, bool] = {}
    active_policy_violations: List[Dict[str, Any]] = []
    pending_remediation_actions: List[str] = []
    delegation_context: Optional[Dict[str, Any]] = None
    session_metadata: Optional[Dict[str, Any]] = None


class ResolvedStack(BaseModelBase):
    """Output of the RuntimeResolver.

    Contains resolved skills, SDK allowlist, UI contract, response contract,
    and governance constraints. Enriched with governance_constraints per enhancement v0.1.

    Attributes:
        stack_id: Unique identifier for this resolved stack.
        context_id: Context ID this stack was resolved from.
        run_id: Associated run identifier.
        project_id: Associated project identifier.
        session_id: Active session identifier.
        trace_id: Distributed trace identifier.
        actor: Actor whose context was resolved.
        timestamp: Resolution timestamp.
        stage_name: Stage name resolved for.
        policy_context: Active policy context.
        schema_version: Schema version.
        resolved_skills: Ordered list of skill identifiers forming the stack.
        sdk_allowlist: SDK methods/tools the agent is permitted to call.
        blocked_tools: Tool names blocked for this context.
        ui_contract: Recommended UI mode, interaction mode, token mode.
        response_contract: HITL/approval/audit requirements.
        governance_constraints: Active governance constraints.
        retry_policy: Effective retry policy.
    """

    stack_id: str
    context_id: str
    run_id: str
    project_id: str
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None
    actor: Optional[ActorRecord] = None
    timestamp: str
    stage_name: Optional[str] = None
    policy_context: Optional[PolicyContextRef] = None
    schema_version: str = "1.0.0"
    resolved_skills: List[str] = []
    sdk_allowlist: List[str] = []
    blocked_tools: List[str] = []
    ui_contract: Dict[str, Any] = {}
    response_contract: Dict[str, Any] = {}
    governance_constraints: Dict[str, Any] = {}
    retry_policy: Dict[str, Any] = {}


class InteractionPayload(BaseModelBase):
    """Payload from UI/Bridge to Controller for any user action or edit.

    Includes bounded actions and policy acknowledgments.
    Enriched with policy_acknowledgments per enhancement v0.1.

    Attributes:
        interaction_id: Unique interaction identifier.
        review_id: Optional linked review ID.
        stage_name: Stage this interaction is for.
        project_id: Associated project.
        run_id: Associated run.
        session_id: Active session.
        trace_id: Distributed trace ID.
        actor: Actor performing the interaction.
        timestamp: Interaction timestamp.
        policy_context: Active policy context.
        schema_version: Schema version.
        interaction_type: Type of interaction.
        action: Bounded action taken.
        structured_edits: Structured edits (e.g. binning modifications).
        parameters: Additional action parameters.
        user_comment: Optional free-text comment (not a substitute for structured action).
        attachments: Optional file attachments.
        policy_acknowledgments: Policy findings the actor has explicitly acknowledged.
        context_ref: Reference to the RuntimeContext that triggered this.
        resolved_stack_ref: Reference to the ResolvedStack used for this interaction.
    """

    interaction_id: str
    review_id: Optional[str] = None
    stage_name: str
    project_id: Optional[str] = None
    run_id: Optional[str] = None
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None
    actor: ActorRecord
    timestamp: str
    policy_context: Optional[PolicyContextRef] = None
    schema_version: str = "1.0.0"
    interaction_type: str
    action: str
    structured_edits: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    user_comment: Optional[str] = None
    attachments: List[Dict[str, Any]] = []
    policy_acknowledgments: List[Dict[str, Any]] = []
    context_ref: Optional[str] = None
    resolved_stack_ref: Optional[str] = None


class ReviewPayload(BaseModelBase):
    """Review payload sent to UI for human review.

    Contains proposal, evidence, bounded actions, and governance requirements.
    Enriched with governance_requirements per enhancement v0.1.

    Attributes:
        review_id: Unique review identifier.
        review_type: Type of review (e.g. coarse_classing_review).
        stage_name: Stage this review is for.
        project_id: Associated project.
        run_id: Associated run.
        session_id: Active session.
        trace_id: Distributed trace ID.
        actor: Actor who created the review.
        timestamp: Review creation timestamp.
        policy_context: Active policy context.
        schema_version: Schema version.
        proposal_summary: Proposal title, summaries, and recommendation.
        evidence: Evidence items (artifact references).
        actions: Bounded allowed actions.
        structured_edit_schema: JSON Schema fragment for Panel B editable fields.
        linked_refs: Cross-references to related entities.
        timestamps: Created/SLA timestamps.
        governance_requirements: Required evidence, acknowledgments, SLA deadline.
        policy_findings: Policy findings to surface to reviewer.
        risk_flags: Risk flags to surface to reviewer.
        reviewer_assignment: Reviewer assignment and delegation.
        candidate_summaries: Candidate version summaries for selection reviews.
    """

    review_id: str
    review_type: str
    stage_name: str
    project_id: Optional[str] = None
    run_id: Optional[str] = None
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None
    actor: Optional[ActorRecord] = None
    timestamp: str
    policy_context: Optional[PolicyContextRef] = None
    schema_version: str = "1.0.0"
    proposal_summary: Optional[Dict[str, Any]] = None
    evidence: List[ArtifactRef] = []
    actions: List[str] = []
    structured_edit_schema: Optional[Dict[str, Any]] = None
    linked_refs: List[Dict[str, Any]] = []
    timestamps: Optional[Dict[str, str]] = None
    governance_requirements: Optional[Dict[str, Any]] = None
    policy_findings: List[Dict[str, Any]] = []
    risk_flags: List[Dict[str, Any]] = []
    reviewer_assignment: Optional[Dict[str, Any]] = None
    candidate_summaries: List[Dict[str, Any]] = []


class StandardResponseEnvelope(BaseResult):
    """Standard response envelope returned by Controllers to UI/Bridges.

    Extends BaseResult with workflow-specific fields and governance traceability.
    Enriched with audit_ref, event_ref, and governance_summary per enhancement v0.1.

    Attributes:
        envelope_id: Unique envelope identifier.
        run_id: Associated run identifier.
        project_id: Associated project identifier.
        session_id: Active session identifier.
        trace_id: Distributed trace identifier.
        correlation_id: Links related operations.
        actor: Actor that triggered this response.
        timestamp: Response timestamp.
        stage_name: Stage this response is for.
        policy_context: Active policy context.
        schema_version: Schema version.
        current_stage: Current stage after this operation.
        next_stage: Next recommended stage.
        required_human_action: Human action required (if any).
        interaction_state: Current UI interaction state.
        review_created: Whether a review was created.
        review_id: ID of created review.
        review_payload: Embedded review payload when review_created=True.
        validation_updates: Validation state updates.
        workflow_state_patch: Partial patch to apply to workflow state.
        audit_ref: Audit record ID for this response.
        event_ref: Observability event ID for this response.
        governance_summary: Policy check result and open violations.
        token_usage_hint: Token usage info for the current request.
    """

    envelope_id: str
    run_id: str
    project_id: Optional[str] = None
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None
    actor: Optional[ActorRecord] = None
    timestamp: str
    stage_name: Optional[str] = None
    policy_context: Optional[PolicyContextRef] = None
    schema_version: str = "1.0.0"
    current_stage: Optional[str] = None
    next_stage: Optional[str] = None
    required_human_action: Optional[str] = None
    interaction_state: Optional[str] = None
    candidate_versions_created: List[str] = []
    selected_candidate_version_id: Optional[str] = None
    updated_metrics: Optional[Dict[str, Any]] = None
    review_created: bool = False
    review_id: Optional[str] = None
    review_payload: Optional[ReviewPayload] = None
    validation_updates: Optional[Dict[str, Any]] = None
    workflow_state_patch: Optional[Dict[str, Any]] = None
    audit_ref: Optional[str] = None
    event_ref: Optional[str] = None
    governance_summary: Optional[GovernanceSummary] = None
    token_usage_hint: Optional[Dict[str, Any]] = None
