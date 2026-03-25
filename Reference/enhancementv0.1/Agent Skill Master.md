# Agent Skill Master  
  
====================================================================  
AGENT AND SKILL MASTER REFERENCE MATRIX  
ENTERPRISE AGENTIC AI MODEL LIFECYCLE PLATFORM  
====================================================================  
  
COLUMNS  
--------------------------------------------------------------------  
Agent/Skill,Type,Purpose,Uses Which SDKs,Key Inputs,Key Outputs,HITL?  
  
NOTES  
--------------------------------------------------------------------  
- "Type" can be Platform Agent, Role Agent, Domain Skill, Stage Skill,  
  Overlay Skill, or Support Skill.  
- "Uses Which SDKs" lists the primary SDKs expected in normal runtime.  
- "HITL?" indicates whether the agent/skill commonly creates, uses,  
  or depends on human-in-the-loop review.  
  
====================================================================  
1) PLATFORM / ORCHESTRATION AGENTS AND SKILLS  
====================================================================  
  
Agent/Skill,Type,Purpose,Uses Which SDKs,Key Inputs,Key Outputs,HITL?  
platform-base-rules,Platform Skill,Enforce invariant platform rules such as no silent approval no silent version selection required logging and human accountability,config_sdk; registry_sdk; observabilitysdk; auditsdk; artifactsdk,workflow_state; active_role; active_stage; policy_mode,enforcement flags; block decisions; standard warnings,Indirect  
model-lifecycle-orchestrator,Platform Agent,Coordinate workflow routing stage transitions SDK invocation review creation and state persistence,workflowsdk; hitlsdk; observabilitysdk; auditsdk; artifactsdk; policysdk; registry_sdk; config_sdk,current workflow_state; role; domain; stage; selected versions; artifacts; policy refs,updated workflow state; next stage; review request; blocked or success status,Yes  
session-bootstrap-orchestrator,Platform Agent,Handle new project bootstrap project selection resume detection and session restoration,workflowsdk; registry_sdk; config_sdk; observabilitysdk; auditsdk,user_id; recent projects; existing runs; pending reviews,active project context; active run; resume mode; initialized session,Yes  
recovery-orchestrator,Platform Agent,Handle safe recovery after failure blocked workflow or interrupted review,workflowsdk; observabilitysdk; auditsdk; artifactsdk; registry_sdk; policysdk,failed workflow_state; error summary; checkpoints; artifacts; review states,recovery recommendation; resumed path; rerun request; blocked state,Yes  
interaction-orchestrator,Platform Agent,Coordinate UI-driven review interaction preview recompute finalization and escalation,hitlsdk; workflowsdk; observabilitysdk; auditsdk; artifactsdk; jupyter_bridge; widgetsdk,interaction payload; current review state; user action,preview result; final decision payload; updated review state,Yes  
  
====================================================================  
2) ROLE AGENTS  
====================================================================  
  
Agent/Skill,Type,Purpose,Uses Which SDKs,Key Inputs,Key Outputs,HITL?  
developer-agent,Role Agent,Assist model developers in proposing refining comparing and finalizing development artifacts,workflowsdk; hitlsdk; artifactsdk; observabilitysdk; dq_sdk; feature_sdk; evaluation_sdk; reporting_sdk; dataprepsdk; relevant domain SDK,project context; active stage; candidate artifacts; metrics; config refs,candidate proposals; summaries; refined outputs; rerun suggestions,Yes  
validator-agent,Role Agent,Assist model validation in independent challenge evidence review model fitness assessment and structured conclusions,validationsdk; hitlsdk; workflowsdk; observabilitysdk; auditsdk; artifactsdk; policysdk; evaluation_sdk; reporting_sdk; knowledge_sdk; rag_sdk,validation config; findings; artifacts; evidence summaries; policy refs,evidence gap summary; findings; fitness summary; conclusion draft,Yes  
governance-agent,Role Agent,Support governance control checks policy interpretation approvals conditions and escalation,policysdk; hitlsdk; workflowsdk; observabilitysdk; auditsdk; artifactsdk; reporting_sdk,policy packs; pending approvals; unresolved findings; deployment state,approval readiness summary; conditions; escalation recommendation,Yes  
reviewer-agent,Role Agent,Support generic structured reviewer behavior where evidence review and bounded actions are needed,hitlsdk; workflowsdk; observabilitysdk; artifactsdk; reporting_sdk,review payload; evidence refs; allowed actions,review response; comments; bounded decision,Yes  
approver-agent,Role Agent,Support approval-oriented review with concise decision framing and conditions tracking,hitlsdk; auditsdk; policysdk; workflowsdk; reporting_sdk,approval payload; conditions; policy rules,approval decision; conditional approval; rejection; escalation,Yes  
documentation-agent,Role Agent,Draft technical notes committee packs validation memos executive summaries and audit responses,reporting_sdk; artifactsdk; auditsdk; flowvizsdk; knowledge_sdk; rag_sdk; validationsdk,templates; approved wording; project summaries; findings; decisions,drafted sections; pack content; narrative blocks,Usually No  
monitoring-agent,Role Agent,Interpret monitoring snapshots breaches trends and annual review outcomes,monitoringsdk; evaluation_sdk; reporting_sdk; observabilitysdk; artifactsdk; knowledge_sdk; rag_sdk,current and prior snapshots; thresholds; monitoring history,monitoring summary; breach interpretation; action recommendation,Yes  
remediation-agent,Role Agent,Support remediation planning closure evidence review and revalidation readiness,validationsdk; auditsdk; observabilitysdk; artifactsdk; reporting_sdk; workflowsdk,open findings; action log; closure evidence; due dates,remediation plan; closure recommendation; status update,Yes  
  
====================================================================  
3) DOMAIN SKILLS  
====================================================================  
  
Agent/Skill,Type,Purpose,Uses Which SDKs,Key Inputs,Key Outputs,HITL?  
scorecard-domain,Domain Skill,Inject scorecard-specific concepts tests artifacts and review expectations,scorecardsdk; dataprepsdk; evaluation_sdk; reporting_sdk; monitoringsdk,scorecard dataset refs; binning artifacts; score metrics,scorecard-aware guidance; warnings; stage context,Indirect  
timeseries-domain,Domain Skill,Inject time-series-specific concepts diagnostics and workflow expectations,timeseriessdk; dataprepsdk; evaluation_sdk; reporting_sdk,time index definitions; series artifacts; model diagnostics,time-series-aware guidance; warnings; stage context,Indirect  
ecl-domain,Domain Skill,Inject ECL-specific concepts such as staging MEV scenarios overlays and output interpretation,eclsdk; dataprepsdk; pdsdk; lgdsdk; eadsdk; evaluation_sdk,ECL inputs; scenarios; overlay refs; staging rules,ECL-aware guidance; warnings; stage context,Indirect  
lgd-domain,Domain Skill,Inject LGD-specific concepts such as cure severity downturn and forward-looking adjustments,lgdsdk; dataprepsdk; evaluation_sdk,LGD artifacts; recovery logic; severity outputs,LGD-aware guidance; warnings,Indirect  
pd-domain,Domain Skill,Inject PD-specific concepts such as calibration term structure and transition logic,pdsdk; dataprepsdk; evaluation_sdk,PD artifacts; calibration outputs; rating/score inputs,PD-aware guidance; warnings,Indirect  
ead-domain,Domain Skill,Inject EAD-specific concepts such as exposure utilization and CCF logic,eadsdk; dataprepsdk; evaluation_sdk,EAD datasets; exposure outputs; utilization features,EAD-aware guidance; warnings,Indirect  
sicr-domain,Domain Skill,Inject SICR-specific concepts such as threshold movement and migration logic,sicr_sdk; dataprepsdk; evaluation_sdk,SICR datasets; threshold configs; migration outputs,SICR-aware guidance; warnings,Indirect  
stress-domain,Domain Skill,Inject stress-testing-specific concepts such as scenarios stressed outputs and aggregation,stresssdk; dataprepsdk; evaluation_sdk,stress scenarios; stressed outputs; macro inputs,stress-aware guidance; warnings,Indirect  
  
====================================================================  
4) STAGE SKILLS – DEVELOPMENT / MODEL BUILD  
====================================================================  
  
