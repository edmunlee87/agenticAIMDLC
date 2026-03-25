# File by file   
  
====================================================================  
FILE-BY-FILE CLASS MAPPING TABLE  
AGENTIC AI MDLC FRAMEWORK  
CODING-READY REFERENCE  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This reference maps the expected files to:  
- primary class  
- parent class  
- key imports  
- key methods  
- who instantiates it  
- dependencies  
- what it returns or produces  
  
This is designed to be implementation-ready for a monorepo with  
multiple internal SDK packages.  
  
LEGEND  
--------------------------------------------------------------------  
Columns:  
- File  
- Class  
- Parent  
- Key Imports  
- Key Methods  
- Instantiated By  
- Depends On  
- Returns / Produces  
  
Notes:  
- "Key Imports" shows the important imports, not every trivial import.  
- "Instantiated By" shows the usual owner or caller.  
- "Returns / Produces" focuses on public behavior.  
  
====================================================================  
A. PLATFORM CORE  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| platform_core/schemas/base_models.py | BaseModelBase | None | pydantic.BaseModel, Field, ConfigDict, datetime | to_dict, to_json, compact_dict, with_updates | imported by all model files | pydantic | Canonical typed model behavior |  
| platform_core/schemas/base_results.py | BaseResult | BaseModelBase | typing, Field | is_success, has_warnings, has_errors, requires_human_review, recommended_next_action, recommended_next_stage | imported by all service files | BaseModelBase | Standard SDK result contract |  
| platform_core/schemas/base_results.py | ValidationResultBase | BaseResult | Field | fail_count, pass_count, validation_summary | validators and services | BaseResult | Standard validation result contract |  
| platform_core/schemas/common_fragments.py | ArtifactRef | BaseModelBase | typing | compact_dict | all SDKs | BaseModelBase | Artifact reference object |  
| platform_core/schemas/common_fragments.py | MetricResult | BaseModelBase | typing | compact_dict | evaluation, monitoring, scorecard | BaseModelBase | Metric record |  
| platform_core/schemas/common_fragments.py | WarningRecord | BaseModelBase | typing | compact_dict | all SDKs | BaseModelBase | Warning record |  
| platform_core/schemas/common_fragments.py | ErrorRecord | BaseModelBase | typing | compact_dict | all SDKs | BaseModelBase | Error record |  
| platform_core/schemas/common_fragments.py | ActorRecord | BaseModelBase | typing | compact_dict | hitl, audit, validation | BaseModelBase | Actor reference |  
| platform_core/schemas/runtime_context.py | RuntimeContext | BaseModelBase | typing, Field | compact_dict, validate_role_stage_alignment | runtime resolver, bridges, controllers | BaseModelBase | Runtime state input |  
| platform_core/schemas/resolved_stack.py | ResolvedStack | BaseModelBase | typing, Field | compact_dict | runtime resolver, bridges | BaseModelBase | Resolved runtime stack |  
| platform_core/schemas/interaction_payload.py | InteractionPayload | BaseModelBase | typing, Field | compact_dict | Jupyter bridge, API bridge | BaseModelBase | Structured human action payload |  
| platform_core/schemas/review_payload.py | ReviewPayload | BaseModelBase | typing, Field | compact_dict | hitlsdk, review_controller | BaseModelBase | Review display payload |  
| platform_core/schemas/response_envelope.py | StandardResponseEnvelope | BaseResult | typing, Field | compact_dict | controllers, bridges | BaseResult | Workflow/controller response envelope |  
| platform_core/exceptions.py | PlatformError | Exception | None | __init__ | raised across platform | None | Root platform exception |  
| platform_core/exceptions.py | ValidationError | PlatformError | None | __init__ | validators | PlatformError | Validation error type |  
| platform_core/utils/result_factory.py | ResultFactory | None | typing | success, warning, blocked, failed, validation_failed | BaseService subclasses | BaseResult, ValidationResultBase | Consistent result creation |  
| platform_core/utils/dependency_container.py | DependencyContainer | None | typing | register, get, has | app bootstrap, service factory | None | Dependency lookup |  
| platform_core/utils/id_utils.py | IDFactory | None | uuid, datetime | make_id, make_timestamped_id | registries, services | None | Stable IDs |  
| platform_core/utils/time_utils.py | TimeProvider | None | datetime | now, today | all services | None | Consistent clock access |  
| platform_core/services/base_service.py | BaseService | None | logging, typing | _build_result, _build_validation_result, _get_dependency, _require_fields, _handle_exception, _log_start, _log_finish | all SDK service classes | ResultFactory, DependencyContainer | Shared service behavior |  
| platform_core/services/base_storage_service.py | BaseStorageService | BaseService | pathlib, json, boto3 optional, s3fs optional | _normalize_path, _exists, _read_json, _write_json, _read_bytes, _write_bytes, _resolve_uri | storage adapters | BaseService | Shared storage abstraction |  
| platform_core/services/base_registry_service.py | BaseRegistryService | BaseService | typing | create_record, get_record, update_record, search_records, _normalize_record, _validate_record_id | registry services | BaseService | Shared registry CRUD/search pattern |  
| platform_core/services/base_review_component.py | BaseReviewComponent | BaseService | typing | _get_review, _validate_actor, _validate_allowed_action, _require_comment_if_needed, _build_review_result | hitl services | BaseService, hitl deps | Shared review logic |  
| platform_core/services/base_spark_service.py | BaseSparkService | BaseService | pyspark.sql.SparkSession, DataFrame, functions as F | _get_spark_session, _validate_dataframe, _safe_count, _project_columns, _safe_join, _write_dataframe, _summarize_dataframe | spark dataprep modules | BaseService, pyspark | Shared Spark logic |  
| platform_core/controllers/base_controller.py | BaseController | None | logging, typing | _get_service, _normalize_response, _emit_event_if_needed, _write_audit_if_needed, _apply_workflow_patch_if_needed, _validate_payload | all controllers | DependencyContainer, BaseResult | Shared controller behavior |  
| platform_core/runtime/base_runtime_component.py | BaseRuntimeComponent | None | logging, typing | resolve, _validate_runtime_context, _build_runtime_decision, _fallback_decision | runtime resolvers | RuntimeContext, ValidationResultBase | Shared runtime resolution pattern |  
| platform_core/runtime/resolver.py | RuntimeResolver | BaseRuntimeComponent | typing | resolve | SessionController, WorkflowController | RuntimeRulesUtility, AllowlistResolver, UIModeResolver, InteractionModeResolver, TokenModeResolver | ResolvedStack |  
| platform_core/runtime/ui_mode_resolver.py | UIModeResolver | BaseRuntimeComponent | typing | resolve | RuntimeResolver | RuntimeContext | ui_mode decision |  
| platform_core/runtime/interaction_mode_resolver.py | InteractionModeResolver | BaseRuntimeComponent | typing | resolve | RuntimeResolver | RuntimeContext | interaction_mode decision |  
| platform_core/runtime/token_mode_resolver.py | TokenModeResolver | BaseRuntimeComponent | typing | resolve | RuntimeResolver | RuntimeContext | token_mode decision |  
| platform_core/runtime/allowlist_resolver.py | AllowlistResolver | BaseRuntimeComponent | typing | resolve | RuntimeResolver, AgentBridge | RuntimeContext, policy/config maps | sdk_allowlist |  
| platform_core/runtime/runtime_rules_utility.py | RuntimeRulesUtility | None | typing | resolve_role_skill, resolve_domain_skill, resolve_stage_skill, resolve_overlays | RuntimeResolver | config maps | runtime skill mapping |  
| platform_core/bridges/base_bridge.py | BaseBridge | None | logging, typing | _normalize_payload, _normalize_result, _validate_interface_contract, _enforce_allowlist, _map_external_to_internal, _map_internal_to_external | all bridges | BaseResult, ValidationResultBase | Shared bridge behavior |  
| platform_core/bridges/agent_bridge.py | AgentBridge | BaseBridge | typing | build_agent_context, dispatch_tool, normalize_response, apply_retry_policy | app bootstrap, orchestrator | DependencyContainer, AllowlistResolver, ToolDispatcher | Agent-callable interface |  
| platform_core/bridges/jupyter_bridge.py | JupyterBridge | BaseBridge | typing | build_workspace, submit_interaction, refresh_workspace | Jupyter extension layer | controllers, Widget classes, payload builders | UI-side orchestration |  
| platform_core/bridges/api_bridge.py | APIBridge | BaseBridge | typing | map_request, invoke_internal, map_response | FastAPI layer | controllers | API boundary outputs |  
| platform_core/bridges/cli_bridge.py | CLIBridge | BaseBridge | typing | parse_command, run_cli_action, format_output | CLI app | controllers | CLI output |  
| platform_core/bridges/mcp_bridge.py | MCPBridge | BaseBridge | typing | register_tool, map_mcp_request, map_mcp_response | future MCP layer | AgentBridge/APIBridge | MCP-compatible boundary |  
| platform_core/ui/base_widget_component.py | BaseWidgetComponent | None | logging, typing | validate_props, build_component, register_callback, get_render_metadata, refresh | widget subclasses | ValidationResultBase | Shared widget behavior |  
  
