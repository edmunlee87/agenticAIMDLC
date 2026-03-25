# Runtime decision  
  
====================================================================  
RUNTIME DECISION TABLE  
AGENTIC AI MDLC FRAMEWORK  
DIRECT IMPLEMENTATION SPEC FOR RUNTIME RESOLVER + ALLOWLIST ENGINE  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This reference translates the orchestration playbook into a direct  
runtime implementation spec.  
  
For each stage and role, it shows:  
- stage  
- actor role  
- access mode  
- preconditions  
- allowed tool groups  
- blocked tool groups  
- whether review is required  
- whether approval is required  
- whether audit is required  
- whether automatic continuation is allowed  
- recommended UI mode  
- recommended interaction mode  
- recommended token mode  
- primary next routes  
  
This is intended to be used by:  
- RuntimeResolver  
- AllowlistResolver  
- UIModeResolver  
- InteractionModeResolver  
- TokenModeResolver  
- AgentBridge  
- JupyterBridge  
- ReviewController  
- WorkflowController  
  
====================================================================  
GLOBAL RUNTIME FIELDS  
====================================================================  
  
Each runtime decision output should look like:  
  
{  
  "stage_name": "string",  
  "actor_role": "string",  
  "access_mode": "READ_ONLY | BUILD_ONLY | REVIEW_REQUIRED | FINALIZATION_GATED | MONITORING_OPERATIONAL",  
  "preconditions_passed": true,  
  "missing_preconditions": [],  
  "allowed_tool_groups": [],  
  "blocked_tool_groups": [],  
  "allowed_tools": [],  
  "blocked_tools": [],  
  "review_required": false,  
  "approval_required": false,  
  "audit_required": false,  
  "auto_continue_allowed": true,  
  "recommended_ui_mode": "chat_only | review_shell | dashboard | flow_explorer | wizard | mixed",  
  "recommended_interaction_mode": "read | build | review | approve | monitor | recover",  
  "recommended_token_mode": "micro_mode | standard_mode | deep_review_mode",  
  "recommended_next_routes": [],  
  "notes": []  
}  
  
====================================================================  
TOOL GROUP REFERENCE  
====================================================================  
  
Tool Group A: Session / Runtime / Workflow  
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
  
Tool Group B: Review / Policy  
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
  
Tool Group C: Data / Dataprep / DQ  
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
  
Tool Group D: Feature / Evaluation  
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
  
Tool Group E: Scorecard  
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
  
Tool Group F: Validation  
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
  
Tool Group G: Reporting  
- build_technical_report  
- build_executive_summary  
- build_committee_pack  
- build_validation_note  
- get_narrative_block  
- export_chart_refs  
- export_table_refs  
- assemble_pack  
  
Tool Group H: Knowledge / Retrieval / Flow / Monitoring  
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
ROLE CAPABILITY SUMMARY  
====================================================================  
  
| Actor Role | Default Capability | Can Build | Can Review | Can Approve | Can Finalize Validation Conclusion | Can Ingest Monitoring | Can Sign Off |  
|---|---|---:|---:|---:|---:|---:|---:|  
| developer | technical builder | Yes | Limited | No | No | No | No |  
| validator | challenger / assessor | Limited | Yes | Limited | Yes | No | No |  
| monitoring | operational monitor | Limited | Yes | Limited | No | Yes | No |  
| governance | control / oversight | Limited | Yes | Yes | Limited | Limited | Limited |  
| approver | formal approver | No | Yes | Yes | No unless dual role | No | Yes |  
| system | bounded automation | Yes, deterministic only | No | No | No | Yes, deterministic only | No |  
  
====================================================================  
A. SESSION + BOOTSTRAP STAGES  
====================================================================  
  
| Stage | Actor Role | Access Mode | Preconditions | Allowed Tool Groups | Blocked Tool Groups | Review Required | Approval Required | Audit Required | Auto Continue Allowed | UI Mode | Interaction Mode | Token Mode | Primary Next Routes |  
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|  
| session_bootstrap | developer | READ_ONLY | actor_id, actor_role | A, H(read-only subset) | C, D, E, F, G(write), H(write) | No | No | No | Yes | wizard | read | micro_mode | workflow_bootstrap, workflow_resume_selection |  
| session_bootstrap | validator | READ_ONLY | actor_id, actor_role | A, H(read-only subset) | C(build), E, monitoring writes | No | No | No | Yes | wizard | read | micro_mode | workflow_bootstrap, workflow_resume_selection |  
| session_bootstrap | monitoring | READ_ONLY | actor_id, actor_role | A, H(read-only subset) | C, D, E, F | No | No | No | Yes | wizard | read | micro_mode | workflow_bootstrap, workflow_resume_selection |  
| session_bootstrap | governance | READ_ONLY | actor_id, actor_role | A, H(read-only subset) | C(build), E(build), monitoring writes | No | No | No | Yes | wizard | read | micro_mode | workflow_bootstrap, workflow_resume_selection |  
| session_bootstrap | approver | READ_ONLY | actor_id, actor_role | A, H(read-only subset) | all build-heavy groups | No | No | No | Yes | wizard | read | micro_mode | workflow_resume_selection |  
| session_bootstrap | system | READ_ONLY | actor_id, actor_role | A | C, D, E, F, G, H(write) | No | No | No | Yes | none | read | micro_mode | workflow_bootstrap |  
  
