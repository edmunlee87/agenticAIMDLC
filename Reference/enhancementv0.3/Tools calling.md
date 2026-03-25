# Tools calling   
  
====================================================================  
TOOL ALLOWLIST MATRIX  
AGENTIC AI MDLC FRAMEWORK  
RUNTIME GOVERNANCE REFERENCE  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This matrix defines which tools are allowed at which workflow stages,  
under which actor roles, and with what governance constraints.  
  
It is designed to support:  
- runtime resolver  
- allowlist resolver  
- agent bridge  
- policy enforcement  
- HITL controls  
- audit discipline  
- safe retry strategy  
  
This is the practical runtime safety layer for the platform.  
  
====================================================================  
HOW TO USE THIS MATRIX  
====================================================================  
  
At runtime, the platform should determine:  
1. current actor role  
2. current domain  
3. current stage  
4. current workflow mode  
5. policy mode  
6. whether a review is already active  
7. whether the stage is read-only, build-only, or decision-capable  
  
Then the AllowlistResolver should use this matrix to decide:  
- which tools are callable  
- which tools are blocked  
- whether HITL is mandatory  
- whether audit is mandatory  
- whether retry is permitted  
- whether only controller tools may be called  
  
====================================================================  
TOOL ACCESS MODES  
====================================================================  
  
Mode meanings:  
  
READ_ONLY  
- Only inspection and retrieval tools allowed  
- No state mutation  
- No artifact finalization  
- No selection / conclusion / approval  
  
BUILD_ONLY  
- Deterministic construction tools allowed  
- Can create candidates or artifacts  
- Cannot finalize governed decisions without review  
  
REVIEW_REQUIRED  
- Review tools allowed  
- Final state changes require review or approval path  
- Usually used after candidates / findings / breaches exist  
  
FINALIZATION_GATED  
- Only bounded decision tools allowed  
- Finalization requires actor role and audit compliance  
  
MONITORING_OPERATIONAL  
- Monitoring refresh and note tools allowed  
- Breach actions may require review  
  
====================================================================  
GLOBAL ROLE CLUSTERS  
====================================================================  
  
Primary role clusters:  
- developer  
- validator  
- monitoring  
- governance  
- approver  
- system  
  
Role interpretation:  
- developer builds, compares, proposes  
- validator challenges, concludes, requests remediation  
- monitoring ingests, refreshes, triages, escalates  
- governance inspects, reviews, signs off, receives packs  
- approver gives formal approval / sign-off where allowed  
- system handles bounded deterministic background platform actions  
  
====================================================================  
GLOBAL TOOL GROUPS  
====================================================================  
  
GROUP A: Session / Runtime / Workflow  
- open_session  
- resume_session  
- resolve_runtime_stack  
- get_workflow_state  
- patch_workflow_state  
- route_next_stage  
- create_candidate_version  
- select_candidate_version  
- create_checkpoint  
- resolve_recovery_path  
  
GROUP B: Review / Policy  
- create_review  
- get_review  
- build_review_payload  
- validate_review_action  
- approve_review  
- approve_review_with_conditions  
- escalate_review  
- capture_review_decision  
- load_policy_pack  
- evaluate_metric_set_against_policy  
- detect_policy_breaches  
- get_stage_controls  
- requires_human_review  
- get_approval_requirements  
- can_actor_approve  
- should_escalate  
- is_waivable  
  
GROUP C: Data / Dataprep / DQ  
- validate_dataprep_config  
- validate_template_request  
- execute_dataprep_request  
- build_cross_sectional_dataset_spark  
- build_panel_dataset_spark  
- build_time_series_dataset_spark  
- build_cohort_dataset_spark  
- build_event_history_dataset_spark  
- run_prep_quality_checks_spark  
- register_dataset  
- create_dataset_snapshot  
- register_dataset_split  
- create_sample_reference  
- create_lineage_reference  
- validate_dataset_contract  
- get_dataset_snapshot  
- run_schema_checks  
- run_missingness_checks  
- run_consistency_checks  
- build_distribution_profile  
- run_business_rule_checks  
- build_dq_summary  
- create_dq_exception  
  
GROUP D: Feature / Evaluation  
- apply_feature_transformations  
- build_feature_lags  
- build_feature_differences  
- build_grouped_features  
- encode_categorical_features  
- register_feature_metadata  
- register_feature_lineage  
- compute_metrics  
- run_diagnostics  
- run_stability_checks  
- run_calibration_checks  
- compare_candidates  
- evaluate_thresholds  
- compare_to_benchmark  
  
