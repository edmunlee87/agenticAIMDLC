# Sdk details   
  
====================================================================  
SDK CATALOG  
ENTERPRISE AGENTIC AI WORKFLOW PLATFORM  
COPIABLE REFERENCE FORMAT  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This document lists all proposed SDKs by category, their purpose,  
their key modules, and the standardized shared signatures /  
connections that allow them to work coherently under one platform.  
  
DESIGN PRINCIPLE  
--------------------------------------------------------------------  
The SDK ecosystem is grouped into:  
  
1. CORE WORKFLOW AUTOMATION SDKS  
2. SHARED ANALYTICAL CAPABILITY SDKS  
3. DOMAIN-SPECIFIC MODELING SDKS  
4. VALIDATION SDK  
5. INTEGRATION / BRIDGE LAYER  
6. SHARED STANDARD CONTRACTS AND CONNECTION PATTERNS  
  
The design principle is:  
- core SDKs = control plane  
- shared capability SDKs = reusable engines  
- domain SDKs = model-family logic  
- validation SDK = independent challenge plane  
- integration layer = exposure to agent / UI / API / MCP  
- shared contracts = common interfaces across everything  
  
====================================================================  
1. CORE WORKFLOW AUTOMATION SDKS  
====================================================================  
  
1.1 workflowsdk  
--------------------------------------------------------------------  
Purpose:  
Control workflow lifecycle, state, stage transitions, checkpoints,  
candidate version handling, selection enforcement, resume, and  
recovery.  
  
Key modules:  
- project_bootstrap  
- workflow_state  
- routing_engine  
- stage_registry  
- checkpoint_manager  
- session_manager  
- recovery_manager  
- candidate_registry  
- selection_registry  
- dependency_manager  
- state_persistence  
- transition_guard  
  
Primary responsibilities:  
- initialize project / run / session  
- move workflow from stage to stage  
- block invalid transitions  
- manage reruns and branches  
- ensure downstream stage knows selected upstream version  
- support resume from prior sessions or failed stages  
  
Standardized shared connections:  
- uses registry_sdk for lookup  
- uses artifactsdk for artifact registration references  
- uses observabilitysdk for event emission  
- uses auditsdk for decision-linked transitions  
- uses policysdk for stage gating  
- consumed by skills and orchestrator agent  
  
1.2 hitlsdk  
--------------------------------------------------------------------  
Purpose:  
Manage human-in-the-loop review lifecycle, bounded actions, approvals,  
overrides, and escalations.  
  
Key modules:  
- review_payloads  
- review_registry  
- approval_manager  
- override_manager  
- reviewer_assignment  
- action_validation  
- escalation_manager  
- review_status_machine  
- decision_capture  
- review_templates  
  
Primary responsibilities:  
- create review payload  
- validate allowed actions  
- capture user decision  
- link review to decision / approval  
- support approval with changes, rerun, reject, escalate  
- support candidate version selection reviews  
- support validation conclusion reviews  
  
Standardized shared connections:  
- uses workflowsdk to pause / resume gated stages  
- uses observabilitysdk for review events  
- uses auditsdk for final sign-off records  
- uses widgetsdk for review UI rendering  
- uses policysdk for approval and escalation rules  
  
1.3 observabilitysdk  
--------------------------------------------------------------------  
Purpose:  
Capture structured append-only runtime and workflow events.  
  
Key modules:  
- event_writer  
- event_schema  
- replay_engine  
- lineage_builder  
- trace_manager  
- event_query  
- event_enrichment  
- event_router  
- event_store_adapter  
  
Primary responsibilities:  
- write event logs  
- assign trace IDs and parent-child relationships  
- support replay by run  
- support lineage reconstruction  
- emit candidate, review, selection, validation, and recovery events  
  
Standardized shared connections:  
- called by all SDKs for material events  
- feeds flowvizsdk  
- referenced by auditsdk  
- queried by workflowsdk for replay / recovery  
  
