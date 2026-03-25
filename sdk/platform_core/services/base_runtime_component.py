"""BaseRuntimeComponent: foundation for all runtime resolver sub-components.

Each runtime resolver sub-component (RoleConfigResolver, ToolGroupResolver,
GovernanceRuleResolver, etc.) extends this base and implements the resolve method.

Design rules:
- Each sub-component resolves one specific concern from the runtime context.
- Sub-components are composable: RuntimeResolver orchestrates them sequentially.
- Sub-components never modify state; they return a decision dict.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..schemas.payload_models import ResolvedStack, RuntimeContext


class BaseRuntimeComponent(ABC):
    """Root base for all runtime resolver sub-components.

    Provides _validate_runtime_context and _build_runtime_decision helpers.

    Args:
        component_name: Name of this component (e.g. "role_config_resolver").
        config: Optional config bundle or config section.
        logger: Optional logger override.
    """

    def __init__(
        self,
        component_name: str,
        config: Optional[Any] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._component_name = component_name
        self._config = config
        self._logger = logger or logging.getLogger(f"platform.runtime.{component_name}")

    @abstractmethod
    def resolve(self, context: RuntimeContext, partial_stack: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve this component's contribution to the runtime decision.

        Receives the current context and the partially-built resolved stack dict
        from prior components. Returns updates to the partial stack.

        Args:
            context: The incoming RuntimeContext.
            partial_stack: Partially constructed resolved stack from prior components.

        Returns:
            Dict of updates to apply to the partial resolved stack.
        """

    def _validate_runtime_context(self, context: RuntimeContext) -> Optional[str]:
        """Validate that the runtime context has the minimum required fields.

        Returns an error message if invalid; None if valid.

        Args:
            context: The runtime context to validate.

        Returns:
            Error message string if invalid, None if valid.
        """
        if not context.context_id:
            return "context_id is required"
        if not context.run_id:
            return "run_id is required"
        if not context.current_stage:
            return "current_stage is required"
        if not context.actor or not context.actor.actor_id:
            return "actor.actor_id is required"
        return None

    def _build_runtime_decision(
        self,
        allowed_tools: list,
        blocked_tools: list,
        resolved_skills: list,
        ui_contract: Dict[str, Any],
        response_contract: Dict[str, Any],
        governance_constraints: Dict[str, Any],
        retry_policy: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build a standardized runtime decision dict.

        Args:
            allowed_tools: Final list of allowed tool names.
            blocked_tools: List of blocked tool names.
            resolved_skills: Ordered list of resolved skill identifiers.
            ui_contract: UI mode and interaction mode recommendations.
            response_contract: HITL/approval/audit requirements.
            governance_constraints: Active governance constraints.
            retry_policy: Effective retry policy.

        Returns:
            Runtime decision dict conforming to the ResolvedStack schema.
        """
        return {
            "sdk_allowlist": allowed_tools,
            "blocked_tools": blocked_tools,
            "resolved_skills": resolved_skills,
            "ui_contract": ui_contract,
            "response_contract": response_contract,
            "governance_constraints": governance_constraints,
            "retry_policy": retry_policy,
        }
