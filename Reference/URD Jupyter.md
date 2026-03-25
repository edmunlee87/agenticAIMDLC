# URD Jupyter  
  
====================================================================  
USER REQUIREMENT DOCUMENT (URD)  
SKILLS-BASED CREDIT SCORING PROJECT WITH HITL, SESSION RESUME,  
OBSERVABILITY, AND FLOW VISUALIZATION  
====================================================================  
  
Project Name : Credit Scoring Skills Orchestration Framework  
Version      : 1.0  
Date         : 2026-03-14  
Prepared For : Credit Scoring / Model Development / Validation /  
               Governance / Technology Stakeholders  
  
====================================================================  
1. INTRODUCTION  
====================================================================  
  
1.1 Purpose  
--------------------------------------------------------------------  
This document defines the requirements for a skills-based orchestration  
framework to support the end-to-end credit scoring model development  
lifecycle with human-in-the-loop (HITL) controls.  
  
The framework shall enable an AI coding assistant operating in a  
Jupyter-based environment to orchestrate deterministic SDK functions,  
workflow tools, review steps, and governance checkpoints through  
structured skills. The framework shall support explainable execution,  
observability, auditability, restartability, and controlled human  
intervention for judgement-heavy decisions.  
  
1.2 Objective  
--------------------------------------------------------------------  
The objective is to build a governed orchestration layer that can:  
  
- guide users through credit scorecard development stages  
- invoke deterministic tools and SDK functions in a structured order  
- prepare human review packages for judgement-based decisions  
- capture all user choices, comments, and downstream actions  
- maintain workflow state across sessions  
- support notebook UI, API, CLI, and future workflow engines  
- remain extensible for new model types, policies, and governance  
  requirements  
  
1.3 Background  
--------------------------------------------------------------------  
Credit scoring development includes many deterministic steps such as  
data profiling, fine classing, coarse classing, WoE transformation,  
feature screening, logistic regression fitting, score scaling,  
documentation, and monitoring. However, several stages require expert  
judgement and governance oversight, especially where business meaning,  
policy interpretation, or trade-offs exist.  
  
A skills-based architecture is required to combine:  
  
- deterministic execution through SDK functions and tools  
- AI-assisted reasoning and orchestration  
- bounded human decisions through HITL review gates  
- structured observability and audit logging  
  
====================================================================  
2. SCOPE  
====================================================================  
  
2.1 In Scope  
--------------------------------------------------------------------  
The project shall cover orchestration skills for the credit scoring  
lifecycle, including:  
  
- workflow initialization  
- data readiness and data quality review  
- exploratory data analysis  
- segmentation review  
- fine classing and coarse classing  
- coarse classing review  
- WoE and IV review  
- feature engineering  
- feature screening  
- policy and variable acceptability review  
- model fitting  
- score scaling and calibration  
- reject inference review where applicable  
- champion-challenger comparison  
- final model review  
- validation pack preparation  
- committee pack preparation  
- deployment readiness  
- deployment approval  
- monitoring pack generation  
- annual review workflow  
  
The project shall also cover:  
  
- HITL workflow design  
- observability event logging  
- audit trail design  
- workflow state management  
- artifact registry integration  
- Jupyter widget linkage pattern  
- session resume and recovery  
- observability flow summarization  
- support for future MCP/API/service integration  
  
2.2 Out of Scope  
--------------------------------------------------------------------  
The following are out of scope for the first phase unless separately  
approved:  
  
- autonomous production deployment without human approval  
- direct override of policy controls without explicit reviewer approval  
- full model training engine implementation  
- regulator-facing document content approval automation  
- organization-wide workflow engine replacement  
- non-scorecard model families beyond extensibility provisions  
  
====================================================================  
3. BUSINESS GOALS  
====================================================================  
  
The framework shall achieve the following business goals:  
  
1. Reduce turnaround time for scorecard development workflow execution.  
2. Standardize model development steps across teams.  
3. Improve governance and transparency of model decisions.  
4. Support reproducible and restartable workflow execution.  
5. Make human approvals explicit, bounded, and logged.  
6. Improve readiness for validation, audit, and governance committees.  
7. Provide a foundation for future model lifecycle automation  
   initiatives.  
  
====================================================================  
4. TARGET USERS  
====================================================================  
  
4.1 Primary Users  
--------------------------------------------------------------------  
- Model developers  
- Credit risk analysts  
- Scorecard developers  
- Portfolio analytics users  
  
4.2 Secondary Users  
--------------------------------------------------------------------  
- Model validators  
- Governance reviewers  
- Business approvers  
- Audit reviewers  
- Technology support and platform teams  
  
4.3 User Personas  
--------------------------------------------------------------------  
A. Model Developer  
Needs guided workflow execution, stage recommendations, and the  
ability to approve or modify binning and model decisions.  
  
B. Reviewer / Approver  
Needs structured review cards, bounded action choices, evidence, and  
comments capture.  
  
C. Validator  
Needs traceable evidence, review history, assumptions, and final  
approved artifacts.  
  
D. Platform Administrator  
Needs observability, workflow state, skill versioning, and failure  
logs.  
  
====================================================================  
5. SOLUTION OVERVIEW  
====================================================================  
  
5.1 Conceptual Design  
--------------------------------------------------------------------  
The solution shall consist of:  
  
- Skills Layer  
  Text-based orchestration definitions that describe stage purpose,  
  required inputs, routing logic, HITL triggers, output contracts, and  
  logging requirements.  
  
- Deterministic Execution Layer  
  Credit scoring SDK functions, Python modules, APIs, or MCP tools  
  that perform calculations and actions.  
  
- Workflow State Layer  
  Persistent structured state that records current stage, completed  
  stages, pending reviews, approvals, artifacts, and block conditions.  
  
