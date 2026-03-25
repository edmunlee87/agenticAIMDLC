"""Checkpoint and recovery management.

:class:`CheckpointManager` saves serialised :class:`WorkflowState` snapshots.
:class:`RecoveryManager` analyses the current workflow state and recommends
a :class:`~sdk.workflowsdk.models.RecoveryPath` when a stage fails.

Design contract:
    - Returns plain Python values or raises on error.
    - The :class:`~sdk.workflowsdk.service.WorkflowService` wraps results in
      :class:`~sdk.platform_core.schemas.base_result.BaseResult`.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from sdk.platform_core.schemas.enums import StageStatusEnum
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider
from sdk.workflowsdk.models import (
    CheckpointRecord,
    RecoveryPath,
    WorkflowState,
)

logger = logging.getLogger(__name__)

# Retry threshold: recommend RERUN instead of RETRY after this many attempts
_MAX_RETRY_ATTEMPTS = 3


class CheckpointManager:
    """Serialises and stores :class:`WorkflowState` snapshots per run.

    Args:
        max_checkpoints_per_run: If > 0, keep only the N most recent valid
            checkpoints per run (older ones are invalidated, not deleted).
    """

    def __init__(self, max_checkpoints_per_run: int = 10) -> None:
        self._max = max_checkpoints_per_run
        # run_id -> ordered list of checkpoint_ids
        self._by_run: Dict[str, List[str]] = {}
        # checkpoint_id -> CheckpointRecord
        self._by_id: Dict[str, CheckpointRecord] = {}

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def save(
        self,
        state: WorkflowState,
        *,
        session_id: str = "",
    ) -> CheckpointRecord:
        """Serialise *state* and store a new :class:`CheckpointRecord`.

        Args:
            state: Current workflow state to snapshot.
            session_id: Active session ID at checkpoint time.

        Returns:
            Newly created :class:`CheckpointRecord`.
        """
        checkpoint_id = IDFactory.checkpoint_id()
        state_json = state.model_dump_json()
        record = CheckpointRecord(
            checkpoint_id=checkpoint_id,
            run_id=state.run_id,
            project_id=state.project_id,
            session_id=session_id,
            taken_at=TimeProvider.now(),
            stage_name=state.current_stage,
            event_count=state.event_count,
            last_event_id=state.last_event_id,
            state_json=state_json,
            is_valid=True,
        )
        self._by_id[checkpoint_id] = record
        run_cids = self._by_run.setdefault(state.run_id, [])
        run_cids.append(checkpoint_id)

        # Enforce max checkpoints — invalidate (not delete) oldest excess
        if self._max > 0 and len(run_cids) > self._max:
            excess = len(run_cids) - self._max
            for old_cid in run_cids[:excess]:
                old = self._by_id.get(old_cid)
                if old and old.is_valid:
                    self._by_id[old_cid] = old.model_copy(update={"is_valid": False})

        logger.debug(
            "Checkpoint saved: id=%s run=%s stage=%s events=%d",
            checkpoint_id,
            state.run_id,
            state.current_stage,
            state.event_count,
        )
        return record

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get(self, checkpoint_id: str) -> CheckpointRecord:
        """Return a :class:`CheckpointRecord` by ID.

        Args:
            checkpoint_id: Target checkpoint.

        Returns:
            Matching :class:`CheckpointRecord`.

        Raises:
            KeyError: If not found.
        """
        record = self._by_id.get(checkpoint_id)
        if record is None:
            raise KeyError(f"Checkpoint '{checkpoint_id}' not found.")
        return record

    def latest_valid(self, run_id: str) -> Optional[CheckpointRecord]:
        """Return the most recent valid checkpoint for *run_id*, or ``None``.

        Args:
            run_id: Run to query.

        Returns:
            Most recent valid :class:`CheckpointRecord` or ``None``.
        """
        for cid in reversed(self._by_run.get(run_id, [])):
            record = self._by_id.get(cid)
            if record and record.is_valid:
                return record
        return None

    def list_for_run(self, run_id: str) -> List[CheckpointRecord]:
        """Return all checkpoints for *run_id* in chronological order.

        Args:
            run_id: Run to query.

        Returns:
            Ordered list of :class:`CheckpointRecord` objects.
        """
        cids = self._by_run.get(run_id, [])
        return [self._by_id[cid] for cid in cids if cid in self._by_id]


# ---------------------------------------------------------------------------
# RecoveryManager
# ---------------------------------------------------------------------------


class RecoveryManager:
    """Analyses failed workflow state and recommends a recovery path.

    The recommendation logic is intentionally simple and config-free — the
    caller (e.g. HITL agent) can override the recommendation.  All reasoning
    is deterministic.
    """

    def recommend(
        self,
        state: WorkflowState,
        *,
        failed_stage: str,
        error_type: str = "*",
    ) -> RecoveryPath:
        """Recommend a :class:`RecoveryPath` for a failed stage.

        Decision table:
        - Stage has never started → ``RERUN``
        - Stage attempt count exceeds ``_MAX_RETRY_ATTEMPTS`` → ``ROLLBACK``
        - Stage has attempt count 1-3 → ``RETRY``
        - Stage was previously completed (regression?) → ``RESUME``

        Args:
            state: Current replayed :class:`WorkflowState`.
            failed_stage: Name of the stage that failed.
            error_type: Error type code (reserved for future routing rules).

        Returns:
            Recommended :class:`RecoveryPath`.
        """
        stage_rec = state.stages.get(failed_stage)
        if stage_rec is None:
            logger.debug(
                "RecoveryManager: stage '%s' not in state — recommending RERUN.",
                failed_stage,
            )
            return RecoveryPath.RERUN

        if stage_rec.status == StageStatusEnum.COMPLETED:
            logger.debug(
                "RecoveryManager: stage '%s' was previously completed — recommending RESUME.",
                failed_stage,
            )
            return RecoveryPath.RESUME

        if stage_rec.attempt_count > _MAX_RETRY_ATTEMPTS:
            logger.debug(
                "RecoveryManager: stage '%s' exceeded %d attempts — recommending ROLLBACK.",
                failed_stage,
                _MAX_RETRY_ATTEMPTS,
            )
            return RecoveryPath.ROLLBACK

        logger.debug(
            "RecoveryManager: stage '%s' attempt %d — recommending RETRY.",
            failed_stage,
            stage_rec.attempt_count,
        )
        return RecoveryPath.RETRY

    def describe(self, path: RecoveryPath) -> str:
        """Return a human-readable description of *path* for the HITL UI.

        Args:
            path: :class:`RecoveryPath` to describe.

        Returns:
            Short description string.
        """
        descriptions = {
            RecoveryPath.RETRY: (
                "Re-attempt the failed stage with the same configuration."
            ),
            RecoveryPath.RERUN: (
                "Re-run the stage from scratch, discarding partial outputs."
            ),
            RecoveryPath.ROLLBACK: (
                "Rollback to the most recent valid checkpoint and restart from there."
            ),
            RecoveryPath.RESUME: (
                "Resume the stage from the last known good state."
            ),
        }
        return descriptions.get(path, path.value)