1.4 auditsdk  
--------------------------------------------------------------------  
Purpose:  
Store formal audit trail for approvals, rejections, overrides,  
selected versions, validation findings, and conclusions.  
  
Key modules:  
- audit_writer  
- decision_registry  
- approval_registry  
- exception_registry  
- audit_export  
- audit_views  
- signoff_registry  
- conditional_approval_manager  
  
Primary responsibilities:  
- persist auditable decision records  
- store sign-off conditions  
- record rationale and evidence links  
- support governance and audit exports  
  
Standardized shared connections:  
- consumes review outcomes from hitlsdk  
- consumes state and stage data from workflowsdk  
- references artifactsdk for evidence linkage  
- references observabilitysdk event IDs  
  
1.5 artifactsdk  
--------------------------------------------------------------------  
Purpose:  
Register artifacts, preserve metadata, maintain lineage, and provide  
artifact lookup.  
  
Key modules:  
- artifact_registry  
- artifact_metadata  
- artifact_lineage  
- artifact_locator  
- artifact_validators  
- artifact_manifest  
- storage_adapter  
- checksum_manager  
- version_resolver  
  
Primary responsibilities:  
- register all material outputs and inputs  
- link artifacts to candidate versions and runs  
- store schema version and storage location  
- support artifact retrieval and traceability  
  
Standardized shared connections:  
- used by all SDKs that produce outputs  
- referenced by reviews, decisions, validation findings  
- used by workflowsdk for dependency checks  
- used by validationsdk for evidence completeness  
  
1.6 flowvizsdk  
--------------------------------------------------------------------  
Purpose:  
Transform raw events into flow nodes, flow edges, and timelines for  
visual review and drill-down.  
  
Key modules:  
- node_builder  
- edge_builder  
- flow_summary  
- timeline_builder  
- graph_export  
- detail_linker  
- flow_filters  
- drilldown_router  
  
Primary responsibilities:  
- summarize lifecycle path  
- show candidate generation and selection  
- show reviews, reruns, failures, and validation outcomes  
- support graph and timeline view  
  
Standardized shared connections:  
- consumes events from observabilitysdk  
- references auditsdk and artifactsdk for drill-down  
- exposed through widgetsdk and reporting_sdk  
  
1.7 policysdk  
--------------------------------------------------------------------  
Purpose:  
Load and evaluate policy packs, thresholds, waiver rules, sign-off  
rules, and control matrix logic.  
  
Key modules:  
- policy_loader  
- threshold_engine  
- breach_detector  
- waiver_rules  
- control_matrix  
- rule_evaluator  
- approval_rules  
- escalation_rules  
  
Primary responsibilities:  
- enforce workflow rules  
- detect breaches and warnings  
- decide mandatory review triggers  
- support development and validation policy controls  
  
Standardized shared connections:  
- consulted by workflowsdk for gating  
- consulted by hitlsdk for required approvals  
- consulted by validationsdk for validation sign-off rules  
- logs findings to observabilitysdk and auditsdk  
  
1.8 widgetsdk  
--------------------------------------------------------------------  
Purpose:  
Provide reusable UI shell and notebook widgets for review, selection,  
bootstrap, recovery, flow, and validation.  
  
Key modules:  
- review_shell  
- selection_cards  
- bootstrap_cards  
- recovery_cards  
- flow_panels  
- detail_panels  
- validation_cards  
- evidence_panels  
- comment_capture  
- action_bar  
  
Primary responsibilities:  
- render HITL review cards  
- render candidate selection cards  
- render bootstrap / resume UI  
- render validation finding and conclusion cards  
- provide consistent notebook UI shell  
  
Standardized shared connections:  
- connected to Python controller layer  
- submits to hitlsdk / workflowsdk  
- reads flowvizsdk outputs  
- displays artifactsdk links  
- uses validation outputs from validationsdk  
  