GROUP E: Scorecard  
- build_fine_bins  
- build_coarse_bin_candidate  
- preview_edited_bins  
- finalize_coarse_bins  
- compare_binning_candidates  
- compute_woe_iv  
- build_feature_shortlist  
- fit_scorecard_candidate_set  
- scale_scorecard  
- build_score_bands  
- build_scorecard_output_bundle  
  
GROUP F: Validation  
- create_validation_scope  
- intake_validation_evidence  
- assess_evidence_completeness  
- evaluate_fitness_dimensions  
- create_validation_finding  
- assess_finding_severity  
- build_validation_conclusion_options  
- finalize_validation_conclusion  
- create_remediation_action  
- build_validation_output_bundle  
  
GROUP G: Reporting  
- build_technical_report  
- build_executive_summary  
- build_committee_pack  
- build_validation_note  
- get_narrative_block  
- export_chart_refs  
- export_table_refs  
- assemble_pack  
  
GROUP H: Knowledge / Retrieval / Flow / Monitoring  
- create_knowledge_object  
- register_knowledge  
- search_knowledge  
- capture_knowledge_from_event  
- capture_knowledge_from_decision  
- set_knowledge_quality_status  
- promote_knowledge  
- export_knowledge_bundle  
- route_retrieval_query  
- retrieve_context  
- rerank_retrieval_results  
- compress_retrieval_context  
- build_context_pack  
- build_flow_nodes  
- build_flow_edges  
- summarize_flow  
- build_flow_timeline  
- export_flow_graph  
- filter_flow_graph  
- get_flow_drilldown_payload  
- get_monitoring_template  
- ingest_monitoring_snapshot  
- validate_monitoring_snapshot  
- append_monitoring_snapshot  
- compute_monitoring_metrics  
- evaluate_monitoring_thresholds  
- compute_monitoring_drift  
- compute_segment_monitoring  
- build_dashboard_payload  
- build_dashboard_config  
- create_monitoring_note  
- build_annual_review_pack  
- write_monitoring_outputs  
  
====================================================================  
STAGE-LEVEL ALLOWLIST MATRIX  
====================================================================  
  
--------------------------------------------------------------------  
1. SESSION_BOOTSTRAP  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | session_bootstrap |  
| Access Mode | READ_ONLY / ROUTING |  
| Allowed Actor Roles | developer, validator, monitoring, governance, approver, system |  
| Allowed Tools | open_session, resume_session, resolve_runtime_stack, get_workflow_state, route_next_stage, search_knowledge, route_retrieval_query, build_context_pack |  
| Blocked Tools | all finalization tools, all write-heavy domain tools, all approval tools |  
| Mandatory Review | No |  
| Mandatory Audit | No |  
| Retry Allowed | Yes |  
| Notes | Only bootstrap, inspect, and resolve context. No stateful governed decisions here. |  
  
--------------------------------------------------------------------  
2. PROJECT_BOOTSTRAP / WORKFLOW_BOOTSTRAP  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | workflow_bootstrap |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | get_workflow_state, patch_workflow_state, route_next_stage, create_checkpoint, register_project, register_run, load_policy_pack |  
| Blocked Tools | approval/finalization tools, validation conclusion tools, candidate selection tools |  
| Mandatory Review | No |  
| Mandatory Audit | Optional for project/run creation in governed environments |  
| Retry Allowed | Yes |  
| Notes | Keep this bounded to setup and state initialization. |  
  
--------------------------------------------------------------------  
3. DATA_PREPARATION_CONFIG  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | data_preparation_config |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | validate_dataprep_config, validate_template_request, load_policy_pack, get_stage_controls, requires_human_review, build_context_pack, route_next_stage |  
| Blocked Tools | scorecard/model fitting tools, validation finalization tools, monitoring tools |  
| Mandatory Review | Optional, based on policy |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes |  
| Notes | Used to validate prep config and decide if config review is needed. |  
  
