"""Candidate version registry.

:class:`CandidateRegistry` manages the lifecycle of :class:`CandidateVersion`
objects for a single run.  Each version is immutable after creation; status
changes produce new :class:`CandidateVersion` instances with ``model_copy``.

Design contract:
    - Returns plain Python values or raises on error.
    - The :class:`~sdk.workflowsdk.service.WorkflowService` wraps results in
      :class:`~sdk.platform_core.schemas.base_result.BaseResult`.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

from sdk.platform_core.schemas.utilities import IDFactory
from sdk.workflowsdk.models import (
    CandidateStatus,
    CandidateType,
    CandidateVersion,
)

logger = logging.getLogger(__name__)


class CandidateRegistry:
    """In-memory registry of :class:`CandidateVersion` objects per run.

    All writes produce new immutable instances; existing records are never
    mutated in place.
    """

    def __init__(self) -> None:
        # candidate_id -> CandidateVersion
        self._by_id: Dict[str, CandidateVersion] = {}
        # stage_name -> ordered list of candidate_ids
        self._by_stage: Dict[str, List[str]] = {}

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def register(
        self,
        *,
        stage_name: str,
        candidate_type: CandidateType,
        run_id: str,
        project_id: str,
        version_label: str = "",
        summary: str = "",
        created_by: str = "",
        artifact_ids: Optional[List[str]] = None,
        metrics: Optional[Dict] = None,
        metadata: Optional[Dict] = None,
    ) -> CandidateVersion:
        """Register a new :class:`CandidateVersion`.

        Args:
            stage_name: Producing MDLC stage.
            candidate_type: :class:`~sdk.workflowsdk.models.CandidateType`.
            run_id: Active run identifier.
            project_id: Owning project identifier.
            version_label: Human-readable label (e.g. ``"v3"``).
            summary: HITL selection UI summary text.
            created_by: Actor ID.
            artifact_ids: Related artifact IDs.
            metrics: KPI dict to display in the selection UI.
            metadata: Arbitrary metadata.

        Returns:
            The newly registered :class:`CandidateVersion`.

        Raises:
            ValueError: If *stage_name*, *run_id*, or *project_id* is empty.
        """
        if not stage_name.strip():
            raise ValueError("stage_name must be non-empty.")
        if not run_id.strip():
            raise ValueError("run_id must be non-empty.")
        if not project_id.strip():
            raise ValueError("project_id must be non-empty.")

        candidate_id = IDFactory.candidate_version_id()
        version = CandidateVersion(
            candidate_id=candidate_id,
            stage_name=stage_name,
            candidate_type=candidate_type,
            run_id=run_id,
            project_id=project_id,
            version_label=version_label,
            summary=summary,
            created_by=created_by,
            created_at=datetime.now(timezone.utc),
            artifact_ids=artifact_ids or [],
            metrics=metrics or {},
            metadata=metadata or {},
            status=CandidateStatus.PENDING_REVIEW,
        )
        self._by_id[candidate_id] = version
        self._by_stage.setdefault(stage_name, []).append(candidate_id)

        logger.debug(
            "Candidate registered: id=%s stage=%s type=%s run=%s",
            candidate_id,
            stage_name,
            candidate_type.value,
            run_id,
        )
        return version

    def _update_status(
        self, candidate_id: str, new_status: CandidateStatus
    ) -> CandidateVersion:
        """Return an updated copy of a :class:`CandidateVersion` with a new status.

        Args:
            candidate_id: Target candidate.
            new_status: New :class:`CandidateStatus`.

        Returns:
            Updated (new) :class:`CandidateVersion` stored in the registry.

        Raises:
            KeyError: If *candidate_id* is not found.
        """
        existing = self._by_id.get(candidate_id)
        if existing is None:
            raise KeyError(f"Candidate '{candidate_id}' not found.")
        updated = existing.model_copy(update={"status": new_status})
        self._by_id[candidate_id] = updated
        return updated

    def mark_selected(self, candidate_id: str) -> CandidateVersion:
        """Mark *candidate_id* as selected and supersede all others in the same stage.

        Args:
            candidate_id: ID of the selected candidate.

        Returns:
            Updated :class:`CandidateVersion` with ``status=SELECTED``.

        Raises:
            KeyError: If *candidate_id* is not found.
        """
        existing = self._by_id.get(candidate_id)
        if existing is None:
            raise KeyError(f"Candidate '{candidate_id}' not found.")

        # Supersede all other candidates in the same stage
        for cid in self._by_stage.get(existing.stage_name, []):
            if cid != candidate_id:
                other = self._by_id.get(cid)
                if other and other.status == CandidateStatus.PENDING_REVIEW:
                    self._by_id[cid] = other.model_copy(
                        update={"status": CandidateStatus.SUPERSEDED}
                    )

        return self._update_status(candidate_id, CandidateStatus.SELECTED)

    def mark_rejected(self, candidate_id: str) -> CandidateVersion:
        """Mark *candidate_id* as rejected.

        Args:
            candidate_id: Target candidate.

        Returns:
            Updated :class:`CandidateVersion`.

        Raises:
            KeyError: If *candidate_id* is not found.
        """
        return self._update_status(candidate_id, CandidateStatus.REJECTED)

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get(self, candidate_id: str) -> CandidateVersion:
        """Retrieve a :class:`CandidateVersion` by ID.

        Args:
            candidate_id: Candidate to retrieve.

        Returns:
            Matching :class:`CandidateVersion`.

        Raises:
            KeyError: If not found.
        """
        result = self._by_id.get(candidate_id)
        if result is None:
            raise KeyError(f"Candidate '{candidate_id}' not found.")
        return result

    def list_for_stage(
        self,
        stage_name: str,
        *,
        status: Optional[CandidateStatus] = None,
    ) -> List[CandidateVersion]:
        """List candidates for *stage_name*, optionally filtered by *status*.

        Args:
            stage_name: MDLC stage to query.
            status: Optional status filter.

        Returns:
            Ordered list of matching :class:`CandidateVersion` objects.
        """
        cids = self._by_stage.get(stage_name, [])
        candidates = [self._by_id[cid] for cid in cids if cid in self._by_id]
        if status is not None:
            candidates = [c for c in candidates if c.status == status]
        return candidates

    def get_selected(self, stage_name: str) -> Optional[CandidateVersion]:
        """Return the selected candidate for *stage_name*, or ``None``.

        Args:
            stage_name: MDLC stage to query.

        Returns:
            :class:`CandidateVersion` with ``status=SELECTED``, or ``None``.
        """
        for c in self.list_for_stage(stage_name):
            if c.status == CandidateStatus.SELECTED:
                return c
        return None