====================================================================  
B. CONFIG SDK  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| config_sdk/models.py | ConfigRecord | BaseModelBase | typing, Field | compact_dict | ConfigService | BaseModelBase | Canonical config record |  
| config_sdk/models.py | ResolvedConfig | BaseModelBase | typing, Field | compact_dict | ConfigService | BaseModelBase | Effective config |  
| config_sdk/models.py | ConfigDiffResult | BaseResult | typing, Field | summarize_changes | ConfigService | BaseResult | Config diff result |  
| config_sdk/service.py | ConfigService | BaseService | pathlib, yaml, json, copy | load_config, validate_config, resolve_config, diff_config, get_config_version | ServiceFactory, controllers, all SDK services | ResultFactory, schema registry utilities | Config results |  
| config_sdk/loader.py | ConfigLoaderUtility | None | pathlib, yaml, json | load_yaml, load_json, load_dict | ConfigService | file utils | raw config payload |  
| config_sdk/validator.py | ConfigValidator | None | typing | validate | ConfigService | schema registry, ValidationResultBase | config validation |  
| config_sdk/overlay.py | ConfigOverlayUtility | None | copy | apply_overlays | ConfigService | None | merged config |  
| config_sdk/diff.py | ConfigDiffUtility | None | typing | diff_configs | ConfigService | None | change summary |  
| config_sdk/schema_registry.py | ConfigSchemaRegistry | None | typing | get_schema, has_schema, register_schema | ConfigValidator | None | schema lookup |  
  
====================================================================  
C. REGISTRY SDK  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| registry_sdk/models.py | ProjectRecord | BaseModelBase | datetime, Field | compact_dict | ProjectRegistryService | BaseModelBase | Project metadata |  
| registry_sdk/models.py | RunRecord | BaseModelBase | datetime, Field | compact_dict | RunRegistryService | BaseModelBase | Run metadata |  
| registry_sdk/models.py | SkillRecord | BaseModelBase | Field | compact_dict | SkillRegistryService | BaseModelBase | Skill metadata |  
| registry_sdk/models.py | SDKRecord | BaseModelBase | Field | compact_dict | SDKRegistryService | BaseModelBase | SDK metadata |  
| registry_sdk/models.py | PolicyRecord | BaseModelBase | Field | compact_dict | PolicyRegistryService | BaseModelBase | Policy metadata |  
| registry_sdk/models.py | ValidationRegistryRecord | BaseModelBase | Field | compact_dict | ValidationRegistryService | BaseModelBase | Validation metadata |  
| registry_sdk/storage.py | RegistryStorageAdapter | BaseStorageService | sqlite3 optional, json | read, write, search | registry services | BaseStorageService | stored registry records |  
| registry_sdk/project_registry.py | ProjectRegistryService | BaseRegistryService | typing | create_record, get_record, update_record, search_records | RegistryService facade, SessionController | BaseRegistryService, RegistryStorageAdapter | ProjectRecord results |  
| registry_sdk/run_registry.py | RunRegistryService | BaseRegistryService | typing | create_record, get_record, update_record, search_records | WorkflowService, SessionController | BaseRegistryService, RegistryStorageAdapter | RunRecord results |  
| registry_sdk/skill_registry.py | SkillRegistryService | BaseRegistryService | typing | create_record, get_record, search_records | Runtime bootstrap | BaseRegistryService | SkillRecord results |  
| registry_sdk/sdk_registry.py | SDKRegistryService | BaseRegistryService | typing | create_record, get_record, search_records | bootstrap/docs | BaseRegistryService | SDKRecord results |  
| registry_sdk/policy_registry.py | PolicyRegistryService | BaseRegistryService | typing | create_record, get_record, search_records | PolicyService | BaseRegistryService | PolicyRecord results |  
| registry_sdk/validation_registry.py | ValidationRegistryService | BaseRegistryService | typing | create_record, get_record, search_records | ValidationService | BaseRegistryService | Validation registry results |  
| registry_sdk/search_utility.py | RegistrySearchUtility | None | typing | match_filters, search | registry services | None | filtered record lists |  
| registry_sdk/service.py | RegistryService | BaseService | typing | register_project, get_project, register_run, get_run, search_registry, register_skill_metadata, register_sdk_metadata | controllers/services | child registry services | unified registry facade |  
  
