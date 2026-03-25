"""platform_core.domain.models -- domain pack contract data models.

Every domain pack is expressed as a :class:`DomainPackManifest` that is
loaded from a YAML file conforming to ``configs/schemas/domain_pack_contract.yaml``.

These models are intentionally schema-first: they mirror the YAML structure
exactly so that YAML ↔ Pydantic round-trips are lossless.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StageClass(str, Enum):
    """Broad class of a domain stage."""
    DEVELOPMENT = "development"
    REVIEW = "review"
    GOVERNANCE = "governance"
    TERMINAL = "terminal"


class RouteCondition(str, Enum):
    """When a routing rule is triggered."""
    ALWAYS = "always"
    ON_SUCCESS = "on_success"
    ON_APPROVAL = "on_approval"
    ON_SELECTION = "on_selection"


class PolicySeverity(str, Enum):
    """Severity of a domain policy rule."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class StageDefinition(BaseModel):
    """A single stage in the domain stage registry.

    Args:
        stage_id: Unique stage identifier.
        label: Human-readable label.
        stage_class: :class:`StageClass`.
        is_terminal: Whether this is a terminal stage.
        requires_hitl: Whether this stage blocks for human review.
        governance_gate: Whether this stage is a governance decision point.
        tool_groups: Tool group IDs available in this stage.
        artifact_types: Artifact types produced in this stage.
        policy_pack_ids: Policy pack IDs applied at this stage.
    """

    model_config = ConfigDict(frozen=True)

    stage_id: str
    label: str = ""
    stage_class: StageClass = StageClass.DEVELOPMENT
    is_terminal: bool = False
    requires_hitl: bool = False
    governance_gate: bool = False
    tool_groups: list[str] = Field(default_factory=list)
    artifact_types: list[str] = Field(default_factory=list)
    policy_pack_ids: list[str] = Field(default_factory=list)


class RoutingRule(BaseModel):
    """A stage transition routing rule.

    Args:
        from_stage: Source stage_id.
        to_stage: Target stage_id on success.
        condition: :class:`RouteCondition`.
        failure_stage: Stage to route to on failure (optional).
    """

    model_config = ConfigDict(frozen=True)

    from_stage: str
    to_stage: str
    condition: RouteCondition = RouteCondition.ON_SUCCESS
    failure_stage: str | None = None


class MetricDefinition(BaseModel):
    """Definition of a domain metric with thresholds.

    Args:
        metric_name: Metric identifier.
        display_name: Human-readable name.
        description: Description.
        higher_is_better: Default: True.
        threshold_low: Minimum acceptable value.
        threshold_high: Maximum acceptable value.
        warn_threshold_low: Warning lower bound.
        dataset_splits: Splits to compute metric on.
        is_primary: Whether this is the primary selection metric.
    """

    model_config = ConfigDict(frozen=True)

    metric_name: str
    display_name: str = ""
    description: str = ""
    higher_is_better: bool = True
    threshold_low: float | None = None
    threshold_high: float | None = None
    warn_threshold_low: float | None = None
    dataset_splits: list[str] = Field(default_factory=lambda: ["test"])
    is_primary: bool = False


class PolicyRule(BaseModel):
    """A domain-specific governance policy rule.

    Args:
        rule_id: Unique rule ID.
        name: Rule name.
        description: Rule description.
        severity: :class:`PolicySeverity`.
        applies_to_stages: Stage IDs where this rule is evaluated.
        condition_expression: Human-readable condition description (documentation only).
        requires_waiver: Whether a waiver is required to bypass.
    """

    model_config = ConfigDict(frozen=True)

    rule_id: str
    name: str = ""
    description: str = ""
    severity: PolicySeverity = PolicySeverity.MEDIUM
    applies_to_stages: list[str] = Field(default_factory=list)
    condition_expression: str = ""
    requires_waiver: bool = False


class ArtifactDefinition(BaseModel):
    """Definition of a domain artifact type.

    Args:
        artifact_type: Unique artifact type identifier.
        display_name: Human-readable name.
        description: Description.
        produced_at_stage: Stage where this artifact is produced.
        schema_ref: Optional path to a JSON schema for validation.
        is_audit_required: Whether this artifact must be in the audit trail.
    """

    model_config = ConfigDict(frozen=True)

    artifact_type: str
    display_name: str = ""
    description: str = ""
    produced_at_stage: str = ""
    schema_ref: str | None = None
    is_audit_required: bool = False


