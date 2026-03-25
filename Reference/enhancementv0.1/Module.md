# Module  
  
====================================================================  
SDK MASTER REFERENCE TABLE  
ENTERPRISE AGENTIC AI MODEL LIFECYCLE PLATFORM  
====================================================================  
  
NOTE  
--------------------------------------------------------------------  
Columns:  
- SDK  
- Description  
- Modules  
- Module Usage  
- Dependencies  
- Related Agent(s)  
  
"Related Agent(s)" means the main agents or virtual sub-agents that  
will most commonly invoke or rely on that SDK.  
  
====================================================================  
1) CORE / FOUNDATION / SHARED CONTROL SDKS  
====================================================================  
  
| SDK | Description | Modules | Module Usage | Dependencies | Related Agent(s) |  
|---|---|---|---|---|---|  
| config_sdk | Central config management SDK for loading, validating, versioning, and resolving environment-aware configuration. | config_loader; config_schema_validator; config_versioning; config_resolver; environment_overlay; config_diff; config_registry_link | config_loader: load YAML/JSON/config objects; config_schema_validator: validate config structure; config_versioning: track config versions; config_resolver: resolve effective config; environment_overlay: apply environment-specific overrides; config_diff: compare config versions; config_registry_link: link config to registry IDs | None | model-lifecycle-orchestrator; developer-agent; validator-agent; governance-agent; monitoring-agent; documentation-agent |  
| registry_sdk | Shared metadata and lookup SDK for projects, runs, skills, policies, datasets, models, and validation objects. | project_registry; run_registry; skill_registry; sdk_registry; policy_registry; validation_registry; lookup_api; search_api | project_registry: store/fetch project metadata; run_registry: manage runs/sessions; skill_registry: skill metadata and versions; sdk_registry: SDK metadata; policy_registry: policy lookups; validation_registry: validation object lookups; lookup_api: exact ID lookup; search_api: metadata search | config_sdk | model-lifecycle-orchestrator; session-bootstrap-orchestrator; recovery-orchestrator; all role agents |  
| observabilitysdk | Structured event logging and replay SDK for traceability, debugging, monitoring, and flow reconstruction. | event_writer; event_schema; replay_engine; lineage_builder; trace_manager; event_query; event_enrichment; event_router; event_store_adapter | event_writer: write events; event_schema: validate event payloads; replay_engine: replay run history; lineage_builder: reconstruct event lineage; trace_manager: manage trace/session IDs; event_query: retrieve events; event_enrichment: add metadata; event_router: route events to stores; event_store_adapter: storage abstraction | config_sdk; registry_sdk | model-lifecycle-orchestrator; interaction-orchestrator; recovery-orchestrator; monitoring-agent; validator-agent; governance-agent |  
| artifactsdk | Artifact lifecycle SDK for registering, locating, versioning, and linking artifacts to workflow objects. | artifact_registry; artifact_metadata; artifact_lineage; artifact_locator; artifact_validators; artifact_manifest; storage_adapter; checksum_manager; version_resolver | artifact_registry: register artifact records; artifact_metadata: maintain metadata; artifact_lineage: link source-to-output; artifact_locator: resolve paths/URIs; artifact_validators: validate artifact presence/schema; artifact_manifest: build manifests; storage_adapter: read/write abstraction; checksum_manager: integrity checks; version_resolver: resolve artifact versions | config_sdk; registry_sdk | developer-agent; validator-agent; governance-agent; documentation-agent; monitoring-agent |  
| auditsdk | Formal audit SDK for approvals, overrides, exceptions, decisions, and sign-off records. | audit_writer; decision_registry; approval_registry; exception_registry; audit_export; audit_views; signoff_registry; conditional_approval_manager | audit_writer: persist audit records; decision_registry: store decisions; approval_registry: store approvals; exception_registry: manage exceptions; audit_export: export audit package; audit_views: build audit views; signoff_registry: track sign-off objects; conditional_approval_manager: manage conditions attached to approvals | observabilitysdk; artifactsdk; registry_sdk | governance-agent; approver-agent; validator-agent; model-lifecycle-orchestrator |  
| workflowsdk | Workflow control SDK for lifecycle routing, stage transitions, checkpointing, selection enforcement, resume, and recovery. | project_bootstrap; workflow_state; routing_engine; stage_registry; checkpoint_manager; session_manager; recovery_manager; candidate_registry; selection_registry; dependency_manager; state_persistence; transition_guard | project_bootstrap: initialize project/run; workflow_state: central state model; routing_engine: determine next stage; stage_registry: manage stage definitions; checkpoint_manager: save checkpoints; session_manager: manage session context; recovery_manager: recovery paths; candidate_registry: candidate version records; selection_registry: final selected version records; dependency_manager: prerequisite checks; state_persistence: durable state writes; transition_guard: block invalid transitions | config_sdk; registry_sdk; observabilitysdk; auditsdk; artifactsdk | model-lifecycle-orchestrator; session-bootstrap-orchestrator; recovery-orchestrator; all role agents indirectly |  
| hitlsdk | Human-in-the-loop control SDK for review creation, bounded actions, approvals, edits, and escalation. | review_payloads; review_registry; approval_manager; override_manager; reviewer_assignment; action_validation; escalation_manager; review_status_machine; decision_capture; review_templates | review_payloads: build review payloads; review_registry: persist reviews; approval_manager: handle approvals; override_manager: track overrides; reviewer_assignment: assign reviewers; action_validation: validate allowed actions; escalation_manager: escalate reviews; review_status_machine: review lifecycle; decision_capture: capture final action; review_templates: standard review shells | workflowsdk; observabilitysdk; auditsdk; widgetsdk; policysdk | developer-agent; validator-agent; governance-agent; reviewer-agent; approver-agent |  
| dataset_sdk | Dataset metadata and lineage SDK for dataset snapshots, splits, contracts, and reproducibility references. | dataset_registry; snapshot_manager; split_manager; sample_reference; lineage_reference; dataset_contract_validator | dataset_registry: register dataset objects; snapshot_manager: manage dataset snapshots; split_manager: record train/test/oot; sample_reference: sample-level metadata; lineage_reference: lineage linkage; dataset_contract_validator: validate dataset schema/contract | config_sdk; registry_sdk; artifactsdk | dataprepsdk; validationsdk; scorecardsdk; timeseriessdk; eclsdk; monitoringsdk |  
  
====================================================================  
2) ANALYTICAL / MODEL SUPPORT SDKS  
====================================================================  
  
| SDK | Description | Modules | Module Usage | Dependencies | Related Agent(s) |  
|---|---|---|---|---|---|  
| dq_sdk | Shared data quality SDK for source and model data checks. | schema_checks; missingness_checks; consistency_checks; distribution_profile; business_rule_checks; dq_summary; dq_exception_builder | schema_checks: validate required columns/types; missingness_checks: null analysis; consistency_checks: logical integrity checks; distribution_profile: summary stats and distributions; business_rule_checks: domain-specific DQ rules; dq_summary: compact DQ output; dq_exception_builder: structured DQ exceptions | config_sdk; registry_sdk; artifactsdk; observabilitysdk | developer-agent; validator-agent; monitoring-agent; model-lifecycle-orchestrator |  
| feature_sdk | Shared feature engineering SDK for reusable transformation and feature lineage. | transformation_engine; lag_engine; differencing_engine; grouping_engine; encoding_helpers; feature_metadata; feature_lineage | transformation_engine: core transforms; lag_engine: lag features; differencing_engine: differenced features; grouping_engine: grouped aggregates; encoding_helpers: controlled encoding; feature_metadata: feature catalog; feature_lineage: source-to-feature lineage | config_sdk; registry_sdk; artifactsdk; observabilitysdk | developer-agent; scorecard-domain; timeseries-domain; ecl-domain; lgd-domain |  
| evaluation_sdk | Shared evaluation SDK for metrics, diagnostics, thresholds, and comparison. | metric_engine; diagnostic_engine; stability_checks; calibration_checks; comparison_framework; threshold_evaluator; benchmark_compare | metric_engine: compute KPIs; diagnostic_engine: diagnostic tests; stability_checks: drift/stability; calibration_checks: calibration metrics; comparison_framework: compare candidates; threshold_evaluator: pass/warn/breach; benchmark_compare: benchmark vs prior or standard | config_sdk; registry_sdk; artifactsdk; observabilitysdk | developer-agent; validator-agent; monitoring-agent; governance-agent |  
| reporting_sdk | Shared reporting SDK for technical packs, committee packs, summaries, and narratives. | technical_report_builder; executive_summary_builder; committee_pack_builder; validation_note_builder; narrative_blocks; chart_table_export; pack_assembler | technical_report_builder: technical docs; executive_summary_builder: exec summary; committee_pack_builder: governance pack; validation_note_builder: validation notes; narrative_blocks: reusable wording; chart_table_export: export figures/tables; pack_assembler: final report/package assembly | config_sdk; registry_sdk; artifactsdk; auditsdk; flowvizsdk | documentation-agent; governance-agent; validator-agent; monitoring-agent |  
  
====================================================================  
3) DATA ENGINEERING / PREPARATION / MONITORING SDKS  
====================================================================  
  
