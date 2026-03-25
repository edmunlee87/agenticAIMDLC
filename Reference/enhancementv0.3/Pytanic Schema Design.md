# Pytanic Schema Design  
  
====================================================================  
PYDANTIC SCHEMA DESIGN  
RUNTIME CONFIG PACK  
AGENTIC AI MDLC FRAMEWORK  
DIRECT PYTHON IMPLEMENTATION REFERENCE  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This document defines the Pydantic schema design for the runtime config  
pack used by:  
  
- ConfigService  
- RuntimeConfigLoader  
- StageConfigResolver  
- RoleConfigResolver  
- ToolGroupResolver  
- GovernanceRuleResolver  
- RetryPolicyResolver  
- RuntimeResolver  
- AllowlistResolver  
- UIModeResolver  
- InteractionModeResolver  
- TokenModeResolver  
  
This is the direct Python contract layer for the YAML / JSON runtime  
configuration pack.  
  
It covers:  
- enums  
- base config models  
- per-file schema models  
- validators  
- recommended defaults  
- cross-config validation rules  
- suggested file mapping  
  
====================================================================  
1. DESIGN PRINCIPLES  
====================================================================  
  
1. Strong typing  
--------------------------------------------------------------------  
Use enums and explicit field types wherever possible.  
  
2. Strict config validation  
--------------------------------------------------------------------  
Unknown fields should be forbidden in most runtime config models.  
  
3. Shallow nested models  
--------------------------------------------------------------------  
Do not create overly deep config models unless the structure truly  
requires it.  
  
4. Reusable fragments  
--------------------------------------------------------------------  
Common models such as route lists, tool lists, and policy flags should  
be reusable across config files.  
  
5. Cross-file validation  
--------------------------------------------------------------------  
Some checks can only happen after all config files are loaded together.  
Those should be handled by a RuntimeConfigBundle validator layer.  
  
====================================================================  
2. RECOMMENDED IMPORTS  
====================================================================  
  
Suggested imports:  
  
from __future__ import annotations  
  
from enum import Enum  
from typing import Any, Dict, List, Optional, Literal  
  
from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator  
  
====================================================================  
3. CORE BASE MODEL  
====================================================================  
  
--------------------------------------------------------------------  
3.1 RuntimeConfigBase  
--------------------------------------------------------------------  
  
Purpose:  
Root base class for all runtime config models.  
  
Suggested design:  
  
class RuntimeConfigBase(BaseModel):  
    model_config = ConfigDict(  
        extra="forbid",  
        validate_assignment=True,  
        populate_by_name=True,  
        use_enum_values=True  
    )  
  
Notes:  
- extra="forbid" is recommended for most runtime config files  
- use_enum_values=True makes YAML/JSON serialization cleaner  
  
====================================================================  
4. ENUM DEFINITIONS  
====================================================================  
  
--------------------------------------------------------------------  
4.1 AccessModeEnum  
--------------------------------------------------------------------  
  
class AccessModeEnum(str, Enum):  
    READ_ONLY = "READ_ONLY"  
    BUILD_ONLY = "BUILD_ONLY"  
    REVIEW_REQUIRED = "REVIEW_REQUIRED"  
    FINALIZATION_GATED = "FINALIZATION_GATED"  
    MONITORING_OPERATIONAL = "MONITORING_OPERATIONAL"  
  
--------------------------------------------------------------------  
4.2 UIModeEnum  
--------------------------------------------------------------------  
  
class UIModeEnum(str, Enum):  
    CHAT_ONLY = "chat_only"  
    WIZARD = "wizard"  
    MIXED = "mixed"  
    REVIEW_SHELL = "review_shell"  
    DASHBOARD = "dashboard"  
    FLOW_EXPLORER = "flow_explorer"  
    NONE = "none"  
  
--------------------------------------------------------------------  
4.3 InteractionModeEnum  
--------------------------------------------------------------------  
  
class InteractionModeEnum(str, Enum):  
    READ = "read"  
    BUILD = "build"  
    REVIEW = "review"  
    APPROVE = "approve"  
    MONITOR = "monitor"  
    RECOVER = "recover"  
  
