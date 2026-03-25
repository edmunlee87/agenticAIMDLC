"""RetryPolicyResolver — resolves effective retry policy for a tool/stage."""

from __future__ import annotations

from typing import Any, Dict

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle


class RetryPolicyResolver:
    """Resolves retry policy per tool from the bundle's retry_policies config.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._bundle = bundle

    def resolve_retry_policy(self, tool_name: str = "") -> Dict[str, Any]:
        """Resolve effective retry policy for a tool.

        Falls back to default retry policy when no tool-specific rule exists.

        Args:
            tool_name: Tool name to resolve retry policy for.

        Returns:
            Dict with ``max_retries``, ``retry_delay_seconds``,
            ``retry_on_timeout``, ``retry_on_error``, and
            ``retry_mode`` (``"safe"`` | ``"risky"``).
        """
        if not self._bundle.retry_policies:
            return self._default_policy()

        section = self._bundle.retry_policies.retry_policies
        defaults = section.defaults.model_dump()

        if tool_name:
            rule = section.get_rule_for_tool(tool_name)
            if rule:
                mode = rule.retry_mode
                return {
                    "retry_mode": mode.value if hasattr(mode, "value") else str(mode),
                    "requires_idempotency_check": False,
                    "max_retries": rule.max_retries,
                    "initial_delay_ms": defaults.get("initial_delay_ms", 1000),
                    "max_delay_ms": defaults.get("max_delay_ms", 30000),
                    "jitter": defaults.get("jitter", True),
                }
        return {"retry_mode": "safe", "requires_idempotency_check": False, **defaults}

    def _default_policy(self) -> Dict[str, Any]:
        return {
            "retry_mode": "safe",
            "requires_idempotency_check": False,
            "max_retries": 3,
            "retry_delay_seconds": 2,
            "retry_on_timeout": True,
            "retry_on_error": True,
        }
