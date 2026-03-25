# Stage by stage orchestration   
  
====================================================================  
STAGE-BY-STAGE ORCHESTRATION PLAYBOOK  
AGENTIC AI MDLC FRAMEWORK  
EXECUTION BLUEPRINT  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This playbook converts the tool allowlist and tool registry into an  
execution blueprint.  
  
For each stage it defines:  
- stage purpose  
- entry criteria  
- actor roles  
- input references  
- allowed tools  
- expected outputs  
- workflow patches  
- failure routes  
- review routes  
- retry rules  
- next-stage routes  
  
This is intended to be the operational guide for:  
- runtime orchestration  
- controller design  
- agent reasoning  
- HITL integration  
- audit and observability behavior  
- stage gating  
  
====================================================================  
GLOBAL STAGE EXECUTION CONTRACT  
====================================================================  
  
Every stage should follow this pattern:  
  
1. entry validation  
2. runtime stack resolution  
3. allowlist resolution  
4. optional retrieval/context enrichment  
5. main tool execution  
6. result normalization  
7. event emission  
8. audit write if required  
9. workflow patch application  
10. review creation if required  
11. route next stage or block  
  
Standard stage result shape:  
{  
  "stage_name": "string",  
  "stage_status": "success | success_with_warning | blocked | failed | pending_human_review | finalized",  
  "entry_check_passed": true,  
  "artifacts_created": [],  
  "workflow_patch": {},  
  "review_created": false,  
  "review_id": null,  
  "recommended_next_stage": "string | null",  
  "failure_route": "string | null"  
}  
  
====================================================================  
STAGE 1. SESSION_BOOTSTRAP  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Initialize or resume a user session and prepare minimal runtime context.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- user has entered the platform  
- actor identity is available  
- no active runtime stack yet  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- validator  
- monitoring  
- governance  
- approver  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
Required:  
- actor_id  
- actor_role  
  
Optional:  
- preferred_project_id  
- preferred_domain  
- prior_session_id  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- open_session  
- resume_session  
- resolve_runtime_stack  
- search_knowledge  
- build_context_pack  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- session_id  
- resume candidates  
- available project list  
- default runtime context  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "session_id": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If session open fails:  
- go to STAGE_FAILURE_BOOTSTRAP  
  
If prior session is corrupted:  
- go to RECOVERY_SESSION_SELECTION  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
None by default  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
If resume chosen:  
- WORKFLOW_RESUME_SELECTION  
  
If new project:  
- WORKFLOW_BOOTSTRAP  
  
====================================================================  
STAGE 2. WORKFLOW_RESUME_SELECTION  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Choose whether to continue from prior work or start new work.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- active session exists  
- one or more resumable projects/runs found  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- all human roles  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- session_id  
- resume_candidates  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- get_workflow_state  
- replay_run  
- resolve_recovery_path  
- patch_workflow_state  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- selected run_id  
- resume decision  
- recovery recommendation if needed  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "run_id": "string",  
  "project_id": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If run cannot be resumed:  
- RECOVERY_SESSION_SELECTION  
- WORKFLOW_BOOTSTRAP  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
Optional if recovery path requires formal decision  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- RUNTIME_STACK_RESOLUTION  
- RECOVERY_REVIEW if stale/broken state  
  
====================================================================  
STAGE 3. WORKFLOW_BOOTSTRAP  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Create project/run and initialize workflow state.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- session_id exists  
- project selected or new project requested  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- session_id  
- project metadata  
- workflow_type  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- register_project  
- register_run  
- bootstrap_project_workflow  
- create_checkpoint  
- load_policy_pack  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- project_id  
- run_id  
- initial workflow state  
- initial checkpoint optional  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "project_id": "string",  
  "run_id": "string",  
  "current_stage": "workflow_bootstrap"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If project/run creation fails:  
- STAGE_FAILURE_BOOTSTRAP  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
Usually none  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed if duplicate prevention exists  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- RUNTIME_STACK_RESOLUTION  
  
====================================================================  
STAGE 4. RUNTIME_STACK_RESOLUTION  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Resolve role, stage, UI, interaction mode, token mode, and tool  
allowlist.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- project_id and run_id exist  
- current_stage known  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- all  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- RuntimeContext  
- workflow state  
- actor role  
- domain  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- resolve_runtime_stack  
- get_stage_controls  
- requires_human_review  
- get_approval_requirements  
- build_context_pack  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- ResolvedStack  
- sdk_allowlist  
- ui_mode  
- interaction_mode  
- token_mode  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
Usually none  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If stage mapping fails:  
- STAGE_RUNTIME_MAPPING_FAILURE  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
None  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- stage determined by workflow state  
- usually into stage-specific execution below  
  
