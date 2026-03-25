# Python Code Skeleton - Runtime Config  
  
# ================================================================  
# PYTHON CODE SKELETON  
# RUNTIME CONFIG PYDANTIC MODELS  
# AGENTIC AI MDLC FRAMEWORK  
# ================================================================  
#  
# Suggested file layout:  
#  
# platform_core/  
#   runtime/  
#     config_models/  
#       __init__.py  
#       base.py  
#       enums.py  
#       fragments.py  
#       runtime_master.py  
#       tool_groups.py  
#       roles.py  
#       ui.py  
#       stages.py  
#       governance.py  
#       retries.py  
#       routes.py  
#       domain.py  
#       environment.py  
#       bundle.py  
#  
# ================================================================  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/base.py  
# ================================================================  
  
from __future__ import annotations  
  
from pydantic import BaseModel, ConfigDict  
  
  
class RuntimeConfigBase(BaseModel):  
    model_config = ConfigDict(  
        extra="forbid",  
        validate_assignment=True,  
        populate_by_name=True,  
        use_enum_values=True,  
    )  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/enums.py  
# ================================================================  
  
from __future__ import annotations  
  
from enum import Enum  
  
  
class AccessModeEnum(str, Enum):  
    READ_ONLY = "READ_ONLY"  
    BUILD_ONLY = "BUILD_ONLY"  
    REVIEW_REQUIRED = "REVIEW_REQUIRED"  
    FINALIZATION_GATED = "FINALIZATION_GATED"  
    MONITORING_OPERATIONAL = "MONITORING_OPERATIONAL"  
  
  
class UIModeEnum(str, Enum):  
    CHAT_ONLY = "chat_only"  
    WIZARD = "wizard"  
    MIXED = "mixed"  
    REVIEW_SHELL = "review_shell"  
    DASHBOARD = "dashboard"  
    FLOW_EXPLORER = "flow_explorer"  
    NONE = "none"  
  
  
class InteractionModeEnum(str, Enum):  
    READ = "read"  
    BUILD = "build"  
    REVIEW = "review"  
    APPROVE = "approve"  
    MONITOR = "monitor"  
    RECOVER = "recover"  
  
  
class TokenModeEnum(str, Enum):  
    MICRO_MODE = "micro_mode"  
    STANDARD_MODE = "standard_mode"  
    DEEP_REVIEW_MODE = "deep_review_mode"  
  
  
class RuntimeModeEnum(str, Enum):  
    STRICT = "strict"  
    PERMISSIVE = "permissive"  
  
  
class UnknownBehaviorEnum(str, Enum):  
    BLOCK = "block"  
    WARN = "warn"  
    ALLOW = "allow"  
  
  
class StaleStateBehaviorEnum(str, Enum):  
    RECOVER_ONLY = "recover_only"  
    BLOCK = "block"  
    WARN_ONLY = "warn_only"  
  
  
class ReviewMissingBehaviorEnum(str, Enum):  
    REVIEW_ONLY = "review_only"  
    BLOCK = "block"  
  
  
class EnvironmentNameEnum(str, Enum):  
    DEV = "dev"  
    UAT = "uat"  
    PROD = "prod"  
  
  
class StageClassEnum(str, Enum):  
    BOOTSTRAP = "bootstrap"  
    BUILD = "build"  
    REVIEW = "review"  
    FINALIZATION = "finalization"  
    MONITORING = "monitoring"  
    FAILURE = "failure"  
    RECOVERY = "recovery"  
    REPORTING = "reporting"  
    KNOWLEDGE = "knowledge"  
    RETRIEVAL = "retrieval"  
  
  
class DomainEnum(str, Enum):  
    GENERIC = "generic"  
    SCORECARD = "scorecard"  
    PD = "pd"  
    LGD = "lgd"  
    EAD = "ead"  
    SICR = "sicr"  
    ECL = "ecl"  
    STRESS = "stress"  
  
  
class ActorRoleEnum(str, Enum):  
    DEVELOPER = "developer"  
    VALIDATOR = "validator"  
    MONITORING = "monitoring"  
    GOVERNANCE = "governance"  
    APPROVER = "approver"  
    SYSTEM = "system"  
  
  
class RetryModeEnum(str, Enum):  
    SAFE = "safe"  
    LIMITED = "limited"  
    NONE = "none"  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/fragments.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import List  
  
from pydantic import Field, field_validator  
  
from .base import RuntimeConfigBase  
from .enums import (  
    InteractionModeEnum,  
    ReviewMissingBehaviorEnum,  
    StaleStateBehaviorEnum,  
    TokenModeEnum,  
    UIModeEnum,  
    UnknownBehaviorEnum,  
)  
  
  
class FileRefMap(RuntimeConfigBase):  
    tool_groups: str  
    role_capabilities: str  
    ui_modes: str  
    interaction_modes: str  
    token_modes: str  
    stage_registry: str  
    stage_tool_matrix: str  
    stage_preconditions: str  
    governance_overlays: str  
    retry_policies: str  
    failure_routes: str  
    workflow_routes: str  
  
  
