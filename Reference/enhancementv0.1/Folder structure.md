# Folder structure  
  
====================================================================  
FOLDER STRUCTURE + FILE-BY-FILE IMPLEMENTATION BLUEPRINT  
ENTERPRISE AGENTIC AI MODEL LIFECYCLE PLATFORM  
INITIAL FOUNDATION BUILD  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This blueprint proposes a practical, implementation-ready folder  
structure and file-by-file breakdown for the platform foundation.  
  
It focuses first on:  
- runtime resolver  
- shared schemas  
- controller layer  
- first six SDKs  
- bridge layer needed for Jupyter / agent integration  
  
This is designed to be:  
- modular  
- Spark/CML friendly  
- S3 friendly  
- agent-friendly  
- governance-ready  
- token-thrifty  
- extensible for future domain SDKs  
  
====================================================================  
1. INITIAL BUILD SCOPE  
====================================================================  
  
The first implementation wave should cover these core packages:  
  
1. config_sdk  
2. registry_sdk  
3. observabilitysdk  
4. artifactsdk  
5. auditsdk  
6. workflowsdk  
  
In addition, the platform shell should include:  
- shared schemas  
- runtime resolver  
- agent bridge  
- Jupyter bridge  
- controller layer  
- common utilities  
  
This gives you a usable base for:  
- session bootstrap  
- stage routing  
- event logging  
- artifact registration  
- audit trail  
- deterministic orchestration  
- future HITL integration  
  
====================================================================  
2. RECOMMENDED REPOSITORY STRUCTURE  
====================================================================  
  
project_root/  
  pyproject.toml  
  README.md  
  .gitignore  
  
  configs/  
    platform/  
      runtime_defaults.yml  
      policy_modes.yml  
      ui_modes.yml  
      token_budgets.yml  
    sdk/  
      config_sdk.yml  
      registry_sdk.yml  
      observabilitysdk.yml  
      artifactsdk.yml  
      auditsdk.yml  
      workflowsdk.yml  
    schemas/  
      runtime_context.schema.json  
      resolved_stack.schema.json  
      interaction_payload.schema.json  
      review_payload.schema.json  
      standard_response_envelope.schema.json  
  
  docs/  
    architecture/  
      platform_overview.md  
      runtime_resolution.md  
      sdk_boundaries.md  
      hitl_design.md  
    sdk/  
      config_sdk.md  
      registry_sdk.md  
      observabilitysdk.md  
      artifactsdk.md  
      auditsdk.md  
      workflowsdk.md  
    examples/  
      end_to_end_coarse_classing.md  
      end_to_end_validation_conclusion.md  
      end_to_end_monitoring_breach.md  
  
  src/  
    platform_core/  
      __init__.py  
      constants.py  
      enums.py  
      exceptions.py  
      typing.py  
  
      runtime/  
        __init__.py  
        context_models.py  
        stack_models.py  
        resolver.py  
        resolver_rules.py  
        allowlist.py  
        ui_mode_resolver.py  
        interaction_mode_resolver.py  
        token_mode_resolver.py  
  
      schemas/  
        __init__.py  
        base_models.py  
        runtime_context.py  
        resolved_stack.py  
        interaction_payload.py  
        review_payload.py  
        response_envelope.py  
        common_fragments.py  
        validators.py  
  
      controllers/  
        __init__.py  
        base_controller.py  
        session_controller.py  
        workflow_controller.py  
        review_controller.py  
        recovery_controller.py  
        documentation_controller.py  
  
      bridges/  
        __init__.py  
        agent_bridge/  
          __init__.py  
          context_builder.py  
          response_normalizer.py  
          tool_dispatcher.py  
          retry_policy.py  
        jupyter_bridge/  
          __init__.py  
          widget_controller.py  
          notebook_state_sync.py  
          action_dispatch.py  
          result_refresh.py  
  
      utils/  
        __init__.py  
        config_utils.py  
        id_utils.py  
        datetime_utils.py  
        hash_utils.py  
        path_utils.py  
        json_utils.py  
        logging_utils.py  
        state_utils.py  
  
    config_sdk/  
      __init__.py  
      loader.py  
      validator.py  
      versioning.py  
      resolver.py  
      overlay.py  
      diff.py  
      models.py  
      exceptions.py  
  
    registry_sdk/  
      __init__.py  
      models.py  
      project_registry.py  
      run_registry.py  
      skill_registry.py  
      sdk_registry.py  
      policy_registry.py  
      validation_registry.py  
      lookup_api.py  
      search_api.py  
      storage.py  
      exceptions.py  
  
    observabilitysdk/  
      __init__.py  
      models.py  
      event_schema.py  
      event_writer.py  
      trace_manager.py  
      event_query.py  
      replay_engine.py  
      lineage_builder.py  
      enrichment.py  
      router.py  
      storage.py  
      exceptions.py  
  
    artifactsdk/  
      __init__.py  
      models.py  
      registry.py  
      metadata.py  
      lineage.py  
      locator.py  
      validators.py  
      manifest.py  
      storage_adapter.py  
      checksum.py  
      version_resolver.py  
      exceptions.py  
  
    auditsdk/  
      __init__.py  
      models.py  
      audit_writer.py  
      decision_registry.py  
      approval_registry.py  
      exception_registry.py  
      signoff_registry.py  
      conditional_approval.py  
      export.py  
      views.py  
      exceptions.py  
  
    workflowsdk/  
      __init__.py  
      models.py  
      project_bootstrap.py  
      workflow_state.py  
      stage_registry.py  
      routing_engine.py  
      checkpoint_manager.py  
      session_manager.py  
      recovery_manager.py  
      candidate_registry.py  
      selection_registry.py  
      dependency_manager.py  
      state_persistence.py  
      transition_guard.py  
      exceptions.py  
  
  tests/  
    unit/  
      platform_core/  
        runtime/  
        schemas/  
        controllers/  
      config_sdk/  
      registry_sdk/  
      observabilitysdk/  
      artifactsdk/  
      auditsdk/  
      workflowsdk/  
    integration/  
      test_runtime_resolution.py  
      test_session_bootstrap_flow.py  
      test_artifact_audit_workflow.py  
      test_review_payload_flow.py  
    fixtures/  
      sample_runtime_context.json  
      sample_resolved_stack.json  
      sample_review_payload.json  
      sample_response_envelope.json  
  
  notebooks/  
    foundation_playbook.ipynb  
    runtime_resolution_demo.ipynb  
    artifact_audit_demo.ipynb  
  
====================================================================  
3. PACKAGE-BY-PACKAGE IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
3.1 platform_core  
--------------------------------------------------------------------  
  
Purpose:  
Shared foundation package for runtime logic, schemas, controllers, and  
common utilities.  
  
Key files and responsibilities:  
  
platform_core/constants.py  
- shared string constants  
- default names  
- common field names  
- SDK and skill identifiers  
  
platform_core/enums.py  
- role enums  
- domain enums  
- ui mode enums  
- interaction mode enums  
- status enums  
  
platform_core/exceptions.py  
- shared platform exception hierarchy  
- validation error  
- routing error  
- schema error  
- state error  
- dependency error  
  
platform_core/typing.py  
- shared type aliases  
- optional protocol-style interfaces  
  
-------------------------  
runtime/  
-------------------------  
  
runtime/context_models.py  
- internal typed models for runtime state  
- thin wrappers around schema objects for runtime use  
  
runtime/stack_models.py  
- typed models for resolved stack and allowlists  
  
runtime/resolver.py  
- main runtime resolution engine  
- input: runtime_context  
- output: resolved_stack  
  
runtime/resolver_rules.py  
- pure functions for mapping:  
  - role -> role skill  
  - domain -> domain skill  
  - stage -> stage skill  
  - overlays -> overlay skills  
  
runtime/allowlist.py  
- maps stage/domain/role to SDK allowlists  
- central place for narrowing tool access  
  
runtime/ui_mode_resolver.py  
- resolves UI mode based on stage and interaction complexity  
  
runtime/interaction_mode_resolver.py  
- resolves interaction mode based on stage and review type  
  
runtime/token_mode_resolver.py  
- micro / standard / deep review mode resolution  
  
-------------------------  
schemas/  
-------------------------  
  
schemas/base_models.py  
- common schema model superclass  
- common serialization helpers  
  
schemas/runtime_context.py  
- runtime_context model and validation  
  
schemas/resolved_stack.py  
- resolved_stack model and validation  
  
schemas/interaction_payload.py  
- human action payload model  
  
schemas/review_payload.py  
- display payload model  
  
schemas/response_envelope.py  
- standard response contract  
  
schemas/common_fragments.py  
- actor object  
- artifact ref  
- warning object  
- error object  
- metric summary object  
- candidate summary object  
  
schemas/validators.py  
- cross-field validation helpers  
- conditional validation logic  
  
-------------------------  
controllers/  
-------------------------  
  
controllers/base_controller.py  
- shared controller base class  
- logging hook  
- response normalization hook  
  
controllers/session_controller.py  
- create session  
- resume session  
- load active project  
- call runtime resolver  
  
controllers/workflow_controller.py  
- call workflow stage actions  
- coordinate with workflowsdk  
- normalize SDK outputs  
  
controllers/review_controller.py  
- load review payload  
- accept interaction payload  
- call interaction orchestrator path  
  
controllers/recovery_controller.py  
- present recovery choices  
- call workflowsdk recovery logic  
  
controllers/documentation_controller.py  
- drafting and document-related control path  
  
Why platform_core first:  
- every future SDK and bridge depends on the core contracts here  
  
--------------------------------------------------------------------  
3.2 config_sdk  
--------------------------------------------------------------------  
  
Purpose:  
Central config management.  
  
Files:  
  
config_sdk/models.py  
- config metadata models  
- resolved config model  
- config diff result model  
  
config_sdk/loader.py  
- load YAML / JSON / dict inputs  
- load from path or object store  
  
config_sdk/validator.py  
- validate config structure  
- route to specific schema validators  
  
config_sdk/versioning.py  
- config hash  
- semantic version helpers  
- config version metadata  
  
config_sdk/resolver.py  
- resolve effective config from layered sources  
  
config_sdk/overlay.py  
- apply environment overlays and local overrides  
  
config_sdk/diff.py  
- compare two config versions  
- useful for audit and validation  
  
config_sdk/exceptions.py  
- config-specific exceptions  
  
Implementation priority:  
- loader  
- validator  
- resolver  
- versioning  
- overlay  
- diff  
  
--------------------------------------------------------------------  
3.3 registry_sdk  
--------------------------------------------------------------------  
  
Purpose:  
Canonical metadata registry.  
  
Files:  
  
registry_sdk/models.py  
- project record  
- run record  
- skill record  
- sdk record  
- policy record  
- validation record  
  
registry_sdk/storage.py  
- abstract storage contract  
- could initially be file-backed or sqlite-backed  
  
registry_sdk/project_registry.py  
- create/get/update project metadata  
  
registry_sdk/run_registry.py  
- create/get/update run metadata  
  
registry_sdk/skill_registry.py  
- store skill metadata  
- versions  
- compatibility  
  
registry_sdk/sdk_registry.py  
- store SDK metadata  
- versions  
- dependency manifest  
  
registry_sdk/policy_registry.py  
- register and fetch policy packs  
  
registry_sdk/validation_registry.py  
- register findings / validation runs / conclusions metadata  
  
registry_sdk/lookup_api.py  
- exact lookup by ID  
  
registry_sdk/search_api.py  
- filtered metadata search  
  
registry_sdk/exceptions.py  
- registry-specific exceptions  
  
Implementation priority:  
- storage  
- models  
- project_registry  
- run_registry  
- lookup_api  
- search_api  
- others after  
  
--------------------------------------------------------------------  
3.4 observabilitysdk  
--------------------------------------------------------------------  
  
Purpose:  
Structured event trail.  
  
Files:  
  
observabilitysdk/models.py  
- event record  
- trace record  
- replay result  
- lineage path models  
  
observabilitysdk/event_schema.py  
- event schema validation  
- event type definitions  
  
observabilitysdk/trace_manager.py  
- trace ID creation  
- parent-child linkage  
- session trace helpers  
  
observabilitysdk/event_writer.py  
- write event record  
- append-only discipline  
  
observabilitysdk/event_query.py  
- fetch events by run/session/type/stage  
  
observabilitysdk/replay_engine.py  
- replay event history into reconstructed view  
  
observabilitysdk/lineage_builder.py  
- derive event lineage and chains  
  
observabilitysdk/enrichment.py  
- enrich events with context metadata  
  
observabilitysdk/router.py  
- route writes to configured store(s)  
  
observabilitysdk/storage.py  
- storage layer abstraction  
  
observabilitysdk/exceptions.py  
- observability-specific exceptions  
  
Implementation priority:  
- event_schema  
- trace_manager  
- event_writer  
- event_query  
- storage  
- enrichment  
- replay_engine  
- lineage_builder  
  
--------------------------------------------------------------------  
3.5 artifactsdk  
--------------------------------------------------------------------  
  
Purpose:  
Artifact lifecycle and lineage.  
  
Files:  
  
artifactsdk/models.py  
- artifact model  
- artifact manifest model  
- artifact lineage model  
  
artifactsdk/registry.py  
- register artifact  
- fetch artifact  
  
artifactsdk/metadata.py  
- metadata helpers  
- metadata updates  
- typed artifact descriptors  
  
artifactsdk/lineage.py  
- source-to-derived lineage management  
  
artifactsdk/locator.py  
- resolve artifact path / URI  
  
artifactsdk/validators.py  
- artifact existence, format, and integrity checks  
  
artifactsdk/manifest.py  
- build artifact manifest  
  
artifactsdk/storage_adapter.py  
- read/write abstraction for file/S3/object layer  
  
artifactsdk/checksum.py  
- checksum creation and verification  
  
artifactsdk/version_resolver.py  
- latest / explicit / tagged version resolution  
  
artifactsdk/exceptions.py  
- artifact-specific exceptions  
  
Implementation priority:  
- models  
- registry  
- storage_adapter  
- locator  
- metadata  
- manifest  
- lineage  
- validators  
- checksum  
- version_resolver  
  
--------------------------------------------------------------------  
3.6 auditsdk  
--------------------------------------------------------------------  
  
Purpose:  
Formal audit and sign-off trail.  
  
Files:  
  
auditsdk/models.py  
- audit record  
- decision record  
- approval record  
- exception record  
- signoff record  
  
auditsdk/audit_writer.py  
- write audit records  
  
auditsdk/decision_registry.py  
- manage explicit decisions  
  
auditsdk/approval_registry.py  
- manage approvals and approval conditions  
  
auditsdk/exception_registry.py  
- manage waived / unresolved exceptions  
  
auditsdk/signoff_registry.py  
- manage final sign-off records  
  
auditsdk/conditional_approval.py  
- support conditional approval logic  
  
auditsdk/export.py  
- export audit package  
  
auditsdk/views.py  
- render audit-friendly summaries  
  
auditsdk/exceptions.py  
- audit-specific exceptions  
  
Implementation priority:  
- models  
- audit_writer  
- decision_registry  
- approval_registry  
- signoff_registry  
- exception_registry  
- conditional_approval  
- export  
- views  
  
--------------------------------------------------------------------  
3.7 workflowsdk  
--------------------------------------------------------------------  
  
Purpose:  
Workflow engine and state manager.  
  
Files:  
  
workflowsdk/models.py  
- workflow state  
- stage execution  
- checkpoint  
- candidate version  
- version selection  
- dependency status  
  
workflowsdk/project_bootstrap.py  
- initialize workflow for a new project  
  
workflowsdk/workflow_state.py  
- create/read/update workflow state  
  
workflowsdk/stage_registry.py  
- stage definitions  
- dependencies  
- metadata  
  
workflowsdk/routing_engine.py  
- determine next stage  
- check stage rules  
- build transition result  
  
workflowsdk/checkpoint_manager.py  
- save/load checkpoints  
  
workflowsdk/session_manager.py  
- attach workflow to session  
- session resumption helpers  
  
workflowsdk/recovery_manager.py  
- select retry/rerun/rollback path  
  
workflowsdk/candidate_registry.py  
- candidate version creation and listing  
  
workflowsdk/selection_registry.py  
- selected version recording  
  
workflowsdk/dependency_manager.py  
- validate prerequisites and required refs  
  
workflowsdk/state_persistence.py  
- durable state write abstraction  
  
workflowsdk/transition_guard.py  
- enforce transition rules  
- prevent invalid continuation  
  
workflowsdk/exceptions.py  
- workflow-specific exceptions  
  
Implementation priority:  
- models  
- workflow_state  
- stage_registry  
- routing_engine  
- dependency_manager  
- transition_guard  
- project_bootstrap  
- session_manager  
- state_persistence  
- candidate_registry  
- selection_registry  
- checkpoint_manager  
- recovery_manager  
  
====================================================================  
4. BRIDGE LAYER IMPLEMENTATION  
====================================================================  
  
--------------------------------------------------------------------  
4.1 agent_bridge  
--------------------------------------------------------------------  
  
Purpose:  
Connect skill/runtime resolution to deterministic SDK calls.  
  
Suggested files:  
  
platform_core/bridges/agent_bridge/context_builder.py  
- build compact agent context from runtime_context + resolved_stack  
  
platform_core/bridges/agent_bridge/tool_dispatcher.py  
- enforce SDK allowlist  
- dispatch deterministic tool calls  
  
platform_core/bridges/agent_bridge/response_normalizer.py  
- convert SDK outputs to standard_response_envelope  
  
platform_core/bridges/agent_bridge/retry_policy.py  
- bounded retry rules for safe deterministic failures  
  
Implementation note:  
Keep this bridge very thin.  
It should not contain business logic that belongs inside SDKs.  
  
--------------------------------------------------------------------  
4.2 jupyter_bridge  
--------------------------------------------------------------------  
  
Purpose:  
Connect JupyterLab UI/workspaces to backend controllers and SDKs.  
  
Suggested files:  
  
platform_core/bridges/jupyter_bridge/widget_controller.py  
- widget event to controller mapping  
  
platform_core/bridges/jupyter_bridge/notebook_state_sync.py  
- sync displayed review state with workflow state  
  
platform_core/bridges/jupyter_bridge/action_dispatch.py  
- convert button actions into interaction_payload  
  
platform_core/bridges/jupyter_bridge/result_refresh.py  
- update displayed payload after backend response  
  
Implementation note:  
Do not let widgets call SDKs directly.  
Widgets should always call controller layer.  
  
====================================================================  
5. SHARED FILE-BY-FILE RESPONSIBILITY MAP  
====================================================================  
  
File,Responsibility  
platform_core/runtime/resolver.py,Main runtime resolver entry point  
platform_core/runtime/resolver_rules.py,Skill resolution rules  
platform_core/runtime/allowlist.py,SDK allowlist by stage/domain/role  
platform_core/runtime/ui_mode_resolver.py,UI mode selection logic  
platform_core/runtime/interaction_mode_resolver.py,Interaction mode mapping  
platform_core/schemas/runtime_context.py,Canonical runtime context schema  
platform_core/schemas/resolved_stack.py,Canonical resolved stack schema  
platform_core/schemas/interaction_payload.py,Canonical interaction payload schema  
platform_core/schemas/review_payload.py,Canonical review payload schema  
platform_core/schemas/response_envelope.py,Canonical response envelope schema  
platform_core/controllers/session_controller.py,Session and project bootstrap control  
platform_core/controllers/workflow_controller.py,Workflow stage execution control  
platform_core/controllers/review_controller.py,HITL review control  
platform_core/controllers/recovery_controller.py,Recovery path control  
config_sdk/loader.py,Load config files  
config_sdk/validator.py,Validate config schema  
registry_sdk/project_registry.py,Manage project metadata  
registry_sdk/run_registry.py,Manage run metadata  
observabilitysdk/event_writer.py,Append event records  
artifactsdk/registry.py,Register artifacts  
auditsdk/audit_writer.py,Append audit records  
workflowsdk/routing_engine.py,Determine next workflow step  
workflowsdk/dependency_manager.py,Enforce prerequisites  
workflowsdk/transition_guard.py,Block invalid transitions  
  
====================================================================  
6. RECOMMENDED BUILD ORDER  
====================================================================  
  
Phase 1A – contracts and foundations  
------------------------------------  
1. platform_core/constants.py  
2. platform_core/enums.py  
3. platform_core/exceptions.py  
4. platform_core/schemas/common_fragments.py  
5. platform_core/schemas/runtime_context.py  
6. platform_core/schemas/resolved_stack.py  
7. platform_core/schemas/interaction_payload.py  
8. platform_core/schemas/review_payload.py  
9. platform_core/schemas/response_envelope.py  
  
Phase 1B – config and registry  
------------------------------  
10. config_sdk/models.py  
11. config_sdk/loader.py  
12. config_sdk/validator.py  
13. config_sdk/resolver.py  
14. registry_sdk/models.py  
15. registry_sdk/storage.py  
16. registry_sdk/project_registry.py  
17. registry_sdk/run_registry.py  
18. registry_sdk/lookup_api.py  
  
Phase 1C – observability and artifacts  
--------------------------------------  
19. observabilitysdk/models.py  
20. observabilitysdk/event_schema.py  
21. observabilitysdk/trace_manager.py  
22. observabilitysdk/storage.py  
23. observabilitysdk/event_writer.py  
24. artifactsdk/models.py  
25. artifactsdk/storage_adapter.py  
26. artifactsdk/registry.py  
27. artifactsdk/locator.py  
28. artifactsdk/metadata.py  
29. artifactsdk/manifest.py  
  
Phase 1D – audit and workflow  
-----------------------------  
30. auditsdk/models.py  
31. auditsdk/audit_writer.py  
32. auditsdk/decision_registry.py  
33. auditsdk/approval_registry.py  
34. workflowsdk/models.py  
35. workflowsdk/workflow_state.py  
36. workflowsdk/stage_registry.py  
37. workflowsdk/dependency_manager.py  
38. workflowsdk/transition_guard.py  
39. workflowsdk/routing_engine.py  
40. workflowsdk/project_bootstrap.py  
41. workflowsdk/session_manager.py  
42. workflowsdk/state_persistence.py  
  
Phase 1E – runtime resolver and bridges  
---------------------------------------  
43. platform_core/runtime/context_models.py  
44. platform_core/runtime/stack_models.py  
45. platform_core/runtime/resolver_rules.py  
46. platform_core/runtime/allowlist.py  
47. platform_core/runtime/ui_mode_resolver.py  
48. platform_core/runtime/interaction_mode_resolver.py  
49. platform_core/runtime/token_mode_resolver.py  
50. platform_core/runtime/resolver.py  
51. platform_core/controllers/base_controller.py  
52. platform_core/controllers/session_controller.py  
53. platform_core/controllers/workflow_controller.py  
54. platform_core/controllers/review_controller.py  
55. platform_core/bridges/agent_bridge/context_builder.py  
56. platform_core/bridges/agent_bridge/tool_dispatcher.py  
57. platform_core/bridges/agent_bridge/response_normalizer.py  
58. platform_core/bridges/jupyter_bridge/widget_controller.py  
59. platform_core/bridges/jupyter_bridge/action_dispatch.py  
60. platform_core/bridges/jupyter_bridge/result_refresh.py  
  
====================================================================  
7. PACKAGE INTERNAL DESIGN STANDARDS  
====================================================================  
  
7.1 Every package should include  
--------------------------------------------------------------------  
- __init__.py  
- models.py  
- exceptions.py  
- primary service files  
- minimal public API  
- internal helpers only where necessary  
  
7.2 Public API pattern  
--------------------------------------------------------------------  
Each SDK should expose a small number of public service functions or  
service classes.  
  
Example:  
- register_artifact(...)  
- write_event(...)  
- resolve_runtime_stack(...)  
- route_next_stage(...)  
  
Do not expose too many low-level internals directly.  
  
7.3 Model-first design  
--------------------------------------------------------------------  
Every package should define its models before implementing service  
logic.  
  
This reduces ambiguity and helps agentic orchestration later.  
  
7.4 Response normalization  
--------------------------------------------------------------------  
Material service outputs should be convertible into the standard  
response envelope.  
  
====================================================================  
8. TEST STRUCTURE BLUEPRINT  
====================================================================  
  
tests/unit/platform_core/runtime/test_resolver_rules.py  
- role/domain/stage mapping tests  
  
tests/unit/platform_core/runtime/test_allowlist.py  
- stage allowlist enforcement  
  
