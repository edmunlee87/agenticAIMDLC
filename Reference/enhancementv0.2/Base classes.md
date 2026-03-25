# Base classes  
  
====================================================================  
DETAILED BASE CLASS DESIGN REFERENCE  
FOR THE AGENTIC AI MDLC FRAMEWORK  
INCLUDING KEY ATTRIBUTES, RESPONSIBILITIES, AND CHILD CLASS EXAMPLES  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This document expands the base class recommendation into a more  
implementation-ready design reference.  
  
It includes:  
- recommended number of base classes  
- why each base class is needed  
- key attributes  
- key methods  
- intended responsibilities  
- example child classes  
- inheritance guidance  
- what should NOT inherit from them  
  
The goal is to standardize the platform enough for maintainability,  
without creating a deep and fragile inheritance tree.  
  
====================================================================  
RECOMMENDED TOTAL  
--------------------------------------------------------------------  
12 BASE CLASSES  
  
This is the recommended target for the full platform.  
  
These 12 base classes are enough to provide:  
- contract consistency  
- service consistency  
- result consistency  
- controller consistency  
- review consistency  
- Spark consistency  
- storage consistency  
- UI consistency  
  
without overengineering the inheritance tree.  
  
====================================================================  
HIGH-LEVEL HIERARCHY  
====================================================================  
  
1. BaseModelBase  
2. BaseResult  
3. ValidationResultBase  
4. BaseService  
5. BaseStorageService  
6. BaseRegistryService  
7. BaseController  
8. BaseBridge  
9. BaseRuntimeComponent  
10. BaseReviewComponent  
11. BaseSparkService  
12. BaseWidgetComponent  
  
====================================================================  
1. BASEMODELBASE  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
BaseModelBase  
  
PURPOSE  
--------------------------------------------------------------------  
Root class for all structured models and records in the platform.  
  
This should be the common base for:  
- runtime_context  
- resolved_stack  
- review_payload  
- interaction_payload  
- response_envelope  
- registry records  
- artifact records  
- workflow records  
- validation records  
- knowledge records  
- monitoring records  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Prefer using Pydantic BaseModel as the technical root.  
  
Suggested design:  
class BaseModelBase(BaseModel):  
    model_config = ConfigDict(  
        extra="forbid",  
        validate_assignment=True,  
        populate_by_name=True,  
        arbitrary_types_allowed=True  
    )  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
Optional common attributes:  
- schema_name: str | None  
- schema_version: str | None  
- created_at: datetime | None  
- updated_at: datetime | None  
- created_by: str | None  
- tags: list[str]  
  
These should not be forced on every model unless useful.  
Keep it lightweight.  
  
KEY METHODS  
--------------------------------------------------------------------  
1. to_dict()  
- standardized serialization  
  
2. to_json()  
- safe JSON export  
  
3. compact_dict()  
- compact representation for agent context  
  
4. with_updates(**kwargs)  
- clone/update helper if helpful  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
- RuntimeContext  
- ResolvedStack  
- InteractionPayload  
- ReviewPayload  
- StandardResponseEnvelope  
- ArtifactRecord  
- DatasetSnapshotRecord  
- ValidationFinding  
- KnowledgeObject  
- MonitoringSnapshot  
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- service classes  
- controllers  
- bridges  
- widget renderers  
  
====================================================================  
2. BASERESULT  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
BaseResult  
  
PURPOSE  
--------------------------------------------------------------------  
Root return object for all material SDK functions.  
  
This is one of the most important base classes in the whole platform.  
  
It standardizes:  
- success/failure format  
- warnings/errors  
- references  
- agent hints  
- workflow hints  
- audit hints  
- observability hints  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Inherit from BaseModelBase.  
  
Suggested design:  
class BaseResult(BaseModelBase):  
    status: str  
    message: str  
    sdk_name: str  
    function_name: str  
    data: dict[str, Any] = Field(default_factory=dict)  
    warnings: list[dict[str, Any]] = Field(default_factory=list)  
    errors: list[dict[str, Any]] = Field(default_factory=list)  
    artifacts_created: list[dict[str, Any]] = Field(default_factory=list)  
    references: dict[str, Any] = Field(default_factory=dict)  
    agent_hint: dict[str, Any] = Field(default_factory=dict)  
    workflow_hint: dict[str, Any] = Field(default_factory=dict)  
    audit_hint: dict[str, Any] = Field(default_factory=dict)  
    observability_hint: dict[str, Any] = Field(default_factory=dict)  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
- status  
- message  
- sdk_name  
- function_name  
- data  
- warnings  
- errors  
- artifacts_created  
- references  
- agent_hint  
- workflow_hint  
- audit_hint  
- observability_hint  
  
KEY METHODS  
--------------------------------------------------------------------  
1. is_success()  
- return True if status in success family  
  
2. has_warnings()  
- return True if warnings exist  
  
3. has_errors()  
- return True if errors exist  
  
4. requires_human_review()  
- inspect agent_hint/workflow_hint  
  
5. recommended_next_action()  
- return agent_hint["recommended_next_action"]  
  
6. recommended_next_stage()  
- return workflow_hint["recommended_next_stage"]  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
- ValidationResultBase  
- DataPrepResult  
- EvaluationResult  
- MonitoringResult  
- RetrievalResultEnvelope  
- ControllerResultEnvelope  
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- pure internal helper outputs  
- raw pandas / Spark outputs  
- widget props objects  
  
====================================================================  
3. VALIDATIONRESULTBASE  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
ValidationResultBase  
  
PURPOSE  
--------------------------------------------------------------------  
Specialized result object for validation-style methods.  
  
This is used for:  
- config validation  
- schema validation  
- policy validation  
- action validation  
- contract validation  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Inherit from BaseResult.  
  
Suggested design:  
class ValidationResultBase(BaseResult):  
    is_valid: bool = False  
    failed_rules: list[dict[str, Any]] = Field(default_factory=list)  
    passed_rules: list[dict[str, Any]] = Field(default_factory=list)  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
- is_valid  
- failed_rules  
- passed_rules  
  
Inherited:  
- status  
- message  
- warnings  
- errors  
- agent_hint  
- workflow_hint  
  
KEY METHODS  
--------------------------------------------------------------------  
1. fail_count()  
- number of failed rules  
  
2. pass_count()  
- number of passed rules  
  
3. validation_summary()  
- compact validation summary string/dict  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
- ConfigValidationResult  
- DatasetContractValidationResult  
- ReviewActionValidationResult  
- PolicyApprovalValidationResult  
- ArtifactValidationResult  
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- full review outcomes  
- workflow finalization results  
  
====================================================================  
4. BASESERVICE  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
BaseService  
  
PURPOSE  
--------------------------------------------------------------------  
Root class for all SDK service classes.  
  
This gives consistent service behavior:  
- logger  
- dependency holder  
- result factory helper  
- validation helper  
- exception wrapping helper  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Normal Python class, not a pydantic model.  
  
Suggested design:  
class BaseService:  
    def __init__(  
        self,  
        config: dict | None = None,  
        dependencies: dict | None = None,  
        logger: logging.Logger | None = None  
    ) -> None:  
        self.config = config or {}  
        self.dependencies = dependencies or {}  
        self.logger = logger or logging.getLogger(self.__class__.__name__)  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
- config: dict  
- dependencies: dict  
- logger: logging.Logger  
- service_name: str  
- sdk_name: str  
  
Optional:  
- strict_mode: bool  
- environment: str | None  
  
KEY METHODS  
--------------------------------------------------------------------  
1. _build_result(...)  
- helper to build BaseResult consistently  
  
2. _build_validation_result(...)  
- helper to build ValidationResultBase consistently  
  
3. _get_dependency(name: str)  
- fetch required dependency from dependency container  
  
4. _require_fields(payload: dict, required_fields: list[str])  
- lightweight input validation helper  
  
5. _handle_exception(exc: Exception, function_name: str)  
- standardized failure result or re-raise policy  
  
6. _log_start(...)  
- operation start logging  
  
7. _log_finish(...)  
- operation end logging  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
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
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- models  
- controllers  
- widget classes  
  
====================================================================  
5. BASESTORAGESERVICE  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
BaseStorageService  
  
PURPOSE  
--------------------------------------------------------------------  
Base for services that interact with storage backends.  
  
This should centralize:  
- read/write patterns  
- storage backend handling  
- path normalization  
- existence checks  
- serialization helpers  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Inherit from BaseService.  
  
Suggested design:  
class BaseStorageService(BaseService):  
    def __init__(...):  
        super().__init__(...)  
        self.storage_backend = self.config.get("storage_backend", "local")  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
- storage_backend: str  
- default_bucket: str | None  
- base_path: str | None  
- path_prefix: str | None  
  
Optional:  
- s3_client  
- file_system  
- serializer_registry  
  
KEY METHODS  
--------------------------------------------------------------------  
1. _normalize_path(path: str) -> str  
2. _exists(path: str) -> bool  
3. _read_json(path: str) -> dict  
4. _write_json(path: str, payload: dict) -> str  
5. _read_bytes(path: str) -> bytes  
6. _write_bytes(path: str, data: bytes) -> str  
7. _resolve_uri(path_or_uri: str) -> dict  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
- ArtifactStorageAdapter  
- RegistryStorage  
- EventStorageAdapter  
- DatasetMetadataStorage  
- KnowledgeExportStorage  
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- high-level business services unless they directly manage storage  
  
====================================================================  
6. BASEREGISTRYSERVICE  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
BaseRegistryService  
  
PURPOSE  
--------------------------------------------------------------------  
Base for all registry-style services.  
  
This should standardize:  
- create/get/update/search behavior  
- entity metadata shape  
- registry record checks  
- common filters  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Inherit from BaseService.  
  
Suggested design:  
class BaseRegistryService(BaseService):  
    entity_type: str = "generic"  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
- entity_type: str  
- registry_name: str  
- storage_service: BaseStorageService | None  
  
