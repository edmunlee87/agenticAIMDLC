# Runtime context   
  
====================================================================  
JSON SCHEMA PACK  
RUNTIME CONTEXT, RESOLVED STACK, INTERACTION PAYLOAD,  
REVIEW PAYLOAD, AND STANDARD RESPONSE ENVELOPE  
FOR ENTERPRISE AGENTIC AI MODEL LIFECYCLE PLATFORM  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This reference defines the core JSON object schemas needed by the  
platform runtime, agent bridge, workflow engine, HITL layer, and UI.  
  
The schemas below are logical implementation schemas. They are meant  
to be:  
- deterministic  
- compact  
- agent-friendly  
- workflow-friendly  
- audit-friendly  
- token-thrifty  
  
The pack includes:  
  
1. runtime_context  
2. resolved_stack  
3. interaction_payload  
4. review_payload  
5. standard_response_envelope  
6. supporting enums and reusable object fragments  
7. validation rules and implementation guidance  
  
====================================================================  
1. DESIGN PRINCIPLES  
====================================================================  
  
1. Compact by default  
--------------------------------------------------------------------  
Schemas should carry enough information for deterministic routing and  
auditable execution, but avoid bloated narrative fields.  
  
2. Exact facts first  
--------------------------------------------------------------------  
State, IDs, statuses, and references should be explicit rather than  
embedded in prose.  
  
3. Stable contracts  
--------------------------------------------------------------------  
These contracts should remain stable so that:  
- UI controllers  
- workflow engine  
- SDKs  
- agent bridge  
- reporting layer  
can all interoperate cleanly.  
  
4. Separation of concerns  
--------------------------------------------------------------------  
- runtime_context = what is true now  
- resolved_stack = what behavior/tooling is active now  
- interaction_payload = what human or UI submitted  
- review_payload = what review workspace should display  
- standard_response_envelope = what every material task should return  
  
====================================================================  
2. COMMON ENUMS  
====================================================================  
  
2.1 role_enum  
--------------------------------------------------------------------  
Allowed values:  
- developer  
- validator  
- governance  
- reviewer  
- approver  
- documentation  
- monitoring  
- remediation  
- system  
  
2.2 domain_enum  
--------------------------------------------------------------------  
Allowed values:  
- scorecard  
- timeseries  
- ecl  
- lgd  
- pd  
- ead  
- sicr  
- stress  
- generic  
  
2.3 workflow_mode_enum  
--------------------------------------------------------------------  
Allowed values:  
- development  
- validation  
- governance  
- monitoring  
- remediation  
- documentation  
- annual_review  
- recovery  
  
2.4 ui_mode_enum  
--------------------------------------------------------------------  
Allowed values:  
- standard_chat_plus_context  
- bootstrap_workspace  
- recovery_workspace  
- three_panel_review_workspace  
- candidate_comparison_workspace  
- validation_review_workspace  
- dashboard_review_workspace  
- documentation_workspace  
- flow_explorer_workspace  
  
2.5 interaction_mode_enum  
--------------------------------------------------------------------  
Allowed values:  
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
- chat_assisted_guidance  
  
2.6 status_enum  
--------------------------------------------------------------------  
Allowed values:  
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
- needs_human_review  
  
2.7 review_status_enum  
--------------------------------------------------------------------  
Allowed values:  
- initialized  
- proposed  
- under_review  
- user_editing  
- preview_generated  
- waiting_for_confirmation  
- pending_review  
- approved  
- approved_with_conditions  
- rejected  
- rerun_requested  
- escalated  
- overdue  
- expired_needs_recreation  
- finalized  
- superseded  
- closed  
  
2.8 action_enum  
--------------------------------------------------------------------  
Allowed values:  
- approve  
- approve_with_changes  
- approve_with_conditions  
- reject  
- reject_and_rerun  
- rerun_with_parameters  
- request_more_analysis  
- preview_changes  
- compare_candidates  
- ask_agent_to_optimize_again  
- refresh_metrics  
- accept  
- accept_with_edits  
- approve_version  
- approve_version_with_overrides  
- create_composite_version  
- escalate  
- finalize_validation_conclusion  
- assign_remediation  
- close_remediation  
- reopen_issue  
- resume  
- retry  
- rollback  
- create_new_project  
  
