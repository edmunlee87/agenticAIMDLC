"""widgetsdk.builders -- factory functions for building standard workspace configurations.

Builders construct :class:`~widgetsdk.models.ReviewWorkspace` objects from
a :class:`~platform_core.schemas.payloads.ReviewPayload` and a
:class:`~platform_core.runtime.resolver.RuntimeDecision`.
"""

from __future__ import annotations

import uuid
from typing import Any

from widgetsdk.models import (
    ActionButtonSpec,
    EvidenceCard,
    GovernanceStatusBar,
    ReviewFormField,
    ReviewWorkspace,
    WidgetMode,
)

# ---------------------------------------------------------------------------
# Standard action sets
# ---------------------------------------------------------------------------

_APPROVE_ACTIONS = [
    ActionButtonSpec(action_id="approve", label="Approve", action_type="approve", is_primary=True, requires_rationale=True),
    ActionButtonSpec(action_id="reject", label="Reject", action_type="reject", is_destructive=True, requires_rationale=True),
    ActionButtonSpec(action_id="escalate", label="Escalate", action_type="escalate", requires_rationale=True),
    ActionButtonSpec(action_id="request_info", label="Request More Info", action_type="request_more_info", requires_rationale=True),
]

_RECOVERY_ACTIONS = [
    ActionButtonSpec(action_id="retry", label="Retry Stage", action_type="retry", is_primary=True, requires_rationale=False),
    ActionButtonSpec(action_id="rollback", label="Roll Back", action_type="rollback", is_destructive=True, requires_rationale=True),
    ActionButtonSpec(action_id="skip", label="Skip Stage", action_type="skip", requires_rationale=True),
    ActionButtonSpec(action_id="abort", label="Abort Run", action_type="abort", is_destructive=True, requires_rationale=True),
]

_SELECTION_ACTIONS = [
    ActionButtonSpec(action_id="select", label="Select Candidate", action_type="select", is_primary=True, requires_rationale=True),
    ActionButtonSpec(action_id="reject_all", label="Reject All", action_type="reject_all", is_destructive=True, requires_rationale=True),
]

_DEFAULT_FORM_FIELDS = [
    ReviewFormField(
        field_id="rationale",
        label="Rationale",
        field_type="textarea",
        required=True,
        placeholder="Provide your rationale for this action...",
        help_text="Minimum 20 characters required for audit trail.",
    ),
    ReviewFormField(
        field_id="conditions",
        label="Conditions (optional)",
        field_type="textarea",
        placeholder="List any conditions attached to this decision...",
    ),
    ReviewFormField(
        field_id="policy_acknowledged",
        label="I acknowledge the governance policy requirements",
        field_type="checkbox",
        required=True,
        value=False,
    ),
]


