"""Domain overlay Pydantic config models.

Domain overlays allow domain-specific adjustments to stage UI modes,
tool additions, and routing without modifying the base config.
Loaded from configs/runtime/domain_overlays/<domain>.yaml.
"""

from typing import Dict, List, Optional

from .base import RuntimeConfigBase
from .enums import DomainEnum


class DomainStageUIOverride(RuntimeConfigBase):
    """Per-stage UI override for a specific domain.

    Attributes:
        stage_name: The stage this override applies to.
        ui_mode: Override UI mode for this stage/domain combination.
        interaction_mode: Override interaction mode.
        token_mode: Override token mode.
    """

    stage_name: str
    ui_mode: Optional[str] = None
    interaction_mode: Optional[str] = None
    token_mode: Optional[str] = None


class DomainStageToolAdditions(RuntimeConfigBase):
    """Additional tool groups to expose for a stage within a domain.

    Attributes:
        stage_name: The stage this addition applies to.
        add_tool_groups: Tool groups to add for this stage.
        remove_tool_groups: Tool groups to remove for this stage.
    """

    stage_name: str
    add_tool_groups: List[str] = []
    remove_tool_groups: List[str] = []


class DomainOverlaySection(RuntimeConfigBase):
    """Container for all domain-specific overlays.

    Attributes:
        domain: The domain this overlay applies to.
        description: Human-readable description.
        ui_overrides: Per-stage UI mode overrides.
        tool_additions: Per-stage tool group additions.
        domain_stages: Stage names specific to this domain (not in base registry).
        skill_hints: Domain-level skill identifiers to prepend to the stack.
    """

    domain: DomainEnum
    description: Optional[str] = None
    ui_overrides: List[DomainStageUIOverride] = []
    tool_additions: List[DomainStageToolAdditions] = []
    domain_stages: List[str] = []
    skill_hints: List[str] = []

    def get_ui_override_map(self) -> Dict[str, DomainStageUIOverride]:
        """Return stage_name -> DomainStageUIOverride for O(1) lookup."""
        return {o.stage_name: o for o in self.ui_overrides}

    def get_tool_additions_map(self) -> Dict[str, DomainStageToolAdditions]:
        """Return stage_name -> DomainStageToolAdditions for O(1) lookup."""
        return {a.stage_name: a for a in self.tool_additions}


class DomainOverlayConfig(RuntimeConfigBase):
    """Root domain overlay config.

    Loaded from configs/runtime/domain_overlays/<domain>.yaml.
    """

    overlay: DomainOverlaySection
