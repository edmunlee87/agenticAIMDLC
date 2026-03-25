"""Base controller for all MDLC platform controllers.

Controllers translate UI/agent :class:`~platform_core.schemas.payloads.InteractionPayload`
into service calls and return :class:`~platform_core.schemas.payloads.StandardResponseEnvelope`.
All controller methods must be stateless -- state lives in the workflow_state store.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.schemas.payloads import InteractionPayload, StandardResponseEnvelope
from platform_core.utils.id_factory import IDFactory, id_factory
from platform_core.utils.time_provider import TimeProvider, time_provider


class BaseController(ABC):
    """Root base class for all MDLC controllers.

    Args:
        bundle: The active :class:`RuntimeConfigBundle`.
        id_factory_: Optional injectable :class:`IDFactory`.
        time_provider_: Optional injectable :class:`TimeProvider`.
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        id_factory_: IDFactory | None = None,
        time_provider_: TimeProvider | None = None,
    ) -> None:
        self._bundle = bundle
        self._id_factory = id_factory_ or id_factory
        self._time_provider = time_provider_ or time_provider
        self._logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )

    @abstractmethod
    def handle(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        """Process an interaction payload and return a response envelope.

        Implementations must:
        1. Validate the payload action against the resolved allowlist.
        2. Execute the requested operation via service calls.
        3. Write an audit record for any material action.
        4. Return a StandardResponseEnvelope with populated audit_ref and event_ref.

        Args:
            payload: Structured input from a UI or agent.

        Returns:
            :class:`StandardResponseEnvelope` -- never raises unchecked exceptions.
        """

    def _build_error_response(
        self,
        payload: InteractionPayload,
        error_code: str,
        error_message: str,
        detail: str = "",
    ) -> StandardResponseEnvelope:
        """Build a standardised error response envelope.

        Args:
            payload: The originating interaction payload.
            error_code: Stable error code.
            error_message: Human-readable error message.
            detail: Optional additional detail.

        Returns:
            :class:`StandardResponseEnvelope` with ``status="failed"``.
        """
        from platform_core.schemas.payloads import ResponseError

        return StandardResponseEnvelope(
            project_id=payload.project_id,
            run_id=payload.run_id,
            session_id=payload.session_id,
            trace_id=payload.trace_id,
            correlation_id=payload.correlation_id,
            actor=payload.actor,
            timestamp=self._time_provider.now(),
            stage_name=payload.stage_name,
            policy_context=payload.policy_context,
            status="failed",
            message=error_message,
            errors=[ResponseError(code=error_code, message=error_message, detail=detail)],
        )
