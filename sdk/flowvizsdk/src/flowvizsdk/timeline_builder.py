"""flowvizsdk.timeline_builder -- converts events to a sorted timeline.

Produces a flat, time-ordered list of :class:`~flowvizsdk.models.TimelineEntry`
objects for rendering in a timeline panel or audit log view.
"""

from __future__ import annotations

import logging
from typing import Any

from flowvizsdk.models import TimelineEntry

logger = logging.getLogger(__name__)

# Map event_type prefix → category label
_CATEGORY_MAP: list[tuple[str, str]] = [
    ("workflow.stage.", "workflow"),
    ("workflow.candidate.", "candidate"),
    ("workflow.recovery.", "recovery"),
    ("workflow.initialized", "workflow"),
    ("hitl.review.", "hitl"),
    ("artifact.", "artifact"),
    ("policy.", "governance"),
    ("audit.", "audit"),
]

_SUMMARY_TEMPLATES: dict[str, str] = {
    "workflow.stage.started": "Stage '{stage_name}' started",
    "workflow.stage.completed": "Stage '{stage_name}' completed",
    "workflow.stage.failed": "Stage '{stage_name}' failed",
    "workflow.stage.blocked": "Stage '{stage_name}' blocked",
    "workflow.initialized": "Workflow run initialized",
    "hitl.review.created": "Review opened for '{stage_name}'",
    "hitl.review.approved": "Review approved for '{stage_name}'",
    "hitl.review.rejected": "Review rejected for '{stage_name}'",
    "hitl.review.escalated": "Review escalated for '{stage_name}'",
    "artifact.registered": "Artifact registered at '{stage_name}'",
    "artifact.promoted": "Artifact promoted at '{stage_name}'",
    "workflow.candidate.registered": "Candidate registered at '{stage_name}'",
    "workflow.candidate.selected": "Candidate selected at '{stage_name}'",
    "workflow.recovery.applied": "Recovery applied at '{stage_name}'",
    "policy.evaluated": "Policy evaluated at '{stage_name}'",
    "policy.breach.detected": "Policy breach detected at '{stage_name}'",
}


def _categorise(event_type: str) -> str:
    for prefix, cat in _CATEGORY_MAP:
        if event_type.startswith(prefix):
            return cat
    return "system"


def _summarise(event_type: str, stage_name: str) -> str:
    tpl = _SUMMARY_TEMPLATES.get(event_type)
    if tpl:
        return tpl.format(stage_name=stage_name or "unknown")
    return event_type


class TimelineBuilder:
    """Accumulates observability events and produces sorted :class:`TimelineEntry` objects.

    Args:
        run_id: The run being visualized.
        project_id: The project being visualized.
    """

    def __init__(self, run_id: str, project_id: str) -> None:
        self._run_id = run_id
        self._project_id = project_id
        self._entries: list[TimelineEntry] = []

    def consume(self, event: Any, node_id: str | None = None) -> None:
        """Convert one observability event to a :class:`TimelineEntry`.

        Args:
            event: :class:`~observabilitysdk.models.ObservabilityEvent`.
            node_id: The node_id this event maps to (for cross-linking).
        """
        event_type: str = getattr(event, "event_type", "") or ""
        stage_name: str = getattr(event, "stage_name", "") or ""
        actor_id: str = getattr(event, "actor_id", "") or ""
        ts = getattr(event, "timestamp", None)
        event_id: str = getattr(event, "event_id", "") or ""
        severity: str = str(getattr(event, "severity", "info") or "info")

        if ts is None:
            return  # skip events without timestamps

        entry = TimelineEntry(
            entry_id=event_id,
            timestamp=ts,
            event_type=event_type,
            stage_name=stage_name,
            actor_id=actor_id,
            category=_categorise(event_type),
            severity=severity,
            summary=_summarise(event_type, stage_name),
            node_id=node_id or "",
            run_id=self._run_id,
            project_id=self._project_id,
        )
        self._entries.append(entry)

    def build_sorted(self) -> list[TimelineEntry]:
        """Return timeline entries sorted by timestamp ascending.

        Returns:
            Sorted list of :class:`TimelineEntry` objects.
        """
        return sorted(self._entries, key=lambda e: e.timestamp)
