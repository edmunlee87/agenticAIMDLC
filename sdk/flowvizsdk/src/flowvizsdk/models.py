"""flowvizsdk.models -- immutable data contracts for FlowNode, FlowEdge, and timeline.

The flow graph is reconstructed from observability events on demand (not persisted),
making it deterministic and replay-safe: given the same event log, the graph is always
identical.

Graph entities:
- :class:`NodeType` -- what kind of node this represents.
- :class:`NodeStatus` -- current execution status of the node.
- :class:`FlowNode` -- a vertex in the workflow graph (stage, HITL gate, artifact, etc.).
- :class:`FlowEdge` -- a directed edge connecting two :class:`FlowNode` instances.
- :class:`TimelineEntry` -- a flattened, time-ordered event record for timeline rendering.
- :class:`FlowGraph` -- the assembled graph with nodes, edges, and timeline.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NodeType(str, Enum):
    """Type of a FlowNode in the workflow graph."""

    STAGE = "stage"
    HITL_GATE = "hitl_gate"
    ARTIFACT = "artifact"
    CANDIDATE = "candidate"
    RECOVERY = "recovery"
    SESSION = "session"
    POLICY_CHECK = "policy_check"
    TERMINAL = "terminal"


class NodeStatus(str, Enum):
    """Execution status of a FlowNode."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    RECOVERED = "recovered"


class FlowNode(BaseModel):
    """A vertex in the MDLC workflow graph.

    Args:
        node_id: Unique node identifier (stable across replays).
        node_type: What this node represents.
        label: Human-readable display label.
        stage_name: MDLC stage this node belongs to (may be empty for cross-stage nodes).
        status: Current execution status.
        started_at: When execution began (UTC).
        completed_at: When execution ended (UTC).
        actor_id: Actor who triggered this node.
        run_id: Run this node belongs to.
        project_id: Project this node belongs to.
        source_event_ids: Observability event IDs that generated this node.
        metadata: Arbitrary additional metadata for rendering.
        has_detail: True if drill-down detail is available.
        is_governance_gate: True if this node represents a governance decision point.
    """

    model_config = ConfigDict(frozen=True)

    node_id: str
    node_type: NodeType
    label: str
    stage_name: str = ""
    status: NodeStatus = NodeStatus.PENDING
    started_at: datetime | None = None
    completed_at: datetime | None = None
    actor_id: str = ""
    run_id: str = ""
    project_id: str = ""
    source_event_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    has_detail: bool = False
    is_governance_gate: bool = False

    @property
    def duration_seconds(self) -> float | None:
        """Return duration in seconds, or None if not yet completed."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class FlowEdge(BaseModel):
    """A directed edge connecting two :class:`FlowNode` instances.

    Args:
        edge_id: Unique edge identifier.
        from_node_id: Source node ID.
        to_node_id: Target node ID.
        label: Optional edge label (e.g. ``"approved"``, ``"failed"``).
        is_failure_path: True if this edge represents a failure route.
        is_recovery_path: True if this edge represents a recovery route.
        triggered_by_event_id: Observability event ID that created this edge.
        metadata: Arbitrary rendering metadata.
    """

    model_config = ConfigDict(frozen=True)

    edge_id: str
    from_node_id: str
    to_node_id: str
    label: str = ""
    is_failure_path: bool = False
    is_recovery_path: bool = False
    triggered_by_event_id: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class TimelineEntry(BaseModel):
    """A flattened, time-ordered entry for timeline visualization.

    Args:
        entry_id: Unique timeline entry ID (= source event ID).
        timestamp: When this event occurred.
        event_type: Original observability event type string.
        stage_name: Stage at time of event.
        actor_id: Actor who caused this event.
        category: High-level category (``"workflow"``, ``"hitl"``, ``"artifact"``, etc.).
        severity: Log severity level.
        summary: One-line human-readable summary.
        node_id: FlowNode this entry maps to (for cross-linking).
        run_id: Run ID.
        project_id: Project ID.
    """

    model_config = ConfigDict(frozen=True)

    entry_id: str
    timestamp: datetime
    event_type: str
    stage_name: str = ""
    actor_id: str = ""
    category: str = ""
    severity: str = "info"
    summary: str = ""
    node_id: str = ""
    run_id: str = ""
    project_id: str = ""


class FlowGraph(BaseModel):
    """The assembled flow graph for a single run.

    Args:
        run_id: Run this graph represents.
        project_id: Project this graph belongs to.
        nodes: All graph nodes keyed by node_id.
        edges: All graph edges keyed by edge_id.
        timeline: Time-ordered list of timeline entries.
        built_at: When the graph was assembled.
        event_count: Total number of source events consumed.
        schema_version: Schema version for forward compatibility.
    """

    model_config = ConfigDict(frozen=True)

    run_id: str
    project_id: str
    nodes: dict[str, FlowNode] = Field(default_factory=dict)
    edges: dict[str, FlowEdge] = Field(default_factory=dict)
    timeline: list[TimelineEntry] = Field(default_factory=list)
    built_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_count: int = 0
    schema_version: str = "1.0.0"

    @property
    def node_count(self) -> int:
        """Number of nodes in the graph."""
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        """Number of edges in the graph."""
        return len(self.edges)

    def get_nodes_by_type(self, node_type: NodeType) -> list[FlowNode]:
        """Return all nodes of a specific type.

        Args:
            node_type: The :class:`NodeType` to filter by.

        Returns:
            List of matching :class:`FlowNode` instances.
        """
        return [n for n in self.nodes.values() if n.node_type == node_type]

    def get_nodes_by_status(self, status: NodeStatus) -> list[FlowNode]:
        """Return all nodes with a specific status.

        Args:
            status: The :class:`NodeStatus` to filter by.

        Returns:
            List of matching :class:`FlowNode` instances.
        """
        return [n for n in self.nodes.values() if n.status == status]

    def get_outbound_edges(self, node_id: str) -> list[FlowEdge]:
        """Return all edges leaving a node.

        Args:
            node_id: Source node identifier.

        Returns:
            List of outbound :class:`FlowEdge` instances.
        """
        return [e for e in self.edges.values() if e.from_node_id == node_id]

    def get_inbound_edges(self, node_id: str) -> list[FlowEdge]:
        """Return all edges entering a node.

        Args:
            node_id: Target node identifier.

        Returns:
            List of inbound :class:`FlowEdge` instances.
        """
        return [e for e in self.edges.values() if e.to_node_id == node_id]