- HITL Review Layer  
  Structured review payloads and Jupyter widgets or other UI  
  components that display recommendations, evidence, and bounded  
  actions.  
  
- Observability and Audit Layer  
  Append-only logs for skill execution, stage transition, review  
  creation, review response, and downstream decisions.  
  
- Flow Visualization Layer  
  A summarized graph/timeline representation generated from structured  
  logs to visualize stage progression, agent actions, user decisions,  
  errors, reruns, and final outcomes.  
  
5.2 Operating Principle  
--------------------------------------------------------------------  
The framework shall follow this principle:  
  
- deterministic tools do the execution  
- skills do the orchestration and reasoning  
- humans do the accountable decisions  
- logs preserve the entire decision trail  
- summarized flows provide visual interpretation of the logs  
  
====================================================================  
6. FUNCTIONAL REQUIREMENTS  
====================================================================  
  
6.1 Skills Framework Requirements  
--------------------------------------------------------------------  
FR-001 Skill Definition Standard  
The system shall support a standard SKILL.md structure for each  
workflow skill.  
  
FR-002 Skill Metadata  
Each skill shall define:  
- skill name  
- description  
- purpose  
- when to use  
- required inputs  
- routing logic  
- escalation criteria  
- output contract  
- observability requirements  
- audit requirements  
- guardrails  
  
FR-003 Stage-Based Skills  
The system shall support stage-specific skills rather than only one  
monolithic workflow skill.  
  
FR-004 Orchestrator Skill  
The system shall provide a master orchestration skill that routes work  
to stage-specific skills and manages workflow transitions.  
  
FR-005 Skill Versioning  
Each skill shall support a version identifier for audit and  
reproducibility.  
  
6.2 Workflow Requirements  
--------------------------------------------------------------------  
FR-010 Workflow Initialization  
The system shall initialize a workflow for a new scorecard project  
with project metadata, run ID, current stage, and artifact registry  
reference.  
  
FR-011 Workflow State Persistence  
The system shall persist workflow state after every material stage  
completion, review response, or block event.  
  
FR-012 Workflow State Structure  
Workflow state shall include:  
- project_id  
- run_id  
- session_id  
- trace_id  
- current_stage  
- stage_status  
- completed_stages  
- pending_stages  
- pending_reviews  
- blocking_reasons  
- artifact_registry_reference  
- approval_state  
- last_successful_transition  
- audit references  
- observability references  
  
FR-013 Workflow Resume  
The system shall support resuming an interrupted or paused workflow  
from persisted state.  
  
FR-014 Workflow Block Handling  
The system shall explicitly enter blocked state when prerequisites,  
approvals, or required logs are missing.  
  
FR-015 Routing Rules  
The system shall support configurable routing rules for linear,  
rework, rejection, escalation, recovery, and resume paths.  
  
6.3 Credit Scoring Lifecycle Coverage  
--------------------------------------------------------------------  
FR-020 Supported Stages  
The system shall support the following stages:  
  
- intake  
- data_readiness  
- dq_review  
- dq_exception_review  
- eda  
- segmentation_review  
- fine_classing  
- coarse_classing  
- coarse_classing_review  
- woe_iv_review  
- feature_engineering  
- feature_screening  
- policy_variable_review  
- model_fitting  
- scaling_and_calibration  
- reject_inference_review  
- champion_challenger_review  
- model_review  
- validation_pack  
- committee_pack  
- deployment_readiness  
- deployment_approval  
- monitoring_pack  
- annual_review  
- closed  
  
FR-021 Stage Prerequisite Validation  
The orchestrator shall validate prerequisite stages and artifacts  
before running any stage.  
  
FR-022 Stage Output Contract  
Each stage shall return structured outputs including status, artifacts  
created, findings, recommendation, and next stage suggestion.  
  
6.4 HITL Requirements  
--------------------------------------------------------------------  
FR-030 HITL Mandatory Gate Support  
The system shall support mandatory human review gates for selected  
workflow steps.  
  
FR-031 HITL Use Cases  
The following use cases shall support HITL:  
  
- material DQ exception acceptance  
- segmentation override  
- non-standard coarse classing approval  
- policy-sensitive variable acceptance  
- final feature shortlist approval  
- reject inference method approval  
- final model selection approval  
- score scaling exception approval  
- deployment readiness approval  
- material monitoring breach disposition  
- annual review adverse outcome review  
  
FR-032 HITL Payload Structure  
Each HITL review shall include:  
- review_id  
- review_type  
- stage  
- title  
- decision_required  
- business_summary  
- technical_summary  
- recommendation  
- alternatives  
- allowed_actions  
- risk_flags  
- policy_findings  
- evidence_refs  
- review_status  
- reviewer_id  
- reviewer_action  
- reviewer_comment  
  
FR-033 Bounded Reviewer Actions  
The system shall support bounded human actions such as:  
- approve  
- approve_with_changes  
- reject  
- rerun_with_parameters  
- request_more_analysis  
- escalate  
- drop_variable  
  
FR-034 No Implicit Approval  
The system shall not interpret free-text comments alone as approval.  
  
FR-035 HITL State Transitions  
The system shall explicitly record review states such as:  
- pending_review  
- approved  
- approved_with_changes  
- rejected  
- rerun_requested  
- escalated  
  
FR-036 Coarse Classing HITL  
The system shall support a dedicated HITL step for coarse classing  
review, especially when:  
- multiple plausible merges exist  
- monotonicity is imperfect  
- IV drop is material  
- minimum support thresholds are breached  
- business interpretation is weak  
- variable is high-importance  
  
6.5 Observability Requirements  
--------------------------------------------------------------------  
FR-040 Structured Event Logging  
The system shall create append-only structured event logs for all  
material workflow actions.  
  
