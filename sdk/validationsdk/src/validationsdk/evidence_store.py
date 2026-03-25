"""validationsdk.evidence_store -- stores and queries evidence records.

Evidence records are immutable once submitted.  The store maintains indexes
by scope, stage, and evidence type for fast lookup.
"""

from __future__ import annotations

import logging

from validationsdk.models import EvidenceRecord

logger = logging.getLogger(__name__)


class EvidenceStore:
    """In-memory evidence store for a validation scope.

    Args:
        scope_id: The validation scope this store belongs to.
    """

    def __init__(self, scope_id: str) -> None:
        self._scope_id = scope_id
        self._records: dict[str, EvidenceRecord] = {}
        self._by_type: dict[str, list[str]] = {}
        self._by_stage: dict[str, list[str]] = {}

    def submit(self, record: EvidenceRecord) -> None:
        """Submit a new evidence record.

        Args:
            record: :class:`EvidenceRecord` to store.

        Raises:
            ValueError: If evidence_id already exists or scope_id mismatches.
        """
        if record.evidence_id in self._records:
            raise ValueError(f"Evidence '{record.evidence_id}' already submitted.")
        if record.scope_id != self._scope_id:
            raise ValueError(
                f"Evidence scope_id '{record.scope_id}' does not match store scope '{self._scope_id}'."
            )
        self._records[record.evidence_id] = record
        self._by_type.setdefault(record.evidence_type, []).append(record.evidence_id)
        self._by_stage.setdefault(record.stage_name, []).append(record.evidence_id)
        logger.info(
            "evidence_store.submitted",
            extra={
                "evidence_id": record.evidence_id,
                "evidence_type": record.evidence_type,
                "scope_id": self._scope_id,
            },
        )

    def get(self, evidence_id: str) -> EvidenceRecord:
        """Retrieve evidence by ID.

        Args:
            evidence_id: Evidence identifier.

        Returns:
            :class:`EvidenceRecord`.

        Raises:
            KeyError: If not found.
        """
        return self._records[evidence_id]

    def list_all(self) -> list[EvidenceRecord]:
        """Return all evidence records.

        Returns:
            List of :class:`EvidenceRecord`.
        """
        return list(self._records.values())

    def list_by_type(self, evidence_type: str) -> list[EvidenceRecord]:
        """Return evidence of a specific type.

        Args:
            evidence_type: Type string to filter by.

        Returns:
            List of :class:`EvidenceRecord`.
        """
        ids = self._by_type.get(evidence_type, [])
        return [self._records[i] for i in ids if i in self._records]

    def list_by_stage(self, stage_name: str) -> list[EvidenceRecord]:
        """Return evidence from a specific stage.

        Args:
            stage_name: Stage name to filter by.

        Returns:
            List of :class:`EvidenceRecord`.
        """
        ids = self._by_stage.get(stage_name, [])
        return [self._records[i] for i in ids if i in self._records]

    def covered_types(self) -> set[str]:
        """Return the set of evidence types currently covered.

        Returns:
            Set of evidence type strings.
        """
        return set(self._by_type.keys())

    def completeness(self, required_types: list[str]) -> float:
        """Compute completeness as fraction of required types covered.

        Args:
            required_types: List of mandatory evidence type strings.

        Returns:
            Score 0.0–1.0.
        """
        if not required_types:
            return 1.0
        covered = self.covered_types() & set(required_types)
        return len(covered) / len(required_types)
