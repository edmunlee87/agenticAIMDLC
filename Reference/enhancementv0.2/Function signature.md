Function signature  
  
  
  
  
====================================================================  
COMPREHENSIVE UNIFIED SDK FUNCTION + CLASS DESIGN REFERENCE  
AGENTIC AI MDLC FRAMEWORK  
WITH DEPENDENCIES, IMPORT LIBRARIES, SIGNATURES, RETURNS,  
SERVICE CLASSES, AND AGENT-INTERPRETABLE OUTPUTS  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This document expands the earlier SDK function design into a more  
implementation-oriented reference.  
  
It covers:  
- unified architectural principles  
- recommended Python import libraries  
- internal and external dependencies  
- core models  
- service classes  
- public functions  
- function signatures  
- return contracts  
- agent reasoning hints  
- workflow hints  
- audit / observability hints  
- implementation notes  
  
This is intended to be used as a blueprint for:  
- package creation  
- service layer design  
- agent tool wrapping  
- controller development  
- code review standards  
- integration planning  
  
This is still a design reference, not final production code.  
  
====================================================================  
1. OVERALL ARCHITECTURAL PRINCIPLES  
====================================================================  
  
1.1 Layering  
--------------------------------------------------------------------  
The platform should follow this layering:  
  
Layer 1: Core contracts and runtime  
- platform_core  
- schemas  
- response contracts  
- runtime resolver  
- controller contracts  
  
Layer 2: Foundation SDKs  
- config_sdk  
- registry_sdk  
- observabilitysdk  
- artifactsdk  
- auditsdk  
- workflowsdk  
- policysdk  
- hitlsdk  
  
Layer 3: Data and analytics SDKs  
- dataset_sdk  
- dq_sdk  
- feature_sdk  
- evaluation_sdk  
- dataprepsdk  
  
Layer 4: Domain and lifecycle SDKs  
- scorecardsdk  
- validationsdk  
- reporting_sdk  
- knowledge_sdk  
- rag_sdk  
- flowvizsdk  
- monitoringsdk  
- other domain SDKs  
  
Layer 5: Bridges and apps  
- agent_bridge  
- jupyter_bridge  
- api_bridge  
- cli_bridge  
- mcp_bridge  
  
1.2 Public API discipline  
--------------------------------------------------------------------  
Each SDK should expose:  
- typed models  
- one main service class  
- a small set of public methods  
- optional top-level functional wrappers  
  
Avoid:  
- huge god-classes  
- dozens of loosely named helper functions exposed publicly  
- direct bridge-to-internal-helper calls  
  
1.3 Import discipline  
--------------------------------------------------------------------  
Each SDK should distinguish:  
  
A. Standard library imports  
B. Third-party imports  
C. Internal platform imports  
D. Local package imports  
  
Example order:  
1. standard library  
2. third-party  
3. platform_core imports  
4. peer SDK imports  
5. local module imports  
  
1.4 Return contract discipline  
--------------------------------------------------------------------  
All material public methods should return:  
- BaseResult for SDK operations  
- ValidationResult for validation operations  
- standard_response_envelope at controller/workflow boundary  
  
1.5 Agent reasoning support  
--------------------------------------------------------------------  
Every important method should include:  
- compact message  
- reasoning summary  
- recommended next action  
- suggested follow-up functions  
- safe_to_continue flag  
  
====================================================================  
2. CORE IMPORT LIBRARY RECOMMENDATIONS  
====================================================================  
  
2.1 Standard library imports  
--------------------------------------------------------------------  
These will be commonly used across SDKs:  
  
- dataclasses  
- typing  
- abc  
- enum  
- pathlib  
- json  
- hashlib  
- uuid  
- datetime  
- time  
- os  
- copy  
- re  
- math  
- statistics  
- itertools  
- functools  
- collections  
- logging  
  
Recommended import examples:  
from __future__ import annotations  
from dataclasses import dataclass, field  
from typing import Any, Dict, List, Optional, Union, Iterable, Sequence, Tuple, Literal  
from abc import ABC, abstractmethod  
from enum import Enum  
from pathlib import Path  
from datetime import datetime, date  
import json  
import hashlib  
import uuid  
import logging  
  
2.2 Third-party libraries – platform-wide recommended  
--------------------------------------------------------------------  
Core:  
- pydantic  
- PyYAML  
- pandas  
- numpy  
  
Spark/data:  
- pyspark  
- pyarrow  
  
Visualization/reporting support:  
- matplotlib  
- plotly (optional if allowed)  
- jinja2  
  
Storage/integration:  
- boto3  
- s3fs  
- sqlalchemy or sqlite3 for lightweight metadata store  
- fastjsonschema or jsonschema optionally  
  
ML / metrics:  
- scikit-learn  
- scipy  
- statsmodels  
- optbinning  
- lifelines optionally for survival workflows  
  
Recommended imports:  
from pydantic import BaseModel, Field, ConfigDict, model_validator  
import yaml  
import pandas as pd  
import numpy as np  
  
Spark imports:  
from pyspark.sql import SparkSession, DataFrame, Window  
from pyspark.sql import functions as F  
from pyspark.sql import types as T  
  
Reporting:  
from jinja2 import Environment, FileSystemLoader  
  
Storage:  
import boto3  
import s3fs  
  
Evaluation:  
from sklearn.metrics import roc_auc_score  
from scipy import stats  
  
Scorecard:  
from optbinning import OptimalBinning  
  
2.3 Libraries by environment  
--------------------------------------------------------------------  
CML / Spark-first environment:  
- pyspark required  
- boto3 / s3fs highly recommended  
- pyarrow recommended  
- pandas used for light summaries only, not heavy governed prep  
  
2.4 Avoid over-dependence  
--------------------------------------------------------------------  
Avoid using too many libraries for the same purpose.  
Prefer:  
- pydantic for contracts  
- pyspark for heavy data  
- pandas for small local summaries  
- sklearn/scipy/statsmodels for metrics and diagnostics  
- jinja2 for reporting templating if needed  
  
====================================================================  
3. UNIFIED CORE CONTRACTS  
====================================================================  
  
--------------------------------------------------------------------  
3.1 BaseResult class  
--------------------------------------------------------------------  
  
Imports:  
from pydantic import BaseModel, Field  
from typing import Any, Dict, List, Optional  
  
Suggested class:  
  
