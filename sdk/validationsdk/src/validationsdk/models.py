"""validationsdk.models -- immutable data contracts for the validation lifecycle.

Covers:
- :class:`ValidationScope` -- what is being validated and who owns it.
- :class:`FindingSeverity` -- enumerated severity levels.
- :class:`FindingStatus` -- lifecycle status of a finding.
- :class:`ValidationFinding` -- a single validation finding (immutable).
- :class:`ConclusionCategory` -- outcome categories.
- :class:`ValidationConclusion` -- final conclusion record (immutable).
- :class:`RemediationStatus` -- lifecycle of a remediation action.
- :class:`RemediationAction` -- a single remediation action record.
- :class:`EvidenceRecord` -- evidence submitted to support a scope.
- :class:`ValidationRun` -- top-level record for a validation run.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FindingSeverity(str, Enum):
    """Severity level of a validation finding."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class FindingStatus(str, Enum):
    """Lifecycle status of a validation finding."""

    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    REMEDIATED = "remediated"
    WAIVED = "waived"
    CLOSED = "closed"


class ConclusionCategory(str, Enum):
    """Final outcome category of a validation run."""

    PASS_UNCONDITIONAL = "pass_unconditional"
    PASS_WITH_CONDITIONS = "pass_with_conditions"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"
    ESCALATED = "escalated"


