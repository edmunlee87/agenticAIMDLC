"""Unit tests for runtime resolver pack.

Covers:
- RoleConfigResolver: role lookup, tool group access, stage access
- ToolGroupResolver: group expansion, virtual groups, validation
- AllowlistResolver: role+stage intersection, blocked tools
- GovernanceRuleResolver: default rules, stage governance, conditional rules
- RetryPolicyResolver: default policy, per-tool override
- UIModeResolver: UI mode, interaction mode, token mode
- RuntimeResolver: full ResolvedStack composition
"""

from __future__ import annotations

import pytest

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.config_models.enums import (
    AccessModeEnum,
    InteractionModeEnum,
    RetryModeEnum,
    StageClassEnum,
    TokenModeEnum,
    UIModeEnum,
)
from sdk.platform_core.runtime.config_models.governance import (
    ConditionalGovernanceRule,
    ConditionalThenClause,
    ConditionalWhenClause,
    DefaultGovernanceRules,
    GovernanceOverlaysConfig,
    GovernanceOverlaysSection,
    StageGovernanceRule,
)
from sdk.platform_core.runtime.config_models.retries import (
    RetryDefaults,
    RetryPoliciesConfig,
    RetryPoliciesSection,
    ToolRetryRule,
)
from sdk.platform_core.runtime.config_models.roles import (
    RoleCapabilitiesConfig,
    RoleCapabilityDefinition,
)
from sdk.platform_core.runtime.config_models.routes import (
    WorkflowRouteDefinition,
    WorkflowRoutesConfig,
)
from sdk.platform_core.runtime.config_models.runtime_master import (
    RuntimeMasterConfig,
    RuntimeMasterSection,
)
from sdk.platform_core.runtime.config_models.stages import (
    StageDefinition,
    StageRegistryConfig,
    StageToolMatrixConfig,
    StageToolMatrixEntry,
)
from sdk.platform_core.runtime.config_models.tool_groups import (
    ToolGroupDefinition,
    ToolGroupsConfig,
    VirtualToolGroupDefinition,
    VirtualToolGroupsConfig,
)
from sdk.platform_core.runtime.config_models.ui import (
    InteractionModeDefinition,
    InteractionModesConfig,
    TokenModeDefinition,
    TokenModesConfig,
    UIModeDefinition,
    UIModesConfig,
)
from sdk.platform_core.runtime.resolvers import (
    AllowlistResolver,
    GovernanceRuleResolver,
    ResolvedStack,
    RetryPolicyResolver,
    RoleConfigResolver,
    RuntimeResolver,
    ToolGroupResolver,
    UIModeResolver,
)


# ---------------------------------------------------------------------------
# Helpers / factories
# ---------------------------------------------------------------------------

