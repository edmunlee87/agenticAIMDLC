# UI UX Planning  
  
====================================================================  
JUPYTERLAB AGENTIC AI UI/UX REQUIREMENT  
BEST-PRACTICE WORKBENCH DESIGN FOR EDMUN'S USE CASES  
====================================================================  
  
DOCUMENT PURPOSE  
--------------------------------------------------------------------  
Define the recommended UI/UX architecture for an Agentic AI solution  
inside JupyterLab, designed for model development, data quality,  
EDA, fine/coarse classing, model comparison, validation, reporting,  
and human-in-the-loop review workflows.  
  
This design assumes:  
- JupyterLab is the host platform  
- Agent is available through a right sidebar extension such as CodeBuddy  
- The solution must support structured, auditable, review-first workflows  
- The solution must be suitable for enterprise analytical work, not just chat  
  
====================================================================  
1. DESIGN PHILOSOPHY  
====================================================================  
  
PRIMARY PRINCIPLE  
--------------------------------------------------------------------  
Chat starts the work, but structured pages and cards complete the work.  
  
RATIONALE  
--------------------------------------------------------------------  
Users in model development and analytical domains do not only need  
answers from an LLM. They need:  
- generated artefacts  
- diagnostics  
- editable outputs  
- approval controls  
- comparison tools  
- auditability  
- workflow continuity  
  
Therefore, the UI must be a workbench, not merely a chatbot sidebar.  
  
DESIGN OBJECTIVES  
--------------------------------------------------------------------  
1. Allow agent output to be rendered as structured artefacts  
2. Allow user review directly on visual outputs  
3. Allow user edits without relying only on free-text chat  
4. Allow accepted or edited outputs to flow back to the agent  
5. Preserve governance, traceability, and reproducibility  
6. Support modular expansion across multiple model lifecycle use cases  
  
====================================================================  
2. HIGH-LEVEL LAYOUT  
====================================================================  
  
RECOMMENDED 4-REGION LAYOUT  
--------------------------------------------------------------------  
1. Left Sidebar   = Workflow Navigator  
2. Main Area      = Review Canvas  
3. Right Sidebar  = Agent Console  
4. Bottom Panel   = Card-Level Control Panel  
  
SUMMARY  
--------------------------------------------------------------------  
Left sidebar anchors the user.  
Main area is the primary work surface.  
Right sidebar is the agent interaction and execution console.  
Bottom panel is the localized control layer for the active card.  
  
====================================================================  
3. LEFT SIDEBAR REQUIREMENT  
WORKFLOW NAVIGATOR  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
Provide a persistent navigation and workflow control surface for the  
entire project, module, page, and artefact structure.  
  
PRIMARY UX ROLE  
--------------------------------------------------------------------  
Acts as:  
- workflow tree  
- page navigator  
- artefact catalog  
- status monitor  
- entry point into each stage of work  
  
STRUCTURE  
--------------------------------------------------------------------  
The left sidebar should support a 4-tier hierarchy:  
  
Tier 1: Workspace / Project  
Tier 2: Module / Use Case  
Tier 3: Page / Task  
Tier 4: Card / Artefact Node  
  
EXAMPLE HIERARCHY  
--------------------------------------------------------------------  
IFRS9 Retail PD  
  - Data Quality  
  - EDA  
  - Fine Classing  
  - Coarse Classing  
  - Feature Selection  
  - Model Fit  
  - Model Comparison  
  - Validation  
  - Reporting  
  - Approval Pack  
  
Each page can further expand into cards such as:  
  - Summary KPI  
  - Variable Distribution  
  - WoE Plot  
  - Bin Table  
  - Recommendation  
  - Narrative Draft  
  - Diagnostic Result  
  
REQUIRED FEATURES  
--------------------------------------------------------------------  
1. Tree-based expandable navigation  
2. Clickable nodes that route the user to page or card  
3. Status badges for each node  
4. Counts for warnings, pending reviews, or approvals  
5. Search/filter within the tree  
6. Highlight current page and current card  
7. Support for pinned or favorite nodes  
8. Optional recent items section  
9. Version-aware display where relevant  
10. Ability to show node-level progress  
  
STATUS STATES  
--------------------------------------------------------------------  
Recommended statuses:  
- not_started  
- in_progress  
- generated  
- review_required  
- user_edited  
- approved  
- rejected  
- failed  
- superseded  
  
UX GUIDANCE  
--------------------------------------------------------------------  
The left sidebar should feel like a workflow explorer, not a generic  
file tree. It must show business progress and review state, not merely  
page names.  
  