Agent/Skill,Type,Purpose,Uses Which SDKs,Key Inputs,Key Outputs,HITL?  
data-readiness-review,Stage Skill,Assess whether source and prepared data are ready for modeling,dataprepsdk; dq_sdk; dataset_sdk; hitlsdk; workflowsdk,prepared dataset manifest; DQ summary; lineage manifest,data readiness summary; issues; review payload,Yes  
coarse-classing-review,Stage Skill,Review proposed coarse bins support structured edits preview recalculation and finalization,scorecardsdk; evaluation_sdk; hitlsdk; workflowsdk; artifactsdk; observabilitysdk,fine bins; proposed coarse bins; WoE/IV; support metrics,preview result; accepted bins; rerun request; final bin artifact,Yes  
binning-version-selection,Stage Skill,Compare multiple binning candidates and enforce explicit final selection,scorecardsdk; evaluation_sdk; hitlsdk; workflowsdk; artifactsdk; auditsdk,candidate binning versions; comparison metrics; policy flags,selected candidate version; comparison summary; selection record,Yes  
feature-shortlist-review,Stage Skill,Review shortlisted variables and finalize feature set,scorecardsdk; feature_sdk; evaluation_sdk; hitlsdk; workflowsdk,feature shortlist candidates; feature diagnostics; policy flags,final shortlist; warnings; rationale,Yes  
model-fitting-review,Stage Skill,Review candidate fitted models and summarize trade-offs before final selection,relevant domain SDK; evaluation_sdk; hitlsdk; workflowsdk; artifactsdk,model candidates; metrics; diagnostics; stability tests,comparison summary; recommended next action; review payload,Yes  
model-selection,Stage Skill,Finalize chosen candidate model for downstream use,relevant domain SDK; workflowsdk; hitlsdk; auditsdk; artifactsdk,model candidate IDs; comparison summary; approval context,selected model record; approval trail; next stage unlock,Yes  
scaling-and-calibration-review,Stage Skill,Review scaling calibration thresholds or overlays before finalizing,relevant domain SDK; evaluation_sdk; hitlsdk; workflowsdk; artifactsdk,scaling outputs; calibration metrics; threshold rules,final scaling/calibration decision; warnings,Yes  
deployment-readiness,Stage Skill,Assess readiness for implementation or deployment and required conditions,policysdk; hitlsdk; workflowsdk; auditsdk; artifactsdk; reporting_sdk,validation conclusion; unresolved issues; implementation evidence,approval readiness summary; conditions; decision payload,Yes  
committee-pack-preparation,Stage Skill,Assemble governance-ready pack for committee review,reporting_sdk; artifactsdk; auditsdk; flowvizsdk; knowledge_sdk,selected outputs; findings; decisions; approved wording,committee pack artifacts; summary notes,Usually No  
documentation-pack-preparation,Stage Skill,Assemble technical documentation and reproducibility artifacts,reporting_sdk; artifactsdk; dataset_sdk; knowledge_sdk,manifests; outputs; lineage; findings; decisions,technical note package; documentation artifacts,Usually No  
  
====================================================================  
5) STAGE SKILLS – VALIDATION  
====================================================================  
  
Agent/Skill,Type,Purpose,Uses Which SDKs,Key Inputs,Key Outputs,HITL?  
validation-scope-definition,Stage Skill,Define validation scope evidence expectations and challenge boundaries,validationsdk; policysdk; hitlsdk; workflowsdk,validation config; project scope; model family; deployment context,validation scope record; evidence checklist; review payload,Yes  
evidence-intake-review,Stage Skill,Review completeness quality and relevance of supplied validation evidence,validationsdk; artifactsdk; knowledge_sdk; rag_sdk; hitlsdk,evidence refs; manifests; required evidence classes,evidence completeness summary; missing evidence list,Yes  
methodology-review,Stage Skill,Challenge conceptual design assumptions and methodology appropriateness,validationsdk; evaluation_sdk; knowledge_sdk; rag_sdk; hitlsdk,methodology docs; model artifacts; prior patterns,methodology findings; challenge notes; suggested tests,Yes  
data-validation-review,Stage Skill,Challenge data representativeness lineage and sample construction,validationsdk; dataprepsdk; dataset_sdk; dq_sdk; hitlsdk,data prep manifests; splits; DQ outputs; sample definitions,data-related findings; evidence gaps; severity proposals,Yes  
implementation-validation-review,Stage Skill,Challenge implementation reproducibility and controls,validationsdk; artifactsdk; auditsdk; reporting_sdk; hitlsdk,implementation evidence; manifests; logs; controls pack,implementation findings; control assessment,Yes  
model-fitness-review,Stage Skill,Assess fit-for-use dimensions and summarize model strengths weaknesses and limitations,validationsdk; evaluation_sdk; knowledge_sdk; rag_sdk; hitlsdk,findings; diagnostics; evidence completeness; policy rules,fitness matrix; draft conclusion options,Yes  
validation-conclusion,Stage Skill,Prepare structured validation conclusion and conditions for human validator decision,validationsdk; hitlsdk; auditsdk; reporting_sdk; policysdk,fitness summary; findings; conditions; approval rules,validation conclusion draft; final conclusion payload,Yes  
remediation-closure,Stage Skill,Assess whether remediation evidence supports closure and revalidation readiness,validationsdk; auditsdk; artifactsdk; hitlsdk; workflowsdk,remediation evidence; closure notes; prior findings,closure recommendation; reopened issue or closure record,Yes  
  
====================================================================  
6) STAGE SKILLS – MONITORING / ANNUAL REVIEW  
====================================================================  
  
Agent/Skill,Type,Purpose,Uses Which SDKs,Key Inputs,Key Outputs,HITL?  
monitoring-snapshot-ingestion,Stage Skill,Ingest and validate a new monitoring snapshot,monitoringsdk; dataset_sdk; dq_sdk; workflowsdk,new snapshot data; monitoring template; baseline refs,validated snapshot; snapshot record; ingestion summary,Usually No  
monitoring-metric-generation,Stage Skill,Generate monitoring metrics and dashboard payloads from latest snapshot,monitoringsdk; evaluation_sdk; artifactsdk; workflowsdk,current snapshot; monitoring history; thresholds,monitoring KPI tables; dashboard payload; breach flags,Usually No  
monitoring-breach-review,Stage Skill,Review and disposition monitoring breaches or warnings,monitoringsdk; hitlsdk; policysdk; auditsdk; reporting_sdk,breach table; trend view; action history,breach disposition; action recommendation; escalation payload,Yes  
annual-review-outcome,Stage Skill,Summarize annual monitoring outcomes unresolved issues and next actions,monitoringsdk; reporting_sdk; flowvizsdk; hitlsdk; knowledge_sdk,monitoring history; annual pack; unresolved actions,annual review summary; action plan; escalation if needed,Yes  
monitoring-action-assignment,Stage Skill,Assign owners and due dates to monitoring actions,monitoringsdk; auditsdk; hitlsdk; workflowsdk,breach actions; owner registry; severity,action assignment records; due dates,Yes  
  
====================================================================  
7) OVERLAY SKILLS  
====================================================================  
  
Agent/Skill,Type,Purpose,Uses Which SDKs,Key Inputs,Key Outputs,HITL?  
strict-governance-overlay,Overlay Skill,Tighten approval and escalation logic for sensitive workflows,policysdk; hitlsdk; workflowsdk,policy mode; stage; severity context,additional controls; stricter escalation thresholds,Indirect  
validation-pack-overlay,Overlay Skill,Inject validation-specific controls evidence expectations and independence rules,validationsdk; policysdk; hitlsdk,validation config; role; stage,validation-specific warnings; stricter evidence requirements,Indirect  
committee-pack-overlay,Overlay Skill,Adjust outputs for governance or committee audience,reporting_sdk; knowledge_sdk,reporting mode; audience type,committee-oriented wording and summaries,No  
annual-review-overlay,Overlay Skill,Apply annual-review-specific expectations and routing,monitoringsdk; workflowsdk; policysdk,annual review mode; unresolved issues,annual-review routing and summary guidance,Indirect  
material-change-overlay,Overlay Skill,Apply controls for redevelopment or material model change,policysdk; workflowsdk; validationsdk,change classification; impacted model/version,additional review triggers and conditions,Indirect  
remediation-overlay,Overlay Skill,Apply controls for remediation and closure workflows,validationsdk; workflowsdk; auditsdk,open finding severity; remediation state,remediation-specific routing and closure conditions,Indirect  
  
====================================================================  
8) SUPPORT SKILLS  
====================================================================  
  
Agent/Skill,Type,Purpose,Uses Which SDKs,Key Inputs,Key Outputs,HITL?  
candidate-comparison-assistant,Support Skill,Produce normalized comparisons of candidates across models bins or outputs,evaluation_sdk; reporting_sdk; artifactsdk,candidate IDs; metrics; diagnostics,comparison summary; ranked alternatives,Usually No  
evidence-gap-detector,Support Skill,Identify missing stale inconsistent or insufficient evidence,validationsdk; knowledge_sdk; rag_sdk; artifactsdk,evidence list; required evidence classes,evidence gap summary; missing evidence list,Usually No  
benchmark-comparison-assistant,Support Skill,Compare current outputs to benchmark or prior accepted patterns,evaluation_sdk; knowledge_sdk; rag_sdk,current summary; benchmark summaries,benchmark comparison note; deviation flags,Usually No  
artifact-readiness-checker,Support Skill,Check whether required artifacts exist and are usable for next stage,artifactsdk; workflowsdk; dataset_sdk,required artifact list; current artifact registry,artifact readiness summary; missing refs,Usually No  
policy-breach-explainer,Support Skill,Explain why a threshold or policy breach happened and likely consequences,policysdk; reporting_sdk; knowledge_sdk,breach object; threshold definition; policy context,compact breach explanation; likely next steps,Usually No  
issue-severity-advisor,Support Skill,Suggest severity level for findings based on impact and evidence,validationsdk; policysdk; knowledge_sdk,finding summary; policy rules; precedent patterns,severity proposal; rationale summary,Usually No  
flow-summary-narrator,Support Skill,Explain workflow path review events and key decisions from a flow graph,flowvizsdk; reporting_sdk; auditsdk,flow graph payload; event summaries; decision refs,flow narrative; timeline summary,Usually No  
technical-report-drafter,Support Skill,Draft technical sections from structured artifacts and summaries,reporting_sdk; knowledge_sdk; rag_sdk; artifactsdk,template; section scope; artifact summaries,drafted technical section,No  
executive-summary-drafter,Support Skill,Draft concise executive or management summary from structured facts,reporting_sdk; knowledge_sdk; auditsdk,approved wording; key decisions; KPIs,drafted executive summary,No  
validation-note-drafter,Support Skill,Draft validation memos and structured finding/conclusion wording,reporting_sdk; validationsdk; knowledge_sdk,findings; fitness summary; conclusion options,drafted validation note sections,No  
audit-response-assistant,Support Skill,Draft evidence-linked responses to audit or review questions,reporting_sdk; artifactsdk; auditsdk; knowledge_sdk,audit query; linked evidence; prior decisions,drafted response; evidence map,No  
  
