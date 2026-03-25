"""Unit tests for individual Pydantic config model classes."""

import pytest
from pydantic import ValidationError

from sdk.platform_core.runtime.config_models.base import RuntimeConfigBase
from sdk.platform_core.runtime.config_models.enums import (
    AccessModeEnum,
    ActorRoleEnum,
    EnvironmentNameEnum,
    InteractionModeEnum,
    RetryModeEnum,
    StageClassEnum,
    TokenModeEnum,
    UIModeEnum,
)
from sdk.platform_core.runtime.config_models.fragments import (
    EnabledModules,
    FileRefMap,
    ResolverDefaults,
    RouteList,
    StageRouteMap,
    StringListRule,
    ToolListModel,
)
from sdk.platform_core.runtime.config_models.governance import (
    ConditionalGovernanceRule,
    ConditionalThenClause,
    ConditionalWhenClause,
    DefaultGovernanceRules,
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
    FailureRouteEntry,
    WorkflowRouteDefinition,
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
)
from sdk.platform_core.runtime.config_models.ui import (
    InteractionModeDefinition,
    InteractionModesConfig,
    TokenModeDefinition,
    TokenModesConfig,
    UIModeDefinition,
    UIModesConfig,
)
# InteractionModeEnum, TokenModeEnum, UIModeEnum are already imported from enums above


# ---------------------------------------------------------------------------
# RuntimeConfigBase
# ---------------------------------------------------------------------------

class TestRuntimeConfigBase:
    def test_extra_field_forbidden(self) -> None:
        with pytest.raises(ValidationError):
            RuntimeConfigBase.model_validate({"unexpected_key": "value"})


# ---------------------------------------------------------------------------
# RuntimeMasterSection / RuntimeMasterConfig
# ---------------------------------------------------------------------------

class TestRuntimeMasterSection:
    def test_defaults(self) -> None:
        section = RuntimeMasterSection()
        assert section.environment == EnvironmentNameEnum.DEV
        assert section.schema_version == "1.0.0"

    def test_valid_semver(self) -> None:
        section = RuntimeMasterSection(schema_version="2.3.1")
        assert section.schema_version == "2.3.1"

    def test_invalid_semver_raises(self) -> None:
        with pytest.raises(ValidationError):
            RuntimeMasterSection(schema_version="1.0")

    def test_invalid_semver_non_digit(self) -> None:
        with pytest.raises(ValidationError):
            RuntimeMasterSection(schema_version="1.a.0")


class TestRuntimeMasterConfig:
    def test_minimal_valid(self) -> None:
        cfg = RuntimeMasterConfig(runtime=RuntimeMasterSection())
        assert cfg.modules is None
        assert cfg.file_refs is None


# ---------------------------------------------------------------------------
# ToolGroupsConfig
# ---------------------------------------------------------------------------

class TestToolGroupsConfig:
    def test_single_group(self) -> None:
        cfg = ToolGroupsConfig(
            groups={"grp_a": ToolGroupDefinition(group_name="grp_a", tools=["tool1", "tool2"])}
        )
        assert "grp_a" in cfg.groups
        assert cfg.groups["grp_a"].tools == ["tool1", "tool2"]

    def test_empty_tools_raises(self) -> None:
        with pytest.raises(ValidationError):
            ToolGroupsConfig(
                groups={"empty": ToolGroupDefinition(group_name="empty", tools=[])}
            )

    def test_blank_group_name_raises(self) -> None:
        with pytest.raises(ValidationError):
            ToolGroupDefinition(group_name="  ", tools=["t1"])


# ---------------------------------------------------------------------------
# RoleCapabilitiesConfig
# ---------------------------------------------------------------------------

class TestRoleCapabilitiesConfig:
    def test_role_with_no_groups(self) -> None:
        role_def = RoleCapabilityDefinition(
            role="developer",
            allowed_tool_groups=[],
            blocked_tool_groups=[],
            allowed_stages=[],
        )
        cfg = RoleCapabilitiesConfig(roles={"developer": role_def})
        assert cfg.roles["developer"].role == "developer"
        assert cfg.roles["developer"].can_approve is False

    def test_role_with_groups(self) -> None:
        role_def = RoleCapabilityDefinition(
            role="approver",
            allowed_tool_groups=["grp_a", "grp_b"],
            blocked_tool_groups=["grp_c"],
            allowed_stages=["stage_x"],
            can_approve=True,
        )
        cfg = RoleCapabilitiesConfig(roles={"approver": role_def})
        assert "grp_a" in cfg.roles["approver"].allowed_tool_groups
        assert cfg.roles["approver"].can_approve is True

    def test_allowed_blocked_overlap_raises(self) -> None:
        with pytest.raises(ValidationError):
            RoleCapabilityDefinition(
                role="developer",
                allowed_tool_groups=["grp_a"],
                blocked_tool_groups=["grp_a"],
            )


