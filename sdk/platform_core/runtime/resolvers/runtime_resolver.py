"""RuntimeResolver — top-level orchestrator for runtime context resolution.

Produces a :class:`ResolvedStack` containing the full effective runtime
configuration for a given (stage, actor_role, access_mode, environment) context.
All sub-resolvers are composed here.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.resolvers.allowlist_resolver import AllowlistResolver
from sdk.platform_core.runtime.resolvers.governance_rule_resolver import GovernanceRuleResolver
from sdk.platform_core.runtime.resolvers.retry_policy_resolver import RetryPolicyResolver
from sdk.platform_core.runtime.resolvers.role_config_resolver import RoleConfigResolver
from sdk.platform_core.runtime.resolvers.tool_group_resolver import ToolGroupResolver
from sdk.platform_core.runtime.resolvers.ui_mode_resolver import UIModeResolver

logger = logging.getLogger(__name__)


@dataclass
class ResolvedStack:
    """Final resolved runtime context for a stage+role combination.

    Attributes:
        stage_name: Stage this context was resolved for.
        actor_role: Actor role this context was resolved for.
        allowed_tools: Effective list of permitted tool names.
        blocked_tools: Effective list of blocked tool names.
        ui_mode: Resolved UI layout mode string.
        interaction_mode: Resolved interaction mode string.
        token_mode: Recommended token budget mode (or None).
        governance_flags: Effective governance settings dict.
        retry_policy: Effective retry policy dict.
        next_stages: List of possible next stage names from routing config.
        stage_class: Stage class string.
        access_mode: Resolved access mode string.
        environment: Deployment environment used during resolution.
        meta: Additional metadata for debug/audit.
    """

    stage_name: str
    actor_role: str
    allowed_tools: List[str] = field(default_factory=list)
    blocked_tools: List[str] = field(default_factory=list)
    ui_mode: str = "minimal"
    interaction_mode: str = "chat"
    token_mode: Optional[str] = None
    governance_flags: Dict[str, Any] = field(default_factory=dict)
    retry_policy: Dict[str, Any] = field(default_factory=dict)
    next_stages: List[str] = field(default_factory=list)
    stage_class: Optional[str] = None
    access_mode: Optional[str] = None
    environment: str = "dev"
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the :class:`ResolvedStack` to a plain dict.

        Returns:
            Dict with all resolved fields.
        """
        return {
            "stage_name": self.stage_name,
            "actor_role": self.actor_role,
            "allowed_tools": self.allowed_tools,
            "blocked_tools": self.blocked_tools,
            "ui_mode": self.ui_mode,
            "interaction_mode": self.interaction_mode,
            "token_mode": self.token_mode,
            "governance_flags": self.governance_flags,
            "retry_policy": self.retry_policy,
            "next_stages": self.next_stages,
            "stage_class": self.stage_class,
            "access_mode": self.access_mode,
            "environment": self.environment,
            "meta": self.meta,
        }