KEY METHODS  
--------------------------------------------------------------------  
1. create_record(payload: dict) -> BaseResult  
2. get_record(record_id: str) -> BaseResult  
3. update_record(record_id: str, patch: dict) -> BaseResult  
4. search_records(filters: dict) -> BaseResult  
5. _normalize_record(payload: dict) -> dict  
6. _validate_record_id(record_id: str) -> ValidationResultBase  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
- ProjectRegistryService  
- RunRegistryService  
- SkillRegistryService  
- SDKRegistryService  
- PolicyRegistryService  
- ValidationRegistryService  
- DatasetRegistryService  
- KnowledgeRegistryService  
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- workflow state manager  
- review state manager  
unless they truly behave as registries  
  
====================================================================  
7. BASECONTROLLER  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
BaseController  
  
PURPOSE  
--------------------------------------------------------------------  
Root base for platform controllers.  
  
Controllers coordinate:  
- input validation  
- service orchestration  
- response normalization  
- event/audit hooks  
- workflow patching  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Normal Python class.  
  
Suggested design:  
class BaseController:  
    def __init__(  
        self,  
        services: dict | None = None,  
        logger: logging.Logger | None = None  
    ) -> None:  
        self.services = services or {}  
        self.logger = logger or logging.getLogger(self.__class__.__name__)  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
- services: dict  
- logger  
- controller_name: str  
  
KEY METHODS  
--------------------------------------------------------------------  
1. _get_service(name: str)  
2. _normalize_response(result: BaseResult) -> BaseResult  
3. _emit_event_if_needed(result: BaseResult)  
4. _write_audit_if_needed(result: BaseResult)  
5. _apply_workflow_patch_if_needed(result: BaseResult)  
6. _validate_payload(payload: dict, required_fields: list[str])  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
- SessionController  
- WorkflowController  
- ReviewController  
- RecoveryController  
- DataPrepController  
- DatasetController  
- DQController  
- FeatureController  
- EvaluationController  
- ScorecardController  
- ValidationController  
- ReportingController  
- KnowledgeController  
- RetrievalController  
- FlowController  
- MonitoringController  
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- low-level services  
- schema models  
  
====================================================================  
8. BASEBRIDGE  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
BaseBridge  
  
PURPOSE  
--------------------------------------------------------------------  
Root base for bridge classes connecting platform internals to external  
or UI-facing interfaces.  
  
This includes:  
- agent bridge  
- Jupyter bridge  
- API bridge  
- CLI bridge  
- MCP bridge  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Normal Python class.  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
- services: dict  
- controllers: dict  
- logger  
- bridge_name: str  
  
KEY METHODS  
--------------------------------------------------------------------  
1. _normalize_payload(payload: dict) -> dict  
2. _normalize_result(result: BaseResult) -> dict  
3. _validate_interface_contract(payload: dict) -> ValidationResultBase  
4. _enforce_allowlist(...)  
5. _map_external_to_internal(...)  
6. _map_internal_to_external(...)  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
- AgentBridge  
- JupyterBridge  
- APIBridge  
- CLIBridge  
- MCPBridge  
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- widgets themselves  
- service classes  
  
====================================================================  
9. BASERUNTIMECOMPONENT  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
BaseRuntimeComponent  
  
PURPOSE  
--------------------------------------------------------------------  
Base for runtime resolver pieces.  
  
This is useful for:  
- stage resolver  
- UI mode resolver  
- interaction mode resolver  
- token mode resolver  
- allowlist resolver  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Normal Python class.  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
- config  
- logger  
- component_name: str  
  
KEY METHODS  
--------------------------------------------------------------------  
1. resolve(runtime_context: dict) -> BaseResult  
2. _validate_runtime_context(runtime_context: dict) -> ValidationResultBase  
3. _build_runtime_decision(...)  
4. _fallback_decision(...)  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
- RuntimeResolver  
- UIModeResolver  
- InteractionModeResolver  
- TokenModeResolver  
- ReviewModeResolver  
- ScorecardStageResolver  
- ValidationStageResolver  
- MonitoringStageResolver  
- RetrievalModeResolver  
- AllowlistResolver  
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- workflow service itself  
- generic controllers  
  
====================================================================  
10. BASEREVIEWCOMPONENT  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
BaseReviewComponent  
  
PURPOSE  
--------------------------------------------------------------------  
Base for review-specific service classes.  
  
This should centralize:  
- review lookup helpers  
- review status helpers  
- allowed action helpers  
- actor role checks  
- rationale enforcement  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Inherit from BaseService.  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
- review_registry_service  
- policy_service  
- audit_service  
- event_service  
  
KEY METHODS  
--------------------------------------------------------------------  
1. _get_review(review_id: str) -> dict  
2. _validate_actor(actor: dict, expected_role: str | None = None) -> ValidationResultBase  
3. _validate_allowed_action(review: dict, action: str) -> ValidationResultBase  
4. _require_comment_if_needed(action: str, comment: str | None) -> ValidationResultBase  
5. _build_review_result(...) -> BaseResult  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
- ReviewPayloadService  
- ReviewRegistryService  
- ApprovalManager  
- OverrideManager  
- ReviewerAssignmentService  
- ActionValidationService  
- EscalationManager  
- ReviewStatusMachine  
- DecisionCaptureService  
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- generic workflow service  
- non-review domain services  
  
====================================================================  
11. BASESPARKSERVICE  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
BaseSparkService  
  
PURPOSE  
--------------------------------------------------------------------  
Base for Spark-first heavy data services.  
  
This is essential for your environment.  
  
It should centralize:  
- Spark session handling  
- DataFrame validation  
- Spark-safe result summaries  
- partition/write helpers  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Inherit from BaseService.  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
- spark: SparkSession | None  
- spark_required: bool  
- default_write_mode: str  
- default_partitions: int | None  
  
Optional:  
- checkpoint_dir: str | None  
- temp_path: str | None  
  
KEY METHODS  
--------------------------------------------------------------------  
1. _get_spark_session() -> SparkSession  
2. _validate_dataframe(df: DataFrame, name: str = "df") -> ValidationResultBase  
3. _safe_count(df: DataFrame) -> int  
4. _project_columns(df: DataFrame, columns: list[str]) -> DataFrame  
5. _safe_join(...)  
6. _write_dataframe(...)  
7. _summarize_dataframe(...) -> dict  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
- SparkSourceReader  
- SparkLineageResolver  
- SparkGrainManager  
- SparkEntityMapper  
- SparkTimeAligner  
- SparkTargetBuilder  
- SparkFeatureAligner  
- SparkPanelConstructor  
- SparkCohortBuilder  
- SparkSpellBuilder  
- SparkSplitBuilder  
- SparkQualityChecker  
- SparkOutputWriter  
- SparkManifestBuilder  
- SparkDataPrepService  
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- lightweight metadata builders  
- non-Spark review or registry services  
  
====================================================================  
12. BASEWIDGETCOMPONENT  
====================================================================  
  
CLASS NAME  
--------------------------------------------------------------------  
BaseWidgetComponent  
  
PURPOSE  
--------------------------------------------------------------------  
Base for reusable widget/UI component classes.  
  
This should centralize:  
- widget prop validation  
- component IDs  
- callback registration  
- render metadata generation  
  
RECOMMENDED IMPLEMENTATION STYLE  
--------------------------------------------------------------------  
Normal Python class.  
  
KEY ATTRIBUTES  
--------------------------------------------------------------------  
- component_id: str  
- props: dict  
- callbacks: dict  
- logger  
  
KEY METHODS  
--------------------------------------------------------------------  
1. validate_props(props: dict) -> ValidationResultBase  
2. build_component(props: dict) -> BaseResult  
3. register_callback(name: str, callback_ref: Any) -> BaseResult  
4. get_render_metadata() -> dict  
5. refresh(props_patch: dict) -> BaseResult  
  
EXAMPLE CHILD CLASSES  
--------------------------------------------------------------------  
- ReviewShell  
- SelectionCards  
- BootstrapCards  
- RecoveryCards  
- FlowPanels  
- DetailPanels  
- ValidationCards  
- EvidencePanels  
- CommentCapture  
- ActionBar  
  
WHAT SHOULD NOT INHERIT  
--------------------------------------------------------------------  
- controller classes  
- Jupyter bridge controller classes  
  
====================================================================  
13. OPTIONAL BASE CLASSES TO ADD LATER ONLY IF NEEDED  
====================================================================  
  
A. BaseExporter  
Purpose:  
Shared export logic if many SDKs begin exporting files/packages.  
  
Possible child classes:  
- AuditExportService  
- KnowledgeExportService  
- MonitoringExportService  
- ReportingExportService  
  
B. BaseTemplateExecutor  
Purpose:  
If multiple SDKs become template-heavy, not just dataprepsdk.  
  
Possible child classes:  
- DataPrepTemplateExecutor  
- MonitoringTemplateExecutor  
  
C. BaseExceptionRecordModel  
Purpose:  
Only if you want structured exception metadata across many layers.  
  
Do NOT add these too early.  
  
====================================================================  
14. CHILD CLASS EXAMPLES BY PACKAGE  
====================================================================  
  
BaseModelBase children:  
- RuntimeContext  
- ResolvedStack  
- InteractionPayload  
- ReviewPayload  
- StandardResponseEnvelope  
- DatasetRecord  
- ValidationFinding  
- KnowledgeObject  
- MonitoringSnapshot  
  
BaseResult children:  
- DataPrepResult  
- MonitoringResult  
- RetrievalResultEnvelope  
- ReportingBuildResult  
  
ValidationResultBase children:  
- ConfigValidationResult  
- DatasetContractValidationResult  
- ReviewActionValidationResult  
- PolicyApprovalValidationResult  
  
BaseService children:  
- ConfigService  
- RegistryService  
- WorkflowService  
- ArtifactService  
- AuditService  
- DQService  
- FeatureService  
- EvaluationService  
- ScorecardService  
- ValidationService  
- ReportingService  
- KnowledgeService  
- RetrievalService  
- MonitoringService  
  
BaseStorageService children:  
- ArtifactStorageAdapter  
- RegistryStorageAdapter  
- EventStorageAdapter  
- DatasetMetadataStorageAdapter  
  
BaseRegistryService children:  
- ProjectRegistryService  
- RunRegistryService  
- SkillRegistryService  
- SDKRegistryService  
- DatasetRegistryService  
- KnowledgeRegistryService  
  
