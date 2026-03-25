"""UI mode, interaction mode, and token mode Pydantic config models.

Defines the configuration for each mode including display properties,
default settings, and usage constraints.
"""

from typing import Dict, List, Optional

from pydantic import field_validator

from .base import RuntimeConfigBase
from .enums import InteractionModeEnum, TokenModeEnum, UIModeEnum


class UIModeDefinition(RuntimeConfigBase):
    """Definition of a UI layout mode.

    Attributes:
        mode: The UI mode identifier.
        description: Human-readable description.
        panels: Panels visible in this mode.
        default_for_stage_classes: Stage classes that default to this mode.
        token_budget_hint: Recommended token budget mode for this UI mode.
    """

    mode: UIModeEnum
    description: Optional[str] = None
    panels: List[str] = []
    default_for_stage_classes: List[str] = []
    token_budget_hint: Optional[TokenModeEnum] = None


class UIModesConfig(RuntimeConfigBase):
    """All UI mode definitions, keyed by mode name.

    Loaded from configs/runtime/ui_modes.yaml.
    """

    modes: Dict[str, UIModeDefinition]

    @field_validator("modes")
    @classmethod
    def validate_non_empty(cls, v: Dict[str, UIModeDefinition]) -> Dict[str, UIModeDefinition]:
        if not v:
            raise ValueError("ui modes config must define at least one mode")
        return v


class InteractionModeDefinition(RuntimeConfigBase):
    """Definition of an interaction mode.

    Attributes:
        mode: The interaction mode identifier.
        description: Human-readable description.
        allowed_actions: Actions permitted in this mode.
        requires_structured_input: Whether free-text only is rejected.
        default_for_stage_classes: Stage classes that default to this mode.
    """

    mode: InteractionModeEnum
    description: Optional[str] = None
    allowed_actions: List[str] = []
    requires_structured_input: bool = False
    default_for_stage_classes: List[str] = []


class InteractionModesConfig(RuntimeConfigBase):
    """All interaction mode definitions, keyed by mode name.

    Loaded from configs/runtime/interaction_modes.yaml.
    """

    modes: Dict[str, InteractionModeDefinition]

    @field_validator("modes")
    @classmethod
    def validate_non_empty(cls, v: Dict[str, InteractionModeDefinition]) -> Dict[str, InteractionModeDefinition]:
        if not v:
            raise ValueError("interaction modes config must define at least one mode")
        return v


class TokenModeDefinition(RuntimeConfigBase):
    """Definition of a token budget mode.

    Attributes:
        mode: The token mode identifier.
        description: Human-readable description.
        max_prompt_tokens: Maximum tokens for prompts in this mode.
        max_completion_tokens: Maximum tokens for completions.
        enable_compression: Whether context compression is applied.
        retrieval_top_k: Top-k retrieval limit for RAG in this mode.
    """

    mode: TokenModeEnum
    description: Optional[str] = None
    max_prompt_tokens: int = 4096
    max_completion_tokens: int = 1024
    enable_compression: bool = False
    retrieval_top_k: int = 5

    @field_validator("max_prompt_tokens", "max_completion_tokens")
    @classmethod
    def validate_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("token limits must be positive integers")
        return v


class TokenModesConfig(RuntimeConfigBase):
    """All token mode definitions, keyed by mode name.

    Loaded from configs/runtime/token_modes.yaml.
    """

    modes: Dict[str, TokenModeDefinition]

    @field_validator("modes")
    @classmethod
    def validate_non_empty(cls, v: Dict[str, TokenModeDefinition]) -> Dict[str, TokenModeDefinition]:
        if not v:
            raise ValueError("token modes config must define at least one mode")
        return v
