"""BaseWidgetComponent: foundation for all UI widget components.

Widget components render review cards, selection panels, bootstrap cards,
and other interactive UI elements in the HITL workspace.

Design rules:
- Widgets receive a ReviewPayload or structured props and return render metadata.
- All callbacks are registered, not hard-coded.
- Widget state is driven by payload; no local state mutation.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional


class BaseWidgetComponent(ABC):
    """Root base for all platform UI widget components.

    Provides validate_props, build_component, register_callback, and
    get_render_metadata.

    Args:
        component_name: Name of this widget component.
        logger: Optional logger override.
    """

    def __init__(
        self,
        component_name: str,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._component_name = component_name
        self._callbacks: Dict[str, Callable] = {}
        self._logger = logger or logging.getLogger(f"platform.ui.{component_name}")

    @abstractmethod
    def validate_props(self, props: Dict[str, Any]) -> Optional[str]:
        """Validate the component's input props.

        Returns an error message if invalid; None if valid.

        Args:
            props: Component props to validate.

        Returns:
            Error message string if invalid, None if valid.
        """

    @abstractmethod
    def build_component(self, props: Dict[str, Any]) -> Dict[str, Any]:
        """Build the component's render specification from props.

        Args:
            props: Component input props.

        Returns:
            Component render specification dict.
        """

    def register_callback(self, event_name: str, handler: Callable) -> None:
        """Register a callback handler for a component event.

        Args:
            event_name: Name of the event to handle (e.g. "on_approve").
            handler: Callable to invoke when the event fires.
        """
        self._callbacks[event_name] = handler
        self._logger.debug(
            "Registered callback for %s on %s",
            event_name,
            self._component_name,
        )

    def get_render_metadata(self) -> Dict[str, Any]:
        """Return metadata about this component's render capabilities.

        Returns:
            Dict with component_name, registered_events, and capabilities.
        """
        return {
            "component_name": self._component_name,
            "registered_events": list(self._callbacks.keys()),
            "capabilities": [],
        }

    def _invoke_callback(self, event_name: str, event_data: Any) -> Any:
        """Invoke a registered callback if one exists for the event.

        Args:
            event_name: Name of the event.
            event_data: Event data to pass to the callback.

        Returns:
            Callback return value, or None if no callback registered.
        """
        handler = self._callbacks.get(event_name)
        if handler:
            try:
                return handler(event_data)
            except Exception as exc:
                self._logger.error(
                    "Callback error for %s on %s: %s",
                    event_name,
                    self._component_name,
                    exc,
                )
        return None
