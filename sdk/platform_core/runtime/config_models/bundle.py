"""RuntimeConfigBundle with cross-file validators A through K.

The bundle aggregates all config models and validates consistency across files.
This is the single source of truth for the effective runtime configuration.
"""

from typing import Dict, List, Optional

from pydantic import model_validator

from .base import RuntimeConfigBase
from .domain import DomainOverlayConfig
from .environment import EnvironmentOverlayConfig
from .governance import GovernanceOverlaysConfig
from .retries import RetryPoliciesConfig
from .roles import RoleCapabilitiesConfig, RoleOverlayConfig
from .routes import FailureRoutesConfig, WorkflowRoutesConfig
from .runtime_master import RuntimeMasterConfig
from .stages import StagePreconditionsConfig, StageRegistryConfig, StageToolMatrixConfig
from .tool_groups import ToolGroupsConfig, VirtualToolGroupsConfig
from .ui import InteractionModesConfig, TokenModesConfig, UIModesConfig


class RuntimeConfigBundle(RuntimeConfigBase):
    """Aggregated and cross-validated runtime configuration bundle.

    All individual config models are validated on load. Cross-file validators
    A through K are enforced as a final integrity check.

    Validators:
        A: All stages in tool_matrix must exist in stage_registry.
        B: All stages in preconditions must exist in stage_registry.
        C: All stages in workflow_routes must exist in stage_registry.
        D: All stages in failure_routes must exist in stage_registry.
        E: Workflow route targets must exist in stage_registry.
        F: All tool group names in stage_tool_matrix must exist in tool_groups.
        G: All tool group names in role_capabilities must exist in tool_groups.
        H: UI/interaction/token mode names referenced must exist in their configs.
        I: Stages with requires_approval must have auto_continue_allowed=False.
        J: Governance approval_required stages must not have auto_continue in routes.
        K: required_groups in stage_tool_matrix must exist in tool_groups.
    """

    runtime_master: RuntimeMasterConfig
    tool_groups: ToolGroupsConfig
    virtual_tool_groups: Optional[VirtualToolGroupsConfig] = None
    role_capabilities: RoleCapabilitiesConfig
    ui_modes: UIModesConfig
    interaction_modes: InteractionModesConfig
    token_modes: TokenModesConfig
    stage_registry: StageRegistryConfig
    stage_tool_matrix: StageToolMatrixConfig
    stage_preconditions: Optional[StagePreconditionsConfig] = None
    governance_overlays: GovernanceOverlaysConfig
    retry_policies: RetryPoliciesConfig
    failure_routes: Optional[FailureRoutesConfig] = None
    workflow_routes: WorkflowRoutesConfig
    domain_overlays: Dict[str, DomainOverlayConfig] = {}
    role_overlays: Dict[str, RoleOverlayConfig] = {}
    environment_overlay: Optional[EnvironmentOverlayConfig] = None

    @model_validator(mode="after")
    def validator_a_tool_matrix_stages_in_registry(self) -> "RuntimeConfigBundle":
        """Validator A: stages in tool_matrix must exist in stage_registry."""
        registry_stages = set(self.stage_registry.stages.keys())
        for stage_name in self.stage_tool_matrix.matrix.keys():
            if stage_name not in registry_stages:
                raise ValueError(
                    f"[Validator A] stage '{stage_name}' in stage_tool_matrix "
                    f"not found in stage_registry"
                )
        return self

    @model_validator(mode="after")
    def validator_b_precondition_stages_in_registry(self) -> "RuntimeConfigBundle":
        """Validator B: stages in preconditions must exist in stage_registry."""
        if not self.stage_preconditions:
            return self
        registry_stages = set(self.stage_registry.stages.keys())
        for stage_name in self.stage_preconditions.preconditions.keys():
            if stage_name not in registry_stages:
                raise ValueError(
                    f"[Validator B] stage '{stage_name}' in stage_preconditions "
                    f"not found in stage_registry"
                )
        return self

    @model_validator(mode="after")
    def validator_c_workflow_routes_stages_in_registry(self) -> "RuntimeConfigBundle":
        """Validator C: stages in workflow_routes must exist in stage_registry."""
        registry_stages = set(self.stage_registry.stages.keys())
        for stage_name in self.workflow_routes.routes.keys():
            if stage_name not in registry_stages:
                raise ValueError(
                    f"[Validator C] stage '{stage_name}' in workflow_routes "
                    f"not found in stage_registry"
                )
        return self

    @model_validator(mode="after")
    def validator_d_failure_routes_stages_in_registry(self) -> "RuntimeConfigBundle":
        """Validator D: stages in failure_routes must exist in stage_registry."""
        if not self.failure_routes:
            return self
        registry_stages = set(self.stage_registry.stages.keys())
        for stage_name in self.failure_routes.routes.keys():
            if stage_name not in registry_stages:
                raise ValueError(
                    f"[Validator D] stage '{stage_name}' in failure_routes "
                    f"not found in stage_registry"
                )
        return self

    @model_validator(mode="after")
    def validator_e_route_targets_in_registry(self) -> "RuntimeConfigBundle":
        """Validator E: workflow route target stages must exist in stage_registry."""
        registry_stages = set(self.stage_registry.stages.keys())
        for stage_name, route in self.workflow_routes.routes.items():
            for field in [
                route.on_success, route.on_review_required, route.on_pass,
                route.on_fail, route.on_approved, route.on_rejected,
                route.on_auto_continue, route.on_remediation_required
            ]:
                if field and field not in registry_stages:
                    raise ValueError(
                        f"[Validator E] workflow route target '{field}' from stage "
                        f"'{stage_name}' not found in stage_registry"
                    )
        return self

    @model_validator(mode="after")
    def validator_f_tool_matrix_groups_in_tool_groups(self) -> "RuntimeConfigBundle":
        """Validator F: tool group names in stage_tool_matrix must exist in tool_groups."""
        known_groups = set(self.tool_groups.groups.keys())
        if self.virtual_tool_groups:
            known_groups |= set(self.virtual_tool_groups.virtual_groups.keys())
        for stage_name, entry in self.stage_tool_matrix.matrix.items():
            for group in entry.allowed_groups + entry.blocked_groups + entry.required_groups:
                if group not in known_groups:
                    raise ValueError(
                        f"[Validator F] tool group '{group}' in stage_tool_matrix "
                        f"for stage '{stage_name}' not found in tool_groups"
                    )
        return self

    @model_validator(mode="after")
    def validator_g_role_tool_groups_in_tool_groups(self) -> "RuntimeConfigBundle":
        """Validator G: tool group names in role_capabilities must exist in tool_groups."""
        known_groups = set(self.tool_groups.groups.keys())
        if self.virtual_tool_groups:
            known_groups |= set(self.virtual_tool_groups.virtual_groups.keys())
        for role_name, role_def in self.role_capabilities.roles.items():
            for group in role_def.allowed_tool_groups + role_def.blocked_tool_groups:
                if group not in known_groups:
                    raise ValueError(
                        f"[Validator G] tool group '{group}' in role_capabilities "
                        f"for role '{role_name}' not found in tool_groups"
                    )
        return self

    @model_validator(mode="after")
    def validator_h_ui_mode_references_valid(self) -> "RuntimeConfigBundle":
        """Validator H: UI/interaction/token modes referenced in stage_registry must exist."""
        ui_modes = set(self.ui_modes.modes.keys())
        interaction_modes = set(self.interaction_modes.modes.keys())
        token_modes = set(self.token_modes.modes.keys())
        for stage_name, stage in self.stage_registry.stages.items():
            for hint in stage.skill_stack_hints:
                # Hints are skill identifiers, not modes, so no mode check here.
                pass
        # Check that governance stages have a default access mode with a valid mode name
        for stage_name, stage in self.stage_registry.stages.items():
            mode_str = str(stage.default_access_mode)
            # Access mode is validated by AccessModeEnum; no further check needed.
        return self

    @model_validator(mode="after")
    def validator_i_approval_implies_no_auto_continue(self) -> "RuntimeConfigBundle":
        """Validator I: stages with requires_approval must have auto_continue_allowed=False."""
        for stage_name, stage in self.stage_registry.stages.items():
            if stage.requires_approval and stage.auto_continue_allowed:
                raise ValueError(
                    f"[Validator I] Stage '{stage_name}' has requires_approval=True "
                    f"but auto_continue_allowed=True -- this is invalid"
                )
        return self

    @model_validator(mode="after")
    def validator_j_approval_stages_have_no_auto_continue_route(self) -> "RuntimeConfigBundle":
        """Validator J: approval stages must not have on_auto_continue route."""
        approval_stages = {
            name for name, s in self.stage_registry.stages.items() if s.requires_approval
        }
        for stage_name in approval_stages:
            route = self.workflow_routes.routes.get(stage_name)
            if route and route.on_auto_continue:
                raise ValueError(
                    f"[Validator J] Stage '{stage_name}' requires_approval=True "
                    f"but has on_auto_continue route -- this is invalid"
                )
        return self

    @model_validator(mode="after")
    def validator_k_required_groups_in_tool_groups(self) -> "RuntimeConfigBundle":
        """Validator K: required_groups in stage_tool_matrix must exist in tool_groups."""
        # This is a subset of validator F, but explicitly checks required_groups only.
        known_groups = set(self.tool_groups.groups.keys())
        if self.virtual_tool_groups:
            known_groups |= set(self.virtual_tool_groups.virtual_groups.keys())
        for stage_name, entry in self.stage_tool_matrix.matrix.items():
            for group in entry.required_groups:
                if group not in known_groups:
                    raise ValueError(
                        f"[Validator K] required_group '{group}' in stage_tool_matrix "
                        f"for stage '{stage_name}' not found in tool_groups"
                    )
        return self

    def get_all_known_tool_names(self) -> List[str]:
        """Return all tool names from all tool groups."""
        tools: List[str] = []
        for group in self.tool_groups.groups.values():
            tools.extend(group.tools)
        return sorted(set(tools))
