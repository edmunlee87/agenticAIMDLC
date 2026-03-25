# Registry table  
  
====================================================================  
TOOL REGISTRY TABLE  
AGENTIC AI MDLC FRAMEWORK  
AGENT-CALLABLE TOOL MASTER REFERENCE  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This reference defines the recommended tool registry for the agentic AI  
MDLC framework.  
  
It maps:  
- tool name  
- backing class and function  
- tool purpose  
- when the agent should call it  
- required inputs  
- key outputs  
- common failure modes  
- whether safe retry is allowed  
- whether the tool should open a review  
- whether the tool should patch workflow state  
  
This is intended to drive:  
- agent tool catalog design  
- tool wrapper implementation  
- allowlist resolution  
- orchestration policy  
- HITL design  
- observability expectations  
- audit integration  
  
NOTES  
--------------------------------------------------------------------  
1. A “tool” here means an agent-callable action, not every internal  
   helper function.  
2. Internal engines, builders, and utilities should normally NOT be  
   directly exposed as tools.  
3. Tools should ideally map to public façade methods on service classes  
   or controller methods.  
4. Controller-backed tools are preferred where orchestration across  
   multiple SDKs is required.  
5. SDK-backed tools are preferred where the action is atomic and  
   deterministic.  
  
COLUMNS  
--------------------------------------------------------------------  
- Tool Name  
- Backing Class.Function  
- Tool Description  
- When Agent Should Call  
- Required Inputs  
- Key Outputs  
- Common Failure Modes  
- Safe Retry?  
- Should Open Review?  
- Should Patch Workflow?  
- Audit Hook?  
- Event Hook?  
- Suggested Tool Type  
  
Suggested Tool Type values:  
- Controller Tool  
- SDK Tool  
- Read Tool  
- Write Tool  
- Review Tool  
- Validation Tool  
- Routing Tool  
- Reporting Tool  
- Monitoring Tool  
- Retrieval Tool  
  
====================================================================  
A. SESSION / RUNTIME / WORKFLOW TOOLS  
====================================================================  
  
| Tool Name | Backing Class.Function | Tool Description | When Agent Should Call | Required Inputs | Key Outputs | Common Failure Modes | Safe Retry? | Should Open Review? | Should Patch Workflow? | Audit Hook? | Event Hook? | Suggested Tool Type |  
|---|---|---|---|---|---|---|---|---|---|---|---|---|  
| open_session | SessionController.open_session | Start or restore session context | New user entry, missing active session, no resolved context | user_context | session_id, project choices, pending work summary | missing user context, registry unavailable | Yes | No | Yes | No | Yes | Controller Tool |  
| resume_session | SessionController.resume_session | Resume existing session and pending work | User chooses resume or interrupted work detected | session_id, actor | active project/run context, pending review info | invalid session_id, expired state, unresolved run | Yes | Optional | Yes | Optional | Yes | Controller Tool |  
| resolve_runtime_stack | RuntimeResolver.resolve | Resolve active role/domain/stage/tool/UI stack | Before any stage action or when context changes | runtime_context | resolved skills, ui mode, sdk allowlist, interaction mode | invalid runtime context, unmapped stage | Yes | No | No | No | Optional | Routing Tool |  
| get_workflow_state | WorkflowService.get_workflow_state | Read current workflow state | Before routing, before recovery, before review, before resume | run_id | workflow state summary, current stage, refs | run not found | Yes | No | No | No | No | Read Tool |  
| patch_workflow_state | WorkflowService.update_workflow_state | Apply state patch to workflow | After finalization, selection, conclusion, monitoring action | run_id, state_patch | updated workflow state, patch applied summary | invalid patch, stale run, guard failure | Limited | No | Yes | Optional | Yes | Write Tool |  
| route_next_stage | WorkflowService.route_next_stage | Determine next stage and blockers | After completing a stage, after review decision, after selection | run_id, current_stage, context | recommended_next_stage, blockers, route_reason | invalid current stage, dependency missing | Yes | Optional | Optional | No | Yes | Routing Tool |  
| create_candidate_version | WorkflowService.create_candidate_version | Register a candidate version for later comparison/selection | After model fit, binning candidate build, shortlist variants | run_id, candidate_payload | candidate_version_id, candidate summary | invalid payload, missing refs | Yes | Optional | Yes | Optional | Yes | Write Tool |  
| select_candidate_version | WorkflowService.select_candidate_version | Record final candidate selection | After governed comparison and final choice | run_id, candidate_version_id, rationale | selected candidate id, workflow patch | invalid candidate id, selection conflict | No unless transient infra | Yes often | Yes | Yes | Yes | Review Tool |  
| create_checkpoint | WorkflowService.create_checkpoint | Save recovery checkpoint | Before risky stage, before long-running run, before review branching | run_id, checkpoint_payload | checkpoint_id, checkpoint summary | invalid run, storage issue | Yes | No | Optional | No | Yes | Write Tool |  
| resolve_recovery_path | WorkflowService.resolve_recovery_path | Recommend retry/rerun/rollback path | Failure detected, session resumes from error, guarded rollback needed | run_id, failure_context | recommended recovery options, safe path summary | missing event history, ambiguous failure state | Yes | Yes sometimes | Optional | Optional | Yes | Routing Tool |  
  
====================================================================  
B. REVIEW / HITL / POLICY TOOLS  
====================================================================  
  
