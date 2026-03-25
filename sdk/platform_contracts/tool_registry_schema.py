"""Tool Registry Schema — canonical definition for tool registration records.

Every tool exposed to the agent/controller layer must have a corresponding
:class:`ToolRegistryEntry` instance registered with the platform's tool
registry at SDK bootstrap time.
"""

from __future__ import annotations

from typing import Any, Optional

from sdk.platform_core.schemas.base_model_base import BaseModelBase


class ToolFailureMode(BaseModelBase):
    """A discrete failure mode that a tool can exhibit.

    Args:
        code: Short machine-readable failure code (e.g. ``"TIMEOUT"``).
        description: Human-readable description of the failure condition.
        is_retriable: Whether the platform retry policy applies to this mode.
        escalation_required: Whether governance escalation is required.

    Examples:
        >>> mode = ToolFailureMode(
        ...     code="TIMEOUT",
        ...     description="Remote store did not respond within SLA.",
        ...     is_retriable=True,
        ...     escalation_required=False,
        ... )
    """

    code: str
    description: str
    is_retriable: bool = False
    escalation_required: bool = False


class ToolRegistryEntry(BaseModelBase):
    """Canonical registration record for a single platform tool.

    Exactly one entry should be registered per tool at SDK bootstrap.

    Args:
        tool_name: Unique kebab-case tool name
            (e.g. ``"artifact-write"``).
        tool_type: Category — one of ``"read"``, ``"write"``,
            ``"validate"``, ``"review"``, ``"route"``, ``"audit"``,
            ``"observe"``.
        backing_class: Fully-qualified Python class path
            (e.g. ``"sdk.artifactsdk.ArtifactService"``).
        inputs: JSON-schema-style dict describing accepted parameters.
        outputs: JSON-schema-style dict describing the returned payload.
        failure_modes: List of :class:`ToolFailureMode` records.
        retry_policy_ref: Optional reference key into ``retry_policies.yaml``.
        review_hook: Optional event type string that triggers a HITL review.
        audit_hook: Optional audit type string emitted on tool invocation.
        event_hook: Optional skill-event type emitted on tool invocation.
        requires_governance_gate: If ``True`` the tool cannot run while a
            blocking policy violation is active.
        sdk_layer: Integer layer number from the SDK layering model.

    Examples:
        >>> entry = ToolRegistryEntry(
        ...     tool_name="artifact-write",
        ...     tool_type="write",
        ...     backing_class="sdk.artifactsdk.ArtifactService",
        ...     inputs={"artifact_type": {"type": "string"}},
        ...     outputs={"artifact_id": {"type": "string"}},
        ...     failure_modes=[],
        ...     sdk_layer=2,
        ... )
    """

    tool_name: str
    tool_type: str
    backing_class: str
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    failure_modes: list[ToolFailureMode] = []
    retry_policy_ref: Optional[str] = None
    review_hook: Optional[str] = None
    audit_hook: Optional[str] = None
    event_hook: Optional[str] = None
    requires_governance_gate: bool = False
    sdk_layer: int = 1