tests/unit/platform_core/schemas/test_runtime_context.py  
- runtime_context validation  
  
tests/unit/platform_core/schemas/test_response_envelope.py  
- response schema validation  
  
tests/unit/config_sdk/test_loader.py  
- config loading tests  
  
tests/unit/config_sdk/test_validator.py  
- config validation tests  
  
tests/unit/registry_sdk/test_project_registry.py  
- project registry CRUD  
  
tests/unit/observabilitysdk/test_event_writer.py  
- event append tests  
  
tests/unit/artifactsdk/test_registry.py  
- artifact registration tests  
  
tests/unit/auditsdk/test_audit_writer.py  
- audit append tests  
  
tests/unit/workflowsdk/test_routing_engine.py  
- stage routing tests  
  
tests/unit/workflowsdk/test_transition_guard.py  
- invalid transition blocking tests  
  
tests/integration/test_runtime_resolution.py  
- runtime_context to resolved_stack end-to-end  
  
tests/integration/test_session_bootstrap_flow.py  
- bootstrap and resume flow  
  
tests/integration/test_artifact_audit_workflow.py  
- artifact + audit + workflow integration  
  
tests/integration/test_review_payload_flow.py  
- review load -> interaction -> response  
  
====================================================================  
9. INITIAL NOTEBOOK PLAYBOOKS  
====================================================================  
  
notebooks/foundation_playbook.ipynb  
- show basic runtime resolution  
- show workflow state creation  
- show standard response envelope  
  
notebooks/runtime_resolution_demo.ipynb  
- give sample runtime_context inputs  
- show resolved_stack outputs  
- show allowlist behavior  
  
notebooks/artifact_audit_demo.ipynb  
- register artifacts  
- write audit records  
- show linked refs  
  
Purpose:  
These notebooks become educational playbooks for both developers and  
agent-assisted implementation.  
  
====================================================================  
10. MINIMUM VIABLE PLATFORM FLOW AFTER FOUNDATIONS  
====================================================================  
  
Once this initial blueprint is implemented, the platform should be  
able to do the following:  
  
1. Start a session  
2. Resolve project/run context  
3. Resolve active runtime stack  
4. Enforce SDK allowlist  
5. Route a workflow stage  
6. Create event and audit records  
7. Register artifacts  
8. Return a normalized response  
9. Support future HITL and domain SDK integration  
  
That is the correct base before expanding into:  
- hitlsdk  
- widgetsdk  
- validationsdk  
- dataprepsdk  
- scorecardsdk  
- monitoringsdk  
- knowledge_sdk / rag_sdk  
  
====================================================================  
11. NEXT PHASE AFTER THIS BLUEPRINT  
====================================================================  
  
After this foundation is complete, the next recommended build wave is:  
  
Wave 2:  
- hitlsdk  
- widgetsdk  
- policymodule / policysdk  
- review workspace integration  
  
Wave 3:  
- dataset_sdk  
- dq_sdk  
- feature_sdk  
- evaluation_sdk  
- dataprepsdk  
  
Wave 4:  
- scorecardsdk  
- validationsdk  
- reporting_sdk  
  
Wave 5:  
- knowledge_sdk  
- rag_sdk  
- flowvizsdk  
- monitoringsdk  
  
====================================================================  
12. FINAL RECOMMENDATION  
====================================================================  
  
For implementation quality and maintainability:  
  
- build contracts first  
- build registries and state second  
- build logging, artifacts, and audit third  
- build workflow routing fourth  
- build bridges and controllers fifth  
- only then move to HITL and domain SDKs  
  
This sequence will make the system:  
- coherent  
- testable  
- agent-friendly  
- future-proof  
- much easier to scale  
  
====================================================================  
END OF FOLDER STRUCTURE + FILE-BY-FILE IMPLEMENTATION BLUEPRINT  
====================================================================  
  
====================================================================  
WAVE 2 IMPLEMENTATION BLUEPRINT  
HITL SDK + POLICY SDK + WIDGETS SDK + REVIEW WORKSPACE INTEGRATION  
ENTERPRISE AGENTIC AI MODEL LIFECYCLE PLATFORM  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This document continues the implementation blueprint with Wave 2.  
  
Wave 2 focuses on the first governed interaction layer of the  
platform. It adds:  
  
1. hitlsdk  
2. policysdk  
3. widgetsdk  
4. review workspace integration  
5. expanded controller and bridge support  
6. first usable governed review experience in JupyterLab  
  
The goal of Wave 2 is to make the platform capable of:  
- creating review payloads  
- showing review workspaces  
- capturing structured human input  
- validating bounded actions  
- applying policy rules  
- recording approvals, overrides, and escalations  
- returning normalized response envelopes  
- updating workflow state cleanly  
  
This is the wave where the platform becomes truly interactive and  
usable for governed model lifecycle tasks.  
  
====================================================================  
1. WAVE 2 SCOPE  
====================================================================  
  
Wave 2 includes:  
  
A. hitlsdk  
- review creation  
- review state machine  
- approval handling  
- override handling  
- escalation handling  
- decision capture  
- reviewer assignment  
- review templates  
  
B. policysdk  
- policy loading  
- threshold evaluation  
- breach detection  
- approval rules  
- escalation rules  
- waiver rules  
- control matrix logic  
  
C. widgetsdk  
- reusable review shell  
- selection cards  
- validation cards  
- flow panels  
- evidence panels  
- action bar  
- comment capture  
  
D. Review workspace integration  
- review controller enhancements  
- Jupyter bridge enhancements  
- 3-panel workspace rendering pattern  
- structured payload submission pattern  
- preview/refresh loop  
  
====================================================================  
2. TARGET OUTCOME OF WAVE 2  
====================================================================  
  
After Wave 2, the platform should be able to support an end-to-end  
governed review such as:  
  
- open a coarse classing review  
- render proposal/evidence in workspace  
- allow structured user edits  
- let user preview updated result  
- let user accept/reject/rerun/escalate  
- validate the action against policy  
- write event and audit records  
- update workflow state  
- return standard_response_envelope  
  
That is the minimum viable governed HITL platform.  
  
====================================================================  
3. UPDATED REPOSITORY STRUCTURE FOR WAVE 2  
====================================================================  
  
project_root/  
  src/  
    hitlsdk/  
      __init__.py  
      models.py  
      review_payloads.py  
      review_registry.py  
      approval_manager.py  
      override_manager.py  
      reviewer_assignment.py  
      action_validation.py  
      escalation_manager.py  
      review_status_machine.py  
      decision_capture.py  
      review_templates.py  
      exceptions.py  
  
    policysdk/  
      __init__.py  
      models.py  
      policy_loader.py  
      threshold_engine.py  
      breach_detector.py  
      waiver_rules.py  
      control_matrix.py  
      rule_evaluator.py  
      approval_rules.py  
      escalation_rules.py  
      exceptions.py  
  
    widgetsdk/  
      __init__.py  
      models.py  
      review_shell.py  
      selection_cards.py  
      bootstrap_cards.py  
      recovery_cards.py  
      flow_panels.py  
      detail_panels.py  
      validation_cards.py  
      evidence_panels.py  
      comment_capture.py  
      action_bar.py  
      exceptions.py  
  
    platform_core/  
      controllers/  
        review_controller.py  
        hitl_controller.py  
        policy_controller.py  
      bridges/  
        jupyter_bridge/  
          workspace_builder.py  
          review_workspace_sync.py  
          review_payload_mapper.py  
          interaction_payload_builder.py  
          preview_refresh.py  
      runtime/  
        review_mode_resolver.py  
  
  tests/  
    unit/  
      hitlsdk/  
      policysdk/  
      widgetsdk/  
    integration/  
      test_hitl_review_flow.py  
      test_policy_enforcement_flow.py  
      test_workspace_interaction_flow.py  
      test_review_preview_cycle.py  
  
  notebooks/  
    hitl_playbook.ipynb  
    policy_playbook.ipynb  
    workspace_playbook.ipynb  
  
====================================================================  
4. HITL SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
4.1 Purpose  
--------------------------------------------------------------------  
hitlsdk is the governed human-in-the-loop control layer.  
  
It should:  
- create review objects  
- define bounded actions  
- record reviewer interaction  
- manage lifecycle of reviews  
- handle approvals and escalations  
- support final decision capture  
  
--------------------------------------------------------------------  
4.2 File-by-file design  
--------------------------------------------------------------------  
  
hitlsdk/models.py  
Purpose:  
- define review record model  
- define approval model  
- define escalation model  
- define override model  
- define decision capture model  
- define review template model  
  
Key models:  
- ReviewRecord  
- ReviewActionRecord  
- ApprovalRecord  
- OverrideRecord  
- EscalationRecord  
- ReviewStatusTransition  
- ReviewTemplate  
  
--------------------------------------------------  
hitlsdk/review_payloads.py  
--------------------------------------------------  
Purpose:  
Build normalized review payload objects from workflow state,  
artifacts, metrics, and review templates.  
  
Responsibilities:  
- assemble review title  
- assemble proposal summary  
- attach evidence references  
- attach candidate summaries  
- set allowed actions  
- define structured edit schema  
  
Main functions:  
- build_review_payload(...)  
- build_candidate_selection_payload(...)  
- build_validation_review_payload(...)  
- build_monitoring_breach_payload(...)  
  
Depends on:  
- review_templates.py  
- artifactsdk  
- workflowsdk  
- registry_sdk  
  
--------------------------------------------------  
hitlsdk/review_registry.py  
--------------------------------------------------  
Purpose:  
Persist and retrieve reviews.  
  
Responsibilities:  
- create review record  
- load review by ID  
- update review metadata  
- list open reviews by project/run/stage  
- close or supersede review  
  
Main functions:  
- create_review(...)  
- get_review(...)  
- update_review(...)  
- list_reviews(...)  
- close_review(...)  
  
Depends on:  
- registry_sdk  
- auditsdk  
- observabilitysdk  
  
--------------------------------------------------  
hitlsdk/approval_manager.py  
--------------------------------------------------  
Purpose:  
Handle approval and approval-with-conditions logic.  
  
Responsibilities:  
- validate approval payload  
- create approval record  
- attach conditions  
- write approval audit  
  
Main functions:  
- approve_review(...)  
- approve_with_conditions(...)  
- revoke_approval(...)  
  
Depends on:  
- review_registry.py  
- auditsdk  
- policysdk  
- observabilitysdk  
  
--------------------------------------------------  
hitlsdk/override_manager.py  
--------------------------------------------------  
Purpose:  
Handle controlled overrides.  
  
Responsibilities:  
- capture override rationale  
- record override type  
- check policy allowance  
- link override to decision and audit  
  
Main functions:  
- create_override(...)  
- validate_override(...)  
- finalize_override(...)  
  
Depends on:  
- policysdk  
- auditsdk  
- review_registry.py  
  
--------------------------------------------------  
hitlsdk/reviewer_assignment.py  
--------------------------------------------------  
Purpose:  
Assign or validate reviewers.  
  
Responsibilities:  
- determine expected role  
- validate assigned actor role  
- support escalation reassignment  
  
Main functions:  
- assign_reviewer(...)  
- validate_reviewer_role(...)  
- reassign_review(...)  
  
Depends on:  
- registry_sdk  
- policysdk  
  
--------------------------------------------------  
hitlsdk/action_validation.py  
--------------------------------------------------  
Purpose:  
Validate whether an interaction payload action is legal.  
  
Responsibilities:  
- validate action in allowed_actions  
- validate structured edits presence  
- validate actor role  
- validate conditional fields  
  
Main functions:  
- validate_action(...)  
- validate_edit_payload(...)  
- validate_selection_payload(...)  
  
Depends on:  
- review_registry.py  
- policysdk  
- platform_core schemas  
  
This file is critical because it prevents free-form uncontrolled review  
behavior.  
  
--------------------------------------------------  
hitlsdk/escalation_manager.py  
--------------------------------------------------  
Purpose:  
Handle escalation of reviews.  
  
Responsibilities:  
- escalate due to severity  
- escalate due to timeout  
- escalate due to policy  
- escalate to another role  
  
Main functions:  
- escalate_review(...)  
- escalate_due_to_timeout(...)  
- determine_escalation_target(...)  
  
Depends on:  
- review_registry.py  
- policysdk  
- auditsdk  
- observabilitysdk  
  
--------------------------------------------------  
hitlsdk/review_status_machine.py  
--------------------------------------------------  
Purpose:  
Manage allowed review state transitions.  
  
Responsibilities:  
- define valid states  
- define valid transitions  
- block illegal transitions  
- apply transition side effects  
  
Main functions:  
- get_allowed_transitions(...)  
- transition_review_state(...)  
- validate_transition(...)  
  
States:  
- initialized  
- proposed  
- under_review  
- user_editing  
- preview_generated  
- waiting_for_confirmation  
- pending_review  
- approved  
- approved_with_conditions  
- rejected  
- rerun_requested  
- escalated  
- overdue  
- expired_needs_recreation  
- finalized  
- superseded  
- closed  
  
Depends on:  
- review_registry.py  
- auditsdk  
- observabilitysdk  
  
--------------------------------------------------  
hitlsdk/decision_capture.py  
--------------------------------------------------  
Purpose:  
Capture final review decision in normalized form.  
  
Responsibilities:  
- map interaction action to final decision  
- attach rationale  
- link to artifacts and audit  
- update workflow patch object  
  
Main functions:  
- capture_decision(...)  
- build_decision_patch(...)  
- link_decision_to_review(...)  
  
Depends on:  
- auditsdk  
- workflowsdk  
- review_registry.py  
  
--------------------------------------------------  
hitlsdk/review_templates.py  
--------------------------------------------------  
Purpose:  
Store reusable review templates.  
  
Responsibilities:  
- define standard review shells  
- map review type to display sections  
- map review type to allowed actions  
- map review type to structured edit schema  
  
Main functions:  
- get_template(...)  
- render_template(...)  
- validate_template(...)  
  
Depends on:  
- config_sdk  
  
--------------------------------------------------  
hitlsdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Review-specific exceptions.  
  
Examples:  
- ReviewNotFoundError  
- InvalidReviewActionError  
- InvalidReviewTransitionError  
- ReviewerAssignmentError  
- ApprovalDeniedError  
  
--------------------------------------------------------------------  
4.3 Public API for hitlsdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
- create_review(...)  
- get_review(...)  
- build_review_payload(...)  
- validate_action(...)  
- transition_review_state(...)  
- approve_review(...)  
- approve_with_conditions(...)  
- escalate_review(...)  
- capture_decision(...)  
- close_review(...)  
  
--------------------------------------------------------------------  
4.4 Implementation priorities for hitlsdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. review_templates.py  
3. review_registry.py  
4. review_payloads.py  
5. action_validation.py  
6. review_status_machine.py  
7. decision_capture.py  
8. approval_manager.py  
9. escalation_manager.py  
10. override_manager.py  
11. reviewer_assignment.py  
  
====================================================================  
5. POLICY SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
5.1 Purpose  
--------------------------------------------------------------------  
policysdk is the rule and control layer.  
  
It should:  
- load active policy packs  
- evaluate thresholds  
- detect breaches  
- determine approval requirements  
- determine escalation requirements  
- determine waiver allowance  
  
--------------------------------------------------------------------  
5.2 File-by-file design  
--------------------------------------------------------------------  
  
policysdk/models.py  
Purpose:  
Define policy objects.  
  
Key models:  
- PolicyPack  
- ThresholdRule  
- ApprovalRule  
- EscalationRule  
- WaiverRule  
- ControlMatrixEntry  
- PolicyEvaluationResult  
  
--------------------------------------------------  
policysdk/policy_loader.py  
--------------------------------------------------  
Purpose:  
Load policy packs from config or registry.  
  
Responsibilities:  
- load active policy profile  
- merge base + domain + overlay rules  
- return policy object  
  
Main functions:  
- load_policy_pack(...)  
- resolve_effective_policy(...)  
  
Depends on:  
- config_sdk  
- registry_sdk  
  
--------------------------------------------------  
policysdk/threshold_engine.py  
--------------------------------------------------  
Purpose:  
Apply threshold logic to metrics.  
  
Responsibilities:  
- compare value to threshold bands  
- return pass/warn/breach/severe_breach  
- support threshold by metric type/domain/stage  
  
Main functions:  
- evaluate_threshold(...)  
- evaluate_metric_set(...)  
  
Depends on:  
- policy_loader.py  
  
--------------------------------------------------  
policysdk/breach_detector.py  
--------------------------------------------------  
Purpose:  
Detect policy and threshold breaches.  
  
Responsibilities:  
- aggregate threshold failures  
- classify breach severity  
- prepare breach summary  
  
Main functions:  
- detect_breaches(...)  
- summarize_breaches(...)  
  
Depends on:  
- threshold_engine.py  
- rule_evaluator.py  
  
--------------------------------------------------  
policysdk/waiver_rules.py  
--------------------------------------------------  
Purpose:  
Evaluate whether a breach/issue is waivable.  
  
Responsibilities:  
- check waiver eligibility  
- define required approver if waiver is allowed  
- block silent waivers  
  
Main functions:  
- is_waivable(...)  
- get_waiver_requirements(...)  
  
Depends on:  
- policy_loader.py  
  
--------------------------------------------------  
policysdk/control_matrix.py  
--------------------------------------------------  
Purpose:  
Map controls to stages and workflow events.  
  
Responsibilities:  
- determine whether HITL required  
- determine required role for review  
- determine required sign-off path  
  
Main functions:  
- get_stage_controls(...)  
- requires_human_review(...)  
- required_role_for_stage(...)  
  
Depends on:  
- policy_loader.py  
  
--------------------------------------------------  
policysdk/rule_evaluator.py  
--------------------------------------------------  
Purpose:  
Generic policy rule evaluation.  
  
Responsibilities:  
- evaluate non-threshold rules  
- evaluate role, status, dependency, and state rules  
  
Main functions:  
- evaluate_rule(...)  
- evaluate_rule_set(...)  
  
Depends on:  
- policy_loader.py  
  
--------------------------------------------------  
policysdk/approval_rules.py  
--------------------------------------------------  
Purpose:  
Determine approval requirements.  
  
Responsibilities:  
- resolve who can approve  
- whether conditions are allowed  
- whether one or multiple approvals needed  
  
Main functions:  
- get_approval_requirements(...)  
- can_actor_approve(...)  
  
Depends on:  
- control_matrix.py  
- rule_evaluator.py  
  
--------------------------------------------------  
policysdk/escalation_rules.py  
--------------------------------------------------  
Purpose:  
Determine escalation requirements.  
  
Responsibilities:  
- severity-based escalation  
- timeout-based escalation  
- rule-based escalation  
- unresolved issue escalation  
  
Main functions:  
- should_escalate(...)  
- get_escalation_target(...)  
  
Depends on:  
- control_matrix.py  
- rule_evaluator.py  
  
--------------------------------------------------  
policysdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Policy-specific exceptions.  
  
Examples:  
- PolicyPackNotFoundError  
- ThresholdRuleError  
- EscalationRuleError  
- ApprovalRuleError  
  
--------------------------------------------------------------------  
5.3 Public API for policysdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
- load_policy_pack(...)  
- resolve_effective_policy(...)  
- evaluate_metric_set(...)  
- detect_breaches(...)  
- get_stage_controls(...)  
- requires_human_review(...)  
- get_approval_requirements(...)  
- can_actor_approve(...)  
- should_escalate(...)  
- is_waivable(...)  
  
--------------------------------------------------------------------  
5.4 Implementation priorities for policysdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. policy_loader.py  
3. threshold_engine.py  
4. control_matrix.py  
5. rule_evaluator.py  
6. breach_detector.py  
7. approval_rules.py  
8. escalation_rules.py  
9. waiver_rules.py  
  
====================================================================  
6. WIDGETS SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
6.1 Purpose  
--------------------------------------------------------------------  
widgetsdk provides reusable UI components for Jupyter review and  
workspace interaction.  
  
The widgets should not contain business logic.  
They should only:  
- render payloads  
- capture structured user input  
- dispatch actions through controllers  
  
--------------------------------------------------------------------  
6.2 File-by-file design  
--------------------------------------------------------------------  
  
widgetsdk/models.py  
Purpose:  
UI payload helper models and component props models.  
  
Examples:  
- ReviewShellProps  
- SelectionCardProps  
- ActionBarProps  
- ValidationCardProps  
- FlowPanelProps  
  
--------------------------------------------------  
widgetsdk/review_shell.py  
--------------------------------------------------  
Purpose:  
Render the main 3-panel review shell.  
  
Responsibilities:  
- header area  
- proposal area  
- evidence area  
- structured edit area  
- action/status area  
  
Usage:  
Main component for coarse classing, model selection, validation  
conclusion, remediation closure.  
  
Depends on:  
- widgetsdk models  
- jupyter_bridge  
  
--------------------------------------------------  
widgetsdk/selection_cards.py  
--------------------------------------------------  
Purpose:  
Render candidate comparison and selection cards.  
  
Responsibilities:  
- render candidate summaries  
- allow candidate selection  
- allow composite selection support later  
  
Usage:  
Binning version selection, model selection, challenger comparison.  
  
--------------------------------------------------  
widgetsdk/bootstrap_cards.py  
--------------------------------------------------  
Purpose:  
Render project bootstrap / resume cards.  
  
Responsibilities:  
- choose resume or new project  
- list unfinished work  
- select active project  
  
Usage:  
Session start.  
  
--------------------------------------------------  
widgetsdk/recovery_cards.py  
--------------------------------------------------  
Purpose:  
Render recovery options.  
  
Responsibilities:  
- show retry / rerun / rollback choices  
- show failed stage summary  
  
Usage:  
Recovery workspace.  
  
--------------------------------------------------  
widgetsdk/flow_panels.py  
--------------------------------------------------  
Purpose:  
Render workflow flow and timeline panels.  
  
Responsibilities:  
- graph view  
- timeline view  
- filtered flow view  
  
Usage:  
Governance, audit, annual review, documentation.  
  
--------------------------------------------------  
widgetsdk/detail_panels.py  
--------------------------------------------------  
Purpose:  
Render drill-down details.  
  
Responsibilities:  
- metrics tables  
- artifact summary  
- warnings  
- findings  
- decision notes  
  
Usage:  
Attached to review shell or flow explorer.  
  
--------------------------------------------------  
widgetsdk/validation_cards.py  
--------------------------------------------------  
Purpose:  
Render validation-focused cards.  
  
Responsibilities:  
- finding summary card  
- fitness matrix card  
- conclusion options card  
  
Usage:  
Validation review workspace.  
  
--------------------------------------------------  
widgetsdk/evidence_panels.py  
--------------------------------------------------  
Purpose:  
Render evidence and artifact references.  
  
Responsibilities:  
- show evidence summaries  
- link to artifacts  
- show completeness notes  
  
Usage:  
Validation and governance reviews.  
  
--------------------------------------------------  
widgetsdk/comment_capture.py  
--------------------------------------------------  
Purpose:  
Render controlled rationale/comment area.  
  
Responsibilities:  
- comment text area  
- validation of required rationale  
- structured note capture  
  
Usage:  
Approvals, rejections, escalations, validation notes.  
  
--------------------------------------------------  
widgetsdk/action_bar.py  
--------------------------------------------------  
Purpose:  
Render bounded actions.  
  
Responsibilities:  
- show allowed action buttons only  
- disable illegal actions  
- expose callbacks  
  
Usage:  
Every review workspace.  
  
--------------------------------------------------  
widgetsdk/exceptions.py  
--------------------------------------------------  
Purpose:  
UI component exceptions and validation issues.  
  
--------------------------------------------------------------------  
6.3 Public API for widgetsdk  
--------------------------------------------------------------------  
  
Suggested public components/functions:  
  
- build_review_shell(...)  
- build_selection_cards(...)  
- build_validation_cards(...)  
- build_action_bar(...)  
- build_evidence_panel(...)  
- build_bootstrap_cards(...)  
- build_recovery_cards(...)  
  
--------------------------------------------------------------------  
6.4 Implementation priorities for widgetsdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. action_bar.py  
3. comment_capture.py  
4. review_shell.py  
5. selection_cards.py  
6. validation_cards.py  
7. evidence_panels.py  
8. bootstrap_cards.py  
9. recovery_cards.py  
10. detail_panels.py  
11. flow_panels.py  
  
