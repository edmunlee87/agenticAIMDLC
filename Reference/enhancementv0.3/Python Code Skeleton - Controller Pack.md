# Python Code Skeleton - Controller Pack  
  
# ================================================================  
# PYTHON CODE SKELETON  
# CONTROLLER PACK  
# AGENTIC AI MDLC FRAMEWORK  
# WIRED TO RUNTIME RESOLVERS  
# ================================================================  
#  
# Suggested files:  
#  
# platform_core/controllers/  
#   base_controller.py  
#   session_controller.py  
#   workflow_controller.py  
#   review_controller.py  
#   dataprep_controller.py  
#   validation_controller.py  
#   monitoring_controller.py  
#   controller_factory.py  
#  
# Notes:  
# - This skeleton assumes you already have:  
#   - RuntimeResolver  
#   - AllowlistResolver  
#   - RuntimeConfigBundle / loader  
#   - BaseResult / ValidationResultBase / StandardResponseEnvelope  
#   - service façade classes  
# - The controllers below are thin orchestration layers.  
# - Business logic should stay inside SDK services.  
# ================================================================  
  
  
# ================================================================  
# FILE: platform_core/controllers/base_controller.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict, Iterable, List, Optional  
  
  
class BaseController:  
    """  
    Base orchestration controller.  
  
    Responsibilities:  
    - resolve runtime decision  
    - verify tool allowance  
    - normalize inputs/outputs  
    - coordinate workflow patch, observability, and audit hooks  
    """  
  
    controller_name: str = "base_controller"  
  
    def __init__(  
        self,  
        *,  
        runtime_resolver: Any,  
        service_registry: Dict[str, Any],  
        observability_service: Optional[Any] = None,  
        audit_service: Optional[Any] = None,  
        workflow_service: Optional[Any] = None,  
    ) -> None:  
        self.runtime_resolver = runtime_resolver  
        self.service_registry = service_registry  
        self.observability_service = observability_service  
        self.audit_service = audit_service  
        self.workflow_service = workflow_service  
  
    # ------------------------------------------------------------  
    # Dependency helpers  
    # ------------------------------------------------------------  
    def _get_service(self, name: str) -> Any:  
        if name not in self.service_registry:  
            raise KeyError(f"Required service not registered: {name}")  
        return self.service_registry[name]  
  
    # ------------------------------------------------------------  
    # Runtime helpers  
    # ------------------------------------------------------------  
    def _resolve_runtime(self, runtime_context: Dict[str, Any]) -> Dict[str, Any]:  
        return self.runtime_resolver.resolve(runtime_context)  
  
    def _ensure_tool_allowed(  
        self,  
        runtime_decision: Dict[str, Any],  
        tool_name: str,  
    ) -> None:  
        allowed_tools = set(runtime_decision.get("allowed_tools", []))  
        if tool_name not in allowed_tools:  
            raise PermissionError(  
                f"Tool '{tool_name}' is not allowed in "  
                f"stage '{runtime_decision.get('stage_name')}' "  
                f"for role '{runtime_decision.get('actor_role')}'."  
            )  
  
    def _ensure_preconditions_passed(self, runtime_decision: Dict[str, Any]) -> None:  
        if not runtime_decision.get("preconditions_passed", False):  
            raise ValueError(  
                "Stage preconditions not satisfied: "  
                + ", ".join(runtime_decision.get("missing_preconditions", []))  
            )  
  
    # ------------------------------------------------------------  
    # Envelope helpers  
    # ------------------------------------------------------------  
    def _build_response(  
        self,  
        *,  
        status: str,  
        message: str,  
        controller_name: str,  
        action_name: str,  
        data: Optional[Dict[str, Any]] = None,  
        warnings: Optional[List[Dict[str, Any]]] = None,  
        errors: Optional[List[Dict[str, Any]]] = None,  
        references: Optional[Dict[str, Any]] = None,  
        runtime_decision: Optional[Dict[str, Any]] = None,  
        workflow_patch: Optional[Dict[str, Any]] = None,  
        agent_hint: Optional[Dict[str, Any]] = None,  
        audit_hint: Optional[Dict[str, Any]] = None,  
        observability_hint: Optional[Dict[str, Any]] = None,  
    ) -> Dict[str, Any]:  
        return {  
            "status": status,  
            "message": message,  
            "controller_name": controller_name,  
            "action_name": action_name,  
            "data": data or {},  
            "warnings": warnings or [],  
            "errors": errors or [],  
            "references": references or {},  
            "runtime_decision": runtime_decision or {},  
            "workflow_patch": workflow_patch or {},  
            "agent_hint": agent_hint or {},  
            "audit_hint": audit_hint or {},  
            "observability_hint": observability_hint or {},  
        }  
  
    # ------------------------------------------------------------  
    # Hook helpers  
    # ------------------------------------------------------------  
    def _emit_event_if_needed(self, result: Dict[str, Any]) -> None:  
        if not self.observability_service:  
            return  
        hint = result.get("observability_hint", {})  
        if hint.get("should_write_event"):  
            self.observability_service.write_event(  
                event_type=hint.get("event_type", "controller_action"),  
                payload={  
                    "controller_name": result.get("controller_name"),  
                    "action_name": result.get("action_name"),  
                    "status": result.get("status"),  
                    "references": result.get("references", {}),  
                    "data_summary": result.get("data", {}),  
                },  
            )  
  
    def _write_audit_if_needed(self, result: Dict[str, Any]) -> None:  
        if not self.audit_service:  
            return  
        hint = result.get("audit_hint", {})  
        if hint.get("should_write_audit"):  
            self.audit_service.write_audit_record(  
                audit_type=hint.get("audit_type", "controller_action"),  
                payload={  
                    "controller_name": result.get("controller_name"),  
                    "action_name": result.get("action_name"),  
                    "status": result.get("status"),  
                    "references": result.get("references", {}),  
                    "workflow_patch": result.get("workflow_patch", {}),  
                },  
            )  
  
    def _apply_workflow_patch_if_needed(self, result: Dict[str, Any]) -> None:  
        if not self.workflow_service:  
            return  
        patch = result.get("workflow_patch", {})  
        run_id = result.get("references", {}).get("run_id")  
        if run_id and patch:  
            self.workflow_service.update_workflow_state(  
                run_id=run_id,  
                state_patch=patch,  
            )  
  
    def _finalize_result(self, result: Dict[str, Any]) -> Dict[str, Any]:  
        self._emit_event_if_needed(result)  
        self._write_audit_if_needed(result)  
        self._apply_workflow_patch_if_needed(result)  
        return result  
  
  
