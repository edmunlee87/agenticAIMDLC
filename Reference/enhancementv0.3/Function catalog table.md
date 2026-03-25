# Function catalog table  
  
  
====================================================================  
FUNCTION CATALOG TABLE  
PUBLIC METHOD MASTER REFERENCE  
AGENTIC AI MDLC FRAMEWORK  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This reference lists the main public methods across the platform in a  
coding-ready, implementation-oriented format.  
  
COLUMNS  
--------------------------------------------------------------------  
- File  
- Class  
- Function  
- Signature  
- Input Contract  
- Output Contract  
- Audit Hook  
- Event Hook  
- Review Hook  
- Next-Step Hint  
  
NOTES  
--------------------------------------------------------------------  
1. "Input Contract" refers to the main schema or payload expected.  
2. "Output Contract" is usually BaseResult, ValidationResultBase, or  
   StandardResponseEnvelope at controller level.  
3. "Audit Hook" means whether the method should normally trigger or  
   suggest audit recording.  
4. "Event Hook" means whether the method should normally emit an  
   observability event.  
5. "Review Hook" means whether the method can or should trigger a  
   governed review.  
6. "Next-Step Hint" is the kind of recommendation that should be placed  
   into agent_hint/workflow_hint.  
  
====================================================================  
A. PLATFORM CORE / CONTROLLERS / BRIDGES / RUNTIME  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| platform_core/runtime/resolver.py | RuntimeResolver | resolve | resolve(runtime_context: dict) | RuntimeContext | BaseResult containing ResolvedStack | No | Optional | No | load UI mode, allowlist, active stage skill |  
| platform_core/runtime/ui_mode_resolver.py | UIModeResolver | resolve | resolve(runtime_context: dict) | RuntimeContext | BaseResult | No | No | No | set ui_mode |  
| platform_core/runtime/interaction_mode_resolver.py | InteractionModeResolver | resolve | resolve(runtime_context: dict) | RuntimeContext | BaseResult | No | No | No | set interaction_mode |  
| platform_core/runtime/token_mode_resolver.py | TokenModeResolver | resolve | resolve(runtime_context: dict) | RuntimeContext | BaseResult | No | No | No | choose token budget mode |  
| platform_core/runtime/allowlist_resolver.py | AllowlistResolver | resolve | resolve(runtime_context: dict) | RuntimeContext | BaseResult | No | No | No | narrow SDK/tool access |  
| platform_core/controllers/session_controller.py | SessionController | open_session | open_session(user_context: dict) | user/session payload | StandardResponseEnvelope | No | Yes | Optional | choose project or resume |  
| platform_core/controllers/session_controller.py | SessionController | resume_session | resume_session(session_id: str, actor: dict) | session id, actor | StandardResponseEnvelope | Yes when governed resume | Yes | Optional | resume pending workflow |  
| platform_core/controllers/workflow_controller.py | WorkflowController | run_stage | run_stage(run_id: str, stage_name: str, payload: dict) | run id, stage payload | StandardResponseEnvelope | Optional | Yes | Optional | next stage or review |  
| platform_core/controllers/workflow_controller.py | WorkflowController | route_next | route_next(run_id: str, current_stage: str, context: dict) | run state context | StandardResponseEnvelope | No | Yes | Optional | recommended next stage |  
| platform_core/controllers/review_controller.py | ReviewController | open_review | open_review(review_id: str, actor: dict) | review id, actor | StandardResponseEnvelope | No | Yes | Yes | render governed review |  
| platform_core/controllers/review_controller.py | ReviewController | get_review_payload | get_review_payload(review_id: str) | review id | StandardResponseEnvelope | No | Optional | Yes | map payload to workspace |  
| platform_core/controllers/review_controller.py | ReviewController | submit_review_action | submit_review_action(review_id: str, interaction_payload: dict) | InteractionPayload | StandardResponseEnvelope | Yes | Yes | Yes | finalize, preview, rerun, escalate |  
| platform_core/controllers/recovery_controller.py | RecoveryController | open_recovery_options | open_recovery_options(run_id: str, actor: dict) | run id, actor | StandardResponseEnvelope | No | Yes | Optional | retry, rerun, rollback |  
| platform_core/controllers/recovery_controller.py | RecoveryController | apply_recovery_choice | apply_recovery_choice(run_id: str, recovery_payload: dict) | recovery choice payload | StandardResponseEnvelope | Yes | Yes | Optional | resume safe path |  
| platform_core/bridges/agent_bridge.py | AgentBridge | build_agent_context | build_agent_context(runtime_context: dict, resolved_stack: dict, extra_context: dict | None = None) | RuntimeContext, ResolvedStack | BaseResult | No | Optional | No | compact context for agent |  
| platform_core/bridges/agent_bridge.py | AgentBridge | dispatch_tool | dispatch_tool(sdk_name: str, function_name: str, payload: dict, allowlist: list[str]) | tool payload | BaseResult | Depends on called method | Depends on called method | Depends on called method | call safe tool |  
| platform_core/bridges/agent_bridge.py | AgentBridge | normalize_response | normalize_response(raw_result: dict, sdk_name: str, function_name: str) | raw result | BaseResult | No | No | No | standardize next-step hints |  
| platform_core/bridges/jupyter_bridge.py | JupyterBridge | build_workspace | build_workspace(ui_mode: str, review_payload: dict | None = None, context: dict | None = None) | UI mode, optional payload | BaseResult | No | No | Optional | open proper workspace |  
| platform_core/bridges/jupyter_bridge.py | JupyterBridge | submit_interaction | submit_interaction(widget_state: dict, actor: dict, stage_name: str, review_id: str | None = None) | widget state | BaseResult | No direct | Optional | Yes | build InteractionPayload |  
| platform_core/bridges/jupyter_bridge.py | JupyterBridge | refresh_workspace | refresh_workspace(workspace_id: str, response_envelope: dict) | workspace id, response | BaseResult | No | No | Optional | update UI state |  
  
