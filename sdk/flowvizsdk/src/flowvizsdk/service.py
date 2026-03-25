"""flowvizsdk.service -- FlowVizService: assembles FlowGraph from observability events.

The service is a pure assembler: it reads events from the
:class:`~observabilitysdk.service.ObservabilityService` and produces a
:class:`~flowvizsdk.models.FlowGraph` using the builder pipeline.

It does not persist graphs; they are rebuilt on demand (replay-safe).
"""

from __future__ import annotations

import logging
from typing import Any

from flowvizsdk.edge_builder import EdgeBuilder
from flowvizsdk.graph_export import to_dict, to_html, to_json, to_svg
from flowvizsdk.models import FlowGraph, NodeStatus, NodeType
from flowvizsdk.node_builder import NodeBuilder
from flowvizsdk.timeline_builder import TimelineBuilder

logger = logging.getLogger(__name__)


class FlowVizService:
    """Assembles :class:`FlowGraph` objects from observability event logs.

    Args:
        observability_service: :class:`~observabilitysdk.service.ObservabilityService`
            instance.  Any object with a ``get_events_for_run(run_id)`` method that
            returns an iterable of event objects is accepted (duck-typing).
    """

    def __init__(self, observability_service: Any) -> None:
        self._obs = observability_service

    # ------------------------------------------------------------------
    # Graph assembly
    # ------------------------------------------------------------------

    def build_graph(self, run_id: str, project_id: str) -> FlowGraph:
        """Assemble the full flow graph for a run.

        Args:
            run_id: Run identifier.
            project_id: Project identifier.

        Returns:
            Assembled :class:`FlowGraph`.
        """
        result = self._obs.get_events_for_run(run_id)
        events = result.data if hasattr(result, "data") else (result or [])

        node_builder = NodeBuilder(run_id, project_id)
        edge_builder = EdgeBuilder(run_id)
        timeline_builder = TimelineBuilder(run_id, project_id)

        # Sort events by timestamp for deterministic processing.
        sorted_events = sorted(
            events,
            key=lambda e: getattr(e, "timestamp", None) or "",
        )

        for event in sorted_events:
            node_id = node_builder.consume(event)
            edge_builder.consume(event, node_id)
            timeline_builder.consume(event, node_id)

        nodes = node_builder.build_all()
        edges = edge_builder.build_all()
        timeline = timeline_builder.build_sorted()

        graph = FlowGraph(
            run_id=run_id,
            project_id=project_id,
            nodes=nodes,
            edges=edges,
            timeline=timeline,
            event_count=len(sorted_events),
        )

        logger.info(
            "flowviz.graph_built",
            extra={
                "run_id": run_id,
                "node_count": graph.node_count,
                "edge_count": graph.edge_count,
                "event_count": graph.event_count,
            },
        )
        return graph

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------

    def get_stage_summary(self, run_id: str, project_id: str) -> list[dict[str, Any]]:
        """Return a lightweight list of stage node summaries.

        Args:
            run_id: Run identifier.
            project_id: Project identifier.

        Returns:
            List of dicts with keys: stage_name, status, started_at, completed_at,
            duration_seconds, has_governance_gate.
        """
        graph = self.build_graph(run_id, project_id)
        stage_nodes = graph.get_nodes_by_type(NodeType.STAGE)
        return [
            {
                "stage_name": n.stage_name,
                "status": n.status.value,
                "started_at": n.started_at.isoformat() if n.started_at else None,
                "completed_at": n.completed_at.isoformat() if n.completed_at else None,
                "duration_seconds": n.duration_seconds,
                "has_governance_gate": any(
                    e.to_node_id == n.node_id or e.from_node_id == n.node_id
                    for e in graph.edges.values()
                    if graph.nodes.get(
                        e.to_node_id if e.from_node_id == n.node_id else e.from_node_id,
                        FlowGraph.__fields_set__,  # type: ignore[arg-type]
                    )
                ),
            }
            for n in stage_nodes
        ]

    def get_governance_gate_summary(self, run_id: str, project_id: str) -> list[dict[str, Any]]:
        """Return all governance gate nodes for a run.

        Args:
            run_id: Run identifier.
            project_id: Project identifier.

        Returns:
            List of dicts describing governance gate nodes.
        """
        graph = self.build_graph(run_id, project_id)
        return [
            {
                "node_id": n.node_id,
                "label": n.label,
                "stage_name": n.stage_name,
                "status": n.status.value,
                "node_type": n.node_type.value,
                "actor_id": n.actor_id,
            }
            for n in graph.nodes.values()
            if n.is_governance_gate
        ]

    def get_failure_nodes(self, run_id: str, project_id: str) -> list[dict[str, Any]]:
        """Return all failed nodes for a run.

        Args:
            run_id: Run identifier.
            project_id: Project identifier.

        Returns:
            List of dicts describing failed nodes.
        """
        graph = self.build_graph(run_id, project_id)
        return [
            {
                "node_id": n.node_id,
                "label": n.label,
                "stage_name": n.stage_name,
                "actor_id": n.actor_id,
            }
            for n in graph.get_nodes_by_status(NodeStatus.FAILED)
        ]

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_json(self, run_id: str, project_id: str, indent: int = 2) -> str:
        """Export the flow graph for a run as JSON.

        Args:
            run_id: Run identifier.
            project_id: Project identifier.
            indent: JSON indentation. Default: 2.

        Returns:
            JSON string.
        """
        graph = self.build_graph(run_id, project_id)
        return to_json(graph, indent=indent)

    def export_html(self, run_id: str, project_id: str) -> str:
        """Export the flow graph for a run as self-contained HTML.

        Args:
            run_id: Run identifier.
            project_id: Project identifier.

        Returns:
            HTML string.
        """
        graph = self.build_graph(run_id, project_id)
        return to_html(graph, title=f"MDLC Flow Graph -- {run_id}")

    def export_svg(self, run_id: str, project_id: str) -> str:
        """Export the flow graph for a run as SVG.

        Args:
            run_id: Run identifier.
            project_id: Project identifier.

        Returns:
            SVG string.
        """
        graph = self.build_graph(run_id, project_id)
        return to_svg(graph)

    def health_check(self) -> dict[str, Any]:
        """Return health status of the service.

        Returns:
            Dict with ``status`` key.
        """
        return {"status": "ok", "service": "FlowVizService"}
