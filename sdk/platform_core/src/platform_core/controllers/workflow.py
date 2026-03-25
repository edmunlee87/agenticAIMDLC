"""WorkflowController -- stage start/complete and routing.

Handles ``STAGE_ACTION`` interaction payloads with actions:
- ``start_stage``
- ``complete_stage``
- ``fail_stage``
- ``route_next``
"""

from __future__ import annotations

import logging
from typing import Any

from platform_core.controllers.base import BaseController
from platform_core.controllers.session import _make_ctx, _ok_envelope
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.runtime.resolver import RuntimeResolver
from platform_core.schemas.payloads import InteractionPayload, StandardResponseEnvelope
from platform_core.utils.id_factory import IDFactory
from platform_core.utils.time_provider import TimeProvider

logger = logging.getLogger(__name__)


class WorkflowController(BaseController):
    """Controller for stage progression and workflow routing.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        workflow_service: :class:`~workflowsdk.service.WorkflowService`.
        resolver: Pre-built :class:`RuntimeResolver`.
        id_factory_: Injectable :class:`IDFactory`.
        time_provider_: Injectable :class:`TimeProvider`.
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        workflow_service: Any,
        resolver: RuntimeResolver | None = None,
        id_factory_: IDFactory | None = None,
        time_provider_: TimeProvider | None = None,
    ) -> None:
        super().__init__(bundle, id_factory_=id_factory_, time_provider_=time_provider_)
        self._workflow = workflow_service
        self._resolver = resolver or RuntimeResolver(bundle)

    def handle(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        action = payload.action
        dispatch = {
            "start_stage": self._start_stage,
            "complete_stage": self._complete_stage,
            "fail_stage": self._fail_stage,
            "route_next": self._route_next,
        }
        handler = dispatch.get(action)
        if handler is None:
            return self._build_error_response(
                payload, "ERR_UNKNOWN_ACTION",
                f"WorkflowController does not handle action '{action}'.",
            )
        return handler(payload)

    # ------------------------------------------------------------------

    def _start_stage(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        ctx = _make_ctx(payload)
        decision = self._resolver.resolve(ctx)

        result = self._workflow.start_stage(
            run_id=payload.run_id,
            project_id=payload.project_id,
            stage_name=payload.stage_name,
            actor=payload.actor,
            session_id=payload.session_id,
            trace_id=payload.trace_id,
            policy_context=payload.policy_context,
            ui_mode=decision.ui_mode.value,
            interaction_mode=decision.interaction_mode.value,
        )
        if not result.success:
            return self._build_error_response(payload, result.error_code or "ERR_START", result.error_message or "")
        return _ok_envelope(payload, self._time_provider, event_ref=result.data, decision=decision)

    def _complete_stage(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        artifact_ids = (payload.data or {}).get("artifact_ids", [])
        result = self._workflow.complete_stage(
            run_id=payload.run_id,
            project_id=payload.project_id,
            stage_name=payload.stage_name,
            actor=payload.actor,
            artifact_ids=artifact_ids,
            session_id=payload.session_id,
            trace_id=payload.trace_id,
            policy_context=payload.policy_context,
        )
        if not result.success:
            return self._build_error_response(payload, result.error_code or "ERR_COMPLETE", result.error_message or "")

        decision = self._resolver.resolve(_make_ctx(payload))
        return _ok_envelope(payload, self._time_provider, event_ref=result.data, decision=decision)

    def _fail_stage(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        error_detail = (payload.data or {}).get("error_detail", "")
        result = self._workflow.fail_stage(
            run_id=payload.run_id,
            project_id=payload.project_id,
            stage_name=payload.stage_name,
            actor=payload.actor,
            error_detail=error_detail,
            session_id=payload.session_id,
            trace_id=payload.trace_id,
        )
        if not result.success:
            return self._build_error_response(payload, result.error_code or "ERR_FAIL", result.error_message or "")
        decision = self._resolver.resolve(_make_ctx(payload))
        return _ok_envelope(payload, self._time_provider, event_ref=result.data, decision=decision)

    def _route_next(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        result = self._workflow.route_next(payload.run_id)
        if not result.success:
            return self._build_error_response(payload, result.error_code or "ERR_ROUTE", result.error_message or "")
        decision = self._resolver.resolve(_make_ctx(payload))
        return _ok_envelope(
            payload, self._time_provider,
            data={"next_stage": result.data},
            decision=decision,
        )
