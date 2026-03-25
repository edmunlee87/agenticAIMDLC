"""Base model classes for all MDLC payload models.

All schema-backed Python models extend :class:`BaseModelBase`. This enforces
frozen immutability, strict alias handling, and audit-complete metadata fields.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from platform_contracts.fragments import ActorRecord, GovernanceFlags, PolicyContextRef


class BaseModelBase(BaseModel):
    """Root model for all MDLC payload schemas.

    Provides mandatory governance fields present on every schema, plus
    Pydantic config for strict, frozen, JSON-serializable models.

    Subclasses must declare their own ``schema_version`` default and add
    schema-specific required fields.

    Args:
        project_id: Project identifier (required on all material schemas).
        run_id: Execution run identifier.
        session_id: UI/agent session identifier.
        trace_id: Distributed trace identifier (OpenTelemetry-compatible).
        correlation_id: Business correlation identifier for grouping related events.
        actor: Who triggered this event.
        timestamp: When the event occurred (UTC ISO-8601).
        stage_name: MDLC stage this event belongs to.
        policy_context: Active policy context snapshot.
        schema_version: Schema semver for forward-compatibility checks.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="forbid")

    project_id: str
    run_id: str
    session_id: str
    trace_id: str = ""
    correlation_id: str = ""
    actor: ActorRecord | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    stage_name: str = ""
    policy_context: PolicyContextRef | None = None
    schema_version: str = "1.0.0"

    @model_validator(mode="after")
    def _validate_ids_not_empty(self) -> "BaseModelBase":
        """Ensure primary identifiers are non-empty strings."""
        for field_name in ("project_id", "run_id", "session_id"):
            if not getattr(self, field_name, "").strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        return self


class GovernanceAwareModelBase(BaseModelBase):
    """Extends :class:`BaseModelBase` with governance state fields.

    Used by payload models that carry active governance state (e.g.
    :class:`RuntimeContext`, :class:`WorkflowState`).

    Args:
        governance_flags: Boolean governance state flags.
        active_policy_violations: Active violation references.
    """

    governance_flags: GovernanceFlags | None = None
    active_policy_violations: list[Any] = Field(default_factory=list)