class EnabledModules(RuntimeConfigBase):  
    stage_registry: bool = True  
    tool_groups: bool = True  
    role_capabilities: bool = True  
    ui_modes: bool = True  
    interaction_modes: bool = True  
    token_modes: bool = True  
    governance_overlays: bool = True  
    retry_policies: bool = True  
    failure_routes: bool = True  
    workflow_routes: bool = True  
  
  
class ResolverDefaults(RuntimeConfigBase):  
    unknown_stage_behavior: UnknownBehaviorEnum = UnknownBehaviorEnum.BLOCK  
    unknown_role_behavior: UnknownBehaviorEnum = UnknownBehaviorEnum.BLOCK  
    missing_tool_group_behavior: UnknownBehaviorEnum = UnknownBehaviorEnum.BLOCK  
    stale_state_behavior: StaleStateBehaviorEnum = StaleStateBehaviorEnum.RECOVER_ONLY  
    missing_review_behavior: ReviewMissingBehaviorEnum = ReviewMissingBehaviorEnum.REVIEW_ONLY  
    unresolved_breach_behavior: str = "block_downstream"  
    default_ui_mode: UIModeEnum = UIModeEnum.CHAT_ONLY  
    default_interaction_mode: InteractionModeEnum = InteractionModeEnum.READ  
    default_token_mode: TokenModeEnum = TokenModeEnum.MICRO_MODE  
  
  
class ToolListModel(RuntimeConfigBase):  
    tools: List[str] = Field(default_factory=list)  
  
    @field_validator("tools")  
    @classmethod  
    def validate_tools(cls, v: List[str]) -> List[str]:  
        cleaned = [x.strip() for x in v if isinstance(x, str) and x.strip()]  
        if len(cleaned) != len(v):  
            raise ValueError("Tool names must be non-empty strings.")  
        return cleaned  
  
  
class StageRouteMap(RuntimeConfigBase):  
    on_success: List[str] = Field(default_factory=list)  
    on_review_required: List[str] = Field(default_factory=list)  
    on_pass: List[str] = Field(default_factory=list)  
    on_fail: List[str] = Field(default_factory=list)  
    on_approved: List[str] = Field(default_factory=list)  
    on_rejected: List[str] = Field(default_factory=list)  
    on_auto_continue: List[str] = Field(default_factory=list)  
    on_remediation_required: List[str] = Field(default_factory=list)  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/runtime_master.py  
# ================================================================  
  
from __future__ import annotations  
  
from pydantic import field_validator  
  
from .base import RuntimeConfigBase  
from .enums import EnvironmentNameEnum, RuntimeModeEnum  
from .fragments import EnabledModules, FileRefMap, ResolverDefaults  
  
  
class RuntimeMasterSection(RuntimeConfigBase):  
    config_version: str  
    runtime_mode: RuntimeModeEnum = RuntimeModeEnum.STRICT  
    default_environment: EnvironmentNameEnum = EnvironmentNameEnum.PROD  
    enabled_modules: EnabledModules = EnabledModules()  
    file_refs: FileRefMap  
    resolver_defaults: ResolverDefaults = ResolverDefaults()  
  
    @field_validator("config_version")  
    @classmethod  
    def validate_config_version(cls, v: str) -> str:  
        if not v.strip():  
            raise ValueError("config_version cannot be empty.")  
        return v  
  
  
class RuntimeMasterConfig(RuntimeConfigBase):  
    runtime_master: RuntimeMasterSection  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/tool_groups.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Dict, List  
  
from pydantic import Field, field_validator  
  
from .base import RuntimeConfigBase  
  
  
class ToolGroupDefinition(RuntimeConfigBase):  
    name: str  
    tools: List[str] = Field(default_factory=list)  
  
    @field_validator("name")  
    @classmethod  
    def validate_name(cls, v: str) -> str:  
        if not v.strip():  
            raise ValueError("Tool group name cannot be empty.")  
        return v  
  
    @field_validator("tools")  
    @classmethod  
    def validate_tools(cls, v: List[str]) -> List[str]:  
        if not v:  
            raise ValueError("Tool group must contain at least one tool.")  
        cleaned = [x.strip() for x in v if x.strip()]  
        if len(cleaned) != len(v):  
            raise ValueError("Tool names must be non-empty.")  
        return cleaned  
  
  
class ToolGroupsConfig(RuntimeConfigBase):  
    tool_groups: Dict[str, ToolGroupDefinition]  
  
  