FR-041 Mandatory Event Types  
The system shall support at minimum:  
- skill_started  
- skill_completed  
- skill_failed  
- stage_started  
- stage_completed  
- stage_failed  
- stage_transition  
- hitl_review_created  
- hitl_review_displayed  
- hitl_user_responded  
- hitl_review_completed  
- policy_breach_detected  
- artifact_registered  
- workflow_blocked  
- workflow_resumed  
- override_logged  
- rerun_requested  
  
FR-042 Event Fields  
Each event shall include:  
- event_id  
- event_type  
- timestamp  
- project_id  
- run_id  
- session_id  
- skill_name  
- skill_version  
- current_stage  
- trace_id  
  
FR-043 HITL Event Fields  
HITL-related events shall also include:  
- review_id  
- recommendation  
- allowed_actions  
- reviewer_id  
- reviewer_action  
- reviewer_comment  
- final_action_taken  
- evidence_refs  
- override_flag  
  
FR-044 Append-Only Logging  
The system shall use append-only logging and shall not overwrite prior  
review or decision events.  
  
FR-045 Logging Failure Rule  
Restricted actions shall not proceed if mandatory observability or  
audit events cannot be persisted.  
  
6.6 Audit Requirements  
--------------------------------------------------------------------  
FR-050 Decision Audit Trail  
The system shall store an audit trail for every material review,  
approval, rejection, rerun, and override.  
  
FR-051 Audit Fields  
Audit records shall include:  
- decision_type  
- stage  
- recommendation  
- rationale  
- evidence references  
- policy findings  
- reviewer identity  
- reviewer action  
- reviewer comment  
- approval status  
- final downstream action  
- timestamp  
- skill version  
  
FR-052 Replay Support  
Audit and observability records shall support replay of decision  
history for a given run.  
  
6.7 Artifact Registry Requirements  
--------------------------------------------------------------------  
FR-060 Artifact Registration  
The system shall register material artifacts generated or consumed by  
the workflow.  
  
FR-061 Artifact Metadata  
Each artifact entry shall include:  
- artifact_id  
- artifact_type  
- stage  
- producer  
- version  
- path or URI  
- created_timestamp  
- schema_version  
- project_id  
- run_id  
  
FR-062 Artifact Linkage  
HITL reviews and audit records shall reference relevant artifacts.  
  
6.8 Jupyter Integration Requirements  
--------------------------------------------------------------------  
FR-070 Jupyter Widget Support  
The system shall support Jupyter widgets to display HITL review cards  
and workflow stage interactions.  
  
FR-071 Widget Responsibilities  
Widgets shall support:  
- displaying review title and summary  
- showing recommendation and alternatives  
- showing evidence references  
- accepting bounded user actions  
- capturing reviewer comments  
- triggering backend action submission  
- refreshing status after response  
  
FR-072 Backend Controller Linkage  
Jupyter widgets shall interact with a Python controller layer rather  
than directly with the skill file.  
  
FR-073 Widget-to-Skill Contract  
The controller shall translate widget actions into structured payloads  
for skill/backend execution.  
  
====================================================================  
7. SKILLS REQUIRED  
====================================================================  
  
7.1 Master Skill  
--------------------------------------------------------------------  
scorecard-orchestrator  
  
Purpose:  
- route and control the overall lifecycle  
- check prerequisites  
- update workflow state  
- invoke downstream skill/tool  
- trigger HITL when needed  
- manage session bootstrap and resume  
- manage observability flow summarization triggers  
  
7.2 Core Stage Skills  
--------------------------------------------------------------------  
Recommended skills:  
- scorecard-dq-review  
- scorecard-eda  
- scorecard-fine-classing  
- scorecard-coarse-classing-review  
- scorecard-woe-iv-review  
- scorecard-feature-screening  
- scorecard-policy-variable-review  
- scorecard-model-fitting  
- scorecard-model-review  
- scorecard-deployment-readiness  
- scorecard-monitoring-review  
- annual-review-orchestrator  
  
7.3 Governance Skills  
--------------------------------------------------------------------  
Recommended governance skills:  
- dq-exception-review  
- manual-override-review  
- committee-pack-preparer  
- coarse-classing-review  
- final-model-approval  
- deployment-approval  
  
====================================================================  
8. NON-FUNCTIONAL REQUIREMENTS  
====================================================================  
  
8.1 Explainability  
--------------------------------------------------------------------  
The system shall produce human-readable summaries for recommendations  
and escalations.  
  
8.2 Traceability  
--------------------------------------------------------------------  
All material actions shall be attributable to stage, skill, reviewer,  
and run.  
  
8.3 Reproducibility  
--------------------------------------------------------------------  
Workflow state, skill version, and artifacts shall enable re-running  
or reconstructing prior outcomes.  
  
8.4 Maintainability  
--------------------------------------------------------------------  
Skills, schemas, routing rules, and tools shall be modular and  
separately maintainable.  
  
8.5 Extensibility  
--------------------------------------------------------------------  
The framework shall allow new model stages, review types, and tool  
backends without redesigning the full architecture.  
  
8.6 Performance  
--------------------------------------------------------------------  
The framework shall not materially delay deterministic computation  
beyond orchestration overhead.  
  
8.7 Reliability  
--------------------------------------------------------------------  
Workflow state and logs shall persist safely even when one stage  
fails.  
  
8.8 Security  
--------------------------------------------------------------------  
Access to approvals, logs, and artifacts shall be controlled  
according to user role.  
  
8.9 Environment Flexibility  
--------------------------------------------------------------------  
The system shall support notebook-based operation first, with future  
support for API, CLI, and service-based orchestration.  
  