| Stage | Actor Role | Access Mode | Preconditions | Allowed Tool Groups | Blocked Tool Groups | Review Required | Approval Required | Audit Required | Auto Continue Allowed | UI Mode | Interaction Mode | Token Mode | Primary Next Routes |  
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|  
| workflow_bootstrap | developer | BUILD_ONLY | session_id, project selection | A, B(read policy subset) | E, F, H(monitoring writes) | No | No | Optional | Yes | wizard | build | micro_mode | runtime_stack_resolution |  
| workflow_bootstrap | system | BUILD_ONLY | session_id, project selection | A, B(read policy subset) | B(review/finalize), E, F, G, H | No | No | Optional | Yes | none | build | micro_mode | runtime_stack_resolution |  
| workflow_resume_selection | developer | READ_ONLY | session_id, resume_candidates | A, H(flow subset) | C-E-F-G writes | Optional | No | No | Yes | mixed | recover | micro_mode | runtime_stack_resolution, recovery_review |  
| workflow_resume_selection | validator | READ_ONLY | session_id, resume_candidates | A, H(flow subset) | developer build groups | Optional | No | No | Yes | mixed | recover | micro_mode | runtime_stack_resolution, recovery_review |  
| workflow_resume_selection | monitoring | READ_ONLY | session_id, resume_candidates | A, H(flow subset) | developer/validation build groups | Optional | No | No | Yes | mixed | recover | micro_mode | runtime_stack_resolution, recovery_review |  
| workflow_resume_selection | governance | READ_ONLY | session_id, resume_candidates | A, H(flow subset) | heavy build groups | Optional | No | No | Yes | mixed | recover | micro_mode | runtime_stack_resolution, recovery_review |  
  
====================================================================  
B. DATA PREPARATION + READINESS  
====================================================================  
  
| Stage | Actor Role | Access Mode | Preconditions | Allowed Tool Groups | Blocked Tool Groups | Review Required | Approval Required | Audit Required | Auto Continue Allowed | UI Mode | Interaction Mode | Token Mode | Primary Next Routes |  
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|  
| data_preparation_config | developer | BUILD_ONLY | project_id, run_id, dataprep config draft | A(route subset), B(policy subset), C(config subset), H(retrieval subset) | E, F, monitoring writes | Policy dependent | No | Optional | Yes if valid and no review | mixed | build | standard_mode | data_preparation_execution, data_preparation_config_review |  
| data_preparation_config | system | BUILD_ONLY | project_id, run_id, dataprep config draft | A(route subset), B(policy subset), C(config subset) | all review/finalization tools | No | No | Optional | Yes | none | build | micro_mode | data_preparation_execution |  
| data_preparation_config_review | developer | REVIEW_REQUIRED | config review requested, review payload exists | A(patch/route subset), B(review subset), H(retrieval subset) | C(execution), E, F(finalization), monitoring writes | Yes | Policy dependent | Yes if final review action | No | review_shell | review | standard_mode | data_preparation_execution, data_preparation_config |  
| data_preparation_config_review | governance | REVIEW_REQUIRED | config review requested, review payload exists | A(patch/route subset), B(review subset), H(read-only subset) | C(execution), E, F(finalization) | Yes | Possible | Yes | No | review_shell | review | deep_review_mode | data_preparation_execution, governance_escalation_review |  
| data_preparation_execution | developer | BUILD_ONLY | validated config, supported template, sources reachable | A(checkpoint subset), C(exec subset) | B(finalization), E, F, G, H(monitoring writes) | No | No | Optional | Yes if success | mixed | build | standard_mode | data_readiness_check |  
| data_preparation_execution | system | BUILD_ONLY | validated config, supported template, sources reachable | A(checkpoint subset), C(exec subset) | all review/finalization groups | No | No | Optional | Yes | none | build | micro_mode | data_readiness_check |  
| data_readiness_check | developer | BUILD_ONLY / REVIEW_REQUIRED | prepared dataset ref exists | B(policy subset), C(DQ subset), H(retrieval subset) | E, F(finalization), monitoring writes | Policy dependent | No | Optional, Yes if severe | Yes if pass/no review | mixed | build | standard_mode | dataset_registration, data_readiness_review, data_remediation |  
| data_readiness_check | validator | BUILD_ONLY / REVIEW_REQUIRED | prepared dataset ref exists | B(policy subset), C(DQ subset), H(retrieval subset) | E(build), F(conclusion), monitoring writes | Policy dependent | No | Optional | Yes if pass/no review | mixed | build | deep_review_mode | dataset_registration, data_readiness_review |  
| data_readiness_check | system | BUILD_ONLY | prepared dataset ref exists | B(policy subset), C(DQ subset) | all review finalization tools | No | No | Optional | Yes if pass/no review | none | build | micro_mode | dataset_registration, data_readiness_review |  
| data_readiness_review | developer | REVIEW_REQUIRED | severe DQ/policy issue or manual review requested | A(patch/route subset), B(review subset), C(DQ subset read-only), H(retrieval subset) | C(exec writes), E, F(finalization), monitoring writes | Yes | Policy dependent | Yes | No | review_shell | review | deep_review_mode | dataset_registration, data_remediation |  
| data_readiness_review | validator | REVIEW_REQUIRED | severe DQ/policy issue or manual review requested | A(patch/route subset), B(review subset), C(DQ subset read-only), H(retrieval subset) | developer build-heavy groups, validation conclusion tools | Yes | Possible | Yes | No | review_shell | review | deep_review_mode | dataset_registration, data_remediation |  
| data_readiness_review | governance | REVIEW_REQUIRED | severe DQ/policy issue or manual review requested | A(patch/route subset), B(review subset), H(read-only subset) | build-heavy C/E groups | Yes | Possible | Yes | No | review_shell | review | deep_review_mode | dataset_registration, governance_escalation_review |  
| dataset_registration | developer | BUILD_ONLY | readiness status pass or approved warning, prepared refs present | A(route/patch subset), C(registration subset) | B(final approvals), E, F, H(monitoring writes) | No | No | Optional | Yes | mixed | build | micro_mode | feature_engineering, fine_classing |  
| dataset_registration | system | BUILD_ONLY | readiness status pass or approved warning, prepared refs present | A(route/patch subset), C(registration subset) | all review/finalization groups | No | No | Optional | Yes | none | build | micro_mode | feature_engineering, fine_classing |  
  
====================================================================  
C. FEATURE + SCORECARD DEVELOPMENT  
====================================================================  
  