--------------------------------------------------------------------  
4.4 TokenModeEnum  
--------------------------------------------------------------------  
  
class TokenModeEnum(str, Enum):  
    MICRO_MODE = "micro_mode"  
    STANDARD_MODE = "standard_mode"  
    DEEP_REVIEW_MODE = "deep_review_mode"  
  
--------------------------------------------------------------------  
4.5 RuntimeModeEnum  
--------------------------------------------------------------------  
  
class RuntimeModeEnum(str, Enum):  
    STRICT = "strict"  
    PERMISSIVE = "permissive"  
  
--------------------------------------------------------------------  
4.6 UnknownBehaviorEnum  
--------------------------------------------------------------------  
  
class UnknownBehaviorEnum(str, Enum):  
    BLOCK = "block"  
    WARN = "warn"  
    ALLOW = "allow"  
  
--------------------------------------------------------------------  
4.7 StaleStateBehaviorEnum  
--------------------------------------------------------------------  
  
class StaleStateBehaviorEnum(str, Enum):  
    RECOVER_ONLY = "recover_only"  
    BLOCK = "block"  
    WARN_ONLY = "warn_only"  
  
--------------------------------------------------------------------  
4.8 ReviewMissingBehaviorEnum  
--------------------------------------------------------------------  
  
class ReviewMissingBehaviorEnum(str, Enum):  
    REVIEW_ONLY = "review_only"  
    BLOCK = "block"  
  
--------------------------------------------------------------------  
4.9 EnvironmentNameEnum  
--------------------------------------------------------------------  
  
class EnvironmentNameEnum(str, Enum):  
    DEV = "dev"  
    UAT = "uat"  
    PROD = "prod"  
  
--------------------------------------------------------------------  
4.10 StageClassEnum  
--------------------------------------------------------------------  
  
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
  
--------------------------------------------------------------------  
4.11 DomainEnum  
--------------------------------------------------------------------  
  
class DomainEnum(str, Enum):  
    GENERIC = "generic"  
    SCORECARD = "scorecard"  
    PD = "pd"  
    LGD = "lgd"  
    EAD = "ead"  
    SICR = "sicr"  
    ECL = "ecl"  
    STRESS = "stress"  
  
--------------------------------------------------------------------  
4.12 ActorRoleEnum  
--------------------------------------------------------------------  
  
class ActorRoleEnum(str, Enum):  
    DEVELOPER = "developer"  
    VALIDATOR = "validator"  
    MONITORING = "monitoring"  
    GOVERNANCE = "governance"  
    APPROVER = "approver"  
    SYSTEM = "system"  
  
--------------------------------------------------------------------  
4.13 RetryModeEnum  
--------------------------------------------------------------------  
  
class RetryModeEnum(str, Enum):  
    SAFE = "safe"  
    LIMITED = "limited"  
    NONE = "none"  
  
====================================================================  
5. SHARED FRAGMENT MODELS  
====================================================================  
  
--------------------------------------------------------------------  
5.1 FileRefMap  
--------------------------------------------------------------------  
  
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
  
--------------------------------------------------------------------  
5.2 EnabledModules  
--------------------------------------------------------------------  
  
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
  
--------------------------------------------------------------------  
5.3 ResolverDefaults  
--------------------------------------------------------------------  
  
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
  
--------------------------------------------------------------------  
5.4 StringListRule  
--------------------------------------------------------------------  
  
class StringListRule(RuntimeConfigBase):  
    values: List[str] = Field(default_factory=list)  
  
--------------------------------------------------------------------  
5.5 RouteList  
--------------------------------------------------------------------  
  
class RouteList(RuntimeConfigBase):  
    routes: List[str] = Field(default_factory=list)  
  
--------------------------------------------------------------------  
5.6 ToolListModel  
--------------------------------------------------------------------  
  
