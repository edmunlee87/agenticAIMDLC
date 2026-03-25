"""widgetsdk.sidebars -- left sidebar, right sidebar, and bottom panel models and builders.

Panel layout for the MDLC platform UI:

- **Left sidebar**: 4-tier workflow tree
  (Workspace/Project → Module/Use Case → Page/Task → Card/Artefact).
- **Right sidebar**: Agent console
  (Chat + Context + Trace + Actions).
- **Bottom panel**: Active card controls and status.

All models are immutable (frozen Pydantic).
UI interaction modes are aligned with :class:`~widgetsdk.models.WidgetMode`.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Left sidebar: workflow tree
# ---------------------------------------------------------------------------

class WorkflowTreeNodeType(str, Enum):
    """Tier type in the 4-tier workflow tree."""
    WORKSPACE = "workspace"
    PROJECT = "project"
    MODULE = "module"
    USE_CASE = "use_case"
    PAGE = "page"
    TASK = "task"
    CARD = "card"
    ARTEFACT = "artefact"


class WorkflowTreeNodeStatus(str, Enum):
    """Execution status for a tree node."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class WorkflowTreeNode(BaseModel):
    """A node in the 4-tier workflow tree.

    Args:
        node_id: Unique tree node identifier.
        label: Display label.
        node_type: :class:`WorkflowTreeNodeType`.
        status: :class:`WorkflowTreeNodeStatus`.
        children: Nested child nodes.
        is_active: Whether this is the currently active node.
        is_expanded: Whether this node is expanded in the UI.
        badge: Optional badge text (e.g. finding count, ``"3 open"``).
        metadata: Arbitrary extra data.
    """

    model_config = ConfigDict(frozen=True)

    node_id: str
    label: str
    node_type: WorkflowTreeNodeType
    status: WorkflowTreeNodeStatus = WorkflowTreeNodeStatus.PENDING
    children: list[WorkflowTreeNode] = Field(default_factory=list)
    is_active: bool = False
    is_expanded: bool = False
    badge: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


WorkflowTreeNode.model_rebuild()


class LeftSidebar(BaseModel):
    """Left sidebar containing the 4-tier workflow tree.

    Args:
        sidebar_id: Unique identifier.
        title: Sidebar title.
        tree: Root-level workflow tree nodes.
        run_id: Active MDLC run.
        project_id: Active project.
        active_node_id: ID of the currently active node.
        search_query: Active search filter string.
    """

    model_config = ConfigDict(frozen=True)

    sidebar_id: str
    title: str = "Workflow Navigation"
    tree: list[WorkflowTreeNode] = Field(default_factory=list)
    run_id: str = ""
    project_id: str = ""
    active_node_id: str = ""
    search_query: str = ""


# ---------------------------------------------------------------------------
# Right sidebar: agent console
# ---------------------------------------------------------------------------

class ChatMessage(BaseModel):
    """A single message in the agent chat panel.

    Args:
        message_id: Unique message identifier.
        role: ``"user"`` | ``"agent"`` | ``"system"``.
        content: Message content text.
        timestamp: ISO timestamp string.
        trace_id: Linked trace ID.
    """

    model_config = ConfigDict(frozen=True)

    message_id: str
    role: str = "agent"
    content: str
    timestamp: str = ""
    trace_id: str = ""


class ContextEntry(BaseModel):
    """A single context entry shown in the Context panel.

    Args:
        entry_id: Unique entry identifier.
        label: Human-readable label.
        value: Value string or summary.
        source: Where this context came from (e.g. ``"rag"``, ``"runtime"``, ``"artifact"``).
        token_count: Estimated token count for this context.
    """

    model_config = ConfigDict(frozen=True)

    entry_id: str
    label: str
    value: str = ""
    source: str = ""
    token_count: int = 0


class TraceEntry(BaseModel):
    """A single span in the trace panel.

    Args:
        trace_id: Trace identifier.
        span_id: Span identifier.
        operation: Operation name.
        status: ``"ok"`` | ``"error"`` | ``"in_progress"``.
        duration_ms: Duration in milliseconds (None if in progress).
        metadata: Extra span metadata.
    """

    model_config = ConfigDict(frozen=True)

    trace_id: str
    span_id: str
    operation: str
    status: str = "ok"
    duration_ms: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ConsoleAction(BaseModel):
    """An action button in the Actions panel of the right sidebar.

    Args:
        action_id: Unique action identifier.
        label: Button label.
        action_type: Action type.
        is_enabled: Whether the action is currently available.
        tooltip: Hover tooltip.
    """

    model_config = ConfigDict(frozen=True)

    action_id: str
    label: str
    action_type: str
    is_enabled: bool = True
    tooltip: str = ""