====================================================================  
7. REVIEW WORKSPACE INTEGRATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
7.1 Purpose  
--------------------------------------------------------------------  
This is the layer that makes Wave 2 usable.  
  
It connects:  
- resolved stack  
- review payload  
- widgets  
- user action  
- interaction payload  
- backend preview/finalization loop  
  
--------------------------------------------------------------------  
7.2 New / expanded controller files  
--------------------------------------------------------------------  
  
platform_core/controllers/review_controller.py  
Enhancements:  
- load review by ID  
- build review payload  
- map review payload to workspace  
- accept interaction payload  
- call hitlsdk validation + decision path  
- return standard response  
  
Main methods:  
- open_review(...)  
- get_review_payload(...)  
- submit_review_action(...)  
- refresh_review(...)  
  
--------------------------------------------------  
platform_core/controllers/hitl_controller.py  
--------------------------------------------------  
Purpose:  
Dedicated controller for review action handling.  
  
Responsibilities:  
- validate action payload  
- call policy checks  
- call preview recompute path  
- call final decision path  
- patch workflow state  
- return standard_response_envelope  
  
Main methods:  
- validate_interaction(...)  
- preview_interaction(...)  
- finalize_interaction(...)  
- escalate_interaction(...)  
  
--------------------------------------------------  
platform_core/controllers/policy_controller.py  
--------------------------------------------------  
Purpose:  
Thin controller around policysdk for review-stage use.  
  
Responsibilities:  
- determine allowed actions  
- determine escalation target  
- evaluate threshold outputs  
- determine approval role  
  
Main methods:  
- get_stage_policy(...)  
- evaluate_review_policy(...)  
- check_actor_permission(...)  
  
--------------------------------------------------------------------  
7.3 Jupyter bridge expansions  
--------------------------------------------------------------------  
  
platform_core/bridges/jupyter_bridge/workspace_builder.py  
Purpose:  
Build workspace from resolved stack + review payload.  
  
Responsibilities:  
- choose widget set  
- map UI mode to widget composition  
- construct 3-panel layout  
  
--------------------------------------------------  
platform_core/bridges/jupyter_bridge/review_workspace_sync.py  
--------------------------------------------------  
Purpose:  
Keep workspace state in sync with backend review state.  
  
Responsibilities:  
- refresh status  
- refresh warnings  
- refresh metrics after preview  
- refresh action availability  
  
--------------------------------------------------  
platform_core/bridges/jupyter_bridge/review_payload_mapper.py  
--------------------------------------------------  
Purpose:  
Map review payload to widget props.  
  
Responsibilities:  
- extract title  
- extract summary  
- extract evidence blocks  
- extract edit schema  
- extract allowed actions  
  
--------------------------------------------------  
platform_core/bridges/jupyter_bridge/interaction_payload_builder.py  
--------------------------------------------------  
Purpose:  
Map widget state to interaction_payload.  
  
Responsibilities:  
- collect selected action  
- collect structured edits  
- collect user comment  
- attach actor identity and refs  
  
--------------------------------------------------  
platform_core/bridges/jupyter_bridge/preview_refresh.py  
--------------------------------------------------  
Purpose:  
Handle preview cycle.  
  
Responsibilities:  
- send preview request  
- receive preview response  
- refresh metrics and warnings  
- maintain current draft edits  
  
====================================================================  
8. REVIEW WORKSPACE UI DESIGN  
====================================================================  
  
--------------------------------------------------------------------  
8.1 Standard layout  
--------------------------------------------------------------------  
Use a standard 3-panel review workspace:  
  
Panel A: Proposal and Evidence  
- title  
- recommendation  
- business summary  
- technical summary  
- metrics  
- warnings  
- artifact links  
  
Panel B: Structured Edit Workspace  
- editable controls  
- candidate selector  
- form fields  
- validation-specific fields  
- comment area  
  
Panel C: Actions and Status  
- preview button  
- accept / approve button  
- reject / rerun  
- escalate  
- status summary  
- backend response summary  
  
--------------------------------------------------------------------  
8.2 Chat role  
--------------------------------------------------------------------  
CodeBuddy chat remains supporting, not the main edit surface.  
  
Chat can:  
- explain a proposal  
- generate another candidate  
- summarize trade-offs  
  
But final edits and decisions must go through structured workspace.  
  
====================================================================  
9. WAVE 2 PUBLIC FLOW  
====================================================================  
  
Standard flow should be:  
  
1. session_controller resolves project and run  
2. runtime resolver builds resolved_stack  
3. review_controller loads review_payload  
4. workspace_builder builds widgets  
5. user edits or selects action  
6. interaction_payload_builder creates interaction_payload  
7. hitl_controller validates action  
8. policy_controller checks policy  
9. if preview:  
   - call deterministic SDK recompute  
   - return preview response  
10. if final:  
   - capture decision  
   - write audit and event  
   - patch workflow state  
   - return final response  
11. review_workspace_sync refreshes UI  
  
====================================================================  
10. TEST BLUEPRINT FOR WAVE 2  
====================================================================  
  
tests/unit/hitlsdk/test_review_templates.py  
- template load and render tests  
  
tests/unit/hitlsdk/test_action_validation.py  
- invalid action rejection  
- missing structured fields rejection  
- role mismatch rejection  
  
tests/unit/hitlsdk/test_review_status_machine.py  
- valid transition tests  
- illegal transition block tests  
  
tests/unit/hitlsdk/test_decision_capture.py  
- final decision normalization tests  
  
tests/unit/policysdk/test_threshold_engine.py  
- pass/warn/breach classification  
  
tests/unit/policysdk/test_control_matrix.py  
- stage control lookup tests  
  
tests/unit/policysdk/test_approval_rules.py  
- actor approval eligibility tests  
  
tests/unit/widgetsdk/test_action_bar.py  
- allowed action rendering tests  
  
tests/unit/widgetsdk/test_review_shell.py  
- payload mapping into workspace props  
  
tests/integration/test_hitl_review_flow.py  
- open review -> preview -> finalize  
  
tests/integration/test_policy_enforcement_flow.py  
- illegal approval blocked  
  
tests/integration/test_workspace_interaction_flow.py  
- widget payload -> interaction payload -> response cycle  
  
tests/integration/test_review_preview_cycle.py  
- preview refresh updates metrics and warnings  
  
====================================================================  
11. NOTEBOOK PLAYBOOKS FOR WAVE 2  
====================================================================  
  
notebooks/hitl_playbook.ipynb  
- create review  
- render review payload  
- submit interaction payload  
- inspect response envelope  
  
notebooks/policy_playbook.ipynb  
- load policy pack  
- evaluate thresholds  
- determine allowed actions  
- determine escalation  
  
notebooks/workspace_playbook.ipynb  
- build 3-panel review shell  
- simulate preview cycle  
- simulate final decision cycle  
  
====================================================================  
12. MINIMUM VIABLE WAVE 2 DEMOS  
====================================================================  
  
Wave 2 should prove these demos:  
  
Demo 1: Coarse Classing Review  
- open review  
- edit bins  
- preview result  
- finalize with audit/event trail  
  
Demo 2: Candidate Version Selection  
- compare 2 candidates  
- choose one  
- finalize selection  
- update workflow state  
  
Demo 3: Validation Conclusion  
- show findings and fitness matrix  
- select conclusion category  
- add conditions  
- finalize with audit trail  
  
====================================================================  
13. BUILD ORDER FOR WAVE 2  
====================================================================  
  
Phase 2A – policy foundation  
----------------------------  
1. policysdk/models.py  
2. policysdk/policy_loader.py  
3. policysdk/threshold_engine.py  
4. policysdk/control_matrix.py  
5. policysdk/rule_evaluator.py  
  
Phase 2B – review foundation  
----------------------------  
6. hitlsdk/models.py  
7. hitlsdk/review_templates.py  
8. hitlsdk/review_registry.py  
9. hitlsdk/review_payloads.py  
10. hitlsdk/action_validation.py  
11. hitlsdk/review_status_machine.py  
  
Phase 2C – decision and escalation  
----------------------------------  
12. hitlsdk/decision_capture.py  
13. hitlsdk/approval_manager.py  
14. policysdk/approval_rules.py  
15. policysdk/escalation_rules.py  
16. hitlsdk/escalation_manager.py  
17. hitlsdk/override_manager.py  
18. hitlsdk/reviewer_assignment.py  
19. policysdk/breach_detector.py  
20. policysdk/waiver_rules.py  
  
Phase 2D – widget base  
----------------------  
21. widgetsdk/models.py  
22. widgetsdk/action_bar.py  
23. widgetsdk/comment_capture.py  
24. widgetsdk/review_shell.py  
25. widgetsdk/selection_cards.py  
26. widgetsdk/validation_cards.py  
27. widgetsdk/evidence_panels.py  
  
Phase 2E – bridge and controller integration  
--------------------------------------------  
28. platform_core/controllers/hitl_controller.py  
29. platform_core/controllers/policy_controller.py  
30. enhance platform_core/controllers/review_controller.py  
31. platform_core/bridges/jupyter_bridge/review_payload_mapper.py  
32. platform_core/bridges/jupyter_bridge/interaction_payload_builder.py  
33. platform_core/bridges/jupyter_bridge/workspace_builder.py  
34. platform_core/bridges/jupyter_bridge/review_workspace_sync.py  
35. platform_core/bridges/jupyter_bridge/preview_refresh.py  
  
Phase 2F – optional first extended widgets  
------------------------------------------  
36. widgetsdk/bootstrap_cards.py  
37. widgetsdk/recovery_cards.py  
38. widgetsdk/detail_panels.py  
39. widgetsdk/flow_panels.py  
  
====================================================================  
14. WHAT WAVE 2 SHOULD NOT DO  
====================================================================  
  
Wave 2 should not:  
- implement domain-specific math inside widgets  
- bypass deterministic SDKs for previews  
- allow free-text-only final decisions  
- store review truth only in chat history  
- overbuild dashboard or flow explorer before review core is stable  
- merge policy logic into UI code  
- merge review logic into widgets  
  
====================================================================  
15. DELIVERABLE CHECKLIST FOR WAVE 2  
====================================================================  
  
Wave 2 is complete when all of the following exist:  
  
- policysdk with threshold, control, approval, escalation logic  
- hitlsdk with review lifecycle and decision capture  
- widgetsdk with reusable review workspace components  
- review workspace integration in Jupyter bridge  
- review_controller + hitl_controller + policy_controller  
- end-to-end preview cycle  
- end-to-end finalize cycle  
- standardized audit/event records from review actions  
- at least 3 working demos:  
  - coarse classing  
  - candidate selection  
  - validation conclusion  
  
====================================================================  
16. FINAL RECOMMENDATION  
====================================================================  
  
Wave 2 is the right place to standardize the governed interaction  
pattern once and reuse it everywhere.  
  
Do not over-customize by domain too early.  
  
Build a strong generic review system first:  
- policy-aware  
- review-aware  
- structured-edit-aware  
- Jupyter-friendly  
- audit-friendly  
  
Then reuse it for:  
- scorecard binning  
- model selection  
- validation conclusion  
- monitoring breach review  
- remediation closure  
  
That will make the platform scalable and coherent.  
  
====================================================================  
END OF WAVE 2 IMPLEMENTATION BLUEPRINT  
====================================================================  
  
====================================================================  
WAVE 3 IMPLEMENTATION BLUEPRINT  
DATASET SDK + DQ SDK + FEATURE SDK + EVALUATION SDK + DATAPREPSDK  
SPARK-FIRST DATA FOUNDATION FOR ENTERPRISE AGENTIC AI PLATFORM  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This document continues the implementation blueprint with Wave 3.  
  
Wave 3 focuses on the data foundation layer of the platform. It adds:  
  
1. dataset_sdk  
2. dq_sdk  
3. feature_sdk  
4. evaluation_sdk  
5. dataprepsdk  
  
Wave 3 is the point where the platform becomes able to:  
- build governed modeling datasets  
- preserve dataset lineage and reproducibility  
- run preparation-stage data quality checks  
- standardize reusable feature construction  
- compute evaluation metrics and comparisons  
- support Spark-first training-data preparation in CML with S3 access  
- expose deterministic, agent-safe, token-thrifty dataset preparation  
  and evaluation services  
  
This wave is critical because all downstream domain SDKs depend on  
reliable data contracts, evaluation contracts, and preparation logic.  
  
====================================================================  
1. WAVE 3 SCOPE  
====================================================================  
  
Wave 3 includes:  
  
A. dataset_sdk  
- dataset registration  
- dataset snapshot management  
- split tracking  
- sample references  
- lineage references  
- dataset contract validation  
  
B. dq_sdk  
- schema checks  
- missingness checks  
- consistency checks  
- distribution profiling  
- business rule checks  
- DQ summary  
- DQ exception building  
  
C. feature_sdk  
- reusable transformations  
- lagging  
- differencing  
- grouping/aggregation  
- controlled encoding  
- feature metadata  
- feature lineage  
  
D. evaluation_sdk  
- metric computation  
- diagnostics  
- calibration checks  
- stability checks  
- comparison framework  
- threshold evaluation  
- benchmark comparison  
  
E. dataprepsdk  
- Spark-first standard-template training-data preparation  
- lineage-driven prep  
- panel / cross-sectional / time-series / cohort / spell data prep  
- target generation  
- split generation  
- metadata, manifest, and lineage output  
- leakage checks  
- agent-safe deterministic APIs  
  
====================================================================  
2. TARGET OUTCOME OF WAVE 3  
====================================================================  
  
After Wave 3, the platform should be able to support an end-to-end  
governed data preparation flow such as:  
  
1. load approved dataprep config  
2. validate config and template  
3. read source datasets in Spark  
4. resolve lineage and joins  
5. construct target dataset by data structure type  
6. run DQ checks  
7. build train/test/oot split  
8. register dataset snapshot and manifests  
9. compute summary metrics  
10. return compact response envelope  
11. make outputs available to later scorecardsdk / validationsdk /  
    monitoringsdk layers  
  
This is the minimum viable governed data foundation.  
  
====================================================================  
3. UPDATED REPOSITORY STRUCTURE FOR WAVE 3  
====================================================================  
  
project_root/  
  src/  
    dataset_sdk/  
      __init__.py  
      models.py  
      dataset_registry.py  
      snapshot_manager.py  
      split_manager.py  
      sample_reference.py  
      lineage_reference.py  
      dataset_contract_validator.py  
      storage.py  
      exceptions.py  
  
    dq_sdk/  
      __init__.py  
      models.py  
      schema_checks.py  
      missingness_checks.py  
      consistency_checks.py  
      distribution_profile.py  
      business_rule_checks.py  
      dq_summary.py  
      dq_exception_builder.py  
      exceptions.py  
  
    feature_sdk/  
      __init__.py  
      models.py  
      transformation_engine.py  
      lag_engine.py  
      differencing_engine.py  
      grouping_engine.py  
      encoding_helpers.py  
      feature_metadata.py  
      feature_lineage.py  
      exceptions.py  
  
    evaluation_sdk/  
      __init__.py  
      models.py  
      metric_engine.py  
      diagnostic_engine.py  
      stability_checks.py  
      calibration_checks.py  
      comparison_framework.py  
      threshold_evaluator.py  
      benchmark_compare.py  
      exceptions.py  
  
    dataprepsdk/  
      __init__.py  
      models.py  
      template_registry.py  
      template_executor.py  
      source_reader.py  
      lineage_resolver.py  
      grain_manager.py  
      entity_mapper.py  
      time_aligner.py  
      target_builder.py  
      feature_aligner.py  
      split_builder.py  
      sample_builder.py  
      quality_checker.py  
      metadata_builder.py  
      lineage_builder.py  
      output_writer.py  
      manifest_builder.py  
      leakage_checker.py  
      config_validator.py  
  
      spark/  
        __init__.py  
        spark_session_manager.py  
        spark_source_reader.py  
        spark_lineage_resolver.py  
        spark_grain_manager.py  
        spark_entity_mapper.py  
        spark_time_aligner.py  
        spark_target_builder.py  
        spark_feature_aligner.py  
        spark_panel_constructor.py  
        spark_cohort_builder.py  
        spark_spell_builder.py  
        spark_split_builder.py  
        spark_quality_checker.py  
        spark_output_writer.py  
        spark_manifest_builder.py  
        spark_utils.py  
  
      templates/  
        __init__.py  
        cross_sectional_template.py  
        panel_template.py  
        time_series_template.py  
        cohort_snapshot_template.py  
        event_history_template.py  
        hierarchical_join_template.py  
        macro_merge_template.py  
        split_template.py  
  
      exceptions.py  
  
    platform_core/  
      controllers/  
        data_prep_controller.py  
        dataset_controller.py  
        dq_controller.py  
        feature_controller.py  
        evaluation_controller.py  
  
      bridges/  
        agent_bridge/  
          dataset_context_builder.py  
          data_prep_response_normalizer.py  
  
  tests/  
    unit/  
      dataset_sdk/  
      dq_sdk/  
      feature_sdk/  
      evaluation_sdk/  
      dataprepsdk/  
    integration/  
      test_dataset_registration_flow.py  
      test_dq_pipeline_flow.py  
      test_feature_lineage_flow.py  
      test_evaluation_comparison_flow.py  
      test_dataprep_cross_sectional_flow.py  
      test_dataprep_panel_flow.py  
      test_dataprep_time_series_flow.py  
      test_dataprep_cohort_flow.py  
      test_dataprep_spell_flow.py  
  
  notebooks/  
    dataset_playbook.ipynb  
    dq_playbook.ipynb  
    feature_playbook.ipynb  
    evaluation_playbook.ipynb  
    dataprep_playbook.ipynb  
    spark_dataprep_playbook.ipynb  
  
====================================================================  
4. DATASET SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
4.1 Purpose  
--------------------------------------------------------------------  
dataset_sdk is the canonical dataset identity and reproducibility  
layer.  
  
It should:  
- register dataset objects  
- manage snapshots  
- track splits  
- preserve sample references  
- preserve lineage references  
- validate dataset contracts  
  
It is not the transformation engine itself.  
It is the governed metadata layer around datasets.  
  
--------------------------------------------------------------------  
4.2 File-by-file design  
--------------------------------------------------------------------  
  
dataset_sdk/models.py  
Purpose:  
Define dataset-related models.  
  
Key models:  
- DatasetRecord  
- DatasetSnapshotRecord  
- SplitRecord  
- SampleReferenceRecord  
- LineageReferenceRecord  
- DatasetContract  
- DatasetCoverageSummary  
  
--------------------------------------------------  
dataset_sdk/dataset_registry.py  
--------------------------------------------------  
Purpose:  
Create and manage canonical dataset identities.  
  
Responsibilities:  
- create dataset record  
- fetch dataset by ID  
- update metadata  
- list datasets by project/domain/model family  
  
Main functions:  
- register_dataset(...)  
- get_dataset(...)  
- update_dataset(...)  
- search_datasets(...)  
  
Depends on:  
- registry_sdk  
- config_sdk  
- artifactsdk  
  
--------------------------------------------------  
dataset_sdk/snapshot_manager.py  
--------------------------------------------------  
Purpose:  
Manage dataset snapshots.  
  
Responsibilities:  
- create snapshot record  
- link snapshot to dataset  
- list historical snapshots  
- mark active or superseded snapshot  
  
Main functions:  
- create_snapshot(...)  
- get_snapshot(...)  
- list_snapshots(...)  
- mark_snapshot_status(...)  
  
Depends on:  
- dataset_registry.py  
- artifactsdk  
- observabilitysdk  
  
--------------------------------------------------  
dataset_sdk/split_manager.py  
--------------------------------------------------  
Purpose:  
Track sample split definitions and outputs.  
  
Responsibilities:  
- register dev/test/oot/holdout definitions  
- attach split refs to snapshot  
- summarize split counts and rules  
  
Main functions:  
- register_split(...)  
- get_split(...)  
- summarize_split(...)  
  
Depends on:  
- snapshot_manager.py  
  
--------------------------------------------------  
dataset_sdk/sample_reference.py  
--------------------------------------------------  
Purpose:  
Document sample construction logic.  
  
Responsibilities:  
- store sample rules  
- store sample filters  
- store inclusion/exclusion logic  
- store sample count summaries  
  
Main functions:  
- create_sample_reference(...)  
- get_sample_reference(...)  
  
Depends on:  
- dataset_registry.py  
- snapshot_manager.py  
  
--------------------------------------------------  
dataset_sdk/lineage_reference.py  
--------------------------------------------------  
Purpose:  
Store lineage references from prepared dataset back to sources.  
  
Responsibilities:  
- link dataset snapshot to source datasets  
- store join path summary  
- store transformation summary ref  
  
Main functions:  
- create_lineage_reference(...)  
- get_lineage_reference(...)  
  
Depends on:  
- dataset_registry.py  
- artifactsdk  
  
--------------------------------------------------  
dataset_sdk/dataset_contract_validator.py  
--------------------------------------------------  
Purpose:  
Validate dataset against governed contract.  
  
Responsibilities:  
- check required columns  
- check types  
- check grain uniqueness  
- check required metadata fields  
  
Main functions:  
- validate_dataset_contract(...)  
- validate_snapshot_contract(...)  
  
Depends on:  
- config_sdk  
- dq_sdk optionally  
  
--------------------------------------------------  
dataset_sdk/storage.py  
--------------------------------------------------  
Purpose:  
Persist and retrieve dataset metadata records.  
  
Responsibilities:  
- metadata storage abstraction  
- initial implementation can be file/sqlite/object backed  
  
--------------------------------------------------  
dataset_sdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Dataset-specific exceptions.  
  
Examples:  
- DatasetNotFoundError  
- SnapshotNotFoundError  
- InvalidSplitError  
- DatasetContractError  
  
--------------------------------------------------------------------  
4.3 Public API for dataset_sdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
- register_dataset(...)  
- create_snapshot(...)  
- register_split(...)  
- create_sample_reference(...)  
- create_lineage_reference(...)  
- validate_dataset_contract(...)  
- get_dataset(...)  
- get_snapshot(...)  
- list_snapshots(...)  
  
--------------------------------------------------------------------  
4.4 Implementation priorities for dataset_sdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. dataset_registry.py  
3. snapshot_manager.py  
4. split_manager.py  
5. lineage_reference.py  
6. sample_reference.py  
7. dataset_contract_validator.py  
8. storage.py  
  
====================================================================  
5. DQ SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
5.1 Purpose  
--------------------------------------------------------------------  
dq_sdk provides preparation-stage and modeling-stage data quality  
checks.  
  
It should:  
- validate schema  
- profile missingness  
- detect duplicates and consistency issues  
- summarize data quality  
- build DQ exceptions where needed  
  
--------------------------------------------------------------------  
5.2 File-by-file design  
--------------------------------------------------------------------  
  
dq_sdk/models.py  
Purpose:  
Define DQ result models.  
  
Key models:  
- SchemaCheckResult  
- MissingnessSummary  
- ConsistencyCheckResult  
- DistributionProfileSummary  
- BusinessRuleResult  
- DQSummary  
- DQExceptionRecord  
  
--------------------------------------------------  
dq_sdk/schema_checks.py  
--------------------------------------------------  
Purpose:  
Check schema integrity.  
  
Responsibilities:  
- validate required columns  
- validate expected data types  
- validate duplicate column names  
- validate forbidden missing columns  
  
Main functions:  
- run_schema_checks(...)  
- validate_required_columns(...)  
  
--------------------------------------------------  
dq_sdk/missingness_checks.py  
--------------------------------------------------  
Purpose:  
Profile nulls and missingness patterns.  
  
Responsibilities:  
- null counts  
- null ratios  
- missingness by segment if needed  
- threshold-based missingness warnings  
  
Main functions:  
- run_missingness_checks(...)  
- summarize_missingness(...)  
  
--------------------------------------------------  
dq_sdk/consistency_checks.py  
--------------------------------------------------  
Purpose:  
Check structural and business consistency.  
  
Responsibilities:  
- key uniqueness  
- duplicate grain  
- date order consistency  
- target consistency  
- status/value consistency  
  
Main functions:  
- run_consistency_checks(...)  
- detect_duplicate_keys(...)  
  
--------------------------------------------------  
dq_sdk/distribution_profile.py  
--------------------------------------------------  
Purpose:  
Generate compact profiling summaries.  
  
Responsibilities:  
- numeric summaries  
- category counts  
- cardinality summaries  
- top category movement if provided two samples  
  
