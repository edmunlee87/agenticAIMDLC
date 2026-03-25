"""UI and interaction mode config models.

Defines valid UI modes, interaction modes, and their per-stage token budgets.
Loaded from ``configs/runtime/ui.yaml``.
"""

from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from platform_contracts.enums import InteractionMode, TokenMode, UIMode
from platform_core.runtime.config_models.base import ConfigModelBase
from platform_core.runtime.config_models.fragments import TokenBudget


class StageUIModeConfig(ConfigModelBase):
    """UI mode configuration for a specific stage.

    Args:
        stage_name: MDLC stage this config applies to.
        ui_mode: Default UI mode for this stage.
        interaction_mode: Required human interaction level.
        token_mode: Default token budget mode.
        display_sections: Ordered list of UI section identifiers to render.
        requires_human_action: Shortcut flag -- True when interaction_mode
            requires human input (review, selection, or approval).
    """

    stage_name: str
    ui_mode: UIMode = UIMode.STAGE_PROGRESS
    interaction_mode: InteractionMode = InteractionMode.NONE
    token_mode: TokenMode = TokenMode.STANDARD
    display_sections: list[str] = Field(default_factory=list)
    requires_human_action: bool = False

    @model_validator(mode="after")
    def _sync_requires_human_action(self) -> "StageUIModeConfig":
        blocking_modes = {
            InteractionMode.REVIEW_REQUIRED,
            InteractionMode.SELECTION_REQUIRED,
            InteractionMode.RECOVERY_REQUIRED,
            InteractionMode.APPROVAL_REQUIRED,
        }
        # Derive requires_human_action from interaction_mode when not explicitly set.
        # Since model is frozen after creation, use object.__setattr__.
        if self.interaction_mode in blocking_modes:
            object.__setattr__(self, "requires_human_action", True)
        return self


class TokenBudgetsByMode(ConfigModelBase):
    """Token budget configuration indexed by TokenMode.

    Args:
        micro: Budget for micro mode (quick agent calls).
        standard: Budget for standard mode.
        deep_review: Budget for deep review mode.
    """

    micro: TokenBudget = Field(default_factory=lambda: TokenBudget(context_tokens=500, completion_tokens=300, total_tokens=1000))
    standard: TokenBudget = Field(default_factory=lambda: TokenBudget(context_tokens=2000, completion_tokens=1000, total_tokens=4000))
    deep_review: TokenBudget = Field(default_factory=lambda: TokenBudget(context_tokens=6000, completion_tokens=3000, total_tokens=10000))


class UIConfig(ConfigModelBase):
    """Top-level UI configuration.

    Args:
        version: Config file version.
        token_budgets: Token budgets per mode.
        stage_ui_modes: Per-stage UI mode configurations.
        default_ui_mode: Fallback UI mode when no stage-specific config exists.
        default_interaction_mode: Fallback interaction mode.
        default_token_mode: Fallback token mode.
    """

    version: str = "1.0.0"
    token_budgets: TokenBudgetsByMode = Field(default_factory=TokenBudgetsByMode)
    stage_ui_modes: list[StageUIModeConfig] = Field(default_factory=list)
    default_ui_mode: UIMode = UIMode.STAGE_PROGRESS
    default_interaction_mode: InteractionMode = InteractionMode.NONE
    default_token_mode: TokenMode = TokenMode.STANDARD

    @model_validator(mode="after")
    def _unique_stage_configs(self) -> "UIConfig":
        seen: set[str] = set()
        for cfg in self.stage_ui_modes:
            if cfg.stage_name in seen:
                raise ValueError(
                    f"Duplicate stage_ui_modes entry for stage '{cfg.stage_name}'"
                )
            seen.add(cfg.stage_name)
        return self