BaseController children:  
- SessionController  
- WorkflowController  
- ReviewController  
- RecoveryController  
- DataPrepController  
- ValidationController  
- MonitoringController  
  
BaseBridge children:  
- AgentBridge  
- JupyterBridge  
- APIBridge  
- CLIBridge  
- MCPBridge  
  
BaseRuntimeComponent children:  
- RuntimeResolver  
- UIModeResolver  
- InteractionModeResolver  
- TokenModeResolver  
- ReviewModeResolver  
- ValidationStageResolver  
- MonitoringStageResolver  
  
BaseReviewComponent children:  
- ReviewPayloadService  
- ApprovalManager  
- EscalationManager  
- ReviewStatusMachine  
- DecisionCaptureService  
  
BaseSparkService children:  
- SparkDataPrepService  
- SparkSourceReader  
- SparkTargetBuilder  
- SparkSplitBuilder  
- SparkQualityChecker  
  
BaseWidgetComponent children:  
- ReviewShell  
- ActionBar  
- EvidencePanel  
- ValidationCards  
- SelectionCards  
- FlowPanels  
  
====================================================================  
15. RECOMMENDED INHERITANCE MAP  
====================================================================  
  
Suggested hierarchy:  
  
BaseModelBase  
  -> BaseResult  
      -> ValidationResultBase  
  -> RuntimeContext  
  -> ResolvedStack  
  -> ReviewPayload  
  -> ArtifactRecord  
  -> ValidationFinding  
  -> KnowledgeObject  
  -> MonitoringSnapshot  
  
BaseService  
  -> BaseStorageService  
  -> BaseRegistryService  
  -> BaseReviewComponent  
  -> BaseSparkService  
  -> ConfigService  
  -> WorkflowService  
  -> ScorecardService  
  -> ValidationService  
  -> MonitoringService  
  -> RetrievalService  
  
BaseController  
  -> SessionController  
  -> WorkflowController  
  -> ReviewController  
  -> ValidationController  
  -> MonitoringController  
  
BaseBridge  
  -> AgentBridge  
  -> JupyterBridge  
  -> APIBridge  
  -> CLIBridge  
  -> MCPBridge  
  
BaseRuntimeComponent  
  -> RuntimeResolver  
  -> UIModeResolver  
  -> InteractionModeResolver  
  -> TokenModeResolver  
  
BaseWidgetComponent  
  -> ReviewShell  
  -> ActionBar  
  -> EvidencePanels  
  -> ValidationCards  
  
====================================================================  
16. DESIGN RULES FOR MAINTAINABILITY  
====================================================================  
  
Rule 1  
--------------------------------------------------------------------  
Keep inheritance shallow.  
Try to avoid more than 2 levels below a base class.  
  
Rule 2  
--------------------------------------------------------------------  
Do not inherit just for naming consistency.  
Only inherit when there is real reusable behavior.  
  
Rule 3  
--------------------------------------------------------------------  
Prefer composition for:  
- policy checks  
- artifact registration  
- event writing  
- audit writing  
- retrieval calls  
- reporting assembly  
  
Rule 4  
--------------------------------------------------------------------  
Use base classes mainly for:  
- shared structure  
- shared helpers  
- shared validation  
- shared result building  
  
Rule 5  
--------------------------------------------------------------------  
Do not make business-specific classes inherit from generic UI classes,  
or vice versa.  
  
====================================================================  
17. FINAL RECOMMENDATION  
====================================================================  
  
Recommended number of base classes:  
12  
  
Recommended most important bases:  
1. BaseModelBase  
2. BaseResult  
3. ValidationResultBase  
4. BaseService  
5. BaseController  
6. BaseSparkService  
  
These six are the most important.  
The remaining six improve consistency and keep large packages cleaner.  
  
This is the right balance for your framework:  
- structured  
- maintainable  
- not overengineered  
- suitable for monorepo modular SDK design  
  
====================================================================  
END OF DETAILED BASE CLASS DESIGN REFERENCE  
====================================================================  
  
====================================================================  
BASE CLASS / CHILD CLASS / STANDALONE UTILITY MASTER TABLE  
AGENTIC AI MDLC FRAMEWORK  
COMPREHENSIVE, FUTURE-PROOF CLASS DESIGN REFERENCE  
====================================================================  
  
LEGEND  
--------------------------------------------------------------------  
Columns:  
- Class / Utility  
- Type  
- Parent  
- Primary Layer  
- Primary Responsibility  
- Example Child Classes / Users  
- Key Attributes  
- Key Functions / Methods  
- Notes  
  
Type values:  
- Base Class  
- Child Class  
- Standalone Utility  
- Standalone Model  
- Standalone Service  
  
Primary Layer values:  
- Core Contract  
- Runtime  
- Controller  
- Bridge  
- Foundation SDK  
- Data SDK  
- Domain SDK  
- Validation SDK  
- Knowledge / Retrieval  
- Monitoring / Visualization  
- UI  
  
====================================================================  
A. CORE BASE CLASSES  
====================================================================  
  
| Class / Utility | Type | Parent | Primary Layer | Primary Responsibility | Example Child Classes / Users | Key Attributes | Key Functions / Methods | Notes |  
|---|---|---|---|---|---|---|---|---|  
| BaseModelBase | Base Class | None | Core Contract | Root typed schema/model base for all records and payloads | RuntimeContext, ResolvedStack, ReviewPayload, ArtifactRecord, ValidationFinding, KnowledgeObject, MonitoringSnapshot | schema_name, schema_version, created_at, updated_at, created_by, tags | to_dict(), to_json(), compact_dict(), with_updates() | Prefer Pydantic-based root |  
| BaseResult | Base Class | BaseModelBase | Core Contract | Standardized return object for all material SDK calls | DataPrepResult, MonitoringResult, ReportingResult, RetrievalResult | status, message, sdk_name, function_name, data, warnings, errors, artifacts_created, references, agent_hint, workflow_hint, audit_hint, observability_hint | is_success(), has_warnings(), has_errors(), requires_human_review(), recommended_next_action(), recommended_next_stage() | One of the most important classes |  
| ValidationResultBase | Base Class | BaseResult | Core Contract | Specialized return type for validators | ConfigValidationResult, DatasetContractValidationResult, ReviewActionValidationResult | is_valid, failed_rules, passed_rules | fail_count(), pass_count(), validation_summary() | Use for config/schema/policy/action validation |  
| BaseService | Base Class | None | Foundation SDK | Root service base for all SDK service classes | ConfigService, WorkflowService, DataPrepService, ScorecardService, ValidationService, MonitoringService | config, dependencies, logger, sdk_name, service_name, strict_mode, environment | _build_result(), _build_validation_result(), _get_dependency(), _require_fields(), _handle_exception(), _log_start(), _log_finish() | Prefer composition for cross-SDK collaboration |  
| BaseStorageService | Base Class | BaseService | Foundation SDK | Shared storage read/write, path normalization, existence checks | ArtifactStorageAdapter, RegistryStorageAdapter, EventStorageAdapter, KnowledgeExportStorage | storage_backend, default_bucket, base_path, path_prefix, serializer_registry | _normalize_path(), _exists(), _read_json(), _write_json(), _read_bytes(), _write_bytes(), _resolve_uri() | Useful for S3 + local abstraction |  
| BaseRegistryService | Base Class | BaseService | Foundation SDK | Shared CRUD/search behavior for registry-style services | ProjectRegistryService, RunRegistryService, DatasetRegistryService, KnowledgeRegistryService | entity_type, registry_name, storage_service | create_record(), get_record(), update_record(), search_records(), _normalize_record(), _validate_record_id() | Keeps registry pattern uniform |  
| BaseController | Base Class | None | Controller | Root controller base for orchestration between UI/agent and SDKs | SessionController, WorkflowController, ReviewController, DataPrepController, ValidationController, MonitoringController | services, logger, controller_name | _get_service(), _normalize_response(), _emit_event_if_needed(), _write_audit_if_needed(), _apply_workflow_patch_if_needed(), _validate_payload() | Controllers should stay thin |  
| BaseBridge | Base Class | None | Bridge | Root interface adapter for UI/API/agent/CLI/MCP boundaries | AgentBridge, JupyterBridge, APIBridge, CLIBridge, MCPBridge | services, controllers, logger, bridge_name | _normalize_payload(), _normalize_result(), _validate_interface_contract(), _enforce_allowlist(), _map_external_to_internal(), _map_internal_to_external() | Boundary-only logic, no business logic |  
| BaseRuntimeComponent | Base Class | None | Runtime | Base for runtime resolution components | RuntimeResolver, UIModeResolver, InteractionModeResolver, TokenModeResolver, AllowlistResolver | config, logger, component_name | resolve(), _validate_runtime_context(), _build_runtime_decision(), _fallback_decision() | Runtime logic should be deterministic |  
| BaseReviewComponent | Base Class | BaseService | Foundation SDK | Shared review/HITL support logic | ReviewPayloadService, ApprovalManager, EscalationManager, ReviewStatusMachine, DecisionCaptureService | review_registry_service, policy_service, audit_service, event_service | _get_review(), _validate_actor(), _validate_allowed_action(), _require_comment_if_needed(), _build_review_result() | Key for consistent governed review behavior |  
| BaseSparkService | Base Class | BaseService | Data SDK | Shared Spark session and DataFrame guardrails | SparkDataPrepService, SparkSourceReader, SparkTargetBuilder, SparkSplitBuilder, SparkQualityChecker | spark, spark_required, default_write_mode, default_partitions, checkpoint_dir, temp_path | _get_spark_session(), _validate_dataframe(), _safe_count(), _project_columns(), _safe_join(), _write_dataframe(), _summarize_dataframe() | Essential for Spark-first design |  
| BaseWidgetComponent | Base Class | None | UI | Shared widget/component shell behavior | ReviewShell, ActionBar, EvidencePanels, ValidationCards, SelectionCards, FlowPanels | component_id, props, callbacks, logger | validate_props(), build_component(), register_callback(), get_render_metadata(), refresh() | UI components should stay presentation-focused |  
  