====================================================================  
B. CONFIG SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| config_sdk/service.py | ConfigService | load_config | load_config(source: str | Path | dict, config_type: str, environment: str | None = None) | path/dict source | BaseResult | No | Optional | No | validate config |  
| config_sdk/service.py | ConfigService | validate_config | validate_config(config: dict, schema_name: str) | config payload | ValidationResultBase | No | Optional | Optional if config materially invalid | resolve if valid; fix fields if invalid |  
| config_sdk/service.py | ConfigService | resolve_config | resolve_config(base_config: dict, overlays: list[dict] | None = None) | config + overlays | BaseResult | No | Optional | No | use effective config |  
| config_sdk/service.py | ConfigService | diff_config | diff_config(old_config: dict, new_config: dict) | two config payloads | BaseResult | Optional for material change | Optional | Optional | highlight material differences |  
| config_sdk/service.py | ConfigService | get_config_version | get_config_version(config: dict) | config payload | BaseResult | No | No | No | attach version/hash refs |  
  
====================================================================  
C. REGISTRY SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| registry_sdk/service.py | RegistryService | register_project | register_project(project_payload: dict) | project payload | BaseResult | Optional | Yes | No | bootstrap workflow |  
| registry_sdk/service.py | RegistryService | get_project | get_project(project_id: str) | project id | BaseResult | No | No | No | load project context |  
| registry_sdk/service.py | RegistryService | register_run | register_run(run_payload: dict) | run payload | BaseResult | Optional | Yes | No | create workflow state |  
| registry_sdk/service.py | RegistryService | get_run | get_run(run_id: str) | run id | BaseResult | No | No | No | retrieve workflow state |  
| registry_sdk/service.py | RegistryService | search_registry | search_registry(entity_type: str, filters: dict) | search filters | BaseResult | No | No | No | choose record/ref |  
| registry_sdk/service.py | RegistryService | register_skill_metadata | register_skill_metadata(skill_payload: dict) | skill metadata | BaseResult | Optional | Optional | No | runtime resolution |  
| registry_sdk/service.py | RegistryService | register_sdk_metadata | register_sdk_metadata(sdk_payload: dict) | sdk metadata | BaseResult | Optional | Optional | No | tool catalog expansion |  
  
====================================================================  
D. OBSERVABILITY SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| observabilitysdk/service.py | ObservabilityService | create_trace | create_trace(context: dict) | trace context | BaseResult | No | Yes | No | use trace_id in later calls |  
| observabilitysdk/service.py | ObservabilityService | write_event | write_event(event_type: str, payload: dict, trace_id: str | None = None) | event payload | BaseResult | No | Yes | No | maintain lineage |  
| observabilitysdk/service.py | ObservabilityService | query_events | query_events(filters: dict) | event filters | BaseResult | No | No | No | build flow, replay state |  
| observabilitysdk/service.py | ObservabilityService | replay_run | replay_run(run_id: str) | run id | BaseResult | No | No | Optional for recovery | choose recovery path |  
| observabilitysdk/service.py | ObservabilityService | build_event_lineage | build_event_lineage(run_id: str) | run id | BaseResult | No | No | No | visualize flow |  
  
====================================================================  
E. ARTIFACT SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| artifactsdk/service.py | ArtifactService | register_artifact | register_artifact(artifact_payload: dict) | artifact metadata + path | BaseResult | Optional for material artifacts | Yes | Optional | attach artifact refs downstream |  
| artifactsdk/service.py | ArtifactService | get_artifact | get_artifact(artifact_id: str) | artifact id | BaseResult | No | No | No | consume artifact |  
| artifactsdk/service.py | ArtifactService | locate_artifact | locate_artifact(artifact_id: str) | artifact id | BaseResult | No | No | No | load/read artifact |  
| artifactsdk/service.py | ArtifactService | build_artifact_manifest | build_artifact_manifest(artifact_ids: list[str], manifest_type: str) | artifact ids | BaseResult | Optional | Yes | No | reporting / reproducibility |  
| artifactsdk/service.py | ArtifactService | validate_artifact | validate_artifact(artifact_id: str) | artifact id | ValidationResultBase | No | Optional | Optional if invalid and governed | fix artifact before continue |  
| artifactsdk/service.py | ArtifactService | link_artifact_lineage | link_artifact_lineage(parent_artifact_ids: list[str], child_artifact_id: str, lineage_type: str) | lineage refs | BaseResult | Optional | Yes | No | preserve traceability |  
  
====================================================================  
F. AUDIT SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| auditsdk/service.py | AuditService | write_audit_record | write_audit_record(audit_type: str, payload: dict) | audit payload | BaseResult | Yes | Optional | No | preserve audit ref |  
| auditsdk/service.py | AuditService | register_decision | register_decision(decision_payload: dict) | decision payload | BaseResult | Yes | Yes | Optional | link decision to workflow |  
| auditsdk/service.py | AuditService | register_approval | register_approval(approval_payload: dict) | approval payload | BaseResult | Yes | Yes | Yes | finalize governed step |  
| auditsdk/service.py | AuditService | register_exception | register_exception(exception_payload: dict) | exception payload | BaseResult | Yes | Yes | Optional | escalate or track waiver |  
| auditsdk/service.py | AuditService | register_signoff | register_signoff(signoff_payload: dict) | signoff payload | BaseResult | Yes | Yes | Yes | deployment readiness / closure |  
| auditsdk/service.py | AuditService | export_audit_bundle | export_audit_bundle(filters: dict) | export filters | BaseResult | Yes | Optional | No | reporting / committee pack |  
  