====================================================================  
9) AGENT / SKILL TO SDK USAGE PATTERN SUMMARY  
====================================================================  
  
Agent/Skill,Type,Purpose,Uses Which SDKs,Key Inputs,Key Outputs,HITL?  
All governed review skills,Pattern,Use the same core control pattern,workflowsdk; hitlsdk; observabilitysdk; auditsdk; artifactsdk,workflow_state; review payload; evidence refs,decision result; updated state; audit/event refs,Yes  
All development skills,Pattern,Use deterministic domain logic plus evaluation and reporting,relevant domain SDK; dataprepsdk; feature_sdk; evaluation_sdk; reporting_sdk,prepared data; candidate artifacts; metrics,candidates; summaries; artifacts,Usually Yes  
All validation skills,Pattern,Use validation workflow plus evidence and policy controls,validationsdk; policysdk; hitlsdk; reporting_sdk; knowledge_sdk; rag_sdk,validation config; findings; evidence; prior patterns,findings; conclusion drafts; remediation updates,Yes  
All monitoring skills,Pattern,Use monitoring snapshot history metrics and dashboards,monitoringsdk; evaluation_sdk; reporting_sdk; policysdk,current snapshot; baseline; history,breach summary; dashboard payload; review action,Usually Yes for breaches  
  
====================================================================  
END OF AGENT AND SKILL MASTER REFERENCE MATRIX  
====================================================================  
  
====================================================================  
RUNTIME RESOLUTION MASTER MATRIX  
ENTERPRISE AGENTIC AI MODEL LIFECYCLE PLATFORM  
COMPREHENSIVE REFERENCE  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This reference defines how the platform should resolve the active  
runtime stack for each major workflow stage.  
  
For each stage, it specifies:  
- workflow context  
- active role agent  
- active domain skill  
- active stage skill  
- overlay skills  
- SDK allowlist  
- UI mode  
- interaction mode  
- expected status patterns  
- HITL expectations  
- main inputs  
- main outputs  
  
This matrix is intended to guide:  
- skill stack resolver design  
- workflow routing design  
- Jupyter / CodeBuddy experience design  
- agent / SDK integration  
- auditability and governance discipline  
  
====================================================================  
1. GLOBAL RUNTIME RESOLUTION RULES  
====================================================================  
  
1.1 Base Resolution Formula  
--------------------------------------------------------------------  
Effective runtime stack shall be:  
  
Platform Base Rules  
+ Platform Orchestrator  
+ Active Role Agent  
+ Active Domain Skill  
+ Active Stage Skill  
+ Optional Overlay Skill(s)  
+ Runtime Context  
+ SDK Allowlist  
+ UI Mode  
+ Interaction Mode  
  
1.2 Always-Active Base Skills  
--------------------------------------------------------------------  
The following shall always be active:  
  
- platform-base-rules  
- model-lifecycle-orchestrator  
  
The following may also be active depending on entry point:  
- session-bootstrap-orchestrator  
- recovery-orchestrator  
- interaction-orchestrator  
  
1.3 Runtime Context Fields Required  
--------------------------------------------------------------------  
The resolver should read at minimum:  
  
- project_id  
- run_id  
- session_id  
- active_role  
- active_domain  
- active_stage  
- workflow_mode  
- validation_mode  
- pending_review_type  
- selected_candidate_version_id  
- candidate_versions_present  
- policy_mode  
- annual_review_mode  
- remediation_mode  
- failure_state  
- ui_entry_point  
  
1.4 Common UI Modes  
--------------------------------------------------------------------  
The platform shall support at least these UI modes:  
  
- standard_chat_plus_context  
- three_panel_review_workspace  
- candidate_comparison_workspace  
- validation_review_workspace  
- dashboard_review_workspace  
- recovery_workspace  
- bootstrap_workspace  
- documentation_workspace  
- flow_explorer_workspace  
  
1.5 Common Interaction Modes  
--------------------------------------------------------------------  
The platform shall support at least these interaction modes:  
  
- routing_only  
- review_and_approve  
- edit_and_finalize  
- candidate_comparison_and_selection  
- validation_challenge  
- review_and_conclude  
- triage_and_disposition  
- recovery_decision  
- drafting_support  
- monitoring_dashboard_review  
  
1.6 Standard Status Expectations  
--------------------------------------------------------------------  
Common statuses expected from stage runtime:  
  
- success  
- success_with_warning  
- blocked  
- failed  
- pending_human_review  
- preview_ready  
- rerun_requested  
- escalated  
- paused  
- resumed  
- finalized  
- invalid_input  
- invalid_needs_review  
  
====================================================================  
2. SESSION / ENTRY / CONTROL STAGES  
====================================================================  
  
--------------------------------------------------------------------  
2.1 SESSION START / PROJECT ENTRY  
--------------------------------------------------------------------  
Stage Name:  
session_start  
  
Workflow Context:  
User opens CodeBuddy or workspace without an active confirmed context.  
  
Active Role Agent:  
None yet or user-default role  
  
Active Domain Skill:  
None yet unless inferred from active project  
  
Active Stage Skill:  
session-bootstrap-orchestrator  
  
Overlay Skills:  
None normally  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- session-bootstrap-orchestrator  
  
SDK Allowlist:  
- config_sdk  
- registry_sdk  
- workflowsdk  
- observabilitysdk  
- auditsdk  
  
UI Mode:  
bootstrap_workspace or standard_chat_plus_context  
  
Interaction Mode:  
routing_only or review_and_approve for resume choice  
  
Expected Status Patterns:  
- success  
- pending_human_review  
- blocked  
  
HITL Expectations:  
Human selects:  
- resume project  
- choose project  
- create new project  
- resume pending review  
  
Main Inputs:  
- user identity  
- project registry  
- run registry  
- pending review records  
  
Main Outputs:  
- active project context  
- active run  
- resume choice  
- initialized session state  
  
Notes:  
This stage should be token-light and rely on exact registry lookups,  
not semantic retrieval.  
  
--------------------------------------------------------------------  
2.2 SAFE RESUME / RECOVERY ENTRY  
--------------------------------------------------------------------  
Stage Name:  
resume_or_recovery_entry  
  
Workflow Context:  
There is prior failed, blocked, or paused work.  
  
Active Role Agent:  
Based on prior role or recovery-mode role  
  
Active Domain Skill:  
Prior project domain  
  
Active Stage Skill:  
recovery-orchestrator  
  
Overlay Skills:  
- remediation-overlay if relevant  
- strict-governance-overlay if sensitive stage  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- recovery-orchestrator  
  
SDK Allowlist:  
- config_sdk  
- registry_sdk  
- workflowsdk  
- observabilitysdk  
- auditsdk  
- artifactsdk  
- policysdk  
  
UI Mode:  
recovery_workspace  
  
Interaction Mode:  
recovery_decision  
  
Expected Status Patterns:  
- success  
- pending_human_review  
- blocked  
- resumed  
- rerun_requested  
  
HITL Expectations:  
Human may choose:  
- retry  
- rerun from checkpoint  
- resume pending review  
- create new branch/run  
  
Main Inputs:  
- failed workflow state  
- event history  
- checkpoint refs  
- artifact status  
- pending reviews  
- selected versions  
  
Main Outputs:  
- recovery recommendation  
- chosen recovery path  
- resumed state or new run branch  
  
====================================================================  
3. DATA PREPARATION AND DATA READINESS STAGES  
====================================================================  
  
--------------------------------------------------------------------  
3.1 DATA PREPARATION REQUEST  
--------------------------------------------------------------------  
Stage Name:  
data_preparation  
  
Workflow Context:  
Need to prepare modeling dataset from approved template and lineage  
config.  
  
Active Role Agent:  
developer-agent  
  
Active Domain Skill:  
Depends on project:  
- scorecard-domain  
- timeseries-domain  
- ecl-domain  
- lgd-domain  
- pd-domain  
- ead-domain  
- sicr-domain  
- stress-domain  
  