2.9 severity_enum  
--------------------------------------------------------------------  
Allowed values:  
- low  
- moderate  
- high  
- critical  
  
2.10 conclusion_category_enum  
--------------------------------------------------------------------  
Allowed values:  
- fit_for_use  
- fit_for_use_with_conditions  
- fit_for_limited_use  
- not_fit_for_use  
- rework_required  
- evidence_incomplete  
  
====================================================================  
3. REUSABLE OBJECT FRAGMENTS  
====================================================================  
  
3.1 id_ref  
--------------------------------------------------------------------  
Logical schema:  
{  
  "type": "string",  
  "description": "Opaque stable identifier"  
}  
  
3.2 artifact_ref  
--------------------------------------------------------------------  
{  
  "artifact_id": "art_001",  
  "artifact_type": "monitoring_kpi_table",  
  "artifact_name": "monthly_monitoring_kpi_2026_03",  
  "version": "v1",  
  "uri_or_path": "s3://bucket/path/file.parquet"  
}  
  
3.3 warning_object  
--------------------------------------------------------------------  
{  
  "warning_code": "WARN_SUPPORT_NEAR_THRESHOLD",  
  "summary": "One group remains near the minimum support threshold.",  
  "severity": "moderate",  
  "linked_refs": {  
    "artifact_ids": ["art_101"],  
    "metric_ids": ["met_010"]  
  }  
}  
  
3.4 error_object  
--------------------------------------------------------------------  
{  
  "error_code": "ERR_INVALID_LINEAGE",  
  "summary": "Join keys are incomplete for source table X.",  
  "details": "Expected keys customer_id, reporting_date.",  
  "is_retryable": false  
}  
  
3.5 metric_summary_object  
--------------------------------------------------------------------  
{  
  "metric_name": "gini",  
  "metric_value": 0.43,  
  "metric_unit": "ratio",  
  "status": "pass"  
}  
  
3.6 candidate_summary_object  
--------------------------------------------------------------------  
{  
  "candidate_version_id": "cand_003",  
  "candidate_name": "binning_candidate_b",  
  "candidate_type": "binning_version",  
  "summary_metrics": [  
    {"metric_name": "iv_retention", "metric_value": 0.91, "metric_unit": "ratio", "status": "pass"},  
    {"metric_name": "support_breach_count", "metric_value": 0, "metric_unit": "count", "status": "pass"}  
  ],  
  "warning_count": 1  
}  
  
3.7 finding_summary_object  
--------------------------------------------------------------------  
{  
  "finding_id": "find_002",  
  "finding_type": "methodology_issue",  
  "severity": "high",  
  "summary": "Evidence for monotonicity exception is insufficient."  
}  
  
3.8 actor_object  
--------------------------------------------------------------------  
{  
  "actor_id": "user_123",  
  "actor_role": "validator",  
  "actor_type": "human"  
}  
  
3.9 stage_context_object  
--------------------------------------------------------------------  
{  
  "active_stage": "validation_conclusion",  
  "stage_class": "review",  
  "stage_sequence_no": 17  
}  
  
====================================================================  
4. SCHEMA 1 – RUNTIME_CONTEXT  
====================================================================  
  
4.1 Purpose  
--------------------------------------------------------------------  
runtime_context is the smallest authoritative object describing the  
current execution state for routing, stack resolution, and SDK  
allowlisting.  
  