====================================================================  
D. OBSERVABILITY SDK  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| observabilitysdk/models.py | EventRecord | BaseModelBase | datetime, Field | compact_dict | EventWriter, ObservabilityService | BaseModelBase | Event record |  
| observabilitysdk/models.py | TraceRecord | BaseModelBase | datetime, Field | compact_dict | TraceManager | BaseModelBase | Trace record |  
| observabilitysdk/models.py | ReplaySummary | BaseModelBase | Field | compact_dict | ReplayEngine | BaseModelBase | Replay summary |  
| observabilitysdk/storage.py | EventStorageAdapter | BaseStorageService | json | read, write, search | EventWriter, EventQueryService | BaseStorageService | persisted events |  
| observabilitysdk/trace_manager.py | TraceManager | None | uuid, datetime | create_trace, get_trace_context | ObservabilityService | IDFactory, TimeProvider | TraceRecord |  
| observabilitysdk/event_writer.py | EventWriter | None | typing | write | ObservabilityService, controllers/services | EventStorageAdapter, TraceManager | Event write result |  
| observabilitysdk/event_query.py | EventQueryService | None | typing | query | ObservabilityService, ReplayEngine, FlowService | EventStorageAdapter | event lists |  
| observabilitysdk/replay_engine.py | ReplayEngine | None | typing | replay | ObservabilityService | EventQueryService | replay view |  
| observabilitysdk/lineage_builder.py | EventLineageBuilder | None | typing | build_lineage | ObservabilityService, FlowService | EventQueryService | lineage nodes/edges |  
| observabilitysdk/service.py | ObservabilityService | BaseService | typing | create_trace, write_event, query_events, replay_run, build_event_lineage | all services/controllers | child observability services | observability results |  
  
====================================================================  
E. ARTIFACT SDK  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| artifactsdk/models.py | ArtifactRecord | BaseModelBase | Field | compact_dict | ArtifactService | BaseModelBase | Artifact record |  
| artifactsdk/models.py | ArtifactManifest | BaseModelBase | Field | compact_dict | ArtifactService | BaseModelBase | Artifact manifest |  
| artifactsdk/models.py | ArtifactLineageRecord | BaseModelBase | Field | compact_dict | ArtifactLineageService | BaseModelBase | Artifact lineage record |  
| artifactsdk/storage_adapter.py | ArtifactStorageAdapter | BaseStorageService | boto3 optional, s3fs optional | read, write, exists, resolve_uri | ArtifactService | BaseStorageService | Artifact I/O |  
| artifactsdk/registry.py | ArtifactRegistryService | BaseRegistryService | typing | create_record, get_record, search_records | ArtifactService | BaseRegistryService | Artifact metadata CRUD |  
| artifactsdk/metadata.py | ArtifactMetadataUtility | None | typing | normalize_metadata, validate_metadata | ArtifactService | None | normalized metadata |  
| artifactsdk/locator.py | ArtifactLocator | None | typing | locate_artifact | ArtifactService | ArtifactRegistryService, ArtifactStorageAdapter | resolved paths/URIs |  
| artifactsdk/manifest.py | ArtifactManifestBuilder | None | typing | build_manifest | ArtifactService | ArtifactRegistryService | ArtifactManifest |  
| artifactsdk/lineage.py | ArtifactLineageService | None | typing | link_lineage, get_lineage | ArtifactService | ArtifactRegistryService | lineage refs |  
| artifactsdk/validators.py | ArtifactValidator | None | typing | validate_artifact | ArtifactService | ArtifactStorageAdapter | ValidationResultBase |  
| artifactsdk/version_resolver.py | ArtifactVersionResolver | None | typing | get_latest, get_explicit_version | ArtifactService | ArtifactRegistryService | artifact version refs |  
| artifactsdk/service.py | ArtifactService | BaseService | typing | register_artifact, get_artifact, locate_artifact, build_artifact_manifest, validate_artifact, link_artifact_lineage | all material SDKs | child artifact classes/services | artifact results |  
  
====================================================================  
F. AUDIT SDK  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| auditsdk/models.py | AuditRecord | BaseModelBase | datetime, Field | compact_dict | AuditService | BaseModelBase | Audit record |  
| auditsdk/models.py | DecisionRecord | BaseModelBase | datetime, Field | compact_dict | AuditService | BaseModelBase | Decision record |  
| auditsdk/models.py | ApprovalRecord | BaseModelBase | datetime, Field | compact_dict | AuditService | BaseModelBase | Approval record |  
| auditsdk/models.py | ExceptionRecord | BaseModelBase | Field | compact_dict | AuditService | BaseModelBase | Exception record |  
| auditsdk/models.py | SignoffRecord | BaseModelBase | Field | compact_dict | AuditService | BaseModelBase | Sign-off record |  
| auditsdk/audit_writer.py | AuditWriter | None | typing | write | AuditService | storage/registry deps | persisted audit |  
| auditsdk/decision_registry.py | DecisionRegistry | None | typing | register_decision, get_decision | AuditService | AuditWriter | DecisionRecord results |  
| auditsdk/approval_registry.py | ApprovalRegistry | None | typing | register_approval, get_approval | AuditService | AuditWriter | ApprovalRecord results |  
| auditsdk/exception_registry.py | ExceptionRegistry | None | typing | register_exception, get_exception | AuditService | AuditWriter | ExceptionRecord results |  
| auditsdk/signoff_registry.py | SignoffRegistry | None | typing | register_signoff, get_signoff | AuditService | AuditWriter | SignoffRecord results |  
| auditsdk/export.py | AuditExportService | None | typing | export_bundle | AuditService, ReportingService | registry/query deps | audit bundle refs |  
| auditsdk/service.py | AuditService | BaseService | typing | write_audit_record, register_decision, register_approval, register_exception, register_signoff, export_audit_bundle | hitl, validation, monitoring, controllers | child audit services | audit results |  
  
