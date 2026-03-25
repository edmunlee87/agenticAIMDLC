# Front End Widget Protocol Spec  
  
====================================================================  
FRONTEND WIDGET PROTOCOL SPEC  
JUPYTERLAB 3-PANEL HITL WORKSPACE  
AGENTIC AI MDLC FRAMEWORK  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This protocol defines how the JupyterLab frontend widget layer should  
communicate with the backend Jupyter bridge for the 3-panel governed  
workspace.  
  
It covers:  
- message names  
- payload shapes  
- lifecycle events  
- state synchronization rules  
- debounce rules  
- optimistic update rules  
- panel-to-panel coordination  
- error handling  
- refresh behavior  
- recovery behavior  
- security and guardrails  
  
This spec is intended for:  
- JupyterLab extension developers  
- widget developers  
- backend bridge developers  
- controller integrators  
- HITL UI designers  
  
====================================================================  
1. HIGH-LEVEL ARCHITECTURE  
====================================================================  
  
UI LAYOUT  
--------------------------------------------------------------------  
The governed workspace has 3 primary panels:  
  
1. LEFT PANEL  
   - navigation tree  
   - candidate list  
   - node list  
   - tabs / sections  
   - filters in some modes  
  
2. CENTER PANEL  
   - main content  
   - proposal summary  
   - charts / tables / previews  
   - evidence blocks  
   - flow graph / dashboard body  
  
3. RIGHT PANEL  
   - action buttons  
   - approval controls  
   - comment box  
   - structured edit controls  
   - rerun parameters  
   - escalation / conditions input  
  
Optional:  
4. CHAT PANEL  
   - assistant conversation  
   - compact contextual guidance  
   - non-authoritative explanation  
  
5. BOTTOM PANEL  
   - drilldown detail  
   - raw diagnostics  
   - logs / artifacts / evidence trace  
  
FRONTEND LAYERS  
--------------------------------------------------------------------  
Layer A: Presentation widgets  
- render cards, tabs, charts, forms, trees  
  
Layer B: Workspace state manager  
- stores active workspace state  
- handles local selections and drafts  
- coordinates panel state  
  
Layer C: Event dispatcher  
- converts UI actions into protocol messages  
  
Layer D: Bridge client  
- sends messages to backend Jupyter bridge  
- receives responses  
- normalizes response patches  
  
BACKEND LAYERS  
--------------------------------------------------------------------  
Layer E: JupyterBridge  
- workspace state hydration  
- contract mapping  
- event routing  
  
Layer F: Controllers  
- orchestrate runtime + SDK calls  
  
Layer G: Services / SDKs  
- do actual work  
  
====================================================================  
2. PROTOCOL DESIGN PRINCIPLES  
====================================================================  
  
1. Frontend is stateful, backend is authoritative  
--------------------------------------------------------------------  
- frontend may keep draft state  
- backend owns workflow state, review state, approvals, and final refs  
  
2. Use explicit event names  
--------------------------------------------------------------------  
No ambiguous generic messages like "do_action".  
  
3. Every event must include workspace_id  
--------------------------------------------------------------------  
This avoids cross-workspace contamination.  
  
4. Every mutating action must include actor context  
--------------------------------------------------------------------  
No hidden identity assumptions.  
  
5. Backend responses must be patch-friendly  
--------------------------------------------------------------------  
Return enough to update only affected UI regions.  
  
6. Frontend may do optimistic UI only for safe local-only actions  
--------------------------------------------------------------------  
Never optimistically finalize governed actions.  
  
7. Review/finalization stages must be conservative  
--------------------------------------------------------------------  
Prefer explicit refresh from backend after action.  
  
====================================================================  
3. WORKSPACE STATE MODEL  
====================================================================  
  
Canonical frontend state shape:  
  