====================================================================  
2. SHARED ANALYTICAL CAPABILITY SDKS  
====================================================================  
  
2.1 config_sdk  
--------------------------------------------------------------------  
Purpose:  
Standardize config-driven behavior for all platform and domain SDKs.  
  
Key modules:  
- config_loader  
- config_schema_validator  
- config_versioning  
- config_resolver  
- environment_overlay  
- config_diff  
- config_registry_link  
  
Primary responsibilities:  
- load YAML / JSON / structured config  
- validate config against schema  
- resolve environment-specific overrides  
- provide versioned config references  
  
Standardized shared connections:  
- used by all SDKs  
- config IDs stored in artifactsdk and auditsdk  
- consumed by workflowsdk and domain SDKs  
  
2.2 registry_sdk  
--------------------------------------------------------------------  
Purpose:  
Provide common metadata registry and lookup APIs.  
  
Key modules:  
- project_registry  
- run_registry  
- skill_registry  
- sdk_registry  
- policy_registry  
- validation_registry  
- lookup_api  
- search_api  
  
Primary responsibilities:  
- resolve IDs to records  
- provide lookup for projects, runs, skills, policies, configs  
- support discovery and linkage across platform  
  
Standardized shared connections:  
- used by workflowsdk, validationsdk, UI controllers, agents  
  
2.3 dataset_sdk  
--------------------------------------------------------------------  
Purpose:  
Manage dataset snapshots, splits, lineage, and dataset references.  
  
Key modules:  
- dataset_registry  
- snapshot_manager  
- split_manager  
- sample_reference  
- lineage_reference  
- dataset_contract_validator  
  
Primary responsibilities:  
- register development / validation / test / oot data  
- assign dataset IDs  
- preserve lineage between data snapshots  
- support reproducibility  
  
Standardized shared connections:  
- referenced by workflowsdk and validationsdk  
- artifact outputs linked through artifactsdk  
  
2.4 dq_sdk  
--------------------------------------------------------------------  
Purpose:  
Perform data profiling and data quality checks.  
  
Key modules:  
- schema_checks  
- missingness_checks  
- consistency_checks  
- distribution_profile  
- business_rule_checks  
- dq_summary  
- dq_exception_builder  
  
Primary responsibilities:  
- identify data issues  
- generate DQ summaries  
- trigger DQ exception reviews  
  
Standardized shared connections:  
- outputs TestResult-like structures  
- logs through observabilitysdk  
- registers outputs through artifactsdk  
- can trigger hitlsdk reviews  
  
2.5 feature_sdk  
--------------------------------------------------------------------  
Purpose:  
Provide reusable feature construction and transformation tools.  
  
Key modules:  
- transformation_engine  
- lag_engine  
- differencing_engine  
- grouping_engine  
- encoding_helpers  
- feature_metadata  
- feature_lineage  
  
Primary responsibilities:  
- create standardized features  
- preserve feature lineage  
- reuse across scorecard, time series, ECL, LGD where appropriate  
  
Standardized shared connections:  
- registers feature outputs to artifactsdk  
- logs actions to observabilitysdk  
- used by scorecardsdk, timeseriessdk, eclsdk, lgdsdk  
  
2.6 evaluation_sdk  
--------------------------------------------------------------------  
Purpose:  
Provide metrics, diagnostics, testing, comparison, and benchmark  
support.  
  
Key modules:  
- metric_engine  
- diagnostic_engine  
- stability_checks  
- calibration_checks  
- comparison_framework  
- threshold_evaluator  
- benchmark_compare  
  
Primary responsibilities:  
- compute metrics and tests  
- compare candidate versions  
- support model review and validation review  
- support monitoring and annual review  
  
Standardized shared connections:  
- used by all domain SDKs  
- outputs linked to artifactsdk  
- consumed by hitlsdk reviews and validationsdk findings  
  
2.7 reporting_sdk  
--------------------------------------------------------------------  
Purpose:  
Create technical and governance-ready reporting outputs.  
  