====================================================================  
G. WORKFLOW SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| workflowsdk/service.py | WorkflowService | bootstrap_project_workflow | bootstrap_project_workflow(project_id: str, workflow_type: str, initial_context: dict) | project/workflow context | BaseResult | Optional | Yes | No | set initial stage |  
| workflowsdk/service.py | WorkflowService | get_workflow_state | get_workflow_state(run_id: str) | run id | BaseResult | No | No | No | inspect state |  
| workflowsdk/service.py | WorkflowService | update_workflow_state | update_workflow_state(run_id: str, state_patch: dict) | state patch | BaseResult | Optional if material | Yes | Optional | continue or block |  
| workflowsdk/service.py | WorkflowService | route_next_stage | route_next_stage(run_id: str, current_stage: str, context: dict) | state + context | BaseResult | No | Yes | Optional | open review or continue |  
| workflowsdk/service.py | WorkflowService | create_candidate_version | create_candidate_version(run_id: str, candidate_payload: dict) | candidate payload | BaseResult | Optional | Yes | Optional if selection later | compare candidates |  
| workflowsdk/service.py | WorkflowService | select_candidate_version | select_candidate_version(run_id: str, candidate_version_id: str, rationale: str) | selected candidate + rationale | BaseResult | Yes | Yes | Yes normally | unlock downstream stage |  
| workflowsdk/service.py | WorkflowService | create_checkpoint | create_checkpoint(run_id: str, checkpoint_payload: dict) | checkpoint payload | BaseResult | Optional | Yes | No | enable recovery |  
| workflowsdk/service.py | WorkflowService | resolve_recovery_path | resolve_recovery_path(run_id: str, failure_context: dict) | run id + failure context | BaseResult | Optional | Yes | Optional | retry/rerun/rollback |  
  
====================================================================  
H. POLICY SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| policysdk/service.py | PolicyService | load_policy_pack | load_policy_pack(policy_mode: str, domain: str | None = None, stage: str | None = None) | policy selection context | BaseResult | No | Optional | No | evaluate controls |  
| policysdk/service.py | PolicyService | evaluate_metric_set | evaluate_metric_set(metric_results: list[dict], policy_pack: dict) | metrics + policy pack | BaseResult | Optional for material breaches | Optional | Optional | classify pass/warn/breach |  
| policysdk/service.py | PolicyService | detect_breaches | detect_breaches(evaluation_results: list[dict], context: dict | None = None) | evaluated metrics | BaseResult | Optional | Yes if breach | Optional | open review/escalate |  
| policysdk/service.py | PolicyService | get_stage_controls | get_stage_controls(stage_name: str, policy_pack: dict) | stage + policy pack | BaseResult | No | No | No | determine HITL need |  
| policysdk/service.py | PolicyService | requires_human_review | requires_human_review(stage_name: str, context: dict, policy_pack: dict) | stage context | BaseResult | No | No | Yes if true | create review |  
| policysdk/service.py | PolicyService | get_approval_requirements | get_approval_requirements(stage_name: str, context: dict, policy_pack: dict) | stage context | BaseResult | No | No | Yes | assign approver |  
| policysdk/service.py | PolicyService | can_actor_approve | can_actor_approve(actor: dict, stage_name: str, policy_pack: dict) | actor + stage | ValidationResultBase | No | No | Yes | allow/block approval |  
| policysdk/service.py | PolicyService | should_escalate | should_escalate(context: dict, policy_pack: dict) | issue/review context | BaseResult | Optional | Optional | Yes if true | escalate review |  
| policysdk/service.py | PolicyService | is_waivable | is_waivable(issue_context: dict, policy_pack: dict) | issue context | BaseResult | Optional | Optional | Optional | waiver path or block |  
  
====================================================================  
I. HITL SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| hitlsdk/service.py | HITLService | create_review | create_review(review_type: str, review_payload: dict, actor_context: dict) | review payload + actor | BaseResult | Optional at creation | Yes | Yes | open workspace |  
| hitlsdk/service.py | HITLService | get_review | get_review(review_id: str) | review id | BaseResult | No | No | Yes | inspect review state |  
| hitlsdk/service.py | HITLService | build_review_payload | build_review_payload(review_type: str, source_context: dict) | source artifacts/context | BaseResult | No | Optional | Yes | render review shell |  
| hitlsdk/service.py | HITLService | validate_action | validate_action(review_id: str, interaction_payload: dict) | review id + InteractionPayload | ValidationResultBase | No | Optional | Yes | preview/finalize or reject |  
| hitlsdk/service.py | HITLService | transition_review_state | transition_review_state(review_id: str, target_status: str, context: dict | None = None) | review state change | BaseResult | Optional | Yes | Yes | continue review lifecycle |  
| hitlsdk/service.py | HITLService | approve_review | approve_review(review_id: str, actor: dict, comment: str | None = None) | approval payload | BaseResult | Yes | Yes | Yes | finalize governed step |  
| hitlsdk/service.py | HITLService | approve_with_conditions | approve_with_conditions(review_id: str, actor: dict, conditions: list[str], comment: str | None = None) | approval w/ conditions | BaseResult | Yes | Yes | Yes | record conditions and continue |  
| hitlsdk/service.py | HITLService | escalate_review | escalate_review(review_id: str, reason: str, target_role: str | None = None) | escalation payload | BaseResult | Yes | Yes | Yes | assign higher review path |  
| hitlsdk/service.py | HITLService | capture_decision | capture_decision(review_id: str, action: str, interaction_payload: dict) | final action payload | BaseResult | Yes | Yes | Yes | patch workflow state |  
  