class RuntimeResolver:
    """Top-level resolver that orchestrates all sub-resolvers.

    Produces a :class:`ResolvedStack` for the given runtime context.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        environment: Deployment environment (affects governance strictness).

    Example::

        resolver = RuntimeResolver(bundle=bundle, environment="production")
        stack = resolver.resolve(
            stage_name="feature_engineering",
            actor_role="developer",
        )
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        environment: str = "dev",
    ) -> None:
        self._bundle = bundle
        self._environment = environment
        self._role_resolver = RoleConfigResolver(bundle)
        self._tool_resolver = ToolGroupResolver(bundle)
        self._allowlist_resolver = AllowlistResolver(bundle)
        self._governance_resolver = GovernanceRuleResolver(bundle, environment)
        self._retry_resolver = RetryPolicyResolver(bundle)
        self._ui_resolver = UIModeResolver(bundle)

    def resolve(
        self,
        stage_name: str,
        actor_role: str,
        runtime_facts: Optional[Dict[str, Any]] = None,
    ) -> ResolvedStack:
        """Resolve the full runtime context for a stage+actor_role pair.

        Args:
            stage_name: Target stage name.
            actor_role: Actor's role string.
            runtime_facts: Optional dict of runtime state flags used for
                conditional governance rule evaluation (e.g.
                ``{"has_active_review": True, "access_mode": "review_only"}``).

        Returns:
            :class:`ResolvedStack` with all resolved fields.
        """
        facts: Dict[str, Any] = runtime_facts or {}
        facts.setdefault("stage_name", stage_name)

        # --- Step 1: tool allowlist ---
        allowed_tools = self._allowlist_resolver.resolve(actor_role, stage_name)
        blocked_tools = self._allowlist_resolver.resolve_blocked(actor_role, stage_name)

        # --- Step 2: apply conditional governance rules (may adjust tool lists) ---
        conditional_result = self._governance_resolver.apply_conditional_rules(
            runtime_facts=facts,
            allowed_tools=allowed_tools,
            blocked_tools=blocked_tools,
        )
        allowed_tools = conditional_result["allowed_tools"]
        blocked_tools = conditional_result["blocked_tools"]

        # --- Step 3: governance flags ---
        governance_flags = self._governance_resolver.get_stage_governance(stage_name)

        # --- Step 4: retry policy ---
        retry_policy = self._retry_resolver.resolve_retry_policy()

        # --- Step 5: UI + interaction + token modes ---
        ui_mode = self._ui_resolver.resolve_ui_mode(stage_name)
        interaction_mode = self._ui_resolver.resolve_interaction_mode(stage_name)
        token_mode = self._ui_resolver.resolve_token_mode(stage_name)

        # --- Step 6: next stages from routes ---
        next_stages = self._resolve_next_stages(stage_name)

        # --- Step 7: stage metadata ---
        stage_class, access_mode = self._resolve_stage_meta(stage_name)

        logger.debug(
            "RuntimeResolver resolved stack",
            extra={
                "stage_name": stage_name,
                "actor_role": actor_role,
                "environment": self._environment,
                "allowed_tool_count": len(allowed_tools),
                "blocked_tool_count": len(blocked_tools),
            },
        )

        return ResolvedStack(
            stage_name=stage_name,
            actor_role=actor_role,
            allowed_tools=allowed_tools,
            blocked_tools=blocked_tools,
            ui_mode=ui_mode,
            interaction_mode=interaction_mode,
            token_mode=token_mode,
            governance_flags=governance_flags,
            retry_policy=retry_policy,
            next_stages=next_stages,
            stage_class=stage_class,
            access_mode=access_mode,
            environment=self._environment,
            meta={
                "resolved_with_facts": bool(runtime_facts),
                "has_conditional_rules": bool(
                    self._bundle.governance_overlays
                    and self._bundle.governance_overlays.governance.conditional_rules
                ),
            },
        )

    def _resolve_next_stages(self, stage_name: str) -> List[str]:
        """Collect candidate next stages from the workflow routes config.

        Args:
            stage_name: Current stage.

        Returns:
            Deduplicated list of next stage names.
        """
        route = self._bundle.workflow_routes.routes.get(stage_name)
        if route is None:
            return []
        candidates: List[Optional[str]] = [
            route.on_success,
            route.on_review_required,
            route.on_pass,
            route.on_fail,
            route.on_approved,
            route.on_rejected,
            route.on_auto_continue,
            route.on_remediation_required,
        ]
        seen: Dict[str, bool] = {}
        result: List[str] = []
        for c in candidates:
            if c and c not in seen:
                seen[c] = True
                result.append(c)
        return result

    def _resolve_stage_meta(self, stage_name: str) -> tuple[Optional[str], Optional[str]]:
        """Return (stage_class, default_access_mode) for the stage.

        Args:
            stage_name: Stage to look up.

        Returns:
            Tuple of (stage_class_str, access_mode_str), each None if not found.
        """
        if not self._bundle.stage_registry:
            return None, None
        stage_def = self._bundle.stage_registry.stages.get(stage_name)
        if stage_def is None:
            return None, None
        sc = stage_def.stage_class
        am = stage_def.default_access_mode
        return (
            sc.value if hasattr(sc, "value") else str(sc),
            am.value if hasattr(am, "value") else str(am),
        )
