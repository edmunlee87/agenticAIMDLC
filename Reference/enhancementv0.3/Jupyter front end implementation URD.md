# Jupyter front end implementation URD  
  
====================================================================  
JUPYTERLAB FRONTEND IMPLEMENTATION URD  
3-PANEL HITL WORKSPACE FOR AGENTIC AI MDLC FRAMEWORK  
====================================================================  
  
DOCUMENT PURPOSE  
--------------------------------------------------------------------  
This document defines the frontend implementation requirements for a  
JupyterLab-based workspace that supports:  
  
- governed human-in-the-loop review  
- agent-assisted workflow execution  
- model development lifecycle interaction  
- monitoring dashboard interaction  
- flow / audit / observability exploration  
- structured decision capture  
  
This URD is intended as a direct handoff for:  
- JupyterLab extension developers  
- frontend engineers  
- widget developers  
- backend bridge integrators  
- UX designers  
- governance workflow implementers  
  
====================================================================  
1. OBJECTIVES  
====================================================================  
  
PRIMARY OBJECTIVES  
--------------------------------------------------------------------  
The frontend must provide a professional, seamless, and auditable user  
experience for:  
  
1. reviewing agent proposals  
2. previewing technical outputs  
3. editing bounded structured inputs  
4. capturing governed user decisions  
5. visualizing workflow and observability states  
6. interacting with monitoring dashboards  
7. resuming interrupted sessions cleanly  
  
SECONDARY OBJECTIVES  
--------------------------------------------------------------------  
The frontend should also:  
- fit naturally within JupyterLab  
- minimize unnecessary screen switching  
- allow role-based UX changes  
- keep the user aware of state, status, and next steps  
- preserve draft inputs across recoverable errors  
- remain extensible for future project types beyond scorecard  
  
====================================================================  
2. SCOPE  
====================================================================  
  
IN SCOPE  
--------------------------------------------------------------------  
- JupyterLab frontend extension  
- 3-panel governed workspace  
- main area workspace rendering  
- optional integration with right-side assistant panel  
- bottom detail panel support  
- state synchronization with backend bridge  
- action bar for review / approval / rerun / escalation  
- structured forms for edits and comments  
- monitoring dashboard workspace mode  
- flow explorer workspace mode  
- runtime-driven UI adaptation  
  
OUT OF SCOPE  
--------------------------------------------------------------------  
- actual modeling algorithms  
- SDK backend logic  
- long-term storage engine implementation  
- enterprise authentication implementation  
- non-Jupyter standalone web app  
- external notification infrastructure  
  
====================================================================  
3. TARGET ENVIRONMENT  
====================================================================  
  
RUNTIME ENVIRONMENT  
--------------------------------------------------------------------  
- JupyterLab extension environment  
- enterprise-controlled workstation / Citrix / internal environment  
- likely restricted outbound connectivity  
- must work with backend services hosted internally  
- should support lightweight frontend asset delivery  
  
TECHNOLOGY COMPATIBILITY  
--------------------------------------------------------------------  
Frontend should be compatible with:  
- JupyterLab shell layout model  
- Lumino widgets and dock panels  
- JupyterLab command registry  
- JupyterLab status bar integration  
- JupyterLab left/right sidebars  
- main area documents/widgets  
- theme change awareness  
  
====================================================================  
4. USER ROLES  
====================================================================  
  
PRIMARY USER ROLES  
--------------------------------------------------------------------  
1. Developer  
   - build artifacts  
   - review candidates  
   - accept bounded technical changes  
   - rerun deterministic steps  
  
2. Validator  
   - challenge methodology  
   - review evidence and findings  
   - finalize validation conclusion where permitted  
  
3. Monitoring User  
   - ingest or inspect monitoring outputs  
   - assess KPI breaches  
   - add notes and actions  
   - support annual review  
  
4. Governance User  
   - review decisions  
   - inspect audit flow  
   - approve or escalate where permitted  
  
5. Approver  
   - perform final approval/signoff actions  
  
6. System-Assisted Mode  
   - no direct UI user, but frontend should reflect system-driven changes  
  
====================================================================  
5. UX PRINCIPLES  
====================================================================  
  