====================================================================  
9. ASSUMPTIONS  
====================================================================  
  
- Deterministic SDK functions or tools exist or will be developed for  
  core scorecard tasks.  
- Users operate primarily in a Jupyter-based environment.  
- Reviewer identity can be captured through user context, application  
  identity, or manual entry.  
- Structured persistence is available for workflow state, logs, and  
  artifacts.  
- Governance policy packs are available or will be codified.  
  
====================================================================  
10. CONSTRAINTS  
====================================================================  
  
- Final model decisions must remain human accountable.  
- Certain policy exceptions cannot be auto-approved by the AI  
  assistant.  
- Jupyter widget UI is not itself the system of record; state and logs  
  must persist outside transient UI.  
- Legacy environments may limit advanced widget behavior or sidebar  
  integration.  
- The first phase should prioritize governed workflow and traceability  
  over full autonomy.  
  
====================================================================  
11. RISKS AND MITIGATIONS  
====================================================================  
  
Risk 1: Over-automation of judgement-heavy tasks  
--------------------------------------------------------------------  
Mitigation:  
- enforce HITL at mandatory gates  
- restrict skill behavior with guardrails  
- use bounded reviewer actions  
  
Risk 2: Missing observability  
--------------------------------------------------------------------  
Mitigation:  
- use append-only structured logs  
- block restricted actions if logging fails  
  
Risk 3: Workflow ambiguity  
--------------------------------------------------------------------  
Mitigation:  
- define routing rules explicitly  
- require structured workflow state  
- return blocked status when ambiguous  
  
Risk 4: UI tightly coupled to orchestration logic  
--------------------------------------------------------------------  
Mitigation:  
- separate widget, controller, and skill layers  
  
Risk 5: Future integration difficulty  
--------------------------------------------------------------------  
Mitigation:  
- use structured JSON contracts  
- define schemas early  
- keep tools backend-agnostic  
  
====================================================================  
12. DATA CONTRACTS / KEY SCHEMAS  
====================================================================  
  
The solution should define at minimum:  
  
- workflow_state.schema.json  
- hitl_review.schema.json  
- skill_event.schema.json  
- audit_event.schema.json  
- stage_transition.schema.json  
- artifact_registry.schema.json  
- policy_findings.schema.json  
- flow_node.schema.json  
- flow_edge.schema.json  
- session_resume.schema.json  
  
====================================================================  
13. HIGH-LEVEL WORKFLOW  
====================================================================  
  
13.1 Standard Path  
--------------------------------------------------------------------  
intake  
-> data_readiness  
-> dq_review  
-> eda  
-> segmentation_review  
-> fine_classing  
-> coarse_classing  
-> coarse_classing_review  
-> woe_iv_review  
-> feature_engineering  
-> feature_screening  
-> policy_variable_review  
-> model_fitting  
-> scaling_and_calibration  
-> reject_inference_review  
-> champion_challenger_review  
-> model_review  
-> validation_pack  
-> committee_pack  
-> deployment_readiness  
-> deployment_approval  
-> monitoring_pack  
-> closed  
  
13.2 Controlled Rework Paths  
--------------------------------------------------------------------  
- dq_review -> dq_exception_review -> dq_review or eda  
- coarse_classing_review -> coarse_classing or woe_iv_review  
- model_review -> model_fitting or validation_pack  
- deployment_readiness -> model_review or deployment_approval  
- annual_review -> monitoring_pack or model_review  
  
====================================================================  
14. SUCCESS CRITERIA  
====================================================================  
  
The project shall be considered successful when:  
  
1. Core credit scoring stages can be orchestrated through skills.  
2. HITL steps can be displayed and completed through Jupyter-based  
   review widgets.  
3. All reviewer actions and comments are logged in append-only  
   structured format.  
4. Workflow state can be resumed after interruption.  
5. Final model approval and deployment readiness cannot proceed  
   without required logged approvals.  
6. Validation and audit users can reconstruct what happened in a run.  
7. Observability logs can be summarized into a readable workflow flow.  
8. Users can drill down from flow nodes to detailed events and  
   artifacts.  
  
====================================================================  
15. IMPLEMENTATION PRIORITY  
====================================================================  
  
Phase 1  
--------------------------------------------------------------------  
Build:  
- scorecard-orchestrator  
- coarse-classing-review  
- scorecard-model-review  
- scorecard-deployment-readiness  
- workflow state store  
- append-only observability and audit logging  
- project bootstrap and resume flow  
- Jupyter HITL review widget  
  
Phase 2  
--------------------------------------------------------------------  
Add:  
- DQ exception review  
- policy variable review  
- monitoring review  
- annual review  
- committee pack preparation  
- API and service interfaces  
- observability flow summary generation  
  
Phase 3  
--------------------------------------------------------------------  
Enhance:  
- richer custom widgets  
- centralized observability dashboard  
- role-based approval routing  
- MCP or external workflow engine integration  
- interactive flow visualization  
- exportable governance flow views  
  
====================================================================  
16. RECOMMENDED DELIVERABLES  
====================================================================  
  
The implementation should produce:  
  
- skill files (SKILL.md) for required stages  
- routing configuration  
- workflow state schema and storage  
- observability event schema and log writer  
- audit schema and log writer  
- session resume / recovery module  
- Jupyter HITL widgets  
- backend controller layer  
- artifact registry integration  
- flow summarization engine  
- sample project templates  
- test cases for stage transitions and approval blocking  
  
====================================================================  
17. APPENDIX A – SAMPLE HITL ACTIONS  
====================================================================  
  
Common bounded reviewer actions:  
- approve  
- approve_with_changes  
- reject  
- rerun_with_parameters  
- request_more_analysis  
- escalate  
- drop_variable  
- keep_fine_bins_temporarily  
  