--------------------------------------------------------------------  
4. DATA_PREPARATION_EXECUTION  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | data_preparation_execution |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | execute_dataprep_request, build_cross_sectional_dataset_spark, build_panel_dataset_spark, build_time_series_dataset_spark, build_cohort_dataset_spark, build_event_history_dataset_spark, create_checkpoint, write_event |  
| Blocked Tools | review finalization tools, candidate selection, validation conclusion, approval tools |  
| Mandatory Review | No |  
| Mandatory Audit | Optional |  
| Retry Allowed | Limited |  
| Notes | Retry only if outputs are idempotent or safely versioned. |  
  
--------------------------------------------------------------------  
5. DATA_READINESS_CHECK  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | data_readiness_check |  
| Access Mode | BUILD_ONLY / REVIEW_REQUIRED |  
| Allowed Actor Roles | developer, validator, system |  
| Allowed Tools | run_prep_quality_checks_spark, run_schema_checks, run_missingness_checks, run_consistency_checks, build_distribution_profile, run_business_rule_checks, build_dq_summary, validate_dataset_contract, detect_policy_breaches, requires_human_review, create_review |  
| Blocked Tools | model fitting, approval finalization, validation conclusion |  
| Mandatory Review | Policy dependent |  
| Mandatory Audit | Optional if material DQ issue |  
| Retry Allowed | Yes |  
| Notes | Severe DQ findings may force review creation. |  
  
--------------------------------------------------------------------  
6. DATASET_REGISTRATION  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | dataset_registration |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | register_dataset, create_dataset_snapshot, register_dataset_split, create_sample_reference, create_lineage_reference, patch_workflow_state, route_next_stage |  
| Blocked Tools | validation conclusion, approval tools, governance signoff tools |  
| Mandatory Review | No |  
| Mandatory Audit | Optional |  
| Retry Allowed | Limited |  
| Notes | Use idempotent dataset/snapshot creation rules where possible. |  
  
--------------------------------------------------------------------  
7. FEATURE_ENGINEERING  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | feature_engineering |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | apply_feature_transformations, build_feature_lags, build_feature_differences, build_grouped_features, encode_categorical_features, register_feature_metadata, register_feature_lineage, create_checkpoint |  
| Blocked Tools | approval tools, validation conclusion tools, monitoring tools |  
| Mandatory Review | No |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes |  
| Notes | Deterministic feature construction only. |  
  
--------------------------------------------------------------------  
8. FINE_CLASSING  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | fine_classing |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | build_fine_bins, register_artifact, create_candidate_version, route_next_stage |  
| Blocked Tools | approval tools, validation tools, final coarse-bin finalization without review |  
| Mandatory Review | No |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes |  
| Notes | Fine bins are preparatory. Review usually starts at coarse classing. |  
  
--------------------------------------------------------------------  
9. COARSE_CLASSING_CANDIDATE_BUILD  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | coarse_classing_candidate_build |  
| Access Mode | BUILD_ONLY / REVIEW_REQUIRED |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | build_coarse_bin_candidate, compare_binning_candidates, create_candidate_version, evaluate_metric_set_against_policy, detect_policy_breaches, requires_human_review, create_review |  
| Blocked Tools | finalize_coarse_bins directly without review where policy requires HITL |  
| Mandatory Review | Usually Yes |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes |  
| Notes | Candidate generation is allowed, finalization is gated. |  
  
--------------------------------------------------------------------  
10. COARSE_CLASSING_REVIEW  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | coarse_classing_review |  
| Access Mode | REVIEW_REQUIRED |  
| Allowed Actor Roles | developer, governance, approver |  
| Allowed Tools | get_review, build_review_payload, validate_review_action, preview_edited_bins, approve_review, approve_review_with_conditions, escalate_review, capture_review_decision, finalize_coarse_bins, patch_workflow_state, route_next_stage |  
| Blocked Tools | create_validation_scope, finalize_validation_conclusion, monitoring ingestion |  
| Mandatory Review | Yes |  
| Mandatory Audit | Yes for final decision |  
| Retry Allowed | Preview only |  
| Notes | Preview may be retried. Final decision should be idempotent and audited. |  
  
--------------------------------------------------------------------  
11. WOE_IV_ANALYSIS  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | woe_iv_analysis |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | compute_woe_iv, build_distribution_profile, register_artifact, route_next_stage |  
| Blocked Tools | validation conclusion, approval tools |  
| Mandatory Review | No |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes |  
| Notes | Pure analytical stage. |  
  