| Tool Name | Backing Class.Function | Tool Description | When Agent Should Call | Required Inputs | Key Outputs | Common Failure Modes | Safe Retry? | Should Open Review? | Should Patch Workflow? | Audit Hook? | Event Hook? | Suggested Tool Type |  
|---|---|---|---|---|---|---|---|---|---|---|---|---|  
| create_review | HITLService.create_review | Create a governed review record | Policy requires human review, candidate comparison complete, breach review needed | review_type, review_payload, actor_context | review_id, review_status, display summary | invalid review type, incomplete payload | Yes | Yes | Optional | Optional | Yes | Review Tool |  
| get_review | HITLService.get_review | Read review record and state | Load review, refresh state, inspect pending review | review_id | review record, status, actor context | review not found | Yes | Yes | No | No | No | Read Tool |  
| build_review_payload | HITLService.build_review_payload | Build normalized review payload | Before rendering governed workspace | review_type, source_context | ReviewPayload, allowed actions, evidence summaries | missing source refs, unsupported review type | Yes | Yes | No | No | Optional | Review Tool |  
| validate_review_action | HITLService.validate_action | Validate structured human action | Before preview/finalization/escalation | review_id, interaction_payload | validation result, allowed/block summary | invalid action, role mismatch, missing rationale | Yes | Yes | No | No | Optional | Validation Tool |  
| transition_review_state | HITLService.transition_review_state | Move review through lifecycle | After preview generation, approval, escalation, expiration | review_id, target_status, context | updated review state | invalid transition, stale review | Limited | Yes | Optional | Optional | Yes | Review Tool |  
| approve_review | HITLService.approve_review | Approve review without conditions | Human approves acceptable result | review_id, actor, optional comment | approval result, decision refs | actor not allowed, review not ready | No unless infra transient | Yes | Yes | Yes | Yes | Review Tool |  
| approve_review_with_conditions | HITLService.approve_with_conditions | Approve with conditions | Human approves but wants explicit conditions tracked | review_id, actor, conditions, optional comment | approval result, condition refs, decision refs | missing conditions, actor not allowed | No unless infra transient | Yes | Yes | Yes | Yes | Review Tool |  
| escalate_review | HITLService.escalate_review | Escalate review to higher authority/role | Severe finding, deadlock, timeout, policy escalation | review_id, reason, target_role optional | escalation record, updated role path | invalid review state, missing escalation target | Limited | Yes | Optional | Yes | Yes | Review Tool |  
| capture_review_decision | HITLService.capture_decision | Capture final review action and outputs | After human final action or structured resolution | review_id, action, interaction_payload | decision result, state patch, next-step hints | invalid action, unresolved preview state | No unless transient infra | Yes | Yes | Yes | Yes | Review Tool |  
| load_policy_pack | PolicyService.load_policy_pack | Load effective policy pack | Before policy checks, stage gating, approvals | policy_mode, domain optional, stage optional | effective policy pack | policy not found, config issue | Yes | No | No | No | Optional | Read Tool |  
| evaluate_metric_set_against_policy | PolicyService.evaluate_metric_set | Evaluate metrics against policy thresholds | After metrics/diagnostics, before selection or monitoring disposition | metric_results, policy_pack | threshold evaluation results | incompatible metric format | Yes | Optional | Optional | Optional | Optional | Validation Tool |  
| detect_policy_breaches | PolicyService.detect_breaches | Summarize material breaches | After threshold evaluation | evaluation_results, context optional | breach summary, severity | malformed evaluation results | Yes | Yes maybe | Optional | Optional | Optional | Validation Tool |  
| get_stage_controls | PolicyService.get_stage_controls | Read stage controls and required gates | Before entering stage or finalizing stage | stage_name, policy_pack | stage controls | unknown stage | Yes | No | No | No | No | Read Tool |  
| requires_human_review | PolicyService.requires_human_review | Determine if review is mandatory | Before automatic continuation | stage_name, context, policy_pack | boolean + rationale | bad policy pack, stage mismatch | Yes | Yes if true | No | No | Optional | Validation Tool |  
| get_approval_requirements | PolicyService.get_approval_requirements | Resolve required approver role/path | Before approval UI or escalation | stage_name, context, policy_pack | approval requirements | missing policy rule | Yes | Yes maybe | No | No | Optional | Read Tool |  
| can_actor_approve | PolicyService.can_actor_approve | Validate approval permission | Before accepting final approval action | actor, stage_name, policy_pack | ValidationResultBase | role mismatch, invalid stage | Yes | No | No | No | Optional | Validation Tool |  
| should_escalate | PolicyService.should_escalate | Determine whether escalation is required | Severe issue, repeated breach, blocked review | context, policy_pack | escalation recommendation | insufficient context | Yes | Yes maybe | Optional | Optional | Optional | Validation Tool |  
| is_waivable | PolicyService.is_waivable | Determine waiver eligibility | Issue exists but continuation requested | issue_context, policy_pack | waiver eligibility + requirements | missing policy/issue data | Yes | Yes maybe | Optional | Yes if approved | Optional | Validation Tool |  
  
====================================================================  
C. DATASET / DATAPREP / DQ TOOLS  
====================================================================  
  
