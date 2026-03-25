"""ReviewController — HITL review lifecycle.

Handles :class:`InteractionPayload` with actions:
- ``open_review``: create a new HITL review.
- ``get_review_payload``: return 3-panel review payload for UI rendering.
- ``submit_review_action``: submit approve / reject / escalate / etc.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from sdk.platform_core.controllers.base import BaseController
from sdk.platform_core.runtime.resolvers.runtime_resolver import RuntimeResolver
from sdk.platform_core.schemas.common_fragments import GovernanceSummary
from sdk.platform_core.schemas.payload_models import (
    InteractionPayload,
    StandardResponseEnvelope,
)


class ReviewController(BaseController):
    """Controller for the HITL review lifecycle.

    Args:
        hitl_service: :class:`~hitlsdk.service.HITLService`.
        resolver: Pre-built :class:`RuntimeResolver`.
        dependencies: Optional :class:`DependencyContainer`.
        logger: Optional logger override.
    """

    def __init__(
        self,
        hitl_service: Any,
        resolver: Optional[RuntimeResolver] = None,
        dependencies: Optional[Any] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        super().__init__(
            controller_name="review_controller",
            resolver=resolver,
            dependencies=dependencies,
            logger=logger,
        )
        self._hitl = hitl_service

    def handle(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        """Dispatch to the appropriate review action handler.

        Args:
            payload: :class:`InteractionPayload` with action in
                ``{open_review, get_review_payload, submit_review_action}``.

        Returns:
            :class:`StandardResponseEnvelope`.
        """
        dispatch = {
            "open_review": self._open_review,
            "get_review_payload": self._get_review_payload,
            "submit_review_action": self._submit_review_action,
        }
        handler = dispatch.get(payload.action)
        if handler is None:
            return self._build_error_envelope(
                function_name="handle",
                run_id=payload.run_id or "",
                error_message=f"ReviewController does not handle action '{payload.action}'.",
                stage_name=payload.stage_name,
                actor=payload.actor,
            )
        return handler(payload)

    # ------------------------------------------------------------------

    def _open_review(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        run_id = payload.run_id or ""
        actor = payload.actor
        params = payload.parameters or {}

        result = self._hitl.create_review(
            review_type=params.get("review_type", "generic"),
            stage_name=payload.stage_name,
            run_id=run_id,
            project_id=payload.project_id or "",
            created_by_id=actor.actor_id if actor else "unknown",
            created_by_role=actor.role if actor else "developer",
            subject_candidate_id=params.get("subject_candidate_id", ""),
            evidence_refs=params.get("evidence_refs", []),
            summary_for_reviewer=params.get("summary_for_reviewer", ""),
            reviewers=params.get("reviewers", []),
            session_id=payload.session_id,
            trace_id=payload.trace_id,
        )

        event_ref = self._emit_event(
            "review.created",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
            payload={"review_type": params.get("review_type", "generic")},
        )
        audit_ref = self._write_audit(
            "review_created",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
            payload=result.data if result.data else {},
        )

        if not result.is_success:
            return self._build_error_envelope(
                function_name="open_review",
                run_id=run_id,
                error_message=result.message,
                stage_name=payload.stage_name,
                actor=actor,
            )

        review_id = result.data.get("review_id") if result.data else None
        return self._build_response(
            run_id=run_id,
            function_name="open_review",
            status="success",
            message="Review opened successfully.",
            data={"review_id": review_id},
            stage_name=payload.stage_name,
            actor=actor,
            audit_ref=audit_ref,
            event_ref=event_ref,
            review_created=True,
            review_id=review_id,
            governance_summary=GovernanceSummary(
                policy_check_result="review_required",
                blocking_reasons=["review_required"],
            ),
        )

    def _get_review_payload(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        run_id = payload.run_id or ""
        actor = payload.actor
        params = payload.parameters or {}
        review_id = params.get("review_id") or payload.review_id

        if not review_id:
            return self._build_error_envelope(
                function_name="get_review_payload",
                run_id=run_id,
                error_message="review_id is required to get review payload.",
                stage_name=payload.stage_name,
                actor=actor,
            )

        result = self._hitl.build_review_payload(review_id=review_id)

        if not result.is_success:
            return self._build_error_envelope(
                function_name="get_review_payload",
                run_id=run_id,
                error_message=result.message,
                stage_name=payload.stage_name,
                actor=actor,
            )

        stack = self._resolve_stack(
            stage_name=payload.stage_name,
            actor_role=actor.role if actor else "reviewer",
            runtime_facts={"has_active_review": True, "review_id": review_id},
        )

        return self._build_response(
            run_id=run_id,
            function_name="get_review_payload",
            status="success",
            message="Review payload retrieved.",
            data={
                "review_payload": result.data,
                "resolved_stack": stack.to_dict() if stack else None,
            },
            stage_name=payload.stage_name,
            actor=actor,
            review_id=review_id,
        )

    def _submit_review_action(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        run_id = payload.run_id or ""
        actor = payload.actor
        params = payload.parameters or {}

        review_id = params.get("review_id") or payload.review_id
        review_action = params.get("review_action", "")
        rationale = params.get("rationale", "")
        conditions = params.get("conditions", [])
        policy_acks = params.get("policy_acknowledgments", payload.policy_acknowledgments or [])
        active_violations = params.get("active_violations", [])

        if not review_id or not review_action:
            return self._build_error_envelope(
                function_name="submit_review_action",
                run_id=run_id,
                error_message="review_id and review_action are both required.",
                stage_name=payload.stage_name,
                actor=actor,
            )

        result = self._hitl.submit_action(
            review_id=review_id,
            action=review_action,
            actor_id=actor.actor_id if actor else "unknown",
            actor_role=actor.role if actor else "reviewer",
            rationale=rationale,
            conditions=conditions,
            policy_acknowledgments=policy_acks,
            active_violations=active_violations,
            session_id=payload.session_id,
            trace_id=payload.trace_id,
        )

        audit_ref = self._write_audit(
            "review_action_submitted",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
            payload={
                "review_id": review_id,
                "review_action": review_action,
                "rationale": rationale,
            },
        )
        event_ref = self._emit_event(
            "review.action_submitted",
            run_id=run_id,
            stage_name=payload.stage_name,
            actor=actor,
            payload={"review_id": review_id, "review_action": review_action},
        )

        if not result.is_success:
            return self._build_error_envelope(
                function_name="submit_review_action",
                run_id=run_id,
                error_message=result.message,
                stage_name=payload.stage_name,
                actor=actor,
            )

        return self._build_response(
            run_id=run_id,
            function_name="submit_review_action",
            status="success",
            message=f"Review action '{review_action}' submitted.",
            data=result.data,
            stage_name=payload.stage_name,
            actor=actor,
            audit_ref=audit_ref,
            event_ref=event_ref,
        )
