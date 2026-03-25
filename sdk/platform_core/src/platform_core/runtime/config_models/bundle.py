"""RuntimeConfigBundle -- the single assembled config object.

The bundle is the canonical view of the entire runtime configuration after
all YAML files are loaded and overlays are applied. It is produced by the
:class:`~platform_core.runtime.config_loader.RuntimeConfigLoader` and consumed
by the :class:`~platform_core.runtime.resolver.RuntimeResolver`.

All cross-file validators (A through K) are defined here.
"""

from __future__ import annotations

from pydantic import Field, model_validator

from platform_core.runtime.config_models.base import ConfigModelBase
from platform_core.runtime.config_models.domain import DomainsConfig
from platform_core.runtime.config_models.environment import EnvironmentConfig
from platform_core.runtime.config_models.governance import GovernanceConfig
from platform_core.runtime.config_models.roles import RolesConfig
from platform_core.runtime.config_models.routes import RoutesConfig
from platform_core.runtime.config_models.stages import StagesConfig
from platform_core.runtime.config_models.tool_groups import ToolGroupConfig
from platform_core.runtime.config_models.ui import UIConfig


class RuntimeConfigBundle(ConfigModelBase):
    """The fully assembled, validated runtime configuration.

    Produced by RuntimeConfigLoader after loading all YAML base files and
    applying any active overlays. Immutable once constructed.

    Args:
        bundle_version: Monotonically increasing version used for cache invalidation.
        roles: All role configurations.
        stages: All stage configurations.
        routes: All stage routing configurations.
        governance: Policy pack and overlay engine configuration.
        tool_groups: Named tool group definitions.
        ui: UI mode and token budget configuration.
        domains: Domain configurations.
        environment: Active environment configuration.
    """

    bundle_version: str = "0.0.0"
    roles: RolesConfig = Field(default_factory=RolesConfig)
    stages: StagesConfig = Field(default_factory=StagesConfig)
    routes: RoutesConfig = Field(default_factory=RoutesConfig)
    governance: GovernanceConfig = Field(default_factory=GovernanceConfig)
    tool_groups: dict[str, ToolGroupConfig] = Field(default_factory=dict)
    ui: UIConfig = Field(default_factory=UIConfig)
    domains: DomainsConfig = Field(default_factory=DomainsConfig)
    environment: EnvironmentConfig = Field(default_factory=EnvironmentConfig)

    # ------------------------------------------------------------------
    # Cross-file validators (A through K)
    # ------------------------------------------------------------------

    @model_validator(mode="after")
    def _a_route_stages_exist(self) -> "RuntimeConfigBundle":
        """(A) Every route from_stage and to_stage must reference a known stage."""
        known = set(self.stages.stages)
        for route_id, route in self.routes.routes.items():
            for attr in ("from_stage", "to_stage"):
                sid = getattr(route, attr)
                if sid not in known:
                    raise ValueError(
                        f"[Validator A] Route '{route_id}' references unknown {attr} '{sid}'"
                    )
        return self

    @model_validator(mode="after")
    def _b_stage_entry_conditions_exist(self) -> "RuntimeConfigBundle":
        """(B) Stage entry_conditions must reference known stage IDs."""
        known = set(self.stages.stages)
        for stage_id, stage in self.stages.stages.items():
            for dep in stage.entry_conditions:
                if dep not in known:
                    raise ValueError(
                        f"[Validator B] Stage '{stage_id}' entry_condition '{dep}' "
                        "does not reference a known stage"
                    )
        return self

    @model_validator(mode="after")
    def _c_review_types_in_ui(self) -> "RuntimeConfigBundle":
        """(C) Each stage's governance gate review_type should be resolvable."""
        # Informational check -- warn only; don't block config load.
        for stage_id, stage in self.stages.stages.items():
            for gate in stage.governance_gates:
                if gate.requires_review and not gate.review_type.strip():
                    raise ValueError(
                        f"[Validator C] Stage '{stage_id}' gate '{gate.gate_id}' "
                        "requires_review=True but review_type is empty"
                    )
        return self

    @model_validator(mode="after")
    def _d_domain_policy_packs_exist(self) -> "RuntimeConfigBundle":
        """(D) Domain policy_pack_ids must reference known governance pack IDs."""
        known = set(self.governance.policy_packs)
        for domain_id, domain in self.domains.domains.items():
            for pack_id in domain.policy_pack_ids:
                if pack_id and pack_id not in known:
                    raise ValueError(
                        f"[Validator D] Domain '{domain_id}' references unknown "
                        f"policy_pack_id '{pack_id}'"
                    )
        return self

    @model_validator(mode="after")
    def _e_tool_groups_referenced_exist(self) -> "RuntimeConfigBundle":
        """(E) Tool allowlist include_groups and exclude_groups must reference known groups."""
        known_groups = set(self.tool_groups)
        for role_id, role in self.roles.roles.items():
            for group_id in (
                role.tool_allowlist.include_groups + role.tool_allowlist.exclude_groups
            ):
                if group_id and group_id not in known_groups:
                    raise ValueError(
                        f"[Validator E] Role '{role_id}' references unknown tool group '{group_id}'"
                    )
        return self

    @model_validator(mode="after")
    def _f_approval_roles_exist(self) -> "RuntimeConfigBundle":
        """(F) Governance gate approval_role must be a known role_id."""
        known_roles = set(self.roles.roles)
        for stage_id, stage in self.stages.stages.items():
            for gate in stage.governance_gates:
                if gate.approval_role and gate.approval_role not in known_roles:
                    raise ValueError(
                        f"[Validator F] Stage '{stage_id}' gate '{gate.gate_id}' "
                        f"references unknown approval_role '{gate.approval_role}'"
                    )
        return self

    @model_validator(mode="after")
    def _g_overlay_rules_apply_when_keys_valid(self) -> "RuntimeConfigBundle":
        """(G) GovernanceOverlayRule applies_when keys must be known field names."""
        allowed_keys = {
            "active_role", "active_domain", "validation_mode",
            "annual_review_mode", "remediation_mode", "environment",
        }
        for overlay in self.governance.overlay_rules:
            unknown = set(overlay.applies_when) - allowed_keys
            if unknown:
                raise ValueError(
                    f"[Validator G] Overlay '{overlay.overlay_id}' applies_when "
                    f"contains unknown keys: {sorted(unknown)}"
                )
        return self

    @model_validator(mode="after")
    def _h_terminal_stages_have_no_outbound_routes(self) -> "RuntimeConfigBundle":
        """(H) Terminal stages must not appear as from_stage in any route."""
        terminal_ids = {s for s, cfg in self.stages.stages.items() if cfg.is_terminal}
        for route_id, route in self.routes.routes.items():
            if route.from_stage in terminal_ids and not route.is_error_path:
                raise ValueError(
                    f"[Validator H] Terminal stage '{route.from_stage}' has a "
                    f"non-error outbound route '{route_id}'"
                )
        return self

    @model_validator(mode="after")
    def _i_default_domain_exists(self) -> "RuntimeConfigBundle":
        """(I) The default_domain_id must reference a known domain (if domains are configured)."""
        if self.domains.domains and self.domains.default_domain_id:
            if self.domains.default_domain_id not in self.domains.domains:
                raise ValueError(
                    f"[Validator I] default_domain_id '{self.domains.default_domain_id}' "
                    "not found in configured domains"
                )
        return self

    @model_validator(mode="after")
    def _j_ui_stage_configs_reference_known_stages(self) -> "RuntimeConfigBundle":
        """(J) StageUIModeConfig.stage_name must reference a known stage."""
        known = set(self.stages.stages)
        for cfg in self.ui.stage_ui_modes:
            if cfg.stage_name not in known:
                raise ValueError(
                    f"[Validator J] UI config references unknown stage '{cfg.stage_name}'"
                )
        return self

    @model_validator(mode="after")
    def _k_overlay_pack_ids_exist(self) -> "RuntimeConfigBundle":
        """(K) GovernanceOverlayRule pack_id_overrides must reference known policy packs."""
        known = set(self.governance.policy_packs)
        for overlay in self.governance.overlay_rules:
            for pack_id in overlay.pack_id_overrides:
                if pack_id and pack_id not in known:
                    raise ValueError(
                        f"[Validator K] Overlay '{overlay.overlay_id}' "
                        f"references unknown policy pack '{pack_id}'"
                    )
        return self
