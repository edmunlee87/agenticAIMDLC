"""Workflow state store — event-sourced, append-only.

:class:`WorkflowStateStore` is the single source of truth for workflow
events.  State is always derived by replaying the event log via
:func:`_replay` — no in-place mutation.

Design contract:
    - Helper class returns plain Python objects or raises on error.
    - The main :class:`~sdk.workflowsdk.service.WorkflowService` is
      responsible for wrapping all results in :class:`BaseResult`.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from sdk.platform_core.schemas.enums import StageStatusEnum
from sdk.workflowsdk.models import (
    BlockReason,
    GovernanceFlags,
    InteractionMode,
    SessionStatus,
    StageRecord,
    UIMode,
    WorkflowEvent,
    WorkflowEventType,
    WorkflowMode,
    WorkflowState,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Replay logic
# ---------------------------------------------------------------------------


def _replay(events: List[WorkflowEvent], run_id: str, project_id: str) -> WorkflowState:
    """Rebuild :class:`WorkflowState` by replaying *events* in order.

    Args:
        events: Ordered list of :class:`WorkflowEvent` entries for the run.
        run_id: Run identifier.
        project_id: Owning project identifier.

    Returns:
        A freshly reconstructed :class:`WorkflowState`.
    """
    current_stage: str = ""
    stages: Dict[str, StageRecord] = {}
    workflow_mode: WorkflowMode = WorkflowMode.DEVELOPMENT
    active_domain: str = "generic"
    ui_mode: UIMode = UIMode.IDLE
    interaction_mode: InteractionMode = InteractionMode.NONE
    session_id: str = ""
    governance_flags: GovernanceFlags = GovernanceFlags()
    last_event_id: str = ""

    for ev in events:
        last_event_id = ev.event_id

        if ev.event_type == WorkflowEventType.WORKFLOW_INITIALIZED:
            workflow_mode = WorkflowMode(ev.payload.get("workflow_mode", WorkflowMode.DEVELOPMENT.value))
            active_domain = ev.payload.get("active_domain", "generic")
            current_stage = ev.stage_name
            ui_mode = UIMode.BOOTSTRAP

        elif ev.event_type == WorkflowEventType.STAGE_STARTED:
            current_stage = ev.stage_name
            existing = stages.get(ev.stage_name)
            attempt = (existing.attempt_count + 1) if existing else 1
            stages[ev.stage_name] = StageRecord(
                stage_name=ev.stage_name,
                status=StageStatusEnum.RUNNING,
                started_at=ev.timestamp,
                attempt_count=attempt,
            )
            ui_mode = UIMode.STAGE_PROGRESS

        elif ev.event_type == WorkflowEventType.STAGE_COMPLETED:
            existing = stages.get(ev.stage_name, StageRecord(stage_name=ev.stage_name))
            artifact_ids = ev.payload.get("artifact_ids", existing.artifact_ids)
            stages[ev.stage_name] = StageRecord(
                stage_name=existing.stage_name,
                status=StageStatusEnum.COMPLETED,
                started_at=existing.started_at,
                completed_at=ev.timestamp,
                attempt_count=existing.attempt_count,
                artifact_ids=artifact_ids,
                selected_candidate_id=existing.selected_candidate_id,
            )
            interaction_mode = InteractionMode.NONE
            ui_mode = UIMode.IDLE

        elif ev.event_type == WorkflowEventType.STAGE_FAILED:
            existing = stages.get(ev.stage_name, StageRecord(stage_name=ev.stage_name))
            stages[ev.stage_name] = StageRecord(
                stage_name=existing.stage_name,
                status=StageStatusEnum.FAILED,
                started_at=existing.started_at,
                failed_at=ev.timestamp,
                attempt_count=existing.attempt_count,
                error_detail=ev.payload.get("error_detail", ""),
            )
            interaction_mode = InteractionMode.RECOVERY_REQUIRED
            ui_mode = UIMode.RECOVERY_PROMPT

        elif ev.event_type == WorkflowEventType.STAGE_BLOCKED:
            existing = stages.get(ev.stage_name, StageRecord(stage_name=ev.stage_name))
            raw_reason = ev.payload.get("block_reason", BlockReason.INVALID_TRANSITION.value)
            block_reason = BlockReason(raw_reason)
            if block_reason == BlockReason.REVIEW_PENDING:
                blocked_status = StageStatusEnum.WAITING_REVIEW
                ui_mode = UIMode.REVIEW_3PANEL
                interaction_mode = InteractionMode.REVIEW_REQUIRED
            elif block_reason == BlockReason.SELECTION_MISSING:
                blocked_status = StageStatusEnum.WAITING_SELECTION
                ui_mode = UIMode.SELECTION_CARDS
                interaction_mode = InteractionMode.SELECTION_REQUIRED
            else:
                blocked_status = StageStatusEnum.BLOCKED
            stages[ev.stage_name] = StageRecord(
                stage_name=existing.stage_name,
                status=blocked_status,
                started_at=existing.started_at,
                attempt_count=existing.attempt_count,
                block_reason=block_reason,
            )

        elif ev.event_type == WorkflowEventType.STAGE_SKIPPED:
            stages[ev.stage_name] = StageRecord(
                stage_name=ev.stage_name,
                status=StageStatusEnum.SKIPPED,
                completed_at=ev.timestamp,
            )

        elif ev.event_type == WorkflowEventType.REVIEW_OPENED:
            existing = stages.get(ev.stage_name, StageRecord(stage_name=ev.stage_name))
            stages[ev.stage_name] = StageRecord(
                stage_name=existing.stage_name,
                status=existing.status,
                started_at=existing.started_at,
                attempt_count=existing.attempt_count,
                review_id=ev.payload.get("review_id", ""),
                selected_candidate_id=existing.selected_candidate_id,
                artifact_ids=existing.artifact_ids,
            )
            ui_mode = UIMode.REVIEW_3PANEL
            interaction_mode = InteractionMode.REVIEW_REQUIRED

        elif ev.event_type == WorkflowEventType.REVIEW_CLOSED:
            existing = stages.get(ev.stage_name, StageRecord(stage_name=ev.stage_name))
            stages[ev.stage_name] = StageRecord(
                stage_name=existing.stage_name,
                status=existing.status,
                started_at=existing.started_at,
                attempt_count=existing.attempt_count,
                review_id="",
                selected_candidate_id=existing.selected_candidate_id,
                artifact_ids=existing.artifact_ids,
            )
            interaction_mode = InteractionMode.NONE

        elif ev.event_type == WorkflowEventType.CANDIDATE_SELECTED:
            existing = stages.get(ev.stage_name, StageRecord(stage_name=ev.stage_name))
            stages[ev.stage_name] = StageRecord(
                stage_name=existing.stage_name,
                status=existing.status,
                started_at=existing.started_at,
                attempt_count=existing.attempt_count,
                review_id=existing.review_id,
                selected_candidate_id=ev.payload.get("candidate_id", ""),
                artifact_ids=existing.artifact_ids,
            )
            ui_mode = UIMode.STAGE_PROGRESS
            interaction_mode = InteractionMode.NONE

        elif ev.event_type in (
            WorkflowEventType.SESSION_CREATED,
            WorkflowEventType.SESSION_RESUMED,
        ):
            session_id = ev.payload.get("session_id", session_id)

        elif ev.event_type == WorkflowEventType.SESSION_CLOSED:
            session_id = ""

        elif ev.event_type == WorkflowEventType.RECOVERY_STARTED:
            ui_mode = UIMode.RECOVERY_PROMPT
            interaction_mode = InteractionMode.RECOVERY_REQUIRED

        elif ev.event_type == WorkflowEventType.RECOVERY_COMPLETED:
            ui_mode = UIMode.IDLE
            interaction_mode = InteractionMode.NONE

        elif ev.event_type == WorkflowEventType.METADATA_UPDATED:
            active_domain = ev.payload.get("active_domain", active_domain)
            raw_flags = ev.payload.get("governance_flags")
            if raw_flags:
                governance_flags = GovernanceFlags(**raw_flags)

    return WorkflowState(
        run_id=run_id,
        project_id=project_id,
        workflow_mode=workflow_mode,
        active_domain=active_domain,
        current_stage=current_stage,
        stages=stages,
        governance_flags=governance_flags,
        ui_mode=ui_mode,
        interaction_mode=interaction_mode,
        event_count=len(events),
        last_event_id=last_event_id,
        session_id=session_id,
    )


# ---------------------------------------------------------------------------
# WorkflowStateStore
# ---------------------------------------------------------------------------


class WorkflowStateStore:
    """Append-only, in-memory event log per run.

    All public methods return plain Python values or raise on error.  The
    :class:`~sdk.workflowsdk.service.WorkflowService` wraps the calls in
    :class:`~sdk.platform_core.base_classes.base.BaseResult`.

    Args:
        auto_checkpoint_every: If > 0, a snapshot hint is emitted every N
            events (logging only; the actual snapshot is taken by
            :class:`~sdk.workflowsdk.recovery.CheckpointManager`).
    """

    def __init__(self, auto_checkpoint_every: int = 50) -> None:
        self._auto_checkpoint_every = auto_checkpoint_every
        # run_id -> ordered list of events
        self._log: Dict[str, List[WorkflowEvent]] = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_run(self, run_id: str) -> List[WorkflowEvent]:
        """Return the event log for *run_id*, initialising if absent."""
        if run_id not in self._log:
            self._log[run_id] = []
        return self._log[run_id]

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def append_event(self, event: WorkflowEvent) -> WorkflowEvent:
        """Append *event* to the log.

        Args:
            event: A fully constructed :class:`WorkflowEvent`.

        Returns:
            The appended event (same object).

        Raises:
            ValueError: If ``event_id`` is already present in the log for
                this run (duplicate detection).
        """
        log = self._ensure_run(event.run_id)

        if any(e.event_id == event.event_id for e in log):
            raise ValueError(
                f"Duplicate event_id '{event.event_id}' for run '{event.run_id}'."
            )

        log.append(event)
        count = len(log)

        if (
            self._auto_checkpoint_every > 0
            and count % self._auto_checkpoint_every == 0
        ):
            logger.debug(
                "Auto-checkpoint hint: run_id=%s event_count=%d",
                event.run_id,
                count,
            )

        logger.debug(
            "Event appended: run_id=%s event_id=%s type=%s stage=%s",
            event.run_id,
            event.event_id,
            event.event_type.value,
            event.stage_name,
        )
        return event

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_events(
        self,
        run_id: str,
        *,
        event_type: Optional[WorkflowEventType] = None,
        stage_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[WorkflowEvent]:
        """Return events for *run_id*, with optional filters.

        Args:
            run_id: Run to query.
            event_type: Filter to this event type.
            stage_name: Filter to this stage.
            limit: Maximum number of events to return (most-recent first if
                specified).

        Returns:
            Filtered, ordered event list.

        Raises:
            KeyError: If *run_id* has no events.
        """
        if run_id not in self._log:
            raise KeyError(f"No event log found for run_id '{run_id}'.")

        events: List[WorkflowEvent] = list(self._log[run_id])

        if event_type is not None:
            events = [e for e in events if e.event_type == event_type]
        if stage_name is not None:
            events = [e for e in events if e.stage_name == stage_name]
        if limit is not None:
            events = events[-limit:]

        return events

    def get_state(self, run_id: str, project_id: str) -> WorkflowState:
        """Replay the event log and return the current :class:`WorkflowState`.

        Args:
            run_id: Run identifier.
            project_id: Owning project.

        Returns:
            Rebuilt :class:`WorkflowState`.

        Raises:
            KeyError: If *run_id* has no event log.
        """
        if run_id not in self._log:
            raise KeyError(f"No event log found for run_id '{run_id}'.")
        return _replay(self._log[run_id], run_id, project_id)

    def has_run(self, run_id: str) -> bool:
        """Return ``True`` if *run_id* has been initialised in the store."""
        return run_id in self._log

    def event_count(self, run_id: str) -> int:
        """Return the total number of events for *run_id*.

        Args:
            run_id: Run identifier.

        Returns:
            Integer event count (0 if run not found).
        """
        return len(self._log.get(run_id, []))

    def list_runs(self) -> List[str]:
        """Return all run IDs present in the store."""
        return list(self._log.keys())