--------------------------------------------------------------------  
12. FEATURE_SHORTLIST_BUILD  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | feature_shortlist_build |  
| Access Mode | BUILD_ONLY / REVIEW_REQUIRED |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | build_feature_shortlist, compare_candidates, evaluate_thresholds, create_candidate_version, create_review |  
| Blocked Tools | final model selection, approval tools |  
| Mandatory Review | Often Yes |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes |  
| Notes | Shortlist can be proposed automatically, but often requires governed confirmation. |  
  
--------------------------------------------------------------------  
13. FEATURE_SHORTLIST_REVIEW  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | feature_shortlist_review |  
| Access Mode | REVIEW_REQUIRED |  
| Allowed Actor Roles | developer, governance, approver |  
| Allowed Tools | get_review, build_review_payload, validate_review_action, approve_review, approve_review_with_conditions, escalate_review, capture_review_decision, patch_workflow_state, route_next_stage |  
| Blocked Tools | validation-specific tools, monitoring tools |  
| Mandatory Review | Yes |  
| Mandatory Audit | Yes |  
| Retry Allowed | Limited |  
| Notes | Keep action set bounded; no free-form finalization. |  
  
--------------------------------------------------------------------  
14. MODEL_FIT_CANDIDATES  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | model_fit_candidates |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | fit_scorecard_candidate_set, compute_metrics, run_diagnostics, create_candidate_version, compare_candidates, create_checkpoint |  
| Blocked Tools | select_candidate_version directly if policy requires review |  
| Mandatory Review | Usually next stage |  
| Mandatory Audit | Optional |  
| Retry Allowed | Limited |  
| Notes | Candidate fitting is allowed. Final selection usually gated. |  
  
--------------------------------------------------------------------  
15. MODEL_SELECTION_REVIEW  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | model_selection_review |  
| Access Mode | REVIEW_REQUIRED / FINALIZATION_GATED |  
| Allowed Actor Roles | developer, governance, approver |  
| Allowed Tools | get_review, build_review_payload, compare_candidates, validate_review_action, approve_review, approve_review_with_conditions, escalate_review, capture_review_decision, select_candidate_version, patch_workflow_state, route_next_stage |  
| Blocked Tools | validation conclusion tools, monitoring tools |  
| Mandatory Review | Yes |  
| Mandatory Audit | Yes |  
| Retry Allowed | Comparison can be retried, final selection no |  
| Notes | Selection should be explicit and traceable. |  
  
--------------------------------------------------------------------  
16. SCORE_SCALING_AND_BANDING  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | score_scaling_and_banding |  
| Access Mode | BUILD_ONLY / REVIEW_REQUIRED |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | scale_scorecard, build_score_bands, compute_metrics, evaluate_thresholds, create_review |  
| Blocked Tools | validation conclusion, monitoring ingestion |  
| Mandatory Review | Policy dependent |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes |  
| Notes | Review may be required for final score/band cut structure. |  
  
--------------------------------------------------------------------  
17. SCORECARD_OUTPUT_BUNDLE  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | scorecard_output_bundle |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | developer, system |  
| Allowed Tools | build_scorecard_output_bundle, register_artifact, build_technical_report, route_next_stage |  
| Blocked Tools | approval tools unrelated to current stage |  
| Mandatory Review | No |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes |  
| Notes | Bundle should be artifact-driven and reproducible. |  
  
--------------------------------------------------------------------  
18. VALIDATION_SCOPE_INIT  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | validation_scope_init |  
| Access Mode | BUILD_ONLY / REVIEW_REQUIRED |  
| Allowed Actor Roles | validator, governance, system |  
| Allowed Tools | create_validation_scope, load_policy_pack, get_stage_controls, create_review |  
| Blocked Tools | developer-only modeling tools, monitoring tools |  
| Mandatory Review | Policy dependent |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes |  
| Notes | Validation scope may be reviewed where required. |  
  
--------------------------------------------------------------------  
19. VALIDATION_EVIDENCE_INTAKE  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | validation_evidence_intake |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | validator, system |  
| Allowed Tools | intake_validation_evidence, assess_evidence_completeness, search_knowledge, retrieve_context, build_context_pack, route_next_stage |  
| Blocked Tools | final conclusion, approval tools |  
| Mandatory Review | Optional if evidence incomplete |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes |  
| Notes | Knowledge retrieval is highly useful here. |  
  