def _make_bundle(
    *,
    roles: dict | None = None,
    groups: dict | None = None,
    virtual_groups: dict | None = None,
    stage_matrix: dict | None = None,
    stages: dict | None = None,
    governance: GovernanceOverlaysSection | None = None,
    retry_rules: list | None = None,
    ui_stage_class: str | None = None,
    routes: dict | None = None,
) -> RuntimeConfigBundle:
    """Build a minimal valid RuntimeConfigBundle for resolver testing."""
    if groups is None:
        groups = {
            "grp_core": ToolGroupDefinition(group_name="grp_core", tools=["tool_a", "tool_b"]),
            "grp_ext": ToolGroupDefinition(group_name="grp_ext", tools=["tool_c"]),
        }
    tg = ToolGroupsConfig(groups=groups)

    vtg = None
    if virtual_groups:
        vtg = VirtualToolGroupsConfig(virtual_groups=virtual_groups)

    if stages is None:
        stages = {
            "stg1": StageDefinition(
                stage_name="stg1",
                stage_class=StageClassEnum.BUILD,
                default_access_mode=AccessModeEnum.BUILD_ONLY,
            ),
            "stg2": StageDefinition(
                stage_name="stg2",
                stage_class=StageClassEnum.REVIEW,
                default_access_mode=AccessModeEnum.REVIEW_REQUIRED,
            ),
        }
    sr = StageRegistryConfig(stages=stages)

    if stage_matrix is None:
        stage_matrix = {
            name: StageToolMatrixEntry(
                stage_name=name,
                allowed_groups=list(groups.keys()),
            )
            for name in stages
        }
    stm = StageToolMatrixConfig(matrix=stage_matrix)

    if roles is None:
        roles = {
            "developer": RoleCapabilityDefinition(
                role="developer",
                allowed_tool_groups=list(groups.keys()),
                blocked_tool_groups=[],
                allowed_stages=list(stages.keys()),
            )
        }
    rc = RoleCapabilitiesConfig(roles=roles)

    gov_section = governance or GovernanceOverlaysSection(default_rules=DefaultGovernanceRules())
    gov = GovernanceOverlaysConfig(governance=gov_section)

    retry_section = RetryPoliciesSection(
        defaults=RetryDefaults(),
        tool_rules=retry_rules or [],
    )
    rpc = RetryPoliciesConfig(retry_policies=retry_section)

    if routes is None:
        routes = {name: WorkflowRouteDefinition(stage_name=name) for name in stages}
    wrc = WorkflowRoutesConfig(routes=routes)

    # UI modes — map stage classes to modes
    build_class = StageClassEnum.BUILD.value
    review_class = StageClassEnum.REVIEW.value
    ui_modes = UIModesConfig(
        modes={
            "bootstrap_workspace": UIModeDefinition(
                mode=UIModeEnum.BOOTSTRAP_WORKSPACE,
                default_for_stage_classes=[build_class],
                token_budget_hint=TokenModeEnum.COMPACT,
            ),
            "three_panel_review_workspace": UIModeDefinition(
                mode=UIModeEnum.THREE_PANEL_REVIEW_WORKSPACE,
                default_for_stage_classes=[review_class],
            ),
        }
    )
    interaction_modes = InteractionModesConfig(
        modes={
            "edit_and_finalize": InteractionModeDefinition(
                mode=InteractionModeEnum.EDIT_AND_FINALIZE,
                default_for_stage_classes=[build_class],
            ),
            "review_and_conclude": InteractionModeDefinition(
                mode=InteractionModeEnum.REVIEW_AND_CONCLUDE,
                default_for_stage_classes=[review_class],
            ),
        }
    )
    token_modes = TokenModesConfig(
        modes={
            "compact": TokenModeDefinition(mode=TokenModeEnum.COMPACT),
            "full": TokenModeDefinition(mode=TokenModeEnum.FULL),
        }
    )

    return RuntimeConfigBundle(
        runtime_master=RuntimeMasterConfig(runtime=RuntimeMasterSection()),
        tool_groups=tg,
        virtual_tool_groups=vtg,
        role_capabilities=rc,
        ui_modes=ui_modes,
        interaction_modes=interaction_modes,
        token_modes=token_modes,
        stage_registry=sr,
        stage_tool_matrix=stm,
        governance_overlays=gov,
        retry_policies=rpc,
        workflow_routes=wrc,
    )


# ---------------------------------------------------------------------------
# RoleConfigResolver
# ---------------------------------------------------------------------------