PRINCIPLE 1: GOVERNED CLARITY  
--------------------------------------------------------------------  
The UI must always make it obvious:  
- what is being reviewed  
- what can be changed  
- what is final  
- what still needs human action  
- what is blocked by governance  
  
PRINCIPLE 2: PANEL SEPARATION OF RESPONSIBILITY  
--------------------------------------------------------------------  
Each panel should have a strong role:  
- left = navigation / selection / structure  
- center = content / preview / evidence / visuals  
- right = decision / comments / action controls  
  
PRINCIPLE 3: LOW-AMBIGUITY ACTIONS  
--------------------------------------------------------------------  
Users should not guess what a button does.  
Each action should clearly indicate:  
- effect  
- whether it is preview-only  
- whether comment is required  
- whether it is final  
- whether audit will be written  
  
PRINCIPLE 4: PROGRESSIVE DISCLOSURE  
--------------------------------------------------------------------  
Show the essential information first.  
Details should be expandable through:  
- accordions  
- tabs  
- bottom detail panel  
- drilldown popups or drawers  
  
PRINCIPLE 5: STRONG STATUS VISIBILITY  
--------------------------------------------------------------------  
The workspace must visibly show:  
- stage  
- review status  
- approval status  
- runtime status  
- loading state  
- last refresh  
- warning / error / blocked indicators  
  
====================================================================  
6. INFORMATION ARCHITECTURE  
====================================================================  
  
TOP-LEVEL WORKSPACE MODES  
--------------------------------------------------------------------  
The frontend must support the following modes:  
  
1. Review Mode  
   - primary mode for HITL and governance actions  
  
2. Dashboard Mode  
   - monitoring KPI and operational review mode  
  
3. Flow Explorer Mode  
   - workflow / observability graph and timeline mode  
  
4. Wizard Mode  
   - bootstrap / setup / resume / guided entry mode  
  
5. Mixed Mode  
   - technical work mode combining selection, content, and actions  
  
6. Chat Support Mode  
   - lightweight explanation or guidance mode  
  
WORKSPACE MODE SWITCHING  
--------------------------------------------------------------------  
Mode should be determined by backend runtime decision.  
Frontend should not independently guess mode.  
  
====================================================================  
7. LAYOUT REQUIREMENTS  
====================================================================  
  
PRIMARY LAYOUT  
--------------------------------------------------------------------  
The main governed workspace should render in JupyterLab main area.  
  
Recommended layout:  
  
------------------------------------------------------------  
| Header / Context Bar                                      |  
------------------------------------------------------------  
| Left Panel | Center Panel                 | Right Panel   |  
|            |                              |               |  
|            |                              |               |  
|            |                              |               |  
------------------------------------------------------------  
| Optional Bottom Detail Panel                              |  
------------------------------------------------------------  
  
HEADER / CONTEXT BAR  
--------------------------------------------------------------------  
The header area should show:  
- project name  
- run id or short run tag  
- stage name  
- actor role  
- workspace mode  
- review id if applicable  
- high-level status badge  
- refresh indicator  
- last updated timestamp  
- quick commands such as refresh / route next / open flow  
  
LEFT PANEL  
--------------------------------------------------------------------  
Should support:  
- navigation tree  
- candidate list  
- stage sections  
- filters  
- flow nodes  
- tabs  
- compact summaries  
  
CENTER PANEL  
--------------------------------------------------------------------  
Should support:  
- proposal summaries  
- charts  
- tables  
- evidence cards  
- preview diffs  
- graph/timeline  
- KPI cards  
- diagnostics summaries  
  
RIGHT PANEL  
--------------------------------------------------------------------  
Should support:  
- action buttons  
- approval controls  
- escalation controls  
- comment box  
- structured edit forms  
- rerun parameter forms  
- action requirements and warnings  
  
BOTTOM PANEL  
--------------------------------------------------------------------  
Should be optional and collapsible.  
Use it for:  
- raw diagnostics  
- evidence detail  
- selected node detail  
- logs  
- audit trace drilldown  
- large table detail  
  
====================================================================  
8. JUPYTERLAB SHELL PLACEMENT REQUIREMENTS  
====================================================================  
  
MAIN AREA  
--------------------------------------------------------------------  
The primary governed workspace must live in JupyterLab main area.  
  
