"""Unit tests for GovernanceOverlayEngine — 4-layer governance overlay resolution."""

from __future__ import annotations

import pytest

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
from sdk.policysdk.overlay_engine import GovernanceContext, GovernanceOverlayEngine

from tests.unit.workflowsdk.conftest import minimal_bundle  # noqa: F401


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_engine(
    minimal_bundle: RuntimeConfigBundle,
    stage_rules: list | None = None,
    role_overrides: list | None = None,
    conditional_rules: list | None = None,
    default_overrides: dict | None = None,
    environment: str = "dev",
) -> GovernanceOverlayEngine:
    """Build a GovernanceOverlayEngine with custom overlay config."""
    defaults = DefaultGovernanceRules(**(default_overrides or {}))
    section = GovernanceOverlaysSection(
        default_rules=defaults,
        stage_rules=stage_rules or [],
        role_overrides=role_overrides or [],
        conditional_rules=conditional_rules or [],
    )
    overlay_config = GovernanceOverlaysConfig(governance=section)
    # Patch the bundle's governance_overlays in-place via model_copy
    patched = minimal_bundle.model_copy(update={"governance_overlays": overlay_config})
    return GovernanceOverlayEngine(patched, environment=environment)


# ---------------------------------------------------------------------------
# Layer 1: Default rules
# ---------------------------------------------------------------------------


