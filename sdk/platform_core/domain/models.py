"""platform_core.domain.models -- domain pack contract models.

These models represent the parsed, validated in-memory representation of a
domain pack YAML file (e.g. ``configs/runtime/domain_overlays/scorecard.yaml``).

All public classes are Pydantic frozen models for immutability.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class RouteCondition(str, Enum):
    """Condition that triggers a routing rule."""
    ON_SUCCESS = "on_success"
    ON_APPROVAL = "on_approval"
    ON_REJECTION = "on_rejection"
    ON_FAILURE = "on_failure"
    ON_ESCALATION = "on_escalation"
    ALWAYS = "always"


class PolicySeverity(str, Enum):
    """Severity level of a domain policy rule."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class StageSpec(BaseModel):
    """Specification for a single stage in the domain lifecycle.

    Args:
        stage_id: Unique stage identifier.
        label: Human-readable label.
        stage_class: Stage category (``"development"``, ``"review"``, ``"governance"``, ``"terminal"``).
        requires_hitl: Whether this stage requires a human-in-the-loop review.
        governance_gate: Whether this is a governance decision gate.
        is_terminal: Whether this is a terminal (end) stage.
        tool_groups: Tool groups available in this stage.
        artifact_types: Artifact types produced by this stage.
        policy_pack_ids: Policy rule IDs that apply to this stage.
    """

    model_config = ConfigDict(frozen=True)

    stage_id: str
    label: str = ""
    stage_class: str = "development"
    requires_hitl: bool = False
    governance_gate: bool = False
    is_terminal: bool = False
    tool_groups: list[str] = Field(default_factory=list)
    artifact_types: list[str] = Field(default_factory=list)
    policy_pack_ids: list[str] = Field(default_factory=list)


class MetricSpec(BaseModel):
    """Specification for a domain performance metric.

    Args:
        metric_name: Metric identifier (e.g. ``"gini"``).
        display_name: Human-readable name.
        description: Metric description.
        higher_is_better: True if higher values are better.
        threshold_low: Minimum acceptable value (None = no bound).
        threshold_high: Maximum acceptable value (None = no bound).
        warn_threshold_low: Warn threshold for lower bound.
        dataset_splits: Dataset splits this metric applies to.
        is_primary: Whether this is the primary comparison metric.
    """

    model_config = ConfigDict(frozen=True)

    metric_name: str
    display_name: str = ""
    description: str = ""
    higher_is_better: bool = True
    threshold_low: float | None = None
    threshold_high: float | None = None
    warn_threshold_low: float | None = None
    dataset_splits: list[str] = Field(default_factory=list)
    is_primary: bool = False


class PolicyRule(BaseModel):
    """A domain-level governance policy rule.

    Args:
        rule_id: Unique rule identifier.
        name: Rule name.
        description: Rule description.
        severity: :class:`PolicySeverity`.
        applies_to_stages: Stage IDs this rule applies to.
        condition_expression: Expression string (for documentation; not evaluated here).
        requires_waiver: Whether a waiver can override a failure.
    """

    model_config = ConfigDict(frozen=True)

    rule_id: str
    name: str = ""
    description: str = ""
    severity: PolicySeverity = PolicySeverity.HIGH
    applies_to_stages: list[str] = Field(default_factory=list)
    condition_expression: str = ""
    requires_waiver: bool = False


class RoutingRule(BaseModel):
    """A routing rule between two stages.

    Args:
        from_stage: Source stage ID.
        to_stage: Target stage ID.
        condition: :class:`RouteCondition`.
        failure_stage: Stage to route to on rejection/failure (optional).
    """

    model_config = ConfigDict(frozen=True)

    from_stage: str
    to_stage: str
    condition: RouteCondition = RouteCondition.ON_SUCCESS
    failure_stage: str | None = None


class ArtifactSpec(BaseModel):
    """Specification for a domain artifact type.

    Args:
        artifact_type: Artifact type identifier.
        display_name: Human-readable name.
        produced_at_stage: Stage that produces this artifact.
        is_audit_required: Whether this artifact must be in the audit trail.
    """

    model_config = ConfigDict(frozen=True)

    artifact_type: str
    display_name: str = ""
    produced_at_stage: str = ""
    is_audit_required: bool = False