====================================================================  
STAGE 5. DATA_PREPARATION_CONFIG  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Validate dataprep request and supported template selection.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- current_stage = data_preparation_config  
- project/run active  
- dataprep request payload available  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- dataprep config  
- template_id  
- domain  
- data_structure_type  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- validate_dataprep_config  
- validate_template_request  
- load_policy_pack  
- requires_human_review  
- create_review  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- validated dataprep config  
- approved template mapping  
- policy review requirement if any  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "dataprep_config_validated": true  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If config invalid:  
- STAGE_FAILURE_DATAPREP_CONFIG  
  
If unsupported template:  
- STAGE_FAILURE_TEMPLATE_VALIDATION  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
If policy requires config review:  
- DATA_PREPARATION_CONFIG_REVIEW  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry after config correction  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
If valid and no review:  
- DATA_PREPARATION_EXECUTION  
  
If review required:  
- DATA_PREPARATION_CONFIG_REVIEW  
  
====================================================================  
STAGE 6. DATA_PREPARATION_CONFIG_REVIEW  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Governed review of dataprep configuration or lineage rules.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- dataprep config exists  
- policy or control matrix requires review  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- governance  
- approver  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- review payload for dataprep config  
- policy controls  
- config diff / summary  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- create_review  
- get_review  
- build_review_payload  
- validate_review_action  
- approve_review  
- approve_review_with_conditions  
- escalate_review  
- capture_review_decision  
- patch_workflow_state  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- review_id  
- decision  
- approved or conditional config status  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "dataprep_config_approved": true  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If rejected:  
- DATA_PREPARATION_CONFIG  
  
If escalated:  
- GOVERNANCE_ESCALATION_REVIEW  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
This stage is the review route  
  
RETRY RULES  
--------------------------------------------------------------------  
- preview/re-read allowed  
- final approval limited  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- DATA_PREPARATION_EXECUTION  
- DATA_PREPARATION_CONFIG on rejection  
  
====================================================================  
STAGE 7. DATA_PREPARATION_EXECUTION  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Execute governed dataprep using approved template and Spark logic.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- valid dataprep config  
- template supported  
- sources available  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- DataPrepRequest  
- source_mappings  
- target definition  
- split definition  
- Spark session or Spark runtime availability  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- execute_dataprep_request  
- build_cross_sectional_dataset_spark  
- build_panel_dataset_spark  
- build_time_series_dataset_spark  
- build_cohort_dataset_spark  
- build_event_history_dataset_spark  
- create_checkpoint  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- dataset artifact refs  
- prep manifest refs  
- lineage refs  
- row counts  
- target summary  
- split summary  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "dataprep_executed": true,  
  "prepared_dataset_ref": "string | null"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If Spark failure:  
- STAGE_FAILURE_DATAPREP_EXECUTION  
- RECOVERY_TECHNICAL_RERUN  
  
If source mismatch:  
- DATA_PREPARATION_CONFIG  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
None by default  
  
RETRY RULES  
--------------------------------------------------------------------  
- limited retry only if idempotent and safe  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- DATA_READINESS_CHECK  
  
====================================================================  
STAGE 8. DATA_READINESS_CHECK  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Check whether prepared data is fit for downstream modeling.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- prepared dataset exists  
- manifest or dataset ref exists  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- validator  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- dataset ref  
- expected schema  
- quality check pack  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- run_prep_quality_checks_spark  
- run_schema_checks  
- run_missingness_checks  
- run_consistency_checks  
- build_distribution_profile  
- run_business_rule_checks  
- build_dq_summary  
- validate_dataset_contract  
- detect_policy_breaches  
- create_dq_exception  
- create_review  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- DQ summary  
- contract validation result  
- readiness status  
- possible exception/review trigger  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "data_readiness_status": "pass | warning | fail"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If severe issues:  
- DATA_REMEDIATION  
- DATA_READINESS_REVIEW  
  
If technical read failure:  
- STAGE_FAILURE_DATA_READINESS  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
If severe DQ or policy breach:  
- DATA_READINESS_REVIEW  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry after dataprep rerun or config fix  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
If pass:  
- DATASET_REGISTRATION  
  
If warning requiring sign-off:  
- DATA_READINESS_REVIEW  
  
If fail:  
- DATA_REMEDIATION  
  
====================================================================  
STAGE 9. DATA_READINESS_REVIEW  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Governed review of material data quality or contract issues.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- dq_summary severity above threshold  
or  
- policy requires review despite warnings  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- validator  
- governance  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- dq_summary  
- contract validation result  
- evidence refs  
- review payload  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- create_review  
- get_review  
- build_review_payload  
- validate_review_action  
- approve_review  
- approve_review_with_conditions  
- escalate_review  
- capture_review_decision  
- create_dq_exception  
- patch_workflow_state  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- approved with conditions / rejected / rerun required  
- remediation requirements if any  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "data_readiness_review_completed": true,  
  "data_readiness_status": "approved | conditional | rejected"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If rejected:  