{  
  "workspace_id": "ws_001",  
  "mode": "review",  
  "runtime_context": {},  
  "runtime_decision": {},  
  "panels": {  
    "left": {  
      "visible": true,  
      "loading": false,  
      "title": "Navigation",  
      "selected_id": null,  
      "data": {}  
    },  
    "center": {  
      "visible": true,  
      "loading": false,  
      "title": "Main Content",  
      "data": {}  
    },  
    "right": {  
      "visible": true,  
      "loading": false,  
      "title": "Actions",  
      "data": {}  
    },  
    "chat": {  
      "visible": true,  
      "loading": false,  
      "title": "Assistant",  
      "data": {}  
    },  
    "bottom": {  
      "visible": false,  
      "loading": false,  
      "title": "Details",  
      "data": {}  
    }  
  },  
  "draft_state": {  
    "comment": "",  
    "structured_edits": {},  
    "selected_candidate_id": null,  
    "selected_node_id": null,  
    "filters": {},  
    "rerun_parameters": {}  
  },  
  "allowed_actions": [],  
  "refresh_token": 1,  
  "last_server_sync_ts": null,  
  "dirty_flags": {  
    "comment": false,  
    "structured_edits": false,  
    "filters": false  
  }  
}  
  
====================================================================  
4. MESSAGE ENVELOPE  
====================================================================  
  
All frontend -> backend messages should follow this envelope:  
  
{  
  "event_id": "evt_001",  
  "event_type": "string",  
  "workspace_id": "ws_001",  
  "panel_id": "left_panel | center_panel | right_panel | chat_panel | bottom_panel",  
  "actor": {  
    "actor_id": "u001",  
    "actor_role": "governance"  
  },  
  "payload": {},  
  "client_ts": "2026-03-18T22:00:00+08:00",  
  "client_meta": {  
    "widget_version": "1.0.0",  
    "workspace_mode": "review",  
    "refresh_token": 5  
  }  
}  
  
All backend -> frontend responses should follow this envelope:  
  
{  
  "status": "success | success_with_warning | invalid_input | blocked | failed | pending_human_review | finalized | preview_ready",  
  "message": "string",  
  "workspace_id": "ws_001",  
  "server_ts": "2026-03-18T22:00:01+08:00",  
  "response_type": "workspace_patch | full_workspace | notification | validation_result",  
  "controller_result": {},  
  "workspace_patch": {},  
  "notifications": [],  
  "errors": [],  
  "warnings": [],  
  "refresh_required": false,  
  "new_refresh_token": 6  
}  
  
====================================================================  
5. EVENT TYPES  
====================================================================  
  
--------------------------------------------------------------------  
5.1 Workspace lifecycle events  
--------------------------------------------------------------------  
  
A. LOAD_WORKSPACE  
Purpose:  
- create or hydrate workspace  
  
Payload:  
{  
  "mode": "review | dashboard | flow | wizard | mixed | chat",  
  "seed_payload": {},  
  "runtime_context": {}  
}  
  
B. REFRESH_WORKSPACE  
Purpose:  
- ask backend for refreshed state  
  
Payload:  
{  
  "refresh_reason": "manual | post_action | server_recommended | route_change",  
  "patch_payload": {}  
}  
  
C. HEARTBEAT  
Purpose:  
- lightweight liveness and state consistency check  
  
Payload:  
{  
  "refresh_token": 5  
}  
  
--------------------------------------------------------------------  
5.2 Navigation / selection events  
--------------------------------------------------------------------  
  
D. SELECT_NODE  
Purpose:  
- select flow node or nav tree item  
  
Payload:  
{  
  "node_id": "n001",  
  "node_type": "flow_node | nav_item | section"  
}  
  
E. SELECT_CANDIDATE  
Purpose:  
- select candidate card  
  
Payload:  
{  
  "candidate_id": "cand_001"  
}  
  
F. TAB_CHANGED  
Purpose:  
- switch tab or section  
  
Payload:  
{  
  "tab_id": "summary_tab"  
}  
  
G. FILTER_CHANGED  
Purpose:  
- dashboard / list filter change  
  
