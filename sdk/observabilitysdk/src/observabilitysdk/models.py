"""Observability SDK event models.

All observability records are immutable and append-only. The event store
is the primary observability system of record for all MDLC platform activity.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventSeverity(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class EventCategory(str, Enum):
    WORKFLOW = "workflow"
    HITL = "hitl"
    GOVERNANCE = "governance"
    CONFIG = "config"
    SKILL = "skill"
    TOOL = "tool"
    ARTIFACT = "artifact"
    AUDIT = "audit"
    SYSTEM = "system"


class ObservabilityEvent(BaseModel):
    """An immutable, append-only observability event record.

    Covers all material platform activity: stage transitions, skill
    invocations, tool calls, HITL interactions, and system events.

    Args:
        event_id: Unique event identifier.
        event_type: Dot-namespaced event type (e.g. ``"workflow.stage.completed"``).
        category: High-level event category.
        severity: Event severity level.
        timestamp: UTC event timestamp.
        project_id: Associated project.
        run_id: Associated run.
        session_id: Associated UI/agent session.
        stage_name: Active MDLC stage at event time.
        trace_id: Distributed trace identifier.
        span_id: Span within the trace (for nested operations).
        actor_id: Actor who triggered the event.
        actor_role: Actor's active role.
        message: Human-readable event summary.
        data: Structured event payload (must be JSON-serialisable).
        duration_ms: Duration of the operation that produced this event.
        error_code: Error code if this is an error event.
        error_detail: Error detail string.
        schema_version: Schema version.
    """

    model_config = ConfigDict(frozen=True)

    event_id: str
    event_type: str
    category: EventCategory = EventCategory.SYSTEM
    severity: EventSeverity = EventSeverity.INFO
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    project_id: str = ""
    run_id: str = ""
    session_id: str = ""
    stage_name: str = ""
    trace_id: str = ""
    span_id: str = ""
    actor_id: str = ""
    actor_role: str = ""
    message: str = ""
    data: dict[str, Any] = Field(default_factory=dict)
    duration_ms: float | None = None
    error_code: str = ""
    error_detail: str = ""
    schema_version: str = "1.0.0"

    @field_validator("event_id", "event_type", mode="before")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("event_id and event_type must be non-empty")
        return v


class TraceContext(BaseModel):
    """Lightweight trace context for correlating spans across service calls.

    Args:
        trace_id: Root trace identifier.
        span_id: Current span identifier.
        parent_span_id: Parent span identifier (empty for root spans).
        baggage: Cross-cutting key-value context propagated through the trace.
    """

    model_config = ConfigDict(frozen=True)

    trace_id: str
    span_id: str
    parent_span_id: str = ""
    baggage: dict[str, str] = Field(default_factory=dict)
