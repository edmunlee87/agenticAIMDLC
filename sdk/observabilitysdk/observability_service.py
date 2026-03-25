"""ObservabilityService — primary observability SDK service class.

Responsibilities:
- Create traces (parent events) for skill/stage invocations.
- Write individual skill events (append-only, governance-enriched).
- Query event history for a run or session.
- Replay a run's event sequence.
- Build event lineage chains.
- Block restricted actions if event write fails.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from sdk.platform_core.schemas.base_result import BaseResult
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider
from sdk.platform_core.services.base_service import BaseService

from .event_store import EventStoreAdapter, InMemoryEventStore
from .models import EventLineage, SkillEvent, TokenUsage

logger = logging.getLogger(__name__)


class ObservabilityService(BaseService):
    """Observability SDK service: create traces and write/query skill events.

    Uses a pluggable :class:`~.event_store.EventStoreAdapter`. Defaults to
    :class:`~.event_store.InMemoryEventStore`.

    IMPORTANT: If :meth:`write_event` fails (store raises), all subsequent
    calls to :meth:`write_event` will return a ``blocked`` result until
    the store is healthy. This enforces the governance principle that
    observability write failures must block progress.

    Args:
        run_id: Optional run_id for correlation.
        actor: Actor identifier.
        event_store: Optional custom event store adapter.

    Examples:
        >>> svc = ObservabilityService()
        >>> result = svc.write_event(
        ...     event_type="skill_start",
        ...     stage_name="session_bootstrap",
        ...     run_id="run_001",
        ...     project_id="proj_001",
        ... )
        >>> assert result.is_success
    """

    SDK_NAME: str = "observabilitysdk"

    def __init__(
        self,
        run_id: Optional[str] = None,
        actor: str = "system",
        event_store: Optional[EventStoreAdapter] = None,
    ) -> None:
        super().__init__(sdk_name=self.SDK_NAME)
        self._run_id = run_id or IDFactory.run_id()
        self._actor = actor
        self._store: EventStoreAdapter = event_store or InMemoryEventStore()
        self._write_blocked: bool = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_trace(
        self,
        skill_name: str,
        stage_name: str,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        actor: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> BaseResult:
        """Create a parent trace event for a skill/stage invocation.

        Args:
            skill_name: Skill identifier initiating the trace.
            stage_name: Stage in which this trace starts.
            run_id: Run identifier.
            project_id: Project identifier.
            session_id: Session identifier.
            actor: Initiating actor.
            payload: Optional trace-specific payload.

        Returns:
            :class:`BaseResult` with ``data["trace_id"]`` on success.
        """
        self._log_start("create_trace", skill_name=skill_name)
        trace_id = IDFactory.trace_id()
        event = SkillEvent(
            event_id=trace_id,
            event_type="trace_start",
            timestamp=TimeProvider.now(),
            project_id=project_id,
            run_id=run_id or self._run_id,
            session_id=session_id,
            skill_name=skill_name,
            stage_name=stage_name,
            actor=actor or self._actor,
            status="success",
            payload=payload,
        )
        result = self._write_or_block("create_trace", event)
        if result.is_success:
            result = self._build_result(
                function_name="create_trace",
                status="success",
                message=f"Trace '{trace_id}' created for skill '{skill_name}'.",
                data={"trace_id": trace_id},
                agent_hint=f"Trace started. Use trace_id={trace_id} as parent_event_id.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="trace_start",
            )
        self._log_finish("create_trace", result)
        return result

    def write_event(
        self,
        event_type: str,
        stage_name: Optional[str] = None,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        skill_name: Optional[str] = None,
        actor: Optional[str] = None,
        status: str = "success",
        parent_event_id: Optional[str] = None,
        token_usage: Optional[TokenUsage] = None,
        governance_gate_hit: bool = False,
        review_created: bool = False,
        payload: Optional[Dict[str, Any]] = None,
        error_detail: Optional[str] = None,
    ) -> BaseResult:
        """Write a single skill event to the event store (append-only).

        If the event store write fails, the service transitions to
        ``write_blocked=True`` and all subsequent calls return ``blocked``.

        Args:
            event_type: Event type identifier (from EventTypeEnum values).
            stage_name: Stage name.
            run_id: Run identifier.
            project_id: Project identifier.
            session_id: Session identifier.
            skill_name: Skill identifier.
            actor: Actor identifier.
            status: Event outcome status.
            parent_event_id: Parent trace/event ID.
            token_usage: Optional token usage metrics.
            governance_gate_hit: Whether a governance gate was triggered.
            review_created: Whether a HITL review was opened.
            payload: Event-specific payload.
            error_detail: Error details if status is failure.

        Returns:
            :class:`BaseResult` with ``data["event_id"]`` on success,
            or ``status="blocked"`` if a prior write failed.
        """
        if self._write_blocked:
            return self._build_result(
                function_name="write_event",
                status="blocked",
                message="ObservabilityService write is blocked due to a prior store failure.",
                errors=["Event store is in a failed state. No new events can be written."],
                agent_hint="Observability write is blocked. Escalate to platform operator.",
                workflow_hint="no_stage_change",
                audit_hint="escalate",
                observability_hint="observability_blocked",
            )
        event_id = IDFactory._generate("evt")
        event = SkillEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=TimeProvider.now(),
            project_id=project_id,
            run_id=run_id or self._run_id,
            session_id=session_id,
            skill_name=skill_name,
            stage_name=stage_name,
            actor=actor or self._actor,
            status=status,
            parent_event_id=parent_event_id,
            token_usage=token_usage,
            governance_gate_hit=governance_gate_hit,
            review_created=review_created,
            payload=payload,
            error_detail=error_detail,
        )
        result = self._write_or_block("write_event", event)
        if result.is_success:
            result = self._build_result(
                function_name="write_event",
                status="success",
                message=f"Event '{event_id}' ({event_type}) written.",
                data={"event_id": event_id},
                agent_hint=f"Event {event_type} recorded.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint=event_type,
            )
        self._log_finish("write_event", result)
        return result

    def query_events(
        self,
        run_id: Optional[str] = None,
        session_id: Optional[str] = None,
        event_type: Optional[str] = None,
        stage_name: Optional[str] = None,
        limit: int = 200,
    ) -> BaseResult:
        """Query stored events with optional filters.

        Args:
            run_id: Filter by run_id.
            session_id: Filter by session_id.
            event_type: Filter by event_type.
            stage_name: Filter by stage_name.
            limit: Maximum events to return.

        Returns:
            :class:`BaseResult` with ``data["events"]`` as a list of event dicts
            and ``data["count"]`` as the match count.
        """
        self._log_start("query_events")
        filters: Dict[str, Any] = {}
        if run_id:
            filters["run_id"] = run_id
        if session_id:
            filters["session_id"] = session_id
        if event_type:
            filters["event_type"] = event_type
        if stage_name:
            filters["stage_name"] = stage_name
        try:
            events = self._store.query(filters=filters or None, limit=limit)
            result = self._build_result(
                function_name="query_events",
                status="success",
                message=f"Found {len(events)} events.",
                data={
                    "events": [e.to_dict() for e in events],
                    "count": len(events),
                },
                agent_hint=f"{len(events)} events matched.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="query_events",
            )
        except Exception as exc:
            result = self._handle_exception("query_events", exc)
        self._log_finish("query_events", result)
        return result

    def replay_run(self, run_id: str) -> BaseResult:
        """Return all events for a run in chronological order.

        Args:
            run_id: Run identifier to replay.

        Returns:
            :class:`BaseResult` with ``data["events"]`` ordered chronologically.
        """
        self._log_start("replay_run", run_id=run_id)
        try:
            events = self._store.query(filters={"run_id": run_id}, limit=10000)
            events_sorted = sorted(events, key=lambda e: e.timestamp or TimeProvider.now())
            result = self._build_result(
                function_name="replay_run",
                status="success",
                message=f"Replaying {len(events_sorted)} events for run '{run_id}'.",
                data={
                    "events": [e.to_dict() for e in events_sorted],
                    "count": len(events_sorted),
                },
                agent_hint=f"Run replay: {len(events_sorted)} events in order.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="replay_run",
            )
        except Exception as exc:
            result = self._handle_exception("replay_run", exc)
        self._log_finish("replay_run", result)
        return result

    def build_event_lineage(self, leaf_event_id: str) -> BaseResult:
        """Build the lineage chain from a leaf event back to the root.

        Follows ``parent_event_id`` links to reconstruct the full chain.

        Args:
            leaf_event_id: Starting (leaf) event ID.

        Returns:
            :class:`BaseResult` with ``data["lineage"]`` containing an
            :class:`EventLineage` dict.
        """
        self._log_start("build_event_lineage", event_id=leaf_event_id)
        try:
            chain: List[str] = []
            types: List[str] = []
            current_id: Optional[str] = leaf_event_id
            visited: set = set()
            while current_id and current_id not in visited:
                visited.add(current_id)
                evt = self._store.get_by_id(current_id)
                if evt is None:
                    break
                chain.append(evt.event_id)
                types.append(evt.event_type)
                current_id = evt.parent_event_id
            chain.reverse()
            types.reverse()
            root_id = chain[0] if chain else leaf_event_id
            lineage = EventLineage(root_event_id=root_id, chain=chain, event_types=types)
            result = self._build_result(
                function_name="build_event_lineage",
                status="success",
                message=f"Lineage chain of {len(chain)} events built.",
                data={"lineage": lineage.to_dict()},
                agent_hint=f"Lineage from root={root_id} depth={len(chain)}.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="build_event_lineage",
            )
        except Exception as exc:
            result = self._handle_exception("build_event_lineage", exc)
        self._log_finish("build_event_lineage", result)
        return result

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _write_or_block(self, function_name: str, event: SkillEvent) -> BaseResult:
        """Attempt to write to the store; set blocked state on failure."""
        try:
            self._store.append(event)
            return self._build_result(
                function_name=function_name, status="success", message="ok"
            )
        except Exception as exc:
            self._write_blocked = True
            return self._build_result(
                function_name=function_name,
                status="blocked",
                message=f"Event store write failed: {exc}",
                errors=[str(exc)],
                agent_hint="Observability write failed. Service is now blocked.",
                workflow_hint="no_stage_change",
                audit_hint="escalate",
                observability_hint="write_failed",
            )