Payload:  
{  
  "filter_changes": {  
    "segment": ["A", "B"],  
    "date_range": {  
      "start": "2026-01-01",  
      "end": "2026-03-31"  
    }  
  }  
}  
  
--------------------------------------------------------------------  
5.3 Review / action events  
--------------------------------------------------------------------  
  
H. OPEN_REVIEW  
Purpose:  
- open existing review in workspace  
  
Payload:  
{  
  "review_id": "rev_001"  
}  
  
I. COMMENT_CHANGED  
Purpose:  
- save or sync comment draft  
  
Payload:  
{  
  "comment": "string"  
}  
  
J. PREVIEW_EDIT  
Purpose:  
- ask backend to recompute preview for structured edits  
  
Payload:  
{  
  "review_id": "rev_001",  
  "review_type": "coarse_classing",  
  "structured_edits": {},  
  "source_context": {}  
}  
  
K. APPLY_EDIT  
Purpose:  
- commit accepted structured edits into draft action context  
  
Payload:  
{  
  "structured_edits": {}  
}  
  
L. SUBMIT_ACTION  
Purpose:  
- submit governed action to backend  
  
Payload:  
{  
  "review_id": "rev_001",  
  "action": "approve | approve_with_conditions | reject | escalate | accept_with_edits | rerun_with_parameters",  
  "comment": "string | null",  
  "structured_edits": {},  
  "selected_candidate_id": "string | null",  
  "selected_node_id": "string | null",  
  "rerun_parameters": {},  
  "action_context": {}  
}  
  
M. SAVE_DRAFT  
Purpose:  
- persist local draft state to backend if needed  
  
Payload:  
{  
  "draft_state": {}  
}  
  
--------------------------------------------------------------------  
5.4 Routing / detail events  
--------------------------------------------------------------------  
  
N. REQUEST_ROUTE  
Purpose:  
- ask backend what next stage should be  
  
Payload:  
{  
  "current_stage": "string",  
  "context": {}  
}  
  
O. OPEN_DETAIL  
Purpose:  
- open bottom/right detail view for selected item  
  
Payload:  
{  
  "detail_type": "artifact | finding | evidence | metric | flow_node",  
  "detail_id": "string"  
}  
  
====================================================================  
6. BACKEND RESPONSE TYPES  
====================================================================  
  
A. full_workspace  
--------------------------------------------------------------------  
Use when:  
- initial load  
- major mode change  
- review opened  
- dashboard/flow fully rebuilt  
  
Shape:  
{  
  "response_type": "full_workspace",  
  "workspace_patch": {  
    "replace_all": true,  
    "workspace_state": {}  
  }  
}  
  
B. workspace_patch  
--------------------------------------------------------------------  
Use when:  
- only one or two panels changed  
- small state updates needed  
  
Shape:  
{  
  "response_type": "workspace_patch",  
  "workspace_patch": {  
    "replace_all": false,  
    "panel_patches": {  
      "left_panel": {},  
      "center_panel": {},  
      "right_panel": {},  
      "bottom_panel": {}  
    },  
    "draft_state_patch": {},  
    "runtime_decision_patch": {},  
    "allowed_actions_patch": []  
  }  
}  
  
C. notification  
--------------------------------------------------------------------  
Use when:  
- no workspace repaint needed  
- message only  
  
Shape:  
{  
  "response_type": "notification",  
  "notifications": [  
    {  
      "level": "info | warning | error | success",  
      "message": "string"  
    }  
  ]  
}  
  
D. validation_result  
--------------------------------------------------------------------  
Use when:  
- immediate form/action validation response needed  
  
Shape:  
{  
  "response_type": "validation_result",  
  "validation": {  
    "is_valid": true,  
    "field_errors": {},  
    "global_errors": []  
  }  
}  
  
====================================================================  
7. PANEL COMMUNICATION RULES  
====================================================================  
  
LEFT -> CENTER  
--------------------------------------------------------------------  
Typical interactions:  
- selecting candidate updates center content  
- selecting section updates visible center blocks  
- selecting node updates flow detail  
  