4.2 Logical Schema  
--------------------------------------------------------------------  
{  
  "schema_name": "runtime_context",  
  "schema_version": "1.0",  
  "project_id": "proj_001",  
  "run_id": "run_001",  
  "session_id": "sess_001",  
  
  "active_role": "developer",  
  "active_domain": "scorecard",  
  "workflow_mode": "development",  
  
  "stage_context": {  
    "active_stage": "coarse_classing_review",  
    "stage_class": "review",  
    "stage_sequence_no": 6  
  },  
  
  "validation_mode": false,  
  "annual_review_mode": false,  
  "remediation_mode": false,  
  
  "policy_mode": "standard",  
  "pending_review_type": "coarse_classing",  
  "ui_entry_point": "main_workspace",  
  
  "selected_candidate_version_id": null,  
  "candidate_versions_present": true,  
  
  "failure_state": false,  
  "last_error_code": null,  
  
  "active_overlays": [  
    "strict-governance-overlay"  
  ],  
  
  "current_refs": {  
    "review_id": "rev_010",  
    "validation_run_id": null,  
    "model_id": "mdl_001",  
    "dataset_id": "ds_020",  
    "artifact_ids": ["art_101", "art_102"]  
  },  
  
  "token_mode": "standard_mode"  
}  
  
4.3 Field Definitions  
--------------------------------------------------------------------  
schema_name  
- constant identifier for this schema  
  
schema_version  
- schema version for compatibility control  
  
project_id  
- active project identifier  
  
run_id  
- active workflow run identifier  
  
session_id  
- active user/session context identifier  
  
active_role  
- current acting role from role_enum  
  
active_domain  
- current domain from domain_enum  
  
workflow_mode  
- current lifecycle mode from workflow_mode_enum  
  
stage_context  
- nested object describing current stage  
  
validation_mode  
- boolean flag indicating validation workflow context  
  
annual_review_mode  
- boolean flag indicating annual review context  
  
remediation_mode  
- boolean flag indicating remediation context  
  
policy_mode  
- short policy profile label such as standard, strict, sandbox  
  
pending_review_type  
- optional string identifying pending review type  
  
ui_entry_point  
- source surface, e.g. main_workspace, right_sidebar_chat, api  
  
selected_candidate_version_id  
- final chosen candidate version if any  
  
candidate_versions_present  
- quick boolean for selection-aware routing  
  
failure_state  
- whether runtime is currently in failure/recovery state  
  
last_error_code  
- optional prior error reference  
  
active_overlays  
- active overlay skills  
  
current_refs  
- useful exact references for routing and display  
  
token_mode  
- micro_mode, standard_mode, deep_review_mode  
  
4.4 Validation Rules  
--------------------------------------------------------------------  
- project_id, run_id, session_id are required  
- active_role, active_domain, workflow_mode are required  
- stage_context.active_stage is required  
- if candidate_versions_present = true and selected_candidate_version_id  
  is null for a stage requiring selection, downstream progression must  
  be blocked  
- if validation_mode = true, active_role should typically be validator,  
  governance, approver, or documentation  
  
====================================================================  
5. SCHEMA 2 – RESOLVED_STACK  
====================================================================  
  
5.1 Purpose  
--------------------------------------------------------------------  
resolved_stack describes the exact active behavior stack, SDK  
allowlist, and UI contract chosen by the runtime resolver.  
  
5.2 Logical Schema  
--------------------------------------------------------------------  
{  
  "schema_name": "resolved_stack",  
  "schema_version": "1.0",  
  
  "project_id": "proj_001",  
  "run_id": "run_001",  
  "session_id": "sess_001",  
  
  "resolved_skills": {  
    "base_skills": [  
      "platform-base-rules",  
      "model-lifecycle-orchestrator"  
    ],  
    "role_skill": "developer-agent",  
    "domain_skill": "scorecard-domain",  
    "stage_skill": "coarse-classing-review",  
    "overlay_skills": [  
      "strict-governance-overlay"  
    ],  
    "support_skills": [  
      "candidate-comparison-assistant"  
    ]  
  },  
  
  "sdk_allowlist": [  
    "scorecardsdk",  
    "evaluation_sdk",  
    "hitlsdk",  
    "workflowsdk",  
    "artifactsdk",  
    "observabilitysdk",  
    "auditsdk",  
    "reporting_sdk",  
    "jupyter_bridge",  
    "widgetsdk"  
  ],  
  
  "ui_contract": {  
    "ui_mode": "three_panel_review_workspace",  
    "interaction_mode": "edit_and_finalize",  
    "requires_human_action": true,  
    "display_sections": [  
      "proposal",  
      "evidence",  
      "structured_edit_workspace",  
      "status",  
      "actions"  
    ]  
  },  
  
  "response_contract": {  
    "expected_response_schema": "standard_response_envelope",  
    "mandatory_statuses": [  
      "preview_ready",  
      "finalized",  
      "invalid_needs_review"  
    ]  
  }  
}  
  