- DATA_REMEDIATION  
- DATA_PREPARATION_CONFIG  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
This stage is the review route  
  
RETRY RULES  
--------------------------------------------------------------------  
- final decision limited  
- evidence refresh allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
If approved:  
- DATASET_REGISTRATION  
  
If rejected:  
- DATA_REMEDIATION  
  
====================================================================  
STAGE 10. DATASET_REGISTRATION  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Create canonical dataset identity and snapshot records.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- prepared dataset passes readiness gates  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- prepared dataset refs  
- row counts  
- metadata  
- split metadata  
- lineage metadata  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- register_dataset  
- create_dataset_snapshot  
- register_dataset_split  
- create_sample_reference  
- create_lineage_reference  
- patch_workflow_state  
- route_next_stage  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- dataset_id  
- dataset_snapshot_id  
- split refs  
- sample refs  
- lineage refs  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "dataset_id": "string",  
  "dataset_snapshot_id": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If registry or storage failure:  
- STAGE_FAILURE_DATASET_REGISTRATION  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
None by default  
  
RETRY RULES  
--------------------------------------------------------------------  
- limited retry with idempotency checks  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- FEATURE_ENGINEERING or FINE_CLASSING depending project setup  
  
====================================================================  
STAGE 11. FEATURE_ENGINEERING  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Create governed feature set and register metadata/lineage.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- dataset_snapshot_id exists  
- feature rules/config exists  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- dataset_snapshot_id  
- feature rules  
- grouping/lag/diff/encoding specs  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- apply_feature_transformations  
- build_feature_lags  
- build_feature_differences  
- build_grouped_features  
- encode_categorical_features  
- register_feature_metadata  
- register_feature_lineage  
- create_checkpoint  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- feature set refs  
- feature catalog refs  
- feature lineage refs  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "feature_engineering_completed": true,  
  "feature_set_ref": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If transform failure:  
- STAGE_FAILURE_FEATURE_ENGINEERING  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
None by default  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry after rule correction  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- FINE_CLASSING  
- FEATURE_SHORTLIST_BUILD for non-scorecard future paths  
  
====================================================================  
STAGE 12. FINE_CLASSING  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Create initial fine bins for scorecard variables.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- scorecard workflow active  
- dataset and target available  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- dataset_snapshot_id  
- variable list  
- target column  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- build_fine_bins  
- register_artifact  
- create_candidate_version  
- route_next_stage  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- fine bin refs  
- fine bin summary  
- candidate version optional  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "fine_bin_ref": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If variable/target issues:  
- STAGE_FAILURE_FINE_CLASSING  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
None  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- COARSE_CLASSING_CANDIDATE_BUILD  
  
====================================================================  
STAGE 13. COARSE_CLASSING_CANDIDATE_BUILD  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Generate coarse classing candidates to be reviewed.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- fine_bin_ref exists  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- fine_bin_ref  
- merge rules  
- support rules  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- build_coarse_bin_candidate  
- compare_binning_candidates  
- create_candidate_version  
- evaluate_metric_set_against_policy  
- detect_policy_breaches  
- requires_human_review  
- create_review  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- candidate_version_ids  
- comparison summary  
- policy/breach summary  
- review trigger if needed  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "coarse_bin_candidate_ids": []  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If no viable candidates:  
- COARSE_CLASSING_RULE_REWORK  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
- COARSE_CLASSING_REVIEW  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry with adjusted merge rules  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- COARSE_CLASSING_REVIEW  
  
====================================================================  
STAGE 14. COARSE_CLASSING_REVIEW  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Human-in-the-loop review and finalization of coarse bins.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- at least one coarse bin candidate exists  
- review created or policy requires review  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- governance  
- approver  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- review_id  
- candidate refs  
- preview artifacts  
- warnings/support summaries  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- get_review  
- build_review_payload  
- validate_review_action  
- preview_edited_bins  
- approve_review  
- approve_review_with_conditions  
- escalate_review  
- capture_review_decision  
- finalize_coarse_bins  
- patch_workflow_state  
- route_next_stage  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- final coarse bin artifact ref  
- review decision  
- conditions if any  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "coarse_bin_artifact_ref": "string",  
  "coarse_classing_finalized": true  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If rejected:  
- COARSE_CLASSING_CANDIDATE_BUILD  
- COARSE_CLASSING_RULE_REWORK  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
This stage is the review stage  
  
RETRY RULES  
--------------------------------------------------------------------  
- preview may retry  
- final approval/finalization limited  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- WOE_IV_ANALYSIS  
  