Rule:  
- left panel never directly mutates backend state  
- left panel emits selection event  
- center refresh is usually local first, backend if detail needed  
  
CENTER -> RIGHT  
--------------------------------------------------------------------  
Typical interactions:  
- selected preview content informs right-side actions  
- preview metrics may disable/enable right-side buttons  
  
Rule:  
- center panel may set local derived state  
- right-side action enablement should ultimately follow backend  
  allowed_actions, not only frontend logic  
  
RIGHT -> CENTER  
--------------------------------------------------------------------  
Typical interactions:  
- preview edit recalculates center panel charts/tables  
- submit action may finalize and refresh center blocks  
  
Rule:  
- preview action may update center optimistically to "loading"  
- final action waits for backend response before definitive update  
  
CHAT -> ALL PANELS  
--------------------------------------------------------------------  
Typical interactions:  
- chat explains what is selected  
- chat suggests next actions  
- chat may ask backend for route or context pack  
  
Rule:  
- chat is advisory unless it triggers explicit event  
- chat must never silently finalize review actions  
  
BOTTOM PANEL  
--------------------------------------------------------------------  
Typical interactions:  
- detail drilldown from left/center/right  
- raw logs or evidence trace  
  
Rule:  
- bottom panel is secondary and should not block primary workspace  
- use lazy loading for heavy detail payloads  
  
====================================================================  
8. STATE SYNC RULES  
====================================================================  
  
Rule 1: Backend authority  
--------------------------------------------------------------------  
The following should always be considered backend-authoritative:  
- runtime_decision  
- allowed_actions  
- review status  
- workflow patch outcomes  
- selected final candidate  
- conclusion / approval / signoff state  
  
Rule 2: Frontend draft authority  
--------------------------------------------------------------------  
The following can stay frontend-local until submitted:  
- comment draft  
- structured edit draft  
- filter draft  
- rerun parameters draft  
- currently highlighted card/tab/node  
  
Rule 3: Refresh token  
--------------------------------------------------------------------  
Every backend response should include new_refresh_token.  
  
Frontend should:  
- store latest refresh token  
- discard stale async responses with older refresh token  
- use refresh token to avoid race-condition overwrite  
  
Rule 4: Partial patch merge  
--------------------------------------------------------------------  
Frontend patch merge order:  
1. runtime_decision_patch  
2. allowed_actions_patch  
3. panel_patches  
4. draft_state_patch  
5. metadata like refresh token  
  
Rule 5: Stale state handling  
--------------------------------------------------------------------  
If backend says refresh_required = true:  
- frontend should immediately call REFRESH_WORKSPACE  
- disable final action buttons until refresh completes  
  
====================================================================  
9. DEBOUNCE RULES  
====================================================================  
  
Debounce is important for performance and token thrift.  
  
A. COMMENT_CHANGED  
--------------------------------------------------------------------  
Debounce:  
- 400ms to 800ms  
  
Reason:  
- do not spam backend with every keystroke  
  
Recommended behavior:  
- local draft updates immediately  
- backend sync only on debounce expiry or blur  
  
B. FILTER_CHANGED  
--------------------------------------------------------------------  
Debounce:  
- 300ms for text filters  
- 0ms for dropdown/select filters  
- 500ms for range sliders  
  
Reason:  
- allow smooth UI without excessive refresh calls  
  
C. PREVIEW_EDIT  
--------------------------------------------------------------------  
Debounce:  
- 500ms to 1000ms  
- or explicit Preview button for heavy computations  
  
Reason:  
- preview computation may be expensive  
  
Best practice:  
- for heavy domain tasks like bin preview, use explicit Preview button  
  
D. HEARTBEAT  
--------------------------------------------------------------------  
Interval:  
- 20s to 60s  
- only while workspace tab active  
  
Reason:  
- lightweight session consistency check  
  