class ToolListModel(RuntimeConfigBase):  
    tools: List[str] = Field(default_factory=list)  
  
    @field_validator("tools")  
    @classmethod  
    def validate_non_empty_tool_names(cls, v: List[str]) -> List[str]:  
        cleaned = [x.strip() for x in v if x and x.strip()]  
        if len(cleaned) != len(v):  
            raise ValueError("Tool names must be non-empty strings.")  
        return cleaned  
  
--------------------------------------------------------------------  
5.7 StageRouteMap  
--------------------------------------------------------------------  
  
class StageRouteMap(RuntimeConfigBase):  
    on_success: List[str] = Field(default_factory=list)  
    on_review_required: List[str] = Field(default_factory=list)  
    on_pass: List[str] = Field(default_factory=list)  
    on_fail: List[str] = Field(default_factory=list)  
    on_approved: List[str] = Field(default_factory=list)  
    on_rejected: List[str] = Field(default_factory=list)  
    on_auto_continue: List[str] = Field(default_factory=list)  
    on_remediation_required: List[str] = Field(default_factory=list)  
  
====================================================================  
6. RUNTIME MASTER SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
6.1 RuntimeMasterConfig  
--------------------------------------------------------------------  
  
class RuntimeMasterSection(RuntimeConfigBase):  
    config_version: str  
    runtime_mode: RuntimeModeEnum = RuntimeModeEnum.STRICT  
    default_environment: EnvironmentNameEnum = EnvironmentNameEnum.PROD  
    enabled_modules: EnabledModules = Field(default_factory=EnabledModules)  
    file_refs: FileRefMap  
    resolver_defaults: ResolverDefaults = Field(default_factory=ResolverDefaults)  
  
class RuntimeMasterConfig(RuntimeConfigBase):  
    runtime_master: RuntimeMasterSection  
  
Validators:  
- config_version must be non-empty  
- file_refs paths must be non-empty strings  
  
Suggested validator:  
  
    @field_validator("config_version")  
    @classmethod  
    def validate_config_version(cls, v: str) -> str:  
        if not v.strip():  
            raise ValueError("config_version cannot be empty.")  
        return v  
  
====================================================================  
7. TOOL GROUP SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
7.1 ToolGroupDefinition  
--------------------------------------------------------------------  
  
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
        return [x.strip() for x in v]  
  
--------------------------------------------------------------------  
7.2 ToolGroupsConfig  
--------------------------------------------------------------------  
  
class ToolGroupsConfig(RuntimeConfigBase):  
    tool_groups: Dict[str, ToolGroupDefinition]  
  
Validator ideas:  
- key should be uppercase single group code or named alias  
- no duplicate tools inside same group  
  
--------------------------------------------------------------------  
7.3 VirtualToolGroupsConfig  
--------------------------------------------------------------------  
  
class VirtualToolGroupDefinition(RuntimeConfigBase):  
    includes: List[str] = Field(default_factory=list)  
  
class VirtualToolGroupsConfig(RuntimeConfigBase):  
    virtual_tool_groups: Dict[str, VirtualToolGroupDefinition]  
  
Validator ideas:  
- includes should refer to actual tool names or subgroup expansions  
- no empty includes list  
  
====================================================================  
8. ROLE CAPABILITY SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
8.1 RoleCapabilityDefinition  
--------------------------------------------------------------------  
  
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
  
--------------------------------------------------------------------  
8.2 RoleCapabilitiesConfig  
--------------------------------------------------------------------  
  
class RoleCapabilitiesConfig(RuntimeConfigBase):  
    role_capabilities: Dict[ActorRoleEnum, RoleCapabilityDefinition]  
  
Cross-field validator recommendation:  
- if can_signoff is true, can_approve should generally also be true  
- system should not have can_approve or can_signoff true  
  
Suggested validator:  
  
    @model_validator(mode="after")  
    def validate_role_logic(self):  
        for role, cfg in self.role_capabilities.items():  
            if cfg.can_signoff and not cfg.can_approve:  
                raise ValueError(f"{role}: can_signoff requires can_approve.")  
            if role == ActorRoleEnum.SYSTEM:  
                if cfg.can_approve or cfg.can_signoff or cfg.can_finalize_validation_conclusion:  
                    raise ValueError("system role cannot approve, sign off, or finalize validation conclusions.")  
        return self  
  
