"""AgentBridge — translates LLM tool calls to platform interactions.

Components:
- ``tool_adapter``: maps tool call name + args to InteractionPayload action
- ``agent_context_builder``: extracts actor, run_id, stage from tool call context
- ``response_normalizer``: formats StandardResponseEnvelope into LLM-consumable dict
- ``retry_policy``: applies bridge-level retry for transient tool-call failures

Design rule: AgentBridge only exposes a *bounded* set of SDK actions per stage.
All exposed actions must be in the resolved_stack allowed_tools for the current context.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from sdk.platform_core.bridges.base_bridge import BaseBridge
from sdk.platform_core.schemas.common_fragments import ActorRecord
from sdk.platform_core.schemas.payload_models import (
    InteractionPayload,
    StandardResponseEnvelope,
)
from sdk.platform_core.schemas.utilities import IDFactory


# Mapping from agent tool-call names to controller + action pairs.
_TOOL_ACTION_MAP: Dict[str, Dict[str, str]] = {
    "platform_open_session": {"controller": "session", "action": "open_session"},
    "platform_resume_session": {"controller": "session", "action": "resume_session"},
    "platform_run_stage": {"controller": "workflow", "action": "run_stage"},
    "platform_complete_stage": {"controller": "workflow", "action": "complete_stage"},
    "platform_fail_stage": {"controller": "workflow", "action": "fail_stage"},
    "platform_route_next": {"controller": "workflow", "action": "route_next"},
    "platform_open_review": {"controller": "review", "action": "open_review"},
    "platform_get_review_payload": {"controller": "review", "action": "get_review_payload"},
    "platform_submit_review_action": {"controller": "review", "action": "submit_review_action"},
    "platform_get_recovery_options": {"controller": "recovery", "action": "get_recovery_options"},
    "platform_apply_recovery": {"controller": "recovery", "action": "apply_recovery"},
}


class AgentBridge(BaseBridge):
    """Bridge for LLM agent tool calls.

    Translates structured tool call dicts (from LLM function-calling)
    into :class:`InteractionPayload` and returns LLM-consumable JSON.

    Expected ``raw_input`` format::

        {
            "tool_name": "platform_run_stage",
            "args": {
                "stage_name": "feature_engineering",
                "run_id": "run_abc123",
                "project_id": "proj_xyz",
                "actor_id": "agent_01",
                "actor_role": "developer",
                "parameters": {...}
            }
        }

    Args:
        controller_factory: :class:`ControllerFactory` instance.
        max_retries: Number of retries on transient failures.
        retry_delay_seconds: Delay between retries.
        logger: Optional logger override.
    """

    def __init__(
        self,
        controller_factory: Any,
        max_retries: int = 2,
        retry_delay_seconds: float = 1.0,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        super().__init__(controller_factory=controller_factory, logger=logger)
        self._max_retries = max_retries
        self._retry_delay_seconds = retry_delay_seconds

    def dispatch(self, raw_input: Any) -> Dict[str, Any]:
        """Translate a tool call dict and dispatch to the appropriate controller.

        Args:
            raw_input: Tool call dict with ``tool_name`` and ``args``.

        Returns:
            Normalized dict response for the LLM.
        """
        if not isinstance(raw_input, dict):
            return self._error_response("invalid_input", "raw_input must be a dict.")

        tool_name = raw_input.get("tool_name", "")
        args = raw_input.get("args", {})

        mapping = _TOOL_ACTION_MAP.get(tool_name)
        if mapping is None:
            return self._error_response(
                "unknown_tool",
                f"Tool '{tool_name}' is not exposed by AgentBridge. "
                f"Available: {list(_TOOL_ACTION_MAP.keys())}",
            )

        try:
            payload = self.build_payload(raw_input)
        except Exception as exc:
            return self._error_response("payload_build_failed", str(exc))

        controller = self._resolve_controller(mapping["controller"])
        if controller is None:
            return self._error_response("controller_unavailable", f"Controller '{mapping['controller']}' unavailable.")

        envelope = self._dispatch_with_retry(controller, payload)
        return self.format_response(envelope)

    def build_payload(self, raw_input: Any) -> InteractionPayload:
        """Build :class:`InteractionPayload` from a tool call dict.

        Args:
            raw_input: Tool call dict.

        Returns:
            :class:`InteractionPayload`.

        Raises:
            ValueError: If required fields are missing.
        """
        tool_name = raw_input.get("tool_name", "")
        args: Dict[str, Any] = raw_input.get("args", {})

        mapping = _TOOL_ACTION_MAP.get(tool_name)
        if mapping is None:
            raise ValueError(f"Unknown tool_name: {tool_name!r}")

        actor_id = args.get("actor_id") or "agent"
        actor_role = args.get("actor_role") or "developer"
        stage_name = args.get("stage_name") or ""
        if not stage_name:
            raise ValueError("stage_name is required in tool call args.")

        actor = self._build_actor(
            actor_id=actor_id,
            role=actor_role,
            display_name=args.get("actor_display_name"),
        )

        return self._build_interaction_payload(
            stage_name=stage_name,
            interaction_type="agent_tool_call",
            action=mapping["action"],
            actor=actor,
            run_id=args.get("run_id"),
            project_id=args.get("project_id"),
            session_id=args.get("session_id"),
            trace_id=args.get("trace_id"),
            correlation_id=args.get("correlation_id"),
            parameters=args.get("parameters"),
            review_id=args.get("review_id"),
            policy_acknowledgments=args.get("policy_acknowledgments"),
        )

    def format_response(self, envelope: StandardResponseEnvelope) -> Dict[str, Any]:
        """Normalize :class:`StandardResponseEnvelope` to an LLM-consumable dict.

        Args:
            envelope: Controller response envelope.

        Returns:
            Normalized dict with ``status``, ``message``, ``data``, ``hints``.
        """
        return {
            "status": envelope.status,
            "message": envelope.message,
            "data": envelope.data,
            "next_stage": envelope.next_stage,
            "review_created": envelope.review_created,
            "review_id": envelope.review_id,
            "audit_ref": envelope.audit_ref,
            "event_ref": envelope.event_ref,
            "warnings": envelope.warnings,
            "errors": envelope.errors,
            "agent_hint": envelope.agent_hint or "",
            "workflow_hint": envelope.workflow_hint or "",
            "governance_summary": (
                envelope.governance_summary.model_dump()
                if envelope.governance_summary
                else None
            ),
        }

    def get_tool_manifest(self) -> List[Dict[str, Any]]:
        """Return the list of exposed platform tools for LLM function-calling.

        Returns:
            List of tool descriptor dicts (tool_name, description, parameters).
        """
        return [
            {
                "tool_name": tool_name,
                "controller": mapping["controller"],
                "action": mapping["action"],
            }
            for tool_name, mapping in _TOOL_ACTION_MAP.items()
        ]

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

    def _dispatch_with_retry(
        self,
        controller: Any,
        payload: InteractionPayload,
    ) -> StandardResponseEnvelope:
        attempts = 0
        last_envelope: Optional[StandardResponseEnvelope] = None
        while attempts <= self._max_retries:
            try:
                envelope = controller.handle(payload)
                if envelope.status != "error" or attempts >= self._max_retries:
                    return envelope
                last_envelope = envelope
            except Exception as exc:
                self._logger.warning(
                    "AgentBridge dispatch attempt %d failed: %s", attempts + 1, exc
                )
                last_envelope = None
            attempts += 1
            if attempts <= self._max_retries:
                time.sleep(self._retry_delay_seconds)

        if last_envelope is not None:
            return last_envelope
        # If we get here (only via exception path), build a generic error envelope.
        from sdk.platform_core.schemas.payload_models import StandardResponseEnvelope as SRE
        from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider
        return SRE(
            envelope_id=IDFactory.envelope_id(),
            status="error",
            message="AgentBridge: all retry attempts exhausted.",
            sdk_name="agent_bridge",
            function_name="dispatch",
            run_id=payload.run_id or "",
            timestamp=TimeProvider.now_iso(),
        )

    def _error_response(self, code: str, message: str) -> Dict[str, Any]:
        return {
            "status": "error",
            "message": message,
            "data": None,
            "next_stage": None,
            "review_created": False,
            "review_id": None,
            "audit_ref": None,
            "event_ref": None,
            "warnings": [],
            "errors": [f"{code}: {message}"],
            "agent_hint": "Fix the input and retry.",
            "workflow_hint": "",
            "governance_summary": None,
        }