Active Stage Skill:  
No separate stage skill mandatory, or use:  
data-preparation-execution  
  
Overlay Skills:  
- strict-governance-overlay if protected template mode  
- material-change-overlay if rebuilding historical dataset for change  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
  
SDK Allowlist:  
- config_sdk  
- registry_sdk  
- dataset_sdk  
- dq_sdk  
- dataprepsdk  
- artifactsdk  
- observabilitysdk  
- auditsdk  
  
UI Mode:  
standard_chat_plus_context or documentation_workspace for summary  
  
Interaction Mode:  
routing_only or review_and_approve if config ambiguity exists  
  
Expected Status Patterns:  
- success  
- success_with_warning  
- needs_human_review  
- invalid_config  
- invalid_lineage  
- failed  
  
HITL Expectations:  
Optional when:  
- grain mapping ambiguous  
- target definition override requested  
- lineage conflict unresolved  
  
Main Inputs:  
- template ID  
- dataprep config  
- source refs  
- target definition  
- split definition  
  
Main Outputs:  
- prepared dataset  
- manifests  
- lineage summary  
- data prep summary  
- warnings  
  
Notes:  
This stage should be heavily deterministic and token-thrifty. Agent  
should summarize outputs, not narrate transformation details unless  
asked.  
  
--------------------------------------------------------------------  
3.2 DATA READINESS REVIEW  
--------------------------------------------------------------------  
Stage Name:  
data_readiness_review  
  
Workflow Context:  
Prepared dataset needs readiness confirmation before modeling.  
  
Active Role Agent:  
developer-agent or reviewer-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
data-readiness-review  
  
Overlay Skills:  
- strict-governance-overlay if readiness must be signed off  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- dataprepsdk  
- dataset_sdk  
- dq_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- observabilitysdk  
- reporting_sdk  
  
UI Mode:  
three_panel_review_workspace  
  
Interaction Mode:  
review_and_approve  
  
Expected Status Patterns:  
- pending_human_review  
- success  
- success_with_warning  
- blocked  
  
HITL Expectations:  
Often yes when readiness approval is governed.  
  
Main Inputs:  
- data prep manifest  
- DQ summary  
- split summary  
- leakage summary  
- lineage manifest  
  
Main Outputs:  
- readiness decision  
- readiness notes  
- rerun request if needed  
  
====================================================================  
4. SCORECARD DEVELOPMENT STAGES  
====================================================================  
  
--------------------------------------------------------------------  
4.1 FINE CLASSING  
--------------------------------------------------------------------  
Stage Name:  
fine_classing  
  
Workflow Context:  
Generate initial bin structures from prepared dataset.  
  
Active Role Agent:  
developer-agent  
  
Active Domain Skill:  
scorecard-domain  
  
Active Stage Skill:  
fine-classing-execution or direct scorecardsdk logic  
  
Overlay Skills:  
None normally  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
  
SDK Allowlist:  
- scorecardsdk  
- dataprepsdk  
- feature_sdk  
- evaluation_sdk  
- artifactsdk  
- observabilitysdk  
  
UI Mode:  
standard_chat_plus_context  
  
Interaction Mode:  
routing_only  
  
Expected Status Patterns:  
- success  
- success_with_warning  
- failed  
  
HITL Expectations:  
Usually no for execution itself  
  
Main Inputs:  
- prepared dataset  
- fine classing config  
- variable list  
  
Main Outputs:  
- fine bin artifacts  
- initial metrics  
- candidate bin structures  
  
--------------------------------------------------------------------  
4.2 COARSE CLASSING REVIEW  
--------------------------------------------------------------------  
Stage Name:  
coarse_classing_review  
  
Workflow Context:  
Review and refine proposed coarse bins, often variable-level.  
  
Active Role Agent:  
developer-agent  
Possible alternate: reviewer-agent  
  
Active Domain Skill:  
scorecard-domain  
  
Active Stage Skill:  
coarse-classing-review  
  
Overlay Skills:  
- strict-governance-overlay if mandatory approval  
- committee-pack-overlay rarely  
- validation-pack-overlay only if validator is reviewing after development  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- scorecardsdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- observabilitysdk  
- auditsdk  
- reporting_sdk  
  
UI Mode:  
three_panel_review_workspace  
  
Interaction Mode:  
edit_and_finalize  
  
Expected Status Patterns:  
- pending_human_review  
- preview_ready  
- valid_final  
- valid_with_warning  
- invalid_needs_review  
- rerun_requested  
- escalated  
  
HITL Expectations:  
Mandatory for governed coarse classing review.  
  
Main Inputs:  
- fine bin table  
- proposed coarse bins  
- variable-level support metrics  
- WoE / IV summaries  
- policy thresholds  
- candidate versions if multiple  
  
Main Outputs:  
- accepted coarse bins  
- edited bin definition  
- updated metrics  
- new candidate version if rerun  
- final artifact refs  
  
Notes:  
This is one of the strongest examples of the 3-panel review workspace.  
  
--------------------------------------------------------------------  
4.3 BINNING VERSION SELECTION  
--------------------------------------------------------------------  
Stage Name:  
binning_version_selection  
  
Workflow Context:  
Multiple binning packages exist and final selected version is needed.  
  
Active Role Agent:  
developer-agent  
Possible alternate: governance-agent if sign-off heavy  
  
Active Domain Skill:  
scorecard-domain  
  
Active Stage Skill:  
binning-version-selection  
  
Overlay Skills:  
- strict-governance-overlay if model fit must be blocked until approved  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- scorecardsdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- auditsdk  
- observabilitysdk  
- reporting_sdk  
  
UI Mode:  
candidate_comparison_workspace  
  
Interaction Mode:  
candidate_comparison_and_selection  
  
Expected Status Patterns:  
- pending_human_review  
- preview_ready  
- finalized  
- blocked  
- rerun_requested  
  
HITL Expectations:  
Usually mandatory.  
  
Main Inputs:  
- candidate binning versions  
- comparison metrics  
- monotonicity summary  
- support breach summary  
- policy flags  
  
Main Outputs:  
- selected_candidate_version_id  
- selection audit trail  
- optional composite version  
- next stage unlock  
  
--------------------------------------------------------------------  
4.4 FEATURE SHORTLIST REVIEW  
--------------------------------------------------------------------  
Stage Name:  
feature_shortlist_review  
  
Workflow Context:  
Review shortlisted variables before model fit.  
  
Active Role Agent:  
developer-agent  
  
Active Domain Skill:  
scorecard-domain  
  
Active Stage Skill:  
feature-shortlist-review  
  
Overlay Skills:  
- strict-governance-overlay if required  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- scorecardsdk  
- feature_sdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- observabilitysdk  
  
UI Mode:  
three_panel_review_workspace  
  
Interaction Mode:  
edit_and_finalize or review_and_approve  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- rerun_requested  
- valid_with_warning  
  
HITL Expectations:  
Often yes  
  
Main Inputs:  
- shortlisted variables  
- variable diagnostics  
- policy flags  
- feature lineage summary  
  
Main Outputs:  
- final feature list  
- rationale  
- selected feature artifact  
  
--------------------------------------------------------------------  
4.5 MODEL FITTING REVIEW  
--------------------------------------------------------------------  
Stage Name:  
model_fitting_review  
  
Workflow Context:  
Review candidate scorecard models after model fitting.  
  
Active Role Agent:  
developer-agent  
  
Active Domain Skill:  
scorecard-domain  
  
Active Stage Skill:  
model-fitting-review  
  
Overlay Skills:  
None or strict-governance-overlay if policy requires  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- scorecardsdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- observabilitysdk  
- reporting_sdk  
  
UI Mode:  
candidate_comparison_workspace  
  
Interaction Mode:  
candidate_comparison_and_selection  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- rerun_requested  
- success_with_warning  
  
HITL Expectations:  
Usually yes  
  
Main Inputs:  
- candidate model artifacts  
- performance metrics  
- diagnostics  
- stability metrics  
  
Main Outputs:  
- comparison summary  
- selected model candidate  
- rerun suggestion  
  
--------------------------------------------------------------------  
4.6 MODEL SELECTION  
--------------------------------------------------------------------  
Stage Name:  
model_selection  
  
Workflow Context:  
Finalize one candidate model for downstream validation or deployment  
preparation.  
  
Active Role Agent:  
developer-agent  
Possible alternate: governance-agent  
  
Active Domain Skill:  
scorecard-domain  
  
Active Stage Skill:  
model-selection  
  
Overlay Skills:  
- strict-governance-overlay  
- material-change-overlay if redevelopment  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- scorecardsdk  
- workflowsdk  
- hitlsdk  
- auditsdk  
- artifactsdk  
- observabilitysdk  
  
UI Mode:  
three_panel_review_workspace or candidate_comparison_workspace  
  
Interaction Mode:  
review_and_approve or candidate_comparison_and_selection  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- blocked  
  
HITL Expectations:  
Usually yes  
  
Main Inputs:  
- model candidates  
- comparison summary  
- policy conditions  
  