# ================================================================  
# FILE: platform_core/controllers/session_controller.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict, Optional  
  
  
class SessionController(BaseController):  
    controller_name = "session_controller"  
  
    def open_session(self, user_context: Dict[str, Any]) -> Dict[str, Any]:  
        """  
        Bootstraps a session. This is intentionally light-touch.  
        """  
        registry_service = self._get_service("registry_service")  
  
        actor_id = user_context["actor_id"]  
        actor_role = user_context["actor_role"]  
  
        session_id = f"sess_{actor_id}"  
  
        data = {  
            "session_id": session_id,  
            "available_projects": [],  
            "resume_candidates": [],  
            "default_runtime_context": {  
                "session_id": session_id,  
                "active_role": actor_role,  
                "active_domain": user_context.get("preferred_domain", "generic"),  
                "workflow_mode": "default",  
                "stage_context": {"active_stage": "session_bootstrap"},  
                "flags": {},  
                "current_refs": {},  
                "completed_stages": [],  
                "active_review_exists": False,  
                "unresolved_severe_breach": False,  
                "stale_state_detected": False,  
            },  
        }  
  
        result = self._build_response(  
            status="success",  
            message="Session opened successfully.",  
            controller_name=self.controller_name,  
            action_name="open_session",  
            data=data,  
            references={"session_id": session_id},  
            workflow_patch={"session_id": session_id},  
            agent_hint={  
                "reasoning_summary": "Session established. Runtime stack can now be resolved.",  
                "recommended_next_action": "resolve_runtime_stack",  
                "requires_human_review": False,  
                "suggested_followup_functions": ["resolve_runtime_stack"],  
                "safe_to_continue": True,  
            },  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "session_opened",  
            },  
        )  
        return self._finalize_result(result)  
  
    def resume_session(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        session_id: str,  
        actor: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "resume_session")  
  
        result = self._build_response(  
            status="success",  
            message="Session resumed successfully.",  
            controller_name=self.controller_name,  
            action_name="resume_session",  
            data={  
                "session_id": session_id,  
                "actor": actor,  
                "resume_status": "resumed",  
            },  
            references={  
                "session_id": session_id,  
                "run_id": runtime_context.get("run_id"),  
                "project_id": runtime_context.get("project_id"),  
            },  
            runtime_decision=runtime_decision,  
            agent_hint={  
                "reasoning_summary": "Session state has been resumed and prior workflow can continue.",  
                "recommended_next_action": "run_stage",  
                "requires_human_review": False,  
                "suggested_followup_functions": ["get_workflow_state", "run_stage"],  
                "safe_to_continue": True,  
            },  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "session_resumed",  
            },  
        )  
        return self._finalize_result(result)  
  
  
