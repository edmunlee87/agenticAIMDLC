"""widgetsdk.models -- UI widget contracts for the 3-panel review workspace.

Panel layout:
- Panel A (Left): Proposal + Evidence (read-only).
- Panel B (Center): Editable review form.
- Panel C (Right): Actions + Status + Governance.

All models are immutable (frozen Pydantic); the UI state is managed externally
by the :class:`~widgetsdk.session.WidgetSession`.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WidgetMode(str, Enum):
    """Rendering mode for a widget session."""
    JUPYTER = "jupyter"
    TERMINAL = "terminal"
    WEB = "web"


class ActionButtonSpec(BaseModel):
    """Specification for an action button in Panel C.

    Args:
        action_id: Unique action identifier.
        label: Button label.
        action_type: Type of action (e.g. ``"approve"``, ``"reject"``, ``"escalate"``).
        is_primary: Whether this is the primary action button.
        is_destructive: Whether this action is destructive (shown in red).
        requires_rationale: Whether the user must provide rationale before executing.
        disabled: Whether the button is currently disabled.
        tooltip: Hover tooltip text.
    """

    model_config = ConfigDict(frozen=True)

    action_id: str
    label: str
    action_type: str
    is_primary: bool = False
    is_destructive: bool = False
    requires_rationale: bool = True
    disabled: bool = False
    tooltip: str = ""


class EvidenceCard(BaseModel):
    """A single evidence card displayed in Panel A.

    Args:
        card_id: Unique card identifier.
        title: Card title.
        artifact_id: Backing artifact ID.
        artifact_type: Type of artifact (e.g. ``"metric_pack"``, ``"dq_report"``).
        summary: Brief summary text.
        metric_highlights: Key metric name → value pairs to display prominently.
        link_url: Optional link to the full artifact.
        is_sufficient: Whether this evidence alone satisfies a requirement.
    """

    model_config = ConfigDict(frozen=True)

    card_id: str
    title: str
    artifact_id: str = ""
    artifact_type: str = ""
    summary: str = ""
    metric_highlights: dict[str, Any] = Field(default_factory=dict)
    link_url: str = ""
    is_sufficient: bool = False


class ReviewFormField(BaseModel):
    """A single editable field in Panel B.

    Args:
        field_id: Unique field identifier.
        label: Field label.
        field_type: HTML-like input type (``"text"``, ``"textarea"``, ``"select"``, ``"checkbox"``).
        value: Current field value.
        options: For select fields, list of ``{"value": ..., "label": ...}`` dicts.
        required: Whether this field is required.
        placeholder: Placeholder text.
        help_text: Help text shown below the field.
    """

    model_config = ConfigDict(frozen=True)

    field_id: str
    label: str
    field_type: str = "textarea"
    value: Any = None
    options: list[dict[str, Any]] = Field(default_factory=list)
    required: bool = False
    placeholder: str = ""
    help_text: str = ""


class GovernanceStatusBar(BaseModel):
    """Governance status displayed at the top of Panel C.

    Args:
        run_id: Run ID.
        project_id: Project ID.
        stage_name: Current stage.
        policy_status: ``"ok"`` | ``"warning"`` | ``"blocking"``.
        blocking_reasons: List of blocking policy reasons.
        required_roles: Roles required to submit a review action.
        trace_id: Current trace ID.
        audit_complete: Whether audit completeness is met.
    """

    model_config = ConfigDict(frozen=True)

    run_id: str
    project_id: str
    stage_name: str = ""
    policy_status: str = "ok"
    blocking_reasons: list[str] = Field(default_factory=list)
    required_roles: list[str] = Field(default_factory=list)
    trace_id: str = ""
    audit_complete: bool = True


class ReviewWorkspace(BaseModel):
    """Complete 3-panel review workspace definition.

    Args:
        workspace_id: Unique workspace identifier.
        title: Workspace title.
        panel_a_title: Title for Panel A.
        evidence_cards: Evidence cards for Panel A.
        form_fields: Editable fields for Panel B.
        action_buttons: Action buttons for Panel C.
        governance_status: Governance status bar for Panel C.
        mode: :class:`WidgetMode`.
        metadata: Arbitrary extra data.
    """

    model_config = ConfigDict(frozen=True)

    workspace_id: str
    title: str
    panel_a_title: str = "Proposal & Evidence"
    evidence_cards: list[EvidenceCard] = Field(default_factory=list)
    form_fields: list[ReviewFormField] = Field(default_factory=list)
    action_buttons: list[ActionButtonSpec] = Field(default_factory=list)
    governance_status: GovernanceStatusBar | None = None
    mode: WidgetMode = WidgetMode.JUPYTER
    metadata: dict[str, Any] = Field(default_factory=dict)
