"""Centralized common enums for the platform domain layer.

These enums are separate from the config_models enums (which are for config
validation). These are the domain/business enums used in payloads, results,
registry entries, and observability events.

All enums are str-based for JSON serialization compatibility.
"""

from enum import Enum


class StatusEnum(str, Enum):
    """Standard result/operation status."""

    SUCCESS = "success"
    WARNING = "warning"
    FAILURE = "failure"
    BLOCKED = "blocked"
    PENDING = "pending"
    REVIEW_REQUIRED = "review_required"


class ReviewStatusEnum(str, Enum):
    """HITL review lifecycle status."""

    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    APPROVED_WITH_CHANGES = "approved_with_changes"
    REJECTED = "rejected"
    RERUN_REQUESTED = "rerun_requested"
    ESCALATED = "escalated"
    CANCELLED = "cancelled"


class ActionEnum(str, Enum):
    """Bounded user actions in interaction payloads."""

    APPROVE = "approve"
    APPROVE_WITH_CHANGES = "approve_with_changes"
    REJECT = "reject"
    RERUN_WITH_PARAMETERS = "rerun_with_parameters"
    REQUEST_MORE_ANALYSIS = "request_more_analysis"
    ESCALATE = "escalate"
    DROP_VARIABLE = "drop_variable"
    APPROVE_VERSION = "approve_version"
    APPROVE_VERSION_WITH_OVERRIDES = "approve_version_with_overrides"
    CREATE_COMPOSITE_VERSION = "create_composite_version"
    RUN_STAGE = "run_stage"
    RESUME_SESSION = "resume_session"
    CREATE_SESSION = "create_session"
    APPLY_RECOVERY = "apply_recovery"
    ACKNOWLEDGE_WARNING = "acknowledge_warning"


