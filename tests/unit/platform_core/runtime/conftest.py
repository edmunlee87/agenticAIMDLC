"""Shared fixtures for platform_core runtime unit tests."""

import pytest

from sdk.platform_core.runtime.config_models.enums import (
    AccessModeEnum,
    RetryModeEnum,
    StageClassEnum,
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
from sdk.platform_core.runtime.config_models.enums import (
    InteractionModeEnum,
    TokenModeEnum,
    UIModeEnum,
)
from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle


def _make_stage(name: str, stage_class: StageClassEnum = StageClassEnum.BUILD) -> StageDefinition:
    return StageDefinition(
        stage_name=name,
        stage_class=stage_class,
        default_access_mode=AccessModeEnum.BUILD_ONLY,
    )


def _make_approval_stage(name: str) -> StageDefinition:
    return StageDefinition(
        stage_name=name,
        stage_class=StageClassEnum.APPROVAL,
        default_access_mode=AccessModeEnum.REVIEW_REQUIRED,
        requires_review=True,
        requires_approval=True,
        auto_continue_allowed=False,
    )


@pytest.fixture()
def minimal_bundle() -> RuntimeConfigBundle:
    """A minimal but fully valid RuntimeConfigBundle for testing validators."""
    stages = {
        "stage_a": _make_stage("stage_a"),
        "stage_b": _make_stage("stage_b"),
    }
    tool_groups = ToolGroupsConfig(
        groups={"grp_a": ToolGroupDefinition(group_name="grp_a", tools=["tool1"])}
    )
    role_caps = RoleCapabilitiesConfig(
        roles={
            "developer": RoleCapabilityDefinition(
                role="developer",
                allowed_tool_groups=["grp_a"],
                blocked_tool_groups=[],
                allowed_stages=["stage_a", "stage_b"],
            )
        }
    )
    ui_modes = UIModesConfig(
        modes={"ws": UIModeDefinition(mode=UIModeEnum.BOOTSTRAP_WORKSPACE)}
    )
    interaction_modes = InteractionModesConfig(
        modes={"edit": InteractionModeDefinition(mode=InteractionModeEnum.EDIT_AND_FINALIZE)}
    )
    token_modes = TokenModesConfig(
        modes={"full": TokenModeDefinition(mode=TokenModeEnum.FULL)}
    )
    stage_registry = StageRegistryConfig(stages=stages)
    stage_tool_matrix = StageToolMatrixConfig(
        matrix={
            "stage_a": StageToolMatrixEntry(stage_name="stage_a", allowed_groups=["grp_a"]),
            "stage_b": StageToolMatrixEntry(stage_name="stage_b", allowed_groups=["grp_a"]),
        }
    )
    governance = GovernanceOverlaysConfig(
        governance=GovernanceOverlaysSection(default_rules=DefaultGovernanceRules())
    )
    retry_policies = RetryPoliciesConfig(
        retry_policies=RetryPoliciesSection(defaults=RetryDefaults())
    )
    workflow_routes = WorkflowRoutesConfig(
        routes={
            "stage_a": WorkflowRouteDefinition(stage_name="stage_a", on_success="stage_b"),
            "stage_b": WorkflowRouteDefinition(stage_name="stage_b"),
        }
    )
    return RuntimeConfigBundle(
        runtime_master=RuntimeMasterConfig(runtime=RuntimeMasterSection()),
        tool_groups=tool_groups,
        role_capabilities=role_caps,
        ui_modes=ui_modes,
        interaction_modes=interaction_modes,
        token_modes=token_modes,
        stage_registry=stage_registry,
        stage_tool_matrix=stage_tool_matrix,
        governance_overlays=governance,
        retry_policies=retry_policies,
        workflow_routes=workflow_routes,
    )
