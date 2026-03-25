"""BaseBridge: foundation for all platform bridges.

Bridges translate external interaction surfaces (agent, Jupyter, API, CLI)
into :class:`InteractionPayload` and dispatch to the appropriate controller.
They translate back the :class:`StandardResponseEnvelope` to the surface format.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from sdk.platform_core.schemas.common_fragments import ActorRecord, PolicyContextRef
from sdk.platform_core.schemas.payload_models import (
    InteractionPayload,
    StandardResponseEnvelope,
)
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider


class BaseBridge(ABC):
    """Root base class for all MDLC bridges.

    Bridges are the outermost layer. They:
    1. Receive surface-specific input (LLM tool call, widget event, HTTP request, etc.).
    2. Build an :class:`InteractionPayload` with full governance context.
    3. Dispatch to the appropriate controller.
    4. Translate the response envelope to the surface format.

    Args:
        controller_factory: :class:`ControllerFactory` for resolving the correct controller.
        logger: Optional logger override.
    """

    def __init__(
        self,
        controller_factory: Any,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._factory = controller_factory
        self._logger = logger or logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )

    @abstractmethod
    def dispatch(self, raw_input: Any) -> Any:
        """Receive surface-specific input, dispatch to controller, return surface output.

        Args:
            raw_input: Surface-specific input.

        Returns:
            Surface-appropriate response.
        """

    @abstractmethod
    def build_payload(self, raw_input: Any) -> InteractionPayload:
        """Translate surface-specific input into an :class:`InteractionPayload`.

        Args:
            raw_input: Surface-specific input.

        Returns:
            Fully populated :class:`InteractionPayload`.
        """

    @abstractmethod
    def format_response(self, envelope: StandardResponseEnvelope) -> Any:
        """Translate a :class:`StandardResponseEnvelope` to the surface format.

        Args:
            envelope: Controller response envelope.

        Returns:
            Surface-appropriate response.
        """

    def _build_actor(
        self,
        actor_id: str,
        role: str,
        display_name: Optional[str] = None,
    ) -> ActorRecord:
        """Build an :class:`ActorRecord` from raw fields.

        Args:
            actor_id: Actor's unique identifier.
            role: Platform role string.
            display_name: Optional human-readable name.

        Returns:
            :class:`ActorRecord`.
        """
        return ActorRecord(actor_id=actor_id, role=role, display_name=display_name)

    def _build_interaction_payload(
        self,
        *,
        stage_name: str,
        interaction_type: str,
        action: str,
        actor: ActorRecord,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        policy_context: Optional[PolicyContextRef] = None,
        review_id: Optional[str] = None,
        policy_acknowledgments: Optional[list] = None,
    ) -> InteractionPayload:
        """Build a fully populated :class:`InteractionPayload`.

        Args:
            stage_name: Target stage name.
            interaction_type: Surface-specific interaction type.
            action: Bounded action string.
            actor: Actor performing the interaction.
            run_id: Active run identifier.
            project_id: Active project identifier.
            session_id: Active session identifier.
            trace_id: Distributed trace ID.
            correlation_id: Correlation ID.
            parameters: Action-specific parameters.
            policy_context: Active policy context.
            review_id: Optional linked review ID.
            policy_acknowledgments: Policy findings acknowledged by actor.

        Returns:
            :class:`InteractionPayload`.
        """
        return InteractionPayload(
            interaction_id=IDFactory.correlation_id(),
            stage_name=stage_name,
            interaction_type=interaction_type,
            action=action,
            actor=actor,
            run_id=run_id,
            project_id=project_id,
            session_id=session_id,
            trace_id=trace_id or IDFactory.trace_id(),
            correlation_id=correlation_id,
            parameters=parameters or {},
            policy_context=policy_context,
            review_id=review_id,
            policy_acknowledgments=policy_acknowledgments or [],
            timestamp=TimeProvider.now_iso(),
        )
