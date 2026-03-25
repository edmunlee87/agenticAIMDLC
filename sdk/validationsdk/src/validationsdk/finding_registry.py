"""validationsdk.finding_registry -- stores and queries validation findings.

The registry is an in-memory, append-on-update store.  Each update produces a
new immutable :class:`~validationsdk.models.ValidationFinding` instance;
the previous version is stored in history for audit purposes.
"""

from __future__ import annotations

import logging
from typing import Any

from validationsdk.models import FindingStatus, FindingSeverity, ValidationFinding

logger = logging.getLogger(__name__)


class FindingRegistry:
    """In-memory registry of :class:`~validationsdk.models.ValidationFinding` records.

    Args:
        scope_id: Scope this registry belongs to.
    """

    def __init__(self, scope_id: str) -> None:
        self._scope_id = scope_id
        self._findings: dict[str, ValidationFinding] = {}
        self._history: dict[str, list[ValidationFinding]] = {}

    def register(self, finding: ValidationFinding) -> None:
        """Add a new finding to the registry.

        Args:
            finding: :class:`ValidationFinding` to register.

        Raises:
            ValueError: If a finding with the same ID already exists.
        """
        if finding.finding_id in self._findings:
            raise ValueError(f"Finding '{finding.finding_id}' already exists. Use update() to change status.")
        self._findings[finding.finding_id] = finding
        self._history[finding.finding_id] = [finding]
        logger.info(
            "finding_registry.registered",
            extra={"finding_id": finding.finding_id, "severity": finding.severity, "scope_id": self._scope_id},
        )

    def update_status(
        self,
        finding_id: str,
        new_status: FindingStatus,
        updated_by: str = "",
        notes: str = "",
    ) -> ValidationFinding:
        """Transition a finding to a new status.

        Args:
            finding_id: Finding to update.
            new_status: Target :class:`FindingStatus`.
            updated_by: Actor making the change.
            notes: Optional notes.

        Returns:
            New immutable :class:`ValidationFinding`.

        Raises:
            KeyError: If finding_id not found.
        """
        current = self._findings[finding_id]
        updated = current.model_copy(update={
            "status": new_status,
            "metadata": {**current.metadata, "updated_by": updated_by, "notes": notes},
        })
        self._findings[finding_id] = updated
        self._history[finding_id].append(updated)
        logger.info(
            "finding_registry.status_updated",
            extra={
                "finding_id": finding_id,
                "old_status": current.status,
                "new_status": new_status,
                "updated_by": updated_by,
            },
        )
        return updated

    def get(self, finding_id: str) -> ValidationFinding:
        """Retrieve a finding by ID.

        Args:
            finding_id: Finding identifier.

        Returns:
            :class:`ValidationFinding`.

        Raises:
            KeyError: If not found.
        """
        return self._findings[finding_id]

    def get_history(self, finding_id: str) -> list[ValidationFinding]:
        """Return all historical versions of a finding.

        Args:
            finding_id: Finding identifier.

        Returns:
            List of :class:`ValidationFinding` (oldest first).
        """
        return list(self._history.get(finding_id, []))

    def list_all(self) -> list[ValidationFinding]:
        """Return all current findings.

        Returns:
            List of :class:`ValidationFinding`.
        """
        return list(self._findings.values())

    def list_by_status(self, status: FindingStatus) -> list[ValidationFinding]:
        """Filter findings by status.

        Args:
            status: :class:`FindingStatus` to filter by.

        Returns:
            Matching findings.
        """
        return [f for f in self._findings.values() if f.status == status]

    def list_by_severity(self, severity: FindingSeverity) -> list[ValidationFinding]:
        """Filter findings by severity.

        Args:
            severity: :class:`FindingSeverity` to filter by.

        Returns:
            Matching findings.
        """
        return [f for f in self._findings.values() if f.severity == severity]

    def open_count(self) -> int:
        """Return count of open findings."""
        return sum(1 for f in self._findings.values() if f.status == FindingStatus.OPEN)

    def critical_open_count(self) -> int:
        """Return count of open critical findings."""
        return sum(
            1 for f in self._findings.values()
            if f.status == FindingStatus.OPEN and f.severity == FindingSeverity.CRITICAL
        )

    def has_blocking_findings(self) -> bool:
        """Return True if any open findings require remediation."""
        return any(
            f.status == FindingStatus.OPEN and f.requires_remediation
            for f in self._findings.values()
        )

    def evidence_completeness(self, required_types: list[str]) -> float:
        """Compute evidence completeness as fraction of required types covered.

        Args:
            required_types: List of evidence_type strings that must be present.

        Returns:
            Score 0.0–1.0.
        """
        if not required_types:
            return 1.0
        covered = set(required_types) & {
            f.finding_type for f in self._findings.values()
        }
        return len(covered) / len(required_types)