| Stage | Actor Role | Access Mode | Preconditions | Allowed Tool Groups | Blocked Tool Groups | Review Required | Approval Required | Audit Required | Auto Continue Allowed | UI Mode | Interaction Mode | Token Mode | Primary Next Routes |  
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|  
| feature_engineering | developer | BUILD_ONLY | dataset_snapshot_id, feature rules | A(checkpoint subset), D(feature subset), H(retrieval subset) | B(finalization), E, F, monitoring writes | No | No | Optional | Yes | mixed | build | standard_mode | fine_classing, feature_shortlist_build |  
| feature_engineering | system | BUILD_ONLY | dataset_snapshot_id, feature rules | A(checkpoint subset), D(feature subset) | review/finalization groups | No | No | Optional | Yes | none | build | micro_mode | fine_classing, feature_shortlist_build |  
| fine_classing | developer | BUILD_ONLY | scorecard mode, dataset_snapshot_id, target column | A(route subset), E(fine bins subset), H(retrieval subset) | B(approval), F, monitoring writes | No | No | Optional | Yes | mixed | build | standard_mode | coarse_classing_candidate_build |  
| fine_classing | system | BUILD_ONLY | scorecard mode, dataset_snapshot_id, target column | A(route subset), E(fine bins subset) | review/finalization groups | No | No | Optional | Yes | none | build | micro_mode | coarse_classing_candidate_build |  
| coarse_classing_candidate_build | developer | BUILD_ONLY / REVIEW_REQUIRED | fine_bin_ref exists | A(route/create candidate subset), B(policy subset), D(compare subset), E(candidate subset), H(retrieval subset) | finalize_coarse_bins if review missing, F, monitoring writes | Usually Yes | No | Optional | No if review mandatory | mixed | build | standard_mode | coarse_classing_review |  
| coarse_classing_candidate_build | system | BUILD_ONLY | fine_bin_ref exists | A(route/create candidate subset), B(policy subset), D(compare subset), E(candidate subset) | all review/finalization tools | No | No | Optional | Yes until review trigger | none | build | micro_mode | coarse_classing_review |  
| coarse_classing_review | developer | REVIEW_REQUIRED | active review, candidate refs, payload built | A(patch/route subset), B(review subset), E(preview/finalize subset), H(retrieval subset) | developer unrelated build groups, F finalization, monitoring writes | Yes | Policy dependent | Yes | No | review_shell | review | deep_review_mode | woe_iv_analysis, coarse_classing_candidate_build |  
| coarse_classing_review | governance | REVIEW_REQUIRED / FINALIZATION_GATED | active review, candidate refs, payload built | A(patch/route subset), B(review subset), E(preview/finalize subset read-limited), H(read-only subset) | developer build groups, F finalization | Yes | Possible | Yes | No | review_shell | review | deep_review_mode | woe_iv_analysis, governance_escalation_review |  
| approver in coarse_classing_review | approver | FINALIZATION_GATED | active review, approval required, can_actor_approve true | A(patch/route subset), B(review/approval subset), E(finalize subset if allowed) | all build groups except review-bound finalize | Yes | Yes | Yes | No | review_shell | approve | deep_review_mode | woe_iv_analysis, governance_escalation_review |  
| woe_iv_analysis | developer | BUILD_ONLY | final coarse bin ref exists | A(route subset), E(woe_iv subset), G(read-only refs), H(retrieval subset) | B(final approvals), F, monitoring writes | No | No | Optional | Yes | mixed | build | standard_mode | feature_shortlist_build |  
| feature_shortlist_build | developer | BUILD_ONLY / REVIEW_REQUIRED | woe_iv_ref exists | A(route/create candidate subset), D(compare subset), E(shortlist subset), H(retrieval subset) | final selection without review, F, monitoring writes | Often Yes | No | Optional | No if review mandatory | mixed | build | standard_mode | feature_shortlist_review, model_fit_candidates |  
| feature_shortlist_build | system | BUILD_ONLY | woe_iv_ref exists | A(route/create candidate subset), D(compare subset), E(shortlist subset) | review/finalization groups | No | No | Optional | Yes until review trigger | none | build | micro_mode | feature_shortlist_review, model_fit_candidates |  
| feature_shortlist_review | developer | REVIEW_REQUIRED | shortlist review exists or mandated | A(patch/route subset), B(review subset), H(retrieval subset) | E(build subset except context reads), F, monitoring writes | Yes | Policy dependent | Yes | No | review_shell | review | deep_review_mode | model_fit_candidates, feature_shortlist_build |  
| feature_shortlist_review | governance | REVIEW_REQUIRED | shortlist review exists or mandated | A(patch/route subset), B(review subset), H(read-only subset) | build-heavy E/F/H monitoring writes | Yes | Possible | Yes | No | review_shell | review | deep_review_mode | model_fit_candidates, governance_escalation_review |  
| model_fit_candidates | developer | BUILD_ONLY | approved shortlist, dataset snapshot | A(checkpoint/create candidate subset), D(eval subset), E(fit subset), H(retrieval subset) | select_candidate_version if review required, F, monitoring writes | Usually next stage | No | Optional | Yes | mixed | build | standard_mode | model_selection_review |  
| model_fit_candidates | system | BUILD_ONLY | approved shortlist, dataset snapshot | A(checkpoint/create candidate subset), D(eval subset), E(fit subset) | review/finalization groups | No | No | Optional | Yes | none | build | micro_mode | model_selection_review |  
| model_selection_review | developer | REVIEW_REQUIRED | candidate metrics and review payload exist | A(select/patch/route subset), B(review subset), D(compare/evaluate subset), H(retrieval subset) | developer build-heavy C/E, F finalization, monitoring writes | Yes | Policy dependent | Yes | No | review_shell | review | deep_review_mode | score_scaling_and_banding, model_fit_candidates |  
| model_selection_review | governance | REVIEW_REQUIRED / FINALIZATION_GATED | candidate metrics and review payload exist | A(select/patch/route subset), B(review subset), D(compare/evaluate subset), H(read-only subset) | build-heavy groups | Yes | Possible | Yes | No | review_shell | review | deep_review_mode | score_scaling_and_banding, governance_escalation_review |  
| model_selection_review | approver | FINALIZATION_GATED | approval needed, review active, actor approved | A(select/patch/route subset), B(approval subset), D(compare subset), H(read-only subset) | build groups | Yes | Yes | Yes | No | review_shell | approve | deep_review_mode | score_scaling_and_banding |  
| score_scaling_and_banding | developer | BUILD_ONLY / REVIEW_REQUIRED | selected candidate version exists | A(route subset), D(metrics/threshold subset), E(scale/band subset), H(retrieval subset) | F, monitoring writes | Policy dependent | No | Optional | Yes if no review required | mixed | build | standard_mode | scorecard_output_bundle, score_scaling_review |  
| score_scaling_and_banding | system | BUILD_ONLY | selected candidate version exists | A(route subset), D(metrics/threshold subset), E(scale/band subset) | review/finalization groups | No | No | Optional | Yes | none | build | micro_mode | scorecard_output_bundle |  
| scorecard_output_bundle | developer | BUILD_ONLY | all final scorecard refs available | A(route subset), E(bundle subset), G(reporting subset), H(knowledge capture read-only subset) | F finalization, monitoring writes | No | No | Optional | Yes | mixed | build | micro_mode | validation_scope_init, reporting_technical |  
| scorecard_output_bundle | system | BUILD_ONLY | all final scorecard refs available | A(route subset), E(bundle subset), G(reporting subset) | review/finalization groups | No | No | Optional | Yes | none | build | micro_mode | validation_scope_init, reporting_technical |  
  