====================================================================  
10. OPTIMISTIC UPDATE RULES  
====================================================================  
  
Safe optimistic updates:  
--------------------------------------------------------------------  
Allowed:  
- local candidate highlight  
- local node selection  
- tab switch  
- comment draft save indicator  
- filter chips update  
- setting center/right panel loading indicators  
  
Unsafe optimistic updates:  
--------------------------------------------------------------------  
Not allowed:  
- final approval display  
- final candidate selection confirmation  
- validation conclusion finalization  
- workflow stage advancement  
- breach closure  
- signoff completion  
  
Preview-specific optimistic behavior:  
--------------------------------------------------------------------  
Allowed:  
- set center panel to loading  
- show "Preview updating..."  
- preserve old preview until new one returns  
  
Not allowed:  
- replace preview with assumed success before backend returns  
  
====================================================================  
11. ERROR HANDLING RULES  
====================================================================  
  
Error classes and frontend behavior:  
  
A. invalid_input  
--------------------------------------------------------------------  
Examples:  
- missing required comment  
- invalid structured edit schema  
- invalid action for state  
  
Frontend action:  
- show inline field errors  
- keep draft state  
- do not reset selection  
  
B. blocked  
--------------------------------------------------------------------  
Examples:  
- action not allowed by runtime decision  
- missing active review  
- stale state  
  
Frontend action:  
- show blocking banner  
- request REFRESH_WORKSPACE  
- disable final action buttons  
  
C. failed  
--------------------------------------------------------------------  
Examples:  
- server exception  
- SDK crash  
- temporary infrastructure issue  
  
Frontend action:  
- show error toast/banner  
- allow retry if retry_mode safe/limited  
- keep draft state when possible  
  
D. pending_human_review  
--------------------------------------------------------------------  
Examples:  
- review created and waiting on another actor  
  
Frontend action:  
- switch workspace to read/review wait mode  
- disable incompatible actions  
- show review status badge  
  
====================================================================  
12. REFRESH BEHAVIOR  
====================================================================  
  
When frontend must refresh immediately:  
--------------------------------------------------------------------  
- after SUBMIT_ACTION success  
- after REQUEST_ROUTE success  
- when backend returns refresh_required = true  
- when review status changes  
- when runtime_decision changes materially  
- when stale state detected  
  
When frontend may patch locally only:  
--------------------------------------------------------------------  
- comment draft updates  
- tab changes  
- left panel selection  
- bottom panel detail open if data already present  
  
Refresh modes:  
--------------------------------------------------------------------  
A. soft refresh  
- patch only affected panels  
  
B. hard refresh  
- rebuild full workspace  
  
Use hard refresh when:  
- workspace mode changes  
- review_id changes  
- route changes to another major stage  
- runtime_decision changes significantly  
- allowed_actions changed substantially  
  
====================================================================  
13. REVIEW-SPECIFIC PROTOCOL  
====================================================================  
  
Review open sequence:  
--------------------------------------------------------------------  
1. Frontend sends OPEN_REVIEW  
2. Backend returns review summary or review status  
3. Frontend sends or backend chains build_review_payload  
4. Backend returns full_workspace or workspace_patch  
5. Frontend renders review_shell  
  
Preview edit sequence:  
--------------------------------------------------------------------  
1. User changes structured edit controls in right panel  
2. Frontend stores local draft  
3. User clicks Preview or debounce expires  
4. Frontend sends PREVIEW_EDIT  
5. Center panel enters loading state  
6. Backend recomputes preview  
7. Backend returns workspace_patch with center_panel update  
8. Right panel remains intact  
  
Submit action sequence:  
--------------------------------------------------------------------  
1. User clicks Approve / Reject / Accept with Edits / Escalate  
2. Frontend validates minimal local requirements  
3. Frontend sends SUBMIT_ACTION  
4. Right panel enters submitting state  
5. Backend validates action  
6. Backend captures decision / writes audit / patches workflow  
7. Backend returns:  
   - controller_result  
   - workflow patch  
   - possibly refresh_required  