class RightSidebar(BaseModel):
    """Right sidebar agent console with Chat, Context, Trace, and Actions panels.

    Args:
        sidebar_id: Unique identifier.
        active_tab: Active tab (``"chat"`` | ``"context"`` | ``"trace"`` | ``"actions"``).
        chat_messages: Chat message history.
        context_entries: RAG/runtime context entries.
        trace_entries: Trace spans.
        console_actions: Available console actions.
        run_id: Active run.
        project_id: Active project.
        stage_name: Current stage.
        token_budget_used: Tokens consumed by current context.
        token_budget_total: Total token budget.
    """

    model_config = ConfigDict(frozen=True)

    sidebar_id: str
    active_tab: str = "chat"
    chat_messages: list[ChatMessage] = Field(default_factory=list)
    context_entries: list[ContextEntry] = Field(default_factory=list)
    trace_entries: list[TraceEntry] = Field(default_factory=list)
    console_actions: list[ConsoleAction] = Field(default_factory=list)
    run_id: str = ""
    project_id: str = ""
    stage_name: str = ""
    token_budget_used: int = 0
    token_budget_total: int = 4096


# ---------------------------------------------------------------------------
# Bottom panel: card-level controls
# ---------------------------------------------------------------------------

class CardControlType(str, Enum):
    """Type of a bottom panel card control."""
    BUTTON = "button"
    SLIDER = "slider"
    TOGGLE = "toggle"
    STATUS = "status"
    PROGRESS = "progress"


class CardControl(BaseModel):
    """A single control in the bottom panel.

    Args:
        control_id: Unique control identifier.
        label: Display label.
        control_type: :class:`CardControlType`.
        value: Current value (type depends on control_type).
        is_enabled: Whether the control is interactive.
        tooltip: Hover tooltip text.
    """

    model_config = ConfigDict(frozen=True)

    control_id: str
    label: str
    control_type: CardControlType = CardControlType.BUTTON
    value: Any = None
    is_enabled: bool = True
    tooltip: str = ""


class BottomPanel(BaseModel):
    """Bottom panel with active card controls and run status.

    Args:
        panel_id: Unique panel identifier.
        stage_name: Stage this panel is attached to.
        run_id: Active run.
        project_id: Active project.
        controls: Card-level controls.
        status_message: Current status message.
        progress_pct: Overall progress percentage (0–100).
        is_visible: Whether the panel is visible.
    """

    model_config = ConfigDict(frozen=True)

    panel_id: str
    stage_name: str = ""
    run_id: str = ""
    project_id: str = ""
    controls: list[CardControl] = Field(default_factory=list)
    status_message: str = ""
    progress_pct: float = 0.0
    is_visible: bool = True


# ---------------------------------------------------------------------------
# Builder functions
# ---------------------------------------------------------------------------

def build_workflow_tree(
    run_id: str,
    project_id: str,
    stages: list[dict[str, Any]],
    active_stage: str = "",
) -> LeftSidebar:
    """Build a :class:`LeftSidebar` from a flat stage list.

    Args:
        run_id: Active MDLC run.
        project_id: Active project.
        stages: List of stage dicts with at least ``name`` and ``status`` keys.
        active_stage: Name of the currently active stage.

    Returns:
        :class:`LeftSidebar`.
    """
    import uuid
    nodes: list[WorkflowTreeNode] = []
    status_map: dict[str, WorkflowTreeNodeStatus] = {
        "pending": WorkflowTreeNodeStatus.PENDING,
        "in_progress": WorkflowTreeNodeStatus.IN_PROGRESS,
        "completed": WorkflowTreeNodeStatus.COMPLETED,
        "failed": WorkflowTreeNodeStatus.FAILED,
        "blocked": WorkflowTreeNodeStatus.BLOCKED,
        "skipped": WorkflowTreeNodeStatus.SKIPPED,
    }
    for stage in stages:
        stage_name = str(stage.get("name", ""))
        status_str = str(stage.get("status", "pending")).lower()
        status = status_map.get(status_str, WorkflowTreeNodeStatus.PENDING)
        nodes.append(
            WorkflowTreeNode(
                node_id=f"stage-{stage_name}",
                label=stage_name.replace("_", " ").title(),
                node_type=WorkflowTreeNodeType.TASK,
                status=status,
                is_active=(stage_name == active_stage),
                is_expanded=(stage_name == active_stage),
            )
        )

    project_node = WorkflowTreeNode(
        node_id=f"project-{project_id}",
        label=project_id,
        node_type=WorkflowTreeNodeType.PROJECT,
        status=WorkflowTreeNodeStatus.IN_PROGRESS,
        children=nodes,
        is_expanded=True,
    )

    return LeftSidebar(
        sidebar_id=str(uuid.uuid4()),
        run_id=run_id,
        project_id=project_id,
        tree=[project_node],
        active_node_id=f"stage-{active_stage}" if active_stage else "",
    )


