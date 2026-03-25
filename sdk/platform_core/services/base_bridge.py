"""BaseBridge: foundation for all platform bridges.

Bridges sit between UI/agent surfaces and Controllers. They:
1. Normalize incoming payloads from their surface (UI, agent, API, CLI)
2. Build interaction_payload and forward to the appropriate Controller
3. Normalize the standard_response_envelope back to the surface format
4. Enforce the SDK allowlist
5. Apply retry policy for transient failures

Concrete bridges: AgentBridge, JupyterBridge, APIBridge, CLIBridge, MCPBridge.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..schemas.base_result import BaseResult
from ..schemas.payload_models import InteractionPayload, StandardResponseEnvelope
from ..schemas.utilities import IDFactory, TimeProvider


class BaseBridge(ABC):
    """Root base for all platform bridges.

    Provides payload normalization, result normalization, interface contract
    validation, and allowlist enforcement.

    Args:
        bridge_name: Name of this bridge (e.g. "agent_bridge").
        controller: Controller instance to delegate requests to.
        allowlist: Optional set of permitted tool/action names.
        logger: Optional logger override.
    """

    def __init__(
        self,
        bridge_name: str,
        controller: Optional[Any] = None,
        allowlist: Optional[set] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._bridge_name = bridge_name
        self._controller = controller
        self._allowlist = allowlist or set()
        self._logger = logger or logging.getLogger(f"platform.bridge.{bridge_name}")

    @abstractmethod
    def dispatch(self, surface_request: Any, context: Optional[Dict[str, Any]] = None) -> Any:
        """Dispatch a surface request through the bridge.

        Normalizes the surface request, builds an InteractionPayload,
        forwards to the controller, and normalizes the response back.

        Args:
            surface_request: Raw request from the surface (UI widget, agent tool call, etc.).
            context: Optional additional context dict.

        Returns:
            Normalized response for the surface.
        """

    def _normalize_payload(
        self, surface_request: Any, context: Optional[Dict[str, Any]] = None
    ) -> InteractionPayload:
        """Convert a surface request into a standardized InteractionPayload.

        Concrete bridges implement this to handle their surface's request format.

        Args:
            surface_request: Raw surface request.
            context: Optional context dict.

        Returns:
            InteractionPayload.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _normalize_payload"
        )

    def _normalize_result(
        self, envelope: StandardResponseEnvelope, context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Convert a StandardResponseEnvelope to the surface response format.

        Concrete bridges implement this to handle their surface's response format.

        Args:
            envelope: The standard response envelope from the controller.
            context: Optional context dict.

        Returns:
            Surface-specific response.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _normalize_result"
        )

    def _validate_interface_contract(self, payload: InteractionPayload) -> Optional[str]:
        """Validate that a payload conforms to this bridge's interface contract.

        Returns an error message if invalid; None if valid.

        Args:
            payload: The interaction payload to validate.

        Returns:
            Error message string if invalid, None if valid.
        """
        if not payload.action:
            return "interaction_payload.action must not be empty"
        if not payload.interaction_type:
            return "interaction_payload.interaction_type must not be empty"
        if not payload.actor or not payload.actor.actor_id:
            return "interaction_payload.actor.actor_id must not be empty"
        return None

    def _enforce_allowlist(self, action: str) -> Optional[str]:
        """Check if an action is in the allowlist.

        Returns an error message if blocked; None if permitted.

        Args:
            action: The action to check.

        Returns:
            Error message if blocked, None if allowed.
        """
        if self._allowlist and action not in self._allowlist:
            return (
                f"Action '{action}' is not in the allowlist for {self._bridge_name}. "
                f"Permitted actions: {sorted(self._allowlist)}"
            )
        return None
