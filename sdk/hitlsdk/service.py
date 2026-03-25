"""HITLService — review lifecycle, action validation, and decision capture.

The public interface covers:
- :meth:`create_review`: open a governance review gate with SLA + reviewers.
- :meth:`build_review_payload`: assemble the 3-panel review payload for the UI.
- :meth:`submit_action`: validate and capture a bounded reviewer action.
- :meth:`approve_review` / :meth:`approve_with_conditions` / :meth:`reject_review`:
  named shortcuts.
- :meth:`escalate_review`: escalate with reason + target reviewer.
- :meth:`get_review` / :meth:`list_reviews_for_run`.

Every finalising action:
1. Validates via :class:`~sdk.hitlsdk.action_validator.ActionValidator`.
2. Writes an audit record via :class:`~sdk.auditsdk.audit_service.AuditService`.
3. Emits a skill event via :class:`~sdk.observabilitysdk.observability_service.ObservabilityService`.
4. Optionally notifies :class:`~sdk.workflowsdk.service.WorkflowService` via
   workflow events (REVIEW_OPENED / REVIEW_CLOSED).
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sdk.auditsdk.audit_service import AuditService
from sdk.hitlsdk.action_validator import ActionValidator
from sdk.hitlsdk.models import (
    EscalationReason,
    EscalationRecord,
    ReviewAction,
    ReviewDecision,
    ReviewRecord,
    ReviewStatus,
    ReviewerAssignment,
)
from sdk.hitlsdk.review_store import ReviewStore
from sdk.observabilitysdk.observability_service import ObservabilityService
from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.schemas.base_result import BaseResult
from sdk.platform_core.schemas.common_fragments import PolicyContextRef
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider
from sdk.platform_core.services.base_service import BaseService
from sdk.workflowsdk.models import ReviewType

_SDK_NAME = "hitlsdk"
logger = logging.getLogger(f"platform.{_SDK_NAME}")


def _enum_str(v: Any) -> str:
    """Return the plain string value of an enum field.

    Handles both enum instances (`.value`) and plain strings (Pydantic
    `use_enum_values=True` already extracted the value on construction).
    """
    return v.value if hasattr(v, "value") else str(v)


def _action_to_status(action: ReviewAction) -> ReviewStatus:
    return {
        ReviewAction.APPROVE: ReviewStatus.APPROVED,
        ReviewAction.APPROVE_WITH_CHANGES: ReviewStatus.APPROVED_WITH_CHANGES,
        ReviewAction.REJECT: ReviewStatus.REJECTED,
        ReviewAction.RERUN_WITH_PARAMETERS: ReviewStatus.RERUN_REQUESTED,
        ReviewAction.ESCALATE: ReviewStatus.ESCALATED,
    }.get(action, ReviewStatus.PENDING_REVIEW)


class HITLService(BaseService):
    """Human-in-the-loop review lifecycle service.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        obs: :class:`ObservabilityService` for event emission.
        audit: :class:`AuditService` for decision records.
        workflow_service: Optional :class:`~sdk.workflowsdk.service.WorkflowService`
            for appending REVIEW_OPENED / REVIEW_CLOSED workflow events.
        action_validator: Injectable :class:`ActionValidator`.
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        obs: ObservabilityService,
        audit: AuditService,
        workflow_service: Optional[Any] = None,
        action_validator: Optional[ActionValidator] = None,
    ) -> None:
        super().__init__(sdk_name=_SDK_NAME)
        self._bundle = bundle
        self._obs = obs
        self._audit = audit
        self._workflow = workflow_service
        self._validator = action_validator or ActionValidator()
        self._store = ReviewStore()
        self._decisions: Dict[str, ReviewDecision] = {}

    # ------------------------------------------------------------------
    # Review lifecycle
    # ------------------------------------------------------------------

    def create_review(
        self,
        *,
        review_type: ReviewType,
        stage_name: str,
        run_id: str,
        project_id: str,
        created_by: str,
        actor_role: str = "system",
        reviewers: Optional[List[ReviewerAssignment]] = None,
        evidence_refs: Optional[List[str]] = None,
        subject_candidate_id: str = "",
        subject_artifact_ids: Optional[List[str]] = None,
        sla_deadline: Optional[datetime] = None,
        summary_for_reviewer: str = "",
        session_id: str = "",
        trace_id: str = "",
        policy_context: Optional[PolicyContextRef] = None,
        template_id: str = "",
    ) -> BaseResult:
        """Open a governance review gate.

        Args:
            review_type: Type of review.
            stage_name: MDLC stage the review is attached to.
            run_id: Active run.
            project_id: Owning project.
            created_by: Actor ID opening the review.
            actor_role: Role of the opening actor.
            reviewers: Assigned reviewers.
            evidence_refs: Artifact/document IDs submitted as evidence.
            subject_candidate_id: Candidate version under review.
            subject_artifact_ids: Artifact IDs under review.
            sla_deadline: SLA deadline for the review.
            summary_for_reviewer: Summary text for the review UI.
            session_id: Active session.
            trace_id: Distributed trace ID.
            policy_context: Active policy context.
            template_id: Review template YAML ID.

        Returns:
            :class:`BaseResult` with ``data["review_id"]`` on success.
        """
        fn = "create_review"
        self._log_start(fn, run_id=run_id, stage_name=stage_name)
        try:
            review_id = IDFactory.review_id()
            record = ReviewRecord(
                review_id=review_id,
                review_type=review_type,
                status=ReviewStatus.PENDING_REVIEW,
                stage_name=stage_name,
                run_id=run_id,
                project_id=project_id,
                session_id=session_id,
                trace_id=trace_id,
                created_by=created_by,
                created_at=TimeProvider.now(),
                sla_deadline=sla_deadline,
                policy_context=policy_context,
                reviewers=reviewers or [],
                evidence_refs=evidence_refs or [],
                template_id=template_id,
                subject_candidate_id=subject_candidate_id,
                subject_artifact_ids=subject_artifact_ids or [],
                summary_for_reviewer=summary_for_reviewer,
            )
            self._store.put(record)

            # Notify workflow service if connected
            if self._workflow is not None:
                self._workflow.start_stage(
                    run_id=run_id,
                    project_id=project_id,
                    stage_name=stage_name,
                    actor_id=created_by,
                    actor_role=actor_role,
                    session_id=session_id,
                    trace_id=trace_id,
                )

            # Observability
            self._obs.write_event(
                event_type="hitl.review.opened",
                stage_name=stage_name,
                run_id=run_id,
                project_id=project_id,
                session_id=session_id or None,
                actor=created_by,
                status="success",
                review_created=True,
                payload={"review_id": review_id, "review_type": review_type.value},
            )

            result = self._build_result(
                fn,
                status="success",
                message=f"Review '{review_id}' ({review_type.value}) opened for stage '{stage_name}'.",
                data={
                    "review_id": review_id,
                    "review_type": review_type.value,
                    "stage_name": stage_name,
                    "run_id": run_id,
                },
                workflow_hint=f"review:{review_id} opened at stage:{stage_name}",
                audit_hint="review opened — audit record recommended",
                observability_hint="emit hitl.review.opened event",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        self._log_finish(fn, result)
        return result

    def get_review(self, review_id: str) -> BaseResult:
        """Return a review by ID.

        Args:
            review_id: Target review.

        Returns:
            :class:`BaseResult` with ``data["review"]`` (dict) on success.
        """
        fn = "get_review"
        try:
            record = self._store.get(review_id)
            if record is None:
                return self._build_result(
                    fn,
                    status="failure",
                    message=f"Review '{review_id}' not found.",
                    errors=[f"Review '{review_id}' not found."],
                )
            result = self._build_result(
                fn,
                status="success",
                message=f"Review '{review_id}' retrieved.",
                data={"review": record.model_dump(), "status": _enum_str(record.status)},
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def list_reviews_for_run(
        self,
        run_id: str,
        status: Optional[ReviewStatus] = None,
    ) -> BaseResult:
        """List reviews for a run, optionally filtered by status.

        Args:
            run_id: Run identifier.
            status: Optional status filter.

        Returns:
            :class:`BaseResult` with ``data["reviews"]`` (list of dicts).
        """
        fn = "list_reviews_for_run"
        try:
            records = self._store.list_for_run(run_id, status=status)
            result = self._build_result(
                fn,
                status="success",
                message=f"{len(records)} review(s) found for run '{run_id}'.",
                data={
                    "reviews": [r.model_dump() for r in records],
                    "count": len(records),
                },
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def build_review_payload(self, review_id: str) -> BaseResult:
        """Build the 3-panel review payload for the UI layer.

        Returns a structured dict with:
        - ``panel_a``: proposal + evidence (subject, artifacts, evidence_refs).
        - ``panel_b``: editable context (summary, reviewer notes slot).
        - ``panel_c``: actions + status (allowed actions, SLA, escalation chain).

        Args:
            review_id: Review to build payload for.

        Returns:
            :class:`BaseResult` with ``data["payload"]`` (dict) on success.
        """
        fn = "build_review_payload"
        try:
            record = self._store.get(review_id)
            if record is None:
                return self._build_result(
                    fn,
                    status="failure",
                    message=f"Review '{review_id}' not found.",
                    errors=[f"Review '{review_id}' not found."],
                )

            primary_role = (
                record.reviewers[0].reviewer_role if record.reviewers else "validator"
            )
            allowed_actions = self._validator.allowed_for_role(primary_role)

            payload: Dict[str, Any] = {
                "review_id": review_id,
                "review_type": _enum_str(record.review_type),
                "status": _enum_str(record.status),
                "schema_version": record.schema_version,
                "panel_a": {
                    "subject_candidate_id": record.subject_candidate_id,
                    "subject_artifact_ids": record.subject_artifact_ids,
                    "evidence_refs": record.evidence_refs,
                    "summary_for_reviewer": record.summary_for_reviewer,
                },
                "panel_b": {
                    "reviewer_notes": "",
                    "template_id": record.template_id,
                    "policy_context": (
                        record.policy_context.model_dump()
                        if record.policy_context else {}
                    ),
                },
                "panel_c": {
                    "allowed_actions": [a.value for a in allowed_actions],
                    "sla_deadline": (
                        record.sla_deadline.isoformat()
                        if record.sla_deadline else None
                    ),
                    "reviewers": [r.model_dump() for r in record.reviewers],
                    "escalation_chain": [e.model_dump() for e in record.escalation_chain],
                },
            }
            result = self._build_result(
                fn,
                status="success",
                message=f"Review payload built for '{review_id}'.",
                data={"payload": payload},
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    # ------------------------------------------------------------------
    # Decision capture
    # ------------------------------------------------------------------

    def submit_action(
        self,
        *,
        review_id: str,
        action: ReviewAction,
        actor_id: str,
        actor_role: str,
        rationale: str = "",
        conditions: Optional[List[str]] = None,
        rerun_parameters: Optional[Dict[str, Any]] = None,
        policy_acknowledgments: Optional[List[str]] = None,
        active_violations: Optional[List[str]] = None,
        session_id: str = "",
        trace_id: str = "",
    ) -> BaseResult:
        """Validate and capture a bounded reviewer action.

        Args:
            review_id: Review to act on.
            action: Bounded :class:`ReviewAction`.
            actor_id: Actor taking the action.
            actor_role: Platform role string.
            rationale: Decision rationale.
            conditions: Approval conditions (for APPROVED_WITH_CHANGES).
            rerun_parameters: Rerun parameters (for RERUN_WITH_PARAMETERS).
            policy_acknowledgments: Policy violation IDs acknowledged.
            active_violations: Active policy violation IDs.
            session_id: Active session.
            trace_id: Distributed trace ID.

        Returns:
            :class:`BaseResult` with ``data["decision_id"]`` on success.
        """
        fn = "submit_action"
        try:
            record = self._store.get(review_id)
            if record is None:
                return self._build_result(
                    fn,
                    status="failure",
                    message=f"Review '{review_id}' not found.",
                    errors=[f"Review '{review_id}' not found."],
                )

            # Validate the action
            errors = self._validator.validate(
                review=record,
                action=action,
                actor_id=actor_id,
                actor_role=actor_role,
                rationale=rationale,
                policy_acknowledgments=policy_acknowledgments,
                active_violations=active_violations,
            )
            if errors:
                return self._build_result(
                    fn,
                    status="failure",
                    message=f"Action '{action.value}' validation failed.",
                    errors=errors,
                    data={"review_id": review_id, "action": action.value},
                )

            # Write audit record
            audit_result = self._audit.register_decision(
                stage_name=record.stage_name,
                run_id=record.run_id,
                project_id=record.project_id,
                actor=actor_id,
                reason=rationale or f"Review action: {action.value}",
                decision_payload={
                    "review_id": review_id,
                    "action": action.value,
                    "conditions": conditions or [],
                },
            )
            audit_id = audit_result.data.get("audit_id", "") if audit_result.is_success else ""

            # Build decision record
            decision_id = IDFactory.audit_id()  # reuse audit prefix for decision IDs
            decision = ReviewDecision(
                decision_id=decision_id,
                review_id=review_id,
                action=action,
                decided_by=actor_id,
                actor_role=actor_role,
                decided_at=TimeProvider.now(),
                rationale=rationale,
                audit_id=audit_id,
                conditions=conditions or [],
                rerun_parameters=rerun_parameters or {},
                policy_acknowledgments=policy_acknowledgments or [],
            )
            self._decisions[decision_id] = decision

            # Update review status if action finalises it
            if self._validator.is_finalising(action):
                new_status = _action_to_status(action)
                updated = record.model_copy(update={"status": new_status})
                self._store.put(updated)

            # Emit observability event
            self._obs.write_event(
                event_type=f"hitl.review.{action.value}",
                stage_name=record.stage_name,
                run_id=record.run_id,
                project_id=record.project_id,
                session_id=session_id or None,
                actor=actor_id,
                status="success",
                governance_gate_hit=True,
                payload={
                    "review_id": review_id,
                    "action": action.value,
                    "audit_id": audit_id,
                    "decision_id": decision_id,
                },
            )

            result = self._build_result(
                fn,
                status="success",
                message=(
                    f"Action '{action.value}' on review '{review_id}' "
                    f"captured (decision: {decision_id})."
                ),
                data={
                    "decision_id": decision_id,
                    "review_id": review_id,
                    "action": action.value,
                    "audit_id": audit_id,
                    "new_status": _action_to_status(action).value
                    if self._validator.is_finalising(action)
                    else ReviewStatus.PENDING_REVIEW.value,
                },
                audit_hint=f"decision audit written: {audit_id}",
                observability_hint=f"emit hitl.review.{action.value} event",
                workflow_hint=f"review:{review_id} action:{action.value}",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    # ------------------------------------------------------------------
    # Named shortcuts
    # ------------------------------------------------------------------

    def approve_review(
        self,
        review_id: str,
        actor_id: str,
        actor_role: str,
        rationale: str = "",
        policy_acknowledgments: Optional[List[str]] = None,
        session_id: str = "",
        trace_id: str = "",
    ) -> BaseResult:
        """Approve a review unconditionally.

        Args:
            review_id: Target review.
            actor_id: Approving actor ID.
            actor_role: Actor role.
            rationale: Optional rationale.
            policy_acknowledgments: Acknowledged violation IDs.
            session_id: Active session.
            trace_id: Trace ID.

        Returns:
            :class:`BaseResult` with ``data["decision_id"]``.
        """
        return self.submit_action(
            review_id=review_id,
            action=ReviewAction.APPROVE,
            actor_id=actor_id,
            actor_role=actor_role,
            rationale=rationale,
            policy_acknowledgments=policy_acknowledgments,
            session_id=session_id,
            trace_id=trace_id,
        )

    def approve_with_conditions(
        self,
        review_id: str,
        actor_id: str,
        actor_role: str,
        conditions: List[str],
        rationale: str = "",
        session_id: str = "",
        trace_id: str = "",
    ) -> BaseResult:
        """Approve a review with stated conditions.

        Args:
            review_id: Target review.
            actor_id: Approving actor ID.
            actor_role: Actor role.
            conditions: Approval conditions list.
            rationale: Optional rationale.
            session_id: Active session.
            trace_id: Trace ID.

        Returns:
            :class:`BaseResult` with ``data["decision_id"]``.
        """
        return self.submit_action(
            review_id=review_id,
            action=ReviewAction.APPROVE_WITH_CHANGES,
            actor_id=actor_id,
            actor_role=actor_role,
            rationale=rationale or f"Approved with {len(conditions)} condition(s).",
            conditions=conditions,
            session_id=session_id,
            trace_id=trace_id,
        )

    def reject_review(
        self,
        review_id: str,
        actor_id: str,
        actor_role: str,
        rationale: str,
        session_id: str = "",
        trace_id: str = "",
    ) -> BaseResult:
        """Reject a review (rationale mandatory).

        Args:
            review_id: Target review.
            actor_id: Rejecting actor ID.
            actor_role: Actor role.
            rationale: Rejection rationale (non-empty required).
            session_id: Active session.
            trace_id: Trace ID.

        Returns:
            :class:`BaseResult` with ``data["decision_id"]``.
        """
        return self.submit_action(
            review_id=review_id,
            action=ReviewAction.REJECT,
            actor_id=actor_id,
            actor_role=actor_role,
            rationale=rationale,
            session_id=session_id,
            trace_id=trace_id,
        )

    def escalate_review(
        self,
        review_id: str,
        actor_id: str,
        actor_role: str,
        escalate_to: str,
        reason: EscalationReason,
        note: str = "",
        session_id: str = "",
        trace_id: str = "",
    ) -> BaseResult:
        """Escalate a review to a higher authority.

        Args:
            review_id: Review to escalate.
            actor_id: Escalating actor ID.
            actor_role: Actor role.
            escalate_to: Target reviewer actor ID.
            reason: :class:`EscalationReason`.
            note: Free-text escalation note.
            session_id: Active session.
            trace_id: Trace ID.

        Returns:
            :class:`BaseResult` with ``data["review_id"]`` and
            ``data["escalated_to"]``.
        """
        fn = "escalate_review"
        try:
            record = self._store.get(review_id)
            if record is None:
                return self._build_result(
                    fn,
                    status="failure",
                    message=f"Review '{review_id}' not found.",
                    errors=[f"Review '{review_id}' not found."],
                )

            escalation = EscalationRecord(
                escalation_id=IDFactory.audit_id(),
                escalated_by=actor_id,
                escalated_to=escalate_to,
                reason=reason,
                note=note,
                escalated_at=TimeProvider.now(),
            )
            updated = record.model_copy(
                update={
                    "status": ReviewStatus.ESCALATED,
                    "escalation_chain": list(record.escalation_chain) + [escalation],
                }
            )
            self._store.put(updated)

            # Write audit record
            self._audit.write_audit_record(
                audit_type="escalation",
                actor=actor_id,
                stage_name=record.stage_name,
                run_id=record.run_id,
                project_id=record.project_id,
                reason=note or reason.value,
                decision_payload={
                    "review_id": review_id,
                    "escalated_to": escalate_to,
                    "reason": reason.value,
                },
            )

            # Observability
            self._obs.write_event(
                event_type="hitl.review.escalated",
                stage_name=record.stage_name,
                run_id=record.run_id,
                project_id=record.project_id,
                session_id=session_id or None,
                actor=actor_id,
                status="success",
                governance_gate_hit=True,
                payload={
                    "review_id": review_id,
                    "escalated_to": escalate_to,
                    "reason": reason.value,
                },
            )

            result = self._build_result(
                fn,
                status="success",
                message=(
                    f"Review '{review_id}' escalated to '{escalate_to}' "
                    f"({reason.value})."
                ),
                data={
                    "review_id": review_id,
                    "escalated_to": escalate_to,
                    "reason": reason.value,
                    "new_status": ReviewStatus.ESCALATED.value,
                },
                audit_hint="escalation audit written",
                workflow_hint=f"review:{review_id} escalated",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def get_decision(self, decision_id: str) -> BaseResult:
        """Return a decision record by ID.

        Args:
            decision_id: Decision to retrieve.

        Returns:
            :class:`BaseResult` with ``data["decision"]`` (dict) on success.
        """
        fn = "get_decision"
        try:
            dec = self._decisions.get(decision_id)
            if dec is None:
                return self._build_result(
                    fn,
                    status="failure",
                    message=f"Decision '{decision_id}' not found.",
                    errors=[f"Decision '{decision_id}' not found."],
                )
            result = self._build_result(
                fn,
                status="success",
                message=f"Decision '{decision_id}' retrieved.",
                data={"decision": dec.model_dump()},
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def health_check(self) -> BaseResult:
        """Return service health statistics.

        Returns:
            :class:`BaseResult` with ``data["n_reviews"]``, ``data["n_open"]``,
            and ``data["n_decisions"]``.
        """
        fn = "health_check"
        n_open = sum(
            1
            for r in self._store._current.values()
            if r.status == ReviewStatus.PENDING_REVIEW
        )
        return self._build_result(
            fn,
            status="success",
            message="HITLService healthy.",
            data={
                "status": "ok",
                "n_reviews": len(self._store._current),
                "n_decisions": len(self._decisions),
                "n_open": n_open,
            },
        )