====================================================================  
B. CORE STANDALONE MODELS AND UTILITIES  
====================================================================  
  
| Class / Utility | Type | Parent | Primary Layer | Primary Responsibility | Example Child Classes / Users | Key Attributes | Key Functions / Methods | Notes |  
|---|---|---|---|---|---|---|---|---|  
| ArtifactRef | Standalone Model | BaseModelBase | Core Contract | Canonical artifact reference | Used by all SDK result payloads | artifact_id, artifact_type, artifact_name, version, uri_or_path | compact_dict() | Keep small and stable |  
| MetricResult | Standalone Model | BaseModelBase | Core Contract | Canonical metric record | evaluation_sdk, monitoringsdk, scorecardsdk | metric_name, metric_value, metric_unit, status, threshold_status | compact_dict() | Avoid metric-specific subclasses too early |  
| WarningRecord | Standalone Model | BaseModelBase | Core Contract | Canonical warning record | All SDKs | warning_code, summary, severity, linked_refs | compact_dict() | Standardize warning structure |  
| ErrorRecord | Standalone Model | BaseModelBase | Core Contract | Canonical error record | All SDKs | error_code, summary, details, is_retryable | compact_dict() | Standardize failure structure |  
| ActorRecord | Standalone Model | BaseModelBase | Core Contract | Canonical actor record | hitlsdk, auditsdk, validationsdk | actor_id, actor_role, actor_type | compact_dict() | Supports human/system distinction |  
| CandidateSummary | Standalone Model | BaseModelBase | Core Contract | Candidate summary for selection/review | scorecardsdk, evaluation_sdk, hitlsdk | candidate_version_id, candidate_name, candidate_type, summary_metrics, warning_count | compact_dict() | Useful in selection cards |  
| ReviewSuggestion | Standalone Model | BaseModelBase | Core Contract | Suggested review opening metadata | workflowsdk, evaluation_sdk, policysdk | should_open_review, review_type, reason, allowed_actions | compact_dict() | Helpful for agents and controllers |  
| BaseExceptionMixin | Standalone Utility | None | Core Contract | Shared exception formatting | Exception classes across SDKs | error_code, severity optional | to_error_record() | Optional but useful |  
| ResultFactory | Standalone Utility | None | Core Contract | Consistent BaseResult construction | BaseService users | default_sdk_name, logger | success(), warning(), blocked(), failed(), validation_failed() | Strongly recommended |  
| DependencyContainer | Standalone Utility | None | Core Contract | Dependency registration/resolution | Services and controllers | services, configs, factories | register(), get(), has() | Better than ad hoc dicts later |  
| IDFactory | Standalone Utility | None | Core Contract | Stable ID creation | registries, artifacts, reviews, findings | prefixes | make_id(), make_timestamped_id() | Avoid business logic in IDs |  
| TimeProvider | Standalone Utility | None | Core Contract | Time abstraction for tests and runtime | All layers | timezone, now_fn | now(), today() | Helps deterministic tests |  
| HashUtility | Standalone Utility | None | Core Contract | Hashing for config/artifacts/manifests | config_sdk, artifactsdk | algorithm | hash_dict(), hash_bytes(), hash_file_ref() | Good for reproducibility |  
| JSONUtility | Standalone Utility | None | Core Contract | Safe JSON serialization helpers | all SDKs | encoder settings | safe_dump(), safe_load(), compact_dump() | Helpful for manifests |  
| LoggingAdapter | Standalone Utility | None | Core Contract | Structured logging helper | all services/controllers | logger_name, context | log_start(), log_finish(), log_exception() | Optional but useful |  
  
====================================================================  
C. RUNTIME LAYER  
====================================================================  
  
| Class / Utility | Type | Parent | Primary Layer | Primary Responsibility | Example Child Classes / Users | Key Attributes | Key Functions / Methods | Notes |  
|---|---|---|---|---|---|---|---|---|  
| RuntimeContext | Child Class | BaseModelBase | Runtime | Current execution truth state | runtime resolver, bridges, controllers | project_id, run_id, session_id, active_role, active_domain, workflow_mode, stage_context, active_overlays, current_refs, token_mode | compact_dict(), validate_role_stage_alignment() | Canonical runtime input |  
| ResolvedStack | Child Class | BaseModelBase | Runtime | Resolved active skill/UI/SDK stack | runtime resolver, agent bridge, jupyter bridge | resolved_skills, sdk_allowlist, ui_contract, response_contract | compact_dict() | Canonical runtime output |  
| RuntimeResolver | Child Class | BaseRuntimeComponent | Runtime | Main runtime stack resolution engine | controllers, session bootstrap | skill maps, allowlist resolver, ui resolver | resolve() | Central runtime engine |  
| UIModeResolver | Child Class | BaseRuntimeComponent | Runtime | UI mode selection | runtime resolver | ui rules | resolve() | Stage-aware UI mode selection |  
| InteractionModeResolver | Child Class | BaseRuntimeComponent | Runtime | Interaction mode selection | runtime resolver | interaction rules | resolve() | Review/edit/routing mode |  
| TokenModeResolver | Child Class | BaseRuntimeComponent | Runtime | Token budget mode selection | runtime resolver, rag_sdk | token mode rules | resolve() | Micro/standard/deep review |  
| AllowlistResolver | Child Class | BaseRuntimeComponent | Runtime | SDK allowlist by stage/role/domain | runtime resolver, agent bridge | allowlist maps | resolve() | Critical for safe tool usage |  
| ReviewModeResolver | Child Class | BaseRuntimeComponent | Runtime | Review-specific resolution logic | hitlsdk, review_controller | review-type rules | resolve() | Useful once reviews diversify |  
| ScorecardStageResolver | Child Class | BaseRuntimeComponent | Runtime | Scorecard stage-specific resolution | scorecard_controller | stage maps | resolve() | Optional specialized resolver |  
| ValidationStageResolver | Child Class | BaseRuntimeComponent | Runtime | Validation stage-specific resolution | validation_controller | validation maps | resolve() | Optional specialized resolver |  
| MonitoringStageResolver | Child Class | BaseRuntimeComponent | Runtime | Monitoring stage-specific resolution | monitoring_controller | monitoring maps | resolve() | Useful with annual review mode |  
| RuntimeRulesUtility | Standalone Utility | None | Runtime | Pure functions for mapping role/domain/stage | RuntimeResolver | maps/config | resolve_role_skill(), resolve_domain_skill(), resolve_stage_skill() | Keep rule logic testable |  
| AllowlistPolicyUtility | Standalone Utility | None | Runtime | Narrow tool access based on resolved stack | AllowlistResolver, AgentBridge | allowlist config | allowed_sdk_names(), validate_call() | Strong guardrail utility |  
  
====================================================================  
D. CONTROLLERS  
====================================================================  
  
| Class / Utility | Type | Parent | Primary Layer | Primary Responsibility | Example Child Classes / Users | Key Attributes | Key Functions / Methods | Notes |  
|---|---|---|---|---|---|---|---|---|  
| SessionController | Child Class | BaseController | Controller | Bootstrap/create/resume session context | app entry, Jupyter chat entry | workflow_service, registry_service, runtime_resolver | open_session(), resume_session(), choose_project() | Thin orchestration |  
| WorkflowController | Child Class | BaseController | Controller | Stage execution and routing | all workflows | workflow_service, audit_service, event_service | run_stage(), route_next(), patch_state() | General workflow coordinator |  
| ReviewController | Child Class | BaseController | Controller | Open review payload and submit actions | governed review workspaces | hitl_service, policy_service, workflow_service | open_review(), get_review_payload(), submit_review_action(), refresh_review() | Central review entry |  
| RecoveryController | Child Class | BaseController | Controller | Recovery/retry/rerun/rollback orchestration | recovery workspace | workflow_service, event_service, audit_service | open_recovery_options(), apply_recovery_choice() | Keep deterministic |  
| DataPrepController | Child Class | BaseController | Controller | End-to-end dataprep flow orchestration | dataprep requests | dataprep_service, dataset_service, artifact_service | prepare_dataset(), reproduce_dataset(), summarize_dataprep() | Main data flow controller |  
| DatasetController | Child Class | BaseController | Controller | Dataset metadata and snapshot operations | dataset metadata UI/API | dataset_service | register_snapshot(), get_dataset_info(), list_snapshots() | Thin metadata layer |  
| DQController | Child Class | BaseController | Controller | Run and summarize data quality checks | data readiness flow | dq_service | run_dq_checks(), get_dq_summary() | Often chained after dataprep |  
| FeatureController | Child Class | BaseController | Controller | Feature engineering orchestration | domain workflows | feature_service | build_features(), get_feature_catalog() | Keep thin |  
| EvaluationController | Child Class | BaseController | Controller | Metrics/diagnostics/comparison orchestration | candidate comparisons | evaluation_service | evaluate_candidate(), compare_candidates(), evaluate_thresholds() | Used by domain SDK controllers |  
| ScorecardController | Child Class | BaseController | Controller | Scorecard domain workflow orchestration | scorecard project | scorecard_service, review_controller, workflow_service | run_fine_classing(), open_coarse_review(), fit_candidates(), finalize_model() | Key domain controller |  
| ValidationController | Child Class | BaseController | Controller | Validation workflow orchestration | validation workspace | validation_service, hitl_service, workflow_service | create_validation_run(), intake_evidence(), finalize_conclusion() | Key validation controller |  
| ReportingController | Child Class | BaseController | Controller | Reporting pack orchestration | docs/committee pack flows | reporting_service, artifact_service | build_technical_pack(), build_validation_pack(), assemble_reporting_bundle() | Output orchestration |  
| KnowledgeController | Child Class | BaseController | Controller | Knowledge capture/promotion/search | knowledge workflows | knowledge_service | capture_knowledge(), search_knowledge(), promote_knowledge() | Wave 5+ |  
| RetrievalController | Child Class | BaseController | Controller | Retrieval/query/context packaging orchestration | agent support | rag_service | retrieve_context(), build_prompt_package() | Wave 5+ |  
| FlowController | Child Class | BaseController | Controller | Flow graph/timeline orchestration | flow explorer UI | flow_service | build_flow(), filter_flow(), get_flow_drilldown() | Wave 5+ |  
| MonitoringController | Child Class | BaseController | Controller | Monitoring snapshot/dashboard/breach orchestration | monitoring workspace | monitoring_service, review_controller | ingest_snapshot(), build_dashboard(), open_breach_review(), build_annual_review_pack() | Wave 5+ |  
| ControllerResponseNormalizer | Standalone Utility | None | Controller | Normalize controller outputs to envelope | all controllers | rules/config | normalize() | Strongly recommended |  
| WorkflowPatchApplier | Standalone Utility | None | Controller | Apply state patches safely | BaseController users | workflow service ref | apply_patch() | Prevent ad hoc patching |  
| EventAuditHookUtility | Standalone Utility | None | Controller | Emit event/audit from result hints | BaseController users | services | handle_hints() | Good reusable helper |  
  