5.3 Field Definitions  
--------------------------------------------------------------------  
resolved_skills.base_skills  
- always-active platform skills  
  
resolved_skills.role_skill  
- currently active role agent  
  
resolved_skills.domain_skill  
- currently active domain skill  
  
resolved_skills.stage_skill  
- currently active stage skill  
  
resolved_skills.overlay_skills  
- optional overlays  
  
resolved_skills.support_skills  
- optional helper skills  
  
sdk_allowlist  
- list of permitted SDKs for this stage  
  
ui_contract  
- active UI expectations for the workspace/controller  
  
response_contract  
- expected output schema and common statuses  
  
5.4 Validation Rules  
--------------------------------------------------------------------  
- role_skill, domain_skill, stage_skill are required except for pure  
  bootstrap flows  
- sdk_allowlist must be non-empty  
- if requires_human_action = true, ui_mode should not be purely  
  routing_only chat mode unless human action is captured elsewhere  
  
====================================================================  
6. SCHEMA 3 – INTERACTION_PAYLOAD  
====================================================================  
  
6.1 Purpose  
--------------------------------------------------------------------  
interaction_payload is the structured object sent from UI/controller to  
the interaction-orchestrator or backend after human action.  
  
6.2 Logical Schema  
--------------------------------------------------------------------  
{  
  "schema_name": "interaction_payload",  
  "schema_version": "1.0",  
  
  "project_id": "proj_001",  
  "run_id": "run_001",  
  "session_id": "sess_001",  
  
  "interaction_id": "int_001",  
  "review_id": "rev_010",  
  
  "stage_name": "coarse_classing_review",  
  "interaction_type": "edit_and_finalize",  
  "action": "accept_with_edits",  
  
  "actor": {  
    "actor_id": "user_123",  
    "actor_role": "developer",  
    "actor_type": "human"  
  },  
  
  "selected_candidate_version_id": null,  
  
  "structured_edits": {  
    "groups": [  
      {"label": "Bin 1", "source_bins": [1]},  
      {"label": "Bin 2", "source_bins": [2, 3]},  
      {"label": "Bin 3", "source_bins": [4]},  
      {"label": "Missing", "source_bins": ["MISSING"]}  
    ]  
  },  
  
  "parameters": {  
    "rerun_strategy": null,  
    "comparison_mode": null  
  },  
  
  "user_comment": "Merged bins 2 and 3 for better support.",  
  "attachments": {  
    "artifact_ids": [],  
    "external_refs": []  
  },  
  
  "timestamp": "2026-03-17T10:30:00+08:00"  
}  
  
6.3 Minimum Required Fields  
--------------------------------------------------------------------  
Required:  
- project_id  
- run_id  
- session_id  
- interaction_id  
- stage_name  
- interaction_type  
- action  
- actor  
- timestamp  
  
Conditionally required:  
- review_id if this action belongs to a review  
- selected_candidate_version_id if action is candidate selection  
- structured_edits if action is edit_and_finalize  
- parameters if rerun_with_parameters or compare mode is requested  
  
6.4 Common Interaction Payload Variants  
--------------------------------------------------------------------  
  
A. Candidate Selection  
{  
  "interaction_type": "candidate_comparison_and_selection",  
  "action": "approve_version",  
  "selected_candidate_version_id": "cand_002"  
}  
  