# ---------------------------------------------------------------------------
# UIModesConfig / InteractionModesConfig / TokenModesConfig
# ---------------------------------------------------------------------------

class TestUIModesConfig:
    def test_basic_mode(self) -> None:
        mode = UIModeDefinition(
            mode=UIModeEnum.THREE_PANEL_REVIEW_WORKSPACE,
            panels=["left", "center"],
        )
        cfg = UIModesConfig(modes={"three_panel_review_workspace": mode})
        assert "left" in cfg.modes["three_panel_review_workspace"].panels

    def test_empty_modes_raises(self) -> None:
        with pytest.raises(ValidationError):
            UIModesConfig(modes={})


class TestInteractionModesConfig:
    def test_edit_mode(self) -> None:
        mode = InteractionModeDefinition(
            mode=InteractionModeEnum.EDIT_AND_FINALIZE,
            allowed_actions=["submit", "edit"],
            requires_structured_input=False,
        )
        cfg = InteractionModesConfig(modes={"edit_and_finalize": mode})
        assert "submit" in cfg.modes["edit_and_finalize"].allowed_actions

    def test_empty_modes_raises(self) -> None:
        with pytest.raises(ValidationError):
            InteractionModesConfig(modes={})


class TestTokenModesConfig:
    def test_full_mode(self) -> None:
        mode = TokenModeDefinition(
            mode=TokenModeEnum.FULL,
            max_prompt_tokens=8192,
            max_completion_tokens=4096,
            retrieval_top_k=10,
        )
        cfg = TokenModesConfig(modes={"full": mode})
        assert cfg.modes["full"].max_prompt_tokens == 8192

    def test_zero_tokens_raises(self) -> None:
        with pytest.raises(ValidationError):
            TokenModeDefinition(
                mode=TokenModeEnum.MINIMAL,
                max_prompt_tokens=0,
                max_completion_tokens=1024,
            )

    def test_negative_tokens_raises(self) -> None:
        with pytest.raises(ValidationError):
            TokenModeDefinition(
                mode=TokenModeEnum.MINIMAL,
                max_prompt_tokens=-1,
                max_completion_tokens=1024,
            )

    def test_empty_modes_raises(self) -> None:
        with pytest.raises(ValidationError):
            TokenModesConfig(modes={})


# ---------------------------------------------------------------------------
# StageDefinition / StageRegistryConfig
# ---------------------------------------------------------------------------

class TestStageDefinition:
    def test_defaults(self) -> None:
        stage = StageDefinition(
            stage_name="build_stage",
            stage_class=StageClassEnum.BUILD,
            description="A build stage",
            default_access_mode=AccessModeEnum.BUILD_ONLY,
        )
        assert stage.requires_review is False
        assert stage.requires_approval is False
        assert stage.requires_audit is True
        assert stage.auto_continue_allowed is True

    def test_approval_with_auto_continue_raises_at_stage_level(self) -> None:
        # StageDefinition validates this directly.
        with pytest.raises(ValidationError):
            StageDefinition(
                stage_name="approval_stage",
                stage_class=StageClassEnum.APPROVAL,
                description="An approval stage",
                default_access_mode=AccessModeEnum.REVIEW_REQUIRED,
                requires_approval=True,
                auto_continue_allowed=True,
            )

    def test_approval_requires_review(self) -> None:
        with pytest.raises(ValidationError):
            StageDefinition(
                stage_name="approval_stage",
                stage_class=StageClassEnum.APPROVAL,
                description="Approval without review",
                default_access_mode=AccessModeEnum.REVIEW_REQUIRED,
                requires_approval=True,
                requires_review=False,
                auto_continue_allowed=False,
            )

    def test_valid_approval_stage(self) -> None:
        stage = StageDefinition(
            stage_name="model_approval",
            stage_class=StageClassEnum.APPROVAL,
            description="Valid approval stage",
            default_access_mode=AccessModeEnum.REVIEW_REQUIRED,
            requires_approval=True,
            requires_review=True,
            auto_continue_allowed=False,
        )
        assert stage.requires_approval is True
        assert stage.requires_review is True

    def test_blank_stage_name_raises(self) -> None:
        with pytest.raises(ValidationError):
            StageDefinition(
                stage_name="   ",
                stage_class=StageClassEnum.BUILD,
                default_access_mode=AccessModeEnum.BUILD_ONLY,
            )