====================================================================  
J. DATASET SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| dataset_sdk/service.py | DatasetService | register_dataset | register_dataset(dataset_payload: dict) | dataset metadata | BaseResult | Optional | Yes | No | create snapshot |  
| dataset_sdk/service.py | DatasetService | create_snapshot | create_snapshot(dataset_id: str, snapshot_payload: dict) | dataset + snapshot metadata | BaseResult | Optional | Yes | No | register split / lineage |  
| dataset_sdk/service.py | DatasetService | register_split | register_split(dataset_snapshot_id: str, split_payload: dict) | split metadata | BaseResult | No | Yes | Optional if split policy violated | validate readiness |  
| dataset_sdk/service.py | DatasetService | create_sample_reference | create_sample_reference(dataset_snapshot_id: str, sample_payload: dict) | sample logic | BaseResult | No | Optional | No | preserve sample lineage |  
| dataset_sdk/service.py | DatasetService | create_lineage_reference | create_lineage_reference(dataset_snapshot_id: str, lineage_payload: dict) | lineage payload | BaseResult | No | Yes | No | preserve source traceability |  
| dataset_sdk/service.py | DatasetService | validate_dataset_contract | validate_dataset_contract(dataset_schema: dict, contract: dict) | schema + contract | ValidationResultBase | Optional if governed failure | Optional | Optional | fix contract or continue |  
| dataset_sdk/service.py | DatasetService | get_dataset_snapshot | get_dataset_snapshot(dataset_snapshot_id: str) | snapshot id | BaseResult | No | No | No | consume snapshot |  
  
====================================================================  
K. DQ SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| dq_sdk/service.py | DQService | run_schema_checks | run_schema_checks(data_ref: dict, expected_schema: dict) | dataset/artifact ref + schema | ValidationResultBase | Optional if material issue | Optional | Optional | fix schema or continue |  
| dq_sdk/service.py | DQService | run_missingness_checks | run_missingness_checks(data_ref: dict, rules: dict | None = None) | data ref | BaseResult | Optional if severe | Optional | Optional | profile data gaps |  
| dq_sdk/service.py | DQService | run_consistency_checks | run_consistency_checks(data_ref: dict, rules: dict) | data ref + rules | BaseResult | Optional if severe | Optional | Optional | fix grain/date inconsistencies |  
| dq_sdk/service.py | DQService | build_distribution_profile | build_distribution_profile(data_ref: dict, columns: list[str] | None = None) | data ref | BaseResult | No | Optional | No | use in DQ/monitoring |  
| dq_sdk/service.py | DQService | run_business_rule_checks | run_business_rule_checks(data_ref: dict, rule_set: dict) | data ref + business rules | BaseResult | Optional | Optional | Optional | escalate if rule breach |  
| dq_sdk/service.py | DQService | build_dq_summary | build_dq_summary(check_results: list[dict]) | check result list | BaseResult | No | Yes | Optional | open data readiness review |  
| dq_sdk/service.py | DQService | create_dq_exception | create_dq_exception(dq_summary: dict, severity: str) | dq summary | BaseResult | Yes | Yes | Yes if governed | remediation / rerun path |  
  
====================================================================  
L. FEATURE SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| feature_sdk/service.py | FeatureService | apply_transformations | apply_transformations(data_ref: dict, feature_rules: dict) | data ref + rules | BaseResult | Optional | Yes | No | register metadata |  
| feature_sdk/service.py | FeatureService | build_lags | build_lags(data_ref: dict, lag_spec: dict) | data ref + lag spec | BaseResult | Optional | Yes | No | continue feature set build |  
| feature_sdk/service.py | FeatureService | build_differences | build_differences(data_ref: dict, diff_spec: dict) | data ref + diff spec | BaseResult | Optional | Yes | No | continue feature build |  
| feature_sdk/service.py | FeatureService | build_grouped_features | build_grouped_features(data_ref: dict, grouping_spec: dict) | data ref + group spec | BaseResult | Optional | Yes | No | continue feature build |  
| feature_sdk/service.py | FeatureService | encode_categorical | encode_categorical(data_ref: dict, encoding_spec: dict) | data ref + encoding spec | BaseResult | Optional | Yes | No | register metadata/lineage |  
| feature_sdk/service.py | FeatureService | register_feature_metadata | register_feature_metadata(feature_metadata_payload: dict) | metadata payload | BaseResult | Optional | Yes | No | preserve catalog |  
| feature_sdk/service.py | FeatureService | register_feature_lineage | register_feature_lineage(feature_name: str, lineage_payload: dict) | lineage payload | BaseResult | Optional | Yes | No | preserve auditability |  
  
