"""canvassdk.models -- Workflow Canvas data model.

The canvas is the main-area cockpit: a directed graph where nodes represent
stages, HITL gates, and artifacts, and edges represent transitions.
Nodes and edges are enriched with governance audit fields.

The canvas is version-controlled: every mutation creates a new
:class:`CanvasSnapshot` appended to an immutable history log.

Entity hierarchy per plan sections 12.1-12.5:
- Workspace (top-level container)
  └── Project (multiple per workspace)
      └── Module / Use Case
          └── Page / Task (= a canvas)
              └── CanvasNode / CanvasEdge / CanvasGroup
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CanvasNodeType(str, Enum):
    """Type of a canvas node."""
    STAGE = "stage"
    HITL_GATE = "hitl_gate"
    ARTIFACT = "artifact"
    CANDIDATE = "candidate"
    RECOVERY = "recovery"
    SESSION = "session"
    POLICY_CHECK = "policy_check"
    ANNOTATION = "annotation"


class CanvasNodeState(str, Enum):
    """Execution state of a canvas node (drives visual styling)."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    RECOVERED = "recovered"
    HITL_WAITING = "hitl_waiting"
    HITL_APPROVED = "hitl_approved"
    HITL_REJECTED = "hitl_rejected"


class CanvasPosition(BaseModel):
    """2D canvas position for layout persistence.

    Args:
        x: Horizontal position (pixels or grid units).
        y: Vertical position.
    """

    model_config = ConfigDict(frozen=True)

    x: float = 0.0
    y: float = 0.0


class CanvasNode(BaseModel):
    """A node in the workflow canvas.

    Args:
        node_id: Unique node identifier (stable across history).
        node_type: :class:`CanvasNodeType`.
        label: Display label.
        state: :class:`CanvasNodeState`.
        stage_name: MDLC stage this node represents.
        run_id: Run this node belongs to.
        project_id: Project.
        actor_id: Last actor who updated this node.
        position: 2D layout position.
        is_governance_gate: True if this is a governance decision point.
        hitl_review_id: Active review ID if state is HITL_WAITING.
        audit_fields: Governance audit fields (trace_id, policy_check_result, etc.).
        source_event_ids: Observability event IDs that drove this node state.
        metadata: Arbitrary extra metadata.
        group_id: Canvas group this node belongs to (optional).
    """

    model_config = ConfigDict(frozen=True)

    node_id: str
    node_type: CanvasNodeType
    label: str
    state: CanvasNodeState = CanvasNodeState.PENDING
    stage_name: str = ""
    run_id: str = ""
    project_id: str = ""
    actor_id: str = ""
    position: CanvasPosition = Field(default_factory=CanvasPosition)
    is_governance_gate: bool = False
    hitl_review_id: str | None = None
    audit_fields: dict[str, Any] = Field(default_factory=dict)
    source_event_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    group_id: str | None = None


class CanvasEdge(BaseModel):
    """A directed edge in the workflow canvas.

    Args:
        edge_id: Unique edge identifier.
        from_node_id: Source node ID.
        to_node_id: Target node ID.
        label: Edge label.
        is_failure_path: True for failure route edges.
        is_recovery_path: True for recovery route edges.
        is_active: True if this edge represents the current execution path.
        metadata: Arbitrary metadata.
    """

    model_config = ConfigDict(frozen=True)

    edge_id: str
    from_node_id: str
    to_node_id: str
    label: str = ""
    is_failure_path: bool = False
    is_recovery_path: bool = False
    is_active: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class CanvasGroup(BaseModel):
    """A visual grouping of canvas nodes.

    Groups correspond to the Module / Use Case layer in the 4-tier hierarchy.

    Args:
        group_id: Unique group identifier.
        label: Display label.
        node_ids: Member node IDs.
        color: Optional group color (hex or CSS name).
        collapsed: Whether the group is visually collapsed.
    """

    model_config = ConfigDict(frozen=True)

    group_id: str
    label: str
    node_ids: list[str] = Field(default_factory=list)
    color: str = "#e8e8e8"
    collapsed: bool = False


class CanvasSnapshot(BaseModel):
    """An immutable point-in-time snapshot of the canvas state.

    Args:
        snapshot_id: Unique snapshot identifier.
        canvas_id: Canvas this snapshot belongs to.
        run_id: MDLC run.
        project_id: Project.
        nodes: All nodes keyed by node_id.
        edges: All edges keyed by edge_id.
        groups: All groups keyed by group_id.
        version: Sequential version number (1-indexed).
        created_at: Snapshot creation timestamp.
        created_by: Actor who triggered the canvas change.
        change_reason: Human-readable reason for the canvas state change.
        schema_version: Schema version for forward compatibility.
    """

    model_config = ConfigDict(frozen=True)

    snapshot_id: str
    canvas_id: str
    run_id: str
    project_id: str
    nodes: dict[str, CanvasNode] = Field(default_factory=dict)
    edges: dict[str, CanvasEdge] = Field(default_factory=dict)
    groups: dict[str, CanvasGroup] = Field(default_factory=dict)
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""
    change_reason: str = ""
    schema_version: str = "1.0.0"

    @property
    def node_count(self) -> int:
        """Number of nodes."""
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        """Number of edges."""
        return len(self.edges)

    def get_nodes_by_state(self, state: CanvasNodeState) -> list[CanvasNode]:
        """Return all nodes with a specific state.

        Args:
            state: :class:`CanvasNodeState` to filter by.

        Returns:
            List of matching :class:`CanvasNode`.
        """
        return [n for n in self.nodes.values() if n.state == state]

    def get_governance_gates(self) -> list[CanvasNode]:
        """Return all governance gate nodes.

        Returns:
            List of :class:`CanvasNode`.
        """
        return [n for n in self.nodes.values() if n.is_governance_gate]

    def get_hitl_waiting(self) -> list[CanvasNode]:
        """Return all nodes currently waiting for HITL review.

        Returns:
            List of :class:`CanvasNode`.
        """
        return self.get_nodes_by_state(CanvasNodeState.HITL_WAITING)


class CanvasHistory(BaseModel):
    """Append-only history of :class:`CanvasSnapshot` objects for a canvas.

    Args:
        canvas_id: Canvas identifier.
        run_id: MDLC run.
        project_id: Project.
        snapshots: Ordered list of snapshots (oldest first).
    """

    model_config = ConfigDict(frozen=True)

    canvas_id: str
    run_id: str
    project_id: str
    snapshots: list[CanvasSnapshot] = Field(default_factory=list)

    @property
    def current(self) -> CanvasSnapshot | None:
        """Return the latest canvas snapshot."""
        return self.snapshots[-1] if self.snapshots else None

    @property
    def version_count(self) -> int:
        """Number of snapshots in the history."""
        return len(self.snapshots)

    def at_version(self, version: int) -> CanvasSnapshot | None:
        """Return the snapshot at a specific version number.

        Args:
            version: Version number (1-indexed).

        Returns:
            :class:`CanvasSnapshot` or None.
        """
        return next((s for s in self.snapshots if s.version == version), None)