====================================================================  
9. UI / INTERACTION / TOKEN MODE SCHEMAS  
====================================================================  
  
--------------------------------------------------------------------  
9.1 UIModeDefinition  
--------------------------------------------------------------------  
  
class UIModeDefinition(RuntimeConfigBase):  
    description: str  
    supports_review_actions: bool = False  
    supports_dashboard: bool = False  
    supports_flow_explorer: bool = False  
  
class UIModesConfig(RuntimeConfigBase):  
    ui_modes: Dict[UIModeEnum, UIModeDefinition]  
  
--------------------------------------------------------------------  
9.2 InteractionModeDefinition  
--------------------------------------------------------------------  
  
class InteractionModeDefinition(RuntimeConfigBase):  
    description: str  
    allows_mutation: bool = False  
  
class InteractionModesConfig(RuntimeConfigBase):  
    interaction_modes: Dict[InteractionModeEnum, InteractionModeDefinition]  
  
--------------------------------------------------------------------  
9.3 TokenModeDefinition  
--------------------------------------------------------------------  
  
class TokenModeDefinition(RuntimeConfigBase):  
    description: str  
    retrieval_top_k: int = Field(ge=1)  
    max_context_tokens: int = Field(ge=100)  
    include_detailed_evidence: bool = False  
    prefer_summaries_only: bool = False  
  
class TokenModesConfig(RuntimeConfigBase):  
    token_modes: Dict[TokenModeEnum, TokenModeDefinition]  
  
Cross-field validator recommendation:  
- deep_review_mode should have higher max_context_tokens than standard  
- standard should be >= micro  
  
====================================================================  
10. STAGE REGISTRY SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
10.1 StageDefinition  
--------------------------------------------------------------------  
  
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
  
--------------------------------------------------------------------  
10.2 StageRegistryConfig  
--------------------------------------------------------------------  
  
class StageRegistryConfig(RuntimeConfigBase):  
    stage_registry: Dict[str, StageDefinition]  
  
Validator ideas:  
- stage names should be snake_case  
- stage_sequence_no should be unique  
- no empty registry  
  
Suggested model validator:  
- check unique sequence numbers  
  
====================================================================  
11. STAGE TOOL MATRIX SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
11.1 StageToolMatrixEntry  
--------------------------------------------------------------------  
  
class StageToolMatrixEntry(RuntimeConfigBase):  
    allowed_tool_groups: List[str] = Field(default_factory=list)  
    blocked_tool_groups: List[str] = Field(default_factory=list)  
    explicit_allow: List[str] = Field(default_factory=list)  
    explicit_block: List[str] = Field(default_factory=list)  
  
--------------------------------------------------------------------  
11.2 StageToolMatrixConfig  
--------------------------------------------------------------------  
  
class StageToolMatrixConfig(RuntimeConfigBase):  
    stage_tool_matrix: Dict[str, StageToolMatrixEntry]  
  
Validator ideas:  
- same tool should not appear in explicit_allow and explicit_block  
- allowed_tool_groups and blocked_tool_groups can overlap only if later logic explicitly resolves precedence, but better to block this at config time unless intentional  
  
Suggested validator:  
  
    @model_validator(mode="after")  
    def validate_stage_tool_matrix(self):  
        for stage, entry in self.stage_tool_matrix.items():  
            overlap = set(entry.explicit_allow) & set(entry.explicit_block)  
            if overlap:  
                raise ValueError(f"{stage}: same tools cannot appear in explicit_allow and explicit_block: {sorted(overlap)}")  
        return self  
  
====================================================================  
12. STAGE PRECONDITION SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
12.1 StagePreconditionEntry  
--------------------------------------------------------------------  
  
class StagePreconditionEntry(RuntimeConfigBase):  
    required_ids: List[str] = Field(default_factory=list)  
    required_refs: List[str] = Field(default_factory=list)  
    required_flags: List[str] = Field(default_factory=list)  
    required_prior_stages: List[str] = Field(default_factory=list)  
    requires_active_review: bool = False  
  
