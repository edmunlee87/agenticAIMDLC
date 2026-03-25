"""ReviewController -- open review, get payload, submit action.

Handles ``REVIEW_RESPONSE`` interaction payloads.

Actions:
- ``open_review``
- ``get_review_payload`` (returns 3-panel UI payload)
- ``submit_review_action`` (approve / reject / escalate / etc.)
"""

from __future__ import annotations

import logging
from typing import Any

from platform_contracts.enums import ReviewType
from platform_core.controllers.base import BaseController
from platform_core.controllers.session import _make_ctx, _ok_envelope
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.runtime.resolver import RuntimeResolver
from platform_core.schemas.payloads import InteractionPayload, StandardResponseEnvelope
from platform_core.utils.id_factory import IDFactory
from platform_core.utils.time_provider import TimeProvider

logger = logging.getLogger(__name__)


class ReviewController(BaseController):
    """Controller for HITL review lifecycle.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        hitl_service: :class:`~hitlsdk.service.HITLService`.
        resolver: Pre-built :class:`RuntimeResolver`.
        id_factory_: Injectable :class:`IDFactory`.
        time_provider_: Injectable :class:`TimeProvider`.
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        hitl_service: Any,
        resolver: RuntimeResolver | None = None,
        id_factory_: IDFactory | None = None,
        time_provider_: TimeProvider | None = None,
    ) -> None:
        super().__init__(bundle, id_factory_=id_factory_, time_provider_=time_provider_)
        self._hitl = hitl_service
        self._resolver = resolver or RuntimeResolver(bundle)

    def handle(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        action = payload.action
        dispatch = {
            "open_review": self._open_review,
            "get_review_payload": self._get_review_payload,
            "submit_review_action": self._submit_review_action,
        }
        handler = dispatch.get(action)
        if handler is None:
            return self._build_error_response(
                payload, "ERR_UNKNOWN_ACTION",
                f"ReviewController does not handle action '{action}'.",
            )
        return handler(payload)

    # ------------------------------------------------------------------

    def _open_review(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        data = payload.data or {}
        review_type_raw = data.get("review_type", ReviewType.GENERIC.value)
        try:
            review_type = ReviewType(review_type_raw)
        except ValueError:
            return self._build_error_response(
                payload, "ERR_INVALID_REVIEW_TYPE",
                f"Unknown review_type '{review_type_raw}'.",
            )

        from hitlsdk.models import ReviewerAssignment
        reviewer_dicts = data.get("reviewers", [])
        reviewers = [ReviewerAssignment(**r) for r in reviewer_dicts] if reviewer_dicts else []

        result = self._hitl.create_review(
            review_type=review_type,
            stage_name=payload.stage_name,
            run_id=payload.run_id,
            project_id=payload.project_id,
            created_by=payload.actor,
            reviewers=reviewers,
            evidence_refs=data.get("evidence_refs", []),
            subject_candidate_id=data.get("subject_candidate_id", ""),
            summary_for_reviewer=data.get("summary_for_reviewer", ""),
            session_id=payload.session_id,
            trace_id=payload.trace_id,
            policy_context=payload.policy_context,
        )
        if not result.success:
            return self._build_error_response(payload, result.error_code or "ERR_REVIEW", result.error_message or "")

        decision = self._resolver.resolve(_make_ctx(payload))
        return _ok_envelope(
            payload, self._time_provider,
            data={"review_id": result.data.review_id},
            decision=decision,
        )

    def _get_review_payload(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        review_id = (payload.data or {}).get("review_id", "")
        if not review_id:
            return self._build_error_response(payload, "ERR_REVIEW_ID_REQUIRED", "review_id is required.")

        result = self._hitl.build_review_payload(review_id)
        if not result.success:
            return self._build_error_response(payload, result.error_code or "ERR_PAYLOAD", result.error_message or "")

        decision = self._resolver.resolve(_make_ctx(payload))
        return _ok_envelope(payload, self._time_provider, data=result.data, decision=decision)

    def _submit_review_action(self, payload: InteractionPayload) -> StandardResponseEnvelope:
        data = payload.data or {}
        review_id = data.get("review_id", "")
        action_str = data.get("review_action", "")
        rationale = data.get("rationale", "")
        conditions = data.get("conditions", [])
        policy_acks = data.get("policy_acknowledgments", [])
        active_violations = data.get("active_violations", [])

        if not review_id or not action_str:
            return self._build_error_response(
                payload, "ERR_MISSING_FIELDS",
                "review_id and review_action are required.",
            )

        from hitlsdk.models import ReviewAction
        try:
            action = ReviewAction(action_str)
        except ValueError:
            return self._build_error_response(
                payload, "ERR_INVALID_ACTION", f"Unknown review action '{action_str}'.",
            )

        result = self._hitl.submit_action(
            review_id=review_id,
            action=action,
            actor=payload.actor,
            rationale=rationale,
            conditions=conditions,
            policy_acknowledgments=policy_acks,
            active_violations=active_violations,
            session_id=payload.session_id,
            trace_id=payload.trace_id,
        )
        if not result.success:
            return self._build_error_response(payload, result.error_code or "ERR_ACTION", result.error_message or "")

        decision = self._resolver.resolve(_make_ctx(payload))
        return _ok_envelope(
            payload, self._time_provider,
            data={"decision_id": result.data.decision_id, "audit_id": result.data.audit_id},
            audit_ref=result.data.audit_id,
            decision=decision,
        )
