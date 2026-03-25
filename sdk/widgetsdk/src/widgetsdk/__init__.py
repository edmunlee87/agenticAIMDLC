"""widgetsdk -- 3-panel review workspace, sidebars, and bottom panel for HITL interactions."""

from widgetsdk.builders import build_recovery_workspace, build_review_workspace
from widgetsdk.models import (
    ActionButtonSpec,
    EvidenceCard,
    GovernanceStatusBar,
    ReviewFormField,
    ReviewWorkspace,
    WidgetMode,
)
from widgetsdk.renderer import render
from widgetsdk.sidebars import (
    BottomPanel,
    CardControl,
    CardControlType,
    ChatMessage,
    ConsoleAction,
    ContextEntry,
    LeftSidebar,
    RightSidebar,
    TraceEntry,
    WorkflowTreeNode,
    WorkflowTreeNodeStatus,
    WorkflowTreeNodeType,
    build_agent_console,
    build_bottom_panel,
    build_workflow_tree,
    render_sidebar_terminal,
)

__all__ = [
    # Review workspace
    "ActionButtonSpec",
    "EvidenceCard",
    "GovernanceStatusBar",
    "ReviewFormField",
    "ReviewWorkspace",
    "WidgetMode",
    "build_recovery_workspace",
    "build_review_workspace",
    "render",
    # Sidebars and panels
    "BottomPanel",
    "CardControl",
    "CardControlType",
    "ChatMessage",
    "ConsoleAction",
    "ContextEntry",
    "LeftSidebar",
    "RightSidebar",
    "TraceEntry",
    "WorkflowTreeNode",
    "WorkflowTreeNodeStatus",
    "WorkflowTreeNodeType",
    "build_agent_console",
    "build_bottom_panel",
    "build_workflow_tree",
    "render_sidebar_terminal",
]