====================================================================  
D. VALIDATION STAGES  
====================================================================  
  
| Stage | Actor Role | Access Mode | Preconditions | Allowed Tool Groups | Blocked Tool Groups | Review Required | Approval Required | Audit Required | Auto Continue Allowed | UI Mode | Interaction Mode | Token Mode | Primary Next Routes |  
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|  
| validation_scope_init | validator | BUILD_ONLY / REVIEW_REQUIRED | final model bundle exists | A(route subset), B(policy subset), F(scope subset), H(retrieval subset) | developer build groups, monitoring writes | Policy dependent | No | Optional | Yes if no review required | mixed | build | standard_mode | validation_scope_review, validation_evidence_intake |  
| validation_scope_init | governance | BUILD_ONLY / REVIEW_REQUIRED | final model bundle exists | A(route subset), B(policy subset), F(scope subset read-limited), H(read-only subset) | developer build groups, monitoring writes | Possible | Possible | Optional | Limited | mixed | review | deep_review_mode | validation_scope_review, validation_evidence_intake |  
| validation_evidence_intake | validator | BUILD_ONLY | validation_run_id exists | A(route subset), F(evidence subset), H(retrieval/knowledge subset), G(read-only narrative subset) | developer build groups, final conclusion, monitoring writes | If evidence insufficient maybe | No | Optional | Yes | mixed | build | deep_review_mode | methodology_review, data_validation_review, evidence_completeness_review |  
| validation_evidence_intake | system | BUILD_ONLY | validation_run_id exists | A(route subset), F(evidence subset limited), H(retrieval subset) | review/finalization tools | No | No | Optional | Yes | none | build | micro_mode | methodology_review, data_validation_review |  
| methodology_review | validator | REVIEW_REQUIRED | evidence intake complete, methodology artifacts present | A(route subset), B(review/policy subset), F(finding/severity subset), H(retrieval/knowledge subset) | developer build groups, final conclusion | Yes | No | Yes if finding or formal decision | No | review_shell | review | deep_review_mode | data_validation_review, fitness_review, remediation_action_setup |  
| methodology_review | governance | REVIEW_REQUIRED | evidence intake complete, methodology artifacts present | A(route subset), B(review/policy subset), F(finding subset limited), H(read-only subset) | build-heavy groups, final conclusion | Yes | Possible | Yes | No | review_shell | review | deep_review_mode | fitness_review, governance_escalation_review |  
| data_validation_review | validator | REVIEW_REQUIRED | evidence intake complete, data artifacts present | A(route subset), B(review subset), C(DQ subset), F(finding/severity subset), H(retrieval subset) | developer build groups, final conclusion | Yes | No | Yes if formal findings | No | review_shell | review | deep_review_mode | fitness_review, remediation_action_setup |  
| data_validation_review | governance | REVIEW_REQUIRED | evidence intake complete, data artifacts present | A(route subset), B(review subset), C(DQ read subset), F(finding subset limited), H(read-only subset) | build groups, final conclusion | Yes | Possible | Yes | No | review_shell | review | deep_review_mode | fitness_review, governance_escalation_review |  
| fitness_review | validator | REVIEW_REQUIRED | key findings and metrics available | A(route subset), B(review subset), D(compare/benchmark subset), F(fitness/finding subset), H(retrieval subset) | developer build groups, final conclusion until options created | Yes | No | Yes | No | review_shell | review | deep_review_mode | validation_conclusion_review |  
| fitness_review | governance | REVIEW_REQUIRED | key findings and metrics available | A(route subset), B(review subset), D(compare subset), F(fitness subset limited), H(read-only subset) | build groups, direct conclusion finalization | Yes | Possible | Yes | No | review_shell | review | deep_review_mode | validation_conclusion_review, governance_escalation_review |  
| validation_conclusion_review | validator | FINALIZATION_GATED | fitness summary, findings summary, conclusion options or ability to build them | A(route/patch subset), B(review/approval subset), F(conclusion/remediation/output subset), H(retrieval subset), G(validation note subset read-only) | developer build groups, monitoring writes | Yes | Possibly if governance requires co-approval | Yes | No | review_shell | approve | deep_review_mode | reporting_technical, remediation_action_setup |  
| validation_conclusion_review | governance | FINALIZATION_GATED | fitness summary, findings summary, conclusion options exist | A(route/patch subset), B(review/approval subset), F(conclusion/remediation subset limited), H(read-only subset), G(validation note subset) | developer build groups, monitoring writes | Yes | Often | Yes | No | review_shell | approve | deep_review_mode | reporting_technical, governance_escalation_review |  
| validation_conclusion_review | approver | FINALIZATION_GATED | co-approval required, actor allowed | A(route/patch subset), B(approval subset), F(conclusion subset if policy allows), G(read-only subset) | build groups | Yes | Yes | Yes | No | review_shell | approve | deep_review_mode | reporting_technical, remediation_action_setup |  
| remediation_action_setup | validator | REVIEW_REQUIRED | material finding or conclusion requiring remediation | A(patch subset), B(review/approval subset), F(remediation subset), H(monitoring note subset read-only) | developer build groups, signoff | Often | Possible | Yes | No | review_shell | review | standard_mode | reporting_technical, monitoring_snapshot_ingest |  
| remediation_action_setup | governance | REVIEW_REQUIRED | material finding or conclusion requiring remediation | A(patch subset), B(review/approval subset), F(remediation subset), H(read-only subset) | build groups | Often | Possible | Yes | No | review_shell | review | standard_mode | reporting_technical, governance_escalation_review |  
| remediation_action_setup | monitoring | REVIEW_REQUIRED | monitoring breach or operational issue requiring action | A(patch subset), B(review subset), F(remediation subset limited), H(monitoring note subset) | validation conclusion tools, developer build groups | Often | Possible | Yes | No | review_shell | review | standard_mode | monitoring_snapshot_ingest, monitoring_breach_review |  
  
