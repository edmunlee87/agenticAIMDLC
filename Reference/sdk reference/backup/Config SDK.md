# Config SDK  
  
====================================================================  
SDK DESIGN SPECIFICATION  
CONFIG_SDK  
AGENTIC AI MDLC / ECL PLATFORM  
DETAILED, COMPREHENSIVE, FUTURE-PROOF  
====================================================================  
  
STATUS  
--------------------------------------------------------------------  
Draft v1.0  
  
PURPOSE  
--------------------------------------------------------------------  
config_sdk is the central configuration foundation for the entire  
agentic AI MDLC platform.  
  
It is responsible for:  
- loading configuration from files and in-memory sources  
- validating configuration structures  
- merging config layers deterministically  
- resolving runtime config stacks  
- supporting domain, role, environment, and project overlays  
- producing immutable effective configuration objects  
- providing a single consistent contract for all other SDKs  
  
config_sdk must be:  
- domain-aware but domain-agnostic in implementation  
- stable and deterministic  
- strongly typed  
- easy to extend  
- safe for enterprise usage  
- compatible with local, Jupyter, API, CLI, MCP, and agent-driven flows  
  
====================================================================  
1. DESIGN OBJECTIVES  
====================================================================  
  
PRIMARY OBJECTIVES  
--------------------------------------------------------------------  
1. Provide a single source of truth for configuration resolution.  
2. Support config layering across:  
   - base  
   - domain  
   - role  
   - environment  
   - project  
   - runtime overrides  
3. Enable all SDKs to consume a consistent resolved config object.  
4. Support strict schema validation with meaningful errors.  
5. Keep configuration deterministic and traceable.  
6. Produce config fingerprints / hashes for lineage and reproducibility.  
7. Support future runtime resolution needs for workflow, UI, policy,  
   monitoring, validation, and domain model logic.  
  
SECONDARY OBJECTIVES  
--------------------------------------------------------------------  
1. Support configuration explainability, including:  
   - where a value came from  
   - which layer overrode which  
2. Allow partial config packages to be reused across projects.  
3. Enable safe config diffing between environments and runs.  
4. Support future config authoring tools and UI editors.  
  
====================================================================  
2. SCOPE  
====================================================================  
  
IN SCOPE  
--------------------------------------------------------------------  
- Config file loading  
- Config schema validation  
- Config stack merging  
- Config overlay precedence  
- Effective config rendering  
- Config hashing / fingerprinting  
- Config reference resolution  
- Config metadata and provenance capture  
- Public config service interfaces  
- Pydantic-backed config contracts  
- Domain/role/env/project overlay logic  
- Runtime override injection  
- YAML / JSON / TOML support  
- Optional secrets reference placeholders  
  
OUT OF SCOPE  
--------------------------------------------------------------------  
- Full secrets management implementation  
- External secrets vault client implementation  
- GUI config editor  
- Live bidirectional config sync  
- Direct database storage of configs  
- Business logic of downstream SDKs  
- Workflow state mutation  
- Policy evaluation logic itself  
- Artifact writing itself  
  
====================================================================  
3. WHY CONFIG_SDK COMES FIRST  
====================================================================  
  
Every other SDK depends on configuration.  
  
Examples:  
- registry_sdk needs registry backend config  
- workflow_sdk needs stage registry and routing config  
- hitl_sdk needs review rules and UI contract config  
- dataset_sdk needs dataset schema and storage config  
- reporting_sdk needs template and export config  
- monitoring_sdk needs threshold and schedule config  
- domain SDKs need modeling assumptions, segmentation rules, template  
  selection, and parameter definitions  
  
If config_sdk is weak or inconsistent:  
- dependency direction becomes messy  
- config drift increases  
- runtime behavior becomes harder to explain  
- auditability suffers  
- reproducibility becomes weak  
  
====================================================================  
4. POSITION IN THE PLATFORM  
====================================================================  
  
LAYER POSITION  
--------------------------------------------------------------------  
config_sdk sits at the bottom of the platform core.  
  
It should be depended on by:  
- registry_sdk  
- artifact_sdk  
- audit_sdk  
- observability_sdk  
- workflow_sdk  
- hitl_sdk  
- dataset_sdk  
- dataprep_sdk  
- dq_sdk  
- feature_sdk  
- evaluation_sdk  
- validation_sdk  
- reporting_sdk  
- monitoring_sdk  
- knowledge_sdk  
- rag_sdk  
- policy_sdk  
- flowviz_sdk  
- all domain SDKs  
- all bridge SDKs  
  
config_sdk itself should have minimal dependencies.  
  
====================================================================  
5. CORE RESPONSIBILITIES  
====================================================================  
  
5.1 Config source loading  
--------------------------------------------------------------------  
Must support loading from:  
- YAML files  
- JSON files  
- TOML files  
- Python dict objects  
- runtime override dicts  
  
5.2 Config stack resolution  
--------------------------------------------------------------------  
Must support deterministic merge order such as:  
1. base  
2. domain overlay  
3. role overlay  
4. environment overlay  
5. project overlay  
6. runtime override  
  
5.3 Validation  
--------------------------------------------------------------------  
Must validate:  
- structure  
- required keys  
- enum values  
- cross-field constraints  
- nested config object constraints  
  
5.4 Provenance tracking  
--------------------------------------------------------------------  
Must track:  
- source file/path  
- layer name  
- merged order  
- value origin  
- effective config hash  
  
5.5 Effective config production  
--------------------------------------------------------------------  
Must output:  
- immutable effective config object  
- optionally typed Pydantic model  
- optionally flattened dict for runtime consumption  
  
5.6 Diff and inspection support  
--------------------------------------------------------------------  
Must support:  
- diff between two config bundles  
- explain override origin  
- render effective config  
- show unresolved or invalid placeholders  
  
====================================================================  
6. KEY DESIGN PRINCIPLES  
====================================================================  
  
PRINCIPLE 1: STRICT BY DEFAULT  
--------------------------------------------------------------------  
Unknown keys should be blocked unless explicitly allowed.  
  
PRINCIPLE 2: EXPLICIT OVER IMPLICIT  
--------------------------------------------------------------------  
Every override layer should be intentional and named.  
  
PRINCIPLE 3: IMMUTABLE RESOLVED CONFIG  
--------------------------------------------------------------------  
Resolved config objects should not be casually mutated.  
  
PRINCIPLE 4: SEPARATE RAW, VALIDATED, AND EFFECTIVE CONFIG  
--------------------------------------------------------------------  
Do not blur these stages.  
  
PRINCIPLE 5: TRACEABILITY  
--------------------------------------------------------------------  
Every significant value should be explainable back to source layer.  
  
PRINCIPLE 6: CONTRACT-FIRST  
--------------------------------------------------------------------  
Schemas should be defined before usage spreads.  
  
PRINCIPLE 7: FUTURE DOMAIN EXTENSIBILITY  
--------------------------------------------------------------------  
The structure must anticipate new domains, workflows, UI modes, and  
integration bridges.  
  
====================================================================  
7. RECOMMENDED PACKAGE STRUCTURE  
====================================================================  
  
config_sdk/  
  pyproject.toml  
  README.md  
  src/config_sdk/  
    __init__.py  
    version.py  
  
    contracts/  
      __init__.py  
      enums.py  
      source_models.py  
      layer_models.py  
      request_models.py  
      response_models.py  
      metadata_models.py  
      bundle_models.py  
  
    models/  
      __init__.py  
      base_models.py  
      common_models.py  
      runtime_models.py  
      registry_models.py  
      storage_models.py  
      ui_models.py  
      workflow_models.py  
      policy_models.py  
      monitoring_models.py  
      domain_models.py  
  
    loaders/  
      __init__.py  
      base_loader.py  
      yaml_loader.py  
      json_loader.py  
      toml_loader.py  
      dict_loader.py  
      loader_factory.py  
  
    mergers/  
      __init__.py  
      merge_engine.py  
      merge_strategies.py  
      overlay_resolver.py  
  
    resolvers/  
      __init__.py  
      config_stack_resolver.py  
      reference_resolver.py  
      inheritance_resolver.py  
      placeholder_resolver.py  
      effective_config_renderer.py  
  
    validators/  
      __init__.py  
      schema_validator.py  
      cross_field_validator.py  
      bundle_validator.py  
      reference_validator.py  
  
    hashing/  
      __init__.py  
      config_hashing.py  
      fingerprinting.py  
  
    provenance/  
      __init__.py  
      provenance_tracker.py  
      origin_explainer.py  
      config_diff.py  
  
    services/  
      __init__.py  
      config_service.py  
      public_service.py  
  
    exceptions/  
      __init__.py  
      errors.py  
  
    utils/  
      __init__.py  
      io_utils.py  
      normalize.py  
      deep_merge.py  
      path_utils.py  
  
  tests/  
    unit/  
    integration/  
    contract/  
    fixtures/  
  
====================================================================  
8. RECOMMENDED PUBLIC API SURFACE  
====================================================================  
  
Public API should be small, stable, and strongly typed.  
  
PRIMARY PUBLIC FUNCTIONS / SERVICES  
--------------------------------------------------------------------  
1. load_config_source(...)  
2. validate_config(...)  
3. resolve_config_stack(...)  
4. render_effective_config(...)  
5. explain_config_origin(...)  
6. diff_config_bundles(...)  
7. hash_config(...)  
8. get_config_value(...)  
9. validate_bundle(...)  
10. export_effective_config(...)  
  
PRIMARY PUBLIC CLASS  
--------------------------------------------------------------------  
ConfigService  
  
It should be the main entrypoint for downstream SDKs.  
  
====================================================================  
9. MAIN CONTRACTS  
====================================================================  
  
9.1 ConfigSourceRef  
--------------------------------------------------------------------  
Represents an input config source.  
  
FIELDS  
- source_id  
- source_type  
- source_path  
- source_name  
- layer_name  
- priority  
- file_format  
- metadata  
  
EXAMPLE SOURCE TYPES  
- yaml_file  
- json_file  
- toml_file  
- in_memory_dict  
- runtime_override  
  
9.2 ConfigLayer  
--------------------------------------------------------------------  
Represents one config layer after load but before full merge.  
  
FIELDS  
- layer_name  
- priority  
- source_ref  
- raw_content  
- validated_content  
- schema_name  
- metadata  
  
9.3 ConfigBundle  
--------------------------------------------------------------------  
Represents a multi-layer config package.  
  
FIELDS  
- bundle_id  
- bundle_name  
- layers  
- domain_name  
- role_name  
- environment_name  
- project_name  
- bundle_metadata  
  
9.4 EffectiveConfig  
--------------------------------------------------------------------  
Represents final merged config.  
  
FIELDS  
- effective_config_id  
- effective_content  
- config_hash  
- provenance_map  
- layer_order  
- validation_status  
- metadata  
  
9.5 ConfigResolutionRequest  
--------------------------------------------------------------------  
FIELDS  
- bundle_name  
- sources  
- domain_name  
- role_name  
- environment_name  
- project_name  
- runtime_override  
- strict_mode  
- schema_name  
  
9.6 ConfigResolutionResponse  
--------------------------------------------------------------------  
FIELDS  
- status  
- message  
- effective_config  
- warnings  
- errors  
- references  
- provenance_summary  
- hash_info  
  
====================================================================  
10. SHARED ENUMS  
====================================================================  
  
Recommended enums:  
  
- ConfigSourceTypeEnum  
  - YAML_FILE  
  - JSON_FILE  
  - TOML_FILE  
  - IN_MEMORY_DICT  
  - RUNTIME_OVERRIDE  
  
- ConfigLayerNameEnum  
  - BASE  
  - DOMAIN  
  - ROLE  
  - ENVIRONMENT  
  - PROJECT  
  - RUNTIME  
  
- MergeStrategyEnum  
  - DEEP_MERGE  
  - REPLACE  
  - APPEND_UNIQUE  
  - APPEND_ALL  
  - NONE  
  
- ValidationModeEnum  
  - STRICT  
  - LENIENT  
  
- PlaceholderTypeEnum  
  - ENV_VAR  
  - SECRET_REF  
  - REGISTRY_REF  
  - ARTIFACT_REF  
  
====================================================================  
11. INTERNAL MODULE DESIGN  
====================================================================  
  
11.1 loaders  
--------------------------------------------------------------------  
PURPOSE  
- Load raw config from source.  
  
FILES  
- base_loader.py  
- yaml_loader.py  
- json_loader.py  
- toml_loader.py  
- dict_loader.py  
- loader_factory.py  
  
RESPONSIBILITIES  
- file reading  
- parse raw content  
- attach source metadata  
- normalize to common structure  
  
NON-GOALS  
- no deep merging  
- no business validation  
- no policy logic  
  
11.2 mergers  
--------------------------------------------------------------------  
PURPOSE  
- Merge config layers using deterministic precedence.  
  
FILES  
- merge_engine.py  
- merge_strategies.py  
- overlay_resolver.py  
  
RESPONSIBILITIES  
- perform deep merge  
- support field-level merge strategies  
- resolve overlay order  
- produce merged dict before final validation  
  
MERGE RULES  
- dicts deep-merge by default  
- scalar values override lower-priority layers  
- list handling should be configurable per field  
- explicit replace should be supported  
  
11.3 resolvers  
--------------------------------------------------------------------  
PURPOSE  
- Resolve higher-level config stack behavior.  
  
FILES  
- config_stack_resolver.py  
- reference_resolver.py  
- inheritance_resolver.py  
- placeholder_resolver.py  
- effective_config_renderer.py  
  
RESPONSIBILITIES  
- resolve base + overlays  
- resolve references like ${env:VAR_NAME}  
- resolve inheritance patterns if supported  
- render effective final config  
  
11.4 validators  
--------------------------------------------------------------------  
PURPOSE  
- Validate raw, merged, and bundle config.  
  
FILES  
- schema_validator.py  
- cross_field_validator.py  
- bundle_validator.py  
- reference_validator.py  
  
RESPONSIBILITIES  
- schema checks  
- cross-field rules  
- required layer checks  
- invalid reference detection  
  
11.5 hashing  
--------------------------------------------------------------------  
PURPOSE  
- Provide deterministic config fingerprinting.  
  
FILES  
- config_hashing.py  
- fingerprinting.py  
  
RESPONSIBILITIES  
- normalize effective config  
- hash canonical representation  
- enable reproducibility and lineage linking  
  
11.6 provenance  
--------------------------------------------------------------------  
PURPOSE  
- Explain origin of effective config values.  
  
FILES  
- provenance_tracker.py  
- origin_explainer.py  
- config_diff.py  
  
RESPONSIBILITIES  
- map each key to source layer  
- explain overrides  
- diff two effective configs  
  
====================================================================  
12. RECOMMENDED KEY CLASSES  
====================================================================  
  
12.1 BaseConfigLoader  
--------------------------------------------------------------------  
PURPOSE  
- Abstract loader interface.  
  
KEY METHODS  
- load(source_ref) -> ConfigLayer  
  
CHILD CLASSES  
- YamlConfigLoader  
- JsonConfigLoader  
- TomlConfigLoader  
- DictConfigLoader  
  
12.2 LoaderFactory  
--------------------------------------------------------------------  
PURPOSE  
- Return appropriate loader by source type.  
  
KEY METHODS  
- get_loader(source_type)  
  
12.3 MergeEngine  
--------------------------------------------------------------------  
PURPOSE  
- Core merge implementation.  
  
KEY METHODS  
- merge_layers(layers)  
- merge_dicts(base, override, strategy_map=None)  
  
12.4 OverlayResolver  
--------------------------------------------------------------------  
PURPOSE  
- Determine layer precedence and filter relevant layers.  
  
KEY METHODS  
- resolve_layer_order(bundle)  
- select_relevant_layers(bundle, domain, role, env, project)  
  
12.5 ConfigStackResolver  
--------------------------------------------------------------------  
PURPOSE  
- Main internal resolver pipeline.  
  
KEY METHODS  
- resolve(request) -> EffectiveConfig  
  
STEPS  
- load  
- validate raw  
- select layers  
- merge  
- validate merged  
- resolve references  
- hash  
- attach provenance  
  
12.6 PlaceholderResolver  
--------------------------------------------------------------------  
PURPOSE  
- Resolve placeholders.  
  
KEY METHODS  
- resolve_placeholders(config_dict)  
- resolve_value(value)  
  
12.7 SchemaValidator  
--------------------------------------------------------------------  
PURPOSE  
- Validate against Pydantic schemas.  
  
KEY METHODS  
- validate(config_dict, schema_name)  
- validate_layer(layer)  
- validate_effective(config)  
  
12.8 BundleValidator  
--------------------------------------------------------------------  
PURPOSE  
- Validate whole bundle integrity.  
  
KEY METHODS  
- validate_bundle(bundle)  
  
12.9 ProvenanceTracker  
--------------------------------------------------------------------  
PURPOSE  
- Build origin map.  
  
KEY METHODS  
- track_merge(base, override, layer_name)  
- build_provenance_map()  
  
12.10 ConfigService  
--------------------------------------------------------------------  
PURPOSE  
- Main public service for downstream SDKs.  
  
KEY METHODS  
- load_config_source  
- validate_config  
- resolve_config_stack  
- render_effective_config  
- explain_config_origin  
- diff_config_bundles  
- hash_config  
  
====================================================================  
13. RECOMMENDED Pydantic MODEL GROUPS  
====================================================================  
  
13.1 source_models.py  
--------------------------------------------------------------------  
- ConfigSourceRef  
- SourceMetadata  
  
13.2 layer_models.py  
--------------------------------------------------------------------  
- ConfigLayer  
- LayerMetadata  
- LayerSelectionCriteria  
  
13.3 request_models.py  
--------------------------------------------------------------------  
- ConfigResolutionRequest  
- ConfigValidationRequest  
- ConfigDiffRequest  
  
13.4 response_models.py  
--------------------------------------------------------------------  
- ConfigResolutionResponse  
- ConfigValidationResponse  
- ConfigDiffResponse  
  
13.5 metadata_models.py  
--------------------------------------------------------------------  
- ConfigProvenanceEntry  
- ConfigHashInfo  
- EffectiveConfigMetadata  
  
13.6 bundle_models.py  
--------------------------------------------------------------------  
- ConfigBundle  
- EffectiveConfig  
  
====================================================================  
14. CONFIG STACK PRECEDENCE  
====================================================================  
  
Recommended default precedence:  
  
1. BASE  
2. DOMAIN  
3. ROLE  
4. ENVIRONMENT  
5. PROJECT  
6. RUNTIME  
  
EXAMPLE  
--------------------------------------------------------------------  
A reporting threshold may exist in:  
- base config  
- domain overlay for ECL  
- environment overlay for prod  
- runtime override for a single run  
  
The final value should follow the precedence above.  
  
RULES  
--------------------------------------------------------------------  
- Runtime overrides must be explicit and auditable  
- Project overlays should not silently redefine unrelated domains  
- Environment overlays should mostly affect infrastructure/runtime  
  behavior, not business logic, unless intentionally designed  
  
====================================================================  
15. PLACEHOLDER AND REFERENCE RESOLUTION  
====================================================================  
  
Supported future-proof placeholder patterns:  
  
15.1 Environment variable placeholder  
--------------------------------------------------------------------  
${env:MY_VAR}  
  
15.2 Secret reference placeholder  
--------------------------------------------------------------------  
${secret:my_secret_key}  
  
15.3 Registry reference placeholder  
--------------------------------------------------------------------  
${registry:reference_name}  
  
15.4 Artifact reference placeholder  
--------------------------------------------------------------------  
${artifact:artifact_id}  
  
Rules:  
- unresolved placeholders should fail in strict mode  
- unresolved placeholders may warn in lenient mode  
- actual secret fetching can remain pluggable and optional  
  
====================================================================  
16. CONFIG HASHING STRATEGY  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
Config hash is needed for:  
- reproducibility  
- run traceability  
- model lineage  
- audit comparison  
- change detection  
  
RECOMMENDED STRATEGY  
--------------------------------------------------------------------  
1. normalize config into canonical dict  
2. sort keys recursively  
3. remove non-semantic metadata if necessary  
4. serialize deterministically  
5. compute SHA256 hash  
  
OUTPUT  
--------------------------------------------------------------------  
- config_hash  
- hash_algorithm  
- normalized_size  
- maybe short hash alias for display  
  
====================================================================  
17. PROVENANCE AND EXPLAINABILITY  
====================================================================  
  
Every effective config should support explanation such as:  
  
- key path: workflow.review.required  
- effective value: true  
- source layer: domain  
- source file: domains/ecl.yaml  
- overridden lower layer: base/runtime_master.yaml  
  
USE CASES  
--------------------------------------------------------------------  
- debugging unexpected runtime behavior  
- validating why an approval was required  
- comparing UAT vs prod behavior  
- audit explanations  
- controlled config reviews  
  
====================================================================  
18. STANDARD RESPONSE ENVELOPE  
====================================================================  
  
All major public service calls should return:  
  
status  
message  
data  
warnings  
errors  
references  
workflow_hint  
agent_hint  
audit_hint  
observability_hint  
  
FOR config_sdk, typical meanings:  
- references: config bundle id, effective config id, source refs  
- workflow_hint: usually empty, unless used in orchestration stage  
- agent_hint: summary for next step or warning  
- audit_hint: whether config resolution was material enough to audit  
- observability_hint: config resolution event details  
  
====================================================================  
19. PUBLIC SERVICE INTERFACE  
====================================================================  
  
Recommended main service:  
  
ConfigService  
  
KEY METHODS  
--------------------------------------------------------------------  
1. load_config_source(source_ref) -> ConfigLayer  
2. load_bundle(sources, bundle_name, metadata=None) -> ConfigBundle  
3. validate_layer(layer, schema_name=None) -> ConfigValidationResponse  
4. validate_bundle(bundle, schema_name=None) -> ConfigValidationResponse  
5. resolve_config_stack(request) -> ConfigResolutionResponse  
6. render_effective_config(effective_config, fmt="dict") -> dict|json|yaml  
7. explain_config_origin(effective_config, key_path) -> provenance entry  
8. diff_config_bundles(left, right) -> ConfigDiffResponse  
9. hash_config(config_dict) -> ConfigHashInfo  
10. export_effective_config(effective_config, path, fmt="yaml") -> reference  
  
====================================================================  
20. DEPENDENCY RULES  
====================================================================  
  
DIRECT DEPENDENCIES  
--------------------------------------------------------------------  
Allowed external dependencies:  
- pydantic  
- pyyaml  
- tomli or tomllib depending on Python version  
- typing_extensions if needed  
  
OPTIONAL DEPENDENCIES  
--------------------------------------------------------------------  
- orjson for fast serialization  
- deepdiff for advanced diffing if desired  
  
FORBIDDEN DEPENDENCIES  
--------------------------------------------------------------------  
config_sdk should not depend on:  
- workflow_sdk  
- registry_sdk  
- artifact_sdk  
- any domain SDK  
- bridge SDKs  
unless via optional plugins in future  
  
