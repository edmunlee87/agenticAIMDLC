"""Centralized enumeration definitions shared across all MDLC SDK packages.

All enums are string-valued for JSON-serialization compatibility. Extend existing
enums in platform_contracts rather than defining local ones in individual SDKs.
"""

from enum import Enum


class StageStatus(str, Enum):
    """Lifecycle status of a workflow stage."""

    NOT_STARTED = "not_started"
    RUNNING = "running"
    WAITING_REVIEW = "waiting_review"
    WAITING_SELECTION = "waiting_selection"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class WorkflowMode(str, Enum):
    """Top-level workflow operating mode."""

    DEVELOPMENT = "development"
    VALIDATION = "validation"
    MONITORING = "monitoring"
    ANNUAL_REVIEW = "annual_review"
    REMEDIATION = "remediation"
    GENERIC = "generic"


class RoleType(str, Enum):
    """Recognised actor roles in the MDLC framework."""

    MODEL_DEVELOPER = "model_developer"
    MODEL_VALIDATOR = "model_validator"
    MODEL_OWNER = "model_owner"
    RISK_MANAGER = "risk_manager"
    COMPLIANCE_OFFICER = "compliance_officer"
    DATA_STEWARD = "data_steward"
    AUDITOR = "auditor"
    SYSTEM = "system"


class AuditType(str, Enum):
    """Type of audit record written by the audit SDK."""

    DECISION = "decision"
    APPROVAL = "approval"
    EXCEPTION = "exception"
    SIGNOFF = "signoff"
    OVERRIDE = "override"
    WAIVER = "waiver"
    ESCALATION = "escalation"
    CONFIG_CHANGE = "config_change"


class GovernanceSeverity(str, Enum):
    """Severity level for policy findings, violations, and risk flags."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PolicyCheckResult(str, Enum):
    """Aggregate outcome of a policy evaluation run."""

    PASS = "pass"
    WARN = "warn"
    BREACH = "breach"
    BLOCKED = "blocked"


class ReviewType(str, Enum):
    """Recognised HITL review types at governance gates."""

    INITIAL_SCOPING = "initial_scoping"
    DATA_SELECTION = "data_selection"
    FEATURE_SELECTION = "feature_selection"
    MODEL_SELECTION = "model_selection"
    VALIDATION_SIGN_OFF = "validation_sign_off"
    FINAL_APPROVAL = "final_approval"
    EXCEPTION_APPROVAL = "exception_approval"
    MONITORING_REVIEW = "monitoring_review"
    REMEDIATION_SIGN_OFF = "remediation_sign_off"
    ANNUAL_REVIEW_SIGN_OFF = "annual_review_sign_off"
    GENERIC = "generic"


class CandidateType(str, Enum):
    """Type of versioned candidate snapshot."""

    MODEL = "model"
    FEATURE_SET = "feature_set"
    BIN_DEFINITION = "bin_definition"
    THRESHOLD_SET = "threshold_set"
    METHODOLOGY_SNAPSHOT = "methodology_snapshot"
    PARAMETER_SET = "parameter_set"


class InteractionType(str, Enum):
    """Type of interaction payload sent by a UI or agent."""

    STAGE_ACTION = "stage_action"
    REVIEW_RESPONSE = "review_response"
    RECOVERY_CHOICE = "recovery_choice"
    SESSION_COMMAND = "session_command"
    QUERY = "query"


class UIMode(str, Enum):
    """Display mode for the UI layer."""

    BOOTSTRAP = "bootstrap"
    STAGE_PROGRESS = "stage_progress"
    REVIEW_3PANEL = "review_3panel"
    SELECTION_CARDS = "selection_cards"
    RECOVERY_PROMPT = "recovery_prompt"
    READONLY = "readonly"
    IDLE = "idle"


class InteractionMode(str, Enum):
    """Human interaction requirement for the current stage."""

    NONE = "none"
    NOTIFY = "notify"
    REVIEW_REQUIRED = "review_required"
    SELECTION_REQUIRED = "selection_required"
    RECOVERY_REQUIRED = "recovery_required"
    APPROVAL_REQUIRED = "approval_required"


class TokenMode(str, Enum):
    """Agent token budget mode."""

    MICRO = "micro"
    STANDARD = "standard"
    DEEP_REVIEW = "deep_review"


class EnvironmentType(str, Enum):
    """Deployment environment."""

    DEV = "dev"
    TEST = "test"
    UAT = "uat"
    PRODUCTION = "production"