Main Outputs:  
- selected model ID  
- selection audit record  
- next stage unlock  
  
--------------------------------------------------------------------  
4.7 SCALING AND CALIBRATION REVIEW  
--------------------------------------------------------------------  
Stage Name:  
scaling_and_calibration_review  
  
Workflow Context:  
Review score scaling and/or calibration outputs before final package.  
  
Active Role Agent:  
developer-agent  
  
Active Domain Skill:  
scorecard-domain  
  
Active Stage Skill:  
scaling-and-calibration-review  
  
Overlay Skills:  
- strict-governance-overlay if required  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- scorecardsdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- reporting_sdk  
  
UI Mode:  
three_panel_review_workspace  
  
Interaction Mode:  
review_and_approve  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- valid_with_warning  
  
HITL Expectations:  
Often yes  
  
Main Inputs:  
- scaling outputs  
- calibration metrics  
- band definitions  
- policy thresholds  
  
Main Outputs:  
- final scaling package  
- calibration decision  
- warnings or conditions  
  
====================================================================  
5. VALIDATION WORKFLOW STAGES  
====================================================================  
  
--------------------------------------------------------------------  
5.1 VALIDATION SCOPE DEFINITION  
--------------------------------------------------------------------  
Stage Name:  
validation_scope_definition  
  
Workflow Context:  
Define what validation will review, required evidence, and expected  
deliverables.  
  
Active Role Agent:  
validator-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
validation-scope-definition  
  
Overlay Skills:  
- validation-pack-overlay  
- strict-governance-overlay if high sensitivity  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- validationsdk  
- policysdk  
- hitlsdk  
- workflowsdk  
- observabilitysdk  
- auditsdk  
- reporting_sdk  
  
UI Mode:  
validation_review_workspace  
  
Interaction Mode:  
review_and_approve  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- blocked  
  
HITL Expectations:  
Yes  
  
Main Inputs:  
- validation config pack  
- project metadata  
- model family  
- deployment scope  
  
Main Outputs:  
- validation scope record  
- required evidence checklist  
- scope approval  
  
--------------------------------------------------------------------  
5.2 EVIDENCE INTAKE REVIEW  
--------------------------------------------------------------------  
Stage Name:  
evidence_intake_review  
  
Workflow Context:  
Assess completeness and quality of supplied validation evidence.  
  
Active Role Agent:  
validator-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
evidence-intake-review  
  
Overlay Skills:  
- validation-pack-overlay  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- validationsdk  
- artifactsdk  
- knowledge_sdk  
- rag_sdk  
- hitlsdk  
- workflowsdk  
- observabilitysdk  
  
UI Mode:  
validation_review_workspace  
  
Interaction Mode:  
validation_challenge  
  
Expected Status Patterns:  
- pending_human_review  
- success  
- success_with_warning  
- blocked  
  
HITL Expectations:  
Usually yes  
  
Main Inputs:  
- evidence refs  
- manifest refs  
- required evidence classes  
  
Main Outputs:  
- evidence completeness summary  
- missing evidence list  
- findings if severe  
  
--------------------------------------------------------------------  
5.3 METHODOLOGY REVIEW  
--------------------------------------------------------------------  
Stage Name:  
methodology_review  
  
Workflow Context:  
Challenge conceptual design and methodological appropriateness.  
  
Active Role Agent:  
validator-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
methodology-review  
  
Overlay Skills:  
- validation-pack-overlay  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- validationsdk  
- evaluation_sdk  
- knowledge_sdk  
- rag_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- reporting_sdk  
  
UI Mode:  
validation_review_workspace  
  
Interaction Mode:  
validation_challenge  
  
Expected Status Patterns:  
- pending_human_review  
- success_with_warning  
- finalized  
- invalid_needs_review  
  
HITL Expectations:  
Yes  
  
Main Inputs:  
- methodology notes  
- selected model artifacts  
- benchmark patterns  
- prior challenge themes  
  
Main Outputs:  
- methodology findings  
- challenge notes  
- recommended follow-up  
  
--------------------------------------------------------------------  
5.4 DATA VALIDATION REVIEW  
--------------------------------------------------------------------  
Stage Name:  
data_validation_review  
  
Workflow Context:  
Challenge sample construction lineage and preparation assumptions.  
  
Active Role Agent:  
validator-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
data-validation-review  
  
Overlay Skills:  
- validation-pack-overlay  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- validationsdk  
- dataprepsdk  
- dataset_sdk  
- dq_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- reporting_sdk  
  
UI Mode:  
validation_review_workspace  
  
Interaction Mode:  
validation_challenge  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- blocked  
- invalid_needs_review  
  
HITL Expectations:  
Yes  
  
Main Inputs:  
- data prep manifest  
- dataset lineage  
- DQ outputs  
- split summary  
  
Main Outputs:  
- data findings  
- evidence gap notes  
- severity proposals  
  
--------------------------------------------------------------------  
5.5 MODEL FITNESS REVIEW  
--------------------------------------------------------------------  
Stage Name:  
model_fitness_review  
  
Workflow Context:  
Assess fit-for-use dimensions based on findings, evidence, and outputs.  
  
Active Role Agent:  
validator-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
model-fitness-review  
  
Overlay Skills:  
- validation-pack-overlay  
- strict-governance-overlay if sign-off is sensitive  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- validationsdk  
- evaluation_sdk  
- knowledge_sdk  
- rag_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- reporting_sdk  
  
UI Mode:  
validation_review_workspace  
  
Interaction Mode:  
review_and_conclude  
  
Expected Status Patterns:  
- pending_human_review  
- preview_ready  
- finalized  
- invalid_needs_review  
  
HITL Expectations:  
Yes  
  
Main Inputs:  
- findings  
- diagnostics  
- evidence completeness summary  
- fitness framework dimensions  
  
Main Outputs:  
- fitness matrix  
- draft conclusion categories  
- conditions if any  
  
--------------------------------------------------------------------  
5.6 VALIDATION CONCLUSION  
--------------------------------------------------------------------  
Stage Name:  
validation_conclusion  
  
Workflow Context:  
Finalize structured validation conclusion with conditions or required  
rework.  
  
Active Role Agent:  
validator-agent  
Possible alternate: approver-agent for final sign-off support  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
validation-conclusion  
  
Overlay Skills:  
- validation-pack-overlay  
- strict-governance-overlay  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- validationsdk  
- hitlsdk  
- auditsdk  
- policysdk  
- reporting_sdk  
- workflowsdk  
- observabilitysdk  
- artifactsdk  
  
UI Mode:  
validation_review_workspace  
  
Interaction Mode:  
review_and_conclude  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- blocked  
- escalated  
  
HITL Expectations:  
Always yes for final validator decision  
  
Main Inputs:  
- findings summary  
- fitness review  
- policy rules  
- proposed conditions  
  
Main Outputs:  
- final validation conclusion  
- conditions  
- approval records  
- linked validation artifact  
  
====================================================================  
6. DEPLOYMENT, GOVERNANCE, AND DOCUMENTATION STAGES  
====================================================================  
  
--------------------------------------------------------------------  
6.1 DEPLOYMENT READINESS  
--------------------------------------------------------------------  
Stage Name:  
deployment_readiness  
  
Workflow Context:  
Assess whether model is ready for deployment or implementation.  
  
Active Role Agent:  
governance-agent  
Possible alternate: approver-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
deployment-readiness  
  
Overlay Skills:  
- strict-governance-overlay  
- material-change-overlay if applicable  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- policysdk  
- hitlsdk  
- workflowsdk  
- auditsdk  
- artifactsdk  
- validationsdk  
- reporting_sdk  
- observabilitysdk  
  
UI Mode:  
three_panel_review_workspace  
  
Interaction Mode:  
review_and_approve  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- blocked  
- escalated  
  
HITL Expectations:  
Yes  
  
Main Inputs:  
- validation conclusion  
- unresolved issues  
- implementation evidence  
- approval rules  
  
Main Outputs:  
- deployment readiness decision  
- approval conditions  
- blockers  
- escalation payload  
  
--------------------------------------------------------------------  
6.2 COMMITTEE PACK PREPARATION  
--------------------------------------------------------------------  
Stage Name:  
committee_pack_preparation  
  
Workflow Context:  
Prepare governance-ready materials for committee consumption.  
  
Active Role Agent:  
documentation-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
committee-pack-preparation  
  
Overlay Skills:  
- committee-pack-overlay  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
  
SDK Allowlist:  
- reporting_sdk  
- artifactsdk  
- auditsdk  
- flowvizsdk  
- knowledge_sdk  
- rag_sdk  
  
UI Mode:  
documentation_workspace  
  
Interaction Mode:  
drafting_support  
  
Expected Status Patterns:  
- success  
- success_with_warning  
- blocked  
  
HITL Expectations:  
Usually no for drafting itself, yes for review/approval  
  
Main Inputs:  
- approved artifacts  
- decisions  
- findings  
- approved wording  
- governance format rules  
  
Main Outputs:  
- committee pack draft  
- governance summary blocks  
- linked evidence map  
  