Reason:  
- most space  
- better for multi-panel content  
- natural for complex reviews  
- suitable for dashboards and charts  
  
RIGHT SIDEBAR  
--------------------------------------------------------------------  
The existing organization assistant, such as a general coding assistant,  
may already occupy the right sidebar.  
  
Therefore:  
- the governed workspace should not depend on owning the main right  
  sidebar permanently  
- the review workspace should instead live in main area  
- the existing assistant sidebar should remain usable as an auxiliary  
  support tool  
  
OPTIONAL RIGHT-SIDEBAR INTEGRATION  
--------------------------------------------------------------------  
If desired, a lightweight companion sidebar can be added for:  
- workspace mini-summary  
- quick status  
- recent actions  
- shortcuts to open the main workspace  
  
LEFT SIDEBAR  
--------------------------------------------------------------------  
Optional use cases:  
- workspace launcher  
- project navigator  
- recent reviews  
- recent runs  
- saved templates  
  
BOTTOM AREA / BOTTOM PANEL  
--------------------------------------------------------------------  
If supported by extension design, use for:  
- detail console  
- action log  
- evidence drilldown  
- preview diff details  
  
STATUS BAR  
--------------------------------------------------------------------  
Status bar integration should show:  
- workspace connected/disconnected  
- current mode  
- pending action count  
- unsaved draft indicator  
- refresh / sync status  
  
====================================================================  
9. COMPONENT REQUIREMENTS  
====================================================================  
  
9.1 Context Header Component  
--------------------------------------------------------------------  
Must display:  
- project label  
- run label  
- stage badge  
- role badge  
- review badge if any  
- status chip  
- refresh button  
- open flow button  
- open monitoring button when relevant  
  
9.2 Navigation Tree Component  
--------------------------------------------------------------------  
Should support:  
- hierarchical nodes  
- expandable/collapsible groups  
- active selection state  
- status markers per node  
- click to load detail  
  
9.3 Candidate Card List  
--------------------------------------------------------------------  
Should support:  
- one card per candidate  
- title and subtitle  
- small metric summary  
- warning badges  
- selected state  
- click to select candidate  
  
9.4 Content Block Renderer  
--------------------------------------------------------------------  
Should support different block types:  
- summary text  
- metric grid  
- chart placeholder/container  
- table placeholder/container  
- evidence card  
- diagnostic panel  
- diff panel  
- trend block  
- narrative block  
  
9.5 Action Bar / Action Controls  
--------------------------------------------------------------------  
Should support:  
- approve  
- approve with conditions  
- reject  
- escalate  
- preview  
- rerun with parameters  
- finalize  
- save note  
  
Each action must support:  
- enabled / disabled state  
- tooltip  
- loading state  
- reason if disabled  
- confirmation prompt for irreversible action  
  
9.6 Comment Box  
--------------------------------------------------------------------  
Should support:  
- autosave draft  
- explicit clear  
- validation for required comment  
- long text input  
- optional markdown-lite rendering later  
  
9.7 Structured Edit Form  
--------------------------------------------------------------------  
Should support:  
- schema-driven rendering  
- text input  
- number input  
- checkbox  
- dropdown  
- multi-select  
- list/group input  
- validation messages  
- preview action  
  
9.8 Detail Drawer / Bottom Detail  
--------------------------------------------------------------------  
Should support:  
- open by clicking a detail link  
- show richer evidence / logs / metrics  
- allow copy/export for governance review  
  
====================================================================  
10. STATE MANAGEMENT REQUIREMENTS  
====================================================================  
  
FRONTEND STORE  
--------------------------------------------------------------------  
There should be a centralized workspace state store per workspace_id.  
  
The store must contain:  
- workspace metadata  
- runtime_context  
- runtime_decision  
- panel states  
- current selection  
- allowed actions  
- draft state  
- refresh token  
- loading flags  
- dirty flags  
- last controller result summary  
  
LOCAL VS AUTHORITATIVE STATE  
--------------------------------------------------------------------  
Local state:  
- current comment draft  
- current structured edit draft  
- selected tab  
- selected candidate highlight  
- selected node highlight  
- filter draft  
  
Authoritative backend state:  
- review status  
- workflow stage  
- final decision outcome  
- approval status  
- allowed actions  
- active review binding  
- final selected candidate  
- validation conclusion  
- monitoring breach disposition  
  