====================================================================  
E. BRIDGE LAYER  
====================================================================  
  
| Class / Utility | Type | Parent | Primary Layer | Primary Responsibility | Example Child Classes / Users | Key Attributes | Key Functions / Methods | Notes |  
|---|---|---|---|---|---|---|---|---|  
| AgentBridge | Child Class | BaseBridge | Bridge | Adapter between agent runtime and SDK/controller calls | code assistant / orchestrator | allowlist_resolver, context_builder, dispatcher | build_agent_context(), dispatch_tool(), normalize_response() | Must enforce allowlist |  
| JupyterBridge | Child Class | BaseBridge | Bridge | Adapter between Jupyter UI and controllers | JupyterLab workspace | workspace_builder, payload_builder, refresh_service | build_workspace(), submit_interaction(), refresh_workspace() | UI integration boundary |  
| APIBridge | Child Class | BaseBridge | Bridge | External API adapter | FastAPI/REST | request_mapper, response_mapper | map_request(), invoke_internal(), map_response() | Optional early |  
| CLIBridge | Child Class | BaseBridge | Bridge | CLI adapter | automation scripts | command_router, formatter | parse_command(), run_cli_action(), format_output() | Useful later |  
| MCPBridge | Child Class | BaseBridge | Bridge | MCP-compatible tool exposure | future external agents | tool_registry, request_mapper | register_tool(), map_mcp_request(), map_mcp_response() | Future-proof layer |  
| AgentContextBuilder | Standalone Utility | None | Bridge | Compact agent context builder | AgentBridge | runtime_context, resolved_stack, extra context | build() | Token-thrifty context |  
| ToolDispatcher | Standalone Utility | None | Bridge | Safe tool/service dispatch | AgentBridge | service registry, allowlist | dispatch() | Must stay deterministic |  
| BridgeResponseMapper | Standalone Utility | None | Bridge | Internal/external result mapping | all bridges | mappings | map_result() | Keeps interfaces stable |  
| InteractionPayloadBuilder | Standalone Utility | None | Bridge | Widget/API input -> interaction payload | JupyterBridge, APIBridge | actor info, widget state | build() | Important for governed review |  
| WorkspaceRefreshService | Standalone Utility | None | Bridge | Refresh UI state after backend response | JupyterBridge | workspace refs | refresh() | Good reusable utility |  
  
====================================================================  
F. FOUNDATION SDKs  
====================================================================  
  
| Class / Utility | Type | Parent | Primary Layer | Primary Responsibility | Example Child Classes / Users | Key Attributes | Key Functions / Methods | Notes |  
|---|---|---|---|---|---|---|---|---|  
| ConfigRecord | Child Class | BaseModelBase | Foundation SDK | Canonical config record | config_sdk | config_id, config_type, version, source, payload | compact_dict() | Core config model |  
| ResolvedConfig | Child Class | BaseModelBase | Foundation SDK | Effective merged config | config_sdk | effective_payload, applied_overlays, config_hash | compact_dict() | Output of resolver |  
| ConfigDiffResult | Child Class | BaseResult | Foundation SDK | Config diff result | config_sdk | changed_fields, added_fields, removed_fields | summarize_changes() | Specialized result ok |  
| ConfigService | Child Class | BaseService | Foundation SDK | Config load/validate/resolve/diff | all SDKs | loader, validator | load_config(), validate_config(), resolve_config(), diff_config(), get_config_version() | Mandatory |  
| ConfigLoaderUtility | Standalone Utility | None | Foundation SDK | File/dict config loader | ConfigService | source handlers | load_yaml(), load_json(), load_dict() | Keep isolated |  
| ConfigSchemaRegistry | Standalone Utility | None | Foundation SDK | Schema lookup registry | ConfigService | schema map | get_schema(), has_schema() | Useful for validator |  
| ProjectRegistryService | Child Class | BaseRegistryService | Foundation SDK | Project metadata registry | registry_sdk | entity_type=project | create_record(), get_record(), search_records() | Child of BaseRegistryService |  
| RunRegistryService | Child Class | BaseRegistryService | Foundation SDK | Run metadata registry | registry_sdk | entity_type=run | create_record(), get_record(), search_records() | Core runtime dependency |  
| SkillRegistryService | Child Class | BaseRegistryService | Foundation SDK | Skill metadata registry | registry_sdk | entity_type=skill | create_record(), search_records() | Useful later |  
| SDKRegistryService | Child Class | BaseRegistryService | Foundation SDK | SDK metadata registry | registry_sdk | entity_type=sdk | create_record(), search_records() | Optional early |  
| PolicyRegistryService | Child Class | BaseRegistryService | Foundation SDK | Policy pack metadata registry | registry_sdk | entity_type=policy | create_record(), get_record() | Used by policysdk |  
| ValidationRegistryService | Child Class | BaseRegistryService | Foundation SDK | Validation metadata registry | registry_sdk | entity_type=validation | create_record(), search_records() | Used later |  
| RegistrySearchUtility | Standalone Utility | None | Foundation SDK | Generic filter/search helper | registry services | filter spec | match_filters(), search() | Keep registry logic DRY |  
| EventRecord | Child Class | BaseModelBase | Foundation SDK | Structured event record | observabilitysdk | event_id, event_type, trace_id, payload, timestamp | compact_dict() | Core event model |  
| TraceRecord | Child Class | BaseModelBase | Foundation SDK | Trace/session context record | observabilitysdk | trace_id, session_id, context | compact_dict() | Correlation root |  
| ObservabilityService | Child Class | BaseService | Foundation SDK | Write/query/replay events | all SDKs/controllers | event_writer, event_query, trace_manager | create_trace(), write_event(), query_events(), replay_run(), build_event_lineage() | Mandatory |  
| EventWriter | Standalone Service | None | Foundation SDK | Persist structured events | ObservabilityService | storage service | write() | Keep append-only semantics |  
| EventQueryService | Standalone Service | None | Foundation SDK | Query event records | ObservabilityService | storage service | query() | Supports replay/flowviz |  
| ReplayEngine | Standalone Service | None | Foundation SDK | Replay run history | ObservabilityService | event query | replay() | Useful for recovery and flowviz |  
| ArtifactRecord | Child Class | BaseModelBase | Foundation SDK | Artifact metadata record | artifactsdk | artifact_id, type, name, version, uri_or_path, metadata | compact_dict() | Core artifact model |  
| ArtifactManifest | Child Class | BaseModelBase | Foundation SDK | Manifest of artifact group | artifactsdk | manifest_id, artifact_ids, summary | compact_dict() | Reproducibility helper |  
| ArtifactService | Child Class | BaseService | Foundation SDK | Artifact registration and lookup | almost all SDKs | storage adapter, registry service | register_artifact(), get_artifact(), locate_artifact(), build_artifact_manifest(), validate_artifact(), link_artifact_lineage() | Mandatory |  
| ArtifactStorageAdapter | Child Class | BaseStorageService | Foundation SDK | Artifact storage backend adapter | ArtifactService | backend config | read(), write(), exists(), resolve_uri() | S3/local abstraction |  
| ArtifactLineageService | Standalone Service | None | Foundation SDK | Artifact lineage linking | ArtifactService | registry/storage refs | link_lineage(), get_lineage() | Keep lineage explicit |  
| AuditRecord | Child Class | BaseModelBase | Foundation SDK | Canonical audit record | auditsdk | audit_id, audit_type, payload, actor, timestamp | compact_dict() | Base audit unit |  
| DecisionRecord | Child Class | BaseModelBase | Foundation SDK | Explicit decision record | auditsdk | decision_id, decision_type, actor, rationale | compact_dict() | Core governance record |  
| ApprovalRecord | Child Class | BaseModelBase | Foundation SDK | Approval record | auditsdk | approval_id, role, conditions, decision_ref | compact_dict() | Separate from decision if desired |  
| AuditService | Child Class | BaseService | Foundation SDK | Write decisions/approvals/exceptions/sign-offs | hitlsdk, validationsdk, governance | writer/exporter | write_audit_record(), register_decision(), register_approval(), register_exception(), register_signoff(), export_audit_bundle() | Mandatory for governed platform |  
| WorkflowState | Child Class | BaseModelBase | Foundation SDK | Canonical workflow state model | workflowsdk | run_id, current_stage, stage_status, selected_candidate_version_id, refs, flags | compact_dict() | Source of truth |  
| CandidateVersion | Child Class | BaseModelBase | Foundation SDK | Candidate artifact/model/version record | workflowsdk | candidate_version_id, candidate_type, refs, metrics | compact_dict() | Crucial for selection |  
| WorkflowService | Child Class | BaseService | Foundation SDK | Workflow bootstrap, state, routing, checkpoints, recovery | all controllers | stage_registry, state_store | bootstrap_project_workflow(), get_workflow_state(), update_workflow_state(), route_next_stage(), create_candidate_version(), select_candidate_version(), create_checkpoint(), resolve_recovery_path() | Mandatory |  
| StageRegistry | Standalone Utility | None | Foundation SDK | Registry of workflow stages/dependencies | WorkflowService | stage map | get_stage(), list_dependencies() | Keep stage logic outside service |  
| TransitionGuard | Standalone Utility | None | Foundation SDK | Validate stage transitions | WorkflowService | rules/policy | validate_transition() | Critical control utility |  
| CandidateSelectionUtility | Standalone Utility | None | Foundation SDK | Candidate selection validation | WorkflowService | rules | validate_selection(), summarize_candidates() | Good helper |  
  