class ReviewTemplate(BaseModel):
    """HITL review panel configuration for a stage.

    Args:
        template_id: Unique template identifier.
        stage_id: Stage this template applies to.
        review_type: ``"approval"`` | ``"selection"`` | ``"recovery"``.
        panel_a_evidence_types: Artifact types shown in Panel A.
        required_form_fields: Form field IDs required in Panel B.
        action_types: Action types available in Panel C.
        required_roles: Role IDs who can submit this review.
    """

    model_config = ConfigDict(frozen=True)

    template_id: str
    stage_id: str
    review_type: str = "approval"
    panel_a_evidence_types: list[str] = Field(default_factory=list)
    required_form_fields: list[str] = Field(default_factory=lambda: ["rationale", "policy_acknowledged"])
    action_types: list[str] = Field(default_factory=lambda: ["approve", "reject", "escalate"])
    required_roles: list[str] = Field(default_factory=list)


class SkillPackDefinition(BaseModel):
    """References to Python skill classes for this domain.

    Args:
        domain_skill: Fully-qualified Python class for the domain orchestrator skill.
        stage_skills: Dict of stage_id → fully-qualified Python class.
    """

    model_config = ConfigDict(frozen=True)

    domain_skill: str = ""
    stage_skills: dict[str, str] = Field(default_factory=dict)


class DomainPackManifest(BaseModel):
    """Complete domain pack manifest -- the top-level contract object.

    Args:
        domain: Unique domain identifier.
        description: Human-readable description.
        model_class: Broad model class.
        regulatory_scope: Applicable regulatory frameworks.
        schema_version: Pack schema version.
        stage_registry: Ordered domain stage definitions.
        routing_rules: Stage transition rules.
        metrics_pack: Metric definitions and thresholds.
        policy_pack: Domain-specific governance rules.
        artifact_pack: Artifact type definitions.
        review_templates: HITL review panel configurations.
        skill_pack: Skill class references.
        domain_overlay: Optional runtime config overrides.
        test_pack: Optional test references.
    """

    model_config = ConfigDict(frozen=True)

    domain: str
    description: str = ""
    model_class: str = ""
    regulatory_scope: list[str] = Field(default_factory=list)
    schema_version: str = "1.0.0"
    stage_registry: list[StageDefinition] = Field(default_factory=list)
    routing_rules: list[RoutingRule] = Field(default_factory=list)
    metrics_pack: list[MetricDefinition] = Field(default_factory=list)
    policy_pack: list[PolicyRule] = Field(default_factory=list)
    artifact_pack: list[ArtifactDefinition] = Field(default_factory=list)
    review_templates: list[ReviewTemplate] = Field(default_factory=list)
    skill_pack: SkillPackDefinition = Field(default_factory=SkillPackDefinition)
    domain_overlay: dict[str, Any] = Field(default_factory=dict)
    test_pack: dict[str, Any] = Field(default_factory=dict)

    @property
    def stage_ids(self) -> list[str]:
        """Return all stage IDs in order."""
        return [s.stage_id for s in self.stage_registry]

    @property
    def hitl_stages(self) -> list[str]:
        """Return stage IDs that require HITL review."""
        return [s.stage_id for s in self.stage_registry if s.requires_hitl]

    @property
    def governance_gate_stages(self) -> list[str]:
        """Return stage IDs that are governance gates."""
        return [s.stage_id for s in self.stage_registry if s.governance_gate]

    def get_stage(self, stage_id: str) -> StageDefinition | None:
        """Return the :class:`StageDefinition` for a given stage_id.

        Args:
            stage_id: Stage identifier.

        Returns:
            :class:`StageDefinition` or None if not found.
        """
        return next((s for s in self.stage_registry if s.stage_id == stage_id), None)

    def get_primary_metric(self) -> MetricDefinition | None:
        """Return the primary metric definition.

        Returns:
            :class:`MetricDefinition` or None if no primary metric is defined.
        """
        return next((m for m in self.metrics_pack if m.is_primary), None)

    def get_routing_rule(self, from_stage: str, condition: RouteCondition = RouteCondition.ON_SUCCESS) -> RoutingRule | None:
        """Return the routing rule for a stage transition.

        Args:
            from_stage: Source stage_id.
            condition: :class:`RouteCondition` to match.

        Returns:
            :class:`RoutingRule` or None.
        """
        return next(
            (r for r in self.routing_rules if r.from_stage == from_stage and r.condition == condition),
            None,
        )

    def get_review_template(self, stage_id: str) -> ReviewTemplate | None:
        """Return the review template for a stage.

        Args:
            stage_id: Stage identifier.

        Returns:
            :class:`ReviewTemplate` or None.
        """
        return next((t for t in self.review_templates if t.stage_id == stage_id), None)