class TestStageRegistryConfig:
    def test_register_stages(self) -> None:
        stage = StageDefinition(
            stage_name="stage_a",
            stage_class=StageClassEnum.BUILD,
            description="Stage A",
            default_access_mode=AccessModeEnum.BUILD_ONLY,
        )
        cfg = StageRegistryConfig(stages={"stage_a": stage})
        assert "stage_a" in cfg.stages

    def test_empty_registry_raises(self) -> None:
        with pytest.raises(ValidationError):
            StageRegistryConfig(stages={})


class TestStageToolMatrixConfig:
    def test_matrix_entry(self) -> None:
        entry = StageToolMatrixEntry(
            stage_name="stage_a",
            allowed_groups=["grp_a"],
            blocked_groups=[],
            required_groups=[],
        )
        cfg = StageToolMatrixConfig(matrix={"stage_a": entry})
        assert "grp_a" in cfg.matrix["stage_a"].allowed_groups

    def test_allowed_blocked_overlap_raises(self) -> None:
        with pytest.raises(ValidationError):
            StageToolMatrixEntry(
                stage_name="stage_b",
                allowed_groups=["grp_a"],
                blocked_groups=["grp_a"],
                required_groups=[],
            )


# ---------------------------------------------------------------------------
# GovernanceOverlays
# ---------------------------------------------------------------------------

class TestDefaultGovernanceRules:
    def test_defaults(self) -> None:
        rules = DefaultGovernanceRules()
        assert rules.block_auto_continue_on_breach is True
        assert rules.require_audit_for_all_approvals is True
        assert rules.require_review_before_finalization is True
        assert rules.min_evidence_count_for_review == 1

    def test_override_values(self) -> None:
        rules = DefaultGovernanceRules(
            block_auto_continue_on_breach=False,
            require_audit_for_all_approvals=False,
        )
        assert rules.block_auto_continue_on_breach is False


class TestStageGovernanceRule:
    def test_stage_level_override(self) -> None:
        rule = StageGovernanceRule(
            stage_name="stage_x",
            requires_review=True,
            requires_approval=False,
            auto_continue_allowed=False,
        )
        assert rule.requires_review is True
        assert rule.auto_continue_allowed is False

    def test_all_none_defaults(self) -> None:
        rule = StageGovernanceRule(stage_name="stage_y")
        assert rule.requires_review is None
        assert rule.requires_approval is None


class TestConditionalGovernanceRule:
    def test_conditional_rule(self) -> None:
        when = ConditionalWhenClause(has_unresolved_severe_breach=True)
        then = ConditionalThenClause(block_auto_continue=True)
        rule = ConditionalGovernanceRule(
            rule_id="cond_rule_1",
            description="Block on violations",
            when=when,
            then=then,
        )
        assert rule.rule_id == "cond_rule_1"
        assert rule.then.block_auto_continue is True

    def test_blank_rule_id_raises(self) -> None:
        with pytest.raises(ValidationError):
            ConditionalGovernanceRule(
                rule_id="  ",
                when=ConditionalWhenClause(),
                then=ConditionalThenClause(),
            )

    def test_applies_to_stages_filter(self) -> None:
        rule = ConditionalGovernanceRule(
            rule_id="filtered_rule",
            when=ConditionalWhenClause(),
            then=ConditionalThenClause(),
            applies_to_stages=["stage_a", "stage_b"],
        )
        assert "stage_a" in rule.applies_to_stages
        assert "stage_c" not in rule.applies_to_stages


# ---------------------------------------------------------------------------
# RetryPoliciesConfig
# ---------------------------------------------------------------------------