Main functions:  
- build_distribution_profile(...)  
- summarize_distribution(...)  
  
--------------------------------------------------  
dq_sdk/business_rule_checks.py  
--------------------------------------------------  
Purpose:  
Run governed business-rule validations.  
  
Responsibilities:  
- credit-risk-specific checks  
- value range checks  
- stage logic checks  
- portfolio-specific rules  
  
Main functions:  
- run_business_rule_checks(...)  
- evaluate_rule_set(...)  
  
--------------------------------------------------  
dq_sdk/dq_summary.py  
--------------------------------------------------  
Purpose:  
Create a compact DQ summary object.  
  
Responsibilities:  
- aggregate all DQ checks  
- classify severity  
- produce token-thrifty summary for agents and reviews  
  
Main functions:  
- build_dq_summary(...)  
- classify_dq_status(...)  
  
--------------------------------------------------  
dq_sdk/dq_exception_builder.py  
--------------------------------------------------  
Purpose:  
Convert material DQ failures into structured exception objects.  
  
Responsibilities:  
- build DQ exceptions  
- attach linked artifacts and metrics  
- support HITL and governance routing  
  
Main functions:  
- create_dq_exception(...)  
- build_exception_payload(...)  
  
--------------------------------------------------  
dq_sdk/exceptions.py  
--------------------------------------------------  
Purpose:  
DQ-specific exceptions.  
  
Examples:  
- SchemaValidationError  
- MissingnessThresholdError  
- ConsistencyCheckError  
  
--------------------------------------------------------------------  
5.3 Public API for dq_sdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
- run_schema_checks(...)  
- run_missingness_checks(...)  
- run_consistency_checks(...)  
- build_distribution_profile(...)  
- run_business_rule_checks(...)  
- build_dq_summary(...)  
- create_dq_exception(...)  
  
--------------------------------------------------------------------  
5.4 Implementation priorities for dq_sdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. schema_checks.py  
3. missingness_checks.py  
4. consistency_checks.py  
5. dq_summary.py  
6. distribution_profile.py  
7. business_rule_checks.py  
8. dq_exception_builder.py  
  
====================================================================  
6. FEATURE SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
6.1 Purpose  
--------------------------------------------------------------------  
feature_sdk is the reusable transformation and feature lineage layer.  
  
It should:  
- apply controlled transformations  
- build lag and differenced features  
- aggregate and group features  
- support controlled encoding  
- preserve feature metadata and lineage  
  
--------------------------------------------------------------------  
6.2 File-by-file design  
--------------------------------------------------------------------  
  
feature_sdk/models.py  
Purpose:  
Define feature models.  
  
Key models:  
- FeatureDefinition  
- FeatureTransformationRecord  
- FeatureLineageRecord  
- FeatureMetadataRecord  
- FeatureSetSummary  
  
--------------------------------------------------  
feature_sdk/transformation_engine.py  
--------------------------------------------------  
Purpose:  
Apply base feature transformations.  
  
Responsibilities:  
- ratio transforms  
- log transforms  
- winsor rules if allowed  
- standard mathematical transforms  
- safe null-aware transforms  
  
Main functions:  
- apply_transformations(...)  
- apply_standard_transform(...)  
  
--------------------------------------------------  
feature_sdk/lag_engine.py  
--------------------------------------------------  
Purpose:  
Create lagged features.  
  
Responsibilities:  
- lag by time index  
- lag by entity and time  
- multiple lag support  
- lag metadata output  
  
Main functions:  
- build_lags(...)  
- build_entity_time_lags(...)  
  
--------------------------------------------------  
feature_sdk/differencing_engine.py  
--------------------------------------------------  
Purpose:  
Create differenced features.  
  
Responsibilities:  
- first difference  
- relative difference  
- configurable difference logic  
  
Main functions:  
- build_differences(...)  
- build_relative_differences(...)  
  
--------------------------------------------------  
feature_sdk/grouping_engine.py  
--------------------------------------------------  
Purpose:  
Create grouped and aggregated features.  
  
Responsibilities:  
- aggregate by entity  
- aggregate by time window  
- roll-up child to parent  
- segment-level aggregations  
  
Main functions:  
- build_grouped_features(...)  
- build_hierarchical_aggregates(...)  
  
--------------------------------------------------  
feature_sdk/encoding_helpers.py  
--------------------------------------------------  
Purpose:  
Apply governed encodings.  
  
Responsibilities:  
- category mapping  
- ordinal encoding  
- controlled one-hot preparation metadata  
- missing category handling  
  
Main functions:  
- encode_categorical(...)  
- map_categories(...)  
  
--------------------------------------------------  
feature_sdk/feature_metadata.py  
--------------------------------------------------  
Purpose:  
Store feature metadata.  
  
Responsibilities:  
- feature catalog  
- transformation tags  
- domain tags  
- source refs  
- missingness profile summary  
  
Main functions:  
- register_feature_metadata(...)  
- build_feature_catalog(...)  
  
--------------------------------------------------  
feature_sdk/feature_lineage.py  
--------------------------------------------------  
Purpose:  
Track feature lineage.  
  
Responsibilities:  
- source columns used  
- transformation steps  
- transformation order  
- output feature linkage  
  
Main functions:  
- register_feature_lineage(...)  
- get_feature_lineage(...)  
  
--------------------------------------------------  
feature_sdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Feature-specific exceptions.  
  
Examples:  
- FeatureTransformationError  
- LagBuildError  
- EncodingRuleError  
  
--------------------------------------------------------------------  
6.3 Public API for feature_sdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
- apply_transformations(...)  
- build_lags(...)  
- build_differences(...)  
- build_grouped_features(...)  
- encode_categorical(...)  
- register_feature_metadata(...)  
- register_feature_lineage(...)  
  
--------------------------------------------------------------------  
6.4 Implementation priorities for feature_sdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. transformation_engine.py  
3. grouping_engine.py  
4. lag_engine.py  
5. feature_metadata.py  
6. feature_lineage.py  
7. differencing_engine.py  
8. encoding_helpers.py  
  
====================================================================  
7. EVALUATION SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
7.1 Purpose  
--------------------------------------------------------------------  
evaluation_sdk is the shared metrics and comparison engine.  
  
It should:  
- compute metrics  
- compute diagnostics  
- compute stability metrics  
- compute calibration checks  
- compare candidates  
- evaluate against thresholds  
  
--------------------------------------------------------------------  
7.2 File-by-file design  
--------------------------------------------------------------------  
  
evaluation_sdk/models.py  
Purpose:  
Define metric and comparison models.  
  
Key models:  
- MetricResult  
- DiagnosticResult  
- StabilityResult  
- CalibrationResult  
- ComparisonSummary  
- ThresholdEvaluationResult  
- BenchmarkComparisonResult  
  
--------------------------------------------------  
evaluation_sdk/metric_engine.py  
--------------------------------------------------  
Purpose:  
Compute core metrics.  
  
Responsibilities:  
- model-family-neutral metric wrapper  
- store metric metadata  
- return normalized metric objects  
  
Main functions:  
- compute_metrics(...)  
- compute_metric_set(...)  
  
--------------------------------------------------  
evaluation_sdk/diagnostic_engine.py  
--------------------------------------------------  
Purpose:  
Compute diagnostics.  
  
Responsibilities:  
- residual/fit diagnostics  
- monotonicity checks  
- ranking checks  
- binary model diagnostics  
- time-series diagnostics wrapper  
  
Main functions:  
- run_diagnostics(...)  
- build_diagnostic_summary(...)  
  
--------------------------------------------------  
evaluation_sdk/stability_checks.py  
--------------------------------------------------  
Purpose:  
Run stability-related tests.  
  
Responsibilities:  
- PSI  
- CSI  
- parameter drift summary  
- drift status classification  
  
Main functions:  
- run_stability_checks(...)  
- summarize_stability(...)  
  
--------------------------------------------------  
evaluation_sdk/calibration_checks.py  
--------------------------------------------------  
Purpose:  
Run calibration-related checks.  
  
Responsibilities:  
- observed vs predicted summaries  
- calibration bands  
- calibration error summary  
  
Main functions:  
- run_calibration_checks(...)  
- summarize_calibration(...)  
  
--------------------------------------------------  
evaluation_sdk/comparison_framework.py  
--------------------------------------------------  
Purpose:  
Compare multiple candidates or versions.  
  
Responsibilities:  
- normalize candidate metrics  
- rank candidates  
- identify trade-offs  
- create comparison summary  
  
Main functions:  
- compare_candidates(...)  
- build_comparison_summary(...)  
  
--------------------------------------------------  
evaluation_sdk/threshold_evaluator.py  
--------------------------------------------------  
Purpose:  
Evaluate metrics against thresholds.  
  
Responsibilities:  
- pass/warn/breach classification  
- stage/domain-aware threshold interpretation  
  
Main functions:  
- evaluate_thresholds(...)  
- classify_metric_status(...)  
  
--------------------------------------------------  
evaluation_sdk/benchmark_compare.py  
--------------------------------------------------  
Purpose:  
Compare against baseline or benchmark.  
  
Responsibilities:  
- historical baseline comparison  
- benchmark pack comparison  
- validation reference comparison  
  
Main functions:  
- compare_to_benchmark(...)  
- summarize_benchmark_gap(...)  
  
--------------------------------------------------  
evaluation_sdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Evaluation-specific exceptions.  
  
Examples:  
- MetricComputationError  
- ComparisonError  
- CalibrationError  
  
--------------------------------------------------------------------  
7.3 Public API for evaluation_sdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
- compute_metrics(...)  
- run_diagnostics(...)  
- run_stability_checks(...)  
- run_calibration_checks(...)  
- compare_candidates(...)  
- evaluate_thresholds(...)  
- compare_to_benchmark(...)  
  
--------------------------------------------------------------------  
7.4 Implementation priorities for evaluation_sdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. metric_engine.py  
3. diagnostic_engine.py  
4. comparison_framework.py  
5. threshold_evaluator.py  
6. stability_checks.py  
7. calibration_checks.py  
8. benchmark_compare.py  
  
====================================================================  
8. DATAPREPSDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
8.1 Purpose  
--------------------------------------------------------------------  
dataprepsdk is the Spark-first governed training-data preparation SDK.  
  
It should:  
- run only approved standard templates  
- support pre-prepared and lineage-driven source modes  
- build cross-sectional / panel / time-series / cohort / spell data  
- generate targets  
- generate splits  
- write manifests and lineage outputs  
- work in CML with S3 access  
- expose deterministic APIs for agents  
  
--------------------------------------------------------------------  
8.2 Design principle  
--------------------------------------------------------------------  
Heavy data preparation must occur in Spark.  
Python-only logic should be used only for:  
- config parsing  
- orchestration  
- metadata  
- manifest writing  
- response summarization  
  
--------------------------------------------------------------------  
8.3 File-by-file design – root package  
--------------------------------------------------------------------  
  
dataprepsdk/models.py  
Purpose:  
Define dataprep objects.  
  
Key models:  
- TemplateDefinition  
- DataPrepRequest  
- DataPrepResult  
- SourceMapping  
- GrainDefinition  
- TimeDefinition  
- TargetDefinition  
- SplitDefinition  
- DataPrepManifest  
- LineageManifest  
- LeakageCheckSummary  
  
--------------------------------------------------  
dataprepsdk/template_registry.py  
--------------------------------------------------  
Purpose:  
Manage approved templates.  
  
Responsibilities:  
- register approved templates  
- resolve by template_id  
- validate supported data type and domain  
  
Main functions:  
- get_template(...)  
- list_templates(...)  
- validate_template_request(...)  
  
--------------------------------------------------  
dataprepsdk/template_executor.py  
--------------------------------------------------  
Purpose:  
Execute approved template path.  
  
Responsibilities:  
- route request to appropriate template implementation  
- coordinate Spark path  
- return compact DataPrepResult  
  
Main functions:  
- execute_template(...)  
- execute_request(...)  
  
Depends on:  
- template_registry.py  
- config_validator.py  
- spark layer  
  
--------------------------------------------------  
dataprepsdk/source_reader.py  
--------------------------------------------------  
Purpose:  
Logical source reader abstraction.  
  
Responsibilities:  
- prepare source descriptors  
- validate source accessibility  
- return source metadata  
  
Main functions:  
- resolve_sources(...)  
- validate_source_refs(...)  
  
--------------------------------------------------  
dataprepsdk/lineage_resolver.py  
--------------------------------------------------  
Purpose:  
Resolve lineage and join plan from config.  
  
Responsibilities:  
- join key resolution  
- source order  
- grain transitions  
- source dependency mapping  
  
Main functions:  
- resolve_lineage(...)  
- build_join_plan(...)  
  
--------------------------------------------------  
dataprepsdk/grain_manager.py  
--------------------------------------------------  
Purpose:  
Define and validate target grain.  
  
Responsibilities:  
- one-row-per-entity  
- one-row-per-entity-time  
- one-row-per-spell-period  
- one-row-per-cohort-member  
  
Main functions:  
- resolve_grain(...)  
- validate_grain(...)  
  
--------------------------------------------------  
dataprepsdk/entity_mapper.py  
--------------------------------------------------  
Purpose:  
Map entity hierarchies.  
  
Responsibilities:  
- customer/account/contract links  
- parent-child mapping  
- retained output grain  
  
Main functions:  
- resolve_entity_mapping(...)  
- validate_entity_relationships(...)  
  
--------------------------------------------------  
dataprepsdk/time_aligner.py  
--------------------------------------------------  
Purpose:  
Resolve observation and target time logic.  
  
Responsibilities:  
- as-of date  
- reporting date  
- cohort date  
- performance window  
- lookback and forward horizon  
  
Main functions:  
- resolve_time_windows(...)  
- validate_time_alignment(...)  
  
--------------------------------------------------  
dataprepsdk/target_builder.py  
--------------------------------------------------  
Purpose:  
Define target construction logic.  
  
Responsibilities:  
- binary targets  
- severity targets  
- recovery targets  
- time-to-event targets  
- horizon alignment  
  
Main functions:  
- resolve_target_definition(...)  
- validate_target_logic(...)  
  
--------------------------------------------------  
dataprepsdk/feature_aligner.py  
--------------------------------------------------  
Purpose:  
Resolve which feature sets are needed.  
  
Responsibilities:  
- static feature refs  
- dynamic feature refs  
- macro feature refs  
- hierarchical aggregated feature refs  
  
Main functions:  
- resolve_feature_sets(...)  
- validate_feature_alignment(...)  
  
--------------------------------------------------  
dataprepsdk/split_builder.py  
--------------------------------------------------  
Purpose:  
Define split logic.  
  
Responsibilities:  
- random split  
- time-based split  
- cohort-based split  
- entity-based split  
  
Main functions:  
- resolve_split_definition(...)  
- validate_split_strategy(...)  
  
--------------------------------------------------  
dataprepsdk/sample_builder.py  
--------------------------------------------------  
Purpose:  
Define sample inclusion logic.  
  
Responsibilities:  
- sample filters  
- exclusions  
- eligibility windows  
- minimum data requirements  
  
Main functions:  
- resolve_sample_rules(...)  
- validate_sample_logic(...)  
  
--------------------------------------------------  
dataprepsdk/quality_checker.py  
--------------------------------------------------  
Purpose:  
Coordinate DQ and prep checks.  
  
Responsibilities:  
- schema quality  
- join success  
- split coverage  
- target coverage  
- grain uniqueness  
  
Main functions:  
- run_prep_quality_checks(...)  
- build_prep_quality_summary(...)  
  
--------------------------------------------------  
dataprepsdk/metadata_builder.py  
--------------------------------------------------  
Purpose:  
Build metadata summaries.  
  
Responsibilities:  
- row counts  
- time coverage  
- grain description  
- split summary  
- target summary  
  
Main functions:  
- build_metadata_summary(...)  
  
--------------------------------------------------  
dataprepsdk/lineage_builder.py  
--------------------------------------------------  
Purpose:  
Build lineage manifests.  
  
Responsibilities:  
- source lineage  
- join lineage  
- target lineage  
- split lineage  
- output lineage  
  
Main functions:  
- build_lineage_manifest(...)  
  
--------------------------------------------------  
dataprepsdk/output_writer.py  
--------------------------------------------------  
Purpose:  
Write prepared outputs and side outputs.  
  
Responsibilities:  
- write prepared dataset  
- write split table  
- write manifest refs  
- return artifact refs  
  
Main functions:  
- write_outputs(...)  
  
--------------------------------------------------  
dataprepsdk/manifest_builder.py  
--------------------------------------------------  
Purpose:  
Build final prep manifest package.  
  
Responsibilities:  
- build data prep manifest  
- link metadata and lineage  
- support reproducibility  
  
Main functions:  
- build_manifest_bundle(...)  
  
--------------------------------------------------  
dataprepsdk/leakage_checker.py  
--------------------------------------------------  
Purpose:  
Check for target leakage.  
  
Responsibilities:  
- future window overlap checks  
- forbidden future field detection  
- target alignment consistency  
  
Main functions:  
- run_leakage_checks(...)  
- summarize_leakage_risk(...)  
  
--------------------------------------------------  
dataprepsdk/config_validator.py  
--------------------------------------------------  
Purpose:  
Validate dataprep config.  
  
Responsibilities:  
- validate required sections  
- validate allowed template  
- validate source mapping completeness  
  
Main functions:  
- validate_dataprep_config(...)  
  
--------------------------------------------------  
dataprepsdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Dataprep-specific exceptions.  
  
Examples:  
- TemplateNotSupportedError  
- InvalidLineageConfigError  
- TargetDefinitionError  
- LeakageRiskError  
  
====================================================================  
9. DATAPREPSDK SPARK LAYER IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
9.1 spark_session_manager.py  
--------------------------------------------------------------------  
Purpose:  
Manage Spark session and Spark config checks.  
  
Responsibilities:  
- attach to Spark  
- validate Spark availability  
- surface session summary  
  
--------------------------------------------------------------------  
9.2 spark_source_reader.py  
--------------------------------------------------------------------  
Purpose:  
Read source datasets into Spark DataFrames.  
  
Responsibilities:  
- read parquet/csv/table refs  
- project columns where possible  
- handle S3 paths  
- return DataFrames with source metadata  
  
--------------------------------------------------------------------  
9.3 spark_lineage_resolver.py  
--------------------------------------------------------------------  
Purpose:  
Translate lineage plan into Spark join operations.  
  
Responsibilities:  
- join ordering  
- key enforcement  
- join type handling  
  
--------------------------------------------------------------------  
9.4 spark_grain_manager.py  
--------------------------------------------------------------------  
Purpose:  
Enforce output grain in Spark.  
  
Responsibilities:  
- deduplicate  
- aggregate  
- reshape to target grain  
  
--------------------------------------------------------------------  
9.5 spark_entity_mapper.py  
--------------------------------------------------------------------  
Purpose:  
Resolve entity hierarchy in Spark.  
  
Responsibilities:  
- join parent-child structure  
- aggregate child-to-parent if needed  
  
--------------------------------------------------------------------  
9.6 spark_time_aligner.py  
--------------------------------------------------------------------  
Purpose:  
Create observation/performance windows in Spark.  
  
Responsibilities:  
- lag windows  
- lookback windows  
- future performance windows  
- date alignment  
  
--------------------------------------------------------------------  
9.7 spark_target_builder.py  
--------------------------------------------------------------------  
Purpose:  
Construct target columns in Spark.  
  
Responsibilities:  
- binary target generation  
- event target generation  
- recovery target generation  
- forward horizon alignment  
  
--------------------------------------------------------------------  
9.8 spark_feature_aligner.py  
--------------------------------------------------------------------  
Purpose:  
Align features to the target grain/time in Spark.  
  
Responsibilities:  
- join static and dynamic features  
- align macro features  
- maintain compact column set  
  
--------------------------------------------------------------------  
9.9 spark_panel_constructor.py  
--------------------------------------------------------------------  
Purpose:  
Build panel / repeated-observation datasets.  
  
Responsibilities:  
- one-row-per-entity-time  
- balanced/unbalanced panel handling  
  
--------------------------------------------------------------------  
9.10 spark_cohort_builder.py  
--------------------------------------------------------------------  
Purpose:  
Build cohort datasets.  
  
Responsibilities:  
- derive cohort members  
- preserve cohort date  
- build follow-up sequences if needed  
  
--------------------------------------------------------------------  
9.11 spark_spell_builder.py  
--------------------------------------------------------------------  
Purpose:  
Build spell/event-history datasets.  
  
Responsibilities:  
- person-period construction  
- event flags  
- censoring flags  
- spell duration support  
  
--------------------------------------------------------------------  
9.12 spark_split_builder.py  
--------------------------------------------------------------------  
Purpose:  
Apply split logic in Spark.  
  
Responsibilities:  
- time split  
- entity split  
- random split with seed control  
- cohort split  
  
--------------------------------------------------------------------  
9.13 spark_quality_checker.py  
--------------------------------------------------------------------  
Purpose:  
Run scalable prep checks in Spark.  
  
Responsibilities:  
- duplicate grain checks  
- join success rates  
- target coverage  
- split balance  
  
--------------------------------------------------------------------  
9.14 spark_output_writer.py  
--------------------------------------------------------------------  
Purpose:  
Write final Spark outputs.  
  
Responsibilities:  
- write prepared DataFrames  
- write split outputs  
- support governed output paths  
  
--------------------------------------------------------------------  
9.15 spark_manifest_builder.py  
--------------------------------------------------------------------  
Purpose:  
Build Spark execution manifest.  
  
Responsibilities:  
- row counts  
- partition info  
- key source refs  
- output refs  
  
--------------------------------------------------------------------  
9.16 spark_utils.py  
--------------------------------------------------------------------  
Purpose:  
Reusable Spark helpers.  
  
Responsibilities:  
- common window utilities  
- safe join helpers  
- projection helpers  
- partition helpers  
  
====================================================================  
10. DATAPREPSDK TEMPLATE IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
10.1 cross_sectional_template.py  
--------------------------------------------------------------------  
Purpose:  
Prepare one-row-per-unit cross-sectional training data.  
  
Examples:  
- application scorecard  
- annual borrower snapshot  
  
--------------------------------------------------------------------  
10.2 panel_template.py  
--------------------------------------------------------------------  
Purpose:  
Prepare repeated observation panel data.  
  
Examples:  
- account-month  
- customer-month  
  
--------------------------------------------------------------------  
10.3 time_series_template.py  
--------------------------------------------------------------------  
Purpose:  
Prepare time series data.  
  
Examples:  
- portfolio default rate series  
- macro forecasting data  
  
--------------------------------------------------------------------  
10.4 cohort_snapshot_template.py  
--------------------------------------------------------------------  
Purpose:  
Prepare cohort-aligned datasets.  
  
Examples:  
- origination cohort  
- reporting cohort  
  
--------------------------------------------------------------------  
10.5 event_history_template.py  
--------------------------------------------------------------------  
Purpose:  
Prepare spell / event-history datasets.  
  
Examples:  
- hazard rate setup  
- cure spell setup  
  
--------------------------------------------------------------------  
10.6 hierarchical_join_template.py  
--------------------------------------------------------------------  
Purpose:  
Prepare datasets requiring hierarchy merge logic.  
  
Examples:  
- customer-account-contract alignment  
  
--------------------------------------------------------------------  
10.7 macro_merge_template.py  
--------------------------------------------------------------------  
Purpose:  
Attach macroeconomic features.  
  
Examples:  
- monthly macro merge  
- scenario macro merge  
  
--------------------------------------------------------------------  
10.8 split_template.py  
--------------------------------------------------------------------  
Purpose:  
Reusable split application helper template.  
  
Examples:  
- time-based split  
- entity split  
- oot split  
  
====================================================================  
11. CONTROLLER LAYER EXPANSION FOR WAVE 3  
====================================================================  
  
platform_core/controllers/data_prep_controller.py  
Purpose:  
Coordinate end-to-end dataprep execution.  
  
Responsibilities:  
- validate request  
- call dataprepsdk  
- register dataset and artifacts  
- normalize response  
  
Main methods:  
- prepare_dataset(...)  
- reproduce_dataset(...)  
- get_dataprep_summary(...)  
  
--------------------------------------------------  
platform_core/controllers/dataset_controller.py  
--------------------------------------------------  
Purpose:  
Serve dataset metadata and snapshot operations.  
  
Main methods:  
- register_dataset_snapshot(...)  
- get_dataset_info(...)  
- list_snapshots(...)  
  