Reason:  
config_sdk must remain at the bottom of dependency graph.  
  
====================================================================  
21. INTEGRATION WITH OTHER SDKS  
====================================================================  
  
21.1 registry_sdk integration  
--------------------------------------------------------------------  
registry_sdk will consume resolved config for:  
- registry backend  
- naming rules  
- metadata fields  
- status mapping  
  
21.2 artifact_sdk integration  
--------------------------------------------------------------------  
artifact_sdk will consume:  
- storage backend config  
- artifact naming config  
- manifest rules  
  
21.3 workflow_sdk integration  
--------------------------------------------------------------------  
workflow_sdk will consume:  
- stage registry  
- stage preconditions  
- routes  
- failure routes  
- role overlays  
- governance controls  
  
21.4 hitl_sdk integration  
--------------------------------------------------------------------  
hitl_sdk will consume:  
- review type definitions  
- action requirements  
- field schema config  
- review state rules  
  
21.5 reporting_sdk integration  
--------------------------------------------------------------------  
reporting_sdk will consume:  
- template config  
- section order  
- rendering style  
- export options  
  
21.6 domain SDK integration  
--------------------------------------------------------------------  
domain SDKs will consume:  
- segmentation rules  
- target definitions  
- scenario config  
- thresholds  
- candidate search spaces  
- package-specific settings  
  
====================================================================  
22. RECOMMENDED FILE FORMATS AND EXAMPLES  
====================================================================  
  
Recommended config file layout at platform level:  
  
configs/  
  base/  
    runtime_master.yaml  
    storage.yaml  
    registry.yaml  
    audit.yaml  
    observability.yaml  
    reporting.yaml  
  
  domains/  
    ecl.yaml  
    pd.yaml  
    lgd.yaml  
    ead.yaml  
    sicr.yaml  
    scorecard.yaml  
    stress.yaml  
  
  roles/  
    developer.yaml  
    validator.yaml  
    governance.yaml  
    approver.yaml  
    monitoring.yaml  
  
  environments/  
    dev.yaml  
    uat.yaml  
    prod.yaml  
  
  projects/  
    project_alpha.yaml  
    project_beta.yaml  
  
  runtime/  
    adhoc_override.yaml  
  
====================================================================  
23. EXAMPLE RESOLUTION FLOW  
====================================================================  
  
Example:  
- base/runtime_master.yaml  
- domains/ecl.yaml  
- roles/validator.yaml  
- environments/prod.yaml  
- projects/project_alpha.yaml  
- runtime_override dict  
  
Flow:  
1. load all sources  
2. validate raw layers  
3. select relevant layers  
4. merge in precedence order  
5. resolve placeholders  
6. validate merged effective config  
7. hash config  
8. build provenance map  
9. return effective config response  
  
====================================================================  
24. EXAMPLE EFFECTIVE CONFIG RESPONSE  
====================================================================  
  
status: success  
message: Effective config resolved successfully  
data:  
  effective_config_id: cfg_eff_001  
  config_hash: abc123...  
  layer_order:  
    - base  
    - domain  
    - role  
    - environment  
    - project  
    - runtime  
  effective_content:  
    workflow:  
      review_required: true  
      approval_required: true  
references:  
  bundle_name: project_alpha_ecl_prod_validator  
warnings: []  
errors: []  
agent_hint:  
  reasoning_summary: Runtime config stack resolved with strict validation.  
  recommended_next_action: resolve_runtime_stack  
  requires_human_review: false  
  safe_to_continue: true  
  
====================================================================  
25. EXCEPTIONS AND ERROR TAXONOMY  
====================================================================  
  
Recommended exception classes:  
  
- ConfigSdkError  
- ConfigLoadError  
- ConfigParseError  
- ConfigValidationError  
- ConfigSchemaError  
- ConfigMergeError  
- ConfigReferenceResolutionError  
- ConfigPlaceholderResolutionError  
- ConfigBundleError  
- ConfigDiffError  
  
Each should support:  
- message  
- source_ref  
- layer_name  
- key_path if available  
- original_exception  
  
====================================================================  
26. TEST STRATEGY  
====================================================================  
  
26.1 Unit tests  
--------------------------------------------------------------------  
Must cover:  
- yaml/json/toml loading  
- merge rules  
- placeholder resolution  
- hashing stability  
- provenance tracking  
- schema validation  
- strict vs lenient modes  
  
26.2 Integration tests  
--------------------------------------------------------------------  
Must cover:  
- full bundle resolution  
- domain + role + env overlays  
- runtime override behavior  
- cross-file validation behavior  
- effective config rendering  
  
26.3 Contract tests  
--------------------------------------------------------------------  
Must cover:  
- public service response schema  
- request/response model compatibility  
- expected exception shapes  
  
26.4 Edge cases  
--------------------------------------------------------------------  
Must cover:  
- missing files  
- duplicate keys  
- invalid placeholders  
- invalid enum values  
- conflicting layers  
- unsupported merge types  
- unresolved required references  
  
====================================================================  
27. PYPROJECT TOML RECOMMENDATION  
====================================================================  
  
Recommended minimal example:  
  
[project]  
name = "config-sdk"  
version = "0.1.0"  
description = "Central configuration SDK for the agentic AI MDLC platform"  
requires-python = ">=3.11"  
dependencies = [  
  "pydantic>=2.6",  
  "PyYAML>=6.0"  
]  
  
[project.optional-dependencies]  
toml = []  
fast = ["orjson>=3.9"]  
diff = ["deepdiff>=7.0"]  
test = [  
  "pytest>=8.0",  
  "pytest-cov>=5.0",  
  "mypy>=1.8"  
]  
  
[build-system]  
requires = ["hatchling"]  
build-backend = "hatchling.build"  
  
====================================================================  
28. IMPLEMENTATION PHASING FOR CONFIG_SDK  
====================================================================  
  
PHASE 1  
--------------------------------------------------------------------  
- base contracts  
- loaders  
- simple merge engine  
- Pydantic validation  
- ConfigService MVP  
  
PHASE 2  
--------------------------------------------------------------------  
- provenance tracking  
- hashing  
- diff support  
- placeholder resolution  
  
PHASE 3  
--------------------------------------------------------------------  
- schema catalog  
- inheritance / advanced overlay features  
- export helpers  
- richer explainability  
  
PHASE 4  
--------------------------------------------------------------------  
- optional plugin points for secret resolvers  
- optional UI/editor integration contracts  
- performance optimization for very large bundles  
  
====================================================================  
29. FUTURE-PROOFING FEATURES  
====================================================================  
  
Recommended future-proof capabilities:  
- pluggable placeholder resolvers  
- pluggable merge strategies by path  
- config schema registry  
- config authoring metadata for UI generation  
- config version migration utilities  
- config deprecation warnings  
- config compatibility checker between SDK versions  
  
====================================================================  
30. ACCEPTANCE CRITERIA  
====================================================================  
  
config_sdk is acceptable when:  
  
1. It can load YAML/JSON/TOML/dict sources reliably.  
2. It can merge base/domain/role/env/project/runtime layers correctly.  
3. It can validate configs strictly with clear errors.  
4. It can return immutable effective config objects.  
5. It can produce deterministic config hashes.  
6. It can explain config value provenance.  
7. It can be consumed cleanly by the next SDKs without leakage of  
   implementation details.  
8. It does not depend on higher-layer SDKs.  
9. It has strong unit and integration test coverage.  
10. Its public service API is stable and contract-driven.  
  
====================================================================  
31. RECOMMENDED NEXT STEP  
====================================================================  
  
Next best artifact:  
--------------------------------------------------------------------  
A full technical design for config_sdk code implementation, including:  
- class-by-class design  
- public method signatures  
- Pydantic models  
- folder-by-folder responsibilities  
- starter code skeleton  
  
====================================================================  
END OF CONFIG_SDK DESIGN SPECIFICATION  
====================================================================  
  
====================================================================  
TECHNICAL DESIGN SPECIFICATION  
CONFIG_SDK CODE IMPLEMENTATION  
AGENTIC AI MDLC / ECL PLATFORM  
DETAILED, COMPREHENSIVE, FUTURE-PROOF  
====================================================================  
  
STATUS  
--------------------------------------------------------------------  
Draft v1.0  
  
PURPOSE  
--------------------------------------------------------------------  
This document translates the config_sdk design into an implementation-  
ready technical specification.  
  
It covers:  
- code architecture  
- class-by-class design  
- public method signatures  
- internal responsibilities  
- Pydantic model structure  
- merge strategy design  
- provenance design  
- hashing design  
- error taxonomy  
- test plan  
- integration hooks with the wider project  
  
This is intended to be directly usable as the implementation reference  
for the config_sdk package.  
  
====================================================================  
1. IMPLEMENTATION OBJECTIVES  
====================================================================  
  
The code implementation must satisfy these platform requirements:  
  
1. Deterministic config resolution  
2. Explicit overlay precedence  
3. Strong validation  
4. Traceable value origin  
5. Reproducible config fingerprints  
6. Clean public API for downstream SDKs  
7. Easy future extension for:  
   - new config domains  
   - new placeholder types  
   - new merge strategies  
   - new bridge consumers  
   - UI-assisted config authoring  
  
====================================================================  
2. PACKAGE LAYOUT  
====================================================================  
  
config_sdk/  
  pyproject.toml  
  README.md  
  
  src/config_sdk/  
    __init__.py  
    version.py  
  
    contracts/  
      __init__.py  
      enums.py  
      source_models.py  
      layer_models.py  
      request_models.py  
      response_models.py  
      metadata_models.py  
      bundle_models.py  
  
    models/  
      __init__.py  
      base_models.py  
      common_models.py  
      runtime_models.py  
      registry_models.py  
      storage_models.py  
      ui_models.py  
      workflow_models.py  
      policy_models.py  
      monitoring_models.py  
      domain_models.py  
      schema_catalog.py  
  
    loaders/  
      __init__.py  
      base_loader.py  
      yaml_loader.py  
      json_loader.py  
      toml_loader.py  
      dict_loader.py  
      loader_factory.py  
  
    mergers/  
      __init__.py  
      merge_engine.py  
      merge_strategies.py  
      overlay_resolver.py  
  
    resolvers/  
      __init__.py  
      config_stack_resolver.py  
      reference_resolver.py  
      placeholder_resolver.py  
      effective_config_renderer.py  
  
    validators/  
      __init__.py  
      schema_validator.py  
      cross_field_validator.py  
      bundle_validator.py  
      reference_validator.py  
  
    hashing/  
      __init__.py  
      config_hashing.py  
      fingerprinting.py  
  
    provenance/  
      __init__.py  
      provenance_tracker.py  
      origin_explainer.py  
      config_diff.py  
  
    services/  
      __init__.py  
      config_service.py  
      public_service.py  
  
    exceptions/  
      __init__.py  
      errors.py  
  
    utils/  
      __init__.py  
      io_utils.py  
      normalize.py  
      deep_merge.py  
      path_utils.py  
      dict_tools.py  
  
  tests/  
    unit/  
    integration/  
    contract/  
    fixtures/  
  
====================================================================  
3. PUBLIC API SURFACE  
====================================================================  
  
The package should expose a deliberately small public API.  
  
3.1 Public imports  
--------------------------------------------------------------------  
Recommended `src/config_sdk/__init__.py` exports:  
  
- ConfigService  
- ConfigResolutionRequest  
- ConfigResolutionResponse  
- ConfigValidationRequest  
- ConfigValidationResponse  
- ConfigDiffRequest  
- ConfigDiffResponse  
- ConfigBundle  
- EffectiveConfig  
- ConfigSourceRef  
- ConfigLayer  
- ConfigSdkError  
- ConfigLoadError  
- ConfigValidationError  
- ConfigMergeError  
- ConfigPlaceholderResolutionError  
  
3.2 Primary public class  
--------------------------------------------------------------------  
ConfigService  
  
This is the main user-facing service and should be enough for most  
downstream SDK integration.  
  
3.3 Public methods  
--------------------------------------------------------------------  
ConfigService.load_config_source(...)  
ConfigService.load_bundle(...)  
ConfigService.validate_layer(...)  
ConfigService.validate_bundle(...)  
ConfigService.resolve_config_stack(...)  
ConfigService.render_effective_config(...)  
ConfigService.explain_config_origin(...)  
ConfigService.diff_config_bundles(...)  
ConfigService.hash_config(...)  
ConfigService.export_effective_config(...)  
  
====================================================================  
4. Pydantic CONTRACT DESIGN  
====================================================================  
  
All contract models should inherit from a shared strict base model.  
  
--------------------------------------------------------------------  
4.1 base model  
--------------------------------------------------------------------  
  
CLASS  
- ConfigSdkBaseModel  
  
RESPONSIBILITY  
- strict parsing  
- forbid unexpected fields by default  
- enable assignment validation  
- consistent serialization behavior  
  
KEY SETTINGS  
- extra="forbid"  
- validate_assignment=True  
- populate_by_name=True  
  
--------------------------------------------------------------------  
4.2 enums.py  
--------------------------------------------------------------------  
  
REQUIRED ENUMS  
  
1. ConfigSourceTypeEnum  
- YAML_FILE  
- JSON_FILE  
- TOML_FILE  
- IN_MEMORY_DICT  
- RUNTIME_OVERRIDE  
  
2. ConfigLayerNameEnum  
- BASE  
- DOMAIN  
- ROLE  
- ENVIRONMENT  
- PROJECT  
- RUNTIME  
  
3. MergeStrategyEnum  
- DEEP_MERGE  
- REPLACE  
- APPEND_UNIQUE  
- APPEND_ALL  
- KEEP_BASE  
- NONE  
  
4. ValidationModeEnum  
- STRICT  
- LENIENT  
  
5. PlaceholderTypeEnum  
- ENV_VAR  
- SECRET_REF  
- REGISTRY_REF  
- ARTIFACT_REF  
  
6. ConfigFormatEnum  
- YAML  
- JSON  
- TOML  
- DICT  
  
7. ConfigStatusEnum  
- LOADED  
- VALIDATED  
- RESOLVED  
- FAILED  
  
--------------------------------------------------------------------  
4.3 source_models.py  
--------------------------------------------------------------------  
  
CLASS  
- ConfigSourceRef  
  
FIELDS  
- source_id: str  
- source_type: ConfigSourceTypeEnum  
- source_name: str  
- source_path: str | None  
- file_format: ConfigFormatEnum | None  
- layer_name: ConfigLayerNameEnum  
- priority: int  
- metadata: dict[str, Any] = {}  
  
USAGE  
- identifies one config source before loading  
  
CLASS  
- SourceMetadata  
  
FIELDS  
- loaded_at: datetime | None  
- file_size: int | None  
- source_checksum: str | None  
- source_tags: list[str] = []  
- owner: str | None  
  
--------------------------------------------------------------------  
4.4 layer_models.py  
--------------------------------------------------------------------  
  
CLASS  
- ConfigLayer  
  
FIELDS  
- layer_id: str  
- layer_name: ConfigLayerNameEnum  
- priority: int  
- source_ref: ConfigSourceRef  
- raw_content: dict[str, Any]  
- validated_content: dict[str, Any] | None  
- schema_name: str | None  
- status: ConfigStatusEnum  
- metadata: dict[str, Any] = {}  
  
USAGE  
- one loaded layer, before and after validation  
  
CLASS  
- LayerSelectionCriteria  
  
FIELDS  
- domain_name: str | None  
- role_name: str | None  
- environment_name: str | None  
- project_name: str | None  
  
--------------------------------------------------------------------  
4.5 metadata_models.py  
--------------------------------------------------------------------  
  
CLASS  
- ConfigProvenanceEntry  
  
FIELDS  
- key_path: str  
- effective_value: Any  
- source_layer: ConfigLayerNameEnum  
- source_name: str | None  
- source_path: str | None  
- overridden_layers: list[str] = []  
- notes: list[str] = []  
  
CLASS  
- ConfigHashInfo  
  
FIELDS  
- config_hash: str  
- hash_algorithm: str  
- normalized_size: int  
- short_hash: str  
  
CLASS  
- EffectiveConfigMetadata  
  
FIELDS  
- bundle_name: str  
- resolved_at: datetime  
- layer_order: list[str]  
- validation_mode: ValidationModeEnum  
- schema_name: str | None  
- metadata: dict[str, Any] = {}  
  
--------------------------------------------------------------------  
4.6 bundle_models.py  
--------------------------------------------------------------------  
  
CLASS  
- ConfigBundle  
  
FIELDS  
- bundle_id: str  
- bundle_name: str  
- layers: list[ConfigLayer]  
- domain_name: str | None  
- role_name: str | None  
- environment_name: str | None  
- project_name: str | None  
- bundle_metadata: dict[str, Any] = {}  
  
CLASS  
- EffectiveConfig  
  
FIELDS  
- effective_config_id: str  
- bundle_id: str  
- bundle_name: str  
- effective_content: dict[str, Any]  
- config_hash_info: ConfigHashInfo  
- provenance_map: dict[str, ConfigProvenanceEntry]  
- metadata: EffectiveConfigMetadata  
- validation_status: ConfigStatusEnum  
  
--------------------------------------------------------------------  
4.7 request_models.py  
--------------------------------------------------------------------  
  
CLASS  
- ConfigResolutionRequest  
  
FIELDS  
- bundle_name: str  
- sources: list[ConfigSourceRef]  
- domain_name: str | None  
- role_name: str | None  
- environment_name: str | None  
- project_name: str | None  
- runtime_override: dict[str, Any] | None  
- validation_mode: ValidationModeEnum = STRICT  
- schema_name: str | None  
- metadata: dict[str, Any] = {}  
  
CLASS  
- ConfigValidationRequest  
  
FIELDS  
- source_ref: ConfigSourceRef | None  
- config_dict: dict[str, Any] | None  
- schema_name: str | None  
- validation_mode: ValidationModeEnum = STRICT  
  
CLASS  
- ConfigDiffRequest  
  
FIELDS  
- left_config: EffectiveConfig | dict[str, Any]  
- right_config: EffectiveConfig | dict[str, Any]  
- include_values: bool = True  
  
--------------------------------------------------------------------  
4.8 response_models.py  
--------------------------------------------------------------------  
  
CLASS  
- ConfigResolutionResponse  
  
FIELDS  
- status: str  
- message: str  
- data: dict[str, Any]  
- warnings: list[dict[str, Any]] = []  
- errors: list[dict[str, Any]] = []  
- references: dict[str, Any] = {}  
- workflow_hint: dict[str, Any] = {}  
- agent_hint: dict[str, Any] = {}  
- audit_hint: dict[str, Any] = {}  
- observability_hint: dict[str, Any] = {}  
  
CLASS  
- ConfigValidationResponse  
  
FIELDS  
- status: str  
- message: str  
- is_valid: bool  
- data: dict[str, Any]  
- warnings: list[dict[str, Any]] = []  
- errors: list[dict[str, Any]] = []  
- references: dict[str, Any] = {}  
  
CLASS  
- ConfigDiffResponse  
  
FIELDS  
- status: str  
- message: str  
- data: dict[str, Any]  
- warnings: list[dict[str, Any]] = []  
- errors: list[dict[str, Any]] = []  
- references: dict[str, Any] = {}  
  
====================================================================  
5. MODEL SCHEMA DESIGN  
====================================================================  
  
The `models/` directory should hold reusable config schemas that other  
SDKs can import or that config_sdk can validate against.  
  
These should not be exhaustive from day one, but should define a stable  
pattern.  
  
5.1 base_models.py  
--------------------------------------------------------------------  
PURPOSE  
- strict shared base models  
- small reusable config fragments  
  
KEY CLASSES  
- StrictConfigModel  
- MergeRuleConfig  
- StorageRefConfig  
- NamedSectionConfig  
  
5.2 common_models.py  
--------------------------------------------------------------------  
PURPOSE  
- common platform-wide config structures  
  
KEY CLASSES  
- LoggingConfig  
- TagsConfig  
- PathConfig  
- TimeoutsConfig  
- RetryConfig  
- IdentityFieldConfig  
  
5.3 runtime_models.py  
--------------------------------------------------------------------  
PURPOSE  
- config relevant to runtime resolution and execution  
  
KEY CLASSES  
- RuntimeMasterConfig  
- RuntimeDefaultsConfig  
- RuntimeBehaviorConfig  
  
5.4 registry_models.py  
--------------------------------------------------------------------  
PURPOSE  
- registry backend and naming config  
  
KEY CLASSES  
- RegistryBackendConfig  
- RegistryEntityConfig  
- RegistryNamingConfig  
  
5.5 storage_models.py  
--------------------------------------------------------------------  
PURPOSE  
- local / S3 storage config  
  
KEY CLASSES  
- LocalStorageConfig  
- S3StorageConfig  
- ArtifactStorageConfig  
  
5.6 ui_models.py  
--------------------------------------------------------------------  
PURPOSE  
- workspace UI mode config, panel defaults, renderer toggles  
  
KEY CLASSES  
- WorkspaceUiConfig  
- ReviewUiConfig  
- DashboardUiConfig  
- FlowUiConfig  
  
5.7 workflow_models.py  
--------------------------------------------------------------------  
PURPOSE  
- stage registry, routing, precondition config  
  
KEY CLASSES  
- StageDefinitionConfig  
- StageRouteConfig  
- StagePreconditionConfig  
- WorkflowControlConfig  
  
5.8 policy_models.py  
--------------------------------------------------------------------  
PURPOSE  
- review, approval, audit, and block behavior config  
  
KEY CLASSES  
- PolicyRuleConfig  
- ReviewRequirementConfig  
- ApprovalRequirementConfig  
- AuditRequirementConfig  
  
5.9 monitoring_models.py  
--------------------------------------------------------------------  
PURPOSE  
- monitoring thresholds, frequencies, annual review config  
  
KEY CLASSES  
- MonitoringMetricConfig  
- MonitoringThresholdConfig  
- MonitoringFrequencyConfig  
  
5.10 domain_models.py  
--------------------------------------------------------------------  
PURPOSE  
- generic domain config containers used by domain SDKs  
  
KEY CLASSES  
- DomainOverlayConfig  
- ModelCandidateConfig  
- SegmentationConfig  
- ScenarioConfig  
- ThresholdConfig  
  
5.11 schema_catalog.py  
--------------------------------------------------------------------  
PURPOSE  
- central schema registry map  
  
KEY CONTENT  
- SCHEMA_CATALOG: dict[str, type[BaseModel]]  
  
EXAMPLE  
- "runtime_master" -> RuntimeMasterConfig  
- "workflow" -> WorkflowControlConfig  
- "policy" -> PolicyRuleConfig  
- "domain_overlay" -> DomainOverlayConfig  
  
====================================================================  
6. LOADER IMPLEMENTATION DESIGN  
====================================================================  
  
6.1 BaseConfigLoader  
--------------------------------------------------------------------  
FILE  
- loaders/base_loader.py  
  
TYPE  
- abstract base class  
  
RESPONSIBILITY  
- define common interface for all loaders  
  
