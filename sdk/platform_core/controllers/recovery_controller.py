"""RecoveryController — surface recovery options and apply a chosen path.

Handles :class:`InteractionPayload` with actions:
- ``get_recovery_options``: recommend a recovery path and provide validation status.
- ``apply_recovery``: apply the chosen recovery path.
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


class RecoveryController(BaseController):
    """Controller for failure recovery.

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
            controller_name="recovery_controller",
            resolver=resolver,
            dependencies=dependencies,
            logger=logger,
        )
        self._workflow = workflow_service

    def handle(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        """Dispatch to recovery action handler.

        Args:
            payload: :class:`InteractionPayload` with action in
                ``{get_recovery_options, apply_recovery}``.

        Returns:
            :class:`StandardResponseEnvelope`.
        """
        dispatch = {
            "get_recovery_options": self._get_recovery_options,
            "apply_recovery": self._apply_recovery,
        }
        handler = dispatch.get(payload.action)
        if handler is None:
            return self._build_error_envelope(
                function_name="handle",
                run_id=payload.run_id or "",
                error_message=f"RecoveryController does not handle action '{payload.action}'.",
                stage_name=payload.stage_name,
                actor=payload.actor,
            )
        return handler(payload)

    # ------------------------------------------------------------------

    def _get_recovery_options(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        run_id = payload.run_id or ""
        actor = payload.actor

        rec_result = self._workflow.get_recovery_recommendation(run_id=run_id)
        val_result = self._workflow.validate_resume(run_id=run_id)

        data: dict = {}
        if rec_result.is_success and rec_result.data:
            data["recommendation"] = rec_result.data
        if val_result.is_success and val_result.data:
            data["resume_validation"] = val_result.data

        stack = self._resolve_stack(
            stage_name=payload.stage_name,
            actor_role=actor.role if actor else "developer",
        )

        return self._build_response(
            run_id=run_id,
            function_name="get_recovery_options",
            status="success",
            message="Recovery options retrieved.",
            data={**data, "resolved_stack": stack.to_dict() if stack else None},
            stage_name=payload.stage_name,
            actor=actor,
        )

    def _apply_recovery(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        run_id = payload.run_id or ""
        actor = payload.actor
        params = payload.parameters or {}
        recovery_path = params.get("recovery_path", "")

        if not recovery_path:
            return self._build_error_envelope(
                function_name="apply_recovery",
                run_id=run_id,
                error_message="recovery_path is required.",
                stage_name=payload.stage_name,
                actor=actor,
            )

        result = self._workflow.apply_recovery(
            run_id=run_id,
            recovery_path=recovery_path,
        )

        audit_ref = self._write_audit(
            "recovery_applied",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
            payload={"recovery_path": recovery_path},
        )
        event_ref = self._emit_event(
            "recovery.applied",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
            payload={"recovery_path": recovery_path},
        )

        if not result.is_success:
            return self._build_error_envelope(
                function_name="apply_recovery",
                run_id=run_id,
                error_message=result.message,
                stage_name=payload.stage_name,
                actor=actor,
            )

        restored_stage = (result.data or {}).get("current_stage", payload.stage_name)
        stack = self._resolve_stack(
            stage_name=restored_stage,
            actor_role=actor.role if actor else "developer",
        )

        return self._build_response(
            run_id=run_id,
            function_name="apply_recovery",
            status="success",
            message=f"Recovery path '{recovery_path}' applied.",
            data={
                "recovery_path": recovery_path,
                "restored_stage": restored_stage,
                "resolved_stack": stack.to_dict() if stack else None,
            },
            stage_name=restored_stage,
            actor=actor,
            audit_ref=audit_ref,
            event_ref=event_ref,
            next_stage=restored_stage,
        )