====================================================================  
4. MAIN AREA REQUIREMENT  
REVIEW CANVAS  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
Serve as the primary review and interaction surface for all structured  
outputs generated by the agent or by the workflow engine.  
  
PRIMARY UX ROLE  
--------------------------------------------------------------------  
Acts as:  
- analytical workspace  
- artefact review canvas  
- comparison surface  
- evidence display  
- interactive editing area  
  
DESIGN PRINCIPLE  
--------------------------------------------------------------------  
The main area must not be wasted on chat. It should host the actual  
work product.  
  
PAGE MODEL  
--------------------------------------------------------------------  
The main area should be organized by pages.  
Each page is composed of cards.  
  
Each page corresponds to a meaningful workflow stage such as:  
- Data Quality  
- EDA  
- Fine Classing  
- Coarse Classing  
- Model Comparison  
- Validation Findings  
- Report Section Drafting  
  
CARD MODEL  
--------------------------------------------------------------------  
Each card represents one reviewable output unit.  
  
Examples:  
- KPI card  
- chart card  
- table card  
- editable rule card  
- narrative card  
- recommendation card  
- warning card  
- comparison card  
- evidence card  
  
REQUIRED PAGE STRUCTURE  
--------------------------------------------------------------------  
1. Page Header  
2. Top KPI Strip  
3. Card Grid / Card Stack  
4. Optional Compare Drawer  
5. Optional Evidence Drawer  
6. Linkage to Bottom Panel for selected card actions  
  
PAGE HEADER CONTENT  
--------------------------------------------------------------------  
- page title  
- workflow stage  
- run status  
- selected model / dataset / segment  
- version tag  
- quick actions  
  
TOP KPI STRIP CONTENT  
--------------------------------------------------------------------  
Examples:  
- total variables  
- warnings count  
- approved cards  
- pending review count  
- run duration  
- quality score  
- drift flags  
- exception count  
  
CARD BEHAVIOR REQUIREMENT  
--------------------------------------------------------------------  
Each card should support:  
- expand / collapse  
- pin  
- compare  
- explain  
- regenerate  
- approve / reject  
- comment  
- show metadata  
- link to trace / provenance  
- link to related cards  
  
PROGRESSIVE DISCLOSURE  
--------------------------------------------------------------------  
The page must prioritize readability:  
- summary above  
- detail below  
- diagnostics expandable  
- raw data optionally hidden by default  
  
COMPARE MODE  
--------------------------------------------------------------------  
The main area should support compare mode for:  
- current vs previous run  
- before vs after user override  
- champion vs challenger  
- agent proposal vs accepted version  
  
====================================================================  
5. RIGHT SIDEBAR REQUIREMENT  
AGENT CONSOLE  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
Provide the conversational and operational control layer for the agent.  
  
PRIMARY UX ROLE  
--------------------------------------------------------------------  
Acts as:  
- chat interface  
- context inspector  
- action launcher  
- execution trace surface  
  
DESIGN PRINCIPLE  
--------------------------------------------------------------------  
The right sidebar must be more than a plain chat box. It should expose  
the agent's context, reasoning boundaries, actions, and traceability.  
  
RECOMMENDED TAB MODEL  
--------------------------------------------------------------------  
Tab 1: Chat  
Tab 2: Context  
Tab 3: Actions  
Tab 4: Trace  
  
TAB 1: CHAT  
--------------------------------------------------------------------  
Purpose:  
- free text interaction with the agent  
- request generation, refinement, explanation, or follow-up  
  
Features:  
- conversation thread  
- prompt suggestions  
- slash-command style quick actions  
- insert current page/card context  
- attach selected artefacts  
  
TAB 2: CONTEXT  
--------------------------------------------------------------------  
Purpose:  
Show exactly what the agent is acting on.  
  
Recommended fields:  
- current workspace  
- current module  
- current page  
- current card  
- selected variable  
- selected dataset  
- selected model version  
- selected segment  
- active filters  
- active scenario  
- approval state  
- current task id  
  
TAB 3: ACTIONS  
--------------------------------------------------------------------  
Purpose:  
Provide action-oriented shortcuts rather than requiring the user to  
type everything.  
  
Examples:  
- rerun current card  
- explain recommendation  
- compare alternative  
- generate commentary  
- export selected output  
- open related artefacts  
- propose correction  
- send edited output back to agent  
  
TAB 4: TRACE  
--------------------------------------------------------------------  
Purpose:  
Provide trust and transparency for execution.  
  
