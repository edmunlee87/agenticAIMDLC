"""Role capability and overlay Pydantic config models.

Defines what each actor role can do: which tool groups are allowed,
which stages they can act in, and governance authority levels.
"""

from typing import Dict, List, Optional

from pydantic import field_validator, model_validator

from .base import RuntimeConfigBase
from .enums import AccessModeEnum, ActorRoleEnum


class RoleCapabilityDefinition(RuntimeConfigBase):
    """Capability definition for a single actor role.

    Attributes:
        role: The actor role this definition applies to.
        description: Human-readable description of the role.
        allowed_tool_groups: Tool groups this role may access by default.
        blocked_tool_groups: Tool groups explicitly blocked for this role.
        allowed_stages: Stage names this role may act in. Empty = all stages.
        can_approve: Whether this role has approval authority.
        can_signoff: Whether this role can issue final sign-offs.
        min_approval_authority: Minimum authority level for approval actions.
        can_escalate: Whether this role can escalate reviews.
        can_waive_policy: Whether this role can issue policy waivers.
    """

    role: ActorRoleEnum
    description: Optional[str] = None
    allowed_tool_groups: List[str] = []
    blocked_tool_groups: List[str] = []
    allowed_stages: List[str] = []
    can_approve: bool = False
    can_signoff: bool = False
    min_approval_authority: Optional[str] = None
    can_escalate: bool = True
    can_waive_policy: bool = False

    @model_validator(mode="after")
    def validate_no_overlap(self) -> "RoleCapabilityDefinition":
        overlap = set(self.allowed_tool_groups) & set(self.blocked_tool_groups)
        if overlap:
            raise ValueError(
                f"Role {self.role}: tool groups cannot be both allowed and blocked: {overlap}"
            )
        return self


class RoleCapabilitiesConfig(RuntimeConfigBase):
    """All role capability definitions, keyed by role name.

    Loaded from configs/runtime/role_capabilities.yaml.
    """

    roles: Dict[str, RoleCapabilityDefinition]

    @field_validator("roles")
    @classmethod
    def validate_non_empty(cls, v: Dict[str, RoleCapabilityDefinition]) -> Dict[str, RoleCapabilityDefinition]:
        if not v:
            raise ValueError("role capabilities config must define at least one role")
        return v


class RoleOverlaySection(RuntimeConfigBase):
    """Per-role tool group and stage overrides applied on top of base capabilities.

    Attributes:
        role: The role this overlay applies to.
        add_tool_groups: Tool groups added by this overlay.
        remove_tool_groups: Tool groups removed by this overlay.
        add_allowed_stages: Additional stages added by this overlay.
    """

    role: ActorRoleEnum
    add_tool_groups: List[str] = []
    remove_tool_groups: List[str] = []
    add_allowed_stages: List[str] = []
    override_access_mode: Optional[AccessModeEnum] = None


class RoleOverlayConfig(RuntimeConfigBase):
    """Collection of role overlays for a domain or environment.

    Loaded from configs/runtime/role_overlays/<role_name>.yaml.
    """

    overlays: List[RoleOverlaySection] = []