DIRTY STATE RULES  
--------------------------------------------------------------------  
Dirty flags must track:  
- unsaved comment  
- unsaved edits  
- unsaved filters  
- unsaved rerun parameters  
  
Dirty state should survive recoverable refreshes where possible.  
  
====================================================================  
11. EVENT BUS AND MESSAGE HANDLING  
====================================================================  
  
EVENT DISPATCHER  
--------------------------------------------------------------------  
Frontend should have a centralized dispatcher that:  
- builds outbound message envelopes  
- attaches workspace id  
- attaches actor context  
- attaches refresh token  
- routes responses to state store updater  
  
MESSAGE PROCESSING  
--------------------------------------------------------------------  
Each outbound message should:  
1. validate required payload fields  
2. mark relevant panel loading state  
3. send to bridge  
4. receive response  
5. apply patch or replace workspace state  
6. clear relevant loading state  
7. handle error or refresh if required  
  
STALE RESPONSE HANDLING  
--------------------------------------------------------------------  
Responses with older refresh token than current workspace token should  
be ignored or handled cautiously.  
  
====================================================================  
12. RENDERING RULES  
====================================================================  
  
RENDERING STRATEGY  
--------------------------------------------------------------------  
Use component-level rendering based on payload contracts.  
Do not hardcode each project’s layout manually.  
  
A config-driven block renderer is preferred.  
  
REQUIRED RENDERING CAPABILITIES  
--------------------------------------------------------------------  
- cards  
- trees  
- accordions  
- tabs  
- split panels  
- tables  
- chart containers  
- timeline list  
- flow graph container  
- status badges  
- banners  
- confirmation modals  
- empty state panels  
- skeleton loaders  
  
EMPTY STATES  
--------------------------------------------------------------------  
Each panel should support graceful empty state:  
- no candidate selected  
- no review loaded  
- no chart available  
- no details available  
- no actions permitted  
  
====================================================================  
13. LOADING AND PERFORMANCE REQUIREMENTS  
====================================================================  
  
LOADING STATES  
--------------------------------------------------------------------  
Each panel should have independent loading state.  
  
Examples:  
- left panel loading candidate list  
- center panel loading preview result  
- right panel submitting decision  
  
SKELETONS  
--------------------------------------------------------------------  
Use skeleton loaders for:  
- cards  
- tables  
- content blocks  
- dashboard tiles  
  
PERFORMANCE GUIDELINES  
--------------------------------------------------------------------  
- avoid full workspace rerender unless necessary  
- prefer panel patches  
- lazy load bottom detail  
- lazy load heavy graph/timeline when opened  
- debounce noisy events  
- avoid excessive backend calls for text input  
  
====================================================================  
14. DEBOUNCE AND THROTTLE REQUIREMENTS  
====================================================================  
  
COMMENT INPUT  
--------------------------------------------------------------------  
- debounce save draft at around 500ms  
- no backend roundtrip for every keystroke unless required  
  
FILTER INPUT  
--------------------------------------------------------------------  
- dropdown/select immediate  
- text filters debounced  
- range slider throttled/debounced  
  
PREVIEW ACTION  
--------------------------------------------------------------------  
Heavy technical preview should be explicit button-first.  
Debounced auto-preview can exist later, but explicit preview is safer.  
  
HEARTBEAT / POLLING  
--------------------------------------------------------------------  
If needed:  
- heartbeat every 20 to 60 seconds  
- active workspace only  
- disabled when tab inactive if possible  
  
====================================================================  
15. OPTIMISTIC UI REQUIREMENTS  
====================================================================  
  
ALLOWED OPTIMISTIC UPDATES  
--------------------------------------------------------------------  
- local selection highlight  
- tab selection  
- show local draft  
- show loading state  
- panel expand/collapse  
- filter chip visuals  
  
DISALLOWED OPTIMISTIC UPDATES  
--------------------------------------------------------------------  
- final approval state  
- final conclusion state  
- signoff completion  
- final workflow stage transition  
- final candidate selection outcome  
  
PREVIEW CASE  
--------------------------------------------------------------------  
Preview requests may optimistically show loading, but not assumed success.  
  
