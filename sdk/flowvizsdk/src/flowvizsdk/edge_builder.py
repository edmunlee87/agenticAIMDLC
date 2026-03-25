"""flowvizsdk.edge_builder -- constructs FlowEdges from observability events.

Edges are created by tracking stage sequence (transition events) and explicit
routing events.  Failure and recovery edges are flagged separately for rendering.
"""

from __future__ import annotations

import logging
from typing import Any

from flowvizsdk.models import FlowEdge

logger = logging.getLogger(__name__)


class EdgeBuilder:
    """Derives directed edges from observability events.

    Strategy:
    - ``workflow.stage.started`` after another ``workflow.stage.completed``
      creates a NORMAL edge between the two stage nodes.
    - ``workflow.stage.failed`` creates a FAILURE edge from the current stage.
    - ``workflow.recovery.applied`` creates a RECOVERY edge back to the
      restored stage.
    - ``hitl.review.created`` creates an edge from the triggering stage to
      the HITL gate node.
    - ``hitl.review.approved`` / ``hitl.review.rejected`` creates an edge from
      the HITL gate back to the stage (or next stage).
    - ``policy.breach.detected`` creates an edge from stage → policy node.

    Args:
        run_id: The run being visualized.
    """

    def __init__(self, run_id: str) -> None:
        self._run_id = run_id
        self._edges: dict[str, FlowEdge] = {}
        self._last_completed_stage_node: str | None = None
        self._stage_node_map: dict[str, str] = {}  # stage_name -> node_id
        self._edge_counter: int = 0

    def consume(self, event: Any, node_id: str | None) -> None:
        """Derive zero or more edges from a single event.

        Args:
            event: :class:`~observabilitysdk.models.ObservabilityEvent`.
            node_id: The node_id produced by :class:`~flowvizsdk.node_builder.NodeBuilder`
                for this event (None if unmapped).
        """
        if node_id is None:
            return

        event_type: str = getattr(event, "event_type", "") or ""
        stage_name: str = getattr(event, "stage_name", "") or ""
        event_id: str = getattr(event, "event_id", "") or ""
        metadata: dict[str, Any] = dict(getattr(event, "metadata", {}) or {})

        if event_type == "workflow.stage.started":
            self._stage_node_map[stage_name] = node_id
            if self._last_completed_stage_node and self._last_completed_stage_node != node_id:
                self._add_edge(
                    from_node=self._last_completed_stage_node,
                    to_node=node_id,
                    label="next",
                    triggered_by=event_id,
                )

        elif event_type == "workflow.stage.completed":
            self._last_completed_stage_node = node_id

        elif event_type == "workflow.stage.failed":
            # Failure marker -- edge will be added when recovery appears
            pass

        elif event_type == "hitl.review.created":
            triggering_stage = metadata.get("stage_name", stage_name)
            triggering_node = self._stage_node_map.get(triggering_stage)
            if triggering_node and triggering_node != node_id:
                self._add_edge(
                    from_node=triggering_node,
                    to_node=node_id,
                    label="requires review",
                    triggered_by=event_id,
                )

        elif event_type in {"hitl.review.approved", "hitl.review.rejected"}:
            outcome = "approved" if event_type.endswith("approved") else "rejected"
            stage_node = self._stage_node_map.get(stage_name)
            if stage_node and stage_node != node_id:
                self._add_edge(
                    from_node=node_id,
                    to_node=stage_node,
                    label=outcome,
                    triggered_by=event_id,
                )

        elif event_type == "workflow.recovery.applied":
            restored_stage = metadata.get("restored_stage", stage_name)
            restored_node = self._stage_node_map.get(restored_stage)
            if restored_node:
                self._add_edge(
                    from_node=node_id,
                    to_node=restored_node,
                    label="recovered",
                    triggered_by=event_id,
                    is_recovery=True,
                )

        elif event_type == "policy.breach.detected":
            stage_node = self._stage_node_map.get(stage_name)
            if stage_node and stage_node != node_id:
                self._add_edge(
                    from_node=stage_node,
                    to_node=node_id,
                    label="policy breach",
                    triggered_by=event_id,
                    is_failure=True,
                )

    def build_all(self) -> dict[str, FlowEdge]:
        """Return all accumulated edges.

        Returns:
            Dict mapping edge_id -> :class:`FlowEdge`.
        """
        return dict(self._edges)

    # ------------------------------------------------------------------

    def _add_edge(
        self,
        from_node: str,
        to_node: str,
        label: str = "",
        triggered_by: str = "",
        is_failure: bool = False,
        is_recovery: bool = False,
    ) -> None:
        self._edge_counter += 1
        edge_id = f"edge__{self._run_id}__{self._edge_counter:04d}"
        # Deduplicate on (from, to, label).
        dedup_key = f"{from_node}__{to_node}__{label}"
        if dedup_key in {f"{e.from_node_id}__{e.to_node_id}__{e.label}" for e in self._edges.values()}:
            return
        self._edges[edge_id] = FlowEdge(
            edge_id=edge_id,
            from_node_id=from_node,
            to_node_id=to_node,
            label=label,
            is_failure_path=is_failure,
            is_recovery_path=is_recovery,
            triggered_by_event_id=triggered_by,
        )