--------------------------------------------------------------------  
20. METHODOLOGY_REVIEW  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | methodology_review |  
| Access Mode | REVIEW_REQUIRED |  
| Allowed Actor Roles | validator, governance |  
| Allowed Tools | get_review, build_review_payload, build_context_pack, retrieve_context, create_validation_finding, assess_finding_severity, approve_review, approve_review_with_conditions, escalate_review, capture_review_decision |  
| Blocked Tools | developer-only fit/build tools, final validation conclusion |  
| Mandatory Review | Yes |  
| Mandatory Audit | Yes if findings or formal decisions |  
| Retry Allowed | Retrieval yes, final decision limited |  
| Notes | This is a challenge-oriented stage. |  
  
--------------------------------------------------------------------  
21. DATA_VALIDATION_REVIEW  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | data_validation_review |  
| Access Mode | REVIEW_REQUIRED |  
| Allowed Actor Roles | validator, governance |  
| Allowed Tools | run_schema_checks, run_missingness_checks, run_consistency_checks, build_dq_summary, create_validation_finding, assess_finding_severity, get_review, build_review_payload, capture_review_decision |  
| Blocked Tools | final validation conclusion |  
| Mandatory Review | Yes |  
| Mandatory Audit | Yes if formal findings |  
| Retry Allowed | Check tools yes, final decision limited |  
| Notes | DQ and validation findings interact here. |  
  
--------------------------------------------------------------------  
22. FITNESS_REVIEW  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | fitness_review |  
| Access Mode | REVIEW_REQUIRED |  
| Allowed Actor Roles | validator, governance |  
| Allowed Tools | evaluate_fitness_dimensions, compare_to_benchmark, build_review_payload, get_review, create_validation_finding, assess_finding_severity, capture_review_decision |  
| Blocked Tools | finalize_validation_conclusion directly without conclusion review |  
| Mandatory Review | Yes |  
| Mandatory Audit | Yes |  
| Retry Allowed | Analytical tools yes |  
| Notes | Generates structured fitness view for conclusion stage. |  
  
--------------------------------------------------------------------  
23. VALIDATION_CONCLUSION_REVIEW  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | validation_conclusion_review |  
| Access Mode | FINALIZATION_GATED |  
| Allowed Actor Roles | validator, governance, approver |  
| Allowed Tools | build_validation_conclusion_options, get_review, build_review_payload, validate_review_action, approve_review, approve_review_with_conditions, escalate_review, capture_review_decision, finalize_validation_conclusion, create_remediation_action, patch_workflow_state, route_next_stage |  
| Blocked Tools | developer model build tools, monitoring ingestion |  
| Mandatory Review | Yes |  
| Mandatory Audit | Yes |  
| Retry Allowed | Options can be rebuilt, final conclusion no |  
| Notes | Human validator decision is mandatory. |  
  
--------------------------------------------------------------------  
24. REMEDIATION_ACTION_SETUP  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | remediation_action_setup |  
| Access Mode | REVIEW_REQUIRED |  
| Allowed Actor Roles | validator, governance, approver |  
| Allowed Tools | create_remediation_action, create_review, approve_review, assign_monitoring_action, patch_workflow_state |  
| Blocked Tools | developer build tools unless remediation rerun explicitly routed |  
| Mandatory Review | Often Yes |  
| Mandatory Audit | Yes |  
| Retry Allowed | Limited |  
| Notes | This stage creates tracked remediation commitments. |  
  
--------------------------------------------------------------------  
25. REPORTING_TECHNICAL  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | reporting_technical |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | developer, validator, governance, system |  
| Allowed Tools | build_technical_report, get_narrative_block, export_chart_refs, export_table_refs, assemble_pack |  
| Blocked Tools | approval finalization unrelated to reporting |  
| Mandatory Review | Optional |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes |  
| Notes | Artifact-driven reporting only. |  
  
--------------------------------------------------------------------  
26. REPORTING_EXECUTIVE / COMMITTEE_PACK  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | committee_pack_build |  
| Access Mode | BUILD_ONLY / REVIEW_REQUIRED |  
| Allowed Actor Roles | governance, approver, validator, system |  
| Allowed Tools | build_executive_summary, build_committee_pack, build_validation_note, assemble_pack, create_review |  
| Blocked Tools | developer-only dataprep/build tools |  
| Mandatory Review | Often Yes |  
| Mandatory Audit | Optional to Yes depending governance |  
| Retry Allowed | Yes |  
| Notes | Governance-facing output stage. |  
  