====================================================================  
E. REPORTING + GOVERNANCE PACK STAGES  
====================================================================  
  
| Stage | Actor Role | Access Mode | Preconditions | Allowed Tool Groups | Blocked Tool Groups | Review Required | Approval Required | Audit Required | Auto Continue Allowed | UI Mode | Interaction Mode | Token Mode | Primary Next Routes |  
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|  
| reporting_technical | developer | BUILD_ONLY | technical inputs/artifacts available | A(route subset), G(technical subset), H(retrieval/knowledge subset) | F(finalization), monitoring writes | Optional | No | Optional | Yes | mixed | build | standard_mode | committee_pack_build, knowledge_capture |  
| reporting_technical | validator | BUILD_ONLY | technical inputs/artifacts available | A(route subset), G(technical/validation note subset), H(retrieval subset) | developer build groups, final approvals | Optional | No | Optional | Yes | mixed | build | standard_mode | committee_pack_build, knowledge_capture |  
| reporting_technical | governance | BUILD_ONLY | technical inputs/artifacts available | A(route subset), G(technical/executive subset), H(read-only subset) | developer build groups, monitoring writes | Optional | No | Optional | Yes | mixed | build | standard_mode | committee_pack_build, knowledge_capture |  
| committee_pack_build | governance | BUILD_ONLY / REVIEW_REQUIRED | technical report and validation outputs available | A(route subset), G(executive/committee subset), H(flow/knowledge read subset) | developer build groups, monitoring writes | Often | Possible | Optional to Yes | Yes if no review required | mixed | build | deep_review_mode | committee_pack_review, approval_signoff, knowledge_capture |  
| committee_pack_build | validator | BUILD_ONLY / REVIEW_REQUIRED | technical report and validation outputs available | A(route subset), G(validation/exec subset), H(read-only subset) | developer build groups | Often | No | Optional | Yes | mixed | build | deep_review_mode | committee_pack_review, approval_signoff |  
| committee_pack_build | system | BUILD_ONLY | technical report and validation outputs available | A(route subset), G(pack assembly subset) | all review/finalization groups | No | No | Optional | Yes | none | build | micro_mode | approval_signoff, knowledge_capture |  
| committee_pack_review | governance | REVIEW_REQUIRED | committee pack built, review required | A(route/patch subset), B(review subset), G(read subset), H(flow subset) | developer build groups | Yes | Possible | Yes | No | review_shell | review | deep_review_mode | approval_signoff, committee_pack_build |  
| committee_pack_review | approver | REVIEW_REQUIRED / FINALIZATION_GATED | committee pack built, review required, actor allowed | A(route/patch subset), B(approval subset), G(read subset), H(flow subset) | build groups | Yes | Yes | Yes | No | review_shell | approve | deep_review_mode | approval_signoff |  
  
====================================================================  
F. KNOWLEDGE + RETRIEVAL + FLOW STAGES  
====================================================================  
  
