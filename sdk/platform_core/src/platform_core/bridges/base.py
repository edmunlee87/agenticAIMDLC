"""Base bridge class for all MDLC platform bridges.

Bridges translate external interaction surfaces (agent, Jupyter, API, CLI, MCP)
into :class:`~platform_core.schemas.payloads.InteractionPayload` and dispatch
to the appropriate controller. They translate back the
:class:`~platform_core.schemas.payloads.StandardResponseEnvelope` into the
surface-appropriate response format.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.schemas.payloads import InteractionPayload, StandardResponseEnvelope
from platform_core.utils.id_factory import IDFactory, id_factory
from platform_core.utils.time_provider import TimeProvider, time_provider


class BaseBridge(ABC):
    """Root base class for all MDLC bridges.

    Bridges are the outermost layer. They:
    1. Receive surface-specific input (LLM tool call, HTTP request, CLI args, etc.).
    2. Build an :class:`InteractionPayload` with full governance context.
    3. Dispatch to the appropriate controller.
    4. Translate the response envelope to the surface format.

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
    def dispatch(self, raw_input: Any) -> Any:
        """Receive surface-specific input, dispatch to controller, return surface output.

        Args:
            raw_input: Surface-specific input (dict, HTTP request, CLI namespace, etc.).

        Returns:
            Surface-appropriate response (dict, HTTP response, CLI output, etc.).
        """

    @abstractmethod
    def build_payload(self, raw_input: Any) -> InteractionPayload:
        """Translate surface-specific input into an :class:`InteractionPayload`.

        Implementations must populate all governance fields (project_id, run_id,
        session_id, trace_id, actor, policy_context) from the surface context.

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