| Tool Name | Backing Class.Function | Tool Description | When Agent Should Call | Required Inputs | Key Outputs | Common Failure Modes | Safe Retry? | Should Open Review? | Should Patch Workflow? | Audit Hook? | Event Hook? | Suggested Tool Type |  
|---|---|---|---|---|---|---|---|---|---|---|---|---|  
| validate_dataprep_config | DataPrepService.validate_dataprep_config | Validate dataprep config structure | Before any dataprep execution | config | validation summary | missing required sections, unsupported template fields | Yes | Optional if governance wants config review | No | Optional | Optional | Validation Tool |  
| validate_template_request | DataPrepService.validate_template_request | Validate template + domain + data structure compatibility | Before dataprep request execution | template_id, domain, data_structure_type | validation result | unsupported template/domain combo | Yes | No | No | No | Optional | Validation Tool |  
| execute_dataprep_request | DataPrepService.execute_request | Logical dataprep entrypoint | When agent wants one standard dataprep execution call | request | dataset refs, manifest refs, split summary, target summary | invalid lineage config, missing source mappings | Limited if same request and no partial state issues | Optional | Yes | Optional | Yes | SDK Tool |  
| build_cross_sectional_dataset | DataPrepService.build_cross_sectional_dataset | Prepare cross-sectional dataset | Cross-sectional modeling use case | request | dataset snapshot summary | bad grain, source mismatch | Limited | Optional | Yes | Optional | Yes | SDK Tool |  
| build_panel_dataset | DataPrepService.build_panel_dataset | Prepare panel dataset | Panel or repeated observation modeling | request | dataset snapshot summary | duplicate grain, time misalignment | Limited | Optional | Yes | Optional | Yes | SDK Tool |  
| build_time_series_dataset | DataPrepService.build_time_series_dataset | Prepare time series dataset | Portfolio series, macro series, forecasting data | request | dataset snapshot summary | time index issues, missing series coverage | Limited | Optional | Yes | Optional | Yes | SDK Tool |  
| build_cohort_dataset | DataPrepService.build_cohort_dataset | Prepare cohort-aligned dataset | Cohort-based modeling, rollout analyses | request | dataset snapshot summary | cohort definition errors | Limited | Optional | Yes | Optional | Yes | SDK Tool |  
| build_event_history_dataset | DataPrepService.build_event_history_dataset | Prepare spell/event-history dataset | Hazard / survival / cure modeling | request | dataset snapshot summary | spell logic errors, censoring mismatch | Limited | Optional | Yes | Optional | Yes | SDK Tool |  
| reproduce_dataset | DataPrepService.reproduce_dataset | Rebuild prior dataset snapshot deterministically | Reproducibility, validation, remediation | dataset_snapshot_id, overrides optional | reproduced dataset refs, comparison summary | missing historical config/artifacts | Limited | Optional | Optional | Yes | Yes | SDK Tool |  
| build_cross_sectional_dataset_spark | SparkDataPrepService.build_cross_sectional_dataset_spark | Spark-heavy cross-sectional dataprep | Heavy data in Spark environment | request, spark_session optional | dataset refs, row counts, manifest refs | Spark unavailable, join explosion, write failure | Limited after checking idempotency | Optional | Yes | Optional | Yes | SDK Tool |  
| build_panel_dataset_spark | SparkDataPrepService.build_panel_dataset_spark | Spark-heavy panel dataprep | Panel data in Spark | request, spark_session optional | dataset refs, row counts, split summary | Spark unavailable, duplicate entity-time grain | Limited | Optional | Yes | Optional | Yes | SDK Tool |  
| build_time_series_dataset_spark | SparkDataPrepService.build_time_series_dataset_spark | Spark-heavy time series prep | Time series build in Spark | request, spark_session optional | dataset refs, time coverage | Spark unavailable, missing periods | Limited | Optional | Yes | Optional | Yes | SDK Tool |  
| build_cohort_dataset_spark | SparkDataPrepService.build_cohort_dataset_spark | Spark-heavy cohort prep | Cohort pipeline in Spark | request, spark_session optional | dataset refs, cohort coverage | Spark unavailable, bad cohort windows | Limited | Optional | Yes | Optional | Yes | SDK Tool |  
| build_event_history_dataset_spark | SparkDataPrepService.build_event_history_dataset_spark | Spark-heavy event history prep | Survival/cure spell prep in Spark | request, spark_session optional | dataset refs, spell summary | Spark unavailable, spell builder issues | Limited | Optional | Yes | Optional | Yes | SDK Tool |  
| run_prep_quality_checks_spark | SparkDataPrepService.run_prep_quality_checks_spark | Run scalable quality checks on prepared data | After dataprep execution, before readiness | dataset_ref, check_pack optional | prep quality summary, warnings | missing dataset ref, Spark read issues | Yes | Yes if major issues | Optional | Yes | Validation Tool |  
| register_dataset | DatasetService.register_dataset | Register canonical dataset identity | First time dataset created | dataset_payload | dataset_id | malformed metadata | Yes | No | Optional | Optional | Yes | Write Tool |  
| create_dataset_snapshot | DatasetService.create_snapshot | Register dataset snapshot version | After prep execution | dataset_id, snapshot_payload | dataset_snapshot_id | missing dataset id | Yes | No | Yes | Optional | Yes | Write Tool |  
| register_dataset_split | DatasetService.register_split | Register split metadata | After split creation | dataset_snapshot_id, split_payload | split_id, split summary | missing snapshot, invalid split payload | Yes | Optional if split is governed | Optional | Yes | Write Tool |  
| create_sample_reference | DatasetService.create_sample_reference | Record sample construction logic | After sample finalized | dataset_snapshot_id, sample_payload | sample_reference_id | missing snapshot | Yes | No | No | Optional | Write Tool |  
| create_lineage_reference | DatasetService.create_lineage_reference | Record source lineage | After lineage resolved | dataset_snapshot_id, lineage_payload | lineage_reference_id | missing snapshot, lineage gaps | Yes | No | No | Optional | Write Tool |  
| validate_dataset_contract | DatasetService.validate_dataset_contract | Validate prepared dataset against contract | Before modeling / validation | dataset_schema, contract | ValidationResultBase | contract mismatch, missing keys | Yes | Yes if invalid and governed | No | Optional | Validation Tool |  
| get_dataset_snapshot | DatasetService.get_dataset_snapshot | Read dataset snapshot metadata | Before modeling, validation, monitoring | dataset_snapshot_id | snapshot metadata | not found | Yes | No | No | No | Read Tool |  
| run_schema_checks | DQService.run_schema_checks | Validate schema correctness | After prep or before using existing dataset | data_ref, expected_schema | ValidationResultBase | missing columns, wrong types | Yes | Optional | Optional | Optional | Validation Tool |  
| run_missingness_checks | DQService.run_missingness_checks | Profile null and missingness patterns | Data readiness, validation, monitoring prep | data_ref, rules optional | missingness summary | unreadable data ref | Yes | Optional | Optional | Optional | Validation Tool |  
| run_consistency_checks | DQService.run_consistency_checks | Run key/date/status consistency checks | Data readiness, validation | data_ref, rules | consistency summary | bad rules, unresolved duplicates | Yes | Optional | Optional | Optional | Validation Tool |  
| build_distribution_profile | DQService.build_distribution_profile | Create compact data profile | DQ summary, drift baseline, review support | data_ref, columns optional | profile summary | heavy data read issue | Yes | No | No | Optional | Read Tool |  
| run_business_rule_checks | DQService.run_business_rule_checks | Apply governed business checks | Domain-specific DQ needs | data_ref, rule_set | rule check summary | bad rule set | Yes | Optional | Optional | Optional | Validation Tool |  
| build_dq_summary | DQService.build_dq_summary | Aggregate DQ outputs into compact summary | After running several checks | check_results | DQ summary, severity summary | malformed check result list | Yes | Yes if severe | Optional | Yes | Validation Tool |  
| create_dq_exception | DQService.create_dq_exception | Convert material DQ failure into exception | Material DQ issue needs governance/remediation | dq_summary, severity | dq_exception refs | invalid severity mapping | No unless infra transient | Yes | Optional | Yes | Yes | Review Tool |  
  
