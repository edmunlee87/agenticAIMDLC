"""RecoveryController -- surface recovery options and apply a chosen path.

Actions:
- ``get_recovery_options``: recommend recovery path + provide validation status.
- ``apply_recovery``: apply the chosen :class:`~workflowsdk.models.RecoveryPath`.
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


class RecoveryController(BaseController):
    """Controller for failure recovery.

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
            "get_recovery_options": self._get_recovery_options,
            "apply_recovery": self._apply_recovery,
        }
        handler = dispatch.get(action)
        if handler is None:
            return self._build_error_response(
                payload, "ERR_UNKNOWN_ACTION",
                f"RecoveryController does not handle action '{action}'.",
            )
        return handler(payload)

    # ------------------------------------------------------------------

    def _get_recovery_options(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        rec_result = self._workflow.get_recovery_recommendation(payload.run_id)
        validate_result = self._workflow.validate_resume(payload.run_id)

        data: dict[str, Any] = {}
        if rec_result.success:
            data["recommendation"] = rec_result.data
        if validate_result.success:
            data["resume_validation"] = validate_result.data

        decision = self._resolver.resolve(_make_ctx(payload))
        return _ok_envelope(payload, self._time_provider, data=data, decision=decision)

    def _apply_recovery(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        path_str = (payload.data or {}).get("recovery_path", "")
        if not path_str:
            return self._build_error_response(payload, "ERR_PATH_REQUIRED", "recovery_path is required.")

        from workflowsdk.models import RecoveryPath
        try:
            path = RecoveryPath(path_str)
        except ValueError:
            return self._build_error_response(
                payload, "ERR_INVALID_PATH",
                f"Unknown recovery_path '{path_str}'. Valid: {[p.value for p in RecoveryPath]}",
            )

        result = self._workflow.apply_recovery(payload.run_id, path)
        if not result.success:
            return self._build_error_response(payload, result.error_code or "ERR_RECOVERY", result.error_message or "")

        decision = self._resolver.resolve(_make_ctx(payload))
        return _ok_envelope(
            payload, self._time_provider,
            data={"applied_path": path.value, "restored_stage": result.data.current_stage},
            decision=decision,
        )