8. Frontend refreshes or patches accordingly  
  
====================================================================  
14. DASHBOARD-SPECIFIC PROTOCOL  
====================================================================  
  
Dashboard load sequence:  
--------------------------------------------------------------------  
1. Frontend sends LOAD_WORKSPACE with mode=dashboard  
2. Backend returns full workspace or dashboard contract  
3. Frontend renders KPI cards, trends, notes actions  
  
Filter change sequence:  
--------------------------------------------------------------------  
1. User changes filters  
2. Local draft updates immediately  
3. Debounced FILTER_CHANGED sent  
4. Backend recomputes dashboard payload  
5. Center panel patches  
6. Optional right panel notes/actions update  
  
Monitoring note sequence:  
--------------------------------------------------------------------  
1. User enters note/comment  
2. Frontend sends COMMENT_CHANGED or SAVE_DRAFT  
3. User clicks Save Note  
4. Frontend sends SUBMIT_ACTION or dedicated note event in future  
5. Backend persists note and returns patch  
  
====================================================================  
15. FLOW EXPLORER PROTOCOL  
====================================================================  
  
Flow load sequence:  
--------------------------------------------------------------------  
1. Frontend sends LOAD_WORKSPACE with mode=flow  
2. Backend returns graph nodes, edges, timeline, optional selected node  
3. Frontend renders left node list, center graph/timeline, right detail  
  
Node select sequence:  
--------------------------------------------------------------------  
1. User clicks node in graph or list  
2. Frontend updates local selection immediately  
3. Frontend sends SELECT_NODE if backend detail needed  
4. Backend returns detail patch  
5. Right or bottom panel refreshes with node detail  
  
====================================================================  
16. LOCAL VALIDATION RULES  
====================================================================  
  
Frontend should do light validation before backend call.  
  
For SUBMIT_ACTION:  
--------------------------------------------------------------------  
- require review_id when in review workspace  
- require action  
- require comment if action button says requires_comment = true  
- require selected_candidate_id if action depends on candidate selection  
- require structured_edits to match frontend schema shape if present  
  
But frontend validation should stay minimal.  
Backend remains source of truth.  
  
====================================================================  
17. SECURITY / GOVERNANCE RULES  
====================================================================  
  
1. No hidden actions  
--------------------------------------------------------------------  
Only render buttons/actions present in allowed_actions or action_buttons.  
  
2. Do not trust disabled-state only  
--------------------------------------------------------------------  
Even if a button is hidden/disabled, backend must still validate.  
  
3. Do not persist approval decisions locally without backend ack  
--------------------------------------------------------------------  
Local state must not imply governance completion.  
  
4. Do not let chat bypass action bar  
--------------------------------------------------------------------  
Chat can recommend, but final action still goes through explicit event.  
  
5. Preserve actor info on every mutation event  
--------------------------------------------------------------------  
Needed for auditability.  
  
====================================================================  
18. RECOMMENDED FRONTEND STATE MACHINE  
====================================================================  
  
Workspace lifecycle states:  
- idle  
- loading  
- ready  
- refreshing  
- submitting  
- blocked  
- error  
  
Review action states:  
- no_review  
- review_loading  
- review_ready  
- preview_loading  
- preview_ready  
- action_submitting  
- action_completed  
- awaiting_refresh  
- action_blocked  
- action_error  
  
Dashboard states:  
- dashboard_loading  
- dashboard_ready  
- dashboard_refreshing  
- dashboard_error  
  
Flow states:  
- flow_loading  
- flow_ready  
- detail_loading  
- detail_ready  
- flow_error  
  
====================================================================  
19. RECOMMENDED MESSAGE NAME LIST  
====================================================================  
  