====================================================================  
P. FEATURE / EVALUATION TOOLS  
====================================================================  
  
| Tool Name | Backing Class.Function | Tool Description | When Agent Should Call | Required Inputs | Key Outputs | Common Failure Modes | Safe Retry? | Should Open Review? | Should Patch Workflow? | Audit Hook? | Event Hook? | Suggested Tool Type |  
|---|---|---|---|---|---|---|---|---|---|---|---|---|  
| apply_feature_transformations | FeatureService.apply_transformations | Apply standard feature transforms | Feature engineering stage | data_ref, feature_rules | transformed feature refs | invalid rules, missing columns | Yes | No | Optional | Optional | Yes | SDK Tool |  
| build_feature_lags | FeatureService.build_lags | Create lagged features | Panel/time-series feature prep | data_ref, lag_spec | lag feature refs | no time key, invalid lag spec | Yes | No | Optional | Optional | Yes | SDK Tool |  
| build_feature_differences | FeatureService.build_differences | Create differenced features | Time-series/panel transforms | data_ref, diff_spec | diff feature refs | invalid diff spec | Yes | No | Optional | Optional | Yes | SDK Tool |  
| build_grouped_features | FeatureService.build_grouped_features | Build grouped/aggregated features | Hierarchical or segment features needed | data_ref, grouping_spec | grouped feature refs | invalid grouping, bad aggregation | Yes | No | Optional | Optional | Yes | SDK Tool |  
| encode_categorical_features | FeatureService.encode_categorical | Encode categories with governed rules | Feature engineering for categorical vars | data_ref, encoding_spec | encoded feature refs | invalid mapping, unseen categories config | Yes | No | Optional | Optional | Yes | SDK Tool |  
| register_feature_metadata | FeatureService.register_feature_metadata | Persist feature catalog metadata | After feature set built | feature_metadata_payload | metadata refs | bad payload | Yes | No | Optional | Optional | Yes | Write Tool |  
| register_feature_lineage | FeatureService.register_feature_lineage | Persist feature lineage | After important feature derivations | feature_name, lineage_payload | lineage refs | incomplete source lineage | Yes | No | Optional | Optional | Yes | Write Tool |  
| compute_metrics | EvaluationService.compute_metrics | Compute standardized metrics | After model fit, after scoring, during monitoring | model_type, inputs, metric_set optional | metric results | bad input refs, unsupported model_type | Yes | Optional if material selection | Optional | Yes | SDK Tool |  
| run_diagnostics | EvaluationService.run_diagnostics | Compute diagnostics | After model fit or during validation | model_type, inputs, diagnostic_set optional | diagnostic results | unsupported diagnostics, bad refs | Yes | Optional if bad diagnostics | Optional | Yes | SDK Tool |  
| run_stability_checks | EvaluationService.run_stability_checks | Compute stability/drift checks | Monitoring, validation, challenger comparison | current_ref, baseline_ref, config | stability results | missing baseline, bad schema alignment | Yes | Optional if breach | Optional | Yes | SDK Tool |  
| run_calibration_checks | EvaluationService.run_calibration_checks | Compute calibration views | Validation and monitoring | actual_ref, predicted_ref, config optional | calibration summary | missing actuals/preds | Yes | Optional if poor calibration | Optional | Yes | SDK Tool |  
| compare_candidates | EvaluationService.compare_candidates | Compare candidate models/packages | Binning, model selection, method selection | candidate_refs, comparison_spec | comparison summary, ranked candidates | inconsistent candidate metadata | Yes | Yes often | Optional | Yes | Review Tool |  
| evaluate_thresholds | EvaluationService.evaluate_thresholds | Apply threshold pack to metric results | After metrics/diagnostics or monitoring KPI calc | metric_results, threshold_pack | pass/warn/breach results | missing threshold definitions | Yes | Optional if severe | Optional | Optional | Validation Tool |  
| compare_to_benchmark | EvaluationService.compare_to_benchmark | Compare current results to benchmark | Validation and annual review | current_summary, benchmark_ref | benchmark gap summary | missing benchmark refs | Yes | Optional | Optional | Optional | Validation Tool |  
  
