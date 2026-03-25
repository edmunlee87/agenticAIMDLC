# Python Code Skeleton- Jupyter bridge & Widget Event Contract  
  
# ================================================================  
# PYTHON CODE SKELETON  
# JUPYTER BRIDGE + WIDGET EVENT CONTRACT  
# AGENTIC AI MDLC FRAMEWORK  
# 3-PANEL HITL WORKSPACE INTEGRATION  
# ================================================================  
#  
# PURPOSE  
# ------------------------------------------------  
# This skeleton defines the interface between:  
# - JupyterLab widgets / frontend panels  
# - Jupyter bridge  
# - controllers  
# - runtime resolver  
#  
# It is designed for a 3-panel governed workspace:  
#  
#   LEFT PANEL   = navigation / candidates / flow / sections  
#   CENTER PANEL = main proposal / preview / charts / tables  
#   RIGHT PANEL  = actions / comments / approval / overrides  
#  
# It covers:  
# - event contracts  
# - payload schemas  
# - bridge orchestration  
# - workspace state model  
# - controller dispatch  
# - refresh protocol  
#  
# SUGGESTED FILES  
# ------------------------------------------------  
# platform_core/jupyter_bridge/  
#   event_models.py  
#   workspace_models.py  
#   payload_mapper.py  
#   event_router.py  
#   workspace_state_store.py  
#   jupyter_bridge.py  
#   widget_contracts.py  
#   callback_registry.py  
#  
# widgetsdk/  
#   review_shell_contract.py  
#   dashboard_contract.py  
#   flow_contract.py  
#  
# ================================================================  
  
  
# ================================================================  
# FILE: platform_core/jupyter_bridge/event_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from enum import Enum  
from typing import Any, Dict, List, Optional  
  
from pydantic import BaseModel, ConfigDict, Field, field_validator  
  
  
class JupyterBridgeBaseModel(BaseModel):  
    model_config = ConfigDict(  
        extra="forbid",  
        validate_assignment=True,  
        populate_by_name=True,  
    )  
  
  
class WorkspaceModeEnum(str, Enum):  
    REVIEW = "review"  
    DASHBOARD = "dashboard"  
    FLOW = "flow"  
    WIZARD = "wizard"  
    MIXED = "mixed"  
    CHAT = "chat"  
  
  
class PanelIdEnum(str, Enum):  
    LEFT = "left_panel"  
    CENTER = "center_panel"  
    RIGHT = "right_panel"  
    CHAT = "chat_panel"  
    BOTTOM = "bottom_panel"  
  
  
class EventTypeEnum(str, Enum):  
    LOAD_WORKSPACE = "load_workspace"  
    REFRESH_WORKSPACE = "refresh_workspace"  
    SELECT_NODE = "select_node"  
    SELECT_CANDIDATE = "select_candidate"  
    OPEN_REVIEW = "open_review"  
    SUBMIT_ACTION = "submit_action"  
    PREVIEW_EDIT = "preview_edit"  
    APPLY_EDIT = "apply_edit"  
    REQUEST_RERUN = "request_rerun"  
    REQUEST_ROUTE = "request_route"  
    OPEN_DETAIL = "open_detail"  
    FILTER_CHANGED = "filter_changed"  
    TAB_CHANGED = "tab_changed"  
    COMMENT_CHANGED = "comment_changed"  
    SAVE_DRAFT = "save_draft"  
    HEARTBEAT = "heartbeat"  
  
  
class ActionTypeEnum(str, Enum):  
    APPROVE = "approve"  
    APPROVE_WITH_CONDITIONS = "approve_with_conditions"  
    REJECT = "reject"  
    ESCALATE = "escalate"  
    ACCEPT_WITH_EDITS = "accept_with_edits"  
    RERUN_WITH_PARAMETERS = "rerun_with_parameters"  
    SAVE_NOTE = "save_note"  
    FINALIZE = "finalize"  
    NONE = "none"  
  
  
class ActorPayload(JupyterBridgeBaseModel):  
    actor_id: str  
    actor_role: str  
  
  
class WidgetEvent(JupyterBridgeBaseModel):  
    event_id: str  
    event_type: EventTypeEnum  
    workspace_id: str  
    panel_id: PanelIdEnum  
    actor: ActorPayload  
    payload: Dict[str, Any] = Field(default_factory=dict)  
    client_ts: Optional[str] = None  
  
    @field_validator("event_id", "workspace_id")  
    @classmethod  
    def validate_non_empty(cls, v: str) -> str:  
        if not v.strip():  
            raise ValueError("Value cannot be empty.")  
        return v  
  
  