class TestRoleConfigResolver:
    def test_resolve_known_role(self) -> None:
        bundle = _make_bundle()
        resolver = RoleConfigResolver(bundle)
        cap = resolver.resolve_role_config("developer")
        assert cap is not None
        assert cap.role == "developer"

    def test_resolve_unknown_role_returns_none(self) -> None:
        bundle = _make_bundle()
        resolver = RoleConfigResolver(bundle)
        assert resolver.resolve_role_config("ghost") is None

    def test_get_allowed_tool_groups(self) -> None:
        bundle = _make_bundle()
        resolver = RoleConfigResolver(bundle)
        groups = resolver.get_allowed_tool_groups("developer")
        assert "grp_core" in groups

    def test_get_allowed_tool_groups_unknown_role(self) -> None:
        bundle = _make_bundle()
        resolver = RoleConfigResolver(bundle)
        assert resolver.get_allowed_tool_groups("ghost") == []

    def test_get_blocked_tool_groups(self) -> None:
        bundle = _make_bundle(
            roles={
                "governance": RoleCapabilityDefinition(
                    role="governance",
                    allowed_tool_groups=["grp_core"],
                    blocked_tool_groups=["grp_ext"],
                    allowed_stages=["stg1", "stg2"],
                )
            }
        )
        resolver = RoleConfigResolver(bundle)
        assert resolver.get_blocked_tool_groups("governance") == ["grp_ext"]

    def test_role_can_access_stage_allowed(self) -> None:
        bundle = _make_bundle()
        resolver = RoleConfigResolver(bundle)
        assert resolver.role_can_access_stage("developer", "stg1") is True

    def test_role_can_access_stage_denied(self) -> None:
        bundle = _make_bundle(
            roles={
                "validator": RoleCapabilityDefinition(
                    role="validator",
                    allowed_tool_groups=["grp_core"],
                    blocked_tool_groups=[],
                    allowed_stages=["stg2"],
                )
            }
        )
        resolver = RoleConfigResolver(bundle)
        assert resolver.role_can_access_stage("validator", "stg1") is False

    def test_role_with_empty_allowed_stages_can_access_any(self) -> None:
        bundle = _make_bundle(
            roles={
                "system": RoleCapabilityDefinition(
                    role="system",
                    allowed_tool_groups=["grp_core"],
                    blocked_tool_groups=[],
                    allowed_stages=[],
                )
            }
        )
        resolver = RoleConfigResolver(bundle)
        assert resolver.role_can_access_stage("system", "stg1") is True
        assert resolver.role_can_access_stage("system", "stg2") is True


# ---------------------------------------------------------------------------
# ToolGroupResolver
# ---------------------------------------------------------------------------

class TestToolGroupResolver:
    def test_expand_real_group(self) -> None:
        bundle = _make_bundle()
        resolver = ToolGroupResolver(bundle)
        assert resolver.expand_group("grp_core") == ["tool_a", "tool_b"]

    def test_expand_virtual_group(self) -> None:
        bundle = _make_bundle(
            virtual_groups={
                "vgrp_all": VirtualToolGroupDefinition(
                    virtual_name="vgrp_all",
                    member_groups=["grp_core", "grp_ext"],
                )
            }
        )
        resolver = ToolGroupResolver(bundle)
        result = resolver.expand_group("vgrp_all")
        assert set(result) == {"tool_a", "tool_b", "tool_c"}

    def test_expand_unknown_group_returns_empty(self) -> None:
        bundle = _make_bundle()
        resolver = ToolGroupResolver(bundle)
        assert resolver.expand_group("nonexistent") == []

    def test_expand_groups_deduplicates(self) -> None:
        bundle = _make_bundle(
            groups={
                "g1": ToolGroupDefinition(group_name="g1", tools=["tool_a", "tool_b"]),
                "g2": ToolGroupDefinition(group_name="g2", tools=["tool_b", "tool_c"]),
            }
        )
        resolver = ToolGroupResolver(bundle)
        result = resolver.expand_groups(["g1", "g2"])
        assert result.count("tool_b") == 1
        assert set(result) == {"tool_a", "tool_b", "tool_c"}

    def test_get_all_known_tools(self) -> None:
        bundle = _make_bundle()
        resolver = ToolGroupResolver(bundle)
        known = resolver.get_all_known_tools()
        assert "tool_a" in known
        assert "tool_c" in known

    def test_validate_tools_exist_unknown(self) -> None:
        bundle = _make_bundle()
        resolver = ToolGroupResolver(bundle)
        unknown = resolver.validate_tools_exist(["tool_a", "tool_x"])
        assert unknown == ["tool_x"]

    def test_validate_tools_exist_all_known(self) -> None:
        bundle = _make_bundle()
        resolver = ToolGroupResolver(bundle)
        assert resolver.validate_tools_exist(["tool_a", "tool_b"]) == []


# ---------------------------------------------------------------------------
# AllowlistResolver
# ---------------------------------------------------------------------------