KEY METHODS  
- load(source_ref: ConfigSourceRef) -> ConfigLayer  
- _read_raw_content(source_ref: ConfigSourceRef) -> dict[str, Any]  
  
NOTES  
- should not validate business schema  
- should only load and normalize  
  
6.2 YamlConfigLoader  
--------------------------------------------------------------------  
FILE  
- loaders/yaml_loader.py  
  
RESPONSIBILITY  
- parse YAML safely  
- normalize empty docs to {}  
- attach metadata  
  
DEPENDENCIES  
- PyYAML  
  
6.3 JsonConfigLoader  
--------------------------------------------------------------------  
FILE  
- loaders/json_loader.py  
  
RESPONSIBILITY  
- parse JSON safely  
- preserve structure deterministically  
  
6.4 TomlConfigLoader  
--------------------------------------------------------------------  
FILE  
- loaders/toml_loader.py  
  
RESPONSIBILITY  
- parse TOML safely  
- support standard Python tomllib where possible  
  
6.5 DictConfigLoader  
--------------------------------------------------------------------  
FILE  
- loaders/dict_loader.py  
  
RESPONSIBILITY  
- accept in-memory dict  
- normalize as if loaded from file  
  
6.6 LoaderFactory  
--------------------------------------------------------------------  
FILE  
- loaders/loader_factory.py  
  
RESPONSIBILITY  
- choose correct loader by source_type  
  
KEY METHODS  
- get_loader(source_type: ConfigSourceTypeEnum) -> BaseConfigLoader  
  
====================================================================  
7. MERGE ENGINE DESIGN  
====================================================================  
  
7.1 MergeEngine  
--------------------------------------------------------------------  
FILE  
- mergers/merge_engine.py  
  
RESPONSIBILITY  
- central deep merge logic  
- enforce deterministic precedence  
- support strategy mapping by key path  
  
KEY METHODS  
- merge_layers(layers: list[ConfigLayer], strategy_map: dict[str, MergeStrategyEnum] | None = None) -> tuple[dict[str, Any], dict[str, Any]]  
- merge_dicts(base: dict[str, Any], override: dict[str, Any], strategy_map: dict[str, MergeStrategyEnum] | None = None, path_prefix: str = "") -> dict[str, Any]  
  
RETURN SHAPE  
- merged effective dict  
- merge provenance seed data  
  
MERGE RULES  
- dict + dict => deep merge by default  
- scalar override => replace base  
- list + list => controlled by strategy  
- None in override => configurable, recommended replace unless rule says KEEP_BASE  
  
7.2 MergeStrategies  
--------------------------------------------------------------------  
FILE  
- mergers/merge_strategies.py  
  
RESPONSIBILITY  
- implement concrete merge operations  
  
FUNCTIONS  
- merge_replace(base, override)  
- merge_deep(base, override)  
- merge_append_unique(base, override)  
- merge_append_all(base, override)  
- merge_keep_base(base, override)  
  
7.3 OverlayResolver  
--------------------------------------------------------------------  
FILE  
- mergers/overlay_resolver.py  
  
RESPONSIBILITY  
- sort and filter layers  
  
KEY METHODS  
- resolve_layer_order(bundle: ConfigBundle) -> list[ConfigLayer]  
- select_relevant_layers(bundle: ConfigBundle, request: ConfigResolutionRequest) -> list[ConfigLayer]  
  
RULES  
- always sort by priority first  
- allow optional filters by layer name  
- runtime overrides should come last  
- project layer optional  
- role/domain/environment may be absent  
  
====================================================================  
8. RESOLVER PIPELINE DESIGN  
====================================================================  
  
8.1 ConfigStackResolver  
--------------------------------------------------------------------  
FILE  
- resolvers/config_stack_resolver.py  
  
RESPONSIBILITY  
- orchestrate the full resolution pipeline  
  
KEY METHODS  
- resolve(request: ConfigResolutionRequest) -> EffectiveConfig  
- load_sources(sources: list[ConfigSourceRef]) -> list[ConfigLayer]  
- build_bundle(request: ConfigResolutionRequest, layers: list[ConfigLayer]) -> ConfigBundle  
  
PIPELINE  
1. load raw layers  
2. validate raw layer structure if schema known  
3. build bundle  
4. select relevant layers  
5. merge layers  
6. resolve placeholders and references  
7. validate effective config  
8. hash config  
9. build provenance map  
10. produce EffectiveConfig  
  
8.2 PlaceholderResolver  
--------------------------------------------------------------------  
FILE  
- resolvers/placeholder_resolver.py  
  
RESPONSIBILITY  
- resolve placeholders in scalar strings and nested structures  
  
KEY METHODS  
- resolve_placeholders(config_dict: dict[str, Any], strict_mode: bool = True) -> dict[str, Any]  
- resolve_value(value: Any) -> Any  
  
SUPPORTED PLACEHOLDERS  
- ${env:NAME}  
- ${secret:KEY}  
- ${registry:REF}  
- ${artifact:ID}  
  
IMPLEMENTATION NOTE  
- only env placeholder needs full initial implementation  
- others may be implemented via pluggable adapters returning unresolved warning unless adapter configured  
  
8.3 ReferenceResolver  
--------------------------------------------------------------------  
FILE  
- resolvers/reference_resolver.py  
  
RESPONSIBILITY  
- resolve internal references across config sections if needed  
  
EXAMPLE  
- ref to shared section in same config bundle  
- named config templates  
  
KEY METHODS  
- resolve_internal_refs(config_dict: dict[str, Any]) -> dict[str, Any]  
  
8.4 EffectiveConfigRenderer  
--------------------------------------------------------------------  
FILE  
- resolvers/effective_config_renderer.py  
  
RESPONSIBILITY  
- render effective config in required output format  
  
KEY METHODS  
- render_dict(effective_config: EffectiveConfig) -> dict[str, Any]  
- render_json(effective_config: EffectiveConfig) -> str  
- render_yaml(effective_config: EffectiveConfig) -> str  
  
====================================================================  
9. VALIDATOR DESIGN  
====================================================================  
  
9.1 SchemaValidator  
--------------------------------------------------------------------  
FILE  
- validators/schema_validator.py  
  
RESPONSIBILITY  
- validate dicts against registered Pydantic schemas  
  
KEY METHODS  
- validate(config_dict: dict[str, Any], schema_name: str | None) -> dict[str, Any]  
- get_schema(schema_name: str) -> type[BaseModel]  
  
RETURN  
- validated normalized dict  
  
9.2 CrossFieldValidator  
--------------------------------------------------------------------  
FILE  
- validators/cross_field_validator.py  
  
RESPONSIBILITY  
- project-level semantic rules beyond plain schema shape  
  
EXAMPLES  
- approval_required cannot coexist with auto_continue_allowed  
- list of routes must target known stages  
- storage backend and path requirements aligned  
  
KEY METHODS  
- validate(config_dict: dict[str, Any], schema_name: str | None) -> list[dict[str, Any]]  
  
9.3 BundleValidator  
--------------------------------------------------------------------  
FILE  
- validators/bundle_validator.py  
  
RESPONSIBILITY  
- validate config bundle consistency  
  
KEY METHODS  
- validate_bundle(bundle: ConfigBundle, schema_name: str | None) -> list[dict[str, Any]]  
  
CHECKS  
- duplicate layer priorities  
- missing required base layer  
- invalid source/layer pairing  
- duplicate source ids  
- empty bundle  
  
9.4 ReferenceValidator  
--------------------------------------------------------------------  
FILE  
- validators/reference_validator.py  
  
RESPONSIBILITY  
- detect unresolved placeholders/references  
  
KEY METHODS  
- validate_references(config_dict: dict[str, Any], strict_mode: bool = True) -> list[dict[str, Any]]  
  
====================================================================  
10. HASHING AND FINGERPRINTING  
====================================================================  
  
10.1 ConfigHashing  
--------------------------------------------------------------------  
FILE  
- hashing/config_hashing.py  
  
RESPONSIBILITY  
- deterministic hash generation  
  
KEY METHODS  
- hash_config(config_dict: dict[str, Any]) -> ConfigHashInfo  
- canonical_serialize(config_dict: dict[str, Any]) -> bytes  
  
RULES  
- recursively sort keys  
- remove fields explicitly marked non-semantic if configured  
- stable numeric/string serialization  
  
10.2 Fingerprinting  
--------------------------------------------------------------------  
FILE  
- hashing/fingerprinting.py  
  
RESPONSIBILITY  
- user-facing short aliases and fingerprint helpers  
  
KEY METHODS  
- build_short_hash(config_hash: str, length: int = 12) -> str  
- build_bundle_fingerprint(bundle_name: str, config_hash: str) -> str  
  
====================================================================  
11. PROVENANCE DESIGN  
====================================================================  
  
11.1 ProvenanceTracker  
--------------------------------------------------------------------  
FILE  
- provenance/provenance_tracker.py  
  
RESPONSIBILITY  
- build key-level source origin map during merge  
  
KEY METHODS  
- initialize_with_base(base_layer_name: str, base_dict: dict[str, Any]) -> None  
- record_override(key_path: str, layer_name: str, source_name: str | None, source_path: str | None, effective_value: Any, previous_layer: str | None) -> None  
- build_map() -> dict[str, ConfigProvenanceEntry]  
  
IMPORTANT NOTE  
- merge engine should emit enough callbacks or events for provenance tracking  
  
11.2 OriginExplainer  
--------------------------------------------------------------------  
FILE  
- provenance/origin_explainer.py  
  
RESPONSIBILITY  
- query provenance for one key path or subtree  
  
KEY METHODS  
- explain_key(effective_config: EffectiveConfig, key_path: str) -> ConfigProvenanceEntry | None  
- explain_prefix(effective_config: EffectiveConfig, prefix: str) -> list[ConfigProvenanceEntry]  
  
11.3 ConfigDiff  
--------------------------------------------------------------------  
FILE  
- provenance/config_diff.py  
  
RESPONSIBILITY  
- compare effective configs  
  
KEY METHODS  
- diff(left: EffectiveConfig | dict[str, Any], right: EffectiveConfig | dict[str, Any], include_values: bool = True) -> dict[str, Any]  
  
OUTPUT CATEGORIES  
- added  
- removed  
- changed  
- unchanged_count  
- summary  
  
====================================================================  
12. EXCEPTION DESIGN  
====================================================================  
  
FILE  
- exceptions/errors.py  
  
CLASS HIERARCHY  
--------------------------------------------------------------------  
- ConfigSdkError(Exception)  
  - ConfigLoadError(ConfigSdkError)  
  - ConfigParseError(ConfigSdkError)  
  - ConfigValidationError(ConfigSdkError)  
  - ConfigSchemaError(ConfigSdkError)  
  - ConfigMergeError(ConfigSdkError)  
  - ConfigPlaceholderResolutionError(ConfigSdkError)  
  - ConfigBundleError(ConfigSdkError)  
  - ConfigDiffError(ConfigSdkError)  
  
COMMON ATTRIBUTES  
- message  
- source_ref: ConfigSourceRef | None  
- layer_name: str | None  
- key_path: str | None  
- original_exception: Exception | None  
- metadata: dict[str, Any]  
  
METHODS  
- to_dict() -> dict[str, Any]  
  
====================================================================  
13. SERVICE LAYER DESIGN  
====================================================================  
  
13.1 ConfigService  
--------------------------------------------------------------------  
FILE  
- services/config_service.py  
  
RESPONSIBILITY  
- primary facade service for all downstream SDK use  
  
DEPENDENCIES  
- LoaderFactory  
- ConfigStackResolver  
- SchemaValidator  
- BundleValidator  
- EffectiveConfigRenderer  
- OriginExplainer  
- ConfigDiff  
- ConfigHashing  
  
KEY METHODS AND SIGNATURES  
--------------------------------------------------------------------  
1.  
load_config_source(  
    self,  
    source_ref: ConfigSourceRef,  
) -> ConfigLayer  
  
2.  
load_bundle(  
    self,  
    sources: list[ConfigSourceRef],  
    bundle_name: str,  
    domain_name: str | None = None,  
    role_name: str | None = None,  
    environment_name: str | None = None,  
    project_name: str | None = None,  
    metadata: dict[str, Any] | None = None,  
) -> ConfigBundle  
  
3.  
validate_layer(  
    self,  
    layer: ConfigLayer,  
    schema_name: str | None = None,  
    validation_mode: ValidationModeEnum = ValidationModeEnum.STRICT,  
) -> ConfigValidationResponse  
  
4.  
validate_bundle(  
    self,  
    bundle: ConfigBundle,  
    schema_name: str | None = None,  
    validation_mode: ValidationModeEnum = ValidationModeEnum.STRICT,  
) -> ConfigValidationResponse  
  
5.  
resolve_config_stack(  
    self,  
    request: ConfigResolutionRequest,  
) -> ConfigResolutionResponse  
  
6.  
render_effective_config(  
    self,  
    effective_config: EffectiveConfig,  
    fmt: str = "dict",  
) -> dict[str, Any] | str  
  
7.  
explain_config_origin(  
    self,  
    effective_config: EffectiveConfig,  
    key_path: str,  
) -> dict[str, Any]  
  
8.  
diff_config_bundles(  
    self,  
    request: ConfigDiffRequest,  
) -> ConfigDiffResponse  
  
9.  
hash_config(  
    self,  
    config_dict: dict[str, Any],  
) -> ConfigHashInfo  
  
10.  
export_effective_config(  
    self,  
    effective_config: EffectiveConfig,  
    path: str,  
    fmt: str = "yaml",  
) -> dict[str, Any]  
  
13.2 PublicService alias  
--------------------------------------------------------------------  
FILE  
- services/public_service.py  
  
PURPOSE  
- optional alias for `ConfigService`  
- future place for backward-compatible facades  
  
====================================================================  
14. STANDARD RESPONSE SHAPE IMPLEMENTATION  
====================================================================  
  
All service responses should follow a stable dict/Pydantic envelope.  
  
CONFIG RESOLUTION RESPONSE  
--------------------------------------------------------------------  
status  
message  
data:  
  effective_config  
  effective_config_id  
  config_hash  
  layer_order  
warnings  
errors  
references:  
  bundle_name  
  bundle_id  
  source_ids  
agent_hint:  
  reasoning_summary  
  recommended_next_action  
  safe_to_continue  
audit_hint  
observability_hint  
  
CONFIG VALIDATION RESPONSE  
--------------------------------------------------------------------  
status  
message  
is_valid  
data:  
  schema_name  
  validation_mode  
warnings  
errors  
references  
  
CONFIG DIFF RESPONSE  
--------------------------------------------------------------------  
status  
message  
data:  
  summary  
  added  
  removed  
  changed  
warnings  
errors  
references  
  
====================================================================  
15. DETAILED METHOD BEHAVIOR  
====================================================================  
  
15.1 load_config_source  
--------------------------------------------------------------------  
FLOW  
1. choose loader by source type  
2. load raw content  
3. construct ConfigLayer with status=LOADED  
4. attach source metadata if available  
5. return layer  
  
FAILURE MODES  
- file not found  
- invalid parse  
- unsupported source type  
  
15.2 load_bundle  
--------------------------------------------------------------------  
FLOW  
1. load each source via load_config_source  
2. create ConfigBundle  
3. sort layers by priority  
4. return bundle  
  
FAILURE MODES  
- duplicate source ids  
- empty source list  
- invalid layer priorities  
  
15.3 validate_layer  
--------------------------------------------------------------------  
FLOW  
1. validate raw_content against schema if provided  
2. if valid, populate validated_content  
3. update status=VALIDATED  
4. return validation response  
  
15.4 validate_bundle  
--------------------------------------------------------------------  
FLOW  
1. run structural bundle checks  
2. validate each layer  
3. return combined validation result  
  
15.5 resolve_config_stack  
--------------------------------------------------------------------  
FLOW  
1. build or load bundle from request sources  
2. add runtime override layer if present  
3. validate bundle  
4. select relevant layers  
5. merge layers  
6. resolve placeholders  
7. resolve references  
8. validate merged effective config  
9. hash effective config  
10. build provenance map  
11. construct EffectiveConfig  
12. return response  
  
15.6 render_effective_config  
--------------------------------------------------------------------  
FLOW  
- dict => return raw effective dict  
- json => deterministic JSON string  
- yaml => YAML string  
- future: toml if needed  
  
15.7 explain_config_origin  
--------------------------------------------------------------------  
FLOW  
1. inspect provenance map  
2. return exact source detail for key  
3. if not found, return informative empty response  
  
15.8 diff_config_bundles  
--------------------------------------------------------------------  
FLOW  
1. normalize both configs  
2. compare recursively  
3. categorize differences  
4. return structured diff response  
  
15.9 export_effective_config  
--------------------------------------------------------------------  
FLOW  
1. render to target format  
2. write to path  
3. return file reference metadata  
  
====================================================================  
16. INTEGRATION WITH PROJECT-WIDE ARCHITECTURE  
====================================================================  
  
16.1 workflow_sdk integration  
--------------------------------------------------------------------  
workflow_sdk should call config_sdk to resolve:  
- stage registry  
- stage tool matrix  
- stage preconditions  
- routing  
- environment-specific behavior  
  
It should never reimplement config merging itself.  
  
16.2 policy_sdk integration  
--------------------------------------------------------------------  
policy_sdk should consume effective policy config only.  
config_sdk should not evaluate policy, only resolve its config.  
  
16.3 jupyter_bridge integration  
--------------------------------------------------------------------  
jupyter_bridge may use config_sdk to resolve:  
- workspace UI defaults  
- review shell settings  
- environment-specific frontend/backend toggles  
  
16.4 agent_bridge integration  
--------------------------------------------------------------------  
agent_bridge may use config_sdk to:  
- resolve agent-safe tool policies  
- choose domain overlay  
- inject runtime overrides  
  
16.5 domain SDK integration  
--------------------------------------------------------------------  
Each domain SDK should request resolved config by schema or section,  
such as:  
- `pd_modeling`  
- `lgd_workout`  
- `ecl_scenario`  
- `monitoring_thresholds`  
  
This keeps domain SDKs decoupled from raw config layering.  
  
====================================================================  
17. RECOMMENDED SCHEMA CATALOG STRATEGY  
====================================================================  
  
SCHEMA CATALOG SHOULD SUPPORT  
--------------------------------------------------------------------  
- global schema lookup by name  
- easy registration of new schemas  
- separation between:  
  - platform schemas  
  - domain schemas  
  - project-specific extension schemas  
  
RECOMMENDED PATTERN  
--------------------------------------------------------------------  
SCHEMA_CATALOG = {  
  "runtime_master": RuntimeMasterConfig,  
  "workflow": WorkflowControlConfig,  
  "registry": RegistryBackendConfig,  
  "storage": ArtifactStorageConfig,  
  "policy": PolicyRuleConfig,  
  "ui": WorkspaceUiConfig,  
  "monitoring": MonitoringMetricConfig,  
  "domain_overlay": DomainOverlayConfig,  
}  
  
FUTURE-PROOF EXTENSION  
--------------------------------------------------------------------  
Allow registration such as:  
register_schema("custom_project_schema", CustomProjectConfig)  
  
====================================================================  
18. PERFORMANCE CONSIDERATIONS  
====================================================================  
  
18.1 Caching  
--------------------------------------------------------------------  
Add optional caching for:  
- file loads  
- parsed layers  
- resolved bundles by fingerprint  
  
Do not enable hidden mutable cache behavior by default.  
Cache should be explicit and invalidatable.  
  
18.2 Large configs  
--------------------------------------------------------------------  
For large enterprise config packs:  
- avoid repeated re-serialization  
- normalize once where possible  
- reuse hash-ready canonical structures carefully  
  
18.3 Lazy provenance detail  
--------------------------------------------------------------------  
If config becomes very large, provenance can be generated in either:  
- eager mode for full explainability  
- lazy mode for performance-sensitive runs  
  
====================================================================  
19. TEST PLAN  
====================================================================  
  
19.1 Unit tests by module  
--------------------------------------------------------------------  
loaders/  
- load yaml file  
- load json file  
- load toml file  
- load dict source  
- bad path handling  
- parse error handling  
  
mergers/  
- deep merge nested dicts  
- replace scalar  
- append unique list  
- append all list  
- keep base strategy  
- path-specific strategy  
  
validators/  
- valid schema  
- invalid schema  
- unknown key blocked  
- strict vs lenient behavior  
- cross-field failure  
  
resolvers/  
- placeholder env resolution  
- unresolved placeholder strict fail  
- unresolved placeholder lenient warn  
- internal reference resolution  
- runtime override injection  
  
hashing/  
- deterministic hash unchanged for same config  
- changed value changes hash  
- key order does not affect hash  
  
provenance/  
- base value origin  
- overridden value origin  
- multiple overrides tracked  
- key prefix explanation  
- diff categories  
  
services/  
- load bundle  
- validate bundle  
- resolve stack  
- explain origin  
- render yaml/json/dict  
- export file  
  
19.2 Integration tests  
--------------------------------------------------------------------  
Test full flow:  
1. base + domain + role + environment + project + runtime  
2. schema validation  
3. merge  
4. placeholder resolution  
5. hash  
6. provenance  
  
Example scenarios:  
- ecl prod validator config  
- pd dev developer config  
- monitoring prod governance config  
  
19.3 Contract tests  
--------------------------------------------------------------------  
Ensure:  
- all response envelopes conform  
- public methods accept and return expected shapes  
- exception to_dict payloads are stable  
  
====================================================================  
20. MINIMUM VIABLE IMPLEMENTATION ORDER  
====================================================================  
  
PHASE 1  
--------------------------------------------------------------------  
- contracts/enums  
- contracts/source/layer/request/response/bundle models  
- base loaders  
- loader factory  
- simple schema validator  
- merge engine  
- config service MVP  
- tests for core loading + merge + validation  
  
PHASE 2  
--------------------------------------------------------------------  
- placeholder resolver  
- config hashing  
- provenance tracker  
- origin explainer  
- diff module  
- integration tests  
  
PHASE 3  
--------------------------------------------------------------------  
- schema catalog growth  
- reference resolver  
- export helpers  
- performance improvements  
- plugin hooks for external placeholder resolvers  
  
====================================================================  
21. RECOMMENDED PYPROJECT.TOML  
====================================================================  
  
[project]  
name = "config-sdk"  
version = "0.1.0"  
description = "Central configuration SDK for the agentic AI MDLC platform"  
requires-python = ">=3.11"  
dependencies = [  
  "pydantic>=2.6",  
  "PyYAML>=6.0"  
]  
  
[project.optional-dependencies]  
toml = []  
fast = ["orjson>=3.9"]  
diff = ["deepdiff>=7.0"]  
test = [  
  "pytest>=8.0",  
  "pytest-cov>=5.0",  
  "mypy>=1.8"  
]  
  
[build-system]  
requires = ["hatchling"]  
build-backend = "hatchling.build"  
  
====================================================================  
22. ACCEPTANCE CRITERIA  
====================================================================  
  