| SDK | Description | Modules | Module Usage | Dependencies | Related Agent(s) |  
|---|---|---|---|---|---|  
| dataprepsdk | Spark-first data preparation SDK for governed training-data construction using approved templates and config-driven lineage. | template_registry; template_executor; source_reader; lineage_resolver; grain_manager; entity_mapper; time_aligner; target_builder; feature_aligner; split_builder; sample_builder; quality_checker; metadata_builder; lineage_builder; output_writer; manifest_builder; leakage_checker; config_validator; spark_session_manager; spark_source_reader; spark_lineage_resolver; spark_grain_manager; spark_entity_mapper; spark_time_aligner; spark_target_builder; spark_feature_aligner; spark_panel_constructor; spark_cohort_builder; spark_spell_builder; spark_split_builder; spark_quality_checker; spark_output_writer; spark_manifest_builder | template_registry: approved prep templates; template_executor: run selected template; source_reader/spark_source_reader: read sources; lineage_resolver/spark_lineage_resolver: resolve joins and lineage; grain_manager/spark_grain_manager: grain control; entity_mapper/spark_entity_mapper: entity mapping; time_aligner/spark_time_aligner: date alignment; target_builder/spark_target_builder: target generation; feature_aligner/spark_feature_aligner: merge features; split_builder/spark_split_builder: train/test/oot; sample_builder/spark_panel_constructor/spark_cohort_builder/spark_spell_builder: construct panel/cohort/spell; quality_checker/spark_quality_checker: prep checks; metadata_builder/manifest_builder/spark_manifest_builder: metadata and lineage output; output_writer/spark_output_writer: dataset write; leakage_checker: future leakage checks; config_validator: config validation; spark_session_manager: Spark context control | config_sdk; registry_sdk; dataset_sdk; artifactsdk; observabilitysdk; dq_sdk | developer-agent; model-lifecycle-orchestrator; validator-agent |  
| monitoringsdk | Post-validation monitoring SDK for snapshot ingestion, metrics, breaches, history, and dashboard payloads. | monitoring_template_registry; snapshot_ingestor; snapshot_validator; monitoring_history_manager; metric_engine; threshold_engine; drift_engine; performance_monitor; segment_monitor; baseline_comparator; dashboard_payload_builder; dashboard_config_builder; monitoring_note_manager; annual_review_pack_builder; monitoring_manifest_builder; monitoring_output_writer | monitoring_template_registry: monitoring templates; snapshot_ingestor: ingest new snapshot; snapshot_validator: validate schema/grain; monitoring_history_manager: append history; metric_engine: compute monitoring metrics; threshold_engine: evaluate thresholds; drift_engine: population/feature drift; performance_monitor: performance metrics; segment_monitor: segment view; baseline_comparator: compare to baseline; dashboard_payload_builder: dashboard data; dashboard_config_builder: dashboard config; monitoring_note_manager: notes/actions; annual_review_pack_builder: annual review outputs; monitoring_manifest_builder: metadata; monitoring_output_writer: persist outputs | config_sdk; registry_sdk; artifactsdk; observabilitysdk; auditsdk; evaluation_sdk; reporting_sdk; validationsdk | monitoring-agent; governance-agent; validator-agent; annual-review-outcome skill |  
  
====================================================================  
4) DOMAIN MODELING SDKS  
====================================================================  
  
| SDK | Description | Modules | Module Usage | Dependencies | Related Agent(s) |  
|---|---|---|---|---|---|  
| scorecardsdk | Domain SDK for scorecard modeling workflows including binning, WoE/IV, scaling, and score bands. | fine_classing; coarse_classing; binning_compare; woe_iv; feature_shortlist; logistic_models; score_scaling; score_bands; scorecard_outputs; scorecard_monitoring_support | fine_classing: fine bin setup; coarse_classing: coarse bin proposals/finalization; binning_compare: compare binning candidates; woe_iv: WoE/IV calculations; feature_shortlist: shortlist variables; logistic_models: model fit; score_scaling: convert odds to score; score_bands: define bands; scorecard_outputs: package outputs; scorecard_monitoring_support: scorecard monitoring metrics support | dataprepsdk; feature_sdk; evaluation_sdk; artifactsdk; observabilitysdk | developer-agent; validator-agent; monitoring-agent; scorecard-domain |  
| timeseriessdk | Domain SDK for time-series model preparation, diagnostics, and forecast support. | stationarity; transformations; lag_engine; model_fit; forecast_compare; residual_diagnostics; scenario_projection; timeseries_outputs | stationarity: unit root/stationarity tests; transformations: time-series transforms; lag_engine: lagged variables; model_fit: fit time-series models; forecast_compare: compare forecasts; residual_diagnostics: residual tests; scenario_projection: scenario-based projection; timeseries_outputs: package outputs | dataprepsdk; feature_sdk; evaluation_sdk; artifactsdk; observabilitysdk | developer-agent; validator-agent; monitoring-agent; timeseries-domain |  
| lgdsdk | Domain SDK for LGD workflows such as cure/severity and downturn/forward-looking adjustments. | cure_model; severity_model; downturn_adjustment; fl_adjustment; recovery_aggregation; lgd_outputs | cure_model: cure probability logic; severity_model: loss severity logic; downturn_adjustment: downturn LGD; fl_adjustment: forward-looking adjustment; recovery_aggregation: aggregate recoveries; lgd_outputs: package LGD outputs | dataprepsdk; feature_sdk; evaluation_sdk; artifactsdk; observabilitysdk | developer-agent; validator-agent; lgd-domain |  
| pdsdk | Domain SDK for PD workflows including calibration and term structure. | rating_pd; score_pd; term_structure; transition_logic; calibration_support; pd_monitoring | rating_pd: rating-based PD logic; score_pd: score-based PD logic; term_structure: lifetime/term PD; transition_logic: migrations/transitions; calibration_support: calibration routines; pd_monitoring: PD monitoring outputs | dataprepsdk; feature_sdk; evaluation_sdk; artifactsdk; observabilitysdk | developer-agent; validator-agent; monitoring-agent; pd-domain |  
| eadsdk | Domain SDK for EAD workflows including exposure/utilization logic. | exposure_estimation; ccf_support; utilization_modeling; ead_monitoring; ead_outputs | exposure_estimation: EAD estimation; ccf_support: conversion factor logic; utilization_modeling: usage/utilization behavior; ead_monitoring: monitoring outputs; ead_outputs: package outputs | dataprepsdk; feature_sdk; evaluation_sdk; artifactsdk; observabilitysdk | developer-agent; validator-agent; monitoring-agent; ead-domain |  
| sicr_sdk | Domain SDK for SICR workflows, rule-based and model-based. | sicr_rules; sicr_thresholds; sicr_model_compare; migration_tracking; sicr_outputs | sicr_rules: rule-based SICR logic; sicr_thresholds: threshold controls; sicr_model_compare: compare SICR methods; migration_tracking: stage migrations; sicr_outputs: package SICR outputs | dataprepsdk; feature_sdk; evaluation_sdk; artifactsdk; observabilitysdk | developer-agent; validator-agent; monitoring-agent; sicr-domain |  
| eclsdk | Domain SDK for ECL workflows coordinating staging, MEV, scenario, overlay, and ECL outputs. | staging; pd_inputs; lgd_inputs; ead_inputs; mev_engine; scenario_engine; overlay_engine; ecl_outputs | staging: stage assignment; pd_inputs/lgd_inputs/ead_inputs: assemble model inputs; mev_engine: macro alignment; scenario_engine: scenario weighting/projection; overlay_engine: overlays; ecl_outputs: final ECL outputs | dataprepsdk; feature_sdk; evaluation_sdk; artifactsdk; observabilitysdk; pdsdk; lgdsdk; eadsdk | developer-agent; validator-agent; monitoring-agent; ecl-domain |  
| stresssdk | Domain SDK for stress testing workflows and stressed aggregation. | scenario_application; macro_linkages; stressed_projection; result_aggregation; stress_outputs | scenario_application: apply stress scenarios; macro_linkages: macro transmission; stressed_projection: stressed metric projection; result_aggregation: aggregate stressed outputs; stress_outputs: package outputs | dataprepsdk; feature_sdk; evaluation_sdk; artifactsdk; observabilitysdk | developer-agent; validator-agent; monitoring-agent; stress-domain |  
  
====================================================================  
5) VALIDATION / KNOWLEDGE / RAG / VISUALIZATION SDKS  
====================================================================  
  