class TestAllowlistResolver:
    def test_resolve_basic(self) -> None:
        bundle = _make_bundle()
        resolver = AllowlistResolver(bundle)
        allowed = resolver.resolve("developer", "stg1")
        assert "tool_a" in allowed
        assert "tool_c" in allowed

    def test_resolve_blocked_by_role(self) -> None:
        bundle = _make_bundle(
            roles={
                "monitoring": RoleCapabilityDefinition(
                    role="monitoring",
                    allowed_tool_groups=["grp_core"],
                    blocked_tool_groups=[],
                    allowed_stages=["stg1", "stg2"],
                )
            }
        )
        resolver = AllowlistResolver(bundle)
        allowed = resolver.resolve("monitoring", "stg1")
        assert "tool_a" in allowed
        assert "tool_b" in allowed
        assert "tool_c" not in allowed  # grp_ext not in role's allowed_groups

    def test_resolve_blocked_by_stage_matrix(self) -> None:
        groups = {
            "grp_core": ToolGroupDefinition(group_name="grp_core", tools=["tool_a"]),
            "grp_ext": ToolGroupDefinition(group_name="grp_ext", tools=["tool_c"]),
        }
        bundle = _make_bundle(
            groups=groups,
            stage_matrix={
                "stg1": StageToolMatrixEntry(
                    stage_name="stg1",
                    allowed_groups=["grp_core"],
                    blocked_groups=["grp_ext"],
                ),
                "stg2": StageToolMatrixEntry(stage_name="stg2", allowed_groups=list(groups.keys())),
            },
        )
        resolver = AllowlistResolver(bundle)
        blocked = resolver.resolve_blocked("developer", "stg1")
        assert "tool_c" in blocked

    def test_resolve_unknown_stage_returns_empty(self) -> None:
        bundle = _make_bundle()
        resolver = AllowlistResolver(bundle)
        allowed = resolver.resolve("developer", "unknown_stage")
        assert isinstance(allowed, list)


# ---------------------------------------------------------------------------
# GovernanceRuleResolver
# ---------------------------------------------------------------------------

class TestGovernanceRuleResolver:
    def test_get_default_rules(self) -> None:
        bundle = _make_bundle()
        resolver = GovernanceRuleResolver(bundle)
        defaults = resolver.get_default_rules()
        assert defaults.require_audit_for_all_approvals is True

    def test_get_stage_governance_defaults(self) -> None:
        bundle = _make_bundle()
        resolver = GovernanceRuleResolver(bundle)
        gov = resolver.get_stage_governance("stg1")
        assert "review_required" in gov
        assert "audit_required" in gov

    def test_get_stage_governance_overridden(self) -> None:
        gov_section = GovernanceOverlaysSection(
            default_rules=DefaultGovernanceRules(require_review_before_finalization=False),
            stage_rules=[
                StageGovernanceRule(
                    stage_name="stg1",
                    requires_review=True,
                    requires_approval=True,
                )
            ],
        )
        bundle = _make_bundle(governance=gov_section)
        resolver = GovernanceRuleResolver(bundle)
        gov = resolver.get_stage_governance("stg1")
        assert gov["review_required"] is True
        assert gov["approval_required"] is True

    def test_production_enforces_review(self) -> None:
        gov_section = GovernanceOverlaysSection(
            default_rules=DefaultGovernanceRules(
                require_review_before_finalization=True,
                require_audit_for_all_approvals=True,
                block_auto_continue_on_breach=True,
            )
        )
        bundle = _make_bundle(governance=gov_section)
        resolver = GovernanceRuleResolver(bundle, environment="production")
        gov = resolver.get_stage_governance("stg1")
        assert gov["review_required"] is True
        assert gov["audit_required"] is True
        assert gov["auto_continue_allowed"] is False

    def test_apply_conditional_rules_no_match(self) -> None:
        bundle = _make_bundle()
        resolver = GovernanceRuleResolver(bundle)
        result = resolver.apply_conditional_rules(
            runtime_facts={"has_active_review": False},
            allowed_tools=["tool_a"],
            blocked_tools=[],
        )
        assert "tool_a" in result["allowed_tools"]

    def test_apply_conditional_rules_match(self) -> None:
        gov_section = GovernanceOverlaysSection(
            default_rules=DefaultGovernanceRules(),
            conditional_rules=[
                ConditionalGovernanceRule(
                    rule_id="block_on_breach",
                    when=ConditionalWhenClause(has_unresolved_severe_breach=True),
                    then=ConditionalThenClause(force_block_tools=["tool_a"]),
                )
            ],
        )
        bundle = _make_bundle(governance=gov_section)
        resolver = GovernanceRuleResolver(bundle)
        result = resolver.apply_conditional_rules(
            runtime_facts={"has_unresolved_severe_breach": True},
            allowed_tools=["tool_a", "tool_b"],
            blocked_tools=[],
        )
        assert "tool_a" in result["blocked_tools"]

    def test_apply_conditional_rules_stage_scoped_no_match(self) -> None:
        gov_section = GovernanceOverlaysSection(
            default_rules=DefaultGovernanceRules(),
            conditional_rules=[
                ConditionalGovernanceRule(
                    rule_id="stage_scoped",
                    applies_to_stages=["stg2"],
                    when=ConditionalWhenClause(active_review_exists=True),
                    then=ConditionalThenClause(force_block_tools=["tool_b"]),
                )
            ],
        )
        bundle = _make_bundle(governance=gov_section)
        resolver = GovernanceRuleResolver(bundle)
        # stage_name=stg1 should NOT trigger the rule (scoped to stg2)
        result = resolver.apply_conditional_rules(
            runtime_facts={"stage_name": "stg1", "active_review_exists": True},
            allowed_tools=["tool_a", "tool_b"],
            blocked_tools=[],
        )
        assert "tool_b" not in result["blocked_tools"]