Recommended content:  
- selected skill or tool  
- execution sequence  
- parameters used  
- warnings  
- generated files  
- failed checks  
- run id  
- timestamp  
- backend reference  
- retry history  
  
UX GUIDANCE  
--------------------------------------------------------------------  
The right sidebar should behave like an agent console, not merely a  
chat window. It must help the user understand what happened and what  
can be done next.  
  
====================================================================  
6. BOTTOM PANEL REQUIREMENT  
CARD-LEVEL CONTROL PANEL  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
Provide a contextual control surface for the currently active card.  
  
PRIMARY UX ROLE  
--------------------------------------------------------------------  
Acts as:  
- local edit layer  
- override panel  
- approval panel  
- detailed adjustment surface  
  
DESIGN PRINCIPLE  
--------------------------------------------------------------------  
The bottom panel is dynamic and card-specific.  
It must react to the selected card in the main area.  
  
STATE HIERARCHY  
--------------------------------------------------------------------  
Recommended priority:  
1. Bottom panel state  
2. Card-local state  
3. Page-level state  
4. Workspace-level defaults  
  
The bottom panel may override page-level settings locally for the  
active card, but must not overwrite unrelated page content.  
  
DYNAMIC BEHAVIOR  
--------------------------------------------------------------------  
If the active card changes, the bottom panel must change accordingly.  
  
Examples:  
- chart card        -> chart options, segment, overlay, drilldown  
- binning card      -> merge, split, relabel, lock, monotonicity tools  
- narrative card    -> rewrite, shorten, expand, tone controls  
- rule card         -> threshold edits, enable/disable, exception notes  
- comparison card   -> choose baseline, toggle metrics, export diff  
  
REQUIRED FEATURES  
--------------------------------------------------------------------  
1. Dynamic rendering by card type  
2. Clear linkage to the selected card  
3. Local override controls  
4. Accept / reject / regenerate actions  
5. Reset to agent proposal  
6. Comment capture  
7. Show unsaved changes  
8. Version comparison  
9. Support fine-grained controls without clutter  
10. Scrollable layout where controls are numerous  
  
EXAMPLE CONTROLS BY CARD TYPE  
--------------------------------------------------------------------  
Fine / Coarse Classing Card:  
- merge bins  
- split bins  
- edit cut points  
- relabel bins  
- lock bin  
- unlock bin  
- compare pre/post  
- accept final bins  
  
Narrative Card:  
- shorten  
- expand  
- rewrite technical  
- rewrite management-friendly  
- edit directly  
- accept wording  
- add rationale  
  
Data Quality Card:  
- severity threshold  
- rule enable / disable  
- acknowledge exception  
- rerun check  
- add issue note  
  
UX GUIDANCE  
--------------------------------------------------------------------  
The bottom panel should feel like a precision control layer, not a  
generic toolbar.  
  
====================================================================  
7. INTERACTION MODEL  
====================================================================  
  
TARGET INTERACTION FLOW  
--------------------------------------------------------------------  
Step 1. Agent generates outputs  
Step 2. Outputs are routed into structured pages and cards  
Step 3. User reviews visually in main area  
Step 4. User edits or accepts using bottom panel and inline controls  
Step 5. Structured feedback is returned to the agent  
Step 6. Workflow state, trace, and audit trail update automatically  
  
CRITICAL PRINCIPLE  
--------------------------------------------------------------------  
Agent output must not be trapped inside chat.  
It must be promoted into structured artefacts.  
  
FEEDBACK MODEL  
--------------------------------------------------------------------  
User feedback should be captured in structured form where possible.  
  
Examples:  
- approve  
- reject  
- regenerate  
- selected alternative  
- changed threshold  
- changed cut points  
- added rationale  
- added exception note  
  
This is preferred over relying entirely on free-text chat for workflow  
continuation.  
  
====================================================================  
8. HUMAN-IN-THE-LOOP DESIGN  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
Support different levels of user review and intervention depending on  
the risk and importance of the artefact.  
  
RECOMMENDED HITL LEVELS  
--------------------------------------------------------------------  
Level 1: Lightweight Acceptance  
- accept  
- reject  
- regenerate  
- compare alternative  
  
Level 2: Guided Adjustment  
- sliders  
- dropdowns  
- toggle switches  
- cut-point editing  
- local config changes  
- narrative editing  
  
Level 3: Formal Approval  
- approval status  
- rationale  
- evidence attachment  
- freeze version  
- produce audit log  
- handoff for downstream use  
  
