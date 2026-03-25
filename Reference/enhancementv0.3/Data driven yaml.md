# Data driven yaml  
  
====================================================================  
DATA-DRIVEN YAML / JSON CONFIG PACK  
AGENTIC AI MDLC FRAMEWORK  
RUNTIME RESOLVER + ALLOWLIST ENGINE IMPLEMENTATION PACK  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This pack turns the runtime decision table into a data-driven config  
design that can be loaded by:  
  
- ConfigService  
- RuntimeResolver  
- AllowlistResolver  
- UIModeResolver  
- InteractionModeResolver  
- TokenModeResolver  
- WorkflowService  
- PolicyService  
- HITLService  
- AgentBridge  
- JupyterBridge  
  
The goal is to avoid hardcoding the entire runtime matrix in Python.  
  
This pack includes:  
1. config file layout  
2. master config structure  
3. YAML examples  
4. JSON shape references  
5. recommended loaders  
6. merge / override rules  
7. validation rules  
8. future-proofing guidance  
  
====================================================================  
1. RECOMMENDED CONFIG FILE LAYOUT  
====================================================================  
  
Suggested folder layout:  
  
configs/  
  runtime/  
    runtime_master.yaml  
    tool_groups.yaml  
    role_capabilities.yaml  
    ui_modes.yaml  
    interaction_modes.yaml  
    token_modes.yaml  
    stage_registry.yaml  
    stage_tool_matrix.yaml  
    stage_preconditions.yaml  
    governance_overlays.yaml  
    retry_policies.yaml  
    failure_routes.yaml  
    workflow_routes.yaml  
    domain_overlays/  
      scorecard.yaml  
      pd.yaml  
      lgd.yaml  
      ead.yaml  
      sicr.yaml  
      ecl.yaml  
      stress.yaml  
    role_overlays/  
      developer.yaml  
      validator.yaml  
      monitoring.yaml  
      governance.yaml  
      approver.yaml  
      system.yaml  
    environment_overlays/  
      dev.yaml  
      uat.yaml  
      prod.yaml  
  
Recommended supporting schema folder:  
  
schemas/  
  runtime/  
    runtime_master.schema.json  
    tool_groups.schema.json  
    role_capabilities.schema.json  
    stage_registry.schema.json  
    stage_tool_matrix.schema.json  
    governance_overlays.schema.json  
  
====================================================================  
2. RECOMMENDED CONFIG LOADING ORDER  
====================================================================  
  
Recommended load order:  
  
1. runtime_master.yaml  
2. tool_groups.yaml  
3. role_capabilities.yaml  
4. ui_modes.yaml  
5. interaction_modes.yaml  
6. token_modes.yaml  
7. stage_registry.yaml  
8. stage_tool_matrix.yaml  
9. stage_preconditions.yaml  
10. governance_overlays.yaml  
11. retry_policies.yaml  
12. failure_routes.yaml  
13. workflow_routes.yaml  
14. domain_overlays/<domain>.yaml  
15. role_overlays/<role>.yaml  
16. environment_overlays/<env>.yaml  
  
Merge order:  
- base first  
- then domain overlay  
- then role overlay  
- then environment overlay  
- finally runtime/request-time explicit overrides  
  
====================================================================  
3. MASTER CONFIG INDEX  
====================================================================  
  
--------------------------------------------------------------------  
3.1 runtime_master.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Top-level index file that defines:  
- config versions  
- enabled modules  
- file references  
- default resolver behavior  
  
Example:  
  
runtime_master:  
  config_version: "1.0.0"  
  runtime_mode: "strict"  
  default_environment: "prod"  
  
  enabled_modules:  
    stage_registry: true  
    tool_groups: true  
    role_capabilities: true  
    ui_modes: true  
    interaction_modes: true  
    token_modes: true  
    governance_overlays: true  
    retry_policies: true  
    failure_routes: true  
    workflow_routes: true  
  
  file_refs:  
    tool_groups: "configs/runtime/tool_groups.yaml"  
    role_capabilities: "configs/runtime/role_capabilities.yaml"  
    ui_modes: "configs/runtime/ui_modes.yaml"  
    interaction_modes: "configs/runtime/interaction_modes.yaml"  
    token_modes: "configs/runtime/token_modes.yaml"  
    stage_registry: "configs/runtime/stage_registry.yaml"  
    stage_tool_matrix: "configs/runtime/stage_tool_matrix.yaml"  
    stage_preconditions: "configs/runtime/stage_preconditions.yaml"  
    governance_overlays: "configs/runtime/governance_overlays.yaml"  
    retry_policies: "configs/runtime/retry_policies.yaml"  
    failure_routes: "configs/runtime/failure_routes.yaml"  
    workflow_routes: "configs/runtime/workflow_routes.yaml"  
  
  resolver_defaults:  
    unknown_stage_behavior: "block"  
    unknown_role_behavior: "block"  
    missing_tool_group_behavior: "block"  
    stale_state_behavior: "recover_only"  
    missing_review_behavior: "review_only"  
    unresolved_breach_behavior: "block_downstream"  
    default_ui_mode: "chat_only"  
    default_interaction_mode: "read"  
    default_token_mode: "micro_mode"  
  
