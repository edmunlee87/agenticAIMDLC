"""flowvizsdk.node_builder -- constructs FlowNodes from observability events.

The builder is stateful for a single build pass: it accumulates events for the
same stage/entity into a single node, merging status updates as newer events arrive.
"""

from __future__ import annotations

import logging
from typing import Any

from flowvizsdk.models import FlowNode, NodeStatus, NodeType

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Event type → (NodeType, label_template, is_governance_gate)
# ---------------------------------------------------------------------------

_EVENT_MAP: dict[str, tuple[NodeType, str, bool]] = {
    # Workflow stage events
    "workflow.stage.started": (NodeType.STAGE, "Stage: {stage_name}", False),
    "workflow.stage.completed": (NodeType.STAGE, "Stage: {stage_name}", False),
    "workflow.stage.failed": (NodeType.STAGE, "Stage: {stage_name}", False),
    "workflow.stage.blocked": (NodeType.STAGE, "Stage: {stage_name}", False),
    "workflow.initialized": (NodeType.SESSION, "Workflow Init", False),
    # HITL / review events
    "hitl.review.created": (NodeType.HITL_GATE, "Review: {stage_name}", True),
    "hitl.review.approved": (NodeType.HITL_GATE, "Review: {stage_name}", True),
    "hitl.review.rejected": (NodeType.HITL_GATE, "Review: {stage_name}", True),
    "hitl.review.escalated": (NodeType.HITL_GATE, "Review: {stage_name}", True),
    # Artifact events
    "artifact.registered": (NodeType.ARTIFACT, "Artifact: {label}", False),
    "artifact.promoted": (NodeType.ARTIFACT, "Artifact: {label}", False),
    # Candidate events
    "workflow.candidate.registered": (NodeType.CANDIDATE, "Candidate: {stage_name}", False),
    "workflow.candidate.selected": (NodeType.CANDIDATE, "Candidate: {stage_name}", False),
    # Recovery events
    "workflow.recovery.applied": (NodeType.RECOVERY, "Recovery: {stage_name}", False),
    # Policy events
    "policy.evaluated": (NodeType.POLICY_CHECK, "Policy Gate: {stage_name}", True),
    "policy.breach.detected": (NodeType.POLICY_CHECK, "Policy Breach: {stage_name}", True),
}

_STATUS_MAP: dict[str, NodeStatus] = {
    "workflow.stage.started": NodeStatus.RUNNING,
    "workflow.stage.completed": NodeStatus.COMPLETED,
    "workflow.stage.failed": NodeStatus.FAILED,
    "workflow.stage.blocked": NodeStatus.BLOCKED,
    "hitl.review.created": NodeStatus.BLOCKED,
    "hitl.review.approved": NodeStatus.COMPLETED,
    "hitl.review.rejected": NodeStatus.FAILED,
    "hitl.review.escalated": NodeStatus.BLOCKED,
    "artifact.registered": NodeStatus.COMPLETED,
    "artifact.promoted": NodeStatus.COMPLETED,
    "workflow.candidate.registered": NodeStatus.PENDING,
    "workflow.candidate.selected": NodeStatus.COMPLETED,
    "workflow.recovery.applied": NodeStatus.RECOVERED,
    "policy.evaluated": NodeStatus.COMPLETED,
    "policy.breach.detected": NodeStatus.BLOCKED,
    "workflow.initialized": NodeStatus.COMPLETED,
}


def _node_id_for_event(event: Any) -> str:
    """Derive a stable node ID from an observability event.

    Stage events share a node ID to allow status merging across start/complete.

    Args:
        event: :class:`~observabilitysdk.models.ObservabilityEvent`.

    Returns:
        Stable string node ID.
    """
    event_type: str = getattr(event, "event_type", "") or ""
    run_id: str = getattr(event, "run_id", "") or ""
    stage: str = getattr(event, "stage_name", "") or ""

    if event_type.startswith("workflow.stage."):
        return f"stage__{run_id}__{stage}"
    if event_type.startswith("hitl.review."):
        review_id = (getattr(event, "metadata", {}) or {}).get("review_id", stage)
        return f"hitl__{run_id}__{review_id}"
    if event_type.startswith("artifact."):
        art_id = (getattr(event, "metadata", {}) or {}).get("artifact_id", "")
        return f"artifact__{run_id}__{art_id}"
    if event_type.startswith("workflow.candidate."):
        cand_id = (getattr(event, "metadata", {}) or {}).get("candidate_id", stage)
        return f"candidate__{run_id}__{cand_id}"
    if event_type.startswith("workflow.recovery."):
        return f"recovery__{run_id}__{stage}"
    if event_type.startswith("policy."):
        return f"policy__{run_id}__{stage}"
    if event_type == "workflow.initialized":
        return f"session__{run_id}"
    return f"unknown__{run_id}__{event_type}"


