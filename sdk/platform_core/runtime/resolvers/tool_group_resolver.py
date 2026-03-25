"""ToolGroupResolver — expands tool group names into concrete tool lists."""

from __future__ import annotations

from typing import List, Set

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle


class ToolGroupResolver:
    """Expands tool group names (real and virtual) into concrete tool names.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._bundle = bundle

    def get_all_known_tools(self) -> Set[str]:
        """Return the set of all known tool names across all groups.

        Returns:
            Set of all tool name strings.
        """
        known: Set[str] = set()
        for group_def in self._bundle.tool_groups.groups.values():
            known.update(group_def.tools)
        if self._bundle.virtual_tool_groups:
            for vg in self._bundle.virtual_tool_groups.virtual_groups.values():
                for concrete_name in vg.member_groups:
                    concrete = self._bundle.tool_groups.groups.get(concrete_name)
                    if concrete:
                        known.update(concrete.tools)
        return known

    def expand_group(self, group_name: str) -> List[str]:
        """Expand a single group name to a list of tool names.

        Checks real tool groups first, then virtual tool groups (which reference
        member concrete groups).

        Args:
            group_name: Tool group name to expand.

        Returns:
            List of concrete tool names (empty if group not found).
        """
        if group_name in self._bundle.tool_groups.groups:
            return list(self._bundle.tool_groups.groups[group_name].tools)
        if (
            self._bundle.virtual_tool_groups
            and group_name in self._bundle.virtual_tool_groups.virtual_groups
        ):
            vg = self._bundle.virtual_tool_groups.virtual_groups[group_name]
            tools: List[str] = []
            seen: Set[str] = set()
            for concrete_name in vg.member_groups:
                concrete = self._bundle.tool_groups.groups.get(concrete_name)
                if concrete:
                    for t in concrete.tools:
                        if t not in seen:
                            tools.append(t)
                            seen.add(t)
            return tools
        return []

    def expand_groups(self, group_names: List[str]) -> List[str]:
        """Expand multiple group names to a deduplicated list of tool names.

        Order is preserved; duplicates are dropped.

        Args:
            group_names: Tool group names to expand.

        Returns:
            Deduplicated list of concrete tool names.
        """
        expanded: List[str] = []
        seen: Set[str] = set()
        for group_name in group_names:
            for tool in self.expand_group(group_name):
                if tool not in seen:
                    expanded.append(tool)
                    seen.add(tool)
        return expanded

    def validate_tools_exist(self, tool_names: List[str]) -> List[str]:
        """Return names from *tool_names* that are not in any known group.

        Args:
            tool_names: Tool names to validate.

        Returns:
            List of unknown tool names (empty if all are known).
        """
        known = self.get_all_known_tools()
        return [t for t in tool_names if t not in known]