====================================================================  
16. ERROR HANDLING REQUIREMENTS  
====================================================================  
  
ERROR DISPLAY ZONES  
--------------------------------------------------------------------  
Errors should be shown in appropriate places:  
- field-level errors near form fields  
- panel-level errors inside affected panel  
- workspace-level blocking banner for governance issues  
- toast/notification for temporary operational messages  
  
ERROR TYPES  
--------------------------------------------------------------------  
1. Validation error  
   - highlight field  
   - preserve draft  
  
2. Permission / blocked error  
   - show banner  
   - disable final actions  
   - recommend refresh  
  
3. Backend failure  
   - show retry option where safe  
   - preserve draft if possible  
  
4. Stale state  
   - show “workspace out of date” banner  
   - force refresh or guided refresh  
  
====================================================================  
17. GOVERNANCE UX REQUIREMENTS  
====================================================================  
  
ACTION CLARITY  
--------------------------------------------------------------------  
Final actions must be visibly distinct from preview actions.  
  
For example:  
- Preview = neutral/secondary visual emphasis  
- Approve / Finalize = primary emphasis  
- Reject / Escalate = warning or danger emphasis  
  
CONFIRMATION DIALOGS  
--------------------------------------------------------------------  
Should be required for:  
- approval with conditions  
- rejection  
- escalation  
- finalization  
- signoff  
  
ACTION REQUIREMENT DISPLAY  
--------------------------------------------------------------------  
Right panel should clearly show:  
- whether comment is required  
- whether audit will be written  
- whether action is irreversible  
- whether action will route workflow  
  
STATUS BADGES  
--------------------------------------------------------------------  
Show badges for:  
- pending review  
- awaiting approval  
- blocked  
- conditionally approved  
- finalized  
- stale  
- refresh required  
  
====================================================================  
18. ASSISTANT / CHAT INTEGRATION REQUIREMENTS  
====================================================================  
  
ROLE OF CHAT  
--------------------------------------------------------------------  
Chat should be supportive, not authoritative.  
  
Chat can:  
- explain current stage  
- explain current selection  
- summarize center content  
- suggest next steps  
- help user interpret a metric or finding  
  
Chat must not:  
- silently submit final actions  
- bypass explicit action buttons  
- alter authoritative state without explicit event  
  
INTEGRATION MODEL  
--------------------------------------------------------------------  
If existing assistant already occupies a right sidebar:  
- keep it separate  
- allow deep-link from governed workspace to assistant context  
- optionally pass read-only context summary to assistant  
- do not couple critical workflows to assistant availability  
  
====================================================================  
19. ACCESSIBILITY AND USABILITY REQUIREMENTS  
====================================================================  
  
ACCESSIBILITY  
--------------------------------------------------------------------  
The frontend should support:  
- keyboard navigation  
- visible focus states  
- readable contrast  
- semantic labeling for controls  
- descriptive tooltips  
- non-color-only status indicators  
  
USABILITY  
--------------------------------------------------------------------  
- large enough click targets  
- scroll-safe action region  
- no critical action hidden below fold without visual cue  
- stable layout during refresh  
- avoid sudden panel jumps  
  
====================================================================  
20. RESPONSIVENESS REQUIREMENTS  
====================================================================  
  
MAIN AREA RESPONSIVENESS  
--------------------------------------------------------------------  
The layout should adapt to narrower widths by:  
- allowing left panel collapse  
- allowing right panel collapse  
- prioritizing center panel width  
- moving detail blocks into tabs or bottom area when needed  
  
MINIMUM USABLE MODES  
--------------------------------------------------------------------  
At narrower width:  
- left panel may collapse into icon or drawer  
- right panel may become tabbed drawer  
- center panel stays primary  
  
Do not rely on mobile-only patterns.  
Primary target is desktop JupyterLab environment.  
  
====================================================================  
21. THEMING REQUIREMENTS  
====================================================================  
  
THEME AWARENESS  
--------------------------------------------------------------------  
The extension should respond to JupyterLab theme changes:  
- light / dark  
- font colors  
- border colors  
- panel backgrounds  
- status badges with accessible contrast  
  
DESIGN TOKENS  
--------------------------------------------------------------------  
Use a small token layer for:  
- spacing  
- radius  
- border styles  
- badge colors  
- banner colors  
- typography sizes  
  