config_sdk implementation is acceptable when:  
  
1. It can load all supported source formats.  
2. It can construct bundles from multiple layers.  
3. It can validate configs against named schemas.  
4. It can merge overlays in deterministic precedence.  
5. It can resolve runtime overrides safely.  
6. It can resolve placeholders with strict/lenient modes.  
7. It can produce a deterministic config hash.  
8. It can explain where any effective key came from.  
9. It can diff two effective configs clearly.  
10. It integrates cleanly with the next SDKs without circular design.  
  
====================================================================  
23. RECOMMENDED NEXT STEP  
====================================================================  
  
Next best artifact:  
--------------------------------------------------------------------  
A code skeleton for config_sdk, including:  
- Pydantic models  
- loader classes  
- merge engine  
- config service  
- exception classes  
- starter tests  
  
====================================================================  
END OF CONFIG_SDK TECHNICAL DESIGN SPECIFICATION  
====================================================================  
  
# ================================================================  
# ENHANCED CONFIG_SDK CODE SKELETON  
# AGENTIC AI MDLC / ECL PLATFORM  
# VALIDATION-GRADE / HUMAN-TRACEABLE / FUTURE-PROOF  
# ================================================================  
  
config_sdk/  
  pyproject.toml  
  src/config_sdk/  
    __init__.py  
    version.py  
  
    contracts/  
      __init__.py  
      enums.py  
      source_models.py  
      layer_models.py  
      request_models.py  
      response_models.py  
      metadata_models.py  
      bundle_models.py  
      actor_models.py  
      agent_models.py  
      change_models.py  
      reasoning_models.py  
      review_models.py  
      decision_models.py  
      trace_models.py  
      snapshot_models.py  
      evidence_models.py  
  
    models/  
      __init__.py  
      base_models.py  
      common_models.py  
      schema_catalog.py  
  
    loaders/  
      __init__.py  
      base_loader.py  
      yaml_loader.py  
      json_loader.py  
      toml_loader.py  
      dict_loader.py  
      loader_factory.py  
  
    mergers/  
      __init__.py  
      merge_strategies.py  
      merge_engine.py  
      overlay_resolver.py  
  
    resolvers/  
      __init__.py  
      placeholder_resolver.py  
      reference_resolver.py  
      effective_config_renderer.py  
      config_stack_resolver.py  
  
    validators/  
      __init__.py  
      schema_validator.py  
      cross_field_validator.py  
      bundle_validator.py  
      reference_validator.py  
      governance_validator.py  
      trace_validator.py  
  
    hashing/  
      __init__.py  
      config_hashing.py  
      fingerprinting.py  
  
    provenance/  
      __init__.py  
      provenance_tracker.py  
      origin_explainer.py  
      config_diff.py  
  
    governance/  
      __init__.py  
      base_repository.py  
      reasoning_repository.py  
      review_repository.py  
      decision_repository.py  
      change_repository.py  
      trace_repository.py  
      snapshot_repository.py  
      evidence_repository.py  
      governance_service.py  
      trace_service.py  
      snapshot_service.py  
      query_service.py  
  
    services/  
      __init__.py  
      config_service.py  
      public_service.py  
  
    exceptions/  
      __init__.py  
      errors.py  
  
    utils/  
      __init__.py  
      io_utils.py  
      normalize.py  
      deep_merge.py  
      path_utils.py  
      dict_tools.py  
      ids.py  
      time_utils.py  
      serialization.py  
  
  tests/  
    unit/  
    integration/  
    contract/  
    governance/  
  
  
# ================================================================  
# FILE: src/config_sdk/version.py  
# ================================================================  
  
__version__ = "0.3.0"  
  
  
# ================================================================  
# FILE: src/config_sdk/models/base_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from pydantic import BaseModel, ConfigDict  
  
  
class ConfigSdkBaseModel(BaseModel):  
    model_config = ConfigDict(  
        extra="forbid",  
        validate_assignment=True,  
        populate_by_name=True,  
        frozen=False,  
    )  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/enums.py  
# ================================================================  
  
from __future__ import annotations  
  
from enum import Enum  
  
  
class ConfigSourceTypeEnum(str, Enum):  
    YAML_FILE = "yaml_file"  
    JSON_FILE = "json_file"  
    TOML_FILE = "toml_file"  
    IN_MEMORY_DICT = "in_memory_dict"  
    RUNTIME_OVERRIDE = "runtime_override"  
  
  
class ConfigLayerNameEnum(str, Enum):  
    BASE = "base"  
    DOMAIN = "domain"  
    ROLE = "role"  
    ENVIRONMENT = "environment"  
    PROJECT = "project"  
    RUNTIME = "runtime"  
  
  
class MergeStrategyEnum(str, Enum):  
    DEEP_MERGE = "deep_merge"  
    REPLACE = "replace"  
    APPEND_UNIQUE = "append_unique"  
    APPEND_ALL = "append_all"  
    KEEP_BASE = "keep_base"  
    NONE = "none"  
  
  
class ValidationModeEnum(str, Enum):  
    STRICT = "strict"  
    LENIENT = "lenient"  
  
  
class PlaceholderTypeEnum(str, Enum):  
    ENV_VAR = "env_var"  
    SECRET_REF = "secret_ref"  
    REGISTRY_REF = "registry_ref"  
    ARTIFACT_REF = "artifact_ref"  
  
  
class ConfigFormatEnum(str, Enum):  
    YAML = "yaml"  
    JSON = "json"  
    TOML = "toml"  
    DICT = "dict"  
  
  
class ConfigStatusEnum(str, Enum):  
    LOADED = "loaded"  
    VALIDATED = "validated"  
    RESOLVED = "resolved"  
    FAILED = "failed"  
  
  
class ActorTypeEnum(str, Enum):  
    HUMAN = "human"  
    AGENT = "agent"  
    SYSTEM = "system"  
  
  
class AuthorityLevelEnum(str, Enum):  
    DRAFT = "draft"  
    REVIEW = "review"  
    APPROVE = "approve"  
    OVERRIDE = "override"  
    EMERGENCY_OVERRIDE = "emergency_override"  
  
  
class ChangeTypeEnum(str, Enum):  
    ADD = "add"  
    UPDATE = "update"  
    REMOVE = "remove"  
    REPLACE = "replace"  
    OVERRIDE = "override"  
    EXCEPTION = "exception"  
  
  
class MaterialityEnum(str, Enum):  
    INFORMATIONAL = "informational"  
    NON_MATERIAL = "non_material"  
    MATERIAL = "material"  
    CRITICAL = "critical"  
  
  
class ReviewStatusEnum(str, Enum):  
    OPEN = "open"  
    RESPONDED = "responded"  
    CLOSED = "closed"  
    ESCALATED = "escalated"  
  
  
class ReviewResponseTypeEnum(str, Enum):  
    CONCUR = "concur"  
    CHALLENGE = "challenge"  
    REQUEST_CLARIFICATION = "request_clarification"  
    CONDITIONAL_ACCEPT = "conditional_accept"  
    REJECT = "reject"  
    NOTE = "note"  
  
  
class ResolutionStatusEnum(str, Enum):  
    OPEN = "open"  
    PARTIALLY_RESOLVED = "partially_resolved"  
    RESOLVED = "resolved"  
    REJECTED = "rejected"  
    SUPERSEDED = "superseded"  
  
  
class DecisionStatusEnum(str, Enum):  
    PROPOSED = "proposed"  
    APPROVED = "approved"  
    REJECTED = "rejected"  
    SUPERSEDED = "superseded"  
    WITHDRAWN = "withdrawn"  
  
  
class DecisionTypeEnum(str, Enum):  
    CONFIG_CHANGE = "config_change"  
    CONFIG_EXCEPTION = "config_exception"  
    PLACEHOLDER_OVERRIDE = "placeholder_override"  
    MERGE_POLICY_OVERRIDE = "merge_policy_override"  
    SCHEMA_EXCEPTION = "schema_exception"  
    RELEASE_APPROVAL = "release_approval"  
  
  
class DecisionBasisTypeEnum(str, Enum):  
    POLICY_BASED = "policy_based"  
    EXPERT_JUDGMENT = "expert_judgment"  
    EXCEPTION_HANDLING = "exception_handling"  
    COMPATIBILITY = "compatibility"  
    OPERATIONAL_CONSTRAINT = "operational_constraint"  
    RELEASE_GATE = "release_gate"  
    TEMPORARY_OVERRIDE = "temporary_override"  
    RISK_MITIGATION = "risk_mitigation"  
  
  
class TimelineEventTypeEnum(str, Enum):  
    BUNDLE_CREATED = "bundle_created"  
    CONFIG_RESOLVED = "config_resolved"  
    REASONING_ADDED = "reasoning_added"  
    CHANGE_SET_CREATED = "change_set_created"  
    REVIEW_REQUESTED = "review_requested"  
    REVIEW_RESPONDED = "review_responded"  
    DECISION_RECORDED = "decision_recorded"  
    DECISION_SUPERSEDED = "decision_superseded"  
    SNAPSHOT_CREATED = "snapshot_created"  
    SNAPSHOT_EXPORTED = "snapshot_exported"  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/source_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from datetime import datetime  
from typing import Any  
  
from pydantic import Field, field_validator  
  
from config_sdk.contracts.enums import (  
    ConfigFormatEnum,  
    ConfigLayerNameEnum,  
    ConfigSourceTypeEnum,  
)  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class SourceMetadata(ConfigSdkBaseModel):  
    loaded_at: datetime | None = None  
    file_size: int | None = None  
    source_checksum: str | None = None  
    source_tags: list[str] = Field(default_factory=list)  
    owner: str | None = None  
  
  
class ConfigSourceRef(ConfigSdkBaseModel):  
    source_id: str  
    source_type: ConfigSourceTypeEnum  
    source_name: str  
    source_path: str | None = None  
    file_format: ConfigFormatEnum | None = None  
    layer_name: ConfigLayerNameEnum  
    priority: int  
    metadata: dict[str, Any] = Field(default_factory=dict)  
  
    @field_validator("source_id", "source_name")  
    @classmethod  
    def validate_required_text(cls, v: str) -> str:  
        if not v.strip():  
            raise ValueError("Value cannot be empty.")  
        return v  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/layer_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from pydantic import Field  
  
from config_sdk.contracts.enums import ConfigLayerNameEnum, ConfigStatusEnum  
from config_sdk.contracts.source_models import ConfigSourceRef  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class LayerSelectionCriteria(ConfigSdkBaseModel):  
    domain_name: str | None = None  
    role_name: str | None = None  
    environment_name: str | None = None  
    project_name: str | None = None  
  
  
class ConfigLayer(ConfigSdkBaseModel):  
    layer_id: str  
    layer_name: ConfigLayerNameEnum  
    priority: int  
    source_ref: ConfigSourceRef  
    raw_content: dict[str, Any]  
    validated_content: dict[str, Any] | None = None  
    schema_name: str | None = None  
    status: ConfigStatusEnum = ConfigStatusEnum.LOADED  
    metadata: dict[str, Any] = Field(default_factory=dict)  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/metadata_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from datetime import datetime  
from typing import Any  
  
from pydantic import Field  
  
from config_sdk.contracts.enums import ConfigLayerNameEnum, ValidationModeEnum  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigProvenanceEntry(ConfigSdkBaseModel):  
    key_path: str  
    effective_value: Any  
    source_layer: ConfigLayerNameEnum  
    source_name: str | None = None  
    source_path: str | None = None  
    overridden_layers: list[str] = Field(default_factory=list)  
    notes: list[str] = Field(default_factory=list)  
    resolution_details: dict[str, Any] = Field(default_factory=dict)  
  
  
class ConfigHashInfo(ConfigSdkBaseModel):  
    config_hash: str  
    hash_algorithm: str = "sha256"  
    normalized_size: int  
    short_hash: str  
  
  
class EffectiveConfigMetadata(ConfigSdkBaseModel):  
    bundle_name: str  
    resolved_at: datetime  
    layer_order: list[str]  
    validation_mode: ValidationModeEnum  
    schema_name: str | None = None  
    metadata: dict[str, Any] = Field(default_factory=dict)  
    reasoning_refs: list[str] = Field(default_factory=list)  
    review_refs: list[str] = Field(default_factory=list)  
    decision_refs: list[str] = Field(default_factory=list)  
    change_set_refs: list[str] = Field(default_factory=list)  
    trace_bundle_ref: str | None = None  
    snapshot_ref: str | None = None  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/bundle_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from pydantic import Field  
  
from config_sdk.contracts.enums import ConfigStatusEnum  
from config_sdk.contracts.layer_models import ConfigLayer  
from config_sdk.contracts.metadata_models import (  
    ConfigHashInfo,  
    ConfigProvenanceEntry,  
    EffectiveConfigMetadata,  
)  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigBundle(ConfigSdkBaseModel):  
    bundle_id: str  
    bundle_name: str  
    layers: list[ConfigLayer]  
    domain_name: str | None = None  
    role_name: str | None = None  
    environment_name: str | None = None  
    project_name: str | None = None  
    bundle_metadata: dict[str, Any] = Field(default_factory=dict)  
  
  
class EffectiveConfig(ConfigSdkBaseModel):  
    effective_config_id: str  
    bundle_id: str  
    bundle_name: str  
    effective_content: dict[str, Any]  
    config_hash_info: ConfigHashInfo  
    provenance_map: dict[str, ConfigProvenanceEntry]  
    metadata: EffectiveConfigMetadata  
    validation_status: ConfigStatusEnum = ConfigStatusEnum.RESOLVED  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/actor_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from pydantic import Field  
  
from config_sdk.contracts.enums import ActorTypeEnum, AuthorityLevelEnum  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigActorRef(ConfigSdkBaseModel):  
    actor_id: str  
    actor_name: str  
    actor_type: ActorTypeEnum  
    actor_role: str  
    actor_org_unit: str | None = None  
    authority_level: AuthorityLevelEnum = AuthorityLevelEnum.DRAFT  
    is_human: bool = True  
    metadata: dict[str, Any] = Field(default_factory=dict)  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/agent_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from pydantic import Field, field_validator  
  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigActionProposal(ConfigSdkBaseModel):  
    action_type: str  
    target_path: str | None = None  
    proposed_value: Any = None  
    metadata: dict[str, Any] = Field(default_factory=dict)  
  
  
class ConfigAgentOutput(ConfigSdkBaseModel):  
    proposed_action: ConfigActionProposal  
    rationale: list[str] = Field(default_factory=list)  
    assumptions: list[str] = Field(default_factory=list)  
    evidence_refs: list[str] = Field(default_factory=list)  
    confidence: float  
    risk_flags: list[str] = Field(default_factory=list)  
    alternative_options: list[str] = Field(default_factory=list)  
    limitations: list[str] = Field(default_factory=list)  
    unresolved_questions: list[str] = Field(default_factory=list)  
  
    @field_validator("confidence")  
    @classmethod  
    def validate_confidence(cls, v: float) -> float:  
        if not 0 <= v <= 1:  
            raise ValueError("confidence must be between 0 and 1")  
        return v  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/change_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from datetime import datetime  
from typing import Any  
  
from pydantic import Field  
  
from config_sdk.contracts.enums import ChangeTypeEnum, MaterialityEnum  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigChangeItem(ConfigSdkBaseModel):  
    change_id: str  
    key_path: str  
    before_value: Any = None  
    after_value: Any = None  
    change_type: ChangeTypeEnum  
    source_layer_before: str | None = None  
    source_layer_after: str | None = None  
    materiality_flag: MaterialityEnum = MaterialityEnum.NON_MATERIAL  
    impact_summary: str | None = None  
    validation_impact: str | None = None  
    downstream_sdk_refs: list[str] = Field(default_factory=list)  
    metadata: dict[str, Any] = Field(default_factory=dict)  
  
  
class ConfigChangeSet(ConfigSdkBaseModel):  
    change_set_id: str  
    subject_type: str  
    subject_id: str  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    config_hash: str | None = None  
    items: list[ConfigChangeItem] = Field(default_factory=list)  
    summary: str | None = None  
    evidence_refs: list[str] = Field(default_factory=list)  
    created_at: datetime  
    metadata: dict[str, Any] = Field(default_factory=dict)  
  
  
class ConfigChangeSetQuery(ConfigSdkBaseModel):  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    subject_type: str | None = None  
    subject_id: str | None = None  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/reasoning_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from datetime import datetime  
from typing import Any  
  
from pydantic import Field  
  
from config_sdk.contracts.actor_models import ConfigActorRef  
from config_sdk.contracts.agent_models import ConfigAgentOutput  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigReasoningRecord(ConfigSdkBaseModel):  
    reasoning_id: str  
    subject_type: str  
    subject_id: str  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    config_hash: str | None = None  
    actor: ConfigActorRef  
    note_type: str = "reasoning"  
    summary: str  
    agent_output: ConfigAgentOutput | None = None  
    evidence_refs: list[str] = Field(default_factory=list)  
    linked_change_set_refs: list[str] = Field(default_factory=list)  
    metadata: dict[str, Any] = Field(default_factory=dict)  
    created_at: datetime  
  
  
class ConfigReasoningQuery(ConfigSdkBaseModel):  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    subject_type: str | None = None  
    subject_id: str | None = None  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/review_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from datetime import datetime  
  
from pydantic import Field  
  
from config_sdk.contracts.actor_models import ConfigActorRef  
from config_sdk.contracts.enums import (  
    ResolutionStatusEnum,  
    ReviewResponseTypeEnum,  
    ReviewStatusEnum,  
)  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigReviewRequest(ConfigSdkBaseModel):  
    review_id: str  
    subject_type: str  
    subject_id: str  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    config_hash: str | None = None  
    requested_by_actor: ConfigActorRef  
    review_type: str  
    title: str  
    description: str  
    linked_reasoning_refs: list[str] = Field(default_factory=list)  
    linked_change_set_refs: list[str] = Field(default_factory=list)  
    evidence_refs: list[str] = Field(default_factory=list)  
    due_at: datetime | None = None  
    priority: str | None = None  
    status: ReviewStatusEnum = ReviewStatusEnum.OPEN  
    metadata: dict = Field(default_factory=dict)  
    created_at: datetime  
  
  
class ConfigReviewResponseRecord(ConfigSdkBaseModel):  
    review_response_id: str  
    review_id: str  
    responded_by_actor: ConfigActorRef  
    response_type: ReviewResponseTypeEnum  
    response_text: str  
    challenge_points: list[str] = Field(default_factory=list)  
    requested_changes: list[str] = Field(default_factory=list)  
    conditions: list[str] = Field(default_factory=list)  
    evidence_refs: list[str] = Field(default_factory=list)  
    open_issue_refs: list[str] = Field(default_factory=list)  
    resolution_status: ResolutionStatusEnum = ResolutionStatusEnum.OPEN  
    metadata: dict = Field(default_factory=dict)  
    created_at: datetime  
  
  
class ConfigReviewQuery(ConfigSdkBaseModel):  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    subject_type: str | None = None  
    subject_id: str | None = None  
    review_type: str | None = None  
    status: ReviewStatusEnum | None = None  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/decision_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from datetime import datetime  
  
from pydantic import Field  
  
from config_sdk.contracts.actor_models import ConfigActorRef  
from config_sdk.contracts.enums import (  
    DecisionBasisTypeEnum,  
    DecisionStatusEnum,  
    DecisionTypeEnum,  
)  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigDecisionRecord(ConfigSdkBaseModel):  
    decision_id: str  
    subject_type: str  
    subject_id: str  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    config_hash: str | None = None  
    decision_type: DecisionTypeEnum  
    decision_status: DecisionStatusEnum  
    decision_basis_type: DecisionBasisTypeEnum  
    title: str  
    rationale: str  
    assumptions: list[str] = Field(default_factory=list)  
    decided_by_actor: ConfigActorRef  
    decision_authority: str | None = None  
    linked_reasoning_refs: list[str] = Field(default_factory=list)  
    linked_review_refs: list[str] = Field(default_factory=list)  
    linked_change_set_refs: list[str] = Field(default_factory=list)  
    evidence_refs: list[str] = Field(default_factory=list)  
    open_issue_refs: list[str] = Field(default_factory=list)  
    conditions_of_approval: list[str] = Field(default_factory=list)  
    supersedes_decision_id: str | None = None  
    superseded_by_decision_id: str | None = None  
    effective_from: datetime | None = None  
    effective_to: datetime | None = None  
    metadata: dict = Field(default_factory=dict)  
    created_at: datetime  
  
  
class ConfigDecisionQuery(ConfigSdkBaseModel):  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    subject_type: str | None = None  
    subject_id: str | None = None  
    decision_type: DecisionTypeEnum | None = None  
    decision_status: DecisionStatusEnum | None = None  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/evidence_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from datetime import datetime  
  
from pydantic import Field  
  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigEvidenceRef(ConfigSdkBaseModel):  
    evidence_id: str  
    evidence_type: str  
    ref: str  
    title: str | None = None  
    description: str | None = None  
    source_system: str | None = None  
    created_at: datetime | None = None  
    created_by: str | None = None  
    integrity_hash: str | None = None  
    metadata: dict = Field(default_factory=dict)  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/trace_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from datetime import datetime  
  
from pydantic import Field  
  
from config_sdk.contracts.change_models import ConfigChangeSet  
from config_sdk.contracts.decision_models import ConfigDecisionRecord  
from config_sdk.contracts.reasoning_models import ConfigReasoningRecord  
from config_sdk.contracts.review_models import (  
    ConfigReviewRequest,  
    ConfigReviewResponseRecord,  
)  
from config_sdk.contracts.enums import TimelineEventTypeEnum  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigTimelineEvent(ConfigSdkBaseModel):  
    event_id: str  
    event_type: TimelineEventTypeEnum  
    event_time: datetime  
    actor_id: str | None = None  
    subject_type: str  
    subject_id: str  
    summary: str  
    linked_refs: list[str] = Field(default_factory=list)  
    metadata: dict = Field(default_factory=dict)  
  
  
class ConfigDecisionTrail(ConfigSdkBaseModel):  
    subject_type: str  
    subject_id: str  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    config_hash: str | None = None  
    reasoning_records: list[ConfigReasoningRecord] = Field(default_factory=list)  
    review_requests: list[ConfigReviewRequest] = Field(default_factory=list)  
    review_responses: list[ConfigReviewResponseRecord] = Field(default_factory=list)  
    decision_records: list[ConfigDecisionRecord] = Field(default_factory=list)  
    change_sets: list[ConfigChangeSet] = Field(default_factory=list)  
    timeline: list[ConfigTimelineEvent] = Field(default_factory=list)  
    unresolved_issues: list[str] = Field(default_factory=list)  
  
  
class ConfigTraceBundle(ConfigSdkBaseModel):  
    trace_bundle_id: str  
    subject_type: str  
    subject_id: str  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    config_hash: str | None = None  
    decision_trail: ConfigDecisionTrail  
    provenance_summary: list[dict] = Field(default_factory=list)  
    current_status: str | None = None  
    evidence_refs: list[str] = Field(default_factory=list)  
    export_metadata: dict = Field(default_factory=dict)  
  
  