====================================================================  
STAGE 15. WOE_IV_ANALYSIS  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Compute WOE/IV using final coarse bins.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- coarse_bin_artifact_ref exists  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- coarse_bin_ref  
- target ref  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- compute_woe_iv  
- register_artifact  
- route_next_stage  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- WOE/IV artifact refs  
- variable summaries  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "woe_iv_ref": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If WOE/IV calculation fails:  
- STAGE_FAILURE_WOE_IV  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
None  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- FEATURE_SHORTLIST_BUILD  
  
====================================================================  
STAGE 16. FEATURE_SHORTLIST_BUILD  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Build variable shortlist from WOE/IV and rules.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- woe_iv_ref exists  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- woe_iv_ref  
- shortlist rules  
- optional correlation/VIF or business rules in future  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- build_feature_shortlist  
- compare_candidates  
- create_candidate_version  
- create_review  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- shortlist candidates  
- shortlist summary  
- review trigger if needed  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "feature_shortlist_candidates": []  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If no valid shortlist:  
- FEATURE_SHORTLIST_RULE_REWORK  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
- FEATURE_SHORTLIST_REVIEW if policy requires  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry with updated shortlist rules  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- FEATURE_SHORTLIST_REVIEW  
- MODEL_FIT_CANDIDATES if no review required  
  
====================================================================  
STAGE 17. FEATURE_SHORTLIST_REVIEW  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Governed review of shortlisted variables.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- shortlist candidate exists  
- review required by policy or user choice  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- governance  
- approver  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- review_id  
- shortlist candidates  
- rationale summaries  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- get_review  
- build_review_payload  
- validate_review_action  
- approve_review  
- approve_review_with_conditions  
- escalate_review  
- capture_review_decision  
- patch_workflow_state  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- approved shortlist ref  
- review decision  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "feature_shortlist_ref": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If rejected:  
- FEATURE_SHORTLIST_BUILD  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
This stage is the review stage  
  
RETRY RULES  
--------------------------------------------------------------------  
- finalization limited  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- MODEL_FIT_CANDIDATES  
  
====================================================================  
STAGE 18. MODEL_FIT_CANDIDATES  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Fit multiple candidate models for comparison.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- feature_shortlist_ref exists  
- dataset_snapshot_id exists  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- dataset_snapshot_id  
- feature_shortlist_ref  
- model specs  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- fit_scorecard_candidate_set  
- compute_metrics  
- run_diagnostics  
- create_candidate_version  
- compare_candidates  
- create_checkpoint  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- candidate_version_ids  
- metrics  
- diagnostics  
- comparison summary  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "model_candidate_ids": []  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If fitting fails materially:  
- MODEL_SPEC_REWORK  
- FEATURE_SHORTLIST_BUILD  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
- MODEL_SELECTION_REVIEW  
  
RETRY RULES  
--------------------------------------------------------------------  
- limited retry with new candidate versioning  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- MODEL_SELECTION_REVIEW  
  
====================================================================  
STAGE 19. MODEL_SELECTION_REVIEW  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Governed review and final selection of model candidate.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- model candidates fitted  
- comparison summary available  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- governance  
- approver  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- candidate refs  
- metrics  
- diagnostics  
- review payload  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- get_review  
- build_review_payload  
- compare_candidates  
- validate_review_action  
- approve_review  
- approve_review_with_conditions  
- escalate_review  
- capture_review_decision  
- select_candidate_version  
- patch_workflow_state  
- route_next_stage  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- selected_candidate_version_id  
- review decision  
- approved conditions if any  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "selected_candidate_version_id": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If rejected:  
- MODEL_FIT_CANDIDATES  
- FEATURE_SHORTLIST_BUILD  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
This stage is the review stage  
  
RETRY RULES  
--------------------------------------------------------------------  
- compare/re-read allowed  
- final selection limited  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- SCORE_SCALING_AND_BANDING  
  
====================================================================  
STAGE 20. SCORE_SCALING_AND_BANDING  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Scale final scorecard and define score bands.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- selected_candidate_version_id exists  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
- governance optionally  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- selected candidate ref  
- scaling spec  
- band spec  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- scale_scorecard  
- build_score_bands  
- compute_metrics  
- evaluate_thresholds  
- create_review  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- score scaling ref  
- score band ref  
- policy summary if needed  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "score_scaling_ref": "string",  
  "score_band_ref": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If scaling/banding unsuitable:  
- MODEL_SELECTION_REVIEW or SCALING_RULE_REWORK  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
Optional:  
- SCORE_SCALING_REVIEW  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry with changed specs  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- SCORECARD_OUTPUT_BUNDLE  
  