====================================================================  
G. WORKFLOW SDK  
====================================================================  
  
| File | Class | Parent | Primary Layer | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|---|  
| workflowsdk/models.py | WorkflowState | BaseModelBase | Foundation SDK | Field | compact_dict | WorkflowService | BaseModelBase | workflow state |  
| workflowsdk/models.py | CandidateVersion | BaseModelBase | Foundation SDK | Field | compact_dict | WorkflowService | BaseModelBase | candidate version |  
| workflowsdk/models.py | CheckpointRecord | BaseModelBase | Foundation SDK | Field | compact_dict | WorkflowService | BaseModelBase | checkpoint |  
| workflowsdk/stage_registry.py | StageRegistry | None | Foundation SDK | typing | get_stage, list_dependencies | WorkflowService | config | stage definitions |  
| workflowsdk/transition_guard.py | TransitionGuard | None | Foundation SDK | typing | validate_transition | WorkflowService | StageRegistry, policy/config rules | ValidationResultBase |  
| workflowsdk/state_store.py | WorkflowStateStore | BaseStorageService | Foundation SDK | json | get_state, update_state | WorkflowService | BaseStorageService | persisted workflow states |  
| workflowsdk/candidate_registry.py | CandidateRegistry | None | Foundation SDK | typing | create_candidate, get_candidate, list_candidates | WorkflowService | state store/artifact refs | candidate metadata |  
| workflowsdk/checkpoint_manager.py | CheckpointManager | None | Foundation SDK | typing | create_checkpoint, load_checkpoint | WorkflowService | state store | checkpoint refs |  
| workflowsdk/recovery_manager.py | RecoveryManager | None | Foundation SDK | typing | resolve_recovery_path | WorkflowService, RecoveryController | state store, event replay | recovery recommendation |  
| workflowsdk/service.py | WorkflowService | BaseService | Foundation SDK | typing | bootstrap_project_workflow, get_workflow_state, update_workflow_state, route_next_stage, create_candidate_version, select_candidate_version, create_checkpoint, resolve_recovery_path | controllers, hitl, monitoring | child workflow components, audit/event services | workflow results |  
  
====================================================================  
H. POLICY SDK  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| policysdk/models.py | PolicyPack | BaseModelBase | Field | compact_dict | PolicyService | BaseModelBase | policy pack |  
| policysdk/models.py | ThresholdRule | BaseModelBase | Field | compact_dict | PolicyService | BaseModelBase | threshold rule |  
| policysdk/models.py | ApprovalRule | BaseModelBase | Field | compact_dict | PolicyService | BaseModelBase | approval rule |  
| policysdk/models.py | EscalationRule | BaseModelBase | Field | compact_dict | PolicyService | BaseModelBase | escalation rule |  
| policysdk/policy_loader.py | PolicyLoader | None | typing | load_policy_pack, resolve_effective_policy | PolicyService | config, registry | effective policy |  
| policysdk/threshold_engine.py | ThresholdEngine | None | typing | evaluate_metric_set | PolicyService | PolicyPack | threshold evaluations |  
| policysdk/control_matrix.py | ControlMatrixService | None | typing | get_stage_controls, requires_human_review | PolicyService, WorkflowService | PolicyPack | stage controls |  
| policysdk/approval_rules.py | ApprovalRulesService | None | typing | get_approval_requirements, can_actor_approve | PolicyService, HITLService | PolicyPack | approval requirements |  
| policysdk/escalation_rules.py | EscalationRulesService | None | typing | should_escalate, get_escalation_target | PolicyService, HITLService | PolicyPack | escalation guidance |  
| policysdk/waiver_rules.py | WaiverRulesService | None | typing | is_waivable, get_waiver_requirements | PolicyService | PolicyPack | waiver decision |  
| policysdk/service.py | PolicyService | BaseService | typing | load_policy_pack, evaluate_metric_set, detect_breaches, get_stage_controls, requires_human_review, get_approval_requirements, can_actor_approve, should_escalate, is_waivable | controllers, hitl, workflow, validation, monitoring | child policy services | policy results |  
  