====================================================================  
G. DATA FOUNDATION SDKs  
====================================================================  
  
| Class / Utility | Type | Parent | Primary Layer | Primary Responsibility | Example Child Classes / Users | Key Attributes | Key Functions / Methods | Notes |  
|---|---|---|---|---|---|---|---|---|  
| DatasetRecord | Child Class | BaseModelBase | Data SDK | Dataset identity metadata | dataset_sdk | dataset_id, name, domain, grain, schema_ref | compact_dict() | Core dataset object |  
| DatasetSnapshotRecord | Child Class | BaseModelBase | Data SDK | Versioned dataset snapshot | dataset_sdk | dataset_snapshot_id, dataset_id, created_at, active_flag, stats | compact_dict() | Key reproducibility record |  
| SplitRecord | Child Class | BaseModelBase | Data SDK | Split metadata | dataset_sdk | split_id, split_type, counts, rules | compact_dict() | Dev/test/oot |  
| DatasetService | Child Class | BaseService | Data SDK | Dataset registry + snapshot orchestration | controllers, dataprepsdk | registry services | register_dataset(), create_snapshot(), register_split(), create_sample_reference(), create_lineage_reference(), validate_dataset_contract(), get_dataset_snapshot() | Key metadata service |  
| DatasetContractValidator | Standalone Service | None | Data SDK | Validate schema/grain/required fields | DatasetService | contract rules | validate_contract() | Strongly recommended |  
| DQSummary | Child Class | BaseModelBase | Data SDK | Compact DQ summary | dq_sdk | check summaries, severity | compact_dict() | Agent-friendly output |  
| DQExceptionRecord | Child Class | BaseModelBase | Data SDK | DQ exception for governance/HITL | dq_sdk | issue list, severity, refs | compact_dict() | Optional but useful |  
| DQService | Child Class | BaseService | Data SDK | Run schema/missingness/consistency/rule checks | dataprep, validation, monitoring | check modules | run_schema_checks(), run_missingness_checks(), run_consistency_checks(), build_distribution_profile(), run_business_rule_checks(), build_dq_summary(), create_dq_exception() | Core check service |  
| SchemaCheckService | Standalone Service | None | Data SDK | Schema check engine | DQService | schema rules | run() | Keep checks modular |  
| MissingnessCheckService | Standalone Service | None | Data SDK | Missingness profiling engine | DQService | thresholds | run() | Separate for clarity |  
| ConsistencyCheckService | Standalone Service | None | Data SDK | Key/date/status consistency engine | DQService | consistency rules | run() | Strong prep check |  
| DistributionProfiler | Standalone Service | None | Data SDK | Compact distribution profile builder | DQService, monitoringsdk | columns/spec | build_profile() | Useful for drift too |  
| FeatureDefinition | Child Class | BaseModelBase | Data SDK | Canonical feature definition | feature_sdk | feature_name, type, source_refs, transformation_tags | compact_dict() | Catalog-friendly |  
| FeatureMetadataRecord | Child Class | BaseModelBase | Data SDK | Feature metadata | feature_sdk | domain tags, missingness, source refs | compact_dict() | Good for docs/validation |  
| FeatureLineageRecord | Child Class | BaseModelBase | Data SDK | Feature lineage detail | feature_sdk | feature_name, source_columns, transform_steps | compact_dict() | Key for auditability |  
| FeatureService | Child Class | BaseService | Data SDK | Reusable transformations and metadata/lineage | dataprep/domain SDKs | transform modules | apply_transformations(), build_lags(), build_differences(), build_grouped_features(), encode_categorical(), register_feature_metadata(), register_feature_lineage() | Shared transformation service |  
| TransformationEngine | Standalone Service | None | Data SDK | Base transforms engine | FeatureService | transform registry | apply_transformations() | Reusable module |  
| LagEngine | Standalone Service | None | Data SDK | Lag feature creation | FeatureService | lag spec | build_lags() | Supports time-series/panel |  
| GroupingEngine | Standalone Service | None | Data SDK | Grouped and hierarchical features | FeatureService | grouping spec | build_grouped_features() | Very useful in risk domain |  
| EncodingHelper | Standalone Utility | None | Data SDK | Controlled category encoding helpers | FeatureService | mapping specs | encode(), map_categories() | Avoid overcomplication early |  
| MetricSummaryRecord | Child Class | BaseModelBase | Data SDK | Canonical metric summary | evaluation_sdk | metric values | compact_dict() | Shared evaluation object |  
| ComparisonSummary | Child Class | BaseModelBase | Data SDK | Candidate comparison result | evaluation_sdk | ranked candidates, tradeoffs | compact_dict() | Used in reviews |  
| EvaluationService | Child Class | BaseService | Data SDK | Metrics/diagnostics/comparisons/thresholds | scorecardsdk, validationsdk, monitoringsdk | metric modules | compute_metrics(), run_diagnostics(), run_stability_checks(), run_calibration_checks(), compare_candidates(), evaluate_thresholds(), compare_to_benchmark() | Core analytics support |  
| MetricEngine | Standalone Service | None | Data SDK | Compute normalized metrics | EvaluationService | metric registry | compute_metrics() | Shared metric core |  
| DiagnosticEngine | Standalone Service | None | Data SDK | Compute diagnostics | EvaluationService | diagnostic registry | run_diagnostics() | Shared diagnostics core |  
| ComparisonEngine | Standalone Service | None | Data SDK | Candidate comparison logic | EvaluationService | ranking rules | compare_candidates() | Important for selection |  
| ThresholdEvaluator | Standalone Service | None | Data SDK | Threshold classification | EvaluationService, policysdk | threshold pack | evaluate_thresholds() | Shared pass/warn/breach engine |  
| DataPrepRequest | Child Class | BaseModelBase | Data SDK | Dataprep request contract | dataprepsdk | template_id, source mappings, target definition, split definition | compact_dict() | Canonical request |  
| DataPrepResult | Child Class | BaseResult | Data SDK | Dataprep result | dataprepsdk | dataset refs, manifest refs, counts | compact_dict() | Specialized result useful |  
| DataPrepService | Child Class | BaseService | Data SDK | Logical dataprep orchestration | data_prep_controller | template registry, validators | validate_dataprep_config(), validate_template_request(), execute_request(), build_cross_sectional_dataset(), build_panel_dataset(), build_time_series_dataset(), build_cohort_dataset(), build_event_history_dataset(), reproduce_dataset() | Main non-Spark dataprep service |  
| SparkDataPrepService | Child Class | BaseSparkService | Data SDK | Spark-first dataprep execution | DataPrepService | spark modules | build_cross_sectional_dataset_spark(), build_panel_dataset_spark(), build_time_series_dataset_spark(), build_cohort_dataset_spark(), build_event_history_dataset_spark(), run_prep_quality_checks_spark() | Heavy execution layer |  
| TemplateRegistryService | Standalone Service | None | Data SDK | Approved dataprep template registry | DataPrepService | template map | get_template(), validate_template_request() | Strong governance point |  
| LineageResolver | Standalone Service | None | Data SDK | Resolve source lineage and join plans | DataPrepService | source maps, join plan | resolve_lineage(), build_join_plan() | Important logic module |  
| GrainManager | Standalone Service | None | Data SDK | Resolve/validate output grain | DataPrepService | grain spec | resolve_grain(), validate_grain() | Shared data structure logic |  
| TimeAligner | Standalone Service | None | Data SDK | Resolve time windows | DataPrepService | time spec | resolve_time_windows(), validate_time_alignment() | Critical for leakage avoidance |  
| TargetBuilder | Standalone Service | None | Data SDK | Define targets logically | DataPrepService | target spec | resolve_target_definition(), validate_target_logic() | Separate from Spark builder |  
| SplitBuilder | Standalone Service | None | Data SDK | Logical split rule builder | DataPrepService | split spec | resolve_split_definition(), validate_split_strategy() | Separate from Spark execution |  
| LeakageChecker | Standalone Service | None | Data SDK | Detect leakage risks | DataPrepService | time/target rules | run_leakage_checks(), summarize_leakage_risk() | Very important in regulated modeling |  
| SparkSourceReader | Child Class | BaseSparkService | Data SDK | Read source datasets into Spark | SparkDataPrepService | read config | read_sources(), project_columns() | Spark module |  
| SparkLineageResolver | Child Class | BaseSparkService | Data SDK | Apply join plan in Spark | SparkDataPrepService | join config | apply_join_plan() | Spark module |  
| SparkTargetBuilder | Child Class | BaseSparkService | Data SDK | Build target columns in Spark | SparkDataPrepService | target rules | build_targets() | Spark module |  
| SparkSplitBuilder | Child Class | BaseSparkService | Data SDK | Apply split logic in Spark | SparkDataPrepService | split rules | build_splits() | Spark module |  
| SparkQualityChecker | Child Class | BaseSparkService | Data SDK | Spark-scale prep checks | SparkDataPrepService | check pack | run_quality_checks() | Spark module |  
| SparkManifestBuilder | Child Class | BaseSparkService | Data SDK | Spark execution manifest build | SparkDataPrepService | output refs | build_manifest() | Spark-specific metadata |  
| SparkUtils | Standalone Utility | None | Data SDK | Shared Spark helpers | all Spark modules | helper settings | safe_join(), safe_count(), project_columns(), repartition_if_needed() | Keep Spark code DRY |  
  
====================================================================  
H. DOMAIN SDKs  
====================================================================  
  
