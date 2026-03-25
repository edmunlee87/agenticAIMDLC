"""Workflow routing engine.

:class:`RoutingEngine` resolves the next stage given the current stage and a
named outcome (``on_success``, ``on_fail``, etc.) using the
:class:`~sdk.platform_core.runtime.config_models.routes.WorkflowRoutesConfig`
embedded in the :class:`~sdk.platform_core.runtime.config_models.bundle.RuntimeConfigBundle`.

Design contract:
    - Return plain Python values or raise on error.
    - The :class:`~sdk.workflowsdk.service.WorkflowService` wraps results in
      :class:`~sdk.platform_core.schemas.base_result.BaseResult`.
"""

from __future__ import annotations

import logging
from typing import List, Optional

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.config_models.routes import (
    FailureRouteEntry,
    WorkflowRouteDefinition,
)

logger = logging.getLogger(__name__)

# All transition outcomes supported by WorkflowRouteDefinition
_OUTCOME_ATTRS = (
    "on_success",
    "on_review_required",
    "on_pass",
    "on_fail",
    "on_approved",
    "on_rejected",
    "on_auto_continue",
    "on_remediation_required",
)


class RoutingEngine:
    """Resolves stage transitions from the config-driven route map.

    Args:
        bundle: Fully validated :class:`RuntimeConfigBundle`.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._routes = bundle.workflow_routes.routes
        self._failure_routes = bundle.failure_routes.routes if bundle.failure_routes else {}

    # ------------------------------------------------------------------
    # Success / outcome routing
    # ------------------------------------------------------------------

    def next_stage(
        self, current_stage: str, outcome: str = "on_success"
    ) -> Optional[str]:
        """Return the next stage name for *current_stage* and *outcome*.

        Args:
            current_stage: The stage the workflow is currently in.
            outcome: Transition outcome key (default ``"on_success"``).
                Must be one of: ``on_success``, ``on_review_required``,
                ``on_pass``, ``on_fail``, ``on_approved``, ``on_rejected``,
                ``on_auto_continue``, ``on_remediation_required``.

        Returns:
            Next stage name, or ``None`` if the stage is terminal or the
            outcome is not configured.

        Raises:
            ValueError: If *outcome* is not a known outcome key.
        """
        if outcome not in _OUTCOME_ATTRS:
            raise ValueError(
                f"Unknown outcome '{outcome}'. "
                f"Must be one of: {sorted(_OUTCOME_ATTRS)}."
            )

        route: Optional[WorkflowRouteDefinition] = self._routes.get(current_stage)
        if route is None:
            logger.debug(
                "RoutingEngine: no route configured for stage '%s'.", current_stage
            )
            return None

        target = getattr(route, outcome, None)
        if target is None:
            logger.debug(
                "RoutingEngine: outcome '%s' not configured for stage '%s'.",
                outcome,
                current_stage,
            )
        return target

    def get_route_definition(
        self, stage_name: str
    ) -> Optional[WorkflowRouteDefinition]:
        """Return the full :class:`WorkflowRouteDefinition` for *stage_name*.

        Args:
            stage_name: Stage to look up.

        Returns:
            Matching :class:`WorkflowRouteDefinition` or ``None``.
        """
        return self._routes.get(stage_name)

    # ------------------------------------------------------------------
    # Failure routing
    # ------------------------------------------------------------------

    def failure_routes_for(self, stage_name: str) -> List[FailureRouteEntry]:
        """Return all configured failure routes for *stage_name*.

        Args:
            stage_name: Stage to look up.

        Returns:
            List of :class:`FailureRouteEntry` objects (empty if none configured).
        """
        return list(self._failure_routes.get(stage_name, []))

    def failure_target(
        self, stage_name: str, error_type: str = "*"
    ) -> Optional[str]:
        """Resolve the failure target stage for *stage_name* and *error_type*.

        Prefers an exact match on ``error_type``; falls back to the catch-all
        ``"*"`` route if no exact match exists.

        Args:
            stage_name: Stage that failed.
            error_type: Error type code (default ``"*"``).

        Returns:
            Target stage name from the failure route, or ``None``.
        """
        entries = self.failure_routes_for(stage_name)
        catchall: Optional[str] = None

        for entry in entries:
            if entry.error_type == error_type:
                return entry.target_stage
            if entry.error_type == "*":
                catchall = entry.target_stage

        return catchall

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def all_routed_stages(self) -> List[str]:
        """Return all stage names that have a route definition."""
        return list(self._routes.keys())