--------------------------------------------------------------------  
27. KNOWLEDGE_CAPTURE  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | knowledge_capture |  
| Access Mode | BUILD_ONLY |  
| Allowed Actor Roles | system, validator, governance, developer |  
| Allowed Tools | create_knowledge_object, register_knowledge, capture_knowledge_from_event, capture_knowledge_from_decision, set_knowledge_quality_status |  
| Blocked Tools | promote_knowledge unless role/policy allows |  
| Mandatory Review | Optional for promotion |  
| Mandatory Audit | Optional to Yes for promotion |  
| Retry Allowed | Yes |  
| Notes | Project-level capture is usually allowed; wider promotion is gated. |  
  
--------------------------------------------------------------------  
28. KNOWLEDGE_PROMOTION  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | knowledge_promotion |  
| Access Mode | FINALIZATION_GATED |  
| Allowed Actor Roles | governance, approver |  
| Allowed Tools | search_knowledge, set_knowledge_quality_status, promote_knowledge, create_review, approve_review |  
| Blocked Tools | developer-only build tools |  
| Mandatory Review | Usually Yes |  
| Mandatory Audit | Yes |  
| Retry Allowed | Limited |  
| Notes | Prevent noisy or low-quality memory promotion. |  
  
--------------------------------------------------------------------  
29. RETRIEVAL_SUPPORT  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | retrieval_support |  
| Access Mode | READ_ONLY |  
| Allowed Actor Roles | developer, validator, monitoring, governance, approver, system |  
| Allowed Tools | route_retrieval_query, retrieve_context, rerank_retrieval_results, compress_retrieval_context, build_context_pack, search_knowledge, export_knowledge_bundle |  
| Blocked Tools | any write tool, approval tool, finalization tool |  
| Mandatory Review | No |  
| Mandatory Audit | No |  
| Retry Allowed | Yes |  
| Notes | Retrieval should be scoped and token-thrifty. |  
  
--------------------------------------------------------------------  
30. FLOW_EXPLORER / AUDIT_EXPLORER  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | flow_explorer |  
| Access Mode | READ_ONLY |  
| Allowed Actor Roles | developer, validator, monitoring, governance, approver |  
| Allowed Tools | build_flow_nodes, build_flow_edges, summarize_flow, build_flow_timeline, export_flow_graph, filter_flow_graph, get_flow_drilldown_payload, query_events, replay_run |  
| Blocked Tools | state mutation tools |  
| Mandatory Review | No |  
| Mandatory Audit | No |  
| Retry Allowed | Yes |  
| Notes | Pure inspection stage. |  
  
--------------------------------------------------------------------  
31. MONITORING_SNAPSHOT_INGEST  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | monitoring_snapshot_ingest |  
| Access Mode | MONITORING_OPERATIONAL |  
| Allowed Actor Roles | monitoring, system |  
| Allowed Tools | get_monitoring_template, ingest_monitoring_snapshot, validate_monitoring_snapshot, append_monitoring_snapshot, patch_workflow_state |  
| Blocked Tools | validation conclusion, scorecard build tools |  
| Mandatory Review | No |  
| Mandatory Audit | Optional |  
| Retry Allowed | Yes if snapshot idempotency exists |  
| Notes | Ingestion should be cleanly separated from breach triage. |  
  
--------------------------------------------------------------------  
32. MONITORING_KPI_REFRESH  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | monitoring_kpi_refresh |  
| Access Mode | MONITORING_OPERATIONAL |  
| Allowed Actor Roles | monitoring, system |  
| Allowed Tools | compute_monitoring_metrics, evaluate_monitoring_thresholds, compute_monitoring_drift, compute_segment_monitoring, build_dashboard_payload, build_dashboard_config, route_next_stage |  
| Blocked Tools | approval tools unrelated to monitoring |  
| Mandatory Review | No unless breach |  
| Mandatory Audit | Optional if material breach |  
| Retry Allowed | Yes |  
| Notes | Breach detection may route to review creation. |  
  
--------------------------------------------------------------------  
33. MONITORING_BREACH_REVIEW  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | monitoring_breach_review |  
| Access Mode | REVIEW_REQUIRED / FINALIZATION_GATED |  
| Allowed Actor Roles | monitoring, governance, approver |  
| Allowed Tools | create_review, get_review, build_review_payload, validate_review_action, approve_review, approve_review_with_conditions, escalate_review, capture_review_decision, create_monitoring_note, create_remediation_action, patch_workflow_state, route_next_stage |  
| Blocked Tools | developer-only build tools, validation conclusion tools |  
| Mandatory Review | Yes |  
| Mandatory Audit | Yes |  
| Retry Allowed | Note creation can retry, final decision limited |  
| Notes | This is the main governed monitoring intervention stage. |  
  