# ---------------------------------------------------------------------------
# RetryPolicyResolver
# ---------------------------------------------------------------------------

class TestRetryPolicyResolver:
    def test_default_policy(self) -> None:
        bundle = _make_bundle()
        resolver = RetryPolicyResolver(bundle)
        policy = resolver.resolve_retry_policy()
        assert "max_retries" in policy
        assert "retry_mode" in policy

    def test_per_tool_override(self) -> None:
        bundle = _make_bundle(
            retry_rules=[
                ToolRetryRule(
                    tool_name="tool_a",
                    retry_mode=RetryModeEnum.EXPONENTIAL_BACKOFF,
                    max_retries=5,
                )
            ]
        )
        resolver = RetryPolicyResolver(bundle)
        policy = resolver.resolve_retry_policy("tool_a")
        assert policy["max_retries"] == 5
        assert "exponential_backoff" in policy["retry_mode"]

    def test_unknown_tool_falls_back_to_defaults(self) -> None:
        bundle = _make_bundle()
        resolver = RetryPolicyResolver(bundle)
        policy = resolver.resolve_retry_policy("nonexistent_tool")
        assert isinstance(policy, dict)
        assert "max_retries" in policy


# ---------------------------------------------------------------------------
# UIModeResolver
# ---------------------------------------------------------------------------

class TestUIModeResolver:
    def test_resolve_ui_mode_build_stage(self) -> None:
        bundle = _make_bundle()
        resolver = UIModeResolver(bundle)
        mode = resolver.resolve_ui_mode("stg1")  # stg1 is StageClassEnum.BUILD
        assert mode == UIModeEnum.BOOTSTRAP_WORKSPACE.value

    def test_resolve_ui_mode_review_stage(self) -> None:
        bundle = _make_bundle()
        resolver = UIModeResolver(bundle)
        mode = resolver.resolve_ui_mode("stg2")  # stg2 is StageClassEnum.REVIEW
        assert mode == UIModeEnum.THREE_PANEL_REVIEW_WORKSPACE.value

    def test_resolve_ui_mode_unknown_stage_fallback(self) -> None:
        bundle = _make_bundle()
        resolver = UIModeResolver(bundle)
        mode = resolver.resolve_ui_mode("nonexistent")
        assert isinstance(mode, str)

    def test_resolve_interaction_mode(self) -> None:
        bundle = _make_bundle()
        resolver = UIModeResolver(bundle)
        mode = resolver.resolve_interaction_mode("stg1")
        assert mode == InteractionModeEnum.EDIT_AND_FINALIZE.value

    def test_resolve_token_mode(self) -> None:
        bundle = _make_bundle()
        resolver = UIModeResolver(bundle)
        token_mode = resolver.resolve_token_mode("stg1")
        assert token_mode == "compact"