| SDK | Description | Modules | Module Usage | Dependencies | Related Agent(s) |  
|---|---|---|---|---|---|  
| validationsdk | Dedicated validation workflow SDK for findings, model fitness, conclusion, and remediation tracking. | validation_scope; evidence_intake; fitness_framework; finding_registry; issue_severity; conclusion_engine; remediation_tracker; validation_outputs; benchmark_compare; evidence_completeness | validation_scope: validation scope config; evidence_intake: intake and classify evidence; fitness_framework: model fitness dimensions; finding_registry: persist findings; issue_severity: severity logic; conclusion_engine: conclusion options; remediation_tracker: remediation actions and closure; validation_outputs: package outputs; benchmark_compare: compare to precedent/benchmark; evidence_completeness: detect missing evidence | workflowsdk; hitlsdk; observabilitysdk; auditsdk; artifactsdk; policysdk; evaluation_sdk; reporting_sdk | validator-agent; governance-agent; model-fitness-review skill; validation-conclusion skill |  
| knowledge_sdk | Knowledge governance SDK for managing knowledge objects, promotion, quality, and lifecycle. | knowledge_object; knowledge_registry; promotion_manager; quality_manager; status_manager; knowledge_linker; knowledge_export | knowledge_object: standard object model; knowledge_registry: store metadata; promotion_manager: promote scope upward; quality_manager: quality review states; status_manager: active/superseded/archived; knowledge_linker: link to artifacts/findings/decisions; knowledge_export: export knowledge packages | config_sdk; registry_sdk; artifactsdk; observabilitysdk | documentation-agent; validator-agent; monitoring-agent; governance-agent; evidence-gap-detector |  
| rag_sdk | Retrieval SDK for chunking, embeddings, semantic search, reranking, compression, and prompt packaging. | chunker; embedder; retriever; reranker; query_router; context_compressor; prompt_packager; token_budget_manager | chunker: split text into retrievable units; embedder: generate embeddings; retriever: semantic retrieval; reranker: rerank results; query_router: route query strategy by role/stage; context_compressor: compress retrieved context; prompt_packager: build compact context packs; token_budget_manager: enforce token thrift | knowledge_sdk; config_sdk; registry_sdk | all role agents indirectly; model-lifecycle-orchestrator; documentation-agent; validator-agent |  
| flowvizsdk | Visualization SDK to convert event and workflow state into flow and timeline representations. | node_builder; edge_builder; flow_summary; timeline_builder; graph_export; detail_linker; flow_filters; drilldown_router | node_builder: build flow nodes; edge_builder: build edges; flow_summary: summarize workflow path; timeline_builder: build time sequence; graph_export: export graph payloads; detail_linker: link nodes to details; flow_filters: filtered views; drilldown_router: route UI drill-down | observabilitysdk; auditsdk; artifactsdk; registry_sdk | documentation-agent; governance-agent; monitoring-agent; flow-summary-narrator |  
  
====================================================================  
6) INTEGRATION / DELIVERY / BRIDGE SDKS  
====================================================================  
  
| SDK | Description | Modules | Module Usage | Dependencies | Related Agent(s) |  
|---|---|---|---|---|---|  
| agent_bridge | Controlled adapter between agents/skills and SDK calls. | tool_adapter; skill_adapter; agent_context_builder; response_normalizer; retry_policy | tool_adapter: invoke SDKs as tools; skill_adapter: connect skill stack to calls; agent_context_builder: build compact agent context; response_normalizer: standardize outputs; retry_policy: controlled retries | workflowsdk; hitlsdk; observabilitysdk; auditsdk; artifactsdk; registry_sdk | all agents |  
| jupyter_bridge | Bridge between JupyterLab UI/workspaces/controllers and backend SDKs. | widget_controller; notebook_state_sync; action_dispatch; result_refresh | widget_controller: bind widgets to handlers; notebook_state_sync: sync UI state; action_dispatch: dispatch user actions; result_refresh: refresh UI after backend result | workflowsdk; hitlsdk; artifactsdk; observabilitysdk; widgetsdk | developer-agent; validator-agent; governance-agent; monitoring-agent |  
| api_bridge | API exposure layer for SDK capabilities. | rest_adapter; request_mapper; response_mapper; auth_hooks; error_mapper | rest_adapter: API endpoint adapter; request_mapper: map inbound requests; response_mapper: normalize outbound responses; auth_hooks: auth integration; error_mapper: standardize errors | registry_sdk; config_sdk; workflowsdk; agent_bridge | external orchestrators; service-mode agents |  
| cli_bridge | CLI exposure layer for SDK capabilities. | command_router; argument_parser; output_formatter | command_router: map CLI commands; argument_parser: parse args; output_formatter: format terminal output | registry_sdk; config_sdk; workflowsdk; agent_bridge | power users; automation scripts; developer-agent indirectly |  
| mcp_bridge | Future MCP-compatible tool exposure layer. | mcp_tool_registry; mcp_request_mapper; mcp_response_mapper | mcp_tool_registry: expose tools to MCP; mcp_request_mapper: map MCP requests; mcp_response_mapper: map responses back | registry_sdk; config_sdk; agent_bridge; api_bridge | future external agent runtimes |  
  
====================================================================  
7) POLICY / UI SUPPORT SDKS  
====================================================================  
  
| SDK | Description | Modules | Module Usage | Dependencies | Related Agent(s) |  
|---|---|---|---|---|---|  
| policysdk | Policy enforcement SDK for threshold rules, breaches, waivers, approvals, and control matrices. | policy_loader; threshold_engine; breach_detector; waiver_rules; control_matrix; rule_evaluator; approval_rules; escalation_rules | policy_loader: load policies; threshold_engine: evaluate thresholds; breach_detector: detect breach/warning; waiver_rules: rule exceptions; control_matrix: map controls; rule_evaluator: generic rule application; approval_rules: approval gates; escalation_rules: escalation logic | config_sdk; registry_sdk; observabilitysdk; auditsdk | governance-agent; validator-agent; monitoring-agent; model-lifecycle-orchestrator |  
| widgetsdk | Reusable Jupyter widget UI SDK for HITL, review, selection, validation, and flow panels. | review_shell; selection_cards; bootstrap_cards; recovery_cards; flow_panels; detail_panels; validation_cards; evidence_panels; comment_capture; action_bar | review_shell: standard review UI; selection_cards: candidate selection; bootstrap_cards: project bootstrap; recovery_cards: recovery UI; flow_panels: flow views; detail_panels: detail display; validation_cards: validation review widgets; evidence_panels: evidence display; comment_capture: rationale input; action_bar: bounded actions | jupyter_bridge; workflowsdk; hitlsdk; flowvizsdk | developer-agent; validator-agent; reviewer-agent; approver-agent |  
  
====================================================================  
8) DEPENDENCY / AGENT NOTES  
====================================================================  
  
COMMON DEPENDENCY BASE  
--------------------------------------------------------------------  
Most SDKs ultimately rely on:  
- config_sdk  
- registry_sdk  
- observabilitysdk  
- artifactsdk  
  
COMMON RELATED AGENT GROUPS  
--------------------------------------------------------------------  
Primary agent families:  
- model-lifecycle-orchestrator  
- session-bootstrap-orchestrator  
- recovery-orchestrator  
- developer-agent  
- validator-agent  
- governance-agent  
- reviewer-agent  
- approver-agent  
- documentation-agent  
- monitoring-agent  
- remediation-agent  
  
====================================================================  
END OF SDK MASTER REFERENCE TABLE  
====================================================================  
  
====================================================================  
SDK MODULE DEPENDENCY MATRIX  
CSV / JIRA-STYLE REFERENCE  
ENTERPRISE AGENTIC AI MODEL LIFECYCLE PLATFORM  
====================================================================  
  
COLUMNS  
--------------------------------------------------------------------  
SDK,Module,Module Purpose,Primary Usage,Depends On,Related Agent(s),Priority,Phase  
  
====================================================================  
CORE / FOUNDATION / SHARED CONTROL SDKS  
====================================================================  
  
SDK,Module,Module Purpose,Primary Usage,Depends On,Related Agent(s),Priority,Phase  
config_sdk,config_loader,Load config files and config objects,Load YAML JSON and structured config inputs,None,model-lifecycle-orchestrator; developer-agent; validator-agent,Critical,Phase 1  
config_sdk,config_schema_validator,Validate config structure and required fields,Check config before execution,config_loader,model-lifecycle-orchestrator; developer-agent; validator-agent,Critical,Phase 1  
config_sdk,config_versioning,Track config versions and hashes,Ensure reproducibility and config lineage,config_loader,model-lifecycle-orchestrator; auditsdk,Critical,Phase 1  
config_sdk,config_resolver,Resolve effective config from layered settings,Build runtime-effective configuration,config_loader; config_schema_validator,model-lifecycle-orchestrator,Critical,Phase 1  
config_sdk,environment_overlay,Apply environment-specific overrides,Support CML/dev/test/prod behavior,config_resolver,model-lifecycle-orchestrator; api_bridge,High,Phase 1  
config_sdk,config_diff,Compare two config versions,Support audit and validation review,config_loader; config_versioning,validator-agent; governance-agent,High,Phase 2  
config_sdk,config_registry_link,Link config to registry metadata,Register config refs against project/run IDs,config_versioning; registry_sdk,model-lifecycle-orchestrator; auditsdk,High,Phase 2  
  
registry_sdk,project_registry,Store and query project metadata,Resolve project context and ownership,config_sdk,model-lifecycle-orchestrator; session-bootstrap-orchestrator,Critical,Phase 1  
registry_sdk,run_registry,Store and query run metadata,Resolve active run state,config_sdk,model-lifecycle-orchestrator; recovery-orchestrator,Critical,Phase 1  
registry_sdk,skill_registry,Store skill metadata and versions,Resolve skill stack versions,config_sdk,model-lifecycle-orchestrator; agent_bridge,High,Phase 2  
registry_sdk,sdk_registry,Store SDK metadata and versions,Resolve available SDKs and versions,config_sdk,model-lifecycle-orchestrator; api_bridge,High,Phase 2  
registry_sdk,policy_registry,Store policy pack metadata,Resolve policy pack references,config_sdk,policysdk; governance-agent,High,Phase 2  
registry_sdk,validation_registry,Store validation object metadata,Resolve validation findings and conclusions,config_sdk,validationsdk; validator-agent,High,Phase 2  
registry_sdk,lookup_api,Provide exact ID-based lookup,Fetch exact registry objects quickly,project_registry; run_registry,all agents,Critical,Phase 1  
registry_sdk,search_api,Provide filtered metadata search,Search projects runs artifacts findings by filters,lookup_api,all agents,High,Phase 2  
  