--------------------------------------------------------------------  
34. MONITORING_DASHBOARD_VIEW  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | monitoring_dashboard_view |  
| Access Mode | READ_ONLY / MONITORING_OPERATIONAL |  
| Allowed Actor Roles | monitoring, governance, approver, validator |  
| Allowed Tools | build_dashboard_payload, build_dashboard_config, create_monitoring_note, build_flow_timeline, get_flow_drilldown_payload |  
| Blocked Tools | direct model build tools, validation finalization |  
| Mandatory Review | No |  
| Mandatory Audit | Optional for notes/actions |  
| Retry Allowed | Yes |  
| Notes | Mostly read and annotate. |  
  
--------------------------------------------------------------------  
35. ANNUAL_REVIEW_BUILD  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | annual_review_build |  
| Access Mode | BUILD_ONLY / REVIEW_REQUIRED |  
| Allowed Actor Roles | monitoring, governance, validator, system |  
| Allowed Tools | build_annual_review_pack, build_executive_summary, build_committee_pack, assemble_pack, create_review, summarize_flow |  
| Blocked Tools | developer-only build tools |  
| Mandatory Review | Often Yes |  
| Mandatory Audit | Optional to Yes |  
| Retry Allowed | Yes |  
| Notes | Annual review package usually leads to governance review. |  
  
--------------------------------------------------------------------  
36. APPROVAL / SIGNOFF  
--------------------------------------------------------------------  
  
| Field | Value |  
|---|---|  
| Stage Name | approval_signoff |  
| Access Mode | FINALIZATION_GATED |  
| Allowed Actor Roles | approver, governance |  
| Allowed Tools | get_review, build_review_payload, can_actor_approve, approve_review, approve_review_with_conditions, register_signoff, patch_workflow_state, route_next_stage |  
| Blocked Tools | developer build tools, validator-only conclusion tools unless explicitly allowed |  
| Mandatory Review | Yes |  
| Mandatory Audit | Yes |  
| Retry Allowed | Very limited |  
| Notes | Final sign-off path must stay tightly controlled. |  
  
====================================================================  
ROLE-TOOL OVERRIDE RULES  
====================================================================  
  
These rules apply across all stages.  
  
--------------------------------------------------------------------  
Rule 1: developer  
--------------------------------------------------------------------  
Allowed to:  
- build  
- compare  
- propose  
- create candidate versions  
- create many reviews  
- respond within permitted review stages  
  
Not allowed to:  
- finalize validation conclusion unless explicitly allowed  
- approve where approval role is required  
- promote knowledge beyond allowed scope without governance approval  
  
--------------------------------------------------------------------  
Rule 2: validator  
--------------------------------------------------------------------  
Allowed to:  
- create validation findings  
- assess evidence completeness  
- evaluate fitness  
- finalize validation conclusion in designated stages  
- request remediation  
  
Not allowed to:  
- perform unrestricted developer build actions in validation-only mode  
- approve governance signoff unless also approver  
  
--------------------------------------------------------------------  
Rule 3: monitoring  
--------------------------------------------------------------------  
Allowed to:  
- ingest monitoring snapshots  
- compute metrics and drift  
- create monitoring notes/actions  
- participate in monitoring breach review  
  
Not allowed to:  
- finalize validation conclusion  
- perform developer-only model build steps  
  
--------------------------------------------------------------------  
Rule 4: governance  
--------------------------------------------------------------------  
Allowed to:  
- inspect  
- review  
- approve where permitted  
- escalate  
- promote knowledge if policy allows  
- assemble governance packs  
  
Not allowed to:  
- run arbitrary developer build tools unless role combination permits  
  
--------------------------------------------------------------------  
Rule 5: approver  
--------------------------------------------------------------------  
Allowed to:  
- approve final governed steps  
- sign off  
- approve with conditions  
  
Not allowed to:  
- mutate technical artifacts unless specific admin/system privileges exist  
  
--------------------------------------------------------------------  
Rule 6: system  
--------------------------------------------------------------------  
Allowed to:  
- perform deterministic non-governed automation  
- bootstrap  
- prepare  
- register  
- calculate  
- refresh dashboards  
- execute retrieval  
  