class RemediationStatus(str, Enum):
    """Lifecycle of a remediation action."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED_NOT_FIXED = "closed_not_fixed"


class ValidationScope(BaseModel):
    """Defines the scope of a validation exercise.

    Args:
        scope_id: Unique scope identifier.
        run_id: Associated MDLC run.
        project_id: Associated project.
        model_type: Domain model type being validated (e.g. ``"scorecard"``).
        validation_type: Type of validation (e.g. ``"development"``, ``"annual_review"``).
        in_scope_stages: Stage IDs included in this validation exercise.
        out_of_scope_stages: Stages explicitly excluded.
        validator_ids: Actor IDs of assigned validators.
        approver_ids: Actor IDs of validation approvers.
        created_at: Creation timestamp.
        created_by: Actor who created the scope.
        policy_pack_ids: Policy packs applicable to this scope.
        metadata: Arbitrary additional scope metadata.
    """

    model_config = ConfigDict(frozen=True)

    scope_id: str
    run_id: str
    project_id: str
    model_type: str = "generic"
    validation_type: str = "development"
    in_scope_stages: list[str] = Field(default_factory=list)
    out_of_scope_stages: list[str] = Field(default_factory=list)
    validator_ids: list[str] = Field(default_factory=list)
    approver_ids: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""
    policy_pack_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("scope_id", "run_id", "project_id", mode="before")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("scope_id, run_id, and project_id must be non-empty")
        return v


class EvidenceRecord(BaseModel):
    """Evidence submitted to support a validation scope.

    Args:
        evidence_id: Unique evidence identifier.
        scope_id: Scope this evidence belongs to.
        artifact_id: Backing artifact ID (from artifactsdk).
        evidence_type: Category (e.g. ``"test_result"``, ``"metric_pack"``,
            ``"dq_report"``, ``"model_card"``).
        stage_name: Stage that produced this evidence.
        submitted_by: Actor who submitted the evidence.
        submitted_at: Submission timestamp.
        summary: Brief human-readable summary.
        is_sufficient: Whether this evidence alone satisfies a requirement.
        metadata: Additional evidence metadata.
    """

    model_config = ConfigDict(frozen=True)

    evidence_id: str
    scope_id: str
    artifact_id: str
    evidence_type: str
    stage_name: str = ""
    submitted_by: str = ""
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    summary: str = ""
    is_sufficient: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class ValidationFinding(BaseModel):
    """A single immutable validation finding.

    Args:
        finding_id: Unique, stable finding identifier.
        scope_id: Validation scope this finding belongs to.
        run_id: MDLC run.
        project_id: Project.
        finding_type: Category (e.g. ``"model_performance"``, ``"data_quality"``,
            ``"governance_gap"``, ``"documentation"``).
        severity: :class:`FindingSeverity`.
        status: :class:`FindingStatus`.
        stage_name: Stage where the finding was raised.
        title: Short descriptive title.
        description: Detailed description of the finding.
        evidence_refs: Evidence artifact IDs supporting this finding.
        raised_by: Actor who raised the finding.
        raised_at: When the finding was raised.
        policy_rule_refs: Policy rule IDs that triggered this finding.
        requires_remediation: Whether remediation is mandatory before conclusion.
        waiver_eligible: Whether a waiver may close this finding.
        metadata: Additional metadata.
    """

    model_config = ConfigDict(frozen=True)

    finding_id: str
    scope_id: str
    run_id: str
    project_id: str
    finding_type: str
    severity: FindingSeverity = FindingSeverity.MEDIUM
    status: FindingStatus = FindingStatus.OPEN
    stage_name: str = ""
    title: str
    description: str = ""
    evidence_refs: list[str] = Field(default_factory=list)
    raised_by: str = ""
    raised_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    policy_rule_refs: list[str] = Field(default_factory=list)
    requires_remediation: bool = False
    waiver_eligible: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class RemediationAction(BaseModel):
    """A single immutable remediation action record.

    Args:
        action_id: Unique action identifier.
        finding_id: Finding this action remediates.
        scope_id: Scope.
        run_id: MDLC run.
        project_id: Project.
        description: What was done.
        assigned_to: Actor responsible.
        status: :class:`RemediationStatus`.
        created_at: When the action was created.
        resolved_at: When the action was resolved (if applicable).
        resolution_notes: Notes on how the finding was resolved.
        evidence_artifact_ids: Artifacts produced as part of this remediation.
    """

    model_config = ConfigDict(frozen=True)

    action_id: str
    finding_id: str
    scope_id: str
    run_id: str
    project_id: str
    description: str
    assigned_to: str = ""
    status: RemediationStatus = RemediationStatus.OPEN
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: datetime | None = None
    resolution_notes: str = ""
    evidence_artifact_ids: list[str] = Field(default_factory=list)


class ValidationConclusion(BaseModel):
    """Final immutable validation conclusion record.

    Args:
        conclusion_id: Unique conclusion identifier.
        scope_id: Scope this conclusion closes.
        run_id: MDLC run.
        project_id: Project.
        category: :class:`ConclusionCategory`.
        summary: Human-readable conclusion summary.
        conditions: List of conditions imposed (for PASS_WITH_CONDITIONS).
        open_findings_count: Number of open findings at conclusion time.
        critical_findings_count: Critical findings count.
        concluded_by: Actor who drew the conclusion.
        concluded_at: Conclusion timestamp.
        audit_id: Audit record ID backing this conclusion.
        evidence_completeness_score: 0.0–1.0 score of evidence coverage.
        metadata: Additional conclusion metadata.
    """

    model_config = ConfigDict(frozen=True)

    conclusion_id: str
    scope_id: str
    run_id: str
    project_id: str
    category: ConclusionCategory
    summary: str = ""
    conditions: list[str] = Field(default_factory=list)
    open_findings_count: int = 0
    critical_findings_count: int = 0
    concluded_by: str = ""
    concluded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    audit_id: str = ""
    evidence_completeness_score: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("evidence_completeness_score", mode="before")
    @classmethod
    def _valid_score(cls, v: float) -> float:
        if not (0.0 <= float(v) <= 1.0):
            raise ValueError("evidence_completeness_score must be between 0.0 and 1.0")
        return v


class ValidationRun(BaseModel):
    """Top-level record grouping scope, evidence, findings, and conclusion.

    Args:
        validation_run_id: Unique validation run ID.
        scope: The :class:`ValidationScope`.
        evidence_ids: Evidence record IDs collected.
        finding_ids: Finding IDs raised.
        conclusion: The :class:`ValidationConclusion` (None if not yet concluded).
        status: Overall status (``"in_progress"`` | ``"concluded"`` | ``"failed"``).
        created_at: When the validation run started.
    """

    model_config = ConfigDict(frozen=True)

    validation_run_id: str
    scope: ValidationScope
    evidence_ids: list[str] = Field(default_factory=list)
    finding_ids: list[str] = Field(default_factory=list)
    conclusion: ValidationConclusion | None = None
    status: str = "in_progress"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