Key modules:  
- technical_report_builder  
- executive_summary_builder  
- committee_pack_builder  
- validation_note_builder  
- narrative_blocks  
- chart_table_export  
- pack_assembler  
  
Primary responsibilities:  
- generate development packs  
- generate validation packs  
- generate committee-ready summaries  
- package evidence and narratives  
  
Standardized shared connections:  
- pulls from artifactsdk, auditsdk, flowvizsdk, validationsdk  
- may expose outputs into docs / deck packages later  
  
2.8 monitoring_sdk  
--------------------------------------------------------------------  
Purpose:  
Support post-development and ongoing monitoring workflows.  
  
Key modules:  
- drift_metrics  
- threshold_application  
- monitoring_summary  
- alert_engine  
- periodic_review_pack  
- ongoing_test_runner  
  
Primary responsibilities:  
- calculate monitoring metrics  
- track threshold breaches  
- support annual review  
- support validation of monitoring adequacy  
  
Standardized shared connections:  
- uses evaluation_sdk  
- logs through observabilitysdk  
- outputs monitoring artifacts  
- may trigger hitlsdk and validationsdk workflows  
  
====================================================================  
3. DOMAIN-SPECIFIC MODELING SDKS  
====================================================================  
  
3.1 scorecardsdk  
--------------------------------------------------------------------  
Purpose:  
Implement scorecard-specific modeling logic.  
  
Key modules:  
- fine_classing  
- coarse_classing  
- binning_compare  
- woe_iv  
- feature_shortlist  
- logistic_models  
- score_scaling  
- score_bands  
- scorecard_outputs  
- scorecard_monitoring_support  
  
Primary responsibilities:  
- run scorecard-specific feature treatment  
- produce binning candidates  
- fit scorecard models  
- support score scaling and score bands  
  
Shared signatures / connections:  
- uses feature_sdk  
- uses evaluation_sdk  
- registers candidate versions and artifacts  
- consumed by workflowsdk, hitlsdk, validationsdk  
  
3.2 timeseriessdk  
--------------------------------------------------------------------  
Purpose:  
Implement time series modeling workflow logic.  
  
Key modules:  
- stationarity  
- transformations  
- lag_engine  
- model_fit  
- forecast_compare  
- residual_diagnostics  
- scenario_projection  
- timeseries_outputs  
  
Primary responsibilities:  
- perform stationarity checks  
- build lags and transformations  
- support forecasting and diagnostics  
- support scenario projections  
  
Shared signatures / connections:  
- uses feature_sdk  
- uses evaluation_sdk  
- outputs artifacts and metrics in standard format  
- supports validation reuse via validationsdk  
  
3.3 eclsdk  
--------------------------------------------------------------------  
Purpose:  
Support ECL workflow orchestration and domain logic.  
  
Key modules:  
- staging  
- pd_inputs  
- lgd_inputs  
- ead_inputs  
- mev_engine  
- scenario_engine  
- overlay_engine  
- ecl_outputs  
  
Primary responsibilities:  
- orchestrate ECL-specific inputs  
- prepare scenario and overlay outputs  
- support downstream ECL reporting and validation  
  
Shared signatures / connections:  
- uses pdsdk, lgdsdk, eadsdk where needed  
- uses feature_sdk and evaluation_sdk  
- connects to validationsdk for challenge workflow  
  
3.4 lgdsdk  
--------------------------------------------------------------------  
Purpose:  
Support LGD-specific modeling workflow.  
  
Key modules:  
- cure_model  
- severity_model  
- downturn_adjustment  
- fl_adjustment  
- recovery_aggregation  
- lgd_outputs  
  
Primary responsibilities:  
- support cure / severity logic  
- support downturn / forward-looking adjustment  
- produce LGD-specific artifacts  
  
Shared signatures / connections:  
- uses evaluation_sdk  
- outputs standard TestResult / Artifact patterns  
- integrates with validationsdk  
  
