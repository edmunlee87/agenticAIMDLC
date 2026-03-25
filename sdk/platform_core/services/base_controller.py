"""BaseController: foundation for all platform controllers.

Controllers are thin orchestration layers that:
1. Receive interaction_payload from bridges
2. Invoke the RuntimeResolver to get resolved_stack
3. Enforce tool allowlist and preconditions
4. Delegate to SDK services
5. Return standard_response_envelope with audit_ref and event_ref

Design rules:
- No business logic in controllers; all logic in SDK services.
- Controllers always return StandardResponseEnvelope, never raw BaseResult.
- All controller actions are observable (emit event) and auditable if material.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..schemas.base_result import BaseResult
from ..schemas.common_fragments import ActorRecord, GovernanceSummary
from ..schemas.payload_models import (
    InteractionPayload,
    ResolvedStack,
    RuntimeContext,
    StandardResponseEnvelope,
)
from ..schemas.utilities import IDFactory, TimeProvider


class BaseController(ABC):
    """Root base for all platform controllers.

    Provides runtime resolution, tool allowance checking, precondition enforcement,
    envelope building, and hook helpers for event emission and audit writing.

    Args:
        controller_name: Name of this controller.
        resolver: RuntimeResolver instance for resolving runtime context.
        dependencies: DependencyContainer with registered services.
        logger: Optional logger override.
    """

    def __init__(
        self,
        controller_name: str,
        resolver: Optional[Any] = None,
        dependencies: Optional[Any] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._controller_name = controller_name
        self._resolver = resolver
        self._dependencies = dependencies
        self._logger = logger or logging.getLogger(f"platform.controller.{controller_name}")

    def _resolve_runtime(self, context: RuntimeContext) -> Optional[ResolvedStack]:
        """Resolve runtime context to get the effective stack.

        Args:
            context: The runtime context to resolve.

        Returns:
            ResolvedStack if resolver is available, None otherwise.
        """
        if self._resolver is None:
            self._logger.warning(
                "RuntimeResolver not configured for %s; skipping resolution",
                self._controller_name,
            )
            return None
        try:
            return self._resolver.resolve(context)
        except Exception as exc:
            self._logger.error(
                "RuntimeResolver failed for %s: %s", self._controller_name, exc
            )
            return None

    def _ensure_tool_allowed(
        self,
        tool_name: str,
        resolved_stack: Optional[ResolvedStack],
        function_name: str,
    ) -> Optional[StandardResponseEnvelope]:
        """Check if a tool is in the SDK allowlist.

        Returns a blocked envelope if the tool is not allowed; None if permitted.

        Args:
            tool_name: The tool/method being called.
            resolved_stack: The resolved stack to check against.
            function_name: Calling function name for envelope metadata.

        Returns:
            Blocked StandardResponseEnvelope if denied, None if allowed.
        """
        if resolved_stack and tool_name not in resolved_stack.sdk_allowlist:
            if resolved_stack.blocked_tools and tool_name in resolved_stack.blocked_tools:
                return self._build_blocked_envelope(
                    function_name=function_name,
                    run_id="unknown",
                    reason=f"Tool '{tool_name}' is explicitly blocked for this stage/role context.",
                )
        return None

    def _ensure_preconditions_passed(
        self,
        precondition_result: Optional[BaseResult],
        function_name: str,
        run_id: str,
    ) -> Optional[StandardResponseEnvelope]:
        """Check precondition result and return blocked envelope if failed.

        Args:
            precondition_result: Result from precondition check (None = passed).
            function_name: Calling function name.
            run_id: Active run identifier.

        Returns:
            Blocked StandardResponseEnvelope if preconditions failed, None if passed.
        """
        if precondition_result and not precondition_result.is_success:
            return self._build_blocked_envelope(
                function_name=function_name,
                run_id=run_id,
                reason=precondition_result.message,
            )
        return None

    def _build_response(
        self,
        result: BaseResult,
        run_id: str,
        stage_name: Optional[str] = None,
        actor: Optional[ActorRecord] = None,
        audit_ref: Optional[str] = None,
        event_ref: Optional[str] = None,
        governance_summary: Optional[GovernanceSummary] = None,
        review_payload: Optional[Any] = None,
        workflow_state_patch: Optional[Dict[str, Any]] = None,
        next_stage: Optional[str] = None,
    ) -> StandardResponseEnvelope:
        """Build a StandardResponseEnvelope from a BaseResult.

        Args:
            result: The SDK result to wrap.
            run_id: Active run identifier.
            stage_name: Current stage name.
            actor: Actor for this response.
            audit_ref: Audit record ID if created.
            event_ref: Observability event ID if emitted.
            governance_summary: Policy check summary.
            review_payload: Embedded review payload if a review was created.
            workflow_state_patch: Workflow state changes to apply.
            next_stage: Recommended next stage.

        Returns:
            StandardResponseEnvelope.
        """
        return StandardResponseEnvelope(
            envelope_id=IDFactory.envelope_id(),
            status=result.status,
            message=result.message,
            sdk_name=self._controller_name,
            function_name=result.function_name,
            data=result.data,
            warnings=result.warnings,
            errors=result.errors,
            artifacts_created=result.artifacts_created,
            references=result.references,
            agent_hint=result.agent_hint,
            workflow_hint=result.workflow_hint,
            audit_hint=result.audit_hint,
            observability_hint=result.observability_hint,
            run_id=run_id,
            timestamp=TimeProvider.now_iso(),
            stage_name=stage_name,
            actor=actor,
            current_stage=stage_name,
            next_stage=next_stage,
            review_created=review_payload is not None,
            review_id=review_payload.review_id if review_payload else None,
            review_payload=review_payload,
            workflow_state_patch=workflow_state_patch,
            audit_ref=audit_ref,
            event_ref=event_ref,
            governance_summary=governance_summary,
        )

    def _build_blocked_envelope(
        self,
        function_name: str,
        run_id: str,
        reason: str,
        stage_name: Optional[str] = None,
        actor: Optional[ActorRecord] = None,
    ) -> StandardResponseEnvelope:
        """Build a blocked StandardResponseEnvelope.

        Args:
            function_name: Calling function name.
            run_id: Active run identifier.
            reason: Blocking reason description.
            stage_name: Current stage name.
            actor: Actor for this response.

        Returns:
            Blocked StandardResponseEnvelope.
        """
        return StandardResponseEnvelope(
            envelope_id=IDFactory.envelope_id(),
            status="blocked",
            message=f"Operation blocked: {reason}",
            sdk_name=self._controller_name,
            function_name=function_name,
            data=None,
            warnings=[],
            errors=[reason],
            artifacts_created=[],
            references={},
            agent_hint=f"Resolve blocking condition before proceeding: {reason}",
            run_id=run_id,
            timestamp=TimeProvider.now_iso(),
            stage_name=stage_name,
            actor=actor,
            governance_summary=GovernanceSummary(
                policy_check_result="blocked",
                blocking_reasons=[reason],
            ),
        )

    def _emit_event_if_needed(
        self,
        event_type: str,
        run_id: str,
        stage_name: str,
        actor: Optional[ActorRecord],
        payload: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Emit an observability event if the observability service is available.

        Args:
            event_type: Event type identifier.
            run_id: Active run identifier.
            stage_name: Current stage name.
            actor: Actor emitting the event.
            payload: Event-specific payload.

        Returns:
            event_id if emitted, None otherwise.
        """
        if self._dependencies is None or not self._dependencies.has("observability"):
            return None
        try:
            obs_service = self._dependencies.get("observability")
            result = obs_service.write_event(
                event_type=event_type,
                run_id=run_id,
                stage_name=stage_name,
                actor=actor,
                payload=payload or {},
            )
            return result.references.get("event_id")
        except Exception as exc:
            self._logger.warning("Failed to emit observability event: %s", exc)
            return None

    def _write_audit_if_needed(
        self,
        audit_type: str,
        run_id: str,
        stage_name: str,
        actor: Optional[ActorRecord],
        payload: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Write an audit record if the audit service is available.

        Args:
            audit_type: Audit record type (decision, approval, etc.).
            run_id: Active run identifier.
            stage_name: Current stage name.
            actor: Actor creating the audit record.
            payload: Audit-specific payload.

        Returns:
            audit_id if written, None otherwise.
        """
        if self._dependencies is None or not self._dependencies.has("audit"):
            return None
        try:
            audit_service = self._dependencies.get("audit")
            result = audit_service.write_audit_record(
                audit_type=audit_type,
                run_id=run_id,
                stage_name=stage_name,
                actor=actor,
                payload=payload or {},
            )
            return result.references.get("audit_id")
        except Exception as exc:
            self._logger.warning("Failed to write audit record: %s", exc)
            return None

    def _apply_workflow_patch_if_needed(
        self,
        run_id: str,
        patch: Dict[str, Any],
    ) -> None:
        """Apply a workflow state patch if the workflow service is available.

        Args:
            run_id: Active run identifier.
            patch: Partial workflow state update to apply.
        """
        if self._dependencies is None or not self._dependencies.has("workflow"):
            return
        try:
            wf_service = self._dependencies.get("workflow")
            wf_service.apply_state_patch(run_id=run_id, patch=patch)
        except Exception as exc:
            self._logger.warning("Failed to apply workflow state patch: %s", exc)
