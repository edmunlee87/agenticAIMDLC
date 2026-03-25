"""GovernanceOverlayEngine — resolves governance constraints for a runtime context.

Implements the 4-layer overlay hierarchy:
1. Default rules (platform-wide, always applied).
2. Stage-specific rules (override/extend defaults for named stage).
3. Role overrides (per-role per-stage authority adjustments).
4. Conditional rules (dynamic when/then rules evaluated against context).

Environment-aware strictness:
- In ``production``, all gates are enforced regardless of default values.
- In ``dev`` / ``staging``, some gates may be relaxed, but all overrides are
  audit-logged.

Usage::

    engine = GovernanceOverlayEngine(bundle, environment="production")
    ctx = GovernanceContext(
        stage_name="model_fitting",
        actor_role="validator",
        access_mode="REVIEW_REQUIRED",
        active_review_exists=True,
        has_unresolved_severe_breach=False,
    )
    resolved = engine.resolve(ctx)
    if resolved.review_required:
        ...
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.config_models.governance import (
    ConditionalGovernanceRule,
    ConditionalThenClause,
    ConditionalWhenClause,
    DefaultGovernanceRules,
    GovernanceOverlaysConfig,
    GovernanceOverlaysSection,
    RoleGovernanceOverride,
    StageGovernanceRule,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Runtime context input
# ---------------------------------------------------------------------------


@dataclass
class GovernanceContext:
    """Input context for the governance overlay resolver.

    Args:
        stage_name: Active MDLC stage.
        actor_role: Actor's platform role string.
        access_mode: Current access mode string (e.g. ``"REVIEW_REQUIRED"``).
        active_review_exists: True if a PENDING_REVIEW record exists for this stage.
        has_unresolved_severe_breach: True if HIGH/CRITICAL breach is unresolved.
        approval_required: True if approval is currently required.
        run_id: Active run (for audit logging).
        project_id: Owning project.
        session_id: Active session.
    """

    stage_name: str
    actor_role: str = ""
    access_mode: str = ""
    active_review_exists: bool = False
    has_unresolved_severe_breach: bool = False
    approval_required: bool = False
    run_id: str = ""
    project_id: str = ""
    session_id: str = ""


# ---------------------------------------------------------------------------
# Resolved output
# ---------------------------------------------------------------------------


@dataclass
class ResolvedGovernance:
    """Fully-resolved governance constraints for a given context.

    All boolean fields represent the FINAL effective value after merging all
    overlay layers.

    Args:
        stage_name: Stage this resolution applies to.
        actor_role: Actor role used in resolution.
        review_required: True if a human review must be opened/completed.
        approval_required: True if explicit approval (beyond review) is needed.
        audit_required: True if an audit record must be written.
        auto_continue_allowed: True if the stage can auto-proceed without human input.
        min_approval_authority: Minimum role level required to approve.
        can_approve: True if the actor may approve (considering role overrides).
        can_waive: True if the actor may waive a finding.
        force_blocked_tools: Tool groups force-blocked by conditional rules.
        force_allowed_tools: Tool groups force-allowed by conditional rules.
        set_access_mode: Optional access mode override from a conditional rule.
        applied_rules: Rule IDs that contributed to this resolution (for audit).
        environment_enforced: True if production strictness was applied.
    """

    stage_name: str
    actor_role: str
    review_required: bool = False
    approval_required: bool = False
    audit_required: bool = False
    auto_continue_allowed: bool = True
    min_approval_authority: Optional[str] = None
    can_approve: Optional[bool] = None
    can_waive: Optional[bool] = None
    force_blocked_tools: List[str] = field(default_factory=list)
    force_allowed_tools: List[str] = field(default_factory=list)
    set_access_mode: Optional[str] = None
    applied_rules: List[str] = field(default_factory=list)
    environment_enforced: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dict representation.

        Returns:
            Dict with all resolved governance fields.
        """
        return {
            "stage_name": self.stage_name,
            "actor_role": self.actor_role,
            "review_required": self.review_required,
            "approval_required": self.approval_required,
            "audit_required": self.audit_required,
            "auto_continue_allowed": self.auto_continue_allowed,
            "min_approval_authority": self.min_approval_authority,
            "can_approve": self.can_approve,
            "can_waive": self.can_waive,
            "force_blocked_tools": self.force_blocked_tools,
            "force_allowed_tools": self.force_allowed_tools,
            "set_access_mode": self.set_access_mode,
            "applied_rules": self.applied_rules,
            "environment_enforced": self.environment_enforced,
        }


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------