B. Validation Conclusion  
{  
  "interaction_type": "review_and_conclude",  
  "action": "finalize_validation_conclusion",  
  "structured_edits": {  
    "conclusion_category": "fit_for_use_with_conditions",  
    "conditions": [  
      "Monitor score drift monthly for 3 periods."  
    ]  
  }  
}  
  
C. Monitoring Breach Review  
{  
  "interaction_type": "triage_and_disposition",  
  "action": "assign_remediation",  
  "structured_edits": {  
    "owner_id": "user_777",  
    "due_date": "2026-04-15",  
    "action_class": "root_cause_review"  
  }  
}  
  
6.5 Validation Rules  
--------------------------------------------------------------------  
- action must be from action_enum  
- actor.actor_role must be from role_enum  
- if action = approve_version, selected_candidate_version_id is required  
- if action = preview_changes, finalization should not occur  
- if action = escalate, escalated status is expected in response  
- structured_edits must be object or null, not free-form string only  
  
====================================================================  
7. SCHEMA 4 – REVIEW_PAYLOAD  
====================================================================  
  
7.1 Purpose  
--------------------------------------------------------------------  
review_payload is the display-ready object used by widgets/workspaces  
for governed review.  
  
7.2 Logical Schema  
--------------------------------------------------------------------  
{  
  "schema_name": "review_payload",  
  "schema_version": "1.0",  
  
  "project_id": "proj_001",  
  "run_id": "run_001",  
  "session_id": "sess_001",  
  "review_id": "rev_010",  
  
  "stage_name": "coarse_classing_review",  
  "review_type": "coarse_classing",  
  "review_status": "under_review",  
  
  "title": "Coarse Classing Review – Utilization Ratio",  
  "decision_required": true,  
  
  "actor_context": {  
    "expected_role": "developer",  
    "current_actor_role": "developer"  
  },  
  
  "proposal_summary": {  
    "business_summary": "Candidate B provides better support distribution with near-monotonic WoE.",  
    "technical_summary": "One support warning remains near threshold but IV retention is high.",  
    "recommendation": "Accept Candidate B or merge bins 2 and 3 and preview again."  
  },  
  
  "evidence": {  
    "key_metrics": [  
      {"metric_name": "iv_retention", "metric_value": 0.91, "metric_unit": "ratio", "status": "pass"},  
      {"metric_name": "support_breach_count", "metric_value": 1, "metric_unit": "count", "status": "warning"}  
    ],  
    "warnings": [  
      {  
        "warning_code": "WARN_SUPPORT_NEAR_THRESHOLD",  
        "summary": "One group remains near the minimum support threshold.",  
        "severity": "moderate",  
        "linked_refs": {"artifact_ids": ["art_101"], "metric_ids": []}  
      }  
    ],  
    "artifact_refs": [  
      {  
        "artifact_id": "art_101",  
        "artifact_type": "binning_summary_table",  
        "artifact_name": "utilization_ratio_binning_summary",  
        "version": "v2",  
        "uri_or_path": "s3://bucket/binning/summary.parquet"  
      }  
    ],  
    "candidate_summaries": [  
      {  
        "candidate_version_id": "cand_002",  
        "candidate_name": "candidate_b",  
        "candidate_type": "binning_version",  
        "summary_metrics": [  
          {"metric_name": "iv_retention", "metric_value": 0.91, "metric_unit": "ratio", "status": "pass"}  
        ],  
        "warning_count": 1  
      }  
    ]  
  },  
  
  "actions": {  
    "allowed_actions": [  
      "preview_changes",  
      "accept",  
      "accept_with_edits",  
      "reject_and_rerun",  
      "escalate"  
    ],  
    "default_action": "preview_changes"  
  },  
  
  "structured_edit_schema": {  
    "edit_type": "bin_group_edit",  
    "required_fields": ["groups"]  
  },  
  
  "linked_refs": {  
    "decision_id": null,  
    "validation_run_id": null,  
    "candidate_version_ids": ["cand_001", "cand_002", "cand_003"]  
  },  
  
  "timestamps": {  
    "created_timestamp": "2026-03-17T09:00:00+08:00",  
    "due_timestamp": "2026-03-19T18:00:00+08:00"  
  }  
}  
  