observabilitysdk,event_writer,Write structured events,Record stage action review and system events,config_sdk; registry_sdk,all agents; model-lifecycle-orchestrator,Critical,Phase 1  
observabilitysdk,event_schema,Validate event payloads,Ensure event structure consistency,config_sdk,observabilitysdk internal,Critical,Phase 1  
observabilitysdk,replay_engine,Replay workflow events,Support recovery and trace reconstruction,event_writer; event_query,recovery-orchestrator; model-lifecycle-orchestrator,High,Phase 2  
observabilitysdk,lineage_builder,Build event lineage chains,Trace parent-child event relationships,event_writer; trace_manager,flowvizsdk; auditsdk,High,Phase 2  
observabilitysdk,trace_manager,Manage trace IDs and session IDs,Correlate all events in one run/session,config_sdk,all agents,Critical,Phase 1  
observabilitysdk,event_query,Query stored events,Load events for flow and audit,event_store_adapter,flowvizsdk; auditsdk; recovery-orchestrator,High,Phase 2  
observabilitysdk,event_enrichment,Add metadata to events,Attach project role stage and refs,event_writer; registry_sdk,all agents,High,Phase 2  
observabilitysdk,event_router,Route events to storage targets,Support multiple sinks if needed,event_writer; event_store_adapter,observabilitysdk internal,High,Phase 2  
observabilitysdk,event_store_adapter,Abstract event storage backend,Support file/db/object storage for events,config_sdk,observabilitysdk internal,Critical,Phase 1  
  
artifactsdk,artifact_registry,Register artifact records,Track all material artifacts,config_sdk; registry_sdk,developer-agent; validator-agent,Critical,Phase 1  
artifactsdk,artifact_metadata,Store artifact metadata,Keep schema version producer type and tags,artifact_registry,all agents,Critical,Phase 1  
artifactsdk,artifact_lineage,Track artifact lineage,Link source and derived artifacts,artifact_registry,validator-agent; documentation-agent,High,Phase 1  
artifactsdk,artifact_locator,Resolve artifact paths and URIs,Find artifact for read/view/use,artifact_registry,all agents,Critical,Phase 1  
artifactsdk,artifact_validators,Validate artifact existence and integrity,Check artifact before downstream use,artifact_registry; checksum_manager,model-lifecycle-orchestrator; validationsdk,High,Phase 2  
artifactsdk,artifact_manifest,Build artifact manifests,Create compact artifact package summaries,artifact_registry; artifact_metadata,reporting_sdk; governance-agent,High,Phase 2  
artifactsdk,storage_adapter,Read/write artifact payloads,Abstract S3/local/object interactions,config_sdk,all SDKs,Critical,Phase 1  
artifactsdk,checksum_manager,Create and validate checksums,Support integrity and reproducibility,storage_adapter,artifactsdk internal,High,Phase 2  
artifactsdk,version_resolver,Resolve artifact versions,Select correct artifact version by policy,artifact_registry,model-lifecycle-orchestrator; validator-agent,High,Phase 2  
  
auditsdk,audit_writer,Write audit records,Record governed decisions and approvals,observabilitysdk; artifactsdk; registry_sdk,governance-agent; validator-agent,Critical,Phase 1  
auditsdk,decision_registry,Store decision records,Persist explicit decisions,audit_writer,model-lifecycle-orchestrator; governance-agent,Critical,Phase 1  
auditsdk,approval_registry,Store approval records,Persist approvals and conditions,audit_writer,approver-agent; governance-agent,Critical,Phase 1  
auditsdk,exception_registry,Store exceptions and waivers,Track unresolved and waived issues,audit_writer,governance-agent; validator-agent,High,Phase 2  
auditsdk,audit_export,Export audit bundles,Prepare audit-ready package,audit_writer; artifactsdk,documentation-agent; governance-agent,High,Phase 2  
auditsdk,audit_views,Generate audit views,Show summarized audit information,audit_writer; decision_registry,governance-agent; auditor role,High,Phase 2  
auditsdk,signoff_registry,Store sign-off records,Track final sign-off state,approval_registry,approver-agent; validator-agent,High,Phase 2  
auditsdk,conditional_approval_manager,Manage approval conditions,Track conditions and closure rules,approval_registry; exception_registry,governance-agent; remediation-agent,High,Phase 2  
  
workflowsdk,project_bootstrap,Initialize project and first run,Create starting workflow objects,config_sdk; registry_sdk,session-bootstrap-orchestrator,Critical,Phase 1  
workflowsdk,workflow_state,Maintain workflow state model,Hold current stage status and refs,config_sdk; registry_sdk,model-lifecycle-orchestrator,Critical,Phase 1  
workflowsdk,routing_engine,Determine next workflow path,Route by status role stage and rules,workflow_state; stage_registry; policysdk,model-lifecycle-orchestrator,Critical,Phase 1  
workflowsdk,stage_registry,Store stage definitions and dependencies,Resolve stage-specific requirements,config_sdk; registry_sdk,model-lifecycle-orchestrator,Critical,Phase 1  
workflowsdk,checkpoint_manager,Save stable checkpoints,Enable recovery and resume,workflow_state; state_persistence,recovery-orchestrator,High,Phase 1  
workflowsdk,session_manager,Manage session lifecycle,Track active and resumed sessions,workflow_state; registry_sdk,session-bootstrap-orchestrator,Critical,Phase 1  
workflowsdk,recovery_manager,Manage recovery paths,Select safe resume/retry/rerun path,workflow_state; checkpoint_manager,recovery-orchestrator,High,Phase 1  
workflowsdk,candidate_registry,Store candidate versions,Track alternative outputs before selection,workflow_state; artifactsdk,developer-agent; validator-agent,Critical,Phase 1  
workflowsdk,selection_registry,Store explicit selected versions,Track final chosen candidate,candidate_registry; auditsdk,model-selection skill; governance-agent,Critical,Phase 1  
workflowsdk,dependency_manager,Validate prerequisites and dependencies,Block stages with unmet requirements,workflow_state; stage_registry,model-lifecycle-orchestrator,Critical,Phase 1  
workflowsdk,state_persistence,Durably persist workflow state,Save state across calls and sessions,workflow_state; registry_sdk,Critical,model-lifecycle-orchestrator,Phase 1  
workflowsdk,transition_guard,Block invalid transitions,Enforce control rules and selection rules,workflow_state; dependency_manager; policysdk,model-lifecycle-orchestrator,Critical,Phase 1  
  
hitlsdk,review_payloads,Build review payloads,Create structured review objects,workflowsdk; artifactsdk,developer-agent; validator-agent,Critical,Phase 1  
hitlsdk,review_registry,Store reviews,Track review lifecycle,workflowsdk; auditsdk,reviewer-agent; approver-agent,Critical,Phase 1  
hitlsdk,approval_manager,Manage approval actions,Handle approve/approve with conditions,review_registry; auditsdk,approver-agent; governance-agent,Critical,Phase 1  
hitlsdk,override_manager,Manage override actions,Record controlled deviations,review_registry; auditsdk,governance-agent; validator-agent,High,Phase 2  
hitlsdk,reviewer_assignment,Assign reviewers and roles,Route review to right actor,review_registry; registry_sdk,model-lifecycle-orchestrator; governance-agent,High,Phase 2  
hitlsdk,action_validation,Validate review actions,Ensure action is allowed and well-formed,review_payloads; policysdk,Critical,reviewer-agent; approver-agent,Phase 1  
hitlsdk,escalation_manager,Escalate reviews,Handle timeout or severity-driven escalation,review_registry; policysdk,governance-agent; recovery-orchestrator,High,Phase 2  
hitlsdk,review_status_machine,Manage review state changes,Control pending/in progress/finalized etc,review_registry,Critical,all review-related agents,Phase 1  
hitlsdk,decision_capture,Capture final review decision,Persist final review action,review_registry; auditsdk,Critical,reviewer-agent; approver-agent,Phase 1  
hitlsdk,review_templates,Store standard review shells,Reuse review patterns across domains,config_sdk; registry_sdk,widgetsdk; interaction-orchestrator,High,Phase 2  
  
dataset_sdk,dataset_registry,Register datasets and dataset IDs,Track datasets used in modeling and validation,config_sdk; registry_sdk; artifactsdk,dataprepsdk; validationsdk,Critical,Phase 1  
dataset_sdk,snapshot_manager,Manage dataset snapshots,Track versioned datasets over time,dataset_registry,dataprepsdk; monitoringsdk,Critical,Phase 1  
dataset_sdk,split_manager,Track dataset splits,Store dev/test/oot/holdout references,dataset_registry,dataprepsdk; validationsdk,Critical,Phase 1  
dataset_sdk,sample_reference,Store sample-level metadata,Document sample definitions and filters,dataset_registry,dataprepsdk; validator-agent,High,Phase 2  
dataset_sdk,lineage_reference,Store dataset lineage refs,Link prepared dataset to sources,dataset_registry; artifactsdk,dataprepsdk; validationsdk,Critical,Phase 1  
dataset_sdk,dataset_contract_validator,Validate dataset schema contracts,Ensure expected structure before use,dataset_registry; config_sdk,dataprepsdk; scorecardsdk; validationsdk,High,Phase 2  
  