class VirtualToolGroupDefinition(RuntimeConfigBase):  
    includes: List[str] = Field(default_factory=list)  
  
    @field_validator("includes")  
    @classmethod  
    def validate_includes(cls, v: List[str]) -> List[str]:  
        if not v:  
            raise ValueError("Virtual tool group must contain at least one include.")  
        return [x.strip() for x in v if x.strip()]  
  
  
class VirtualToolGroupsConfig(RuntimeConfigBase):  
    virtual_tool_groups: Dict[str, VirtualToolGroupDefinition]  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/roles.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Dict, List  
  
from pydantic import Field, model_validator  
  
from .base import RuntimeConfigBase  
from .enums import ActorRoleEnum, TokenModeEnum, UIModeEnum, InteractionModeEnum  
  
  
class RoleCapabilityDefinition(RuntimeConfigBase):  
    can_build: bool = False  
    can_review: bool = False  
    can_approve: bool = False  
    can_finalize_validation_conclusion: bool = False  
    can_ingest_monitoring: bool = False  
    can_signoff: bool = False  
    can_promote_knowledge_beyond_project: bool = False  
    default_ui_mode: UIModeEnum  
    default_interaction_mode: InteractionModeEnum  
    default_token_mode: TokenModeEnum  
  
  
class RoleCapabilitiesConfig(RuntimeConfigBase):  
    role_capabilities: Dict[ActorRoleEnum, RoleCapabilityDefinition]  
  
    @model_validator(mode="after")  
    def validate_role_logic(self):  
        for role, cfg in self.role_capabilities.items():  
            if cfg.can_signoff and not cfg.can_approve:  
                raise ValueError(f"{role}: can_signoff requires can_approve.")  
            if role == ActorRoleEnum.SYSTEM:  
                if cfg.can_approve or cfg.can_signoff or cfg.can_finalize_validation_conclusion:  
                    raise ValueError(  
                        "system role cannot approve, sign off, or finalize validation conclusions."  
                    )  
        return self  
  
  
class RoleOverlaySection(RuntimeConfigBase):  
    role_name: ActorRoleEnum  
    force_block_tools: List[str] = Field(default_factory=list)  
    force_allow_tools: List[str] = Field(default_factory=list)  
    ui_mode_overrides: Dict[str, UIModeEnum] = Field(default_factory=dict)  
    token_mode_overrides: Dict[str, TokenModeEnum] = Field(default_factory=dict)  
  
    @model_validator(mode="after")  
    def validate_overlap(self):  
        overlap = set(self.force_block_tools) & set(self.force_allow_tools)  
        if overlap:  
            raise ValueError(f"Tools cannot be both blocked and allowed: {sorted(overlap)}")  
        return self  
  
  
class RoleOverlayConfig(RuntimeConfigBase):  
    role_overlay: RoleOverlaySection  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/ui.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Dict  
  
from pydantic import Field, model_validator  
  
from .base import RuntimeConfigBase  
from .enums import InteractionModeEnum, TokenModeEnum, UIModeEnum  
  
  
class UIModeDefinition(RuntimeConfigBase):  
    description: str  
    supports_review_actions: bool = False  
    supports_dashboard: bool = False  
    supports_flow_explorer: bool = False  
  
  
class UIModesConfig(RuntimeConfigBase):  
    ui_modes: Dict[UIModeEnum, UIModeDefinition]  
  
  
class InteractionModeDefinition(RuntimeConfigBase):  
    description: str  
    allows_mutation: bool = False  
  
  
class InteractionModesConfig(RuntimeConfigBase):  
    interaction_modes: Dict[InteractionModeEnum, InteractionModeDefinition]  
  
  
class TokenModeDefinition(RuntimeConfigBase):  
    description: str  
    retrieval_top_k: int = Field(ge=1)  
    max_context_tokens: int = Field(ge=100)  
    include_detailed_evidence: bool = False  
    prefer_summaries_only: bool = False  
  
  
class TokenModesConfig(RuntimeConfigBase):  
    token_modes: Dict[TokenModeEnum, TokenModeDefinition]  
  
    @model_validator(mode="after")  
    def validate_token_mode_ordering(self):  
        tm = self.token_modes  
        if (  
            TokenModeEnum.MICRO_MODE in tm  
            and TokenModeEnum.STANDARD_MODE in tm  
            and tm[TokenModeEnum.STANDARD_MODE].max_context_tokens < tm[TokenModeEnum.MICRO_MODE].max_context_tokens  
        ):  
            raise ValueError("standard_mode.max_context_tokens must be >= micro_mode.")  
        if (  
            TokenModeEnum.STANDARD_MODE in tm  
            and TokenModeEnum.DEEP_REVIEW_MODE in tm  
            and tm[TokenModeEnum.DEEP_REVIEW_MODE].max_context_tokens < tm[TokenModeEnum.STANDARD_MODE].max_context_tokens  
        ):  
            raise ValueError("deep_review_mode.max_context_tokens must be >= standard_mode.")  
        return self  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/stages.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Dict, List  
  