class ActionSubmissionPayload(JupyterBridgeBaseModel):  
    review_id: Optional[str] = None  
    action_type: ActionTypeEnum  
    comment: Optional[str] = None  
    structured_edits: Dict[str, Any] = Field(default_factory=dict)  
    selected_candidate_id: Optional[str] = None  
    selected_node_id: Optional[str] = None  
    rerun_parameters: Dict[str, Any] = Field(default_factory=dict)  
    action_context: Dict[str, Any] = Field(default_factory=dict)  
  
  
class InteractionPayload(JupyterBridgeBaseModel):  
    stage_name: str  
    interaction_type: str  
    action: str  
    actor: ActorPayload  
    structured_edits: Dict[str, Any] = Field(default_factory=dict)  
    user_comment: Optional[str] = None  
    selected_candidate_id: Optional[str] = None  
    selected_node_id: Optional[str] = None  
    client_meta: Dict[str, Any] = Field(default_factory=dict)  
  
  
# ================================================================  
# FILE: platform_core/jupyter_bridge/workspace_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict, List, Optional  
  
from pydantic import Field  
  
from platform_core.jupyter_bridge.event_models import (  
    JupyterBridgeBaseModel,  
    WorkspaceModeEnum,  
)  
  
  
class WorkspaceRef(JupyterBridgeBaseModel):  
    workspace_id: str  
    project_id: Optional[str] = None  
    run_id: Optional[str] = None  
    review_id: Optional[str] = None  
    session_id: Optional[str] = None  
    mode: WorkspaceModeEnum  
  
  
class PanelState(JupyterBridgeBaseModel):  
    title: Optional[str] = None  
    selected_id: Optional[str] = None  
    visible: bool = True  
    loading: bool = False  
    error_message: Optional[str] = None  
    data: Dict[str, Any] = Field(default_factory=dict)  
  
  
class WorkspaceState(JupyterBridgeBaseModel):  
    workspace_ref: WorkspaceRef  
    left_panel: PanelState = Field(default_factory=PanelState)  
    center_panel: PanelState = Field(default_factory=PanelState)  
    right_panel: PanelState = Field(default_factory=PanelState)  
    chat_panel: PanelState = Field(default_factory=PanelState)  
    bottom_panel: PanelState = Field(default_factory=PanelState)  
    runtime_context: Dict[str, Any] = Field(default_factory=dict)  
    runtime_decision: Dict[str, Any] = Field(default_factory=dict)  
    allowed_actions: List[str] = Field(default_factory=list)  
    draft_state: Dict[str, Any] = Field(default_factory=dict)  
    refresh_token: int = 0  
  
  
class WorkspaceBuildRequest(JupyterBridgeBaseModel):  
    workspace_id: str  
    mode: WorkspaceModeEnum  
    runtime_context: Dict[str, Any]  
    seed_payload: Dict[str, Any] = Field(default_factory=dict)  
  
  
class WorkspaceRefreshRequest(JupyterBridgeBaseModel):  
    workspace_id: str  
    runtime_context: Dict[str, Any]  
    refresh_reason: str  
    patch_payload: Dict[str, Any] = Field(default_factory=dict)  
  
  
# ================================================================  
# FILE: platform_core/jupyter_bridge/widget_contracts.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict, List, Optional  
  
from pydantic import Field  
  
from platform_core.jupyter_bridge.event_models import JupyterBridgeBaseModel  
  
  
class ActionButtonSpec(JupyterBridgeBaseModel):  
    action_id: str  
    label: str  
    action_type: str  
    style_variant: str = "primary"  
    requires_comment: bool = False  
    disabled: bool = False  
    tooltip: Optional[str] = None  
  
  
class CandidateCardSpec(JupyterBridgeBaseModel):  
    candidate_id: str  
    title: str  
    subtitle: Optional[str] = None  
    metrics: List[Dict[str, Any]] = Field(default_factory=list)  
    warnings: List[str] = Field(default_factory=list)  
    selected: bool = False  
  
  
class DetailBlockSpec(JupyterBridgeBaseModel):  
    block_id: str  
    block_type: str  
    title: str  
    payload: Dict[str, Any] = Field(default_factory=dict)  
  
  
