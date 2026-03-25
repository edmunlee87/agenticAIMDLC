"""api_bridge.adapter -- REST adapter: maps APIRequest → AgentDispatcher → APIResponse.

The adapter is the HTTP boundary.  It:
1. Validates and enriches the :class:`~api_bridge.models.APIRequest`.
2. Constructs an :class:`~platform_core.schemas.payloads.InteractionPayload`.
3. Delegates to :class:`~agent_bridge.dispatcher.AgentDispatcher`.
4. Maps the :class:`~platform_core.schemas.payloads.StandardResponseEnvelope`
   back to an :class:`~api_bridge.models.APIResponse`.
"""

from __future__ import annotations

import logging
from typing import Any

from api_bridge.models import APIRequest, APIResponse

logger = logging.getLogger(__name__)


class APIAdapter:
    """REST adapter that bridges HTTP requests to the AgentDispatcher.

    Args:
        dispatcher: :class:`~agent_bridge.dispatcher.AgentDispatcher` instance.
        auth_hook: Optional callable ``(auth_claims: dict) -> bool`` for auth validation.
    """

    def __init__(self, dispatcher: Any, auth_hook: Any | None = None) -> None:
        self._dispatcher = dispatcher
        self._auth_hook = auth_hook

    def handle(self, request: APIRequest) -> APIResponse:
        """Process an inbound API request.

        Args:
            request: :class:`APIRequest` from the REST layer.

        Returns:
            :class:`APIResponse`.
        """
        # Auth validation
        if self._auth_hook and not self._auth_hook(request.auth_claims):
            logger.warning("api_adapter.auth_failed", extra={"trace_id": request.trace_id, "actor_id": request.actor_id})
            return APIResponse(
                success=False,
                status_code=401,
                error_code="ERR_UNAUTHORIZED",
                error_message="Authentication failed.",
                trace_id=request.trace_id,
            )

        try:
            from platform_contracts.enums import InteractionType
            interaction_type = InteractionType(request.interaction_type)
        except (ValueError, ImportError) as exc:
            return APIResponse(
                success=False,
                status_code=400,
                error_code="ERR_INVALID_INTERACTION_TYPE",
                error_message=f"Unknown interaction_type: {request.interaction_type}",
                trace_id=request.trace_id,
            )

        try:
            from platform_core.schemas.payloads import InteractionPayload
            payload = InteractionPayload(
                interaction_type=interaction_type,
                run_id=request.run_id,
                project_id=request.project_id,
                actor_id=request.actor_id,
                trace_id=request.trace_id,
                **request.payload,
            )
        except Exception as exc:
            return APIResponse(
                success=False,
                status_code=400,
                error_code="ERR_PAYLOAD_VALIDATION",
                error_message=str(exc),
                trace_id=request.trace_id,
            )

        try:
            envelope = self._dispatcher.dispatch(payload)
        except Exception as exc:
            logger.error("api_adapter.dispatch_error", extra={"error": str(exc), "trace_id": request.trace_id})
            return APIResponse(
                success=False,
                status_code=500,
                error_code="ERR_DISPATCH",
                error_message=str(exc),
                trace_id=request.trace_id,
            )

        success = getattr(envelope, "success", True)
        return APIResponse(
            success=success,
            status_code=200 if success else 422,
            data=envelope.model_dump() if hasattr(envelope, "model_dump") else vars(envelope),
            trace_id=request.trace_id,
        )

    def health(self) -> dict[str, Any]:
        """Return health status.

        Returns:
            Dict with status.
        """
        return {"status": "ok", "service": "APIAdapter"}