3.5 pdsdk  
--------------------------------------------------------------------  
Purpose:  
Support PD-specific workflows.  
  
Key modules:  
- rating_pd  
- score_pd  
- term_structure  
- transition_logic  
- calibration_support  
- pd_monitoring  
  
Primary responsibilities:  
- support PD model workflows  
- support term structure and calibration  
- expose PD artifacts in common format  
  
3.6 eadsdk  
--------------------------------------------------------------------  
Purpose:  
Support EAD-specific workflows.  
  
Key modules:  
- exposure_estimation  
- ccf_support  
- utilization_modeling  
- ead_monitoring  
- ead_outputs  
  
Primary responsibilities:  
- support EAD model estimation  
- support conversion factors and utilization logic  
  
3.7 sicr_sdk  
--------------------------------------------------------------------  
Purpose:  
Support SICR-related rules and model-based workflow.  
  
Key modules:  
- sicr_rules  
- sicr_thresholds  
- sicr_model_compare  
- migration_tracking  
- sicr_outputs  
  
Primary responsibilities:  
- support rule-based and model-based SICR  
- support migration and threshold tracking  
  
3.8 stresssdk  
--------------------------------------------------------------------  
Purpose:  
Support stress testing workflows.  
  
Key modules:  
- scenario_application  
- macro_linkages  
- stressed_projection  
- result_aggregation  
- stress_outputs  
  
Primary responsibilities:  
- apply scenarios  
- generate stressed outputs  
- support governance packs and review  
  
====================================================================  
4. VALIDATION SDK  
====================================================================  
  
4.1 validationsdk  
--------------------------------------------------------------------  
Purpose:  
Provide a first-class, independent, configurable validation workflow  
and challenge engine aligned with the platform.  
  
Key modules:  
- validation_scope  
- evidence_intake  
- fitness_framework  
- finding_registry  
- issue_severity  
- conclusion_engine  
- remediation_tracker  
- validation_outputs  
- benchmark_compare  
- evidence_completeness  
  
Primary responsibilities:  
- run validation workflow  
- store findings and severity  
- support model fitness assessment  
- support final validation conclusion  
- support remediation tracking  
- support re-validation  
  
Shared signatures / connections:  
- uses workflowsdk for validation stage flow  
- uses hitlsdk for validation HITL  
- uses observabilitysdk and auditsdk  
- uses artifactsdk for evidence linkage  
- uses evaluation_sdk for test / metric interpretation  
- uses domain SDK outputs as evidence  
- may use policysdk for sign-off controls  
  
====================================================================  
5. INTEGRATION / BRIDGE LAYER  
====================================================================  
  
5.1 agent_bridge  
--------------------------------------------------------------------  
Purpose:  
Provide a controlled connection layer between SDKs and agent / skill  
runtime.  
  
Key modules:  
- tool_adapter  
- skill_adapter  
- agent_context_builder  
- response_normalizer  
- retry_policy  
  
Primary responsibilities:  
- expose deterministic SDK calls to agents  
- normalize outputs into shared format  
- enforce bounded tool interactions  
  
5.2 api_bridge  
--------------------------------------------------------------------  
Purpose:  
Expose SDK capabilities through APIs.  
  
Key modules:  
- rest_adapter  
- request_mapper  
- response_mapper  
- auth_hooks  
- error_mapper  
  
5.3 cli_bridge  
--------------------------------------------------------------------  
Purpose:  
Expose SDK capabilities through CLI.  
  
Key modules:  
- command_router  
- argument_parser  
- output_formatter  
  
5.4 jupyter_bridge  
--------------------------------------------------------------------  
Purpose:  
Bind widgets, controllers, and notebook runtime to SDKs.  
  
Key modules:  
- widget_controller  
- notebook_state_sync  
- action_dispatch  
- result_refresh  
  
