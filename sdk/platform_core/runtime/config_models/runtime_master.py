"""RuntimeMasterConfig Pydantic models.

Defines the top-level runtime master configuration that ties together
environment, behavior defaults, and file references.
"""

from typing import Optional

from pydantic import field_validator

from .base import RuntimeConfigBase
from .enums import EnvironmentNameEnum, UnknownBehaviorEnum, StaleStateBehaviorEnum, ReviewMissingBehaviorEnum
from .fragments import EnabledModules, FileRefMap, ResolverDefaults


class RuntimeMasterSection(RuntimeConfigBase):
    """Core section of the runtime master config.

    Attributes:
        environment: Target deployment environment.
        runtime_mode: Overall runtime mode (development, validation, etc.).
        schema_version: Version of the config schema.
        description: Human-readable description.
    """

    environment: EnvironmentNameEnum = EnvironmentNameEnum.DEV
    runtime_mode: str = "development"
    schema_version: str = "1.0.0"
    description: Optional[str] = None
    unknown_stage_behavior: UnknownBehaviorEnum = UnknownBehaviorEnum.FAIL
    stale_state_behavior: StaleStateBehaviorEnum = StaleStateBehaviorEnum.BLOCK
    review_missing_behavior: ReviewMissingBehaviorEnum = ReviewMissingBehaviorEnum.BLOCK

    @field_validator("schema_version")
    @classmethod
    def validate_semver(cls, v: str) -> str:
        parts = v.split(".")
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            raise ValueError(f"schema_version must be semver (X.Y.Z), got: {v!r}")
        return v


class RuntimeMasterConfig(RuntimeConfigBase):
    """Root runtime master configuration loaded from runtime_master.yaml.

    Attributes:
        runtime: Core runtime behavior section.
        modules: Enabled/disabled platform modules.
        file_refs: Logical name -> file path mapping for all config files.
        resolver_defaults: Default resolver behavior parameters.
    """

    runtime: RuntimeMasterSection
    modules: Optional[EnabledModules] = None
    file_refs: Optional[FileRefMap] = None
    resolver_defaults: Optional[ResolverDefaults] = None