| Class / Utility | Type | Parent | Primary Layer | Primary Responsibility | Example Child Classes / Users | Key Attributes | Key Functions / Methods | Notes |  
|---|---|---|---|---|---|---|---|---|  
| FineClassingResult | Child Class | BaseModelBase | Domain SDK | Fine bin output | scorecardsdk | variable summaries, bin refs | compact_dict() | Scorecard object |  
| CoarseClassingCandidate | Child Class | BaseModelBase | Domain SDK | Coarse bin candidate | scorecardsdk | candidate_version_id, bin groups, metrics | compact_dict() | Review-ready |  
| ScorecardModelCandidate | Child Class | BaseModelBase | Domain SDK | Scorecard candidate model | scorecardsdk | candidate_version_id, coeff refs, metrics | compact_dict() | Selection-ready |  
| ScorecardService | Child Class | BaseService | Domain SDK | Scorecard development workflow logic | scorecard_controller | dataprep/evaluation/feature deps | build_fine_bins(), build_coarse_bin_candidate(), preview_edited_bins(), finalize_coarse_bins(), compare_binning_candidates(), compute_woe_iv(), build_feature_shortlist(), fit_candidate_set(), scale_scorecard(), build_score_bands(), build_scorecard_output_bundle() | First full domain SDK |  
| FineClassingEngine | Standalone Service | None | Domain SDK | Fine classing implementation | ScorecardService | variable specs | build_fine_bins() | Separate math/logic unit |  
| CoarseClassingEngine | Standalone Service | None | Domain SDK | Coarse classing implementation | ScorecardService | merge rules | build_candidate(), preview_edits(), finalize_bins() | Review-heavy unit |  
| WOEIVEngine | Standalone Service | None | Domain SDK | WoE/IV computation | ScorecardService | target refs | compute_woe_iv() | Shared scorecard analytics |  
| FeatureShortlistEngine | Standalone Service | None | Domain SDK | Build shortlist from metrics/rules | ScorecardService | shortlist rules | build_shortlist() | Separate logic |  
| LogisticCandidateEngine | Standalone Service | None | Domain SDK | Fit scorecard model candidates | ScorecardService | model spec | fit_candidate_set() | Core model fitting |  
| ScalingEngine | Standalone Service | None | Domain SDK | Score scaling logic | ScorecardService | scaling spec | scale_scorecard() | Separate math layer |  
| ScoreBandEngine | Standalone Service | None | Domain SDK | Score band generation | ScorecardService | band spec | build_score_bands() | Useful for monitoring too |  
| TimeSeriesService | Child Class | BaseService | Domain SDK | Time-series development workflow | timeseriessdk | dataprep/eval deps | run_stationarity_checks(), apply_time_series_transforms(), build_time_lags(), fit_time_series_candidates(), compare_forecasts(), run_residual_diagnostics(), build_scenario_projection(), build_timeseries_output_bundle() | Future domain service |  
| LGDService | Child Class | BaseService | Domain SDK | LGD workflow logic | lgdsdk | dataprep/eval deps | build_cure_model_dataset(), fit_cure_model(), fit_severity_model(), apply_downturn_adjustment(), apply_fl_adjustment(), aggregate_recoveries(), build_lgd_output_bundle() | Future domain service |  
| PDService | Child Class | BaseService | Domain SDK | PD workflow logic | pdsdk | dataprep/eval deps | build_rating_pd(), build_score_pd(), build_term_structure(), run_transition_logic(), calibrate_pd(), build_pd_monitoring_payload() | Future domain service |  
| EADService | Child Class | BaseService | Domain SDK | EAD workflow logic | eadsdk | dataprep/eval deps | estimate_exposure(), build_ccf_model(), model_utilization(), build_ead_monitoring_payload(), build_ead_output_bundle() | Future domain service |  
| SICRService | Child Class | BaseService | Domain SDK | SICR workflow logic | sicr_sdk | dataprep/eval deps | apply_sicr_rules(), evaluate_sicr_thresholds(), compare_sicr_methods(), track_stage_migrations(), build_sicr_output_bundle() | Future domain service |  
| ECLService | Child Class | BaseService | Domain SDK | ECL coordination logic | eclsdk | PD/LGD/EAD deps | assign_stage(), assemble_pd_inputs(), assemble_lgd_inputs(), assemble_ead_inputs(), resolve_mev_inputs(), run_scenario_engine(), apply_overlay(), build_ecl_outputs() | Future domain service |  
| StressService | Child Class | BaseService | Domain SDK | Stress testing logic | stresssdk | dataprep/eval deps | apply_stress_scenario(), resolve_macro_linkages(), generate_stressed_projection(), aggregate_stress_results(), build_stress_output_bundle() | Future domain service |  
  
====================================================================  
I. VALIDATION / REPORTING / KNOWLEDGE / RETRIEVAL / MONITORING  
====================================================================  
  
| Class / Utility | Type | Parent | Primary Layer | Primary Responsibility | Example Child Classes / Users | Key Attributes | Key Functions / Methods | Notes |  
|---|---|---|---|---|---|---|---|---|  
| ValidationRun | Child Class | BaseModelBase | Validation SDK | Validation run metadata | validationsdk | validation_run_id, scope, model_ref, status | compact_dict() | Core validation model |  
| ValidationFinding | Child Class | BaseModelBase | Validation SDK | Validation finding | validationsdk | finding_id, severity, category, evidence_refs, status | compact_dict() | Key challenge record |  
| FitnessDimensionResult | Child Class | BaseModelBase | Validation SDK | Fitness dimension result | validationsdk | dimension_name, status, notes | compact_dict() | Supports conclusion engine |  
| ValidationService | Child Class | BaseService | Validation SDK | Validation workflow logic | validation_controller | workflow/audit/hitl deps | create_validation_scope(), intake_evidence(), assess_evidence_completeness(), evaluate_fitness_dimensions(), create_finding(), assess_severity(), build_conclusion_options(), finalize_conclusion(), create_remediation_action(), build_validation_output_bundle() | Core validation SDK |  
| EvidenceIntakeService | Standalone Service | None | Validation SDK | Evidence classification/intake | ValidationService | evidence classes | intake_evidence(), classify_evidence() | Separate evidence logic |  
| FitnessFrameworkService | Standalone Service | None | Validation SDK | Evaluate fit-for-use dimensions | ValidationService | dimension rules | evaluate_fitness_dimensions() | Strong validation core |  
| ConclusionEngine | Standalone Service | None | Validation SDK | Build/finalize conclusion options | ValidationService | conclusion rules | build_conclusion_options(), finalize_conclusion() | Final validator choice still human |  
| RemediationTracker | Standalone Service | None | Validation SDK | Remediation actions and closure tracking | ValidationService | action registry | create_action(), update_status(), summarize() | Links to annual review |  
| ReportSection | Child Class | BaseModelBase | Validation SDK | Report section model | reporting_sdk | section_id, title, content refs | compact_dict() | Reporting core model |  
| NarrativeBlock | Child Class | BaseModelBase | Validation SDK | Reusable wording block | reporting_sdk | block_id, audience, domain, template_text | compact_dict() | Important for consistency |  
| ReportingService | Child Class | BaseService | Validation SDK | Technical/executive/committee/validation reporting | reporting_controller | narrative/chart/pack deps | build_technical_report(), build_executive_summary(), build_committee_pack(), build_validation_note(), get_narrative_block(), export_chart_refs(), export_table_refs(), assemble_pack() | Core reporting SDK |  
| NarrativeBlockRegistry | Standalone Service | None | Validation SDK | Narrative block lookup/manage | ReportingService | block storage | get_block(), register_block(), render_block() | Great for standardization |  
| PackAssembler | Standalone Service | None | Validation SDK | Assemble sections into final pack | ReportingService | section ordering | assemble_pack(), validate_pack_structure() | Reusable pack builder |  
| KnowledgeObject | Child Class | BaseModelBase | Knowledge / Retrieval | Canonical knowledge object | knowledge_sdk | knowledge_id, type, scope, summaries, linked_refs, quality_status | compact_dict() | Core knowledge model |  
| KnowledgeService | Child Class | BaseService | Knowledge / Retrieval | Knowledge lifecycle and promotion | knowledge_controller | registry/linker/promotion deps | create_knowledge_object(), register_knowledge(), search_knowledge(), capture_from_event(), capture_from_decision(), set_quality_status(), promote_knowledge(), export_knowledge_bundle() | Governed memory layer |  
| KnowledgeLinker | Standalone Service | None | Knowledge / Retrieval | Link knowledge to decisions/artifacts/findings | KnowledgeService | ref services | link_to_artifact(), link_to_decision(), link_to_finding() | Strong traceability |  
| PromotionManager | Standalone Service | None | Knowledge / Retrieval | Promote project knowledge to broader scopes | KnowledgeService | quality rules | request_promotion(), approve_promotion(), promote() | Prevent noisy global memory |  
| RetrievalQuery | Child Class | BaseModelBase | Knowledge / Retrieval | Retrieval query object | rag_sdk | query, scope filters, budget mode | compact_dict() | Core retrieval input |  
| ContextPack | Child Class | BaseModelBase | Knowledge / Retrieval | Prompt-ready compact context | rag_sdk | summaries, source_refs, token_estimate | compact_dict() | Main retrieval output |  
| RetrievalService | Child Class | BaseService | Knowledge / Retrieval | Retrieval/chunk/rerank/compress/package | retrieval_controller | query router/retriever/compressor | chunk_document(), embed_chunks(), route_query(), retrieve(), rerank_results(), compress_context(), build_context_pack(), get_budget_profile() | RAG orchestration service |  
| QueryRouter | Standalone Service | None | Knowledge / Retrieval | Role/domain/stage-aware retrieval planning | RetrievalService | routing rules | route_query() | Important for token thrift |  
| Retriever | Standalone Service | None | Knowledge / Retrieval | Semantic retrieval execution | RetrievalService | index/vector client | retrieve() | Keep separate from routing |  
| Reranker | Standalone Service | None | Knowledge / Retrieval | Relevance reranking and dedupe | RetrievalService | rerank rules | rerank_results() | Improves pack quality |  
| ContextCompressor | Standalone Service | None | Knowledge / Retrieval | Compress retrieval output | RetrievalService | compression mode | compress_context() | Very important for token thrift |  
| TokenBudgetManager | Standalone Utility | None | Knowledge / Retrieval | Token mode/budget utility | RetrievalService, runtime | budget profiles | get_budget_profile(), apply_budget(), estimate_size() | Critical utility |  
| FlowNode | Child Class | BaseModelBase | Monitoring / Visualization | Graph node | flowvizsdk | node_id, node_type, refs, status | compact_dict() | Visualization object |  
| FlowEdge | Child Class | BaseModelBase | Monitoring / Visualization | Graph edge | flowvizsdk | source, target, edge_type | compact_dict() | Visualization object |  
| FlowService | Child Class | BaseService | Monitoring / Visualization | Graph/timeline/drilldown orchestration | flow_controller | node/edge/detail services | build_nodes(), build_edges(), summarize_flow(), build_timeline(), export_graph(), filter_graph(), get_drilldown_payload() | Workflow visibility layer |  
| NodeBuilder | Standalone Service | None | Monitoring / Visualization | Build graph nodes | FlowService | event/state sources | build_nodes() | Keep graph logic modular |  
| EdgeBuilder | Standalone Service | None | Monitoring / Visualization | Build graph edges | FlowService | transition/dependency sources | build_edges() | Keep graph logic modular |  
| TimelineBuilder | Standalone Service | None | Monitoring / Visualization | Build timeline views | FlowService | event sources | build_timeline() | Separate chronological logic |  
| MonitoringSnapshot | Child Class | BaseModelBase | Monitoring / Visualization | Monitoring snapshot model | monitoringsdk | snapshot_id, date, grain, refs | compact_dict() | Core monitoring model |  
| MonitoringMetricSummary | Child Class | BaseModelBase | Monitoring / Visualization | Monitoring KPI summary | monitoringsdk | metrics, threshold statuses | compact_dict() | Dashboard-ready |  
| MonitoringService | Child Class | BaseService | Monitoring / Visualization | Snapshot/history/metrics/breaches/dashboard/annual review | monitoring_controller | metric/drift/dashboard modules | get_monitoring_template(), ingest_snapshot(), validate_snapshot(), append_snapshot(), compute_monitoring_metrics(), evaluate_monitoring_thresholds(), compute_drift(), compute_segment_monitoring(), build_dashboard_payload(), build_dashboard_config(), create_monitoring_note(), build_annual_review_pack(), write_monitoring_outputs() | Post-validation lifecycle SDK |  
| SnapshotValidator | Standalone Service | None | Monitoring / Visualization | Validate monitoring snapshots | MonitoringService | template rules | validate_snapshot() | Critical |  
| MonitoringHistoryManager | Standalone Service | None | Monitoring / Visualization | Append and query monitoring history | MonitoringService | history store | append_snapshot(), get_history(), get_baseline() | Important |  
| MonitoringMetricEngine | Standalone Service | None | Monitoring / Visualization | Compute monitoring metrics | MonitoringService | metric spec | compute_monitoring_metrics() | Separate metric engine |  
| DriftEngine | Standalone Service | None | Monitoring / Visualization | Drift-specific calculations | MonitoringService | drift spec | compute_drift() | Important |  
| DashboardPayloadBuilder | Standalone Service | None | Monitoring / Visualization | Build dashboard-ready data payloads | MonitoringService, Jupyter dashboard | dashboard config | build_dashboard_payload() | UI-neutral payload builder |  
| AnnualReviewPackBuilder | Standalone Service | None | Monitoring / Visualization | Build annual review pack | MonitoringService, reporting | annual review logic | build_annual_review_pack() | Key future-proof component |  
  