7.3 Required Fields  
--------------------------------------------------------------------  
Required:  
- project_id  
- run_id  
- session_id  
- review_id  
- stage_name  
- review_type  
- review_status  
- title  
- decision_required  
- proposal_summary  
- actions.allowed_actions  
  
Optional but strongly recommended:  
- evidence  
- structured_edit_schema  
- linked_refs  
- due_timestamp  
  
7.4 Validation Rules  
--------------------------------------------------------------------  
- allowed_actions must be non-empty  
- if decision_required = true, review_status should not be closed  
- if review_type is candidate selection, candidate_summaries should be  
  present when available  
- if structured editing is allowed, structured_edit_schema should be  
  provided  
  
====================================================================  
8. SCHEMA 5 – STANDARD_RESPONSE_ENVELOPE  
====================================================================  
  
8.1 Purpose  
--------------------------------------------------------------------  
standard_response_envelope is the canonical output shape for all  
material tasks, including SDK calls, agent-orchestrated steps, review  
actions, and preview actions.  
  
8.2 Logical Schema  
--------------------------------------------------------------------  
{  
  "schema_name": "standard_response_envelope",  
  "schema_version": "1.0",  
  
  "status": "valid_with_warning",  
  "message": "Edited bins are acceptable, but one group remains near the minimum support threshold.",  
  
  "project_id": "proj_001",  
  "run_id": "run_001",  
  "session_id": "sess_001",  
  
  "current_stage": "coarse_classing_review",  
  "next_stage": "woe_iv_review",  
  
  "required_human_action": true,  
  "interaction_state": "preview_generated",  
  
  "warnings": [  
    {  
      "warning_code": "WARN_SUPPORT_NEAR_THRESHOLD",  
      "summary": "One group remains near the minimum support threshold.",  
      "severity": "moderate",  
      "linked_refs": {"artifact_ids": ["art_101"], "metric_ids": []}  
    }  
  ],  
  
  "errors": [],  
  
  "artifacts_created": [  
    {  
      "artifact_id": "art_201",  
      "artifact_type": "coarse_bin_definition",  
      "artifact_name": "utilization_ratio_coarse_bins_v3",  
      "version": "v3",  
      "uri_or_path": "s3://bucket/output/coarse_bins_v3.json"  
    }  
  ],  
  
  "candidate_versions_created": [],  
  "selected_candidate_version_id": null,  
  
  "updated_metrics": [  
    {"metric_name": "iv_after", "metric_value": 0.171, "metric_unit": "ratio", "status": "pass"},  
    {"metric_name": "support_breach_count", "metric_value": 1, "metric_unit": "count", "status": "warning"}  
  ],  
  
  "review_created": null,  
  
  "validation_updates": {  
    "finding_ids": [],  
    "conclusion_id": null  
  },  
  
  "workflow_state_patch": {  
    "review_status": "preview_generated",  
    "current_stage_status": "paused"  
  },  
  
  "audit_ref": "audit://run_001/rev_010",  
  "event_ref": "event://evt_200",  
  
  "token_usage_hint": {  
    "mode": "standard_mode",  
    "recommended_next_context": "compact"  
  }  
}  
  
8.3 Required Fields  
--------------------------------------------------------------------  
Required:  
- status  
- message  
- current_stage  
- required_human_action  
- warnings  
- errors  
- artifacts_created  
- candidate_versions_created  
- workflow_state_patch  
- audit_ref  
- event_ref  
  
Strongly recommended:  
- project_id  
- run_id  
- session_id  
- next_stage  
- interaction_state  
- updated_metrics  
- selected_candidate_version_id  
- review_created  
  
8.4 Status Mapping Guidance  
--------------------------------------------------------------------  
success  
- task completed normally  
  
success_with_warning  
- task completed but warnings exist  
  
blocked  
- task cannot proceed due to unmet prerequisite or rule  
  
failed  
- execution failed technically or logically  
  
