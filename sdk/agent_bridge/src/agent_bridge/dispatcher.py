"""AgentDispatcher -- routes agent tool-call payloads to the correct controller.

The dispatcher is the single entry point for any LLM/agent tool call into the
MDLC platform.  It:

1. Receives a raw dict payload from the agent (e.g. OpenAI function-call args).
2. Validates and constructs an :class:`~platform_core.schemas.payloads.InteractionPayload`.
3. Routes to the correct controller via :class:`~platform_core.controllers.factory.ControllerFactory`.
4. Returns the serialised :class:`~platform_core.schemas.payloads.StandardResponseEnvelope`.

Routing table (``interaction_type`` → controller):
- ``SESSION_COMMAND`` → :class:`~platform_core.controllers.session.SessionController`
- ``STAGE_ACTION`` → :class:`~platform_core.controllers.workflow.WorkflowController`
- ``REVIEW_RESPONSE`` → :class:`~platform_core.controllers.review.ReviewController`
- ``RECOVERY_CHOICE`` → :class:`~platform_core.controllers.recovery.RecoveryController`
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import ValidationError

from platform_contracts.enums import InteractionType
from platform_core.controllers.factory import ControllerFactory
from platform_core.schemas.payloads import InteractionPayload, StandardResponseEnvelope

logger = logging.getLogger(__name__)

_ROUTING: dict[str, str] = {
    InteractionType.SESSION_COMMAND.value: "session",
    InteractionType.STAGE_ACTION.value: "workflow",
    InteractionType.REVIEW_RESPONSE.value: "review",
    InteractionType.RECOVERY_CHOICE.value: "recovery",
}


class AgentDispatcher:
    """Routes agent tool calls to the appropriate controller.

    Args:
        factory: :class:`~platform_core.controllers.factory.ControllerFactory`
            pre-wired with all services.
    """

    def __init__(self, factory: ControllerFactory) -> None:
        self._factory = factory

    def dispatch(self, raw_payload: dict[str, Any]) -> dict[str, Any]:
        """Validate and route a raw payload dict to the correct controller.

        Args:
            raw_payload: Dict matching the ``InteractionPayload`` schema.

        Returns:
            Serialised ``StandardResponseEnvelope`` as a dict.
        """
        # Parse and validate.
        try:
            payload = InteractionPayload.model_validate(raw_payload)
        except ValidationError as exc:
            logger.warning("agent_dispatcher.validation_error", extra={"errors": exc.errors()})
            return self._validation_error_envelope(raw_payload, exc)

        interaction_type = payload.interaction_type.value
        controller_name = _ROUTING.get(interaction_type)

        if controller_name is None:
            return self._unknown_type_envelope(payload, interaction_type)

        controller = getattr(self._factory, controller_name)()
        response: StandardResponseEnvelope = controller.handle(payload)

        logger.info(
            "agent_dispatcher.dispatched",
            extra={
                "interaction_type": interaction_type,
                "action": payload.action,
                "run_id": payload.run_id,
                "status": response.status,
            },
        )
        return response.model_dump()

    # ------------------------------------------------------------------
    # Error envelope builders
    # ------------------------------------------------------------------

    def _validation_error_envelope(
        self, raw: dict[str, Any], exc: ValidationError
    ) -> dict[str, Any]:
        return {
            "status": "failed",
            "message": "Payload validation failed.",
            "errors": [{"code": "ERR_VALIDATION", "message": str(exc)}],
            "data": {},
        }

    def _unknown_type_envelope(
        self, payload: InteractionPayload, interaction_type: str
    ) -> dict[str, Any]:
        return {
            "status": "failed",
            "project_id": payload.project_id,
            "run_id": payload.run_id,
            "message": f"No controller registered for interaction_type '{interaction_type}'.",
            "errors": [
                {
                    "code": "ERR_NO_ROUTE",
                    "message": f"Unknown interaction_type: {interaction_type}",
                }
            ],
            "data": {},
        }