WHEN TO USE EACH LEVEL  
--------------------------------------------------------------------  
Level 1:  
Low-risk outputs such as chart summaries or simple narrative drafts  
  
Level 2:  
Analytical artefacts such as binning, segmentation, thresholds, or  
scenario-driven outputs  
  
Level 3:  
Governance-sensitive artefacts such as final model outputs, committee  
packs, validation responses, or official narratives  
  
====================================================================  
9. TRUST, EXPLAINABILITY, AND TRACEABILITY  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
Ensure users can trust, audit, and challenge agent outputs.  
  
EVERY MAJOR OUTPUT SHOULD SUPPORT  
--------------------------------------------------------------------  
1. Why this output was produced  
2. What data and context were used  
3. Confidence or warning level  
4. Alternative choices  
5. Reproducibility metadata  
  
EXAMPLE EXPLANATION FIELDS  
--------------------------------------------------------------------  
- business rationale  
- statistical rationale  
- selected method  
- assumptions made  
- constraints observed  
- warning conditions  
- quality issues detected  
  
EXAMPLE PROVENANCE FIELDS  
--------------------------------------------------------------------  
- run id  
- model id  
- dataset snapshot id  
- segment  
- reporting date  
- parameters used  
- timestamp  
- tool or skill invoked  
- output version  
  
UX GUIDANCE  
--------------------------------------------------------------------  
Trust-related information should be easy to inspect but not intrusive.  
Use metadata drawers, trace tabs, and expandable provenance sections.  
  
====================================================================  
10. STATE MODEL  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
Provide a stable and consistent state hierarchy across all UI regions.  
  
RECOMMENDED STATE LEVELS  
--------------------------------------------------------------------  
1. Workspace State  
2. Page State  
3. Card State  
4. Agent Session State  
  
WORKSPACE STATE  
--------------------------------------------------------------------  
Examples:  
- selected project  
- selected module  
- selected model family  
- selected dataset  
- selected version  
- permissions  
- workflow stage  
  
PAGE STATE  
--------------------------------------------------------------------  
Examples:  
- active filters  
- segment  
- scenario  
- compare set  
- diagnostics visible  
- page mode  
  
CARD STATE  
--------------------------------------------------------------------  
Examples:  
- local overrides  
- accepted / rejected status  
- card-specific comments  
- local edits  
- active selection  
- temporary changes  
  
AGENT SESSION STATE  
--------------------------------------------------------------------  
Examples:  
- current task  
- last run id  
- available actions  
- pending execution  
- warnings  
- referenced artefacts  
  
STATE BEHAVIOR PRINCIPLE  
--------------------------------------------------------------------  
All UI regions should subscribe to the shared state appropriately.  
  
Examples:  
- left sidebar reflects workflow and review status  
- main area reflects page and card state  
- bottom panel reflects active card state  
- right sidebar reflects agent session and action state  
  
====================================================================  
11. RESPONSIVENESS TO AGENT OUTPUT  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
Ensure the entire workspace responds coherently when the agent produces  
new output or updates existing artefacts.  
  
RECOMMENDED EVENT FLOW  
--------------------------------------------------------------------  
1. Agent finishes a task  
2. Shared state store is updated  
3. Left sidebar updates page/card status  
4. Main area opens or refreshes affected cards  
5. Bottom panel updates if selected card changed  
6. Right sidebar trace and actions update  
7. Audit trail entry is recorded  
  
DESIGN PRINCIPLE  
--------------------------------------------------------------------  
The UI should feel alive and synchronized without forcing the user to  
manually search for the agent's result.  
  
====================================================================  
12. USE CASE MAPPING  
====================================================================  
  
12.1 DATA QUALITY  
--------------------------------------------------------------------  
Main Area:  
- DQ summary cards  
- failed rules table  
- severity distribution  
- issue drilldown  
  
Bottom Panel:  
- threshold override  
- rule enable / disable  
- acknowledge exception  
- rerun checks  
  
Right Sidebar:  
- explain failure  
- suggest remediation  
- generate narrative  
- export issue list  
  
12.2 EDA  
--------------------------------------------------------------------  
Main Area:  
- variable summary  
- trend charts  
- missingness  
- PSI / drift  
- segmentation cards  
  
Bottom Panel:  
- segment selection  
- transformation toggle  
- winsorization preview  
- date granularity  
  
Right Sidebar:  
- explain variable behavior  
- suggest transformation  
- highlight anomalies  
  
12.3 FINE / COARSE CLASSING  
--------------------------------------------------------------------  
Main Area:  
- bin table  
- event rate chart  
- WoE chart  
- monotonicity warnings  
- recommendation card  
  