====================================================================  
18. APPENDIX B – SAMPLE COARSE CLASSING HITL SCENARIOS  
====================================================================  
  
The coarse classing review shall trigger HITL when:  
  
- IV reduction after merging exceeds configured threshold  
- monotonicity is imperfect after merge  
- one or more bins breach minimum support  
- variable cut points are difficult to explain operationally  
- multiple merge solutions appear acceptable  
- variable is marked high-importance for the final shortlist  
  
====================================================================  
19. SESSION AND PROJECT CONTINUITY  
====================================================================  
  
19.1 Purpose  
--------------------------------------------------------------------  
The system shall support continuity across notebook sessions, user  
sessions, and interrupted workflow runs.  
  
The framework shall allow the user to:  
- resume a prior scorecard project from the latest saved state  
- resume from a failed or blocked stage  
- inspect available prior sessions for a project  
- create a new project when no existing project should be resumed  
  
The system shall minimize user friction by automatically prompting the  
user to choose whether to continue an existing project or create a new  
one.  
  
====================================================================  
20. BUSINESS OBJECTIVE FOR SESSION CONTINUITY  
====================================================================  
  
The session continuity feature is required to:  
  
1. avoid restarting long workflows from the beginning  
2. preserve user effort and prior decisions  
3. support interrupted notebook or kernel sessions  
4. recover safely from failed or partially completed stages  
5. maintain continuity of observability and audit logs  
6. make the assistant more practical for real project usage  
  
====================================================================  
21. FUNCTIONAL REQUIREMENTS – PROJECT BOOTSTRAP AND SESSION RESUME  
====================================================================  
  
FR-080 Project Bootstrap Prompt  
--------------------------------------------------------------------  
When the assistant starts a workflow session without an active project  
context, the system shall automatically prompt the user to either:  
- provide an existing project_id to resume  
- select from available projects  
- create a new project  
  
FR-081 Automatic Continuity Check  
--------------------------------------------------------------------  
At the beginning of each new interaction or orchestration request, the  
system shall check whether:  
- an active workflow state exists  
- the prior session ended in progress  
- the prior session ended in blocked state  
- the prior session ended in failed state  
- the user is already associated with a recent unfinished project  
  
FR-082 Resume Prompt  
--------------------------------------------------------------------  
If a resumable project exists, the system shall prompt the user with a  
structured question such as:  
- resume existing project  
- resume last failed session  
- resume last paused review  
- create new project  
  
FR-083 Project Discovery  
--------------------------------------------------------------------  
The system shall support lookup of prior projects by:  
- project_id  
- portfolio name  
- project name  
- recent session history  
- user ownership or user access scope  
  
FR-084 New Project Creation  
--------------------------------------------------------------------  
If the user chooses not to resume an existing project, the system  
shall support creation of a new project record with:  
- project_id  
- project name  
- portfolio name  
- target definition  
- segment scope  
- business objective  
- creation timestamp  
- created_by  
  
FR-085 Resume from Last Successful State  
--------------------------------------------------------------------  
The system shall support resuming from the last successfully completed  
stage of a project.  
  
FR-086 Resume from Last Failed State  
--------------------------------------------------------------------  
The system shall support resuming from the most recent failed stage,  
provided the failure context and required artifacts are still  
available.  
  
FR-087 Resume from Pending Review  
--------------------------------------------------------------------  
If a project contains a pending HITL review, the system shall resume  
at the review state rather than rerunning downstream stages  
automatically.  
  
FR-088 User Choice on Resume Mode  
--------------------------------------------------------------------  
When resuming a prior project, the system shall let the user choose  
among:  
- resume from latest state  
- resume from last failed stage  
- resume from a selected prior stage  
- create new project instead  
  
FR-089 Error Recovery Mode  
--------------------------------------------------------------------  
If the last session ended with an error, the system shall provide a  
recovery path that includes:  
- error summary  
- failed stage  
- last successful stage  
- artifacts already available  
- suggested next action  
  
FR-090 Safe Resume Validation  
--------------------------------------------------------------------  
Before resuming from any prior state, the system shall validate:  
- workflow state integrity  
- required artifacts still exist  
- prior approvals remain valid  
- stage dependencies are still satisfied  
- no mandatory review is bypassed  
  
FR-091 Resume Blocking Rule  
--------------------------------------------------------------------  
If resume validation fails, the system shall enter blocked state and  
explain:  
- why resume cannot proceed  
- which artifact or approval is missing  
- whether rerun or new project creation is required  
  
FR-092 Session Lineage Preservation  
--------------------------------------------------------------------  
The system shall preserve lineage across resumed sessions, including:  
- original project_id  
- original run_id  
- resumed session ID  
- parent session ID  
- resume timestamp  
- resume reason  
  
FR-093 Resume Logging  
--------------------------------------------------------------------  
The system shall log all resume-related actions, including:  
- resume prompt shown  
- project selected  
- resume mode selected  
- resume validation result  
- stage resumed  
- error recovery path chosen  
  
FR-094 Auto-Suggest Recent Project  
--------------------------------------------------------------------  
If the user has only one recent unfinished project, the system should  
automatically suggest that project first.  
  
FR-095 Multi-Project Choice  
--------------------------------------------------------------------  
If multiple unfinished projects exist, the system shall present a  
clear selection list or structured options rather than guessing.  
  
====================================================================  
22. USER INTERACTION REQUIREMENTS – SESSION START  
====================================================================  
  
UR-001 Initial Session Prompt  
--------------------------------------------------------------------  
When there is no active workflow in memory, the assistant shall ask:  
  
- Do you want to resume an existing scorecard project?  
- Please provide project_id, or choose create new project.  
  