from pydantic import Field, model_validator, field_validator  
  
from .base import RuntimeConfigBase  
from .enums import (  
    AccessModeEnum,  
    DomainEnum,  
    InteractionModeEnum,  
    StageClassEnum,  
    TokenModeEnum,  
    UIModeEnum,  
)  
  
  
class StageDefinition(RuntimeConfigBase):  
    stage_class: StageClassEnum  
    stage_sequence_no: int = Field(ge=1)  
    domain_scope: List[DomainEnum] = Field(default_factory=list)  
    access_mode: AccessModeEnum  
    default_ui_mode: UIModeEnum  
    default_interaction_mode: InteractionModeEnum  
    default_token_mode: TokenModeEnum  
  
    @field_validator("domain_scope")  
    @classmethod  
    def validate_domain_scope(cls, v: List[DomainEnum]) -> List[DomainEnum]:  
        if not v:  
            raise ValueError("domain_scope cannot be empty.")  
        return v  
  
  
class StageRegistryConfig(RuntimeConfigBase):  
    stage_registry: Dict[str, StageDefinition]  
  
    @model_validator(mode="after")  
    def validate_unique_sequence_numbers(self):  
        seqs = [x.stage_sequence_no for x in self.stage_registry.values()]  
        if len(seqs) != len(set(seqs)):  
            raise ValueError("stage_sequence_no values must be unique.")  
        return self  
  
  
class StageToolMatrixEntry(RuntimeConfigBase):  
    allowed_tool_groups: List[str] = Field(default_factory=list)  
    blocked_tool_groups: List[str] = Field(default_factory=list)  
    explicit_allow: List[str] = Field(default_factory=list)  
    explicit_block: List[str] = Field(default_factory=list)  
  
    @model_validator(mode="after")  
    def validate_explicit_overlap(self):  
        overlap = set(self.explicit_allow) & set(self.explicit_block)  
        if overlap:  
            raise ValueError(f"Same tools cannot appear in explicit_allow and explicit_block: {sorted(overlap)}")  
        return self  
  
  
class StageToolMatrixConfig(RuntimeConfigBase):  
    stage_tool_matrix: Dict[str, StageToolMatrixEntry]  
  
  
class StagePreconditionEntry(RuntimeConfigBase):  
    required_ids: List[str] = Field(default_factory=list)  
    required_refs: List[str] = Field(default_factory=list)  
    required_flags: List[str] = Field(default_factory=list)  
    required_prior_stages: List[str] = Field(default_factory=list)  
    requires_active_review: bool = False  
  
  
class StagePreconditionsConfig(RuntimeConfigBase):  
    stage_preconditions: Dict[str, StagePreconditionEntry]  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/governance.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Dict, List, Optional  
  
from pydantic import Field, model_validator  
  
from .base import RuntimeConfigBase  
from .enums import AccessModeEnum, ActorRoleEnum  
  
  
class DefaultGovernanceRules(RuntimeConfigBase):  
    review_required: bool = False  
    approval_required: bool = False  
    audit_required: bool = False  
    auto_continue_allowed: bool = True  
  
    @model_validator(mode="after")  
    def validate_logic(self):  
        if self.approval_required and self.auto_continue_allowed:  
            raise ValueError("approval_required and auto_continue_allowed cannot both be true.")  
        return self  
  
  
class StageGovernanceRule(RuntimeConfigBase):  
    review_required: bool = False  
    approval_required: bool = False  
    audit_required: bool = False  
    auto_continue_allowed: bool = True  
  
    @model_validator(mode="after")  
    def validate_logic(self):  
        if self.approval_required and self.auto_continue_allowed:  
            raise ValueError("approval_required and auto_continue_allowed cannot both be true.")  
        if self.review_required and self.auto_continue_allowed:  
            raise ValueError("review_required and auto_continue_allowed cannot both be true.")  
        return self  
  
  
class RoleGovernanceOverride(RuntimeConfigBase):  
    force_block_tools: List[str] = Field(default_factory=list)  
    allow_tools: List[str] = Field(default_factory=list)  
  
    @model_validator(mode="after")  
    def validate_overlap(self):  
        overlap = set(self.force_block_tools) & set(self.allow_tools)  
        if overlap:  
            raise ValueError(f"Same tool cannot be both blocked and allowed: {sorted(overlap)}")  
        return self  
  
  