====================================================================  
I. HITL SDK  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| hitlsdk/models.py | ReviewRecord | BaseModelBase | Field | compact_dict | HITLService | BaseModelBase | review record |  
| hitlsdk/models.py | ReviewTemplate | BaseModelBase | Field | compact_dict | HITLService | BaseModelBase | review template |  
| hitlsdk/models.py | ReviewActionRecord | BaseModelBase | Field | compact_dict | HITLService | BaseModelBase | review action |  
| hitlsdk/review_templates.py | ReviewTemplateRegistry | Standalone Service | typing | get_template, validate_template | HITLService | config/templates | template lookup |  
| hitlsdk/review_registry.py | ReviewRegistryService | BaseRegistryService | typing | create_record, get_record, update_record, search_records | HITLService | BaseRegistryService | review CRUD |  
| hitlsdk/review_payloads.py | ReviewPayloadService | BaseReviewComponent | typing | build_review_payload, build_candidate_selection_payload, build_validation_review_payload, build_monitoring_breach_payload | ReviewController, HITLService | review registry, artifacts, workflow, templates | ReviewPayload |  
| hitlsdk/action_validation.py | ActionValidationService | BaseReviewComponent | typing | validate_action, validate_edit_payload, validate_selection_payload | HITLService, ReviewController | review registry, policy service | ValidationResultBase |  
| hitlsdk/review_status_machine.py | ReviewStatusMachine | BaseReviewComponent | typing | get_allowed_transitions, transition_review_state, validate_transition | HITLService | review registry, audit/event services | review state transition results |  
| hitlsdk/approval_manager.py | ApprovalManager | BaseReviewComponent | typing | approve_review, approve_with_conditions, revoke_approval | HITLService | review registry, audit, policy | approval results |  
| hitlsdk/override_manager.py | OverrideManager | BaseReviewComponent | typing | create_override, validate_override, finalize_override | HITLService | policy, audit, review registry | override results |  
| hitlsdk/escalation_manager.py | EscalationManager | BaseReviewComponent | typing | escalate_review, escalate_due_to_timeout, determine_target | HITLService | policy, audit, review registry | escalation results |  
| hitlsdk/decision_capture.py | DecisionCaptureService | BaseReviewComponent | typing | capture_decision, build_decision_patch, link_decision_to_review | HITLService, ReviewController | workflow, audit, review registry | decision result/state patch |  
| hitlsdk/service.py | HITLService | BaseService | typing | create_review, get_review, build_review_payload, validate_action, transition_review_state, approve_review, approve_with_conditions, escalate_review, capture_decision | ReviewController, ValidationController, MonitoringController | child HITL services, policy, audit, workflow | review results |  
  
====================================================================  
J. DATASET / DQ / FEATURE / EVALUATION / DATAPREP  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| dataset_sdk/service.py | DatasetService | BaseService | typing | register_dataset, create_snapshot, register_split, create_sample_reference, create_lineage_reference, validate_dataset_contract, get_dataset_snapshot | DataPrepController, MonitoringController | registry/artifact/DQ helpers | dataset metadata results |  
| dataset_sdk/contract_validator.py | DatasetContractValidator | Standalone Service | typing | validate_contract, validate_snapshot_contract | DatasetService | contract config | ValidationResultBase |  
| dq_sdk/service.py | DQService | BaseService | typing, pandas, numpy, pyspark optional | run_schema_checks, run_missingness_checks, run_consistency_checks, build_distribution_profile, run_business_rule_checks, build_dq_summary, create_dq_exception | DataPrepController, MonitoringController, ValidationController | check modules | DQ results |  
| dq_sdk/schema_checks.py | SchemaCheckService | Standalone Service | typing | run | DQService | schema rules | schema check output |  
| dq_sdk/missingness_checks.py | MissingnessCheckService | Standalone Service | typing | run | DQService | thresholds | missingness output |  
| dq_sdk/consistency_checks.py | ConsistencyCheckService | Standalone Service | typing | run | DQService | consistency rules | consistency output |  
| dq_sdk/distribution_profile.py | DistributionProfiler | Standalone Service | typing | build_profile | DQService, MonitoringService | None | profile summary |  
| feature_sdk/service.py | FeatureService | BaseService | typing | apply_transformations, build_lags, build_differences, build_grouped_features, encode_categorical, register_feature_metadata, register_feature_lineage | DataPrepController, ScorecardService | child feature modules | feature results |  
| feature_sdk/transformation_engine.py | TransformationEngine | Standalone Service | typing | apply_transformations | FeatureService | transform rules | transformed feature refs |  
| feature_sdk/lag_engine.py | LagEngine | Standalone Service | typing | build_lags | FeatureService | lag spec | lag feature refs |  
| feature_sdk/grouping_engine.py | GroupingEngine | Standalone Service | typing | build_grouped_features | FeatureService | grouping spec | grouped feature refs |  
| feature_sdk/encoding_helpers.py | EncodingHelper | Standalone Utility | typing | encode, map_categories | FeatureService | encoding spec | encoded outputs |  
| evaluation_sdk/service.py | EvaluationService | BaseService | typing, sklearn, scipy | compute_metrics, run_diagnostics, run_stability_checks, run_calibration_checks, compare_candidates, evaluate_thresholds, compare_to_benchmark | ScorecardService, ValidationService, MonitoringService, EvaluationController | child eval modules | evaluation results |  
| evaluation_sdk/metric_engine.py | MetricEngine | Standalone Service | typing | compute_metrics | EvaluationService | metric registry | metric outputs |  
| evaluation_sdk/diagnostic_engine.py | DiagnosticEngine | Standalone Service | typing | run_diagnostics | EvaluationService | diagnostic registry | diagnostic outputs |  
| evaluation_sdk/comparison_framework.py | ComparisonEngine | Standalone Service | typing | compare_candidates, build_comparison_summary | EvaluationService | ranking rules | candidate comparisons |  
| evaluation_sdk/threshold_evaluator.py | ThresholdEvaluator | Standalone Service | typing | evaluate_thresholds, classify_metric_status | EvaluationService, PolicyService | threshold packs | threshold results |  
| dataprepsdk/service.py | DataPrepService | BaseService | typing | validate_dataprep_config, validate_template_request, execute_request, build_cross_sectional_dataset, build_panel_dataset, build_time_series_dataset, build_cohort_dataset, build_event_history_dataset, reproduce_dataset | DataPrepController | template registry, logical modules, Spark service | logical dataprep results |  
| dataprepsdk/spark_service.py | SparkDataPrepService | BaseSparkService | pyspark | build_cross_sectional_dataset_spark, build_panel_dataset_spark, build_time_series_dataset_spark, build_cohort_dataset_spark, build_event_history_dataset_spark, run_prep_quality_checks_spark | DataPrepService | Spark child modules | Spark dataprep results |  
| dataprepsdk/template_registry.py | TemplateRegistryService | Standalone Service | typing | get_template, list_templates, validate_template_request | DataPrepService | config/template map | template resolution |  
| dataprepsdk/lineage_resolver.py | LineageResolver | Standalone Service | typing | resolve_lineage, build_join_plan | DataPrepService | source mappings | logical lineage plan |  
| dataprepsdk/grain_manager.py | GrainManager | Standalone Service | typing | resolve_grain, validate_grain | DataPrepService | grain rules | grain decision |  
| dataprepsdk/time_aligner.py | TimeAligner | Standalone Service | typing | resolve_time_windows, validate_time_alignment | DataPrepService | time rules | time alignment plan |  
| dataprepsdk/target_builder.py | TargetBuilder | Standalone Service | typing | resolve_target_definition, validate_target_logic | DataPrepService | target rules | target plan |  
| dataprepsdk/split_builder.py | SplitBuilder | Standalone Service | typing | resolve_split_definition, validate_split_strategy | DataPrepService | split rules | split plan |  
| dataprepsdk/leakage_checker.py | LeakageChecker | Standalone Service | typing | run_leakage_checks, summarize_leakage_risk | DataPrepService | time/target refs | leakage summary |  
| dataprepsdk/spark_source_reader.py | SparkSourceReader | BaseSparkService | pyspark | read_sources, project_columns | SparkDataPrepService | Spark session | Spark DataFrames |  
| dataprepsdk/spark_target_builder.py | SparkTargetBuilder | BaseSparkService | pyspark | build_targets | SparkDataPrepService | target rules | target columns |  
| dataprepsdk/spark_split_builder.py | SparkSplitBuilder | BaseSparkService | pyspark | build_splits | SparkDataPrepService | split rules | split flags |  
| dataprepsdk/spark_quality_checker.py | SparkQualityChecker | BaseSparkService | pyspark | run_quality_checks | SparkDataPrepService | DQ service/check rules | Spark quality summary |  
| dataprepsdk/spark_manifest_builder.py | SparkManifestBuilder | BaseSparkService | pyspark | build_manifest | SparkDataPrepService | artifact/dataset refs | manifest refs |  
| dataprepsdk/spark_utils.py | SparkUtils | Standalone Utility | pyspark | safe_join, safe_count, project_columns, repartition_if_needed | all Spark modules | None | Spark helper outputs |  
  