class BaseResult(BaseModel):  
    status: str  
    message: str  
    sdk_name: str  
    function_name: str  
    data: Dict[str, Any] = Field(default_factory=dict)  
    warnings: List[Dict[str, Any]] = Field(default_factory=list)  
    errors: List[Dict[str, Any]] = Field(default_factory=list)  
    artifacts_created: List[Dict[str, Any]] = Field(default_factory=list)  
    references: Dict[str, Any] = Field(default_factory=dict)  
    agent_hint: Dict[str, Any] = Field(default_factory=dict)  
    workflow_hint: Dict[str, Any] = Field(default_factory=dict)  
    audit_hint: Dict[str, Any] = Field(default_factory=dict)  
    observability_hint: Dict[str, Any] = Field(default_factory=dict)  
  
Description:  
Base return object for all material SDK calls.  
  
Typical status:  
- success  
- success_with_warning  
- blocked  
- failed  
- invalid_input  
- pending_human_review  
- preview_ready  
- finalized  
  
--------------------------------------------------------------------  
3.2 ValidationResult class  
--------------------------------------------------------------------  
  
Imports:  
from pydantic import BaseModel, Field  
from typing import Any, Dict, List  
  
Suggested class:  
  
class ValidationResult(BaseResult):  
    is_valid: bool = False  
    failed_rules: List[Dict[str, Any]] = Field(default_factory=list)  
    passed_rules: List[Dict[str, Any]] = Field(default_factory=list)  
  
Description:  
Specialized result for config/schema/policy/action validation.  
  
--------------------------------------------------------------------  
3.3 Shared utility models  
--------------------------------------------------------------------  
  
Suggested shared models:  
- ArtifactRef  
- MetricResult  
- ReviewSuggestion  
- WarningRecord  
- ErrorRecord  
- ActorRecord  
- CandidateSummary  
- FindingSummary  
  
Recommended location:  
platform_core/schemas/common_fragments.py  
  
====================================================================  
4. FOUNDATION SDKS  
====================================================================  
  
####################################################################  
4.1 config_sdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Central configuration loading, validation, resolution, diffing,  
overlaying, and version control.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- pathlib  
- json  
- hashlib  
- copy  
- logging  
  
Third-party:  
- pydantic  
- yaml  
  
Internal dependencies:  
- platform_core.schemas.response_envelope or BaseResult  
- platform_core.exceptions  
- platform_core.utils.hash_utils  
- platform_core.utils.json_utils  
  
DIRECT SDK DEPENDENCIES  
--------------------------------------------------------------------  
Depends on:  
- platform_core only  
  
Used by:  
- all SDKs  
- runtime resolver  
- controllers  
- bridges  
  
SUGGESTED FILES  
--------------------------------------------------------------------  
- models.py  
- loader.py  
- validator.py  
- versioning.py  
- resolver.py  
- overlay.py  
- diff.py  
- exceptions.py  
- service.py  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. ConfigRecord  
2. ResolvedConfig  
3. ConfigDiffResult  
4. ConfigService  
  
CLASS DESIGN  
--------------------------------------------------------------------  
class ConfigRecord(BaseModel):  
    config_id: str  
    config_type: str  
    version: str  
    source: str  
    payload: Dict[str, Any]  
  
class ConfigService:  
    def load_config(...)  
    def validate_config(...)  
    def resolve_config(...)  
    def diff_config(...)  
    def get_config_version(...)  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
  
1. load_config  
Signature:  
load_config(  
    source: Union[str, Path, Dict[str, Any]],  
    config_type: str,  
    environment: Optional[str] = None  
) -> BaseResult  
  
Description:  
Load config from file/path/object store/dict.  
  
Return data keys:  
- config_payload  
- config_type  
- source  
- environment  
  
Agent hint:  
- recommended_next_action: validate_config  
- safe_to_continue: true  
  
2. validate_config  
Signature:  
validate_config(  
    config: Dict[str, Any],  
    schema_name: str  
) -> ValidationResult  
  
Return data keys:  
- schema_name  
- validation_summary  
  
Agent hint:  
- recommended_next_action: resolve_config if valid  
- safe_to_continue: is_valid  
  
3. resolve_config  
Signature:  
resolve_config(  
    base_config: Dict[str, Any],  
    overlays: Optional[List[Dict[str, Any]]] = None  
) -> BaseResult  
  
Return data keys:  
- effective_config  
- applied_overlays  
- config_hash  
  