====================================================================  
22. COMMANDS AND SHORTCUTS  
====================================================================  
  
RECOMMENDED COMMANDS  
--------------------------------------------------------------------  
- Open governed workspace  
- Refresh workspace  
- Open flow explorer  
- Open monitoring dashboard  
- Toggle bottom detail panel  
- Focus comment box  
- Submit preview  
- Submit primary action  
- Clear local draft  
  
KEYBOARD SHORTCUTS  
--------------------------------------------------------------------  
Examples:  
- Ctrl/Cmd + R for refresh workspace  
- Ctrl/Cmd + Enter for primary action in some contexts  
- Esc to close detail drawer or modal  
- Alt + 1/2/3 to focus left/center/right panel optionally  
  
All shortcuts should avoid conflicting with core JupyterLab defaults.  
  
====================================================================  
23. PERSISTENCE REQUIREMENTS  
====================================================================  
  
LOCAL PERSISTENCE  
--------------------------------------------------------------------  
Frontend may locally persist:  
- current panel widths  
- panel collapse state  
- last selected tab  
- non-sensitive draft content if allowed by policy  
  
CAUTION  
--------------------------------------------------------------------  
Do not persist sensitive or governance-critical final state solely in  
frontend local storage.  
  
SESSION RESUME UX  
--------------------------------------------------------------------  
When resuming:  
- restore layout preferences  
- restore last non-authoritative draft if safe  
- fetch authoritative workspace state from backend  
- clearly indicate restored draft vs authoritative state  
  
====================================================================  
24. SECURITY REQUIREMENTS  
====================================================================  
  
FRONTEND SECURITY  
--------------------------------------------------------------------  
- never assume hidden button means authorized  
- always rely on backend allowed_actions  
- sanitize rendered text content  
- do not execute arbitrary HTML from payload  
- protect against malformed widget payloads  
  
BACKEND COORDINATION  
--------------------------------------------------------------------  
- every mutating event includes actor context  
- every final action revalidated server-side  
- every approval/finalization reflected only after backend confirmation  
  
====================================================================  
25. OBSERVABILITY REQUIREMENTS  
====================================================================  
  
FRONTEND OBSERVABILITY  
--------------------------------------------------------------------  
The frontend should log or surface:  
- workspace load success/failure  
- event dispatch success/failure  
- refresh count  
- current refresh token  
- panel load duration if possible  
- most recent controller result summary  
  
USER-VISIBLE STATUS  
--------------------------------------------------------------------  
Show:  
- syncing  
- refreshed  
- blocked  
- draft saved  
- preview updated  
- awaiting decision  
  
====================================================================  
26. TESTING REQUIREMENTS  
====================================================================  
  
UNIT TESTS  
--------------------------------------------------------------------  
Should cover:  
- state reducer / patch merge logic  
- event envelope construction  
- debounce handling  
- stale response rejection  
- button enable/disable logic  
- form validation logic  
  
INTEGRATION TESTS  
--------------------------------------------------------------------  
Should cover:  
- load workspace  
- open review  
- preview edit  
- submit action  
- refresh after finalization  
- dashboard filter refresh  
- flow node detail open  
  
UX TEST SCENARIOS  
--------------------------------------------------------------------  
Should include:  
- review with multiple candidates  
- preview failure but draft preserved  
- stale state detected after long session  
- action blocked by role  
- monitoring breach review flow  
- validation conclusion finalization flow  
  
====================================================================  
27. FUTURE-PROOFING REQUIREMENTS  
====================================================================  
  
The frontend should be designed to support future additions such as:  
- additional domain-specific cards  
- richer chart integration  
- multi-step rerun configuration panels  
- embedded artifact viewers  
- document export preview  
- side-by-side candidate comparison  
- inline diff rendering for configs and decisions  
- timeline playback for audit review  
  
Preferred strategy:  
- contract-driven rendering  
- schema-driven forms  
- modular panel components  
- shared workspace state core  
  
====================================================================  
28. DELIVERABLES  
====================================================================  
  