5.5 mcp_bridge  
--------------------------------------------------------------------  
Purpose:  
Expose deterministic SDK capabilities to future MCP-compatible agent  
tooling.  
  
Key modules:  
- mcp_tool_registry  
- mcp_request_mapper  
- mcp_response_mapper  
  
====================================================================  
6. SHARED STANDARD SIGNATURES / STANDARDIZED CONNECTIONS  
====================================================================  
  
6.1 Standard Result Envelope  
--------------------------------------------------------------------  
All SDKs should return a common high-level result envelope.  
  
Suggested shared structure:  
- status  
- message  
- run_id  
- stage_name  
- module_name  
- module_version  
- artifacts_created  
- metrics_created  
- test_results_created  
- candidate_version_id if applicable  
- selected_candidate_version_id if applicable  
- warnings  
- errors  
  
6.2 Standard Artifact Registration Hook  
--------------------------------------------------------------------  
SDKs producing persisted outputs should support a common registration  
hook.  
  
Suggested shared call pattern:  
register_artifact(  
    artifact_type,  
    artifact_name,  
    producer_stage,  
    producer,  
    version,  
    uri_or_path,  
    metadata  
)  
  
6.3 Standard Observability Event Hook  
--------------------------------------------------------------------  
SDKs should support a common event logging hook.  
  
Suggested shared call pattern:  
log_event(  
    event_type,  
    run_id,  
    session_id,  
    stage_name,  
    actor_type,  
    actor_id,  
    summary,  
    payload  
)  
  
6.4 Standard Candidate Version Hook  
--------------------------------------------------------------------  
SDKs that produce multiple alternatives should support candidate  
registration.  
  
Suggested shared call pattern:  
register_candidate_version(  
    run_id,  
    project_id,  
    source_stage,  
    candidate_type,  
    candidate_name,  
    version_label,  
    summary_metrics,  
    artifact_refs,  
    metadata  
)  
  
6.5 Standard Version Selection Hook  
--------------------------------------------------------------------  
Workflow or review layers should support final version selection.  
  
Suggested shared call pattern:  
register_version_selection(  
    run_id,  
    selection_scope,  
    selected_candidate_version_id,  
    selection_type,  
    selected_by,  
    review_id,  
    comment  
)  
  
6.6 Standard Review Payload Contract  
--------------------------------------------------------------------  
HITL reviews across development and validation should support the same  
shell.  
  
Suggested shared structure:  
- review_id  
- review_type  
- title  
- decision_required  
- business_summary  
- technical_summary  
- recommendation  
- alternatives  
- allowed_actions  
- risk_flags  
- policy_findings  
- evidence_refs  
- review_status  
  
6.7 Standard Validation Finding Contract  
--------------------------------------------------------------------  
Validation findings should follow a common schema.  
  
Suggested shared structure:  
- finding_id  
- validation_run_id  
- stage_name  
- finding_type  
- severity  
- summary  
- detailed_description  
- supporting_evidence_refs  
- linked_artifact_ids  
- owner  
- due_date  
- status  
  
6.8 Standard Test Result Contract  
--------------------------------------------------------------------  
Any diagnostic / validation / rule test should support a shared  
structure.  
  
Suggested shared structure:  
- test_result_id  
- run_id  
- stage_name  
- test_name  
- test_category  
- result_status  
- test_statistic  
- threshold  
- interpretation  
- evidence_refs  
  
6.9 Standard Config Signature  
--------------------------------------------------------------------  
SDKs should support a common config loading interface.  
  
Suggested shared call pattern:  
load_config(  
    config_id=None,  
    config_path=None,  
    version=None,  
    environment=None  
)  
  
6.10 Standard Controller-to-SDK Connection Pattern  
--------------------------------------------------------------------  
The preferred notebook pattern shall be:  
  
Widget -> Python Controller -> workflowsdk / hitlsdk / validationsdk  
-> supporting SDKs -> artifactsdk / observabilitysdk / auditsdk  
  