class TestRetryPoliciesConfig:
    def test_retry_defaults(self) -> None:
        defaults = RetryDefaults(
            max_retries=3,
            retry_mode=RetryModeEnum.EXPONENTIAL_BACKOFF,
        )
        assert defaults.max_retries == 3
        assert defaults.jitter is True

    def test_tool_retry_rule(self) -> None:
        rule = ToolRetryRule(
            tool_name="my-tool",
            max_retries=5,
            retry_mode=RetryModeEnum.FIXED,
        )
        cfg = RetryPoliciesConfig(
            retry_policies=RetryPoliciesSection(
                defaults=RetryDefaults(
                    max_retries=3,
                    retry_mode=RetryModeEnum.NONE,
                ),
                tool_rules=[rule],
            )
        )
        assert cfg.retry_policies.tool_rules[0].tool_name == "my-tool"

    def test_get_rule_for_tool(self) -> None:
        rule = ToolRetryRule(tool_name="artifact-write", max_retries=2)
        section = RetryPoliciesSection(tool_rules=[rule])
        found = section.get_rule_for_tool("artifact-write")
        assert found is not None
        assert found.max_retries == 2

    def test_get_rule_for_missing_tool_returns_none(self) -> None:
        section = RetryPoliciesSection()
        assert section.get_rule_for_tool("does-not-exist") is None

    def test_negative_max_retries_raises(self) -> None:
        with pytest.raises(ValidationError):
            RetryDefaults(max_retries=-1)

    def test_zero_delay_raises(self) -> None:
        with pytest.raises(ValidationError):
            RetryDefaults(initial_delay_ms=0)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

class TestWorkflowRouteDefinition:
    def test_on_success(self) -> None:
        route = WorkflowRouteDefinition(stage_name="stage_a", on_success="stage_b")
        assert route.on_success == "stage_b"
        assert route.on_fail is None

    def test_all_nones_by_default(self) -> None:
        route = WorkflowRouteDefinition(stage_name="stage_a")
        for field in ["on_success", "on_fail", "on_approved", "on_rejected",
                      "on_review_required", "on_auto_continue",
                      "on_pass", "on_remediation_required"]:
            assert getattr(route, field) is None

    def test_blank_stage_name_raises(self) -> None:
        with pytest.raises(ValidationError):
            WorkflowRouteDefinition(stage_name="  ")


class TestFailureRouteEntry:
    def test_failure_route(self) -> None:
        entry = FailureRouteEntry(
            stage_name="stage_a",
            error_type="TIMEOUT",
            recovery_action="retry",
            target_stage="stage_a",
        )
        assert entry.error_type == "TIMEOUT"
        assert entry.target_stage == "stage_a"

    def test_invalid_recovery_action_raises(self) -> None:
        with pytest.raises(ValidationError):
            FailureRouteEntry(
                stage_name="stage_a",
                recovery_action="delete_everything",
            )

    def test_catchall_error_type(self) -> None:
        entry = FailureRouteEntry(stage_name="stage_a", recovery_action="escalate")
        assert entry.error_type == "*"


# ---------------------------------------------------------------------------
# Fragments
# ---------------------------------------------------------------------------

class TestFragments:
    def test_tool_list_model(self) -> None:
        model = ToolListModel(group_name="grp_a", tools=["tool_a", "tool_b"])
        assert len(model.tools) == 2

    def test_route_list(self) -> None:
        rl = RouteList(routes=["stage_a", "stage_b"])
        assert "stage_a" in rl.routes

    def test_route_list_empty_raises(self) -> None:
        with pytest.raises(ValidationError):
            RouteList(routes=[])

    def test_string_list_rule(self) -> None:
        rule = StringListRule(name="my_allowlist", values=["val1", "val2"])
        assert "val1" in rule.values

    def test_stage_route_map(self) -> None:
        srm = StageRouteMap(routes={"stage_a": ["stage_b", "stage_c"]})
        assert "stage_b" in srm.routes["stage_a"]

    def test_stage_route_map_empty_raises(self) -> None:
        with pytest.raises(ValidationError):
            StageRouteMap(routes={})

    def test_resolver_defaults(self) -> None:
        rd = ResolverDefaults(
            unknown_stage_behavior="warn",
            stale_state_behavior="warn",
        )
        assert rd.unknown_stage_behavior == "warn"
        assert rd.enable_overlay_resolution is True

    def test_enabled_modules_with_flags(self) -> None:
        em = EnabledModules(modules={"hitl": True, "audit": True, "policy": False})
        assert em.modules["hitl"] is True
        assert em.modules["policy"] is False

    def test_file_ref_map(self) -> None:
        frm = FileRefMap(files={"stage_registry": "configs/runtime/stage_registry.yaml"})
        assert "stage_registry" in frm.files

    def test_file_ref_map_empty_raises(self) -> None:
        with pytest.raises(ValidationError):
            FileRefMap(files={})
