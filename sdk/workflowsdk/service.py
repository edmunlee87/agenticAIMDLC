"""WorkflowService — the public facade for all workflow SDK operations.

All public methods return :class:`~sdk.platform_core.schemas.base_result.BaseResult`.
Internal helpers raise exceptions on error; this service catches them and wraps
them in failure results.

Composition:
    - :class:`~sdk.workflowsdk.state_store.WorkflowStateStore` — event log & state replay
    - :class:`~sdk.workflowsdk.stage_registry.StageRegistryLoader` — stage catalogue
    - :class:`~sdk.workflowsdk.stage_registry.TransitionGuard` — pre-transition checks
    - :class:`~sdk.workflowsdk.routing_engine.RoutingEngine` — success/failure routing
    - :class:`~sdk.workflowsdk.candidate.CandidateRegistry` — versioned candidates
    - :class:`~sdk.workflowsdk.selection.SelectionRegistry` — version selections
    - :class:`~sdk.workflowsdk.session.SessionManager` — UI/agent sessions
    - :class:`~sdk.workflowsdk.recovery.CheckpointManager` — state checkpoints
    - :class:`~sdk.workflowsdk.recovery.RecoveryManager` — recovery path logic
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.schemas.base_result import BaseResult
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider
from sdk.platform_core.services.base_service import BaseService
from sdk.workflowsdk.bootstrap import bootstrap_project_workflow
from sdk.workflowsdk.candidate import CandidateRegistry
from sdk.workflowsdk.models import (
    CandidateType,
    RecoveryPath,
    ReviewType,
    UIMode,
    WorkflowEvent,
    WorkflowEventType,
    WorkflowMode,
    WorkflowState,
)
from sdk.workflowsdk.recovery import CheckpointManager, RecoveryManager
from sdk.workflowsdk.routing_engine import RoutingEngine
from sdk.workflowsdk.selection import SelectionRegistry
from sdk.workflowsdk.session import SessionManager
from sdk.workflowsdk.stage_registry import StageRegistryLoader, TransitionGuard
from sdk.workflowsdk.state_store import WorkflowStateStore

_SDK_NAME = "workflowsdk"
logger = logging.getLogger(f"platform.{_SDK_NAME}")


class WorkflowService(BaseService):
    """Public facade for all workflow SDK operations.

    Args:
        bundle: Validated :class:`RuntimeConfigBundle` for this deployment.
        max_checkpoints_per_run: How many checkpoints to retain per run.
        auto_checkpoint_every: Auto-checkpoint event interval (0 = disabled).
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        max_checkpoints_per_run: int = 10,
        auto_checkpoint_every: int = 50,
    ) -> None:
        super().__init__(sdk_name=_SDK_NAME)
        self._bundle = bundle

        # Internal components (not exposed directly)
        self._store = WorkflowStateStore(
            auto_checkpoint_every=auto_checkpoint_every
        )
        self._stage_registry = StageRegistryLoader(bundle)
        self._guard = TransitionGuard(self._stage_registry)
        self._router = RoutingEngine(bundle)
        self._candidates = CandidateRegistry()
        self._selections = SelectionRegistry()
        self._sessions = SessionManager()
        self._checkpoints = CheckpointManager(
            max_checkpoints_per_run=max_checkpoints_per_run
        )
        self._recovery = RecoveryManager()

    # ------------------------------------------------------------------
    # Bootstrap
    # ------------------------------------------------------------------

    def initialize_run(
        self,
        *,
        run_id: str,
        project_id: str,
        first_stage: str,
        actor_id: str = "system",
        actor_role: str = "system",
        workflow_mode: str = WorkflowMode.DEVELOPMENT.value,
        active_domain: str = "generic",
        session_id: str = "",
        trace_id: str = "",
    ) -> BaseResult:
        """Bootstrap a new workflow run.

        Args:
            run_id: Unique run identifier.
            project_id: Owning project.
            first_stage: First MDLC stage name.
            actor_id: Bootstrapping actor.
            actor_role: Actor role.
            workflow_mode: :class:`~sdk.workflowsdk.models.WorkflowMode` value.
            active_domain: Domain pack name.
            session_id: Optional initial session.
            trace_id: Optional trace ID.

        Returns:
            :class:`BaseResult` with ``data["run_id"]`` on success.
        """
        fn = "initialize_run"
        self._log_start(fn, run_id=run_id, project_id=project_id)
        try:
            event = bootstrap_project_workflow(
                store=self._store,
                run_id=run_id,
                project_id=project_id,
                first_stage=first_stage,
                actor_id=actor_id,
                actor_role=actor_role,
                workflow_mode=workflow_mode,
                active_domain=active_domain,
                session_id=session_id,
                trace_id=trace_id,
            )
            result = self._build_result(
                fn,
                status="success",
                message=f"Run '{run_id}' initialised at stage '{first_stage}'.",
                data={
                    "run_id": run_id,
                    "project_id": project_id,
                    "first_stage": first_stage,
                    "event_id": event.event_id,
                },
                workflow_hint=f"run:{run_id} initialised",
                audit_hint="workflow.initialized event written",
                observability_hint="emit workflow.initialized trace event",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        self._log_finish(fn, result)
        return result

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def get_state(self, run_id: str, project_id: str) -> BaseResult:
        """Return the current replayed :class:`WorkflowState` for *run_id*.

        Args:
            run_id: Run to query.
            project_id: Owning project.

        Returns:
            :class:`BaseResult` with ``data["state"]`` (serialised dict) on success.
        """
        fn = "get_state"
        try:
            state = self._store.get_state(run_id, project_id)
            result = self._build_result(
                fn,
                status="success",
                message=f"State replayed for run '{run_id}' ({state.event_count} events).",
                data={"state": state.to_dict(), "event_count": state.event_count},
                workflow_hint=f"current_stage:{state.current_stage}",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def get_events(
        self,
        run_id: str,
        *,
        event_type: Optional[WorkflowEventType] = None,
        stage_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> BaseResult:
        """Return workflow events for *run_id*.

        Args:
            run_id: Run to query.
            event_type: Optional event type filter.
            stage_name: Optional stage name filter.
            limit: Maximum number of events to return.

        Returns:
            :class:`BaseResult` with ``data["events"]`` (list of dicts).
        """
        fn = "get_events"
        try:
            events = self._store.get_events(
                run_id,
                event_type=event_type,
                stage_name=stage_name,
                limit=limit,
            )
            result = self._build_result(
                fn,
                status="success",
                message=f"{len(events)} event(s) returned for run '{run_id}'.",
                data={
                    "events": [e.to_dict() for e in events],
                    "count": len(events),
                },
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    # ------------------------------------------------------------------
    # Stage transitions
    # ------------------------------------------------------------------

    def start_stage(
        self,
        *,
        run_id: str,
        project_id: str,
        stage_name: str,
        actor_id: str = "system",
        actor_role: str = "system",
        session_id: str = "",
        trace_id: str = "",
    ) -> BaseResult:
        """Emit a ``stage.started`` event for *stage_name*.

        Pre-validates the transition via :class:`~sdk.workflowsdk.stage_registry.TransitionGuard`.

        Args:
            run_id: Active run.
            project_id: Owning project.
            stage_name: Stage to start.
            actor_id: Initiating actor.
            actor_role: Actor role.
            session_id: Active session.
            trace_id: Trace ID.

        Returns:
            :class:`BaseResult` with ``data["event_id"]`` on success.
        """
        fn = "start_stage"
        try:
            state = self._store.get_state(run_id, project_id)
            selected_stages = self._selections.stages_with_active_selection()
            block_reason = self._guard.validate(
                target_stage=stage_name,
                state=state,
                selected_candidate_stages=selected_stages,
            )
            if block_reason is not None:
                event_id = IDFactory.event_id()
                block_event = WorkflowEvent(
                    event_id=event_id,
                    event_type=WorkflowEventType.STAGE_BLOCKED,
                    run_id=run_id,
                    project_id=project_id,
                    stage_name=stage_name,
                    actor_id=actor_id,
                    actor_role=actor_role,
                    session_id=session_id,
                    trace_id=trace_id,
                    timestamp=TimeProvider.now(),
                    payload={"block_reason": block_reason.value},
                )
                self._store.append_event(block_event)
                return self._build_result(
                    fn,
                    status="failure",
                    message=f"Stage '{stage_name}' blocked: {block_reason.value}.",
                    errors=[f"Transition blocked: {block_reason.value}"],
                    data={"block_reason": block_reason.value, "event_id": event_id},
                    workflow_hint=f"stage:{stage_name} blocked",
                )

            event = WorkflowEvent(
                event_id=IDFactory.event_id(),
                event_type=WorkflowEventType.STAGE_STARTED,
                run_id=run_id,
                project_id=project_id,
                stage_name=stage_name,
                actor_id=actor_id,
                actor_role=actor_role,
                session_id=session_id,
                trace_id=trace_id,
                timestamp=TimeProvider.now(),
            )
            self._store.append_event(event)
            result = self._build_result(
                fn,
                status="success",
                message=f"Stage '{stage_name}' started.",
                data={"event_id": event.event_id, "stage_name": stage_name},
                workflow_hint=f"stage:{stage_name} started",
                observability_hint="emit stage.started event",
                audit_hint="stage start audit record recommended",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def complete_stage(
        self,
        *,
        run_id: str,
        project_id: str,
        stage_name: str,
        actor_id: str = "system",
        actor_role: str = "system",
        artifact_ids: Optional[List[str]] = None,
        session_id: str = "",
        trace_id: str = "",
    ) -> BaseResult:
        """Emit a ``stage.completed`` event.

        Args:
            run_id: Active run.
            project_id: Owning project.
            stage_name: Stage to complete.
            actor_id: Completing actor.
            actor_role: Actor role.
            artifact_ids: Artifact IDs produced by this stage.
            session_id: Active session.
            trace_id: Trace ID.

        Returns:
            :class:`BaseResult` with ``data["next_stage"]`` (if routed).
        """
        fn = "complete_stage"
        try:
            event = WorkflowEvent(
                event_id=IDFactory.event_id(),
                event_type=WorkflowEventType.STAGE_COMPLETED,
                run_id=run_id,
                project_id=project_id,
                stage_name=stage_name,
                actor_id=actor_id,
                actor_role=actor_role,
                session_id=session_id,
                trace_id=trace_id,
                timestamp=TimeProvider.now(),
                payload={"artifact_ids": artifact_ids or []},
            )
            self._store.append_event(event)
            next_stage = self._router.next_stage(stage_name, "on_success")
            result = self._build_result(
                fn,
                status="success",
                message=f"Stage '{stage_name}' completed.",
                data={
                    "event_id": event.event_id,
                    "stage_name": stage_name,
                    "next_stage": next_stage,
                },
                workflow_hint=f"next_stage:{next_stage or 'terminal'}",
                audit_hint="stage completion audit record recommended",
                observability_hint="emit stage.completed event",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def fail_stage(
        self,
        *,
        run_id: str,
        project_id: str,
        stage_name: str,
        error_detail: str,
        error_type: str = "*",
        actor_id: str = "system",
        actor_role: str = "system",
        session_id: str = "",
        trace_id: str = "",
    ) -> BaseResult:
        """Emit a ``stage.failed`` event and return the recommended recovery path.

        Args:
            run_id: Active run.
            project_id: Owning project.
            stage_name: Stage that failed.
            error_detail: Human-readable error description.
            error_type: Error type code for failure route resolution.
            actor_id: Failing actor (usually ``"system"``).
            actor_role: Actor role.
            session_id: Active session.
            trace_id: Trace ID.

        Returns:
            :class:`BaseResult` with ``data["recovery_path"]`` and
            ``data["failure_target"]``.
        """
        fn = "fail_stage"
        try:
            state = self._store.get_state(run_id, project_id)
            event = WorkflowEvent(
                event_id=IDFactory.event_id(),
                event_type=WorkflowEventType.STAGE_FAILED,
                run_id=run_id,
                project_id=project_id,
                stage_name=stage_name,
                actor_id=actor_id,
                actor_role=actor_role,
                session_id=session_id,
                trace_id=trace_id,
                timestamp=TimeProvider.now(),
                payload={"error_detail": error_detail, "error_type": error_type},
            )
            self._store.append_event(event)

            recovery = self._recovery.recommend(
                state, failed_stage=stage_name, error_type=error_type
            )
            failure_target = self._router.failure_target(stage_name, error_type)
            recovery_desc = self._recovery.describe(recovery)

            result = self._build_result(
                fn,
                status="failure",
                message=f"Stage '{stage_name}' failed: {error_detail}",
                errors=[error_detail],
                data={
                    "event_id": event.event_id,
                    "stage_name": stage_name,
                    "recovery_path": recovery.value,
                    "recovery_description": recovery_desc,
                    "failure_target": failure_target,
                },
                workflow_hint=f"recovery:{recovery.value}",
                audit_hint="stage failure audit record required",
                observability_hint="emit stage.failed event",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    # ------------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------------

    def resolve_next_stage(
        self, stage_name: str, outcome: str = "on_success"
    ) -> BaseResult:
        """Return the next stage for *stage_name* given *outcome*.

        Args:
            stage_name: Current stage.
            outcome: Transition outcome key.

        Returns:
            :class:`BaseResult` with ``data["next_stage"]``.
        """
        fn = "resolve_next_stage"
        try:
            next_stage = self._router.next_stage(stage_name, outcome)
            result = self._build_result(
                fn,
                status="success",
                message=(
                    f"Next stage for '{stage_name}' ({outcome}): "
                    f"{next_stage or 'terminal'}."
                ),
                data={"next_stage": next_stage, "outcome": outcome},
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    # ------------------------------------------------------------------
    # Candidate management
    # ------------------------------------------------------------------

    def register_candidate(
        self,
        *,
        stage_name: str,
        candidate_type: CandidateType,
        run_id: str,
        project_id: str,
        version_label: str = "",
        summary: str = "",
        created_by: str = "",
        artifact_ids: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> BaseResult:
        """Register a new versioned candidate.

        Args:
            stage_name: Producing MDLC stage.
            candidate_type: :class:`~sdk.workflowsdk.models.CandidateType`.
            run_id: Active run.
            project_id: Owning project.
            version_label: Human-readable label.
            summary: HITL UI summary.
            created_by: Actor ID.
            artifact_ids: Related artifact IDs.
            metrics: KPI dict.
            metadata: Arbitrary metadata.

        Returns:
            :class:`BaseResult` with ``data["candidate_id"]``.
        """
        fn = "register_candidate"
        try:
            version = self._candidates.register(
                stage_name=stage_name,
                candidate_type=candidate_type,
                run_id=run_id,
                project_id=project_id,
                version_label=version_label,
                summary=summary,
                created_by=created_by,
                artifact_ids=artifact_ids,
                metrics=metrics,
                metadata=metadata,
            )
            event = WorkflowEvent(
                event_id=IDFactory.event_id(),
                event_type=WorkflowEventType.CANDIDATE_REGISTERED,
                run_id=run_id,
                project_id=project_id,
                stage_name=stage_name,
                actor_id=created_by or "system",
                timestamp=TimeProvider.now(),
                payload={
                    "candidate_id": version.candidate_id,
                    "candidate_type": version.candidate_type.value,
                    "version_label": version_label,
                },
            )
            self._store.append_event(event)
            result = self._build_result(
                fn,
                status="success",
                message=f"Candidate '{version.candidate_id}' registered for stage '{stage_name}'.",
                data={
                    "candidate_id": version.candidate_id,
                    "stage_name": stage_name,
                    "event_id": event.event_id,
                },
                workflow_hint=f"candidate:{version.candidate_id} pending_review",
                observability_hint="emit candidate.registered event",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def record_selection(
        self,
        *,
        stage_name: str,
        run_id: str,
        project_id: str,
        candidate_id: str,
        selected_by: str,
        rationale: str = "",
        audit_id: str = "",
        review_type: ReviewType = ReviewType.GENERIC,
        conditions: Optional[List[str]] = None,
    ) -> BaseResult:
        """Record a HITL version selection and emit a ``candidate.selected`` event.

        Args:
            stage_name: Stage the selection applies to.
            run_id: Active run.
            project_id: Owning project.
            candidate_id: Selected candidate ID.
            selected_by: Actor making the selection.
            rationale: Decision rationale.
            audit_id: Linked audit record ID.
            review_type: Review context type.
            conditions: Approval conditions.

        Returns:
            :class:`BaseResult` with ``data["selection_id"]``.
        """
        fn = "record_selection"
        try:
            # Mark candidate as selected in candidate registry
            self._candidates.mark_selected(candidate_id)

            selection = self._selections.record_selection(
                stage_name=stage_name,
                run_id=run_id,
                project_id=project_id,
                selected_candidate_id=candidate_id,
                selected_by=selected_by,
                rationale=rationale,
                audit_id=audit_id,
                review_type=review_type,
                conditions=conditions,
            )
            event = WorkflowEvent(
                event_id=IDFactory.event_id(),
                event_type=WorkflowEventType.CANDIDATE_SELECTED,
                run_id=run_id,
                project_id=project_id,
                stage_name=stage_name,
                actor_id=selected_by,
                timestamp=TimeProvider.now(),
                payload={
                    "candidate_id": candidate_id,
                    "selection_id": selection.selection_id,
                    "review_type": review_type.value,
                    "rationale": rationale,
                },
            )
            self._store.append_event(event)
            result = self._build_result(
                fn,
                status="success",
                message=f"Candidate '{candidate_id}' selected for stage '{stage_name}'.",
                data={
                    "selection_id": selection.selection_id,
                    "candidate_id": candidate_id,
                    "stage_name": stage_name,
                    "event_id": event.event_id,
                },
                workflow_hint=f"selection:{selection.selection_id} active",
                audit_hint="selection audit record recommended",
                observability_hint="emit candidate.selected event",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def create_session(
        self,
        *,
        run_id: str,
        project_id: str,
        created_by: str = "",
        ui_mode: UIMode = UIMode.IDLE,
        last_stage: str = "",
    ) -> BaseResult:
        """Create a new UI/agent session.

        Args:
            run_id: Associated run.
            project_id: Owning project.
            created_by: Actor creating the session.
            ui_mode: Initial UI mode.
            last_stage: Stage active when the session starts.

        Returns:
            :class:`BaseResult` with ``data["session_id"]``.
        """
        fn = "create_session"
        try:
            session = self._sessions.create(
                run_id=run_id,
                project_id=project_id,
                created_by=created_by,
                ui_mode=ui_mode,
                last_stage=last_stage,
            )
            event = WorkflowEvent(
                event_id=IDFactory.event_id(),
                event_type=WorkflowEventType.SESSION_CREATED,
                run_id=run_id,
                project_id=project_id,
                stage_name=last_stage or "bootstrap",
                actor_id=created_by or "system",
                session_id=session.session_id,
                timestamp=TimeProvider.now(),
                payload={
                    "session_id": session.session_id,
                    "ui_mode": ui_mode.value,
                },
            )
            self._store.append_event(event)
            result = self._build_result(
                fn,
                status="success",
                message=f"Session '{session.session_id}' created for run '{run_id}'.",
                data={
                    "session_id": session.session_id,
                    "run_id": run_id,
                    "event_id": event.event_id,
                },
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def close_session(self, session_id: str) -> BaseResult:
        """Close *session_id*.

        Args:
            session_id: Session to close.

        Returns:
            :class:`BaseResult` with ``data["session_id"]``.
        """
        fn = "close_session"
        try:
            session = self._sessions.get(session_id)
            self._sessions.close(session_id)
            event = WorkflowEvent(
                event_id=IDFactory.event_id(),
                event_type=WorkflowEventType.SESSION_CLOSED,
                run_id=session.run_id,
                project_id=session.project_id,
                stage_name=session.last_stage or "bootstrap",
                session_id=session_id,
                timestamp=TimeProvider.now(),
                payload={"session_id": session_id},
            )
            self._store.append_event(event)
            result = self._build_result(
                fn,
                status="success",
                message=f"Session '{session_id}' closed.",
                data={"session_id": session_id, "event_id": event.event_id},
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    # ------------------------------------------------------------------
    # Checkpoint / Recovery
    # ------------------------------------------------------------------

    def save_checkpoint(
        self, run_id: str, project_id: str, session_id: str = ""
    ) -> BaseResult:
        """Snapshot the current workflow state.

        Args:
            run_id: Run to checkpoint.
            project_id: Owning project.
            session_id: Active session.

        Returns:
            :class:`BaseResult` with ``data["checkpoint_id"]``.
        """
        fn = "save_checkpoint"
        try:
            state = self._store.get_state(run_id, project_id)
            record = self._checkpoints.save(state, session_id=session_id)
            event = WorkflowEvent(
                event_id=IDFactory.event_id(),
                event_type=WorkflowEventType.CHECKPOINT_SAVED,
                run_id=run_id,
                project_id=project_id,
                stage_name=state.current_stage or "bootstrap",
                session_id=session_id,
                timestamp=TimeProvider.now(),
                payload={
                    "checkpoint_id": record.checkpoint_id,
                    "event_count": state.event_count,
                },
            )
            self._store.append_event(event)
            result = self._build_result(
                fn,
                status="success",
                message=f"Checkpoint '{record.checkpoint_id}' saved for run '{run_id}'.",
                data={
                    "checkpoint_id": record.checkpoint_id,
                    "event_id": event.event_id,
                    "event_count": state.event_count,
                },
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def recommend_recovery(
        self,
        run_id: str,
        project_id: str,
        failed_stage: str,
        error_type: str = "*",
    ) -> BaseResult:
        """Analyse the current state and recommend a recovery path.

        Args:
            run_id: Run in failure.
            project_id: Owning project.
            failed_stage: Stage that failed.
            error_type: Error type code.

        Returns:
            :class:`BaseResult` with ``data["recovery_path"]``.
        """
        fn = "recommend_recovery"
        try:
            state = self._store.get_state(run_id, project_id)
            path = self._recovery.recommend(
                state, failed_stage=failed_stage, error_type=error_type
            )
            desc = self._recovery.describe(path)
            failure_target = self._router.failure_target(failed_stage, error_type)
            latest_chk = self._checkpoints.latest_valid(run_id)
            result = self._build_result(
                fn,
                status="success",
                message=f"Recovery recommendation: {path.value} — {desc}",
                data={
                    "recovery_path": path.value,
                    "recovery_description": desc,
                    "failure_target": failure_target,
                    "latest_checkpoint_id": (
                        latest_chk.checkpoint_id if latest_chk else None
                    ),
                },
                workflow_hint=f"recovery:{path.value}",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    # ------------------------------------------------------------------
    # Stage registry queries
    # ------------------------------------------------------------------

    def list_stages(self) -> BaseResult:
        """Return all registered stage names.

        Returns:
            :class:`BaseResult` with ``data["stages"]``.
        """
        fn = "list_stages"
        try:
            stages = self._stage_registry.all_stage_names()
            result = self._build_result(
                fn,
                status="success",
                message=f"{len(stages)} stage(s) registered.",
                data={"stages": stages, "count": len(stages)},
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def get_stage_definition(self, stage_name: str) -> BaseResult:
        """Return the :class:`~sdk.platform_core.runtime.config_models.stages.StageDefinition`
        for *stage_name*.

        Args:
            stage_name: Stage to look up.

        Returns:
            :class:`BaseResult` with ``data["stage"]`` (dict).
        """
        fn = "get_stage_definition"
        try:
            defn = self._stage_registry.get(stage_name)
            result = self._build_result(
                fn,
                status="success",
                message=f"Stage definition found: '{stage_name}'.",
                data={"stage": defn.model_dump()},
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result