====================================================================  
Q. SCORECARD TOOLS  
====================================================================  
  
| Tool Name | Backing Class.Function | Tool Description | When Agent Should Call | Required Inputs | Key Outputs | Common Failure Modes | Safe Retry? | Should Open Review? | Should Patch Workflow? | Audit Hook? | Event Hook? | Suggested Tool Type |  
|---|---|---|---|---|---|---|---|---|---|---|---|---|  
| build_fine_bins | ScorecardService.build_fine_bins | Create initial fine bins | Start of scorecard binning stage | dataset_ref, variable_spec, config optional | fine bin refs, bin summaries | bad variable spec, missing target | Yes | Optional | Optional | Optional | Yes | SDK Tool |  
| build_coarse_bin_candidate | ScorecardService.build_coarse_bin_candidate | Generate coarse bin candidate | After fine bins available | fine_bin_ref, merge_rules optional | candidate version ref, support summary | invalid merge plan, unstable support | Yes | Yes often | Optional | Optional | Yes | Review Tool |  
| preview_edited_bins | ScorecardService.preview_edited_bins | Preview manual bin edits | Human edits bins in review workspace | fine_bin_ref, edited_bin_groups | preview metrics, warnings | invalid edit groups | Yes | Yes | No | No | Yes | Review Tool |  
| finalize_coarse_bins | ScorecardService.finalize_coarse_bins | Finalize accepted coarse bins | After human accepts/edits bins | candidate_ref, final_bin_groups, rationale optional | final coarse bin ref | invalid final grouping, unmet support rules | No unless infra transient | Yes | Yes | Yes | Yes | Review Tool |  
| compare_binning_candidates | ScorecardService.compare_binning_candidates | Compare binning candidates | Before choosing final binning version | candidate_refs, comparison_spec optional | comparison summary | incompatible candidate summaries | Yes | Yes | Optional | Optional | Yes | Review Tool |  
| compute_woe_iv | ScorecardService.compute_woe_iv | Compute WOE/IV from final bins | After coarse bins finalized | coarse_bin_ref, target_ref optional | WOE/IV refs, variable summary | missing target, broken bins | Yes | Optional | Optional | Optional | Yes | SDK Tool |  
| build_feature_shortlist | ScorecardService.build_feature_shortlist | Build shortlist of scorecard variables | After WOE/IV stage | woe_iv_ref, shortlist_rules | shortlist ref, rationale summary | rule conflicts, insufficient variables | Yes | Yes often | Optional | Optional | Yes | Review Tool |  
| fit_scorecard_candidate_set | ScorecardService.fit_candidate_set | Fit scorecard candidate models | After shortlist finalized | dataset_ref, feature_set_ref, model_spec | candidate versions, metrics | fitting failure, bad features, singularity | Limited | Yes often | Yes if candidate versions registered | Optional | Yes | SDK Tool |  
| scale_scorecard | ScorecardService.scale_scorecard | Convert score outputs into score scale | After final candidate chosen | model_candidate_ref, scaling_spec | scaled score output ref | invalid scaling spec | Yes | Yes if scaling governed | Optional | Optional | Yes | Review Tool |  
| build_score_bands | ScorecardService.build_score_bands | Generate score bands | After scaling complete | score_output_ref, band_spec | band refs, band summary | bad band rules | Yes | Optional | Optional | Optional | Yes | SDK Tool |  
| build_scorecard_output_bundle | ScorecardService.build_scorecard_output_bundle | Bundle all final scorecard outputs | End of scorecard build | context | output bundle refs | missing required artifacts | Yes | Optional | Optional | Yes | Yes | Reporting Tool |  
  
====================================================================  
R. VALIDATION TOOLS  
====================================================================  
  