--------------------------------------------------  
platform_core/controllers/dq_controller.py  
--------------------------------------------------  
Purpose:  
Run and summarize DQ checks.  
  
Main methods:  
- run_dq_checks(...)  
- get_dq_summary(...)  
  
--------------------------------------------------  
platform_core/controllers/feature_controller.py  
--------------------------------------------------  
Purpose:  
Coordinate feature construction and metadata registration.  
  
Main methods:  
- build_features(...)  
- get_feature_catalog(...)  
  
--------------------------------------------------  
platform_core/controllers/evaluation_controller.py  
--------------------------------------------------  
Purpose:  
Run evaluation logic and candidate comparison.  
  
Main methods:  
- evaluate_candidate(...)  
- compare_candidates(...)  
- evaluate_thresholds(...)  
  
====================================================================  
12. AGENT BRIDGE EXPANSION FOR WAVE 3  
====================================================================  
  
platform_core/bridges/agent_bridge/dataset_context_builder.py  
Purpose:  
Build compact dataset-related agent context.  
  
Responsibilities:  
- dataset IDs  
- snapshot refs  
- split summary  
- DQ summary  
- lineage summary  
- token-thrifty dataprep summary  
  
--------------------------------------------------  
platform_core/bridges/agent_bridge/data_prep_response_normalizer.py  
--------------------------------------------------  
Purpose:  
Normalize dataprep and evaluation outputs into standard response  
envelope.  
  
Responsibilities:  
- compact output  
- artifact refs  
- manifest refs  
- warning mapping  
- workflow patch mapping  
  
====================================================================  
13. PUBLIC APIs FOR WAVE 3 PACKAGES  
====================================================================  
  
dataset_sdk public API:  
- register_dataset(...)  
- create_snapshot(...)  
- register_split(...)  
- create_sample_reference(...)  
- create_lineage_reference(...)  
- validate_dataset_contract(...)  
- get_dataset(...)  
- get_snapshot(...)  
  
dq_sdk public API:  
- run_schema_checks(...)  
- run_missingness_checks(...)  
- run_consistency_checks(...)  
- build_distribution_profile(...)  
- run_business_rule_checks(...)  
- build_dq_summary(...)  
- create_dq_exception(...)  
  
feature_sdk public API:  
- apply_transformations(...)  
- build_lags(...)  
- build_differences(...)  
- build_grouped_features(...)  
- encode_categorical(...)  
- register_feature_metadata(...)  
- register_feature_lineage(...)  
  
evaluation_sdk public API:  
- compute_metrics(...)  
- run_diagnostics(...)  
- run_stability_checks(...)  
- run_calibration_checks(...)  
- compare_candidates(...)  
- evaluate_thresholds(...)  
- compare_to_benchmark(...)  
  
dataprepsdk public API:  
- validate_dataprep_config(...)  
- validate_template_request(...)  
- execute_request(...)  
- build_cross_sectional_dataset(...)  
- build_panel_dataset(...)  
- build_time_series_dataset(...)  
- build_cohort_dataset(...)  
- build_event_history_dataset(...)  
- reproduce_dataset(...)  
  
dataprepsdk Spark public API:  
- build_cross_sectional_dataset_spark(...)  
- build_panel_dataset_spark(...)  
- build_time_series_dataset_spark(...)  
- build_cohort_dataset_spark(...)  
- build_event_history_dataset_spark(...)  
- run_prep_quality_checks_spark(...)  
  
====================================================================  
14. TEST BLUEPRINT FOR WAVE 3  
====================================================================  
  
tests/unit/dataset_sdk/test_dataset_registry.py  
- dataset record creation  
- duplicate dataset ID behavior  
- metadata updates  
  
tests/unit/dataset_sdk/test_snapshot_manager.py  
- snapshot creation  
- active/superseded status logic  
  
tests/unit/dq_sdk/test_schema_checks.py  
- missing column detection  
- wrong type detection  
  
tests/unit/dq_sdk/test_missingness_checks.py  
- null ratio classification  
  
tests/unit/feature_sdk/test_transformation_engine.py  
- standard transform outputs  
  
tests/unit/feature_sdk/test_lag_engine.py  
- lag correctness by entity/time  
  
tests/unit/evaluation_sdk/test_metric_engine.py  
- metric normalization and output  
  
tests/unit/evaluation_sdk/test_comparison_framework.py  
- candidate comparison ranking  
  
tests/unit/dataprepsdk/test_config_validator.py  
- config completeness validation  
  
tests/unit/dataprepsdk/test_template_registry.py  
- approved template resolution  
  
tests/unit/dataprepsdk/spark/test_spark_time_aligner.py  
- time window generation  
  
tests/unit/dataprepsdk/spark/test_spark_target_builder.py  
- target generation alignment  
  
tests/unit/dataprepsdk/spark/test_spark_split_builder.py  
- split logic  
  
tests/integration/test_dataset_registration_flow.py  
- dataprep -> dataset registration -> snapshot linkage  
  
tests/integration/test_dq_pipeline_flow.py  
- dataset -> DQ checks -> summary  
  
tests/integration/test_feature_lineage_flow.py  
- transformed features -> lineage registration  
  
tests/integration/test_evaluation_comparison_flow.py  
- candidate metrics -> comparison summary  
  
tests/integration/test_dataprep_cross_sectional_flow.py  
- cross-sectional end-to-end  
  
tests/integration/test_dataprep_panel_flow.py  
- panel end-to-end  
  
tests/integration/test_dataprep_time_series_flow.py  
- time series end-to-end  
  
tests/integration/test_dataprep_cohort_flow.py  
- cohort end-to-end  
  
tests/integration/test_dataprep_spell_flow.py  
- event-history end-to-end  
  
====================================================================  
15. NOTEBOOK PLAYBOOKS FOR WAVE 3  
====================================================================  
  
notebooks/dataset_playbook.ipynb  
- register dataset  
- create snapshot  
- track split and lineage  
  
notebooks/dq_playbook.ipynb  
- run schema and consistency checks  
- inspect compact DQ summary  
  
notebooks/feature_playbook.ipynb  
- apply standard transformations  
- build lags and grouped features  
- register metadata and lineage  
  
notebooks/evaluation_playbook.ipynb  
- compute metrics  
- compare candidate outputs  
- threshold evaluation demo  
  
notebooks/dataprep_playbook.ipynb  
- load dataprep config  
- validate template request  
- inspect logical prep plan  
  
notebooks/spark_dataprep_playbook.ipynb  
- run Spark cross-sectional example  
- run Spark panel example  
- inspect metadata and manifest output  
  
====================================================================  
16. WAVE 3 END-TO-END FLOW  
====================================================================  
  
Standard flow should be:  
  
1. data_prep_controller receives request  
2. config_sdk validates dataprep config  
3. dataprepsdk validates template and lineage config  
4. Spark execution path starts  
5. source datasets loaded  
6. lineage resolved  
7. target grain built  
8. target generated  
9. features aligned  
10. split built  
11. prep quality checks run  
12. outputs written  
13. dataset_sdk registers dataset and snapshot  
14. artifacts registered  
15. compact response returned  
  
Optional next:  
16. evaluation_controller compares candidate datasets or sample  
    variants if needed  
  
====================================================================  
17. BUILD ORDER FOR WAVE 3  
====================================================================  
  
Phase 3A – dataset foundations  
------------------------------  
1. dataset_sdk/models.py  
2. dataset_sdk/storage.py  
3. dataset_sdk/dataset_registry.py  
4. dataset_sdk/snapshot_manager.py  
5. dataset_sdk/split_manager.py  
6. dataset_sdk/lineage_reference.py  
7. dataset_sdk/sample_reference.py  
8. dataset_sdk/dataset_contract_validator.py  
  
Phase 3B – DQ foundations  
-------------------------  
9. dq_sdk/models.py  
10. dq_sdk/schema_checks.py  
11. dq_sdk/missingness_checks.py  
12. dq_sdk/consistency_checks.py  
13. dq_sdk/dq_summary.py  
14. dq_sdk/distribution_profile.py  
15. dq_sdk/business_rule_checks.py  
16. dq_sdk/dq_exception_builder.py  
  
Phase 3C – feature foundations  
------------------------------  
17. feature_sdk/models.py  
18. feature_sdk/transformation_engine.py  
19. feature_sdk/grouping_engine.py  
20. feature_sdk/lag_engine.py  
21. feature_sdk/feature_metadata.py  
22. feature_sdk/feature_lineage.py  
23. feature_sdk/differencing_engine.py  
24. feature_sdk/encoding_helpers.py  
  
Phase 3D – evaluation foundations  
---------------------------------  
25. evaluation_sdk/models.py  
26. evaluation_sdk/metric_engine.py  
27. evaluation_sdk/diagnostic_engine.py  
28. evaluation_sdk/comparison_framework.py  
29. evaluation_sdk/threshold_evaluator.py  
30. evaluation_sdk/stability_checks.py  
31. evaluation_sdk/calibration_checks.py  
32. evaluation_sdk/benchmark_compare.py  
  
Phase 3E – dataprep logical layer  
---------------------------------  
33. dataprepsdk/models.py  
34. dataprepsdk/template_registry.py  
35. dataprepsdk/config_validator.py  
36. dataprepsdk/source_reader.py  
37. dataprepsdk/lineage_resolver.py  
38. dataprepsdk/grain_manager.py  
39. dataprepsdk/entity_mapper.py  
40. dataprepsdk/time_aligner.py  
41. dataprepsdk/target_builder.py  
42. dataprepsdk/feature_aligner.py  
43. dataprepsdk/split_builder.py  
44. dataprepsdk/sample_builder.py  
45. dataprepsdk/quality_checker.py  
46. dataprepsdk/metadata_builder.py  
47. dataprepsdk/lineage_builder.py  
48. dataprepsdk/manifest_builder.py  
49. dataprepsdk/leakage_checker.py  
50. dataprepsdk/output_writer.py  
51. dataprepsdk/template_executor.py  
  
Phase 3F – dataprep Spark layer  
--------------------------------  
52. dataprepsdk/spark/spark_session_manager.py  
53. dataprepsdk/spark/spark_utils.py  
54. dataprepsdk/spark/spark_source_reader.py  
55. dataprepsdk/spark/spark_lineage_resolver.py  
56. dataprepsdk/spark/spark_grain_manager.py  
57. dataprepsdk/spark/spark_entity_mapper.py  
58. dataprepsdk/spark/spark_time_aligner.py  
59. dataprepsdk/spark/spark_target_builder.py  
60. dataprepsdk/spark/spark_feature_aligner.py  
61. dataprepsdk/spark/spark_panel_constructor.py  
62. dataprepsdk/spark/spark_cohort_builder.py  
63. dataprepsdk/spark/spark_spell_builder.py  
64. dataprepsdk/spark/spark_split_builder.py  
65. dataprepsdk/spark/spark_quality_checker.py  
66. dataprepsdk/spark/spark_output_writer.py  
67. dataprepsdk/spark/spark_manifest_builder.py  
  
Phase 3G – templates and controllers  
------------------------------------  
68. dataprepsdk/templates/cross_sectional_template.py  
69. dataprepsdk/templates/panel_template.py  
70. dataprepsdk/templates/time_series_template.py  
71. dataprepsdk/templates/cohort_snapshot_template.py  
72. dataprepsdk/templates/event_history_template.py  
73. dataprepsdk/templates/hierarchical_join_template.py  
74. dataprepsdk/templates/macro_merge_template.py  
75. dataprepsdk/templates/split_template.py  
76. platform_core/controllers/dataset_controller.py  
77. platform_core/controllers/dq_controller.py  
78. platform_core/controllers/feature_controller.py  
79. platform_core/controllers/evaluation_controller.py  
80. platform_core/controllers/data_prep_controller.py  
81. platform_core/bridges/agent_bridge/dataset_context_builder.py  
82. platform_core/bridges/agent_bridge/data_prep_response_normalizer.py  
  
====================================================================  
18. WAVE 3 MINIMUM VIABLE DEMOS  
====================================================================  
  
Demo 1: Cross-sectional dataprep  
- approved template  
- Spark execution  
- dataset registration  
- DQ summary  
- compact response  
  
Demo 2: Panel dataprep  
- repeated observation panel  
- lag-ready setup  
- split summary  
- manifest generation  
  
Demo 3: Time-series dataprep  
- series alignment  
- target horizon logic  
- train/validation/forecast partition  
  
Demo 4: Cohort dataprep  
- cohort definition  
- cohort member build  
- target alignment  
  
Demo 5: Event-history dataprep  
- spell build  
- event indicator  
- person-period output  
  
====================================================================  
19. WHAT WAVE 3 SHOULD NOT DO  
====================================================================  
  
Wave 3 should not:  
- fit final domain models inside dataprepsdk  
- allow ungoverned custom prep scripts in standard execution path  
- move large Spark lineage logic into chat prompts  
- rely on pandas for governed large-scale prep  
- mix dataset metadata registry logic with workflow routing logic  
- let agents improvise unsupported templates  
  
====================================================================  
20. DELIVERABLE CHECKLIST FOR WAVE 3  
====================================================================  
  
Wave 3 is complete when all of the following exist:  
  
- dataset_sdk with dataset and snapshot registration  
- dq_sdk with compact DQ summaries  
- feature_sdk with feature transforms and lineage  
- evaluation_sdk with comparison and threshold logic  
- dataprepsdk with Spark-first governed execution  
- standard approved templates for key data structures  
- data_prep_controller and related controllers  
- compact standardized response envelopes  
- at least 5 working demos across supported data structures  
  
====================================================================  
21. FINAL RECOMMENDATION  
====================================================================  
  
Wave 3 should be built with a very strong contract-first mindset:  
  
- template contract first  
- dataset identity first  
- lineage first  
- Spark execution second  
- compact summaries by default  
- domain logic later in domain SDKs  
  
This will make the platform highly reusable and safe for agentic AI.  
  
====================================================================  
END OF WAVE 3 IMPLEMENTATION BLUEPRINT  
====================================================================  
  
====================================================================  
WAVE 4 IMPLEMENTATION BLUEPRINT  
SCORECARD SDK + VALIDATION SDK + REPORTING SDK  
END-TO-END MODEL DEVELOPMENT, VALIDATION, AND GOVERNED OUTPUTS  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This document continues the implementation blueprint with Wave 4.  
  
Wave 4 focuses on the first fully usable domain workflow for your  
platform. It adds:  
  
1. scorecardsdk  
2. validationsdk  
3. reporting_sdk  
  
Wave 4 is the point where the platform becomes capable of supporting  
a practical end-to-end scorecard lifecycle with governed review,  
validation, and reporting.  
  
This wave should make the platform able to:  
- build and compare scorecard candidates  
- manage binning and feature review  
- fit and select scorecard models  
- support validation findings and model fitness review  
- finalize validation conclusions  
- generate technical notes and governance packs  
- produce reusable artifacts and review outputs for downstream  
  monitoring and annual review  
  
====================================================================  
1. WAVE 4 SCOPE  
====================================================================  
  
Wave 4 includes:  
  
A. scorecardsdk  
- fine classing  
- coarse classing  
- binning comparison  
- WoE / IV  
- feature shortlist  
- logistic model support  
- score scaling  
- score bands  
- scorecard outputs  
- scorecard monitoring support  
  
B. validationsdk  
- validation scope  
- evidence intake  
- model fitness framework  
- finding registry  
- severity support  
- conclusion engine  
- remediation tracking  
- validation outputs  
- benchmark comparison  
- evidence completeness  
  
C. reporting_sdk  
- technical report builder  
- executive summary builder  
- committee pack builder  
- validation note builder  
- narrative blocks  
- chart/table export  
- pack assembler  
  
====================================================================  
2. TARGET OUTCOME OF WAVE 4  
====================================================================  
  
After Wave 4, the platform should be able to support an end-to-end  
scorecard workflow such as:  
  
1. prepare training dataset in dataprepsdk  
2. run fine classing  
3. open coarse classing review  
4. compare binning versions  
5. finalize shortlisted variables  
6. fit scorecard candidates  
7. compare and select final model  
8. review score scaling and score bands  
9. produce model artifacts  
10. open validation workflow  
11. record findings and model fitness view  
12. finalize validation conclusion  
13. generate technical pack and committee pack  
  
This is the first strong full-lifecycle business workflow.  
  
====================================================================  
3. UPDATED REPOSITORY STRUCTURE FOR WAVE 4  
====================================================================  
  
project_root/  
  src/  
    scorecardsdk/  
      __init__.py  
      models.py  
      fine_classing.py  
      coarse_classing.py  
      binning_compare.py  
      woe_iv.py  
      feature_shortlist.py  
      logistic_models.py  
      score_scaling.py  
      score_bands.py  
      scorecard_outputs.py  
      scorecard_monitoring_support.py  
      exceptions.py  
  
    validationsdk/  
      __init__.py  
      models.py  
      validation_scope.py  
      evidence_intake.py  
      fitness_framework.py  
      finding_registry.py  
      issue_severity.py  
      conclusion_engine.py  
      remediation_tracker.py  
      validation_outputs.py  
      benchmark_compare.py  
      evidence_completeness.py  
      exceptions.py  
  
    reporting_sdk/  
      __init__.py  
      models.py  
      technical_report_builder.py  
      executive_summary_builder.py  
      committee_pack_builder.py  
      validation_note_builder.py  
      narrative_blocks.py  
      chart_table_export.py  
      pack_assembler.py  
      exceptions.py  
  
    platform_core/  
      controllers/  
        scorecard_controller.py  
        validation_controller.py  
        reporting_controller.py  
      runtime/  
        scorecard_stage_resolver.py  
        validation_stage_resolver.py  
        reporting_mode_resolver.py  
      bridges/  
        agent_bridge/  
          scorecard_context_builder.py  
          validation_context_builder.py  
          reporting_context_builder.py  
          scorecard_response_normalizer.py  
          validation_response_normalizer.py  
          reporting_response_normalizer.py  
  
  tests/  
    unit/  
      scorecardsdk/  
      validationsdk/  
      reporting_sdk/  
    integration/  
      test_scorecard_binning_flow.py  
      test_scorecard_model_selection_flow.py  
      test_validation_finding_flow.py  
      test_validation_conclusion_flow.py  
      test_reporting_pack_flow.py  
  
  notebooks/  
    scorecard_playbook.ipynb  
    validation_playbook.ipynb  
    reporting_playbook.ipynb  
    end_to_end_scorecard_validation_playbook.ipynb  
  
====================================================================  
4. SCORECARD SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
4.1 Purpose  
--------------------------------------------------------------------  
scorecardsdk is the first domain SDK to provide a full model-building  
workflow.  
  
It should:  
- run scorecard-specific transformation logic  
- create binning candidates  
- compute WoE and IV  
- support variable review and shortlisting  
- fit candidate logistic scorecards  
- support score scaling and score bands  
- package scorecard outputs for validation and governance  
  
--------------------------------------------------------------------  
4.2 File-by-file design  
--------------------------------------------------------------------  
  
scorecardsdk/models.py  
Purpose:  
Define scorecard-specific objects.  
  
Key models:  
- FineClassingResult  
- CoarseClassingCandidate  
- BinningComparisonResult  
- WoeIvSummary  
- FeatureShortlistRecord  
- ScorecardModelCandidate  
- ScoreScalingResult  
- ScoreBandDefinition  
- ScorecardOutputBundle  
  
--------------------------------------------------  
scorecardsdk/fine_classing.py  
--------------------------------------------------  
Purpose:  
Create initial fine bins and supporting summaries.  
  
Responsibilities:  
- derive fine bins for variables  
- preserve variable-level bin metadata  
- compute basic counts and rates  
- produce artifacts for coarse classing stage  
  
Main functions:  
- build_fine_bins(...)  
- summarize_fine_bins(...)  
  
Depends on:  
- dataprepsdk  
- evaluation_sdk  
- artifactsdk  
  
--------------------------------------------------  
scorecardsdk/coarse_classing.py  
--------------------------------------------------  
Purpose:  
Create and validate coarse bin proposals.  
  
Responsibilities:  
- generate candidate merged bins  
- validate support and monotonicity  
- support preview recalculation after edits  
- persist final accepted bin definitions  
  
Main functions:  
- build_coarse_bin_candidate(...)  
- validate_coarse_bins(...)  
- preview_edited_bins(...)  
- finalize_coarse_bins(...)  
  
Depends on:  
- fine_classing.py  
- evaluation_sdk  
- artifactsdk  
- hitlsdk in runtime flow  
  
This module is central to the governed HITL workflow.  
  
--------------------------------------------------  
scorecardsdk/binning_compare.py  
--------------------------------------------------  
Purpose:  
Compare multiple binning candidates or packages.  
  
Responsibilities:  
- compare IV retention  
- compare support breaches  
- compare monotonicity quality  
- summarize candidate trade-offs  
  
Main functions:  
- compare_binning_candidates(...)  
- rank_binning_candidates(...)  
  
Depends on:  
- coarse_classing.py  
- evaluation_sdk  
  
--------------------------------------------------  
scorecardsdk/woe_iv.py  
--------------------------------------------------  
Purpose:  
Compute WoE and IV metrics and related summaries.  
  
Responsibilities:  
- calculate bin-level WoE  
- calculate variable IV  
- produce compact variable summaries  
- support later reporting and validation  
  
Main functions:  
- compute_woe_iv(...)  
- summarize_woe_iv(...)  
  
Depends on:  
- coarse_classing.py  
- evaluation_sdk  
  
--------------------------------------------------  
scorecardsdk/feature_shortlist.py  
--------------------------------------------------  
Purpose:  
Construct and finalize shortlist of scorecard features.  
  
Responsibilities:  
- use WoE/IV and additional filters  
- support variable inclusion/exclusion rationale  
- provide shortlist comparison and final selection support  
  
Main functions:  
- build_feature_shortlist(...)  
- compare_feature_shortlists(...)  
- finalize_feature_shortlist(...)  
  
Depends on:  
- woe_iv.py  
- evaluation_sdk  
- feature_sdk  
  
--------------------------------------------------  
scorecardsdk/logistic_models.py  
--------------------------------------------------  
Purpose:  
Build and compare scorecard logistic model candidates.  
  
Responsibilities:  
- fit model candidates  
- support standardized candidate metadata  
- calculate main metrics  
- package candidates for selection review  
  
Main functions:  
- fit_logistic_candidate(...)  
- fit_candidate_set(...)  
- summarize_model_candidate(...)  
  
Depends on:  
- feature_shortlist.py  
- evaluation_sdk  
- artifactsdk  
  
--------------------------------------------------  
scorecardsdk/score_scaling.py  
--------------------------------------------------  
Purpose:  
Convert odds/logit outputs into scorecard scale.  
  
Responsibilities:  
- support scaling parameters  
- map odds to score points  
- output scaling formula metadata  
- support governance-friendly summaries  
  
Main functions:  
- scale_scorecard(...)  
- summarize_scaling(...)  
  
Depends on:  
- logistic_models.py  
- reporting_sdk optionally for summaries  
  
--------------------------------------------------  
scorecardsdk/score_bands.py  
--------------------------------------------------  
Purpose:  
Define score bands and related cut structures.  
  
Responsibilities:  
- generate bands  
- summarize band population and bad rate  
- compare banding choices if needed  
  
Main functions:  
- build_score_bands(...)  
- summarize_score_bands(...)  
  
Depends on:  
- score_scaling.py  
- evaluation_sdk  
  
--------------------------------------------------  
scorecardsdk/scorecard_outputs.py  
--------------------------------------------------  
Purpose:  
Package scorecard outputs into final artifact bundle.  
  
Responsibilities:  
- collect binning artifacts  
- collect shortlist artifacts  
- collect model artifacts  
- collect scaling/band outputs  
- build final scorecard bundle  
  
Main functions:  
- build_scorecard_output_bundle(...)  
- write_scorecard_outputs(...)  
  
Depends on:  
- artifactsdk  
- reporting_sdk  
- workflowsdk  
  
--------------------------------------------------  
scorecardsdk/scorecard_monitoring_support.py  
--------------------------------------------------  
Purpose:  
Provide scorecard-specific monitoring support outputs.  
  
Responsibilities:  
- expose score distribution structures  
- expose band structures  
- expose drift-ready views  
- support monitoringsdk later  
  
Main functions:  
- build_scorecard_monitoring_payload(...)  
- build_band_monitoring_summary(...)  
  