class ConditionalWhenClause(RuntimeConfigBase):  
    stage_access_mode_in: List[AccessModeEnum] = Field(default_factory=list)  
    active_review_exists: Optional[bool] = None  
    approval_required: Optional[bool] = None  
    actor_not_in_approval_roles: Optional[bool] = None  
    unresolved_severe_breach: Optional[bool] = None  
  
  
class ConditionalThenClause(RuntimeConfigBase):  
    force_block_tools: List[str] = Field(default_factory=list)  
    force_allow_tools: List[str] = Field(default_factory=list)  
    force_block_tool_groups: List[str] = Field(default_factory=list)  
  
  
class ConditionalGovernanceRule(RuntimeConfigBase):  
    rule_id: str  
    when: ConditionalWhenClause  
    then: ConditionalThenClause  
  
  
class GovernanceOverlaysSection(RuntimeConfigBase):  
    default_rules: DefaultGovernanceRules  
    stage_rules: Dict[str, StageGovernanceRule] = Field(default_factory=dict)  
    role_overrides: Dict[ActorRoleEnum, RoleGovernanceOverride] = Field(default_factory=dict)  
    conditional_rules: List[ConditionalGovernanceRule] = Field(default_factory=list)  
  
  
class GovernanceOverlaysConfig(RuntimeConfigBase):  
    governance_overlays: GovernanceOverlaysSection  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/retries.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Dict, List  
  
from pydantic import Field  
  
from .base import RuntimeConfigBase  
from .enums import RetryModeEnum  
  
  
class RetryDefaults(RuntimeConfigBase):  
    safe_retry_backoff_seconds: List[int] = Field(default_factory=lambda: [1, 3, 5])  
    limited_retry_backoff_seconds: List[int] = Field(default_factory=lambda: [2, 5])  
    no_retry: List[int] = Field(default_factory=list)  
  
  
class ToolRetryRule(RuntimeConfigBase):  
    retry_mode: RetryModeEnum  
    requires_idempotency_check: bool = False  
  
  
class RetryPoliciesSection(RuntimeConfigBase):  
    defaults: RetryDefaults = RetryDefaults()  
    tool_rules: Dict[str, ToolRetryRule] = Field(default_factory=dict)  
  
  
class RetryPoliciesConfig(RuntimeConfigBase):  
    retry_policies: RetryPoliciesSection  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/routes.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Dict, Optional  
  
from pydantic import model_validator  
  
from .base import RuntimeConfigBase  
from .fragments import StageRouteMap  
  
  
class FailureRouteEntry(RuntimeConfigBase):  
    on_failure: Optional[str] = None  
    on_rejection: Optional[str] = None  
  
    @model_validator(mode="after")  
    def validate_has_route(self):  
        if not self.on_failure and not self.on_rejection:  
            raise ValueError("At least one of on_failure or on_rejection must be provided.")  
        return self  
  
  
class FailureRoutesConfig(RuntimeConfigBase):  
    failure_routes: Dict[str, FailureRouteEntry]  
  
  
class WorkflowRoutesConfig(RuntimeConfigBase):  
    workflow_routes: Dict[str, StageRouteMap]  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/domain.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Dict, List, Optional  
  
from pydantic import Field, model_validator  
  
from .base import RuntimeConfigBase  
from .enums import DomainEnum, InteractionModeEnum, TokenModeEnum, UIModeEnum  
  
  
class DomainStageUIOverride(RuntimeConfigBase):  
    ui_mode: Optional[UIModeEnum] = None  
    interaction_mode: Optional[InteractionModeEnum] = None  
    token_mode: Optional[TokenModeEnum] = None  
  
  
class DomainStageToolAdditions(RuntimeConfigBase):  
    explicit_allow: List[str] = Field(default_factory=list)  
    explicit_block: List[str] = Field(default_factory=list)  
  
    @model_validator(mode="after")  
    def validate_overlap(self):  
        overlap = set(self.explicit_allow) & set(self.explicit_block)  
        if overlap:  
            raise ValueError(f"Tools cannot be both explicitly allowed and blocked: {sorted(overlap)}")  
        return self  
  
  
class DomainOverlaySection(RuntimeConfigBase):  
    domain_name: DomainEnum  
    enabled_stages: List[str] = Field(default_factory=list)  
    disabled_stages: List[str] = Field(default_factory=list)  
    stage_tool_additions: Dict[str, DomainStageToolAdditions] = Field(default_factory=dict)  
    stage_ui_overrides: Dict[str, DomainStageUIOverride] = Field(default_factory=dict)  
  
    @model_validator(mode="after")  
    def validate_stage_overlap(self):  
        overlap = set(self.enabled_stages) & set(self.disabled_stages)  
        if overlap:  
            raise ValueError(f"Stages cannot be both enabled and disabled: {sorted(overlap)}")  
        return self  
  
  
