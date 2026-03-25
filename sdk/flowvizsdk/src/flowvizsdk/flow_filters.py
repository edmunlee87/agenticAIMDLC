"""flowvizsdk.flow_filters -- filter and slice FlowGraph views.

Filters are composable predicates applied to nodes, edges, and timeline
entries.  They return new :class:`~flowvizsdk.models.FlowGraph` instances
(immutable), never mutating the original.
"""

from __future__ import annotations

from datetime import datetime
from typing import Callable

from flowvizsdk.models import FlowEdge, FlowGraph, FlowNode, NodeStatus, NodeType, TimelineEntry


def filter_by_stage(graph: FlowGraph, stage_names: set[str]) -> FlowGraph:
    """Return a sub-graph containing only nodes for the given stages.

    Args:
        graph: Source :class:`FlowGraph`.
        stage_names: Set of stage name strings to retain.

    Returns:
        New :class:`FlowGraph` with only matching nodes and their edges.
    """
    kept_nodes = {
        nid: n for nid, n in graph.nodes.items() if n.stage_name in stage_names
    }
    kept_node_ids = set(kept_nodes)
    kept_edges = {
        eid: e
        for eid, e in graph.edges.items()
        if e.from_node_id in kept_node_ids and e.to_node_id in kept_node_ids
    }
    kept_timeline = [t for t in graph.timeline if t.stage_name in stage_names]
    return graph.model_copy(update={
        "nodes": kept_nodes,
        "edges": kept_edges,
        "timeline": kept_timeline,
    })


def filter_by_node_type(graph: FlowGraph, node_types: set[NodeType]) -> FlowGraph:
    """Return a sub-graph retaining only nodes of the given types.

    Args:
        graph: Source :class:`FlowGraph`.
        node_types: Set of :class:`~flowvizsdk.models.NodeType` values.

    Returns:
        New :class:`FlowGraph`.
    """
    kept_nodes = {nid: n for nid, n in graph.nodes.items() if n.node_type in node_types}
    kept_node_ids = set(kept_nodes)
    kept_edges = {
        eid: e
        for eid, e in graph.edges.items()
        if e.from_node_id in kept_node_ids or e.to_node_id in kept_node_ids
    }
    kept_timeline = [t for t in graph.timeline if t.node_id in kept_node_ids]
    return graph.model_copy(update={
        "nodes": kept_nodes,
        "edges": kept_edges,
        "timeline": kept_timeline,
    })


def filter_by_status(graph: FlowGraph, statuses: set[NodeStatus]) -> FlowGraph:
    """Return a sub-graph retaining only nodes with the given statuses.

    Args:
        graph: Source :class:`FlowGraph`.
        statuses: Set of :class:`~flowvizsdk.models.NodeStatus` values.

    Returns:
        New :class:`FlowGraph`.
    """
    kept_nodes = {nid: n for nid, n in graph.nodes.items() if n.status in statuses}
    kept_node_ids = set(kept_nodes)
    kept_edges = {
        eid: e
        for eid, e in graph.edges.items()
        if e.from_node_id in kept_node_ids and e.to_node_id in kept_node_ids
    }
    kept_timeline = [t for t in graph.timeline if t.node_id in kept_node_ids]
    return graph.model_copy(update={
        "nodes": kept_nodes,
        "edges": kept_edges,
        "timeline": kept_timeline,
    })


def filter_by_time_range(
    graph: FlowGraph, start: datetime, end: datetime
) -> FlowGraph:
    """Return timeline entries within [start, end] (inclusive).

    Does not filter nodes/edges -- only the timeline is sliced.

    Args:
        graph: Source :class:`FlowGraph`.
        start: Range start (UTC).
        end: Range end (UTC).

    Returns:
        New :class:`FlowGraph` with filtered timeline.
    """
    kept_timeline = [t for t in graph.timeline if start <= t.timestamp <= end]
    return graph.model_copy(update={"timeline": kept_timeline})


def filter_governance_gates(graph: FlowGraph) -> FlowGraph:
    """Return a sub-graph containing only governance gate nodes and their edges.

    Args:
        graph: Source :class:`FlowGraph`.

    Returns:
        New :class:`FlowGraph` with only governance gate nodes.
    """
    kept_nodes = {nid: n for nid, n in graph.nodes.items() if n.is_governance_gate}
    kept_node_ids = set(kept_nodes)
    kept_edges = {
        eid: e
        for eid, e in graph.edges.items()
        if e.from_node_id in kept_node_ids or e.to_node_id in kept_node_ids
    }
    kept_timeline = [t for t in graph.timeline if t.node_id in kept_node_ids]
    return graph.model_copy(update={
        "nodes": kept_nodes,
        "edges": kept_edges,
        "timeline": kept_timeline,
    })


def filter_failure_paths(graph: FlowGraph) -> FlowGraph:
    """Return only edges on failure paths and the nodes they connect.

    Args:
        graph: Source :class:`FlowGraph`.

    Returns:
        New :class:`FlowGraph` with only failure path edges.
    """
    failure_edges = {eid: e for eid, e in graph.edges.items() if e.is_failure_path}
    involved_ids = {e.from_node_id for e in failure_edges.values()} | {
        e.to_node_id for e in failure_edges.values()
    }
    kept_nodes = {nid: n for nid, n in graph.nodes.items() if nid in involved_ids}
    kept_timeline = [t for t in graph.timeline if t.node_id in involved_ids]
    return graph.model_copy(update={
        "nodes": kept_nodes,
        "edges": failure_edges,
        "timeline": kept_timeline,
    })


def apply_custom_filter(
    graph: FlowGraph,
    node_predicate: Callable[[FlowNode], bool] | None = None,
    edge_predicate: Callable[[FlowEdge], bool] | None = None,
    timeline_predicate: Callable[[TimelineEntry], bool] | None = None,
) -> FlowGraph:
    """Apply arbitrary predicate filters to the graph.

    Args:
        graph: Source :class:`FlowGraph`.
        node_predicate: Optional callable returning True to keep a node.
        edge_predicate: Optional callable returning True to keep an edge.
        timeline_predicate: Optional callable returning True to keep a timeline entry.

    Returns:
        New :class:`FlowGraph` with filtered content.
    """
    nodes = (
        {nid: n for nid, n in graph.nodes.items() if node_predicate(n)}
        if node_predicate
        else dict(graph.nodes)
    )
    edges = (
        {eid: e for eid, e in graph.edges.items() if edge_predicate(e)}
        if edge_predicate
        else dict(graph.edges)
    )
    timeline = (
        [t for t in graph.timeline if timeline_predicate(t)]
        if timeline_predicate
        else list(graph.timeline)
    )
    return graph.model_copy(update={"nodes": nodes, "edges": edges, "timeline": timeline})