Depends on:  
- score_bands.py  
- monitoringsdk later  
- artifactsdk  
  
--------------------------------------------------  
scorecardsdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Scorecard-specific exceptions.  
  
Examples:  
- FineClassingError  
- CoarseClassingValidationError  
- WoeComputationError  
- ScoreScalingError  
- ScoreBandError  
  
--------------------------------------------------------------------  
4.3 Public API for scorecardsdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
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
  
--------------------------------------------------------------------  
4.4 Implementation priorities for scorecardsdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. fine_classing.py  
3. coarse_classing.py  
4. woe_iv.py  
5. binning_compare.py  
6. feature_shortlist.py  
7. logistic_models.py  
8. score_scaling.py  
9. score_bands.py  
10. scorecard_outputs.py  
11. scorecard_monitoring_support.py  
  
====================================================================  
5. VALIDATION SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
5.1 Purpose  
--------------------------------------------------------------------  
validationsdk provides the governed validation workflow layer.  
  
It should:  
- define validation scope  
- classify and ingest evidence  
- manage findings  
- classify severity  
- assess model fitness  
- support validation conclusion  
- track remediation  
- create validation-specific outputs  
  
--------------------------------------------------------------------  
5.2 File-by-file design  
--------------------------------------------------------------------  
  
validationsdk/models.py  
Purpose:  
Define validation objects.  
  
Key models:  
- ValidationRun  
- ValidationScopeRecord  
- EvidenceItem  
- EvidenceCompletenessSummary  
- ValidationFinding  
- SeverityAssessment  
- FitnessDimensionResult  
- ValidationConclusionRecord  
- RemediationActionRecord  
- ValidationOutputBundle  
  
--------------------------------------------------  
validationsdk/validation_scope.py  
--------------------------------------------------  
Purpose:  
Initialize and define validation scope.  
  
Responsibilities:  
- define validation boundaries  
- required evidence classes  
- validation dimensions  
- validation run metadata  
  
Main functions:  
- create_validation_scope(...)  
- validate_scope_request(...)  
  
Depends on:  
- workflowsdk  
- policysdk  
- registry_sdk  
  
--------------------------------------------------  
validationsdk/evidence_intake.py  
--------------------------------------------------  
Purpose:  
Organize evidence for validation.  
  
Responsibilities:  
- ingest evidence refs  
- classify evidence by category  
- tag quality/completeness  
- attach to validation run  
  
Main functions:  
- intake_evidence(...)  
- classify_evidence(...)  
- summarize_evidence_inventory(...)  
  
Depends on:  
- artifactsdk  
- knowledge_sdk later  
- registry_sdk  
  
--------------------------------------------------  
validationsdk/fitness_framework.py  
--------------------------------------------------  
Purpose:  
Evaluate fit-for-use dimensions.  
  
Responsibilities:  
- conceptual soundness dimension  
- data adequacy dimension  
- calibration/performance dimension  
- implementation readiness dimension  
- controls/documentation dimension  
  
Main functions:  
- evaluate_fitness_dimensions(...)  
- summarize_fitness_framework(...)  
  
Depends on:  
- evidence_intake.py  
- evaluation_sdk  
- reporting_sdk  
  
--------------------------------------------------  
validationsdk/finding_registry.py  
--------------------------------------------------  
Purpose:  
Persist and manage validation findings.  
  
Responsibilities:  
- create findings  
- update status  
- attach evidence refs  
- attach owner and due date  
  
Main functions:  
- create_finding(...)  
- update_finding(...)  
- list_findings(...)  
- close_finding(...)  
  
Depends on:  
- registry_sdk  
- auditsdk  
- observabilitysdk  
  
--------------------------------------------------  
validationsdk/issue_severity.py  
--------------------------------------------------  
Purpose:  
Assign severity to findings.  
  
Responsibilities:  
- apply severity rules  
- use policy-aware severity logic  
- produce explainable severity result  
  
Main functions:  
- assess_severity(...)  
- summarize_severity_rationale(...)  
  
Depends on:  
- finding_registry.py  
- policysdk  
- evaluation_sdk  
  
--------------------------------------------------  
validationsdk/conclusion_engine.py  
--------------------------------------------------  
Purpose:  
Support structured validation conclusion options.  
  
Responsibilities:  
- map fitness and findings to conclusion categories  
- build condition lists  
- support final conclusion preparation  
  
Main functions:  
- build_conclusion_options(...)  
- finalize_conclusion(...)  
  
Depends on:  
- fitness_framework.py  
- finding_registry.py  
- policysdk  
- hitlsdk in runtime flow  
  
--------------------------------------------------  
validationsdk/remediation_tracker.py  
--------------------------------------------------  
Purpose:  
Track remediation actions linked to findings.  
  
Responsibilities:  
- create remediation actions  
- update due dates and owners  
- track closure evidence  
- expose remediation summary  
  
Main functions:  
- create_remediation_action(...)  
- update_remediation_status(...)  
- summarize_remediation(...)  
  
Depends on:  
- finding_registry.py  
- auditsdk  
- workflowsdk  
  
--------------------------------------------------  
validationsdk/validation_outputs.py  
--------------------------------------------------  
Purpose:  
Package validation artifacts and summaries.  
  
Responsibilities:  
- finding summary  
- evidence summary  
- fitness summary  
- conclusion outputs  
- remediation summary  
  
Main functions:  
- build_validation_output_bundle(...)  
- write_validation_outputs(...)  
  
Depends on:  
- artifactsdk  
- reporting_sdk  
  
--------------------------------------------------  
validationsdk/benchmark_compare.py  
--------------------------------------------------  
Purpose:  
Compare current validation context with benchmark patterns or prior  
validated cases.  
  
Responsibilities:  
- benchmark methodology concerns  
- benchmark severity patterns  
- benchmark conclusion patterns  
  
Main functions:  
- compare_validation_context_to_benchmark(...)  
- summarize_benchmark_deltas(...)  
  
Depends on:  
- knowledge_sdk  
- rag_sdk  
- evaluation_sdk  
  
--------------------------------------------------  
validationsdk/evidence_completeness.py  
--------------------------------------------------  
Purpose:  
Evaluate whether evidence is sufficient.  
  
Responsibilities:  
- compare supplied evidence to required evidence classes  
- detect stale or missing evidence  
- support evidence deficiency findings  
  
Main functions:  
- assess_evidence_completeness(...)  
- summarize_missing_evidence(...)  
  
Depends on:  
- validation_scope.py  
- evidence_intake.py  
- knowledge_sdk later  
  
--------------------------------------------------  
validationsdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Validation-specific exceptions.  
  
Examples:  
- ValidationScopeError  
- EvidenceIntakeError  
- FindingRegistryError  
- ConclusionEngineError  
  
--------------------------------------------------------------------  
5.3 Public API for validationsdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
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
  
--------------------------------------------------------------------  
5.4 Implementation priorities for validationsdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. validation_scope.py  
3. evidence_intake.py  
4. evidence_completeness.py  
5. finding_registry.py  
6. issue_severity.py  
7. fitness_framework.py  
8. conclusion_engine.py  
9. remediation_tracker.py  
10. validation_outputs.py  
11. benchmark_compare.py  
  
====================================================================  
6. REPORTING SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
6.1 Purpose  
--------------------------------------------------------------------  
reporting_sdk turns structured platform outputs into reporting-ready  
deliverables.  
  
It should:  
- generate technical sections  
- generate executive summaries  
- generate committee packs  
- generate validation notes  
- manage reusable narrative blocks  
- export chart/table artifacts  
- assemble packs  
  
--------------------------------------------------------------------  
6.2 File-by-file design  
--------------------------------------------------------------------  
  
reporting_sdk/models.py  
Purpose:  
Define reporting objects.  
  
Key models:  
- ReportSection  
- NarrativeBlock  
- TechnicalReportBundle  
- ExecutiveSummaryBundle  
- CommitteePackBundle  
- ValidationNoteBundle  
- ChartExportRecord  
- PackAssemblyResult  
  
--------------------------------------------------  
reporting_sdk/technical_report_builder.py  
--------------------------------------------------  
Purpose:  
Build technical model development or validation report sections.  
  
Responsibilities:  
- method section  
- data section  
- model section  
- diagnostics section  
- limitations section  
  
Main functions:  
- build_technical_report(...)  
- build_technical_section(...)  
  
Depends on:  
- narrative_blocks.py  
- artifactsdk  
- knowledge_sdk later  
  
--------------------------------------------------  
reporting_sdk/executive_summary_builder.py  
--------------------------------------------------  
Purpose:  
Build concise executive summary.  
  
Responsibilities:  
- summarize key decisions  
- summarize material findings  
- summarize risks and conditions  
- keep management-facing style  
  
Main functions:  
- build_executive_summary(...)  
- summarize_for_exec(...)  
  
Depends on:  
- narrative_blocks.py  
- auditsdk  
- reporting models  
  
--------------------------------------------------  
reporting_sdk/committee_pack_builder.py  
--------------------------------------------------  
Purpose:  
Build committee/governance-ready pack content.  
  
Responsibilities:  
- combine executive summary  
- include decision rationale  
- include conditions and escalation items  
- include linked visual summaries  
  
Main functions:  
- build_committee_pack(...)  
- build_committee_sections(...)  
  
Depends on:  
- executive_summary_builder.py  
- chart_table_export.py  
- flowvizsdk later  
  
--------------------------------------------------  
reporting_sdk/validation_note_builder.py  
--------------------------------------------------  
Purpose:  
Build validation-specific notes and memos.  
  
Responsibilities:  
- findings section  
- fitness summary section  
- conclusion section  
- remediation section  
  
Main functions:  
- build_validation_note(...)  
- build_finding_section(...)  
  
Depends on:  
- narrative_blocks.py  
- validationsdk  
- artifactsdk  
  
--------------------------------------------------  
reporting_sdk/narrative_blocks.py  
--------------------------------------------------  
Purpose:  
Manage reusable wording blocks and structured narrative snippets.  
  
Responsibilities:  
- approved wording  
- audience-tagged wording  
- domain-specific wording  
- validation wording  
- limitation wording  
  
Main functions:  
- get_narrative_block(...)  
- render_narrative_block(...)  
- register_narrative_block(...)  
  
Depends on:  
- config_sdk  
- registry_sdk  
- knowledge_sdk later  
  
This is one of the most important modules for consistency and token  
thrift.  
  
--------------------------------------------------  
reporting_sdk/chart_table_export.py  
--------------------------------------------------  
Purpose:  
Prepare chart and table references for reports.  
  
Responsibilities:  
- export linked chart refs  
- export table refs  
- summarize chart meaning  
- standardize chart/table metadata  
  
Main functions:  
- export_chart_refs(...)  
- export_table_refs(...)  
- summarize_visual_assets(...)  
  
Depends on:  
- artifactsdk  
  
--------------------------------------------------  
reporting_sdk/pack_assembler.py  
--------------------------------------------------  
Purpose:  
Assemble full reporting pack.  
  
Responsibilities:  
- combine sections  
- attach visuals  
- enforce pack order  
- emit final bundle  
  
Main functions:  
- assemble_pack(...)  
- validate_pack_structure(...)  
  
Depends on:  
- technical_report_builder.py  
- executive_summary_builder.py  
- committee_pack_builder.py  
- validation_note_builder.py  
  
--------------------------------------------------  
reporting_sdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Reporting-specific exceptions.  
  
Examples:  
- ReportBuildError  
- NarrativeBlockNotFoundError  
- PackAssemblyError  
  
--------------------------------------------------------------------  
6.3 Public API for reporting_sdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
- build_technical_report(...)  
- build_executive_summary(...)  
- build_committee_pack(...)  
- build_validation_note(...)  
- get_narrative_block(...)  
- export_chart_refs(...)  
- export_table_refs(...)  
- assemble_pack(...)  
  
--------------------------------------------------------------------  
6.4 Implementation priorities for reporting_sdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. narrative_blocks.py  
3. technical_report_builder.py  
4. executive_summary_builder.py  
5. validation_note_builder.py  
6. chart_table_export.py  
7. committee_pack_builder.py  
8. pack_assembler.py  
  
====================================================================  
7. CONTROLLER LAYER EXPANSION FOR WAVE 4  
====================================================================  
  
platform_core/controllers/scorecard_controller.py  
Purpose:  
Coordinate scorecard-specific workflow steps.  
  
Responsibilities:  
- run fine classing  
- open coarse classing review  
- compare binning versions  
- shortlist variables  
- fit scorecard models  
- finalize model  
- trigger scaling review  
  
Main methods:  
- run_fine_classing(...)  
- open_coarse_classing_review(...)  
- compare_binning_versions(...)  
- finalize_feature_shortlist(...)  
- fit_scorecard_candidates(...)  
- finalize_model_selection(...)  
- run_score_scaling(...)  
  
--------------------------------------------------  
platform_core/controllers/validation_controller.py  
--------------------------------------------------  
Purpose:  
Coordinate validation workflow steps.  
  
Responsibilities:  
- create validation scope  
- intake evidence  
- open methodology review  
- open data validation review  
- build fitness summary  
- finalize conclusion  
- trigger remediation  
  
Main methods:  
- create_validation_run(...)  
- intake_validation_evidence(...)  
- open_validation_review(...)  
- finalize_validation_conclusion(...)  
- open_remediation_action(...)  
  
--------------------------------------------------  
platform_core/controllers/reporting_controller.py  
--------------------------------------------------  
Purpose:  
Coordinate technical, committee, and validation reporting outputs.  
  
Responsibilities:  
- build technical pack  
- build executive summary  
- build validation note  
- assemble governance pack  
  
Main methods:  
- build_technical_pack(...)  
- build_validation_pack(...)  
- build_committee_pack(...)  
- assemble_reporting_bundle(...)  
  
====================================================================  
8. AGENT BRIDGE EXPANSION FOR WAVE 4  
====================================================================  
  
platform_core/bridges/agent_bridge/scorecard_context_builder.py  
Purpose:  
Build compact scorecard context for developer-agent and validator-agent.  
  
Responsibilities:  
- selected dataset refs  
- active candidate refs  
- binning summary  
- key metrics  
- selected feature list  
- score scaling summary  
  
--------------------------------------------------  
platform_core/bridges/agent_bridge/validation_context_builder.py  
--------------------------------------------------  
Purpose:  
Build compact validation context.  
  
Responsibilities:  
- validation scope summary  
- evidence completeness summary  
- open findings  
- fitness dimensions  
- draft conclusion options  
  
--------------------------------------------------  
platform_core/bridges/agent_bridge/reporting_context_builder.py  
--------------------------------------------------  
Purpose:  
Build compact reporting context.  
  
Responsibilities:  
- template refs  
- approved wording refs  
- key decisions  
- findings  
- artifact summary refs  
  
--------------------------------------------------  
platform_core/bridges/agent_bridge/scorecard_response_normalizer.py  
--------------------------------------------------  
Purpose:  
Normalize scorecard outputs into standard response envelope.  
  
--------------------------------------------------  
platform_core/bridges/agent_bridge/validation_response_normalizer.py  
--------------------------------------------------  
Purpose:  
Normalize validation outputs into standard response envelope.  
  
--------------------------------------------------  
platform_core/bridges/agent_bridge/reporting_response_normalizer.py  
--------------------------------------------------  
Purpose:  
Normalize reporting outputs into standard response envelope.  
  
====================================================================  
9. WAVE 4 END-TO-END WORKFLOW DESIGN  
====================================================================  
  
--------------------------------------------------------------------  
9.1 Scorecard build flow  
--------------------------------------------------------------------  
1. dataprepsdk produces prepared dataset  
2. scorecard_controller runs fine classing  
3. review_controller opens coarse classing review  
4. user finalizes bins  
5. scorecard_controller computes WoE/IV  
6. feature shortlist review opens  
7. shortlist finalized  
8. logistic model candidates fitted  
9. model comparison review opens  
10. model selected  
11. scaling and band review opens  
12. final scorecard bundle written  
  
--------------------------------------------------------------------  
9.2 Validation flow  
--------------------------------------------------------------------  
1. validation_controller creates validation scope  
2. evidence intake and completeness review  
3. methodology review  
4. data validation review  
5. model fitness review  
6. validator finalizes conclusion  
7. validation outputs written  
8. remediation created if needed  
  
--------------------------------------------------------------------  
9.3 Reporting flow  
--------------------------------------------------------------------  
1. reporting_controller gathers artifact refs  
2. technical report sections built  
3. validation note built  
4. executive summary built  
5. committee pack built  
6. pack assembler combines outputs  
7. reporting artifacts written  
  
====================================================================  
10. UI / REVIEW WORKSPACE IMPLICATIONS  
====================================================================  
  
Wave 4 should reuse the generic Wave 2 review shell.  
  
New review types to fully support:  
- coarse_classing  
- binning_version_selection  
- feature_shortlist_review  
- model_selection  
- scaling_and_calibration_review  
- validation_scope_definition  
- methodology_review  
- data_validation_review  
- model_fitness_review  
- validation_conclusion  
  
Scorecard-specific widgets are not required yet.  
Use generic widgets with scorecard-aware payloads first.  
  
====================================================================  
11. TEST BLUEPRINT FOR WAVE 4  
====================================================================  
  
tests/unit/scorecardsdk/test_fine_classing.py  
- fine bin generation  
- bin metadata integrity  
  
tests/unit/scorecardsdk/test_coarse_classing.py  
- candidate generation  
- support checks  
- monotonicity checks  
  
tests/unit/scorecardsdk/test_woe_iv.py  
- WoE and IV calculations  
  
tests/unit/scorecardsdk/test_feature_shortlist.py  
- shortlist construction and selection  
  
tests/unit/scorecardsdk/test_logistic_models.py  
- candidate fit output structure  
  
tests/unit/scorecardsdk/test_score_scaling.py  
- scaling correctness and metadata  
  
tests/unit/scorecardsdk/test_score_bands.py  
- band creation and summaries  
  
tests/unit/validationsdk/test_validation_scope.py  
- scope initialization  
  
tests/unit/validationsdk/test_evidence_intake.py  
- evidence classification  
  
tests/unit/validationsdk/test_evidence_completeness.py  
- missing evidence detection  
  
tests/unit/validationsdk/test_finding_registry.py  
- finding CRUD and lifecycle  
  
tests/unit/validationsdk/test_issue_severity.py  
- severity mapping  
  
tests/unit/validationsdk/test_fitness_framework.py  
- fitness dimension summaries  
  
tests/unit/validationsdk/test_conclusion_engine.py  
- conclusion option generation  
- condition list generation  
  
tests/unit/validationsdk/test_remediation_tracker.py  
- remediation lifecycle  
  
tests/unit/reporting_sdk/test_narrative_blocks.py  
- approved wording lookup  
- fallback behavior  
  
tests/unit/reporting_sdk/test_technical_report_builder.py  
- section generation  
  
tests/unit/reporting_sdk/test_validation_note_builder.py  
- validation note output structure  
  
tests/unit/reporting_sdk/test_pack_assembler.py  
- pack assembly structure  
  
tests/integration/test_scorecard_binning_flow.py  
- fine classing -> coarse classing review -> finalize  
  
tests/integration/test_scorecard_model_selection_flow.py  
- shortlist -> fit candidates -> select model -> scale  
  
tests/integration/test_validation_finding_flow.py  
- evidence intake -> finding creation -> severity  
  
tests/integration/test_validation_conclusion_flow.py  
- fitness review -> conclusion -> output bundle  
  
tests/integration/test_reporting_pack_flow.py  
- technical + validation + executive -> assembled pack  
  
====================================================================  
12. NOTEBOOK PLAYBOOKS FOR WAVE 4  
====================================================================  
  
notebooks/scorecard_playbook.ipynb  
- build fine bins  
- preview coarse bin candidates  
- compute WoE/IV  
- fit simple scorecard candidates  
  
notebooks/validation_playbook.ipynb  
- create validation scope  
- intake evidence  
- create findings  
- generate conclusion options  
  
notebooks/reporting_playbook.ipynb  
- build technical section  
- build validation note  
- build executive summary  
- assemble pack  
  
notebooks/end_to_end_scorecard_validation_playbook.ipynb  
- run full demo from prepared dataset to validation output  
  
====================================================================  
13. BUILD ORDER FOR WAVE 4  
====================================================================  
  
Phase 4A – reporting base  
-------------------------  
1. reporting_sdk/models.py  
2. reporting_sdk/narrative_blocks.py  
3. reporting_sdk/technical_report_builder.py  
4. reporting_sdk/executive_summary_builder.py  
  
Phase 4B – validation base  
--------------------------  
5. validationsdk/models.py  
6. validationsdk/validation_scope.py  
7. validationsdk/evidence_intake.py  
8. validationsdk/evidence_completeness.py  
9. validationsdk/finding_registry.py  
10. validationsdk/issue_severity.py  
  
Phase 4C – scorecard binning core  
---------------------------------  
11. scorecardsdk/models.py  
12. scorecardsdk/fine_classing.py  
13. scorecardsdk/coarse_classing.py  
14. scorecardsdk/woe_iv.py  
15. scorecardsdk/binning_compare.py  
  
Phase 4D – scorecard model core  
-------------------------------  
16. scorecardsdk/feature_shortlist.py  
17. scorecardsdk/logistic_models.py  
18. scorecardsdk/score_scaling.py  
19. scorecardsdk/score_bands.py  
20. scorecardsdk/scorecard_outputs.py  
  
Phase 4E – validation conclusion and reporting expansion  
--------------------------------------------------------  
21. validationsdk/fitness_framework.py  
22. validationsdk/conclusion_engine.py  
23. validationsdk/remediation_tracker.py  
24. validationsdk/validation_outputs.py  
25. validationsdk/benchmark_compare.py  
26. reporting_sdk/validation_note_builder.py  
27. reporting_sdk/chart_table_export.py  
28. reporting_sdk/committee_pack_builder.py  
29. reporting_sdk/pack_assembler.py  
  
Phase 4F – controllers and bridge support  
-----------------------------------------  
30. platform_core/controllers/scorecard_controller.py  
31. platform_core/controllers/validation_controller.py  
32. platform_core/controllers/reporting_controller.py  
33. platform_core/bridges/agent_bridge/scorecard_context_builder.py  
34. platform_core/bridges/agent_bridge/validation_context_builder.py  
35. platform_core/bridges/agent_bridge/reporting_context_builder.py  
36. platform_core/bridges/agent_bridge/scorecard_response_normalizer.py  
37. platform_core/bridges/agent_bridge/validation_response_normalizer.py  
38. platform_core/bridges/agent_bridge/reporting_response_normalizer.py  
  
Phase 4G – monitoring support hook  
----------------------------------  
39. scorecardsdk/scorecard_monitoring_support.py  
  
====================================================================  
14. WAVE 4 MINIMUM VIABLE DEMOS  
====================================================================  
  
Demo 1: Coarse Classing Workflow  
- fine bin generation  
- coarse classing review  
- preview and finalize bins  
  
Demo 2: Binning Version Selection  
- compare multiple binning candidates  
- select final version  
- record selection  
  
Demo 3: Scorecard Model Selection  
- fit candidate models  
- compare metrics  
- select final candidate  
- scale score  
  
Demo 4: Validation Conclusion Workflow  
- create validation run  
- intake evidence  
- record findings  
- assess fitness  
- finalize conclusion  
  
Demo 5: Reporting Pack  
- technical summary  
- validation note  
- executive summary  
- assembled pack  
  
====================================================================  
15. WHAT WAVE 4 SHOULD NOT DO  
====================================================================  
  
Wave 4 should not:  
- over-customize UI for scorecards beyond generic review shell  
- implement all advanced scorecard methods at once  
- mix validation logic into scorecardsdk  
- let reporting builder become a raw string-concatenation engine  
- allow validation conclusions without explicit human validator action  
- turn narrative generation into the source of truth  
  
The source of truth must remain:  
- artifacts  
- registries  
- workflow state  
- validation records  
- audit records  
  
====================================================================  
16. DELIVERABLE CHECKLIST FOR WAVE 4  
====================================================================  
  
Wave 4 is complete when all of the following exist:  
  
- scorecardsdk with binning, WoE/IV, shortlist, candidate fit, scaling  
- validationsdk with findings, fitness, conclusion, remediation  
- reporting_sdk with technical, validation, executive, and committee  
  outputs  
