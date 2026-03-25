"""canvassdk.service -- CanvasService: builds and manages workflow canvas history.

The service builds a canvas from a :class:`~flowvizsdk.models.FlowGraph`
(or directly from observability events) and maintains an append-only history
of :class:`~canvassdk.models.CanvasSnapshot` objects.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from canvassdk.models import (
    CanvasEdge,
    CanvasGroup,
    CanvasHistory,
    CanvasNode,
    CanvasNodeState,
    CanvasNodeType,
    CanvasPosition,
    CanvasSnapshot,
)

logger = logging.getLogger(__name__)

# FlowViz NodeType → CanvasNodeType mapping
_NODE_TYPE_MAP: dict[str, CanvasNodeType] = {
    "stage": CanvasNodeType.STAGE,
    "hitl_gate": CanvasNodeType.HITL_GATE,
    "artifact": CanvasNodeType.ARTIFACT,
    "candidate": CanvasNodeType.CANDIDATE,
    "recovery": CanvasNodeType.RECOVERY,
    "session": CanvasNodeType.SESSION,
    "policy_check": CanvasNodeType.POLICY_CHECK,
}

# FlowViz NodeStatus → CanvasNodeState mapping
_STATE_MAP: dict[str, CanvasNodeState] = {
    "pending": CanvasNodeState.PENDING,
    "running": CanvasNodeState.RUNNING,
    "completed": CanvasNodeState.COMPLETED,
    "failed": CanvasNodeState.FAILED,
    "blocked": CanvasNodeState.HITL_WAITING,
    "hitl_waiting": CanvasNodeState.HITL_WAITING,
    "hitl_approved": CanvasNodeState.HITL_APPROVED,
    "hitl_rejected": CanvasNodeState.HITL_REJECTED,
    "skipped": CanvasNodeState.SKIPPED,
    "recovered": CanvasNodeState.RECOVERED,
}

# Grid layout constants
_COL_WIDTH = 200
_ROW_HEIGHT = 120


class CanvasService:
    """Builds and manages workflow canvas history.

    Args:
        observability_service: Optional observability service.
    """

    def __init__(self, observability_service: Any = None) -> None:
        self._obs = observability_service
        self._histories: dict[str, CanvasHistory] = {}

    def build_from_flow_graph(
        self,
        canvas_id: str,
        flow_graph: Any,
        run_id: str,
        project_id: str,
        created_by: str = "",
        group_by_stage_type: bool = True,
    ) -> CanvasSnapshot:
        """Build an initial canvas snapshot from a :class:`~flowvizsdk.models.FlowGraph`.

        Args:
            canvas_id: Canvas identifier.
            flow_graph: :class:`~flowvizsdk.models.FlowGraph` instance.
            run_id: MDLC run.
            project_id: Project.
            created_by: Actor.
            group_by_stage_type: Whether to auto-group nodes by stage type. Default: True.

        Returns:
            Initial :class:`CanvasSnapshot`.
        """
        flow_nodes = getattr(flow_graph, "nodes", {})
        flow_edges = getattr(flow_graph, "edges", {})

        canvas_nodes: dict[str, CanvasNode] = {}
        canvas_edges: dict[str, CanvasEdge] = {}
        canvas_groups: dict[str, CanvasGroup] = {}

        # Convert flow nodes to canvas nodes with grid layout.
        for idx, (nid, fn) in enumerate(flow_nodes.items()):
            col = idx % 6
            row = idx // 6
            node_type = _NODE_TYPE_MAP.get(
                getattr(fn, "node_type", "stage") if hasattr(fn, "node_type") else str(fn.get("node_type", "stage")),
                CanvasNodeType.STAGE,
            )
            state_str = str(getattr(fn, "status", "pending") if hasattr(fn, "status") else fn.get("status", "pending"))
            if hasattr(state_str, "value"):
                state_str = state_str.value
            state = _STATE_MAP.get(state_str, CanvasNodeState.PENDING)

            canvas_nodes[nid] = CanvasNode(
                node_id=nid,
                node_type=node_type,
                label=str(getattr(fn, "label", nid) if hasattr(fn, "label") else fn.get("label", nid)),
                state=state,
                stage_name=str(getattr(fn, "stage_name", "") if hasattr(fn, "stage_name") else fn.get("stage_name", "")),
                run_id=run_id,
                project_id=project_id,
                position=CanvasPosition(x=col * _COL_WIDTH, y=row * _ROW_HEIGHT),
                is_governance_gate=bool(getattr(fn, "is_governance_gate", False) if hasattr(fn, "is_governance_gate") else fn.get("is_governance_gate", False)),
                source_event_ids=list(getattr(fn, "source_event_ids", []) if hasattr(fn, "source_event_ids") else fn.get("source_event_ids", [])),
            )

        # Convert flow edges to canvas edges.
        for eid, fe in flow_edges.items():
            canvas_edges[eid] = CanvasEdge(
                edge_id=eid,
                from_node_id=str(getattr(fe, "from_node_id", "") if hasattr(fe, "from_node_id") else fe.get("from_node_id", "")),
                to_node_id=str(getattr(fe, "to_node_id", "") if hasattr(fe, "to_node_id") else fe.get("to_node_id", "")),
                label=str(getattr(fe, "label", "") if hasattr(fe, "label") else fe.get("label", "")),
                is_failure_path=bool(getattr(fe, "is_failure_path", False) if hasattr(fe, "is_failure_path") else fe.get("is_failure_path", False)),
                is_recovery_path=bool(getattr(fe, "is_recovery_path", False) if hasattr(fe, "is_recovery_path") else fe.get("is_recovery_path", False)),
            )

        # Auto-group governance gates.
        if group_by_stage_type:
            gate_nodes = [nid for nid, n in canvas_nodes.items() if n.is_governance_gate]
            if gate_nodes:
                gid = f"grp_governance_{canvas_id}"
                canvas_groups[gid] = CanvasGroup(
                    group_id=gid,
                    label="Governance Gates",
                    node_ids=gate_nodes,
                    color="#fff3cd",
                )
                canvas_nodes = {
                    nid: n.model_copy(update={"group_id": gid}) if nid in gate_nodes else n
                    for nid, n in canvas_nodes.items()
                }

        snapshot = CanvasSnapshot(
            snapshot_id=str(uuid.uuid4()),
            canvas_id=canvas_id,
            run_id=run_id,
            project_id=project_id,
            nodes=canvas_nodes,
            edges=canvas_edges,
            groups=canvas_groups,
            version=1,
            created_by=created_by,
            change_reason="Initial canvas from flow graph",
        )

        # Initialise history.
        self._histories[canvas_id] = CanvasHistory(
            canvas_id=canvas_id,
            run_id=run_id,
            project_id=project_id,
            snapshots=[snapshot],
        )

        logger.info(
            "canvas_service.built",
            extra={
                "canvas_id": canvas_id,
                "nodes": snapshot.node_count,
                "edges": snapshot.edge_count,
            },
        )
        return snapshot

    def update_node_state(
        self,
        canvas_id: str,
        node_id: str,
        new_state: CanvasNodeState,
        actor_id: str = "",
        change_reason: str = "",
        audit_fields: dict[str, Any] | None = None,
        hitl_review_id: str | None = None,
    ) -> CanvasSnapshot:
        """Update a node's state and append a new snapshot to history.

        Args:
            canvas_id: Canvas to update.
            node_id: Node to update.
            new_state: Target :class:`CanvasNodeState`.
            actor_id: Actor making the change.
            change_reason: Reason for the state change.
            audit_fields: Governance audit fields to attach to the node.
            hitl_review_id: Active review ID (for HITL states).

        Returns:
            New :class:`CanvasSnapshot`.

        Raises:
            KeyError: If canvas or node not found.
        """
        history = self._histories.get(canvas_id)
        if history is None:
            raise KeyError(f"Canvas '{canvas_id}' not found.")

        current = history.current
        if current is None:
            raise KeyError(f"Canvas '{canvas_id}' has no snapshots.")

        node = current.nodes.get(node_id)
        if node is None:
            raise KeyError(f"Node '{node_id}' not found in canvas '{canvas_id}'.")

        update: dict[str, Any] = {
            "state": new_state,
            "actor_id": actor_id,
        }
        if audit_fields:
            update["audit_fields"] = {**node.audit_fields, **audit_fields}
        if hitl_review_id is not None:
            update["hitl_review_id"] = hitl_review_id

        new_node = node.model_copy(update=update)
        new_nodes = {**current.nodes, node_id: new_node}

        new_snapshot = current.model_copy(update={
            "snapshot_id": str(uuid.uuid4()),
            "nodes": new_nodes,
            "version": current.version + 1,
            "created_at": datetime.now(timezone.utc),
            "created_by": actor_id,
            "change_reason": change_reason or f"Node '{node_id}' → {new_state.value}",
        })

        updated_history = history.model_copy(
            update={"snapshots": [*history.snapshots, new_snapshot]}
        )
        self._histories[canvas_id] = updated_history

        logger.info(
            "canvas_service.node_updated",
            extra={"canvas_id": canvas_id, "node_id": node_id, "new_state": new_state},
        )
        return new_snapshot

    def get_current(self, canvas_id: str) -> CanvasSnapshot | None:
        """Return the current canvas snapshot.

        Args:
            canvas_id: Canvas identifier.

        Returns:
            Latest :class:`CanvasSnapshot` or None.
        """
        history = self._histories.get(canvas_id)
        return history.current if history else None

    def get_history(self, canvas_id: str) -> CanvasHistory | None:
        """Return the full canvas history.

        Args:
            canvas_id: Canvas identifier.

        Returns:
            :class:`CanvasHistory` or None.
        """
        return self._histories.get(canvas_id)

    def export_snapshot_json(self, canvas_id: str) -> str | None:
        """Export the current canvas snapshot as JSON.

        Args:
            canvas_id: Canvas identifier.

        Returns:
            JSON string or None.
        """
        snapshot = self.get_current(canvas_id)
        if snapshot is None:
            return None
        return snapshot.model_dump_json(indent=2)

    def health_check(self) -> dict[str, Any]:
        """Return health status."""
        return {"status": "ok", "service": "CanvasService", "canvas_count": len(self._histories)}
