"""Append-only HITL review store.

Reviews are immutable records. Status transitions produce new immutable
records replacing the old entry. The store maintains full history via
a ``_history`` log per review_id.

Design contract:
    - Returns plain Python values or raises on error.
    - The :class:`~sdk.hitlsdk.service.HITLService` wraps results in
      :class:`~sdk.platform_core.schemas.base_result.BaseResult`.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Dict, List, Optional

from sdk.hitlsdk.models import ReviewRecord, ReviewStatus

logger = logging.getLogger(__name__)


class ReviewStore:
    """In-memory review store with full history per review.

    Args: none
    """

    def __init__(self) -> None:
        # Current (latest) record per review_id.
        self._current: Dict[str, ReviewRecord] = {}
        # Full history: review_id -> ordered list of record snapshots.
        self._history: Dict[str, List[ReviewRecord]] = defaultdict(list)
        # run_id -> [review_ids]
        self._idx_run: Dict[str, List[str]] = defaultdict(list)
        # stage_name -> [review_ids]
        self._idx_stage: Dict[str, List[str]] = defaultdict(list)

    def put(self, record: ReviewRecord) -> None:
        """Insert or replace the current review record and append to history.

        Args:
            record: New or updated :class:`ReviewRecord`.
        """
        is_new = record.review_id not in self._current
        self._current[record.review_id] = record
        self._history[record.review_id].append(record)
        if is_new:
            self._idx_run[record.run_id].append(record.review_id)
            self._idx_stage[record.stage_name].append(record.review_id)
        logger.debug(
            "review_store.put: review_id=%s status=%s",
            record.review_id,
            record.status,
        )

    def get(self, review_id: str) -> Optional[ReviewRecord]:
        """Return the current (latest) record for a review ID, or None."""
        return self._current.get(review_id)

    def get_or_raise(self, review_id: str) -> ReviewRecord:
        """Return the current record for a review ID.

        Args:
            review_id: Target review.

        Returns:
            Matching :class:`ReviewRecord`.

        Raises:
            KeyError: If *review_id* is not found.
        """
        rec = self._current.get(review_id)
        if rec is None:
            raise KeyError(f"Review '{review_id}' not found.")
        return rec

    def get_history(self, review_id: str) -> List[ReviewRecord]:
        """Return all historical snapshots for a review ID.

        Args:
            review_id: Review identifier.

        Returns:
            Ordered list of all :class:`ReviewRecord` snapshots (oldest first).
        """
        return list(self._history.get(review_id, []))

    def list_for_run(
        self,
        run_id: str,
        status: Optional[ReviewStatus] = None,
    ) -> List[ReviewRecord]:
        """List all reviews for a run, optionally filtered by status.

        Args:
            run_id: Run identifier.
            status: Filter by review status.

        Returns:
            List of current :class:`ReviewRecord` objects.
        """
        ids = self._idx_run.get(run_id, [])
        records = [self._current[rid] for rid in ids if rid in self._current]
        if status is not None:
            records = [r for r in records if r.status == status]
        return records

    def list_for_stage(self, stage_name: str) -> List[ReviewRecord]:
        """List all reviews for a stage.

        Args:
            stage_name: Stage name.

        Returns:
            List of current :class:`ReviewRecord` objects.
        """
        ids = self._idx_stage.get(stage_name, [])
        return [self._current[rid] for rid in ids if rid in self._current]

    def has_open_review(self, run_id: str, stage_name: str) -> bool:
        """Return True if there is an open (pending) review for the run/stage.

        Args:
            run_id: Run identifier.
            stage_name: Stage name.

        Returns:
            True when at least one PENDING_REVIEW record exists.
        """
        for record in self.list_for_run(run_id, status=ReviewStatus.PENDING_REVIEW):
            if record.stage_name == stage_name:
                return True
        return False