====================================================================  
STAGE 21. SCORECARD_OUTPUT_BUNDLE  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Assemble final scorecard artifacts.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- selected candidate exists  
- scaling/band refs exist if required  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- selected candidate ref  
- bin refs  
- WOE/IV ref  
- shortlist ref  
- scaling ref  
- band ref  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- build_scorecard_output_bundle  
- register_artifact  
- build_technical_report  
- route_next_stage  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- final scorecard bundle  
- report section refs optional  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "scorecard_output_bundle_ref": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If missing artifacts:  
- previous producing stage as applicable  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
None by default  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- VALIDATION_SCOPE_INIT  
  
====================================================================  
STAGE 22. VALIDATION_SCOPE_INIT  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Initialize validation run and validation scope.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- final model output bundle exists  
- validation not yet initialized  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- validator  
- governance  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- project_id  
- model refs  
- validation scope config  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- create_validation_scope  
- load_policy_pack  
- get_stage_controls  
- create_review optional  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- validation_run_id  
- scope summary  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "validation_run_id": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If scope invalid:  
- VALIDATION_SCOPE_REWORK  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
Optional:  
- VALIDATION_SCOPE_REVIEW  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- VALIDATION_EVIDENCE_INTAKE  
  
====================================================================  
STAGE 23. VALIDATION_EVIDENCE_INTAKE  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Collect and classify evidence for validation.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- validation_run_id exists  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- validator  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- validation_run_id  
- evidence artifact refs  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- intake_validation_evidence  
- assess_evidence_completeness  
- search_knowledge  
- retrieve_context  
- build_context_pack  
- route_next_stage  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- evidence inventory  
- completeness summary  
- retrieval pack optional  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "validation_evidence_intake_completed": true  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If missing evidence severe:  
- EVIDENCE_REQUEST_REMEDIATION  
- EVIDENCE_COMPLETENESS_REVIEW  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
If completeness materially insufficient:  
- EVIDENCE_COMPLETENESS_REVIEW  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry after more evidence added  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- METHODOLOGY_REVIEW  
- DATA_VALIDATION_REVIEW  
  
====================================================================  
STAGE 24. METHODOLOGY_REVIEW  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Challenge model methodology and assumptions.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- evidence intake completed  
- methodology artifacts available  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- validator  
- governance  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- methodology artifacts  
- prior knowledge context  
- review payload  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- get_review  
- build_review_payload  
- build_context_pack  
- retrieve_context  
- create_validation_finding  
- assess_finding_severity  
- approve_review  
- approve_review_with_conditions  
- escalate_review  
- capture_review_decision  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- methodology findings  
- reviewed methodology notes  
- decision to continue or escalate  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "methodology_review_completed": true  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If severe methodology concerns:  
- REMEDIATION_ACTION_SETUP  
- GOVERNANCE_ESCALATION_REVIEW  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
This stage is inherently review-oriented  
  
RETRY RULES  
--------------------------------------------------------------------  
- retrieval can retry  
- final decision limited  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- DATA_VALIDATION_REVIEW  
- FITNESS_REVIEW  
  
====================================================================  
STAGE 25. DATA_VALIDATION_REVIEW  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Challenge data adequacy, quality, and implementation of data.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- validation evidence exists  
- data artifacts available  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- validator  
- governance  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- data artifacts  
- DQ summaries  
- review payload  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- run_schema_checks  
- run_missingness_checks  
- run_consistency_checks  
- build_dq_summary  
- create_validation_finding  
- assess_finding_severity  
- get_review  
- build_review_payload  
- capture_review_decision  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- data findings  
- reviewed data notes  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "data_validation_review_completed": true  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If severe data issues:  
- REMEDIATION_ACTION_SETUP  
- DATA_REMEDIATION  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
This stage is review-oriented  
  
RETRY RULES  
--------------------------------------------------------------------  
- checks may retry after refreshed evidence  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- FITNESS_REVIEW  
  
====================================================================  
STAGE 26. FITNESS_REVIEW  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Assess fit-for-use dimensions using findings, evidence, and metrics.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- methodology and data review sufficiently advanced  
- key metrics available  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- validator  
- governance  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- findings  
- metrics  
- evidence summary  
- benchmark refs optional  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- evaluate_fitness_dimensions  
- compare_to_benchmark  
- build_review_payload  
- get_review  
- create_validation_finding  
- assess_finding_severity  
- capture_review_decision  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- fitness summary  
- additional findings if necessary  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "fitness_review_completed": true,  
  "fitness_summary_ref": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If insufficient evidence:  
- VALIDATION_EVIDENCE_INTAKE  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
May be wrapped in a governed review depending policy  
  
RETRY RULES  
--------------------------------------------------------------------  
- analytical recompute allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- VALIDATION_CONCLUSION_REVIEW  
  