====================================================================  
M. EVALUATION SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| evaluation_sdk/service.py | EvaluationService | compute_metrics | compute_metrics(model_type: str, inputs: dict, metric_set: list[str] | None = None) | model inputs + metric set | BaseResult | Optional for material selection | Yes | Optional | compare candidates |  
| evaluation_sdk/service.py | EvaluationService | run_diagnostics | run_diagnostics(model_type: str, inputs: dict, diagnostic_set: list[str] | None = None) | model inputs | BaseResult | Optional | Yes | Optional | review diagnostics |  
| evaluation_sdk/service.py | EvaluationService | run_stability_checks | run_stability_checks(current_ref: dict, baseline_ref: dict, config: dict) | current + baseline refs | BaseResult | Optional if breach | Yes | Optional | monitoring / validation |  
| evaluation_sdk/service.py | EvaluationService | run_calibration_checks | run_calibration_checks(actual_ref: dict, predicted_ref: dict, config: dict | None = None) | actual/predicted refs | BaseResult | Optional | Yes | Optional | validation/monitoring |  
| evaluation_sdk/service.py | EvaluationService | compare_candidates | compare_candidates(candidate_refs: list[dict], comparison_spec: dict) | candidate refs | BaseResult | Optional if selection stage | Yes | Yes often | select candidate |  
| evaluation_sdk/service.py | EvaluationService | evaluate_thresholds | evaluate_thresholds(metric_results: list[dict], threshold_pack: dict) | metrics + thresholds | BaseResult | Optional on breach | Optional | Optional | pass/warn/breach gating |  
| evaluation_sdk/service.py | EvaluationService | compare_to_benchmark | compare_to_benchmark(current_summary: dict, benchmark_ref: dict) | summary + benchmark ref | BaseResult | Optional | Optional | Optional | assess deviation |  
  
====================================================================  
N. DATAPREP SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| dataprepsdk/service.py | DataPrepService | validate_dataprep_config | validate_dataprep_config(config: dict) | dataprep config | ValidationResultBase | Optional if material invalidity | Optional | Optional | fix config or execute |  
| dataprepsdk/service.py | DataPrepService | validate_template_request | validate_template_request(template_id: str, domain: str, data_structure_type: str) | template request | ValidationResultBase | No | Optional | No | select supported template |  
| dataprepsdk/service.py | DataPrepService | execute_request | execute_request(request: dict) | DataPrepRequest | BaseResult | Optional | Yes | Optional | dataset registration / DQ |  
| dataprepsdk/service.py | DataPrepService | build_cross_sectional_dataset | build_cross_sectional_dataset(request: dict) | DataPrepRequest | BaseResult | Optional | Yes | Optional | register snapshot |  
| dataprepsdk/service.py | DataPrepService | build_panel_dataset | build_panel_dataset(request: dict) | DataPrepRequest | BaseResult | Optional | Yes | Optional | register snapshot |  
| dataprepsdk/service.py | DataPrepService | build_time_series_dataset | build_time_series_dataset(request: dict) | DataPrepRequest | BaseResult | Optional | Yes | Optional | register snapshot |  
| dataprepsdk/service.py | DataPrepService | build_cohort_dataset | build_cohort_dataset(request: dict) | DataPrepRequest | BaseResult | Optional | Yes | Optional | register snapshot |  
| dataprepsdk/service.py | DataPrepService | build_event_history_dataset | build_event_history_dataset(request: dict) | DataPrepRequest | BaseResult | Optional | Yes | Optional | register snapshot |  
| dataprepsdk/service.py | DataPrepService | reproduce_dataset | reproduce_dataset(dataset_snapshot_id: str, overrides: dict | None = None) | existing snapshot id | BaseResult | Optional | Yes | Optional | compare reproduced output |  
| dataprepsdk/spark_service.py | SparkDataPrepService | build_cross_sectional_dataset_spark | build_cross_sectional_dataset_spark(request: dict, spark_session: object | None = None) | DataPrepRequest | BaseResult | Optional | Yes | Optional | dataset + snapshot registration |  
| dataprepsdk/spark_service.py | SparkDataPrepService | build_panel_dataset_spark | build_panel_dataset_spark(request: dict, spark_session: object | None = None) | DataPrepRequest | BaseResult | Optional | Yes | Optional | dataset + snapshot registration |  
| dataprepsdk/spark_service.py | SparkDataPrepService | build_time_series_dataset_spark | build_time_series_dataset_spark(request: dict, spark_session: object | None = None) | DataPrepRequest | BaseResult | Optional | Yes | Optional | dataset + snapshot registration |  
| dataprepsdk/spark_service.py | SparkDataPrepService | build_cohort_dataset_spark | build_cohort_dataset_spark(request: dict, spark_session: object | None = None) | DataPrepRequest | BaseResult | Optional | Yes | Optional | dataset + snapshot registration |  
| dataprepsdk/spark_service.py | SparkDataPrepService | build_event_history_dataset_spark | build_event_history_dataset_spark(request: dict, spark_session: object | None = None) | DataPrepRequest | BaseResult | Optional | Yes | Optional | dataset + snapshot registration |  
| dataprepsdk/spark_service.py | SparkDataPrepService | run_prep_quality_checks_spark | run_prep_quality_checks_spark(dataset_ref: dict, check_pack: dict | None = None) | dataset ref | BaseResult | Optional if severe issues | Yes | Optional / data readiness | open readiness review or rerun |  
  
