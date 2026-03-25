"""Config-specific enumerations for the runtime config pack.

These extend the platform_contracts enums with config-system-specific values
that only make sense within the Pydantic config layer.
"""

from enum import Enum


class BackoffMode(str, Enum):
    """Retry backoff strategy."""

    FIXED = "fixed"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    JITTER = "jitter"


class AccessMode(str, Enum):
    """Effective access mode resolved for a stage/role combination."""

    READ_ONLY = "READ_ONLY"
    BUILD_ONLY = "BUILD_ONLY"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    FINALIZATION_GATED = "FINALIZATION_GATED"
    MONITORING_OPERATIONAL = "MONITORING_OPERATIONAL"


class PolicyMode(str, Enum):
    """Policy enforcement mode."""

    STRICT = "strict"
    ADVISORY = "advisory"
    AUDIT_ONLY = "audit_only"
    DISABLED = "disabled"


class SkillResolutionLayer(str, Enum):
    """Ordered layers in skill stack resolution."""

    BASE = "base"
    ROLE = "role"
    DOMAIN = "domain"
    STAGE = "stage"
    OVERLAY = "overlay"
    SUPPORT = "support"


class ConfigLoadSource(str, Enum):
    """Source of a loaded config value -- used in audit log entries."""

    FILE = "file"
    ENV = "env"
    CLI = "cli"
    DEFAULT = "default"
    OVERLAY = "overlay"