class ReviewShellContract(JupyterBridgeBaseModel):  
    workspace_id: str  
    review_id: str  
    left_navigation_items: List[Dict[str, Any]] = Field(default_factory=list)  
    candidate_cards: List[CandidateCardSpec] = Field(default_factory=list)  
    center_blocks: List[DetailBlockSpec] = Field(default_factory=list)  
    action_buttons: List[ActionButtonSpec] = Field(default_factory=list)  
    comment_box_enabled: bool = True  
    structured_edit_schema: Dict[str, Any] = Field(default_factory=dict)  
    context_summary: Dict[str, Any] = Field(default_factory=dict)  
  
  
class DashboardContract(JupyterBridgeBaseModel):  
    workspace_id: str  
    dashboard_title: str  
    filter_schema: Dict[str, Any] = Field(default_factory=dict)  
    kpi_cards: List[Dict[str, Any]] = Field(default_factory=list)  
    trend_blocks: List[DetailBlockSpec] = Field(default_factory=list)  
    notes_actions: List[ActionButtonSpec] = Field(default_factory=list)  
  
  
class FlowExplorerContract(JupyterBridgeBaseModel):  
    workspace_id: str  
    graph_nodes: List[Dict[str, Any]] = Field(default_factory=list)  
    graph_edges: List[Dict[str, Any]] = Field(default_factory=list)  
    timeline_items: List[Dict[str, Any]] = Field(default_factory=list)  
    selected_node_id: Optional[str] = None  
    detail_blocks: List[DetailBlockSpec] = Field(default_factory=list)  
  
  
# ================================================================  
# FILE: platform_core/jupyter_bridge/payload_mapper.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict, List  
  
from platform_core.jupyter_bridge.widget_contracts import (  
    ActionButtonSpec,  
    CandidateCardSpec,  
    DetailBlockSpec,  
    ReviewShellContract,  
    DashboardContract,  
    FlowExplorerContract,  
)  
  
  
class ReviewPayloadMapper:  
    """  
    Maps backend review payloads into UI contracts.  
    """  
  
    def map_review_payload(  
        self,  
        *,  
        workspace_id: str,  
        review_id: str,  
        review_payload: Dict[str, Any],  
    ) -> ReviewShellContract:  
        candidates = [  
            CandidateCardSpec(  
                candidate_id=str(item.get("candidate_id", "")),  
                title=item.get("title", "Candidate"),  
                subtitle=item.get("subtitle"),  
                metrics=item.get("metrics", []),  
                warnings=item.get("warnings", []),  
                selected=bool(item.get("selected", False)),  
            )  
            for item in review_payload.get("candidate_cards", [])  
        ]  
  
        blocks = [  
            DetailBlockSpec(  
                block_id=str(item.get("block_id", "")),  
                block_type=item.get("block_type", "summary"),  
                title=item.get("title", "Block"),  
                payload=item.get("payload", {}),  
            )  
            for item in review_payload.get("center_blocks", [])  
        ]  
  
        actions = [  
            ActionButtonSpec(  
                action_id=str(item.get("action_id", "")),  
                label=item.get("label", "Action"),  
                action_type=item.get("action_type", "none"),  
                style_variant=item.get("style_variant", "primary"),  
                requires_comment=bool(item.get("requires_comment", False)),  
                disabled=bool(item.get("disabled", False)),  
                tooltip=item.get("tooltip"),  
            )  
            for item in review_payload.get("action_buttons", [])  
        ]  
  
        return ReviewShellContract(  
            workspace_id=workspace_id,  
            review_id=review_id,  
            left_navigation_items=review_payload.get("left_navigation_items", []),  
            candidate_cards=candidates,  
            center_blocks=blocks,  
            action_buttons=actions,  
            comment_box_enabled=bool(review_payload.get("comment_box_enabled", True)),  
            structured_edit_schema=review_payload.get("structured_edit_schema", {}),  
            context_summary=review_payload.get("context_summary", {}),  
        )  
  
    def map_dashboard_payload(  
        self,  
        *,  
        workspace_id: str,  
        dashboard_payload: Dict[str, Any],  
    ) -> DashboardContract:  
        trend_blocks = [  
            DetailBlockSpec(  
                block_id=str(item.get("block_id", "")),  
                block_type=item.get("block_type", "trend"),  
                title=item.get("title", "Trend"),  
                payload=item.get("payload", {}),  
            )  
            for item in dashboard_payload.get("trend_blocks", [])  
        ]  
  
        notes_actions = [  
            ActionButtonSpec(  
                action_id=str(item.get("action_id", "")),  
                label=item.get("label", "Action"),  
                action_type=item.get("action_type", "none"),  
                style_variant=item.get("style_variant", "secondary"),  
                requires_comment=bool(item.get("requires_comment", False)),  
                disabled=bool(item.get("disabled", False)),  
                tooltip=item.get("tooltip"),  
            )  
            for item in dashboard_payload.get("notes_actions", [])  
        ]  
  
        return DashboardContract(  
            workspace_id=workspace_id,  
            dashboard_title=dashboard_payload.get("dashboard_title", "Monitoring Dashboard"),  
            filter_schema=dashboard_payload.get("filter_schema", {}),  
            kpi_cards=dashboard_payload.get("kpi_cards", []),  
            trend_blocks=trend_blocks,  
            notes_actions=notes_actions,  
        )  
  
    def map_flow_payload(  
        self,  
        *,  
        workspace_id: str,  
        flow_payload: Dict[str, Any],  
    ) -> FlowExplorerContract:  
        detail_blocks = [  
            DetailBlockSpec(  
                block_id=str(item.get("block_id", "")),  
                block_type=item.get("block_type", "detail"),  
                title=item.get("title", "Detail"),  
                payload=item.get("payload", {}),  
            )  
            for item in flow_payload.get("detail_blocks", [])  
        ]  
  
        return FlowExplorerContract(  
            workspace_id=workspace_id,  
            graph_nodes=flow_payload.get("graph_nodes", []),  
            graph_edges=flow_payload.get("graph_edges", []),  
            timeline_items=flow_payload.get("timeline_items", []),  
            selected_node_id=flow_payload.get("selected_node_id"),  
            detail_blocks=detail_blocks,  
        )  
  
  
