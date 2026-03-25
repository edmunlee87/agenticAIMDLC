# UX URD  
  
====================================================================  
USER REQUIREMENT DOCUMENT (URD)  
GENERALIZED HUMAN-IN-THE-LOOP INTERACTION FRAMEWORK  
FOR ENTERPRISE AGENTIC AI WORKFLOW PLATFORM  
====================================================================  
  
Project Name : HITL Interaction Framework  
Version      : 1.0  
Date         : 2026-03-15  
Prepared For : Model Development, Model Validation, Governance,  
               Audit, Technology, Portfolio Analytics, Risk Methodology  
  
====================================================================  
1. PURPOSE  
====================================================================  
  
This document defines the requirements for a generalized interaction  
framework that allows users to review, refine, approve, reject, edit,  
rerun, or escalate agent-generated outputs across all supported use  
cases.  
  
The framework shall be reusable across:  
- credit scoring  
- time series modeling  
- ECL workflows  
- LGD workflows  
- PD / EAD workflows  
- SICR workflows  
- stress testing  
- monitoring and annual review  
- model validation  
- documentation and governance packs  
- future domain packs  
  
The purpose is to provide a unified, governed, user-friendly, and  
agent-compatible interaction pattern that supports human-in-the-loop  
decision making and seamless handoff back to the agent / SDK layer.  
  
====================================================================  
2. OBJECTIVES  
====================================================================  
  
The interaction framework shall:  
  
1. Present agent outputs in a clear and structured way.  
2. Let users accept, refine, override, or reject proposed results.  
3. Allow structured editing instead of relying only on free text.  
4. Return user choices back to the agent seamlessly.  
5. Support preview and recalculation before finalization.  
6. Preserve observability, auditability, and lineage.  
7. Generalize across many use cases without redesigning the UI shell.  
8. Remain compatible with notebook UI, future web UI, CLI, and API.  
9. Support both development and validation roles.  
10. Support future-proof, modular extension.  
  
====================================================================  
3. DESIGN PRINCIPLES  
====================================================================  
  
The interaction framework shall follow these principles:  
  
3.1 Structured over unstructured  
--------------------------------------------------------------------  
User interaction should be captured through structured fields,  
controls, selections, and edits whenever possible.  
  
3.2 Review workspace over popup approval  
--------------------------------------------------------------------  
The preferred pattern is an interactive review workspace rather than  
a simple yes/no prompt.  
  
3.3 Preview before finalization  
--------------------------------------------------------------------  
Where changes affect metrics or artifacts, the user should be able to  
preview updated results before finalizing.  
  
3.4 Human accountable judgement  
--------------------------------------------------------------------  
The framework supports and records human judgement. It does not hide  
the final human decision behind automation.  
  
3.5 Agent-assisted, not agent-imposed  
--------------------------------------------------------------------  
The agent may recommend actions and help interpret results, but the  
user must be able to review and refine outputs.  
  
3.6 Reusable shell, domain-specific content  
--------------------------------------------------------------------  
The same interaction shell shall be reusable across domains, while  
the content inside the shell may vary by use case.  
  
3.7 Full traceability  
--------------------------------------------------------------------  
Every interaction shall be linkable to a project, run, stage, user,  
artifact, review, and event trail.  
  
====================================================================  
4. SCOPE OF INTERACTIONS  
====================================================================  
  
The framework shall support interaction patterns such as:  
  
- review and approve  
- review and approve with edits  
- reject and rerun  
- compare candidates  
- choose final version  
- create composite version  
- edit parameters  
- provide rationale  
- escalate to reviewer / approver  
- ask agent to optimize again  
- ask agent to compare alternatives  
- request more evidence  
- confirm validation findings  
- confirm validation conclusions  
- review remediation status  
- confirm deployment readiness  
- confirm monitoring breach disposition  
  
====================================================================  
5. GENERALIZED INTERACTION MODEL  
====================================================================  
  
The platform shall support a common interaction model consisting of:  
  
5.1 Agent Proposal  
--------------------------------------------------------------------  
The agent provides an initial proposed result, recommendation, or  
candidate set.  
  
Examples:  
- proposed coarse bins  
- proposed final selected version  
- recommended model choice  
- suggested validation conclusion  
- suggested remediation severity  
- recommended deployment decision  
  
5.2 User Review  
--------------------------------------------------------------------  
The user inspects evidence, summaries, metrics, charts, warnings,  
alternatives, and proposed actions.  
  
5.3 User Refinement  
--------------------------------------------------------------------  
The user may:  
- accept without change  
- edit the result  
- choose another candidate  
- request rerun with parameters  
- escalate  
- reject  
  