class SeverityEnum(str, Enum):
    """Severity levels for findings, warnings, and policy violations."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ConclusionCategoryEnum(str, Enum):
    """Validation conclusion categories."""

    PASS = "pass"
    PASS_WITH_CONDITIONS = "pass_with_conditions"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"
    REFER_BACK = "refer_back"


class WorkflowModeEnum(str, Enum):
    """Overall workflow execution mode."""

    DEVELOPMENT = "development"
    VALIDATION = "validation"
    MONITORING = "monitoring"
    REMEDIATION = "remediation"
    COMMITTEE_REVIEW = "committee_review"


class RoleEnum(str, Enum):
    """Platform actor role."""

    DEVELOPER = "developer"
    VALIDATOR = "validator"
    GOVERNANCE = "governance"
    APPROVER = "approver"
    MONITORING = "monitoring"
    REMEDIATION = "remediation"
    SYSTEM = "system"
    REVIEWER = "reviewer"


class DomainEnum(str, Enum):
    """Model development domain."""

    SCORECARD = "scorecard"
    TIME_SERIES = "time_series"
    ECL = "ecl"
    LGD = "lgd"
    PD = "pd"
    EAD = "ead"
    SICR = "sicr"
    STRESS = "stress"
    GENERIC = "generic"


class UIModeDomainEnum(str, Enum):
    """UI layout mode."""

    THREE_PANEL_REVIEW_WORKSPACE = "three_panel_review_workspace"
    VALIDATION_REVIEW_WORKSPACE = "validation_review_workspace"
    DASHBOARD_REVIEW_WORKSPACE = "dashboard_review_workspace"
    BOOTSTRAP_WORKSPACE = "bootstrap_workspace"
    RECOVERY_WORKSPACE = "recovery_workspace"
    MONITORING_WORKSPACE = "monitoring_workspace"
    READ_ONLY_WORKSPACE = "read_only_workspace"


class InteractionModeDomainEnum(str, Enum):
    """Interaction pattern mode."""

    EDIT_AND_FINALIZE = "edit_and_finalize"
    REVIEW_AND_CONCLUDE = "review_and_conclude"
    TRIAGE_AND_DISPOSITION = "triage_and_disposition"
    REVIEW_AND_APPROVE = "review_and_approve"
    RECOVERY_DECISION = "recovery_decision"
    READ_ONLY = "read_only"


class TokenModeDomainEnum(str, Enum):
    """Token budget mode."""

    FULL = "full"
    COMPACT = "compact"
    MINIMAL = "minimal"
    ROUTING_ONLY = "routing_only"


class AccessModeEnum(str, Enum):
    """Stage access mode."""

    READ_ONLY = "READ_ONLY"
    BUILD_ONLY = "BUILD_ONLY"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    FINALIZATION_GATED = "FINALIZATION_GATED"
    MONITORING_OPERATIONAL = "MONITORING_OPERATIONAL"


class AuditTypeEnum(str, Enum):
    """Audit record type."""

    DECISION = "decision"
    APPROVAL = "approval"
    EXCEPTION = "exception"
    SIGNOFF = "signoff"
    OVERRIDE = "override"
    WAIVER = "waiver"
    ESCALATION = "escalation"
    CONFIG_CHANGE = "config_change"


class EventTypeEnum(str, Enum):
    """Observability event type."""

    SKILL_STARTED = "skill_started"
    SKILL_COMPLETED = "skill_completed"
    SKILL_FAILED = "skill_failed"
    STAGE_STARTED = "stage_started"
    STAGE_COMPLETED = "stage_completed"
    STAGE_FAILED = "stage_failed"
    STAGE_TRANSITION = "stage_transition"
    HITL_REVIEW_CREATED = "hitl_review_created"
    HITL_USER_RESPONDED = "hitl_user_responded"
    HITL_REVIEW_COMPLETED = "hitl_review_completed"
    CANDIDATE_VERSION_CREATED = "candidate_version_created"
    VERSION_SELECTION_CREATED = "version_selection_created"
    ARTIFACT_REGISTERED = "artifact_registered"
    WORKFLOW_BLOCKED = "workflow_blocked"
    WORKFLOW_RESUMED = "workflow_resumed"
    OVERRIDE_LOGGED = "override_logged"
    RERUN_REQUESTED = "rerun_requested"
    RECOVERY_ACTION_STARTED = "recovery_action_started"
    RECOVERY_ACTION_COMPLETED = "recovery_action_completed"
    RECOVERY_ACTION_FAILED = "recovery_action_failed"
    CONFIG_LOADED = "config_loaded"
    POLICY_EVALUATED = "policy_evaluated"
    GOVERNANCE_GATE_TRIGGERED = "governance_gate_triggered"
    SESSION_CREATED = "session_created"
    SESSION_RESUMED = "session_resumed"
    SESSION_SUSPENDED = "session_suspended"
    SESSION_CLOSED = "session_closed"


class PolicyResultEnum(str, Enum):
    """Policy evaluation overall result."""

    PASS = "pass"
    WARN = "warn"
    BREACH = "breach"
    BLOCKED = "blocked"


class StageStatusEnum(str, Enum):
    """Workflow stage status."""

    NOT_STARTED = "not_started"
    RUNNING = "running"
    WAITING_REVIEW = "waiting_review"
    WAITING_SELECTION = "waiting_selection"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class RecoveryActionEnum(str, Enum):
    """Recovery action types."""

    RETRY = "retry"
    RERUN = "rerun"
    ROLLBACK = "rollback"
    ESCALATE = "escalate"
    RESUME = "resume"
    SKIP = "skip"
    MANUAL = "manual"


class NodeStatusEnum(str, Enum):
    """Flow visualization node status."""

    NOT_STARTED = "not_started"
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_INPUT = "waiting_input"
    WAITING_REVIEW = "waiting_review"
    COMPLETED = "completed"
    COMPLETED_WITH_WARNING = "completed_with_warning"
    FAILED = "failed"
    SKIPPED = "skipped"
    APPROVED = "approved"
    REJECTED = "rejected"