====================================================================  
K. SCORECARD / VALIDATION / REPORTING  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| scorecardsdk/service.py | ScorecardService | BaseService | typing, sklearn, optbinning optional | build_fine_bins, build_coarse_bin_candidate, preview_edited_bins, finalize_coarse_bins, compare_binning_candidates, compute_woe_iv, build_feature_shortlist, fit_candidate_set, scale_scorecard, build_score_bands, build_scorecard_output_bundle | ScorecardController | dataprep, evaluation, feature, artifact/reporting helpers | scorecard results |  
| scorecardsdk/fine_classing.py | FineClassingEngine | Standalone Service | typing | build_fine_bins, summarize_fine_bins | ScorecardService | dataset/data refs | fine bin outputs |  
| scorecardsdk/coarse_classing.py | CoarseClassingEngine | Standalone Service | typing | build_candidate, validate_candidate, preview_edits, finalize_bins | ScorecardService, ReviewController | evaluation, artifact refs | coarse bin candidates/finals |  
| scorecardsdk/woe_iv.py | WOEIVEngine | Standalone Service | typing | compute_woe_iv, summarize_woe_iv | ScorecardService | bin refs, target refs | WOE/IV outputs |  
| scorecardsdk/feature_shortlist.py | FeatureShortlistEngine | Standalone Service | typing | build_shortlist, compare_shortlists, finalize_shortlist | ScorecardService | WOE/IV, feature rules | shortlist refs |  
| scorecardsdk/logistic_models.py | LogisticCandidateEngine | Standalone Service | sklearn, typing | fit_candidate_set, summarize_model_candidate | ScorecardService | evaluation, dataset refs | model candidates |  
| scorecardsdk/score_scaling.py | ScalingEngine | Standalone Service | math, typing | scale_scorecard, summarize_scaling | ScorecardService | model candidate refs | score scaling output |  
| scorecardsdk/score_bands.py | ScoreBandEngine | Standalone Service | typing | build_score_bands, summarize_score_bands | ScorecardService | score outputs | score band outputs |  
| validationsdk/service.py | ValidationService | BaseService | typing | create_validation_scope, intake_evidence, assess_evidence_completeness, evaluate_fitness_dimensions, create_finding, assess_severity, build_conclusion_options, finalize_conclusion, create_remediation_action, build_validation_output_bundle | ValidationController | workflow, hitl, policy, audit, evaluation, reporting helpers | validation results |  
| validationsdk/evidence_intake.py | EvidenceIntakeService | Standalone Service | typing | intake_evidence, classify_evidence, summarize_evidence_inventory | ValidationService | artifact refs | evidence inventory |  
| validationsdk/evidence_completeness.py | EvidenceCompletenessService | Standalone Service | typing | assess_evidence_completeness, summarize_missing_evidence | ValidationService | scope/evidence inventory | completeness summary |  
| validationsdk/fitness_framework.py | FitnessFrameworkService | Standalone Service | typing | evaluate_fitness_dimensions, summarize_fitness_framework | ValidationService | evaluation/evidence refs | fitness summaries |  
| validationsdk/conclusion_engine.py | ConclusionEngine | Standalone Service | typing | build_conclusion_options, finalize_conclusion | ValidationService | fitness/findings/policy | conclusion outputs |  
| validationsdk/remediation_tracker.py | RemediationTracker | Standalone Service | typing | create_remediation_action, update_remediation_status, summarize_remediation | ValidationService | finding registry/audit/workflow | remediation results |  
| reporting_sdk/service.py | ReportingService | BaseService | typing, jinja2 | build_technical_report, build_executive_summary, build_committee_pack, build_validation_note, get_narrative_block, export_chart_refs, export_table_refs, assemble_pack | ReportingController, ValidationController, MonitoringController | artifacts, audit, narrative registry, pack assembler | reporting results |  
| reporting_sdk/narrative_blocks.py | NarrativeBlockRegistry | Standalone Service | typing | get_block, register_block, render_block | ReportingService | config/registry | narrative text blocks |  
| reporting_sdk/technical_report_builder.py | TechnicalReportBuilder | Standalone Service | typing | build_technical_report, build_technical_section | ReportingService | narrative blocks, artifact refs | technical report sections |  
| reporting_sdk/executive_summary_builder.py | ExecutiveSummaryBuilder | Standalone Service | typing | build_executive_summary, summarize_for_exec | ReportingService | decisions/findings | exec summary |  
| reporting_sdk/validation_note_builder.py | ValidationNoteBuilder | Standalone Service | typing | build_validation_note, build_finding_section | ReportingService | validation refs, narratives | validation note |  
| reporting_sdk/committee_pack_builder.py | CommitteePackBuilder | Standalone Service | typing | build_committee_pack, build_committee_sections | ReportingService | exec summary, visuals | committee sections |  
| reporting_sdk/chart_table_export.py | ChartTableExportService | Standalone Service | typing | export_chart_refs, export_table_refs, summarize_visual_assets | ReportingService | artifact refs | visual asset refs |  
| reporting_sdk/pack_assembler.py | PackAssembler | Standalone Service | typing | assemble_pack, validate_pack_structure | ReportingService | section refs | final pack bundle |  
  
