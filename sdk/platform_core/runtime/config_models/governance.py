"""Governance overlay Pydantic config models.

Implements the default rules + stage rules + role overrides + conditional rules
hierarchy from enhancement v0.3. Loaded from configs/runtime/governance_overlays.yaml.
"""

from typing import Dict, List, Optional

from pydantic import field_validator

from .base import RuntimeConfigBase


class DefaultGovernanceRules(RuntimeConfigBase):
    """Platform-wide default governance rules applied to all stages.

    Attributes:
        require_audit_for_all_approvals: All approvals must create an audit record.
        require_review_before_finalization: No finalization without a review.
        block_auto_continue_on_breach: Auto-continue is blocked when a policy breach exists.
        require_policy_acknowledgment_on_findings: Actors must acknowledge policy findings.
        min_evidence_count_for_review: Minimum evidence items required to open a review.
    """

    require_audit_for_all_approvals: bool = True
    require_review_before_finalization: bool = True
    block_auto_continue_on_breach: bool = True
    require_policy_acknowledgment_on_findings: bool = True
    min_evidence_count_for_review: int = 1


class StageGovernanceRule(RuntimeConfigBase):
    """Stage-specific governance rule that overrides or extends defaults.

    Attributes:
        stage_name: The stage this rule applies to.
        requires_review: Override requires_review for this stage.
        requires_approval: Override requires_approval for this stage.
        min_approval_authority: Minimum role authority required for approval.
        audit_required: Override audit requirement for this stage.
        escalation_trigger: Conditions that trigger escalation at this stage.
        auto_continue_allowed: Override auto_continue for this stage.
    """

    stage_name: str
    requires_review: Optional[bool] = None
    requires_approval: Optional[bool] = None
    min_approval_authority: Optional[str] = None
    audit_required: Optional[bool] = None
    escalation_trigger: Optional[str] = None
    auto_continue_allowed: Optional[bool] = None


class RoleGovernanceOverride(RuntimeConfigBase):
    """Per-role governance override for specific stages.

    Attributes:
        role: Actor role this override applies to.
        stage_name: Stage this override applies to.
        can_approve: Whether this role can approve at this specific stage.
        can_waive: Whether this role can issue a policy waiver at this stage.
        additional_blocked_actions: Actions blocked for this role at this stage.
    """

    role: str
    stage_name: str
    can_approve: Optional[bool] = None
    can_waive: Optional[bool] = None
    additional_blocked_actions: List[str] = []


class ConditionalWhenClause(RuntimeConfigBase):
    """Condition check for a conditional governance rule.

    Attributes:
        stage_access_mode_in: True if current access mode is in this list.
        active_review_exists: True if a pending review exists.
        approval_required: True if approval is required.
        has_unresolved_severe_breach: True if there are unresolved high/critical breaches.
        environment_is: True if environment matches this value.
    """

    stage_access_mode_in: List[str] = []
    active_review_exists: Optional[bool] = None
    approval_required: Optional[bool] = None
    has_unresolved_severe_breach: Optional[bool] = None
    environment_is: Optional[str] = None


class ConditionalThenClause(RuntimeConfigBase):
    """Action to apply when a conditional governance rule fires.

    Attributes:
        force_block_tools: Tool groups to force-block when condition is true.
        force_allow_tools: Tool groups to force-allow when condition is true.
        set_access_mode: Force a specific access mode.
        require_audit: Force audit requirement on.
        block_auto_continue: Force auto_continue off.
    """

    force_block_tools: List[str] = []
    force_allow_tools: List[str] = []
    set_access_mode: Optional[str] = None
    require_audit: Optional[bool] = None
    block_auto_continue: Optional[bool] = None


class ConditionalGovernanceRule(RuntimeConfigBase):
    """A conditional governance rule: if `when` matches context, apply `then`.

    Attributes:
        rule_id: Unique identifier for this conditional rule.
        description: Human-readable description.
        when: Condition clause.
        then: Action clause applied when condition is true.
        applies_to_stages: Limit this rule to specific stages. Empty = all stages.
    """

    rule_id: str
    description: Optional[str] = None
    when: ConditionalWhenClause
    then: ConditionalThenClause
    applies_to_stages: List[str] = []

    @field_validator("rule_id")
    @classmethod
    def validate_non_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("rule_id must not be blank")
        return v


class GovernanceOverlaysSection(RuntimeConfigBase):
    """Container for all governance overlay sub-sections.

    Attributes:
        default_rules: Platform-wide default governance rules.
        stage_rules: Per-stage governance rule overrides.
        role_overrides: Per-role per-stage governance overrides.
        conditional_rules: Conditional rules applied dynamically at runtime.
    """

    default_rules: DefaultGovernanceRules = DefaultGovernanceRules()
    stage_rules: List[StageGovernanceRule] = []
    role_overrides: List[RoleGovernanceOverride] = []
    conditional_rules: List[ConditionalGovernanceRule] = []


class GovernanceOverlaysConfig(RuntimeConfigBase):
    """Root governance overlays config.

    Loaded from configs/runtime/governance_overlays.yaml.
    """

    governance: GovernanceOverlaysSection

    def get_stage_rules_map(self) -> Dict[str, StageGovernanceRule]:
        """Return stage_name -> StageGovernanceRule mapping for O(1) lookup."""
        return {r.stage_name: r for r in self.governance.stage_rules}

    def get_conditional_rules_for_stage(self, stage_name: str) -> List[ConditionalGovernanceRule]:
        """Return conditional rules applicable to a specific stage."""
        return [
            r for r in self.governance.conditional_rules
            if not r.applies_to_stages or stage_name in r.applies_to_stages
        ]