UR-002 Smart Resume Prompt  
--------------------------------------------------------------------  
If a recent unfinished project exists, the assistant shall ask:  
  
- I found a recent unfinished project: <project_id>.  
- Do you want to resume it, resume the last failed stage, or create a  
  new project?  
  
UR-003 Error Recovery Prompt  
--------------------------------------------------------------------  
If the last session failed, the assistant shall ask:  
  
- The last session for project <project_id> stopped at stage <stage>  
  due to an error.  
- Do you want to resume from the failed stage, return to the last  
  successful stage, or create a new project?  
  
UR-004 Pending HITL Prompt  
--------------------------------------------------------------------  
If a pending review exists, the assistant shall ask:  
  
- Project <project_id> has a pending review at stage <stage>.  
- Do you want to continue the review now?  
  
====================================================================  
23. WORKFLOW STATE ENHANCEMENTS  
====================================================================  
  
The workflow state object shall be extended to include session  
continuity fields.  
  
Additional workflow state fields shall include:  
- project_name  
- parent_session_id  
- resume_source_session_id  
- resume_mode  
- resume_reason  
- last_successful_stage  
- last_failed_stage  
- last_error_summary  
- created_by  
- created_timestamp  
- last_updated_timestamp  
  
====================================================================  
24. OBSERVABILITY REQUIREMENTS – SESSION CONTINUITY  
====================================================================  
  
FR-100 Resume Event Types  
--------------------------------------------------------------------  
The system shall support the following additional event types:  
- session_started  
- project_lookup_performed  
- resume_prompt_displayed  
- resume_option_selected  
- resume_validation_passed  
- resume_validation_failed  
- session_resumed  
- recovery_mode_selected  
- new_project_created  
  
FR-101 Resume Event Fields  
--------------------------------------------------------------------  
Resume-related events shall include:  
- event_id  
- event_type  
- timestamp  
- project_id  
- run_id  
- session_id  
- parent_session_id  
- resume_mode  
- previous_stage  
- resumed_stage  
- user_action  
- validation_status  
- error_summary if applicable  
  
FR-102 Error Recovery Logging  
--------------------------------------------------------------------  
If the system resumes after failure, the error summary and selected  
recovery option shall be logged in append-only format.  
  
====================================================================  
25. AUDIT REQUIREMENTS – SESSION RESUME  
====================================================================  
  
FR-110 Resume Audit Trace  
--------------------------------------------------------------------  
The system shall maintain an auditable trace of:  
- when the project was resumed  
- who resumed it  
- which session it resumed from  
- whether it resumed from failed, blocked, paused, or last successful  
  state  
- what validations were performed before resuming  
  
FR-111 No Silent Resume  
--------------------------------------------------------------------  
The system shall not silently resume a failed or paused project  
without explicit user awareness.  
  
FR-112 No Hidden Reset  
--------------------------------------------------------------------  
The system shall not silently create a new project when a resumable  
project exists unless the user explicitly chooses to do so.  
  
====================================================================  
26. ORCHESTRATOR SKILL ENHANCEMENTS  
====================================================================  
  
The scorecard-orchestrator skill shall be enhanced with bootstrap and  
resume logic.  
  
The orchestration skill shall:  
- initialize new projects  
- discover resumable prior projects  
- prompt user for project selection when project context is missing  
- resume safely from paused, blocked, or failed states  
- continue from the correct stage after validation  
  
Additional responsibilities shall include:  
- detect whether the current interaction belongs to an existing  
  project  
- prompt the user for project_id when project context is missing  
- offer new project creation when no prior project is selected  
- resume from the latest valid session state after validation  
- support safe recovery from prior failed stages  
  
Additional required capabilities shall include:  
- list_recent_projects  
- find_project_by_id  
- create_project_record  
- load_latest_project_state  
- load_failed_session_state  
- validate_resume_state  
- create_new_session_from_prior_project  
- persist_session_resume_event  
  
====================================================================  
27. SESSION BOOTSTRAP FLOW  
====================================================================  
  
Standard bootstrap flow:  
1. user starts interaction  
2. orchestrator checks active project context  
3. if no active project exists:  
   - search recent unfinished projects  
   - ask user to provide project_id or create new project  
4. if project selected:  
   - load latest workflow state  
   - validate resume state  
   - propose resume options  
5. if new project selected:  
   - create new project record  
   - initialize workflow state  
6. persist session start and choice logs  
7. continue to first or resumed stage  
  
====================================================================  
28. RESUME MODES  
====================================================================  
  
RM-001 Resume Latest State  
--------------------------------------------------------------------  
Resume from the current saved state if no errors or blocks prevent  
continuation.  
  
RM-002 Resume Last Failed Stage  
--------------------------------------------------------------------  
Resume from the stage that failed last, after validating required  
artifacts and dependencies.  
  
RM-003 Resume Last Successful Stage  
--------------------------------------------------------------------  
Resume from the last successfully completed stage and rerun downstream  
steps.  
  
RM-004 Resume Pending HITL Review  
--------------------------------------------------------------------  
Resume from an outstanding human review without rerunning the prior  
stage.  
  
RM-005 Start New Project  
--------------------------------------------------------------------  
Start a new project while preserving prior project history  
separately.  
  
====================================================================  
29. JUPYTER WIDGET REQUIREMENTS – SESSION CONTINUITY  
====================================================================  
  
FR-120 Project Selection Widget  
--------------------------------------------------------------------  
The system should support a project selection widget in Jupyter to:  
- display recent projects  
- allow manual project_id entry  
- allow new project creation  
  
FR-121 Resume Choice Widget  
--------------------------------------------------------------------  
The system should support a resume choice card that shows:  
- project ID  
- latest stage  
- last successful stage  
- last failed stage  
- pending reviews  
- available resume actions  
  