5.4 Agent Validation / Recompute  
--------------------------------------------------------------------  
After user edits, the system revalidates the edited result and may:  
- recompute metrics  
- rerun checks  
- refresh warnings  
- generate updated artifacts  
- request confirmation if edits introduce issues  
  
5.5 Finalization  
--------------------------------------------------------------------  
The user confirms final action, and the platform records:  
- final accepted output  
- edit history  
- user rationale  
- resulting artifacts  
- event log  
- audit trail  
- next workflow state  
  
====================================================================  
6. STANDARD INTERACTION STATES  
====================================================================  
  
The platform shall support standard interaction states including:  
  
- initialized  
- proposed  
- under_review  
- user_editing  
- preview_generated  
- waiting_for_confirmation  
- accepted  
- accepted_with_edits  
- rejected  
- rerun_requested  
- escalated  
- blocked  
- finalized  
- superseded  
  
These states shall be reusable across all interaction types.  
  
====================================================================  
7. STANDARD INTERACTION TYPES  
====================================================================  
  
The framework shall support reusable interaction types such as:  
  
7.1 Approval Interaction  
--------------------------------------------------------------------  
Purpose:  
User approves or rejects a proposed result.  
  
Examples:  
- approve model choice  
- approve deployment readiness  
- approve validation conclusion  
  
7.2 Edit-and-Finalize Interaction  
--------------------------------------------------------------------  
Purpose:  
User directly edits a proposed output and then finalizes it.  
  
Examples:  
- coarse classing edits  
- score band adjustments  
- threshold tuning  
- validation issue wording updates  
  
7.3 Candidate Comparison Interaction  
--------------------------------------------------------------------  
Purpose:  
User compares multiple alternatives and chooses one.  
  
Examples:  
- compare binning versions  
- compare challenger models  
- compare overlay options  
- compare forecast models  
  
7.4 Composite Selection Interaction  
--------------------------------------------------------------------  
Purpose:  
User selects parts from multiple proposals to form a final result.  
  
Examples:  
- create final composite binning version  
- create combined feature shortlist  
- create combined remediation plan  
  
7.5 Escalation Interaction  
--------------------------------------------------------------------  
Purpose:  
User escalates the decision to another reviewer or approver.  
  
Examples:  
- policy-sensitive variable acceptance  
- high-risk validation finding  
- critical deployment block  
  
7.6 Validation Challenge Interaction  
--------------------------------------------------------------------  
Purpose:  
User records findings, severity, model fitness opinion, or required  
remediation.  
  
Examples:  
- mark finding severity  
- accept or revise model fitness summary  
- confirm validation conclusion  
  
====================================================================  
8. GENERALIZED 3-PANEL INTERACTION DESIGN  
====================================================================  
  
The default recommended interaction layout shall be a 3-panel review  
workspace.  
  
8.1 Panel A – Proposal and Evidence  
--------------------------------------------------------------------  
Purpose:  
Show what the agent proposes and why.  
  
Typical contents:  
- title  
- context summary  
- recommendation  
- business summary  
- technical summary  
- evidence table  
- metrics  
- diagnostics  
- charts  
- warnings  
- policy findings  
- candidate comparison snapshot  
- linked artifacts  
  
Examples:  
- proposed coarse bins and WoE trend  
- proposed model comparison metrics  
- proposed validation conclusion with supporting evidence  
  
8.2 Panel B – User Refinement Workspace  
--------------------------------------------------------------------  
Purpose:  
Allow the user to refine or configure the result in a structured way.  
  
Typical contents:  
- editable tables  
- candidate selector  
- merge / split controls  
- toggles  
- text inputs for rationale  
- parameter overrides  
- structured adjustment controls  
- evidence inclusion toggles  
- severity / conclusion dropdowns  
  
Examples:  
- edit final bins  
- choose one candidate version  
- adjust selected variables  
- mark validation finding severity  
- edit remediation condition  
  
8.3 Panel C – Actions, Status, and Feedback  
--------------------------------------------------------------------  
Purpose:  
Provide workflow controls, preview results, and execution status.  
  
Typical contents:  
- preview button  
- accept button  
- accept with edits button  
- reject button  
- rerun button  
- escalate button  
- status box  
- warnings box  
- backend response summary  
- audit / event reference  
- next step indicator  
  
====================================================================  
9. INTERACTION ACTION MODEL  
====================================================================  
  
The framework shall support two action classes.  
  
9.1 Soft Actions  
--------------------------------------------------------------------  
Soft actions do not finalize the decision.  
  
