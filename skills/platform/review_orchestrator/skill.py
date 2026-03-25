"""ReviewOrchestratorSkill -- manages the full HITL review lifecycle for a stage.

Responsibilities:
1. Open a review for the specified stage/candidate.
2. Poll or await reviewer action (simulated by an optional auto-approve callback in tests).
3. Submit the review action (approve / reject / escalate).
4. Return the final :class:`ReviewOutcome`.

Usage::

    from skills.platform.review_orchestrator.skill import ReviewOrchestratorSkill, ReviewRequest

    skill = ReviewOrchestratorSkill(dispatcher, request)
    outcome = skill.run()
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable

from platform_contracts.enums import InteractionType

logger = logging.getLogger(__name__)


@dataclass
class ReviewRequest:
    """Inputs for the review orchestrator.

    Attributes:
        project_id: MDLC project identifier.
        run_id: MDLC run identifier.
        stage_name: Stage requiring review.
        actor_id: Actor opening the review.
        role: Actor's MDLC role.
        review_type: One of the :class:`~platform_contracts.enums.ReviewType` values.
        summary_for_reviewer: Human-readable context for the reviewer.
        evidence_refs: List of artifact refs as evidence.
        subject_candidate_id: Candidate being reviewed (if applicable).
        session_id: Active session ID.
        policy_acknowledgments: List of policy IDs to acknowledge.
        action_provider: Optional callable that returns ``(action, rationale)`` for
            automated testing.  In production this is provided by a human via UI.
    """

    project_id: str
    run_id: str
    stage_name: str
    actor_id: str
    role: str
    review_type: str = "GENERIC"
    summary_for_reviewer: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    subject_candidate_id: str = ""
    session_id: str = ""
    policy_acknowledgments: list[str] = field(default_factory=list)
    action_provider: Callable[[], tuple[str, str]] | None = None


@dataclass
class ReviewOutcome:
    """Result of a completed review orchestration.

    Attributes:
        success: True if the review resolved (approved or rejected).
        review_id: The review ID.
        action: The final review action taken.
        decision_id: Resulting decision record ID.
        audit_id: Backing audit record.
        error: Error message if unsuccessful.
    """

    success: bool
    review_id: str = ""
    action: str = ""
    decision_id: str = ""
    audit_id: str = ""
    error: str = ""


class ReviewOrchestratorSkill:
    """Manages the full HITL review flow for a single review.

    Args:
        dispatcher: :class:`~agent_bridge.dispatcher.AgentDispatcher`.
        request: :class:`ReviewRequest` describing the review to open.
    """

    def __init__(self, dispatcher: Any, request: ReviewRequest) -> None:
        self._dispatcher = dispatcher
        self._request = request

    def run(self) -> ReviewOutcome:
        """Open, surface, and resolve a review.

        Returns:
            :class:`ReviewOutcome`.
        """
        # 1. Open review.
        open_resp = self._dispatch(
            "open_review",
            InteractionType.REVIEW_RESPONSE,
            {
                "review_type": self._request.review_type,
                "summary_for_reviewer": self._request.summary_for_reviewer,
                "evidence_refs": self._request.evidence_refs,
                "subject_candidate_id": self._request.subject_candidate_id,
                "reviewers": [],
            },
        )
        if open_resp.get("status") != "ok":
            return ReviewOutcome(success=False, error=open_resp.get("message", "open_review failed."))

        review_id = (open_resp.get("data") or {}).get("review_id", "")
        if not review_id:
            return ReviewOutcome(success=False, error="No review_id returned from open_review.")

        # 2. Get review payload (for display or forwarding to reviewer).
        payload_resp = self._dispatch(
            "get_review_payload",
            InteractionType.REVIEW_RESPONSE,
            {"review_id": review_id},
        )
        if payload_resp.get("status") != "ok":
            logger.warning("review_orchestrator.payload_fetch_failed", extra={"review_id": review_id})

        # 3. Obtain action (from auto-provider or raise for interactive mode).
        if self._request.action_provider is not None:
            action, rationale = self._request.action_provider()
        else:
            # In production this would be injected from the UI callback.
            logger.info("review_orchestrator.awaiting_human_input", extra={"review_id": review_id})
            return ReviewOutcome(
                success=True,
                review_id=review_id,
                action="pending",
                error="Review is open and awaiting human input.",
            )

        # 4. Submit action.
        submit_resp = self._dispatch(
            "submit_review_action",
            InteractionType.REVIEW_RESPONSE,
            {
                "review_id": review_id,
                "review_action": action,
                "rationale": rationale,
                "policy_acknowledgments": self._request.policy_acknowledgments,
                "conditions": [],
                "active_violations": [],
            },
        )
        if submit_resp.get("status") != "ok":
            return ReviewOutcome(
                success=False,
                review_id=review_id,
                action=action,
                error=submit_resp.get("message", "submit_review_action failed."),
            )

        data = submit_resp.get("data") or {}
        return ReviewOutcome(
            success=True,
            review_id=review_id,
            action=action,
            decision_id=data.get("decision_id", ""),
            audit_id=data.get("audit_id", ""),
        )

    # ------------------------------------------------------------------

    def _dispatch(
        self,
        action: str,
        interaction_type: InteractionType,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        from platform_contracts.fragments import ActorRecord
        from platform_core.utils.id_factory import id_factory
        from platform_core.utils.time_provider import time_provider

        payload = {
            "project_id": self._request.project_id,
            "run_id": self._request.run_id,
            "session_id": self._request.session_id,
            "trace_id": id_factory.audit_id("trace"),
            "correlation_id": id_factory.audit_id("corr"),
            "actor": ActorRecord(actor_id=self._request.actor_id, role=self._request.role).model_dump(),
            "timestamp": time_provider.now().isoformat(),
            "stage_name": self._request.stage_name,
            "interaction_type": interaction_type.value,
            "action": action,
            "data": data or {},
        }
        return self._dispatcher.dispatch(payload)
