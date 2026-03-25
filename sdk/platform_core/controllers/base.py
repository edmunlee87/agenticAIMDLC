"""BaseController: foundation for all platform controllers.

Controllers are thin orchestration layers that:
1. Receive :class:`InteractionPayload` from bridges.
2. Invoke the :class:`RuntimeResolver` to get :class:`ResolvedStack`.
3. Enforce tool allowlist and preconditions.
4. Delegate to SDK services.
5. Return :class:`StandardResponseEnvelope` with audit_ref and event_ref.

Design rules:
- No business logic in controllers; all logic lives in SDK services.
- Controllers always return StandardResponseEnvelope, never raw BaseResult.
- All material controller actions are observable and auditable.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from sdk.platform_core.runtime.resolvers.runtime_resolver import (
    ResolvedStack,
    RuntimeResolver,
)
from sdk.platform_core.schemas.common_fragments import ActorRecord, GovernanceSummary
from sdk.platform_core.schemas.payload_models import (
    InteractionPayload,
    StandardResponseEnvelope,
)
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider


class BaseController(ABC):
    """Root base class for all MDLC controllers.

    Args:
        controller_name: Logical name for this controller (used in logging).
        resolver: Optional pre-built :class:`RuntimeResolver`.
        dependencies: Optional :class:`DependencyContainer` with registered services.
        logger: Optional logger override.
    """

    def __init__(
        self,
        controller_name: str,
        resolver: Optional[RuntimeResolver] = None,
        dependencies: Optional[Any] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._controller_name = controller_name
        self._resolver = resolver
        self._dependencies = dependencies
        self._logger = logger or logging.getLogger(
            f"platform.controller.{controller_name}"
        )

    @abstractmethod
    def handle(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        """Process an interaction payload and return a response envelope.

        Implementations must:
        1. Resolve runtime context (stage/role → resolved_stack).
        2. Enforce tool allowlist.
        3. Execute the requested operation via service calls.
        4. Write an audit record for any material action.
        5. Return a StandardResponseEnvelope with populated audit_ref and event_ref.

        Args:
            payload: Structured input from a UI or agent.

        Returns:
            :class:`StandardResponseEnvelope` -- never raises unchecked exceptions.
        """

    # ------------------------------------------------------------------
    # Runtime resolution helpers
    # ------------------------------------------------------------------

    def _resolve_stack(
        self,
        stage_name: str,
        actor_role: str,
        runtime_facts: Optional[Dict[str, Any]] = None,
    ) -> Optional[ResolvedStack]:
        """Invoke the RuntimeResolver for the given stage+role.

        Args:
            stage_name: Target stage.
            actor_role: Actor's role string.
            runtime_facts: Optional runtime context flags.

        Returns:
            :class:`ResolvedStack` or None if resolver is unavailable.
        """
        if self._resolver is None:
            self._logger.warning(
                "RuntimeResolver not configured for %s; skipping resolution.",
                self._controller_name,
            )
            return None
        try:
            return self._resolver.resolve(
                stage_name=stage_name,
                actor_role=actor_role,
                runtime_facts=runtime_facts,
            )
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
        run_id: str,
        stage_name: Optional[str] = None,
        actor: Optional[ActorRecord] = None,
    ) -> Optional[StandardResponseEnvelope]:
        """Return a blocked envelope if the tool is not permitted.

        Args:
            tool_name: Tool/method name being invoked.
            resolved_stack: Resolved stack to check.
            function_name: Calling function name for envelope metadata.
            run_id: Active run identifier.
            stage_name: Current stage name.
            actor: Actor for this response.

        Returns:
            Blocked :class:`StandardResponseEnvelope` if denied; None if allowed.
        """
        if resolved_stack is None:
            return None
        if tool_name in resolved_stack.blocked_tools:
            return self._build_blocked_envelope(
                function_name=function_name,
                run_id=run_id,
                reason=f"Tool '{tool_name}' is explicitly blocked for this stage/role.",
                stage_name=stage_name,
                actor=actor,
            )
        return None

    # ------------------------------------------------------------------
    # Envelope builders
    # ------------------------------------------------------------------

    def _build_response(
        self,
        run_id: str,
        function_name: str,
        *,
        status: str = "success",
        message: str = "",
        data: Optional[Dict[str, Any]] = None,
        stage_name: Optional[str] = None,
        actor: Optional[ActorRecord] = None,
        audit_ref: Optional[str] = None,
        event_ref: Optional[str] = None,
        governance_summary: Optional[GovernanceSummary] = None,
        next_stage: Optional[str] = None,
        review_created: bool = False,
        review_id: Optional[str] = None,
        warnings: Optional[List[str]] = None,
        errors: Optional[List[str]] = None,
    ) -> StandardResponseEnvelope:
        """Build a :class:`StandardResponseEnvelope`.

        Args:
            run_id: Active run identifier.
            function_name: Calling function name.
            status: Response status string.
            message: Human-readable message.
            data: Payload data.
            stage_name: Current stage name.
            actor: Actor for this response.
            audit_ref: Audit record ID if created.
            event_ref: Observability event ID if emitted.
            governance_summary: Policy check summary.
            next_stage: Recommended next stage.
            review_created: Whether a review was created.
            review_id: ID of created review.
            warnings: Warning strings.
            errors: Error strings.

        Returns:
            :class:`StandardResponseEnvelope`.
        """
        return StandardResponseEnvelope(
            envelope_id=IDFactory.envelope_id(),
            status=status,
            message=message,
            sdk_name=self._controller_name,
            function_name=function_name,
            data=data,
            warnings=warnings or [],
            errors=errors or [],
            artifacts_created=[],
            references={},
            run_id=run_id,
            timestamp=TimeProvider.now_iso(),
            stage_name=stage_name,
            actor=actor,
            current_stage=stage_name,
            next_stage=next_stage,
            review_created=review_created,
            review_id=review_id,
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
        """Build a blocked :class:`StandardResponseEnvelope`.

        Args:
            function_name: Calling function name.
            run_id: Active run identifier.
            reason: Blocking reason description.
            stage_name: Current stage name.
            actor: Actor for this response.

        Returns:
            :class:`StandardResponseEnvelope` with status ``"blocked"``.
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
            agent_hint=f"Resolve blocking condition before retrying: {reason}",
            run_id=run_id,
            timestamp=TimeProvider.now_iso(),
            stage_name=stage_name,
            actor=actor,
            governance_summary=GovernanceSummary(
                policy_check_result="blocked",
                blocking_reasons=[reason],
            ),
        )

    def _build_error_envelope(
        self,
        function_name: str,
        run_id: str,
        error_message: str,
        stage_name: Optional[str] = None,
        actor: Optional[ActorRecord] = None,
    ) -> StandardResponseEnvelope:
        """Build an error :class:`StandardResponseEnvelope`.

        Args:
            function_name: Calling function name.
            run_id: Active run identifier.
            error_message: Error description.
            stage_name: Current stage name.
            actor: Actor for this response.

        Returns:
            :class:`StandardResponseEnvelope` with status ``"error"``.
        """
        return StandardResponseEnvelope(
            envelope_id=IDFactory.envelope_id(),
            status="error",
            message=error_message,
            sdk_name=self._controller_name,
            function_name=function_name,
            data=None,
            warnings=[],
            errors=[error_message],
            artifacts_created=[],
            references={},
            run_id=run_id,
            timestamp=TimeProvider.now_iso(),
            stage_name=stage_name,
            actor=actor,
        )

    # ------------------------------------------------------------------
    # Observability / audit hooks
    # ------------------------------------------------------------------

    def _emit_event(
        self,
        event_type: str,
        run_id: str,
        stage_name: str,
        actor: Optional[ActorRecord] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Emit an observability event via the registered observability service.

        Args:
            event_type: Event type identifier.
            run_id: Active run identifier.
            stage_name: Current stage name.
            actor: Actor emitting the event.
            payload: Event-specific payload.

        Returns:
            ``event_id`` if emitted, None otherwise.
        """
        if self._dependencies is None or not self._dependencies.has("observability"):
            return None
        try:
            obs = self._dependencies.get("observability")
            result = obs.write_event(
                event_type=event_type,
                run_id=run_id,
                stage_name=stage_name,
                actor=actor,
                payload=payload or {},
            )
            return result.references.get("event_id")
        except Exception as exc:
            self._logger.warning("Failed to emit event %s: %s", event_type, exc)
            return None

    def _write_audit(
        self,
        audit_type: str,
        run_id: str,
        stage_name: str,
        actor: Optional[ActorRecord] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Write an audit record via the registered audit service.

        Args:
            audit_type: Audit record type (decision, approval, etc.).
            run_id: Active run identifier.
            stage_name: Current stage name.
            actor: Actor creating the record.
            payload: Audit-specific payload.

        Returns:
            ``audit_id`` if written, None otherwise.
        """
        if self._dependencies is None or not self._dependencies.has("audit"):
            return None
        try:
            audit = self._dependencies.get("audit")
            result = audit.write_audit_record(
                audit_type=audit_type,
                run_id=run_id,
                stage_name=stage_name,
                actor=actor,
                payload=payload or {},
            )
            return result.references.get("audit_id")
        except Exception as exc:
            self._logger.warning("Failed to write audit record %s: %s", audit_type, exc)
            return None

    def _get_service(self, service_name: str) -> Optional[Any]:
        """Retrieve a registered service from the dependency container.

        Args:
            service_name: Name of the service to retrieve.

        Returns:
            Service instance or None.
        """
        if self._dependencies is None:
            return None
        try:
            return self._dependencies.get(service_name)
        except Exception:
            return None