# ================================================================  
# FILE: platform_core/jupyter_bridge/callback_registry.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Callable, Dict  
  
  
class CallbackRegistry:  
    """  
    Registry for frontend widget callback names -> backend handlers.  
    """  
  
    def __init__(self) -> None:  
        self._callbacks: Dict[str, Callable[..., Any]] = {}  
  
    def register(self, callback_name: str, fn: Callable[..., Any]) -> None:  
        self._callbacks[callback_name] = fn  
  
    def get(self, callback_name: str) -> Callable[..., Any]:  
        if callback_name not in self._callbacks:  
            raise KeyError(f"Callback not registered: {callback_name}")  
        return self._callbacks[callback_name]  
  
    def has(self, callback_name: str) -> bool:  
        return callback_name in self._callbacks  
  
  
# ================================================================  
# FILE: platform_core/jupyter_bridge/workspace_state_store.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Dict  
  
from platform_core.jupyter_bridge.workspace_models import WorkspaceState  
  
  
class WorkspaceStateStore:  
    """  
    In-memory store.  
    Replaceable later with Redis, file-backed, or DB-backed store.  
    """  
  
    def __init__(self) -> None:  
        self._state: Dict[str, WorkspaceState] = {}  
  
    def put(self, state: WorkspaceState) -> None:  
        self._state[state.workspace_ref.workspace_id] = state  
  
    def get(self, workspace_id: str) -> WorkspaceState:  
        if workspace_id not in self._state:  
            raise KeyError(f"Workspace state not found: {workspace_id}")  
        return self._state[workspace_id]  
  
    def exists(self, workspace_id: str) -> bool:  
        return workspace_id in self._state  
  
    def delete(self, workspace_id: str) -> None:  
        self._state.pop(workspace_id, None)  
  
  
# ================================================================  
# FILE: platform_core/jupyter_bridge/event_router.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict  
  