====================================================================  
ANALYTICAL / MODEL SUPPORT SDKS  
====================================================================  
  
SDK,Module,Module Purpose,Primary Usage,Depends On,Related Agent(s),Priority,Phase  
dq_sdk,schema_checks,Validate schema and required fields,Check sources and prepared datasets,config_sdk; registry_sdk,developer-agent; validator-agent,Critical,Phase 1  
dq_sdk,missingness_checks,Profile null and missingness patterns,Assess data completeness,schema_checks,developer-agent; monitoring-agent,Critical,Phase 1  
dq_sdk,consistency_checks,Check logic and consistency rules,Validate business and structural logic,schema_checks; config_sdk,developer-agent; validator-agent,Critical,Phase 1  
dq_sdk,distribution_profile,Create distribution summaries,Support DQ and drift views,config_sdk; artifactsdk,developer-agent; monitoring-agent,High,Phase 1  
dq_sdk,business_rule_checks,Run domain-specific DQ rules,Check credit-risk-specific data constraints,config_sdk; registry_sdk,developer-agent; validator-agent,High,Phase 2  
dq_sdk,dq_summary,Build compact DQ summaries,Provide token-thrifty DQ output,missingness_checks; consistency_checks,developer-agent; validator-agent,Critical,Phase 1  
dq_sdk,dq_exception_builder,Create structured DQ exceptions,Support governed DQ review,dq_summary; hitlsdk,developer-agent; governance-agent,High,Phase 2  
  
feature_sdk,transformation_engine,Run standard feature transforms,Apply transformations and standard derivations,config_sdk; registry_sdk,developer-agent; scorecard-domain,Critical,Phase 1  
feature_sdk,lag_engine,Create lag features,Support panel and time-series prep,transformation_engine,developer-agent; timeseries-domain,High,Phase 1  
feature_sdk,differencing_engine,Create differenced features,Support stationarity-oriented prep,transformation_engine,developer-agent; timeseries-domain,High,Phase 2  
feature_sdk,grouping_engine,Aggregate/group features,Support hierarchy and segment features,transformation_engine,developer-agent; ecl-domain,High,Phase 1  
feature_sdk,encoding_helpers,Apply governed encodings,Handle category encoding and mapping,transformation_engine,developer-agent; scorecard-domain,High,Phase 2  
feature_sdk,feature_metadata,Store feature catalog info,Document feature definitions and tags,artifactsdk; registry_sdk,developer-agent; validator-agent,High,Phase 2  
feature_sdk,feature_lineage,Track feature lineage,Link feature to source and logic,feature_metadata; artifactsdk,validator-agent; documentation-agent,High,Phase 2  
  
evaluation_sdk,metric_engine,Compute evaluation metrics,Generate KPIs for candidates and monitoring,config_sdk; registry_sdk,developer-agent; monitoring-agent,Critical,Phase 1  
evaluation_sdk,diagnostic_engine,Run diagnostic tests,Generate model diagnostics,metric_engine,developer-agent; validator-agent,Critical,Phase 1  
evaluation_sdk,stability_checks,Run stability tests,Detect drift and stability issues,metric_engine,monitoring-agent; validator-agent,High,Phase 1  
evaluation_sdk,calibration_checks,Run calibration tests,Assess observed vs predicted alignment,metric_engine,developer-agent; validator-agent,High,Phase 1  
evaluation_sdk,comparison_framework,Compare alternatives,Support candidate/model comparisons,metric_engine; diagnostic_engine,developer-agent; governance-agent,Critical,Phase 1  
evaluation_sdk,threshold_evaluator,Classify metrics by threshold,Convert metric into pass/warn/breach,metric_engine; policysdk,monitoring-agent; governance-agent,High,Phase 2  
evaluation_sdk,benchmark_compare,Compare against benchmark/prior,Support precedent comparison,metric_engine; registry_sdk,validator-agent; monitoring-agent,High,Phase 2  
  
reporting_sdk,technical_report_builder,Build technical report content,Prepare model/validation technical sections,config_sdk; artifactsdk,documentation-agent; validator-agent,Critical,Phase 1  
reporting_sdk,executive_summary_builder,Build executive summary,Prepare concise management-level summaries,technical_report_builder,documentation-agent; governance-agent,High,Phase 1  
reporting_sdk,committee_pack_builder,Build committee pack content,Prepare approval/governance materials,technical_report_builder; auditsdk,documentation-agent; governance-agent,High,Phase 2  
reporting_sdk,validation_note_builder,Build validation note content,Prepare validation memos and notes,technical_report_builder; validationsdk,documentation-agent; validator-agent,High,Phase 2  
reporting_sdk,narrative_blocks,Manage reusable narrative snippets,Reuse approved wording and text blocks,config_sdk; registry_sdk,documentation-agent,Critical,Phase 1  
reporting_sdk,chart_table_export,Export charts and tables,Prepare document-ready figures and tables,artifactsdk; flowvizsdk,documentation-agent; monitoring-agent,High,Phase 2  
reporting_sdk,pack_assembler,Assemble final reporting pack,Combine sections into governed deliverable,technical_report_builder; executive_summary_builder; chart_table_export,documentation-agent; governance-agent,High,Phase 2  
  
====================================================================  
DATA ENGINEERING / PREPARATION / MONITORING SDKS  
====================================================================  
  
SDK,Module,Module Purpose,Primary Usage,Depends On,Related Agent(s),Priority,Phase  
dataprepsdk,template_registry,Register approved prep templates,Resolve governed preparation template,config_sdk; registry_sdk,developer-agent; model-lifecycle-orchestrator,Critical,Phase 1  
dataprepsdk,template_executor,Execute selected prep template,Run end-to-end data prep logic,template_registry; config_validator,Critical,developer-agent,Phase 1  
dataprepsdk,source_reader,Read source data logically,Ingest source references and metadata,config_sdk; dataset_sdk,developer-agent,High,Phase 1  
dataprepsdk,lineage_resolver,Resolve lineage mapping,Build join and dependency plan,config_sdk; registry_sdk,Critical,developer-agent; validator-agent,Phase 1  
dataprepsdk,grain_manager,Control target grain,Enforce cross-sectional/panel/time grain,lineage_resolver,Critical,developer-agent,Phase 1  
dataprepsdk,entity_mapper,Map entities and hierarchies,Map customer/account/contract relationships,grain_manager,developer-agent,High,Phase 1  
dataprepsdk,time_aligner,Align observation/reporting/target dates,Create time-consistent preparation output,grain_manager; config_sdk,Critical,developer-agent,Phase 1  
dataprepsdk,target_builder,Build target variables,Generate modeling target from rules,time_aligner; config_sdk,Critical,developer-agent; validator-agent,Phase 1  
dataprepsdk,feature_aligner,Align source features to target structure,Merge and align feature sets,time_aligner; feature_sdk,Critical,developer-agent,Phase 1  
dataprepsdk,split_builder,Build dataset splits,Create dev/test/oot/holdout assignments,target_builder; dataset_sdk,Critical,developer-agent; validator-agent,Phase 1  
dataprepsdk,sample_builder,Build final sample selection,Apply sample filters and retention logic,split_builder; target_builder,Critical,developer-agent,Phase 1  
dataprepsdk,quality_checker,Run prep-stage checks,Validate prep integrity,dq_sdk; sample_builder,Critical,developer-agent; validator-agent,Phase 1  
dataprepsdk,metadata_builder,Build dataset metadata,Create metadata for prepared dataset,sample_builder; dataset_sdk,documentation-agent; validator-agent,High,Phase 1  
dataprepsdk,lineage_builder,Build data lineage manifest,Document source-to-output lineage,lineage_resolver; artifactsdk,Critical,validator-agent; governance-agent,Phase 1  
dataprepsdk,output_writer,Write prepared outputs,Persist prepared dataset and side outputs,artifactsdk; dataset_sdk,Critical,developer-agent,Phase 1  
dataprepsdk,manifest_builder,Build prep manifests,Create summary manifest for reproducibility,metadata_builder; lineage_builder,Critical,validator-agent; governance-agent,Phase 1  
dataprepsdk,leakage_checker,Check target leakage,Detect future leakage issues,target_builder; time_aligner,Critical,developer-agent; validator-agent,Phase 2  
dataprepsdk,config_validator,Validate dataprep config,Check completeness and allowed template usage,config_sdk; template_registry,Critical,developer-agent,Phase 1  
dataprepsdk,spark_session_manager,Manage Spark session,Initialize and validate Spark context,config_sdk,Critical,developer-agent,Phase 1  
dataprepsdk,spark_source_reader,Read source data with Spark,Load S3/local datasets into Spark DataFrames,spark_session_manager; source_reader,Critical,developer-agent,Phase 1  
dataprepsdk,spark_lineage_resolver,Resolve lineage plan in Spark,Translate lineage plan into Spark operations,spark_source_reader; lineage_resolver,Critical,developer-agent,Phase 1  
dataprepsdk,spark_grain_manager,Manage dataset grain in Spark,Enforce one-row-per-grain as needed,spark_lineage_resolver; grain_manager,Critical,developer-agent,Phase 1  
dataprepsdk,spark_entity_mapper,Map hierarchical entities in Spark,Aggregate/match customer-account-contract relationships,spark_grain_manager; entity_mapper,High,developer-agent,Phase 1  
dataprepsdk,spark_time_aligner,Align time windows in Spark,Create observation and target windows,spark_grain_manager; time_aligner,Critical,developer-agent,Phase 1  
dataprepsdk,spark_target_builder,Build target columns in Spark,Generate labels using Spark logic,spark_time_aligner; target_builder,Critical,developer-agent,Phase 1  
dataprepsdk,spark_feature_aligner,Align features in Spark,Join and transform features at scale,spark_target_builder; feature_aligner,Critical,developer-agent,Phase 1  
dataprepsdk,spark_panel_constructor,Construct panel datasets in Spark,Build repeated observations per entity/time,spark_feature_aligner; sample_builder,Critical,developer-agent,Phase 1  
dataprepsdk,spark_cohort_builder,Construct cohort datasets in Spark,Build cohort-aligned datasets,spark_feature_aligner; sample_builder,High,developer-agent,Phase 2  
dataprepsdk,spark_spell_builder,Construct spell/event datasets in Spark,Build hazard/survival-ready panels,spark_feature_aligner; sample_builder,High,developer-agent,Phase 2  
dataprepsdk,spark_split_builder,Build splits in Spark,Assign split flags at scale,spark_target_builder; split_builder,Critical,developer-agent,Phase 1  
dataprepsdk,spark_quality_checker,Run quality checks in Spark,Compute scalable prep quality checks,spark_panel_constructor; quality_checker,Critical,developer-agent; validator-agent,Phase 1  
dataprepsdk,spark_output_writer,Write outputs from Spark,Persist final Spark DataFrames and summaries,spark_quality_checker; output_writer,Critical,developer-agent,Phase 1  
dataprepsdk,spark_manifest_builder,Build Spark execution manifest,Capture Spark-specific lineage and output summary,spark_output_writer; manifest_builder,High,validator-agent; governance-agent,Phase 1  
  