class ConfigTraceBundleQuery(ConfigSdkBaseModel):  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    subject_type: str | None = None  
    subject_id: str | None = None  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/snapshot_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from datetime import datetime  
  
from pydantic import Field  
  
from config_sdk.contracts.actor_models import ConfigActorRef  
from config_sdk.contracts.bundle_models import EffectiveConfig  
from config_sdk.contracts.change_models import ConfigChangeSet  
from config_sdk.contracts.decision_models import ConfigDecisionRecord  
from config_sdk.contracts.reasoning_models import ConfigReasoningRecord  
from config_sdk.contracts.review_models import (  
    ConfigReviewRequest,  
    ConfigReviewResponseRecord,  
)  
from config_sdk.contracts.trace_models import ConfigTraceBundle  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigAuditSnapshot(ConfigSdkBaseModel):  
    snapshot_id: str  
    snapshot_type: str  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    config_hash: str  
    exported_at: datetime  
    exported_by_actor: ConfigActorRef  
    freeze_reason: str  
    effective_config: EffectiveConfig  
    change_sets: list[ConfigChangeSet] = Field(default_factory=list)  
    reasoning_records: list[ConfigReasoningRecord] = Field(default_factory=list)  
    review_requests: list[ConfigReviewRequest] = Field(default_factory=list)  
    review_responses: list[ConfigReviewResponseRecord] = Field(default_factory=list)  
    decision_records: list[ConfigDecisionRecord] = Field(default_factory=list)  
    trace_bundle: ConfigTraceBundle  
    evidence_refs: list[str] = Field(default_factory=list)  
    integrity_hash: str | None = None  
    metadata: dict = Field(default_factory=dict)  
  
  
class ConfigSnapshotQuery(ConfigSdkBaseModel):  
    project_name: str | None = None  
    bundle_id: str | None = None  
    effective_config_id: str | None = None  
    snapshot_type: str | None = None  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/request_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from pydantic import Field  
  
from config_sdk.contracts.bundle_models import EffectiveConfig  
from config_sdk.contracts.enums import ValidationModeEnum  
from config_sdk.contracts.source_models import ConfigSourceRef  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class ConfigResolutionRequest(ConfigSdkBaseModel):  
    bundle_name: str  
    sources: list[ConfigSourceRef]  
    domain_name: str | None = None  
    role_name: str | None = None  
    environment_name: str | None = None  
    project_name: str | None = None  
    runtime_override: dict[str, Any] | None = None  
    validation_mode: ValidationModeEnum = ValidationModeEnum.STRICT  
    schema_name: str | None = None  
    metadata: dict[str, Any] = Field(default_factory=dict)  
  
  
class ConfigValidationRequest(ConfigSdkBaseModel):  
    source_ref: ConfigSourceRef | None = None  
    config_dict: dict[str, Any] | None = None  
    schema_name: str | None = None  
    validation_mode: ValidationModeEnum = ValidationModeEnum.STRICT  
  
  
class ConfigDiffRequest(ConfigSdkBaseModel):  
    left_config: EffectiveConfig | dict[str, Any]  
    right_config: EffectiveConfig | dict[str, Any]  
    include_values: bool = True  
  
  
# ================================================================  
# FILE: src/config_sdk/contracts/response_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from pydantic import Field  
  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class BaseConfigResponse(ConfigSdkBaseModel):  
    status: str  
    message: str  
    data: dict[str, Any] = Field(default_factory=dict)  
    warnings: list[dict[str, Any]] = Field(default_factory=list)  
    errors: list[dict[str, Any]] = Field(default_factory=list)  
    references: dict[str, Any] = Field(default_factory=dict)  
    workflow_hint: dict[str, Any] = Field(default_factory=dict)  
    agent_hint: dict[str, Any] = Field(default_factory=dict)  
    audit_hint: dict[str, Any] = Field(default_factory=dict)  
    observability_hint: dict[str, Any] = Field(default_factory=dict)  
    reasoning_refs: list[str] = Field(default_factory=list)  
    review_refs: list[str] = Field(default_factory=list)  
    decision_refs: list[str] = Field(default_factory=list)  
    change_set_refs: list[str] = Field(default_factory=list)  
    trace_bundle_ref: str | None = None  
    snapshot_ref: str | None = None  
  
  
class ConfigResolutionResponse(BaseConfigResponse):  
    pass  
  
  
class ConfigValidationResponse(BaseConfigResponse):  
    is_valid: bool  
  
  
class ConfigDiffResponse(BaseConfigResponse):  
    pass  
  
  
# ================================================================  
# FILE: src/config_sdk/models/common_models.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from pydantic import Field  
  
from config_sdk.models.base_models import ConfigSdkBaseModel  
  
  
class NamedSectionConfig(ConfigSdkBaseModel):  
    name: str  
    metadata: dict[str, Any] = Field(default_factory=dict)  
  
  
class RetryConfig(ConfigSdkBaseModel):  
    max_retries: int = 0  
    backoff_seconds: list[int] = Field(default_factory=list)  
  
  
class PathConfig(ConfigSdkBaseModel):  
    root_path: str | None = None  
    temp_path: str | None = None  
    export_path: str | None = None  
  
  
class TagsConfig(ConfigSdkBaseModel):  
    tags: list[str] = Field(default_factory=list)  
  
  
# ================================================================  
# FILE: src/config_sdk/models/schema_catalog.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Type  
  
from pydantic import BaseModel  
  
  
SCHEMA_CATALOG: dict[str, Type[BaseModel]] = {}  
  
  
def register_schema(schema_name: str, schema_cls: Type[BaseModel]) -> None:  
    SCHEMA_CATALOG[schema_name] = schema_cls  
  
  
def get_schema(schema_name: str) -> Type[BaseModel]:  
    if schema_name not in SCHEMA_CATALOG:  
        raise KeyError(f"Schema not registered: {schema_name}")  
    return SCHEMA_CATALOG[schema_name]  
  
  
# ================================================================  
# FILE: src/config_sdk/exceptions/errors.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from config_sdk.contracts.source_models import ConfigSourceRef  
  
  
class ConfigSdkError(Exception):  
    def __init__(  
        self,  
        message: str,  
        source_ref: ConfigSourceRef | None = None,  
        layer_name: str | None = None,  
        key_path: str | None = None,  
        original_exception: Exception | None = None,  
        metadata: dict[str, Any] | None = None,  
    ) -> None:  
        super().__init__(message)  
        self.message = message  
        self.source_ref = source_ref  
        self.layer_name = layer_name  
        self.key_path = key_path  
        self.original_exception = original_exception  
        self.metadata = metadata or {}  
  
    def to_dict(self) -> dict[str, Any]:  
        return {  
            "message": self.message,  
            "source_ref": self.source_ref.model_dump() if self.source_ref else None,  
            "layer_name": self.layer_name,  
            "key_path": self.key_path,  
            "original_exception": repr(self.original_exception) if self.original_exception else None,  
            "metadata": self.metadata,  
        }  
  
  
class ConfigLoadError(ConfigSdkError):  
    pass  
  
  
class ConfigParseError(ConfigSdkError):  
    pass  
  
  
class ConfigValidationError(ConfigSdkError):  
    pass  
  
  
class ConfigSchemaError(ConfigSdkError):  
    pass  
  
  
class ConfigMergeError(ConfigSdkError):  
    pass  
  
  
class ConfigReferenceResolutionError(ConfigSdkError):  
    pass  
  
  
class ConfigPlaceholderResolutionError(ConfigSdkError):  
    pass  
  
  
class ConfigBundleError(ConfigSdkError):  
    pass  
  
  
class ConfigDiffError(ConfigSdkError):  
    pass  
  
  
class ConfigGovernanceError(ConfigSdkError):  
    pass  
  
  
class ConfigReviewError(ConfigGovernanceError):  
    pass  
  
  
class ConfigDecisionError(ConfigGovernanceError):  
    pass  
  
  
class ConfigTraceError(ConfigGovernanceError):  
    pass  
  
  
class ConfigSnapshotError(ConfigGovernanceError):  
    pass  
  
  
# ================================================================  
# FILE: src/config_sdk/utils/io_utils.py  
# ================================================================  
  
from __future__ import annotations  
  
from pathlib import Path  
  
  
def read_text_file(path: str) -> str:  
    return Path(path).read_text(encoding="utf-8")  
  
  
def write_text_file(path: str, content: str) -> None:  
    target = Path(path)  
    target.parent.mkdir(parents=True, exist_ok=True)  
    target.write_text(content, encoding="utf-8")  
  
  
# ================================================================  
# FILE: src/config_sdk/utils/normalize.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
  
def normalize_mapping(value: Any) -> dict[str, Any]:  
    if value is None:  
        return {}  
    if not isinstance(value, dict):  
        raise TypeError("Expected a dictionary-like object.")  
    return value  
  
  
# ================================================================  
# FILE: src/config_sdk/utils/path_utils.py  
# ================================================================  
  
from __future__ import annotations  
  
from pathlib import Path  
  
  
def detect_file_format(path: str) -> str | None:  
    suffix = Path(path).suffix.lower()  
    if suffix in {".yaml", ".yml"}:  
        return "yaml"  
    if suffix == ".json":  
        return "json"  
    if suffix == ".toml":  
        return "toml"  
    return None  
  
  
# ================================================================  
# FILE: src/config_sdk/utils/dict_tools.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
  
def get_by_dotted_path(data: dict[str, Any], key_path: str) -> Any:  
    current: Any = data  
    if not key_path:  
        return current  
    for part in key_path.split("."):  
        if not isinstance(current, dict) or part not in current:  
            return None  
        current = current[part]  
    return current  
  
  
def flatten_dict(data: dict[str, Any], prefix: str = "") -> dict[str, Any]:  
    out: dict[str, Any] = {}  
    for key, value in data.items():  
        full_key = f"{prefix}.{key}" if prefix else key  
        if isinstance(value, dict):  
            out.update(flatten_dict(value, full_key))  
        else:  
            out[full_key] = value  
    return out  
  
  
# ================================================================  
# FILE: src/config_sdk/utils/ids.py  
# ================================================================  
  
from __future__ import annotations  
  
import uuid  
  
  
def new_id(prefix: str) -> str:  
    return f"{prefix}_{uuid.uuid4().hex[:12]}"  
  
  
# ================================================================  
# FILE: src/config_sdk/utils/time_utils.py  
# ================================================================  
  
from __future__ import annotations  
  
from datetime import datetime, timezone  
  
  
def utc_now() -> datetime:  
    return datetime.now(timezone.utc)  
  
  
# ================================================================  
# FILE: src/config_sdk/utils/serialization.py  
# ================================================================  
  
from __future__ import annotations  
  
import json  
from typing import Any  
  
  
def to_canonical_json(data: dict[str, Any]) -> str:  
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))  
  
  
# ================================================================  
# FILE: src/config_sdk/loaders/base_loader.py  
# ================================================================  
  
from __future__ import annotations  
  
from abc import ABC, abstractmethod  
from typing import Any  
  
from config_sdk.contracts.enums import ConfigStatusEnum  
from config_sdk.contracts.layer_models import ConfigLayer  
from config_sdk.contracts.source_models import ConfigSourceRef  
from config_sdk.exceptions.errors import ConfigLoadError  
from config_sdk.utils.ids import new_id  
  
  
class BaseConfigLoader(ABC):  
    @abstractmethod  
    def _read_raw_content(self, source_ref: ConfigSourceRef) -> dict[str, Any]:  
        raise NotImplementedError  
  
    def load(self, source_ref: ConfigSourceRef) -> ConfigLayer:  
        try:  
            raw = self._read_raw_content(source_ref)  
        except Exception as exc:  
            raise ConfigLoadError(  
                message=f"Failed to load config source: {source_ref.source_name}",  
                source_ref=source_ref,  
                original_exception=exc,  
            ) from exc  
  
        return ConfigLayer(  
            layer_id=new_id("layer"),  
            layer_name=source_ref.layer_name,  
            priority=source_ref.priority,  
            source_ref=source_ref,  
            raw_content=raw,  
            validated_content=None,  
            schema_name=None,  
            status=ConfigStatusEnum.LOADED,  
            metadata={},  
        )  
  
  
# ================================================================  
# FILE: src/config_sdk/loaders/yaml_loader.py  
# ================================================================  
  
from __future__ import annotations  
  
import yaml  
  
from config_sdk.contracts.source_models import ConfigSourceRef  
from config_sdk.loaders.base_loader import BaseConfigLoader  
from config_sdk.utils.io_utils import read_text_file  
from config_sdk.utils.normalize import normalize_mapping  
  
  
class YamlConfigLoader(BaseConfigLoader):  
    def _read_raw_content(self, source_ref: ConfigSourceRef) -> dict:  
        if not source_ref.source_path:  
            raise ValueError("YAML source_path is required.")  
        content = read_text_file(source_ref.source_path)  
        parsed = yaml.safe_load(content)  
        return normalize_mapping(parsed)  
  
  
# ================================================================  
# FILE: src/config_sdk/loaders/json_loader.py  
# ================================================================  
  
from __future__ import annotations  
  
import json  
  
from config_sdk.contracts.source_models import ConfigSourceRef  
from config_sdk.loaders.base_loader import BaseConfigLoader  
from config_sdk.utils.io_utils import read_text_file  
from config_sdk.utils.normalize import normalize_mapping  
  
  
class JsonConfigLoader(BaseConfigLoader):  
    def _read_raw_content(self, source_ref: ConfigSourceRef) -> dict:  
        if not source_ref.source_path:  
            raise ValueError("JSON source_path is required.")  
        content = read_text_file(source_ref.source_path)  
        parsed = json.loads(content)  
        return normalize_mapping(parsed)  
  
  
# ================================================================  
# FILE: src/config_sdk/loaders/toml_loader.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.source_models import ConfigSourceRef  
from config_sdk.loaders.base_loader import BaseConfigLoader  
from config_sdk.utils.io_utils import read_text_file  
from config_sdk.utils.normalize import normalize_mapping  
  
try:  
    import tomllib  
except ImportError:  
    tomllib = None  
  
  
class TomlConfigLoader(BaseConfigLoader):  
    def _read_raw_content(self, source_ref: ConfigSourceRef) -> dict:  
        if not source_ref.source_path:  
            raise ValueError("TOML source_path is required.")  
        if tomllib is None:  
            raise RuntimeError("tomllib is not available in this environment.")  
        content = read_text_file(source_ref.source_path)  
        parsed = tomllib.loads(content)  
        return normalize_mapping(parsed)  
  
  
# ================================================================  
# FILE: src/config_sdk/loaders/dict_loader.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.source_models import ConfigSourceRef  
from config_sdk.loaders.base_loader import BaseConfigLoader  
from config_sdk.utils.normalize import normalize_mapping  
  
  
class DictConfigLoader(BaseConfigLoader):  
    def __init__(self, in_memory_payloads: dict[str, dict] | None = None) -> None:  
        self.in_memory_payloads = in_memory_payloads or {}  
  
    def _read_raw_content(self, source_ref: ConfigSourceRef) -> dict:  
        payload = self.in_memory_payloads.get(source_ref.source_id)  
        if payload is None:  
            raise ValueError(f"No in-memory payload found for source_id={source_ref.source_id}")  
        return normalize_mapping(payload)  
  
  
# ================================================================  
# FILE: src/config_sdk/loaders/loader_factory.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.enums import ConfigSourceTypeEnum  
from config_sdk.loaders.base_loader import BaseConfigLoader  
from config_sdk.loaders.dict_loader import DictConfigLoader  
from config_sdk.loaders.json_loader import JsonConfigLoader  
from config_sdk.loaders.toml_loader import TomlConfigLoader  
from config_sdk.loaders.yaml_loader import YamlConfigLoader  
  
  
class LoaderFactory:  
    def __init__(self, in_memory_payloads: dict[str, dict] | None = None) -> None:  
        self.in_memory_payloads = in_memory_payloads or {}  
  
    def get_loader(self, source_type: ConfigSourceTypeEnum) -> BaseConfigLoader:  
        if source_type == ConfigSourceTypeEnum.YAML_FILE:  
            return YamlConfigLoader()  
        if source_type == ConfigSourceTypeEnum.JSON_FILE:  
            return JsonConfigLoader()  
        if source_type == ConfigSourceTypeEnum.TOML_FILE:  
            return TomlConfigLoader()  
        if source_type in {  
            ConfigSourceTypeEnum.IN_MEMORY_DICT,  
            ConfigSourceTypeEnum.RUNTIME_OVERRIDE,  
        }:  
            return DictConfigLoader(in_memory_payloads=self.in_memory_payloads)  
        raise ValueError(f"Unsupported config source type: {source_type}")  
  
  
# ================================================================  
# FILE: src/config_sdk/mergers/merge_strategies.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
  
def merge_replace(base: Any, override: Any) -> Any:  
    return override  
  
  
def merge_keep_base(base: Any, override: Any) -> Any:  
    return base  
  
  
def merge_append_unique(base: list[Any], override: list[Any]) -> list[Any]:  
    out = list(base)  
    for item in override:  
        if item not in out:  
            out.append(item)  
    return out  
  
  
def merge_append_all(base: list[Any], override: list[Any]) -> list[Any]:  
    return list(base) + list(override)  
  
  
# ================================================================  
# FILE: src/config_sdk/mergers/merge_engine.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from config_sdk.contracts.enums import MergeStrategyEnum  
from config_sdk.contracts.layer_models import ConfigLayer  
from config_sdk.exceptions.errors import ConfigMergeError  
  
  
class MergeEngine:  
    def merge_layers(  
        self,  
        layers: list[ConfigLayer],  
        strategy_map: dict[str, MergeStrategyEnum] | None = None,  
    ) -> tuple[dict[str, Any], dict[str, str]]:  
        if not layers:  
            return {}, {}  
  
        sorted_layers = sorted(layers, key=lambda x: x.priority)  
        merged: dict[str, Any] = {}  
        provenance_seed: dict[str, str] = {}  
  
        for layer in sorted_layers:  
            content = layer.validated_content if layer.validated_content is not None else layer.raw_content  
            merged = self.merge_dicts(  
                merged,  
                content,  
                strategy_map=strategy_map,  
                path_prefix="",  
                provenance_seed=provenance_seed,  
                layer_name=layer.layer_name.value,  
            )  
        return merged, provenance_seed  
  
    def merge_dicts(  
        self,  
        base: dict[str, Any],  
        override: dict[str, Any],  
        strategy_map: dict[str, MergeStrategyEnum] | None = None,  
        path_prefix: str = "",  
        provenance_seed: dict[str, str] | None = None,  
        layer_name: str | None = None,  
    ) -> dict[str, Any]:  
        strategy_map = strategy_map or {}  
        provenance_seed = provenance_seed or {}  
        out = dict(base)  
  
        for key, override_value in override.items():  
            full_path = f"{path_prefix}.{key}" if path_prefix else key  
            strategy = strategy_map.get(full_path)  
  
            if key not in out:  
                out[key] = override_value  
                if layer_name:  
                    provenance_seed[full_path] = layer_name  
                continue  
  
            base_value = out[key]  
  
            if strategy == MergeStrategyEnum.KEEP_BASE:  
                out[key] = base_value  
            elif strategy == MergeStrategyEnum.REPLACE:  
                out[key] = override_value  
            elif strategy == MergeStrategyEnum.APPEND_UNIQUE:  
                if not isinstance(base_value, list) or not isinstance(override_value, list):  
                    raise ConfigMergeError(  
                        message=f"APPEND_UNIQUE requires list types at path '{full_path}'",  
                        key_path=full_path,  
                    )  
                out[key] = list(base_value) + [x for x in override_value if x not in base_value]  
            elif strategy == MergeStrategyEnum.APPEND_ALL:  
                if not isinstance(base_value, list) or not isinstance(override_value, list):  
                    raise ConfigMergeError(  
                        message=f"APPEND_ALL requires list types at path '{full_path}'",  
                        key_path=full_path,  
                    )  
                out[key] = list(base_value) + list(override_value)  
            else:  
                if isinstance(base_value, dict) and isinstance(override_value, dict):  
                    out[key] = self.merge_dicts(  
                        base_value,  
                        override_value,  
                        strategy_map=strategy_map,  
                        path_prefix=full_path,  
                        provenance_seed=provenance_seed,  
                        layer_name=layer_name,  
                    )  
                else:  
                    out[key] = override_value  
  
            if layer_name:  
                provenance_seed[full_path] = layer_name  
  
        return out  
  
  
# ================================================================  
# FILE: src/config_sdk/mergers/overlay_resolver.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.bundle_models import ConfigBundle  
from config_sdk.contracts.layer_models import ConfigLayer  
from config_sdk.contracts.request_models import ConfigResolutionRequest  
  
  
class OverlayResolver:  
    def resolve_layer_order(self, bundle: ConfigBundle) -> list[ConfigLayer]:  
        return sorted(bundle.layers, key=lambda x: x.priority)  
  
    def select_relevant_layers(  
        self,  
        bundle: ConfigBundle,  
        request: ConfigResolutionRequest,  
    ) -> list[ConfigLayer]:  
        return self.resolve_layer_order(bundle)  
  
  
# ================================================================  
# FILE: src/config_sdk/validators/schema_validator.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from pydantic import ValidationError  
  
from config_sdk.exceptions.errors import ConfigSchemaError  
from config_sdk.models.schema_catalog import get_schema  
  
  
class SchemaValidator:  
    def validate(self, config_dict: dict[str, Any], schema_name: str | None) -> dict[str, Any]:  
        if not schema_name:  
            return config_dict  
        try:  
            schema_cls = get_schema(schema_name)  
            validated = schema_cls.model_validate(config_dict)  
            return validated.model_dump()  
        except KeyError as exc:  
            raise ConfigSchemaError(message=f"Schema not found: {schema_name}") from exc  
        except ValidationError as exc:  
            raise ConfigSchemaError(  
                message=f"Schema validation failed for schema={schema_name}",  
                original_exception=exc,  
            ) from exc  
  
  
# ================================================================  
# FILE: src/config_sdk/validators/cross_field_validator.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
  
class CrossFieldValidator:  
    def validate(self, config_dict: dict[str, Any], schema_name: str | None = None) -> list[dict[str, Any]]:  
        issues: list[dict[str, Any]] = []  
        workflow = config_dict.get("workflow")  
        if isinstance(workflow, dict):  
            if workflow.get("approval_required") and workflow.get("auto_continue_allowed"):  
                issues.append(  
                    {  
                        "level": "error",  
                        "message": "approval_required and auto_continue_allowed cannot both be true.",  
                        "key_path": "workflow",  
                    }  
                )  
        return issues  
  
  