This prevents widgets from directly invoking low-level SDK logic.  
  
6.11 Standard Agent-to-SDK Connection Pattern  
--------------------------------------------------------------------  
The preferred agent pattern shall be:  
  
Skill / Agent -> agent_bridge -> bounded SDK function -> standard  
result envelope -> observability hook -> artifact hook  
  
This prevents agents from bypassing logging and registration.  
  
====================================================================  
7. PROPOSED MINIMUM COMMON METHOD FAMILIES  
====================================================================  
  
The following method families should be standardized as common  
interface groups across SDKs:  
  
A. initialize_*  
- initialize_project  
- initialize_run  
- initialize_session  
- initialize_validation_run  
  
B. load_*  
- load_config  
- load_state  
- load_policy_pack  
- load_validation_pack  
- load_artifact  
- load_candidate_version  
  
C. validate_*  
- validate_inputs  
- validate_stage_prerequisites  
- validate_resume_state  
- validate_review_action  
- validate_evidence_completeness  
  
D. register_*  
- register_artifact  
- register_candidate_version  
- register_version_selection  
- register_validation_finding  
  
E. compute_*  
- compute_metrics  
- compute_tests  
- compute_diagnostics  
- compute_flow_summary  
  
F. create_*  
- create_review_payload  
- create_validation_note  
- create_committee_pack  
- create_monitoring_pack  
  
G. finalize_*  
- finalize_selection  
- finalize_review  
- finalize_validation_conclusion  
- finalize_run  
  
====================================================================  
8. DEPENDENCY VIEW  
====================================================================  
  
8.1 Core Dependency Logic  
--------------------------------------------------------------------  
Most SDKs should depend on these common services:  
- config_sdk  
- registry_sdk  
- artifactsdk  
- observabilitysdk  
  
8.2 Typical Development Workflow Dependency  
--------------------------------------------------------------------  
scorecardsdk  
-> feature_sdk  
-> evaluation_sdk  
-> artifactsdk  
-> observabilitysdk  
-> hitlsdk / workflowsdk  
  
8.3 Typical Validation Workflow Dependency  
--------------------------------------------------------------------  
validationsdk  
-> workflowsdk  
-> hitlsdk  
-> evaluation_sdk  
-> artifactsdk  
-> auditsdk  
-> observabilitysdk  
-> policysdk  
  
====================================================================  
9. IMPLEMENTATION PRIORITY  
====================================================================  
  
Phase 1 mandatory SDKs:  
- workflowsdk  
- hitlsdk  
- observabilitysdk  
- auditsdk  
- artifactsdk  
- config_sdk  
- registry_sdk  
- dataset_sdk  
- dq_sdk  
- feature_sdk  
- evaluation_sdk  
- reporting_sdk  
- scorecardsdk  
- jupyter_bridge  
- agent_bridge  
  
Phase 2 recommended SDKs:  
- flowvizsdk  
- policysdk  
- widgetsdk  
- validationsdk  
- monitoring_sdk  
- api_bridge  
- cli_bridge  
  
Phase 3 future SDKs:  
- timeseriessdk  
- eclsdk  
- lgdsdk  
- pdsdk  
- eadsdk  
- sicr_sdk  
- stresssdk  
- mcp_bridge  
  
====================================================================  
10. SUCCESS CRITERIA  
====================================================================  
  
The SDK design shall be considered successful when:  
  
1. all current scorecard workflow needs can be covered without ad hoc  
   one-off packages  
2. shared SDKs can be reused across future model families  
3. candidate version generation and final selection use common hooks  
4. development and validation use the same core workflow shell while  
   preserving role separation  
5. all SDKs expose consistent deterministic interfaces suitable for  
   skills and agents  
6. artifacts, logs, reviews, selections, and findings remain linked  
   coherently across the platform  
  
====================================================================  
END OF SDK CATALOG  
====================================================================  