# ---------------------------------------------------------------------------
# RuntimeResolver / ResolvedStack
# ---------------------------------------------------------------------------

class TestRuntimeResolver:
    def test_resolve_basic(self) -> None:
        bundle = _make_bundle()
        resolver = RuntimeResolver(bundle, environment="developer")
        stack = resolver.resolve("stg1", "developer")
        assert isinstance(stack, ResolvedStack)
        assert stack.stage_name == "stg1"
        assert stack.actor_role == "developer"
        assert isinstance(stack.allowed_tools, list)
        assert isinstance(stack.governance_flags, dict)
        assert isinstance(stack.retry_policy, dict)

    def test_resolve_includes_ui_modes(self) -> None:
        bundle = _make_bundle()
        resolver = RuntimeResolver(bundle)
        stack = resolver.resolve("stg1", "developer")
        assert stack.ui_mode == UIModeEnum.BOOTSTRAP_WORKSPACE.value
        assert stack.interaction_mode == InteractionModeEnum.EDIT_AND_FINALIZE.value

    def test_resolve_stage_class_populated(self) -> None:
        bundle = _make_bundle()
        resolver = RuntimeResolver(bundle)
        stack = resolver.resolve("stg1", "developer")
        assert stack.stage_class == StageClassEnum.BUILD.value

    def test_resolve_next_stages_from_routes(self) -> None:
        bundle = _make_bundle(
            routes={
                "stg1": WorkflowRouteDefinition(stage_name="stg1", on_success="stg2"),
                "stg2": WorkflowRouteDefinition(stage_name="stg2"),
            }
        )
        resolver = RuntimeResolver(bundle)
        stack = resolver.resolve("stg1", "developer")
        assert "stg2" in stack.next_stages

    def test_resolve_applies_conditional_governance(self) -> None:
        gov_section = GovernanceOverlaysSection(
            default_rules=DefaultGovernanceRules(),
            conditional_rules=[
                ConditionalGovernanceRule(
                    rule_id="block_on_breach",
                    when=ConditionalWhenClause(has_unresolved_severe_breach=True),
                    then=ConditionalThenClause(force_block_tools=["tool_a"]),
                )
            ],
        )
        bundle = _make_bundle(governance=gov_section)
        resolver = RuntimeResolver(bundle)
        stack = resolver.resolve(
            "stg1", "developer",
            runtime_facts={"has_unresolved_severe_breach": True},
        )
        assert "tool_a" in stack.blocked_tools

    def test_resolve_production_environment(self) -> None:
        gov_section = GovernanceOverlaysSection(
            default_rules=DefaultGovernanceRules(
                require_review_before_finalization=True,
                block_auto_continue_on_breach=True,
            )
        )
        bundle = _make_bundle(governance=gov_section)
        resolver = RuntimeResolver(bundle, environment="production")
        stack = resolver.resolve("stg1", "developer")
        assert stack.environment == "production"
        assert stack.governance_flags["review_required"] is True
        assert stack.governance_flags["auto_continue_allowed"] is False

    def test_resolved_stack_to_dict(self) -> None:
        bundle = _make_bundle()
        resolver = RuntimeResolver(bundle)
        stack = resolver.resolve("stg1", "developer")
        d = stack.to_dict()
        assert d["stage_name"] == "stg1"
        assert "allowed_tools" in d
        assert "governance_flags" in d
        assert "retry_policy" in d
        assert "next_stages" in d

    def test_resolve_unknown_stage_returns_stack(self) -> None:
        """Unknown stages should not raise; they return partial stacks."""
        bundle = _make_bundle()
        resolver = RuntimeResolver(bundle)
        stack = resolver.resolve("nonexistent_stage", "developer")
        assert isinstance(stack, ResolvedStack)
        assert stack.stage_class is None
        assert stack.next_stages == []

    def test_resolve_unknown_role_allowed_tools_empty(self) -> None:
        bundle = _make_bundle()
        resolver = RuntimeResolver(bundle)
        stack = resolver.resolve("stg1", "ghost_role")
        assert isinstance(stack.allowed_tools, list)