pending_human_review  
- review has been created and awaits human input  
  
preview_ready  
- preview/recompute completed and awaits confirmation  
  
rerun_requested  
- rerun branch or request has been created  
  
escalated  
- issue/review was escalated  
  
paused  
- workflow paused intentionally  
  
resumed  
- workflow resumed from prior state  
  
finalized  
- final decision/task completion recorded  
  
invalid_input  
- request payload invalid  
  
invalid_needs_review  
- result exists but is not acceptable without further review  
  
needs_human_review  
- explicit human review required before continuation  
  
8.5 Validation Rules  
--------------------------------------------------------------------  
- status must be from status_enum  
- warnings and errors must always be arrays, even if empty  
- artifacts_created and candidate_versions_created must always be arrays  
- if status = failed, errors should not be empty  
- if status = pending_human_review, review_created should normally be  
  populated  
- if status = finalized, workflow_state_patch should reflect final state  
  change  
- if status = preview_ready, required_human_action should usually be true  
  
====================================================================  
9. COMPACT JSON EXAMPLES BY SCENARIO  
====================================================================  
  
9.1 Candidate Selection Example  
--------------------------------------------------------------------  
{  
  "status": "finalized",  
  "message": "Candidate version cand_002 has been selected.",  
  "project_id": "proj_001",  
  "run_id": "run_001",  
  "session_id": "sess_001",  
  "current_stage": "binning_version_selection",  
  "next_stage": "model_fitting_review",  
  "required_human_action": false,  
  "interaction_state": "finalized",  
  "warnings": [],  
  "errors": [],  
  "artifacts_created": [],  
  "candidate_versions_created": [],  
  "selected_candidate_version_id": "cand_002",  
  "updated_metrics": [],  
  "review_created": null,  
  "validation_updates": {"finding_ids": [], "conclusion_id": null},  
  "workflow_state_patch": {  
    "selected_candidate_version_id": "cand_002",  
    "current_stage_status": "finalized"  
  },  
  "audit_ref": "audit://run_001/sel_002",  
  "event_ref": "event://evt_202",  
  "token_usage_hint": {  
    "mode": "micro_mode",  
    "recommended_next_context": "minimal"  
  }  
}  
  
9.2 Validation Conclusion Example  
--------------------------------------------------------------------  
{  
  "status": "finalized",  
  "message": "Validation conclusion recorded as fit_for_use_with_conditions.",  
  "project_id": "proj_001",  
  "run_id": "run_001",  
  "session_id": "sess_002",  
  "current_stage": "validation_conclusion",  
  "next_stage": "deployment_readiness",  
  "required_human_action": false,  
  "interaction_state": "finalized",  
  "warnings": [],  
  "errors": [],  
  "artifacts_created": [  
    {  
      "artifact_id": "art_501",  
      "artifact_type": "validation_conclusion_note",  
      "artifact_name": "validation_conclusion_v1",  
      "version": "v1",  
      "uri_or_path": "s3://bucket/validation/conclusion_v1.docx"  
    }  
  ],  
  "candidate_versions_created": [],  
  "selected_candidate_version_id": null,  
  "updated_metrics": [],  
  "review_created": null,  
  "validation_updates": {  
    "finding_ids": ["find_001", "find_002"],  
    "conclusion_id": "vcon_001"  
  },  
  "workflow_state_patch": {  
    "validation_conclusion_status": "finalized",  
    "current_stage_status": "finalized"  
  },  
  "audit_ref": "audit://run_001/vcon_001",  
  "event_ref": "event://evt_305",  
  "token_usage_hint": {  
    "mode": "deep_review_mode",  
    "recommended_next_context": "compact"  
  }  
}  
  
