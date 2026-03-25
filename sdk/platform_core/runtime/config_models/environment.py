"""Environment overlay Pydantic config models.

Environment overlays adjust platform behavior per deployment environment
(dev/uat/prod). Production environments enforce all governance gates;
dev environments may relax some gates with mandatory audit logging.
Loaded from configs/runtime/environment_overlays/<env>.yaml.
"""

from typing import Dict, List, Optional

from pydantic import field_validator, model_validator

from .base import RuntimeConfigBase
from .enums import EnvironmentNameEnum


class EnvironmentStrictness(RuntimeConfigBase):
    """Strictness settings per environment.

    Attributes:
        enforce_all_governance_gates: If True, all gates are enforced unconditionally.
        allow_auto_continue_on_warn: Allow auto-continue when result is 'warn' (not breach).
        require_policy_acknowledgment: Require actors to acknowledge policy findings.
        strict_audit_chain: Enforce preceding_audit_id chain (fail if missing).
    """

    enforce_all_governance_gates: bool = True
    allow_auto_continue_on_warn: bool = False
    require_policy_acknowledgment: bool = True
    strict_audit_chain: bool = True


class EnvironmentRetries(RuntimeConfigBase):
    """Per-environment retry setting overrides.

    Attributes:
        max_retries_override: Override max retries for all tools.
        retry_mode_override: Override retry mode for all tools.
    """

    max_retries_override: Optional[int] = None
    retry_mode_override: Optional[str] = None

    @field_validator("max_retries_override")
    @classmethod
    def validate_non_negative(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError("max_retries_override must be >= 0")
        return v


class EnvironmentBlockRules(RuntimeConfigBase):
    """Actions/tools that are hard-blocked in this environment.

    Attributes:
        blocked_tools: Tool names blocked in this environment.
        blocked_actions: Interaction actions blocked in this environment.
        blocked_stage_classes: Stage class types blocked in this environment.
    """

    blocked_tools: List[str] = []
    blocked_actions: List[str] = []
    blocked_stage_classes: List[str] = []


class EnvironmentUIDefaults(RuntimeConfigBase):
    """Default UI/interaction/token mode overrides for this environment.

    Attributes:
        default_ui_mode: Override default UI mode.
        default_interaction_mode: Override default interaction mode.
        default_token_mode: Override default token mode.
    """

    default_ui_mode: Optional[str] = None
    default_interaction_mode: Optional[str] = None
    default_token_mode: Optional[str] = None


class EnvironmentOverlaySection(RuntimeConfigBase):
    """Container for all environment-specific settings.

    Attributes:
        environment: The target deployment environment.
        description: Human-readable description.
        strictness: Governance enforcement strictness.
        retries: Retry behavior overrides.
        block_rules: Hard-block rules.
        ui_defaults: Default UI mode overrides.
    """

    environment: EnvironmentNameEnum
    description: Optional[str] = None
    strictness: EnvironmentStrictness = EnvironmentStrictness()
    retries: EnvironmentRetries = EnvironmentRetries()
    block_rules: EnvironmentBlockRules = EnvironmentBlockRules()
    ui_defaults: EnvironmentUIDefaults = EnvironmentUIDefaults()

    @model_validator(mode="after")
    def validate_prod_strictness(self) -> "EnvironmentOverlaySection":
        if self.environment == EnvironmentNameEnum.PROD:
            if not self.strictness.enforce_all_governance_gates:
                raise ValueError(
                    "PROD environment must have enforce_all_governance_gates=True"
                )
            if not self.strictness.strict_audit_chain:
                raise ValueError(
                    "PROD environment must have strict_audit_chain=True"
                )
        return self


class EnvironmentOverlayConfig(RuntimeConfigBase):
    """Root environment overlay config.

    Loaded from configs/runtime/environment_overlays/<env>.yaml.
    """

    overlay: EnvironmentOverlaySection
