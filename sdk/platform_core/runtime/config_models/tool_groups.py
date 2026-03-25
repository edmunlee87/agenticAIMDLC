"""Tool group Pydantic config models.

Tool groups are named collections of platform tools/SDK methods that can be
allowed or blocked at the stage/role level via the runtime resolver.
Groups A-H correspond to Tool calling.md from enhancement v0.3.
"""

from typing import Dict, List, Optional

from pydantic import field_validator

from .base import RuntimeConfigBase
from .enums import AccessModeEnum


class ToolGroupDefinition(RuntimeConfigBase):
    """Definition of a concrete tool group.

    Attributes:
        group_name: Unique identifier for this group (e.g. "group_a_workflow").
        description: Human-readable description of the group's purpose.
        tools: List of tool/method names in this group.
        default_access_mode: Default access mode when this group is active.
        tags: Optional categorization tags.
    """

    group_name: str
    description: Optional[str] = None
    tools: List[str]
    default_access_mode: AccessModeEnum = AccessModeEnum.BUILD_ONLY
    tags: List[str] = []

    @field_validator("tools")
    @classmethod
    def validate_non_empty(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError(f"tool group must have at least one tool")
        return v

    @field_validator("group_name")
    @classmethod
    def validate_group_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("group_name must not be blank")
        return v


class ToolGroupsConfig(RuntimeConfigBase):
    """All concrete tool group definitions, keyed by group_name.

    Loaded from configs/runtime/tool_groups.yaml.
    """

    groups: Dict[str, ToolGroupDefinition]

    @field_validator("groups")
    @classmethod
    def validate_non_empty(cls, v: Dict[str, ToolGroupDefinition]) -> Dict[str, ToolGroupDefinition]:
        if not v:
            raise ValueError("tool groups config must define at least one group")
        return v


class VirtualToolGroupDefinition(RuntimeConfigBase):
    """A virtual group that is an alias or union of one or more concrete groups.

    Useful for defining shorthand collections like "all_read_tools" or
    "governance_tools" that span multiple concrete groups.

    Attributes:
        virtual_name: Unique identifier for this virtual group.
        member_groups: List of concrete group_names included in this virtual group.
        description: Human-readable description.
    """

    virtual_name: str
    member_groups: List[str]
    description: Optional[str] = None

    @field_validator("member_groups")
    @classmethod
    def validate_non_empty(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("virtual group must reference at least one concrete group")
        return v


class VirtualToolGroupsConfig(RuntimeConfigBase):
    """All virtual tool group definitions, keyed by virtual_name.

    Loaded from configs/runtime/tool_groups.yaml under a 'virtual_groups' key.
    """

    virtual_groups: Dict[str, VirtualToolGroupDefinition] = {}