- scorecard_controller, validation_controller, reporting_controller  
- end-to-end scorecard demo with governed reviews  
- end-to-end validation conclusion demo  
- assembled reporting pack demo  
- standardized response envelopes and artifact outputs throughout  
  
====================================================================  
17. FINAL RECOMMENDATION  
====================================================================  
  
Wave 4 is where the platform becomes truly persuasive to stakeholders.  
  
To make it strong:  
- keep scorecardsdk domain-focused  
- keep validationsdk independent and challenge-oriented  
- keep reporting_sdk structured and reusable  
- keep all major decisions governed through HITL and audit  
- reuse the generic workspace pattern from Wave 2  
  
That will give you the first complete showcase workflow for your  
agentic AI model lifecycle platform.  
  
====================================================================  
END OF WAVE 4 IMPLEMENTATION BLUEPRINT  
====================================================================  
  
====================================================================  
WAVE 5 IMPLEMENTATION BLUEPRINT  
KNOWLEDGE SDK + RAG SDK + FLOWVIZSDK + MONITORINGSDK  
GROWING KNOWLEDGE, TOKEN-THRIFTY RETRIEVAL, FLOW VISIBILITY,  
AND POST-VALIDATION MONITORING  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This document continues the implementation blueprint with Wave 5.  
  
Wave 5 focuses on institutional memory, token-thrifty retrieval,  
workflow visualization, and post-validation monitoring. It adds:  
  
1. knowledge_sdk  
2. rag_sdk  
3. flowvizsdk  
4. monitoringsdk  
  
Wave 5 is the point where the platform becomes able to:  
- accumulate reusable knowledge across projects  
- retrieve compact, relevant context for agents  
- visualize workflow, review, and decision flows  
- ingest monitoring snapshots and refresh monitoring dashboards  
- support monitoring breach reviews and annual review flows  
- write back learning and decisions into governed knowledge objects  
  
This wave turns the platform from a governed execution system into a  
growing agentic ecosystem with memory and operational continuity.  
  
====================================================================  
1. WAVE 5 SCOPE  
====================================================================  
  
Wave 5 includes:  
  
A. knowledge_sdk  
- governed knowledge object model  
- knowledge registry  
- promotion workflow  
- quality and status management  
- knowledge linkage to artifacts/findings/decisions  
- knowledge export  
  
B. rag_sdk  
- chunking  
- embeddings orchestration  
- semantic retrieval  
- reranking  
- query routing  
- context compression  
- prompt packaging  
- token budget management  
  
C. flowvizsdk  
- flow node building  
- flow edge building  
- timeline building  
- filtered flow views  
- drill-down routing  
- graph export  
  
D. monitoringsdk  
- monitoring template registry  
- snapshot ingestion and validation  
- metric generation  
- threshold and breach evaluation  
- trend and drift views  
- dashboard payload generation  
- annual review pack generation  
- monitoring notes and actions  
  
====================================================================  
2. TARGET OUTCOME OF WAVE 5  
====================================================================  
  
After Wave 5, the platform should be able to support flows such as:  
  
1. user finalizes a validation conclusion  
2. knowledge_sdk captures conclusion summary as project knowledge  
3. rag_sdk later retrieves similar prior conclusions for new projects  
4. flowvizsdk shows the workflow path, review decisions, and sign-offs  
5. monitoringsdk ingests monthly production snapshot  
6. monitoring-agent summarizes breaches and recommends action  
7. annual review pack is generated from monitoring history  
8. reusable lessons are promoted from project scope to domain scope  
9. the whole system remains token-thrifty through compact retrieval  
  
This is the first wave where the platform meaningfully “learns” across  
projects while keeping governance boundaries.  
  
====================================================================  
3. UPDATED REPOSITORY STRUCTURE FOR WAVE 5  
====================================================================  
  
project_root/  
  src/  
    knowledge_sdk/  
      __init__.py  
      models.py  
      knowledge_object.py  
      knowledge_registry.py  
      promotion_manager.py  
      quality_manager.py  
      status_manager.py  
      knowledge_linker.py  
      knowledge_export.py  
      scope_classifier.py  
      lifecycle_service.py  
      exceptions.py  
  
    rag_sdk/  
      __init__.py  
      models.py  
      chunker.py  
      embedder.py  
      retriever.py  
      reranker.py  
      query_router.py  
      context_compressor.py  
      prompt_packager.py  
      token_budget_manager.py  
      retrieval_filters.py  
      cache_manager.py  
      exceptions.py  
  
    flowvizsdk/  
      __init__.py  
      models.py  
      node_builder.py  
      edge_builder.py  
      flow_summary.py  
      timeline_builder.py  
      graph_export.py  
      detail_linker.py  
      flow_filters.py  
      drilldown_router.py  
      exceptions.py  
  
    monitoringsdk/  
      __init__.py  
      models.py  
      monitoring_template_registry.py  
      snapshot_ingestor.py  
      snapshot_validator.py  
      monitoring_history_manager.py  
      metric_engine.py  
      threshold_engine.py  
      drift_engine.py  
      performance_monitor.py  
      segment_monitor.py  
      baseline_comparator.py  
      dashboard_payload_builder.py  
      dashboard_config_builder.py  
      monitoring_note_manager.py  
      annual_review_pack_builder.py  
      monitoring_manifest_builder.py  
      monitoring_output_writer.py  
      exceptions.py  
  
    platform_core/  
      controllers/  
        knowledge_controller.py  
        retrieval_controller.py  
        flow_controller.py  
        monitoring_controller.py  
      runtime/  
        retrieval_mode_resolver.py  
        monitoring_stage_resolver.py  
      bridges/  
        agent_bridge/  
          knowledge_context_builder.py  
          rag_context_builder.py  
          monitoring_context_builder.py  
          flow_context_builder.py  
          retrieval_response_normalizer.py  
          monitoring_response_normalizer.py  
        jupyter_bridge/  
          dashboard_workspace_builder.py  
          flow_workspace_builder.py  
          monitoring_workspace_sync.py  
  
  tests/  
    unit/  
      knowledge_sdk/  
      rag_sdk/  
      flowvizsdk/  
      monitoringsdk/  
    integration/  
      test_knowledge_capture_flow.py  
      test_rag_retrieval_flow.py  
      test_flowviz_generation_flow.py  
      test_monitoring_snapshot_flow.py  
      test_monitoring_breach_review_flow.py  
      test_annual_review_pack_flow.py  
  
  notebooks/  
    knowledge_playbook.ipynb  
    rag_playbook.ipynb  
    flowviz_playbook.ipynb  
    monitoring_playbook.ipynb  
    annual_review_playbook.ipynb  
  
====================================================================  
4. KNOWLEDGE SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
4.1 Purpose  
--------------------------------------------------------------------  
knowledge_sdk is the governed knowledge lifecycle layer.  
  
It should:  
- define a standard knowledge object model  
- register and store knowledge objects  
- classify scope and reusability  
- manage promotion from project to domain/global  
- manage quality and lifecycle states  
- link knowledge back to source decisions, artifacts, findings, and  
  conclusions  
- export reusable knowledge packages  
  
It is not the retrieval engine. It owns the knowledge itself.  
  
--------------------------------------------------------------------  
4.2 File-by-file design  
--------------------------------------------------------------------  
  
knowledge_sdk/models.py  
Purpose:  
Define knowledge-related objects.  
  
Key models:  
- KnowledgeObject  
- KnowledgeRegistryRecord  
- KnowledgeScopeRecord  
- PromotionRequest  
- QualityReviewRecord  
- KnowledgeLifecycleStatus  
- KnowledgeExportBundle  
  
--------------------------------------------------  
knowledge_sdk/knowledge_object.py  
--------------------------------------------------  
Purpose:  
Create and validate canonical knowledge objects.  
  
Responsibilities:  
- object schema creation  
- support knowledge types  
- support short and detailed summaries  
- support source refs and tags  
  
Main functions:  
- create_knowledge_object(...)  
- validate_knowledge_object(...)  
  
--------------------------------------------------  
knowledge_sdk/knowledge_registry.py  
--------------------------------------------------  
Purpose:  
Persist and retrieve knowledge metadata and links.  
  
Responsibilities:  
- register knowledge object  
- get knowledge by ID  
- search by scope/type/domain/project  
- update metadata  
  
Main functions:  
- register_knowledge(...)  
- get_knowledge(...)  
- search_knowledge(...)  
- update_knowledge(...)  
  
Depends on:  
- registry_sdk  
- artifactsdk  
  
--------------------------------------------------  
knowledge_sdk/promotion_manager.py  
--------------------------------------------------  
Purpose:  
Promote knowledge upward in scope.  
  
Responsibilities:  
- move project knowledge to domain/global reuse  
- enforce approval requirement for promotion  
- track promotion history  
  
Main functions:  
- request_promotion(...)  
- approve_promotion(...)  
- promote_knowledge(...)  
  
Depends on:  
- knowledge_registry.py  
- quality_manager.py  
- auditsdk  
  
--------------------------------------------------  
knowledge_sdk/quality_manager.py  
--------------------------------------------------  
Purpose:  
Manage quality states and reuse approval.  
  
Responsibilities:  
- set draft/reviewed/approved/superseded  
- capture reviewer and quality notes  
- determine if knowledge is eligible for promotion  
  
Main functions:  
- set_quality_status(...)  
- assess_reuse_eligibility(...)  
- mark_superseded(...)  
  
Depends on:  
- knowledge_registry.py  
- auditsdk  
  
--------------------------------------------------  
knowledge_sdk/status_manager.py  
--------------------------------------------------  
Purpose:  
Manage lifecycle status.  
  
Responsibilities:  
- active  
- archived  
- superseded  
- hidden from default retrieval  
  
Main functions:  
- set_lifecycle_status(...)  
- is_retrievable(...)  
  
Depends on:  
- knowledge_registry.py  
  
--------------------------------------------------  
knowledge_sdk/knowledge_linker.py  
--------------------------------------------------  
Purpose:  
Link knowledge to source objects.  
  
Responsibilities:  
- attach artifact refs  
- attach decision refs  
- attach finding refs  
- attach conclusion refs  
- attach workflow refs  
  
Main functions:  
- link_knowledge_to_artifact(...)  
- link_knowledge_to_decision(...)  
- link_knowledge_to_finding(...)  
  
Depends on:  
- artifactsdk  
- auditsdk  
- validationsdk  
- workflowsdk  
  
--------------------------------------------------  
knowledge_sdk/knowledge_export.py  
--------------------------------------------------  
Purpose:  
Export governed knowledge packages.  
  
Responsibilities:  
- export by scope  
- export by domain  
- export by approved reusable set  
- produce metadata-rich export bundles  
  
Main functions:  
- export_knowledge_bundle(...)  
- export_domain_reusable_knowledge(...)  
  
Depends on:  
- knowledge_registry.py  
- promotion_manager.py  
  
--------------------------------------------------  
knowledge_sdk/scope_classifier.py  
--------------------------------------------------  
Purpose:  
Classify scope and reuse class.  
  
Responsibilities:  
- session_only  
- project_only  
- domain_reusable  
- global_reusable  
- assist event-driven capture  
  
Main functions:  
- classify_scope(...)  
- suggest_promotion_scope(...)  
  
Depends on:  
- config_sdk  
- knowledge_object.py  
  
--------------------------------------------------  
knowledge_sdk/lifecycle_service.py  
--------------------------------------------------  
Purpose:  
High-level service to create/update/promote knowledge from workflow  
events.  
  
Responsibilities:  
- event-driven capture  
- summary registration  
- quality state initialization  
- export compatibility  
  
Main functions:  
- capture_from_event(...)  
- capture_from_review(...)  
- capture_from_decision(...)  
- capture_from_validation_conclusion(...)  
  
Depends on:  
- knowledge_registry.py  
- knowledge_linker.py  
- scope_classifier.py  
- observabilitysdk  
  
--------------------------------------------------  
knowledge_sdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Knowledge-specific exceptions.  
  
Examples:  
- KnowledgeNotFoundError  
- InvalidKnowledgeScopeError  
- PromotionDeniedError  
- QualityStateError  
  
--------------------------------------------------------------------  
4.3 Public API for knowledge_sdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
- create_knowledge_object(...)  
- register_knowledge(...)  
- search_knowledge(...)  
- capture_from_event(...)  
- capture_from_decision(...)  
- set_quality_status(...)  
- promote_knowledge(...)  
- export_knowledge_bundle(...)  
  
--------------------------------------------------------------------  
4.4 Implementation priorities for knowledge_sdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. knowledge_object.py  
3. knowledge_registry.py  
4. scope_classifier.py  
5. status_manager.py  
6. quality_manager.py  
7. knowledge_linker.py  
8. lifecycle_service.py  
9. promotion_manager.py  
10. knowledge_export.py  
  
====================================================================  
5. RAG SDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
5.1 Purpose  
--------------------------------------------------------------------  
rag_sdk is the retrieval and prompt-grounding layer.  
  
It should:  
- chunk source text or summaries  
- generate and manage embedding requests  
- retrieve relevant semantic context  
- rerank results  
- route retrieval strategies by role/domain/stage  
- compress context for token thrift  
- package prompt-ready context  
- enforce token budgets  
  
It does not own the knowledge lifecycle. It retrieves from governed  
knowledge and related indexed sources.  
  
--------------------------------------------------------------------  
5.2 File-by-file design  
--------------------------------------------------------------------  
  
rag_sdk/models.py  
Purpose:  
Define retrieval-related objects.  
  
Key models:  
- ChunkRecord  
- RetrievalQuery  
- RetrievalResult  
- RerankResult  
- ContextPack  
- TokenBudgetProfile  
- PromptPackage  
  
--------------------------------------------------  
rag_sdk/chunker.py  
--------------------------------------------------  
Purpose:  
Split text into retrievable chunks.  
  
Responsibilities:  
- chunk by length  
- chunk by semantic boundaries  
- support summary-first chunking  
- avoid duplicate overlap bloat  
  
Main functions:  
- chunk_text(...)  
- chunk_document(...)  
- chunk_summary(...)  
  
--------------------------------------------------  
rag_sdk/embedder.py  
--------------------------------------------------  
Purpose:  
Orchestrate embedding generation.  
  
Responsibilities:  
- request embeddings  
- attach embeddings to chunk refs  
- store embedding metadata  
- support batched embedding workflows  
  
Main functions:  
- embed_chunks(...)  
- embed_texts(...)  
  
Depends on:  
- chunker.py  
- config_sdk  
  
--------------------------------------------------  
rag_sdk/retriever.py  
--------------------------------------------------  
Purpose:  
Perform semantic retrieval.  
  
Responsibilities:  
- search indexed chunk sets  
- filter by scope/domain/project/type  
- retrieve top candidates  
  
Main functions:  
- retrieve(...)  
- retrieve_by_scope(...)  
- retrieve_by_project(...)  
  
Depends on:  
- embedder.py  
- retrieval_filters.py  
- knowledge_sdk  
  
--------------------------------------------------  
rag_sdk/reranker.py  
--------------------------------------------------  
Purpose:  
Improve relevance ordering.  
  
Responsibilities:  
- rerank retrieved chunks  
- remove weak or duplicate chunks  
- prioritize compact summaries  
  
Main functions:  
- rerank_results(...)  
- deduplicate_results(...)  
  
Depends on:  
- retriever.py  
  
--------------------------------------------------  
rag_sdk/query_router.py  
--------------------------------------------------  
Purpose:  
Choose retrieval strategy based on runtime context.  
  
Responsibilities:  
- choose filters by role/domain/stage  
- choose top-k profile  
- choose summary-vs-detail retrieval depth  
  
Main functions:  
- route_query(...)  
- build_retrieval_plan(...)  
  
Depends on:  
- runtime context  
- config_sdk  
- registry_sdk  
  
--------------------------------------------------  
rag_sdk/context_compressor.py  
--------------------------------------------------  
Purpose:  
Compress retrieved context into compact summaries.  
  
Responsibilities:  
- merge duplicate ideas  
- keep exact refs  
- prefer short summaries first  
- preserve key facts only  
  
Main functions:  
- compress_context(...)  
- compress_results_to_summary(...)  
  
Depends on:  
- reranker.py  
  
--------------------------------------------------  
rag_sdk/prompt_packager.py  
--------------------------------------------------  
Purpose:  
Build prompt-ready retrieval packs.  
  
Responsibilities:  
- exact facts section  
- top summaries section  
- optional detailed section  
- source refs section  
  
Main functions:  
- build_context_pack(...)  
- build_prompt_package(...)  
  
Depends on:  
- context_compressor.py  
- registry_sdk  
  
--------------------------------------------------  
rag_sdk/token_budget_manager.py  
--------------------------------------------------  
Purpose:  
Enforce token-thrifty retrieval budgets.  
  
Responsibilities:  
- micro_mode  
- standard_mode  
- deep_review_mode  
- cap retrieval size  
- cap context package size  
  
Main functions:  
- get_budget_profile(...)  
- apply_budget(...)  
- estimate_context_size(...)  
  
Depends on:  
- config_sdk  
- prompt_packager.py  
  
--------------------------------------------------  
rag_sdk/retrieval_filters.py  
--------------------------------------------------  
Purpose:  
Apply structured retrieval filters.  
  
Responsibilities:  
- filter superseded knowledge  
- filter stale knowledge  
- filter by scope/domain/project/stage/type  
  
Main functions:  
- filter_results(...)  
- build_filter_spec(...)  
  
Depends on:  
- knowledge_sdk  
- registry_sdk  
  
--------------------------------------------------  
rag_sdk/cache_manager.py  
--------------------------------------------------  
Purpose:  
Cache reusable retrieval packs.  
  
Responsibilities:  
- reuse prior retrieval pack in same run/stage  
- invalidate on stage or state change  
  
Main functions:  
- get_cached_context(...)  
- cache_context(...)  
- invalidate_cache(...)  
  
Depends on:  
- token_budget_manager.py  
- registry_sdk  
  
--------------------------------------------------  
rag_sdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Retrieval-specific exceptions.  
  
Examples:  
- RetrievalPlanError  
- ChunkingError  
- EmbeddingError  
- BudgetExceededError  
  
--------------------------------------------------------------------  
5.3 Public API for rag_sdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
- chunk_document(...)  
- embed_chunks(...)  
- retrieve(...)  
- route_query(...)  
- rerank_results(...)  
- compress_context(...)  
- build_context_pack(...)  
- get_budget_profile(...)  
  
--------------------------------------------------------------------  
5.4 Implementation priorities for rag_sdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. chunker.py  
3. retrieval_filters.py  
4. query_router.py  
5. retriever.py  
6. reranker.py  
7. context_compressor.py  
8. prompt_packager.py  
9. token_budget_manager.py  
10. cache_manager.py  
11. embedder.py  
  
Note:  
If embeddings infrastructure is not ready, early builds can stub or  
abstract embedder while keeping the rest of the contract stable.  
  
====================================================================  
6. FLOWVIZSDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
6.1 Purpose  
--------------------------------------------------------------------  
flowvizsdk is the workflow visualization layer.  
  
It should:  
- build flow nodes and edges from event history and state records  
- build timeline views  
- summarize workflow paths  
- support filtered graph views  
- link graph elements to details  
- export graph payloads for Jupyter and reports  
  
--------------------------------------------------------------------  
6.2 File-by-file design  
--------------------------------------------------------------------  
  
flowvizsdk/models.py  
Purpose:  
Define visualization graph objects.  
  
Key models:  
- FlowNode  
- FlowEdge  
- FlowGraph  
- TimelineEvent  
- FlowSummary  
- DrilldownPayload  
- GraphExportBundle  
  
--------------------------------------------------  
flowvizsdk/node_builder.py  
--------------------------------------------------  
Purpose:  
Create nodes from workflow objects.  
  
Responsibilities:  
- stage nodes  
- review nodes  
- decision nodes  
- finding nodes  
- artifact milestone nodes  
  
Main functions:  
- build_nodes(...)  
- build_stage_nodes(...)  
- build_review_nodes(...)  
  
Depends on:  
- observabilitysdk  
- workflowsdk  
- auditsdk  
  
--------------------------------------------------  
flowvizsdk/edge_builder.py  
--------------------------------------------------  
Purpose:  
Connect nodes with directed edges.  
  
Responsibilities:  
- stage transitions  
- review dependencies  
- escalation links  
- artifact production links  
  
Main functions:  
- build_edges(...)  
- build_transition_edges(...)  
- build_dependency_edges(...)  
  
Depends on:  
- node_builder.py  
- observabilitysdk  
- workflowsdk  
  
--------------------------------------------------  
flowvizsdk/flow_summary.py  
--------------------------------------------------  
Purpose:  
Create compact workflow narrative summaries.  
  
Responsibilities:  
- summarize path  
- summarize decisions  
- summarize major branch points  
- summarize unresolved items  
  
Main functions:  
- summarize_flow(...)  
- summarize_branching(...)  
  
Depends on:  
- node_builder.py  
- edge_builder.py  
- reporting_sdk optionally  
  
--------------------------------------------------  
flowvizsdk/timeline_builder.py  
--------------------------------------------------  
Purpose:  
Build chronological event/timeline views.  
  
Responsibilities:  
- order by event timestamp  
- group by stage/review  
- tag major decisions and escalations  
  
Main functions:  
- build_timeline(...)  
- summarize_timeline(...)  
  
Depends on:  
- observabilitysdk  
  
--------------------------------------------------  
flowvizsdk/graph_export.py  
--------------------------------------------------  
Purpose:  
Export graph payloads for UI or reporting.  
  
Responsibilities:  
- export as JSON-like graph structure  
- export filtered graph subsets  
- export graph + summary package  
  
Main functions:  
- export_graph(...)  
- export_flow_bundle(...)  
  
Depends on:  
- node_builder.py  
- edge_builder.py  
- flow_summary.py  
  
--------------------------------------------------  
flowvizsdk/detail_linker.py  
--------------------------------------------------  
Purpose:  
Attach details to graph elements.  
  
Responsibilities:  
- link node to artifact refs  
- link node to review details  
- link node to audit refs  
  
Main functions:  
- link_node_details(...)  
- build_drilldown_payload(...)  
  
Depends on:  
- artifactsdk  
- auditsdk  
- hitlsdk  
- validationsdk  
  
--------------------------------------------------  
flowvizsdk/flow_filters.py  
--------------------------------------------------  
Purpose:  
Filter graph views.  
  
Responsibilities:  
- by role  
- by stage  
- by date range  
- by branch  
- by unresolved status  
  
Main functions:  
- filter_graph(...)  
- build_filtered_view(...)  
  
Depends on:  
- graph_export.py  
  
--------------------------------------------------  
flowvizsdk/drilldown_router.py  
--------------------------------------------------  
Purpose:  
Route UI drill-down interactions.  
  
Responsibilities:  
- route node click to detail payload  
- choose detail panel content  
- keep graph-to-detail navigation consistent  
  
Main functions:  
- get_drilldown_payload(...)  
- route_detail_request(...)  
  
Depends on:  
- detail_linker.py  
- flow_filters.py  
  
--------------------------------------------------  
flowvizsdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Flow visualization exceptions.  
  
Examples:  
- FlowBuildError  
- DrilldownRouteError  
- GraphExportError  
  
--------------------------------------------------------------------  
6.3 Public API for flowvizsdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
- build_nodes(...)  
- build_edges(...)  
- summarize_flow(...)  
- build_timeline(...)  
- export_graph(...)  
- filter_graph(...)  
- get_drilldown_payload(...)  
  
--------------------------------------------------------------------  
6.4 Implementation priorities for flowvizsdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. node_builder.py  
3. edge_builder.py  
4. timeline_builder.py  
5. flow_summary.py  
6. graph_export.py  
7. detail_linker.py  
8. flow_filters.py  
9. drilldown_router.py  
  
====================================================================  
7. MONITORINGSDK IMPLEMENTATION BLUEPRINT  
====================================================================  
  
--------------------------------------------------------------------  
7.1 Purpose  
--------------------------------------------------------------------  
monitoringsdk is the post-validation monitoring and dashboard layer.  
  
It should:  
- ingest new monitoring snapshots  
- validate and append snapshot history  
- compute metrics and tests  
- evaluate thresholds and breaches  
- create dashboard-ready payloads  
- support monitoring notes and action logs  
- support annual review pack generation  
  
--------------------------------------------------------------------  
7.2 File-by-file design  
--------------------------------------------------------------------  
  
monitoringsdk/models.py  
Purpose:  
Define monitoring objects.  
  