4. diff_config  
Signature:  
diff_config(  
    old_config: Dict[str, Any],  
    new_config: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- added_fields  
- removed_fields  
- changed_fields  
- material_change_summary  
  
5. get_config_version  
Signature:  
get_config_version(  
    config: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- config_hash  
- version_label  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- Use pydantic for structure validation where practical  
- Support YAML and dict inputs first  
- Keep environment overlay separate from schema validation  
- Never silently drop unknown critical fields in strict mode  
  
####################################################################  
4.2 registry_sdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Metadata registry for projects, runs, skills, SDKs, policies,  
validation runs, findings, and generic lookup/search.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- datetime  
- uuid  
- logging  
- sqlite3 optionally  
  
Third-party:  
- pydantic  
- sqlalchemy optional  
  
Internal dependencies:  
- config_sdk  
- platform_core schemas  
- platform_core exceptions  
  
DIRECT SDK DEPENDENCIES  
--------------------------------------------------------------------  
Depends on:  
- config_sdk  
- platform_core  
  
Used by:  
- workflowsdk  
- hitlsdk  
- validationsdk  
- knowledge_sdk  
- monitoringsdk  
- all controllers  
  
SUGGESTED FILES  
--------------------------------------------------------------------  
- models.py  
- project_registry.py  
- run_registry.py  
- skill_registry.py  
- sdk_registry.py  
- policy_registry.py  
- validation_registry.py  
- lookup_api.py  
- search_api.py  
- storage.py  
- service.py  
- exceptions.py  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. ProjectRecord  
2. RunRecord  
3. SkillRecord  
4. RegistryStorage  
5. RegistryService  
  
CLASS DESIGN  
--------------------------------------------------------------------  
class ProjectRecord(BaseModel):  
    project_id: str  
    project_name: str  
    domain: str  
    owner_id: str  
    created_at: datetime  
  
class RegistryService:  
    def register_project(...)  
    def get_project(...)  
    def register_run(...)  
    def get_run(...)  
    def search_registry(...)  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
  
1. register_project  
Signature:  
register_project(  
    project_payload: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- project_id  
- project_record  
  
2. get_project  
Signature:  
get_project(  
    project_id: str  
) -> BaseResult  
  
3. register_run  
Signature:  
register_run(  
    run_payload: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- run_id  
- run_record  
  
4. get_run  
Signature:  
get_run(  
    run_id: str  
) -> BaseResult  
  
5. search_registry  
Signature:  
search_registry(  
    entity_type: str,  
    filters: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- entity_type  
- results  
- count  
  
6. register_skill_metadata  
Signature:  
register_skill_metadata(  
    skill_payload: Dict[str, Any]  
) -> BaseResult  
  
7. register_sdk_metadata  
Signature:  
register_sdk_metadata(  
    sdk_payload: Dict[str, Any]  
) -> BaseResult  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- Start with sqlite/file-backed metadata if needed  
- Make search/filter outputs compact  
- Support exact lookup and filtered search separately  
- Keep entity_type explicit  
  
####################################################################  
4.3 observabilitysdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Structured event and trace logging for replay, debugging, lineage, and  
flow visualization.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- datetime  
- uuid  
- logging  
- json  
  
Third-party:  
- pydantic  
  
Internal dependencies:  
- registry_sdk  
- config_sdk  
- platform_core BaseResult  
  
DIRECT SDK DEPENDENCIES  
--------------------------------------------------------------------  
Depends on:  
- config_sdk  
- registry_sdk  
  
Used by:  
- all SDKs for material events  
- flowvizsdk  
- recovery logic  
- audit and review flows  
  
SUGGESTED FILES  
--------------------------------------------------------------------  
- models.py  
- event_schema.py  
- trace_manager.py  
- event_writer.py  
- event_query.py  
- replay_engine.py  
- lineage_builder.py  
- enrichment.py  
- router.py  
- storage.py  
- service.py  
- exceptions.py  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. EventRecord  
2. TraceRecord  
3. ReplaySummary  
4. ObservabilityService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
  
1. create_trace  
Signature:  
create_trace(  
    context: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- trace_id  
- session_id  
- context_summary  
  
2. write_event  
Signature:  
write_event(  
    event_type: str,  
    payload: Dict[str, Any],  
    trace_id: Optional[str] = None  
) -> BaseResult  
  
Return data keys:  
- event_id  
- trace_id  
- event_type  
  
3. query_events  
Signature:  
query_events(  
    filters: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- events  
- count  
  
4. replay_run  
Signature:  
replay_run(  
    run_id: str  
) -> BaseResult  
  
Return data keys:  
- replay_events  
- replay_summary  
- last_known_state  
  
5. build_event_lineage  
Signature:  
build_event_lineage(  
    run_id: str  
) -> BaseResult  
  
Return data keys:  
- lineage_nodes  
- lineage_edges  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- event_type taxonomy should be standardized early  
- trace_id should be first-class  
- every material decision, review, artifact write should emit event  
  
####################################################################  
4.4 artifactsdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Artifact registration, storage abstraction, metadata, manifests,  
lineage, and location resolution.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- hashlib  
- pathlib  
- datetime  
- os  
- logging  
  
Third-party:  
- pydantic  
- boto3  
- s3fs  
- pyarrow optional  
  
Internal dependencies:  
- registry_sdk  
- config_sdk  
- platform_core BaseResult  
  
DIRECT SDK DEPENDENCIES  
--------------------------------------------------------------------  
Depends on:  
- config_sdk  
- registry_sdk  
- observabilitysdk optionally  
  
Used by:  
- almost all SDKs  
- reporting  
- validation  
- monitoring  
- dataprep  
- scorecard  
  
SUGGESTED FILES  
--------------------------------------------------------------------  
- models.py  
- registry.py  
- metadata.py  
- lineage.py  
- locator.py  
- validators.py  
- manifest.py  
- storage_adapter.py  
- checksum.py  
- version_resolver.py  
- service.py  
- exceptions.py  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. ArtifactRecord  
2. ArtifactManifest  
3. ArtifactLineageRecord  
4. ArtifactService  
5. StorageAdapter  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
  
1. register_artifact  
Signature:  
register_artifact(  
    artifact_payload: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- artifact_id  
- artifact_ref  
- metadata  
  
2. get_artifact  
Signature:  
get_artifact(  
    artifact_id: str  
) -> BaseResult  
  
3. locate_artifact  
Signature:  
locate_artifact(  
    artifact_id: str  
) -> BaseResult  
  
Return data keys:  
- uri_or_path  
- storage_type  
  
4. build_artifact_manifest  
Signature:  
build_artifact_manifest(  
    artifact_ids: List[str],  
    manifest_type: str  
) -> BaseResult  
  
5. validate_artifact  
Signature:  
validate_artifact(  
    artifact_id: str  
) -> ValidationResult  
  
6. link_artifact_lineage  
Signature:  
link_artifact_lineage(  
    parent_artifact_ids: List[str],  
    child_artifact_id: str,  
    lineage_type: str  
) -> BaseResult  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- support S3 and local path uniformly  
- artifact type taxonomy is important  
- artifact manifests should be compact and reusable  
  
####################################################################  
4.5 auditsdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Decisions, approvals, exceptions, sign-offs, and exportable audit  
bundle.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- datetime  
- uuid  
- logging  
  
Third-party:  
- pydantic  
  
Internal dependencies:  
- artifactsdk  
- registry_sdk  
- observabilitysdk  
- platform_core BaseResult  
  
DIRECT SDK DEPENDENCIES  
--------------------------------------------------------------------  
Depends on:  
- registry_sdk  
- artifactsdk  
- observabilitysdk  
  
Used by:  
- hitlsdk  
- workflowsdk  
- validationsdk  
- deployment/governance reviews  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. AuditRecord  
2. DecisionRecord  
3. ApprovalRecord  
4. ExceptionRecord  
5. AuditService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
  
1. write_audit_record  
Signature:  
write_audit_record(  
    audit_type: str,  
    payload: Dict[str, Any]  
) -> BaseResult  
  
2. register_decision  
Signature:  
register_decision(  
    decision_payload: Dict[str, Any]  
) -> BaseResult  
  
3. register_approval  
Signature:  
register_approval(  
    approval_payload: Dict[str, Any]  
) -> BaseResult  
  
4. register_exception  
Signature:  
register_exception(  
    exception_payload: Dict[str, Any]  
) -> BaseResult  
  
5. register_signoff  
Signature:  
register_signoff(  
    signoff_payload: Dict[str, Any]  
) -> BaseResult  
  
6. export_audit_bundle  
Signature:  
export_audit_bundle(  
    filters: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- audit_bundle_ref  
- included_records_count  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- explicit decision records are critical  
- approvals and conditional approvals should be distinct  
- export format should be reporting-friendly  
  
####################################################################  
4.6 workflowsdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Workflow state, routing, transitions, candidate versions, checkpoints,  
resume, and recovery.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- datetime  
- uuid  
- logging  
- copy  
  
Third-party:  
- pydantic  
  
Internal dependencies:  
- config_sdk  
- registry_sdk  
- auditsdk  
- observabilitysdk  
- artifactsdk  
- policysdk later  
- platform_core BaseResult  
  
DIRECT SDK DEPENDENCIES  
--------------------------------------------------------------------  
Depends on:  
- config_sdk  
- registry_sdk  
- observabilitysdk  
- auditsdk  
- artifactsdk  
  
Used by:  
- controllers  
- hitlsdk  
- review flow  
- all lifecycle stage routing  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. WorkflowState  
2. CandidateVersion  
3. CheckpointRecord  
4. WorkflowService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
  
1. bootstrap_project_workflow  
Signature:  
bootstrap_project_workflow(  
    project_id: str,  
    workflow_type: str,  
    initial_context: Dict[str, Any]  
) -> BaseResult  
  
2. get_workflow_state  
Signature:  
get_workflow_state(  
    run_id: str  
) -> BaseResult  
  
3. update_workflow_state  
Signature:  
update_workflow_state(  
    run_id: str,  
    state_patch: Dict[str, Any]  
) -> BaseResult  
  
4. route_next_stage  
Signature:  
route_next_stage(  
    run_id: str,  
    current_stage: str,  
    context: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- recommended_next_stage  
- blockers  
- conditions  
- route_reason  
  
5. create_candidate_version  
Signature:  
create_candidate_version(  
    run_id: str,  
    candidate_payload: Dict[str, Any]  
) -> BaseResult  
  
6. select_candidate_version  
Signature:  
select_candidate_version(  
    run_id: str,  
    candidate_version_id: str,  
    rationale: str  
) -> BaseResult  
  
7. create_checkpoint  
Signature:  
create_checkpoint(  
    run_id: str,  
    checkpoint_payload: Dict[str, Any]  
) -> BaseResult  
  
8. resolve_recovery_path  
Signature:  
resolve_recovery_path(  
    run_id: str,  
    failure_context: Dict[str, Any]  
) -> BaseResult  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- do not let downstream code bypass candidate selection  
- transition guards should be strict  
- workflow state should remain source of truth, not chat history  
  
====================================================================  
5. INTERACTION / CONTROL SDKs  
====================================================================  
  
####################################################################  
5.7 policysdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Policy packs, thresholds, approval rules, escalation rules, waiver  
logic, control matrix.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- copy  
  
Third-party:  
- pydantic  
  
Internal dependencies:  
- config_sdk  
- registry_sdk  
- evaluation_sdk optionally  
- platform_core BaseResult  
  
DIRECT SDK DEPENDENCIES  
--------------------------------------------------------------------  
Depends on:  
- config_sdk  
- registry_sdk  
  
Used by:  
- workflowsdk  
- hitlsdk  
- validationsdk  
- monitoringsdk  
- governance flows  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. PolicyPack  
2. ThresholdRule  
3. ApprovalRule  
4. EscalationRule  
5. PolicyService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
  
1. load_policy_pack  
Signature:  
load_policy_pack(  
    policy_mode: str,  
    domain: Optional[str] = None,  
    stage: Optional[str] = None  
) -> BaseResult  
  
2. evaluate_metric_set  
Signature:  
evaluate_metric_set(  
    metric_results: List[Dict[str, Any]],  
    policy_pack: Dict[str, Any]  
) -> BaseResult  
  
3. detect_breaches  
Signature:  
detect_breaches(  
    evaluation_results: List[Dict[str, Any]],  
    context: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
4. get_stage_controls  
Signature:  
get_stage_controls(  
    stage_name: str,  
    policy_pack: Dict[str, Any]  
) -> BaseResult  
  
5. requires_human_review  
Signature:  
requires_human_review(  
    stage_name: str,  
    context: Dict[str, Any],  
    policy_pack: Dict[str, Any]  
) -> BaseResult  
  
6. get_approval_requirements  
Signature:  
get_approval_requirements(  
    stage_name: str,  
    context: Dict[str, Any],  
    policy_pack: Dict[str, Any]  
) -> BaseResult  
  
7. can_actor_approve  
Signature:  
can_actor_approve(  
    actor: Dict[str, Any],  
    stage_name: str,  
    policy_pack: Dict[str, Any]  
) -> ValidationResult  
  
8. should_escalate  
Signature:  
should_escalate(  
    context: Dict[str, Any],  
    policy_pack: Dict[str, Any]  
) -> BaseResult  
  
9. is_waivable  
Signature:  
is_waivable(  
    issue_context: Dict[str, Any],  
    policy_pack: Dict[str, Any]  
) -> BaseResult  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- stage controls should be explicit  
- thresholds should be separated from workflow approval rules  
- keep waiver logic explicit and auditable  
  
####################################################################  
5.8 hitlsdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Review creation, validation of actions, review lifecycle, approvals,  
overrides, escalations, decision capture.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- datetime  
- logging  
- uuid  
  
Third-party:  
- pydantic  
  
Internal dependencies:  
- workflowsdk  
- observabilitysdk  
- auditsdk  
- artifactsdk  
- policysdk  
- registry_sdk  
- platform_core BaseResult and ValidationResult  
  
DIRECT SDK DEPENDENCIES  
--------------------------------------------------------------------  
Depends on:  
- workflowsdk  
- observabilitysdk  
- auditsdk  
- artifactsdk  
- policysdk  
- registry_sdk  
  
Used by:  
- all governed review stages  
- review_controller  
- validation and monitoring breach reviews  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. ReviewRecord  
2. ReviewTemplate  
3. ReviewActionRecord  
4. HITLService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
  
1. create_review  
Signature:  
create_review(  
    review_type: str,  
    review_payload: Dict[str, Any],  
    actor_context: Dict[str, Any]  
) -> BaseResult  
  
2. get_review  
Signature:  
get_review(  
    review_id: str  
) -> BaseResult  
  
3. build_review_payload  
Signature:  
build_review_payload(  
    review_type: str,  
    source_context: Dict[str, Any]  
) -> BaseResult  
  
4. validate_action  
Signature:  
validate_action(  
    review_id: str,  
    interaction_payload: Dict[str, Any]  
) -> ValidationResult  
  
5. transition_review_state  
Signature:  
transition_review_state(  
    review_id: str,  
    target_status: str,  
    context: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
6. approve_review  
Signature:  
approve_review(  
    review_id: str,  
    actor: Dict[str, Any],  
    comment: Optional[str] = None  
) -> BaseResult  
  
7. approve_with_conditions  
Signature:  
approve_with_conditions(  
    review_id: str,  
    actor: Dict[str, Any],  
    conditions: List[str],  
    comment: Optional[str] = None  
) -> BaseResult  
  
8. escalate_review  
Signature:  
escalate_review(  
    review_id: str,  
    reason: str,  
    target_role: Optional[str] = None  
) -> BaseResult  
  
9. capture_decision  
Signature:  
capture_decision(  
    review_id: str,  
    action: str,  
    interaction_payload: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- review_id  
- decision_record  
- review_status  
- state_patch  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- allowed actions must be explicit  
- free-form final decisions should not be allowed  
- review state transitions should be strict  
  
====================================================================  
6. DATA FOUNDATION SDKs  
====================================================================  
  
####################################################################  
6.1 dataset_sdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Dataset identity, snapshots, splits, sample refs, lineage refs,  
contract validation.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- datetime  
- uuid  
- logging  
  
Third-party:  
- pydantic  
  
Internal dependencies:  
- config_sdk  
- registry_sdk  
- artifactsdk  
- dq_sdk optionally  
- platform_core BaseResult  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. DatasetRecord  
2. DatasetSnapshotRecord  
3. SplitRecord  
4. DatasetService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- register_dataset(...)  
- create_snapshot(...)  
- register_split(...)  
- create_sample_reference(...)  
- create_lineage_reference(...)  
- validate_dataset_contract(...)  
- get_dataset_snapshot(...)  
  
Key signatures:  
  
register_dataset(  
    dataset_payload: Dict[str, Any]  
) -> BaseResult  
  
create_snapshot(  
    dataset_id: str,  
    snapshot_payload: Dict[str, Any]  
) -> BaseResult  
  
register_split(  
    dataset_snapshot_id: str,  
    split_payload: Dict[str, Any]  
) -> BaseResult  
  
validate_dataset_contract(  
    dataset_schema: Dict[str, Any],  
    contract: Dict[str, Any]  
) -> ValidationResult  
  
####################################################################  
6.2 dq_sdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Preparation-stage and modeling-stage data quality checks.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- statistics  
  
Third-party:  
- pydantic  
- pandas  
- numpy  
- pyspark optionally  
  
Internal dependencies:  
- dataset_sdk optionally  
- platform_core BaseResult  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. DQSummary  
2. DQExceptionRecord  
3. DQService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- run_schema_checks(...)  
- run_missingness_checks(...)  
- run_consistency_checks(...)  
- build_distribution_profile(...)  
- run_business_rule_checks(...)  
- build_dq_summary(...)  
- create_dq_exception(...)  
  
Key signatures:  
  
run_schema_checks(  
    data_ref: Dict[str, Any],  
    expected_schema: Dict[str, Any]  
) -> ValidationResult  
  
run_missingness_checks(  
    data_ref: Dict[str, Any],  
    rules: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
run_consistency_checks(  
    data_ref: Dict[str, Any],  
    rules: Dict[str, Any]  
) -> BaseResult  
  
build_dq_summary(  
    check_results: List[Dict[str, Any]]  
) -> BaseResult  
  
####################################################################  
6.3 feature_sdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Reusable transformation and feature lineage layer.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- math  
  
Third-party:  
- pydantic  
- pandas  
- numpy  
- pyspark  
  
Internal dependencies:  
- artifactsdk  
- registry_sdk  
- dataset_sdk  
- platform_core BaseResult  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. FeatureDefinition  
2. FeatureMetadataRecord  
3. FeatureService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- apply_transformations(...)  
- build_lags(...)  
- build_differences(...)  
- build_grouped_features(...)  
- encode_categorical(...)  
- register_feature_metadata(...)  
- register_feature_lineage(...)  
  
Key signatures:  
  
apply_transformations(  
    data_ref: Dict[str, Any],  
    feature_rules: Dict[str, Any]  
) -> BaseResult  
  
build_lags(  
    data_ref: Dict[str, Any],  
    lag_spec: Dict[str, Any]  
) -> BaseResult  
  
build_grouped_features(  
    data_ref: Dict[str, Any],  
    grouping_spec: Dict[str, Any]  
) -> BaseResult  
  
####################################################################  
6.4 evaluation_sdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Metrics, diagnostics, comparisons, thresholds, benchmarks.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- math  
  
Third-party:  
- pydantic  
- pandas  
- numpy  
- scipy  
- scikit-learn  
- statsmodels optionally  
  
Internal dependencies:  
- policysdk optionally  
- artifactsdk  
- platform_core BaseResult  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. MetricResult  
2. ComparisonSummary  
3. EvaluationService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- compute_metrics(...)  
- run_diagnostics(...)  
- run_stability_checks(...)  
- run_calibration_checks(...)  
- compare_candidates(...)  
- evaluate_thresholds(...)  
- compare_to_benchmark(...)  
  
Key signatures:  
  
compute_metrics(  
    model_type: str,  
    inputs: Dict[str, Any],  
    metric_set: Optional[List[str]] = None  
) -> BaseResult  
  
compare_candidates(  
    candidate_refs: List[Dict[str, Any]],  
    comparison_spec: Dict[str, Any]  
) -> BaseResult  
  
evaluate_thresholds(  
    metric_results: List[Dict[str, Any]],  
    threshold_pack: Dict[str, Any]  
) -> BaseResult  
  
####################################################################  
6.5 dataprepsdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Spark-first governed data preparation for approved templates and  
supported data structures.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- copy  
- uuid  
- datetime  
  
Third-party:  
- pydantic  
- pandas small-scale only  
- numpy  
- pyspark  
- pyarrow  
- boto3  
- s3fs  
  
Spark-specific imports:  
from pyspark.sql import SparkSession, DataFrame, Window  
from pyspark.sql import functions as F  
from pyspark.sql import types as T  
  
Internal dependencies:  
- config_sdk  
- dataset_sdk  
- dq_sdk  
- feature_sdk  
- artifactsdk  
- observabilitysdk  
- platform_core BaseResult  
  
DIRECT SDK DEPENDENCIES  
--------------------------------------------------------------------  
Depends on:  
- config_sdk  
- dataset_sdk  
- dq_sdk  
- feature_sdk  
- artifactsdk  
- observabilitysdk  
  
Used by:  
- scorecardsdk  
- pdsdk  
- lgdsdk  
- eadsdk  
- timeseriessdk  
- eclsdk  
- monitoringsdk indirectly  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. TemplateDefinition  
2. DataPrepRequest  
3. DataPrepResult  
4. DataPrepService  
5. SparkDataPrepService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- validate_dataprep_config(...)  
- validate_template_request(...)  
- execute_request(...)  
- build_cross_sectional_dataset(...)  
- build_panel_dataset(...)  
- build_time_series_dataset(...)  
- build_cohort_dataset(...)  
- build_event_history_dataset(...)  
- reproduce_dataset(...)  
- build_*_spark(...)  
- run_prep_quality_checks_spark(...)  
  
Key signatures:  
  
validate_dataprep_config(  
    config: Dict[str, Any]  
) -> ValidationResult  
  
validate_template_request(  
    template_id: str,  
    domain: str,  
    data_structure_type: str  
) -> ValidationResult  
  
execute_request(  
    request: Dict[str, Any]  
) -> BaseResult  
  
build_cross_sectional_dataset_spark(  
    request: Dict[str, Any],  
    spark_session: Optional[SparkSession] = None  
) -> BaseResult  
  
build_panel_dataset_spark(  
    request: Dict[str, Any],  
    spark_session: Optional[SparkSession] = None  
) -> BaseResult  
  
run_prep_quality_checks_spark(  
    dataset_ref: Dict[str, Any],  
    check_pack: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
Return data keys:  
- dataset_id  
- dataset_snapshot_id  
- data_structure_type  
- grain  
- row_count  
- target_summary  
- split_summary  
- manifest_refs  
- lineage_refs  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- all heavy prep should happen in Spark  
- pandas only for summaries or tiny outputs  
- template executor should route to Spark implementations  
- output should be compact and artifact-driven  
  
====================================================================  
7. DOMAIN / VALIDATION / REPORTING SDKs  
====================================================================  
  
####################################################################  
7.1 scorecardsdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Scorecard development: fine classing, coarse classing, WoE/IV,  
shortlisting, logistic candidates, scaling, score bands.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- math  
  
Third-party:  
- pydantic  
- pandas  
- numpy  
- pyspark  
- scikit-learn  
- optbinning  
  
Internal dependencies:  
- dataprepsdk  
- evaluation_sdk  
- feature_sdk  
- artifactsdk  
- reporting_sdk optionally  
- platform_core BaseResult  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. FineClassingResult  
2. CoarseClassingCandidate  
3. ScorecardModelCandidate  
4. ScorecardService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- build_fine_bins(...)  
- build_coarse_bin_candidate(...)  
- preview_edited_bins(...)  
- finalize_coarse_bins(...)  
- compare_binning_candidates(...)  
- compute_woe_iv(...)  
- build_feature_shortlist(...)  
- fit_candidate_set(...)  
- scale_scorecard(...)  
- build_score_bands(...)  
- build_scorecard_output_bundle(...)  
  
Key signatures:  
  
build_fine_bins(  
    dataset_ref: Dict[str, Any],  
    variable_spec: Dict[str, Any],  
    config: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
preview_edited_bins(  
    fine_bin_ref: Dict[str, Any],  
    edited_bin_groups: Dict[str, Any]  
) -> BaseResult  
  
fit_candidate_set(  
    dataset_ref: Dict[str, Any],  
    feature_set_ref: Dict[str, Any],  
    model_spec: Dict[str, Any]  
) -> BaseResult  
  
scale_scorecard(  
    model_candidate_ref: Dict[str, Any],  
    scaling_spec: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- candidate_version_ids  
- comparison_summary  
- model_metrics  
- output_refs  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- keep review-related outputs explicit  
- binning compare and finalization should integrate naturally with  
  hitlsdk/workflowsdk  
- do not hide support or monotonicity warnings  
  
####################################################################  
7.2 validationsdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Validation workflow: scope, evidence, findings, severity, fitness,  
conclusions, remediation.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- datetime  
- uuid  
  
Third-party:  
- pydantic  
- pandas optionally  
  
Internal dependencies:  
- workflowsdk  
- hitlsdk  
- policysdk  
- auditsdk  
- artifactsdk  
- evaluation_sdk  
- reporting_sdk  
- knowledge_sdk later  
- rag_sdk later  
- platform_core BaseResult  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. ValidationRun  
2. ValidationFinding  
3. FitnessDimensionResult  
4. ValidationService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- create_validation_scope(...)  
- intake_evidence(...)  
- assess_evidence_completeness(...)  
- evaluate_fitness_dimensions(...)  
- create_finding(...)  
- assess_severity(...)  
- build_conclusion_options(...)  
- finalize_conclusion(...)  
- create_remediation_action(...)  
- build_validation_output_bundle(...)  
  
Key signatures:  
  
create_validation_scope(  
    project_id: str,  
    model_ref: Dict[str, Any],  
    scope_config: Dict[str, Any]  
) -> BaseResult  
  
intake_evidence(  
    validation_run_id: str,  
    evidence_refs: List[Dict[str, Any]]  
) -> BaseResult  
  
evaluate_fitness_dimensions(  
    validation_run_id: str,  
    evidence_summary: Dict[str, Any],  
    metric_summary: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
finalize_conclusion(  
    validation_run_id: str,  
    conclusion_payload: Dict[str, Any],  
    actor: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- validation_run_id  
- findings  
- fitness_summary  
- conclusion_options or final_conclusion  
- remediation_refs  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- validation independence should be reflected in logic separation  
- conclusion finalization should require explicit human actor  
- evidence completeness should be a first-class result  
  
####################################################################  
7.3 reporting_sdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Technical, executive, validation, and committee reporting.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- json  
  
Third-party:  
- pydantic  
- jinja2  
- pandas  
- matplotlib optionally  
  
Internal dependencies:  
- artifactsdk  
- auditsdk  
- knowledge_sdk later  
- validationsdk optionally  
- flowvizsdk later  
- platform_core BaseResult  
  
MAIN CLASSES  
--------------------------------------------------------------------  
1. ReportSection  
2. NarrativeBlock  
3. ReportingService  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- build_technical_report(...)  
- build_executive_summary(...)  
- build_committee_pack(...)  
- build_validation_note(...)  
- get_narrative_block(...)  
- export_chart_refs(...)  
- export_table_refs(...)  
- assemble_pack(...)  
  
Key signatures:  
  
build_technical_report(  
    report_context: Dict[str, Any],  
    section_spec: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
build_validation_note(  
    validation_context: Dict[str, Any]  
) -> BaseResult  
  
assemble_pack(  
    section_refs: List[Dict[str, Any]],  
    pack_type: str  
) -> BaseResult  
  
Return data keys:  
- section_refs  
- report_bundle_ref  
- narrative_block_ids  
- pack_ref  
  
IMPLEMENTATION NOTES  
--------------------------------------------------------------------  
- reusable narrative blocks are very important  
- reports should be artifact-driven, not raw chat-driven  
- outputs should remain structured and composable  
  
====================================================================  
8. KNOWLEDGE / RETRIEVAL / MONITORING SDKs  
====================================================================  
  
####################################################################  
8.1 knowledge_sdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Governed knowledge object lifecycle and promotion.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- datetime  
- uuid  
  
Third-party:  
- pydantic  
  
Internal dependencies:  
- registry_sdk  
- artifactsdk  
- auditsdk  
- observabilitysdk  
- platform_core BaseResult  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- create_knowledge_object(...)  
- register_knowledge(...)  
- search_knowledge(...)  
- capture_from_event(...)  
- capture_from_decision(...)  
- set_quality_status(...)  
- promote_knowledge(...)  
- export_knowledge_bundle(...)  
  
Key signatures:  
  
create_knowledge_object(  
    knowledge_payload: Dict[str, Any]  
) -> BaseResult  
  
capture_from_decision(  
    decision_ref: Dict[str, Any],  
    summary_payload: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
promote_knowledge(  
    knowledge_id: str,  
    target_scope: str,  
    actor: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
Return data keys:  
- knowledge_id  
- scope  
- quality_status  
- linked_refs  
  
####################################################################  
8.2 rag_sdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Chunking, retrieval, reranking, compression, prompt packaging, token  
budgeting.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- math  
  
Third-party:  
- pydantic  
- numpy  
- pandas optionally  
- vector store client depending implementation  
  
Internal dependencies:  
- knowledge_sdk  
- registry_sdk  
- config_sdk  
- platform_core BaseResult  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- chunk_document(...)  
- embed_chunks(...)  
- route_query(...)  
- retrieve(...)  
- rerank_results(...)  
- compress_context(...)  
- build_context_pack(...)  
- get_budget_profile(...)  
  
Key signatures:  
  
route_query(  
    query: str,  
    runtime_context: Dict[str, Any],  
    retrieval_mode: Optional[str] = None  
) -> BaseResult  
  
retrieve(  
    query: str,  
    filters: Dict[str, Any],  
    budget_profile: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
build_context_pack(  
    query: str,  
    runtime_context: Dict[str, Any],  
    filters: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
Return data keys:  
- retrieval_plan  
- top_results  
- compressed_context  
- source_refs  
- token_estimate  
  
####################################################################  
8.3 flowvizsdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Flow graph, timeline, filtered views, drill-down.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- collections  
  
Third-party:  
- pydantic  
  
Internal dependencies:  
- observabilitysdk  
- workflowsdk  
- auditsdk  
- artifactsdk  
- hitlsdk  
- platform_core BaseResult  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- build_nodes(...)  
- build_edges(...)  
- summarize_flow(...)  
- build_timeline(...)  
- export_graph(...)  
- filter_graph(...)  
- get_drilldown_payload(...)  
  
Key signatures:  
  
summarize_flow(  
    run_id: str,  
    summary_mode: str = "compact"  
) -> BaseResult  
  
export_graph(  
    run_id: str,  
    export_mode: str = "ui"  
) -> BaseResult  
  
Return data keys:  
- graph_nodes  
- graph_edges  
- flow_summary  
- timeline  
- drilldown_refs  
  
####################################################################  
8.4 monitoringsdk  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Post-validation monitoring snapshots, trends, thresholds, dashboards,  
annual review outputs.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- datetime  
  
Third-party:  
- pydantic  
- pandas  
- numpy  
  
Internal dependencies:  
- config_sdk  
- dataset_sdk  
- dq_sdk  
- evaluation_sdk  
- policysdk  
- artifactsdk  
- auditsdk  
- workflowsdk  
- hitlsdk  
- reporting_sdk  
- platform_core BaseResult  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- get_monitoring_template(...)  
- ingest_snapshot(...)  
- validate_snapshot(...)  
- append_snapshot(...)  
- compute_monitoring_metrics(...)  
- evaluate_monitoring_thresholds(...)  
- compute_drift(...)  
- compute_segment_monitoring(...)  
- build_dashboard_payload(...)  
- build_dashboard_config(...)  
- create_monitoring_note(...)  
- build_annual_review_pack(...)  
- write_monitoring_outputs(...)  
  
Key signatures:  
  
ingest_snapshot(  
    snapshot_payload: Dict[str, Any],  
    template_ref: Dict[str, Any]  
) -> BaseResult  
  
compute_monitoring_metrics(  
    model_id: str,  
    snapshot_ref: Dict[str, Any],  
    metric_spec: Optional[Dict[str, Any]] = None  
) -> BaseResult  
  
build_dashboard_payload(  
    model_id: str,  
    snapshot_ref: Dict[str, Any],  
    dashboard_mode: str = "standard"  
) -> BaseResult  
  
build_annual_review_pack(  
    model_id: str,  
    period_spec: Dict[str, Any]  
) -> BaseResult  
  
Return data keys:  
- snapshot_id  
- history_ref  
- metric_summary  
- breach_summary  
- dashboard_payload_ref  
- annual_review_pack_ref  
  
====================================================================  
9. BRIDGE LAYER  
====================================================================  
  
####################################################################  
9.1 agent_bridge  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
Thin adapter between runtime/agent and SDK service calls.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
- importlib optionally  
  
Third-party:  
- pydantic  
  
Internal dependencies:  
- platform_core runtime and schema modules  
- all SDK service classes indirectly  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- build_agent_context(...)  
- dispatch_tool(...)  
- normalize_response(...)  
- apply_retry_policy(...)  
  
Key signatures:  
  
dispatch_tool(  
    sdk_name: str,  
    function_name: str,  
    payload: Dict[str, Any],  
    allowlist: List[str]  
) -> BaseResult  
  
normalize_response(  
    raw_result: Dict[str, Any],  
    sdk_name: str,  
    function_name: str  
) -> BaseResult  
  
####################################################################  
9.2 jupyter_bridge  
####################################################################  
  
DESCRIPTION  
--------------------------------------------------------------------  
UI-side controller binding for workspace and widget interaction.  
  
EXTERNAL LIBRARY IMPORTS  
--------------------------------------------------------------------  
Standard:  
- logging  
  
Third-party:  
- anywidget or ipywidgets / JupyterLab extension APIs depending design  
  
Internal dependencies:  
- widgetsdk  
- platform_core controllers  
- platform_core schemas  
  
PUBLIC FUNCTIONS  
--------------------------------------------------------------------  
- build_workspace(...)  
- map_review_payload_to_widgets(...)  
- build_interaction_payload(...)  
- refresh_workspace(...)  
  
====================================================================  
10. UNIFIED AGENT OUTPUT DESIGN  
====================================================================  
  
Every material function should populate these fields:  
  
message  
- one-line direct description of result  
  
data  
- exact structured result  
  
warnings  
- compact warning list  
  
errors  
- compact error list  
  
agent_hint  
- reasoning_summary  
- recommended_next_action  
- requires_human_review  
- suggested_followup_functions  
- safe_to_continue  
  
workflow_hint  
- recommended_next_stage  
- state_patch  
- should_open_review  
- review_type  
  
audit_hint  
- should_write_audit  
- audit_type  
  
observability_hint  
- should_write_event  
- event_type  
  
Recommended pattern:  
  
agent_hint = {  
  "reasoning_summary": "Candidate B is stronger on IV retention and has fewer support breaches.",  
  "recommended_next_action": "create_review",  
  "requires_human_review": true,  
  "suggested_followup_functions": [  
    "hitlsdk.create_review",  
    "workflowsdk.route_next_stage"  
  ],  
  "safe_to_continue": false  
}  
  
====================================================================  
11. RECOMMENDED SERVICE CLASS IMPORT PATTERN  
====================================================================  
  
Example:  
  
from __future__ import annotations  
  
from typing import Any, Dict, List, Optional  
from dataclasses import dataclass  
import logging  
  
from pydantic import BaseModel, Field  
  
from platform_core.schemas.common_fragments import BaseResult, ValidationResult  
from platform_core.exceptions import PlatformValidationError  
from config_sdk.service import ConfigService  
from registry_sdk.service import RegistryService  
from artifactsdk.service import ArtifactService  
  
class ExampleService:  
    def __init__(  
        self,  
        config_service: ConfigService,  
        registry_service: RegistryService,  
        artifact_service: ArtifactService,  
        logger: Optional[logging.Logger] = None  
    ) -> None:  
        self.config_service = config_service  
        self.registry_service = registry_service  
        self.artifact_service = artifact_service  
        self.logger = logger or logging.getLogger(__name__)  
  
====================================================================  
12. COMPREHENSIVE DEPENDENCY SUMMARY BY SDK  
====================================================================  
  
| SDK | Internal SDK Dependencies | Typical External Libraries |  
|---|---|---|  
| config_sdk | platform_core | pydantic, yaml |  
| registry_sdk | config_sdk, platform_core | pydantic, sqlite3/sqlalchemy |  
| observabilitysdk | config_sdk, registry_sdk | pydantic |  
| artifactsdk | config_sdk, registry_sdk, observabilitysdk optional | pydantic, boto3, s3fs, pyarrow |  
| auditsdk | registry_sdk, artifactsdk, observabilitysdk | pydantic |  
| workflowsdk | config_sdk, registry_sdk, observabilitysdk, auditsdk, artifactsdk, policysdk optional | pydantic |  
| policysdk | config_sdk, registry_sdk, evaluation_sdk optional | pydantic |  
| hitlsdk | workflowsdk, observabilitysdk, auditsdk, artifactsdk, policysdk, registry_sdk | pydantic |  
| dataset_sdk | config_sdk, registry_sdk, artifactsdk, dq_sdk optional | pydantic |  
| dq_sdk | dataset_sdk optional, platform_core | pydantic, pandas, numpy, pyspark |  
| feature_sdk | artifactsdk, registry_sdk, dataset_sdk | pydantic, pandas, numpy, pyspark |  
| evaluation_sdk | policysdk optional, artifactsdk | pydantic, pandas, numpy, scipy, sklearn, statsmodels |  
| reporting_sdk | artifactsdk, auditsdk, validationsdk optional, knowledge_sdk later | pydantic, jinja2, pandas |  
| dataprepsdk | config_sdk, dataset_sdk, dq_sdk, feature_sdk, artifactsdk, observabilitysdk | pydantic, pyspark, pandas, numpy, boto3, s3fs |  
| scorecardsdk | dataprepsdk, evaluation_sdk, feature_sdk, artifactsdk, reporting_sdk optional | pydantic, pandas, numpy, sklearn, optbinning |  
| validationsdk | workflowsdk, hitlsdk, policysdk, auditsdk, artifactsdk, evaluation_sdk, reporting_sdk | pydantic, pandas |  
| knowledge_sdk | registry_sdk, artifactsdk, auditsdk, observabilitysdk | pydantic |  
| rag_sdk | knowledge_sdk, registry_sdk, config_sdk | pydantic, numpy, vector store client |  
| flowvizsdk | observabilitysdk, workflowsdk, auditsdk, artifactsdk, hitlsdk | pydantic |  
| monitoringsdk | config_sdk, dataset_sdk, dq_sdk, evaluation_sdk, policysdk, artifactsdk, auditsdk, workflowsdk, hitlsdk, reporting_sdk | pydantic, pandas, numpy |  
| agent_bridge | platform_core, all SDK service classes indirectly | pydantic |  
| jupyter_bridge | widgetsdk, platform_core controllers | anywidget/ipywidgets or Jupyter extension stack |  
| api_bridge | platform_core controllers, agent_bridge | fastapi/pydantic optional |  
| cli_bridge | platform_core controllers, agent_bridge | typer/click optional |  
| mcp_bridge | agent_bridge, api_bridge | MCP-compatible libs later |  
  
====================================================================  
13. RECOMMENDED NEXT STEP  
====================================================================  
  
The best next artifact is a **full function catalog table** for the  
Phase 1–4 build set with columns:  
  
- SDK  
- Class  
- Function  
- Signature  
- Description  
- Internal dependencies  
- External libraries  
- Return data keys  
- Agent hint  
- Workflow hint  
- Audit required?  
- HITL required?  
  
That would be the most implementation-ready reference before coding.  
  
====================================================================  
END OF COMPREHENSIVE UNIFIED SDK FUNCTION + CLASS DESIGN REFERENCE  
====================================================================  