--------------------------------------------------------------------  
12.2 StagePreconditionsConfig  
--------------------------------------------------------------------  
  
class StagePreconditionsConfig(RuntimeConfigBase):  
    stage_preconditions: Dict[str, StagePreconditionEntry]  
  
Validator ideas:  
- if requires_active_review true, access mode for that stage should generally be REVIEW_REQUIRED or FINALIZATION_GATED; this is cross-file validation and belongs in bundle validator  
  
====================================================================  
13. GOVERNANCE OVERLAY SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
13.1 DefaultGovernanceRules  
--------------------------------------------------------------------  
  
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
  
--------------------------------------------------------------------  
13.2 StageGovernanceRule  
--------------------------------------------------------------------  
  
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
  
--------------------------------------------------------------------  
13.3 RoleGovernanceOverride  
--------------------------------------------------------------------  
  
class RoleGovernanceOverride(RuntimeConfigBase):  
    force_block_tools: List[str] = Field(default_factory=list)  
    allow_tools: List[str] = Field(default_factory=list)  
  
    @model_validator(mode="after")  
    def validate_overlap(self):  
        overlap = set(self.force_block_tools) & set(self.allow_tools)  
        if overlap:  
            raise ValueError(f"Same tool cannot be both blocked and allowed: {sorted(overlap)}")  
        return self  
  
--------------------------------------------------------------------  
13.4 ConditionalWhenClause  
--------------------------------------------------------------------  
  
class ConditionalWhenClause(RuntimeConfigBase):  
    stage_access_mode_in: List[AccessModeEnum] = Field(default_factory=list)  
    active_review_exists: Optional[bool] = None  
    approval_required: Optional[bool] = None  
    actor_not_in_approval_roles: Optional[bool] = None  
    unresolved_severe_breach: Optional[bool] = None  
  
--------------------------------------------------------------------  
13.5 ConditionalThenClause  
--------------------------------------------------------------------  
  
class ConditionalThenClause(RuntimeConfigBase):  
    force_block_tools: List[str] = Field(default_factory=list)  
    force_allow_tools: List[str] = Field(default_factory=list)  
    force_block_tool_groups: List[str] = Field(default_factory=list)  
  
--------------------------------------------------------------------  
13.6 ConditionalGovernanceRule  
--------------------------------------------------------------------  
  
class ConditionalGovernanceRule(RuntimeConfigBase):  
    rule_id: str  
    when: ConditionalWhenClause  
    then: ConditionalThenClause  
  
--------------------------------------------------------------------  
13.7 GovernanceOverlaysConfig  
--------------------------------------------------------------------  
  
class GovernanceOverlaysConfig(RuntimeConfigBase):  
    governance_overlays: Dict[str, Any]  
  
This is one place where a typed nested structure is better:  
  
class GovernanceOverlaysSection(RuntimeConfigBase):  
    default_rules: DefaultGovernanceRules  
    stage_rules: Dict[str, StageGovernanceRule] = Field(default_factory=dict)  
    role_overrides: Dict[ActorRoleEnum, RoleGovernanceOverride] = Field(default_factory=dict)  
    conditional_rules: List[ConditionalGovernanceRule] = Field(default_factory=list)  
  
class GovernanceOverlaysConfig(RuntimeConfigBase):  
    governance_overlays: GovernanceOverlaysSection  
  
====================================================================  
14. RETRY POLICY SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
14.1 RetryDefaults  
--------------------------------------------------------------------  
  
class RetryDefaults(RuntimeConfigBase):  
    safe_retry_backoff_seconds: List[int] = Field(default_factory=lambda: [1, 3, 5])  
    limited_retry_backoff_seconds: List[int] = Field(default_factory=lambda: [2, 5])  
    no_retry: List[int] = Field(default_factory=list)  
  
--------------------------------------------------------------------  
14.2 ToolRetryRule  
--------------------------------------------------------------------  
  
class ToolRetryRule(RuntimeConfigBase):  
    retry_mode: RetryModeEnum  
    requires_idempotency_check: bool = False  
  
