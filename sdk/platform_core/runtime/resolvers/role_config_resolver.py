"""RoleConfigResolver — resolves effective role capabilities from the bundle."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.config_models.roles import RoleCapabilityDefinition


class RoleConfigResolver:
    """Resolves effective role capabilities by merging base config with role overlays.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._bundle = bundle

    def resolve_role_config(self, actor_role: str) -> Optional[RoleCapabilityDefinition]:
        """Return the :class:`RoleCapabilityDefinition` for a role, or None.

        Args:
            actor_role: Platform role string (e.g. ``"validator"``).

        Returns:
            :class:`RoleCapabilityDefinition` or None if role is not found.
        """
        return self._bundle.role_capabilities.roles.get(actor_role)

    def get_allowed_tool_groups(self, actor_role: str) -> List[str]:
        """Return the list of allowed tool groups for an actor role.

        Args:
            actor_role: Platform role string.

        Returns:
            List of allowed group names (empty if role not found).
        """
        role_def = self.resolve_role_config(actor_role)
        return list(role_def.allowed_tool_groups) if role_def else []

    def get_blocked_tool_groups(self, actor_role: str) -> List[str]:
        """Return the list of blocked tool groups for an actor role.

        Args:
            actor_role: Platform role string.

        Returns:
            List of blocked group names (empty if role not found).
        """
        role_def = self.resolve_role_config(actor_role)
        return list(role_def.blocked_tool_groups) if role_def else []

    def get_allowed_stages(self, actor_role: str) -> List[str]:
        """Return the list of stages this role may access.

        Args:
            actor_role: Platform role string.

        Returns:
            List of stage names (empty if role not found or unrestricted).
        """
        role_def = self.resolve_role_config(actor_role)
        return list(role_def.allowed_stages) if role_def else []

    def role_can_access_stage(self, actor_role: str, stage_name: str) -> bool:
        """Return True if the role is permitted to access the stage.

        A role with an empty ``allowed_stages`` list is treated as having access
        to all stages (unrestricted).

        Args:
            actor_role: Platform role string.
            stage_name: Stage to check.

        Returns:
            True if access is permitted.
        """
        allowed = self.get_allowed_stages(actor_role)
        return (not allowed) or (stage_name in allowed)