monitoringsdk,monitoring_template_registry,Register approved monitoring templates,Resolve monitoring template by model family,config_sdk; registry_sdk,monitoring-agent,Critical,Phase 2  
monitoringsdk,snapshot_ingestor,Ingest new monitoring snapshots,Load current monitoring period data,monitoring_template_registry; dataset_sdk,Critical,monitoring-agent,Phase 2  
monitoringsdk,snapshot_validator,Validate monitoring snapshot,Check schema grain and required fields,snapshot_ingestor; dq_sdk,Critical,monitoring-agent; validator-agent,Phase 2  
monitoringsdk,monitoring_history_manager,Manage monitoring time history,Append snapshot to monitoring series,snapshot_validator; dataset_sdk,Critical,monitoring-agent,Phase 2  
monitoringsdk,metric_engine,Compute monitoring metrics,Generate KPI tables from snapshots,monitoring_history_manager; evaluation_sdk,Critical,monitoring-agent,Phase 2  
monitoringsdk,threshold_engine,Apply monitoring thresholds,Classify pass/warn/breach,separate from generic policy if needed,metric_engine; policysdk,Critical,monitoring-agent; governance-agent,Phase 2  
monitoringsdk,drift_engine,Compute drift indicators,Track population/feature drift,monitoring_history_manager; evaluation_sdk,monitoring-agent,Critical,Phase 2  
monitoringsdk,performance_monitor,Compute performance metrics over time,Track Gini/KS/calibration etc,monitoring_history_manager; evaluation_sdk,Critical,monitoring-agent; validator-agent,Phase 2  
monitoringsdk,segment_monitor,Compute segment drill-downs,Show movement by segment/product/market,monitoring_history_manager; evaluation_sdk,monitoring-agent,High,Phase 2  
monitoringsdk,baseline_comparator,Compare current vs baseline,Compare to prior validation/deployment or prior period,metric_engine; registry_sdk,monitoring-agent; validator-agent,High,Phase 2  
monitoringsdk,dashboard_payload_builder,Build dashboard data payloads,Produce dashboard-ready data for UI,metric_engine; drift_engine; performance_monitor,Critical,monitoring-agent; jupyter_bridge,Phase 2  
monitoringsdk,dashboard_config_builder,Build dashboard config payloads,Define dashboard layout metadata,dashboard_payload_builder; config_sdk,monitoring-agent; widgetsdk,High,Phase 2  
monitoringsdk,monitoring_note_manager,Manage monitoring notes and actions,Store breach notes and action logs,artifactsdk; auditsdk,monitoring-agent; remediation-agent,High,Phase 2  
monitoringsdk,annual_review_pack_builder,Build annual review monitoring pack,Prepare annual monitoring summary,monitoring_history_manager; reporting_sdk,monitoring-agent; documentation-agent,High,Phase 2  
monitoringsdk,monitoring_manifest_builder,Build monitoring manifests,Document snapshot lineage and outputs,artifactsdk; registry_sdk,validator-agent; governance-agent,High,Phase 2  
monitoringsdk,monitoring_output_writer,Write monitoring artifacts,Persist dashboard payloads and tables,artifactsdk; storage_adapter,Critical,monitoring-agent,Phase 2  
  
====================================================================  
DOMAIN MODELING SDKS  
====================================================================  
  
SDK,Module,Module Purpose,Primary Usage,Depends On,Related Agent(s),Priority,Phase  
scorecardsdk,fine_classing,Manage fine bin setup,Prepare initial bins for variables,dataprepsdk; feature_sdk,developer-agent; scorecard-domain,Critical,Phase 1  
scorecardsdk,coarse_classing,Manage coarse bin proposals and validation,Create and validate merged bins,fine_classing; evaluation_sdk,Critical,developer-agent; validator-agent,Phase 1  
scorecardsdk,binning_compare,Compare binning candidates,Support candidate selection and HITL,coarse_classing; evaluation_sdk,Critical,developer-agent; governance-agent,Phase 1  
scorecardsdk,woe_iv,Compute WoE and IV,Support scorecard variable assessment,coarse_classing,Critical,developer-agent; validator-agent,Phase 1  
scorecardsdk,feature_shortlist,Build feature shortlist,Select variables for final model,woe_iv; evaluation_sdk,Critical,developer-agent,Phase 1  
scorecardsdk,logistic_models,Fit logistic scorecard models,Produce model candidates,feature_shortlist; evaluation_sdk,Critical,developer-agent,Phase 1  
scorecardsdk,score_scaling,Scale model outputs to score,Convert odds/logit to score,logistic_models,Critical,developer-agent; governance-agent,Phase 1  
scorecardsdk,score_bands,Create score bands,Group score outputs into bands,score_scaling,High,developer-agent; monitoring-agent,Phase 2  
scorecardsdk,scorecard_outputs,Package scorecard outputs,Write artifacts and summaries,artifactsdk; reporting_sdk,documentation-agent; governance-agent,High,Phase 1  
scorecardsdk,scorecard_monitoring_support,Provide scorecard-specific monitoring helpers,Support monitoring metrics for scorecards,monitoringsdk; score_bands,monitoring-agent,High,Phase 2  
  
timeseriessdk,stationarity,Run stationarity checks,Assess input time series suitability,dataprepsdk; evaluation_sdk,developer-agent; validator-agent,Medium,Phase 3  
timeseriessdk,transformations,Apply time-series transformations,Prepare transformed series,dataprepsdk; feature_sdk,developer-agent,Medium,Phase 3  
timeseriessdk,lag_engine,Create lags for time series,Build lagged feature structures,transformations; feature_sdk,developer-agent,Medium,Phase 3  
timeseriessdk,model_fit,Fit time-series models,Generate candidate time-series models,lag_engine; evaluation_sdk,developer-agent,Medium,Phase 3  
timeseriessdk,forecast_compare,Compare forecast candidates,Support forecast model selection,model_fit; evaluation_sdk,developer-agent; validator-agent,Medium,Phase 3  
timeseriessdk,residual_diagnostics,Run residual diagnostics,Check residual assumptions,model_fit; evaluation_sdk,developer-agent; validator-agent,Medium,Phase 3  
timeseriessdk,scenario_projection,Project scenarios through model,Create scenario outputs,model_fit; feature_sdk,developer-agent; governance-agent,Medium,Phase 3  
timeseriessdk,timeseries_outputs,Package time-series outputs,Write model outputs and diagnostics,artifactsdk; reporting_sdk,documentation-agent,Medium,Phase 3  
  
lgdsdk,cure_model,Support cure model workflow,Model cure probability or state,dataprepsdk; evaluation_sdk,developer-agent; validator-agent,Medium,Phase 3  
lgdsdk,severity_model,Support severity model workflow,Model severity conditional on event,dataprepsdk; evaluation_sdk,developer-agent; validator-agent,Medium,Phase 3  
lgdsdk,downturn_adjustment,Apply downturn LGD logic,Generate downturn-adjusted LGD,severity_model; policysdk,developer-agent; governance-agent,Medium,Phase 3  
lgdsdk,fl_adjustment,Apply forward-looking adjustment,Generate FL-adjusted LGD,downturn_adjustment; feature_sdk,developer-agent,Medium,Phase 3  
lgdsdk,recovery_aggregation,Aggregate recoveries and recoveries timeline,Build recovery-based features/targets,dataprepsdk; feature_sdk,developer-agent,Medium,Phase 3  
lgdsdk,lgd_outputs,Package LGD outputs,Write LGD artifacts and summaries,artifactsdk; reporting_sdk,documentation-agent,Medium,Phase 3  
  