FR-122 Error Recovery Widget  
--------------------------------------------------------------------  
The system should support a recovery widget showing:  
- prior error summary  
- failed stage  
- recommended recovery path  
- action buttons for resume options  
  
====================================================================  
30. SUCCESS CRITERIA – SESSION CONTINUITY  
====================================================================  
  
The project shall meet the continuity requirement when:  
  
1. the assistant automatically asks for project_id or offers new  
   project creation when no active project exists  
2. a user can resume from last paused, failed, or successful stage  
3. failed sessions can be recovered without losing prior artifacts or  
   decisions  
4. all resume and recovery actions are logged  
5. no restricted stage is resumed without validation  
6. pending HITL reviews are resumed correctly  
  
====================================================================  
31. RECOMMENDED IMPLEMENTATION PRIORITY UPDATE  
====================================================================  
  
Add to Phase 1:  
- project bootstrap prompt  
- recent project lookup  
- new project creation flow  
- resume latest state  
- resume failed state  
- resume pending review  
- session continuity logging  
  
====================================================================  
32. OBSERVABILITY VISUALIZATION AND FLOW SUMMARIZATION  
====================================================================  
  
32.1 Purpose  
--------------------------------------------------------------------  
The system shall transform structured observability and audit events  
into a summarized workflow flow that visually shows the lifecycle  
progression of a project run.  
  
The flow visualization shall allow users to understand:  
- stages executed  
- agent actions taken  
- human decisions made  
- reruns, rejections, and escalations  
- blocked or failed stages  
- final approved route  
  
The visualization shall provide a high-level decision trail, while  
allowing drill-down to detailed event logs, artifacts, evidence, and  
review payloads.  
  
====================================================================  
33. BUSINESS OBJECTIVE FOR FLOW VISUALIZATION  
====================================================================  
  
The observability flow visualization is required to:  
  
1. provide an intuitive view of workflow progression  
2. help users understand where a run succeeded, failed, paused, or  
   rerouted  
3. show the interaction between agent action and human decision  
4. reduce the need to inspect raw logs for every review  
5. improve validation, audit, and governance readability  
6. support post-mortem analysis for failed sessions  
7. support storytelling for model development and governance review  
  
====================================================================  
34. FUNCTIONAL REQUIREMENTS – FLOW SUMMARIZATION  
====================================================================  
  
FR-130 Flow Summary Generation  
--------------------------------------------------------------------  
The system shall summarize structured observability logs into a  
workflow flow representation for each project run.  
  
FR-131 Flow Node Types  
--------------------------------------------------------------------  
The flow visualization shall support distinct node types including:  
- stage node  
- agent action node  
- HITL review node  
- human decision node  
- rerun node  
- escalation node  
- blocked node  
- failed node  
- completed node  
- artifact generation node  
  
FR-132 Flow Edge Types  
--------------------------------------------------------------------  
The flow visualization shall support directional edges to represent:  
- normal progression  
- rerun / retry  
- rejection / rollback  
- escalation  
- resume after pause  
- resume after failure  
- approval path  
- blocked path  
  
FR-133 Flow Status Encoding  
--------------------------------------------------------------------  
Each node and edge shall support status classification such as:  
- pending  
- in_progress  
- completed  
- approved  
- approved_with_changes  
- rejected  
- rerun_requested  
- escalated  
- blocked  
- failed  
- resumed  
  
FR-134 Human vs Agent Distinction  
--------------------------------------------------------------------  
The visualization shall clearly distinguish:  
- agent actions  
- user decisions  
- automated system events  
- review / approval checkpoints  
  
FR-135 Detail Drill-Down  
--------------------------------------------------------------------  
Each flow node shall support linkage to detailed underlying  
information, including:  
- event logs  
- review payload  
- reviewer comment  
- recommendation summary  
- policy findings  
- evidence references  
- artifact links  
- error summary  
  
FR-136 Run-Specific Visualization  
--------------------------------------------------------------------  
The system shall generate the flow visualization at the level of:  
- project  
- run  
- session  
- review instance where applicable  
  
FR-137 Session Lineage View  
--------------------------------------------------------------------  
The system shall support flow continuation across resumed sessions,  
showing:  
- original session  
- resumed session  
- recovery path  
- failed stage recovery  
- continuation after pending HITL review  
  
FR-138 Interactive Navigation  
--------------------------------------------------------------------  
The visualization shall support click-through or linked navigation  
from summary nodes to detailed event records.  
  
FR-139 Flow Export  
--------------------------------------------------------------------  
The system should support export of the summarized flow into:  
- HTML  
- JSON graph structure  
- PNG or SVG snapshot  
- governance pack embedding format  
  
FR-140 Filtering  
--------------------------------------------------------------------  
The visualization should support filtering by:  
- stage  
- status  
- agent action  
- reviewer action  
- error only  
- HITL only  
- rerun only  
- project  
- session  
  
====================================================================  
35. FLOW CONTENT REQUIREMENTS  
====================================================================  
  
FR-141 Node Information  
--------------------------------------------------------------------  
Each summarized node shall contain, where applicable:  
- node_id  
- node_type  
- title  
- stage  
- status  
- timestamp  
- actor_type  
- actor_id  
- summary text  
- linked event IDs  
- linked artifact IDs  
- review_id if applicable  
  
FR-142 Agent Action Summary  
--------------------------------------------------------------------  
Agent action nodes shall summarize:  
- recommendation made  
- tool or skill invoked  
- decision rationale  
- next suggested stage  
- whether the action triggered HITL  
  
FR-143 Human Decision Summary  
--------------------------------------------------------------------  
Human decision nodes shall summarize:  
- reviewer action  
- reviewer selected option  
- reviewer comment  
- whether the reviewer overrode the agent recommendation  
  