| Stage | Actor Role | Access Mode | Preconditions | Allowed Tool Groups | Blocked Tool Groups | Review Required | Approval Required | Audit Required | Auto Continue Allowed | UI Mode | Interaction Mode | Token Mode | Primary Next Routes |  
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|  
| knowledge_capture | system | BUILD_ONLY | meaningful event/decision/conclusion exists | A(route subset), H(knowledge capture subset) | H(knowledge promotion), developer/validation build groups | No | No | Optional | Yes | none | build | micro_mode | knowledge_promotion, approval_signoff, monitoring_snapshot_ingest |  
| knowledge_capture | validator | BUILD_ONLY | meaningful event/decision/conclusion exists | A(route subset), H(knowledge capture subset) | promotion without authority, build groups | Optional | No | Optional to Yes on decision capture | Yes | mixed | build | standard_mode | knowledge_promotion, approval_signoff |  
| knowledge_capture | governance | BUILD_ONLY | meaningful event/decision/conclusion exists | A(route subset), H(knowledge capture subset) | promotion without review if policy says no | Optional | No | Optional to Yes | Yes | mixed | build | standard_mode | knowledge_promotion, approval_signoff |  
| knowledge_promotion | governance | FINALIZATION_GATED | knowledge exists, quality eligible, promotion requested | A(route subset), B(review/approval subset), H(knowledge promotion/read subset) | build-heavy groups, monitoring writes | Usually Yes | Often | Yes | No | review_shell | approve | deep_review_mode | approval_signoff, workflow_closed |  
| knowledge_promotion | approver | FINALIZATION_GATED | promotion requires approval and actor permitted | A(route subset), B(approval subset), H(knowledge promotion/read subset) | build groups | Yes | Yes | Yes | No | review_shell | approve | deep_review_mode | workflow_closed |  
| retrieval_support | developer | READ_ONLY | query/context present | A(read subset), H(retrieval subset) | all writes/finalizations | No | No | No | Yes | mixed | read | standard_mode | any stage needing support context |  
| retrieval_support | validator | READ_ONLY | query/context present | A(read subset), H(retrieval subset) | all writes/finalizations except independent stage tools | No | No | No | Yes | mixed | read | deep_review_mode | any validation stage |  
| retrieval_support | monitoring | READ_ONLY | query/context present | A(read subset), H(retrieval subset) | all writes/finalizations except monitoring notes in proper stage | No | No | No | Yes | mixed | read | standard_mode | any monitoring stage |  
| retrieval_support | governance | READ_ONLY | query/context present | A(read subset), H(retrieval subset) | all writes/finalizations except approved review stages | No | No | No | Yes | mixed | read | deep_review_mode | governance/review stages |  
| flow_explorer | developer | READ_ONLY | run_id or graph_ref present | A(read subset), H(flow subset) | all writes/finalizations | No | No | No | Yes | flow_explorer | read | micro_mode | inspection only |  
| flow_explorer | validator | READ_ONLY | run_id or graph_ref present | A(read subset), H(flow subset) | all writes/finalizations | No | No | No | Yes | flow_explorer | read | micro_mode | inspection only |  
| flow_explorer | monitoring | READ_ONLY | run_id or graph_ref present | A(read subset), H(flow subset) | all writes/finalizations | No | No | No | Yes | flow_explorer | read | micro_mode | inspection only |  
| flow_explorer | governance | READ_ONLY | run_id or graph_ref present | A(read subset), H(flow subset) | all writes/finalizations | No | No | No | Yes | flow_explorer | read | micro_mode | inspection only |  
| flow_explorer | approver | READ_ONLY | run_id or graph_ref present | A(read subset), H(flow subset) | all writes/finalizations | No | No | No | Yes | flow_explorer | read | micro_mode | inspection only |  
  
====================================================================  
G. MONITORING STAGES  
====================================================================  
  
| Stage | Actor Role | Access Mode | Preconditions | Allowed Tool Groups | Blocked Tool Groups | Review Required | Approval Required | Audit Required | Auto Continue Allowed | UI Mode | Interaction Mode | Token Mode | Primary Next Routes |  
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|  
| monitoring_snapshot_ingest | monitoring | MONITORING_OPERATIONAL | model_id, snapshot payload, template available | A(patch subset), H(monitoring ingest subset) | developer build groups, validation finalization, approval signoff | No | No | Optional | Yes | mixed | monitor | standard_mode | monitoring_kpi_refresh, monitoring_snapshot_remediation |  
| monitoring_snapshot_ingest | system | MONITORING_OPERATIONAL | model_id, snapshot payload, template available | A(patch subset), H(monitoring ingest subset) | all review/finalization groups | No | No | Optional | Yes | none | monitor | micro_mode | monitoring_kpi_refresh |  
| monitoring_kpi_refresh | monitoring | MONITORING_OPERATIONAL | latest snapshot appended | A(route subset), D(stability/calibration subset), H(monitoring KPI subset) | developer build groups, validation finalization, signoff | No unless breach | No | Optional to Yes on severe breach | Yes if no breach | dashboard | monitor | standard_mode | monitoring_dashboard_view, monitoring_breach_review |  
| monitoring_kpi_refresh | system | MONITORING_OPERATIONAL | latest snapshot appended | A(route subset), D(stability subset), H(monitoring KPI subset) | review/finalization groups | No | No | Optional | Yes if no breach | none | monitor | micro_mode | monitoring_dashboard_view, monitoring_breach_review |  
| monitoring_breach_review | monitoring | REVIEW_REQUIRED / FINALIZATION_GATED | breach summary exists, review active or required | A(route/patch subset), B(review subset), F(remediation subset limited), H(monitoring note/breach subset, retrieval/flow subset) | developer build groups, validation conclusion, signoff | Yes | Policy dependent | Yes | No | review_shell | review | deep_review_mode | monitoring_dashboard_view, remediation_action_setup, annual_review_build |  
| monitoring_breach_review | governance | REVIEW_REQUIRED / FINALIZATION_GATED | breach summary exists, review active or required | A(route/patch subset), B(review/approval subset), H(monitoring note/breach subset, flow subset) | developer build groups, validation finalization | Yes | Often | Yes | No | review_shell | review | deep_review_mode | monitoring_dashboard_view, governance_escalation_review |  
| monitoring_breach_review | approver | FINALIZATION_GATED | breach summary exists, approval required, actor allowed | A(route/patch subset), B(approval subset), H(monitoring note/breach subset read-limited) | build groups | Yes | Yes | Yes | No | review_shell | approve | deep_review_mode | monitoring_dashboard_view, remediation_action_setup |  
| monitoring_dashboard_view | monitoring | MONITORING_OPERATIONAL / READ_ONLY | dashboard payload exists | A(read subset), H(dashboard/note/flow subset) | developer build groups, validation conclusion, signoff | No | No | Optional for note/action | Yes | dashboard | monitor | micro_mode | annual_review_build, next monitoring cycle |  
| monitoring_dashboard_view | governance | READ_ONLY / MONITORING_OPERATIONAL | dashboard payload exists | A(read subset), H(dashboard/note/flow subset) | build groups | No | No | Optional | Yes | dashboard | read | micro_mode | annual_review_build |  
| monitoring_dashboard_view | validator | READ_ONLY | dashboard payload exists | A(read subset), H(dashboard/flow subset) | build groups, monitoring writes except maybe notes if policy allows | No | No | No | Yes | dashboard | read | micro_mode | annual_review_build |  
| annual_review_build | monitoring | BUILD_ONLY / REVIEW_REQUIRED | sufficient history, period specified | A(route subset), G(exec/committee subset), H(annual review/flow subset) | developer build groups, validation finalization | Often | No | Optional to Yes | Yes if no review required | mixed | build | deep_review_mode | annual_review_governance_review, approval_signoff |  
| annual_review_build | governance | BUILD_ONLY / REVIEW_REQUIRED | sufficient history, period specified | A(route subset), G(exec/committee subset), H(annual review/flow subset) | build groups | Often | Possible | Optional to Yes | Yes if no review required | mixed | build | deep_review_mode | annual_review_governance_review, approval_signoff |  
| annual_review_build | system | BUILD_ONLY | sufficient history, period specified | A(route subset), G(pack subset), H(annual review subset) | review/finalization groups | No | No | Optional | Yes | none | build | micro_mode | annual_review_governance_review, approval_signoff |  
  