Bottom Panel:  
- merge bins  
- split bins  
- relabel bins  
- lock bins  
- revert changes  
- compare alternatives  
  
Right Sidebar:  
- explain recommendation  
- generate alternative binning  
- summarize business trade-offs  
  
12.4 MODEL FIT / MODEL COMPARISON  
--------------------------------------------------------------------  
Main Area:  
- model metrics cards  
- comparison table  
- calibration plots  
- stability diagnostics  
- explainability cards  
  
Bottom Panel:  
- variable lock  
- threshold tuning  
- select challenger  
- rerun subset  
- choose final model  
  
Right Sidebar:  
- explain winner  
- propose alternative shortlist  
- generate commentary  
  
12.5 REPORTING / NARRATIVE  
--------------------------------------------------------------------  
Main Area:  
- section cards  
- draft narratives  
- visual evidence cards  
- committee-ready summaries  
  
Bottom Panel:  
- rewrite controls  
- shorten / expand  
- technical / management tone  
- accept wording  
  
Right Sidebar:  
- explain edits  
- regenerate section  
- produce summary pack  
  
====================================================================  
13. VISUAL DESIGN GUIDELINES  
====================================================================  
  
DESIGN DIRECTION  
--------------------------------------------------------------------  
Use an enterprise analytical style, not a playful consumer chat style.  
  
RECOMMENDED VISUAL CHARACTERISTICS  
--------------------------------------------------------------------  
- clean spacing  
- stable card grid  
- subtle borders  
- restrained palette  
- strong typography hierarchy  
- compact but readable controls  
- badges and status chips for state  
- progressive disclosure for detail  
- traffic-light accents only when meaningful  
  
AVOID  
--------------------------------------------------------------------  
- overly flashy color schemes  
- cluttered multi-toolbar design  
- excessive modal dialogs  
- chat-first layouts that bury outputs  
- cramped control density  
  
====================================================================  
14. ADVANCED UX FEATURES  
====================================================================  
  
RECOMMENDED ADVANCED FEATURES  
--------------------------------------------------------------------  
1. Compare Mode  
2. Evidence Drawer  
3. Global Command Palette Integration  
4. Inline AI Actions on Cards  
5. Session Timeline  
6. Recent Activity Feed  
7. Pinned Artefacts  
8. Approval Queue  
9. Export Panel  
10. Version History View  
  
COMPARE MODE  
--------------------------------------------------------------------  
Support explicit side-by-side comparisons for:  
- current vs prior run  
- before vs after user edit  
- proposal vs accepted version  
- champion vs challenger  
  
EVIDENCE DRAWER  
--------------------------------------------------------------------  
A side or secondary panel showing:  
- assumptions  
- linked evidence  
- policy notes  
- comments  
- supporting diagnostics  
  
SESSION TIMELINE  
--------------------------------------------------------------------  
A chronological record of:  
- agent runs  
- user edits  
- approvals  
- exports  
- exceptions  
- failures  
  
====================================================================  
15. IMPLEMENTATION PRIORITY  
====================================================================  
  
MVP PRIORITY  
--------------------------------------------------------------------  
Phase 1  
- Left sidebar workflow tree  
- Main area card-based review page  
- Right sidebar with Chat + Context + Trace  
- Bottom panel for active card controls  
- Shared state synchronization  
  
Phase 2  
- Compare mode  
- Inline AI actions  
- Approval statuses  
- Version tagging  
- Audit trail viewer  
  
Phase 3  
- Evidence drawer  
- Export workflows  
- Session timeline  
- Role-based views  
- Advanced formal approvals  
  
====================================================================  
16. FINAL RECOMMENDATION  
====================================================================  
  
RECOMMENDED UX SHAPE  
--------------------------------------------------------------------  
Left Sidebar   = Workflow Navigator  
Main Area      = Card-Based Review Canvas  
Right Sidebar  = Agent Console with Chat, Context, Actions, Trace  
Bottom Panel   = Adaptive Card-Level Control Panel  
  
WHY THIS IS THE BEST FIT  
--------------------------------------------------------------------  
This design best supports:  
- agentic generation  
- human review  
- local editing  
- structured feedback  
- auditability  
- multi-step workflows  
- model lifecycle use cases  
- enterprise-grade UX in JupyterLab  
  
ONE-LINE DESIGN PHILOSOPHY  
--------------------------------------------------------------------  
Chat starts the work, but cards complete the work.  
  
====================================================================  
END OF DOCUMENT  
====================================================================  