====================================================================  
O. SCORECARD SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| scorecardsdk/service.py | ScorecardService | build_fine_bins | build_fine_bins(dataset_ref: dict, variable_spec: dict, config: dict | None = None) | dataset ref + vars | BaseResult | Optional | Yes | Optional | coarse classing next |  
| scorecardsdk/service.py | ScorecardService | build_coarse_bin_candidate | build_coarse_bin_candidate(fine_bin_ref: dict, merge_rules: dict | None = None) | fine bin refs | BaseResult | Optional | Yes | Yes often | open coarse review |  
| scorecardsdk/service.py | ScorecardService | preview_edited_bins | preview_edited_bins(fine_bin_ref: dict, edited_bin_groups: dict) | edit payload | BaseResult | No direct | Yes | Yes | finalize or rerun |  
| scorecardsdk/service.py | ScorecardService | finalize_coarse_bins | finalize_coarse_bins(candidate_ref: dict, final_bin_groups: dict, rationale: str | None = None) | selected candidate + final bins | BaseResult | Yes | Yes | Yes | compute WOE/IV |  
| scorecardsdk/service.py | ScorecardService | compare_binning_candidates | compare_binning_candidates(candidate_refs: list[dict], comparison_spec: dict | None = None) | candidate refs | BaseResult | Optional | Yes | Yes | select final binning version |  
| scorecardsdk/service.py | ScorecardService | compute_woe_iv | compute_woe_iv(coarse_bin_ref: dict, target_ref: dict | None = None) | coarse bins + target | BaseResult | Optional | Yes | Optional | shortlist features |  
| scorecardsdk/service.py | ScorecardService | build_feature_shortlist | build_feature_shortlist(woe_iv_ref: dict, shortlist_rules: dict) | WOE/IV refs | BaseResult | Optional | Yes | Yes often | review shortlist |  
| scorecardsdk/service.py | ScorecardService | fit_candidate_set | fit_candidate_set(dataset_ref: dict, feature_set_ref: dict, model_spec: dict) | dataset + features + model spec | BaseResult | Optional | Yes | Yes often | compare candidates |  
| scorecardsdk/service.py | ScorecardService | scale_scorecard | scale_scorecard(model_candidate_ref: dict, scaling_spec: dict) | model candidate | BaseResult | Optional | Yes | Yes if governed | build bands / finalize |  
| scorecardsdk/service.py | ScorecardService | build_score_bands | build_score_bands(score_output_ref: dict, band_spec: dict) | scored output + band spec | BaseResult | Optional | Yes | Optional | bundle outputs |  
| scorecardsdk/service.py | ScorecardService | build_scorecard_output_bundle | build_scorecard_output_bundle(context: dict) | selected refs | BaseResult | Yes | Yes | Optional | validation next |  
  
====================================================================  
P. VALIDATION SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| validationsdk/service.py | ValidationService | create_validation_scope | create_validation_scope(project_id: str, model_ref: dict, scope_config: dict) | project/model/scope config | BaseResult | Optional | Yes | Yes often | intake evidence |  
| validationsdk/service.py | ValidationService | intake_evidence | intake_evidence(validation_run_id: str, evidence_refs: list[dict]) | evidence refs | BaseResult | Optional | Yes | Optional | assess completeness |  
| validationsdk/service.py | ValidationService | assess_evidence_completeness | assess_evidence_completeness(validation_run_id: str, required_evidence_pack: dict) | validation run + evidence requirements | BaseResult | Optional | Yes | Yes if incomplete materially | request more evidence |  
| validationsdk/service.py | ValidationService | evaluate_fitness_dimensions | evaluate_fitness_dimensions(validation_run_id: str, evidence_summary: dict, metric_summary: dict | None = None) | validation run context | BaseResult | Optional | Yes | Yes often | build conclusions |  
| validationsdk/service.py | ValidationService | create_finding | create_finding(validation_run_id: str, finding_payload: dict) | finding payload | BaseResult | Yes | Yes | Yes if severity high | assess severity/remediation |  
| validationsdk/service.py | ValidationService | assess_severity | assess_severity(finding_payload: dict, policy_pack: dict | None = None) | finding payload | BaseResult | Optional | Optional | Yes if severe | escalate / note |  
| validationsdk/service.py | ValidationService | build_conclusion_options | build_conclusion_options(validation_run_id: str, fitness_summary: dict, findings: list[dict]) | fitness + findings | BaseResult | Optional | Yes | Yes | finalize conclusion |  
| validationsdk/service.py | ValidationService | finalize_conclusion | finalize_conclusion(validation_run_id: str, conclusion_payload: dict, actor: dict) | conclusion payload + validator actor | BaseResult | Yes | Yes | Yes always | deployment readiness or remediation |  
| validationsdk/service.py | ValidationService | create_remediation_action | create_remediation_action(finding_id: str, remediation_payload: dict) | finding + action | BaseResult | Yes | Yes | Yes if assignment | track remediation |  
| validationsdk/service.py | ValidationService | build_validation_output_bundle | build_validation_output_bundle(validation_run_id: str) | validation run id | BaseResult | Yes | Yes | Optional | reporting pack |  
  
====================================================================  
Q. REPORTING SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| reporting_sdk/service.py | ReportingService | build_technical_report | build_technical_report(report_context: dict, section_spec: dict | None = None) | report context | BaseResult | Optional | Yes | Optional | validation/committee review |  
| reporting_sdk/service.py | ReportingService | build_executive_summary | build_executive_summary(summary_context: dict) | summary context | BaseResult | Optional | Yes | Optional | committee pack |  
| reporting_sdk/service.py | ReportingService | build_committee_pack | build_committee_pack(pack_context: dict) | committee pack context | BaseResult | Optional | Yes | Yes before governance use | submit for review |  
| reporting_sdk/service.py | ReportingService | build_validation_note | build_validation_note(validation_context: dict) | validation context | BaseResult | Optional | Yes | Optional | attach to validation outputs |  
| reporting_sdk/service.py | ReportingService | get_narrative_block | get_narrative_block(block_id: str, audience: str | None = None) | block id | BaseResult | No | No | No | render approved narrative |  
| reporting_sdk/service.py | ReportingService | export_chart_refs | export_chart_refs(artifact_ids: list[str]) | chart artifact ids | BaseResult | No | Optional | No | pack assembly |  
| reporting_sdk/service.py | ReportingService | export_table_refs | export_table_refs(artifact_ids: list[str]) | table artifact ids | BaseResult | No | Optional | No | pack assembly |  
| reporting_sdk/service.py | ReportingService | assemble_pack | assemble_pack(section_refs: list[dict], pack_type: str) | section refs | BaseResult | Optional | Yes | Optional | final package ready |  
  