pdsdk,rating_pd,Support rating-based PD logic,Model or map PD from rating structures,dataprepsdk; evaluation_sdk,developer-agent; validator-agent,Medium,Phase 3  
pdsdk,score_pd,Support score-based PD logic,Model or map PD from score structures,dataprepsdk; evaluation_sdk,developer-agent; validator-agent,Medium,Phase 3  
pdsdk,term_structure,Build PD term structure,Generate lifetime/term PD outputs,score_pd; rating_pd,developer-agent; validator-agent,Medium,Phase 3  
pdsdk,transition_logic,Model migrations and transitions,Support grade/state movement logic,term_structure; evaluation_sdk,developer-agent,Medium,Phase 3  
pdsdk,calibration_support,Support PD calibration,Calibrate observed and predicted PD,score_pd; evaluation_sdk,developer-agent; validator-agent,Medium,Phase 3  
pdsdk,pd_monitoring,Provide PD monitoring outputs,Support monitoring for PD models,monitoringsdk; evaluation_sdk,monitoring-agent,Medium,Phase 3  
  
eadsdk,exposure_estimation,Support EAD estimation,Estimate exposure measures,dataprepsdk; evaluation_sdk,developer-agent; validator-agent,Medium,Phase 3  
eadsdk,ccf_support,Support conversion factor logic,Estimate or apply CCF-related logic,exposure_estimation; evaluation_sdk,developer-agent,Medium,Phase 3  
eadsdk,utilization_modeling,Support utilization behavior modeling,Model balances/utilization,dataprepsdk; feature_sdk,developer-agent,Medium,Phase 3  
eadsdk,ead_monitoring,Provide EAD monitoring outputs,Support ongoing EAD monitoring,monitoringsdk; evaluation_sdk,monitoring-agent,Medium,Phase 3  
eadsdk,ead_outputs,Package EAD outputs,Write EAD artifacts and summaries,artifactsdk; reporting_sdk,documentation-agent,Medium,Phase 3  
  
sicr_sdk,sicr_rules,Support rule-based SICR logic,Apply predefined SICR rules,dataprepsdk; policysdk,developer-agent; validator-agent,Medium,Phase 3  
sicr_sdk,sicr_thresholds,Manage SICR thresholds,Evaluate threshold movement,sicr_rules; policysdk,developer-agent; validator-agent,Medium,Phase 3  
sicr_sdk,sicr_model_compare,Compare SICR methods,Compare rule/model variants,evaluation_sdk; sicr_rules,developer-agent; validator-agent,Medium,Phase 3  
sicr_sdk,migration_tracking,Track stage migrations,Monitor SICR stage movements,monitoringsdk; dataprepsdk,monitoring-agent,Medium,Phase 3  
sicr_sdk,sicr_outputs,Package SICR outputs,Write SICR artifacts and summaries,artifactsdk; reporting_sdk,documentation-agent,Medium,Phase 3  
  
eclsdk,staging,Support ECL stage assignment,Assign stage based on rules/models,dataprepsdk; sicr_sdk,developer-agent; validator-agent,Medium,Phase 3  
eclsdk,pd_inputs,Assemble PD inputs into ECL flow,Pull PD model outputs into ECL,pdsdk; dataprepsdk,developer-agent,Medium,Phase 3  
eclsdk,lgd_inputs,Assemble LGD inputs into ECL flow,Pull LGD outputs into ECL,lgdsdk; dataprepsdk,developer-agent,Medium,Phase 3  
eclsdk,ead_inputs,Assemble EAD inputs into ECL flow,Pull EAD outputs into ECL,eadsdk; dataprepsdk,developer-agent,Medium,Phase 3  
eclsdk,mev_engine,Handle macroeconomic variables for ECL,Align MEVs to ECL framework,feature_sdk; dataprepsdk,developer-agent; validator-agent,Medium,Phase 3  
eclsdk,scenario_engine,Support ECL scenarios,Apply scenario weighting and projections,mev_engine; evaluation_sdk,developer-agent; governance-agent,Medium,Phase 3  
eclsdk,overlay_engine,Support management overlays,Apply and document overlay logic,scenario_engine; policysdk,developer-agent; governance-agent,Medium,Phase 3  
eclsdk,ecl_outputs,Package ECL outputs,Write ECL artifacts and summaries,artifactsdk; reporting_sdk,documentation-agent,Medium,Phase 3  
  
stresssdk,scenario_application,Apply stress scenarios,Run stressed feature or model scenarios,dataprepsdk; feature_sdk,developer-agent,Medium,Phase 3  
stresssdk,macro_linkages,Support macro linkages,Connect macro variables to stress outputs,feature_sdk; evaluation_sdk,developer-agent; validator-agent,Medium,Phase 3  
stresssdk,stressed_projection,Generate stressed projections,Create stressed metrics/forecasts/scalars,scenario_application; macro_linkages,developer-agent; governance-agent,Medium,Phase 3  
stresssdk,result_aggregation,Aggregate stressed outputs,Roll stressed outputs to portfolio/report level,stressed_projection; artifactsdk,developer-agent; documentation-agent,Medium,Phase 3  
stresssdk,stress_outputs,Package stress outputs,Write stress artifacts and summaries,artifactsdk; reporting_sdk,documentation-agent,Medium,Phase 3  
  
====================================================================  
VALIDATION / KNOWLEDGE / RAG / FLOWVIZ SDKS  
====================================================================  
  
SDK,Module,Module Purpose,Primary Usage,Depends On,Related Agent(s),Priority,Phase  
validationsdk,validation_scope,Define validation scope,Initialize validation requirements and dimensions,config_sdk; workflowsdk,validator-agent,Critical,Phase 2  
validationsdk,evidence_intake,Collect and classify validation evidence,Organize evidence into classes,artifactsdk; registry_sdk,validator-agent,Critical,Phase 2  
validationsdk,fitness_framework,Manage model fitness dimensions,Evaluate soundness adequacy and limitations,evidence_intake; evaluation_sdk,validator-agent,Critical,Phase 2  
validationsdk,finding_registry,Store validation findings,Persist issue records and states,registry_sdk; auditsdk,validator-agent,Critical,Phase 2  
validationsdk,issue_severity,Classify finding severity,Set low/moderate/high/critical severity,finding_registry; policysdk,validator-agent; governance-agent,Critical,Phase 2  
validationsdk,conclusion_engine,Generate validation conclusion options,Support fit-for-use type conclusions,fitness_framework; finding_registry,Critical,validator-agent; approver-agent,Phase 2  
validationsdk,remediation_tracker,Track remediation actions and closure,Manage remediation lifecycle,finding_registry; auditsdk,remediation-agent; validator-agent,High,Phase 2  
validationsdk,validation_outputs,Package validation outputs,Write validation notes findings summaries,artifactsdk; reporting_sdk,documentation-agent; validator-agent,High,Phase 2  
validationsdk,benchmark_compare,Compare to prior validated patterns,Support precedent-based challenge,evaluation_sdk; knowledge_sdk,validator-agent,High,Phase 2  
validationsdk,evidence_completeness,Assess evidence sufficiency,Detect missing stale or insufficient evidence,evidence_intake; knowledge_sdk,Critical,validator-agent,Phase 2  
  
knowledge_sdk,knowledge_object,Define knowledge object structure,Standardize knowledge records,config_sdk,documentation-agent; validator-agent,High,Phase 2  
knowledge_sdk,knowledge_registry,Store knowledge metadata and refs,Track knowledge objects by scope and status,registry_sdk; artifactsdk,Critical,documentation-agent; validator-agent,Phase 2  
knowledge_sdk,promotion_manager,Promote knowledge across scopes,Move project knowledge to domain/global,knowledge_registry; quality_manager,High,governance-agent; documentation-agent,Phase 2  
knowledge_sdk,quality_manager,Manage quality status,Set draft/reviewed/approved/superseded,knowledge_registry,governance-agent; validator-agent,High,Phase 2  
knowledge_sdk,status_manager,Manage lifecycle status,Track active archived superseded state,knowledge_registry,Critical,knowledge_sdk internal,Phase 2  
knowledge_sdk,knowledge_linker,Link knowledge to source objects,Connect to artifacts findings decisions,artifactsdk; auditsdk; registry_sdk,Critical,documentation-agent; validator-agent,Phase 2  
knowledge_sdk,knowledge_export,Export governed knowledge packages,Prepare knowledge bundles for reuse,knowledge_registry; promotion_manager,High,documentation-agent; governance-agent,Phase 2  
  