====================================================================  
4. TOOL GROUP CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
4.1 tool_groups.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Maps tool group names to concrete tool names.  
  
Example:  
  
tool_groups:  
  A:  
    name: "session_runtime_workflow"  
    tools:  
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
  
  B:  
    name: "review_policy"  
    tools:  
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
  
  C:  
    name: "data_dataprep_dq"  
    tools:  
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
  
  D:  
    name: "feature_evaluation"  
    tools:  
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
  
  E:  
    name: "scorecard"  
    tools:  
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
  
  F:  
    name: "validation"  
    tools:  
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
  
  G:  
    name: "reporting"  
    tools:  
      - build_technical_report  
      - build_executive_summary  
      - build_committee_pack  
      - build_validation_note  
      - get_narrative_block  
      - export_chart_refs  
      - export_table_refs  
      - assemble_pack  
  
  H:  
    name: "knowledge_retrieval_flow_monitoring"  
    tools:  
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
5. ROLE CAPABILITY CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
5.1 role_capabilities.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Defines what each role can fundamentally do.  
  
Example:  
  
role_capabilities:  
  developer:  
    can_build: true  
    can_review: true  
    can_approve: false  
    can_finalize_validation_conclusion: false  
    can_ingest_monitoring: false  
    can_signoff: false  
    can_promote_knowledge_beyond_project: false  
    default_ui_mode: "mixed"  
    default_interaction_mode: "build"  
    default_token_mode: "standard_mode"  
  
  validator:  
    can_build: false  
    can_review: true  
    can_approve: false  
    can_finalize_validation_conclusion: true  
    can_ingest_monitoring: false  
    can_signoff: false  
    can_promote_knowledge_beyond_project: false  
    default_ui_mode: "review_shell"  
    default_interaction_mode: "review"  
    default_token_mode: "deep_review_mode"  
  
  monitoring:  
    can_build: false  
    can_review: true  
    can_approve: false  
    can_finalize_validation_conclusion: false  
    can_ingest_monitoring: true  
    can_signoff: false  
    can_promote_knowledge_beyond_project: false  
    default_ui_mode: "dashboard"  
    default_interaction_mode: "monitor"  
    default_token_mode: "standard_mode"  
  
  governance:  
    can_build: false  
    can_review: true  
    can_approve: true  
    can_finalize_validation_conclusion: false  
    can_ingest_monitoring: false  
    can_signoff: true  
    can_promote_knowledge_beyond_project: true  
    default_ui_mode: "review_shell"  
    default_interaction_mode: "review"  
    default_token_mode: "deep_review_mode"  
  
  approver:  
    can_build: false  
    can_review: true  
    can_approve: true  
    can_finalize_validation_conclusion: false  
    can_ingest_monitoring: false  
    can_signoff: true  
    can_promote_knowledge_beyond_project: true  
    default_ui_mode: "review_shell"  
    default_interaction_mode: "approve"  
    default_token_mode: "deep_review_mode"  
  
  system:  
    can_build: true  
    can_review: false  
    can_approve: false  
    can_finalize_validation_conclusion: false  
    can_ingest_monitoring: true  
    can_signoff: false  
    can_promote_knowledge_beyond_project: false  
    default_ui_mode: "none"  
    default_interaction_mode: "build"  
    default_token_mode: "micro_mode"  
  
====================================================================  
6. UI MODE CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
6.1 ui_modes.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Defines supported UI modes and their meaning.  
  
Example:  
  
ui_modes:  
  chat_only:  
    description: "Simple chat interface with minimal structured panels"  
    supports_review_actions: false  
    supports_dashboard: false  
    supports_flow_explorer: false  
  
  wizard:  
    description: "Step-by-step guided initialization UI"  
    supports_review_actions: false  
    supports_dashboard: false  
    supports_flow_explorer: false  
  
  mixed:  
    description: "Main workspace with chat plus structured output panels"  
    supports_review_actions: true  
    supports_dashboard: false  
    supports_flow_explorer: false  
  
  review_shell:  
    description: "Governed 3-panel review interface"  
    supports_review_actions: true  
    supports_dashboard: false  
    supports_flow_explorer: false  
  
  dashboard:  
    description: "Operational monitoring dashboard UI"  
    supports_review_actions: true  
    supports_dashboard: true  
    supports_flow_explorer: false  
  
  flow_explorer:  
    description: "Flow graph + timeline + drilldown"  
    supports_review_actions: false  
    supports_dashboard: false  
    supports_flow_explorer: true  
  
  none:  
    description: "System-only runtime path"  
    supports_review_actions: false  
    supports_dashboard: false  
    supports_flow_explorer: false  
  