| Tool Name | Backing Class.Function | Tool Description | When Agent Should Call | Required Inputs | Key Outputs | Common Failure Modes | Safe Retry? | Should Open Review? | Should Patch Workflow? | Audit Hook? | Event Hook? | Suggested Tool Type |  
|---|---|---|---|---|---|---|---|---|---|---|---|---|  
| create_validation_scope | ValidationService.create_validation_scope | Initialize validation scope | Start of validation lifecycle | project_id, model_ref, scope_config | validation_run_id, scope summary | invalid scope config | Yes | Yes often | Yes | Optional | Yes | Review Tool |  
| intake_validation_evidence | ValidationService.intake_evidence | Intake evidence for validation | After scope created | validation_run_id, evidence_refs | evidence inventory | missing artifacts, bad refs | Yes | Optional | Optional | Optional | Yes | SDK Tool |  
| assess_evidence_completeness | ValidationService.assess_evidence_completeness | Check if evidence is sufficient | Before methodology/data/final conclusion | validation_run_id, required_evidence_pack | completeness summary, missing evidence | wrong evidence pack, missing refs | Yes | Yes if incomplete | Optional | Optional | Yes | Validation Tool |  
| evaluate_fitness_dimensions | ValidationService.evaluate_fitness_dimensions | Evaluate fit-for-use dimensions | Mid validation after evidence and metrics available | validation_run_id, evidence_summary, metric_summary optional | fitness summary | insufficient evidence, bad metric mapping | Yes | Yes often | Optional | Optional | Yes | Validation Tool |  
| create_validation_finding | ValidationService.create_finding | Create validation finding | Methodology issue, data issue, implementation issue detected | validation_run_id, finding_payload | finding id, finding summary | malformed finding payload | Yes | Yes if governed | Optional | Yes | Yes | Review Tool |  
| assess_finding_severity | ValidationService.assess_severity | Assess finding severity | After finding created | finding_payload, policy_pack optional | severity summary | insufficient finding info | Yes | Optional | Optional | Optional | Optional | Validation Tool |  
| build_validation_conclusion_options | ValidationService.build_conclusion_options | Suggest structured conclusion options | Before final validator choice | validation_run_id, fitness_summary, findings | conclusion options, conditions summary | missing fitness or findings | Yes | Yes | Optional | Optional | Yes | Review Tool |  
| finalize_validation_conclusion | ValidationService.finalize_conclusion | Record final validation conclusion | Human validator finalizes fit-for-use decision | validation_run_id, conclusion_payload, actor | final conclusion refs, state patch | actor unauthorized, incomplete conclusion | No unless transient infra | Yes always | Yes | Yes | Yes | Review Tool |  
| create_remediation_action | ValidationService.create_remediation_action | Create remediation linked to finding | Finding needs follow-up | finding_id, remediation_payload | remediation action refs | invalid finding id | Yes | Yes if assignment review exists | Optional | Yes | Yes | Review Tool |  
| build_validation_output_bundle | ValidationService.build_validation_output_bundle | Assemble validation outputs | End of validation or for reporting | validation_run_id | validation bundle refs | missing required artifacts | Yes | Optional | Optional | Yes | Yes | Reporting Tool |  
  
====================================================================  
S. REPORTING TOOLS  
====================================================================  
  
| Tool Name | Backing Class.Function | Tool Description | When Agent Should Call | Required Inputs | Key Outputs | Common Failure Modes | Safe Retry? | Should Open Review? | Should Patch Workflow? | Audit Hook? | Event Hook? | Suggested Tool Type |  
|---|---|---|---|---|---|---|---|---|---|---|---|---|  
| build_technical_report | ReportingService.build_technical_report | Build technical model/validation report | Report drafting stage | report_context, section_spec optional | report section refs | missing narrative/artifact refs | Yes | Optional | No | Optional | Yes | Reporting Tool |  
| build_executive_summary | ReportingService.build_executive_summary | Build exec summary | Governance or committee storytelling | summary_context | exec summary refs | insufficient summary context | Yes | Optional | No | Optional | Yes | Reporting Tool |  
| build_committee_pack | ReportingService.build_committee_pack | Build committee-ready content pack | Governance submission preparation | pack_context | committee pack refs | missing mandatory sections | Yes | Yes often | No | Optional | Yes | Reporting Tool |  
| build_validation_note | ReportingService.build_validation_note | Build validation memo/note | Validation reporting stage | validation_context | validation note refs | missing validation refs | Yes | Optional | No | Optional | Yes | Reporting Tool |  
| get_narrative_block | ReportingService.get_narrative_block | Retrieve approved narrative text block | Need consistent wording | block_id, audience optional | narrative block payload | block not found | Yes | No | No | No | No | Read Tool |  
| export_chart_refs | ReportingService.export_chart_refs | Prepare chart refs for pack | Building report or dashboard doc | artifact_ids | chart refs | missing chart artifacts | Yes | No | No | No | Optional | Read Tool |  
| export_table_refs | ReportingService.export_table_refs | Prepare table refs for pack | Building report or dashboard doc | artifact_ids | table refs | missing table artifacts | Yes | No | No | No | Optional | Read Tool |  
| assemble_pack | ReportingService.assemble_pack | Assemble final pack from section refs | Final output packaging | section_refs, pack_type | final pack ref | broken section refs, invalid pack order | Yes | Optional | No | Optional | Yes | Reporting Tool |  
  
====================================================================  
T. KNOWLEDGE / RETRIEVAL / FLOW / MONITORING TOOLS  
====================================================================  
  