MINIMUM DELIVERABLES  
--------------------------------------------------------------------  
1. JupyterLab extension shell  
2. Main-area workspace widget  
3. 3-panel review workspace  
4. Dashboard workspace  
5. Flow explorer workspace  
6. Shared state store  
7. Event dispatcher  
8. Bridge client  
9. Loading/error/banner system  
10. Action bar and structured form framework  
  
NICE-TO-HAVE DELIVERABLES  
--------------------------------------------------------------------  
1. Workspace launcher sidebar  
2. Status bar widget  
3. Draft recovery helper  
4. Command palette integration  
5. Keyboard shortcut set  
6. Theme token layer  
7. Panel layout persistence  
  
====================================================================  
29. ACCEPTANCE CRITERIA  
====================================================================  
  
A. Review workspace acceptance  
--------------------------------------------------------------------  
- user can open a review in main area  
- left panel shows candidates/navigation  
- center panel shows proposal/preview/evidence  
- right panel shows allowed actions and comments  
- submit action sends explicit event and updates state correctly  
- final action requires backend confirmation before UI final state  
  
B. Dashboard acceptance  
--------------------------------------------------------------------  
- user can open dashboard mode  
- KPI cards and trend blocks render  
- filters refresh data correctly  
- notes/actions can be captured where allowed  
  
C. Flow explorer acceptance  
--------------------------------------------------------------------  
- user can open flow explorer  
- graph/timeline render  
- node selection updates detail panel  
  
D. Runtime-awareness acceptance  
--------------------------------------------------------------------  
- frontend reacts to runtime_decision  
- disallowed actions are not interactable  
- review/finalization stages use correct UI mode  
  
E. Error-handling acceptance  
--------------------------------------------------------------------  
- invalid input errors show cleanly  
- blocked states are visible  
- stale responses do not corrupt local state  
- recoverable errors preserve drafts  
  
====================================================================  
30. RECOMMENDED TECHNICAL STACK  
====================================================================  
  
RECOMMENDED FRONTEND STACK  
--------------------------------------------------------------------  
Within JupyterLab extension context:  
- TypeScript  
- JupyterLab extension APIs  
- Lumino widgets/layout  
- React for panel internals where appropriate  
- schema-driven form rendering for right panel  
- centralized state store pattern  
  
RECOMMENDED ARCHITECTURE  
--------------------------------------------------------------------  
- extension plugin registers commands and workspace launcher  
- main workspace widget hosts multi-panel shell  
- panel content rendered by React components  
- bridge client handles backend communication  
- store manages state and patch merges  
  
====================================================================  
31. IMPLEMENTATION PHASING  
====================================================================  
  
PHASE 1  
--------------------------------------------------------------------  
- main area workspace shell  
- review mode  
- state store  
- event dispatcher  
- open review + submit action  
  
PHASE 2  
--------------------------------------------------------------------  
- dashboard mode  
- flow explorer mode  
- bottom detail panel  
- refresh token handling  
- error banner framework  
  
PHASE 3  
--------------------------------------------------------------------  
- draft persistence  
- status bar integration  
- keyboard shortcuts  
- layout persistence  
- richer structured form renderer  
  
PHASE 4  
--------------------------------------------------------------------  
- advanced comparisons  
- export preview  
- enhanced accessibility  
- performance optimization  
- analytics / observability polish  
  
====================================================================  
32. FINAL RECOMMENDATION  
====================================================================  
  
The best implementation approach is:  
  
- keep the governed workspace in JupyterLab main area  
- keep existing coding assistant in sidebar as auxiliary support  
- build a contract-driven 3-panel shell  
- let backend runtime decision drive mode and actions  
- treat backend as authoritative for governance state  
- keep frontend smart enough for UX, but not for final authority  
  
That gives the best balance of:  
- seamless UX  
- governance safety  
- maintainability  
- extensibility  
- fit with JupyterLab  
  
====================================================================  
NEXT BEST ARTIFACT  
====================================================================  
  
The strongest next artifact is a:  
  
COPIABLE FRONTEND FOLDER STRUCTURE + COMPONENT MAP  
including:  
- TypeScript file layout  
- component names  
- store modules  
- service modules  
- JupyterLab plugin entrypoints  
- which component renders each panel  
  
That would be the most direct handoff for coding the frontend.  
====================================================================  
END OF JUPYTERLAB FRONTEND IMPLEMENTATION URD  
====================================================================  