====================================================================  
7. INTERACTION MODE CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
7.1 interaction_modes.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Defines interaction intent for UI and agent.  
  
Example:  
  
interaction_modes:  
  read:  
    description: "Inspect only"  
    allows_mutation: false  
  
  build:  
    description: "Deterministic construction"  
    allows_mutation: true  
  
  review:  
    description: "Structured human evaluation and bounded action"  
    allows_mutation: true  
  
  approve:  
    description: "Formal approval / signoff action mode"  
    allows_mutation: true  
  
  monitor:  
    description: "Operational monitoring and dashboard triage"  
    allows_mutation: true  
  
  recover:  
    description: "Recovery, rerun, rollback, resume path selection"  
    allows_mutation: true  
  
====================================================================  
8. TOKEN MODE CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
8.1 token_modes.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Defines token budget modes for retrieval and prompt packaging.  
  
Example:  
  
token_modes:  
  micro_mode:  
    description: "Minimal context for lightweight actions"  
    retrieval_top_k: 3  
    max_context_tokens: 800  
    include_detailed_evidence: false  
    prefer_summaries_only: true  
  
  standard_mode:  
    description: "Balanced context for normal build/review stages"  
    retrieval_top_k: 6  
    max_context_tokens: 2200  
    include_detailed_evidence: true  
    prefer_summaries_only: false  
  
  deep_review_mode:  
    description: "Expanded context for governance and validation review"  
    retrieval_top_k: 10  
    max_context_tokens: 5000  
    include_detailed_evidence: true  
    prefer_summaries_only: false  
  
====================================================================  
9. STAGE REGISTRY CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
9.1 stage_registry.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Defines all stages, their metadata, and their high-level type.  
  
Example:  
  
stage_registry:  
  session_bootstrap:  
    stage_class: "bootstrap"  
    stage_sequence_no: 1  
    domain_scope: ["generic"]  
    access_mode: "READ_ONLY"  
    default_ui_mode: "wizard"  
    default_interaction_mode: "read"  
    default_token_mode: "micro_mode"  
  
  workflow_bootstrap:  
    stage_class: "bootstrap"  
    stage_sequence_no: 2  
    domain_scope: ["generic"]  
    access_mode: "BUILD_ONLY"  
    default_ui_mode: "wizard"  
    default_interaction_mode: "build"  
    default_token_mode: "micro_mode"  
  
  data_preparation_config:  
    stage_class: "build"  
    stage_sequence_no: 10  
    domain_scope: ["scorecard", "pd", "lgd", "ead", "sicr", "ecl", "stress", "generic"]  
    access_mode: "BUILD_ONLY"  
    default_ui_mode: "mixed"  
    default_interaction_mode: "build"  
    default_token_mode: "standard_mode"  
  
  coarse_classing_review:  
    stage_class: "review"  
    stage_sequence_no: 25  
    domain_scope: ["scorecard"]  
    access_mode: "REVIEW_REQUIRED"  
    default_ui_mode: "review_shell"  
    default_interaction_mode: "review"  
    default_token_mode: "deep_review_mode"  
  
  validation_conclusion_review:  
    stage_class: "finalization"  
    stage_sequence_no: 60  
    domain_scope: ["scorecard", "pd", "lgd", "ead", "sicr", "ecl", "stress", "generic"]  
    access_mode: "FINALIZATION_GATED"  
    default_ui_mode: "review_shell"  
    default_interaction_mode: "approve"  
    default_token_mode: "deep_review_mode"  
  
  monitoring_kpi_refresh:  
    stage_class: "monitoring"  
    stage_sequence_no: 80  
    domain_scope: ["scorecard", "pd", "lgd", "ead", "sicr", "ecl", "stress"]  
    access_mode: "MONITORING_OPERATIONAL"  
    default_ui_mode: "dashboard"  
    default_interaction_mode: "monitor"  
    default_token_mode: "standard_mode"  
  
Continue same pattern for all stages.  
  
====================================================================  
10. STAGE TOOL MATRIX CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
10.1 stage_tool_matrix.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Defines per-stage allowed tool groups and explicit tool overrides.  
  
Example:  
  