Not allowed to:  
- simulate human approvals  
- finalize governed conclusions  
- silently bypass review requirements  
  
====================================================================  
GLOBAL BLOCK RULES  
====================================================================  
  
Block Rule A  
--------------------------------------------------------------------  
If review is required and no review exists:  
- block finalization tools  
- allow create_review  
- allow read/inspection tools  
  
Block Rule B  
--------------------------------------------------------------------  
If actor role does not satisfy approval requirements:  
- block approve_review  
- block approve_review_with_conditions  
- block signoff tools  
  
Block Rule C  
--------------------------------------------------------------------  
If workflow state is stale or invalid:  
- block mutation tools  
- allow get_workflow_state  
- allow resolve_recovery_path  
- allow replay_run  
  
Block Rule D  
--------------------------------------------------------------------  
If severe DQ or policy breach exists and policy says stop:  
- block downstream build/finalization tools  
- allow create_review  
- allow escalation tools  
- allow reporting / inspection tools  
  
Block Rule E  
--------------------------------------------------------------------  
If annual_review_mode = true:  
- expand monitoring/flow/reporting tools  
- restrict developer build tools unless explicitly routed  
  
====================================================================  
RETRY POLICY MATRIX  
====================================================================  
  
| Tool Category | Retry Default | Notes |  
|---|---|---|  
| Read tools | Yes | Safe to retry |  
| Retrieval tools | Yes | Safe unless backend rate limits |  
| Deterministic analytical tools | Yes | Safe if inputs unchanged |  
| Artifact writes | Limited | Safe only with idempotent naming/versioning |  
| Candidate creation | Limited | Avoid duplicate candidate versions |  
| Finalization tools | No | Only retry with explicit idempotency protection |  
| Approval/signoff tools | No | Must be treated as governed one-way actions |  
| Review preview tools | Yes | Safe to recompute |  
| Monitoring ingestion | Yes with idempotent snapshot key | Important for operational reliability |  
  
====================================================================  
MANDATORY AUDIT RULES  
====================================================================  
  
Audit must be mandatory for:  
- candidate selection  
- final coarse bin finalization  
- validation finding creation where severity is material  
- validation conclusion finalization  
- remediation action creation where due dates/owners are assigned  
- monitoring breach disposition  
- approval and signoff  
- knowledge promotion beyond project scope  
  
Audit usually optional for:  
- metric computation  
- retrieval  
- technical report drafting  
- dataset registration  
- feature metadata registration  
  
====================================================================  
MANDATORY REVIEW RULES  
====================================================================  
  
Review should be mandatory for:  
- coarse classing finalization  
- feature shortlist finalization where policy requires  
- model selection  
- validation conclusion  
- material monitoring breach disposition  
- governance signoff  
- knowledge promotion to broader reusable scope  
  
Review usually optional for:  
- dataprep config approval  
- dataset contract issues  
- DQ exception review  
- scaling/banding review  
- annual review pack approval  
  
====================================================================  
IMPLEMENTATION RECOMMENDATION  
====================================================================  
  
The AllowlistResolver should implement this in three layers:  
  
Layer 1: Stage default allowlist  
- base tool list for stage  
  
Layer 2: Role filter  
- remove tools not permitted for actor role  
  
Layer 3: State / policy overlay  
- remove tools blocked by:  
  - missing review  
  - missing approval right  
  - blocker conditions  
  - stale state  
  - severe breach  
  - annual review mode  
  - remediation mode  
  
Final output should be something like:  
{  
  "allowed_tools": [],  
  "blocked_tools": [],  
  "requires_human_review": false,  
  "requires_approval_role": false,  
  "audit_mandatory": false,  
  "retry_mode": "safe | limited | none"  
}  
  
====================================================================  
NEXT BEST ARTIFACT  
====================================================================  
  
The next strongest deliverable is a:  
  
STAGE-BY-STAGE ORCHESTRATION PLAYBOOK  
  
For each stage:  
- entry criteria  
- allowed tools  
- required artifacts/refs  
- expected outputs  
- failure routes  
- review routes  
- retry rules  
- next-stage routes  
  
That would turn the governance matrix into an execution blueprint.  
  
====================================================================  
END OF TOOL ALLOWLIST MATRIX  
====================================================================  