| Tool Name | Backing Class.Function | Tool Description | When Agent Should Call | Required Inputs | Key Outputs | Common Failure Modes | Safe Retry? | Should Open Review? | Should Patch Workflow? | Audit Hook? | Event Hook? | Suggested Tool Type |  
|---|---|---|---|---|---|---|---|---|---|---|---|---|  
| create_knowledge_object | KnowledgeService.create_knowledge_object | Build governed knowledge object | After meaningful decision/finding/output | knowledge_payload | knowledge object summary | malformed payload | Yes | Optional | No | Optional | Yes | Write Tool |  
| register_knowledge | KnowledgeService.register_knowledge | Persist knowledge object | After knowledge object built | knowledge_object | knowledge_id | registry issue | Yes | No | No | Optional | Yes | Write Tool |  
| search_knowledge | KnowledgeService.search_knowledge | Search governed knowledge | Reuse prior knowledge, support validation/reporting | filters | search results | bad filters | Yes | No | No | No | No | Read Tool |  
| capture_knowledge_from_event | KnowledgeService.capture_from_event | Create knowledge from an event | Important event should become reusable memory | event_ref, capture_config optional | knowledge ref | event missing, summarization issue | Yes | Optional | No | Optional | Yes | Write Tool |  
| capture_knowledge_from_decision | KnowledgeService.capture_from_decision | Create knowledge from a formal decision | After approval, conclusion, major governed choice | decision_ref, summary_payload optional | knowledge ref | missing decision, poor summary payload | Yes | Optional | No | Yes maybe | Yes | Write Tool |  
| set_knowledge_quality_status | KnowledgeService.set_quality_status | Change quality/reuse status | Knowledge reviewed or superseded | knowledge_id, quality_status, review_note optional | updated status | invalid status | Yes | Yes if governed promotion | No | Yes maybe | Yes | Review Tool |  
| promote_knowledge | KnowledgeService.promote_knowledge | Promote knowledge scope | Project knowledge becomes domain/global reusable | knowledge_id, target_scope, actor optional | promoted knowledge summary | not eligible, actor not allowed | No unless infra transient | Yes often | No | Yes | Yes | Review Tool |  
| export_knowledge_bundle | KnowledgeService.export_knowledge_bundle | Export governed knowledge set | Sharing, backup, analytics, training | filters | export bundle refs | missing entries | Yes | No | No | Optional | Optional | Reporting Tool |  
| route_retrieval_query | RetrievalService.route_query | Build retrieval plan by context | Before semantic retrieval | query, runtime_context, retrieval_mode optional | retrieval plan | bad context | Yes | No | No | No | Optional | Retrieval Tool |  
| retrieve_context | RetrievalService.retrieve | Retrieve scoped context | Need relevant prior knowledge/docs | query, filters, budget_profile optional | retrieval results | retrieval backend unavailable | Yes if backend transient | No | No | No | Optional | Retrieval Tool |  
| rerank_retrieval_results | RetrievalService.rerank_results | Improve retrieval ordering | After retrieval returns noisy results | retrieval_results, rerank_spec optional | reranked results | malformed retrieval results | Yes | No | No | No | No | Retrieval Tool |  
| compress_retrieval_context | RetrievalService.compress_context | Compress retrieval set for prompt | Before agent prompt assembly | retrieval_results, compression_mode | compressed summary | malformed input | Yes | No | No | No | No | Retrieval Tool |  
| build_context_pack | RetrievalService.build_context_pack | Build agent-ready prompt pack | Agent needs compact context with refs | query, runtime_context, filters optional | ContextPack | retrieval/packaging failure | Yes | No | No | No | Optional | Retrieval Tool |  
| build_flow_nodes | FlowService.build_nodes | Build workflow graph nodes | Flow explorer/reporting | run_id, filters optional | node list | missing event state | Yes | No | No | No | No | Read Tool |  
| build_flow_edges | FlowService.build_edges | Build workflow graph edges | Flow explorer/reporting | run_id, filters optional | edge list | missing node/event relations | Yes | No | No | No | No | Read Tool |  
| summarize_flow | FlowService.summarize_flow | Build compact flow summary | Audit/executive summary, recovery analysis | run_id, summary_mode | flow summary | sparse event history | Yes | No | No | No | No | Read Tool |  
| build_flow_timeline | FlowService.build_timeline | Build chronological timeline | Audit, observability, flow UI | run_id, filters optional | timeline payload | missing event timestamps | Yes | No | No | No | No | Read Tool |  
| export_flow_graph | FlowService.export_graph | Export graph payload | UI/report integration | run_id, export_mode | graph bundle | export mode mismatch | Yes | No | No | No | Optional | Reporting Tool |  
| filter_flow_graph | FlowService.filter_graph | Filter existing flow graph | Drill into role/stage/branch | graph_ref, filter_spec | filtered graph payload | bad filter spec | Yes | No | No | No | No | Read Tool |  
| get_flow_drilldown_payload | FlowService.get_drilldown_payload | Get detail view for node | Node click in UI or report explanation | node_id, graph_ref | drilldown detail payload | missing node or refs | Yes | No | No | No | No | Read Tool |  
| get_monitoring_template | MonitoringService.get_monitoring_template | Load approved monitoring template | Before snapshot ingestion or dashboard build | model_family, template_id optional | template ref | template not found | Yes | No | No | No | No | Read Tool |  
| ingest_monitoring_snapshot | MonitoringService.ingest_snapshot | Ingest new monitoring snapshot | Monthly/periodic monitoring run | snapshot_payload, template_ref | snapshot ref | payload invalid, schema mismatch | Yes if idempotent design | Optional | Optional | Optional | Yes | Monitoring Tool |  
| validate_monitoring_snapshot | MonitoringService.validate_snapshot | Validate snapshot structure | Before append to history | snapshot_ref, template_ref | ValidationResultBase | invalid grain, duplicate snapshot | Yes | Yes if severe issue | No | Optional | Optional | Validation Tool |  
| append_monitoring_snapshot | MonitoringService.append_snapshot | Append snapshot to monitoring history | After validation passes | model_id, snapshot_ref | history refs | missing model/history state | Yes | No | Optional | Optional | Yes | Write Tool |  
| compute_monitoring_metrics | MonitoringService.compute_monitoring_metrics | Compute current monitoring KPIs | After snapshot append or refresh | model_id, snapshot_ref, metric_spec optional | KPI summary | missing baseline refs, metric calc fail | Yes | Optional | Optional | Optional | Yes | Monitoring Tool |  
| evaluate_monitoring_thresholds | MonitoringService.evaluate_monitoring_thresholds | Apply threshold logic to KPI set | After KPI calc | metric_summary, threshold_pack | breach summary | missing threshold pack | Yes | Yes if breach | Optional | Optional | Yes | Monitoring Tool |  
| compute_monitoring_drift | MonitoringService.compute_drift | Compute drift views | After current/baseline available | current_snapshot_ref, baseline_snapshot_ref, drift_spec optional | drift summary | baseline mismatch | Yes | Optional | Optional | Optional | Yes | Monitoring Tool |  
| compute_segment_monitoring | MonitoringService.compute_segment_monitoring | Compute segment drilldowns | Dashboard refresh and breach analysis | snapshot_ref, segment_spec | segment summary | bad segment spec | Yes | Optional | Optional | Optional | Yes | Monitoring Tool |  
| build_dashboard_payload | MonitoringService.build_dashboard_payload | Build UI-neutral dashboard data | Refresh dashboard workspace | model_id, snapshot_ref, dashboard_mode | dashboard payload ref | missing KPI/drift inputs | Yes | No | No | Optional | Yes | Monitoring Tool |  
| build_dashboard_config | MonitoringService.build_dashboard_config | Build dashboard card/chart config | Render monitoring dashboard | template_ref, dashboard_mode | dashboard config | invalid template | Yes | No | No | No | No | Read Tool |  
| create_monitoring_note | MonitoringService.create_monitoring_note | Record monitoring note/action | Monitoring review or breach disposition | model_id, snapshot_ref, note_payload | note/action refs | invalid payload | Yes | Yes if action assignment | Optional | Yes | Yes | Review Tool |  
| build_annual_review_pack | MonitoringService.build_annual_review_pack | Build annual monitoring review pack | Annual review cycle | model_id, period_spec | annual review pack refs | insufficient history | Yes | Yes often | Optional | Optional | Yes | Reporting Tool |  
| write_monitoring_outputs | MonitoringService.write_monitoring_outputs | Write monitoring outputs/artifacts | After dashboard or annual pack built | model_id, output_bundle | artifact refs | artifact write failure | Yes | No | No | Optional | Yes | Write Tool |  
  