class DomainOverlayConfig(RuntimeConfigBase):  
    domain_overlay: DomainOverlaySection  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/environment.py  
# ================================================================  
  
from __future__ import annotations  
  
from pydantic import Field  
  
from .base import RuntimeConfigBase  
from .enums import EnvironmentNameEnum  
  
  
class EnvironmentStrictness(RuntimeConfigBase):  
    enforce_stage_preconditions: bool = True  
    enforce_review_requirement: bool = True  
    enforce_audit_requirement: bool = True  
    enforce_role_approval_check: bool = True  
  
  
class EnvironmentRetries(RuntimeConfigBase):  
    max_safe_retries: int = Field(default=3, ge=0)  
    max_limited_retries: int = Field(default=1, ge=0)  
  
  
class EnvironmentBlockRules(RuntimeConfigBase):  
    block_unknown_tools: bool = True  
    block_unknown_stages: bool = True  
    block_unknown_roles: bool = True  
  
  
class EnvironmentUIDefaults(RuntimeConfigBase):  
    prefer_review_shell_for_governed_stages: bool = True  
  
  
class EnvironmentOverlaySection(RuntimeConfigBase):  
    environment_name: EnvironmentNameEnum  
    strictness: EnvironmentStrictness = EnvironmentStrictness()  
    retries: EnvironmentRetries = EnvironmentRetries()  
    block_rules: EnvironmentBlockRules = EnvironmentBlockRules()  
    ui_defaults: EnvironmentUIDefaults = EnvironmentUIDefaults()  
  
  
class EnvironmentOverlayConfig(RuntimeConfigBase):  
    environment_overlay: EnvironmentOverlaySection  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/bundle.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Optional, Set  
  
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
    runtime_master: RuntimeMasterConfig  
    tool_groups: ToolGroupsConfig  
    virtual_tool_groups: Optional[VirtualToolGroupsConfig] = None  
    role_capabilities: RoleCapabilitiesConfig  
    ui_modes: UIModesConfig  
    interaction_modes: InteractionModesConfig  
    token_modes: TokenModesConfig  
    stage_registry: StageRegistryConfig  
    stage_tool_matrix: StageToolMatrixConfig  
    stage_preconditions: StagePreconditionsConfig  
    governance_overlays: GovernanceOverlaysConfig  
    retry_policies: RetryPoliciesConfig  
    failure_routes: FailureRoutesConfig  
    workflow_routes: WorkflowRoutesConfig  
    domain_overlay: Optional[DomainOverlayConfig] = None  
    role_overlay: Optional[RoleOverlayConfig] = None  
    environment_overlay: Optional[EnvironmentOverlayConfig] = None  
  
    @model_validator(mode="after")  
    def validate_cross_file_consistency(self):  
        stage_names: Set[str] = set(self.stage_registry.stage_registry.keys())  
  
        # A. stage references  
        for stage_name in self.stage_tool_matrix.stage_tool_matrix:  
            if stage_name not in stage_names:  
                raise ValueError(f"Stage tool matrix references unknown stage: {stage_name}")  
  
        for stage_name in self.stage_preconditions.stage_preconditions:  
            if stage_name not in stage_names:  
                raise ValueError(f"Stage preconditions reference unknown stage: {stage_name}")  
  
        for stage_name in self.workflow_routes.workflow_routes:  
            if stage_name not in stage_names:  
                raise ValueError(f"Workflow routes reference unknown stage: {stage_name}")  
  
        for stage_name in self.failure_routes.failure_routes:  
            if stage_name not in stage_names:  
                raise ValueError(f"Failure routes reference unknown stage: {stage_name}")  
  
        # B. workflow route targets  
        for stage_name, route_map in self.workflow_routes.workflow_routes.items():  
            for route_list in [  
                route_map.on_success,  
                route_map.on_review_required,  
                route_map.on_pass,  
                route_map.on_fail,  
                route_map.on_approved,  
                route_map.on_rejected,  
                route_map.on_auto_continue,  
                route_map.on_remediation_required,  
            ]:  
                for target in route_list:  
                    if target not in stage_names:  
                        raise ValueError(  
                            f"Workflow route target does not exist: {target} (from {stage_name})"  
                        )  
  
        # C. failure route targets  
        for stage_name, failure_entry in self.failure_routes.failure_routes.items():  
            for target in [failure_entry.on_failure, failure_entry.on_rejection]:  
                if target and target not in stage_names:  
                    raise ValueError(  
                        f"Failure route target does not exist: {target} (from {stage_name})"  
                    )  
  
        # D. UI / interaction / token mode references from stage registry  
        ui_mode_names = set(self.ui_modes.ui_modes.keys())  
        interaction_mode_names = set(self.interaction_modes.interaction_modes.keys())  
        token_mode_names = set(self.token_modes.token_modes.keys())  
  
        for stage_name, stage_cfg in self.stage_registry.stage_registry.items():  
            if stage_cfg.default_ui_mode not in ui_mode_names:  
                raise ValueError(f"{stage_name}: unknown UI mode {stage_cfg.default_ui_mode}")  
            if stage_cfg.default_interaction_mode not in interaction_mode_names:  
                raise ValueError(  
                    f"{stage_name}: unknown interaction mode {stage_cfg.default_interaction_mode}"  
                )  
            if stage_cfg.default_token_mode not in token_mode_names:  
                raise ValueError(f"{stage_name}: unknown token mode {stage_cfg.default_token_mode}")  
  
        # E. requires_active_review should align with stage access mode  
        for stage_name, precfg in self.stage_preconditions.stage_preconditions.items():  
            if precfg.requires_active_review:  
                access_mode = self.stage_registry.stage_registry[stage_name].access_mode  
                if access_mode not in {"REVIEW_REQUIRED", "FINALIZATION_GATED"}:  
                    raise ValueError(  
                        f"{stage_name}: requires_active_review=true but access_mode={access_mode}"  
                    )  
  
        # F. governance rule sanity  
        for stage_name, gov in self.governance_overlays.governance_overlays.stage_rules.items():  
            if stage_name not in stage_names:  
                raise ValueError(f"Governance overlay references unknown stage: {stage_name}")  
  
        return self  
  
  
