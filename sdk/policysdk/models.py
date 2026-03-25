"""Policy SDK data models.

:class:`PolicyRule` defines a single governance threshold or constraint.
:class:`PolicyPack` groups rules for a domain/stage combination.
:class:`PolicyFinding` is the output of a single rule evaluation.
:class:`PolicyEvaluationResult` aggregates all findings from an evaluation run.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from pydantic import ConfigDict, Field, field_validator

from sdk.platform_core.schemas.base_model_base import BaseModelBase
from sdk.platform_core.schemas.enums import PolicyResultEnum, SeverityEnum


class PolicyRuleType(str, Enum):
    """Category of the policy rule."""

    METRIC_THRESHOLD = "metric_threshold"
    MANDATORY_REVIEW = "mandatory_review"
    APPROVAL_AUTHORITY = "approval_authority"
    DATA_GOVERNANCE = "data_governance"
    MODEL_GOVERNANCE = "model_governance"
    PROCESS = "process"
    REGULATORY = "regulatory"


class PolicyFinding(BaseModelBase):
    """The output of evaluating a single :class:`PolicyRule`.

    Args:
        finding_id: Unique finding identifier.
        rule_id: Rule that produced this finding.
        rule_type: Category of the rule.
        severity: Finding severity.
        description: Human-readable finding description.
        is_breach: True when the rule threshold is breached.
        observed_value: Metric value evaluated (None for non-metric rules).
        threshold_value: Threshold that was compared against.
        is_waivable: True if this finding can be waived.
        stage_name: Stage the finding applies to.
        metric_name: Metric key evaluated.
        evaluated_at: Timestamp of evaluation.
    """

    model_config = ConfigDict(frozen=True)

    finding_id: str
    rule_id: str
    rule_type: PolicyRuleType
    severity: SeverityEnum
    description: str
    is_breach: bool
    observed_value: Optional[float] = None
    threshold_value: Optional[float] = None
    is_waivable: bool = True
    stage_name: str = ""
    metric_name: str = ""
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PolicyEvaluationResult(BaseModelBase):
    """Aggregated result of a policy evaluation run.

    Args:
        evaluation_id: Unique evaluation run identifier.
        run_id: Run this evaluation belongs to.
        project_id: Owning project.
        stage_name: Stage evaluated.
        timestamp: Evaluation timestamp.
        outcome: Overall :class:`~sdk.platform_core.schemas.enums.PolicyResultEnum`.
        findings: All individual :class:`PolicyFinding` objects.
        n_breaches: Number of breach findings.
        n_warnings: Number of non-breach warning findings.
        requires_human_review: True if any mandatory-review rule triggered.
        blocking: True if the overall outcome blocks downstream transitions.
    """

    model_config = ConfigDict(frozen=True)

    evaluation_id: str
    run_id: str
    project_id: str
    stage_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    outcome: PolicyResultEnum
    findings: List[PolicyFinding] = Field(default_factory=list)
    n_breaches: int = 0
    n_warnings: int = 0
    requires_human_review: bool = False
    blocking: bool = False


class PolicyRule(BaseModelBase):
    """A single governance rule or threshold constraint.

    Args:
        rule_id: Unique rule identifier.
        rule_type: Rule category.
        metric_name: Metric key this rule applies to (empty for non-metric rules).
        threshold: Numeric threshold value (None for non-metric rules).
        operator: Comparison operator (``gte``, ``lte``, ``gt``, ``lt``, ``eq``, ``ne``).
        severity: Severity when this rule is breached.
        description: Human-readable rule description.
        stage_scope: Stages this rule applies to (empty = all stages).
        role_scope: Roles this rule applies to (empty = all roles).
        is_mandatory_review: True if breach requires HITL review.
        is_blocking: True if breach blocks stage transition.
        is_waivable: True if a waiver can override this rule.
        environment_scope: Environments this rule applies to (empty = all).
    """

    model_config = ConfigDict(frozen=True)

    rule_id: str
    rule_type: PolicyRuleType
    metric_name: str = ""
    threshold: Optional[float] = None
    operator: str = "gte"
    severity: SeverityEnum = SeverityEnum.MEDIUM
    description: str = ""
    stage_scope: List[str] = Field(default_factory=list)
    role_scope: List[str] = Field(default_factory=list)
    is_mandatory_review: bool = False
    is_blocking: bool = False
    is_waivable: bool = True
    environment_scope: List[str] = Field(default_factory=list)

    @field_validator("operator", mode="before")
    @classmethod
    def _valid_operator(cls, v: str) -> str:
        if v not in {"gte", "lte", "gt", "lt", "eq", "ne"}:
            raise ValueError(
                f"Invalid operator '{v}'. Must be one of: gte, lte, gt, lt, eq, ne"
            )
        return v


class PolicyPack(BaseModelBase):
    """A named collection of :class:`PolicyRule` objects for a domain/stage.

    Args:
        pack_id: Unique policy pack identifier.
        name: Human-readable pack name.
        domain: Business domain (empty = generic).
        version: Pack version string.
        rules: All rules in this pack.
        description: Pack description.
    """

    model_config = ConfigDict(frozen=True)

    pack_id: str
    name: str
    domain: str = ""
    version: str = "1.0.0"
    rules: List[PolicyRule] = Field(default_factory=list)
    description: str = ""
