"""Role configuration models.

A ``RoleConfig`` defines capabilities, tool access, and governance gates for
a named actor role. All roles are configured in ``configs/runtime/roles.yaml``
and validated by this model.
"""

from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from platform_core.runtime.config_models.base import ConfigModelBase
from platform_core.runtime.config_models.fragments import ApprovalAuthorityConfig
from platform_core.runtime.config_models.tool_groups import ToolAllowlistConfig


class RoleCapabilityConfig(ConfigModelBase):
    """Per-stage capability flags for a role.

    Args:
        stage_name: The stage this capability block applies to.
        can_execute: Whether this role may trigger automated stage execution.
        can_review: Whether this role may perform HITL reviews.
        can_approve: Whether this role may approve governance gates.
        can_override: Whether this role may issue governance overrides.
        can_waive: Whether this role may grant policy waivers.
        access_mode: Effective access mode for this role at this stage.
    """

    stage_name: str
    can_execute: bool = False
    can_review: bool = False
    can_approve: bool = False
    can_override: bool = False
    can_waive: bool = False
    access_mode: str = "READ_ONLY"


class RoleConfig(ConfigModelBase):
    """Full configuration for a named actor role.

    Args:
        role_id: Unique role identifier (matches RoleType enum values).
        display_name: Human-readable name.
        description: Role description.
        tool_allowlist: SDK/tool allowlist for this role.
        stage_capabilities: Per-stage capability flags.
        default_approval_authority: Default approval authority for governance gates.
        can_delegate: Whether this role may delegate their authority.
        max_delegation_depth: Maximum delegation chain length. Default: 2.
    """

    role_id: str
    display_name: str = ""
    description: str = ""
    tool_allowlist: ToolAllowlistConfig = Field(default_factory=ToolAllowlistConfig)
    stage_capabilities: list[RoleCapabilityConfig] = Field(default_factory=list)
    default_approval_authority: ApprovalAuthorityConfig | None = None
    can_delegate: bool = False
    max_delegation_depth: int = 2

    @field_validator("role_id", mode="before")
    @classmethod
    def _non_empty_id(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("role_id must be non-empty")
        return v

    @field_validator("max_delegation_depth", mode="before")
    @classmethod
    def _delegation_depth_range(cls, v: int) -> int:
        if not (0 <= v <= 10):
            raise ValueError("max_delegation_depth must be between 0 and 10")
        return v

    @model_validator(mode="after")
    def _unique_stage_capabilities(self) -> "RoleConfig":
        seen: set[str] = set()
        for cap in self.stage_capabilities:
            if cap.stage_name in seen:
                raise ValueError(
                    f"Duplicate stage_capabilities entry for stage '{cap.stage_name}' "
                    f"in role '{self.role_id}'"
                )
            seen.add(cap.stage_name)
        return self


class RolesConfig(ConfigModelBase):
    """Top-level wrapper for the roles YAML config file.

    Args:
        version: Config file version.
        roles: Map of role_id -> RoleConfig.
    """

    version: str = "1.0.0"
    roles: dict[str, RoleConfig] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _keys_match_role_ids(self) -> "RolesConfig":
        for key, role in self.roles.items():
            if key != role.role_id:
                raise ValueError(
                    f"Roles dict key '{key}' does not match role_id '{role.role_id}'"
                )
        return self
