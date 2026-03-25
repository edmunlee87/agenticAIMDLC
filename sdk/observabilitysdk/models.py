"""Observability SDK typed models.

Defines the SkillEvent domain model used by ObservabilityService.
Maps directly to configs/schemas/skill_event.schema.json.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sdk.platform_core.schemas.base_model_base import BaseModelBase


class TokenUsage(BaseModelBase):
    """Token usage metrics for an LLM invocation.

    Args:
        prompt_tokens: Tokens consumed in the prompt.
        completion_tokens: Tokens produced in the completion.
        total_tokens: Sum of prompt and completion tokens.
    """

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class SkillEvent(BaseModelBase):
    """Append-only observability event for any platform action.

    Maps to configs/schemas/skill_event.schema.json.

    Args:
        event_id: Unique event identifier.
        event_type: Type of event (from EventTypeEnum).
        timestamp: UTC event creation timestamp.
        project_id: Parent project identifier.
        run_id: Parent run identifier.
        session_id: Current session identifier.
        skill_name: Skill that emitted this event.
        stage_name: Stage in which this event occurred.
        actor: Actor who triggered the event.
        status: Outcome status (success/failure/warning/blocked).
        parent_event_id: Optional parent event for lineage tracing.
        token_usage: Optional token usage metrics.
        governance_gate_hit: Whether a governance gate was hit.
        review_created: Whether a HITL review was created.
        payload: Event-type-specific structured payload.
        error_detail: Error details if status is failure.
    """

    event_id: str
    event_type: str
    timestamp: Optional[datetime] = None
    project_id: Optional[str] = None
    run_id: Optional[str] = None
    session_id: Optional[str] = None
    skill_name: Optional[str] = None
    stage_name: Optional[str] = None
    actor: Optional[str] = None
    status: str = "success"
    parent_event_id: Optional[str] = None
    token_usage: Optional[TokenUsage] = None
    governance_gate_hit: bool = False
    review_created: bool = False
    payload: Optional[Dict[str, Any]] = None
    error_detail: Optional[str] = None


class EventLineage(BaseModelBase):
    """Lineage chain for a sequence of related events.

    Args:
        root_event_id: The originating event ID.
        chain: Ordered list of event IDs from root to leaf.
        event_types: Parallel list of event_type for each chain entry.
    """

    root_event_id: str
    chain: List[str] = []
    event_types: List[str] = []