====================================================================  
H. APPROVAL + SIGNOFF STAGE  
====================================================================  
  
| Stage | Actor Role | Access Mode | Preconditions | Allowed Tool Groups | Blocked Tool Groups | Review Required | Approval Required | Audit Required | Auto Continue Allowed | UI Mode | Interaction Mode | Token Mode | Primary Next Routes |  
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|  
| approval_signoff | approver | FINALIZATION_GATED | approval package exists, review active if needed, actor permitted | A(route/patch subset), B(approval subset), G(read subset), H(flow read subset) | all build groups, monitoring writes, validation build tools | Yes | Yes | Yes | No | review_shell | approve | deep_review_mode | workflow_closed, remediation_action_setup |  
| approval_signoff | governance | FINALIZATION_GATED | approval path active, actor permitted | A(route/patch subset), B(approval subset), G(read subset), H(flow read subset) | build groups | Yes | Often | Yes | No | review_shell | approve | deep_review_mode | workflow_closed, governance_escalation_review |  
| approval_signoff | validator | READ_ONLY unless dual role | approval path active but validator not approver | A(read subset), G(read subset), H(flow read subset) | approval/finalization tools unless dual-role | No | No | No | No | review_shell | read | deep_review_mode | inspection only |  
| approval_signoff | developer | READ_ONLY | approval path active | A(read subset), G(read subset), H(flow read subset) | all approval/finalization tools | No | No | No | No | review_shell | read | deep_review_mode | inspection only |  
  
====================================================================  
I. FAILURE / RECOVERY STAGES  
====================================================================  
  
| Stage | Actor Role | Access Mode | Preconditions | Allowed Tool Groups | Blocked Tool Groups | Review Required | Approval Required | Audit Required | Auto Continue Allowed | UI Mode | Interaction Mode | Token Mode | Primary Next Routes |  
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|  
| recovery_review | developer | REVIEW_REQUIRED | failed stage, recovery options available | A(recovery subset), B(review subset), H(flow subset) | finalization tools unrelated to recovery | Optional | No | Optional | No | review_shell | recover | standard_mode | rerun target stage, rollback target stage |  
| recovery_review | governance | REVIEW_REQUIRED | failed stage, material recovery decision needed | A(recovery subset), B(review/approval subset), H(flow subset) | build groups | Often | Possible | Yes if material | No | review_shell | recover | deep_review_mode | rerun target stage, governance_escalation_review |  
| stage_failure_bootstrap | developer | READ_ONLY / RECOVER | failed bootstrap event exists | A(recovery/read subset), H(flow subset) | build/finalization groups | Optional | No | No | Yes | mixed | recover | micro_mode | session_bootstrap, workflow_bootstrap |  
| stage_failure_dataprep_execution | developer | RECOVER | dataprep stage failed | A(recovery/checkpoint/patch subset), B(policy/review subset), H(flow subset) | approval/signoff, validation conclusion | Optional | No | Optional | Limited | mixed | recover | standard_mode | data_preparation_execution, data_preparation_config |  
| stage_failure_feature_engineering | developer | RECOVER | feature stage failed | A(recovery/patch subset), H(flow subset) | approval/signoff, validation conclusion | Optional | No | Optional | Limited | mixed | recover | standard_mode | feature_engineering, dataset_registration |  
| stage_failure_monitoring_refresh | monitoring | RECOVER | monitoring refresh failed | A(recovery/patch subset), H(monitoring note/flow subset) | validation/signoff/build groups | Optional | No | Optional | Limited | dashboard | recover | standard_mode | monitoring_kpi_refresh, monitoring_snapshot_ingest |  
  
====================================================================  
PRECONDITION CHECK RULES  
====================================================================  
  
For each stage, RuntimeResolver should validate these categories:  
  
1. Identity Preconditions  
--------------------------------------------------------------------  
- session_id present where required  
- project_id present where required  
- run_id present where required  
- actor role present and supported  
  
2. Workflow Preconditions  
--------------------------------------------------------------------  
- current_stage matches stage request  
- stage dependencies completed  
- blocker flags not active  
- stale state not detected  
  
3. Artifact / Reference Preconditions  
--------------------------------------------------------------------  
- required refs exist  
- referenced artifacts are resolvable  
- selected_candidate_version_id exists where required  
- validation_run_id exists where required  
- latest_snapshot_id exists where required  
  
4. Governance Preconditions  
--------------------------------------------------------------------  
- review exists if review_required = true  
- actor has approval rights if approval_required = true  
- unresolved severe breaches do not block continuation  
- waiver path exists if continuation despite breach is requested  
  
5. Runtime Preconditions  
--------------------------------------------------------------------  
- sdk allowlist resolved  
- UI mode resolved  
- token mode resolved  
- Spark availability confirmed where needed  
  
