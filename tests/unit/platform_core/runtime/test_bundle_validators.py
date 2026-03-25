"""Unit tests for RuntimeConfigBundle cross-file validators A-K."""

import pytest
from pydantic import ValidationError

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.config_models.enums import (
    AccessModeEnum,
    InteractionModeEnum,
    StageClassEnum,
    TokenModeEnum,
    UIModeEnum,
)
from sdk.platform_core.runtime.config_models.governance import (
    DefaultGovernanceRules,
    GovernanceOverlaysConfig,
    GovernanceOverlaysSection,
)
from sdk.platform_core.runtime.config_models.retries import (
    RetryDefaults,
    RetryPoliciesConfig,
    RetryPoliciesSection,
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
)
from sdk.platform_core.runtime.config_models.ui import (
    InteractionModeDefinition,
    InteractionModesConfig,
    TokenModeDefinition,
    TokenModesConfig,
    UIModeDefinition,
    UIModesConfig,
)


def _build_bundle(
    stages: dict,
    tool_matrix: dict,
    tool_groups: dict,
    role_groups: list,
    workflow_routes: dict,
    with_approval_routes: bool = False,
) -> RuntimeConfigBundle:
    role_caps = RoleCapabilitiesConfig(
        roles={
            "developer": RoleCapabilityDefinition(
                role="developer",
                allowed_tool_groups=role_groups,
                blocked_tool_groups=[],
                allowed_stages=list(stages.keys()),
            )
        }
    )
    return RuntimeConfigBundle(
        runtime_master=RuntimeMasterConfig(runtime=RuntimeMasterSection()),
        tool_groups=ToolGroupsConfig(groups=tool_groups),
        role_capabilities=role_caps,
        ui_modes=UIModesConfig(
            modes={"ws": UIModeDefinition(mode=UIModeEnum.BOOTSTRAP_WORKSPACE)}
        ),
        interaction_modes=InteractionModesConfig(
            modes={"edit": InteractionModeDefinition(mode=InteractionModeEnum.EDIT_AND_FINALIZE)}
        ),
        token_modes=TokenModesConfig(
            modes={"full": TokenModeDefinition(mode=TokenModeEnum.FULL)}
        ),
        stage_registry=StageRegistryConfig(stages=stages),
        stage_tool_matrix=StageToolMatrixConfig(matrix=tool_matrix),
        governance_overlays=GovernanceOverlaysConfig(
            governance=GovernanceOverlaysSection(default_rules=DefaultGovernanceRules())
        ),
        retry_policies=RetryPoliciesConfig(
            retry_policies=RetryPoliciesSection(defaults=RetryDefaults())
        ),
        workflow_routes=WorkflowRoutesConfig(routes=workflow_routes),
    )


def _stage(name: str) -> StageDefinition:
    return StageDefinition(
        stage_name=name,
        stage_class=StageClassEnum.BUILD,
        default_access_mode=AccessModeEnum.BUILD_ONLY,
    )


def _matrix_entry(name: str, allowed: list | None = None) -> StageToolMatrixEntry:
    return StageToolMatrixEntry(
        stage_name=name,
        allowed_groups=allowed or ["grp_a"],
    )


def _route(name: str, **kwargs: str) -> WorkflowRouteDefinition:
    return WorkflowRouteDefinition(stage_name=name, **kwargs)


class TestBundleValidatorA:
    """Validator A: stages in tool_matrix must exist in stage_registry."""

    def test_valid_bundle(self, minimal_bundle: RuntimeConfigBundle) -> None:
        assert minimal_bundle is not None

    def test_unknown_stage_in_matrix_raises(self) -> None:
        stages = {"stage_a": _stage("stage_a")}
        matrix = {
            "stage_a": _matrix_entry("stage_a"),
            "stage_ghost": _matrix_entry("stage_ghost"),  # not in registry
        }
        with pytest.raises(ValidationError, match="Validator A"):
            _build_bundle(
                stages=stages,
                tool_matrix=matrix,
                tool_groups={"grp_a": ToolGroupDefinition(group_name="grp_a", tools=["t1"])},
                role_groups=["grp_a"],
                workflow_routes={"stage_a": _route("stage_a")},
            )


class TestBundleValidatorC:
    """Validator C: stages in workflow_routes must exist in stage_registry."""

    def test_unknown_stage_in_routes_raises(self) -> None:
        stages = {"stage_a": _stage("stage_a")}
        with pytest.raises(ValidationError, match="Validator C"):
            _build_bundle(
                stages=stages,
                tool_matrix={"stage_a": _matrix_entry("stage_a")},
                tool_groups={"grp_a": ToolGroupDefinition(group_name="grp_a", tools=["t1"])},
                role_groups=["grp_a"],
                workflow_routes={
                    "stage_a": _route("stage_a"),
                    "nonexistent_stage": _route("nonexistent_stage"),
                },
            )