====================================================================  
L. KNOWLEDGE / RETRIEVAL / FLOW / MONITORING  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| knowledge_sdk/service.py | KnowledgeService | BaseService | typing | create_knowledge_object, register_knowledge, search_knowledge, capture_from_event, capture_from_decision, set_quality_status, promote_knowledge, export_knowledge_bundle | KnowledgeController, ValidationController | registry, audit, event, linker, promotion | knowledge results |  
| knowledge_sdk/knowledge_linker.py | KnowledgeLinker | Standalone Service | typing | link_to_artifact, link_to_decision, link_to_finding, link_to_conclusion | KnowledgeService | artifact/audit/validation refs | linked refs |  
| knowledge_sdk/promotion_manager.py | PromotionManager | Standalone Service | typing | request_promotion, approve_promotion, promote | KnowledgeService | quality manager, audit | promotion results |  
| rag_sdk/service.py | RetrievalService | BaseService | typing | chunk_document, embed_chunks, route_query, retrieve, rerank_results, compress_context, build_context_pack, get_budget_profile | RetrievalController, AgentBridge | query router, retriever, compressor, budget manager | retrieval/context results |  
| rag_sdk/query_router.py | QueryRouter | Standalone Service | typing | route_query, build_retrieval_plan | RetrievalService | runtime context/config | retrieval plan |  
| rag_sdk/retriever.py | Retriever | Standalone Service | typing | retrieve, retrieve_by_scope, retrieve_by_project | RetrievalService | vector/index store, filters | raw retrieval results |  
| rag_sdk/reranker.py | Reranker | Standalone Service | typing | rerank_results, deduplicate_results | RetrievalService | retrieval results | reranked results |  
| rag_sdk/context_compressor.py | ContextCompressor | Standalone Service | typing | compress_context, compress_results_to_summary | RetrievalService | reranked results | compressed summaries |  
| rag_sdk/token_budget_manager.py | TokenBudgetManager | Standalone Utility | typing | get_budget_profile, apply_budget, estimate_size | RetrievalService, RuntimeResolver | config | budget enforcement |  
| flowvizsdk/service.py | FlowService | BaseService | typing | build_nodes, build_edges, summarize_flow, build_timeline, export_graph, filter_graph, get_drilldown_payload | FlowController, ReportingController | node builder, edge builder, timeline builder, detail linker | flow/timeline outputs |  
| flowvizsdk/node_builder.py | NodeBuilder | Standalone Service | typing | build_nodes, build_stage_nodes, build_review_nodes | FlowService | event/workflow/audit refs | flow nodes |  
| flowvizsdk/edge_builder.py | EdgeBuilder | Standalone Service | typing | build_edges, build_transition_edges, build_dependency_edges | FlowService | node builder, workflow refs | flow edges |  
| flowvizsdk/timeline_builder.py | TimelineBuilder | Standalone Service | typing | build_timeline, summarize_timeline | FlowService | event refs | timeline |  
| flowvizsdk/detail_linker.py | DetailLinker | Standalone Service | typing | build_drilldown_payload, link_node_details | FlowService | artifact/audit/hitl refs | drilldown payload |  
| monitoringsdk/service.py | MonitoringService | BaseService | typing | get_monitoring_template, ingest_snapshot, validate_snapshot, append_snapshot, compute_monitoring_metrics, evaluate_monitoring_thresholds, compute_drift, compute_segment_monitoring, build_dashboard_payload, build_dashboard_config, create_monitoring_note, build_annual_review_pack, write_monitoring_outputs | MonitoringController | template registry, validator, history manager, metric engine, drift engine, dashboard builder | monitoring results |  
| monitoringsdk/monitoring_template_registry.py | MonitoringTemplateRegistry | Standalone Service | typing | get_monitoring_template, validate_monitoring_template | MonitoringService | config/registry | template refs |  
| monitoringsdk/snapshot_validator.py | SnapshotValidator | Standalone Service | typing | validate_snapshot, validate_snapshot_grain | MonitoringService | DQ checks/template | ValidationResultBase |  
| monitoringsdk/history_manager.py | MonitoringHistoryManager | Standalone Service | typing | append_snapshot, get_history, get_current_baseline | MonitoringService | dataset/history store | history refs |  
| monitoringsdk/metric_engine.py | MonitoringMetricEngine | Standalone Service | typing | compute_monitoring_metrics, summarize_monitoring_metrics | MonitoringService | evaluation_sdk | KPI summaries |  
| monitoringsdk/drift_engine.py | DriftEngine | Standalone Service | typing | compute_drift, summarize_drift | MonitoringService | evaluation_sdk | drift summaries |  
| monitoringsdk/segment_monitor.py | SegmentMonitor | Standalone Service | typing | compute_segment_monitoring, summarize_segment_movements | MonitoringService | history/evaluation refs | segment summaries |  
| monitoringsdk/dashboard_payload_builder.py | DashboardPayloadBuilder | Standalone Service | typing | build_dashboard_payload, build_kpi_view, build_trend_view | MonitoringService, JupyterBridge | metric/drift/segment outputs | dashboard payload |  
| monitoringsdk/dashboard_config_builder.py | DashboardConfigBuilder | Standalone Service | typing | build_dashboard_config | MonitoringService | template/dashboard rules | dashboard config |  
| monitoringsdk/annual_review_pack_builder.py | AnnualReviewPackBuilder | Standalone Service | typing | build_annual_review_pack, summarize_annual_monitoring | MonitoringService, ReportingService | history/reporting refs | annual review pack |  
| monitoringsdk/note_manager.py | MonitoringNoteManager | Standalone Service | typing | create_monitoring_note, assign_monitoring_action, summarize_action_log | MonitoringService, ReviewController | audit/workflow/hitl refs | notes/actions |  
  
