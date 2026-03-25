"""Reusable Pydantic fragment models used across multiple config schemas.

Fragments are small, composable sub-models embedded in larger config models.
All fragments use RuntimeConfigBase for strict validation.
"""

from typing import Dict, List, Optional

from pydantic import field_validator

from .base import RuntimeConfigBase


class FileRefMap(RuntimeConfigBase):
    """Maps logical names to file paths.

    Example:
        {"stage_registry": "configs/runtime/stage_registry.yaml"}
    """

    files: Dict[str, str]

    @field_validator("files")
    @classmethod
    def validate_non_empty(cls, v: Dict[str, str]) -> Dict[str, str]:
        if not v:
            raise ValueError("files map must not be empty")
        return v


class EnabledModules(RuntimeConfigBase):
    """Toggle list for platform feature modules.

    Example:
        {"hitl": true, "policy": true, "flow_viz": false}
    """

    modules: Dict[str, bool]


class ResolverDefaults(RuntimeConfigBase):
    """Default resolution parameters for the RuntimeResolver."""

    unknown_stage_behavior: str = "fail"
    stale_state_behavior: str = "block"
    review_missing_behavior: str = "block"
    max_skill_stack_depth: int = 8
    enable_overlay_resolution: bool = True


class StringListRule(RuntimeConfigBase):
    """A named list of string values, used for allowlists/blocklists.

    Example:
        {"name": "allowed_tools_build", "values": ["run_coarse_classing", "run_woe_iv"]}
    """

    name: str
    values: List[str]
    description: Optional[str] = None


class RouteList(RuntimeConfigBase):
    """An ordered list of stage route identifiers.

    Example:
        {"routes": ["data_readiness", "eda", "feature_engineering"]}
    """

    routes: List[str]

    @field_validator("routes")
    @classmethod
    def validate_non_empty(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("routes must not be empty")
        return v


class ToolListModel(RuntimeConfigBase):
    """A named list of tools for a tool group.

    Example:
        {"group_name": "group_a_workflow", "tools": ["bootstrap_project", "get_workflow_state"]}
    """

    group_name: str
    tools: List[str]
    description: Optional[str] = None


class StageRouteMap(RuntimeConfigBase):
    """Maps stage names to their successor routes.

    Keys are stage names; values are lists of possible successor stage names.
    """

    routes: Dict[str, List[str]]

    @field_validator("routes")
    @classmethod
    def validate_non_empty(cls, v: Dict[str, List[str]]) -> Dict[str, List[str]]:
        if not v:
            raise ValueError("stage route map must not be empty")
        return v
