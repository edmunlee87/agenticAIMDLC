"""flowvizsdk.graph_export -- serializes FlowGraph to JSON, HTML, and SVG.

All export functions are pure (no side effects) and deterministic.
"""

from __future__ import annotations

import json
from typing import Any

from flowvizsdk.models import FlowEdge, FlowGraph, FlowNode, NodeStatus, NodeType


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------


def to_json(graph: FlowGraph, indent: int = 2) -> str:
    """Serialize a :class:`FlowGraph` to a JSON string.

    Args:
        graph: The graph to serialize.
        indent: JSON indentation level. Default: 2.

    Returns:
        JSON string.
    """
    return graph.model_dump_json(indent=indent)


def to_dict(graph: FlowGraph) -> dict[str, Any]:
    """Serialize a :class:`FlowGraph` to a plain dict.

    Args:
        graph: The graph to serialize.

    Returns:
        Dict suitable for JSON serialization or API responses.
    """
    return json.loads(graph.model_dump_json())


# ---------------------------------------------------------------------------
# SVG export
# ---------------------------------------------------------------------------

_STATUS_COLORS: dict[NodeStatus, str] = {
    NodeStatus.PENDING: "#d0d0d0",
    NodeStatus.RUNNING: "#4a90d9",
    NodeStatus.COMPLETED: "#5cb85c",
    NodeStatus.FAILED: "#d9534f",
    NodeStatus.BLOCKED: "#f0ad4e",
    NodeStatus.SKIPPED: "#aaaaaa",
    NodeStatus.RECOVERED: "#9b59b6",
}

_NODE_SHAPES: dict[NodeType, str] = {
    NodeType.STAGE: "rect",
    NodeType.HITL_GATE: "diamond",
    NodeType.ARTIFACT: "ellipse",
    NodeType.CANDIDATE: "ellipse",
    NodeType.RECOVERY: "rect",
    NodeType.SESSION: "rect",
    NodeType.POLICY_CHECK: "diamond",
    NodeType.TERMINAL: "rect",
}


def to_svg(graph: FlowGraph, width: int = 1200, height: int = 600) -> str:
    """Generate a simple SVG visualization of the flow graph.

    Nodes are laid out left-to-right in the order they appear in
    ``graph.timeline``.  This is a minimal layout -- no edge routing.

    Args:
        graph: The graph to visualize.
        width: SVG canvas width in pixels. Default: 1200.
        height: SVG canvas height in pixels. Default: 600.

    Returns:
        SVG string.
    """
    node_list = list(graph.nodes.values())
    n = len(node_list)
    if n == 0:
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><text x="10" y="30">Empty graph</text></svg>'

    # Simple grid layout: left to right, wrap every 8 nodes.
    cols = min(n, 8)
    cell_w = width // cols
    cell_h = height // max(1, (n + cols - 1) // cols)
    node_pos: dict[str, tuple[int, int]] = {}
    shapes: list[str] = []
    labels: list[str] = []

    for idx, node in enumerate(node_list):
        col = idx % cols
        row = idx // cols
        cx = col * cell_w + cell_w // 2
        cy = row * cell_h + cell_h // 2
        node_pos[node.node_id] = (cx, cy)
        color = _STATUS_COLORS.get(node.status, "#cccccc")
        ntype = _NODE_SHAPES.get(node.node_type, "rect")

        if ntype == "diamond":
            hw, hh = 55, 30
            pts = f"{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}"
            shapes.append(f'<polygon points="{pts}" fill="{color}" stroke="#333" stroke-width="1.5"/>')
        elif ntype == "ellipse":
            shapes.append(f'<ellipse cx="{cx}" cy="{cy}" rx="55" ry="28" fill="{color}" stroke="#333" stroke-width="1.5"/>')
        else:
            shapes.append(f'<rect x="{cx-55}" y="{cy-25}" width="110" height="50" rx="6" fill="{color}" stroke="#333" stroke-width="1.5"/>')

        short_label = node.label[:16] + "…" if len(node.label) > 16 else node.label
        labels.append(f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="11" font-family="monospace">{short_label}</text>')

    # Edges
    edge_lines: list[str] = []
    for edge in graph.edges.values():
        if edge.from_node_id in node_pos and edge.to_node_id in node_pos:
            x1, y1 = node_pos[edge.from_node_id]
            x2, y2 = node_pos[edge.to_node_id]
            color = "#d9534f" if edge.is_failure_path else "#9b59b6" if edge.is_recovery_path else "#888"
            edge_lines.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" marker-end="url(#arrow)"/>'
            )

    arrow_def = (
        '<defs><marker id="arrow" markerWidth="10" markerHeight="7" '
        'refX="9" refY="3.5" orient="auto">'
        '<polygon points="0 0, 10 3.5, 0 7" fill="#888"/>'
        "</marker></defs>"
    )

    inner = arrow_def + "\n".join(edge_lines + shapes + labels)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" style="background:#fafafa">{inner}</svg>'


# ---------------------------------------------------------------------------
# HTML export
# ---------------------------------------------------------------------------


def to_html(graph: FlowGraph, title: str = "MDLC Workflow Flow Graph") -> str:
    """Generate a self-contained HTML page with the flow graph SVG and timeline.

    Args:
        graph: The graph to render.
        title: Page title.

    Returns:
        Complete HTML string.
    """
    svg = to_svg(graph, width=1200, height=500)
    timeline_rows = "\n".join(
        f"<tr><td>{e.timestamp.strftime('%H:%M:%S')}</td>"
        f"<td>{e.category}</td>"
        f"<td>{e.stage_name}</td>"
        f"<td>{e.summary}</td>"
        f"<td>{e.actor_id}</td></tr>"
        for e in graph.timeline
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>{title}</title>
<style>
  body {{ font-family: monospace; margin: 20px; background: #f8f8f8; }}
  h1 {{ font-size: 18px; color: #333; }}
  .graph {{ border: 1px solid #ccc; background: white; margin-bottom: 20px; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 12px; }}
  th, td {{ border: 1px solid #ddd; padding: 4px 8px; }}
  th {{ background: #eee; }}
  tr:nth-child(even) {{ background: #f9f9f9; }}
</style>
</head>
<body>
<h1>{title}</h1>
<p>Run: <b>{graph.run_id}</b> | Project: <b>{graph.project_id}</b> |
   Nodes: {graph.node_count} | Edges: {graph.edge_count} | Events: {graph.event_count}</p>
<div class="graph">{svg}</div>
<h2>Timeline</h2>
<table>
  <thead><tr><th>Time</th><th>Category</th><th>Stage</th><th>Summary</th><th>Actor</th></tr></thead>
  <tbody>{timeline_rows}</tbody>
</table>
</body>
</html>"""
