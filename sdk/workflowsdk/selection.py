"""Version selection registry.

:class:`SelectionRegistry` records and queries :class:`VersionSelection`
decisions made by HITL actors.  Each selection is immutable; superseding a
selection produces a new record.

Design contract:
    - Returns plain Python values or raises on error.
    - The :class:`~sdk.workflowsdk.service.WorkflowService` wraps results in
      :class:`~sdk.platform_core.schemas.base_result.BaseResult`.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

from sdk.platform_core.schemas.utilities import IDFactory
from sdk.workflowsdk.models import (
    ReviewType,
    SelectionStatus,
    VersionSelection,
)

logger = logging.getLogger(__name__)


class SelectionRegistry:
    """In-memory registry of :class:`VersionSelection` records per run."""

    def __init__(self) -> None:
        # selection_id -> VersionSelection
        self._by_id: Dict[str, VersionSelection] = {}
        # stage_name -> ordered list of selection_ids (most recent last)
        self._by_stage: Dict[str, List[str]] = {}

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def record_selection(
        self,
        *,
        stage_name: str,
        run_id: str,
        project_id: str,
        selected_candidate_id: str,
        selected_by: str,
        rationale: str = "",
        audit_id: str = "",
        review_type: ReviewType = ReviewType.GENERIC,
        conditions: Optional[List[str]] = None,
    ) -> VersionSelection:
        """Record a new version selection.

        Supersedes any previously ``ACTIVE`` selection for the same stage.

        Args:
            stage_name: Stage the selection applies to.
            run_id: Active run.
            project_id: Owning project.
            selected_candidate_id: ID of the chosen :class:`CandidateVersion`.
            selected_by: Actor ID.
            rationale: Decision rationale.
            audit_id: Linked audit record ID.
            review_type: Review context type.
            conditions: Approval conditions list.

        Returns:
            Newly created :class:`VersionSelection`.

        Raises:
            ValueError: If mandatory fields are empty.
        """
        for field_name, value in [
            ("stage_name", stage_name),
            ("run_id", run_id),
            ("project_id", project_id),
            ("selected_candidate_id", selected_candidate_id),
            ("selected_by", selected_by),
        ]:
            if not str(value).strip():
                raise ValueError(f"'{field_name}' must be non-empty.")

        # Supersede previous active selection for this stage
        for sid in self._by_stage.get(stage_name, []):
            prev = self._by_id.get(sid)
            if prev and prev.status == SelectionStatus.ACTIVE:
                self._by_id[sid] = prev.model_copy(
                    update={"status": SelectionStatus.SUPERSEDED}
                )

        selection_id = IDFactory.selection_id()
        selection = VersionSelection(
            selection_id=selection_id,
            stage_name=stage_name,
            run_id=run_id,
            project_id=project_id,
            selected_candidate_id=selected_candidate_id,
            selected_by=selected_by,
            selected_at=datetime.now(timezone.utc),
            rationale=rationale,
            audit_id=audit_id,
            review_type=review_type,
            conditions=conditions or [],
            status=SelectionStatus.ACTIVE,
        )
        self._by_id[selection_id] = selection
        self._by_stage.setdefault(stage_name, []).append(selection_id)

        logger.debug(
            "Selection recorded: id=%s stage=%s candidate=%s by=%s",
            selection_id,
            stage_name,
            selected_candidate_id,
            selected_by,
        )
        return selection

    def revoke(self, selection_id: str, reason: str = "") -> VersionSelection:
        """Revoke a selection by setting its status to ``REVOKED``.

        Args:
            selection_id: Selection to revoke.
            reason: Revocation reason (logged only).

        Returns:
            Updated :class:`VersionSelection`.

        Raises:
            KeyError: If *selection_id* is not found.
            ValueError: If the selection is not currently ``ACTIVE``.
        """
        sel = self._by_id.get(selection_id)
        if sel is None:
            raise KeyError(f"Selection '{selection_id}' not found.")
        if sel.status != SelectionStatus.ACTIVE:
            raise ValueError(
                f"Selection '{selection_id}' cannot be revoked "
                f"(current status: {sel.status.value})."
            )
        updated = sel.model_copy(update={"status": SelectionStatus.REVOKED})
        self._by_id[selection_id] = updated
        logger.info(
            "Selection revoked: id=%s stage=%s reason=%s",
            selection_id,
            sel.stage_name,
            reason or "(no reason given)",
        )
        return updated

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get(self, selection_id: str) -> VersionSelection:
        """Retrieve a :class:`VersionSelection` by ID.

        Args:
            selection_id: Target selection.

        Returns:
            Matching :class:`VersionSelection`.

        Raises:
            KeyError: If not found.
        """
        sel = self._by_id.get(selection_id)
        if sel is None:
            raise KeyError(f"Selection '{selection_id}' not found.")
        return sel

    def active_for_stage(self, stage_name: str) -> Optional[VersionSelection]:
        """Return the currently active selection for *stage_name*, or ``None``.

        Args:
            stage_name: MDLC stage to query.

        Returns:
            :class:`VersionSelection` with ``status=ACTIVE`` or ``None``.
        """
        for sid in reversed(self._by_stage.get(stage_name, [])):
            sel = self._by_id.get(sid)
            if sel and sel.status == SelectionStatus.ACTIVE:
                return sel
        return None

    def stages_with_active_selection(self) -> Set[str]:
        """Return the set of stage names that have an active selection.

        Returns:
            Set of stage name strings.
        """
        return {
            stage
            for stage in self._by_stage
            if self.active_for_stage(stage) is not None
        }

    def list_for_stage(self, stage_name: str) -> List[VersionSelection]:
        """Return all selections for *stage_name* in chronological order.

        Args:
            stage_name: MDLC stage to query.

        Returns:
            Ordered list of :class:`VersionSelection` objects.
        """
        sids = self._by_stage.get(stage_name, [])
        return [self._by_id[sid] for sid in sids if sid in self._by_id]