9.3 Monitoring Breach Escalation Example  
--------------------------------------------------------------------  
{  
  "status": "escalated",  
  "message": "Monitoring breach escalated due to repeated severe score drift.",  
  "project_id": "proj_100",  
  "run_id": "run_090",  
  "session_id": "sess_050",  
  "current_stage": "monitoring_breach_review",  
  "next_stage": "remediation_planning",  
  "required_human_action": true,  
  "interaction_state": "escalated",  
  "warnings": [  
    {  
      "warning_code": "WARN_SEVERE_SCORE_DRIFT",  
      "summary": "Score drift has exceeded severe threshold for two consecutive periods.",  
      "severity": "high",  
      "linked_refs": {"artifact_ids": ["art_880"], "metric_ids": []}  
    }  
  ],  
  "errors": [],  
  "artifacts_created": [],  
  "candidate_versions_created": [],  
  "selected_candidate_version_id": null,  
  "updated_metrics": [  
    {"metric_name": "psi_score", "metric_value": 0.31, "metric_unit": "ratio", "status": "breach"}  
  ],  
  "review_created": {  
    "review_id": "rev_mon_010",  
    "review_type": "monitoring_breach",  
    "review_status": "pending_review"  
  },  
  "validation_updates": {  
    "finding_ids": [],  
    "conclusion_id": null  
  },  
  "workflow_state_patch": {  
    "current_stage_status": "escalated",  
    "remediation_mode": true  
  },  
  "audit_ref": "audit://run_090/breach_010",  
  "event_ref": "event://evt_900",  
  "token_usage_hint": {  
    "mode": "standard_mode",  
    "recommended_next_context": "compact"  
  }  
}  
  
====================================================================  
10. IMPLEMENTATION GUIDANCE  
====================================================================  
  
10.1 Keep IDs Opaque  
--------------------------------------------------------------------  
Do not encode business logic in IDs. IDs should be stable references.  
  
10.2 Keep Arrays Present  
--------------------------------------------------------------------  
Even if empty, arrays like warnings, errors, artifacts_created should  
still be present to simplify downstream handling.  
  
10.3 Separate Review Payload From Interaction Payload  
--------------------------------------------------------------------  
review_payload is for UI display.  
interaction_payload is for UI submission.  
Do not overload one for both purposes.  
  
10.4 Standard Response Must Be Universal  
--------------------------------------------------------------------  
All material SDK tasks and agent-orchestrated stage tasks should map  
their outputs into standard_response_envelope.  
  
10.5 Use workflow_state_patch Sparingly  
--------------------------------------------------------------------  
Only patch changed state fields. Avoid copying full workflow state in  
responses.  
  
10.6 Token Thrift Guidance  
--------------------------------------------------------------------  
For chat/runtime grounding:  
- pass runtime_context in compact form  
- pass resolved_stack in compact form  
- pass review_payload summary rather than full artifact content  
- rely on artifact refs and summaries, not full raw payloads  
  
====================================================================  
11. MINIMUM VALIDATION CHECKLIST  
====================================================================  
  
Before accepting runtime_context:  
- required IDs present  
- role/domain/stage valid enums  
- stage_context.active_stage populated  
  
Before accepting resolved_stack:  
- role skill present  
- domain skill present if domain-specific  
- stage skill present unless bootstrap/recovery  
- SDK allowlist non-empty  
  
Before accepting interaction_payload:  
- action valid  
- actor valid  
- required conditional fields present  
- structured_edits object valid if provided  
  
Before rendering review_payload:  
- allowed_actions non-empty  
- title present  
- proposal summary present  
- evidence refs formatted correctly  
  
Before returning standard_response_envelope:  
- status valid  
- warnings/errors arrays present  
- audit_ref and event_ref present  
- workflow_state_patch object present  
  
====================================================================  
12. FINAL RECOMMENDATION  
====================================================================  
  
Use these schema contracts as the canonical interface between:  
- CodeBuddy / agent runtime  
- Jupyter controller layer  
- workflow engine  
- HITL engine  
- SDK execution layer  
- reporting and audit layers  
  
That will give you:  
- deterministic routing  
- strong governance  
- easier debugging  
- cleaner UI integration  
- better token thrift  
- lower ambiguity across the full platform  
  
====================================================================  
END OF JSON SCHEMA PACK  
====================================================================  