# ================================================================  
# FILE: platform_core/runtime/config_models/__init__.py  
# ================================================================  
  
from .base import RuntimeConfigBase  
from .bundle import RuntimeConfigBundle  
from .domain import DomainOverlayConfig  
from .environment import EnvironmentOverlayConfig  
from .enums import (  
    AccessModeEnum,  
    ActorRoleEnum,  
    DomainEnum,  
    EnvironmentNameEnum,  
    InteractionModeEnum,  
    RetryModeEnum,  
    RuntimeModeEnum,  
    StageClassEnum,  
    TokenModeEnum,  
    UIModeEnum,  
)  
from .governance import GovernanceOverlaysConfig  
from .retries import RetryPoliciesConfig  
from .roles import RoleCapabilitiesConfig, RoleOverlayConfig  
from .routes import FailureRoutesConfig, WorkflowRoutesConfig  
from .runtime_master import RuntimeMasterConfig  
from .stages import StagePreconditionsConfig, StageRegistryConfig, StageToolMatrixConfig  
from .tool_groups import ToolGroupsConfig, VirtualToolGroupsConfig  
from .ui import InteractionModesConfig, TokenModesConfig, UIModesConfig  
  
__all__ = [  
    "RuntimeConfigBase",  
    "RuntimeConfigBundle",  
    "RuntimeMasterConfig",  
    "ToolGroupsConfig",  
    "VirtualToolGroupsConfig",  
    "RoleCapabilitiesConfig",  
    "RoleOverlayConfig",  
    "UIModesConfig",  
    "InteractionModesConfig",  
    "TokenModesConfig",  
    "StageRegistryConfig",  
    "StageToolMatrixConfig",  
    "StagePreconditionsConfig",  
    "GovernanceOverlaysConfig",  
    "RetryPoliciesConfig",  
    "FailureRoutesConfig",  
    "WorkflowRoutesConfig",  
    "DomainOverlayConfig",  
    "EnvironmentOverlayConfig",  
    "AccessModeEnum",  
    "ActorRoleEnum",  
    "DomainEnum",  
    "EnvironmentNameEnum",  
    "InteractionModeEnum",  
    "RetryModeEnum",  
    "RuntimeModeEnum",  
    "StageClassEnum",  
    "TokenModeEnum",  
    "UIModeEnum",  
]  
  
  
# ================================================================  
# OPTIONAL: FILE  
# platform_core/runtime/runtime_config_loader.py  
# ================================================================  
  
from __future__ import annotations  
  
from pathlib import Path  
from typing import Any, Dict, Optional  
  
import yaml  
  