If any precondition fails:  
- preconditions_passed = false  
- missing_preconditions = [...]  
- auto_continue_allowed = false  
- allowed_tools should collapse to:  
  - get_workflow_state  
  - resolve_recovery_path  
  - replay_run  
  - create_review if governance choice is needed  
  
====================================================================  
AUTOMATIC CONTINUATION RULES  
====================================================================  
  
Auto-continue should be TRUE only when all are satisfied:  
- no mandatory review  
- no mandatory approval  
- no blocker flags  
- no stale state  
- no unresolved severe breach  
- preconditions passed  
- action is deterministic and non-finalizing  
  
Auto-continue should be FALSE when any are true:  
- review_required = true  
- approval_required = true  
- audit_required for irreversible final action and actor has not acted yet  
- severe DQ or policy breach blocks continuation  
- stage is FINALIZATION_GATED  
- review is open and awaiting actor decision  
  
====================================================================  
UI MODE RULES  
====================================================================  
  
| UI Mode | Use When |  
|---|---|  
| wizard | session bootstrap, simple guided setup |  
| mixed | technical build stages with artifacts + optional side context |  
| review_shell | any governed HITL/review/finalization stage |  
| dashboard | monitoring operational view |  
| flow_explorer | flow/timeline inspection |  
| chat_only | very lightweight read-only queries or support context |  
| none | system-only execution paths |  
  
Recommended defaults:  
- build stages -> mixed  
- review/finalization stages -> review_shell  
- monitoring display -> dashboard  
- flow inspection -> flow_explorer  
- system-only -> none  
  
====================================================================  
INTERACTION MODE RULES  
====================================================================  
  
| Interaction Mode | Use When |  
|---|---|  
| read | inspection only |  
| build | deterministic artifact generation |  
| review | human evaluates proposal |  
| approve | actor is granting formal approval/signoff |  
| monitor | operational dashboard / KPI triage |  
| recover | rerun/rollback/recovery decision |  
  
====================================================================  
TOKEN MODE RULES  
====================================================================  
  
| Token Mode | Use When |  
|---|---|  
| micro_mode | bootstrap, read-only views, dashboard refresh, system operations |  
| standard_mode | most build stages and normal review stages |  
| deep_review_mode | validation review, conclusion review, major governance review, committee/annual review build |  
  
Heuristic:  
- if review/finalization/governance stage -> deep_review_mode  
- if build stage with moderate complexity -> standard_mode  
- if read-only or system deterministic stage -> micro_mode  
  
====================================================================  
RUNTIME RESOLVER PSEUDOCODE  
====================================================================  
  
1. Read current workflow state  
2. Determine requested stage and actor role  
3. Validate stage exists in stage registry  
4. Load stage default config:  
   - access mode  
   - allowed tool groups  
   - default ui mode  
   - default interaction mode  
   - default token mode  
5. Apply role filter:  
   - remove tools/groups not allowed to role  
6. Check stage preconditions:  
   - ids/refs/state/blockers  
7. Apply governance overlay:  
   - review_required?  
   - approval_required?  
   - audit_required?  
8. Apply state overlay:  
   - open review present?  
   - stale state?  
   - unresolved severe breach?  
   - remediation_mode?  
   - annual_review_mode?  
9. Build final allowlist:  
   - allowed_tools  
   - blocked_tools  
10. Build runtime decision output  
11. Return ResolvedStack + runtime decision  
  
====================================================================  
SUGGESTED OUTPUT EXAMPLE  
====================================================================  
  
{  
  "stage_name": "model_selection_review",  
  "actor_role": "governance",  
  "access_mode": "REVIEW_REQUIRED",  
  "preconditions_passed": true,  
  "missing_preconditions": [],  
  "allowed_tool_groups": ["A", "B", "D", "H"],  
  "blocked_tool_groups": ["C", "E_build", "F", "monitoring_writes"],  
  "allowed_tools": [  
    "get_review",  
    "build_review_payload",  
    "compare_candidates",  
    "validate_review_action",  
    "approve_review",  
    "approve_review_with_conditions",  
    "escalate_review",  
    "capture_review_decision",  
    "select_candidate_version",  
    "patch_workflow_state",  
    "route_next_stage"  
  ],  
  "blocked_tools": [  
    "fit_scorecard_candidate_set",  
    "execute_dataprep_request",  
    "finalize_validation_conclusion"  
  ],  
  "review_required": true,  
  "approval_required": true,  
  "audit_required": true,  
  "auto_continue_allowed": false,  
  "recommended_ui_mode": "review_shell",  
  "recommended_interaction_mode": "review",  
  "recommended_token_mode": "deep_review_mode",  
  "recommended_next_routes": [  
    "score_scaling_and_banding",  
    "governance_escalation_review"  
  ],  
  "notes": [  
    "Candidate selection must be explicit and audited.",  
    "Actor must satisfy approval requirements before final selection."  
  ]  
}  
  
====================================================================  
FINAL RECOMMENDATIONS  
====================================================================  
  
1. Keep the stage registry and runtime decision table as data-driven  
   configs, not hardcoded logic only.  
  
2. Runtime decision output should be logged for every stage entry.  
  
3. The agent should never infer hidden permissions.  
   It should always consume the resolved allowlist.  
  
4. Review and approval requirements should be explicit booleans in the  
   runtime output.  
  
5. The UI should read:  
   - recommended_ui_mode  
   - recommended_interaction_mode  
   - allowed_tools  
   directly from this runtime decision.  
  
====================================================================  
NEXT BEST ARTIFACT  
====================================================================  
  
The strongest next deliverable is a:  
  
DATA-DRIVEN YAML / JSON CONFIG PACK  
for:  
- stage registry  
- role rules  
- tool groups  
- runtime defaults  
- governance overlays  
  
That would make the resolver fully implementable without hardcoding the  
entire matrix.  
  
====================================================================  
END OF RUNTIME DECISION TABLE  
====================================================================  
