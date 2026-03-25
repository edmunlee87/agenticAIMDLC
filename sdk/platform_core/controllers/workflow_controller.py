"""WorkflowController — stage progression and workflow routing.

Handles :class:`InteractionPayload` with actions:
- ``run_stage``: start a stage and run pre-stage checks.
- ``complete_stage``: mark the current stage as complete.
- ``fail_stage``: mark the current stage as failed.
- ``route_next``: resolve and transition to the next stage.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from sdk.platform_core.controllers.base import BaseController
from sdk.platform_core.runtime.resolvers.runtime_resolver import RuntimeResolver
from sdk.platform_core.schemas.payload_models import (
    InteractionPayload,
    StandardResponseEnvelope,
)


class WorkflowController(BaseController):
    """Controller for stage lifecycle and workflow routing.

    Args:
        workflow_service: :class:`~workflowsdk.service.WorkflowService`.
        resolver: Pre-built :class:`RuntimeResolver`.
        dependencies: Optional :class:`DependencyContainer`.
        logger: Optional logger override.
    """

    def __init__(
        self,
        workflow_service: Any,
        resolver: Optional[RuntimeResolver] = None,
        dependencies: Optional[Any] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        super().__init__(
            controller_name="workflow_controller",
            resolver=resolver,
            dependencies=dependencies,
            logger=logger,
        )
        self._workflow = workflow_service

    def handle(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        """Dispatch to the appropriate action handler.

        Args:
            payload: :class:`InteractionPayload` with action in
                ``{run_stage, complete_stage, fail_stage, route_next}``.

        Returns:
            :class:`StandardResponseEnvelope`.
        """
        dispatch = {
            "run_stage": self._run_stage,
            "complete_stage": self._complete_stage,
            "fail_stage": self._fail_stage,
            "route_next": self._route_next,
        }
        handler = dispatch.get(payload.action)
        if handler is None:
            return self._build_error_envelope(
                function_name="handle",
                run_id=payload.run_id or "",
                error_message=f"WorkflowController does not handle action '{payload.action}'.",
                stage_name=payload.stage_name,
                actor=payload.actor,
            )
        return handler(payload)

    # ------------------------------------------------------------------

    def _run_stage(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        run_id = payload.run_id or ""
        actor = payload.actor
        params = payload.parameters or {}

        stack = self._resolve_stack(
            stage_name=payload.stage_name,
            actor_role=actor.role if actor else "developer",
        )

        blocked = self._ensure_tool_allowed(
            "run_stage",
            stack,
            function_name="run_stage",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
        )
        if blocked:
            return blocked

        result = self._workflow.start_stage(
            run_id=run_id,
            stage_name=payload.stage_name,
            actor_id=actor.actor_id if actor else "unknown",
            actor_role=actor.role if actor else "developer",
        )

        event_ref = self._emit_event(
            "stage.started",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
            payload={"stage_name": payload.stage_name},
        )

        if not result.is_success:
            return self._build_error_envelope(
                function_name="run_stage",
                run_id=run_id,
                error_message=result.message,
                stage_name=payload.stage_name,
                actor=actor,
            )

        return self._build_response(
            run_id=run_id,
            function_name="run_stage",
            status="success",
            message=f"Stage '{payload.stage_name}' started.",
            data={
                "stage_name": payload.stage_name,
                "resolved_stack": stack.to_dict() if stack else None,
            },
            stage_name=payload.stage_name,
            actor=actor,
            event_ref=event_ref,
            governance_summary=self._governance_summary_from_stack(stack),
        )

    def _complete_stage(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        run_id = payload.run_id or ""
        actor = payload.actor
        params = payload.parameters or {}
        artifact_ids = params.get("artifact_ids", [])

        result = self._workflow.complete_stage(
            run_id=run_id,
            stage_name=payload.stage_name,
            actor_id=actor.actor_id if actor else "unknown",
            artifact_ids=artifact_ids,
        )

        event_ref = self._emit_event(
            "stage.completed",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
            payload={"artifact_ids": artifact_ids},
        )

        if not result.is_success:
            return self._build_error_envelope(
                function_name="complete_stage",
                run_id=run_id,
                error_message=result.message,
                stage_name=payload.stage_name,
                actor=actor,
            )

        stack = self._resolve_stack(
            stage_name=payload.stage_name,
            actor_role=actor.role if actor else "developer",
        )

        return self._build_response(
            run_id=run_id,
            function_name="complete_stage",
            status="success",
            message=f"Stage '{payload.stage_name}' completed.",
            data={"stage_name": payload.stage_name},
            stage_name=payload.stage_name,
            actor=actor,
            event_ref=event_ref,
            next_stage=stack.next_stages[0] if stack and stack.next_stages else None,
        )

    def _fail_stage(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        run_id = payload.run_id or ""
        actor = payload.actor
        params = payload.parameters or {}
        error_detail = params.get("error_detail", "")

        result = self._workflow.fail_stage(
            run_id=run_id,
            stage_name=payload.stage_name,
            actor_id=actor.actor_id if actor else "unknown",
            error_detail=error_detail,
        )

        event_ref = self._emit_event(
            "stage.failed",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
            payload={"error_detail": error_detail},
        )

        if not result.is_success:
            return self._build_error_envelope(
                function_name="fail_stage",
                run_id=run_id,
                error_message=result.message,
                stage_name=payload.stage_name,
                actor=actor,
            )

        return self._build_response(
            run_id=run_id,
            function_name="fail_stage",
            status="success",
            message=f"Stage '{payload.stage_name}' marked failed.",
            data={"stage_name": payload.stage_name, "error_detail": error_detail},
            stage_name=payload.stage_name,
            actor=actor,
            event_ref=event_ref,
        )

    def _route_next(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        run_id = payload.run_id or ""
        actor = payload.actor

        result = self._workflow.route_next(run_id=run_id)

        if not result.is_success:
            return self._build_error_envelope(
                function_name="route_next",
                run_id=run_id,
                error_message=result.message,
                stage_name=payload.stage_name,
                actor=actor,
            )

        next_stage = result.data.get("next_stage") if result.data else None
        stack = self._resolve_stack(
            stage_name=next_stage or payload.stage_name,
            actor_role=actor.role if actor else "developer",
        )

        return self._build_response(
            run_id=run_id,
            function_name="route_next",
            status="success",
            message=f"Routed to next stage: {next_stage}.",
            data={
                "next_stage": next_stage,
                "resolved_stack": stack.to_dict() if stack else None,
            },
            stage_name=next_stage,
            actor=actor,
            next_stage=next_stage,
        )

    def _governance_summary_from_stack(self, stack: Any) -> Any:
        if stack is None:
            return None
        from sdk.platform_core.schemas.common_fragments import GovernanceSummary
        flags = stack.governance_flags or {}
        blocking = []
        if flags.get("review_required"):
            blocking.append("review_required")
        if flags.get("approval_required"):
            blocking.append("approval_required")
        return GovernanceSummary(
            policy_check_result="pass" if not blocking else "review_required",
            blocking_reasons=blocking,
        )