--------------------------------------------------------------------  
14.3 RetryPoliciesSection  
--------------------------------------------------------------------  
  
class RetryPoliciesSection(RuntimeConfigBase):  
    defaults: RetryDefaults = Field(default_factory=RetryDefaults)  
    tool_rules: Dict[str, ToolRetryRule] = Field(default_factory=dict)  
  
class RetryPoliciesConfig(RuntimeConfigBase):  
    retry_policies: RetryPoliciesSection  
  
====================================================================  
15. FAILURE ROUTE SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
15.1 FailureRouteEntry  
--------------------------------------------------------------------  
  
class FailureRouteEntry(RuntimeConfigBase):  
    on_failure: Optional[str] = None  
    on_rejection: Optional[str] = None  
  
--------------------------------------------------------------------  
15.2 FailureRoutesConfig  
--------------------------------------------------------------------  
  
class FailureRoutesConfig(RuntimeConfigBase):  
    failure_routes: Dict[str, FailureRouteEntry]  
  
Validator ideas:  
- at least one of on_failure or on_rejection should be present  
  
====================================================================  
16. WORKFLOW ROUTES SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
16.1 WorkflowRoutesConfig  
--------------------------------------------------------------------  
  
class WorkflowRoutesConfig(RuntimeConfigBase):  
    workflow_routes: Dict[str, StageRouteMap]  
  
Validator ideas:  
- route targets should not be duplicated within one route list  
- cross-file validation should verify route targets exist in stage registry  
  
====================================================================  
17. DOMAIN OVERLAY SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
17.1 DomainStageUIOverride  
--------------------------------------------------------------------  
  
class DomainStageUIOverride(RuntimeConfigBase):  
    ui_mode: Optional[UIModeEnum] = None  
    interaction_mode: Optional[InteractionModeEnum] = None  
    token_mode: Optional[TokenModeEnum] = None  
  
--------------------------------------------------------------------  
17.2 DomainStageToolAdditions  
--------------------------------------------------------------------  
  
class DomainStageToolAdditions(RuntimeConfigBase):  
    explicit_allow: List[str] = Field(default_factory=list)  
    explicit_block: List[str] = Field(default_factory=list)  
  
--------------------------------------------------------------------  
17.3 DomainOverlaySection  
--------------------------------------------------------------------  
  
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
  
====================================================================  
18. ROLE OVERLAY SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
18.1 RoleStageOverride  
--------------------------------------------------------------------  
  
class RoleStageOverride(RuntimeConfigBase):  
    ui_mode: Optional[UIModeEnum] = None  
    interaction_mode: Optional[InteractionModeEnum] = None  
    token_mode: Optional[TokenModeEnum] = None  
  
--------------------------------------------------------------------  
18.2 RoleOverlaySection  
--------------------------------------------------------------------  
  
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
  
====================================================================  
19. ENVIRONMENT OVERLAY SCHEMA  
====================================================================  
  
--------------------------------------------------------------------  
19.1 EnvironmentStrictness  
--------------------------------------------------------------------  
  
class EnvironmentStrictness(RuntimeConfigBase):  
    enforce_stage_preconditions: bool = True  
    enforce_review_requirement: bool = True  
    enforce_audit_requirement: bool = True  
    enforce_role_approval_check: bool = True  
  
--------------------------------------------------------------------  
19.2 EnvironmentRetries  
--------------------------------------------------------------------  
  
class EnvironmentRetries(RuntimeConfigBase):  
    max_safe_retries: int = Field(default=3, ge=0)  
    max_limited_retries: int = Field(default=1, ge=0)  
  
--------------------------------------------------------------------  
19.3 EnvironmentBlockRules  
--------------------------------------------------------------------  
  
class EnvironmentBlockRules(RuntimeConfigBase):  
    block_unknown_tools: bool = True  
    block_unknown_stages: bool = True  
    block_unknown_roles: bool = True  
  
--------------------------------------------------------------------  
19.4 EnvironmentUIDefaults  
--------------------------------------------------------------------  
  
