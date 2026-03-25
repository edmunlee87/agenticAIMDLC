"""flowvizsdk -- flow visualization SDK.

Converts observability events into a FlowGraph (nodes + edges + timeline)
with export to JSON, HTML, and SVG, and composable filter functions.
"""

from flowvizsdk.graph_export import to_dict, to_html, to_json, to_svg
from flowvizsdk.models import (
    FlowEdge,
    FlowGraph,
    FlowNode,
    NodeStatus,
    NodeType,
    TimelineEntry,
)
from flowvizsdk.service import FlowVizService
from flowvizsdk.flow_filters import (
    apply_custom_filter,
    filter_by_node_type,
    filter_by_stage,
    filter_by_status,
    filter_by_time_range,
    filter_failure_paths,
    filter_governance_gates,
)

__all__ = [
    "FlowEdge",
    "FlowGraph",
    "FlowNode",
    "FlowVizService",
    "NodeStatus",
    "NodeType",
    "TimelineEntry",
    "apply_custom_filter",
    "filter_by_node_type",
    "filter_by_stage",
    "filter_by_status",
    "filter_by_time_range",
    "filter_failure_paths",
    "filter_governance_gates",
    "to_dict",
    "to_html",
    "to_json",
    "to_svg",
]