stage_tool_matrix:  
  session_bootstrap:  
    allowed_tool_groups:  
      - A  
      - H_READ_ONLY  
    blocked_tool_groups:  
      - C  
      - D  
      - E  
      - F  
      - G_WRITE  
      - H_WRITE  
    explicit_allow: []  
    explicit_block: []  
  
  data_preparation_execution:  
    allowed_tool_groups:  
      - A_CHECKPOINT  
      - C_DATAPREP_EXEC  
    blocked_tool_groups:  
      - B_FINALIZATION  
      - E  
      - F  
      - G  
      - H_MONITORING_WRITE  
    explicit_allow:  
      - execute_dataprep_request  
      - build_cross_sectional_dataset_spark  
      - build_panel_dataset_spark  
      - build_time_series_dataset_spark  
      - build_cohort_dataset_spark  
      - build_event_history_dataset_spark  
      - create_checkpoint  
    explicit_block:  
      - approve_review  
      - finalize_validation_conclusion  
      - register_signoff  
  
  coarse_classing_review:  
    allowed_tool_groups:  
      - A_ROUTE_PATCH  
      - B_REVIEW  
      - E_COARSE_REVIEW  
      - H_RETRIEVAL  
    blocked_tool_groups:  
      - C_BUILD  
      - F  
      - H_MONITORING_WRITE  
    explicit_allow:  
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
    explicit_block:  
      - execute_dataprep_request  
      - fit_scorecard_candidate_set  
      - finalize_validation_conclusion  
  
  validation_conclusion_review:  
    allowed_tool_groups:  
      - A_ROUTE_PATCH  
      - B_REVIEW  
      - F_CONCLUSION  
      - H_RETRIEVAL  
    blocked_tool_groups:  
      - C_BUILD  
      - E_BUILD  
      - H_MONITORING_WRITE  
    explicit_allow:  
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
    explicit_block:  
      - execute_dataprep_request  
      - build_fine_bins  
      - ingest_monitoring_snapshot  
  
--------------------------------------------------------------------  
10.2 Tool Group Expansion Convention  
--------------------------------------------------------------------  
  
To avoid huge files, support virtual subgroups:  
  
virtual_tool_groups:  
  A_CHECKPOINT:  
    includes:  
      - create_checkpoint  
  
  A_ROUTE_PATCH:  
    includes:  
      - patch_workflow_state  
      - route_next_stage  
  
  B_REVIEW:  
    includes:  
      - create_review  
      - get_review  
      - build_review_payload  
      - validate_review_action  
      - approve_review  
      - approve_review_with_conditions  
      - escalate_review  
      - capture_review_decision  
  
  B_FINALIZATION:  
    includes:  
      - approve_review  
      - approve_review_with_conditions  
      - capture_review_decision  
  
  C_DATAPREP_EXEC:  
    includes:  
      - execute_dataprep_request  
      - build_cross_sectional_dataset_spark  
      - build_panel_dataset_spark  
      - build_time_series_dataset_spark  
      - build_cohort_dataset_spark  
      - build_event_history_dataset_spark  
  
  E_COARSE_REVIEW:  
    includes:  
      - preview_edited_bins  
      - finalize_coarse_bins  
  
  F_CONCLUSION:  
    includes:  
      - build_validation_conclusion_options  
      - finalize_validation_conclusion  
      - create_remediation_action  
  
  H_RETRIEVAL:  
    includes:  
      - search_knowledge  
      - route_retrieval_query  
      - retrieve_context  
      - rerank_retrieval_results  
      - compress_retrieval_context  
      - build_context_pack  
  
  H_MONITORING_WRITE:  
    includes:  
      - ingest_monitoring_snapshot  
      - append_monitoring_snapshot  
      - create_monitoring_note  
      - write_monitoring_outputs  
  
  H_READ_ONLY:  
    includes:  
      - search_knowledge  
      - route_retrieval_query  
      - retrieve_context  
      - build_context_pack  
      - build_flow_nodes  
      - build_flow_edges  
      - summarize_flow  
      - build_flow_timeline  
      - export_flow_graph  
      - filter_flow_graph  
      - get_flow_drilldown_payload  
  
====================================================================  
11. STAGE PRECONDITION CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
11.1 stage_preconditions.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Defines required IDs, refs, flags, and dependency stages.  
  
Example:  
  