class EnvironmentUIDefaults(RuntimeConfigBase):  
    prefer_review_shell_for_governed_stages: bool = True  
  
--------------------------------------------------------------------  
19.5 EnvironmentOverlaySection  
--------------------------------------------------------------------  
  
class EnvironmentOverlaySection(RuntimeConfigBase):  
    environment_name: EnvironmentNameEnum  
    strictness: EnvironmentStrictness = Field(default_factory=EnvironmentStrictness)  
    retries: EnvironmentRetries = Field(default_factory=EnvironmentRetries)  
    block_rules: EnvironmentBlockRules = Field(default_factory=EnvironmentBlockRules)  
    ui_defaults: EnvironmentUIDefaults = Field(default_factory=EnvironmentUIDefaults)  
  
class EnvironmentOverlayConfig(RuntimeConfigBase):  
    environment_overlay: EnvironmentOverlaySection  
  
====================================================================  
20. RUNTIME CONFIG BUNDLE SCHEMA  
====================================================================  
  
This is the most important cross-file validation object.  
  
--------------------------------------------------------------------  
20.1 RuntimeConfigBundle  
--------------------------------------------------------------------  
  
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
  
--------------------------------------------------------------------  
20.2 Cross-file validators  
--------------------------------------------------------------------  
  
Recommended bundle validators:  
  
Validator A:  
Every stage in stage_tool_matrix must exist in stage_registry  
  
Validator B:  
Every stage in stage_preconditions must exist in stage_registry  
  
Validator C:  
Every stage in workflow_routes must exist in stage_registry  
  
Validator D:  
Every stage in failure_routes must exist in stage_registry  
  
Validator E:  
Every route target must exist in stage_registry  
  
Validator F:  
Every tool in tool_groups, virtual_tool_groups, explicit_allow,  
explicit_block, role force allow/block, governance overrides must exist  
in the master tool universe  
  
Validator G:  
Every UI mode referenced by stage registry or overlays must exist in  
ui_modes  
  
Validator H:  
Every interaction mode referenced by stage registry must exist in  
interaction_modes  
  
Validator I:  
Every token mode referenced by stage registry or overlays must exist in  
token_modes  
  
Validator J:  
If a stage has requires_active_review in stage_preconditions, its  
access_mode should usually be REVIEW_REQUIRED or FINALIZATION_GATED  
  
Validator K:  
If stage governance says approval_required=true, auto_continue_allowed  
must be false  
  
Suggested model validator outline:  
  
    @model_validator(mode="after")  
    def validate_cross_file_consistency(self):  
        stage_names = set(self.stage_registry.stage_registry.keys())  
  
        for stage_name in self.stage_tool_matrix.stage_tool_matrix:  
            if stage_name not in stage_names:  
                raise ValueError(f"Stage tool matrix references unknown stage: {stage_name}")  
  
        for stage_name in self.stage_preconditions.stage_preconditions:  
            if stage_name not in stage_names:  
                raise ValueError(f"Stage preconditions reference unknown stage: {stage_name}")  
  
        for stage_name, route_map in self.workflow_routes.workflow_routes.items():  
            if stage_name not in stage_names:  
                raise ValueError(f"Workflow routes reference unknown stage: {stage_name}")  
  
            for route_list in [  
                route_map.on_success,  
                route_map.on_review_required,  
                route_map.on_pass,  
                route_map.on_fail,  
                route_map.on_approved,  
                route_map.on_rejected,  
                route_map.on_auto_continue,  
                route_map.on_remediation_required  
            ]:  
                for target in route_list:  
                    if target not in stage_names:  
                        raise ValueError(f"Workflow route target does not exist: {target}")  
  
        return self  
  
====================================================================  
21. RECOMMENDED FILE MAPPING  
====================================================================  
  
Suggested Python files:  
  
platform_core/runtime/config_models/base.py  
- RuntimeConfigBase  
  
platform_core/runtime/config_models/enums.py  
- all enums  
  
platform_core/runtime/config_models/fragments.py  
- shared fragment models  
  