def build_review_workspace(
    review_payload: Any,
    runtime_decision: Any | None = None,
    mode: WidgetMode = WidgetMode.JUPYTER,
) -> ReviewWorkspace:
    """Build a standard 3-panel review workspace from a review payload.

    Args:
        review_payload: :class:`~hitlsdk.models.ReviewPayload` or compatible dict.
        runtime_decision: Optional :class:`~platform_core.runtime.resolver.RuntimeDecision`.
        mode: :class:`WidgetMode`. Default: JUPYTER.

    Returns:
        :class:`ReviewWorkspace`.
    """
    if isinstance(review_payload, dict):
        payload_dict = review_payload
    elif hasattr(review_payload, "model_dump"):
        payload_dict = review_payload.model_dump()
    else:
        payload_dict = vars(review_payload)

    stage_name = str(payload_dict.get("stage_name", ""))
    run_id = str(payload_dict.get("run_id", ""))
    project_id = str(payload_dict.get("project_id", ""))
    review_type = str(payload_dict.get("review_type", "approval"))
    candidates = payload_dict.get("candidates", [])
    metrics_summary = payload_dict.get("metrics_summary", {})

    # Panel A: evidence cards from metrics and candidates.
    evidence_cards: list[EvidenceCard] = []
    if metrics_summary:
        evidence_cards.append(
            EvidenceCard(
                card_id="metrics",
                title="Metrics Summary",
                summary="Key performance metrics from this stage.",
                metric_highlights={k: v for k, v in (metrics_summary if isinstance(metrics_summary, dict) else {}).items()},
            )
        )
    for i, candidate in enumerate(candidates if isinstance(candidates, list) else []):
        cand_dict = candidate if isinstance(candidate, dict) else vars(candidate)
        evidence_cards.append(
            EvidenceCard(
                card_id=f"candidate_{i}",
                title=f"Candidate: {cand_dict.get('candidate_id', i)}",
                artifact_id=str(cand_dict.get("artifact_id", "")),
                summary=str(cand_dict.get("description", "")),
                metric_highlights=cand_dict.get("metrics", {}),
            )
        )

    # Panel C: action buttons based on review type.
    if review_type == "recovery":
        actions = _RECOVERY_ACTIONS
    elif review_type == "selection":
        actions = _SELECTION_ACTIONS
    else:
        actions = _APPROVE_ACTIONS

    # Governance status bar.
    blocking_reasons: list[str] = []
    policy_status = "ok"
    if runtime_decision:
        gc = getattr(runtime_decision, "governance_constraints", None)
        if gc:
            blocking_reasons = list(getattr(gc, "blocking_reasons", []) or [])
            policy_status = "blocking" if blocking_reasons else "ok"

    gov_bar = GovernanceStatusBar(
        run_id=run_id,
        project_id=project_id,
        stage_name=stage_name,
        policy_status=policy_status,
        blocking_reasons=blocking_reasons,
        required_roles=list(getattr(runtime_decision, "required_review_roles", []) if runtime_decision else []),
        trace_id=str(payload_dict.get("trace_id", "")),
        audit_complete=not blocking_reasons,
    )

    workspace_id = str(uuid.uuid4())
    return ReviewWorkspace(
        workspace_id=workspace_id,
        title=f"Review: {stage_name or 'Stage'} — {review_type.replace('_', ' ').title()}",
        evidence_cards=evidence_cards,
        form_fields=_DEFAULT_FORM_FIELDS,
        action_buttons=actions,
        governance_status=gov_bar,
        mode=mode,
        metadata={"run_id": run_id, "project_id": project_id},
    )


def build_recovery_workspace(
    stage_name: str,
    run_id: str,
    project_id: str,
    error_message: str = "",
    recovery_options: list[str] | None = None,
    mode: WidgetMode = WidgetMode.JUPYTER,
) -> ReviewWorkspace:
    """Build a recovery workspace with contextual error information.

    Args:
        stage_name: Failed stage name.
        run_id: MDLC run ID.
        project_id: Project ID.
        error_message: Error description.
        recovery_options: Available recovery option labels.
        mode: :class:`WidgetMode`. Default: JUPYTER.

    Returns:
        :class:`ReviewWorkspace`.
    """
    evidence_cards = [
        EvidenceCard(
            card_id="error",
            title="Failure Details",
            summary=error_message or "No error details available.",
        )
    ]
    if recovery_options:
        evidence_cards.append(
            EvidenceCard(
                card_id="options",
                title="Available Recovery Paths",
                summary="\n".join(f"• {opt}" for opt in recovery_options),
            )
        )

    gov_bar = GovernanceStatusBar(
        run_id=run_id,
        project_id=project_id,
        stage_name=stage_name,
        policy_status="warning",
    )

    return ReviewWorkspace(
        workspace_id=str(uuid.uuid4()),
        title=f"Recovery: {stage_name}",
        evidence_cards=evidence_cards,
        form_fields=_DEFAULT_FORM_FIELDS,
        action_buttons=_RECOVERY_ACTIONS,
        governance_status=gov_bar,
        mode=mode,
    )