FR-144 Error Node Summary  
--------------------------------------------------------------------  
Failed or blocked nodes shall summarize:  
- failure reason  
- error category  
- blocked dependency  
- recommended recovery action  
  
FR-145 Artifact Summary Node  
--------------------------------------------------------------------  
Artifact-related nodes may summarize:  
- artifact generated  
- artifact type  
- producing stage  
- artifact version  
- artifact link  
  
====================================================================  
36. DETAIL LINKAGE REQUIREMENTS  
====================================================================  
  
FR-150 Detailed Event Linkage  
--------------------------------------------------------------------  
Every summarized flow node shall map back to one or more detailed  
structured events.  
  
FR-151 Review Linkage  
--------------------------------------------------------------------  
HITL and reviewer decision nodes shall link to:  
- review payload  
- reviewer response  
- final approved action  
- audit event  
- evidence references  
  
FR-152 Artifact Linkage  
--------------------------------------------------------------------  
Flow nodes shall support links to produced or consumed artifacts such  
as:  
- binning summaries  
- model metrics  
- validation pack  
- committee pack  
- deployment checklist  
- monitoring pack  
  
FR-153 Error Detail Linkage  
--------------------------------------------------------------------  
Error and blocked nodes shall link to:  
- exception summary  
- failed tool call  
- missing artifact reference  
- validation failure details  
  
====================================================================  
37. OBSERVABILITY DATA MODEL ENHANCEMENTS  
====================================================================  
  
The observability model shall include a summarized flow  
representation in addition to raw append-only logs.  
  
Additional logical structures shall include:  
- flow_nodes  
- flow_edges  
- node_event_map  
- node_artifact_map  
- flow_summary_metadata  
  
====================================================================  
38. JUPYTER VISUALIZATION REQUIREMENTS  
====================================================================  
  
FR-160 Flowchart Widget  
--------------------------------------------------------------------  
The system should support a Jupyter visualization component or widget  
that displays the summarized workflow flow.  
  
FR-161 Node Click Interaction  
--------------------------------------------------------------------  
Clicking a node in the flowchart should display:  
- node summary  
- detailed events  
- related artifacts  
- linked review data  
- error details if applicable  
  
FR-162 Right Panel / Detail Pane  
--------------------------------------------------------------------  
The visualization should support a detail pane or linked detail  
section to show expanded information when a node is selected.  
  
FR-163 Stage Timeline View  
--------------------------------------------------------------------  
The system should support an alternative timeline view in addition to  
graph view.  
  
FR-164 Multi-Level View  
--------------------------------------------------------------------  
The visualization should support multiple levels:  
- high-level lifecycle flow  
- stage-level drill-down  
- event-level details  
  
====================================================================  
39. REPORTING AND GOVERNANCE REQUIREMENTS  
====================================================================  
  
FR-170 Governance Storytelling View  
--------------------------------------------------------------------  
The system should provide a concise governance-friendly view showing:  
- stage progression  
- major human approvals  
- major reruns  
- key exceptions  
- final outcome  
  
FR-171 Technical Replay View  
--------------------------------------------------------------------  
The system should provide a technical replay view showing:  
- event sequence  
- tool actions  
- detailed state changes  
- failure and retry path  
  
FR-172 Audit Support  
--------------------------------------------------------------------  
The flowchart shall serve as a navigation layer only. It shall not  
replace raw logs as the system of record.  
  
FR-173 Embedded Flow for Packs  
--------------------------------------------------------------------  
The flow visualization should be embeddable into:  
- technical documentation  
- validation pack  
- committee pack  
- annual review pack  
  
====================================================================  
40. NON-FUNCTIONAL REQUIREMENTS – FLOW VISUALIZATION  
====================================================================  
  
NFR-020 Clarity  
--------------------------------------------------------------------  
The summarized flow shall be understandable by both technical and  
non-technical users.  
  
NFR-021 Traceability  
--------------------------------------------------------------------  
Every visual node shall be traceable to underlying event records.  
  
NFR-022 Performance  
--------------------------------------------------------------------  
The system should generate the flow summary efficiently for long-  
running projects with many events.  
  
NFR-023 Extensibility  
--------------------------------------------------------------------  
The visualization model shall support future node types and lifecycle  
stages without redesigning the whole structure.  
  
NFR-024 Consistency  
--------------------------------------------------------------------  
Flow summarization rules shall be consistent across all skills and  
stages.  
  
====================================================================  
41. SUCCESS CRITERIA – FLOW VISUALIZATION  
====================================================================  
  
This requirement shall be considered successful when:  
  
1. a project run can be visualized as a flow of stage, agent, and  
   human decision nodes  
2. reviewers can identify reruns, approvals, rejections, escalations,  
   and failures quickly  
3. each flow node can be linked back to underlying detailed logs and  
   artifacts  
4. resumed sessions can be shown as part of one coherent lineage  
5. the flow can be embedded into governance or review outputs  
  
====================================================================  
42. RECOMMENDED IMPLEMENTATION PRIORITY UPDATE  
====================================================================  
  
Add to implementation roadmap:  
  
Phase 1  
--------------------------------------------------------------------  
- structured event logs  
- node and edge summarization rules  
- basic flow JSON generation  
- stage transition visualization  
  
Phase 2  
--------------------------------------------------------------------  
- interactive Jupyter flow widget  
- drill-down detail panel  
- filtering and highlighting  
- resume lineage display  
  
Phase 3  
--------------------------------------------------------------------  
- export to HTML / SVG / governance packs  
- cross-run comparison flow  
- aggregated analytics of reviewer behavior and rerun patterns  
  
====================================================================  
END OF URD  
====================================================================  
