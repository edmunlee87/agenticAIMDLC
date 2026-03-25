"""ObservabilityService -- append-only event store with trace support.

All platform actions that emit an :class:`~observabilitysdk.models.ObservabilityEvent`
go through this service. The store is append-only by design: events are never
updated or deleted. Querying is index-assisted (by run_id, trace_id, stage).
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

from platform_contracts.results import BaseResult, ResultFactory
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.services.base import BaseService
from platform_core.utils.id_factory import IDFactory, id_factory
from platform_core.utils.time_provider import TimeProvider, time_provider

from observabilitysdk.models import EventCategory, EventSeverity, ObservabilityEvent, TraceContext

logger = logging.getLogger(__name__)


class ObservabilityService(BaseService):
    """Append-only event store for MDLC platform observability.

    Maintains in-memory indexes (by run_id, trace_id, stage_name) for fast
    retrieval. Swap ``_store`` for a durable backing (e.g. SQLite, Kafka)
    without changing the public interface.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        id_factory_: Injectable :class:`IDFactory`.
        time_provider_: Injectable :class:`TimeProvider`.
        max_events: In-memory cap. Events beyond this limit are dropped from
            the tail. 0 = unlimited. Default: 100_000.
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        id_factory_: IDFactory | None = None,
        time_provider_: TimeProvider | None = None,
        max_events: int = 100_000,
    ) -> None:
        super().__init__(bundle=bundle, id_factory_=id_factory_, time_provider_=time_provider_)
        self._store: list[ObservabilityEvent] = []
        self._max_events = max_events
        # Indexes: run_id -> [event_ids], trace_id -> [event_ids], stage -> [event_ids]
        self._idx_run: dict[str, list[str]] = defaultdict(list)
        self._idx_trace: dict[str, list[str]] = defaultdict(list)
        self._idx_stage: dict[str, list[str]] = defaultdict(list)
        self._idx_id: dict[str, ObservabilityEvent] = {}

    # ------------------------------------------------------------------
    # Write API
    # ------------------------------------------------------------------

    def emit(self, event: ObservabilityEvent) -> BaseResult[str]:
        """Append an event to the store.

        Args:
            event: The event to append.

        Returns:
            :class:`BaseResult` containing the ``event_id``.
        """
        if event.event_id in self._idx_id:
            return ResultFactory.fail(
                "ERR_EVENT_DUPLICATE",
                f"Event '{event.event_id}' already exists (append-only store).",
            )
        if self._max_events and len(self._store) >= self._max_events:
            # Drop the oldest event to stay within the cap.
            oldest = self._store.pop(0)
            self._idx_id.pop(oldest.event_id, None)

        self._store.append(event)
        self._idx_id[event.event_id] = event
        if event.run_id:
            self._idx_run[event.run_id].append(event.event_id)
        if event.trace_id:
            self._idx_trace[event.trace_id].append(event.event_id)
        if event.stage_name:
            self._idx_stage[event.stage_name].append(event.event_id)

        self._logger.debug(
            "observability.event_emitted",
            extra={
                "event_id": event.event_id,
                "event_type": event.event_type,
                "run_id": event.run_id,
                "severity": event.severity,
            },
        )
        return ResultFactory.ok(event.event_id)

    def emit_simple(
        self,
        event_type: str,
        message: str,
        run_id: str = "",
        session_id: str = "",
        project_id: str = "",
        stage_name: str = "",
        trace_id: str = "",
        actor_id: str = "",
        actor_role: str = "",
        category: EventCategory = EventCategory.SYSTEM,
        severity: EventSeverity = EventSeverity.INFO,
        data: dict[str, Any] | None = None,
        duration_ms: float | None = None,
    ) -> BaseResult[str]:
        """Convenience builder: create and emit an event with named parameters.

        Args:
            event_type: Dot-namespaced event type.
            message: Human-readable summary.
            run_id: Associated run ID.
            session_id: Associated session ID.
            project_id: Associated project ID.
            stage_name: Active MDLC stage.
            trace_id: Distributed trace ID.
            actor_id: Actor identifier.
            actor_role: Actor role.
            category: Event category.
            severity: Event severity.
            data: Structured payload dict.
            duration_ms: Operation duration in milliseconds.

        Returns:
            :class:`BaseResult` containing the generated ``event_id``.
        """
        event = ObservabilityEvent(
            event_id=self._id_factory.audit_id(),
            event_type=event_type,
            category=category,
            severity=severity,
            timestamp=self._time_provider.now(),
            project_id=project_id,
            run_id=run_id,
            session_id=session_id,
            stage_name=stage_name,
            trace_id=trace_id,
            actor_id=actor_id,
            actor_role=actor_role,
            message=message,
            data=data or {},
            duration_ms=duration_ms,
        )
        return self.emit(event)

    # ------------------------------------------------------------------
    # Query API
    # ------------------------------------------------------------------

    def get_event(self, event_id: str) -> BaseResult[ObservabilityEvent]:
        """Retrieve a single event by ID."""
        event = self._idx_id.get(event_id)
        if event is None:
            return ResultFactory.fail("ERR_EVENT_NOT_FOUND", f"Event '{event_id}' not found.")
        return ResultFactory.ok(event)

    def get_events_for_run(
        self,
        run_id: str,
        category: EventCategory | None = None,
        severity: EventSeverity | None = None,
        limit: int = 500,
    ) -> BaseResult[list[ObservabilityEvent]]:
        """Return events for a run, optionally filtered.

        Args:
            run_id: Run identifier.
            category: Filter by category.
            severity: Filter by severity.
            limit: Maximum number of events to return. Default: 500.

        Returns:
            :class:`BaseResult` containing the event list (chronological order).
        """
        ids = self._idx_run.get(run_id, [])
        events = [self._idx_id[eid] for eid in ids if eid in self._idx_id]
        if category:
            events = [e for e in events if e.category == category]
        if severity:
            events = [e for e in events if e.severity == severity]
        return ResultFactory.ok(events[:limit])

    def get_events_for_trace(self, trace_id: str) -> BaseResult[list[ObservabilityEvent]]:
        """Return all events in a distributed trace."""
        ids = self._idx_trace.get(trace_id, [])
        events = [self._idx_id[eid] for eid in ids if eid in self._idx_id]
        return ResultFactory.ok(events)

    def count(self) -> int:
        """Return total number of stored events."""
        return len(self._store)

    def health_check(self) -> BaseResult[dict[str, Any]]:
        """Return store health statistics."""
        return ResultFactory.ok({
            "status": "ok",
            "total_events": len(self._store),
            "indexed_runs": len(self._idx_run),
            "indexed_traces": len(self._idx_trace),
        })
