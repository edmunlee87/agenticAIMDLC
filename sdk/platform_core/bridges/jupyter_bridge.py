"""JupyterBridge — translates Jupyter widget events to platform interactions.

Components:
- ``widget_controller``: maps widget event types to interaction actions
- ``action_dispatch``: dispatches payloads to the appropriate controller
- ``result_refresh``: formats the response for widget state refresh

Design rule: JupyterBridge emits display-ready dicts consumable by ipywidgets.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from sdk.platform_core.bridges.base_bridge import BaseBridge
from sdk.platform_core.schemas.common_fragments import ActorRecord
from sdk.platform_core.schemas.payload_models import (
    InteractionPayload,
    StandardResponseEnvelope,
)
from sdk.platform_core.schemas.utilities import IDFactory


# Widget event type → controller + action
_WIDGET_ACTION_MAP: Dict[str, Dict[str, str]] = {
    "session_open": {"controller": "session", "action": "open_session"},
    "session_resume": {"controller": "session", "action": "resume_session"},
    "stage_run": {"controller": "workflow", "action": "run_stage"},
    "stage_complete": {"controller": "workflow", "action": "complete_stage"},
    "stage_fail": {"controller": "workflow", "action": "fail_stage"},
    "stage_route_next": {"controller": "workflow", "action": "route_next"},
    "review_open": {"controller": "review", "action": "open_review"},
    "review_get_payload": {"controller": "review", "action": "get_review_payload"},
    "review_submit": {"controller": "review", "action": "submit_review_action"},
    "recovery_options": {"controller": "recovery", "action": "get_recovery_options"},
    "recovery_apply": {"controller": "recovery", "action": "apply_recovery"},
}


class JupyterBridge(BaseBridge):
    """Bridge for Jupyter notebook widget interactions.

    Translates widget event dicts into :class:`InteractionPayload` and returns
    display-ready state dicts for widget refresh.

    Expected ``raw_input`` format::

        {
            "event_type": "stage_run",
            "stage_name": "feature_engineering",
            "run_id": "run_abc123",
            "project_id": "proj_xyz",
            "session_id": "ses_abc",
            "actor_id": "user_01",
            "actor_role": "developer",
            "parameters": {...}
        }

    Args:
        controller_factory: :class:`ControllerFactory` instance.
        logger: Optional logger override.
    """

    def __init__(
        self,
        controller_factory: Any,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        super().__init__(controller_factory=controller_factory, logger=logger)

    def dispatch(self, raw_input: Any) -> Dict[str, Any]:
        """Receive a widget event dict and dispatch to the appropriate controller.

        Args:
            raw_input: Widget event dict.

        Returns:
            Display-ready state dict for widget refresh.
        """
        if not isinstance(raw_input, dict):
            return self._widget_error("invalid_input", "raw_input must be a dict.")

        event_type = raw_input.get("event_type", "")
        mapping = _WIDGET_ACTION_MAP.get(event_type)
        if mapping is None:
            return self._widget_error(
                "unknown_event",
                f"Widget event '{event_type}' is not handled by JupyterBridge. "
                f"Supported: {list(_WIDGET_ACTION_MAP.keys())}",
            )

        try:
            payload = self.build_payload(raw_input)
        except Exception as exc:
            return self._widget_error("payload_build_failed", str(exc))

        controller = self._resolve_controller(mapping["controller"])
        if controller is None:
            return self._widget_error(
                "controller_unavailable",
                f"Controller '{mapping['controller']}' unavailable.",
            )

        try:
            envelope = controller.handle(payload)
        except Exception as exc:
            self._logger.error("JupyterBridge dispatch error: %s", exc)
            return self._widget_error("dispatch_error", str(exc))

        return self.format_response(envelope)

    def build_payload(self, raw_input: Any) -> InteractionPayload:
        """Build :class:`InteractionPayload` from a widget event dict.

        Args:
            raw_input: Widget event dict.

        Returns:
            :class:`InteractionPayload`.

        Raises:
            ValueError: If required fields are missing.
        """
        event_type = raw_input.get("event_type", "")
        mapping = _WIDGET_ACTION_MAP.get(event_type)
        if mapping is None:
            raise ValueError(f"Unknown event_type: {event_type!r}")

        stage_name = raw_input.get("stage_name", "")
        if not stage_name:
            raise ValueError("stage_name is required in widget event.")

        actor_id = raw_input.get("actor_id") or "jupyter_user"
        actor_role = raw_input.get("actor_role") or "developer"
        actor = self._build_actor(actor_id=actor_id, role=actor_role)

        return self._build_interaction_payload(
            stage_name=stage_name,
            interaction_type="jupyter_widget_event",
            action=mapping["action"],
            actor=actor,
            run_id=raw_input.get("run_id"),
            project_id=raw_input.get("project_id"),
            session_id=raw_input.get("session_id"),
            trace_id=raw_input.get("trace_id"),
            correlation_id=raw_input.get("correlation_id"),
            parameters=raw_input.get("parameters"),
            review_id=raw_input.get("review_id"),
            policy_acknowledgments=raw_input.get("policy_acknowledgments"),
        )

    def format_response(self, envelope: StandardResponseEnvelope) -> Dict[str, Any]:
        """Format :class:`StandardResponseEnvelope` as widget display state.

        Args:
            envelope: Controller response envelope.

        Returns:
            Widget state dict with display-ready fields.
        """
        return {
            "widget_status": envelope.status,
            "message": envelope.message,
            "data": envelope.data,
            "current_stage": envelope.current_stage,
            "next_stage": envelope.next_stage,
            "review_created": envelope.review_created,
            "review_id": envelope.review_id,
            "review_payload": (
                envelope.review_payload.model_dump()
                if envelope.review_payload
                else None
            ),
            "audit_ref": envelope.audit_ref,
            "event_ref": envelope.event_ref,
            "warnings": envelope.warnings,
            "errors": envelope.errors,
            "governance_summary": (
                envelope.governance_summary.model_dump()
                if envelope.governance_summary
                else None
            ),
            "needs_refresh": envelope.status in ("success", "blocked"),
        }

    def action_dispatch(
        self,
        event_type: str,
        stage_name: str,
        run_id: str,
        actor_id: str,
        actor_role: str,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        review_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Convenience method for direct widget action dispatch.

        Args:
            event_type: Widget event type (e.g. ``"stage_run"``).
            stage_name: Target stage name.
            run_id: Active run identifier.
            actor_id: Actor identifier.
            actor_role: Actor role string.
            project_id: Active project identifier.
            session_id: Active session identifier.
            parameters: Action-specific parameters.
            review_id: Optional linked review ID.

        Returns:
            Widget state dict from :meth:`format_response`.
        """
        return self.dispatch({
            "event_type": event_type,
            "stage_name": stage_name,
            "run_id": run_id,
            "project_id": project_id,
            "session_id": session_id,
            "actor_id": actor_id,
            "actor_role": actor_role,
            "parameters": parameters or {},
            "review_id": review_id,
        })

    def result_refresh(self, envelope: StandardResponseEnvelope) -> Dict[str, Any]:
        """Format an envelope specifically for widget state refresh.

        Equivalent to :meth:`format_response` with a ``refresh`` flag.

        Args:
            envelope: Controller response envelope.

        Returns:
            Widget state dict with ``refresh=True``.
        """
        state = self.format_response(envelope)
        state["refresh"] = True
        return state

    def get_supported_events(self) -> List[str]:
        """Return the list of supported widget event types.

        Returns:
            List of event type strings.
        """
        return list(_WIDGET_ACTION_MAP.keys())

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _resolve_controller(self, controller_name: str) -> Any:
        dispatch = {
            "session": self._factory.session,
            "workflow": self._factory.workflow,
            "review": self._factory.review,
            "recovery": self._factory.recovery,
        }
        factory_fn = dispatch.get(controller_name)
        return factory_fn() if factory_fn else None

    def _widget_error(self, code: str, message: str) -> Dict[str, Any]:
        return {
            "widget_status": "error",
            "message": message,
            "data": None,
            "current_stage": None,
            "next_stage": None,
            "review_created": False,
            "review_id": None,
            "review_payload": None,
            "audit_ref": None,
            "event_ref": None,
            "warnings": [],
            "errors": [f"{code}: {message}"],
            "governance_summary": None,
            "needs_refresh": False,
        }
