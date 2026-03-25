# Python Code Skeleton - Runtime Resolver  
  
# ================================================================  
# PYTHON CODE SKELETON  
# RUNTIME RESOLVERS  
# AGENTIC AI MDLC FRAMEWORK  
# ================================================================  
#  
# Suggested files:  
#  
# platform_core/runtime/  
#   role_config_resolver.py  
#   tool_group_resolver.py  
#   governance_rule_resolver.py  
#   retry_policy_resolver.py  
#   allowlist_resolver.py  
#   runtime_resolver.py  
#  
# This skeleton is designed to work with the earlier Pydantic config  
# models and RuntimeConfigLoader / StageConfigResolver.  
# ================================================================  
  
  
# ================================================================  
# FILE: platform_core/runtime/role_config_resolver.py  
# ================================================================  
  
from __future__ import annotations  
  
from copy import deepcopy  
from typing import Any, Dict, Optional  
  
from .config_models.bundle import RuntimeConfigBundle  
from .config_models.enums import ActorRoleEnum  
  
  
class RoleConfigResolver:  
    """  
    Resolves effective role capabilities by combining:  
    - base role_capabilities  
    - optional role_overlay  
    """  
  
    def __init__(self, bundle: RuntimeConfigBundle):  
        self.bundle = bundle  
  
    def resolve_role_config(self, actor_role: str | ActorRoleEnum) -> Dict[str, Any]:  
        role_enum = ActorRoleEnum(actor_role)  
        base = deepcopy(  
            self.bundle.role_capabilities.role_capabilities[role_enum].model_dump()  
        )  
  
        overlay = self.bundle.role_overlay  
        if overlay and overlay.role_overlay.role_name == role_enum:  
            base["force_block_tools"] = overlay.role_overlay.force_block_tools  
            base["force_allow_tools"] = overlay.role_overlay.force_allow_tools  
            base["ui_mode_overrides"] = overlay.role_overlay.ui_mode_overrides  
            base["token_mode_overrides"] = overlay.role_overlay.token_mode_overrides  
        else:  
            base["force_block_tools"] = []  
            base["force_allow_tools"] = []  
            base["ui_mode_overrides"] = {}  
            base["token_mode_overrides"] = {}  
  
        return base  
  
    def can_build(self, actor_role: str | ActorRoleEnum) -> bool:  
        return bool(self.resolve_role_config(actor_role)["can_build"])  
  
    def can_review(self, actor_role: str | ActorRoleEnum) -> bool:  
        return bool(self.resolve_role_config(actor_role)["can_review"])  
  
    def can_approve(self, actor_role: str | ActorRoleEnum) -> bool:  
        return bool(self.resolve_role_config(actor_role)["can_approve"])  
  
    def can_finalize_validation_conclusion(  
        self, actor_role: str | ActorRoleEnum  
    ) -> bool:  
        return bool(  
            self.resolve_role_config(actor_role)[  
                "can_finalize_validation_conclusion"  
            ]  
        )  
  
    def can_ingest_monitoring(self, actor_role: str | ActorRoleEnum) -> bool:  
        return bool(self.resolve_role_config(actor_role)["can_ingest_monitoring"])  
  
    def can_signoff(self, actor_role: str | ActorRoleEnum) -> bool:  
        return bool(self.resolve_role_config(actor_role)["can_signoff"])  
  
  
# ================================================================  
# FILE: platform_core/runtime/tool_group_resolver.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Dict, List, Set  
  