class ReviewTemplate(BaseModel):
    """Review template for a HITL governance stage.

    Args:
        template_id: Unique template identifier.
        stage_id: Stage this template applies to.
        review_type: Review type (``"approval"``, ``"selection"``, etc.).
        panel_a_evidence_types: Evidence types shown in Panel A.
        required_form_fields: Form field IDs that must be filled.
        action_types: Available action type strings.
        required_roles: Roles that must be present for submission.
    """

    model_config = ConfigDict(frozen=True)

    template_id: str
    stage_id: str = ""
    review_type: str = "approval"
    panel_a_evidence_types: list[str] = Field(default_factory=list)
    required_form_fields: list[str] = Field(default_factory=list)
    action_types: list[str] = Field(default_factory=list)
    required_roles: list[str] = Field(default_factory=list)


class DomainPackManifest(BaseModel):
    """In-memory representation of a fully-parsed domain pack.

    This is the output of :class:`~platform_core.domain.loader.DomainPackLoader`.

    Args:
        domain: Domain identifier (e.g. ``"scorecard"``).
        description: Human-readable domain description.
        model_class: Base model class (e.g. ``"credit_scorecard"``).
        regulatory_scope: Applicable regulatory frameworks.
        schema_version: Pack schema version.
        stage_registry: All stage specifications.
        routing_rules: All routing rules.
        metrics_pack: Metric specifications.
        policy_pack: Policy rules.
        artifact_pack: Artifact specifications.
        review_templates: Review templates for HITL stages.
        skill_pack: Skill configuration dict.
        test_pack: Test configuration dict.
    """

    model_config = ConfigDict(frozen=True)

    domain: str
    description: str = ""
    model_class: str = ""
    regulatory_scope: list[str] = Field(default_factory=list)
    schema_version: str = "1.0.0"
    stage_registry: list[StageSpec] = Field(default_factory=list)
    routing_rules: list[RoutingRule] = Field(default_factory=list)
    metrics_pack: list[MetricSpec] = Field(default_factory=list)
    policy_pack: list[PolicyRule] = Field(default_factory=list)
    artifact_pack: list[ArtifactSpec] = Field(default_factory=list)
    review_templates: list[ReviewTemplate] = Field(default_factory=list)
    skill_pack: dict[str, Any] = Field(default_factory=dict)
    test_pack: dict[str, Any] = Field(default_factory=dict)

    # ------------------------------------------------------------------
    # Derived views
    # ------------------------------------------------------------------

    @property
    def governance_gate_stages(self) -> list[str]:
        """Return IDs of stages that are governance gates."""
        return [s.stage_id for s in self.stage_registry if s.governance_gate]

    @property
    def hitl_stages(self) -> list[str]:
        """Return IDs of stages that require HITL review."""
        return [s.stage_id for s in self.stage_registry if s.requires_hitl]

    def get_primary_metric(self) -> MetricSpec | None:
        """Return the primary performance metric.

        Returns:
            :class:`MetricSpec` with ``is_primary=True``, or None.
        """
        return next((m for m in self.metrics_pack if m.is_primary), None)

    def get_routing_rule(
        self,
        from_stage: str,
        condition: RouteCondition,
    ) -> RoutingRule | None:
        """Return the routing rule for a given source stage and condition.

        Args:
            from_stage: Source stage ID.
            condition: :class:`RouteCondition`.

        Returns:
            :class:`RoutingRule` or None.
        """
        return next(
            (r for r in self.routing_rules if r.from_stage == from_stage and r.condition == condition),
            None,
        )

    def get_review_template(self, stage_id: str) -> ReviewTemplate | None:
        """Return the review template for a HITL stage.

        Args:
            stage_id: Stage identifier.

        Returns:
            :class:`ReviewTemplate` or None.
        """
        return next((t for t in self.review_templates if t.stage_id == stage_id), None)

    def get_next_stage(self, from_stage: str) -> str | None:
        """Return the next stage on success routing.

        Args:
            from_stage: Source stage ID.

        Returns:
            Target stage ID or None.
        """
        rule = self.get_routing_rule(from_stage, RouteCondition.ON_SUCCESS)
        return rule.to_stage if rule else None