# ================================================================  
# FILE: platform_core/controllers/workflow_controller.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict  
  
  
class WorkflowController(BaseController):  
    controller_name = "workflow_controller"  
  
    def run_stage(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        stage_name: str,  
        payload: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        """  
        Generic stage runner.  
        This method usually delegates to a stage-specific controller  
        or SDK service based on payload/action metadata.  
        """  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_preconditions_passed(runtime_decision)  
  
        result = self._build_response(  
            status="success",  
            message=f"Stage '{stage_name}' is ready for execution.",  
            controller_name=self.controller_name,  
            action_name="run_stage",  
            data={  
                "stage_name": stage_name,  
                "payload_summary": payload,  
            },  
            references={  
                "run_id": runtime_context.get("run_id"),  
                "project_id": runtime_context.get("project_id"),  
            },  
            runtime_decision=runtime_decision,  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "stage_execution_requested",  
            },  
        )  
        return self._finalize_result(result)  
  
    def route_next(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        current_stage: str,  
        context: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        workflow_service = self._get_service("workflow_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "route_next_stage")  
  
        route_result = workflow_service.route_next_stage(  
            run_id=runtime_context["run_id"],  
            current_stage=current_stage,  
            context=context,  
        )  
  
        result = self._build_response(  
            status=route_result.get("status", "success"),  
            message=route_result.get("message", "Next stage routed."),  
            controller_name=self.controller_name,  
            action_name="route_next",  
            data=route_result.get("data", {}),  
            references={  
                "run_id": runtime_context.get("run_id"),  
                "project_id": runtime_context.get("project_id"),  
            },  
            runtime_decision=runtime_decision,  
            workflow_patch=route_result.get("workflow_hint", {}).get("state_patch", {}),  
            agent_hint=route_result.get("agent_hint", {}),  
            audit_hint=route_result.get("audit_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "workflow_routed",  
            },  
        )  
        return self._finalize_result(result)  
  
    def apply_patch(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        state_patch: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        workflow_service = self._get_service("workflow_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "patch_workflow_state")  
  
        service_result = workflow_service.update_workflow_state(  
            run_id=runtime_context["run_id"],  
            state_patch=state_patch,  
        )  
  
        result = self._build_response(  
            status=service_result.get("status", "success"),  
            message=service_result.get("message", "Workflow state updated."),  
            controller_name=self.controller_name,  
            action_name="apply_patch",  
            data=service_result.get("data", {}),  
            references={"run_id": runtime_context["run_id"]},  
            runtime_decision=runtime_decision,  
            agent_hint=service_result.get("agent_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "workflow_state_patched",  
            },  
        )  
        return self._finalize_result(result)  
  
  
# ================================================================  
# FILE: platform_core/controllers/review_controller.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict  
  
  
class ReviewController(BaseController):  
    controller_name = "review_controller"  
  
    def open_review(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        review_id: str,  
        actor: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        hitl_service = self._get_service("hitl_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "get_review")  
  
        review_result = hitl_service.get_review(review_id=review_id)  
  
        result = self._build_response(  
            status=review_result.get("status", "success"),  
            message=review_result.get("message", "Review opened."),  
            controller_name=self.controller_name,  
            action_name="open_review",  
            data=review_result.get("data", {}),  
            references={  
                "review_id": review_id,  
                "run_id": runtime_context.get("run_id"),  
                "project_id": runtime_context.get("project_id"),  
            },  
            runtime_decision=runtime_decision,  
            agent_hint={  
                "reasoning_summary": "Review state has been loaded and the governed workspace can now be rendered.",  
                "recommended_next_action": "get_review_payload",  
                "requires_human_review": True,  
                "suggested_followup_functions": ["get_review_payload"],  
                "safe_to_continue": False,  
            },  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "review_opened",  
            },  
        )  
        return self._finalize_result(result)  
  
    def get_review_payload(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        review_id: str,  
        review_type: str,  
        source_context: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        hitl_service = self._get_service("hitl_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "build_review_payload")  
  
        payload_result = hitl_service.build_review_payload(  
            review_type=review_type,  
            source_context=source_context,  
        )  
  
        result = self._build_response(  
            status=payload_result.get("status", "success"),  
            message=payload_result.get("message", "Review payload built."),  
            controller_name=self.controller_name,  
            action_name="get_review_payload",  
            data=payload_result.get("data", {}),  
            references={  
                "review_id": review_id,  
                "run_id": runtime_context.get("run_id"),  
            },  
            runtime_decision=runtime_decision,  
            agent_hint=payload_result.get("agent_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "review_payload_built",  
            },  
        )  
        return self._finalize_result(result)  
  
    def submit_review_action(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        review_id: str,  
        interaction_payload: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        hitl_service = self._get_service("hitl_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "validate_review_action")  
  
        validation = hitl_service.validate_action(  
            review_id=review_id,  
            interaction_payload=interaction_payload,  
        )  
  
        if not validation.get("is_valid", False):  
            result = self._build_response(  
                status="invalid_input",  
                message="Review action is invalid.",  
                controller_name=self.controller_name,  
                action_name="submit_review_action",  
                data=validation.get("data", {}),  
                errors=validation.get("errors", []),  
                references={"review_id": review_id, "run_id": runtime_context.get("run_id")},  
                runtime_decision=runtime_decision,  
                agent_hint=validation.get("agent_hint", {}),  
                observability_hint={  
                    "should_write_event": True,  
                    "event_type": "review_action_rejected",  
                },  
            )  
            return self._finalize_result(result)  
  
        action = interaction_payload["action"]  
        decision_result = hitl_service.capture_decision(  
            review_id=review_id,  
            action=action,  
            interaction_payload=interaction_payload,  
        )  
  
        result = self._build_response(  
            status=decision_result.get("status", "success"),  
            message=decision_result.get("message", "Review action submitted."),  
            controller_name=self.controller_name,  
            action_name="submit_review_action",  
            data=decision_result.get("data", {}),  
            references={  
                "review_id": review_id,  
                "run_id": runtime_context.get("run_id"),  
                **decision_result.get("references", {}),  
            },  
            runtime_decision=runtime_decision,  
            workflow_patch=decision_result.get("workflow_hint", {}).get("state_patch", {}),  
            agent_hint=decision_result.get("agent_hint", {}),  
            audit_hint=decision_result.get("audit_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "review_action_submitted",  
            },  
        )  
        return self._finalize_result(result)  
  
  
# ================================================================  
# FILE: platform_core/controllers/dataprep_controller.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict  
  
  
class DataPrepController(BaseController):  
    controller_name = "dataprep_controller"  
  
    def prepare_dataset(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        request: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        dataprep_service = self._get_service("dataprep_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_preconditions_passed(runtime_decision)  
        self._ensure_tool_allowed(runtime_decision, "execute_dataprep_request")  
  
        prep_result = dataprep_service.execute_request(request=request)  
  
        result = self._build_response(  
            status=prep_result.get("status", "success"),  
            message=prep_result.get("message", "Dataprep executed."),  
            controller_name=self.controller_name,  
            action_name="prepare_dataset",  
            data=prep_result.get("data", {}),  
            warnings=prep_result.get("warnings", []),  
            errors=prep_result.get("errors", []),  
            references={  
                "run_id": runtime_context.get("run_id"),  
                "project_id": runtime_context.get("project_id"),  
                **prep_result.get("references", {}),  
            },  
            runtime_decision=runtime_decision,  
            workflow_patch=prep_result.get("workflow_hint", {}).get("state_patch", {}),  
            agent_hint=prep_result.get("agent_hint", {}),  
            audit_hint=prep_result.get("audit_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "dataset_prepared",  
            },  
        )  
        return self._finalize_result(result)  
  
    def run_data_readiness_checks(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        dataset_ref: Dict[str, Any],  
        check_pack: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        dataprep_service = self._get_service("spark_dataprep_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "run_prep_quality_checks_spark")  
  
        check_result = dataprep_service.run_prep_quality_checks_spark(  
            dataset_ref=dataset_ref,  
            check_pack=check_pack,  
        )  
  
        result = self._build_response(  
            status=check_result.get("status", "success"),  
            message=check_result.get("message", "Preparation quality checks completed."),  
            controller_name=self.controller_name,  
            action_name="run_data_readiness_checks",  
            data=check_result.get("data", {}),  
            warnings=check_result.get("warnings", []),  
            references={  
                "run_id": runtime_context.get("run_id"),  
                **check_result.get("references", {}),  
            },  
            runtime_decision=runtime_decision,  
            agent_hint=check_result.get("agent_hint", {}),  
            audit_hint=check_result.get("audit_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "data_readiness_checked",  
            },  
        )  
        return self._finalize_result(result)  
  
    def register_dataset_snapshot(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        dataset_payload: Dict[str, Any],  
        snapshot_payload: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        dataset_service = self._get_service("dataset_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "register_dataset")  
  
        reg_result = dataset_service.register_dataset(dataset_payload=dataset_payload)  
        dataset_id = reg_result["data"]["dataset_id"]  
  
        snap_result = dataset_service.create_snapshot(  
            dataset_id=dataset_id,  
            snapshot_payload=snapshot_payload,  
        )  
  
        result = self._build_response(  
            status="success",  
            message="Dataset and snapshot registered successfully.",  
            controller_name=self.controller_name,  
            action_name="register_dataset_snapshot",  
            data={  
                "dataset": reg_result.get("data", {}),  
                "snapshot": snap_result.get("data", {}),  
            },  
            references={  
                "run_id": runtime_context.get("run_id"),  
                "dataset_id": dataset_id,  
                "dataset_snapshot_id": snap_result["data"]["dataset_snapshot_id"],  
            },  
            runtime_decision=runtime_decision,  
            workflow_patch={  
                "dataset_id": dataset_id,  
                "dataset_snapshot_id": snap_result["data"]["dataset_snapshot_id"],  
            },  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "dataset_snapshot_registered",  
            },  
        )  
        return self._finalize_result(result)  
  
  
# ================================================================  
# FILE: platform_core/controllers/validation_controller.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict, List  
  
  
class ValidationController(BaseController):  
    controller_name = "validation_controller"  
  
    def create_validation_run(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        model_ref: Dict[str, Any],  
        scope_config: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        validation_service = self._get_service("validation_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "create_validation_scope")  
  
        service_result = validation_service.create_validation_scope(  
            project_id=runtime_context["project_id"],  
            model_ref=model_ref,  
            scope_config=scope_config,  
        )  
  
        result = self._build_response(  
            status=service_result.get("status", "success"),  
            message=service_result.get("message", "Validation scope created."),  
            controller_name=self.controller_name,  
            action_name="create_validation_run",  
            data=service_result.get("data", {}),  
            references={  
                "run_id": runtime_context.get("run_id"),  
                "project_id": runtime_context.get("project_id"),  
                **service_result.get("references", {}),  
            },  
            runtime_decision=runtime_decision,  
            workflow_patch=service_result.get("workflow_hint", {}).get("state_patch", {}),  
            agent_hint=service_result.get("agent_hint", {}),  
            audit_hint=service_result.get("audit_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "validation_run_created",  
            },  
        )  
        return self._finalize_result(result)  
  
    def intake_evidence(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        validation_run_id: str,  
        evidence_refs: List[Dict[str, Any]],  
    ) -> Dict[str, Any]:  
        validation_service = self._get_service("validation_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "intake_validation_evidence")  
  
        service_result = validation_service.intake_evidence(  
            validation_run_id=validation_run_id,  
            evidence_refs=evidence_refs,  
        )  
  
        result = self._build_response(  
            status=service_result.get("status", "success"),  
            message=service_result.get("message", "Validation evidence ingested."),  
            controller_name=self.controller_name,  
            action_name="intake_evidence",  
            data=service_result.get("data", {}),  
            references={  
                "run_id": runtime_context.get("run_id"),  
                "validation_run_id": validation_run_id,  
            },  
            runtime_decision=runtime_decision,  
            agent_hint=service_result.get("agent_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "validation_evidence_ingested",  
            },  
        )  
        return self._finalize_result(result)  
  
    def finalize_conclusion(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        validation_run_id: str,  
        conclusion_payload: Dict[str, Any],  
        actor: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        validation_service = self._get_service("validation_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_preconditions_passed(runtime_decision)  
        self._ensure_tool_allowed(runtime_decision, "finalize_validation_conclusion")  
  
        service_result = validation_service.finalize_conclusion(  
            validation_run_id=validation_run_id,  
            conclusion_payload=conclusion_payload,  
            actor=actor,  
        )  
  
        result = self._build_response(  
            status=service_result.get("status", "finalized"),  
            message=service_result.get("message", "Validation conclusion finalized."),  
            controller_name=self.controller_name,  
            action_name="finalize_conclusion",  
            data=service_result.get("data", {}),  
            references={  
                "run_id": runtime_context.get("run_id"),  
                "validation_run_id": validation_run_id,  
                **service_result.get("references", {}),  
            },  
            runtime_decision=runtime_decision,  
            workflow_patch=service_result.get("workflow_hint", {}).get("state_patch", {}),  
            agent_hint=service_result.get("agent_hint", {}),  
            audit_hint={  
                "should_write_audit": True,  
                "audit_type": "validation_conclusion",  
            },  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "validation_conclusion_finalized",  
            },  
        )  
        return self._finalize_result(result)  
  
  
# ================================================================  
# FILE: platform_core/controllers/monitoring_controller.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict  
  
  
class MonitoringController(BaseController):  
    controller_name = "monitoring_controller"  
  
    def ingest_snapshot(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        snapshot_payload: Dict[str, Any],  
        template_ref: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        monitoring_service = self._get_service("monitoring_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "ingest_monitoring_snapshot")  
  
        service_result = monitoring_service.ingest_snapshot(  
            snapshot_payload=snapshot_payload,  
            template_ref=template_ref,  
        )  
  
        result = self._build_response(  
            status=service_result.get("status", "success"),  
            message=service_result.get("message", "Monitoring snapshot ingested."),  
            controller_name=self.controller_name,  
            action_name="ingest_snapshot",  
            data=service_result.get("data", {}),  
            references={  
                "run_id": runtime_context.get("run_id"),  
                **service_result.get("references", {}),  
            },  
            runtime_decision=runtime_decision,  
            agent_hint=service_result.get("agent_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "monitoring_snapshot_ingested",  
            },  
        )  
        return self._finalize_result(result)  
  
    def refresh_kpis(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        model_id: str,  
        snapshot_ref: Dict[str, Any],  
        metric_spec: Dict[str, Any],  
        threshold_pack: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        monitoring_service = self._get_service("monitoring_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "compute_monitoring_metrics")  
  
        metric_result = monitoring_service.compute_monitoring_metrics(  
            model_id=model_id,  
            snapshot_ref=snapshot_ref,  
            metric_spec=metric_spec,  
        )  
        threshold_result = monitoring_service.evaluate_monitoring_thresholds(  
            metric_summary=metric_result.get("data", {}),  
            threshold_pack=threshold_pack,  
        )  
  
        result = self._build_response(  
            status="success",  
            message="Monitoring KPIs refreshed successfully.",  
            controller_name=self.controller_name,  
            action_name="refresh_kpis",  
            data={  
                "metric_result": metric_result.get("data", {}),  
                "threshold_result": threshold_result.get("data", {}),  
            },  
            references={  
                "run_id": runtime_context.get("run_id"),  
                "model_id": model_id,  
            },  
            runtime_decision=runtime_decision,  
            agent_hint=threshold_result.get("agent_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "monitoring_kpis_refreshed",  
            },  
        )  
        return self._finalize_result(result)  
  
    def open_breach_review(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        review_payload: Dict[str, Any],  
        actor_context: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        hitl_service = self._get_service("hitl_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "create_review")  
  
        service_result = hitl_service.create_review(  
            review_type="monitoring_breach",  
            review_payload=review_payload,  
            actor_context=actor_context,  
        )  
  
        result = self._build_response(  
            status=service_result.get("status", "pending_human_review"),  
            message=service_result.get("message", "Monitoring breach review created."),  
            controller_name=self.controller_name,  
            action_name="open_breach_review",  
            data=service_result.get("data", {}),  
            references={  
                "run_id": runtime_context.get("run_id"),  
                **service_result.get("references", {}),  
            },  
            runtime_decision=runtime_decision,  
            workflow_patch=service_result.get("workflow_hint", {}).get("state_patch", {}),  
            agent_hint=service_result.get("agent_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "monitoring_breach_review_created",  
            },  
        )  
        return self._finalize_result(result)  
  
    def build_annual_review_pack(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        model_id: str,  
        period_spec: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        monitoring_service = self._get_service("monitoring_service")  
  
        runtime_decision = self._resolve_runtime(runtime_context)  
        self._ensure_tool_allowed(runtime_decision, "build_annual_review_pack")  
  
        service_result = monitoring_service.build_annual_review_pack(  
            model_id=model_id,  
            period_spec=period_spec,  
        )  
  
        result = self._build_response(  
            status=service_result.get("status", "success"),  
            message=service_result.get("message", "Annual review pack built."),  
            controller_name=self.controller_name,  
            action_name="build_annual_review_pack",  
            data=service_result.get("data", {}),  
            references={  
                "run_id": runtime_context.get("run_id"),  
                "model_id": model_id,  
                **service_result.get("references", {}),  
            },  
            runtime_decision=runtime_decision,  
            agent_hint=service_result.get("agent_hint", {}),  
            observability_hint={  
                "should_write_event": True,  
                "event_type": "annual_review_pack_built",  
            },  
        )  
        return self._finalize_result(result)  
  
  
# ================================================================  
# FILE: platform_core/controllers/controller_factory.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict  
  
# Assumes the controller classes are importable in real project layout  
# from .session_controller import SessionController  
# from .workflow_controller import WorkflowController  
# from .review_controller import ReviewController  
# from .dataprep_controller import DataPrepController  
# from .validation_controller import ValidationController  
# from .monitoring_controller import MonitoringController  
  
  
class ControllerFactory:  
    """  
    Creates controller instances with shared dependencies.  
    """  
  
    def __init__(  
        self,  
        *,  
        runtime_resolver: Any,  
        service_registry: Dict[str, Any],  
    ) -> None:  
        self.runtime_resolver = runtime_resolver  
        self.service_registry = service_registry  
  
    def build_common_kwargs(self) -> Dict[str, Any]:  
        return {  
            "runtime_resolver": self.runtime_resolver,  
            "service_registry": self.service_registry,  
            "observability_service": self.service_registry.get("observability_service"),  
            "audit_service": self.service_registry.get("audit_service"),  
            "workflow_service": self.service_registry.get("workflow_service"),  
        }  
  
    def create_session_controller(self) -> "SessionController":  
        return SessionController(**self.build_common_kwargs())  
  
    def create_workflow_controller(self) -> "WorkflowController":  
        return WorkflowController(**self.build_common_kwargs())  
  
    def create_review_controller(self) -> "ReviewController":  
        return ReviewController(**self.build_common_kwargs())  
  
    def create_dataprep_controller(self) -> "DataPrepController":  
        return DataPrepController(**self.build_common_kwargs())  
  
    def create_validation_controller(self) -> "ValidationController":  
        return ValidationController(**self.build_common_kwargs())  
  
    def create_monitoring_controller(self) -> "MonitoringController":  
        return MonitoringController(**self.build_common_kwargs())  
  
  
# ================================================================  
# OPTIONAL EXAMPLE: WIRING SKETCH  
# ================================================================  
  
if __name__ == "__main__":  
    # Example only. Replace stubs with actual implementations.  
    class DummyService:  
        def route_next_stage(self, **kwargs):  
            return {"status": "success", "message": "Routed.", "data": {"recommended_next_stage": "next_stage"}}  
  
        def update_workflow_state(self, **kwargs):  
            return {"status": "success", "message": "Patched.", "data": {}}  
  
        def get_review(self, **kwargs):  
            return {"status": "success", "message": "Review loaded.", "data": {"review_status": "pending_review"}}  
  
        def build_review_payload(self, **kwargs):  
            return {"status": "success", "message": "Payload built.", "data": {"payload": {}}}  
  
        def validate_action(self, **kwargs):  
            return {"status": "success", "is_valid": True, "data": {}}  
  
        def capture_decision(self, **kwargs):  
            return {  
                "status": "finalized",  
                "message": "Decision captured.",  
                "data": {"decision_record": {}},  
                "workflow_hint": {"state_patch": {"review_completed": True}},  
                "audit_hint": {"should_write_audit": True, "audit_type": "review_decision"},  
                "references": {"decision_id": "dec_001"},  
            }  
  
        def execute_request(self, **kwargs):  
            return {  
                "status": "success",  
                "message": "Prepared.",  
                "data": {"dataset_id": "ds_001", "dataset_snapshot_id": "snap_001"},  
                "workflow_hint": {"state_patch": {"dataset_snapshot_id": "snap_001"}},  
                "references": {"dataset_snapshot_id": "snap_001"},  
            }  
  
        def run_prep_quality_checks_spark(self, **kwargs):  
            return {  
                "status": "success",  
                "message": "Checks passed.",  
                "data": {"prep_quality_summary": {"overall_status": "pass"}},  
            }  
  
        def register_dataset(self, **kwargs):  
            return {"status": "success", "data": {"dataset_id": "ds_001"}}  
  
        def create_snapshot(self, **kwargs):  
            return {"status": "success", "data": {"dataset_snapshot_id": "snap_001"}}  
  
        def create_validation_scope(self, **kwargs):  
            return {  
                "status": "success",  
                "message": "Validation scope created.",  
                "data": {"validation_run_id": "val_001"},  
                "references": {"validation_run_id": "val_001"},  
                "workflow_hint": {"state_patch": {"validation_run_id": "val_001"}},  
            }  
  
        def intake_evidence(self, **kwargs):  
            return {"status": "success", "message": "Evidence ingested.", "data": {}}  
  
        def finalize_conclusion(self, **kwargs):  
            return {  
                "status": "finalized",  
                "message": "Validation conclusion finalized.",  
                "data": {"conclusion_id": "vcon_001"},  
                "references": {"conclusion_id": "vcon_001"},  
                "workflow_hint": {"state_patch": {"validation_conclusion_id": "vcon_001"}},  
            }  
  
        def ingest_snapshot(self, **kwargs):  
            return {  
                "status": "success",  
                "message": "Snapshot ingested.",  
                "data": {"snapshot_ref": {"snapshot_id": "msnap_001"}},  
                "references": {"snapshot_id": "msnap_001"},  
            }  
  
        def compute_monitoring_metrics(self, **kwargs):  
            return {"status": "success", "data": {"metric_summary": {"psi": 0.08}}}  
  
        def evaluate_monitoring_thresholds(self, **kwargs):  
            return {"status": "success", "data": {"breach_summary": {"breach_count": 0}}}  
  
        def create_review(self, **kwargs):  
            return {  
                "status": "pending_human_review",  
                "message": "Review created.",  
                "data": {"review_id": "rev_001"},  
                "references": {"review_id": "rev_001"},  
                "workflow_hint": {"state_patch": {"active_review_id": "rev_001"}},  
                "agent_hint": {"requires_human_review": True},  
            }  
  
        def build_annual_review_pack(self, **kwargs):  
            return {  
                "status": "success",  
                "message": "Annual review pack built.",  
                "data": {"annual_review_pack_ref": "arp_001"},  
                "references": {"annual_review_pack_ref": "arp_001"},  
            }  
  
        def write_event(self, **kwargs):  
            return None  
  
        def write_audit_record(self, **kwargs):  
            return None  
  
    class DummyRuntimeResolver:  
        def resolve(self, runtime_context):  
            return {  
                "stage_name": runtime_context["stage_context"]["active_stage"],  
                "actor_role": runtime_context["active_role"],  
                "preconditions_passed": True,  
                "missing_preconditions": [],  
                "allowed_tools": [  
                    "resume_session",  
                    "route_next_stage",  
                    "patch_workflow_state",  
                    "get_review",  
                    "build_review_payload",  
                    "validate_review_action",  
                    "execute_dataprep_request",  
                    "run_prep_quality_checks_spark",  
                    "register_dataset",  
                    "create_validation_scope",  
                    "intake_validation_evidence",  
                    "finalize_validation_conclusion",  
                    "ingest_monitoring_snapshot",  
                    "compute_monitoring_metrics",  
                    "create_review",  
                    "build_annual_review_pack",  
                ],  
            }  
  
    service_registry = {  
        "registry_service": DummyService(),  
        "workflow_service": DummyService(),  
        "hitl_service": DummyService(),  
        "dataprep_service": DummyService(),  
        "spark_dataprep_service": DummyService(),  
        "dataset_service": DummyService(),  
        "validation_service": DummyService(),  
        "monitoring_service": DummyService(),  
        "observability_service": DummyService(),  
        "audit_service": DummyService(),  
    }  
  
    runtime_resolver = DummyRuntimeResolver()  
    factory = ControllerFactory(  
        runtime_resolver=runtime_resolver,  
        service_registry=service_registry,  
    )  
  
    review_controller = factory.create_review_controller()  
    response = review_controller.submit_review_action(  
        runtime_context={  
            "project_id": "proj_001",  
            "run_id": "run_001",  
            "active_role": "governance",  
            "stage_context": {"active_stage": "coarse_classing_review"},  
        },  
        review_id="rev_001",  
        interaction_payload={  
            "action": "approve",  
            "actor": {"actor_id": "u001", "actor_role": "governance"},  
            "user_comment": "Looks acceptable.",  
        },  
    )  
    print(response)  