====================================================================  
STAGE 27. VALIDATION_CONCLUSION_REVIEW  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Human validator chooses final validation conclusion.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- fitness summary exists  
- findings summary exists  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- validator  
- governance  
- approver if required  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- validation_run_id  
- conclusion options  
- findings  
- fitness summary  
- review payload  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- build_validation_conclusion_options  
- get_review  
- build_review_payload  
- validate_review_action  
- approve_review  
- approve_review_with_conditions  
- escalate_review  
- capture_review_decision  
- finalize_validation_conclusion  
- create_remediation_action  
- patch_workflow_state  
- route_next_stage  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- final validation conclusion  
- conditions  
- remediation requirements if any  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "validation_conclusion_id": "string",  
  "validation_status": "finalized"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If conclusion blocked:  
- FITNESS_REVIEW  
- REMEDIATION_ACTION_SETUP  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
This is the final review stage  
  
RETRY RULES  
--------------------------------------------------------------------  
- option generation can retry  
- final conclusion limited  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
If fit for use:  
- REPORTING_TECHNICAL  
- COMMITTEE_PACK_BUILD  
  
If remediation required:  
- REMEDIATION_ACTION_SETUP  
  
====================================================================  
STAGE 28. REMEDIATION_ACTION_SETUP  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Define actions, owners, and due dates for remediation.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- material finding exists  
or  
- validation conclusion requires remediation  
or  
- monitoring breach requires action  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- validator  
- governance  
- approver  
- monitoring for monitoring cases  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- finding_id or breach context  
- remediation payload  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- create_remediation_action  
- create_review  
- approve_review  
- approve_review_with_conditions  
- patch_workflow_state  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- remediation action refs  
- owners and due dates  
- state patch  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "remediation_required": true,  
  "remediation_action_ids": []  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If assignment fails:  
- REMEDIATION_ASSIGNMENT_REWORK  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
Optional to mandatory depending policy  
  
RETRY RULES  
--------------------------------------------------------------------  
- limited retry  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- REPORTING_TECHNICAL  
- MONITORING_SNAPSHOT_INGEST later for closure tracking  
  
====================================================================  
STAGE 29. REPORTING_TECHNICAL  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Build technical documentation outputs.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- model or validation outputs available  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- developer  
- validator  
- governance  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- scorecard/model bundle  
- validation bundle  
- narrative blocks  
- chart/table refs  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- build_technical_report  
- get_narrative_block  
- export_chart_refs  
- export_table_refs  
- assemble_pack  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- technical report section refs  
- pack refs  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "technical_report_ref": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If missing narrative/artifacts:  
- REPORTING_CONTENT_REWORK  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
Optional technical review  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- COMMITTEE_PACK_BUILD  
- KNOWLEDGE_CAPTURE  
  
====================================================================  
STAGE 30. COMMITTEE_PACK_BUILD  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Build executive and committee-facing output pack.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- technical and validation outputs available  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- governance  
- validator  
- approver  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- technical report refs  
- validation note refs  
- executive summary context  
- committee pack context  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- build_executive_summary  
- build_committee_pack  
- build_validation_note  
- assemble_pack  
- create_review  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- committee pack ref  
- executive summary ref  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "committee_pack_ref": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If incomplete sections:  
- REPORTING_TECHNICAL  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
Optional:  
- COMMITTEE_PACK_REVIEW  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- APPROVAL_SIGNOFF  
- KNOWLEDGE_CAPTURE  
  
====================================================================  
STAGE 31. KNOWLEDGE_CAPTURE  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Capture reusable knowledge from events, decisions, and conclusions.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- meaningful governed output exists  
- final or major milestone decision recorded  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- system  
- validator  
- governance  
- developer  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- event refs  
- decision refs  
- conclusion refs  
- summary payloads  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- create_knowledge_object  
- register_knowledge  
- capture_knowledge_from_event  
- capture_knowledge_from_decision  
- set_knowledge_quality_status  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- knowledge object refs  
- quality status  
- scope classification  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "knowledge_capture_completed": true  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If capture fails:  
- KNOWLEDGE_CAPTURE_RETRY or manual defer  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
Promotion usually later, not capture itself  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- KNOWLEDGE_PROMOTION  
- MONITORING_SNAPSHOT_INGEST  
- APPROVAL_SIGNOFF  
  
====================================================================  
STAGE 32. KNOWLEDGE_PROMOTION  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Promote knowledge from project scope to broader reusable scope.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- knowledge object exists  
- quality status eligible for promotion  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- governance  
- approver  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- knowledge_id  
- target scope  
- review notes  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- search_knowledge  
- set_knowledge_quality_status  
- promote_knowledge  
- create_review  
- approve_review  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- promoted knowledge scope  
- promotion decision  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "knowledge_promoted": true  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If not eligible:  
- remain in project scope  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
Usually review/approval required  
  
RETRY RULES  
--------------------------------------------------------------------  
- limited retry  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- APPROVAL_SIGNOFF or end-of-cycle  
  