rag_sdk,chunker,Split text into retrievable chunks,Prepare semantic retrieval units,knowledge_sdk; config_sdk,Critical,rag_sdk internal,Phase 2  
rag_sdk,embedder,Generate embeddings,Create vector representations,chunker; config_sdk,Critical,rag_sdk internal,Phase 2  
rag_sdk,retriever,Perform semantic retrieval,Find semantically relevant chunks,embedder; knowledge_sdk,Critical,all agents indirectly,Phase 2  
rag_sdk,reranker,Rerank retrieved results,Improve relevance ordering,retriever; query_router,Critical,all agents indirectly,Phase 2  
rag_sdk,query_router,Route retrieval strategy by role/domain/stage,Choose retrieval filters and mode,config_sdk; registry_sdk,Critical,model-lifecycle-orchestrator; all role agents,Phase 2  
rag_sdk,context_compressor,Compress retrieved context,Produce compact summaries for prompt pack,retriever; reranker,Critical,all agents indirectly,Phase 2  
rag_sdk,prompt_packager,Build final context pack for LLM,Assemble exact facts and summaries,context_compressor; registry_sdk,Critical,agent_bridge; all agents,Phase 2  
rag_sdk,token_budget_manager,Enforce token-thrifty retrieval,Limit retrieval and packing size,prompt_packager; config_sdk,Critical,agent_bridge; model-lifecycle-orchestrator,Phase 2  
  
flowvizsdk,node_builder,Build graph nodes from workflow/events,Create stage/review/finding nodes,observabilitysdk; registry_sdk,flow-summary-narrator; documentation-agent,High,Phase 2  
flowvizsdk,edge_builder,Build graph edges,Link nodes into workflow graph,node_builder; observabilitysdk,flow-summary-narrator,High,Phase 2  
flowvizsdk,flow_summary,Summarize workflow path,Create compact path summary,node_builder; edge_builder,Critical,documentation-agent; governance-agent,Phase 2  
flowvizsdk,timeline_builder,Build timeline views,Show chronological actions and events,observabilitysdk; node_builder,documentation-agent; monitoring-agent,High,Phase 2  
flowvizsdk,graph_export,Export graph payloads,Support UI or report consumption,flow_summary; timeline_builder,widgetsdk; reporting_sdk,High,Phase 2  
flowvizsdk,detail_linker,Link graph elements to details,Connect graph nodes to artifacts/audits,artifactsdk; auditsdk,documentation-agent; governance-agent,High,Phase 2  
flowvizsdk,flow_filters,Provide filtered flow views,Allow stage/role/time filtered graph,flow_summary; timeline_builder,widgetsdk,High,Phase 2  
flowvizsdk,drilldown_router,Route drill-down requests,Serve detailed node/edge inspection,detail_linker; registry_sdk,widgetsdk; jupyter_bridge,High,Phase 2  
  
====================================================================  
INTEGRATION / DELIVERY / BRIDGE / UI SDKS  
====================================================================  
  
SDK,Module,Module Purpose,Primary Usage,Depends On,Related Agent(s),Priority,Phase  
agent_bridge,tool_adapter,Adapt SDK calls to agent-safe tools,Expose deterministic SDK functions,workflowsdk; registry_sdk,Critical,all agents,Phase 1  
agent_bridge,skill_adapter,Connect skill stack to runtime execution,Map resolved skills to execution context,registry_sdk; config_sdk,Critical,model-lifecycle-orchestrator,Phase 1  
agent_bridge,agent_context_builder,Build compact agent context,Prepare token-thrifty runtime prompt context,registry_sdk; rag_sdk; workflowsdk,Critical,all agents,Phase 1  
agent_bridge,response_normalizer,Normalize tool/SDK responses,Return common response envelope,tool_adapter; workflowsdk,Critical,all agents,Phase 1  
agent_bridge,retry_policy,Manage bounded retries,Retry deterministic calls safely,response_normalizer; observabilitysdk,model-lifecycle-orchestrator; recovery-orchestrator,High,Phase 2  
  
jupyter_bridge,widget_controller,Bind widgets to backend actions,Handle user input from notebook UI,workflowsdk; hitlsdk; widgetsdk,Critical,developer-agent; validator-agent,Phase 1  
jupyter_bridge,notebook_state_sync,Sync notebook UI with workflow state,Keep UI current with backend state,widget_controller; workflowsdk,Critical,developer-agent; validator-agent,Phase 1  
jupyter_bridge,action_dispatch,Dispatch UI actions to backend,Route accept/edit/rerun/escalate actions,widget_controller; agent_bridge,Critical,developer-agent; validator-agent,Phase 1  
jupyter_bridge,result_refresh,Refresh UI after backend result,Update panels with latest response,action_dispatch; widgetsdk,Critical,developer-agent; validator-agent,Phase 1  
  
api_bridge,rest_adapter,Expose SDKs through REST-like APIs,Provide service endpoints,config_sdk; registry_sdk,external orchestrators,High,Phase 2  
api_bridge,request_mapper,Map inbound request to internal payload,Normalize external inputs,rest_adapter; agent_bridge,external orchestrators,High,Phase 2  
api_bridge,response_mapper,Map internal response to API output,Normalize API responses,request_mapper; response_normalizer,external orchestrators,High,Phase 2  
api_bridge,auth_hooks,Apply auth and access checks,Secure exposed endpoints,config_sdk; registry_sdk,api clients,High,Phase 2  
api_bridge,error_mapper,Normalize API errors,Return structured errors consistently,response_mapper; auditsdk,api clients,High,Phase 2  
  
cli_bridge,command_router,Route CLI commands to internal actions,Expose SDK actions in CLI,config_sdk; registry_sdk,power users; automation scripts,High,Phase 2  
cli_bridge,argument_parser,Parse CLI arguments,Build structured payload from command input,command_router,power users; automation scripts,High,Phase 2  
cli_bridge,output_formatter,Format CLI output,Render compact terminal output,argument_parser; response_normalizer,power users; automation scripts,High,Phase 2  
  
mcp_bridge,mcp_tool_registry,Register MCP-exposed tools,Expose approved tools to MCP,registry_sdk; agent_bridge,external MCP agents,Medium,Phase 3  
mcp_bridge,mcp_request_mapper,Map MCP requests to internal tool calls,Translate MCP payloads,mcp_tool_registry; agent_bridge,external MCP agents,Medium,Phase 3  
mcp_bridge,mcp_response_mapper,Map internal results to MCP response,Translate results back to MCP,mcp_request_mapper; response_normalizer,external MCP agents,Medium,Phase 3  
  
policysdk,policy_loader,Load policy packs,Resolve active policy set,config_sdk; registry_sdk,governance-agent; model-lifecycle-orchestrator,High,Phase 2  
policysdk,threshold_engine,Evaluate thresholds,Apply pass/warn/breach logic,policy_loader; evaluation_sdk,Critical,governance-agent; monitoring-agent,Phase 2  
policysdk,breach_detector,Detect policy breaches,Identify threshold and rule failures,threshold_engine,Critical,governance-agent; validator-agent,Phase 2  
policysdk,waiver_rules,Apply waiver logic,Determine waivable vs non-waivable,policy_loader; breach_detector,governance-agent,High,Phase 2  
policysdk,control_matrix,Map controls to workflow steps,Define required reviews/approvals,policy_loader; registry_sdk,model-lifecycle-orchestrator; governance-agent,High,Phase 2  
policysdk,rule_evaluator,Run generic rules,Evaluate non-threshold policy rules,policy_loader,Critical,governance-agent; validator-agent,Phase 2  
policysdk,approval_rules,Define approval requirements,Resolve approver and sign-off needs,control_matrix; rule_evaluator,Critical,approver-agent; governance-agent,Phase 2  
policysdk,escalation_rules,Define escalation conditions,Route severe/overdue issues upward,control_matrix; rule_evaluator,governance-agent; recovery-orchestrator,High,Phase 2  
  
widgetsdk,review_shell,Standard review UI shell,Display proposal evidence and actions,jupyter_bridge; hitlsdk,Critical,developer-agent; validator-agent,Phase 2  
widgetsdk,selection_cards,Candidate selection UI,Choose candidate versions or options,review_shell; workflowsdk,Critical,developer-agent; governance-agent,Phase 2  
widgetsdk,bootstrap_cards,Project bootstrap UI,Support new/resume project choices,jupyter_bridge; workflowsdk,session-bootstrap-orchestrator,High,Phase 2  
widgetsdk,recovery_cards,Recovery UI,Support retry/rerun/resume path choice,jupyter_bridge; workflowsdk,recovery-orchestrator,High,Phase 2  
widgetsdk,flow_panels,Flow visualization UI,Display graphs and timelines,flowvizsdk; jupyter_bridge,documentation-agent; governance-agent,High,Phase 2  
widgetsdk,detail_panels,Detail drill-down UI,Show metrics/artifacts/audit linked details,artifactsdk; auditsdk; flowvizsdk,developer-agent; validator-agent,High,Phase 2  
widgetsdk,validation_cards,Validation review UI,Support findings and conclusions,validationsdk; hitlsdk,Critical,validator-agent,Phase 2  
widgetsdk,evidence_panels,Evidence display UI,Show linked artifacts and evidence,artifactsdk; validationsdk,validator-agent; reviewer-agent,High,Phase 2  
widgetsdk,comment_capture,Comment/rationale input UI,Capture human rationale and notes,hitlsdk; jupyter_bridge,Critical,reviewer-agent; approver-agent,Phase 2  
widgetsdk,action_bar,Bounded action controls,Present accept/reject/rerun/escalate actions,hitlsdk; jupyter_bridge,Critical,developer-agent; validator-agent; approver-agent,Phase 2  
  
====================================================================  
END OF SDK MODULE DEPENDENCY MATRIX  
====================================================================  