# ================================================================  
# FILE: src/config_sdk/validators/bundle_validator.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.bundle_models import ConfigBundle  
  
  
class BundleValidator:  
    def validate_bundle(self, bundle: ConfigBundle, schema_name: str | None = None) -> list[dict]:  
        issues: list[dict] = []  
  
        if not bundle.layers:  
            issues.append({"level": "error", "message": "Bundle contains no layers."})  
  
        seen_ids: set[str] = set()  
        for layer in bundle.layers:  
            if layer.layer_id in seen_ids:  
                issues.append(  
                    {  
                        "level": "error",  
                        "message": f"Duplicate layer_id detected: {layer.layer_id}",  
                    }  
                )  
            seen_ids.add(layer.layer_id)  
  
        return issues  
  
  
# ================================================================  
# FILE: src/config_sdk/validators/reference_validator.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from config_sdk.contracts.enums import ValidationModeEnum  
  
  
class ReferenceValidator:  
    def validate_references(  
        self,  
        config_dict: dict[str, Any],  
        validation_mode: ValidationModeEnum = ValidationModeEnum.STRICT,  
    ) -> list[dict[str, Any]]:  
        issues: list[dict[str, Any]] = []  
  
        def walk(value: Any, key_path: str = "") -> None:  
            if isinstance(value, dict):  
                for k, v in value.items():  
                    next_path = f"{key_path}.{k}" if key_path else k  
                    walk(v, next_path)  
            elif isinstance(value, list):  
                for idx, item in enumerate(value):  
                    next_path = f"{key_path}[{idx}]"  
                    walk(item, next_path)  
            elif isinstance(value, str) and value.startswith("${") and value.endswith("}"):  
                issues.append(  
                    {  
                        "level": "error" if validation_mode == ValidationModeEnum.STRICT else "warning",  
                        "message": f"Unresolved placeholder detected: {value}",  
                        "key_path": key_path,  
                    }  
                )  
  
        walk(config_dict)  
        return issues  
  
  
# ================================================================  
# FILE: src/config_sdk/validators/governance_validator.py  
# ================================================================  
  
from __future__ import annotations  
  
  
class GovernanceValidator:  
    def validate(self, payload: dict) -> list[dict]:  
        return []  
  
  
# ================================================================  
# FILE: src/config_sdk/validators/trace_validator.py  
# ================================================================  
  
from __future__ import annotations  
  
  
class TraceValidator:  
    def validate(self, payload: dict) -> list[dict]:  
        return []  
  
  
# ================================================================  
# FILE: src/config_sdk/resolvers/placeholder_resolver.py  
# ================================================================  
  
from __future__ import annotations  
  
import os  
import re  
from typing import Any  
  
from config_sdk.contracts.enums import ValidationModeEnum  
from config_sdk.exceptions.errors import ConfigPlaceholderResolutionError  
  
  
PLACEHOLDER_PATTERN = re.compile(r"^\$\{(?P<kind>[a-zA-Z_]+):(?P<value>.+)\}$")  
  
  
class PlaceholderResolver:  
    def resolve_placeholders(  
        self,  
        config_dict: dict[str, Any],  
        validation_mode: ValidationModeEnum = ValidationModeEnum.STRICT,  
    ) -> dict[str, Any]:  
        def walk(value: Any, key_path: str = "") -> Any:  
            if isinstance(value, dict):  
                return {k: walk(v, f"{key_path}.{k}" if key_path else k) for k, v in value.items()}  
            if isinstance(value, list):  
                return [walk(v, f"{key_path}[{idx}]") for idx, v in enumerate(value)]  
            return self.resolve_value(value, key_path=key_path, validation_mode=validation_mode)  
  
        return walk(config_dict)  
  
    def resolve_value(  
        self,  
        value: Any,  
        key_path: str = "",  
        validation_mode: ValidationModeEnum = ValidationModeEnum.STRICT,  
    ) -> Any:  
        if not isinstance(value, str):  
            return value  
  
        match = PLACEHOLDER_PATTERN.match(value)  
        if not match:  
            return value  
  
        kind = match.group("kind")  
        payload = match.group("value")  
  
        if kind == "env":  
            resolved = os.getenv(payload)  
            if resolved is None:  
                if validation_mode == ValidationModeEnum.STRICT:  
                    raise ConfigPlaceholderResolutionError(  
                        message=f"Environment variable not found: {payload}",  
                        key_path=key_path,  
                    )  
                return value  
            return resolved  
  
        if validation_mode == ValidationModeEnum.STRICT:  
            raise ConfigPlaceholderResolutionError(  
                message=f"Unsupported placeholder type: {kind}",  
                key_path=key_path,  
            )  
        return value  
  
  
# ================================================================  
# FILE: src/config_sdk/resolvers/reference_resolver.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
  
class ReferenceResolver:  
    def resolve_internal_refs(self, config_dict: dict[str, Any]) -> dict[str, Any]:  
        return config_dict  
  
  
# ================================================================  
# FILE: src/config_sdk/resolvers/effective_config_renderer.py  
# ================================================================  
  
from __future__ import annotations  
  
import json  
import yaml  
  
from config_sdk.contracts.bundle_models import EffectiveConfig  
  
  
class EffectiveConfigRenderer:  
    def render_dict(self, effective_config: EffectiveConfig) -> dict:  
        return effective_config.effective_content  
  
    def render_json(self, effective_config: EffectiveConfig) -> str:  
        return json.dumps(effective_config.effective_content, indent=2, sort_keys=True)  
  
    def render_yaml(self, effective_config: EffectiveConfig) -> str:  
        return yaml.safe_dump(  
            effective_config.effective_content,  
            sort_keys=True,  
            allow_unicode=True,  
        )  
  
  
# ================================================================  
# FILE: src/config_sdk/hashing/config_hashing.py  
# ================================================================  
  
from __future__ import annotations  
  
import hashlib  
import json  
from typing import Any  
  
from config_sdk.contracts.metadata_models import ConfigHashInfo  
  
  
class ConfigHashing:  
    def canonical_serialize(self, config_dict: dict[str, Any]) -> bytes:  
        return json.dumps(  
            config_dict,  
            sort_keys=True,  
            ensure_ascii=False,  
            separators=(",", ":"),  
            default=str,  
        ).encode("utf-8")  
  
    def hash_config(self, config_dict: dict[str, Any]) -> ConfigHashInfo:  
        payload = self.canonical_serialize(config_dict)  
        digest = hashlib.sha256(payload).hexdigest()  
        return ConfigHashInfo(  
            config_hash=digest,  
            hash_algorithm="sha256",  
            normalized_size=len(payload),  
            short_hash=digest[:12],  
        )  
  
  
# ================================================================  
# FILE: src/config_sdk/hashing/fingerprinting.py  
# ================================================================  
  
from __future__ import annotations  
  
  
def build_short_hash(config_hash: str, length: int = 12) -> str:  
    return config_hash[:length]  
  
  
def build_bundle_fingerprint(bundle_name: str, config_hash: str) -> str:  
    return f"{bundle_name}:{config_hash[:12]}"  
  
  
# ================================================================  
# FILE: src/config_sdk/provenance/provenance_tracker.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from config_sdk.contracts.enums import ConfigLayerNameEnum  
from config_sdk.contracts.metadata_models import ConfigProvenanceEntry  
  
  
class ProvenanceTracker:  
    def __init__(self) -> None:  
        self._entries: dict[str, ConfigProvenanceEntry] = {}  
  
    def record_override(  
        self,  
        key_path: str,  
        effective_value: Any,  
        source_layer: str,  
        source_name: str | None = None,  
        source_path: str | None = None,  
        previous_layer: str | None = None,  
    ) -> None:  
        overridden_layers = []  
        if previous_layer and previous_layer != source_layer:  
            overridden_layers.append(previous_layer)  
  
        self._entries[key_path] = ConfigProvenanceEntry(  
            key_path=key_path,  
            effective_value=effective_value,  
            source_layer=ConfigLayerNameEnum(source_layer),  
            source_name=source_name,  
            source_path=source_path,  
            overridden_layers=overridden_layers,  
            notes=[],  
            resolution_details={},  
        )  
  
    def build_map(self) -> dict[str, ConfigProvenanceEntry]:  
        return dict(self._entries)  
  
  
# ================================================================  
# FILE: src/config_sdk/provenance/origin_explainer.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.bundle_models import EffectiveConfig  
  
  
class OriginExplainer:  
    def explain_key(  
        self,  
        effective_config: EffectiveConfig,  
        key_path: str,  
    ) -> dict | None:  
        entry = effective_config.provenance_map.get(key_path)  
        return entry.model_dump() if entry else None  
  
    def explain_prefix(  
        self,  
        effective_config: EffectiveConfig,  
        prefix: str,  
    ) -> list[dict]:  
        out: list[dict] = []  
        for key, entry in effective_config.provenance_map.items():  
            if key == prefix or key.startswith(f"{prefix}."):  
                out.append(entry.model_dump())  
        return out  
  
  
# ================================================================  
# FILE: src/config_sdk/provenance/config_diff.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from config_sdk.contracts.bundle_models import EffectiveConfig  
from config_sdk.exceptions.errors import ConfigDiffError  
  
  
class ConfigDiff:  
    def diff(  
        self,  
        left: EffectiveConfig | dict[str, Any],  
        right: EffectiveConfig | dict[str, Any],  
        include_values: bool = True,  
    ) -> dict[str, Any]:  
        left_dict = left.effective_content if isinstance(left, EffectiveConfig) else left  
        right_dict = right.effective_content if isinstance(right, EffectiveConfig) else right  
  
        if not isinstance(left_dict, dict) or not isinstance(right_dict, dict):  
            raise ConfigDiffError(message="Both inputs must resolve to dictionaries.")  
  
        added: dict[str, Any] = {}  
        removed: dict[str, Any] = {}  
        changed: dict[str, Any] = {}  
  
        all_keys = set(left_dict.keys()) | set(right_dict.keys())  
  
        for key in sorted(all_keys):  
            if key not in left_dict:  
                added[key] = right_dict[key] if include_values else {"status": "added"}  
            elif key not in right_dict:  
                removed[key] = left_dict[key] if include_values else {"status": "removed"}  
            elif left_dict[key] != right_dict[key]:  
                changed[key] = {  
                    "left": left_dict[key] if include_values else "changed",  
                    "right": right_dict[key] if include_values else "changed",  
                }  
  
        return {  
            "summary": {  
                "added_count": len(added),  
                "removed_count": len(removed),  
                "changed_count": len(changed),  
            },  
            "added": added,  
            "removed": removed,  
            "changed": changed,  
        }  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/base_repository.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Generic, TypeVar  
  
T = TypeVar("T")  
  
  
class InMemoryRepository(Generic[T]):  
    def __init__(self) -> None:  
        self._items: list[T] = []  
  
    def add(self, item: T) -> T:  
        self._items.append(item)  
        return item  
  
    def list_all(self) -> list[T]:  
        return list(self._items)  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/reasoning_repository.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.reasoning_models import ConfigReasoningQuery, ConfigReasoningRecord  
from config_sdk.governance.base_repository import InMemoryRepository  
  
  
class ReasoningRepository(InMemoryRepository[ConfigReasoningRecord]):  
    def query(self, q: ConfigReasoningQuery) -> list[ConfigReasoningRecord]:  
        out = self.list_all()  
        if q.project_name is not None:  
            out = [x for x in out if x.project_name == q.project_name]  
        if q.bundle_id is not None:  
            out = [x for x in out if x.bundle_id == q.bundle_id]  
        if q.effective_config_id is not None:  
            out = [x for x in out if x.effective_config_id == q.effective_config_id]  
        if q.subject_type is not None:  
            out = [x for x in out if x.subject_type == q.subject_type]  
        if q.subject_id is not None:  
            out = [x for x in out if x.subject_id == q.subject_id]  
        return out  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/review_repository.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.review_models import (  
    ConfigReviewQuery,  
    ConfigReviewRequest,  
    ConfigReviewResponseRecord,  
)  
from config_sdk.governance.base_repository import InMemoryRepository  
  
  
class ReviewRequestRepository(InMemoryRepository[ConfigReviewRequest]):  
    def query(self, q: ConfigReviewQuery) -> list[ConfigReviewRequest]:  
        out = self.list_all()  
        if q.project_name is not None:  
            out = [x for x in out if x.project_name == q.project_name]  
        if q.bundle_id is not None:  
            out = [x for x in out if x.bundle_id == q.bundle_id]  
        if q.effective_config_id is not None:  
            out = [x for x in out if x.effective_config_id == q.effective_config_id]  
        if q.subject_type is not None:  
            out = [x for x in out if x.subject_type == q.subject_type]  
        if q.subject_id is not None:  
            out = [x for x in out if x.subject_id == q.subject_id]  
        if q.review_type is not None:  
            out = [x for x in out if x.review_type == q.review_type]  
        if q.status is not None:  
            out = [x for x in out if x.status == q.status]  
        return out  
  
  
class ReviewResponseRepository(InMemoryRepository[ConfigReviewResponseRecord]):  
    def by_review_id(self, review_id: str) -> list[ConfigReviewResponseRecord]:  
        return [x for x in self.list_all() if x.review_id == review_id]  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/decision_repository.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.decision_models import ConfigDecisionQuery, ConfigDecisionRecord  
from config_sdk.governance.base_repository import InMemoryRepository  
  
  
class DecisionRepository(InMemoryRepository[ConfigDecisionRecord]):  
    def query(self, q: ConfigDecisionQuery) -> list[ConfigDecisionRecord]:  
        out = self.list_all()  
        if q.project_name is not None:  
            out = [x for x in out if x.project_name == q.project_name]  
        if q.bundle_id is not None:  
            out = [x for x in out if x.bundle_id == q.bundle_id]  
        if q.effective_config_id is not None:  
            out = [x for x in out if x.effective_config_id == q.effective_config_id]  
        if q.subject_type is not None:  
            out = [x for x in out if x.subject_type == q.subject_type]  
        if q.subject_id is not None:  
            out = [x for x in out if x.subject_id == q.subject_id]  
        if q.decision_type is not None:  
            out = [x for x in out if x.decision_type == q.decision_type]  
        if q.decision_status is not None:  
            out = [x for x in out if x.decision_status == q.decision_status]  
        return out  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/change_repository.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.change_models import ConfigChangeSet, ConfigChangeSetQuery  
from config_sdk.governance.base_repository import InMemoryRepository  
  
  
class ChangeRepository(InMemoryRepository[ConfigChangeSet]):  
    def query(self, q: ConfigChangeSetQuery) -> list[ConfigChangeSet]:  
        out = self.list_all()  
        if q.project_name is not None:  
            out = [x for x in out if x.project_name == q.project_name]  
        if q.bundle_id is not None:  
            out = [x for x in out if x.bundle_id == q.bundle_id]  
        if q.effective_config_id is not None:  
            out = [x for x in out if x.effective_config_id == q.effective_config_id]  
        if q.subject_type is not None:  
            out = [x for x in out if x.subject_type == q.subject_type]  
        if q.subject_id is not None:  
            out = [x for x in out if x.subject_id == q.subject_id]  
        return out  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/trace_repository.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.trace_models import ConfigTraceBundle, ConfigTraceBundleQuery  
from config_sdk.governance.base_repository import InMemoryRepository  
  
  
class TraceRepository(InMemoryRepository[ConfigTraceBundle]):  
    def query(self, q: ConfigTraceBundleQuery) -> list[ConfigTraceBundle]:  
        out = self.list_all()  
        if q.project_name is not None:  
            out = [x for x in out if x.project_name == q.project_name]  
        if q.bundle_id is not None:  
            out = [x for x in out if x.bundle_id == q.bundle_id]  
        if q.effective_config_id is not None:  
            out = [x for x in out if x.effective_config_id == q.effective_config_id]  
        if q.subject_type is not None:  
            out = [x for x in out if x.subject_type == q.subject_type]  
        if q.subject_id is not None:  
            out = [x for x in out if x.subject_id == q.subject_id]  
        return out  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/snapshot_repository.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.snapshot_models import ConfigAuditSnapshot, ConfigSnapshotQuery  
from config_sdk.governance.base_repository import InMemoryRepository  
  
  
class SnapshotRepository(InMemoryRepository[ConfigAuditSnapshot]):  
    def query(self, q: ConfigSnapshotQuery) -> list[ConfigAuditSnapshot]:  
        out = self.list_all()  
        if q.project_name is not None:  
            out = [x for x in out if x.project_name == q.project_name]  
        if q.bundle_id is not None:  
            out = [x for x in out if x.bundle_id == q.bundle_id]  
        if q.effective_config_id is not None:  
            out = [x for x in out if x.effective_config_id == q.effective_config_id]  
        if q.snapshot_type is not None:  
            out = [x for x in out if x.snapshot_type == q.snapshot_type]  
        return out  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/evidence_repository.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.evidence_models import ConfigEvidenceRef  
from config_sdk.governance.base_repository import InMemoryRepository  
  
  
class EvidenceRepository(InMemoryRepository[ConfigEvidenceRef]):  
    pass  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/governance_service.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.change_models import ConfigChangeSet  
from config_sdk.contracts.decision_models import ConfigDecisionRecord  
from config_sdk.contracts.evidence_models import ConfigEvidenceRef  
from config_sdk.contracts.reasoning_models import ConfigReasoningRecord  
from config_sdk.contracts.review_models import (  
    ConfigReviewRequest,  
    ConfigReviewResponseRecord,  
)  
from config_sdk.governance.change_repository import ChangeRepository  
from config_sdk.governance.decision_repository import DecisionRepository  
from config_sdk.governance.evidence_repository import EvidenceRepository  
from config_sdk.governance.reasoning_repository import ReasoningRepository  
from config_sdk.governance.review_repository import (  
    ReviewRequestRepository,  
    ReviewResponseRepository,  
)  
  
  
class GovernanceService:  
    def __init__(  
        self,  
        reasoning_repo: ReasoningRepository,  
        review_request_repo: ReviewRequestRepository,  
        review_response_repo: ReviewResponseRepository,  
        decision_repo: DecisionRepository,  
        change_repo: ChangeRepository,  
        evidence_repo: EvidenceRepository,  
    ) -> None:  
        self.reasoning_repo = reasoning_repo  
        self.review_request_repo = review_request_repo  
        self.review_response_repo = review_response_repo  
        self.decision_repo = decision_repo  
        self.change_repo = change_repo  
        self.evidence_repo = evidence_repo  
  
    def append_reasoning_note(self, record: ConfigReasoningRecord) -> ConfigReasoningRecord:  
        return self.reasoning_repo.add(record)  
  
    def create_change_set(self, change_set: ConfigChangeSet) -> ConfigChangeSet:  
        return self.change_repo.add(change_set)  
  
    def request_review(self, record: ConfigReviewRequest) -> ConfigReviewRequest:  
        return self.review_request_repo.add(record)  
  
    def respond_review(self, record: ConfigReviewResponseRecord) -> ConfigReviewResponseRecord:  
        return self.review_response_repo.add(record)  
  
    def record_decision(self, record: ConfigDecisionRecord) -> ConfigDecisionRecord:  
        return self.decision_repo.add(record)  
  
    def attach_evidence(self, evidence: ConfigEvidenceRef) -> ConfigEvidenceRef:  
        return self.evidence_repo.add(evidence)  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/query_service.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.change_models import ConfigChangeSetQuery  
from config_sdk.contracts.decision_models import ConfigDecisionQuery  
from config_sdk.contracts.reasoning_models import ConfigReasoningQuery  
from config_sdk.contracts.review_models import ConfigReviewQuery  
from config_sdk.contracts.snapshot_models import ConfigSnapshotQuery  
from config_sdk.contracts.trace_models import ConfigTraceBundleQuery  
from config_sdk.governance.change_repository import ChangeRepository  
from config_sdk.governance.decision_repository import DecisionRepository  
from config_sdk.governance.reasoning_repository import ReasoningRepository  
from config_sdk.governance.review_repository import (  
    ReviewRequestRepository,  
    ReviewResponseRepository,  
)  
from config_sdk.governance.snapshot_repository import SnapshotRepository  
from config_sdk.governance.trace_repository import TraceRepository  
  
  
class QueryService:  
    def __init__(  
        self,  
        reasoning_repo: ReasoningRepository,  
        review_request_repo: ReviewRequestRepository,  
        review_response_repo: ReviewResponseRepository,  
        decision_repo: DecisionRepository,  
        change_repo: ChangeRepository,  
        trace_repo: TraceRepository,  
        snapshot_repo: SnapshotRepository,  
    ) -> None:  
        self.reasoning_repo = reasoning_repo  
        self.review_request_repo = review_request_repo  
        self.review_response_repo = review_response_repo  
        self.decision_repo = decision_repo  
        self.change_repo = change_repo  
        self.trace_repo = trace_repo  
        self.snapshot_repo = snapshot_repo  
  
    def query_reasoning_records(self, query: ConfigReasoningQuery):  
        return self.reasoning_repo.query(query)  
  
    def query_review_records(self, query: ConfigReviewQuery):  
        reqs = self.review_request_repo.query(query)  
        ids = {x.review_id for x in reqs}  
        resps = [x for x in self.review_response_repo.list_all() if x.review_id in ids]  
        return {"requests": reqs, "responses": resps}  
  
    def query_decision_records(self, query: ConfigDecisionQuery):  
        return self.decision_repo.query(query)  
  
    def query_change_sets(self, query: ConfigChangeSetQuery):  
        return self.change_repo.query(query)  
  
    def query_trace_bundles(self, query: ConfigTraceBundleQuery):  
        return self.trace_repo.query(query)  
  
    def query_snapshots(self, query: ConfigSnapshotQuery):  
        return self.snapshot_repo.query(query)  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/trace_service.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.change_models import ConfigChangeSetQuery  