====================================================================  
U. TOOL REGISTRY DESIGN RULES  
====================================================================  
  
1. Prefer Controller Tools when:  
--------------------------------------------------------------------  
- more than one SDK is involved  
- workflow patching is needed  
- review opening may be needed  
- audit/event hooks need coordination  
- UI and agent should see the same behavior  
  
Examples:  
- open_session  
- run_stage  
- submit_review_action  
- prepare_dataset  
- finalize_validation_conclusion  
- build_monitoring_dashboard  
  
2. Prefer SDK Tools when:  
--------------------------------------------------------------------  
- action is atomic  
- inputs/outputs are well-bounded  
- no cross-SDK orchestration is required beyond service composition  
- operation is deterministic and reusable  
  
Examples:  
- compute_metrics  
- build_fine_bins  
- validate_snapshot  
- build_context_pack  
  
3. Do not expose internal helper engines directly as tools  
--------------------------------------------------------------------  
Avoid direct tool exposure for:  
- MetricEngine  
- ConfigLoaderUtility  
- SparkUtils  
- NodeBuilder  
- EdgeBuilder  
- PackAssembler internals  
- TransformationEngine internals  
- ReviewPayloadMapper internals  
  
4. Every tool should return agent-readable hints  
--------------------------------------------------------------------  
Each tool wrapper should ensure outputs contain:  
- reasoning_summary  
- recommended_next_action  
- requires_human_review  
- suggested_followup_functions  
- safe_to_continue  
  
5. Review-opening tools should be explicit  
--------------------------------------------------------------------  
Do not rely on the agent to infer that a review must be created.  
Tool outputs should explicitly say:  
- should_open_review = true  
- review_type = ...  
- allowed_actions = ...  
  
====================================================================  
V. RECOMMENDED INITIAL TOOLSET FOR PHASE 1 TO PHASE 4  
====================================================================  
  
Recommended first tool exposure set:  
  
Core / Workflow:  
- open_session  
- resume_session  
- resolve_runtime_stack  
- get_workflow_state  
- patch_workflow_state  
- route_next_stage  
- create_candidate_version  
- select_candidate_version  
- resolve_recovery_path  
  
Review / Policy:  
- create_review  
- get_review  
- build_review_payload  
- validate_review_action  
- approve_review  
- approve_review_with_conditions  
- escalate_review  
- capture_review_decision  
- load_policy_pack  
- requires_human_review  
- get_approval_requirements  
- can_actor_approve  
  
Data:  
- validate_dataprep_config  
- execute_dataprep_request  
- build_cross_sectional_dataset_spark  
- build_panel_dataset_spark  
- build_time_series_dataset_spark  
- run_prep_quality_checks_spark  
- register_dataset  
- create_dataset_snapshot  
- validate_dataset_contract  
- build_dq_summary  
  
Evaluation / Domain:  
- compute_metrics  
- run_diagnostics  
- compare_candidates  
- evaluate_thresholds  
- build_fine_bins  
- build_coarse_bin_candidate  
- preview_edited_bins  
- finalize_coarse_bins  
- compute_woe_iv  
- build_feature_shortlist  
- fit_scorecard_candidate_set  
- scale_scorecard  
- build_score_bands  
- build_scorecard_output_bundle  
  
Validation / Reporting:  
- create_validation_scope  
- intake_validation_evidence  
- assess_evidence_completeness  
- evaluate_fitness_dimensions  
- create_validation_finding  
- build_validation_conclusion_options  
- finalize_validation_conclusion  
- create_remediation_action  
- build_validation_output_bundle  
- build_technical_report  
- build_validation_note  
- build_committee_pack  
- assemble_pack  
  
====================================================================  
W. RECOMMENDED NEXT ARTIFACT  
====================================================================  
  
The most useful next deliverable is a:  
  
TOOL INPUT / OUTPUT SCHEMA PACK  
  
with one section per tool showing:  
- exact JSON input schema  
- exact JSON output schema  
- required fields  
- optional fields  
- retry policy  
- observability event type  
- audit behavior  
- workflow patch behavior  
- review creation behavior  
  
That would be the most implementation-ready handoff for actual coding.  
  
====================================================================  
END OF TOOL REGISTRY TABLE  
====================================================================  