stage_preconditions:  
  workflow_bootstrap:  
    required_ids:  
      - session_id  
    required_refs: []  
    required_flags: []  
    required_prior_stages: []  
  
  data_preparation_execution:  
    required_ids:  
      - project_id  
      - run_id  
    required_refs: []  
    required_flags:  
      - dataprep_config_validated  
    required_prior_stages:  
      - data_preparation_config  
  
  data_readiness_check:  
    required_ids:  
      - run_id  
    required_refs:  
      - prepared_dataset_ref  
    required_flags:  
      - dataprep_executed  
    required_prior_stages:  
      - data_preparation_execution  
  
  coarse_classing_review:  
    required_ids:  
      - run_id  
    required_refs:  
      - fine_bin_ref  
      - coarse_bin_candidate_ids  
    required_flags: []  
    required_prior_stages:  
      - coarse_classing_candidate_build  
    requires_active_review: true  
  
  validation_conclusion_review:  
    required_ids:  
      - run_id  
      - validation_run_id  
    required_refs:  
      - fitness_summary_ref  
    required_flags:  
      - methodology_review_completed  
      - data_validation_review_completed  
    required_prior_stages:  
      - fitness_review  
    requires_active_review: true  
  
  monitoring_kpi_refresh:  
    required_ids:  
      - run_id  
    required_refs:  
      - latest_monitoring_snapshot_id  
    required_flags: []  
    required_prior_stages:  
      - monitoring_snapshot_ingest  
  
====================================================================  
12. GOVERNANCE OVERLAY CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
12.1 governance_overlays.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Defines mandatory review/audit/approval rules by stage.  
  
Example:  
  
governance_overlays:  
  default_rules:  
    review_required: false  
    approval_required: false  
    audit_required: false  
    auto_continue_allowed: true  
  
  stage_rules:  
    coarse_classing_review:  
      review_required: true  
      approval_required: false  
      audit_required: true  
      auto_continue_allowed: false  
  
    feature_shortlist_review:  
      review_required: true  
      approval_required: false  
      audit_required: true  
      auto_continue_allowed: false  
  
    model_selection_review:  
      review_required: true  
      approval_required: true  
      audit_required: true  
      auto_continue_allowed: false  
  
    validation_conclusion_review:  
      review_required: true  
      approval_required: true  
      audit_required: true  
      auto_continue_allowed: false  
  
    monitoring_breach_review:  
      review_required: true  
      approval_required: true  
      audit_required: true  
      auto_continue_allowed: false  
  
    approval_signoff:  
      review_required: true  
      approval_required: true  
      audit_required: true  
      auto_continue_allowed: false  
  
  role_overrides:  
    developer:  
      force_block_tools:  
        - finalize_validation_conclusion  
        - register_signoff  
        - promote_knowledge  
  
    validator:  
      allow_tools:  
        - finalize_validation_conclusion  
  
    monitoring:  
      allow_tools:  
        - ingest_monitoring_snapshot  
        - compute_monitoring_metrics  
        - build_dashboard_payload  
  
    approver:  
      allow_tools:  
        - approve_review  
        - approve_review_with_conditions  
        - register_signoff  
  
--------------------------------------------------------------------  
12.2 Conditional Governance Rules  
--------------------------------------------------------------------  
  
Add optional conditions:  
  
conditional_rules:  
  - rule_id: "block_finalization_without_review"  
    when:  
      stage_access_mode_in:  
        - REVIEW_REQUIRED  
        - FINALIZATION_GATED  
      active_review_exists: false  
    then:  
      force_block_tools:  
        - finalize_coarse_bins  
        - select_candidate_version  
        - finalize_validation_conclusion  
        - register_signoff  
      force_allow_tools:  
        - create_review  
  
  - rule_id: "block_approval_if_role_insufficient"  
    when:  
      approval_required: true  
      actor_not_in_approval_roles: true  
    then:  
      force_block_tools:  
        - approve_review  
        - approve_review_with_conditions  
        - register_signoff  
  
  - rule_id: "block_downstream_if_severe_breach_unresolved"  
    when:  
      unresolved_severe_breach: true  
    then:  
      force_block_tool_groups:  
        - E  
        - F  
      force_allow_tools:  
        - create_review  
        - escalate_review  
        - create_monitoring_note  
  
====================================================================  
13. RETRY POLICY CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
13.1 retry_policies.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Defines retry mode by tool.  
  
Example:  
  
retry_policies:  
  defaults:  
    safe_retry_backoff_seconds: [1, 3, 5]  
    limited_retry_backoff_seconds: [2, 5]  
    no_retry: []  
  
  tool_rules:  
    open_session:  
      retry_mode: "safe"  
  
    resolve_runtime_stack:  
      retry_mode: "safe"  
  
    execute_dataprep_request:  
      retry_mode: "limited"  
      requires_idempotency_check: true  
  
    build_cross_sectional_dataset_spark:  
      retry_mode: "limited"  
      requires_idempotency_check: true  
  
    create_dataset_snapshot:  
      retry_mode: "limited"  
      requires_idempotency_check: true  
  
    preview_edited_bins:  
      retry_mode: "safe"  
  
    finalize_coarse_bins:  
      retry_mode: "none"  
  
    select_candidate_version:  
      retry_mode: "none"  
  
    finalize_validation_conclusion:  
      retry_mode: "none"  
  
    ingest_monitoring_snapshot:  
      retry_mode: "safe"  
      requires_idempotency_check: true  
  
    build_dashboard_payload:  
      retry_mode: "safe"  
  
    register_signoff:  
      retry_mode: "none"  
  