Key models:  
- MonitoringTemplate  
- MonitoringSnapshot  
- MonitoringHistoryRecord  
- MonitoringMetricSummary  
- MonitoringBreachRecord  
- MonitoringDashboardPayload  
- MonitoringActionRecord  
- AnnualReviewPack  
  
--------------------------------------------------  
monitoringsdk/monitoring_template_registry.py  
--------------------------------------------------  
Purpose:  
Manage approved monitoring templates.  
  
Responsibilities:  
- register by model family  
- define required fields  
- define metrics and thresholds  
- define dashboard dimensions  
  
Main functions:  
- get_monitoring_template(...)  
- validate_monitoring_template(...)  
  
Depends on:  
- config_sdk  
- registry_sdk  
  
--------------------------------------------------  
monitoringsdk/snapshot_ingestor.py  
--------------------------------------------------  
Purpose:  
Ingest new monitoring snapshots.  
  
Responsibilities:  
- accept latest snapshot input  
- normalize structure  
- prepare for validation and append  
  
Main functions:  
- ingest_snapshot(...)  
- normalize_snapshot_input(...)  
  
Depends on:  
- dataset_sdk  
- monitoring_template_registry.py  
  
--------------------------------------------------  
monitoringsdk/snapshot_validator.py  
--------------------------------------------------  
Purpose:  
Validate monitoring snapshot.  
  
Responsibilities:  
- schema checks  
- grain checks  
- required fields  
- date and snapshot uniqueness checks  
  
Main functions:  
- validate_snapshot(...)  
- validate_snapshot_grain(...)  
  
Depends on:  
- snapshot_ingestor.py  
- dq_sdk  
  
--------------------------------------------------  
monitoringsdk/monitoring_history_manager.py  
--------------------------------------------------  
Purpose:  
Manage monitoring history.  
  
Responsibilities:  
- append snapshot to history  
- list prior snapshots  
- expose current/prior view  
- maintain baseline refs  
  
Main functions:  
- append_snapshot(...)  
- get_monitoring_history(...)  
- get_current_baseline(...)  
  
Depends on:  
- dataset_sdk  
- snapshot_validator.py  
  
--------------------------------------------------  
monitoringsdk/metric_engine.py  
--------------------------------------------------  
Purpose:  
Compute monitoring metrics.  
  
Responsibilities:  
- KPI computation  
- score distribution summary  
- feature drift summary  
- performance summary  
  
Main functions:  
- compute_monitoring_metrics(...)  
- summarize_monitoring_metrics(...)  
  
Depends on:  
- monitoring_history_manager.py  
- evaluation_sdk  
  
--------------------------------------------------  
monitoringsdk/threshold_engine.py  
--------------------------------------------------  
Purpose:  
Apply monitoring thresholds.  
  
Responsibilities:  
- pass/warn/breach/severe_breach classification  
- metric-level threshold result  
- threshold summary  
  
Main functions:  
- evaluate_monitoring_thresholds(...)  
- classify_breach_status(...)  
  
Depends on:  
- metric_engine.py  
- policysdk  
  
--------------------------------------------------  
monitoringsdk/drift_engine.py  
--------------------------------------------------  
Purpose:  
Compute drift-specific views.  
  
Responsibilities:  
- PSI/CSI or equivalent  
- population shift  
- score drift  
- feature drift  
  
Main functions:  
- compute_drift(...)  
- summarize_drift(...)  
  
Depends on:  
- metric_engine.py  
- evaluation_sdk  
  
--------------------------------------------------  
monitoringsdk/performance_monitor.py  
--------------------------------------------------  
Purpose:  
Compute performance metrics over time.  
  
Responsibilities:  
- discrimination metrics  
- calibration metrics  
- observed vs predicted trend  
- performance stability trend  
  
Main functions:  
- compute_performance_trend(...)  
- summarize_performance_trend(...)  
  
Depends on:  
- metric_engine.py  
- evaluation_sdk  
  
--------------------------------------------------  
monitoringsdk/segment_monitor.py  
--------------------------------------------------  
Purpose:  
Compute segment-level monitoring summaries.  
  
Responsibilities:  
- segment drift  
- segment performance  
- segment mix change  
- segment breach view  
  
Main functions:  
- compute_segment_monitoring(...)  
- summarize_segment_movements(...)  
  
Depends on:  
- monitoring_history_manager.py  
- evaluation_sdk  
  
--------------------------------------------------  
monitoringsdk/baseline_comparator.py  
--------------------------------------------------  
Purpose:  
Compare current snapshot with baseline.  
  
Responsibilities:  
- previous period comparison  
- validation baseline comparison  
- deployment baseline comparison  
  
Main functions:  
- compare_to_baseline(...)  
- summarize_baseline_gap(...)  
  
Depends on:  
- monitoring_history_manager.py  
- metric_engine.py  
  
--------------------------------------------------  
monitoringsdk/dashboard_payload_builder.py  
--------------------------------------------------  
Purpose:  
Build dashboard-ready data payload.  
  
Responsibilities:  
- KPI table  
- trend series  
- drift series  
- breach summary  
- segment drilldown data  
  
Main functions:  
- build_dashboard_payload(...)  
- build_kpi_view(...)  
- build_trend_view(...)  
  
Depends on:  
- metric_engine.py  
- drift_engine.py  
- performance_monitor.py  
- segment_monitor.py  
  
--------------------------------------------------  
monitoringsdk/dashboard_config_builder.py  
--------------------------------------------------  
Purpose:  
Build dashboard configuration metadata.  
  
Responsibilities:  
- card definitions  
- chart group definitions  
- drilldown definitions  
  
Main functions:  
- build_dashboard_config(...)  
  
Depends on:  
- monitoring_template_registry.py  
- dashboard_payload_builder.py  
  
--------------------------------------------------  
monitoringsdk/monitoring_note_manager.py  
--------------------------------------------------  
Purpose:  
Manage monitoring notes and actions.  
  
Responsibilities:  
- add review notes  
- assign action owner  
- record due dates  
- track disposition  
  
Main functions:  
- create_monitoring_note(...)  
- assign_monitoring_action(...)  
- summarize_action_log(...)  
  
Depends on:  
- auditsdk  
- workflowsdk  
- hitlsdk  
  
--------------------------------------------------  
monitoringsdk/annual_review_pack_builder.py  
--------------------------------------------------  
Purpose:  
Build annual review monitoring package.  
  
Responsibilities:  
- annual KPI summary  
- yearly breach summary  
- action history summary  
- unresolved issue summary  
  
Main functions:  
- build_annual_review_pack(...)  
- summarize_annual_monitoring(...)  
  
Depends on:  
- monitoring_history_manager.py  
- reporting_sdk  
- flowvizsdk optionally  
  
--------------------------------------------------  
monitoringsdk/monitoring_manifest_builder.py  
--------------------------------------------------  
Purpose:  
Build monitoring manifest bundle.  
  
Responsibilities:  
- snapshot refs  
- metric config refs  
- threshold refs  
- dashboard refs  
  
Main functions:  
- build_monitoring_manifest(...)  
  
Depends on:  
- artifactsdk  
- monitoring_history_manager.py  
  
--------------------------------------------------  
monitoringsdk/monitoring_output_writer.py  
--------------------------------------------------  
Purpose:  
Write monitoring outputs.  
  
Responsibilities:  
- write dashboard payloads  
- write KPI tables  
- write breach tables  
- write annual pack outputs  
  
Main functions:  
- write_monitoring_outputs(...)  
  
Depends on:  
- artifactsdk  
- monitoring_manifest_builder.py  
  
--------------------------------------------------  
monitoringsdk/exceptions.py  
--------------------------------------------------  
Purpose:  
Monitoring-specific exceptions.  
  
Examples:  
- MonitoringTemplateError  
- SnapshotValidationError  
- DashboardBuildError  
- AnnualReviewPackError  
  
--------------------------------------------------------------------  
7.3 Public API for monitoringsdk  
--------------------------------------------------------------------  
  
Suggested public functions:  
  
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
  
--------------------------------------------------------------------  
7.4 Implementation priorities for monitoringsdk  
--------------------------------------------------------------------  
  
Priority order:  
1. models.py  
2. monitoring_template_registry.py  
3. snapshot_ingestor.py  
4. snapshot_validator.py  
5. monitoring_history_manager.py  
6. metric_engine.py  
7. threshold_engine.py  
8. drift_engine.py  
9. performance_monitor.py  
10. dashboard_payload_builder.py  
11. dashboard_config_builder.py  
12. baseline_comparator.py  
13. segment_monitor.py  
14. monitoring_note_manager.py  
15. annual_review_pack_builder.py  
16. monitoring_manifest_builder.py  
17. monitoring_output_writer.py  
  
====================================================================  
8. CONTROLLER LAYER EXPANSION FOR WAVE 5  
====================================================================  
  
platform_core/controllers/knowledge_controller.py  
Purpose:  
Coordinate governed knowledge capture and promotion.  
  
Responsibilities:  
- capture knowledge from event/review/decision  
- search knowledge  
- promote knowledge  
- export knowledge bundle  
  
Main methods:  
- capture_knowledge(...)  
- search_knowledge(...)  
- promote_knowledge(...)  
- export_knowledge(...)  
  
--------------------------------------------------  
platform_core/controllers/retrieval_controller.py  
--------------------------------------------------  
Purpose:  
Coordinate retrieval requests for agents and reporting flows.  
  
Responsibilities:  
- route query  
- retrieve context  
- compress and package context  
- enforce token budget  
  
Main methods:  
- retrieve_context(...)  
- retrieve_for_stage(...)  
- build_prompt_package(...)  
  
--------------------------------------------------  
platform_core/controllers/flow_controller.py  
--------------------------------------------------  
Purpose:  
Coordinate flow graph and timeline generation.  
  
Responsibilities:  
- build graph  
- filter graph  
- route drilldown  
- export flow bundle  
  
Main methods:  
- build_flow(...)  
- filter_flow(...)  
- get_flow_drilldown(...)  
  
--------------------------------------------------  
platform_core/controllers/monitoring_controller.py  
--------------------------------------------------  
Purpose:  
Coordinate monitoring workflows.  
  
Responsibilities:  
- ingest snapshot  
- refresh metrics  
- build dashboard payload  
- open breach review  
- build annual review pack  
  
Main methods:  
- ingest_monitoring_snapshot(...)  
- refresh_monitoring(...)  
- build_monitoring_dashboard(...)  
- open_breach_review(...)  
- build_annual_review_pack(...)  
  
====================================================================  
9. AGENT BRIDGE EXPANSION FOR WAVE 5  
====================================================================  
  
platform_core/bridges/agent_bridge/knowledge_context_builder.py  
Purpose:  
Build compact knowledge-layer context.  
  
Responsibilities:  
- include top knowledge refs  
- include scope/type/domain filters  
- avoid raw dump  
  
--------------------------------------------------  
platform_core/bridges/agent_bridge/rag_context_builder.py  
--------------------------------------------------  
Purpose:  
Build retrieval request context.  
  
Responsibilities:  
- role-aware filters  
- stage-aware filters  
- token mode  
- budget profile  
  
--------------------------------------------------  
platform_core/bridges/agent_bridge/monitoring_context_builder.py  
--------------------------------------------------  
Purpose:  
Build compact monitoring context.  
  
Responsibilities:  
- current snapshot refs  
- top KPI movements  
- breach summary  
- annual review mode indicator  
  
--------------------------------------------------  
platform_core/bridges/agent_bridge/flow_context_builder.py  
--------------------------------------------------  
Purpose:  
Build compact flow context.  
  
Responsibilities:  
- run/session refs  
- active branch  
- time range  
- unresolved nodes summary  
  
--------------------------------------------------  
platform_core/bridges/agent_bridge/retrieval_response_normalizer.py  
--------------------------------------------------  
Purpose:  
Normalize retrieval outputs.  
  
Responsibilities:  
- compact context pack  
- token usage hint  
- source refs  
  
--------------------------------------------------  
platform_core/bridges/agent_bridge/monitoring_response_normalizer.py  
--------------------------------------------------  
Purpose:  
Normalize monitoring outputs.  
  
Responsibilities:  
- KPI summary  
- breach summary  
- dashboard refs  
- annual review refs  
  
====================================================================  
10. JUPYTER BRIDGE EXPANSION FOR WAVE 5  
====================================================================  
  
platform_core/bridges/jupyter_bridge/dashboard_workspace_builder.py  
Purpose:  
Build dashboard review workspace for monitoring.  
  
Responsibilities:  
- KPI panel  
- trend panel  
- breach panel  
- segment panel  
- action panel  
  
--------------------------------------------------  
platform_core/bridges/jupyter_bridge/flow_workspace_builder.py  
--------------------------------------------------  
Purpose:  
Build flow explorer workspace.  
  
Responsibilities:  
- graph panel  
- timeline panel  
- detail drilldown panel  
  
--------------------------------------------------  
platform_core/bridges/jupyter_bridge/monitoring_workspace_sync.py  
--------------------------------------------------  
Purpose:  
Sync monitoring dashboard state after refresh or breach review.  
  
Responsibilities:  
- refresh snapshot status  
- refresh KPI panels  
- refresh notes/actions  
- refresh breach state  
  
====================================================================  
11. WAVE 5 END-TO-END WORKFLOW DESIGN  
====================================================================  
  
--------------------------------------------------------------------  
11.1 Knowledge capture flow  
--------------------------------------------------------------------  
1. validation conclusion finalized  
2. knowledge_controller captures decision summary  
3. knowledge_sdk creates project-level knowledge object  
4. knowledge_linker attaches conclusion and findings refs  
5. quality state initialized as captured  
6. knowledge object available for later search/reuse  
  
--------------------------------------------------------------------  
11.2 Retrieval flow  
--------------------------------------------------------------------  
1. validator-agent enters methodology_review  
2. retrieval_controller receives stage-aware retrieval request  
3. rag_sdk query_router chooses retrieval plan  
4. retriever gets scoped candidates  
5. reranker and compressor reduce to compact pack  
6. prompt_packager builds token-thrifty context package  
7. agent receives only compact top summaries and refs  
  
--------------------------------------------------------------------  
11.3 Flow visualization flow  
--------------------------------------------------------------------  
1. flow_controller gets run_id  
2. flowvizsdk builds nodes and edges from event history  
3. timeline built  
4. filtered graph exported for UI  
5. drilldown routed on node click  
  
--------------------------------------------------------------------  
11.4 Monitoring flow  
--------------------------------------------------------------------  
1. monitoring_controller ingests new snapshot  
2. snapshot validated  
3. history updated  
4. metrics and thresholds recomputed  
5. dashboard payload refreshed  
6. breach flags evaluated  
7. if breach:  
   - review opened via hitlsdk/workflowsdk  
8. monitoring-agent summarizes and recommends next actions  
  
====================================================================  
12. TEST BLUEPRINT FOR WAVE 5  
====================================================================  
  
tests/unit/knowledge_sdk/test_knowledge_object.py  
- knowledge object validation  
- scope/type validation  
  
tests/unit/knowledge_sdk/test_knowledge_registry.py  
- register and search knowledge  
  
tests/unit/knowledge_sdk/test_promotion_manager.py  
- promotion approval rules  
- project to domain transition  
  
tests/unit/knowledge_sdk/test_quality_manager.py  
- quality state changes  
- superseded handling  
  
tests/unit/rag_sdk/test_chunker.py  
- chunk construction  
- overlap discipline  
  
tests/unit/rag_sdk/test_query_router.py  
- role/domain/stage retrieval plan logic  
  
tests/unit/rag_sdk/test_retrieval_filters.py  
- superseded filter  
- scope filter  
- project filter  
  
tests/unit/rag_sdk/test_context_compressor.py  
- compact summary construction  
- deduplication  
  
tests/unit/rag_sdk/test_token_budget_manager.py  
- micro/standard/deep modes  
- budget enforcement  
  
tests/unit/flowvizsdk/test_node_builder.py  
- node construction from workflow objects  
  
tests/unit/flowvizsdk/test_edge_builder.py  
- correct edge creation  
  
tests/unit/flowvizsdk/test_flow_summary.py  
- compact path summary output  
  
tests/unit/flowvizsdk/test_drilldown_router.py  
- node detail routing  
  
tests/unit/monitoringsdk/test_snapshot_validator.py  
- schema and grain checks  
- duplicate snapshot detection  
  
tests/unit/monitoringsdk/test_metric_engine.py  
- KPI generation  
  
tests/unit/monitoringsdk/test_threshold_engine.py  
- pass/warn/breach/severe_breach  
  
tests/unit/monitoringsdk/test_drift_engine.py  
- drift summary outputs  
  
tests/unit/monitoringsdk/test_dashboard_payload_builder.py  
- dashboard payload structure  
  
tests/unit/monitoringsdk/test_annual_review_pack_builder.py  
- annual pack summary output  
  
tests/integration/test_knowledge_capture_flow.py  
- decision -> knowledge object creation  
  
tests/integration/test_rag_retrieval_flow.py  
- scoped retrieval -> compressed context pack  
  
tests/integration/test_flowviz_generation_flow.py  
- events -> graph/timeline export  
  
tests/integration/test_monitoring_snapshot_flow.py  
- snapshot ingestion -> KPI refresh  
  
tests/integration/test_monitoring_breach_review_flow.py  
- breach -> review opening -> disposition  
  
tests/integration/test_annual_review_pack_flow.py  
- history -> annual review pack build  
  
====================================================================  
13. NOTEBOOK PLAYBOOKS FOR WAVE 5  
====================================================================  
  
notebooks/knowledge_playbook.ipynb  
- create project knowledge object  
- link to decision and artifacts  
- promote to domain scope  
  
notebooks/rag_playbook.ipynb  
- build retrieval plan  
- retrieve scoped context  
- compress and package prompt context  
  
notebooks/flowviz_playbook.ipynb  
- build flow graph  
- build timeline  
- drill into node details  
  
notebooks/monitoring_playbook.ipynb  
- ingest snapshot  
- compute KPIs  
- build dashboard payload  
- create breach review  
  
notebooks/annual_review_playbook.ipynb  
- load monitoring history  
- build annual review summary  
- export annual monitoring pack  
  
====================================================================  
14. BUILD ORDER FOR WAVE 5  
====================================================================  
  
Phase 5A – knowledge base foundation  
------------------------------------  
1. knowledge_sdk/models.py  
2. knowledge_sdk/knowledge_object.py  
3. knowledge_sdk/knowledge_registry.py  
4. knowledge_sdk/scope_classifier.py  
5. knowledge_sdk/status_manager.py  
6. knowledge_sdk/quality_manager.py  
  
Phase 5B – retrieval base  
-------------------------  
7. rag_sdk/models.py  
8. rag_sdk/chunker.py  
9. rag_sdk/retrieval_filters.py  
10. rag_sdk/query_router.py  
11. rag_sdk/retriever.py  
12. rag_sdk/reranker.py  
13. rag_sdk/context_compressor.py  
14. rag_sdk/prompt_packager.py  
15. rag_sdk/token_budget_manager.py  
  
Phase 5C – knowledge lifecycle services  
---------------------------------------  
16. knowledge_sdk/knowledge_linker.py  
17. knowledge_sdk/lifecycle_service.py  
18. knowledge_sdk/promotion_manager.py  
19. knowledge_sdk/knowledge_export.py  
  
Phase 5D – flow visualization  
-----------------------------  
20. flowvizsdk/models.py  
21. flowvizsdk/node_builder.py  
22. flowvizsdk/edge_builder.py  
23. flowvizsdk/timeline_builder.py  
24. flowvizsdk/flow_summary.py  
25. flowvizsdk/graph_export.py  
26. flowvizsdk/detail_linker.py  
27. flowvizsdk/flow_filters.py  
28. flowvizsdk/drilldown_router.py  
  
Phase 5E – monitoring core  
--------------------------  
29. monitoringsdk/models.py  
30. monitoringsdk/monitoring_template_registry.py  
31. monitoringsdk/snapshot_ingestor.py  
32. monitoringsdk/snapshot_validator.py  
33. monitoringsdk/monitoring_history_manager.py  
34. monitoringsdk/metric_engine.py  
35. monitoringsdk/threshold_engine.py  
36. monitoringsdk/drift_engine.py  
37. monitoringsdk/performance_monitor.py  
38. monitoringsdk/dashboard_payload_builder.py  
39. monitoringsdk/dashboard_config_builder.py  
  
Phase 5F – monitoring advanced  
------------------------------  
40. monitoringsdk/baseline_comparator.py  
41. monitoringsdk/segment_monitor.py  
42. monitoringsdk/monitoring_note_manager.py  
43. monitoringsdk/annual_review_pack_builder.py  
44. monitoringsdk/monitoring_manifest_builder.py  
45. monitoringsdk/monitoring_output_writer.py  
  
Phase 5G – controllers and bridges  
----------------------------------  
46. platform_core/controllers/knowledge_controller.py  
47. platform_core/controllers/retrieval_controller.py  
48. platform_core/controllers/flow_controller.py  
49. platform_core/controllers/monitoring_controller.py  
50. platform_core/bridges/agent_bridge/knowledge_context_builder.py  
51. platform_core/bridges/agent_bridge/rag_context_builder.py  
52. platform_core/bridges/agent_bridge/monitoring_context_builder.py  
53. platform_core/bridges/agent_bridge/flow_context_builder.py  
54. platform_core/bridges/agent_bridge/retrieval_response_normalizer.py  
55. platform_core/bridges/agent_bridge/monitoring_response_normalizer.py  
56. platform_core/bridges/jupyter_bridge/dashboard_workspace_builder.py  
57. platform_core/bridges/jupyter_bridge/flow_workspace_builder.py  
58. platform_core/bridges/jupyter_bridge/monitoring_workspace_sync.py  
  
Phase 5H – optional cache and embedder completion  
-------------------------------------------------  
59. rag_sdk/cache_manager.py  
60. rag_sdk/embedder.py  
  
====================================================================  
15. WAVE 5 MINIMUM VIABLE DEMOS  
====================================================================  
  
Demo 1: Knowledge Capture  
- finalize validation conclusion  
- capture knowledge object  
- search project knowledge  
  
Demo 2: Scoped Retrieval  
- validator enters methodology review  
- retrieve compact domain-reusable and project-specific context  
- package token-thrifty prompt context  
  
Demo 3: Flow Explorer  
- generate flow graph from one completed project run  
- click node to see details  
  
Demo 4: Monitoring Snapshot Refresh  
- add new monthly snapshot  
- compute KPI refresh  
- rebuild dashboard payload  
  
Demo 5: Monitoring Breach Review  
- detect breach  
- open review  
- assign remediation  
  
Demo 6: Annual Review Pack  
- load 12 months of history  
- summarize breaches/actions  
- produce annual review monitoring pack  
  
====================================================================  
16. WHAT WAVE 5 SHOULD NOT DO  
====================================================================  
  
Wave 5 should not:  
- store raw chain-of-thought style reasoning as reusable knowledge  
- allow unrestricted retrieval across all scopes without filters  
- dump large raw documents into prompts by default  
- make dashboard generation UI-specific only  
- let monitoring notes replace formal audit or workflow state  
- promote project-specific noise directly to global reusable knowledge  
  
====================================================================  
17. DELIVERABLE CHECKLIST FOR WAVE 5  
====================================================================  
  
Wave 5 is complete when all of the following exist:  
  
- knowledge_sdk with governed object lifecycle  
- rag_sdk with scoped, compressed, token-thrifty retrieval  
- flowvizsdk with graph/timeline export and drill-down  
- monitoringsdk with snapshot, KPI, breach, dashboard, annual review  
- controllers for knowledge, retrieval, flow, and monitoring  
- at least 6 demos listed above  
- end-to-end monitoring breach review integrated with Wave 2 HITL  
- annual review pack generation integrated with reporting_sdk  
- reusable knowledge capture from validation and governance decisions  
  
====================================================================  
18. FINAL RECOMMENDATION  
====================================================================  
  
Wave 5 should be implemented with a strong separation of concerns:  
  
- knowledge_sdk governs what knowledge exists  
- rag_sdk decides what should be retrieved and how compactly  
- flowvizsdk explains what happened  
- monitoringsdk tracks what is happening now and over time  
  
This separation will keep the platform scalable, governed, and token-  
thrifty.  
  
====================================================================  
END OF WAVE 5 IMPLEMENTATION BLUEPRINT  
====================================================================  
  
