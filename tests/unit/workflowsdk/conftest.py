"""Fixtures for workflowsdk unit tests.

Re-exports ``minimal_bundle`` from the platform_core runtime conftest so that
WorkflowService tests can use a fully valid :class:`RuntimeConfigBundle`.
"""

import pytest

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


@pytest.fixture()
def minimal_bundle() -> RuntimeConfigBundle:
    """Minimal fully valid RuntimeConfigBundle for workflowsdk tests.

    Stages: stage_a -> stage_b (via on_success route).
    No preconditions, no failure routes.
    """
    stages = {
        "stage_a": StageDefinition(
            stage_name="stage_a",
            stage_class=StageClassEnum.BUILD,
            default_access_mode=AccessModeEnum.BUILD_ONLY,
        ),
        "stage_b": StageDefinition(
            stage_name="stage_b",
            stage_class=StageClassEnum.BUILD,
            default_access_mode=AccessModeEnum.BUILD_ONLY,
        ),
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