====================================================================  
14. FAILURE ROUTE CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
14.1 failure_routes.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Maps stages to failure-stage routes.  
  
Example:  
  
failure_routes:  
  session_bootstrap:  
    on_failure: "stage_failure_bootstrap"  
  
  workflow_bootstrap:  
    on_failure: "stage_failure_bootstrap"  
  
  data_preparation_execution:  
    on_failure: "stage_failure_dataprep_execution"  
  
  feature_engineering:  
    on_failure: "stage_failure_feature_engineering"  
  
  monitoring_kpi_refresh:  
    on_failure: "stage_failure_monitoring_refresh"  
  
  coarse_classing_review:  
    on_rejection: "coarse_classing_candidate_build"  
  
  model_selection_review:  
    on_rejection: "model_fit_candidates"  
  
  validation_conclusion_review:  
    on_rejection: "remediation_action_setup"  
  
====================================================================  
15. WORKFLOW ROUTE CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
15.1 workflow_routes.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Defines normal next-stage routes.  
  
Example:  
  
workflow_routes:  
  session_bootstrap:  
    on_success:  
      - workflow_bootstrap  
  
  workflow_bootstrap:  
    on_success:  
      - runtime_stack_resolution  
  
  data_preparation_config:  
    on_success:  
      - data_preparation_execution  
    on_review_required:  
      - data_preparation_config_review  
  
  data_preparation_execution:  
    on_success:  
      - data_readiness_check  
  
  data_readiness_check:  
    on_pass:  
      - dataset_registration  
    on_review_required:  
      - data_readiness_review  
    on_fail:  
      - data_remediation  
  
  dataset_registration:  
    on_success:  
      - feature_engineering  
  
  feature_engineering:  
    on_success:  
      - fine_classing  
  
  fine_classing:  
    on_success:  
      - coarse_classing_candidate_build  
  
  coarse_classing_candidate_build:  
    on_success:  
      - coarse_classing_review  
  
  coarse_classing_review:  
    on_approved:  
      - woe_iv_analysis  
    on_rejected:  
      - coarse_classing_candidate_build  
  
  woe_iv_analysis:  
    on_success:  
      - feature_shortlist_build  
  
  feature_shortlist_build:  
    on_success:  
      - feature_shortlist_review  
    on_auto_continue:  
      - model_fit_candidates  
  
  feature_shortlist_review:  
    on_approved:  
      - model_fit_candidates  
    on_rejected:  
      - feature_shortlist_build  
  
  model_fit_candidates:  
    on_success:  
      - model_selection_review  
  
  model_selection_review:  
    on_approved:  
      - score_scaling_and_banding  
    on_rejected:  
      - model_fit_candidates  
  
  score_scaling_and_banding:  
    on_success:  
      - scorecard_output_bundle  
  
  scorecard_output_bundle:  
    on_success:  
      - validation_scope_init  
  
  validation_scope_init:  
    on_success:  
      - validation_evidence_intake  
  
  validation_evidence_intake:  
    on_success:  
      - methodology_review  
  
  methodology_review:  
    on_success:  
      - data_validation_review  
  
  data_validation_review:  
    on_success:  
      - fitness_review  
  
  fitness_review:  
    on_success:  
      - validation_conclusion_review  
  
  validation_conclusion_review:  
    on_approved:  
      - reporting_technical  
    on_remediation_required:  
      - remediation_action_setup  
  
  reporting_technical:  
    on_success:  
      - committee_pack_build  
  
  committee_pack_build:  
    on_success:  
      - approval_signoff  
  
  approval_signoff:  
    on_success:  
      - workflow_closed  
  
====================================================================  
16. DOMAIN OVERLAY CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
16.1 Example: domain_overlays/scorecard.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Adds domain-specific stage changes for scorecard projects.  
  
Example:  
  