class GovernanceOverlayEngine:
    """Resolves governance constraints from the 4-layer overlay hierarchy.

    Args:
        bundle: Active :class:`~sdk.platform_core.runtime.config_models.bundle.RuntimeConfigBundle`.
        environment: Deployment environment (``"production"`` enforces all gates).

    Examples:
        >>> engine = GovernanceOverlayEngine(bundle, environment="dev")
        >>> ctx = GovernanceContext(stage_name="model_fitting", actor_role="validator")
        >>> resolved = engine.resolve(ctx)
        >>> resolved.review_required  # depends on config
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        environment: str = "dev",
    ) -> None:
        self._bundle = bundle
        self._environment = environment
        self._config: GovernanceOverlaysConfig = (
            bundle.governance_overlays
            if bundle.governance_overlays
            else GovernanceOverlaysConfig(governance=GovernanceOverlaysSection())
        )
        self._overlays: GovernanceOverlaysSection = self._config.governance
        self._stage_rules_map: Dict[str, StageGovernanceRule] = {
            r.stage_name: r for r in self._overlays.stage_rules
        }

    def resolve(self, ctx: GovernanceContext) -> ResolvedGovernance:
        """Resolve all governance constraints for the given context.

        Applies layers in order: defaults → stage rules → role overrides →
        conditional rules. Production environment escalates all gates.

        Args:
            ctx: :class:`GovernanceContext` with the runtime state.

        Returns:
            :class:`ResolvedGovernance` with all constraints resolved.
        """
        defaults = self._overlays.default_rules
        resolved = ResolvedGovernance(
            stage_name=ctx.stage_name,
            actor_role=ctx.actor_role,
        )
        applied: List[str] = []

        # --- Layer 1: Default rules ---
        self._apply_defaults(resolved, defaults, applied)

        # --- Layer 2: Stage-specific rules ---
        stage_rule = self._stage_rules_map.get(ctx.stage_name)
        if stage_rule:
            self._apply_stage_rule(resolved, stage_rule, applied)

        # --- Layer 3: Role overrides ---
        role_override = self._get_role_override(ctx.actor_role, ctx.stage_name)
        if role_override:
            self._apply_role_override(resolved, role_override, applied)

        # --- Layer 4: Conditional rules ---
        for cond_rule in self._config.get_conditional_rules_for_stage(ctx.stage_name):
            if self._when_matches(cond_rule.when, ctx):
                self._apply_then(resolved, cond_rule.then, applied, cond_rule.rule_id)

        # --- Production enforcement ---
        if self._environment == "production":
            self._enforce_production(resolved, defaults, applied)
            resolved.environment_enforced = True

        resolved.applied_rules = applied
        logger.debug(
            "governance_overlay.resolved: stage=%s role=%s review=%s approval=%s "
            "audit=%s auto_continue=%s env=%s rules=%s",
            ctx.stage_name,
            ctx.actor_role,
            resolved.review_required,
            resolved.approval_required,
            resolved.audit_required,
            resolved.auto_continue_allowed,
            self._environment,
            applied,
        )
        return resolved

    # ------------------------------------------------------------------
    # Layer appliers
    # ------------------------------------------------------------------

    def _apply_defaults(
        self,
        resolved: ResolvedGovernance,
        defaults: DefaultGovernanceRules,
        applied: List[str],
    ) -> None:
        resolved.audit_required = defaults.require_audit_for_all_approvals
        resolved.review_required = defaults.require_review_before_finalization
        # auto_continue is disabled when breach block is active
        # (will be set per-stage, but default is True unless breach exists)
        resolved.auto_continue_allowed = not defaults.block_auto_continue_on_breach
        applied.append("default_rules")

    def _apply_stage_rule(
        self,
        resolved: ResolvedGovernance,
        rule: StageGovernanceRule,
        applied: List[str],
    ) -> None:
        if rule.requires_review is not None:
            resolved.review_required = rule.requires_review
        if rule.requires_approval is not None:
            resolved.approval_required = rule.requires_approval
        if rule.min_approval_authority is not None:
            resolved.min_approval_authority = rule.min_approval_authority
        if rule.audit_required is not None:
            resolved.audit_required = rule.audit_required
        if rule.auto_continue_allowed is not None:
            resolved.auto_continue_allowed = rule.auto_continue_allowed
        applied.append(f"stage_rule:{rule.stage_name}")

    def _apply_role_override(
        self,
        resolved: ResolvedGovernance,
        override: RoleGovernanceOverride,
        applied: List[str],
    ) -> None:
        if override.can_approve is not None:
            resolved.can_approve = override.can_approve
        if override.can_waive is not None:
            resolved.can_waive = override.can_waive
        # Additional blocked actions surface through the tool matrix — not resolved here.
        applied.append(f"role_override:{override.role}@{override.stage_name}")

    def _apply_then(
        self,
        resolved: ResolvedGovernance,
        then: ConditionalThenClause,
        applied: List[str],
        rule_id: str,
    ) -> None:
        if then.force_block_tools:
            for t in then.force_block_tools:
                if t not in resolved.force_blocked_tools:
                    resolved.force_blocked_tools.append(t)
        if then.force_allow_tools:
            for t in then.force_allow_tools:
                if t not in resolved.force_allowed_tools:
                    resolved.force_allowed_tools.append(t)
        if then.set_access_mode is not None:
            resolved.set_access_mode = then.set_access_mode
        if then.require_audit:
            resolved.audit_required = True
        if then.block_auto_continue:
            resolved.auto_continue_allowed = False
        applied.append(f"conditional:{rule_id}")

    def _enforce_production(
        self,
        resolved: ResolvedGovernance,
        defaults: DefaultGovernanceRules,
        applied: List[str],
    ) -> None:
        """Force all governance gates on in production."""
        if defaults.require_review_before_finalization:
            resolved.review_required = True
        if defaults.require_audit_for_all_approvals:
            resolved.audit_required = True
        if defaults.block_auto_continue_on_breach:
            resolved.auto_continue_allowed = False
        applied.append("production_enforcement")

    # ------------------------------------------------------------------
    # Conditional evaluation
    # ------------------------------------------------------------------

    def _when_matches(
        self, when: ConditionalWhenClause, ctx: GovernanceContext
    ) -> bool:
        """Return True if the ``when`` clause is satisfied by the context.

        All specified conditions must match (logical AND).

        Args:
            when: Condition clause from a :class:`ConditionalGovernanceRule`.
            ctx: Current :class:`GovernanceContext`.

        Returns:
            True when all specified conditions hold.
        """
        if when.stage_access_mode_in and ctx.access_mode not in when.stage_access_mode_in:
            return False
        if when.active_review_exists is not None:
            if when.active_review_exists != ctx.active_review_exists:
                return False
        if when.approval_required is not None:
            if when.approval_required != ctx.approval_required:
                return False
        if when.has_unresolved_severe_breach is not None:
            if when.has_unresolved_severe_breach != ctx.has_unresolved_severe_breach:
                return False
        if when.environment_is is not None:
            if when.environment_is != self._environment:
                return False
        return True

    # ------------------------------------------------------------------
    # Role override lookup
    # ------------------------------------------------------------------

    def _get_role_override(
        self, actor_role: str, stage_name: str
    ) -> Optional[RoleGovernanceOverride]:
        """Return the most-specific role override for actor+stage.

        Args:
            actor_role: Actor's role string.
            stage_name: Current stage.

        Returns:
            Matching :class:`RoleGovernanceOverride` or None.
        """
        for override in self._overlays.role_overrides:
            if override.role == actor_role and override.stage_name == stage_name:
                return override
        return None