====================================================================  
STAGE 33. MONITORING_SNAPSHOT_INGEST  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Ingest new periodic monitoring snapshot.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- model in production or monitoring scope  
- new snapshot available  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- monitoring  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- model_id  
- snapshot payload  
- monitoring template  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- get_monitoring_template  
- ingest_monitoring_snapshot  
- validate_monitoring_snapshot  
- append_monitoring_snapshot  
- patch_workflow_state  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- snapshot_id  
- monitoring history updated  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "latest_monitoring_snapshot_id": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If invalid snapshot:  
- MONITORING_SNAPSHOT_REMEDIATION  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
None by default  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry with idempotent snapshot keys  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- MONITORING_KPI_REFRESH  
  
====================================================================  
STAGE 34. MONITORING_KPI_REFRESH  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Compute monitoring metrics, drift, and dashboard payloads.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- latest snapshot appended  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- monitoring  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- snapshot ref  
- baseline refs  
- threshold pack  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- compute_monitoring_metrics  
- evaluate_monitoring_thresholds  
- compute_monitoring_drift  
- compute_segment_monitoring  
- build_dashboard_payload  
- build_dashboard_config  
- route_next_stage  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- KPI summary  
- drift summary  
- breach summary  
- dashboard payload  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "monitoring_refresh_completed": true  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If metric or drift calc fails:  
- STAGE_FAILURE_MONITORING_REFRESH  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
If breach exists:  
- MONITORING_BREACH_REVIEW  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
If no breach:  
- MONITORING_DASHBOARD_VIEW  
  
If breach:  
- MONITORING_BREACH_REVIEW  
  
====================================================================  
STAGE 35. MONITORING_BREACH_REVIEW  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Governed handling of material monitoring breach.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- monitoring breach summary exists  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- monitoring  
- governance  
- approver  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- breach summary  
- KPI summaries  
- dashboard payload  
- review payload  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- create_review  
- get_review  
- build_review_payload  
- validate_review_action  
- approve_review  
- approve_review_with_conditions  
- escalate_review  
- capture_review_decision  
- create_monitoring_note  
- create_remediation_action  
- patch_workflow_state  
- route_next_stage  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- breach disposition  
- action notes  
- remediation setup if required  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "monitoring_breach_review_completed": true,  
  "monitoring_breach_status": "accepted | action_required | escalated"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If no resolution:  
- GOVERNANCE_ESCALATION_REVIEW  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
This is the review stage  
  
RETRY RULES  
--------------------------------------------------------------------  
- note/action edits may retry  
- final disposition limited  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- MONITORING_DASHBOARD_VIEW  
- REMEDIATION_ACTION_SETUP  
- ANNUAL_REVIEW_BUILD  
  
====================================================================  
STAGE 36. MONITORING_DASHBOARD_VIEW  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Operational read/annotate workspace for monitoring.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- dashboard payload exists  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- monitoring  
- governance  
- validator  
- approver  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- dashboard payload  
- dashboard config  
- latest breach notes  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- build_dashboard_payload  
- build_dashboard_config  
- create_monitoring_note  
- build_flow_timeline  
- get_flow_drilldown_payload  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- refreshed dashboard  
- optional notes/actions  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
Usually none  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If payload broken:  
- MONITORING_KPI_REFRESH  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
No mandatory review, but note creation may be governed  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- ANNUAL_REVIEW_BUILD  
- next periodic MONITORING_SNAPSHOT_INGEST  
  
====================================================================  
STAGE 37. ANNUAL_REVIEW_BUILD  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Build annual review evidence pack from monitoring history.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- sufficient monitoring history available  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- monitoring  
- governance  
- validator  
- system  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- model_id  
- date range  
- monitoring history  
- action logs  
- flow summaries  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- build_annual_review_pack  
- build_executive_summary  
- build_committee_pack  
- assemble_pack  
- summarize_flow  
- create_review  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- annual review pack  
- executive summary  
- committee pack if needed  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "annual_review_pack_ref": "string"  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If insufficient history:  
- ANNUAL_REVIEW_DATA_GAP_REMEDIATION  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
Often:  
- ANNUAL_REVIEW_GOVERNANCE_REVIEW  
  
RETRY RULES  
--------------------------------------------------------------------  
- safe retry allowed  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- APPROVAL_SIGNOFF  
- ANNUAL_REVIEW_GOVERNANCE_REVIEW  
  
====================================================================  
STAGE 38. APPROVAL_SIGNOFF  
====================================================================  
  
STAGE PURPOSE  
--------------------------------------------------------------------  
Formal approval or signoff of governed outputs.  
  
ENTRY CRITERIA  
--------------------------------------------------------------------  
- committee pack or final governed review complete  
- approval path active  
  
PRIMARY ACTOR ROLES  
--------------------------------------------------------------------  
- approver  
- governance  
  