def build_agent_console(
    run_id: str,
    project_id: str,
    stage_name: str = "",
    messages: list[dict[str, Any]] | None = None,
    context_entries: list[dict[str, Any]] | None = None,
    trace_entries: list[dict[str, Any]] | None = None,
    token_budget_used: int = 0,
    token_budget_total: int = 4096,
) -> RightSidebar:
    """Build a :class:`RightSidebar` agent console.

    Args:
        run_id: Active run.
        project_id: Active project.
        stage_name: Current stage.
        messages: List of message dicts with ``role``, ``content``, ``message_id``.
        context_entries: List of context dicts.
        trace_entries: List of trace span dicts.
        token_budget_used: Tokens consumed.
        token_budget_total: Total token budget.

    Returns:
        :class:`RightSidebar`.
    """
    import uuid
    chat = [
        ChatMessage(
            message_id=m.get("message_id", str(uuid.uuid4())),
            role=m.get("role", "agent"),
            content=m.get("content", ""),
            timestamp=m.get("timestamp", ""),
            trace_id=m.get("trace_id", ""),
        )
        for m in (messages or [])
    ]
    ctx = [
        ContextEntry(
            entry_id=c.get("entry_id", str(uuid.uuid4())),
            label=c.get("label", ""),
            value=c.get("value", ""),
            source=c.get("source", ""),
            token_count=int(c.get("token_count", 0)),
        )
        for c in (context_entries or [])
    ]
    traces = [
        TraceEntry(
            trace_id=t.get("trace_id", ""),
            span_id=t.get("span_id", str(uuid.uuid4())),
            operation=t.get("operation", ""),
            status=t.get("status", "ok"),
            duration_ms=t.get("duration_ms"),
            metadata=t.get("metadata", {}),
        )
        for t in (trace_entries or [])
    ]
    default_actions = [
        ConsoleAction(action_id="refresh", label="Refresh", action_type="refresh", tooltip="Refresh context"),
        ConsoleAction(action_id="export_trace", label="Export Trace", action_type="export_trace", tooltip="Export current trace"),
        ConsoleAction(action_id="clear_chat", label="Clear Chat", action_type="clear_chat", tooltip="Clear chat history"),
    ]

    return RightSidebar(
        sidebar_id=str(uuid.uuid4()),
        run_id=run_id,
        project_id=project_id,
        stage_name=stage_name,
        chat_messages=chat,
        context_entries=ctx,
        trace_entries=traces,
        console_actions=default_actions,
        token_budget_used=token_budget_used,
        token_budget_total=token_budget_total,
    )


def build_bottom_panel(
    run_id: str,
    project_id: str,
    stage_name: str = "",
    status_message: str = "",
    progress_pct: float = 0.0,
    extra_controls: list[dict[str, Any]] | None = None,
) -> BottomPanel:
    """Build a :class:`BottomPanel` for active card controls.

    Args:
        run_id: Active run.
        project_id: Active project.
        stage_name: Active stage.
        status_message: Current status display text.
        progress_pct: Progress percentage 0–100.
        extra_controls: Additional custom control dicts.

    Returns:
        :class:`BottomPanel`.
    """
    import uuid
    controls: list[CardControl] = [
        CardControl(
            control_id="status_bar",
            label="Status",
            control_type=CardControlType.STATUS,
            value=status_message,
        ),
        CardControl(
            control_id="progress",
            label="Progress",
            control_type=CardControlType.PROGRESS,
            value=progress_pct,
        ),
    ]
    for ctrl in extra_controls or []:
        controls.append(
            CardControl(
                control_id=ctrl.get("control_id", str(uuid.uuid4())),
                label=ctrl.get("label", ""),
                control_type=CardControlType(ctrl.get("control_type", "button")),
                value=ctrl.get("value"),
                is_enabled=ctrl.get("is_enabled", True),
                tooltip=ctrl.get("tooltip", ""),
            )
        )

    return BottomPanel(
        panel_id=str(uuid.uuid4()),
        stage_name=stage_name,
        run_id=run_id,
        project_id=project_id,
        controls=controls,
        status_message=status_message,
        progress_pct=progress_pct,
    )