from .config_models.bundle import RuntimeConfigBundle  
  
  
class ToolGroupResolver:  
    """  
    Expands real and virtual tool groups into concrete tool names.  
    """  
  
    def __init__(self, bundle: RuntimeConfigBundle):  
        self.bundle = bundle  
  
    def get_all_known_tools(self) -> Set[str]:  
        known: Set[str] = set()  
        for group_def in self.bundle.tool_groups.tool_groups.values():  
            known.update(group_def.tools)  
        if self.bundle.virtual_tool_groups:  
            for virtual_def in self.bundle.virtual_tool_groups.virtual_tool_groups.values():  
                known.update(virtual_def.includes)  
        return known  
  
    def expand_group(self, group_name: str) -> List[str]:  
        if group_name in self.bundle.tool_groups.tool_groups:  
            return list(self.bundle.tool_groups.tool_groups[group_name].tools)  
  
        if self.bundle.virtual_tool_groups and (  
            group_name in self.bundle.virtual_tool_groups.virtual_tool_groups  
        ):  
            return list(  
                self.bundle.virtual_tool_groups.virtual_tool_groups[group_name].includes  
            )  
  
        return []  
  
    def expand_groups(self, group_names: List[str]) -> List[str]:  
        expanded: List[str] = []  
        seen: Set[str] = set()  
  
        for group_name in group_names:  
            for tool in self.expand_group(group_name):  
                if tool not in seen:  
                    expanded.append(tool)  
                    seen.add(tool)  
  
        return expanded  
  
    def validate_tools_exist(self, tool_names: List[str]) -> List[str]:  
        known = self.get_all_known_tools()  
        return [tool for tool in tool_names if tool not in known]  
  
  
# ================================================================  
# FILE: platform_core/runtime/governance_rule_resolver.py  
# ================================================================  
  
from __future__ import annotations  
  
from copy import deepcopy  
from typing import Any, Dict, List, Set  
  
from .config_models.bundle import RuntimeConfigBundle  
from .config_models.enums import AccessModeEnum, ActorRoleEnum  
  
  
class GovernanceRuleResolver:  
    """  
    Resolves effective governance requirements for a stage and applies  
    conditional governance rules at runtime.  
    """  
  
    def __init__(self, bundle: RuntimeConfigBundle):  
        self.bundle = bundle  
  
    def get_stage_governance(self, stage_name: str) -> Dict[str, Any]:  
        gov_section = self.bundle.governance_overlays.governance_overlays  
        base = deepcopy(gov_section.default_rules.model_dump())  
  
        if stage_name in gov_section.stage_rules:  
            base.update(gov_section.stage_rules[stage_name].model_dump())  
  
        return base  
  
    def get_role_governance_override(  
        self, actor_role: str | ActorRoleEnum  
    ) -> Dict[str, Any]:  
        role_enum = ActorRoleEnum(actor_role)  
        gov_section = self.bundle.governance_overlays.governance_overlays  
  
        if role_enum in gov_section.role_overrides:  
            return gov_section.role_overrides[role_enum].model_dump()  
  
        return {  
            "force_block_tools": [],  
            "allow_tools": [],  
        }  
  
    def _condition_matches(  
        self, when_clause: Dict[str, Any], runtime_facts: Dict[str, Any]  
    ) -> bool:  
        # Only check supported keys that are explicitly present in the rule.  
        for key, value in when_clause.items():  
            if value is None:  
                continue  
  
            if key == "stage_access_mode_in":  
                current_access_mode = runtime_facts.get("stage_access_mode")  
                if current_access_mode not in value:  
                    return False  
                continue  
  
            if runtime_facts.get(key) != value:  
                return False  
  
        return True  
  
    def apply_conditional_rules(  
        self,  
        runtime_facts: Dict[str, Any],  
        allowed_tools: List[str],  
        blocked_tools: List[str],  
    ) -> Dict[str, Any]:  
        gov_section = self.bundle.governance_overlays.governance_overlays  
  
        allowed: Set[str] = set(allowed_tools)  
        blocked: Set[str] = set(blocked_tools)  
  
        for rule in gov_section.conditional_rules:  
            when_clause = rule.when.model_dump()  
            then_clause = rule.then.model_dump()  
  
            if not self._condition_matches(when_clause, runtime_facts):  
                continue  
  
            allowed.update(then_clause.get("force_allow_tools", []))  
            blocked.update(then_clause.get("force_block_tools", []))  
  
            # Force block tool groups  
            for group_name in then_clause.get("force_block_tool_groups", []):  
                # Group expansion happens in AllowlistResolver; here just pass through  
                runtime_facts.setdefault("_force_block_tool_groups", []).append(group_name)  
  
        return {  
            "allowed_tools": sorted(allowed),  
            "blocked_tools": sorted(blocked),  
            "force_block_tool_groups": runtime_facts.get("_force_block_tool_groups", []),  
        }  
  
  
# ================================================================  
# FILE: platform_core/runtime/retry_policy_resolver.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict  
  
