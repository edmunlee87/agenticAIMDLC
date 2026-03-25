"""validationsdk.remediation_tracker -- tracks remediation actions for findings.

Each finding may have one or more remediation actions.  Actions are immutable
once created; status transitions create new versions in the history.
"""

from __future__ import annotations

import logging

from validationsdk.models import RemediationAction, RemediationStatus

logger = logging.getLogger(__name__)


class RemediationTracker:
    """Tracks :class:`~validationsdk.models.RemediationAction` records.

    Args:
        scope_id: Scope this tracker belongs to.
    """

    def __init__(self, scope_id: str) -> None:
        self._scope_id = scope_id
        self._actions: dict[str, RemediationAction] = {}
        self._history: dict[str, list[RemediationAction]] = {}
        # finding_id -> list[action_id]
        self._by_finding: dict[str, list[str]] = {}

    def create(self, action: RemediationAction) -> None:
        """Register a new remediation action.

        Args:
            action: :class:`RemediationAction` to register.

        Raises:
            ValueError: If action_id already exists.
        """
        if action.action_id in self._actions:
            raise ValueError(f"Remediation action '{action.action_id}' already exists.")
        self._actions[action.action_id] = action
        self._history[action.action_id] = [action]
        self._by_finding.setdefault(action.finding_id, []).append(action.action_id)
        logger.info(
            "remediation_tracker.created",
            extra={
                "action_id": action.action_id,
                "finding_id": action.finding_id,
                "scope_id": self._scope_id,
            },
        )

    def update_status(
        self,
        action_id: str,
        new_status: RemediationStatus,
        resolution_notes: str = "",
        evidence_artifact_ids: list[str] | None = None,
    ) -> RemediationAction:
        """Transition a remediation action to a new status.

        Args:
            action_id: Action to update.
            new_status: Target :class:`RemediationStatus`.
            resolution_notes: Notes on resolution.
            evidence_artifact_ids: New evidence produced.

        Returns:
            Updated :class:`RemediationAction`.

        Raises:
            KeyError: If action_id not found.
        """
        current = self._actions[action_id]
        update: dict = {"status": new_status, "resolution_notes": resolution_notes}
        if evidence_artifact_ids is not None:
            update["evidence_artifact_ids"] = evidence_artifact_ids
        if new_status in {RemediationStatus.RESOLVED, RemediationStatus.CLOSED_NOT_FIXED}:
            from datetime import datetime, timezone
            update["resolved_at"] = datetime.now(timezone.utc)

        updated = current.model_copy(update=update)
        self._actions[action_id] = updated
        self._history[action_id].append(updated)
        logger.info(
            "remediation_tracker.status_updated",
            extra={
                "action_id": action_id,
                "old_status": current.status,
                "new_status": new_status,
            },
        )
        return updated

    def get(self, action_id: str) -> RemediationAction:
        """Retrieve a remediation action by ID.

        Args:
            action_id: Action identifier.

        Returns:
            :class:`RemediationAction`.

        Raises:
            KeyError: If not found.
        """
        return self._actions[action_id]

    def get_for_finding(self, finding_id: str) -> list[RemediationAction]:
        """Return all remediation actions for a finding.

        Args:
            finding_id: Finding identifier.

        Returns:
            List of :class:`RemediationAction`.
        """
        action_ids = self._by_finding.get(finding_id, [])
        return [self._actions[aid] for aid in action_ids if aid in self._actions]

    def get_history(self, action_id: str) -> list[RemediationAction]:
        """Return all versions of a remediation action.

        Args:
            action_id: Action identifier.

        Returns:
            List of :class:`RemediationAction` (oldest first).
        """
        return list(self._history.get(action_id, []))

    def list_open(self) -> list[RemediationAction]:
        """Return all open or in-progress remediation actions.

        Returns:
            List of :class:`RemediationAction`.
        """
        return [
            a for a in self._actions.values()
            if a.status in {RemediationStatus.OPEN, RemediationStatus.IN_PROGRESS}
        ]

    def all_resolved(self) -> bool:
        """Return True if every remediation action is resolved or closed."""
        return all(
            a.status in {RemediationStatus.RESOLVED, RemediationStatus.CLOSED_NOT_FIXED}
            for a in self._actions.values()
        )