def render_sidebar_terminal(sidebar: LeftSidebar | RightSidebar | BottomPanel) -> str:
    """Render any sidebar or panel as ASCII terminal output.

    Args:
        sidebar: :class:`LeftSidebar`, :class:`RightSidebar`, or :class:`BottomPanel`.

    Returns:
        Terminal-friendly string.
    """
    if isinstance(sidebar, LeftSidebar):
        return _render_left_sidebar(sidebar)
    if isinstance(sidebar, RightSidebar):
        return _render_right_sidebar(sidebar)
    if isinstance(sidebar, BottomPanel):
        return _render_bottom_panel(sidebar)
    return str(sidebar)


def _render_left_sidebar(s: LeftSidebar) -> str:
    lines = [f"[LEFT SIDEBAR] {s.title}  run={s.run_id}  project={s.project_id}"]
    for node in s.tree:
        lines.extend(_render_tree_node(node, indent=0, active_id=s.active_node_id))
    return "\n".join(lines)


def _render_tree_node(node: WorkflowTreeNode, indent: int, active_id: str) -> list[str]:
    prefix = "  " * indent
    active_marker = " ← ACTIVE" if node.node_id == active_id else ""
    badge = f"  [{node.badge}]" if node.badge else ""
    status_icon = {
        WorkflowTreeNodeStatus.COMPLETED: "✓",
        WorkflowTreeNodeStatus.IN_PROGRESS: "▶",
        WorkflowTreeNodeStatus.FAILED: "✗",
        WorkflowTreeNodeStatus.BLOCKED: "⊘",
        WorkflowTreeNodeStatus.SKIPPED: "⊖",
    }.get(node.status, "○")
    lines = [f"{prefix}{status_icon} {node.label}{badge}{active_marker}"]
    for child in node.children:
        lines.extend(_render_tree_node(child, indent + 1, active_id))
    return lines


def _render_right_sidebar(s: RightSidebar) -> str:
    lines = [
        f"[RIGHT SIDEBAR] Agent Console  stage={s.stage_name}  run={s.run_id}",
        f"  Tokens: {s.token_budget_used}/{s.token_budget_total}",
        f"  Active tab: {s.active_tab.upper()}",
    ]
    if s.active_tab == "chat" and s.chat_messages:
        lines.append("  --- Chat ---")
        for msg in s.chat_messages[-5:]:
            lines.append(f"  [{msg.role.upper()}] {msg.content[:80]}")
    elif s.active_tab == "context" and s.context_entries:
        lines.append("  --- Context ---")
        for ctx in s.context_entries:
            lines.append(f"  {ctx.label}: {ctx.value[:60]}  (tokens={ctx.token_count})")
    elif s.active_tab == "trace" and s.trace_entries:
        lines.append("  --- Trace ---")
        for span in s.trace_entries:
            dur = f"{span.duration_ms:.1f}ms" if span.duration_ms is not None else "pending"
            lines.append(f"  {span.operation}: {span.status} ({dur})")
    elif s.active_tab == "actions":
        lines.append("  --- Actions ---")
        for action in s.console_actions:
            state = "ON" if action.is_enabled else "OFF"
            lines.append(f"  [{action.action_id}] {action.label} [{state}]")
    return "\n".join(lines)


def _render_bottom_panel(p: BottomPanel) -> str:
    bar = "#" * int(p.progress_pct / 5)
    empty = "." * (20 - len(bar))
    lines = [
        f"[BOTTOM PANEL] {p.stage_name}  run={p.run_id}",
        f"  Progress: [{bar}{empty}] {p.progress_pct:.0f}%",
        f"  Status  : {p.status_message}",
    ]
    for ctrl in p.controls:
        if ctrl.control_type not in (CardControlType.STATUS, CardControlType.PROGRESS):
            lines.append(f"  [{ctrl.control_id}] {ctrl.label}: {ctrl.value}")
    return "\n".join(lines)