domain_overlay:  
  domain_name: "scorecard"  
  
  enabled_stages:  
    - fine_classing  
    - coarse_classing_candidate_build  
    - coarse_classing_review  
    - woe_iv_analysis  
    - feature_shortlist_build  
    - feature_shortlist_review  
    - model_fit_candidates  
    - model_selection_review  
    - score_scaling_and_banding  
    - scorecard_output_bundle  
  
  disabled_stages:  
    - time_series_candidate_build  
    - ecl_scenario_engine  
    - monitoring_term_structure_review  
  
  stage_tool_additions:  
    coarse_classing_review:  
      explicit_allow:  
        - preview_edited_bins  
        - finalize_coarse_bins  
  
  stage_ui_overrides:  
    coarse_classing_review:  
      ui_mode: "review_shell"  
      interaction_mode: "review"  
      token_mode: "deep_review_mode"  
  
====================================================================  
17. ROLE OVERLAY CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
17.1 Example: role_overlays/validator.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Role-specific restrictions and additions.  
  
Example:  
  
role_overlay:  
  role_name: "validator"  
  
  force_block_tools:  
    - execute_dataprep_request  
    - build_cross_sectional_dataset_spark  
    - build_panel_dataset_spark  
    - fit_scorecard_candidate_set  
  
  force_allow_tools:  
    - create_validation_scope  
    - intake_validation_evidence  
    - assess_evidence_completeness  
    - evaluate_fitness_dimensions  
    - create_validation_finding  
    - assess_finding_severity  
    - build_validation_conclusion_options  
    - finalize_validation_conclusion  
  
  ui_mode_overrides:  
    methodology_review: "review_shell"  
    fitness_review: "review_shell"  
  
  token_mode_overrides:  
    methodology_review: "deep_review_mode"  
    validation_conclusion_review: "deep_review_mode"  
  
====================================================================  
18. ENVIRONMENT OVERLAY CONFIG  
====================================================================  
  
--------------------------------------------------------------------  
18.1 Example: environment_overlays/prod.yaml  
--------------------------------------------------------------------  
  
Purpose:  
Production runtime hardening.  
  
Example:  
  
environment_overlay:  
  environment_name: "prod"  
  
  strictness:  
    enforce_stage_preconditions: true  
    enforce_review_requirement: true  
    enforce_audit_requirement: true  
    enforce_role_approval_check: true  
  
  retries:  
    max_safe_retries: 3  
    max_limited_retries: 1  
  
  block_rules:  
    block_unknown_tools: true  
    block_unknown_stages: true  
    block_unknown_roles: true  
  
  ui_defaults:  
    prefer_review_shell_for_governed_stages: true  
  
====================================================================  
19. JSON SHAPE REFERENCE  
====================================================================  
  
If you also want a JSON representation, the main object shape can be:  
  
{  
  "runtime_master": {},  
  "tool_groups": {},  
  "role_capabilities": {},  
  "ui_modes": {},  
  "interaction_modes": {},  
  "token_modes": {},  
  "stage_registry": {},  
  "stage_tool_matrix": {},  
  "stage_preconditions": {},  
  "governance_overlays": {},  
  "retry_policies": {},  
  "failure_routes": {},  
  "workflow_routes": {},  
  "domain_overlay": {},  
  "role_overlay": {},  
  "environment_overlay": {}  
}  
  
====================================================================  
20. CONFIG VALIDATION RULES  
====================================================================  
  
Recommended validation rules:  
  
Rule 1  
--------------------------------------------------------------------  
Every stage in stage_tool_matrix must exist in stage_registry.  
  
Rule 2  
--------------------------------------------------------------------  
Every tool in tool_groups must exist in the tool registry.  
  
Rule 3  
--------------------------------------------------------------------  
Every route target in workflow_routes must exist in stage_registry.  
  
Rule 4  
--------------------------------------------------------------------  
Every failure route target must exist in stage_registry or be a known  
failure-stage alias.  
  
Rule 5  
--------------------------------------------------------------------  
Every role overlay role_name must exist in role_capabilities.  
  
Rule 6  
--------------------------------------------------------------------  
Every explicit_allow or explicit_block tool must exist in tool_groups or  
tool registry.  
  
Rule 7  
--------------------------------------------------------------------  
A stage cannot have:  
- auto_continue_allowed = true  
and  
- approval_required = true  
at the same time.  
  
Rule 8  
--------------------------------------------------------------------  
A stage with access_mode = FINALIZATION_GATED should default to:  
- review_required = true  
- audit_required = true  
unless explicitly overridden with justification.  
  
====================================================================  
21. RESOLVER MERGE LOGIC  
====================================================================  
  
Suggested merge precedence:  
  
base stage config  
-> governance overlay  
-> domain overlay  
-> role overlay  
-> environment overlay  
-> runtime conditional rules  
-> request-time overrides  
  
In pseudocode:  
  