Frontend -> Backend:  
- LOAD_WORKSPACE  
- REFRESH_WORKSPACE  
- HEARTBEAT  
- OPEN_REVIEW  
- SELECT_NODE  
- SELECT_CANDIDATE  
- TAB_CHANGED  
- FILTER_CHANGED  
- COMMENT_CHANGED  
- PREVIEW_EDIT  
- APPLY_EDIT  
- SUBMIT_ACTION  
- SAVE_DRAFT  
- REQUEST_ROUTE  
- OPEN_DETAIL  
  
Backend -> Frontend logical response intents:  
- FULL_WORKSPACE  
- WORKSPACE_PATCH  
- VALIDATION_RESULT  
- NOTIFICATION  
- REFRESH_REQUIRED  
  
====================================================================  
20. SAMPLE END-TO-END MESSAGE FLOWS  
====================================================================  
  
A. Coarse classing review approve flow  
--------------------------------------------------------------------  
  
1. OPEN_REVIEW  
{  
  "event_id": "evt_001",  
  "event_type": "OPEN_REVIEW",  
  "workspace_id": "ws_001",  
  "panel_id": "left_panel",  
  "actor": {"actor_id": "u001", "actor_role": "governance"},  
  "payload": {"review_id": "rev_001"}  
}  
  
2. Backend returns full workspace with review payload  
  
3. User clicks Approve in right panel  
  
4. SUBMIT_ACTION  
{  
  "event_id": "evt_002",  
  "event_type": "SUBMIT_ACTION",  
  "workspace_id": "ws_001",  
  "panel_id": "right_panel",  
  "actor": {"actor_id": "u001", "actor_role": "governance"},  
  "payload": {  
    "review_id": "rev_001",  
    "action": "approve",  
    "comment": "Approved after review.",  
    "structured_edits": {}  
  }  
}  
  
5. Backend returns:  
{  
  "status": "finalized",  
  "response_type": "workspace_patch",  
  "refresh_required": true,  
  "workspace_patch": {  
    "panel_patches": {  
      "right_panel": {"submitting": false}  
    }  
  }  
}  
  
6. Frontend immediately sends REFRESH_WORKSPACE  
  
B. Preview edited bins flow  
--------------------------------------------------------------------  
  
1. APPLY_EDIT local only  
2. PREVIEW_EDIT sent after user clicks Preview  
3. Center panel loading  
4. Backend returns preview patch  
5. Center panel updated  
6. Right panel keeps draft and actions  
  
C. Monitoring dashboard filter flow  
--------------------------------------------------------------------  
  
1. FILTER_CHANGED  
2. Debounced send  
3. Backend returns center panel KPI/trend patch  
4. Frontend merges patch, keeps current notes draft  
  
====================================================================  
21. IMPLEMENTATION RECOMMENDATIONS  
====================================================================  
  
Recommended frontend implementation pattern:  
--------------------------------------------------------------------  
- use one workspace store per workspace_id  
- use one event dispatcher service  
- keep panel components dumb where possible  
- keep state merge logic centralized  
- keep backend response normalization centralized  
  
Recommended backend bridge behavior:  
--------------------------------------------------------------------  
- always return workspace_id  
- always include response_type  
- always include refresh token  
- prefer panel patch over full workspace when possible  
- for governed actions, prefer refresh after finalization  
  
Recommended UX behavior:  
--------------------------------------------------------------------  
- show clear loading states per panel  
- disable final actions while submitting  
- preserve user comment/edit draft on recoverable errors  
- show audit/governance status badges clearly  
  
====================================================================  
22. NEXT BEST ARTIFACT  
====================================================================  
  
The strongest next artifact is a:  
  
JUPYTERLAB FRONTEND IMPLEMENTATION URD  
covering:  
- widget composition  
- Lumino panel layout  
- state store design  
- message bus  
- callback bindings  
- right sidebar / main area / bottom panel placement  
- responsiveness  
- accessibility  
- theming  
- error banners and loading skeletons  
  
That would be the best handoff for actual frontend development in  
JupyterLab.  
====================================================================  
END OF FRONTEND WIDGET PROTOCOL SPEC  
====================================================================  