Supported examples:  
- preview_changes  
- compare_candidates  
- ask_agent_to_optimize_again  
- ask_for_more_analysis  
- refresh_metrics  
- show_more_evidence  
  
9.2 Final Actions  
--------------------------------------------------------------------  
Final actions produce workflow consequences.  
  
Supported examples:  
- accept  
- accept_with_edits  
- approve_version  
- approve_version_with_overrides  
- create_composite_version  
- reject_and_rerun  
- escalate  
- finalize_validation_conclusion  
- finalize_remediation_action  
  
====================================================================  
10. STANDARD USER INPUT MODEL  
====================================================================  
  
The framework shall support three classes of user input.  
  
10.1 Structured Selection Input  
--------------------------------------------------------------------  
Examples:  
- chosen candidate version  
- selected action  
- selected severity  
- selected conclusion category  
- selected deployment option  
  
10.2 Structured Editing Input  
--------------------------------------------------------------------  
Examples:  
- edited bin group definitions  
- modified parameters  
- selected variable set  
- updated issue fields  
- threshold overrides  
  
10.3 Narrative Input  
--------------------------------------------------------------------  
Examples:  
- reviewer comments  
- rationale  
- challenge notes  
- acceptance notes  
- escalation justification  
  
Narrative input should supplement, not replace, structured input.  
  
====================================================================  
11. STANDARD PAYLOAD CONTRACT FROM UI TO AGENT  
====================================================================  
  
All interaction UIs shall submit a structured payload to the backend  
controller / agent runner.  
  
Minimum shared payload:  
- project_id  
- run_id  
- session_id  
- review_id or interaction_id  
- stage_name  
- interaction_type  
- action  
- actor_id  
- actor_role  
- structured_edits  
- selected_candidate_version_id if applicable  
- user_comment  
- timestamp  
  
Example generalized payload:  
{  
  "project_id": "proj_001",  
  "run_id": "run_001",  
  "session_id": "sess_001",  
  "review_id": "rev_010",  
  "stage_name": "coarse_classing_review",  
  "interaction_type": "edit_and_finalize",  
  "action": "accept_with_edits",  
  "actor_id": "user_123",  
  "actor_role": "model_developer",  
  "structured_edits": {  
    "groups": [  
      {"label": "Bin 1", "source_bins": [1]},  
      {"label": "Bin 2", "source_bins": [2, 3]},  
      {"label": "Bin 3", "source_bins": [4]}  
    ]  
  },  
  "user_comment": "Merged bins 2 and 3 for better support.",  
  "timestamp": "2026-03-15T10:30:00+08:00"  
}  
  
====================================================================  
12. STANDARD RESPONSE CONTRACT FROM AGENT TO UI  
====================================================================  
  
The backend shall return a structured response envelope.  
  
Minimum shared response:  
- status  
- message  
- stage_name  
- interaction_state  
- updated_metrics  
- warnings  
- errors  
- artifacts_created  
- selected_candidate_version_id if applicable  
- audit_ref  
- event_ref  
- next_step  
  
Possible status values:  
- preview_ready  
- valid_final  
- valid_with_warning  
- invalid_needs_review  
- blocked  
- finalized  
- escalated  
- rerun_created  
  
Example generalized response:  
{  
  "status": "valid_with_warning",  
  "message": "Edited result is acceptable, but one threshold remains borderline.",  
  "stage_name": "coarse_classing_review",  
  "interaction_state": "preview_generated",  
  "updated_metrics": {  
    "iv_after": 0.171,  
    "support_breach_count": 1  
  },  
  "warnings": [  
    "One group remains slightly below target support."  
  ],  
  "errors": [],  
  "artifacts_created": [  
    "artifact://coarse_bins_v3"  
  ],  
  "audit_ref": "audit://run_001/rev_010",  
  "event_ref": "event://evt_200",  
  "next_step": "waiting_for_confirmation"  
}  
  
====================================================================  
13. GENERALIZED USER EXPERIENCE REQUIREMENTS  
====================================================================  
  
13.1 Clarity  
--------------------------------------------------------------------  
The user shall be able to understand:  
- what the agent proposes  
- why it is proposed  
- what evidence supports it  
- what actions are available  
- what the consequences are  
  
13.2 Minimal Friction  
--------------------------------------------------------------------  
The interaction shall minimize unnecessary back-and-forth text and  
prefer direct structured editing.  
  
13.3 Preview Before Commit  
--------------------------------------------------------------------  
Users should be able to preview the impact of their edits before  
finalizing where practical.  
  
13.4 Reversible Within Review  
--------------------------------------------------------------------  
Before finalization, the user should be able to revise or reset edits.  
  