class NodeBuilder:
    """Accumulates observability events and produces merged :class:`FlowNode` instances.

    Args:
        run_id: The run being visualized.
        project_id: The project being visualized.
    """

    def __init__(self, run_id: str, project_id: str) -> None:
        self._run_id = run_id
        self._project_id = project_id
        # node_id -> mutable node dict (merged as events arrive)
        self._node_drafts: dict[str, dict[str, Any]] = {}

    def consume(self, event: Any) -> str | None:
        """Process one observability event and update internal node state.

        Args:
            event: :class:`~observabilitysdk.models.ObservabilityEvent`.

        Returns:
            Node ID if the event maps to a known node type; None otherwise.
        """
        event_type: str = getattr(event, "event_type", "") or ""
        if event_type not in _EVENT_MAP:
            return None

        node_type, label_tpl, is_gate = _EVENT_MAP[event_type]
        new_status = _STATUS_MAP.get(event_type, NodeStatus.PENDING)
        stage_name: str = getattr(event, "stage_name", "") or ""
        actor_id: str = getattr(event, "actor_id", "") or ""
        ts = getattr(event, "timestamp", None)
        event_id: str = getattr(event, "event_id", "") or ""
        metadata: dict[str, Any] = dict(getattr(event, "metadata", {}) or {})

        label = label_tpl.format(
            stage_name=stage_name or "unknown",
            label=metadata.get("artifact_type", stage_name) or stage_name,
        )
        node_id = _node_id_for_event(event)

        if node_id not in self._node_drafts:
            self._node_drafts[node_id] = {
                "node_id": node_id,
                "node_type": node_type,
                "label": label,
                "stage_name": stage_name,
                "status": new_status,
                "run_id": self._run_id,
                "project_id": self._project_id,
                "actor_id": actor_id,
                "source_event_ids": [],
                "metadata": metadata,
                "is_governance_gate": is_gate,
                "has_detail": bool(metadata),
                "started_at": None,
                "completed_at": None,
            }

        draft = self._node_drafts[node_id]
        draft["source_event_ids"].append(event_id)

        # Merge status: only advance (running < completed/failed/blocked)
        current = draft["status"]
        if _status_rank(new_status) > _status_rank(current):
            draft["status"] = new_status

        # Timestamps
        if ts and event_type.endswith(".started") and draft["started_at"] is None:
            draft["started_at"] = ts
        if ts and event_type in {
            "workflow.stage.completed", "workflow.stage.failed",
            "hitl.review.approved", "hitl.review.rejected",
            "artifact.promoted", "workflow.candidate.selected",
            "workflow.recovery.applied",
        }:
            draft["completed_at"] = ts

        # Actor (prefer later events which have more context)
        if actor_id:
            draft["actor_id"] = actor_id

        draft["metadata"].update(metadata)
        return node_id

    def build_all(self) -> dict[str, FlowNode]:
        """Freeze all accumulated node drafts into immutable :class:`FlowNode` objects.

        Returns:
            Dict mapping node_id -> :class:`FlowNode`.
        """
        result: dict[str, FlowNode] = {}
        for node_id, d in self._node_drafts.items():
            try:
                result[node_id] = FlowNode(**d)
            except Exception as exc:
                logger.warning("node_builder.build_failed", extra={"node_id": node_id, "error": str(exc)})
        return result


def _status_rank(status: NodeStatus) -> int:
    """Return an integer rank for status ordering (higher = more terminal)."""
    order = {
        NodeStatus.PENDING: 0,
        NodeStatus.RUNNING: 1,
        NodeStatus.BLOCKED: 2,
        NodeStatus.RECOVERED: 3,
        NodeStatus.SKIPPED: 3,
        NodeStatus.FAILED: 4,
        NodeStatus.COMPLETED: 5,
    }
    return order.get(status, 0)
