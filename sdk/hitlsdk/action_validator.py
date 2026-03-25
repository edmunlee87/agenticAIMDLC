"""Action validator — bounded review action enforcement.

Only the actions defined in :class:`~sdk.hitlsdk.models.ReviewAction` are
accepted.  Free-text-only approval (no explicit action) is rejected.

Validation checks:
1. Review must be open (``PENDING_REVIEW``).
2. Action is in the allowed set for the actor's role.
3. Rationale is present for non-trivial actions.
4. Policy acknowledgments are present when active violations exist.

Design contract:
    - Returns a list of error strings (empty = valid) — caller wraps in
      :class:`~sdk.platform_core.schemas.base_result.BaseResult`.
"""

from __future__ import annotations

import logging
from typing import Dict, FrozenSet, List, Optional

from sdk.hitlsdk.models import ReviewAction, ReviewRecord, ReviewStatus

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Role → allowed actions mapping.
# Uses platform RoleEnum values: developer, validator, governance, approver,
# monitoring, remediation, system, reviewer.
# ---------------------------------------------------------------------------

_ROLE_ALLOWED_ACTIONS: Dict[str, FrozenSet[ReviewAction]] = {
    "developer": frozenset({
        ReviewAction.REQUEST_MORE_ANALYSIS,
        ReviewAction.ACKNOWLEDGE,
    }),
    "validator": frozenset({
        ReviewAction.APPROVE,
        ReviewAction.APPROVE_WITH_CHANGES,
        ReviewAction.REJECT,
        ReviewAction.RERUN_WITH_PARAMETERS,
        ReviewAction.REQUEST_MORE_ANALYSIS,
        ReviewAction.ESCALATE,
        ReviewAction.ACKNOWLEDGE,
        ReviewAction.DEFER,
    }),
    "reviewer": frozenset({
        ReviewAction.APPROVE,
        ReviewAction.APPROVE_WITH_CHANGES,
        ReviewAction.REJECT,
        ReviewAction.REQUEST_MORE_ANALYSIS,
        ReviewAction.ESCALATE,
        ReviewAction.ACKNOWLEDGE,
        ReviewAction.DEFER,
    }),
    "governance": frozenset({
        ReviewAction.APPROVE,
        ReviewAction.APPROVE_WITH_CHANGES,
        ReviewAction.REJECT,
        ReviewAction.ESCALATE,
        ReviewAction.ACKNOWLEDGE,
        ReviewAction.DEFER,
    }),
    "approver": frozenset({
        ReviewAction.APPROVE,
        ReviewAction.APPROVE_WITH_CHANGES,
        ReviewAction.REJECT,
        ReviewAction.ESCALATE,
        ReviewAction.ACKNOWLEDGE,
    }),
    "monitoring": frozenset({
        ReviewAction.ACKNOWLEDGE,
        ReviewAction.ESCALATE,
    }),
    "remediation": frozenset({
        ReviewAction.ACKNOWLEDGE,
        ReviewAction.ESCALATE,
        ReviewAction.REQUEST_MORE_ANALYSIS,
    }),
    "system": frozenset({
        ReviewAction.ACKNOWLEDGE,
    }),
}

# Actions requiring a non-empty rationale.
_RATIONALE_REQUIRED: FrozenSet[ReviewAction] = frozenset({
    ReviewAction.REJECT,
    ReviewAction.RERUN_WITH_PARAMETERS,
    ReviewAction.APPROVE_WITH_CHANGES,
    ReviewAction.ESCALATE,
    ReviewAction.REQUEST_MORE_ANALYSIS,
})

# Finalising actions (transition review out of PENDING_REVIEW).
_FINALISING_ACTIONS: FrozenSet[ReviewAction] = frozenset({
    ReviewAction.APPROVE,
    ReviewAction.APPROVE_WITH_CHANGES,
    ReviewAction.REJECT,
    ReviewAction.RERUN_WITH_PARAMETERS,
    ReviewAction.ESCALATE,
})


class ActionValidator:
    """Validates that a reviewer's proposed action is permitted.

    Args:
        role_allowed_actions: Override the default role → actions map.
    """

    def __init__(
        self,
        role_allowed_actions: Optional[Dict[str, FrozenSet[ReviewAction]]] = None,
    ) -> None:
        self._role_map = role_allowed_actions or _ROLE_ALLOWED_ACTIONS

    def validate(
        self,
        review: ReviewRecord,
        action: ReviewAction,
        actor_id: str,
        actor_role: str,
        rationale: str = "",
        policy_acknowledgments: Optional[List[str]] = None,
        active_violations: Optional[List[str]] = None,
    ) -> List[str]:
        """Validate that *actor_role* may take *action* on *review*.

        Args:
            review: The review being acted upon.
            action: Proposed :class:`ReviewAction`.
            actor_id: Actor attempting the action (for logging).
            actor_role: Platform role string (e.g. ``"validator"``).
            rationale: Decision rationale text.
            policy_acknowledgments: Policy violation IDs explicitly acknowledged.
            active_violations: Violation IDs currently active.

        Returns:
            List of error strings (empty list = valid).
        """
        errors: List[str] = []

        # 1. Review must be open.
        if review.status != ReviewStatus.PENDING_REVIEW:
            errors.append(
                f"Review '{review.review_id}' is not open "
                f"(status: {review.status}). Cannot act on a closed review."
            )
            return errors  # early return — remaining checks are irrelevant

        # 2. Actor role must be authorised for this action.
        allowed = self._role_map.get(actor_role, frozenset())
        if action not in allowed:
            errors.append(
                f"Role '{actor_role}' is not authorised to take action "
                f"'{action.value}'. Authorised actions: "
                f"{[a.value for a in allowed] or ['none']}."
            )

        # 3. Rationale required for non-trivial actions.
        if action in _RATIONALE_REQUIRED and not rationale.strip():
            errors.append(
                f"Action '{action.value}' requires a non-empty rationale."
            )

        # 4. Policy acknowledgments required when active violations exist.
        violations = active_violations or []
        acks = set(policy_acknowledgments or [])
        unacknowledged = [v for v in violations if v not in acks]
        if unacknowledged and action in _FINALISING_ACTIONS:
            errors.append(
                f"Action '{action.value}' requires acknowledgment of "
                f"{len(unacknowledged)} active policy violation(s): "
                f"{unacknowledged}."
            )

        if not errors:
            logger.debug(
                "ActionValidator passed: review_id=%s action=%s actor=%s role=%s",
                review.review_id,
                action.value,
                actor_id,
                actor_role,
            )
        return errors

    def is_finalising(self, action: ReviewAction) -> bool:
        """Return True if the action finalises (closes) the review.

        Args:
            action: :class:`ReviewAction` to check.

        Returns:
            True if the action transitions the review out of PENDING_REVIEW.
        """
        return action in _FINALISING_ACTIONS

    def allowed_for_role(self, role: str) -> List[ReviewAction]:
        """Return the list of actions allowed for a given role.

        Args:
            role: Role string.

        Returns:
            Allowed :class:`ReviewAction` list.
        """
        return list(self._role_map.get(role, frozenset()))