from platform_core.jupyter_bridge.event_models import (  
    EventTypeEnum,  
    WidgetEvent,  
    InteractionPayload,  
)  
  
  
class JupyterEventRouter:  
    """  
    Routes widget events to the correct controller action.  
    """  
  
    def __init__(  
        self,  
        *,  
        session_controller: Any,  
        workflow_controller: Any,  
        review_controller: Any,  
        dataprep_controller: Any,  
        validation_controller: Any,  
        monitoring_controller: Any,  
    ) -> None:  
        self.session_controller = session_controller  
        self.workflow_controller = workflow_controller  
        self.review_controller = review_controller  
        self.dataprep_controller = dataprep_controller  
        self.validation_controller = validation_controller  
        self.monitoring_controller = monitoring_controller  
  
    def route(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        event: WidgetEvent,  
    ) -> Dict[str, Any]:  
        if event.event_type == EventTypeEnum.OPEN_REVIEW:  
            return self.review_controller.open_review(  
                runtime_context=runtime_context,  
                review_id=event.payload["review_id"],  
                actor=event.actor.model_dump(),  
            )  
  
        if event.event_type == EventTypeEnum.SUBMIT_ACTION:  
            interaction_payload = {  
                "action": event.payload["action"],  
                "actor": event.actor.model_dump(),  
                "user_comment": event.payload.get("comment"),  
                "structured_edits": event.payload.get("structured_edits", {}),  
                "selected_candidate_id": event.payload.get("selected_candidate_id"),  
                "selected_node_id": event.payload.get("selected_node_id"),  
            }  
            return self.review_controller.submit_review_action(  
                runtime_context=runtime_context,  
                review_id=event.payload["review_id"],  
                interaction_payload=interaction_payload,  
            )  
  
        if event.event_type == EventTypeEnum.PREVIEW_EDIT:  
            return self.review_controller.get_review_payload(  
                runtime_context=runtime_context,  
                review_id=event.payload["review_id"],  
                review_type=event.payload["review_type"],  
                source_context=event.payload.get("source_context", {}),  
            )  
  
        if event.event_type == EventTypeEnum.REQUEST_ROUTE:  
            return self.workflow_controller.route_next(  
                runtime_context=runtime_context,  
                current_stage=runtime_context["stage_context"]["active_stage"],  
                context=event.payload,  
            )  
  
        if event.event_type == EventTypeEnum.REFRESH_WORKSPACE:  
            return {  
                "status": "success",  
                "message": "Workspace refresh acknowledged.",  
                "data": {},  
                "references": {  
                    "workspace_id": event.workspace_id,  
                },  
            }  
  
        raise ValueError(f"Unsupported event type: {event.event_type}")  
  
  
# ================================================================  
# FILE: platform_core/jupyter_bridge/jupyter_bridge.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict  
  