from config_sdk.contracts.decision_models import ConfigDecisionQuery  
from config_sdk.contracts.enums import TimelineEventTypeEnum  
from config_sdk.contracts.reasoning_models import ConfigReasoningQuery  
from config_sdk.contracts.review_models import ConfigReviewQuery  
from config_sdk.contracts.trace_models import (  
    ConfigDecisionTrail,  
    ConfigTimelineEvent,  
    ConfigTraceBundle,  
)  
from config_sdk.governance.query_service import QueryService  
from config_sdk.provenance.origin_explainer import OriginExplainer  
from config_sdk.utils.ids import new_id  
from config_sdk.utils.time_utils import utc_now  
  
  
class TraceService:  
    def __init__(  
        self,  
        query_service: QueryService,  
        origin_explainer: OriginExplainer,  
    ) -> None:  
        self.query_service = query_service  
        self.origin_explainer = origin_explainer  
  
    def build_decision_trail(  
        self,  
        subject_type: str,  
        subject_id: str,  
        project_name: str | None = None,  
        bundle_id: str | None = None,  
        effective_config_id: str | None = None,  
        config_hash: str | None = None,  
    ) -> ConfigDecisionTrail:  
        reasoning = self.query_service.query_reasoning_records(  
            ConfigReasoningQuery(  
                project_name=project_name,  
                bundle_id=bundle_id,  
                effective_config_id=effective_config_id,  
                subject_type=subject_type,  
                subject_id=subject_id,  
            )  
        )  
        reviews = self.query_service.query_review_records(  
            ConfigReviewQuery(  
                project_name=project_name,  
                bundle_id=bundle_id,  
                effective_config_id=effective_config_id,  
                subject_type=subject_type,  
                subject_id=subject_id,  
            )  
        )  
        decisions = self.query_service.query_decision_records(  
            ConfigDecisionQuery(  
                project_name=project_name,  
                bundle_id=bundle_id,  
                effective_config_id=effective_config_id,  
                subject_type=subject_type,  
                subject_id=subject_id,  
            )  
        )  
        change_sets = self.query_service.query_change_sets(  
            ConfigChangeSetQuery(  
                project_name=project_name,  
                bundle_id=bundle_id,  
                effective_config_id=effective_config_id,  
                subject_type=subject_type,  
                subject_id=subject_id,  
            )  
        )  
  
        timeline: list[ConfigTimelineEvent] = []  
        for item in reasoning:  
            timeline.append(  
                ConfigTimelineEvent(  
                    event_id=new_id("evt"),  
                    event_type=TimelineEventTypeEnum.REASONING_ADDED,  
                    event_time=item.created_at,  
                    actor_id=item.actor.actor_id,  
                    subject_type=subject_type,  
                    subject_id=subject_id,  
                    summary=item.summary,  
                    linked_refs=[item.reasoning_id],  
                )  
            )  
        for item in reviews["requests"]:  
            timeline.append(  
                ConfigTimelineEvent(  
                    event_id=new_id("evt"),  
                    event_type=TimelineEventTypeEnum.REVIEW_REQUESTED,  
                    event_time=item.created_at,  
                    actor_id=item.requested_by_actor.actor_id,  
                    subject_type=subject_type,  
                    subject_id=subject_id,  
                    summary=item.title,  
                    linked_refs=[item.review_id],  
                )  
            )  
        for item in reviews["responses"]:  
            timeline.append(  
                ConfigTimelineEvent(  
                    event_id=new_id("evt"),  
                    event_type=TimelineEventTypeEnum.REVIEW_RESPONDED,  
                    event_time=item.created_at,  
                    actor_id=item.responded_by_actor.actor_id,  
                    subject_type=subject_type,  
                    subject_id=subject_id,  
                    summary=item.response_text,  
                    linked_refs=[item.review_id, item.review_response_id],  
                )  
            )  
        for item in decisions:  
            timeline.append(  
                ConfigTimelineEvent(  
                    event_id=new_id("evt"),  
                    event_type=TimelineEventTypeEnum.DECISION_RECORDED,  
                    event_time=item.created_at,  
                    actor_id=item.decided_by_actor.actor_id,  
                    subject_type=subject_type,  
                    subject_id=subject_id,  
                    summary=item.title,  
                    linked_refs=[item.decision_id],  
                )  
            )  
  
        timeline = sorted(timeline, key=lambda x: x.event_time)  
  
        return ConfigDecisionTrail(  
            subject_type=subject_type,  
            subject_id=subject_id,  
            project_name=project_name,  
            bundle_id=bundle_id,  
            effective_config_id=effective_config_id,  
            config_hash=config_hash,  
            reasoning_records=reasoning,  
            review_requests=reviews["requests"],  
            review_responses=reviews["responses"],  
            decision_records=decisions,  
            change_sets=change_sets,  
            timeline=timeline,  
            unresolved_issues=[],  
        )  
  
    def build_trace_bundle(  
        self,  
        subject_type: str,  
        subject_id: str,  
        project_name: str | None,  
        bundle_id: str | None,  
        effective_config_id: str | None,  
        config_hash: str | None,  
    ) -> ConfigTraceBundle:  
        trail = self.build_decision_trail(  
            subject_type=subject_type,  
            subject_id=subject_id,  
            project_name=project_name,  
            bundle_id=bundle_id,  
            effective_config_id=effective_config_id,  
            config_hash=config_hash,  
        )  
        return ConfigTraceBundle(  
            trace_bundle_id=new_id("trace"),  
            subject_type=subject_type,  
            subject_id=subject_id,  
            project_name=project_name,  
            bundle_id=bundle_id,  
            effective_config_id=effective_config_id,  
            config_hash=config_hash,  
            decision_trail=trail,  
            provenance_summary=[],  
            current_status="assembled",  
            evidence_refs=[],  
            export_metadata={"built_at": utc_now().isoformat()},  
        )  
  
  
# ================================================================  
# FILE: src/config_sdk/governance/snapshot_service.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.actor_models import ConfigActorRef  
from config_sdk.contracts.snapshot_models import ConfigAuditSnapshot  
from config_sdk.governance.snapshot_repository import SnapshotRepository  
from config_sdk.governance.trace_service import TraceService  
from config_sdk.hashing.config_hashing import ConfigHashing  
from config_sdk.utils.ids import new_id  
from config_sdk.utils.time_utils import utc_now  
  
  
class SnapshotService:  
    def __init__(  
        self,  
        snapshot_repo: SnapshotRepository,  
        trace_service: TraceService,  
        hashing: ConfigHashing,  
    ) -> None:  
        self.snapshot_repo = snapshot_repo  
        self.trace_service = trace_service  
        self.hashing = hashing  
  
    def create_audit_snapshot(  
        self,  
        *,  
        subject_type: str,  
        subject_id: str,  
        snapshot_type: str,  
        exported_by: ConfigActorRef,  
        freeze_reason: str,  
        effective_config,  
    ) -> ConfigAuditSnapshot:  
        trace_bundle = self.trace_service.build_trace_bundle(  
            subject_type=subject_type,  
            subject_id=subject_id,  
            project_name=effective_config.metadata.metadata.get("project_name"),  
            bundle_id=effective_config.bundle_id,  
            effective_config_id=effective_config.effective_config_id,  
            config_hash=effective_config.config_hash_info.config_hash,  
        )  
        snapshot = ConfigAuditSnapshot(  
            snapshot_id=new_id("snap"),  
            snapshot_type=snapshot_type,  
            project_name=effective_config.metadata.metadata.get("project_name"),  
            bundle_id=effective_config.bundle_id,  
            effective_config_id=effective_config.effective_config_id,  
            config_hash=effective_config.config_hash_info.config_hash,  
            exported_at=utc_now(),  
            exported_by_actor=exported_by,  
            freeze_reason=freeze_reason,  
            effective_config=effective_config,  
            change_sets=trace_bundle.decision_trail.change_sets,  
            reasoning_records=trace_bundle.decision_trail.reasoning_records,  
            review_requests=trace_bundle.decision_trail.review_requests,  
            review_responses=trace_bundle.decision_trail.review_responses,  
            decision_records=trace_bundle.decision_trail.decision_records,  
            trace_bundle=trace_bundle,  
            evidence_refs=trace_bundle.evidence_refs,  
            integrity_hash=self.hashing.hash_config(trace_bundle.model_dump()).config_hash,  
            metadata={},  
        )  
        return self.snapshot_repo.add(snapshot)  
  
  
# ================================================================  
# FILE: src/config_sdk/resolvers/config_stack_resolver.py  
# ================================================================  
  
from __future__ import annotations  
  
from config_sdk.contracts.bundle_models import ConfigBundle, EffectiveConfig  
from config_sdk.contracts.enums import (  
    ConfigFormatEnum,  
    ConfigLayerNameEnum,  
    ConfigStatusEnum,  
    ConfigSourceTypeEnum,  
)  
from config_sdk.contracts.layer_models import ConfigLayer  
from config_sdk.contracts.metadata_models import EffectiveConfigMetadata  
from config_sdk.contracts.request_models import ConfigResolutionRequest  
from config_sdk.contracts.source_models import ConfigSourceRef  
from config_sdk.exceptions.errors import ConfigBundleError, ConfigValidationError  
from config_sdk.provenance.provenance_tracker import ProvenanceTracker  
from config_sdk.utils.ids import new_id  
from config_sdk.utils.time_utils import utc_now  
  
  
class ConfigStackResolver:  
    def __init__(  
        self,  
        loader_factory,  
        merge_engine,  
        overlay_resolver,  
        schema_validator,  
        cross_field_validator,  
        bundle_validator,  
        placeholder_resolver,  
        reference_resolver,  
        reference_validator,  
        hashing,  
    ) -> None:  
        self.loader_factory = loader_factory  
        self.merge_engine = merge_engine  
        self.overlay_resolver = overlay_resolver  
        self.schema_validator = schema_validator  
        self.cross_field_validator = cross_field_validator  
        self.bundle_validator = bundle_validator  
        self.placeholder_resolver = placeholder_resolver  
        self.reference_resolver = reference_resolver  
        self.reference_validator = reference_validator  
        self.hashing = hashing  
  
    def load_sources(self, sources: list[ConfigSourceRef]) -> list[ConfigLayer]:  
        return [self.loader_factory.get_loader(src.source_type).load(src) for src in sources]  
  
    def build_bundle(self, request: ConfigResolutionRequest, layers: list[ConfigLayer]) -> ConfigBundle:  
        return ConfigBundle(  
            bundle_id=new_id("bundle"),  
            bundle_name=request.bundle_name,  
            layers=layers,  
            domain_name=request.domain_name,  
            role_name=request.role_name,  
            environment_name=request.environment_name,  
            project_name=request.project_name,  
            bundle_metadata=request.metadata,  
        )  
  
    def _build_runtime_override_layer(self, request: ConfigResolutionRequest) -> ConfigLayer | None:  
        if not request.runtime_override:  
            return None  
  
        source_ref = ConfigSourceRef(  
            source_id=new_id("runtime"),  
            source_type=ConfigSourceTypeEnum.RUNTIME_OVERRIDE,  
            source_name="runtime_override",  
            source_path=None,  
            file_format=ConfigFormatEnum.DICT,  
            layer_name=ConfigLayerNameEnum.RUNTIME,  
            priority=9999,  
            metadata={},  
        )  
        return ConfigLayer(  
            layer_id=new_id("layer"),  
            layer_name=ConfigLayerNameEnum.RUNTIME,  
            priority=9999,  
            source_ref=source_ref,  
            raw_content=request.runtime_override,  
            validated_content=request.runtime_override,  
            schema_name=request.schema_name,  
            status=ConfigStatusEnum.LOADED,  
            metadata={"generated": True},  
        )  
  
    def resolve(self, request: ConfigResolutionRequest) -> EffectiveConfig:  
        layers = self.load_sources(request.sources)  
        bundle = self.build_bundle(request, layers)  
  
        bundle_issues = self.bundle_validator.validate_bundle(bundle, request.schema_name)  
        if any(x["level"] == "error" for x in bundle_issues):  
            raise ConfigBundleError(message=f"Bundle validation failed: {bundle_issues}")  
  
        runtime_layer = self._build_runtime_override_layer(request)  
        if runtime_layer:  
            bundle.layers.append(runtime_layer)  
  
        selected_layers = self.overlay_resolver.select_relevant_layers(bundle, request)  
  
        for layer in selected_layers:  
            validated = self.schema_validator.validate(layer.raw_content, request.schema_name)  
            cross_issues = self.cross_field_validator.validate(validated, request.schema_name)  
            if any(x["level"] == "error" for x in cross_issues):  
                raise ConfigValidationError(  
                    message=f"Cross-field validation failed in layer={layer.layer_name.value}: {cross_issues}"  
                )  
            layer.validated_content = validated  
            layer.schema_name = request.schema_name  
            layer.status = ConfigStatusEnum.VALIDATED  
  
        merged_dict, provenance_seed = self.merge_engine.merge_layers(selected_layers)  
        merged_dict = self.placeholder_resolver.resolve_placeholders(  
            merged_dict,  
            validation_mode=request.validation_mode,  
        )  
        merged_dict = self.reference_resolver.resolve_internal_refs(merged_dict)  
  
        reference_issues = self.reference_validator.validate_references(  
            merged_dict,  
            validation_mode=request.validation_mode,  
        )  
        if any(x["level"] == "error" for x in reference_issues):  
            raise ConfigValidationError(message=f"Reference validation failed: {reference_issues}")  
  
        merged_dict = self.schema_validator.validate(merged_dict, request.schema_name)  
  
        hash_info = self.hashing.hash_config(merged_dict)  
  
        tracker = ProvenanceTracker()  
        for layer in selected_layers:  
            content = layer.validated_content or layer.raw_content  
            for key, value in content.items():  
                tracker.record_override(  
                    key_path=key,  
                    effective_value=merged_dict.get(key),  
                    source_layer=layer.layer_name.value,  
                    source_name=layer.source_ref.source_name,  
                    source_path=layer.source_ref.source_path,  
                    previous_layer=provenance_seed.get(key),  
                )  
  
        return EffectiveConfig(  
            effective_config_id=new_id("cfg_eff"),  
            bundle_id=bundle.bundle_id,  
            bundle_name=bundle.bundle_name,  
            effective_content=merged_dict,  
            config_hash_info=hash_info,  
            provenance_map=tracker.build_map(),  
            metadata=EffectiveConfigMetadata(  
                bundle_name=bundle.bundle_name,  
                resolved_at=utc_now(),  
                layer_order=[x.layer_name.value for x in selected_layers],  
                validation_mode=request.validation_mode,  
                schema_name=request.schema_name,  
                metadata={  
                    **request.metadata,  
                    "project_name": request.project_name,  
                    "domain_name": request.domain_name,  
                    "role_name": request.role_name,  
                    "environment_name": request.environment_name,  
                },  
            ),  
            validation_status=ConfigStatusEnum.RESOLVED,  
        )  
  
  
# ================================================================  
# FILE: src/config_sdk/services/config_service.py  
# ================================================================  
  
from __future__ import annotations  
  
from typing import Any  
  
from config_sdk.contracts.actor_models import ConfigActorRef  
from config_sdk.contracts.bundle_models import ConfigBundle, EffectiveConfig  
from config_sdk.contracts.change_models import ConfigChangeSet, ConfigChangeSetQuery  
from config_sdk.contracts.decision_models import ConfigDecisionQuery, ConfigDecisionRecord  
from config_sdk.contracts.evidence_models import ConfigEvidenceRef  
from config_sdk.contracts.layer_models import ConfigLayer  
from config_sdk.contracts.reasoning_models import ConfigReasoningQuery, ConfigReasoningRecord  
from config_sdk.contracts.request_models import (  
    ConfigDiffRequest,  
    ConfigResolutionRequest,  
    ConfigValidationRequest,  
)  
from config_sdk.contracts.response_models import (  
    ConfigDiffResponse,  
    ConfigResolutionResponse,  
    ConfigValidationResponse,  
)  
from config_sdk.contracts.review_models import (  
    ConfigReviewQuery,  
    ConfigReviewRequest,  
    ConfigReviewResponseRecord,  
)  
from config_sdk.contracts.snapshot_models import ConfigSnapshotQuery  
from config_sdk.contracts.source_models import ConfigSourceRef  
from config_sdk.contracts.trace_models import ConfigTraceBundleQuery  
from config_sdk.contracts.enums import ResolutionStatusEnum, ValidationModeEnum  
from config_sdk.governance.change_repository import ChangeRepository  
from config_sdk.governance.decision_repository import DecisionRepository  
from config_sdk.governance.evidence_repository import EvidenceRepository  
from config_sdk.governance.governance_service import GovernanceService  
from config_sdk.governance.query_service import QueryService  
from config_sdk.governance.reasoning_repository import ReasoningRepository  
from config_sdk.governance.review_repository import (  
    ReviewRequestRepository,  
    ReviewResponseRepository,  
)  
from config_sdk.governance.snapshot_repository import SnapshotRepository  
from config_sdk.governance.snapshot_service import SnapshotService  
from config_sdk.governance.trace_repository import TraceRepository  
from config_sdk.governance.trace_service import TraceService  
from config_sdk.hashing.config_hashing import ConfigHashing  
from config_sdk.loaders.loader_factory import LoaderFactory  
from config_sdk.mergers.merge_engine import MergeEngine  
from config_sdk.mergers.overlay_resolver import OverlayResolver  
from config_sdk.provenance.config_diff import ConfigDiff  
from config_sdk.provenance.origin_explainer import OriginExplainer  
from config_sdk.resolvers.config_stack_resolver import ConfigStackResolver  
from config_sdk.resolvers.effective_config_renderer import EffectiveConfigRenderer  
from config_sdk.resolvers.placeholder_resolver import PlaceholderResolver  
from config_sdk.resolvers.reference_resolver import ReferenceResolver  
from config_sdk.utils.io_utils import write_text_file  
from config_sdk.validators.bundle_validator import BundleValidator  
from config_sdk.validators.cross_field_validator import CrossFieldValidator  
from config_sdk.validators.reference_validator import ReferenceValidator  
from config_sdk.validators.schema_validator import SchemaValidator  
  
  
class ConfigService:  
    def __init__(self, in_memory_payloads: dict[str, dict] | None = None) -> None:  
        loader_factory = LoaderFactory(in_memory_payloads=in_memory_payloads)  
        schema_validator = SchemaValidator()  
        self._renderer = EffectiveConfigRenderer()  
        self._origin_explainer = OriginExplainer()  
        self._hashing = ConfigHashing()  
        self._diff = ConfigDiff()  
        self._bundle_validator = BundleValidator()  
  
        self._resolver = ConfigStackResolver(  
            loader_factory=loader_factory,  
            merge_engine=MergeEngine(),  
            overlay_resolver=OverlayResolver(),  
            schema_validator=schema_validator,  
            cross_field_validator=CrossFieldValidator(),  
            bundle_validator=self._bundle_validator,  
            placeholder_resolver=PlaceholderResolver(),  
            reference_resolver=ReferenceResolver(),  
            reference_validator=ReferenceValidator(),  
            hashing=self._hashing,  
        )  
        self._loader_factory = loader_factory  
        self._schema_validator = schema_validator  
  
        self._reasoning_repo = ReasoningRepository()  
        self._review_request_repo = ReviewRequestRepository()  
        self._review_response_repo = ReviewResponseRepository()  
        self._decision_repo = DecisionRepository()  
        self._change_repo = ChangeRepository()  
        self._trace_repo = TraceRepository()  
        self._snapshot_repo = SnapshotRepository()  
        self._evidence_repo = EvidenceRepository()  
  
        self._governance = GovernanceService(  
            reasoning_repo=self._reasoning_repo,  
            review_request_repo=self._review_request_repo,  
            review_response_repo=self._review_response_repo,  
            decision_repo=self._decision_repo,  
            change_repo=self._change_repo,  
            evidence_repo=self._evidence_repo,  
        )  
        self._query = QueryService(  
            reasoning_repo=self._reasoning_repo,  
            review_request_repo=self._review_request_repo,  
            review_response_repo=self._review_response_repo,  
            decision_repo=self._decision_repo,  
            change_repo=self._change_repo,  
            trace_repo=self._trace_repo,  
            snapshot_repo=self._snapshot_repo,  
        )  
        self._trace = TraceService(  
            query_service=self._query,  
            origin_explainer=self._origin_explainer,  
        )  
        self._snapshot = SnapshotService(  
            snapshot_repo=self._snapshot_repo,  
            trace_service=self._trace,  
            hashing=self._hashing,  
        )  
  
    def load_config_source(self, source_ref: ConfigSourceRef) -> ConfigLayer:  
        loader = self._loader_factory.get_loader(source_ref.source_type)  
        return loader.load(source_ref)  
  
    def load_bundle(  
        self,  
        sources: list[ConfigSourceRef],  
        bundle_name: str,  
        domain_name: str | None = None,  
        role_name: str | None = None,  
        environment_name: str | None = None,  
        project_name: str | None = None,  
        metadata: dict[str, Any] | None = None,  
    ) -> ConfigBundle:  
        layers = [self.load_config_source(src) for src in sources]  
        return ConfigBundle(  
            bundle_id=f"bundle_{bundle_name}",  
            bundle_name=bundle_name,  
            layers=layers,  
            domain_name=domain_name,  
            role_name=role_name,  
            environment_name=environment_name,  
            project_name=project_name,  
            bundle_metadata=metadata or {},  
        )  
  
    def validate_layer(  
        self,  
        layer: ConfigLayer,  
        schema_name: str | None = None,  
        validation_mode: ValidationModeEnum = ValidationModeEnum.STRICT,  
    ) -> ConfigValidationResponse:  
        try:  
            validated = self._schema_validator.validate(layer.raw_content, schema_name)  
            layer.validated_content = validated  
            return ConfigValidationResponse(  
                status="success",  
                message="Layer validation succeeded.",  
                is_valid=True,  
                data={"layer_id": layer.layer_id, "schema_name": schema_name},  
                references={"source_id": layer.source_ref.source_id},  
            )  
        except Exception as exc:  
            return ConfigValidationResponse(  
                status="failed",  
                message="Layer validation failed.",  
                is_valid=False,  
                errors=[{"message": str(exc)}],  
                references={"source_id": layer.source_ref.source_id},  
            )  
  
    def validate_bundle(  
        self,  
        bundle: ConfigBundle,  
        schema_name: str | None = None,  
        validation_mode: ValidationModeEnum = ValidationModeEnum.STRICT,  
    ) -> ConfigValidationResponse:  
        issues = self._bundle_validator.validate_bundle(bundle, schema_name)  
        has_error = any(x["level"] == "error" for x in issues)  
        return ConfigValidationResponse(  
            status="failed" if has_error else "success",  
            message="Bundle validation completed.",  
            is_valid=not has_error,  
            data={"bundle_id": bundle.bundle_id, "bundle_name": bundle.bundle_name},  
            warnings=[x for x in issues if x["level"] != "error"],  
            errors=[x for x in issues if x["level"] == "error"],  
            references={"bundle_id": bundle.bundle_id},  
        )  
  
    def validate_config(self, request: ConfigValidationRequest) -> ConfigValidationResponse:  
        try:  
            config_dict = request.config_dict  
            if config_dict is None and request.source_ref is not None:  
                layer = self.load_config_source(request.source_ref)  
                config_dict = layer.raw_content  
            if config_dict is None:  
                raise ValueError("Either config_dict or source_ref is required.")  
            validated = self._schema_validator.validate(config_dict, request.schema_name)  
            return ConfigValidationResponse(  
                status="success",  
                message="Config validation succeeded.",  
                is_valid=True,  
                data={"validated_config": validated},  
            )  
        except Exception as exc:  
            return ConfigValidationResponse(  
                status="failed",  
                message="Config validation failed.",  
                is_valid=False,  
                errors=[{"message": str(exc)}],  
            )  
  
    def resolve_config_stack(self, request: ConfigResolutionRequest) -> ConfigResolutionResponse:  
        try:  
            effective = self._resolver.resolve(request)  
            return ConfigResolutionResponse(  
                status="success",  
                message="Effective config resolved successfully.",  
                data={  
                    "effective_config": effective.model_dump(),  
                    "effective_config_id": effective.effective_config_id,  
                    "config_hash": effective.config_hash_info.config_hash,  
                    "layer_order": effective.metadata.layer_order,  
                },  
                references={  
                    "bundle_name": effective.bundle_name,  
                    "bundle_id": effective.bundle_id,  
                    "source_ids": [x.source_id for x in request.sources],  
                },  
                agent_hint={  
                    "reasoning_summary": "Runtime config stack resolved with strict validation.",  
                    "recommended_next_action": "resolve_runtime_stack",  
                    "safe_to_continue": True,  
                },  
                observability_hint={  
                    "should_write_event": True,  
                    "event_type": "config_resolved",  
                },  
            )  
        except Exception as exc:  
            return ConfigResolutionResponse(  
                status="failed",  
                message="Config resolution failed.",  
                errors=[{"message": str(exc)}],  
                references={"bundle_name": request.bundle_name},  
                agent_hint={  
                    "reasoning_summary": "Config resolution failed and should be corrected before proceeding.",  
                    "recommended_next_action": "fix_config",  
                    "safe_to_continue": False,  
                },  
                observability_hint={  
                    "should_write_event": True,  
                    "event_type": "config_resolution_failed",  
                },  
            )  
  
    def render_effective_config(self, effective_config: EffectiveConfig, fmt: str = "dict") -> dict[str, Any] | str:  
        if fmt == "dict":  
            return self._renderer.render_dict(effective_config)  
        if fmt == "json":  
            return self._renderer.render_json(effective_config)  
        if fmt == "yaml":  
            return self._renderer.render_yaml(effective_config)  
        raise ValueError(f"Unsupported render format: {fmt}")  
  
    def explain_config_origin(self, effective_config: EffectiveConfig, key_path: str) -> dict[str, Any]:  
        entry = self._origin_explainer.explain_key(effective_config, key_path)  
        return entry or {"message": "No provenance entry found.", "key_path": key_path}  
  
    def get_config_value(self, effective_config: EffectiveConfig, key_path: str, default: Any | None = None) -> Any:  
        current: Any = effective_config.effective_content  
        for part in key_path.split("."):  
            if not isinstance(current, dict) or part not in current:  
                return default  
            current = current[part]  
        return current  
  
    def diff_config_bundles(self, request: ConfigDiffRequest) -> ConfigDiffResponse:  
        try:  
            diff_result = self._diff.diff(request.left_config, request.right_config, include_values=request.include_values)  
            return ConfigDiffResponse(  
                status="success",  
                message="Config diff completed successfully.",  
                data=diff_result,  
            )  
        except Exception as exc:  
            return ConfigDiffResponse(  
                status="failed",  
                message="Config diff failed.",  
                errors=[{"message": str(exc)}],  
            )  
  
    def hash_config(self, config_dict: dict[str, Any]):  
        return self._hashing.hash_config(config_dict)  
  
    def export_effective_config(self, effective_config: EffectiveConfig, path: str, fmt: str = "yaml") -> dict[str, Any]:  
        rendered = self.render_effective_config(effective_config, fmt=fmt)  
        if not isinstance(rendered, str):  
            raise ValueError("Rendered export format must be string-based.")  
        write_text_file(path, rendered)  
        return {  
            "status": "success",  
            "path": path,  
            "format": fmt,  
            "effective_config_id": effective_config.effective_config_id,  
        }  
  
    def append_reasoning_note(self, record: ConfigReasoningRecord) -> ConfigReasoningRecord:  
        return self._governance.append_reasoning_note(record)  
  
    def create_change_set(self, change_set: ConfigChangeSet) -> ConfigChangeSet:  
        return self._governance.create_change_set(change_set)  
  
    def request_review(self, record: ConfigReviewRequest) -> ConfigReviewRequest:  
        return self._governance.request_review(record)  
  
    def respond_review(self, record: ConfigReviewResponseRecord) -> ConfigReviewResponseRecord:  
        return self._governance.respond_review(record)  
  
    def close_review(  
        self,  
        review_id: str,  
        closed_by: ConfigActorRef,  
        resolution_status: ResolutionStatusEnum,  
        notes: str | None = None,  
    ) -> dict[str, Any]:  
        return {  
            "status": "success",  
            "review_id": review_id,  
            "closed_by": closed_by.actor_id,  
            "resolution_status": resolution_status.value,  
            "notes": notes,  
        }  
  
    def record_decision(self, record: ConfigDecisionRecord) -> ConfigDecisionRecord:  
        return self._governance.record_decision(record)  
  
    def supersede_decision(self, old_decision_id: str, new_decision: ConfigDecisionRecord) -> ConfigDecisionRecord:  
        new_decision.supersedes_decision_id = old_decision_id  
        return self._governance.record_decision(new_decision)  
  
    def attach_evidence(self, subject_type: str, subject_id: str, evidence_refs: list[ConfigEvidenceRef]) -> dict[str, Any]:  
        for evidence in evidence_refs:  
            self._governance.attach_evidence(evidence)  
        return {"status": "success", "subject_type": subject_type, "subject_id": subject_id}  
  
    def query_reasoning_records(self, query: ConfigReasoningQuery):  
        return self._query.query_reasoning_records(query)  
  
    def query_review_records(self, query: ConfigReviewQuery):  
        return self._query.query_review_records(query)  
  
    def query_decision_records(self, query: ConfigDecisionQuery):  
        return self._query.query_decision_records(query)  
  
    def query_change_sets(self, query: ConfigChangeSetQuery):  
        return self._query.query_change_sets(query)  
  
    def query_trace_bundles(self, query: ConfigTraceBundleQuery):  
        return self._query.query_trace_bundles(query)  
  
    def query_snapshots(self, query: ConfigSnapshotQuery):  
        return self._query.query_snapshots(query)  
  
    def build_decision_trail(  
        self,  
        subject_type: str,  
        subject_id: str,  
        project_name: str | None = None,  
        bundle_id: str | None = None,  
        effective_config_id: str | None = None,  
        config_hash: str | None = None,  
    ):  
        return self._trace.build_decision_trail(  
            subject_type=subject_type,  
            subject_id=subject_id,  
            project_name=project_name,  
            bundle_id=bundle_id,  
            effective_config_id=effective_config_id,  
            config_hash=config_hash,  
        )  
  
    def build_trace_bundle(  
        self,  
        subject_type: str,  
        subject_id: str,  
        project_name: str | None = None,  
        bundle_id: str | None = None,  
        effective_config_id: str | None = None,  
        config_hash: str | None = None,  
    ):  
        trace_bundle = self._trace.build_trace_bundle(  
            subject_type=subject_type,  
            subject_id=subject_id,  
            project_name=project_name,  
            bundle_id=bundle_id,  
            effective_config_id=effective_config_id,  
            config_hash=config_hash,  
        )  
        self._trace_repo.add(trace_bundle)  
        return trace_bundle  
  
    def render_trace_bundle(self, trace_bundle, fmt: str = "dict"):  
        if fmt == "dict":  
            return trace_bundle.model_dump()  
        raise ValueError(f"Unsupported render format: {fmt}")  
  
    def summarize_governance_history(self, subject_type: str, subject_id: str) -> dict[str, Any]:  
        tb = self.build_trace_bundle(subject_type=subject_type, subject_id=subject_id)  
        return {  
            "subject_type": subject_type,  
            "subject_id": subject_id,  
            "reasoning_count": len(tb.decision_trail.reasoning_records),  
            "review_request_count": len(tb.decision_trail.review_requests),  
            "review_response_count": len(tb.decision_trail.review_responses),  
            "decision_count": len(tb.decision_trail.decision_records),  
            "change_set_count": len(tb.decision_trail.change_sets),  
            "timeline_event_count": len(tb.decision_trail.timeline),  
        }  
  
    def explain_change_impact(self, change_set_id: str) -> dict[str, Any]:  
        matches = [x for x in self._change_repo.list_all() if x.change_set_id == change_set_id]  
        if not matches:  
            return {"status": "not_found", "change_set_id": change_set_id}  
        change_set = matches[0]  
        return {  
            "change_set_id": change_set_id,  
            "summary": change_set.summary,  
            "item_count": len(change_set.items),  
            "items": [item.model_dump() for item in change_set.items],  
        }  
  
    def create_audit_snapshot(  
        self,  
        subject_type: str,  
        subject_id: str,  
        snapshot_type: str,  
        exported_by: ConfigActorRef,  
        freeze_reason: str,  
        effective_config: EffectiveConfig,  
    ):  
        return self._snapshot.create_audit_snapshot(  
            subject_type=subject_type,  
            subject_id=subject_id,  
            snapshot_type=snapshot_type,  
            exported_by=exported_by,  
            freeze_reason=freeze_reason,  
            effective_config=effective_config,  
        )  
  
    def validate_snapshot_integrity(self, snapshot) -> dict[str, Any]:  
        recomputed = self._hashing.hash_config(snapshot.trace_bundle.model_dump()).config_hash  
        return {  
            "snapshot_id": snapshot.snapshot_id,  
            "stored_integrity_hash": snapshot.integrity_hash,  
            "recomputed_integrity_hash": recomputed,  
            "is_valid": snapshot.integrity_hash == recomputed,  
        }  
  
    def export_snapshot(self, snapshot, path: str, fmt: str = "json") -> dict[str, Any]:  
        if fmt != "json":  
            raise ValueError("Only json export in starter skeleton.")  
        import json  
        write_text_file(path, json.dumps(snapshot.model_dump(mode="json"), indent=2))  
        return {"status": "success", "snapshot_id": snapshot.snapshot_id, "path": path, "format": fmt}  
  
  
