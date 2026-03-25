"""Tool group and allowlist config models.

A ``ToolGroupConfig`` defines a named, versioned set of SDK/tool identifiers.
``ToolAllowlistConfig`` assembles these groups into per-stage or per-role allowlists.
"""

from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from platform_core.runtime.config_models.base import ConfigModelBase
from platform_core.runtime.config_models.fragments import RetryConfig


class ToolGroupConfig(ConfigModelBase):
    """A named group of SDK or tool identifiers.

    Args:
        group_id: Unique identifier for this tool group.
        description: Human-readable description.
        tool_ids: List of SDK/tool identifiers included in this group.
        retry_config: Optional retry policy applied to all tools in this group.
        deprecated: Mark as deprecated; resolving this group emits a warning.
    """

    group_id: str
    description: str = ""
    tool_ids: list[str] = Field(default_factory=list)
    retry_config: RetryConfig = Field(default_factory=RetryConfig)
    deprecated: bool = False

    @field_validator("group_id", mode="before")
    @classmethod
    def _non_empty_id(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("group_id must be non-empty")
        return v

    @field_validator("tool_ids", mode="before")
    @classmethod
    def _unique_tool_ids(cls, v: list[str]) -> list[str]:
        if len(v) != len(set(v)):
            raise ValueError("tool_ids must not contain duplicates")
        return v


class ToolAllowlistConfig(ConfigModelBase):
    """Resolved allowlist: groups included, groups excluded, and explicit overrides.

    Args:
        include_groups: Tool group IDs to include.
        exclude_groups: Tool group IDs to exclude (takes precedence over include).
        explicit_allow: Individual tool IDs to always allow regardless of groups.
        explicit_block: Individual tool IDs to always block regardless of groups.
    """

    include_groups: list[str] = Field(default_factory=list)
    exclude_groups: list[str] = Field(default_factory=list)
    explicit_allow: list[str] = Field(default_factory=list)
    explicit_block: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _no_overlap_in_explicit(self) -> "ToolAllowlistConfig":
        overlap = set(self.explicit_allow) & set(self.explicit_block)
        if overlap:
            raise ValueError(
                f"Tools appear in both explicit_allow and explicit_block: {sorted(overlap)}"
            )
        return self
