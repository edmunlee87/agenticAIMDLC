"""Stage registry loader and transition guard.

:class:`StageRegistryLoader` reads the :class:`RuntimeConfigBundle` and exposes
convenient stage-level queries.  :class:`TransitionGuard` enforces that every
stage transition is valid before the workflow engine proceeds.

Design contract:
    - Return plain Python values or raise on error.
    - The :class:`~sdk.workflowsdk.service.WorkflowService` wraps results in
      :class:`~sdk.platform_core.schemas.base_result.BaseResult`.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.config_models.stages import StageDefinition
from sdk.platform_core.schemas.enums import StageStatusEnum
from sdk.workflowsdk.models import BlockReason, WorkflowState

logger = logging.getLogger(__name__)


class StageRegistryLoader:
    """Wraps :class:`RuntimeConfigBundle` for stage-level queries.

    Args:
        bundle: The fully validated :class:`RuntimeConfigBundle`.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._bundle = bundle
        # Eager index: stage_name -> StageDefinition
        self._stages: Dict[str, StageDefinition] = dict(bundle.stage_registry.stages)

    # ------------------------------------------------------------------
    # Stage lookup
    # ------------------------------------------------------------------

    def get(self, stage_name: str) -> StageDefinition:
        """Return the :class:`StageDefinition` for *stage_name*.

        Args:
            stage_name: Canonical stage identifier.

        Returns:
            Matching :class:`StageDefinition`.

        Raises:
            KeyError: If *stage_name* is not found in the registry.
        """
        try:
            return self._stages[stage_name]
        except KeyError:
            raise KeyError(
                f"Stage '{stage_name}' is not defined in the stage registry."
            )

    def exists(self, stage_name: str) -> bool:
        """Return ``True`` if *stage_name* is registered."""
        return stage_name in self._stages

    def all_stage_names(self) -> List[str]:
        """Return all registered stage names in insertion order."""
        return list(self._stages.keys())

    def terminal_stages(self) -> List[str]:
        """Return all stage names where ``is_terminal=True``."""
        return [name for name, s in self._stages.items() if s.is_terminal]

    def stages_requiring_review(self) -> List[str]:
        """Return all stage names where ``requires_review=True``."""
        return [name for name, s in self._stages.items() if s.requires_review]

    # ------------------------------------------------------------------
    # Precondition helpers
    # ------------------------------------------------------------------

    def required_prior_stages(self, stage_name: str) -> List[str]:
        """Return the list of stages that must be completed before *stage_name*.

        Args:
            stage_name: Target stage.

        Returns:
            List of prerequisite stage names (empty if none configured).
        """
        if self._bundle.stage_preconditions is None:
            return []
        entry = self._bundle.stage_preconditions.preconditions.get(stage_name)
        if entry is None:
            return []
        return list(entry.required_prior_stages)

    def required_selection_stages(self, stage_name: str) -> List[str]:
        """Return stages that must have an active :class:`VersionSelection`
        before *stage_name* can begin.

        Args:
            stage_name: Target stage.

        Returns:
            List of stage names.
        """
        if self._bundle.stage_preconditions is None:
            return []
        entry = self._bundle.stage_preconditions.preconditions.get(stage_name)
        if entry is None:
            return []
        return list(entry.required_selection_stages)


# ---------------------------------------------------------------------------
# TransitionGuard
# ---------------------------------------------------------------------------


class TransitionGuard:
    """Validates that a stage transition is permissible.

    Checks:
    1. Target stage must exist in the registry.
    2. All required prior stages must be ``COMPLETED`` or ``SKIPPED`` in state.
    3. Stages requiring selection must have a resolved candidate in state.
    4. Terminal stages cannot have a successor.

    Args:
        registry: A loaded :class:`StageRegistryLoader`.
    """

    def __init__(self, registry: StageRegistryLoader) -> None:
        self._registry = registry

    def validate(
        self,
        *,
        target_stage: str,
        state: WorkflowState,
        selected_candidate_stages: Optional[Set[str]] = None,
    ) -> Optional[BlockReason]:
        """Validate the transition to *target_stage* given *state*.

        Args:
            target_stage: Stage to transition into.
            state: Current :class:`WorkflowState` (event-replayed).
            selected_candidate_stages: Set of stage names where a
                :class:`VersionSelection` currently exists (used to check
                ``required_selection_stages``).

        Returns:
            ``None`` if the transition is valid.
            :class:`~sdk.workflowsdk.models.BlockReason` enum member if blocked.
        """
        if not self._registry.exists(target_stage):
            logger.warning("TransitionGuard: unknown target stage '%s'.", target_stage)
            return BlockReason.INVALID_TRANSITION

        # Check required prior stages are completed/skipped
        completed_statuses: set = {StageStatusEnum.COMPLETED, StageStatusEnum.SKIPPED}
        for prereq in self._registry.required_prior_stages(target_stage):
            stage_rec = state.stages.get(prereq)
            if stage_rec is None or stage_rec.status not in completed_statuses:
                logger.debug(
                    "TransitionGuard blocked: prerequisite '%s' not completed "
                    "(required before '%s').",
                    prereq,
                    target_stage,
                )
                return BlockReason.PREREQUISITE_NOT_MET

        # Check required selection stages
        _selected = selected_candidate_stages or set()
        for sel_stage in self._registry.required_selection_stages(target_stage):
            if sel_stage not in _selected:
                logger.debug(
                    "TransitionGuard blocked: selection missing for stage '%s' "
                    "(required before '%s').",
                    sel_stage,
                    target_stage,
                )
                return BlockReason.SELECTION_MISSING

        return None  # transition is valid