====================================================================  
R. KNOWLEDGE SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| knowledge_sdk/service.py | KnowledgeService | create_knowledge_object | create_knowledge_object(knowledge_payload: dict) | knowledge payload | BaseResult | Optional | Yes | Optional for promotion | register knowledge |  
| knowledge_sdk/service.py | KnowledgeService | register_knowledge | register_knowledge(knowledge_object: dict) | knowledge object | BaseResult | Optional | Yes | No | searchable memory |  
| knowledge_sdk/service.py | KnowledgeService | search_knowledge | search_knowledge(filters: dict) | filters | BaseResult | No | No | No | retrieval candidate selection |  
| knowledge_sdk/service.py | KnowledgeService | capture_from_event | capture_from_event(event_ref: dict, capture_config: dict | None = None) | event ref | BaseResult | Optional | Yes | Optional | persist project knowledge |  
| knowledge_sdk/service.py | KnowledgeService | capture_from_decision | capture_from_decision(decision_ref: dict, summary_payload: dict | None = None) | decision ref | BaseResult | Yes optional | Yes | Optional | reusable decision knowledge |  
| knowledge_sdk/service.py | KnowledgeService | set_quality_status | set_quality_status(knowledge_id: str, quality_status: str, review_note: str | None = None) | knowledge id + quality status | BaseResult | Yes if promotion-related | Yes | Yes if governed | promote or keep project-only |  
| knowledge_sdk/service.py | KnowledgeService | promote_knowledge | promote_knowledge(knowledge_id: str, target_scope: str, actor: dict | None = None) | promotion request | BaseResult | Yes | Yes | Yes often | reusable domain/global memory |  
| knowledge_sdk/service.py | KnowledgeService | export_knowledge_bundle | export_knowledge_bundle(filters: dict) | export filters | BaseResult | Optional | Optional | No | reusable bundle |  
  
====================================================================  
S. RAG SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| rag_sdk/service.py | RetrievalService | chunk_document | chunk_document(document_ref: dict, chunk_spec: dict | None = None) | document ref | BaseResult | No | Optional | No | embed or index |  
| rag_sdk/service.py | RetrievalService | embed_chunks | embed_chunks(chunk_refs: list[dict], embedding_profile: dict | None = None) | chunk refs | BaseResult | No | Optional | No | retrieve later |  
| rag_sdk/service.py | RetrievalService | route_query | route_query(query: str, runtime_context: dict, retrieval_mode: str | None = None) | query + runtime context | BaseResult | No | Optional | No | choose retrieval plan |  
| rag_sdk/service.py | RetrievalService | retrieve | retrieve(query: str, filters: dict, budget_profile: dict | None = None) | query + filters | BaseResult | No | Optional | No | rerank/compress |  
| rag_sdk/service.py | RetrievalService | rerank_results | rerank_results(retrieval_results: list[dict], rerank_spec: dict | None = None) | retrieval result list | BaseResult | No | No | No | compress context |  
| rag_sdk/service.py | RetrievalService | compress_context | compress_context(retrieval_results: list[dict], compression_mode: str = "compact") | retrieval results | BaseResult | No | No | No | build context pack |  
| rag_sdk/service.py | RetrievalService | build_context_pack | build_context_pack(query: str, runtime_context: dict, filters: dict | None = None) | query + context | BaseResult | No | Optional | No | agent-ready prompt pack |  
| rag_sdk/service.py | RetrievalService | get_budget_profile | get_budget_profile(token_mode: str) | token mode | BaseResult | No | No | No | enforce context limits |  
  
====================================================================  
T. FLOWVIZ SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| flowvizsdk/service.py | FlowService | build_nodes | build_nodes(run_id: str, filters: dict | None = None) | run id | BaseResult | No | No | No | build edges |  
| flowvizsdk/service.py | FlowService | build_edges | build_edges(run_id: str, filters: dict | None = None) | run id | BaseResult | No | No | No | export graph |  
| flowvizsdk/service.py | FlowService | summarize_flow | summarize_flow(run_id: str, summary_mode: str = "compact") | run id | BaseResult | No | No | No | reporting / governance summary |  
| flowvizsdk/service.py | FlowService | build_timeline | build_timeline(run_id: str, filters: dict | None = None) | run id | BaseResult | No | No | No | visualize chronology |  
| flowvizsdk/service.py | FlowService | export_graph | export_graph(run_id: str, export_mode: str = "ui") | run id | BaseResult | No | No | No | UI or report rendering |  
| flowvizsdk/service.py | FlowService | filter_graph | filter_graph(graph_ref: dict, filter_spec: dict) | graph ref + filters | BaseResult | No | No | No | focused flow view |  
| flowvizsdk/service.py | FlowService | get_drilldown_payload | get_drilldown_payload(node_id: str, graph_ref: dict) | node id + graph ref | BaseResult | No | No | No | detail panel data |  
  