platform_core/runtime/config_models/runtime_master.py  
- RuntimeMasterConfig  
- RuntimeMasterSection  
- EnabledModules  
- ResolverDefaults  
- FileRefMap  
  
platform_core/runtime/config_models/tool_groups.py  
- ToolGroupDefinition  
- ToolGroupsConfig  
- VirtualToolGroupDefinition  
- VirtualToolGroupsConfig  
  
platform_core/runtime/config_models/roles.py  
- RoleCapabilityDefinition  
- RoleCapabilitiesConfig  
- RoleOverlaySection  
- RoleOverlayConfig  
  
platform_core/runtime/config_models/ui.py  
- UIModeDefinition  
- UIModesConfig  
- InteractionModeDefinition  
- InteractionModesConfig  
- TokenModeDefinition  
- TokenModesConfig  
  
platform_core/runtime/config_models/stages.py  
- StageDefinition  
- StageRegistryConfig  
- StageToolMatrixEntry  
- StageToolMatrixConfig  
- StagePreconditionEntry  
- StagePreconditionsConfig  
  
platform_core/runtime/config_models/governance.py  
- DefaultGovernanceRules  
- StageGovernanceRule  
- RoleGovernanceOverride  
- ConditionalWhenClause  
- ConditionalThenClause  
- ConditionalGovernanceRule  
- GovernanceOverlaysSection  
- GovernanceOverlaysConfig  
  
platform_core/runtime/config_models/retries.py  
- RetryDefaults  
- ToolRetryRule  
- RetryPoliciesSection  
- RetryPoliciesConfig  
  
platform_core/runtime/config_models/routes.py  
- FailureRouteEntry  
- FailureRoutesConfig  
- StageRouteMap  
- WorkflowRoutesConfig  
  
platform_core/runtime/config_models/domain.py  
- DomainStageUIOverride  
- DomainStageToolAdditions  
- DomainOverlaySection  
- DomainOverlayConfig  
  
platform_core/runtime/config_models/environment.py  
- EnvironmentStrictness  
- EnvironmentRetries  
- EnvironmentBlockRules  
- EnvironmentUIDefaults  
- EnvironmentOverlaySection  
- EnvironmentOverlayConfig  
  
platform_core/runtime/config_models/bundle.py  
- RuntimeConfigBundle  
  
====================================================================  
22. RECOMMENDED DEFAULTS  
====================================================================  
  
Good defaults:  
  
- runtime_mode = strict  
- unknown_stage_behavior = block  
- unknown_role_behavior = block  
- missing_tool_group_behavior = block  
- default_ui_mode = chat_only  
- default_interaction_mode = read  
- default_token_mode = micro_mode  
  
- safe retry default backoff = [1, 3, 5]  
- limited retry default backoff = [2, 5]  
  
- production block_unknown_tools = true  
- production enforce_review_requirement = true  
- production enforce_audit_requirement = true  
  
====================================================================  
23. FUTURE-PROOFING NOTES  
====================================================================  
  
1. Keep enums centralized  
--------------------------------------------------------------------  
Do not redefine string literals across files.  
  
2. Keep bundle validation separate  
--------------------------------------------------------------------  
Per-file models should validate local structure.  
Bundle validator should validate cross-file consistency.  
  
3. Avoid giant models  
--------------------------------------------------------------------  
Split config models by concern and keep bundle as final assembly.  
  
4. Use Optional overlays  
--------------------------------------------------------------------  
Domain, role, and environment overlays should remain optional.  
  
5. Support future extensions  
--------------------------------------------------------------------  
Potential additions later:  
- stage timeout rules  
- escalation SLA rules  
- review actor assignment rules  
- notification rules  
- UI layout presets  
- domain-specific evidence packs  
  
====================================================================  
24. RECOMMENDED NEXT STEP  
====================================================================  
  
The best next artifact is:  
  
PYTHON CODE SKELETON  
for these Pydantic models,  
including:  
- actual class definitions  
- validators  
- imports  
- file-by-file implementation stubs  
  
That would be the most direct handoff for coding.  
  
====================================================================  
END OF PYDANTIC SCHEMA DESIGN  
====================================================================  