from .config_models.bundle import RuntimeConfigBundle  
  
  
class RetryPolicyResolver:  
    """  
    Resolves retry policy per tool.  
    """  
  
    def __init__(self, bundle: RuntimeConfigBundle):  
        self.bundle = bundle  
  
    def resolve_retry_policy(self, tool_name: str) -> Dict[str, Any]:  
        section = self.bundle.retry_policies.retry_policies  
  
        defaults = section.defaults.model_dump()  
  
        if tool_name in section.tool_rules:  
            rule = section.tool_rules[tool_name].model_dump()  
            return {  
                "retry_mode": rule["retry_mode"],  
                "requires_idempotency_check": rule["requires_idempotency_check"],  
                "defaults": defaults,  
            }  
  
        return {  
            "retry_mode": "safe",  
            "requires_idempotency_check": False,  
            "defaults": defaults,  
        }  
  
  
# ================================================================  
# FILE: platform_core/runtime/allowlist_resolver.py  
# ================================================================  
  
from __future__ import annotations  
  
from copy import deepcopy  
from typing import Any, Dict, List, Set  
  
from .config_models.bundle import RuntimeConfigBundle  
from .config_models.enums import ActorRoleEnum  
from .governance_rule_resolver import GovernanceRuleResolver  
from .role_config_resolver import RoleConfigResolver  
from .stage_config_resolver import StageConfigResolver  
from .tool_group_resolver import ToolGroupResolver  
  
  
class AllowlistResolver:  
    """  
    Resolves final allowed and blocked tools from:  
    - stage registry / stage tool matrix  
    - role capabilities / role overlay  
    - governance overlays  
    - runtime facts  
    """  
  
    def __init__(self, bundle: RuntimeConfigBundle):  
        self.bundle = bundle  
        self.stage_config_resolver = StageConfigResolver(bundle)  
        self.role_config_resolver = RoleConfigResolver(bundle)  
        self.tool_group_resolver = ToolGroupResolver(bundle)  
        self.governance_rule_resolver = GovernanceRuleResolver(bundle)  
  
    def _expand_stage_tools(self, stage_name: str) -> Dict[str, List[str]]:  
        stage_tool_matrix = self.bundle.stage_tool_matrix.stage_tool_matrix.get(stage_name)  
        if not stage_tool_matrix:  
            return {"allowed_tools": [], "blocked_tools": []}  
  
        allowed = self.tool_group_resolver.expand_groups(  
            stage_tool_matrix.allowed_tool_groups  
        )  
        blocked = self.tool_group_resolver.expand_groups(  
            stage_tool_matrix.blocked_tool_groups  
        )  
  
        # explicit overrides  
        allowed.extend(stage_tool_matrix.explicit_allow)  
        blocked.extend(stage_tool_matrix.explicit_block)  
  
        return {  
            "allowed_tools": sorted(set(allowed)),  
            "blocked_tools": sorted(set(blocked)),  
        }  
  
    def _apply_domain_overlay(  
        self, stage_name: str, allowed_tools: Set[str], blocked_tools: Set[str]  
    ) -> None:  
        overlay = self.bundle.domain_overlay  
        if not overlay:  
            return  
  
        domain_overlay = overlay.domain_overlay  
  
        if stage_name in domain_overlay.stage_tool_additions:  
            additions = domain_overlay.stage_tool_additions[stage_name]  
            allowed_tools.update(additions.explicit_allow)  
            blocked_tools.update(additions.explicit_block)  
  
    def _apply_role_overlay(  
        self, actor_role: str | ActorRoleEnum, allowed_tools: Set[str], blocked_tools: Set[str]  
    ) -> None:  
        role_cfg = self.role_config_resolver.resolve_role_config(actor_role)  
        allowed_tools.update(role_cfg.get("force_allow_tools", []))  
        blocked_tools.update(role_cfg.get("force_block_tools", []))  
  
    def _apply_role_capability_filters(  
        self,  
        actor_role: str | ActorRoleEnum,  
        allowed_tools: Set[str],  
        blocked_tools: Set[str],  
    ) -> None:  
        role_enum = ActorRoleEnum(actor_role)  
        role_cfg = self.role_config_resolver.resolve_role_config(role_enum)  
  
        # Hard capability-based blocks  
        if not role_cfg["can_approve"]:  
            blocked_tools.update(  
                {  
                    "approve_review",  
                    "approve_review_with_conditions",  
                    "register_signoff",  
                }  
            )  
  
        if not role_cfg["can_finalize_validation_conclusion"]:  
            blocked_tools.add("finalize_validation_conclusion")  
  
        if not role_cfg["can_ingest_monitoring"]:  
            blocked_tools.update(  
                {  
                    "ingest_monitoring_snapshot",  
                    "append_monitoring_snapshot",  
                }  
            )  
  
        if not role_cfg["can_signoff"]:  
            blocked_tools.add("register_signoff")  
  
        if not role_cfg["can_promote_knowledge_beyond_project"]:  
            blocked_tools.add("promote_knowledge")  
  
    def resolve_allowlist(  
        self,  
        stage_name: str,  
        actor_role: str | ActorRoleEnum,  
        runtime_facts: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        stage_cfg = self.stage_config_resolver.resolve_stage_config(stage_name)  
        stage_tools = self._expand_stage_tools(stage_name)  
  
        allowed_tools: Set[str] = set(stage_tools["allowed_tools"])  
        blocked_tools: Set[str] = set(stage_tools["blocked_tools"])  
  
        # domain overlay  
        self._apply_domain_overlay(stage_name, allowed_tools, blocked_tools)  
  
        # role overlay  
        self._apply_role_overlay(actor_role, allowed_tools, blocked_tools)  
  
        # role capability filter  
        self._apply_role_capability_filters(actor_role, allowed_tools, blocked_tools)  
  
        # stage governance  
        stage_gov = self.governance_rule_resolver.get_stage_governance(stage_name)  
        role_gov = self.governance_rule_resolver.get_role_governance_override(actor_role)  
  
        allowed_tools.update(role_gov.get("allow_tools", []))  
        blocked_tools.update(role_gov.get("force_block_tools", []))  
  
        # conditional governance  
        runtime_facts = deepcopy(runtime_facts)  
        runtime_facts["stage_access_mode"] = stage_cfg["access_mode"]  
        gov_adjusted = self.governance_rule_resolver.apply_conditional_rules(  
            runtime_facts=runtime_facts,  
            allowed_tools=sorted(allowed_tools),  
            blocked_tools=sorted(blocked_tools),  
        )  
        allowed_tools = set(gov_adjusted["allowed_tools"])  
        blocked_tools = set(gov_adjusted["blocked_tools"])  
  
        # Apply any force-block-tool-groups from conditional rules  
        force_block_groups = gov_adjusted.get("force_block_tool_groups", [])  
        if force_block_groups:  
            blocked_tools.update(self.tool_group_resolver.expand_groups(force_block_groups))  
  
        # Final rule: blocked wins over allowed  
        final_allowed = sorted(tool for tool in allowed_tools if tool not in blocked_tools)  
        final_blocked = sorted(blocked_tools)  
  
        return {  
            "stage_name": stage_name,  
            "actor_role": str(actor_role),  
            "access_mode": stage_cfg["access_mode"],  
            "allowed_tools": final_allowed,  
            "blocked_tools": final_blocked,  
            "review_required": stage_gov.get("review_required", False),  
            "approval_required": stage_gov.get("approval_required", False),  
            "audit_required": stage_gov.get("audit_required", False),  
            "auto_continue_allowed": stage_gov.get("auto_continue_allowed", True),  
        }  
  
  
# ================================================================  
# FILE: platform_core/runtime/runtime_resolver.py  
# ================================================================  
  
from __future__ import annotations  
  
from copy import deepcopy  
from typing import Any, Dict, List, Optional  
  
from .allowlist_resolver import AllowlistResolver  
from .config_models.bundle import RuntimeConfigBundle  
from .config_models.enums import (  
    AccessModeEnum,  
    ActorRoleEnum,  
    InteractionModeEnum,  
    TokenModeEnum,  
    UIModeEnum,  
)  
from .role_config_resolver import RoleConfigResolver  
from .stage_config_resolver import StageConfigResolver  
  
  
class RuntimeResolver:  
    """  
    Produces final runtime decision output:  
    - allowed_tools  
    - blocked_tools  
    - review_required  
    - approval_required  
    - audit_required  
    - UI mode  
    - interaction mode  
    - token mode  
    - auto_continue_allowed  
    """  
  
    def __init__(self, bundle: RuntimeConfigBundle):  
        self.bundle = bundle  
        self.stage_config_resolver = StageConfigResolver(bundle)  
        self.role_config_resolver = RoleConfigResolver(bundle)  
        self.allowlist_resolver = AllowlistResolver(bundle)  
  
    def _validate_preconditions(  
        self,  
        stage_name: str,  
        runtime_context: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        preconditions_cfg = self.bundle.stage_preconditions.stage_preconditions.get(stage_name)  
        if not preconditions_cfg:  
            return {  
                "preconditions_passed": True,  
                "missing_preconditions": [],  
            }  
  
        missing: List[str] = []  
  
        for req_id in preconditions_cfg.required_ids:  
            if not runtime_context.get(req_id):  
                missing.append(f"id:{req_id}")  
  
        current_refs = runtime_context.get("current_refs", {})  
        for req_ref in preconditions_cfg.required_refs:  
            if req_ref not in current_refs or current_refs.get(req_ref) in (None, ""):  
                missing.append(f"ref:{req_ref}")  
  
        flags = runtime_context.get("flags", {})  
        for req_flag in preconditions_cfg.required_flags:  
            if not flags.get(req_flag, False):  
                missing.append(f"flag:{req_flag}")  
  
        completed_stages = set(runtime_context.get("completed_stages", []))  
        for req_stage in preconditions_cfg.required_prior_stages:  
            if req_stage not in completed_stages:  
                missing.append(f"prior_stage:{req_stage}")  
  
        if preconditions_cfg.requires_active_review and not runtime_context.get("active_review_exists", False):  
            missing.append("active_review")  
  
        return {  
            "preconditions_passed": len(missing) == 0,  
            "missing_preconditions": missing,  
        }  
  
    def _resolve_ui_mode(  
        self,  
        stage_name: str,  
        actor_role: str | ActorRoleEnum,  
        stage_cfg: Dict[str, Any],  
    ) -> str:  
        ui_mode = stage_cfg["default_ui_mode"]  
  
        # domain overlay  
        if self.bundle.domain_overlay:  
            stage_ui_overrides = self.bundle.domain_overlay.domain_overlay.stage_ui_overrides  
            if stage_name in stage_ui_overrides and stage_ui_overrides[stage_name].ui_mode:  
                ui_mode = stage_ui_overrides[stage_name].ui_mode  
  
        # role overlay  
        role_cfg = self.role_config_resolver.resolve_role_config(actor_role)  
        if stage_name in role_cfg.get("ui_mode_overrides", {}):  
            ui_mode = role_cfg["ui_mode_overrides"][stage_name]  
  
        # environment override preference  
        env_overlay = self.bundle.environment_overlay  
        if env_overlay:  
            env_ui_defaults = env_overlay.environment_overlay.ui_defaults  
            access_mode = stage_cfg["access_mode"]  
            if (  
                env_ui_defaults.prefer_review_shell_for_governed_stages  
                and access_mode in {AccessModeEnum.REVIEW_REQUIRED, AccessModeEnum.FINALIZATION_GATED}  
            ):  
                ui_mode = UIModeEnum.REVIEW_SHELL  
  
        return str(ui_mode)  
  
    def _resolve_interaction_mode(  
        self,  
        stage_cfg: Dict[str, Any],  
        review_required: bool,  
        approval_required: bool,  
    ) -> str:  
        interaction_mode = stage_cfg["default_interaction_mode"]  
  
        if approval_required:  
            return str(InteractionModeEnum.APPROVE)  
        if review_required:  
            return str(InteractionModeEnum.REVIEW)  
  
        access_mode = stage_cfg["access_mode"]  
        if access_mode == AccessModeEnum.MONITORING_OPERATIONAL:  
            return str(InteractionModeEnum.MONITOR)  
        if access_mode == AccessModeEnum.READ_ONLY:  
            return str(InteractionModeEnum.READ)  
  
        return str(interaction_mode)  
  
    def _resolve_token_mode(  
        self,  
        stage_name: str,  
        actor_role: str | ActorRoleEnum,  
        stage_cfg: Dict[str, Any],  
        review_required: bool,  
        approval_required: bool,  
    ) -> str:  
        token_mode = stage_cfg["default_token_mode"]  
  
        # domain overlay  
        if self.bundle.domain_overlay:  
            stage_ui_overrides = self.bundle.domain_overlay.domain_overlay.stage_ui_overrides  
            if stage_name in stage_ui_overrides and stage_ui_overrides[stage_name].token_mode:  
                token_mode = stage_ui_overrides[stage_name].token_mode  
  
        # role overlay  
        role_cfg = self.role_config_resolver.resolve_role_config(actor_role)  
        if stage_name in role_cfg.get("token_mode_overrides", {}):  
            token_mode = role_cfg["token_mode_overrides"][stage_name]  
  
        # governance heuristic  
        if review_required or approval_required:  
            token_mode = TokenModeEnum.DEEP_REVIEW_MODE  
  
        return str(token_mode)  
  
    def _compute_auto_continue(  
        self,  
        preconditions_passed: bool,  
        review_required: bool,  
        approval_required: bool,  
        audit_required: bool,  
        runtime_context: Dict[str, Any],  
        base_auto_continue_allowed: bool,  
    ) -> bool:  
        if not preconditions_passed:  
            return False  
        if review_required:  
            return False  
        if approval_required:  
            return False  
        if runtime_context.get("unresolved_severe_breach", False):  
            return False  
        if runtime_context.get("stale_state_detected", False):  
            return False  
  
        return bool(base_auto_continue_allowed)  
  
    def resolve(self, runtime_context: Dict[str, Any]) -> Dict[str, Any]:  
        """  
        Expected runtime_context shape:  
        {  
          "project_id": "...",  
          "run_id": "...",  
          "session_id": "...",  
          "active_role": "developer",  
          "active_domain": "scorecard",  
          "workflow_mode": "default",  
          "stage_context": {"active_stage": "..."},  
          "flags": {...},  
          "current_refs": {...},  
          "completed_stages": [...],  
          "active_review_exists": False,  
          "approval_required": False,  
          "unresolved_severe_breach": False,  
          "stale_state_detected": False  
        }  
        """  
        actor_role = runtime_context["active_role"]  
        stage_name = runtime_context["stage_context"]["active_stage"]  
  
        stage_cfg = self.stage_config_resolver.resolve_stage_config(stage_name)  
        precondition_result = self._validate_preconditions(stage_name, runtime_context)  
  
        allowlist_result = self.allowlist_resolver.resolve_allowlist(  
            stage_name=stage_name,  
            actor_role=actor_role,  
            runtime_facts=runtime_context,  
        )  
  
        review_required = bool(allowlist_result["review_required"])  
        approval_required = bool(allowlist_result["approval_required"])  
        audit_required = bool(allowlist_result["audit_required"])  
  
        ui_mode = self._resolve_ui_mode(stage_name, actor_role, stage_cfg)  
        interaction_mode = self._resolve_interaction_mode(  
            stage_cfg=stage_cfg,  
            review_required=review_required,  
            approval_required=approval_required,  
        )  
        token_mode = self._resolve_token_mode(  
            stage_name=stage_name,  
            actor_role=actor_role,  
            stage_cfg=stage_cfg,  
            review_required=review_required,  
            approval_required=approval_required,  
        )  
  
        auto_continue_allowed = self._compute_auto_continue(  
            preconditions_passed=precondition_result["preconditions_passed"],  
            review_required=review_required,  
            approval_required=approval_required,  
            audit_required=audit_required,  
            runtime_context=runtime_context,  
            base_auto_continue_allowed=allowlist_result["auto_continue_allowed"],  
        )  
  
        # workflow routes  
        routes_cfg = self.bundle.workflow_routes.workflow_routes.get(stage_name)  
        next_routes: List[str] = []  
        if routes_cfg:  
            next_routes = routes_cfg.on_success  
  
        # Collapse tools if preconditions fail  
        allowed_tools = allowlist_result["allowed_tools"]  
        blocked_tools = allowlist_result["blocked_tools"]  
  
        if not precondition_result["preconditions_passed"]:  
            recovery_safe_tools = {  
                "get_workflow_state",  
                "resolve_recovery_path",  
                "replay_run",  
                "create_review",  
            }  
            allowed_tools = sorted(tool for tool in allowed_tools if tool in recovery_safe_tools)  
            blocked_tools = sorted(set(blocked_tools) | (set(allowlist_result["allowed_tools"]) - set(allowed_tools)))  
            auto_continue_allowed = False  
  
        return {  
            "stage_name": stage_name,  
            "actor_role": actor_role,  
            "access_mode": allowlist_result["access_mode"],  
            "preconditions_passed": precondition_result["preconditions_passed"],  
            "missing_preconditions": precondition_result["missing_preconditions"],  
            "allowed_tools": allowed_tools,  
            "blocked_tools": blocked_tools,  
            "review_required": review_required,  
            "approval_required": approval_required,  
            "audit_required": audit_required,  
            "auto_continue_allowed": auto_continue_allowed,  
            "recommended_ui_mode": ui_mode,  
            "recommended_interaction_mode": interaction_mode,  
            "recommended_token_mode": token_mode,  
            "recommended_next_routes": next_routes,  
            "notes": self._build_notes(  
                stage_name=stage_name,  
                review_required=review_required,  
                approval_required=approval_required,  
                audit_required=audit_required,  
                preconditions_passed=precondition_result["preconditions_passed"],  
                missing_preconditions=precondition_result["missing_preconditions"],  
            ),  
        }  
  
    def _build_notes(  
        self,  
        stage_name: str,  
        review_required: bool,  
        approval_required: bool,  
        audit_required: bool,  
        preconditions_passed: bool,  
        missing_preconditions: List[str],  
    ) -> List[str]:  
        notes: List[str] = []  
  
        if not preconditions_passed:  
            notes.append(  
                f"Stage {stage_name} has missing preconditions: {', '.join(missing_preconditions)}"  
            )  
  
        if review_required:  
            notes.append("Human review is required before continuation.")  
  
        if approval_required:  
            notes.append("Formal approval is required before finalization.")  
  
        if audit_required:  
            notes.append("Audit capture is mandatory for irreversible actions.")  
  
        return notes  
  
  
# ================================================================  
# OPTIONAL: QUICK USAGE EXAMPLE  
# ================================================================  
  
if __name__ == "__main__":  
    # Example only. Assumes RuntimeConfigLoader and YAML files exist.  
    from pathlib import Path  
  
    # from platform_core.runtime.runtime_config_loader import RuntimeConfigLoader  
  
    # loader = RuntimeConfigLoader(Path("configs/runtime"))  
    # bundle = loader.load_bundle(  
    #     domain_overlay_path="configs/runtime/domain_overlays/scorecard.yaml",  
    #     role_overlay_path="configs/runtime/role_overlays/developer.yaml",  
    #     environment_overlay_path="configs/runtime/environment_overlays/prod.yaml",  
    # )  
  
    # resolver = RuntimeResolver(bundle)  
    # decision = resolver.resolve(  
    #     {  
    #         "project_id": "proj_001",  
    #         "run_id": "run_001",  
    #         "session_id": "sess_001",  
    #         "active_role": "developer",  
    #         "active_domain": "scorecard",  
    #         "workflow_mode": "default",  
    #         "stage_context": {"active_stage": "coarse_classing_review"},  
    #         "flags": {  
    #             "dataprep_executed": True,  
    #             "methodology_review_completed": False,  
    #         },  
    #         "current_refs": {  
    #             "fine_bin_ref": "art_001",  
    #             "coarse_bin_candidate_ids": ["cand_001", "cand_002"],  
    #         },  
    #         "completed_stages": [  
    #             "data_preparation_config",  
    #             "data_preparation_execution",  
    #             "data_readiness_check",  
    #             "dataset_registration",  
    #             "feature_engineering",  
    #             "fine_classing",  
    #             "coarse_classing_candidate_build",  
    #         ],  
    #         "active_review_exists": True,  
    #         "unresolved_severe_breach": False,  
    #         "stale_state_detected": False,  
    #     }  
    # )  
    # print(decision)  
    pass  
