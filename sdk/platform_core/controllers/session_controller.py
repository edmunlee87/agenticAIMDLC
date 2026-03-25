"""SessionController — open and resume platform sessions.

Handles :class:`InteractionPayload` with actions:
- ``open_session``: bootstrap a new project/run and open a session.
- ``resume_session``: resume a suspended session from checkpoint.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from sdk.platform_core.controllers.base import BaseController
from sdk.platform_core.runtime.resolvers.runtime_resolver import RuntimeResolver
from sdk.platform_core.schemas.common_fragments import ActorRecord
from sdk.platform_core.schemas.payload_models import (
    InteractionPayload,
    StandardResponseEnvelope,
)


class SessionController(BaseController):
    """Controller for session bootstrap and resume.

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
            controller_name="session_controller",
            resolver=resolver,
            dependencies=dependencies,
            logger=logger,
        )
        self._workflow = workflow_service

    def handle(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        """Dispatch to open_session or resume_session based on payload action.

        Args:
            payload: :class:`InteractionPayload` with ``action`` set to
                ``"open_session"`` or ``"resume_session"``.

        Returns:
            :class:`StandardResponseEnvelope`.
        """
        action = payload.action
        if action == "open_session":
            return self._open_session(payload)
        if action == "resume_session":
            return self._resume_session(payload)
        return self._build_error_envelope(
            function_name="handle",
            run_id=payload.run_id or "",
            error_message=f"SessionController does not handle action '{action}'.",
            stage_name=payload.stage_name,
            actor=payload.actor,
        )

    # ------------------------------------------------------------------

    def _open_session(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        run_id = payload.run_id or ""
        actor = payload.actor
        params = payload.parameters or {}

        result = self._workflow.open_session(
            run_id=run_id,
            project_id=payload.project_id,
            actor_id=actor.actor_id if actor else "unknown",
            actor_role=actor.role if actor else "system",
            last_stage=payload.stage_name,
            session_metadata=params.get("session_metadata"),
        )

        event_ref = self._emit_event(
            "session.opened",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
            payload={"project_id": payload.project_id},
        )

        if not result.is_success:
            return self._build_error_envelope(
                function_name="open_session",
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
            function_name="open_session",
            status="success",
            message="Session opened successfully.",
            data={
                "session_id": result.data.get("session_id") if result.data else None,
                "resolved_stack": stack.to_dict() if stack else None,
            },
            stage_name=payload.stage_name,
            actor=actor,
            event_ref=event_ref,
            next_stage=stack.next_stages[0] if stack and stack.next_stages else None,
        )

    def _resume_session(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        run_id = payload.run_id or ""
        actor = payload.actor
        params = payload.parameters or {}
        session_id = params.get("session_id") or payload.session_id

        if not session_id:
            return self._build_error_envelope(
                function_name="resume_session",
                run_id=run_id,
                error_message="session_id is required to resume a session.",
                stage_name=payload.stage_name,
                actor=actor,
            )

        result = self._workflow.resume_session(
            session_id=session_id,
            actor_id=actor.actor_id if actor else "unknown",
        )

        event_ref = self._emit_event(
            "session.resumed",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
            payload={"session_id": session_id},
        )

        if not result.is_success:
            return self._build_error_envelope(
                function_name="resume_session",
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
            function_name="resume_session",
            status="success",
            message="Session resumed successfully.",
            data={
                "session_id": session_id,
                "resolved_stack": stack.to_dict() if stack else None,
            },
            stage_name=payload.stage_name,
            actor=actor,
            event_ref=event_ref,
        )