====================================================================  
U. MONITORING SDK  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| monitoringsdk/service.py | MonitoringService | get_monitoring_template | get_monitoring_template(model_family: str, template_id: str | None = None) | model family/template selection | BaseResult | No | No | No | validate snapshot |  
| monitoringsdk/service.py | MonitoringService | ingest_snapshot | ingest_snapshot(snapshot_payload: dict, template_ref: dict) | snapshot payload | BaseResult | Optional | Yes | Optional | validate snapshot |  
| monitoringsdk/service.py | MonitoringService | validate_snapshot | validate_snapshot(snapshot_ref: dict, template_ref: dict) | snapshot ref | ValidationResultBase | Optional if severe issues | Optional | Optional | append or fix |  
| monitoringsdk/service.py | MonitoringService | append_snapshot | append_snapshot(model_id: str, snapshot_ref: dict) | model + snapshot ref | BaseResult | Optional | Yes | No | refresh metrics |  
| monitoringsdk/service.py | MonitoringService | compute_monitoring_metrics | compute_monitoring_metrics(model_id: str, snapshot_ref: dict, metric_spec: dict | None = None) | monitoring snapshot | BaseResult | Optional | Yes | Optional | threshold evaluation |  
| monitoringsdk/service.py | MonitoringService | evaluate_monitoring_thresholds | evaluate_monitoring_thresholds(metric_summary: dict, threshold_pack: dict) | metric summary | BaseResult | Optional if breach | Yes | Yes if breach | open breach review |  
| monitoringsdk/service.py | MonitoringService | compute_drift | compute_drift(current_snapshot_ref: dict, baseline_snapshot_ref: dict, drift_spec: dict | None = None) | current + baseline refs | BaseResult | Optional if material | Yes | Optional | include in dashboard/review |  
| monitoringsdk/service.py | MonitoringService | compute_segment_monitoring | compute_segment_monitoring(snapshot_ref: dict, segment_spec: dict) | snapshot + segment spec | BaseResult | Optional | Yes | Optional | segment drilldown |  
| monitoringsdk/service.py | MonitoringService | build_dashboard_payload | build_dashboard_payload(model_id: str, snapshot_ref: dict, dashboard_mode: str = "standard") | snapshot context | BaseResult | No | Yes | Optional | refresh dashboard UI |  
| monitoringsdk/service.py | MonitoringService | build_dashboard_config | build_dashboard_config(template_ref: dict, dashboard_mode: str = "standard") | template ref | BaseResult | No | No | No | render dashboard |  
| monitoringsdk/service.py | MonitoringService | create_monitoring_note | create_monitoring_note(model_id: str, snapshot_ref: dict, note_payload: dict) | note/action payload | BaseResult | Yes if action/decision | Yes | Yes if action assignment | remediation tracking |  
| monitoringsdk/service.py | MonitoringService | build_annual_review_pack | build_annual_review_pack(model_id: str, period_spec: dict) | model + review period | BaseResult | Optional | Yes | Yes often | annual review / governance pack |  
| monitoringsdk/service.py | MonitoringService | write_monitoring_outputs | write_monitoring_outputs(model_id: str, output_bundle: dict) | output bundle | BaseResult | Optional | Yes | Optional | artifact refs/reporting |  
  
====================================================================  
V. OPTIONAL FUTURE DOMAIN SDK FUNCTIONS  
====================================================================  
  
| File | Class | Function | Signature | Input Contract | Output Contract | Audit Hook | Event Hook | Review Hook | Next-Step Hint |  
|---|---|---|---|---|---|---|---|---|---|  
| timeseriessdk/service.py | TimeSeriesService | fit_time_series_candidates | fit_time_series_candidates(dataset_ref: dict, model_spec: dict) | dataset + model spec | BaseResult | Optional | Yes | Yes often | compare forecasts |  
| lgdsdk/service.py | LGDService | fit_cure_model | fit_cure_model(dataset_ref: dict, model_spec: dict) | dataset + model spec | BaseResult | Optional | Yes | Yes often | fit severity model |  
| pdsdk/service.py | PDService | calibrate_pd | calibrate_pd(pd_ref: dict, calibration_spec: dict) | PD refs + config | BaseResult | Optional | Yes | Yes often | validation/review |  
| eadsdk/service.py | EADService | estimate_exposure | estimate_exposure(context: dict) | EAD context | BaseResult | Optional | Yes | Yes often | validation/review |  
| sicr_sdk/service.py | SICRService | compare_sicr_methods | compare_sicr_methods(candidate_refs: list[dict]) | candidate refs | BaseResult | Optional | Yes | Yes | select method |  
| eclsdk/service.py | ECLService | run_scenario_engine | run_scenario_engine(context: dict) | ECL context | BaseResult | Optional | Yes | Yes often | overlay/review |  
| stresssdk/service.py | StressService | generate_stressed_projection | generate_stressed_projection(context: dict) | stress context | BaseResult | Optional | Yes | Yes often | aggregate results |  
  
====================================================================  
W. FINAL IMPLEMENTATION NOTES  
====================================================================  
  
1. Use this table to decide:  
   - public façade methods only  
   - what to wrap as agent-callable tools  
   - what should remain internal helper logic  
  
2. Strong candidates for direct agent tools:  
   - WorkflowService public methods  
   - HITLService public methods  
   - DataPrepService public methods  
   - EvaluationService public methods  
   - ScorecardService public methods  
   - ValidationService public methods  
   - MonitoringService public methods  
   - ReportingService public methods  
   - RetrievalService public methods  
  
3. Usually do NOT expose internal helpers directly as agent tools:  
   - NodeBuilder  
   - EdgeBuilder  
   - ConfigLoaderUtility  
   - TransformationEngine  
   - MetricEngine  
   - TemplateRegistryService  
   - SparkUtils  
   - PackAssembler internals  
  
4. Controllers should be the preferred boundary for:  
   - UI  
   - API  
   - chat/agent workflows  
   where multi-step orchestration is needed.  
  
====================================================================  
X. NEXT BEST ARTIFACT  
====================================================================  
  
The next most useful deliverable is a:  
  
TOOL REGISTRY TABLE  
with columns:  
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
  
That would be the most direct design for integrating this into your  
agentic platform.  
  
====================================================================  
END OF FUNCTION CATALOG TABLE  
====================================================================  
