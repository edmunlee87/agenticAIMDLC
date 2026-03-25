"""AllowlistResolver — computes effective tool allowlist for a role+stage combo.

Intersects role-level allowed groups and stage-level allowed/blocked groups to
produce a concrete set of permitted tool names.
"""

from __future__ import annotations

from typing import List, Set

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.resolvers.role_config_resolver import RoleConfigResolver
from sdk.platform_core.runtime.resolvers.tool_group_resolver import ToolGroupResolver


class AllowlistResolver:
    """Resolves effective tool allowlist for a (role, stage) pair.

    Computation:
        1. Expand role-level ``allowed_tool_groups`` → role_allowed_tools
        2. Expand stage-level ``allowed_groups`` from StageToolMatrix → stage_allowed_tools
        3. intersect to find effective_allowed_tools
        4. Subtract anything in role-level or stage-level ``blocked_tool_groups``

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._bundle = bundle
        self._role_resolver = RoleConfigResolver(bundle)
        self._tool_resolver = ToolGroupResolver(bundle)

    def resolve(self, actor_role: str, stage_name: str) -> List[str]:
        """Return sorted list of tools allowed for a role in a stage.

        Args:
            actor_role: Platform role string.
            stage_name: Stage to resolve tools for.

        Returns:
            Sorted list of allowed tool name strings.
        """
        allowed_tools = self._compute_allowed(actor_role, stage_name)
        blocked_tools = self._compute_blocked(actor_role, stage_name)
        effective = sorted(allowed_tools - blocked_tools)
        return effective

    def resolve_blocked(self, actor_role: str, stage_name: str) -> List[str]:
        """Return sorted list of tools blocked for a role in a stage.

        Args:
            actor_role: Platform role string.
            stage_name: Stage to resolve blocked tools for.

        Returns:
            Sorted list of blocked tool name strings.
        """
        return sorted(self._compute_blocked(actor_role, stage_name))

    def _compute_allowed(self, actor_role: str, stage_name: str) -> Set[str]:
        role_groups = self._role_resolver.get_allowed_tool_groups(actor_role)
        role_tools: Set[str] = set(self._tool_resolver.expand_groups(role_groups))

        stage_tools: Set[str] = self._get_stage_allowed_tools(stage_name)

        # When role defines tool groups: intersect with stage.
        # When role has no tool-group constraints: use stage set only.
        if role_tools:
            return role_tools & stage_tools if stage_tools else role_tools
        return stage_tools

    def _compute_blocked(self, actor_role: str, stage_name: str) -> Set[str]:
        role_blocked_groups = self._role_resolver.get_blocked_tool_groups(actor_role)
        role_blocked: Set[str] = set(self._tool_resolver.expand_groups(role_blocked_groups))

        stage_blocked: Set[str] = self._get_stage_blocked_tools(stage_name)
        return role_blocked | stage_blocked

    def _get_stage_allowed_tools(self, stage_name: str) -> Set[str]:
        if not self._bundle.stage_tool_matrix:
            return set()
        entry = self._bundle.stage_tool_matrix.matrix.get(stage_name)
        if entry is None:
            return set()
        return set(self._tool_resolver.expand_groups(entry.allowed_groups))

    def _get_stage_blocked_tools(self, stage_name: str) -> Set[str]:
        if not self._bundle.stage_tool_matrix:
            return set()
        entry = self._bundle.stage_tool_matrix.matrix.get(stage_name)
        if entry is None:
            return set()
        return set(self._tool_resolver.expand_groups(entry.blocked_groups))