13.5 Bounded Final Actions  
--------------------------------------------------------------------  
Final actions shall be explicit and bounded.  
  
13.6 Traceable Feedback  
--------------------------------------------------------------------  
The user should see updated metrics, warnings, and system status after  
interaction.  
  
====================================================================  
14. COARSE CLASSING USE CASE EXAMPLE  
====================================================================  
  
For coarse classing, the interaction shall support:  
  
- show fine bins  
- show proposed coarse bins  
- show WoE / bad rate trend  
- show IV before vs after  
- show monotonicity and support checks  
- allow user to merge bins  
- allow user to choose candidate proposal  
- allow preview of updated metrics  
- allow accept / accept_with_edits / rerun / escalate  
- return final accepted bin structure to the agent  
- persist final bins and audit trail  
  
====================================================================  
15. GENERALIZATION TO OTHER USE CASES  
====================================================================  
  
The same interaction shell shall generalize to:  
  
15.1 Binning Version Selection  
--------------------------------------------------------------------  
- show candidate versions  
- compare metrics  
- choose one version  
- create composite version  
- finalize chosen version  
  
15.2 Model Selection  
--------------------------------------------------------------------  
- show candidate models  
- compare performance and stability  
- choose final model  
- request challenger rerun  
- escalate model choice  
  
15.3 Validation Findings  
--------------------------------------------------------------------  
- show proposed finding summary  
- choose severity  
- edit wording  
- link evidence  
- finalize finding  
  
15.4 Validation Conclusion  
--------------------------------------------------------------------  
- show model fitness summary  
- show required conditions  
- choose final conclusion category  
- add validator rationale  
- finalize validation conclusion  
  
15.5 Deployment Readiness  
--------------------------------------------------------------------  
- show readiness checklist  
- show missing items  
- accept with conditions  
- reject for remediation  
- escalate to approver  
  
15.6 Monitoring Breach Review  
--------------------------------------------------------------------  
- show breach metrics  
- show trend charts  
- select remediation action  
- escalate if severe  
- finalize breach disposition  
  
====================================================================  
16. TECH STACK REQUIREMENTS  
====================================================================  
  
The default notebook-based interaction stack shall be:  
  
Frontend in notebook:  
- ipywidgets  
- Output widget  
- IPython.display  
- optional anywidget for advanced custom editing  
  
Backend in Python kernel:  
- controller layer  
- workflowsdk  
- hitlsdk  
- observabilitysdk  
- auditsdk  
- artifactsdk  
- relevant domain SDK  
- validationsdk where applicable  
  
Bridges:  
- jupyter_bridge  
- agent_bridge  
  
This architecture shall allow evolution to web UI later without  
breaking shared contracts.  
  
====================================================================  
17. CONTROLLER PATTERN  
====================================================================  
  
The interaction framework shall use a controller layer between UI and  
agent / SDK runtime.  
  
Standard path:  
Widget UI  
-> Python Controller  
-> Agent / Skill Runner  
-> SDKs  
-> Result Envelope  
-> Controller  
-> UI Refresh  
  
The controller shall:  
- collect UI state  
- build structured payload  
- call backend / agent  
- write local interaction event if required  
- receive structured response  
- refresh panels  
- update workflow status  
  
Widgets shall not directly embed workflow or SDK logic.  
  
====================================================================  
18. CONNECTION BACK TO AGENT  
====================================================================  
  
The framework shall support seamless return of structured user input  
back to the agent.  
  
Preferred path:  
- user edits in structured UI  
- UI sends structured payload to controller  
- controller sends payload to agent / skill runtime  
- agent validates and recomputes using SDKs  
- backend returns standard response envelope  
- UI refreshes with updated state  
  
The agent shall not rely only on free-form text interpretation if  
structured edits are available.  
  
====================================================================  
19. POST-EDIT VALIDATION  
====================================================================  
  
After user edits, the agent / SDK layer shall run a post-edit  
validation pass.  
  
This may include:  
- metric recalculation  
- threshold checks  
- policy checks  
- consistency checks  
- evidence completeness checks  
- artifact generation  
  
The system shall return:  
- valid_final  
- valid_with_warning  
- invalid_needs_review  
- blocked  
depending on the result.  
  
====================================================================  
20. OBSERVABILITY REQUIREMENTS FOR INTERACTIONS  
====================================================================  
  
Each interaction shall generate structured observability events such  
as:  
- interaction_opened  
- interaction_preview_requested  
- interaction_preview_generated  
- interaction_action_submitted  
- interaction_validated  
- interaction_finalized  
- interaction_escalated  
- interaction_rejected  
- interaction_reset  
  