--------------------------------------------------------------------  
6.3 DOCUMENTATION PACK PREPARATION  
--------------------------------------------------------------------  
Stage Name:  
documentation_pack_preparation  
  
Workflow Context:  
Prepare technical and audit-ready documentation packs.  
  
Active Role Agent:  
documentation-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
documentation-pack-preparation  
  
Overlay Skills:  
None or committee-pack-overlay if audience-specific  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
  
SDK Allowlist:  
- reporting_sdk  
- artifactsdk  
- dataset_sdk  
- knowledge_sdk  
- rag_sdk  
- flowvizsdk  
  
UI Mode:  
documentation_workspace  
  
Interaction Mode:  
drafting_support  
  
Expected Status Patterns:  
- success  
- success_with_warning  
- blocked  
  
HITL Expectations:  
Usually no for drafting itself  
  
Main Inputs:  
- manifests  
- lineage docs  
- decisions  
- validation outputs  
- selected wording blocks  
  
Main Outputs:  
- technical note draft  
- documentation artifacts  
- reproducibility appendix content  
  
====================================================================  
7. MONITORING AND ANNUAL REVIEW STAGES  
====================================================================  
  
--------------------------------------------------------------------  
7.1 MONITORING SNAPSHOT INGESTION  
--------------------------------------------------------------------  
Stage Name:  
monitoring_snapshot_ingestion  
  
Workflow Context:  
A new production monitoring snapshot arrives.  
  
Active Role Agent:  
monitoring-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
monitoring-snapshot-ingestion  
  
Overlay Skills:  
- annual-review-overlay if annual-review context  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
  
SDK Allowlist:  
- monitoringsdk  
- dataset_sdk  
- dq_sdk  
- artifactsdk  
- observabilitysdk  
- workflowsdk  
  
UI Mode:  
dashboard_review_workspace or standard_chat_plus_context  
  
Interaction Mode:  
routing_only  
  
Expected Status Patterns:  
- success  
- success_with_warning  
- failed  
- invalid_input  
  
HITL Expectations:  
Usually no  
  
Main Inputs:  
- current monitoring snapshot  
- monitoring template  
- baseline refs  
  
Main Outputs:  
- validated snapshot record  
- ingestion summary  
- dashboard refresh trigger  
  
--------------------------------------------------------------------  
7.2 MONITORING METRIC GENERATION  
--------------------------------------------------------------------  
Stage Name:  
monitoring_metric_generation  
  
Workflow Context:  
Refresh metrics and dashboard after snapshot ingestion.  
  
Active Role Agent:  
monitoring-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
monitoring-metric-generation  
  
Overlay Skills:  
- annual-review-overlay if needed  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
  
SDK Allowlist:  
- monitoringsdk  
- evaluation_sdk  
- artifactsdk  
- reporting_sdk  
- observabilitysdk  
  
UI Mode:  
dashboard_review_workspace  
  
Interaction Mode:  
monitoring_dashboard_review  
  
Expected Status Patterns:  
- success  
- success_with_warning  
- failed  
  
HITL Expectations:  
No for computation; yes later if breach review needed  
  
Main Inputs:  
- current snapshot  
- prior history  
- threshold config  
  
Main Outputs:  
- KPI tables  
- drift tables  
- dashboard payload  
- breach flags  
  
--------------------------------------------------------------------  
7.3 MONITORING BREACH REVIEW  
--------------------------------------------------------------------  
Stage Name:  
monitoring_breach_review  
  
Workflow Context:  
One or more monitoring thresholds are breached and require review.  
  
Active Role Agent:  
monitoring-agent  
Possible alternate: governance-agent for severe breaches  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
monitoring-breach-review  
  
Overlay Skills:  
- strict-governance-overlay if severe  
- annual-review-overlay if annual review  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- monitoringsdk  
- policysdk  
- hitlsdk  
- auditsdk  
- reporting_sdk  
- workflowsdk  
- observabilitysdk  
  
UI Mode:  
dashboard_review_workspace  
  
Interaction Mode:  
triage_and_disposition  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- escalated  
- blocked  
  
HITL Expectations:  
Yes  
  
Main Inputs:  
- breach table  
- history trends  
- baseline comparison  
- action log  
  
Main Outputs:  
- breach disposition  
- action assignment  
- escalation record if needed  
  
--------------------------------------------------------------------  
7.4 ANNUAL REVIEW OUTCOME  
--------------------------------------------------------------------  
Stage Name:  
annual_review_outcome  
  
Workflow Context:  
Prepare annual review summary and determine follow-up actions.  
  
Active Role Agent:  
monitoring-agent  
Possible alternate: governance-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
annual-review-outcome  
  
Overlay Skills:  
- annual-review-overlay  
- strict-governance-overlay if high sensitivity  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- monitoringsdk  
- reporting_sdk  
- flowvizsdk  
- knowledge_sdk  
- rag_sdk  
- hitlsdk  
- workflowsdk  
- auditsdk  
  
UI Mode:  
dashboard_review_workspace or three_panel_review_workspace  
  
Interaction Mode:  
review_and_approve  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- escalated  
- success_with_warning  
  
HITL Expectations:  
Yes  
  
Main Inputs:  
- annual monitoring pack  
- unresolved issues  
- breach history  
- action history  
  
Main Outputs:  
- annual review summary  
- next action recommendation  
- remediation request or closure view  
  
====================================================================  
8. REMEDIATION AND ISSUE CLOSURE STAGES  
====================================================================  
  
--------------------------------------------------------------------  
8.1 REMEDIATION PLANNING  
--------------------------------------------------------------------  
Stage Name:  
remediation_planning  
  
Workflow Context:  
Open issues or findings require action planning.  
  
Active Role Agent:  
remediation-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
issue-remediation-planner  
  
Overlay Skills:  
- remediation-overlay  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- validationsdk  
- auditsdk  
- workflowsdk  
- hitlsdk  
- reporting_sdk  
- knowledge_sdk  
  
UI Mode:  
three_panel_review_workspace  
  
Interaction Mode:  
review_and_approve  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- blocked  
  
HITL Expectations:  
Yes  
  
Main Inputs:  
- findings  
- breach outcomes  
- due dates  
- owners  
- closure criteria  
  
Main Outputs:  
- remediation plan  
- action assignments  
- due dates  
  
--------------------------------------------------------------------  
8.2 REMEDIATION CLOSURE REVIEW  
--------------------------------------------------------------------  
Stage Name:  
remediation_closure  
  
Workflow Context:  
Review evidence to determine if remediation can be closed.  
  
Active Role Agent:  
remediation-agent  
Possible alternate: validator-agent  
  
Active Domain Skill:  
Relevant domain skill  
  
Active Stage Skill:  
remediation-closure  
  
Overlay Skills:  
- remediation-overlay  
- validation-pack-overlay if linked to validation closure  
  
Always-Active Base Skills:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- interaction-orchestrator  
  
SDK Allowlist:  
- validationsdk  
- auditsdk  
- artifactsdk  
- hitlsdk  
- workflowsdk  
- reporting_sdk  
- observabilitysdk  
  
UI Mode:  
three_panel_review_workspace  
  
Interaction Mode:  
review_and_conclude  
  
Expected Status Patterns:  
- pending_human_review  
- finalized  
- blocked  
- escalated  
  
HITL Expectations:  
Yes  
  
Main Inputs:  
- closure evidence  
- prior finding  
- action history  
- closure criteria  
  
Main Outputs:  
- closure recommendation  
- reopen decision if needed  
- closure audit record  
  
====================================================================  
9. DOMAIN-SPECIFIC EXTENSION RUNTIME STACKS  
====================================================================  
  
--------------------------------------------------------------------  
9.1 TIME SERIES MODEL REVIEW  
--------------------------------------------------------------------  
Stage Name:  
timeseries_model_review  
  
Active Role Agent:  
developer-agent or validator-agent  
  
Active Domain Skill:  
timeseries-domain  
  
Active Stage Skill:  
model-fitting-review or methodology-review depending context  
  
Overlay Skills:  
- validation-pack-overlay if validation  
- strict-governance-overlay if approval stage  
  
SDK Allowlist:  
- timeseriessdk  
- dataprepsdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- reporting_sdk  
- knowledge_sdk  
- rag_sdk  
  
UI Mode:  
candidate_comparison_workspace or validation_review_workspace  
  
Interaction Mode:  
candidate_comparison_and_selection or validation_challenge  
  
--------------------------------------------------------------------  
9.2 LGD MODEL REVIEW  
--------------------------------------------------------------------  
Stage Name:  
lgd_model_review  
  
Active Role Agent:  
developer-agent or validator-agent  
  
Active Domain Skill:  
lgd-domain  
  
Active Stage Skill:  
model-fitting-review or methodology-review  
  
Overlay Skills:  
- validation-pack-overlay if validation  
  
SDK Allowlist:  
- lgdsdk  
- dataprepsdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- reporting_sdk  
  
UI Mode:  
candidate_comparison_workspace or validation_review_workspace  
  
Interaction Mode:  
candidate_comparison_and_selection or validation_challenge  
  