class TestDefaultRules:
    def test_require_audit_by_default(self, minimal_bundle: RuntimeConfigBundle) -> None:
        engine = _make_engine(
            minimal_bundle,
            default_overrides={"require_audit_for_all_approvals": True},
        )
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = engine.resolve(ctx)
        assert resolved.audit_required is True

    def test_review_not_required_when_default_off(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        engine = _make_engine(
            minimal_bundle,
            default_overrides={"require_review_before_finalization": False},
        )
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = engine.resolve(ctx)
        assert resolved.review_required is False

    def test_auto_continue_blocked_when_breach_block_on(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        engine = _make_engine(
            minimal_bundle,
            default_overrides={"block_auto_continue_on_breach": True},
        )
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = engine.resolve(ctx)
        assert resolved.auto_continue_allowed is False

    def test_auto_continue_allowed_when_breach_block_off(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        engine = _make_engine(
            minimal_bundle,
            default_overrides={"block_auto_continue_on_breach": False},
        )
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = engine.resolve(ctx)
        assert resolved.auto_continue_allowed is True

    def test_default_rules_in_applied_list(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        engine = _make_engine(minimal_bundle)
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = engine.resolve(ctx)
        assert "default_rules" in resolved.applied_rules


# ---------------------------------------------------------------------------
# Layer 2: Stage-specific rules
# ---------------------------------------------------------------------------


class TestStageRules:
    def test_stage_rule_overrides_review_required(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        stage_rule = StageGovernanceRule(
            stage_name="stage_a",
            requires_review=True,
            auto_continue_allowed=False,
        )
        engine = _make_engine(
            minimal_bundle,
            stage_rules=[stage_rule],
            default_overrides={"require_review_before_finalization": False},
        )
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = engine.resolve(ctx)
        assert resolved.review_required is True
        assert resolved.auto_continue_allowed is False

    def test_stage_rule_does_not_apply_to_other_stage(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        stage_rule = StageGovernanceRule(
            stage_name="stage_b",
            requires_review=True,
        )
        engine = _make_engine(
            minimal_bundle,
            stage_rules=[stage_rule],
            default_overrides={"require_review_before_finalization": False},
        )
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = engine.resolve(ctx)
        assert resolved.review_required is False

    def test_stage_rule_sets_min_approval_authority(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        stage_rule = StageGovernanceRule(
            stage_name="stage_a",
            min_approval_authority="governance",
        )
        engine = _make_engine(minimal_bundle, stage_rules=[stage_rule])
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = engine.resolve(ctx)
        assert resolved.min_approval_authority == "governance"

    def test_stage_rule_applied_in_rules_list(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        stage_rule = StageGovernanceRule(stage_name="stage_a", requires_review=True)
        engine = _make_engine(minimal_bundle, stage_rules=[stage_rule])
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = engine.resolve(ctx)
        assert "stage_rule:stage_a" in resolved.applied_rules


# ---------------------------------------------------------------------------
# Layer 3: Role overrides
# ---------------------------------------------------------------------------


class TestRoleOverrides:
    def test_role_override_can_approve(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        override = RoleGovernanceOverride(
            role="validator",
            stage_name="stage_a",
            can_approve=True,
        )
        engine = _make_engine(minimal_bundle, role_overrides=[override])
        ctx = GovernanceContext(stage_name="stage_a", actor_role="validator")
        resolved = engine.resolve(ctx)
        assert resolved.can_approve is True

    def test_role_override_can_waive(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        override = RoleGovernanceOverride(
            role="governance",
            stage_name="stage_a",
            can_waive=True,
        )
        engine = _make_engine(minimal_bundle, role_overrides=[override])
        ctx = GovernanceContext(stage_name="stage_a", actor_role="governance")
        resolved = engine.resolve(ctx)
        assert resolved.can_waive is True

    def test_role_override_does_not_apply_for_other_role(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        override = RoleGovernanceOverride(
            role="governance",
            stage_name="stage_a",
            can_approve=True,
        )
        engine = _make_engine(minimal_bundle, role_overrides=[override])
        ctx = GovernanceContext(stage_name="stage_a", actor_role="developer")
        resolved = engine.resolve(ctx)
        assert resolved.can_approve is None  # not set

    def test_role_override_applied_in_rules_list(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        override = RoleGovernanceOverride(
            role="validator", stage_name="stage_a", can_approve=True
        )
        engine = _make_engine(minimal_bundle, role_overrides=[override])
        ctx = GovernanceContext(stage_name="stage_a", actor_role="validator")
        resolved = engine.resolve(ctx)
        assert "role_override:validator@stage_a" in resolved.applied_rules


# ---------------------------------------------------------------------------
# Layer 4: Conditional rules
# ---------------------------------------------------------------------------


class TestConditionalRules:
    def test_conditional_fires_when_review_active(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        cond = ConditionalGovernanceRule(
            rule_id="block_on_review",
            when=ConditionalWhenClause(active_review_exists=True),
            then=ConditionalThenClause(
                force_block_tools=["write_tools"],
                block_auto_continue=True,
            ),
            applies_to_stages=["stage_a"],
        )
        engine = _make_engine(minimal_bundle, conditional_rules=[cond])
        ctx = GovernanceContext(
            stage_name="stage_a",
            active_review_exists=True,
        )
        resolved = engine.resolve(ctx)
        assert "write_tools" in resolved.force_blocked_tools
        assert resolved.auto_continue_allowed is False

    def test_conditional_does_not_fire_when_condition_false(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        cond = ConditionalGovernanceRule(
            rule_id="block_on_review",
            when=ConditionalWhenClause(active_review_exists=True),
            then=ConditionalThenClause(force_block_tools=["write_tools"]),
            applies_to_stages=["stage_a"],
        )
        engine = _make_engine(minimal_bundle, conditional_rules=[cond])
        ctx = GovernanceContext(stage_name="stage_a", active_review_exists=False)
        resolved = engine.resolve(ctx)
        assert "write_tools" not in resolved.force_blocked_tools

    def test_conditional_force_allow_tools(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        cond = ConditionalGovernanceRule(
            rule_id="allow_read_on_breach",
            when=ConditionalWhenClause(has_unresolved_severe_breach=True),
            then=ConditionalThenClause(force_allow_tools=["read_tools"]),
        )
        engine = _make_engine(minimal_bundle, conditional_rules=[cond])
        ctx = GovernanceContext(stage_name="stage_a", has_unresolved_severe_breach=True)
        resolved = engine.resolve(ctx)
        assert "read_tools" in resolved.force_allowed_tools

    def test_conditional_set_access_mode(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        cond = ConditionalGovernanceRule(
            rule_id="force_review_mode",
            when=ConditionalWhenClause(approval_required=True),
            then=ConditionalThenClause(set_access_mode="REVIEW_REQUIRED"),
        )
        engine = _make_engine(minimal_bundle, conditional_rules=[cond])
        ctx = GovernanceContext(stage_name="stage_a", approval_required=True)
        resolved = engine.resolve(ctx)
        assert resolved.set_access_mode == "REVIEW_REQUIRED"

    def test_conditional_environment_filter(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        cond = ConditionalGovernanceRule(
            rule_id="prod_only_rule",
            when=ConditionalWhenClause(environment_is="production"),
            then=ConditionalThenClause(require_audit=True),
        )
        dev_engine = _make_engine(
            minimal_bundle, conditional_rules=[cond], environment="dev"
        )
        prod_engine = _make_engine(
            minimal_bundle, conditional_rules=[cond], environment="production"
        )
        ctx = GovernanceContext(stage_name="stage_a")
        assert "conditional:prod_only_rule" not in dev_engine.resolve(ctx).applied_rules
        assert "conditional:prod_only_rule" in prod_engine.resolve(ctx).applied_rules

    def test_conditional_access_mode_filter(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        cond = ConditionalGovernanceRule(
            rule_id="review_required_mode",
            when=ConditionalWhenClause(stage_access_mode_in=["REVIEW_REQUIRED"]),
            then=ConditionalThenClause(force_block_tools=["finalize_tools"]),
        )
        engine = _make_engine(minimal_bundle, conditional_rules=[cond])
        ctx_review = GovernanceContext(stage_name="stage_a", access_mode="REVIEW_REQUIRED")
        ctx_build = GovernanceContext(stage_name="stage_a", access_mode="BUILD_ONLY")
        assert "finalize_tools" in engine.resolve(ctx_review).force_blocked_tools
        assert "finalize_tools" not in engine.resolve(ctx_build).force_blocked_tools

    def test_multiple_conditions_and_semantics(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        """All conditions in a when clause must match (AND semantics)."""
        cond = ConditionalGovernanceRule(
            rule_id="multi_cond",
            when=ConditionalWhenClause(
                active_review_exists=True,
                has_unresolved_severe_breach=True,
            ),
            then=ConditionalThenClause(block_auto_continue=True),
        )
        engine = _make_engine(minimal_bundle, conditional_rules=[cond])
        ctx_both = GovernanceContext(
            stage_name="stage_a",
            active_review_exists=True,
            has_unresolved_severe_breach=True,
        )
        ctx_one = GovernanceContext(
            stage_name="stage_a",
            active_review_exists=True,
            has_unresolved_severe_breach=False,
        )
        # Both conditions met → rule fires
        assert engine.resolve(ctx_both).auto_continue_allowed is False
        # Only one condition met → rule does NOT fire


# ---------------------------------------------------------------------------
# Production enforcement
# ---------------------------------------------------------------------------


class TestProductionEnforcement:
    def test_production_forces_review_on(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        engine = _make_engine(
            minimal_bundle,
            default_overrides={"require_review_before_finalization": True},
            environment="production",
        )
        # Stage rule tries to disable review
        stage_rule = StageGovernanceRule(stage_name="stage_a", requires_review=False)
        prod_engine = _make_engine(
            minimal_bundle,
            stage_rules=[stage_rule],
            default_overrides={"require_review_before_finalization": True},
            environment="production",
        )
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = prod_engine.resolve(ctx)
        # Production enforcement re-enables it
        assert resolved.review_required is True
        assert resolved.environment_enforced is True

    def test_production_enforcement_applied_in_rules(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        engine = _make_engine(minimal_bundle, environment="production")
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = engine.resolve(ctx)
        assert "production_enforcement" in resolved.applied_rules

    def test_dev_environment_no_enforcement(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        engine = _make_engine(minimal_bundle, environment="dev")
        ctx = GovernanceContext(stage_name="stage_a")
        resolved = engine.resolve(ctx)
        assert resolved.environment_enforced is False
        assert "production_enforcement" not in resolved.applied_rules


# ---------------------------------------------------------------------------
# to_dict
# ---------------------------------------------------------------------------


class TestResolvedGovernanceToDict:
    def test_to_dict_contains_all_keys(
        self, minimal_bundle: RuntimeConfigBundle
    ) -> None:
        engine = _make_engine(minimal_bundle)
        ctx = GovernanceContext(stage_name="stage_a", actor_role="validator")
        resolved = engine.resolve(ctx)
        d = resolved.to_dict()
        expected_keys = {
            "stage_name", "actor_role", "review_required", "approval_required",
            "audit_required", "auto_continue_allowed", "min_approval_authority",
            "can_approve", "can_waive", "force_blocked_tools", "force_allowed_tools",
            "set_access_mode", "applied_rules", "environment_enforced",
        }
        assert expected_keys == set(d.keys())