# ================================================================  
# FILE: src/config_sdk/services/public_service.py  
# ================================================================  
  
from config_sdk.services.config_service import ConfigService  
  
__all__ = ["ConfigService"]  
  
  
# ================================================================  
# FILE: src/config_sdk/__init__.py  
# ================================================================  
  
from config_sdk.version import __version__  
from config_sdk.services.config_service import ConfigService  
  
from config_sdk.contracts.request_models import (  
    ConfigResolutionRequest,  
    ConfigValidationRequest,  
    ConfigDiffRequest,  
)  
from config_sdk.contracts.response_models import (  
    ConfigResolutionResponse,  
    ConfigValidationResponse,  
    ConfigDiffResponse,  
)  
from config_sdk.contracts.source_models import ConfigSourceRef, SourceMetadata  
from config_sdk.contracts.layer_models import ConfigLayer, LayerSelectionCriteria  
from config_sdk.contracts.bundle_models import ConfigBundle, EffectiveConfig  
from config_sdk.contracts.metadata_models import (  
    ConfigProvenanceEntry,  
    ConfigHashInfo,  
    EffectiveConfigMetadata,  
)  
from config_sdk.contracts.actor_models import ConfigActorRef  
from config_sdk.contracts.agent_models import ConfigActionProposal, ConfigAgentOutput  
from config_sdk.contracts.change_models import ConfigChangeItem, ConfigChangeSet, ConfigChangeSetQuery  
from config_sdk.contracts.reasoning_models import ConfigReasoningRecord, ConfigReasoningQuery  
from config_sdk.contracts.review_models import (  
    ConfigReviewRequest,  
    ConfigReviewResponseRecord,  
    ConfigReviewQuery,  
)  
from config_sdk.contracts.decision_models import ConfigDecisionRecord, ConfigDecisionQuery  
from config_sdk.contracts.trace_models import (  
    ConfigTimelineEvent,  
    ConfigDecisionTrail,  
    ConfigTraceBundle,  
    ConfigTraceBundleQuery,  
)  
from config_sdk.contracts.snapshot_models import ConfigAuditSnapshot, ConfigSnapshotQuery  
from config_sdk.contracts.evidence_models import ConfigEvidenceRef  
from config_sdk.exceptions.errors import *  
  
__all__ = [  
    "__version__",  
    "ConfigService",  
    "ConfigResolutionRequest",  
    "ConfigValidationRequest",  
    "ConfigDiffRequest",  
    "ConfigResolutionResponse",  
    "ConfigValidationResponse",  
    "ConfigDiffResponse",  
    "ConfigSourceRef",  
    "SourceMetadata",  
    "ConfigLayer",  
    "LayerSelectionCriteria",  
    "ConfigBundle",  
    "EffectiveConfig",  
    "ConfigProvenanceEntry",  
    "ConfigHashInfo",  
    "EffectiveConfigMetadata",  
    "ConfigActorRef",  
    "ConfigActionProposal",  
    "ConfigAgentOutput",  
    "ConfigChangeItem",  
    "ConfigChangeSet",  
    "ConfigChangeSetQuery",  
    "ConfigReasoningRecord",  
    "ConfigReasoningQuery",  
    "ConfigReviewRequest",  
    "ConfigReviewResponseRecord",  
    "ConfigReviewQuery",  
    "ConfigDecisionRecord",  
    "ConfigDecisionQuery",  
    "ConfigTimelineEvent",  
    "ConfigDecisionTrail",  
    "ConfigTraceBundle",  
    "ConfigTraceBundleQuery",  
    "ConfigAuditSnapshot",  
    "ConfigSnapshotQuery",  
    "ConfigEvidenceRef",  
]  
  
  
# ================================================================  
# FILE: tests/unit/test_merge_engine.py  
# ================================================================  
  
from config_sdk.contracts.enums import MergeStrategyEnum  
  
  
def test_merge_engine_smoke():  
    from config_sdk.mergers.merge_engine import MergeEngine  
  
    engine = MergeEngine()  
    merged = engine.merge_dicts(  
        {"a": 1, "b": {"x": 1}, "c": [1]},  
        {"b": {"y": 2}, "c": [2], "d": 9},  
        strategy_map={"c": MergeStrategyEnum.APPEND_UNIQUE},  
    )  
    assert merged["a"] == 1  
    assert merged["b"]["x"] == 1  
    assert merged["b"]["y"] == 2  
    assert merged["c"] == [1, 2]  
    assert merged["d"] == 9  
  
  
# ================================================================  
# FILE: tests/unit/test_hashing.py  
# ================================================================  
  
def test_hash_is_deterministic():  
    from config_sdk.hashing.config_hashing import ConfigHashing  
  
    service = ConfigHashing()  
    left = {"b": 2, "a": 1}  
    right = {"a": 1, "b": 2}  
    left_hash = service.hash_config(left).config_hash  
    right_hash = service.hash_config(right).config_hash  
    assert left_hash == right_hash  
  
  
# ================================================================  
# FILE: tests/unit/test_placeholder_resolver.py  
# ================================================================  
  
def test_env_placeholder_resolution(monkeypatch):  
    from config_sdk.contracts.enums import ValidationModeEnum  
    from config_sdk.resolvers.placeholder_resolver import PlaceholderResolver  
  
    monkeypatch.setenv("MY_TEST_VAR", "hello")  
    resolver = PlaceholderResolver()  
    result = resolver.resolve_placeholders(  
        {"x": "${env:MY_TEST_VAR}"},  
        validation_mode=ValidationModeEnum.STRICT,  
    )  
    assert result["x"] == "hello"  
  
  
# ================================================================  
# FILE: tests/integration/test_config_service_resolution.py  
# ================================================================  
  
def test_config_service_resolution_in_memory():  
    from config_sdk.contracts.enums import (  
        ConfigFormatEnum,  
        ConfigLayerNameEnum,  
        ConfigSourceTypeEnum,  
    )  
    from config_sdk.contracts.request_models import ConfigResolutionRequest  
    from config_sdk.contracts.source_models import ConfigSourceRef  
    from config_sdk.services.config_service import ConfigService  
  
    payloads = {  
        "base_1": {"workflow": {"review_required": False, "approval_required": False}},  
        "domain_1": {"workflow": {"review_required": True}},  
    }  
  
    service = ConfigService(in_memory_payloads=payloads)  
  
    req = ConfigResolutionRequest(  
        bundle_name="demo_bundle",  
        sources=[  
            ConfigSourceRef(  
                source_id="base_1",  
                source_type=ConfigSourceTypeEnum.IN_MEMORY_DICT,  
                source_name="base",  
                source_path=None,  
                file_format=ConfigFormatEnum.DICT,  
                layer_name=ConfigLayerNameEnum.BASE,  
                priority=10,  
            ),  
            ConfigSourceRef(  
                source_id="domain_1",  
                source_type=ConfigSourceTypeEnum.IN_MEMORY_DICT,  
                source_name="domain",  
                source_path=None,  
                file_format=ConfigFormatEnum.DICT,  
                layer_name=ConfigLayerNameEnum.DOMAIN,  
                priority=20,  
            ),  
        ],  
    )  
  
    response = service.resolve_config_stack(req)  
    assert response.status == "success"  
    effective = response.data["effective_config"]["effective_content"]  
    assert effective["workflow"]["review_required"] is True  
    assert effective["workflow"]["approval_required"] is False  
  
  
# ================================================================  
# FILE: tests/governance/test_reasoning_decision_trace.py  
# ================================================================  
  
from config_sdk.contracts.actor_models import ConfigActorRef  
from config_sdk.contracts.agent_models import ConfigActionProposal, ConfigAgentOutput  
from config_sdk.contracts.change_models import ConfigChangeItem, ConfigChangeSet  
from config_sdk.contracts.decision_models import ConfigDecisionRecord  
from config_sdk.contracts.enums import (  
    ActorTypeEnum,  
    AuthorityLevelEnum,  
    ChangeTypeEnum,  
    DecisionBasisTypeEnum,  
    DecisionStatusEnum,  
    DecisionTypeEnum,  
    MaterialityEnum,  
)  
from config_sdk.contracts.reasoning_models import ConfigReasoningRecord  
from config_sdk.utils.ids import new_id  
from config_sdk.utils.time_utils import utc_now  
  
  
def test_governance_records_are_queryable():  
    from config_sdk.services.config_service import ConfigService  
  
    service = ConfigService()  
  
    actor = ConfigActorRef(  
        actor_id="u1",  
        actor_name="Edmun",  
        actor_type=ActorTypeEnum.HUMAN,  
        actor_role="model_developer",  
        authority_level=AuthorityLevelEnum.APPROVE,  
        is_human=True,  
    )  
  
    reasoning = service.append_reasoning_note(  
        ConfigReasoningRecord(  
            reasoning_id=new_id("rsn"),  
            subject_type="effective_config",  
            subject_id="cfg_1",  
            project_name="alpha",  
            bundle_id="bundle_1",  
            effective_config_id="cfg_1",  
            config_hash="hash1",  
            actor=actor,  
            summary="Need to enable review gate in prod.",  
            agent_output=ConfigAgentOutput(  
                proposed_action=ConfigActionProposal(  
                    action_type="set_value",  
                    target_path="workflow.review_required",  
                    proposed_value=True,  
                ),  
                rationale=["Prod config requires review."],  
                assumptions=["Prod routing applies."],  
                evidence_refs=["cfg:domain"],  
                confidence=0.91,  
            ),  
            created_at=utc_now(),  
        )  
    )  
  
    service.create_change_set(  
        ConfigChangeSet(  
            change_set_id=new_id("chg"),  
            subject_type="effective_config",  
            subject_id="cfg_1",  
            project_name="alpha",  
            bundle_id="bundle_1",  
            effective_config_id="cfg_1",  
            config_hash="hash1",  
            items=[  
                ConfigChangeItem(  
                    change_id=new_id("item"),  
                    key_path="workflow.review_required",  
                    before_value=False,  
                    after_value=True,  
                    change_type=ChangeTypeEnum.UPDATE,  
                    materiality_flag=MaterialityEnum.MATERIAL,  
                )  
            ],  
            summary="Enable review gate",  
            created_at=utc_now(),  
        )  
    )  
  
    service.record_decision(  
        ConfigDecisionRecord(  
            decision_id=new_id("dec"),  
            subject_type="effective_config",  
            subject_id="cfg_1",  
            project_name="alpha",  
            bundle_id="bundle_1",  
            effective_config_id="cfg_1",  
            config_hash="hash1",  
            decision_type=DecisionTypeEnum.CONFIG_CHANGE,  
            decision_status=DecisionStatusEnum.APPROVED,  
            decision_basis_type=DecisionBasisTypeEnum.POLICY_BASED,  
            title="Approve review gate",  
            rationale="Aligned with production control policy.",  
            decided_by_actor=actor,  
            linked_reasoning_refs=[reasoning.reasoning_id],  
            created_at=utc_now(),  
        )  
    )  
  
    summary = service.summarize_governance_history("effective_config", "cfg_1")  
    assert summary["reasoning_count"] == 1  
    assert summary["decision_count"] == 1  
  
  
# ================================================================  
# FILE: tests/governance/test_snapshot_integrity.py  
# ================================================================  
  
def test_snapshot_integrity_roundtrip():  
    from config_sdk.contracts.actor_models import ConfigActorRef  
    from config_sdk.contracts.bundle_models import EffectiveConfig  
    from config_sdk.contracts.enums import ActorTypeEnum, AuthorityLevelEnum, ValidationModeEnum  
    from config_sdk.contracts.metadata_models import ConfigHashInfo, EffectiveConfigMetadata  
    from config_sdk.services.config_service import ConfigService  
    from config_sdk.utils.time_utils import utc_now  
  
    service = ConfigService()  
    actor = ConfigActorRef(  
        actor_id="approver_1",  
        actor_name="Approver",  
        actor_type=ActorTypeEnum.HUMAN,  
        actor_role="approver",  
        authority_level=AuthorityLevelEnum.APPROVE,  
        is_human=True,  
    )  
  
    effective = EffectiveConfig(  
        effective_config_id="cfg_eff_1",  
        bundle_id="bundle_1",  
        bundle_name="bundle_1",  
        effective_content={"workflow": {"review_required": True}},  
        config_hash_info=ConfigHashInfo(  
            config_hash="abc123",  
            hash_algorithm="sha256",  
            normalized_size=10,  
            short_hash="abc123",  
        ),  
        provenance_map={},  
        metadata=EffectiveConfigMetadata(  
            bundle_name="bundle_1",  
            resolved_at=utc_now(),  
            layer_order=["base", "domain"],  
            validation_mode=ValidationModeEnum.STRICT,  
        ),  
    )  
  
    snap = service.create_audit_snapshot(  
        subject_type="effective_config",  
        subject_id=effective.effective_config_id,  
        snapshot_type="validation_pack",  
        exported_by=actor,  
        freeze_reason="validation submission",  
        effective_config=effective,  
    )  
    result = service.validate_snapshot_integrity(snap)  
    assert "is_valid" in result  
  
  
# ================================================================  
# FILE: pyproject.toml  
# ================================================================  
  
[project]  
name = "config-sdk"  
version = "0.3.0"  
description = "Central configuration SDK for the agentic AI MDLC platform"  
requires-python = ">=3.11"  
dependencies = [  
  "pydantic>=2.6",  
  "PyYAML>=6.0"  
]  
  
[project.optional-dependencies]  
toml = []  
fast = ["orjson>=3.9"]  
diff = ["deepdiff>=7.0"]  
test = [  
  "pytest>=8.0",  
  "pytest-cov>=5.0",  
  "mypy>=1.8"  
]  
  
[build-system]  
requires = ["hatchling"]  
build-backend = "hatchling.build"  