--------------------------------------------------------------------  
9.3 PD MODEL REVIEW  
--------------------------------------------------------------------  
Stage Name:  
pd_model_review  
  
Active Role Agent:  
developer-agent or validator-agent  
  
Active Domain Skill:  
pd-domain  
  
Active Stage Skill:  
model-fitting-review or methodology-review  
  
Overlay Skills:  
- validation-pack-overlay if needed  
  
SDK Allowlist:  
- pdsdk  
- dataprepsdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- reporting_sdk  
  
UI Mode:  
candidate_comparison_workspace or validation_review_workspace  
  
Interaction Mode:  
candidate_comparison_and_selection or validation_challenge  
  
--------------------------------------------------------------------  
9.4 EAD MODEL REVIEW  
--------------------------------------------------------------------  
Stage Name:  
ead_model_review  
  
Active Role Agent:  
developer-agent or validator-agent  
  
Active Domain Skill:  
ead-domain  
  
Active Stage Skill:  
model-fitting-review or methodology-review  
  
Overlay Skills:  
- validation-pack-overlay if needed  
  
SDK Allowlist:  
- eadsdk  
- dataprepsdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- reporting_sdk  
  
UI Mode:  
candidate_comparison_workspace or validation_review_workspace  
  
Interaction Mode:  
candidate_comparison_and_selection or validation_challenge  
  
--------------------------------------------------------------------  
9.5 ECL WORKFLOW REVIEW  
--------------------------------------------------------------------  
Stage Name:  
ecl_workflow_review  
  
Active Role Agent:  
developer-agent or validator-agent  
  
Active Domain Skill:  
ecl-domain  
  
Active Stage Skill:  
methodology-review or model-selection or validation-conclusion  
depending substage  
  
Overlay Skills:  
- validation-pack-overlay  
- material-change-overlay if redevelopment  
- strict-governance-overlay if approval-sensitive  
  
SDK Allowlist:  
- eclsdk  
- pdsdk  
- lgdsdk  
- eadsdk  
- dataprepsdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- reporting_sdk  
- knowledge_sdk  
- rag_sdk  
  
UI Mode:  
validation_review_workspace or three_panel_review_workspace  
  
Interaction Mode:  
validation_challenge or review_and_approve  
  
--------------------------------------------------------------------  
9.6 SICR WORKFLOW REVIEW  
--------------------------------------------------------------------  
Stage Name:  
sicr_workflow_review  
  
Active Role Agent:  
developer-agent or validator-agent  
  
Active Domain Skill:  
sicr-domain  
  
Active Stage Skill:  
methodology-review or model-selection  
  
Overlay Skills:  
- validation-pack-overlay if needed  
  
SDK Allowlist:  
- sicr_sdk  
- dataprepsdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- reporting_sdk  
  
UI Mode:  
validation_review_workspace or candidate_comparison_workspace  
  
Interaction Mode:  
validation_challenge or candidate_comparison_and_selection  
  
--------------------------------------------------------------------  
9.7 STRESS TESTING WORKFLOW REVIEW  
--------------------------------------------------------------------  
Stage Name:  
stress_workflow_review  
  
Active Role Agent:  
developer-agent or validator-agent or governance-agent  
  
Active Domain Skill:  
stress-domain  
  
Active Stage Skill:  
model-fitting-review or methodology-review or deployment-readiness  
depending substage  
  
Overlay Skills:  
- validation-pack-overlay  
- strict-governance-overlay  
  
SDK Allowlist:  
- stresssdk  
- dataprepsdk  
- evaluation_sdk  
- hitlsdk  
- workflowsdk  
- artifactsdk  
- reporting_sdk  
- knowledge_sdk  
- rag_sdk  
  
UI Mode:  
candidate_comparison_workspace or validation_review_workspace  
  
Interaction Mode:  
candidate_comparison_and_selection or validation_challenge  
  
====================================================================  
10. RUNTIME STACK RESOLUTION BY ROLE MODE  
====================================================================  
  
--------------------------------------------------------------------  
10.1 DEVELOPER MODE  
--------------------------------------------------------------------  
Standard runtime stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- developer-agent  
- active-domain-skill  
- active-stage-skill  
- optional overlay(s)  
  
Typical UI:  
- standard_chat_plus_context  
- three_panel_review_workspace  
- candidate_comparison_workspace  
  
Typical SDK allowlist:  
- workflowsdk  
- hitlsdk if review stage  
- observabilitysdk  
- auditsdk  
- artifactsdk  
- dataprepsdk if needed  
- evaluation_sdk  
- feature_sdk  
- relevant domain SDK  
- reporting_sdk if pack generation  
- jupyter_bridge  
- widgetsdk if workspace active  
  
--------------------------------------------------------------------  
10.2 VALIDATOR MODE  
--------------------------------------------------------------------  
Standard runtime stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- validator-agent  
- active-domain-skill  
- active-validation-stage-skill  
- validation-pack-overlay  
- optional strict-governance-overlay  
  
Typical UI:  
- validation_review_workspace  
- three_panel_review_workspace  
  
Typical SDK allowlist:  
- workflowsdk  
- hitlsdk  
- observabilitysdk  
- auditsdk  
- artifactsdk  
- validationsdk  
- policysdk  
- evaluation_sdk  
- reporting_sdk  
- knowledge_sdk  
- rag_sdk  
- jupyter_bridge  
- widgetsdk  
  
--------------------------------------------------------------------  
10.3 GOVERNANCE MODE  
--------------------------------------------------------------------  
Standard runtime stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- governance-agent  
- active-domain-skill  
- active-stage-skill  
- strict-governance-overlay  
  
Typical UI:  
- three_panel_review_workspace  
- documentation_workspace  
- flow_explorer_workspace  
  
Typical SDK allowlist:  
- workflowsdk  
- hitlsdk  
- observabilitysdk  
- auditsdk  
- artifactsdk  
- policysdk  
- reporting_sdk  
- flowvizsdk  
- jupyter_bridge  
- widgetsdk  
  
--------------------------------------------------------------------  
10.4 DOCUMENTATION MODE  
--------------------------------------------------------------------  
Standard runtime stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- documentation-agent  
- active-domain-skill  
- active-stage-skill  
- optional committee-pack-overlay  
  
Typical UI:  
- documentation_workspace  
  
Typical SDK allowlist:  
- reporting_sdk  
- artifactsdk  
- auditsdk  
- flowvizsdk  
- knowledge_sdk  
- rag_sdk  
  
--------------------------------------------------------------------  
10.5 MONITORING MODE  
--------------------------------------------------------------------  
Standard runtime stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- monitoring-agent  
- active-domain-skill  
- active-stage-skill  
- annual-review-overlay if annual mode  
  
Typical UI:  
- dashboard_review_workspace  
- three_panel_review_workspace for breaches  
  
Typical SDK allowlist:  
- monitoringsdk  
- evaluation_sdk  
- reporting_sdk  
- policysdk  
- artifactsdk  
- observabilitysdk  
- auditsdk  
- knowledge_sdk  
- rag_sdk  
- widgetsdk  
- jupyter_bridge  
  
--------------------------------------------------------------------  
10.6 REMEDIATION MODE  
--------------------------------------------------------------------  
Standard runtime stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- remediation-agent  
- active-domain-skill  
- active-stage-skill  
- remediation-overlay  
  
Typical UI:  
- three_panel_review_workspace  
  
Typical SDK allowlist:  
- validationsdk  
- monitoringsdk if source from monitoring breach  
- auditsdk  
- workflowsdk  
- hitlsdk  
- artifactsdk  
- reporting_sdk  
- widgetsdk  
- jupyter_bridge  
  
====================================================================  
11. UI ENTRY POINT TO RUNTIME STACK MAPPING  
====================================================================  
  
--------------------------------------------------------------------  
11.1 CODEBUDDY CHAT ENTRY  
--------------------------------------------------------------------  
Entry Point:  
right-sidebar CodeBuddy chat  
  
Typical purpose:  
- ask for explanation  
- ask for alternative  
- open governed review  
- request status  
- request draft summary  
  
Runtime rule:  
Use compact context pack only.  
Escalate to workspace when structured editing or approval is needed.  
  
Likely UI mode:  
- standard_chat_plus_context  
  
Likely interaction mode:  
- routing_only  
- drafting_support  
- chat_assisted_guidance  
  
--------------------------------------------------------------------  
11.2 MAIN-AREA REVIEW WORKSPACE ENTRY  
--------------------------------------------------------------------  
Entry Point:  
main-area governed workspace  
  
Typical purpose:  
- structured edits  
- candidate selection  
- validation findings review  
- conclusion approval  
- breach disposition  
  
Runtime rule:  
Activate interaction-orchestrator and widgetsdk.  
Prefer explicit review payloads and bounded actions.  
  
Likely UI mode:  
- three_panel_review_workspace  
- candidate_comparison_workspace  
- validation_review_workspace  
- dashboard_review_workspace  
  
--------------------------------------------------------------------  
11.3 DOWN-AREA LOG / PREVIEW ENTRY  
--------------------------------------------------------------------  
Entry Point:  
bottom/down area  
  
