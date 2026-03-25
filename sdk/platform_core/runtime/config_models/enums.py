"""All 13 runtime configuration enums.

These enums are used across Pydantic config models, YAML config validation,
and runtime resolution. They represent every categorical axis in the runtime
decision matrix.
"""

from enum import Enum


class AccessModeEnum(str, Enum):
    """Controls what operations are permitted in a given stage/role context."""

    READ_ONLY = "READ_ONLY"
    BUILD_ONLY = "BUILD_ONLY"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    FINALIZATION_GATED = "FINALIZATION_GATED"
    MONITORING_OPERATIONAL = "MONITORING_OPERATIONAL"


class UIModeEnum(str, Enum):
    """UI layout mode presented to the user."""

    THREE_PANEL_REVIEW_WORKSPACE = "three_panel_review_workspace"
    VALIDATION_REVIEW_WORKSPACE = "validation_review_workspace"
    DASHBOARD_REVIEW_WORKSPACE = "dashboard_review_workspace"
    BOOTSTRAP_WORKSPACE = "bootstrap_workspace"
    RECOVERY_WORKSPACE = "recovery_workspace"
    MONITORING_WORKSPACE = "monitoring_workspace"
    READ_ONLY_WORKSPACE = "read_only_workspace"


class InteractionModeEnum(str, Enum):
    """Interaction pattern for the current session/stage."""

    EDIT_AND_FINALIZE = "edit_and_finalize"
    REVIEW_AND_CONCLUDE = "review_and_conclude"
    TRIAGE_AND_DISPOSITION = "triage_and_disposition"
    REVIEW_AND_APPROVE = "review_and_approve"
    RECOVERY_DECISION = "recovery_decision"
    READ_ONLY = "read_only"


class TokenModeEnum(str, Enum):
    """Token budget mode for LLM/agent calls."""

    FULL = "full"
    COMPACT = "compact"
    MINIMAL = "minimal"
    ROUTING_ONLY = "routing_only"


class RuntimeModeEnum(str, Enum):
    """Overall runtime execution mode."""

    DEVELOPMENT = "development"
    VALIDATION = "validation"
    GOVERNANCE = "governance"
    MONITORING = "monitoring"
    REMEDIATION = "remediation"
    RECOVERY = "recovery"


class UnknownBehaviorEnum(str, Enum):
    """Behavior when an unknown stage or tool is encountered."""

    FAIL = "fail"
    WARN = "warn"
    SKIP = "skip"


class StaleStateBehaviorEnum(str, Enum):
    """Behavior when workflow state is detected as stale."""

    BLOCK = "block"
    WARN = "warn"
    AUTO_RESUME = "auto_resume"


class ReviewMissingBehaviorEnum(str, Enum):
    """Behavior when a required review is missing."""

    BLOCK = "block"
    ESCALATE = "escalate"
    WARN = "warn"


class EnvironmentNameEnum(str, Enum):
    """Deployment environment name."""

    DEV = "dev"
    UAT = "uat"
    PROD = "prod"
    STAGING = "staging"


class StageClassEnum(str, Enum):
    """Broad classification of a stage by its governance characteristics."""

    BUILD = "build"
    REVIEW = "review"
    SELECTION = "selection"
    APPROVAL = "approval"
    MONITORING = "monitoring"
    REMEDIATION = "remediation"
    VALIDATION = "validation"
    BOOTSTRAP = "bootstrap"
    RECOVERY = "recovery"


class DomainEnum(str, Enum):
    """Model domain / use-case type."""

    SCORECARD = "scorecard"
    TIME_SERIES = "time_series"
    ECL = "ecl"
    LGD = "lgd"
    PD = "pd"
    EAD = "ead"
    SICR = "sicr"
    STRESS = "stress"
    GENERIC = "generic"


class ActorRoleEnum(str, Enum):
    """Actor role in the platform."""

    DEVELOPER = "developer"
    VALIDATOR = "validator"
    GOVERNANCE = "governance"
    APPROVER = "approver"
    MONITORING = "monitoring"
    REMEDIATION = "remediation"
    SYSTEM = "system"
    REVIEWER = "reviewer"


class RetryModeEnum(str, Enum):
    """Retry behavior for tools/skills."""

    NONE = "none"
    FIXED = "fixed"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    MANUAL = "manual"