Each event should include:  
- interaction_id  
- project_id  
- run_id  
- session_id  
- stage_name  
- interaction_type  
- actor_id  
- action  
- summary  
- linked_artifacts  
- linked_review_id if applicable  
  
====================================================================  
21. AUDIT REQUIREMENTS FOR INTERACTIONS  
====================================================================  
  
For final actions, the framework shall store:  
- original proposal  
- user edits  
- final accepted output  
- agent recommendation  
- warnings shown  
- user action  
- user comment  
- timestamp  
- actor identity  
- linked artifact IDs  
- linked review / decision IDs  
  
This shall apply to both development and validation interactions.  
  
====================================================================  
22. REUSABLE INTERACTION SHELL REQUIREMENTS  
====================================================================  
  
The platform shall provide a reusable interaction shell with:  
  
- header area  
- proposal/evidence area  
- editable workspace area  
- action/status area  
- comments area  
- warning/error area  
- linked artifacts / evidence area  
- interaction history area  
  
Domain packs may customize:  
- fields shown  
- charts shown  
- structured edit controls  
- action labels  
- validation messages  
  
But the shell structure shall remain consistent.  
  
====================================================================  
23. ROLE-SENSITIVE INTERACTION SUPPORT  
====================================================================  
  
The framework shall adapt by role.  
  
23.1 Developer mode  
--------------------------------------------------------------------  
Focus:  
- proposal review  
- refinement  
- rerun  
- modeling decisions  
  
23.2 Validator mode  
--------------------------------------------------------------------  
Focus:  
- evidence challenge  
- finding creation  
- severity selection  
- model fitness review  
- validation conclusion  
  
23.3 Approver mode  
--------------------------------------------------------------------  
Focus:  
- summary  
- conditions  
- decision  
- escalation  
  
23.4 Auditor / Reader mode  
--------------------------------------------------------------------  
Focus:  
- traceability  
- read-only review  
- drill-down  
  
====================================================================  
24. SDK / PLATFORM ALIGNMENT  
====================================================================  
  
The interaction framework shall align with:  
  
- workflowsdk for state and stage movement  
- hitlsdk for review and approval logic  
- observabilitysdk for event logging  
- auditsdk for final decision trace  
- artifactsdk for evidence linkage  
- flowvizsdk for summarized interaction flow  
- widgetsdk for reusable UI shell  
- validationsdk for validation-specific interactions  
- domain SDKs for recomputation and validation of edits  
  
====================================================================  
25. REQUIREMENT IDS  
====================================================================  
  
The following requirement IDs are proposed:  
  
INT-FR-001  
Support a generalized interaction framework reusable across all use  
cases.  
  
INT-FR-002  
Support a 3-panel review workspace pattern.  
  
INT-FR-003  
Support structured edits, selections, and narrative comments.  
  
INT-FR-004  
Support preview-before-finalize interaction.  
  
INT-FR-005  
Support a controller pattern between UI and agent / SDK runtime.  
  
INT-FR-006  
Support a standardized UI-to-agent payload contract.  
  
INT-FR-007  
Support a standardized agent-to-UI response envelope.  
  
INT-FR-008  
Support post-edit validation before finalization.  
  
INT-FR-009  
Support role-sensitive interaction rendering.  
  
INT-FR-010  
Support reusable shell with domain-specific content injection.  
  
INT-FR-011  
Support interaction observability events.  
  
INT-FR-012  
Support interaction audit records.  
  
INT-FR-013  
Support generalized interaction for development, validation, and  
governance use cases.  
  
INT-UR-001  
Users shall be able to understand the agent proposal, evidence, and  
available actions clearly.  
  
INT-UR-002  
Users shall be able to refine results in a structured way.  
  
INT-UR-003  
Users shall be able to preview updated results before finalizing.  
  
INT-NFR-001  
The interaction shell shall remain reusable, modular, and future-  
proof.  
  
INT-NFR-002  
The interaction framework shall remain compatible with notebook-first  
delivery and future web-based delivery.  
  
====================================================================  
26. SUCCESS CRITERIA  
====================================================================  
  
The interaction framework shall be considered successful when:  
  
1. users can review agent output clearly  
2. users can refine outputs in a structured way  
3. edited results can be returned to the agent seamlessly  
4. post-edit validation and preview work consistently  
5. final accepted results are auditable and traceable  
6. the same interaction shell can be reused across development,  
   validation, deployment, monitoring, and governance use cases  
7. the framework remains coherent with the platform SDK and workflow  
   design  
  
====================================================================  
END OF URD  
====================================================================  