Typical purpose:  
- event trace  
- warnings  
- preview history  
- execution history  
  
Runtime rule:  
Mostly read-only.  
Should not trigger heavy semantic retrieval by default.  
  
Likely UI mode:  
- flow_explorer_workspace  
- detail_panels  
  
====================================================================  
12. COMPREHENSIVE STAGE-TO-STACK SUMMARY TABLE  
====================================================================  
  
Stage,Role Agent,Domain Skill,Stage Skill,Overlay(s),Primary SDK Allowlist,UI Mode,Interaction Mode,HITL?  
session_start,session-bootstrap-orchestrator,None,session-bootstrap-orchestrator,None,config_sdk; registry_sdk; workflowsdk; observabilitysdk; auditsdk,bootstrap_workspace,routing_only,Yes  
resume_or_recovery_entry,recovery-orchestrator,prior domain,recovery-orchestrator,remediation-overlay optional,workflowsdk; observabilitysdk; auditsdk; artifactsdk; policysdk,recovery_workspace,recovery_decision,Yes  
data_preparation,developer-agent,relevant domain,data-preparation-execution,None,dataprepsdk; dataset_sdk; dq_sdk; artifactsdk; observabilitysdk,standard_chat_plus_context,routing_only,Optional  
data_readiness_review,developer-agent or reviewer-agent,relevant domain,data-readiness-review,strict-governance-overlay optional,dataprepsdk; dataset_sdk; dq_sdk; hitlsdk; workflowsdk; reporting_sdk,three_panel_review_workspace,review_and_approve,Yes  
fine_classing,developer-agent,scorecard-domain,fine-classing-execution,None,scorecardsdk; evaluation_sdk; artifactsdk; observabilitysdk,standard_chat_plus_context,routing_only,No  
coarse_classing_review,developer-agent,scorecard-domain,coarse-classing-review,strict-governance-overlay optional,scorecardsdk; evaluation_sdk; hitlsdk; workflowsdk; artifactsdk; auditsdk,three_panel_review_workspace,edit_and_finalize,Yes  
binning_version_selection,developer-agent,scorecard-domain,binning-version-selection,strict-governance-overlay optional,scorecardsdk; evaluation_sdk; hitlsdk; workflowsdk; artifactsdk; auditsdk,candidate_comparison_workspace,candidate_comparison_and_selection,Yes  
feature_shortlist_review,developer-agent,scorecard-domain,feature-shortlist-review,strict-governance-overlay optional,scorecardsdk; feature_sdk; evaluation_sdk; hitlsdk; workflowsdk,three_panel_review_workspace,edit_and_finalize,Yes  
model_fitting_review,developer-agent,relevant domain,model-fitting-review,None,relevant domain SDK; evaluation_sdk; hitlsdk; workflowsdk; artifactsdk,candidate_comparison_workspace,candidate_comparison_and_selection,Yes  
model_selection,developer-agent or governance-agent,relevant domain,model-selection,strict-governance-overlay,relevant domain SDK; workflowsdk; hitlsdk; auditsdk; artifactsdk,three_panel_review_workspace,review_and_approve,Yes  
scaling_and_calibration_review,developer-agent,scorecard-domain,scaling-and-calibration-review,strict-governance-overlay optional,scorecardsdk; evaluation_sdk; hitlsdk; workflowsdk; artifactsdk,three_panel_review_workspace,review_and_approve,Yes  
validation_scope_definition,validator-agent,relevant domain,validation-scope-definition,validation-pack-overlay,validationsdk; policysdk; hitlsdk; workflowsdk,validation_review_workspace,review_and_approve,Yes  
evidence_intake_review,validator-agent,relevant domain,evidence-intake-review,validation-pack-overlay,validationsdk; artifactsdk; knowledge_sdk; rag_sdk; hitlsdk,validation_review_workspace,validation_challenge,Yes  
methodology_review,validator-agent,relevant domain,methodology-review,validation-pack-overlay,validationsdk; evaluation_sdk; knowledge_sdk; rag_sdk; hitlsdk,validation_review_workspace,validation_challenge,Yes  
data_validation_review,validator-agent,relevant domain,data-validation-review,validation-pack-overlay,validationsdk; dataprepsdk; dataset_sdk; dq_sdk; hitlsdk,validation_review_workspace,validation_challenge,Yes  
model_fitness_review,validator-agent,relevant domain,model-fitness-review,validation-pack-overlay; strict-governance-overlay optional,validationsdk; evaluation_sdk; knowledge_sdk; rag_sdk; hitlsdk,validation_review_workspace,review_and_conclude,Yes  
validation_conclusion,validator-agent,relevant domain,validation-conclusion,validation-pack-overlay; strict-governance-overlay,validationsdk; hitlsdk; auditsdk; policysdk; reporting_sdk,validation_review_workspace,review_and_conclude,Yes  
deployment_readiness,governance-agent,relevant domain,deployment-readiness,strict-governance-overlay; material-change-overlay optional,policysdk; hitlsdk; workflowsdk; auditsdk; validationsdk; reporting_sdk,three_panel_review_workspace,review_and_approve,Yes  
committee_pack_preparation,documentation-agent,relevant domain,committee-pack-preparation,committee-pack-overlay,reporting_sdk; artifactsdk; auditsdk; flowvizsdk; knowledge_sdk; rag_sdk,documentation_workspace,drafting_support,No  
documentation_pack_preparation,documentation-agent,relevant domain,documentation-pack-preparation,None,reporting_sdk; artifactsdk; dataset_sdk; knowledge_sdk; rag_sdk,documentation_workspace,drafting_support,No  
monitoring_snapshot_ingestion,monitoring-agent,relevant domain,monitoring-snapshot-ingestion,annual-review-overlay optional,monitoringsdk; dataset_sdk; dq_sdk; artifactsdk,standard_chat_plus_context,routing_only,No  
monitoring_metric_generation,monitoring-agent,relevant domain,monitoring-metric-generation,annual-review-overlay optional,monitoringsdk; evaluation_sdk; reporting_sdk; artifactsdk,dashboard_review_workspace,monitoring_dashboard_review,No  
monitoring_breach_review,monitoring-agent or governance-agent,relevant domain,monitoring-breach-review,strict-governance-overlay optional; annual-review-overlay optional,monitoringsdk; policysdk; hitlsdk; auditsdk; reporting_sdk,dashboard_review_workspace,triage_and_disposition,Yes  
annual_review_outcome,monitoring-agent or governance-agent,relevant domain,annual-review-outcome,annual-review-overlay; strict-governance-overlay optional,monitoringsdk; reporting_sdk; flowvizsdk; knowledge_sdk; rag_sdk; hitlsdk,dashboard_review_workspace,review_and_approve,Yes  
remediation_planning,remediation-agent,relevant domain,issue-remediation-planner,remediation-overlay,validationsdk; auditsdk; hitlsdk; workflowsdk; reporting_sdk,three_panel_review_workspace,review_and_approve,Yes  
remediation_closure,remediation-agent or validator-agent,relevant domain,remediation-closure,remediation-overlay; validation-pack-overlay optional,validationsdk; auditsdk; artifactsdk; hitlsdk; workflowsdk,three_panel_review_workspace,review_and_conclude,Yes  
  
====================================================================  
13. DESIGN RECOMMENDATIONS  
====================================================================  
  
13.1 Do Not Use One Flat Runtime Prompt  
--------------------------------------------------------------------  
The runtime should resolve only the active stack:  
- base rules  
- orchestrator  
- one role  
- one domain  
- one stage  
- zero to two overlays  
- compact runtime context  
  
13.2 Prefer UI Mode Switching Over Prompt Expansion  
--------------------------------------------------------------------  
When interaction becomes structured:  
- open workspace  
- keep chat compact  
- move heavy review detail into UI and artifacts  
- send compact state back to LLM  
  
13.3 Use Stage-Specific SDK Allowlists  
--------------------------------------------------------------------  
Do not expose all SDKs at every stage.  
Keep the allowlist narrow.  
  
13.4 Use Token-Thrifty Context Packs  
--------------------------------------------------------------------  
For each stage, pass:  
- exact state facts  
- top summaries  
- selected artifact refs  
- active warnings  
Do not replay full history unless deep review is justified.  
  
13.5 Keep HITL State Outside Chat  
--------------------------------------------------------------------  
Review state, selected version state, finding state, and approval  
state must live in workflow state and registries, not chat history.  
  
====================================================================  
14. SUCCESS CRITERIA  
====================================================================  
  
The runtime resolution model shall be considered successful when:  
  
1. each workflow stage activates a precise, minimal, and appropriate  
   stack  
2. the right role, domain, and stage behavior are consistently loaded  
3. SDK access is constrained by stage need  
4. UI mode matches the interaction complexity  
5. HITL is invoked only where required but never bypassed silently  
6. workflow state remains the source of truth  
7. token usage remains controlled through compact context packs  
8. developers, validators, governance users, and monitoring users all  
   experience a coherent but role-appropriate system behavior  
  
====================================================================  
END OF RUNTIME RESOLUTION MASTER MATRIX  
====================================================================  