====================================================================  
M. UI COMPONENTS  
====================================================================  
  
| File | Class | Parent | Key Imports | Key Methods | Instantiated By | Depends On | Returns / Produces |  
|---|---|---|---|---|---|---|---|  
| widgetsdk/review_shell.py | ReviewShell | BaseWidgetComponent | typing | validate_props, build_component, refresh | JupyterBridge, WorkspaceBuilder | ReviewPayloadMapper | 3-panel review UI spec |  
| widgetsdk/selection_cards.py | SelectionCards | BaseWidgetComponent | typing | validate_props, build_component, refresh | JupyterBridge | candidate payloads | selection UI spec |  
| widgetsdk/bootstrap_cards.py | BootstrapCards | BaseWidgetComponent | typing | validate_props, build_component | JupyterBridge | session options | bootstrap UI spec |  
| widgetsdk/recovery_cards.py | RecoveryCards | BaseWidgetComponent | typing | validate_props, build_component | JupyterBridge | recovery options | recovery UI spec |  
| widgetsdk/flow_panels.py | FlowPanels | BaseWidgetComponent | typing | validate_props, build_component, refresh | JupyterBridge | flow graph payload | flow UI spec |  
| widgetsdk/detail_panels.py | DetailPanels | BaseWidgetComponent | typing | validate_props, build_component, refresh | JupyterBridge | drilldown payload | detail UI spec |  
| widgetsdk/validation_cards.py | ValidationCards | BaseWidgetComponent | typing | validate_props, build_component, refresh | JupyterBridge | validation payloads | validation UI spec |  
| widgetsdk/evidence_panels.py | EvidencePanels | BaseWidgetComponent | typing | validate_props, build_component, refresh | JupyterBridge | evidence refs | evidence UI spec |  
| widgetsdk/comment_capture.py | CommentCapture | BaseWidgetComponent | typing | validate_props, build_component | JupyterBridge | action/rationale schema | comment UI spec |  
| widgetsdk/action_bar.py | ActionBar | BaseWidgetComponent | typing | validate_props, build_component, register_callback, refresh | JupyterBridge | allowed actions | bounded action UI spec |  
| jupyter_bridge/review_payload_mapper.py | ReviewPayloadMapper | Standalone Utility | typing | map_review_payload | JupyterBridge | ReviewPayload | widget props |  
| jupyter_bridge/interaction_payload_builder.py | InteractionPayloadBuilder | Standalone Utility | typing | build | JupyterBridge | widget state, actor info | InteractionPayload |  
| jupyter_bridge/workspace_builder.py | WorkspaceBuilder | Standalone Utility | typing | build_review_workspace, build_dashboard_workspace, build_flow_workspace | JupyterBridge | widget classes | workspace composition |  
| jupyter_bridge/monitoring_workspace_sync.py | MonitoringWorkspaceSync | Standalone Utility | typing | refresh_snapshot, refresh_breach_state | JupyterBridge | MonitoringService results | refreshed UI state |  
  
====================================================================  
N. FILE PLACEMENT GUIDANCE  
====================================================================  
  
| File Group | Recommended Location | Notes |  
|---|---|---|  
| Base models and result contracts | platform_core/schemas/ | Keep global contracts centralized |  
| Base service / controller / bridge / runtime / widget classes | platform_core/services/, controllers/, bridges/, runtime/, ui/ | Do not duplicate bases inside SDKs |  
| SDK-specific models | each_sdk/models.py | Domain-local model ownership |  
| SDK facade service | each_sdk/service.py | One main public service per SDK |  
| Heavy internal logic units | each_sdk/<module>.py | Keep service facade thin |  
| Storage adapters | either sdk/storage.py or shared under platform_core/storage/ | Depends on reuse level |  
| Registries | registry_sdk/ and SDK-specific local registries only if needed | Avoid duplicate registry patterns |  
| Spark execution classes | dataprepsdk/spark/*.py | Keep Spark logic isolated |  
| Widget components | widgetsdk/*.py | Presentation only |  
| Mappers/builders | jupyter_bridge/*.py or platform_core/utils/ | Keep UI glue separate from widgets |  
  
====================================================================  
O. FINAL RECOMMENDATIONS  
====================================================================  
  
1. Each SDK should ideally have:  
   - models.py  
   - service.py  
   - exceptions.py  
   - 3 to 8 focused helper modules  
  
2. Keep `service.py` as the public façade.  
   It should delegate to internal child services/utilities.  
  
3. Prefer standalone services/utilities for:  
   - engines  
   - builders  
   - validators  
   - mappers  
   - exporters  
   - registries  
   rather than creating more base classes.  
  
4. The most important files to standardize first are:  
   - platform_core/schemas/base_results.py  
   - platform_core/services/base_service.py  
   - platform_core/services/base_spark_service.py  
   - platform_core/controllers/base_controller.py  
   - platform_core/bridges/base_bridge.py  
   - platform_core/runtime/resolver.py  
  
5. The most important public façade classes are:  
   - ConfigService  
   - RegistryService  
   - ObservabilityService  
   - ArtifactService  
   - AuditService  
   - WorkflowService  
   - PolicyService  
   - HITLService  
   - DatasetService  
   - DQService  
   - FeatureService  
   - EvaluationService  
   - DataPrepService  
   - ScorecardService  
   - ValidationService  
   - ReportingService  
   - KnowledgeService  
   - RetrievalService  
   - MonitoringService  
  
====================================================================  
P. NEXT BEST ARTIFACT  
====================================================================  
  
The next most useful deliverable would be a:  
  
FUNCTION CATALOG TABLE  
with one row per public method and columns:  
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
  
That would be the most direct coding reference before implementation.  
  
====================================================================  
END OF FILE-BY-FILE CLASS MAPPING TABLE  
====================================================================  