from platform_core.jupyter_bridge.event_models import WidgetEvent  
from platform_core.jupyter_bridge.payload_mapper import ReviewPayloadMapper  
from platform_core.jupyter_bridge.workspace_models import (  
    PanelState,  
    WorkspaceBuildRequest,  
    WorkspaceRef,  
    WorkspaceState,  
)  
from platform_core.jupyter_bridge.workspace_state_store import WorkspaceStateStore  
  
  
class JupyterBridge:  
    """  
    Main boundary layer between Jupyter frontend and backend controllers.  
    """  
  
    def __init__(  
        self,  
        *,  
        runtime_resolver: Any,  
        event_router: Any,  
        workspace_state_store: WorkspaceStateStore,  
        payload_mapper: ReviewPayloadMapper,  
    ) -> None:  
        self.runtime_resolver = runtime_resolver  
        self.event_router = event_router  
        self.workspace_state_store = workspace_state_store  
        self.payload_mapper = payload_mapper  
  
    # ------------------------------------------------------------  
    # Workspace lifecycle  
    # ------------------------------------------------------------  
    def build_workspace(self, request: WorkspaceBuildRequest) -> Dict[str, Any]:  
        runtime_decision = self.runtime_resolver.resolve(request.runtime_context)  
  
        state = WorkspaceState(  
            workspace_ref=WorkspaceRef(  
                workspace_id=request.workspace_id,  
                project_id=request.runtime_context.get("project_id"),  
                run_id=request.runtime_context.get("run_id"),  
                review_id=request.seed_payload.get("review_id"),  
                session_id=request.runtime_context.get("session_id"),  
                mode=request.mode,  
            ),  
            left_panel=PanelState(title="Navigation"),  
            center_panel=PanelState(title="Main Content"),  
            right_panel=PanelState(title="Actions"),  
            chat_panel=PanelState(title="Assistant"),  
            bottom_panel=PanelState(title="Details", visible=False),  
            runtime_context=request.runtime_context,  
            runtime_decision=runtime_decision,  
            allowed_actions=runtime_decision.get("allowed_tools", []),  
            draft_state={},  
            refresh_token=1,  
        )  
        self.workspace_state_store.put(state)  
  
        return {  
            "status": "success",  
            "message": "Workspace built successfully.",  
            "data": {  
                "workspace_state": state.model_dump(),  
            },  
            "references": {  
                "workspace_id": request.workspace_id,  
            },  
        }  
  
    def refresh_workspace(  
        self,  
        *,  
        workspace_id: str,  
        runtime_context: Dict[str, Any],  
        patch_payload: Dict[str, Any] | None = None,  
    ) -> Dict[str, Any]:  
        state = self.workspace_state_store.get(workspace_id)  
        runtime_decision = self.runtime_resolver.resolve(runtime_context)  
  
        state.runtime_context = runtime_context  
        state.runtime_decision = runtime_decision  
        state.allowed_actions = runtime_decision.get("allowed_tools", [])  
        state.refresh_token += 1  
  
        if patch_payload:  
            state.draft_state.update(patch_payload)  
  
        self.workspace_state_store.put(state)  
  
        return {  
            "status": "success",  
            "message": "Workspace refreshed successfully.",  
            "data": {  
                "workspace_state": state.model_dump(),  
            },  
            "references": {  
                "workspace_id": workspace_id,  
            },  
        }  
  
    # ------------------------------------------------------------  
    # Review workspace loaders  
    # ------------------------------------------------------------  
    def load_review_workspace(  
        self,  
        *,  
        workspace_id: str,  
        runtime_context: Dict[str, Any],  
        review_id: str,  
        review_payload: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        contract = self.payload_mapper.map_review_payload(  
            workspace_id=workspace_id,  
            review_id=review_id,  
            review_payload=review_payload,  
        )  
  
        state = self.workspace_state_store.get(workspace_id)  
        state.workspace_ref.review_id = review_id  
        state.left_panel.data = {  
            "left_navigation_items": contract.left_navigation_items,  
            "candidate_cards": [x.model_dump() for x in contract.candidate_cards],  
        }  
        state.center_panel.data = {  
            "center_blocks": [x.model_dump() for x in contract.center_blocks],  
            "context_summary": contract.context_summary,  
        }  
        state.right_panel.data = {  
            "action_buttons": [x.model_dump() for x in contract.action_buttons],  
            "comment_box_enabled": contract.comment_box_enabled,  
            "structured_edit_schema": contract.structured_edit_schema,  
        }  
        state.runtime_context = runtime_context  
        state.runtime_decision = self.runtime_resolver.resolve(runtime_context)  
        state.allowed_actions = state.runtime_decision.get("allowed_tools", [])  
        state.refresh_token += 1  
  
        self.workspace_state_store.put(state)  
  
        return {  
            "status": "success",  
            "message": "Review workspace loaded.",  
            "data": {  
                "workspace_state": state.model_dump(),  
                "review_contract": contract.model_dump(),  
            },  
            "references": {  
                "workspace_id": workspace_id,  
                "review_id": review_id,  
            },  
        }  
  
    def load_dashboard_workspace(  
        self,  
        *,  
        workspace_id: str,  
        runtime_context: Dict[str, Any],  
        dashboard_payload: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        contract = self.payload_mapper.map_dashboard_payload(  
            workspace_id=workspace_id,  
            dashboard_payload=dashboard_payload,  
        )  
  
        state = self.workspace_state_store.get(workspace_id)  
        state.left_panel.data = {  
            "filter_schema": contract.filter_schema,  
        }  
        state.center_panel.data = {  
            "kpi_cards": contract.kpi_cards,  
            "trend_blocks": [x.model_dump() for x in contract.trend_blocks],  
        }  
        state.right_panel.data = {  
            "notes_actions": [x.model_dump() for x in contract.notes_actions],  
        }  
        state.runtime_context = runtime_context  
        state.runtime_decision = self.runtime_resolver.resolve(runtime_context)  
        state.allowed_actions = state.runtime_decision.get("allowed_tools", [])  
        state.refresh_token += 1  
  
        self.workspace_state_store.put(state)  
  
        return {  
            "status": "success",  
            "message": "Dashboard workspace loaded.",  
            "data": {  
                "workspace_state": state.model_dump(),  
                "dashboard_contract": contract.model_dump(),  
            },  
            "references": {  
                "workspace_id": workspace_id,  
            },  
        }  
  
    def load_flow_workspace(  
        self,  
        *,  
        workspace_id: str,  
        runtime_context: Dict[str, Any],  
        flow_payload: Dict[str, Any],  
    ) -> Dict[str, Any]:  
        contract = self.payload_mapper.map_flow_payload(  
            workspace_id=workspace_id,  
            flow_payload=flow_payload,  
        )  
  
        state = self.workspace_state_store.get(workspace_id)  
        state.left_panel.data = {  
            "graph_nodes": contract.graph_nodes,  
        }  
        state.center_panel.data = {  
            "graph_edges": contract.graph_edges,  
            "timeline_items": contract.timeline_items,  
        }  
        state.right_panel.data = {  
            "selected_node_id": contract.selected_node_id,  
            "detail_blocks": [x.model_dump() for x in contract.detail_blocks],  
        }  
        state.runtime_context = runtime_context  
        state.runtime_decision = self.runtime_resolver.resolve(runtime_context)  
        state.allowed_actions = state.runtime_decision.get("allowed_tools", [])  
        state.refresh_token += 1  
  
        self.workspace_state_store.put(state)  
  
        return {  
            "status": "success",  
            "message": "Flow workspace loaded.",  
            "data": {  
                "workspace_state": state.model_dump(),  
                "flow_contract": contract.model_dump(),  
            },  
            "references": {  
                "workspace_id": workspace_id,  
            },  
        }  
  
    # ------------------------------------------------------------  
    # Event handling  
    # ------------------------------------------------------------  
    def handle_event(  
        self,  
        *,  
        runtime_context: Dict[str, Any],  
        event: WidgetEvent,  
    ) -> Dict[str, Any]:  
        state = self.workspace_state_store.get(event.workspace_id)  
  
        controller_result = self.event_router.route(  
            runtime_context=runtime_context,  
            event=event,  
        )  
  
        # Basic refresh strategy:  
        # - keep current draft state  
        # - bump refresh token  
        # - attach latest controller result to center panel meta  
        state.runtime_context = runtime_context  
        state.runtime_decision = self.runtime_resolver.resolve(runtime_context)  
        state.allowed_actions = state.runtime_decision.get("allowed_tools", [])  
        state.center_panel.data["last_controller_result"] = controller_result  
        state.refresh_token += 1  
  
        # Save comment draft if event had it  
        if "comment" in event.payload:  
            state.draft_state["last_comment"] = event.payload["comment"]  
  
        self.workspace_state_store.put(state)  
  
        return {  
            "status": "success",  
            "message": "Widget event handled successfully.",  
            "data": {  
                "controller_result": controller_result,  
                "workspace_state": state.model_dump(),  
            },  
            "references": {  
                "workspace_id": event.workspace_id,  
            },  
        }  
  
  
# ================================================================  
# FILE: widgetsdk/review_shell_contract.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict  
  
  
class ReviewShellRendererContract:  
    """  
    Frontend-facing contract reference.  
  
    A real widget implementation should accept a payload like:  
    {  
      "workspace_id": "...",  
      "left_navigation_items": [...],  
      "candidate_cards": [...],  
      "center_blocks": [...],  
      "action_buttons": [...],  
      "comment_box_enabled": true,  
      "structured_edit_schema": {...},  
      "context_summary": {...}  
    }  
  
    And emit events like:  
    - SELECT_CANDIDATE  
    - PREVIEW_EDIT  
    - SUBMIT_ACTION  
    - COMMENT_CHANGED  
    """  
  
    @staticmethod  
    def example_payload() -> Dict[str, Any]:  
        return {  
            "workspace_id": "ws_001",  
            "review_id": "rev_001",  
            "left_navigation_items": [  
                {"id": "sec_1", "label": "Summary"},  
                {"id": "sec_2", "label": "Candidates"},  
            ],  
            "candidate_cards": [  
                {  
                    "candidate_id": "cand_001",  
                    "title": "Candidate A",  
                    "subtitle": "Best tradeoff",  
                    "metrics": [{"metric_name": "gini", "metric_value": 0.42}],  
                    "warnings": [],  
                    "selected": True,  
                }  
            ],  
            "center_blocks": [  
                {  
                    "block_id": "summary_1",  
                    "block_type": "summary",  
                    "title": "Model Summary",  
                    "payload": {"text": "Summary content"},  
                }  
            ],  
            "action_buttons": [  
                {  
                    "action_id": "approve_btn",  
                    "label": "Approve",  
                    "action_type": "approve",  
                    "style_variant": "primary",  
                    "requires_comment": False,  
                    "disabled": False,  
                },  
                {  
                    "action_id": "approve_cond_btn",  
                    "label": "Approve with Conditions",  
                    "action_type": "approve_with_conditions",  
                    "style_variant": "secondary",  
                    "requires_comment": True,  
                    "disabled": False,  
                },  
            ],  
            "comment_box_enabled": True,  
            "structured_edit_schema": {  
                "fields": [  
                    {  
                        "field_name": "bin_group",  
                        "field_type": "list",  
                    }  
                ]  
            },  
            "context_summary": {  
                "stage": "coarse_classing_review",  
                "domain": "scorecard",  
            },  
        }  
  
  
# ================================================================  
# FILE: widgetsdk/dashboard_contract.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict  
  
  
class DashboardRendererContract:  
    @staticmethod  
    def example_payload() -> Dict[str, Any]:  
        return {  
            "workspace_id": "ws_dash_001",  
            "dashboard_title": "Monitoring Dashboard",  
            "filter_schema": {  
                "date_range": {"type": "date_range"},  
                "segment": {"type": "multi_select"},  
            },  
            "kpi_cards": [  
                {"title": "PSI", "value": 0.08, "status": "pass"},  
                {"title": "Bad Rate Drift", "value": 0.02, "status": "warning"},  
            ],  
            "trend_blocks": [  
                {  
                    "block_id": "trend_psi",  
                    "block_type": "trend",  
                    "title": "PSI Trend",  
                    "payload": {"series": []},  
                }  
            ],  
            "notes_actions": [  
                {  
                    "action_id": "save_note_btn",  
                    "label": "Save Note",  
                    "action_type": "save_note",  
                    "style_variant": "secondary",  
                    "requires_comment": True,  
                    "disabled": False,  
                }  
            ],  
        }  
  
  
# ================================================================  
# FILE: widgetsdk/flow_contract.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any, Dict  
  
  
class FlowRendererContract:  
    @staticmethod  
    def example_payload() -> Dict[str, Any]:  
        return {  
            "workspace_id": "ws_flow_001",  
            "graph_nodes": [  
                {"id": "n1", "label": "Data Prep", "status": "success"},  
                {"id": "n2", "label": "Fine Classing", "status": "success"},  
            ],  
            "graph_edges": [  
                {"source": "n1", "target": "n2"},  
            ],  
            "timeline_items": [  
                {"ts": "2026-03-18T10:00:00", "label": "Run started"},  
            ],  
            "selected_node_id": "n2",  
            "detail_blocks": [  
                {  
                    "block_id": "detail_1",  
                    "block_type": "detail",  
                    "title": "Fine Classing Detail",  
                    "payload": {"summary": "Completed"},  
                }  
            ],  
        }  
  
  
# ================================================================  
# OPTIONAL: QUICK WIRING EXAMPLE  
# ================================================================  
  
if __name__ == "__main__":  
    class DummyRuntimeResolver:  
        def resolve(self, runtime_context):  
            return {  
                "stage_name": runtime_context["stage_context"]["active_stage"],  
                "actor_role": runtime_context["active_role"],  
                "allowed_tools": [  
                    "get_review",  
                    "build_review_payload",  
                    "validate_review_action",  
                    "route_next_stage",  
                ],  
            }  
  
    class DummyReviewController:  
        def open_review(self, **kwargs):  
            return {  
                "status": "success",  
                "message": "Review opened.",  
                "data": {"review_status": "pending_review"},  
                "references": {"review_id": kwargs["review_id"]},  
            }  
  
        def get_review_payload(self, **kwargs):  
            return {  
                "status": "success",  
                "message": "Payload built.",  
                "data": {"review_payload": {}},  
            }  
  
        def submit_review_action(self, **kwargs):  
            return {  
                "status": "finalized",  
                "message": "Action submitted.",  
                "data": {"decision_record": {}},  
            }  
  
    class DummyWorkflowController:  
        def route_next(self, **kwargs):  
            return {  
                "status": "success",  
                "message": "Next stage routed.",  
                "data": {"recommended_next_stage": "next_stage"},  
            }  
  
    class DummyController:  
        pass  
  
    runtime_resolver = DummyRuntimeResolver()  
    payload_mapper = ReviewPayloadMapper()  
    state_store = WorkspaceStateStore()  
    event_router = JupyterEventRouter(  
        session_controller=DummyController(),  
        workflow_controller=DummyWorkflowController(),  
        review_controller=DummyReviewController(),  
        dataprep_controller=DummyController(),  
        validation_controller=DummyController(),  
        monitoring_controller=DummyController(),  
    )  
  
    bridge = JupyterBridge(  
        runtime_resolver=runtime_resolver,  
        event_router=event_router,  
        workspace_state_store=state_store,  
        payload_mapper=payload_mapper,  
    )  
  
    build_result = bridge.build_workspace(  
        WorkspaceBuildRequest(  
            workspace_id="ws_001",  
            mode=WorkspaceModeEnum.REVIEW,  
            runtime_context={  
                "session_id": "sess_001",  
                "project_id": "proj_001",  
                "run_id": "run_001",  
                "active_role": "governance",  
                "stage_context": {"active_stage": "coarse_classing_review"},  
            },  
            seed_payload={"review_id": "rev_001"},  
        )  
    )  
    print(build_result["message"])  