effective_stage = merge(  
  stage_registry[stage_name],  
  governance_overlays.stage_rules.get(stage_name, {}),  
  domain_overlay.stage_overrides.get(stage_name, {}),  
  role_overlay.stage_overrides.get(stage_name, {}),  
  environment_overlay.stage_overrides.get(stage_name, {}),  
  evaluate_conditional_rules(runtime_context),  
  request_overrides  
)  
  
====================================================================  
22. RECOMMENDED PYTHON LOADER CLASSES  
====================================================================  
  
Suggested classes:  
  
1. RuntimeConfigLoader  
Responsibilities:  
- load all runtime config files  
- resolve file refs from runtime_master  
  
2. StageConfigResolver  
Responsibilities:  
- merge stage registry + stage tool matrix + overlays  
  
3. RoleConfigResolver  
Responsibilities:  
- apply role capability rules and role overlays  
  
4. ToolGroupResolver  
Responsibilities:  
- expand tool groups and virtual tool groups  
  
5. GovernanceRuleResolver  
Responsibilities:  
- apply review/approval/audit requirements  
  
6. RetryPolicyResolver  
Responsibilities:  
- resolve retry_mode by tool  
  
Suggested file structure:  
  
platform_core/runtime/runtime_config_loader.py  
platform_core/runtime/stage_config_resolver.py  
platform_core/runtime/role_config_resolver.py  
platform_core/runtime/tool_group_resolver.py  
platform_core/runtime/governance_rule_resolver.py  
platform_core/runtime/retry_policy_resolver.py  
  
====================================================================  
23. RECOMMENDED OUTPUT OF THE RESOLVER  
====================================================================  
  
Final resolved runtime decision example:  
  
{  
  "stage_name": "validation_conclusion_review",  
  "actor_role": "validator",  
  "access_mode": "FINALIZATION_GATED",  
  "preconditions_passed": true,  
  "missing_preconditions": [],  
  "allowed_tools": [  
    "build_validation_conclusion_options",  
    "get_review",  
    "build_review_payload",  
    "validate_review_action",  
    "approve_review",  
    "approve_review_with_conditions",  
    "escalate_review",  
    "capture_review_decision",  
    "finalize_validation_conclusion",  
    "create_remediation_action",  
    "patch_workflow_state",  
    "route_next_stage"  
  ],  
  "blocked_tools": [  
    "execute_dataprep_request",  
    "build_fine_bins",  
    "ingest_monitoring_snapshot"  
  ],  
  "review_required": true,  
  "approval_required": true,  
  "audit_required": true,  
  "auto_continue_allowed": false,  
  "recommended_ui_mode": "review_shell",  
  "recommended_interaction_mode": "approve",  
  "recommended_token_mode": "deep_review_mode",  
  "recommended_next_routes": [  
    "reporting_technical",  
    "remediation_action_setup"  
  ]  
}  
  
====================================================================  
24. FUTURE-PROOFING RECOMMENDATIONS  
====================================================================  
  
1. Keep stage registry declarative  
--------------------------------------------------------------------  
Do not hardcode stage metadata in Python unless absolutely required.  
  
2. Support virtual tool groups  
--------------------------------------------------------------------  
This keeps config compact and readable.  
  
3. Separate domain overlays  
--------------------------------------------------------------------  
Scorecard, LGD, PD, ECL, and monitoring will diverge over time.  
  
4. Keep role overlay separate from role capability  
--------------------------------------------------------------------  
Capability = what the role can do generally.  
Overlay = temporary or environment/domain-specific change.  
  
5. Use environment overlays carefully  
--------------------------------------------------------------------  
Prod should be stricter than dev/uat.  
  
6. Keep conditional rules simple at first  
--------------------------------------------------------------------  
A small rules engine is enough. Do not overbuild.  
  
7. Version the config  
--------------------------------------------------------------------  
Every runtime config pack should have version and hash.  
  
====================================================================  
25. FINAL RECOMMENDATION  
====================================================================  
  
Best implementation approach:  
  
- store configs in YAML  
- validate them with JSON schema or Pydantic models  
- load through ConfigService  
- resolve through dedicated runtime resolver classes  
- output one final runtime decision object for the UI and agent  
  
This gives you:  
- maintainability  
- transparency  
- easy updates  
- lower code churn  
- cleaner governance control  
  
====================================================================  
NEXT BEST ARTIFACT  
====================================================================  
  
The next strongest artifact is a:  
  
Pydantic schema design for these runtime config files,  
including:  
- class names  
- fields  
- validators  
- default values  
- enum definitions  
  
That would make the config pack directly implementable in Python.  
  
====================================================================  
END OF DATA-DRIVEN YAML / JSON CONFIG PACK  
====================================================================  