INPUT REFERENCES  
--------------------------------------------------------------------  
- review refs  
- pack refs  
- decision refs  
- approval requirements  
  
ALLOWED TOOLS  
--------------------------------------------------------------------  
- get_review  
- build_review_payload  
- can_actor_approve  
- approve_review  
- approve_review_with_conditions  
- register_signoff  
- patch_workflow_state  
- route_next_stage  
  
EXPECTED OUTPUTS  
--------------------------------------------------------------------  
- approval record  
- signoff record  
- final workflow closure state  
  
WORKFLOW PATCH  
--------------------------------------------------------------------  
{  
  "approval_status": "approved | approved_with_conditions",  
  "signoff_completed": true  
}  
  
FAILURE ROUTES  
--------------------------------------------------------------------  
If not approved:  
- GOVERNANCE_ESCALATION_REVIEW  
- REMEDIATION_ACTION_SETUP  
  
REVIEW ROUTES  
--------------------------------------------------------------------  
This is the final approval stage  
  
RETRY RULES  
--------------------------------------------------------------------  
- very limited, ideally idempotent once approved  
  
NEXT-STAGE ROUTES  
--------------------------------------------------------------------  
- WORKFLOW_CLOSED  
- REMEDIATION_ACTION_SETUP if conditional or rejected  
  
====================================================================  
FAILURE / RECOVERY STAGES  
====================================================================  
  
--------------------------------------------------------------------  
STAGE_FAILURE_BOOTSTRAP  
--------------------------------------------------------------------  
Purpose:  
Handle session/project bootstrap failures.  
  
Allowed Tools:  
- replay_run  
- resolve_recovery_path  
- create_review optional  
- open_session  
- resume_session  
  
Next Routes:  
- SESSION_BOOTSTRAP  
- WORKFLOW_BOOTSTRAP  
- GOVERNANCE_ESCALATION_REVIEW if repeated issue  
  
--------------------------------------------------------------------  
STAGE_FAILURE_DATAPREP_EXECUTION  
--------------------------------------------------------------------  
Purpose:  
Handle technical dataprep execution failure.  
  
Allowed Tools:  
- resolve_recovery_path  
- create_checkpoint  
- create_review optional  
- patch_workflow_state  
  
Next Routes:  
- DATA_PREPARATION_EXECUTION  
- DATA_PREPARATION_CONFIG  
- RECOVERY_TECHNICAL_RERUN  
  
--------------------------------------------------------------------  
STAGE_FAILURE_FEATURE_ENGINEERING  
--------------------------------------------------------------------  
Purpose:  
Handle failed feature generation.  
  
Allowed Tools:  
- resolve_recovery_path  
- patch_workflow_state  
- create_review optional  
  
Next Routes:  
- FEATURE_ENGINEERING  
- DATASET_REGISTRATION  
  
--------------------------------------------------------------------  
STAGE_FAILURE_MONITORING_REFRESH  
--------------------------------------------------------------------  
Purpose:  
Handle monitoring refresh failure.  
  
Allowed Tools:  
- resolve_recovery_path  
- create_monitoring_note  
- patch_workflow_state  
  
Next Routes:  
- MONITORING_KPI_REFRESH  
- MONITORING_SNAPSHOT_INGEST  
  
====================================================================  
CROSS-STAGE RULES  
====================================================================  
  
RULE 1  
--------------------------------------------------------------------  
No finalization tool should be callable if:  
- required review does not exist  
- actor role is insufficient  
- policy says blocked  
- workflow state is stale  
  
RULE 2  
--------------------------------------------------------------------  
Every stage that creates a major artifact should:  
- emit an event  
- return artifact refs  
- provide next-step hints  
  
RULE 3  
--------------------------------------------------------------------  
Every stage that records a governed decision should:  
- write audit  
- emit event  
- patch workflow state  
- preserve actor identity  
  
RULE 4  
--------------------------------------------------------------------  
Retrieval is supplemental, not authoritative.  
Source of truth remains:  
- registries  
- artifacts  
- workflow state  
- review records  
- audit records  
  
RULE 5  
--------------------------------------------------------------------  
System actor may automate deterministic steps, but must never simulate:  
- human approval  
- human conclusion  
- governance signoff  
  
====================================================================  
RECOMMENDED NEXT ARTIFACT  
====================================================================  
  
The next strongest deliverable is a:  
  
RUNTIME DECISION TABLE  
  
For each stage and role:  
- allowed tool names  
- required inputs present?  
- review already open?  
- approval required?  
- audit required?  
- can continue automatically?  
- recommended UI mode  
- recommended interaction mode  
  
That would become the direct implementation spec for the runtime  
resolver and allowlist engine.  
  
====================================================================  
END OF STAGE-BY-STAGE ORCHESTRATION PLAYBOOK  
====================================================================  
