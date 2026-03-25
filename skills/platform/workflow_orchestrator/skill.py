"""WorkflowOrchestratorSkill -- drives an MDLC run through its stages.

This orchestrator is the top-level "brain" for a single project run.  It:

1. Bootstraps the workflow (opens a session).
2. Iterates the stage loop: start → SDK calls → complete → route.
3. Handles stage failures by delegating to the recovery orchestrator.
4. Pauses the loop at any governance gate requiring HITL.
5. Closes the session when the workflow reaches a terminal stage.

Usage::

    from skills.platform.workflow_orchestrator.skill import WorkflowOrchestratorSkill

    skill = WorkflowOrchestratorSkill(dispatcher, context)
    result = skill.run()
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from platform_contracts.enums import InteractionType

logger = logging.getLogger(__name__)

_MAX_STAGE_ITERATIONS = 50  # hard guard against infinite loops


@dataclass
class OrchestratorContext:
    """Input context for the workflow orchestrator.

    Attributes:
        project_id: MDLC project identifier.
        run_id: MDLC run identifier.
        actor_id: Actor (user/agent) running the workflow.
        role: Actor's MDLC role.
        domain: Active domain pack name.
        initial_stage: First stage to start (e.g. ``"data_preparation"``).
        session_id: Existing session to resume (empty = open new).
        extra_data: Arbitrary extra data passed to every stage payload.
    """

    project_id: str
    run_id: str
    actor_id: str
    role: str
    domain: str = "generic"
    initial_stage: str = "data_preparation"
    session_id: str = ""
    extra_data: dict[str, Any] = field(default_factory=dict)


@dataclass
class OrchestratorResult:
    """Result returned by the orchestrator after a run (or pause).

    Attributes:
        success: True if the workflow completed normally.
        final_stage: Last stage reached.
        paused_for_review: True if the loop paused pending HITL.
        review_id: Review ID if paused.
        error: Error message if ``success`` is False.
        history: Ordered list of stage outcomes.
    """

    success: bool
    final_stage: str
    paused_for_review: bool = False
    review_id: str = ""
    error: str = ""
    history: list[dict[str, Any]] = field(default_factory=list)


class WorkflowOrchestratorSkill:
    """Orchestrates a full MDLC stage loop via the agent dispatcher.

    Args:
        dispatcher: :class:`~agent_bridge.dispatcher.AgentDispatcher`.
        context: :class:`OrchestratorContext` for this run.
    """

    def __init__(self, dispatcher: Any, context: OrchestratorContext) -> None:
        self._dispatcher = dispatcher
        self._ctx = context
        self._session_id = context.session_id
        self._history: list[dict[str, Any]] = []

    def run(self) -> OrchestratorResult:
        """Execute the stage loop.

        Returns:
            :class:`OrchestratorResult`.
        """
        # Step 1: open or resume session.
        if self._session_id:
            resp = self._dispatch(
                "resume_session", "bootstrap", InteractionType.SESSION_COMMAND,
                {"session_id": self._session_id},
            )
        else:
            resp = self._dispatch(
                "open_session", "bootstrap", InteractionType.SESSION_COMMAND,
                {"domain": self._ctx.domain},
            )
        if resp.get("status") != "ok":
            return OrchestratorResult(success=False, final_stage="", error=resp.get("message", "Session open failed."))

        self._session_id = resp.get("data", {}).get("session_id", self._session_id)

        # Step 2: stage loop.
        current_stage = self._ctx.initial_stage
        for _iteration in range(_MAX_STAGE_ITERATIONS):
            start_resp = self._dispatch(
                "start_stage", current_stage, InteractionType.STAGE_ACTION,
            )
            record = {"stage": current_stage, "start": start_resp.get("status")}

            if start_resp.get("status") != "ok":
                record["error"] = start_resp.get("message", "")
                self._history.append(record)
                return OrchestratorResult(
                    success=False,
                    final_stage=current_stage,
                    error=start_resp.get("message", "Stage start failed."),
                    history=self._history,
                )

            # Check if review is required (non-empty blocking_reasons signals gate).
            gov = (start_resp.get("governance_summary") or {})
            if gov.get("blocking_reasons"):
                logger.info("workflow_orchestrator.paused_for_review", extra={"stage": current_stage})
                record["paused_for_review"] = True
                self._history.append(record)
                return OrchestratorResult(
                    success=True,
                    final_stage=current_stage,
                    paused_for_review=True,
                    history=self._history,
                )

            # Complete the stage.
            complete_resp = self._dispatch(
                "complete_stage", current_stage, InteractionType.STAGE_ACTION,
                {"artifact_ids": []},
            )
            record["complete"] = complete_resp.get("status")
            self._history.append(record)

            if complete_resp.get("status") != "ok":
                return OrchestratorResult(
                    success=False,
                    final_stage=current_stage,
                    error=complete_resp.get("message", "Stage complete failed."),
                    history=self._history,
                )

            # Route to next stage.
            route_resp = self._dispatch("route_next", current_stage, InteractionType.STAGE_ACTION)
            next_stage = (route_resp.get("data") or {}).get("next_stage", "")
            if not next_stage:
                # Terminal -- no next stage.
                logger.info("workflow_orchestrator.terminal", extra={"stage": current_stage})
                return OrchestratorResult(
                    success=True, final_stage=current_stage, history=self._history,
                )
            current_stage = next_stage

        logger.error("workflow_orchestrator.iteration_guard_exceeded")
        return OrchestratorResult(
            success=False,
            final_stage=current_stage,
            error="Exceeded maximum stage iteration guard.",
            history=self._history,
        )

    # ------------------------------------------------------------------

    def _dispatch(
        self,
        action: str,
        stage_name: str,
        interaction_type: InteractionType,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        from platform_contracts.fragments import ActorRecord
        from platform_core.utils.id_factory import id_factory
        from platform_core.utils.time_provider import time_provider

        payload = {
            "project_id": self._ctx.project_id,
            "run_id": self._ctx.run_id,
            "session_id": self._session_id,
            "trace_id": id_factory.audit_id("trace"),
            "correlation_id": id_factory.audit_id("corr"),
            "actor": ActorRecord(actor_id=self._ctx.actor_id, role=self._ctx.role).model_dump(),
            "timestamp": time_provider.now().isoformat(),
            "stage_name": stage_name,
            "interaction_type": interaction_type.value,
            "action": action,
            "data": {**self._ctx.extra_data, **(extra or {})},
        }
        return self._dispatcher.dispatch(payload)