class TestBundleValidatorE:
    """Validator E: workflow route target stages must exist in stage_registry."""

    def test_unknown_target_raises(self) -> None:
        stages = {"stage_a": _stage("stage_a")}
        with pytest.raises(ValidationError, match="Validator E"):
            _build_bundle(
                stages=stages,
                tool_matrix={"stage_a": _matrix_entry("stage_a")},
                tool_groups={"grp_a": ToolGroupDefinition(group_name="grp_a", tools=["t1"])},
                role_groups=["grp_a"],
                workflow_routes={
                    "stage_a": _route("stage_a", on_success="stage_does_not_exist"),
                },
            )

    def test_valid_target(self) -> None:
        stages = {"stage_a": _stage("stage_a"), "stage_b": _stage("stage_b")}
        bundle = _build_bundle(
            stages=stages,
            tool_matrix={
                "stage_a": _matrix_entry("stage_a"),
                "stage_b": _matrix_entry("stage_b"),
            },
            tool_groups={"grp_a": ToolGroupDefinition(group_name="grp_a", tools=["t1"])},
            role_groups=["grp_a"],
            workflow_routes={
                "stage_a": _route("stage_a", on_success="stage_b"),
                "stage_b": _route("stage_b"),
            },
        )
        assert bundle is not None


class TestBundleValidatorF:
    """Validator F: tool group names in stage_tool_matrix must exist in tool_groups."""

    def test_unknown_group_in_matrix_raises(self) -> None:
        stages = {"stage_a": _stage("stage_a")}
        with pytest.raises(ValidationError, match="Validator F"):
            _build_bundle(
                stages=stages,
                tool_matrix={
                    "stage_a": StageToolMatrixEntry(
                        stage_name="stage_a",
                        allowed_groups=["nonexistent_group"],
                    )
                },
                tool_groups={"grp_a": ToolGroupDefinition(group_name="grp_a", tools=["t1"])},
                role_groups=["grp_a"],
                workflow_routes={"stage_a": _route("stage_a")},
            )


class TestBundleValidatorG:
    """Validator G: tool group names in role_capabilities must exist in tool_groups."""

    def test_unknown_group_in_role_caps_raises(self) -> None:
        stages = {"stage_a": _stage("stage_a")}
        with pytest.raises(ValidationError, match="Validator G"):
            _build_bundle(
                stages=stages,
                tool_matrix={"stage_a": _matrix_entry("stage_a")},
                tool_groups={"grp_a": ToolGroupDefinition(group_name="grp_a", tools=["t1"])},
                role_groups=["grp_a", "nonexistent_group"],  # nonexistent_group not in tool_groups
                workflow_routes={"stage_a": _route("stage_a")},
            )


class TestBundleValidatorI:
    """Validator I: stages with requires_approval must have auto_continue_allowed=False.

    Note: This is already enforced at StageDefinition level, so this test confirms
    the StageDefinition validator catches it before the bundle validator.
    """

    def test_stage_level_validation_catches_approval_auto_continue(self) -> None:
        """StageDefinition itself raises, so bundle validator I is redundant but safe."""
        with pytest.raises(ValidationError):
            StageDefinition(
                stage_name="bad_stage",
                stage_class=StageClassEnum.APPROVAL,
                default_access_mode=AccessModeEnum.REVIEW_REQUIRED,
                requires_review=True,
                requires_approval=True,
                auto_continue_allowed=True,
            )


class TestBundleValidatorJ:
    """Validator J: approval stages must not have on_auto_continue route."""

    def test_approval_stage_with_auto_continue_route_raises(self) -> None:
        approval_stage = StageDefinition(
            stage_name="approval_stage",
            stage_class=StageClassEnum.APPROVAL,
            default_access_mode=AccessModeEnum.REVIEW_REQUIRED,
            requires_review=True,
            requires_approval=True,
            auto_continue_allowed=False,
        )
        stages = {"approval_stage": approval_stage}
        with pytest.raises(ValidationError, match="Validator J"):
            _build_bundle(
                stages=stages,
                tool_matrix={"approval_stage": _matrix_entry("approval_stage")},
                tool_groups={"grp_a": ToolGroupDefinition(group_name="grp_a", tools=["t1"])},
                role_groups=["grp_a"],
                workflow_routes={
                    "approval_stage": _route(
                        "approval_stage", on_auto_continue="approval_stage"
                    )
                },
            )


class TestBundleGetAllToolNames:
    def test_returns_sorted_unique(self, minimal_bundle: RuntimeConfigBundle) -> None:
        tools = minimal_bundle.get_all_known_tool_names()
        assert tools == sorted(set(tools))
