"""SessionController -- open and resume UI/agent sessions.

Handles :class:`~platform_core.schemas.payloads.InteractionPayload` with
``interaction_type`` of ``SESSION_COMMAND``.

Actions:
- ``open_session``: bootstrap a new project/run and open a session.
- ``resume_session``: resume a suspended session from checkpoint.
"""

from __future__ import annotations

import logging
from typing import Any

from platform_core.controllers.base import BaseController
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.runtime.resolver import RuntimeResolver
from platform_core.schemas.payloads import InteractionPayload, StandardResponseEnvelope
from platform_core.utils.id_factory import IDFactory
from platform_core.utils.time_provider import TimeProvider

logger = logging.getLogger(__name__)


class SessionController(BaseController):
    """Controller for session bootstrap and resume.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        workflow_service: :class:`~workflowsdk.service.WorkflowService`.
        resolver: Pre-built :class:`~platform_core.runtime.resolver.RuntimeResolver`.
        id_factory_: Injectable :class:`IDFactory`.
        time_provider_: Injectable :class:`TimeProvider`.
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        workflow_service: Any,
        resolver: RuntimeResolver | None = None,
        id_factory_: IDFactory | None = None,
        time_provider_: TimeProvider | None = None,
    ) -> None:
        super().__init__(bundle, id_factory_=id_factory_, time_provider_=time_provider_)
        self._workflow = workflow_service
        self._resolver = resolver or RuntimeResolver(bundle)

    def handle(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        """Dispatch to open_session or resume_session based on payload action.

        Args:
            payload: Interaction payload with ``action`` set to
                ``"open_session"`` or ``"resume_session"``.

        Returns:
            :class:`StandardResponseEnvelope`.
        """
        action = payload.action
        if action == "open_session":
            return self._open_session(payload)
        if action == "resume_session":
            return self._resume_session(payload)
        return self._build_error_response(
            payload, "ERR_UNKNOWN_ACTION",
            f"SessionController does not handle action '{action}'.",
        )

    # ------------------------------------------------------------------
    # Private handlers
    # ------------------------------------------------------------------

    def _open_session(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        result = self._workflow.open_session(
            run_id=payload.run_id,
            project_id=payload.project_id,
            actor=payload.actor,
            last_stage=payload.stage_name,
        )
        if not result.success:
            return self._build_error_response(payload, result.error_code or "ERR_SESSION", result.error_message or "")

        decision = self._resolver.resolve(_make_ctx(payload))
        return _ok_envelope(payload, self._time_provider, data={"session_id": result.data.session_id}, decision=decision)

    def _resume_session(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        session_id = (payload.data or {}).get("session_id", payload.session_id)
        if not session_id:
            return self._build_error_response(payload, "ERR_SESSION_ID_REQUIRED", "session_id required for resume.")

        result = self._workflow.resume_session(session_id, payload.actor)
        if not result.success:
            return self._build_error_response(payload, result.error_code or "ERR_RESUME", result.error_message or "")

        decision = self._resolver.resolve(_make_ctx(payload))
        return _ok_envelope(payload, self._time_provider, data={"session_id": session_id}, decision=decision)


# ---------------------------------------------------------------------------
# Shared helpers (imported by all controllers in this package)
# ---------------------------------------------------------------------------

def _make_ctx(payload: InteractionPayload) -> Any:
    from platform_core.schemas.payloads import RuntimeContext
    from platform_contracts.enums import WorkflowMode
    return RuntimeContext(
        project_id=payload.project_id,
        run_id=payload.run_id,
        session_id=payload.session_id,
        trace_id=payload.trace_id,
        correlation_id=payload.correlation_id,
        actor=payload.actor,
        timestamp=payload.timestamp,
        stage_name=payload.stage_name,
        active_role=payload.actor.role,
        active_domain=(payload.data or {}).get("domain", "generic"),
        workflow_mode=WorkflowMode((payload.data or {}).get("workflow_mode", WorkflowMode.DEVELOPMENT.value)),
    )


def _ok_envelope(
    payload: InteractionPayload,
    time_provider: Any,
    data: dict[str, Any] | None = None,
    decision: Any = None,
    audit_ref: str = "",
    event_ref: str = "",
) -> StandardResponseEnvelope:
    from platform_contracts.enums import PolicyCheckResult
    from platform_core.schemas.payloads import GovernanceSummary

    gov_summary = GovernanceSummary()
    if decision is not None:
        review_required = decision.governance_constraints.requires_human_review
        gov_summary = GovernanceSummary(
            policy_check_result=PolicyCheckResult.PASS,
            blocking_reasons=[] if not review_required else ["review_required"],
        )

    return StandardResponseEnvelope(
        project_id=payload.project_id,
        run_id=payload.run_id,
        session_id=payload.session_id,
        trace_id=payload.trace_id,
        correlation_id=payload.correlation_id,
        actor=payload.actor,
        timestamp=time_provider.now(),
        stage_name=payload.stage_name,
        policy_context=payload.policy_context,
        status="ok",
        message="",
        workflow_state_patch=data or {},
        audit_ref=audit_ref,
        event_ref=event_ref,
        governance_summary=gov_summary,
    )