====================================================================  
J. UI CLASSES  
====================================================================  
  
| Class / Utility | Type | Parent | Primary Layer | Primary Responsibility | Example Child Classes / Users | Key Attributes | Key Functions / Methods | Notes |  
|---|---|---|---|---|---|---|---|---|  
| ReviewShell | Child Class | BaseWidgetComponent | UI | Main 3-panel review shell | review workspace | title, proposal, evidence, edit schema, actions | build_component(), refresh() | Core governed UI |  
| SelectionCards | Child Class | BaseWidgetComponent | UI | Candidate comparison and selection cards | scorecard/model selection | candidate summaries, selected candidate | build_component(), refresh() | Highly reusable |  
| BootstrapCards | Child Class | BaseWidgetComponent | UI | Session/project bootstrap cards | session start | recent projects, choices | build_component() | Optional early |  
| RecoveryCards | Child Class | BaseWidgetComponent | UI | Recovery decision cards | recovery workspace | recovery options | build_component() | Useful for interrupted work |  
| FlowPanels | Child Class | BaseWidgetComponent | UI | Flow graph/timeline panels | flow explorer | graph payload, timeline | build_component(), refresh() | Wave 5+ |  
| DetailPanels | Child Class | BaseWidgetComponent | UI | Drilldown details panel | flow/review dashboards | detail payload | build_component(), refresh() | Reusable details UI |  
| ValidationCards | Child Class | BaseWidgetComponent | UI | Validation-specific cards | validation workspace | findings, fitness, conclusion options | build_component(), refresh() | Specialized but reusable |  
| EvidencePanels | Child Class | BaseWidgetComponent | UI | Evidence/artifact display panel | validation/review | evidence refs, summaries | build_component(), refresh() | Important for trust |  
| CommentCapture | Child Class | BaseWidgetComponent | UI | Rationale/comment capture component | approvals/rejections | text, validation rules | build_component(), validate_props() | Useful everywhere |  
| ActionBar | Child Class | BaseWidgetComponent | UI | Bounded actions area | all governed reviews | allowed actions, callbacks | build_component(), register_callback(), refresh() | Critical control surface |  
| DashboardWorkspaceBuilder | Standalone Utility | None | UI | Monitoring dashboard layout builder | JupyterBridge | panel configs | build_dashboard_workspace() | UI-neutral orchestration helper |  
| FlowWorkspaceBuilder | Standalone Utility | None | UI | Flow explorer layout builder | JupyterBridge | graph/detail configs | build_flow_workspace() | Wave 5+ |  
| ReviewPayloadMapper | Standalone Utility | None | UI | Review payload -> widget props | JupyterBridge | mapping rules | map_review_payload() | Great DRY helper |  
| MonitoringWorkspaceSync | Standalone Utility | None | UI | Refresh monitoring dashboard state | JupyterBridge | workspace refs | refresh_snapshot(), refresh_breach_state() | Useful for dynamic updates |  
  
====================================================================  
K. FUTURE-PROOF STANDALONE UTILITIES / CLASSES TO KEEP  
====================================================================  
  
| Class / Utility | Type | Parent | Primary Layer | Primary Responsibility | Example Child Classes / Users | Key Attributes | Key Functions / Methods | Notes |  
|---|---|---|---|---|---|---|---|---|  
| SchemaRegistry | Standalone Utility | None | Core Contract | Central schema lookup | config_sdk, runtime, bridges | schema map | register_schema(), get_schema() | Good long-term utility |  
| PublicAPIMetadata | Standalone Model | BaseModelBase | Core Contract | Public API function metadata | docs/generation/tooling | sdk_name, function_name, signature, return_type | compact_dict() | Great for self-describing SDKs |  
| FunctionCatalogEntry | Standalone Model | BaseModelBase | Core Contract | Function catalog object | docs/tool registry | description, signature, dependencies, hints | compact_dict() | Useful for tool metadata |  
| ServiceFactory | Standalone Utility | None | Core Contract | Instantiate services consistently | app bootstrapping | dependency config | build_service(), build_all() | Strongly recommended |  
| PolicyInterpreter | Standalone Utility | None | Foundation SDK | Convert policy packs to actionable rules | policysdk, hitlsdk | policy pack | interpret_controls() | Good abstraction |  
| StatePatchValidator | Standalone Utility | None | Controller | Validate workflow patches before apply | controllers/workflowsdk | patch rules | validate_patch() | Prevent corrupted state |  
| ContextCompactor | Standalone Utility | None | Bridge | Build compact context blocks | agent bridge / retrieval | compaction rules | compact_runtime(), compact_review(), compact_metrics() | Good for token thrift |  
| PackReferenceBuilder | Standalone Utility | None | Reporting / Monitoring | Build refs for assembled packs | reporting_sdk, monitoringsdk | ref rules | build_pack_ref() | Good helper |  
| DomainRulesRegistry | Standalone Utility | None | Domain SDK | Domain-specific rule lookup | scorecard, PD, LGD, ECL, monitoring | rule maps | get_rule_set() | Good future-proof utility |  
| BenchmarkRepository | Standalone Service | None | Validation SDK | Store/query benchmark summaries | validationsdk, evaluation_sdk | benchmark entries | get_benchmark(), compare() | Useful later |  
| ReviewTemplateRegistry | Standalone Service | None | Foundation SDK | Reusable review templates registry | hitlsdk | template map | get_template(), validate_template() | Strong reuse utility |  
| TemplateExecutorBaseLike | Standalone Utility | None | Data SDK | Shared template execution helper | dataprepsdk, monitoringsdk maybe | template registry | execute_template() | Use utility before adding base class |  
  
====================================================================  
L. FINAL RECOMMENDATIONS  
====================================================================  
  
1. Keep the 12 base classes as the core inheritance framework.  
2. Use standalone utilities and services aggressively for:  
   - rule evaluation  
   - mapping  
   - formatting  
   - storage helpers  
   - graph building  
   - Spark helper logic  
3. Avoid turning every helper into a base class.  
4. Prefer:  
   - shallow inheritance  
   - rich composition  
   - stable contracts  
5. The most important reusable classes for long-term maintainability are:  
   - BaseResult  
   - ValidationResultBase  
   - BaseService  
   - BaseController  
   - BaseSparkService  
   - BaseReviewComponent  
6. The most important standalone utilities for future-proofing are:  
   - ResultFactory  
   - DependencyContainer  
   - IDFactory  
   - TokenBudgetManager  
   - ReviewPayloadMapper  
   - StatePatchValidator  
   - ContextCompactor  
  
====================================================================  
M. SUGGESTED NEXT ARTIFACT  
====================================================================  
  
The next most useful artifact is:  
  
A FILE-BY-FILE CLASS MAPPING TABLE  
with columns:  
- File  
- Class  
- Parent  
- Key Imports  
- Key Methods  
- Instantiated By  
- Depends On  
- Returns / Produces  
  
That would be the most coding-ready reference before implementation.  
  
====================================================================  
END OF BASE CLASS / CHILD CLASS / STANDALONE UTILITY MASTER TABLE  
====================================================================  
  