from .config_models.bundle import RuntimeConfigBundle  
from .config_models.domain import DomainOverlayConfig  
from .config_models.environment import EnvironmentOverlayConfig  
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
  
  
class RuntimeConfigLoader:  
    def __init__(self, config_root: str | Path):  
        self.config_root = Path(config_root)  
  
    def _read_yaml(self, path: str | Path) -> Dict[str, Any]:  
        with Path(path).open("r", encoding="utf-8") as f:  
            return yaml.safe_load(f) or {}  
  
    def load_bundle(  
        self,  
        domain_overlay_path: Optional[str | Path] = None,  
        role_overlay_path: Optional[str | Path] = None,  
        environment_overlay_path: Optional[str | Path] = None,  
    ) -> RuntimeConfigBundle:  
        master_path = self.config_root / "runtime_master.yaml"  
        runtime_master = RuntimeMasterConfig.model_validate(self._read_yaml(master_path))  
        refs = runtime_master.runtime_master.file_refs  
  
        bundle = RuntimeConfigBundle(  
            runtime_master=runtime_master,  
            tool_groups=ToolGroupsConfig.model_validate(self._read_yaml(self.config_root / Path(refs.tool_groups).name)),  
            role_capabilities=RoleCapabilitiesConfig.model_validate(  
                self._read_yaml(self.config_root / Path(refs.role_capabilities).name)  
            ),  
            ui_modes=UIModesConfig.model_validate(self._read_yaml(self.config_root / Path(refs.ui_modes).name)),  
            interaction_modes=InteractionModesConfig.model_validate(  
                self._read_yaml(self.config_root / Path(refs.interaction_modes).name)  
            ),  
            token_modes=TokenModesConfig.model_validate(  
                self._read_yaml(self.config_root / Path(refs.token_modes).name)  
            ),  
            stage_registry=StageRegistryConfig.model_validate(  
                self._read_yaml(self.config_root / Path(refs.stage_registry).name)  
            ),  
            stage_tool_matrix=StageToolMatrixConfig.model_validate(  
                self._read_yaml(self.config_root / Path(refs.stage_tool_matrix).name)  
            ),  
            stage_preconditions=StagePreconditionsConfig.model_validate(  
                self._read_yaml(self.config_root / Path(refs.stage_preconditions).name)  
            ),  
            governance_overlays=GovernanceOverlaysConfig.model_validate(  
                self._read_yaml(self.config_root / Path(refs.governance_overlays).name)  
            ),  
            retry_policies=RetryPoliciesConfig.model_validate(  
                self._read_yaml(self.config_root / Path(refs.retry_policies).name)  
            ),  
            failure_routes=FailureRoutesConfig.model_validate(  
                self._read_yaml(self.config_root / Path(refs.failure_routes).name)  
            ),  
            workflow_routes=WorkflowRoutesConfig.model_validate(  
                self._read_yaml(self.config_root / Path(refs.workflow_routes).name)  
            ),  
            virtual_tool_groups=None,  
            domain_overlay=DomainOverlayConfig.model_validate(self._read_yaml(domain_overlay_path))  
            if domain_overlay_path  
            else None,  
            role_overlay=RoleOverlayConfig.model_validate(self._read_yaml(role_overlay_path))  
            if role_overlay_path  
            else None,  
            environment_overlay=EnvironmentOverlayConfig.model_validate(self._read_yaml(environment_overlay_path))  
            if environment_overlay_path  
            else None,  
        )  
        return bundle  
  
  
# ================================================================  
# OPTIONAL: FILE  
# platform_core/runtime/stage_config_resolver.py  
# ================================================================  
  
from __future__ import annotations  
  
from copy import deepcopy  
from typing import Any, Dict  
  
from .config_models.bundle import RuntimeConfigBundle  
  
  
class StageConfigResolver:  
    def __init__(self, bundle: RuntimeConfigBundle):  
        self.bundle = bundle  
  
    def resolve_stage_config(self, stage_name: str) -> Dict[str, Any]:  
        base = deepcopy(self.bundle.stage_registry.stage_registry[stage_name].model_dump())  
  
        # attach stage tool matrix if exists  
        if stage_name in self.bundle.stage_tool_matrix.stage_tool_matrix:  
            base["tool_matrix"] = self.bundle.stage_tool_matrix.stage_tool_matrix[stage_name].model_dump()  
  
        # attach preconditions if exists  
        if stage_name in self.bundle.stage_preconditions.stage_preconditions:  
            base["preconditions"] = self.bundle.stage_preconditions.stage_preconditions[stage_name].model_dump()  
  
        # attach governance if exists  
        gov = self.bundle.governance_overlays.governance_overlays  
        if stage_name in gov.stage_rules:  
            base["governance"] = gov.stage_rules[stage_name].model_dump()  
        else:  
            base["governance"] = gov.default_rules.model_dump()  
  
        # domain overlay  
        if self.bundle.domain_overlay:  
            domain_overlay = self.bundle.domain_overlay.domain_overlay  
            if stage_name in domain_overlay.stage_ui_overrides:  
                base["domain_ui_override"] = domain_overlay.stage_ui_overrides[stage_name].model_dump()  
            if stage_name in domain_overlay.stage_tool_additions:  
                base["domain_tool_additions"] = domain_overlay.stage_tool_additions[stage_name].model_dump()  
  
        return base  
