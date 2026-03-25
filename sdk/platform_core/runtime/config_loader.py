"""RuntimeConfigLoader and StageConfigResolver.

RuntimeConfigLoader loads all YAML config files in the correct order, validates
each via the corresponding Pydantic model, merges domain/role/environment overlays,
and returns a fully validated RuntimeConfigBundle.

StageConfigResolver resolves the effective configuration for a given
stage/role/domain combination from the loaded bundle.

Usage:
    loader = RuntimeConfigLoader(base_path="configs/runtime")
    bundle = loader.load()
    resolver = StageConfigResolver(bundle)
    effective = resolver.resolve(stage_name="model_fitting", role="developer", domain="scorecard")
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import ValidationError

from .config_models.bundle import RuntimeConfigBundle
from .config_models.domain import DomainOverlayConfig
from .config_models.environment import EnvironmentOverlayConfig
from .config_models.enums import EnvironmentNameEnum
from .config_models.governance import GovernanceOverlaysConfig
from .config_models.retries import RetryPoliciesConfig
from .config_models.roles import RoleCapabilitiesConfig, RoleOverlayConfig
from .config_models.routes import FailureRoutesConfig, WorkflowRoutesConfig
from .config_models.runtime_master import RuntimeMasterConfig
from .config_models.stages import (
    StagePreconditionsConfig,
    StageRegistryConfig,
    StageToolMatrixConfig,
)
from .config_models.tool_groups import ToolGroupsConfig, VirtualToolGroupsConfig
from .config_models.ui import InteractionModesConfig, TokenModesConfig, UIModesConfig

logger = logging.getLogger(__name__)


class ConfigLoadError(Exception):
    """Raised when a config file cannot be loaded or fails validation."""


def _load_yaml(path: Path) -> Dict[str, Any]:
    """Load a YAML file and return its parsed content.

    Args:
        path: Path to the YAML file.

    Returns:
        Parsed YAML content as a dict.

    Raises:
        ConfigLoadError: If the file does not exist or cannot be parsed.
    """
    if not path.exists():
        raise ConfigLoadError(f"Config file not found: {path}")
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        if data is None:
            return {}
        return data
    except yaml.YAMLError as exc:
        raise ConfigLoadError(f"YAML parse error in {path}: {exc}") from exc


def _validate_model(model_class: Any, data: Dict[str, Any], file_path: Path) -> Any:
    """Validate a dict against a Pydantic model.

    Args:
        model_class: The Pydantic model class.
        data: The raw data dict.
        file_path: Used in error messages.

    Returns:
        Validated Pydantic model instance.

    Raises:
        ConfigLoadError: If validation fails.
    """
    try:
        return model_class.model_validate(data)
    except ValidationError as exc:
        raise ConfigLoadError(
            f"Validation error in {file_path}:\n{exc}"
        ) from exc


class RuntimeConfigLoader:
    """Loads all runtime YAML configs and returns a validated RuntimeConfigBundle.

    Load order:
        1. runtime_master.yaml
        2. tool_groups.yaml
        3. role_capabilities.yaml
        4. ui_modes.yaml, interaction_modes.yaml, token_modes.yaml
        5. stage_registry.yaml, stage_tool_matrix.yaml, stage_preconditions.yaml
        6. governance_overlays.yaml, retry_policies.yaml
        7. failure_routes.yaml, workflow_routes.yaml
        8. domain_overlays/<domain>.yaml (all available)
        9. role_overlays/<role>.yaml (all available)
        10. environment_overlays/<env>.yaml (matching current environment)

    Args:
        base_path: Root directory of the configs/runtime/ tree.
        environment: Override the environment from runtime_master.yaml.
    """

    def __init__(self, base_path: str = "configs/runtime", environment: Optional[str] = None) -> None:
        self._base = Path(base_path)
        self._environment_override = environment
        logger.info("RuntimeConfigLoader initialized", extra={"base_path": str(self._base)})

    def _path(self, relative: str) -> Path:
        return self._base / relative

    def load(self) -> RuntimeConfigBundle:
        """Load, validate, and merge all runtime configs.

        Returns:
            Fully validated RuntimeConfigBundle.

        Raises:
            ConfigLoadError: If any file fails to load or validate.
        """
        logger.info("Loading runtime config bundle", extra={"base_path": str(self._base)})

        # 1. Runtime master
        runtime_master_data = _load_yaml(self._path("runtime_master.yaml"))
        runtime_master: RuntimeMasterConfig = _validate_model(
            RuntimeMasterConfig, runtime_master_data, self._path("runtime_master.yaml")
        )
        logger.debug("Loaded runtime_master.yaml")

        # 2. Tool groups
        tool_groups_data = _load_yaml(self._path("tool_groups.yaml"))
        tool_groups: ToolGroupsConfig = _validate_model(
            ToolGroupsConfig, {"groups": tool_groups_data.get("groups", {})},
            self._path("tool_groups.yaml")
        )
        virtual_tool_groups: Optional[VirtualToolGroupsConfig] = None
        if "virtual_groups" in tool_groups_data:
            virtual_tool_groups = _validate_model(
                VirtualToolGroupsConfig,
                {"virtual_groups": tool_groups_data["virtual_groups"]},
                self._path("tool_groups.yaml")
            )
        logger.debug("Loaded tool_groups.yaml")

        # 3. Role capabilities
        role_caps_data = _load_yaml(self._path("role_capabilities.yaml"))
        role_capabilities: RoleCapabilitiesConfig = _validate_model(
            RoleCapabilitiesConfig, role_caps_data, self._path("role_capabilities.yaml")
        )
        logger.debug("Loaded role_capabilities.yaml")

        # 4. UI/interaction/token modes
        ui_modes: UIModesConfig = _validate_model(
            UIModesConfig, _load_yaml(self._path("ui_modes.yaml")), self._path("ui_modes.yaml")
        )
        interaction_modes: InteractionModesConfig = _validate_model(
            InteractionModesConfig,
            _load_yaml(self._path("interaction_modes.yaml")),
            self._path("interaction_modes.yaml")
        )
        token_modes: TokenModesConfig = _validate_model(
            TokenModesConfig,
            _load_yaml(self._path("token_modes.yaml")),
            self._path("token_modes.yaml")
        )
        logger.debug("Loaded ui/interaction/token modes")

        # 5. Stage registry, tool matrix, preconditions
        stage_registry: StageRegistryConfig = _validate_model(
            StageRegistryConfig,
            _load_yaml(self._path("stage_registry.yaml")),
            self._path("stage_registry.yaml")
        )
        stage_tool_matrix: StageToolMatrixConfig = _validate_model(
            StageToolMatrixConfig,
            {"matrix": _load_yaml(self._path("stage_tool_matrix.yaml")).get("matrix", {})},
            self._path("stage_tool_matrix.yaml")
        )
        stage_preconditions: Optional[StagePreconditionsConfig] = None
        precond_path = self._path("stage_preconditions.yaml")
        if precond_path.exists():
            stage_preconditions = _validate_model(
                StagePreconditionsConfig,
                _load_yaml(precond_path),
                precond_path
            )
        logger.debug("Loaded stage registry and tool matrix")

        # 6. Governance and retry
        governance_overlays: GovernanceOverlaysConfig = _validate_model(
            GovernanceOverlaysConfig,
            _load_yaml(self._path("governance_overlays.yaml")),
            self._path("governance_overlays.yaml")
        )
        retry_policies: RetryPoliciesConfig = _validate_model(
            RetryPoliciesConfig,
            _load_yaml(self._path("retry_policies.yaml")),
            self._path("retry_policies.yaml")
        )
        logger.debug("Loaded governance and retry policies")

        # 7. Routes
        failure_routes: Optional[FailureRoutesConfig] = None
        fail_path = self._path("failure_routes.yaml")
        if fail_path.exists():
            raw = _load_yaml(fail_path)
            # Routes are stored as lists under stage names
            routes_data = {"routes": {k: v for k, v in raw.get("routes", {}).items()}}
            failure_routes = _validate_model(FailureRoutesConfig, routes_data, fail_path)

        workflow_routes: WorkflowRoutesConfig = _validate_model(
            WorkflowRoutesConfig,
            _load_yaml(self._path("workflow_routes.yaml")),
            self._path("workflow_routes.yaml")
        )
        logger.debug("Loaded routes")

        # 8. Domain overlays (config-format only; domain pack YAMLs without an
        #    "overlay:" wrapper are domain pack manifests and are skipped here).
        domain_overlays: Dict[str, DomainOverlayConfig] = {}
        domain_dir = self._path("domain_overlays")
        if domain_dir.exists():
            for yaml_file in domain_dir.glob("*.yaml"):
                raw = _load_yaml(yaml_file)
                if "overlay" not in raw:
                    logger.debug(
                        "Skipping domain pack manifest (no 'overlay' key): %s", yaml_file.name
                    )
                    continue
                domain_name = yaml_file.stem
                overlay = _validate_model(
                    DomainOverlayConfig, raw, yaml_file
                )
                domain_overlays[domain_name] = overlay
                logger.debug("Loaded domain overlay: %s", domain_name)

        # 9. Role overlays
        role_overlays: Dict[str, RoleOverlayConfig] = {}
        role_dir = self._path("role_overlays")
        if role_dir.exists():
            for yaml_file in role_dir.glob("*.yaml"):
                role_name = yaml_file.stem
                overlay = _validate_model(
                    RoleOverlayConfig, _load_yaml(yaml_file), yaml_file
                )
                role_overlays[role_name] = overlay
                logger.debug("Loaded role overlay: %s", role_name)

        # 10. Environment overlay
        env_name = self._environment_override or runtime_master.runtime.environment
        environment_overlay: Optional[EnvironmentOverlayConfig] = None
        env_path = self._path(f"environment_overlays/{env_name}.yaml")
        if env_path.exists():
            environment_overlay = _validate_model(
                EnvironmentOverlayConfig, _load_yaml(env_path), env_path
            )
            logger.debug("Loaded environment overlay: %s", env_name)

        # Assemble and cross-validate bundle
        bundle = RuntimeConfigBundle(
            runtime_master=runtime_master,
            tool_groups=tool_groups,
            virtual_tool_groups=virtual_tool_groups,
            role_capabilities=role_capabilities,
            ui_modes=ui_modes,
            interaction_modes=interaction_modes,
            token_modes=token_modes,
            stage_registry=stage_registry,
            stage_tool_matrix=stage_tool_matrix,
            stage_preconditions=stage_preconditions,
            governance_overlays=governance_overlays,
            retry_policies=retry_policies,
            failure_routes=failure_routes,
            workflow_routes=workflow_routes,
            domain_overlays=domain_overlays,
            role_overlays=role_overlays,
            environment_overlay=environment_overlay,
        )
        logger.info(
            "Runtime config bundle loaded successfully",
            extra={
                "stages": len(bundle.stage_registry.stages),
                "tool_groups": len(bundle.tool_groups.groups),
                "roles": len(bundle.role_capabilities.roles),
                "domain_overlays": len(bundle.domain_overlays),
                "environment": env_name,
            }
        )
        return bundle


class EffectiveStageConfig:
    """Resolved effective configuration for a specific stage/role/domain combination.

    Attributes:
        stage_name: The resolved stage name.
        role: The actor role.
        domain: The domain (if any).
        access_mode: Effective access mode.
        requires_review: Whether review is required.
        requires_approval: Whether approval is required.
        requires_audit: Whether audit is required.
        auto_continue_allowed: Whether auto-continue is permitted.
        allowed_tools: Final allowed tool list (intersection of stage + role + domain).
        blocked_tools: Final blocked tool list.
        ui_mode: Recommended UI mode.
        interaction_mode: Recommended interaction mode.
        token_mode: Recommended token mode.
        skill_hints: Resolved skill hints.
        governance_constraints: Active governance constraints.
        retry_policy: Effective retry policy for this context.
    """

    def __init__(
        self,
        stage_name: str,
        role: str,
        domain: Optional[str],
        access_mode: str,
        requires_review: bool,
        requires_approval: bool,
        requires_audit: bool,
        auto_continue_allowed: bool,
        allowed_tools: list,
        blocked_tools: list,
        ui_mode: str,
        interaction_mode: str,
        token_mode: str,
        skill_hints: list,
        governance_constraints: dict,
        retry_policy: dict,
    ) -> None:
        self.stage_name = stage_name
        self.role = role
        self.domain = domain
        self.access_mode = access_mode
        self.requires_review = requires_review
        self.requires_approval = requires_approval
        self.requires_audit = requires_audit
        self.auto_continue_allowed = auto_continue_allowed
        self.allowed_tools = allowed_tools
        self.blocked_tools = blocked_tools
        self.ui_mode = ui_mode
        self.interaction_mode = interaction_mode
        self.token_mode = token_mode
        self.skill_hints = skill_hints
        self.governance_constraints = governance_constraints
        self.retry_policy = retry_policy


class StageConfigResolver:
    """Resolves the effective config for a given stage/role/domain combination.

    This is the per-request resolver that produces the effective runtime decision
    from the loaded RuntimeConfigBundle.

    Args:
        bundle: The loaded and validated RuntimeConfigBundle.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._bundle = bundle

    def resolve(
        self,
        stage_name: str,
        role: str,
        domain: Optional[str] = None,
    ) -> EffectiveStageConfig:
        """Resolve effective config for a stage/role/domain combination.

        Args:
            stage_name: The current stage name.
            role: The actor role name.
            domain: Optional domain name.

        Returns:
            EffectiveStageConfig with all resolved values.

        Raises:
            KeyError: If stage_name or role is not found in the registry.
        """
        stage = self._bundle.stage_registry.stages.get(stage_name)
        if stage is None:
            raise KeyError(f"Stage '{stage_name}' not found in stage registry")

        role_def = self._bundle.role_capabilities.roles.get(role)
        if role_def is None:
            raise KeyError(f"Role '{role}' not found in role capabilities")

        # Resolve tool matrix for this stage
        matrix_entry = self._bundle.stage_tool_matrix.matrix.get(stage_name)
        stage_allowed_groups: set = set(matrix_entry.allowed_groups) if matrix_entry else set()
        stage_blocked_groups: set = set(matrix_entry.blocked_groups) if matrix_entry else set()

        # Intersect with role allowed groups; subtract blocked
        role_allowed: set = set(role_def.allowed_tool_groups)
        role_blocked: set = set(role_def.blocked_tool_groups)
        effective_groups = (stage_allowed_groups & role_allowed) - role_blocked - stage_blocked_groups

        # Apply domain tool additions
        if domain and domain in self._bundle.domain_overlays:
            domain_overlay = self._bundle.domain_overlays[domain]
            tool_additions_map = domain_overlay.overlay.get_tool_additions_map() if hasattr(domain_overlay.overlay, "get_tool_additions_map") else {}
            if stage_name in tool_additions_map:
                ta = tool_additions_map[stage_name]
                effective_groups |= set(ta.add_tool_groups)
                effective_groups -= set(ta.remove_tool_groups)

        # Expand groups to tool names
        allowed_tools: list = []
        blocked_tools: list = []
        for group_name, group_def in self._bundle.tool_groups.groups.items():
            if group_name in effective_groups:
                allowed_tools.extend(group_def.tools)
            elif group_name in stage_blocked_groups or group_name in role_blocked:
                blocked_tools.extend(group_def.tools)

        # Resolve UI modes
        ui_mode = stage.default_access_mode  # fallback
        interaction_mode = "read_only"
        token_mode = "compact"

        # Apply domain UI override if present
        if domain and domain in self._bundle.domain_overlays:
            domain_overlay = self._bundle.domain_overlays[domain]
            ui_override_map = domain_overlay.overlay.get_ui_override_map()
            if stage_name in ui_override_map:
                override = ui_override_map[stage_name]
                if override.ui_mode:
                    ui_mode = override.ui_mode
                if override.interaction_mode:
                    interaction_mode = override.interaction_mode
                if override.token_mode:
                    token_mode = override.token_mode

        # Resolve governance constraints
        stage_rules_map = self._bundle.governance_overlays.get_stage_rules_map()
        gov_rule = stage_rules_map.get(stage_name)
        requires_review = gov_rule.requires_review if (gov_rule and gov_rule.requires_review is not None) else stage.requires_review
        requires_approval = gov_rule.requires_approval if (gov_rule and gov_rule.requires_approval is not None) else stage.requires_approval
        requires_audit = gov_rule.audit_required if (gov_rule and gov_rule.audit_required is not None) else stage.requires_audit
        auto_continue = gov_rule.auto_continue_allowed if (gov_rule and gov_rule.auto_continue_allowed is not None) else stage.auto_continue_allowed

        # Check conditional rules
        conditional_rules = self._bundle.governance_overlays.get_conditional_rules_for_stage(stage_name)

        governance_constraints: dict = {
            "requires_review": requires_review,
            "requires_approval": requires_approval,
            "requires_audit": requires_audit,
            "auto_continue_allowed": auto_continue,
            "conditional_rules_count": len(conditional_rules),
        }

        # Resolve retry policy
        retry_defaults = self._bundle.retry_policies.retry_policies.defaults
        retry_policy = {
            "retry_mode": retry_defaults.retry_mode,
            "max_retries": retry_defaults.max_retries,
        }

        # Skill hints: platform base + domain + stage
        skill_hints: list = list(stage.skill_stack_hints)
        if domain and domain in self._bundle.domain_overlays:
            domain_hints = self._bundle.domain_overlays[domain].overlay.skill_hints
            skill_hints = domain_hints + skill_hints

        return EffectiveStageConfig(
            stage_name=stage_name,
            role=role,
            domain=domain,
            access_mode=str(stage.default_access_mode),
            requires_review=requires_review,
            requires_approval=requires_approval,
            requires_audit=requires_audit,
            auto_continue_allowed=auto_continue,
            allowed_tools=sorted(set(allowed_tools)),
            blocked_tools=sorted(set(blocked_tools)),
            ui_mode=str(ui_mode),
            interaction_mode=interaction_mode,
            token_mode=token_mode,
            skill_hints=skill_hints,
            governance_constraints=governance_constraints,
            retry_policy=retry_policy,
        )
