# Refined URD with PPT and Word  
  
# USER REQUIREMENT DOCUMENT (URD)  
# MDLC Agentic AI Platform for ECL Models  
# Strict Governance, Durable Workflow State, Curated Knowledge, Reproducibility, MCP-vs-Skills Design  
  
## 1. Document purpose  
  
This document defines the target user requirements for an agentic AI platform to support the Model Development Life Cycle (MDLC) for ECL models in a strict governance environment.  
  
The platform shall support:  
- ECL model development across PD, LGD, EAD, SICR, stage allocation support, overlays, and monitoring  
- multiple model candidate versions  
- durable workflow state and pause/resume  
- strict governance and auditability  
- reproducibility via model manifest and rerun package  
- curated knowledge and governed memory  
- editor-agnostic operation  
- current deployment in CML  
- future migration to GCP  
- use of deterministic SDKs underneath agent orchestration  
- use of MCP tools and skills in a controlled and explainable manner  
  
This URD also defines:  
- the final set of core platform packages  
- the role of each SDK, service, store, and application  
- which capabilities should be exposed as MCP tools  
- which capabilities should be implemented as skills  
- which capabilities should use both  
  
## 2. Business objective  
  
The objective is to build a governed AI operating layer for ECL MDLC rather than a lightweight coding assistant.  
  
The platform shall:  
1. support end-to-end ECL model development workflows  
2. manage multiple candidate model versions in a traceable way  
3. reduce token usage through retrieval, state externalization, and reusable skills  
4. keep all authoritative states outside prompt history  
5. make final approved model products reproducible by humans and systems  
6. support long-running, human-in-the-loop workflows  
7. create reusable institutional knowledge over time  
8. remain portable across execution environments and frontends  
  
## 3. Scope  
  
### 3.1 In scope  
The platform covers:  
- project intake and setup  
- workflow planning  
- data preparation  
- data quality checks  
- feature engineering  
- model fitting  
- evaluation  
- validation  
- reporting  
- formal document generation  
- presentation generation  
- model packaging  
- model manifest creation  
- rerun and reproducibility validation  
- approval and governance processes  
- knowledge management  
- memory management  
- post-approval monitoring and review support  
  
### 3.2 ECL domain scope  
The platform shall support at minimum:  
- PIT / TTC PD development  
- lifetime PD term structure support  
- forward-looking and macro-linked LGD development  
- EAD / CCF style exposure modelling  
- SICR rules and model-based SICR  
- stage allocation support  
- overlays and management adjustments  
- model comparison and challenger analysis  
- monitoring packs for ongoing use  
  
### 3.3 Out of scope for initial phase  
- direct deployment into booking systems  
- fully autonomous approvals  
- unrestricted autonomous code mutation without governance controls  
- replacing deterministic modelling logic with LLM-only logic  
  
## 4. Target users  
  
Primary users:  
- model developers  
- model validators  
- model governance teams  
- reviewers and approvers  
- risk managers  
- data engineers  
- ECL reporting teams  
- audit and oversight teams  
  
Secondary users:  
- platform engineers  
- AI engineering teams  
- documentation and reporting teams  
  
## 5. Guiding principles  
  
1. Deterministic execution first  
   Agents reason and orchestrate. SDKs execute.  
  
2. Governance first  
   Material actions must not bypass approvals, lineage, audit, and policy controls.  
  
3. State outside the prompt  
   Prompt history is not the system of record.  
  
4. Artifact first  
   Material outputs must be stored as structured, versioned artifacts.  
  
5. Editor agnostic  
   Core platform logic must not depend on Jupyter, VS Code, or any single UI.  
  
6. Reproducibility by construction  
   Final models must be reproducible through manifest, recipe, config, dependency lock, and artifact references.  
  
7. Memory must be curated  
   Retained memory must be source-linked, scoped, confidence-tagged, and governed.  
  
8. Knowledge must be curated  
   Reusable domain knowledge must be versioned, reviewed, and authority-tagged.  
  
9. Token thrift  
   The platform should use compact retrieval, structured summaries, and reusable skills to avoid unnecessary prompt bloat.  
  
10. Clear separation of concerns  
   Skills shape reasoning. MCP tools expose authoritative capabilities. SDKs implement logic.  
  
## 6. High-level architecture  
  
### 6.1 Target architecture  
The platform shall consist of:  
- Google ADK as agent runtime and orchestration layer  
- deterministic SDK packages as the business and governance logic layer  
- MCP-exposed capabilities for authoritative retrieval and actions  
- skill assets for reusable reasoning, review, checklist, and drafting patterns  
- durable workflow/state layer  
- metadata registry and lineage store  
- artifact store  
- memory store  
- knowledge store  
- optional UI/runtime apps  
  
### 6.2 Architectural layers  
  
#### Layer 1: Interaction layer  
Interfaces:  
- Python SDK  
- CLI  
- REST API  
- optional ADK web for development  
- optional custom UI / reviewer app  
- optional notebook adapter  
- optional IDE adapter  
  
#### Layer 2: Agent orchestration layer  
Implemented through ADK:  
- intake agent  
- planning agent  
- data assessment agent  
- feature agent  
- modelling agent  
- evaluation agent  
- validation agent  
- documentation agent  
- governance agent  
- memory curator agent  
- workflow coordinator agent  
  
#### Layer 3: Durable workflow/state layer  
Implemented through workflow runtime:  
- workflow instance state  
- retries  
- pause/resume  
- approval waits  
- escalation and timeout  
- crash recovery  
- run continuity  
  
#### Layer 4: Deterministic execution layer  
Reusable SDKs for:  
- control and governance  
- domain execution  
- reporting and publication  
- reproducibility  
- knowledge and memory  
- monitoring  
  
#### Layer 5: Persistence layer  
Stores:  
- artifact store  
- metadata store  
- model registry  
- memory store  
- knowledge store  
  
#### Layer 6: Observability and audit layer  
- structured logs  
- tool logs  
- agent decision logs  
- approval records  
- lineage  
- memory change logs  
- knowledge change logs  
- rerun validation logs  
- monitoring logs  
  
## 7. Why this architecture is required  
  
This architecture is required because the project needs:  
- multi-version candidate model workflows  
- strict governance  
- traceability and reproducibility  
- durable execution  
- reusable domain knowledge  
- low token usage  
- portability from CML to GCP  
- non-notebook-only operation  
  
The architecture separates:  
- reasoning from execution  
- authoritative system state from prompt context  
- governed retrieval from free-form generation  
- knowledge from memory  
- reporting from formal publication artifacts  
  
## 8. Platform component model  
  
The platform shall not call everything an SDK.  
  
The platform shall distinguish between:  
- SDKs  
- services  
- applications  
- engines  
- adapters  
- stores  
- registries  
  
### 8.1 Naming rules  
- *_sdk      = reusable developer library/package  
- *_service  = deployed operational backend  
- *_app      = runtime-facing or user-facing application  
- *_engine   = internal execution engine  
- *_adapter  = integration bridge  
- *_store    = persistence component  
- *_registry = registry/catalog component  
  
## 9. Final platform package set  
  
### 9.1 Reusable SDKs  
  
#### Core control SDKs  
- governance_sdk  
- workflow_sdk  
- registry_sdk  
- observability_sdk  
  
#### ECL domain SDKs  
- ecl_data_prep_sdk  
- dq_sdk  
- feature_sdk  
- pd_model_sdk  
- lgd_model_sdk  
- ead_model_sdk  
- sicr_sdk  
- overlay_sdk  
- evaluation_sdk  
- validation_sdk  
- monitoring_sdk  
  
#### Reporting and publication SDKs  
- reporting_sdk  
- docgen_sdk  
- pptgen_sdk  
  
#### Reproducibility and packaging SDKs  
- manifest_sdk  
- repro_sdk  
- packaging_sdk  
  
#### Knowledge and memory SDKs  
- memory_sdk  
- knowledge_sdk  
- knowledge_retrieval_sdk  
  
#### Optional support SDKs  
- api_sdk  
- ui_adapter_sdk  
- scheduler_adapter_sdk  
- authz_sdk  
  
### 9.2 Services  
- workflow_service  
- approval_service  
- registry_service  
- memory_service  
- knowledge_service  
- rerun_service  
- artifact_service  
- monitoring_service  
  
### 9.3 Applications  
- adk_agent_app  
- api_app  
- reviewer_app  
- admin_app  
- optional ui_app  
  
### 9.4 Engines  
- retrieval_engine  
- prompt_assembly_engine  
- artifact_packaging_engine  
- evaluation_engine  
  
### 9.5 Adapters  
- temporal_adapter or equivalent workflow adapter  
- s3_adapter  
- cml_adapter  
- gcp_adapter  
- adk_adapter  
  
### 9.6 Stores and registries  
- artifact_store  
- metadata_store  
- memory_store  
- knowledge_store  
- model_registry  
  
## 10. Package purpose and requirements  
  
### 10.1 governance_sdk  
Purpose:  
- policy control  
- stage gating  
- approvals  
- exception handling  
- freeze and publish controls  
- sign-off tracking  
  
Required capabilities:  
- request approval  
- record decision  
- validate actor authority  
- validate stage transition  
- freeze candidate  
- publish approved state  
- register policy exception  
- retrieve governance status  
  
### 10.2 workflow_sdk  
Purpose:  
- workflow contracts  
- stage model  
- transition model  
- workflow orchestration abstractions  
- pause/resume semantics  
- retry semantics  
  
Required capabilities:  
- create run  
- get run state  
- move stage  
- pause for approval  
- resume run  
- mark failed  
- mark complete  
- emit transition event  
  
### 10.3 registry_sdk  
Purpose:  
- registry for project, run, candidate, artifact, dataset, feature set, manifest, memory, knowledge  
  
Required capabilities:  
- create project  
- create run  
- register candidate  
- register dataset snapshot  
- register feature set  
- register artifact  
- register manifest  
- register memory entry  
- register knowledge entry  
- query lineage  
  
### 10.4 observability_sdk  
Purpose:  
- structured logging  
- run trace  
- agent trace  
- tool trace  
- token/cost trace  
- audit event trace  
  
Required capabilities:  
- log event  
- log tool call  
- log agent decision  
- log memory event  
- log knowledge event  
- log rerun event  
- fetch run trace bundle  
  
### 10.5 ecl_data_prep_sdk  
Purpose:  
- source extraction  
- panel assembly  
- cohort generation  
- reporting-date alignment  
- cure/redefault preparation  
- macro join preparation  
- snapshot creation  
  
Required capabilities:  
- build dataset snapshot  
- build panel dataset  
- build cohort dataset  
- generate data summary  
- persist snapshot references  
  
### 10.6 dq_sdk  
Purpose:  
- schema validation  
- temporal validation  
- business rule validation  
- join integrity  
- leakage checks  
- missingness and outlier analysis  
  
Required capabilities:  
- run schema checks  
- run temporal checks  
- run business rule checks  
- run join checks  
- compile DQ pack  
  
### 10.7 feature_sdk  
Purpose:  
- feature generation  
- lags  
- transformations  
- WOE/binning where relevant  
- macro prep  
- feature lineage  
  
Required capabilities:  
- create feature set  
- create macro transform set  
- create WOE mappings  
- create feature lineage  
- summarize feature set  
  
### 10.8 pd_model_sdk  
Purpose:  
- PD candidate fitting  
- hazard/logistic/scorecard-related modelling support  
- PD term structure support  
- fit statistics and outputs  
  
Required capabilities:  
- fit PD candidate  
- generate PD term structure outputs  
- evaluate PD candidate  
- serialize model artifact  
  
### 10.9 lgd_model_sdk  
Purpose:  
- LGD candidate fitting  
- macro-linked LGD logic  
- cure/severity logic  
- cohort/workout support  
  
Required capabilities:  
- fit LGD candidate  
- generate LGD outputs  
- evaluate LGD candidate  
- serialize model artifact  
  
### 10.10 ead_model_sdk  
Purpose:  
- EAD/CCF candidate fitting  
- utilization and exposure-related modelling support  
  
Required capabilities:  
- fit EAD candidate  
- generate EAD outputs  
- evaluate EAD candidate  
- serialize model artifact  
  
### 10.11 sicr_sdk  
Purpose:  
- SICR rules and model logic  
- threshold comparison  
- origination vs reporting comparison  
- impact analysis  
  
Required capabilities:  
- run SICR rules  
- fit SICR candidate  
- compare thresholds  
- generate threshold impact pack  
  
### 10.12 overlay_sdk  
Purpose:  
- overlay preparation  
- rationale packaging  
- adjustment tracking  
- governance support for overlays  
  
Required capabilities:  
- create overlay pack  
- assess rationale support  
- track overlay adjustments  
  
### 10.13 evaluation_sdk  
Purpose:  
- metric computation  
- candidate comparison  
- shortlist support  
- challenger comparison  
  
Required capabilities:  
- compare candidates  
- create shortlist recommendation inputs  
- build metric pack  
  
### 10.14 validation_sdk  
Purpose:  
- validator-friendly testing  
- threshold checks  
- exception packaging  
- methodological challenge support  
  
Required capabilities:  
- run validation tests  
- create validation pack  
- summarize limitations  
- summarize exceptions  
  
### 10.15 monitoring_sdk  
Purpose:  
- post-approval monitoring support  
- model drift and stability review support  
- population shift and calibration monitoring support  
- governance-ready monitoring packs  
  
Required capabilities:  
- generate monitoring dataset snapshot  
- compute monitoring metrics  
- compare current vs reference period  
- generate monitoring exceptions  
- generate monitoring pack  
- track threshold breaches  
- support periodic review summaries  
  
### 10.16 reporting_sdk  
Purpose:  
- analytical reporting outputs  
- charts  
- tables  
- summary reporting packs  
- reporting datasets for stakeholders  
  
Required capabilities:  
- generate charts  
- generate summary tables  
- generate stakeholder reporting pack  
- export reporting datasets  
  
### 10.17 docgen_sdk  
Purpose:  
- formal document generation  
- methodology notes  
- implementation notes  
- validation response documents  
- handover docs  
- governance text documents  
  
Required capabilities:  
- generate methodology note  
- generate implementation note  
- generate validation response document  
- generate handover document  
- assemble document sections from artifacts  
  
### 10.18 pptgen_sdk  
Purpose:  
- PowerPoint generation  
- committee packs  
- CRO decks  
- review decks  
- project update decks  
  
Required capabilities:  
- generate committee presentation  
- generate model approval deck  
- generate project update deck  
- bind charts/tables/narratives into slide structure  
  
### 10.19 manifest_sdk  
Purpose:  
- model manifest generation  
- execution recipe generation  
- fingerprint generation  
- manifest validation  
  
Required capabilities:  
- build manifest  
- validate manifest  
- compute hashes  
- build execution recipe  
  
### 10.20 repro_sdk  
Purpose:  
- rerun from manifest  
- compare rerun vs expected  
- reproducibility validation report  
  
Required capabilities:  
- rerun from manifest  
- compare outputs  
- create reproducibility report  
  
### 10.21 packaging_sdk  
Purpose:  
- package final model product  
- package config, recipe, manifest, artifacts, evidence  
- publish immutable release bundle  
  
Required capabilities:  
- create model product bundle  
- publish product  
- resolve included artifact references  
  
### 10.22 memory_sdk  
Purpose:  
- governed retained contextual memory  
- scoped memory management  
- memory lifecycle and compression  
  
Memory scopes:  
- session memory  
- run memory  
- project memory  
- domain memory  
- institutional memory  
  
Memory types:  
- decision memory  
- assumption memory  
- issue memory  
- rejection memory  
- reviewer feedback memory  
- summary memory  
- execution memory  
- exception memory  
  
Required capabilities:  
- add memory  
- update memory  
- retire memory  
- retrieve memory by scope  
- summarize scope memory  
- compress run memory into project memory  
- track memory lineage and confidence  
  
### 10.23 knowledge_sdk  
Purpose:  
- curated reusable domain knowledge management  
- authority-tagged knowledge lifecycle  
  
Knowledge categories:  
- policy knowledge  
- methodology knowledge  
- portfolio/domain knowledge  
- validation precedent knowledge  
- committee precedent knowledge  
- implementation knowledge  
- reporting knowledge  
- known issue knowledge  
  
Required capabilities:  
- ingest knowledge  
- curate knowledge  
- approve knowledge  
- version knowledge  
- retire knowledge  
- link to source evidence  
- classify by topic and authority  
  
### 10.24 knowledge_retrieval_sdk  
Purpose:  
- governed retrieval over curated knowledge and selected memory  
- authority-aware search and compact retrieval output  
  
Required capabilities:  
- search approved knowledge  
- fetch knowledge item  
- build prompt context from retrieved knowledge  
- rank by authority, relevance, and scope  
- apply metadata filters  
  
## 11. Required third-party package categories  
  
Exact versions shall be finalized later, but the platform should plan for:  
  
### 11.1 Agent and workflow runtime  
- google-adk or chosen ADK runtime packages  
- workflow runtime Python SDK such as temporalio if Temporal is selected  
  
### 11.2 API and schema  
- fastapi  
- uvicorn  
- pydantic  
- pydantic-settings  
  
### 11.3 Data and storage  
- pandas  
- numpy  
- pyarrow  
- boto3  
- sqlalchemy  
- database driver such as psycopg2 or equivalent  
- alembic  
  
### 11.4 Modelling and analytics  
- scikit-learn  
- statsmodels  
- scipy  
- optbinning  
- lifelines if required  
- xgboost or lightgbm only where approved  
- mlflow if experiment tracking is adopted  
  
### 11.5 Reporting and publication  
- jinja2  
- matplotlib  
- plotly if approved  
- python-docx  
- python-pptx  
- openpyxl  
  
### 11.6 Retrieval and text processing  
- sentence-transformers or approved embedding package  
- faiss-cpu or approved vector backend  
- rapidfuzz  
  
### 11.7 Testing and quality  
- pytest  
- pytest-mock  
- coverage  
- mypy  
- ruff  
  
### 11.8 Config and serialization  
- pyyaml  
- tomllib or tomli depending on Python version  
- orjson if approved  
  
## 12. Functional requirements  
  
### 12.1 Project intake and setup  
The platform shall:  
- create a project record  
- capture project scope  
- capture model family and portfolio scope  
- assign workflow template  
- record governance classification  
- identify mandatory checkpoints  
  
### 12.2 Workflow planning  
The platform shall:  
- create stage plan  
- define required inputs and outputs per stage  
- define approval gates  
- define retrieval policy for knowledge and memory per stage  
  
### 12.3 Multiple candidate version management  
The platform shall:  
- support many candidate versions per run  
- maintain candidate identifiers and statuses  
- store configuration and lineage references  
- compare candidates  
- shortlist candidates  
- freeze selected candidate  
- preserve rejected and abandoned history  
  
### 12.4 Durable workflow state  
The platform shall:  
- survive process interruption  
- resume from last committed stage  
- wait for human approval without state loss  
- support retry and timeout behavior  
- keep state outside prompt history  
  
### 12.5 Human-in-the-loop governance  
The platform shall:  
- create approval requests  
- allow approve / reject / return for rework  
- store reviewer notes  
- record who approved what and when  
- support policy exception recording  
  
### 12.6 Artifact generation  
The platform shall:  
- persist material artifacts  
- assign artifact identifiers  
- classify artifacts  
- link artifacts to run, candidate, and manifest  
  
### 12.7 Model manifest and rerun  
The platform shall:  
- generate final model manifest  
- generate execution recipe  
- generate dependency and environment references  
- rerun from manifest  
- compare rerun results against expected outputs  
  
### 12.8 Knowledge and memory  
The platform shall:  
- store curated knowledge  
- store governed memory  
- retrieve only relevant scoped information  
- retire stale memory and obsolete knowledge  
- preserve source references and authority tagging  
  
### 12.9 Monitoring  
The platform shall:  
- support ongoing monitoring pack creation  
- support stability and drift review  
- support threshold breach reporting  
- support periodic review summaries and governance packs  
  
## 13. Non-functional requirements  
  
### 13.1 Governance  
- every material action must be traceable  
- every stage transition must be recorded  
- every approval must be durable  
- every memory and knowledge change must be auditable  
- every final artifact must be attributable  
  
### 13.2 Reproducibility  
- final model must be rerunnable from manifest and recipe  
- config and dependency references must be frozen or immutably referenced  
- datasets must be snapshot referenced  
- rerun must validate outputs within defined tolerance  
  
### 13.3 Token thrift  
- prompts must use compact summaries and references  
- skills must avoid repeated long reasoning instructions  
- MCP tools must return compact structured payloads  
- full reports should not be injected into prompts unnecessarily  
  
### 13.4 Security and access  
- role-based access required  
- approval actions attributable  
- sensitive artifacts controlled  
- knowledge and memory access filtered by scope and authority  
  
### 13.5 Extensibility  
- new model families must be pluggable  
- new workflow templates configurable  
- new skills addable without core redesign  
- new MCP tools addable with stable contracts  
  
### 13.6 Portability  
- platform must run in CML now  
- platform must support migration to GCP later  
- migration must preserve SDK contracts, manifest schema, and workflow semantics  
  
## 14. Data and state model  
  
### 14.1 Core entities  
- Project  
- WorkflowTemplate  
- Run  
- StageExecution  
- CandidateModel  
- DatasetSnapshot  
- FeatureSet  
- Artifact  
- ApprovalRequest  
- ApprovalDecision  
- Manifest  
- RerunExecution  
- MemoryEntry  
- KnowledgeEntry  
- MonitoringRun  
- MonitoringException  
  
### 14.2 Minimal identifiers  
- project_id  
- run_id  
- stage_id  
- candidate_id  
- dataset_snapshot_id  
- feature_set_id  
- artifact_id  
- approval_id  
- manifest_id  
- rerun_id  
- memory_id  
- knowledge_id  
- monitoring_run_id  
  
### 14.3 Workflow state minimum fields  
- current stage  
- stage status  
- completed stages  
- pending approvals  
- retry count  
- failure reason  
- last committed checkpoint  
- stage output summary  
- active candidate set  
- shortlisted candidate set  
- final candidate id if frozen  
  
## 15. Model manifest requirements  
  
The manifest shall be mandatory for any selected or approved model.  
  
Required contents:  
  
### 15.1 Identity  
- model product name  
- project id  
- run id  
- candidate id  
- model id  
- model family  
- portfolio scope  
- status  
  
### 15.2 Versioning  
- manifest version  
- workflow version  
- config version  
- code version or release tag  
- package versions  
  
### 15.3 Data lineage  
- source dataset references  
- dataset snapshot id  
- observation and performance windows  
- slicing and filters  
- DQ report reference  
  
### 15.4 Feature lineage  
- feature set id  
- transformation steps  
- mapping specs  
- final feature list  
- feature selection rationale reference  
  
### 15.5 Model specification  
- algorithm  
- objective  
- hyperparameters  
- constraints  
- segmentation logic  
- random seed  
- fitting procedure reference  
  
### 15.6 Artifact references  
- model object URI  
- metrics URI  
- validation pack URI  
- documentation pack URI  
- presentation pack URI where applicable  
- governance pack URI  
- monitoring baseline pack URI where applicable  
  
### 15.7 Reproduction instructions  
- entrypoint command  
- required parameters  
- dependency lock reference  
- environment reference  
- expected outputs  
- rerun validation logic  
  
### 15.8 Governance  
- created by  
- reviewed by  
- approved by  
- approval date  
- exceptions  
- limitations  
- usage boundaries  
  
### 15.9 Fingerprints  
- config hash  
- dataset hash  
- feature hash  
- artifact hashes  
- manifest hash  
  
## 16. Memory and knowledge design  
  
### 16.1 Memory rules  
Memory shall be:  
- scoped  
- source-linked  
- confidence-scored  
- status-tagged  
- retired or superseded when stale  
  
Memory shall not be:  
- raw unfiltered chat dump  
- uncontrolled long-term accumulation  
- substitute for authoritative registry state  
  
### 16.2 Knowledge rules  
Knowledge shall be:  
- curated  
- versioned  
- authority-tagged  
- linked to source evidence  
- reviewed and approved where necessary  
  
Knowledge shall not be:  
- silently merged when conflicting  
- treated as authoritative without approval status  
- polluted by low-quality raw conversation fragments  
  
### 16.3 Retrieval rules  
Prompt context assembly shall prioritize:  
1. current workflow state  
2. run memory  
3. project memory  
4. approved knowledge  
5. compact artifact summaries  
  
## 17. MCP tools vs skills design  
  
## 17.1 Definitions  
  
### Skill  
A skill is a reusable reasoning, checklist, drafting, or interpretation asset.  
  
Used for:  
- how the agent should think  
- how the agent should review  
- how the agent should compare  
- how the agent should draft  
- how the agent should follow a domain checklist  
  
A skill is not:  
- authoritative state  
- an approval mechanism  
- a workflow state engine  
- a system-of-record interface  
  
### MCP tool  
An MCP tool is an authoritative callable capability exposed to agents for structured reads, writes, retrieval, and system actions.  
  
Used for:  
- authoritative retrieval  
- system writes  
- state transitions  
- approvals  
- registry access  
- manifest and artifact operations  
- governed knowledge access  
  
## 17.2 Guiding rule  
- Skills shape reasoning  
- MCP tools expose authoritative capabilities  
- Deterministic SDKs perform the logic underneath  
  
## 17.3 Decision framework  
  
A capability shall be MCP if:  
- it changes system state  
- it reads authoritative state  
- it needs strict schema  
- it must be shared across runtimes  
- it touches governance, registry, manifest, approvals, or artifacts  
- it must be audited  
- it must be deterministic  
  
A capability shall be a skill if:  
- it is mainly a reasoning pattern  
- it is mainly a drafting pattern  
- it is mainly a checklist  
- it does not own authoritative state  
- it does not perform critical system writes  
  
A capability shall be hybrid if:  
- it needs authoritative tool retrieval or execution  
- and also benefits from a reusable reasoning/drafting pattern  
  
## 18. MCP-first capability groups  
  
The following shall be MCP tools or equivalent authoritative tool interfaces.  
  
### 18.1 Governance and approvals  
- create approval request  
- get approval status  
- record approval decision  
- validate stage transition  
- register policy exception  
- freeze candidate  
- publish approved state  
  
### 18.2 Workflow state  
- create run  
- get run state  
- update stage status  
- pause for approval  
- resume run  
- get pending tasks  
- get stage checkpoint summary  
  
### 18.3 Registry and lineage  
- register candidate  
- fetch candidate summary  
- fetch dataset snapshot metadata  
- fetch feature lineage  
- fetch artifact index  
- fetch run lineage  
- fetch model product record  
  
### 18.4 Manifest and reproducibility  
- build manifest  
- validate manifest  
- fetch manifest  
- rerun from manifest  
- compare rerun outputs  
- publish model product bundle  
  
### 18.5 Knowledge retrieval  
- search approved knowledge  
- fetch knowledge item  
- fetch validation precedent  
- fetch committee precedent  
- fetch policy note  
  
### 18.6 Memory operations  
- retrieve project memory  
- retrieve run memory summary  
- add approved memory  
- retire deprecated memory  
- compress run memory into project memory  
  
### 18.7 Artifact operations  
- get validation pack  
- get documentation pack  
- get presentation pack  
- resolve artifact URI  
- publish artifact bundle  
- fetch evidence pack  
  
### 18.8 Monitoring operations  
- generate monitoring snapshot  
- fetch monitoring metrics  
- fetch monitoring exceptions  
- publish monitoring pack  
- record threshold breach review  
  
## 19. Skill-first capability groups  
  
The following should primarily be skills.  
  
### 19.1 Review and challenge playbooks  
- PD candidate review checklist  
- LGD recursive structure challenge guide  
- EAD methodological review pattern  
- SICR threshold challenge framework  
- overlay rationale review guide  
- monitoring breach interpretation guide  
  
### 19.2 Drafting playbooks  
- methodology note drafting style  
- committee summary drafting style  
- validation rebuttal drafting style  
- limitation summary drafting pattern  
- implementation note drafting pattern  
- monitoring review summary drafting style  
- CRO deck narrative style  
  
### 19.3 Comparison and interpretation guides  
- candidate comparison checklist  
- DQ issue interpretation guide  
- threshold trade-off guide  
- performance trade-off review guide  
- stability and calibration interpretation guide  
- monitoring movement interpretation guide  
  
### 19.4 Process and analyst guidance  
- ECL MDLC stage checklist  
- pre-submission checklist  
- evidence completeness checklist  
- challenger comparison checklist  
- reviewer handoff checklist  
- periodic monitoring checklist  
  
### 19.5 Formatting and house style  
- standard abbreviations  
- portfolio terminology guide  
- governance tone guide  
- approved narrative wording guide  
- presentation tone guide  
  
## 20. Hybrid capability groups  
  
These should use both MCP and skills.  
  
### 20.1 Data quality  
- MCP tool: run and fetch DQ results  
- Skill: interpret DQ significance for ECL suitability  
  
### 20.2 Feature engineering  
- MCP tool: fetch feature summary and lineage  
- Skill: explain feature quality and shortlist rationale  
  
### 20.3 Evaluation  
- MCP tool: compare candidates and fetch metrics  
- Skill: interpret trade-offs and draft recommendation  
  
### 20.4 Validation  
- MCP tool: fetch validation pack and exceptions  
- Skill: explain significance and draft validation response  
  
### 20.5 Knowledge retrieval  
- MCP tool: retrieve approved knowledge  
- Skill: explain how to apply it in context  
  
### 20.6 Memory  
- MCP tool: retrieve scoped memory summary  
- Skill: decide relevance and summarize it for current reasoning  
  
### 20.7 Monitoring  
- MCP tool: fetch monitoring metrics and breaches  
- Skill: explain implications and draft monitoring commentary  
  
## 21. Package-by-package MCP vs skills recommendation  
  
### 21.1 Mainly MCP-facing  
- governance_sdk  
- workflow_sdk  
- registry_sdk  
- manifest_sdk  
- repro_sdk  
- packaging_sdk  
- memory_sdk  
- knowledge_sdk  
- knowledge_retrieval_sdk  
- monitoring_sdk  
  
### 21.2 Mainly skill-facing  
- pd_model_sdk  
- lgd_model_sdk  
- ead_model_sdk  
- sicr_sdk  
- overlay_sdk  
- reporting_sdk  
- docgen_sdk  
- pptgen_sdk  
  
### 21.3 Hybrid  
- dq_sdk  
- feature_sdk  
- evaluation_sdk  
- validation_sdk  
- memory_sdk  
- knowledge_sdk  
- monitoring_sdk  
  
## 22. ECL workflow application examples  
  
### 22.1 PD workflow  
Use MCP for:  
- candidate registration  
- metric retrieval  
- manifest generation  
- artifact retrieval  
  
Use skills for:  
- PD review checklist  
- calibration interpretation  
- limitation drafting  
- committee narrative  
  
### 22.2 LGD workflow  
Use MCP for:  
- macro treatment precedent retrieval  
- candidate result retrieval  
- manifest and rerun functions  
  
Use skills for:  
- recursive design challenge framing  
- forward-looking explanation  
- methodology note drafting  
  
### 22.3 EAD workflow  
Use MCP for:  
- candidate metrics  
- workflow updates  
- artifact lookup  
  
Use skills for:  
- utilization dynamics interpretation  
- reviewer narrative  
  
### 22.4 SICR workflow  
Use MCP for:  
- approved threshold retrieval  
- threshold impact pack retrieval  
- approval actions  
  
Use skills for:  
- trade-off interpretation  
- rule-vs-model comparison narrative  
  
### 22.5 Overlay workflow  
Use MCP for:  
- approved overlay rationale retrieval  
- governance sign-off recording  
  
Use skills for:  
- rationale drafting  
- exception explanation  
  
### 22.6 Monitoring workflow  
Use MCP for:  
- current monitoring metric retrieval  
- threshold breach retrieval  
- monitoring pack publishing  
  
Use skills for:  
- stability interpretation  
- drift commentary  
- periodic review narrative  
- governance escalation wording  
  
## 23. Concise end-to-end flow  
  
1. User starts ECL project  
2. Project and run are created  
3. Workflow plan is assigned  
4. Data snapshot is built  
5. DQ is executed  
6. Features are created  
7. Candidate models are fitted  
8. Candidates are compared  
9. Agent uses skill-guided reasoning over MCP-fetched evidence  
10. Human reviewer shortlists candidates  
11. Validation is executed  
12. Reporting, documents, and presentations are generated  
13. Governance approval is routed  
14. Selected candidate is frozen  
15. Manifest and execution recipe are generated  
16. Final model product is packaged  
17. Rerun from manifest is validated  
18. Monitoring baseline pack is created  
19. Knowledge and memory are curated for reuse  
  
## 24. Final model product definition  
  
A final model product is complete only if it includes:  
- final model manifest  
- execution recipe  
- frozen config bundle  
- dependency/environment reference  
- model object  
- metric pack  
- validation pack  
- reporting pack  
- formal documents  
- presentation deck where required  
- governance approval evidence  
- reproducibility report  
- monitoring baseline pack if applicable  
- artifact index  
  
## 25. Acceptance criteria  
  
The platform shall be accepted only if:  
  
1. an ECL project can be run end-to-end through governed stages  
2. multiple candidate model versions can be built and compared  
3. workflow state survives interruption and resumes correctly  
4. approvals pause and resume correctly  
5. artifacts are registered with lineage  
6. final selected candidate generates a complete manifest  
7. rerun from manifest is possible without ambiguity  
8. rerun outputs are validated within tolerance  
9. memory and knowledge changes are auditable  
10. monitoring packs can be generated after model approval  
11. all governance-sensitive actions are exposed through MCP or equivalent authoritative tools  
12. skills are used only for reasoning, drafting, checklist, and interpretation patterns  
13. the platform remains usable beyond notebook-only environments  
  
## 26. Recommended implementation sequence  
  
### Phase 1: Core control backbone  
- observability_sdk  
- registry_sdk  
- governance_sdk  
- workflow_sdk  
  
### Phase 2: Knowledge and memory backbone  
- memory_sdk  
- knowledge_sdk  
- knowledge_retrieval_sdk  
  
### Phase 3: Data and features  
- ecl_data_prep_sdk  
- dq_sdk  
- feature_sdk  
  
### Phase 4: ECL modelling  
- pd_model_sdk  
- lgd_model_sdk  
- ead_model_sdk  
- sicr_sdk  
- overlay_sdk  
  
### Phase 5: Evaluation and validation  
- evaluation_sdk  
- validation_sdk  
- monitoring_sdk  
  
### Phase 6: Reporting and publication  
- reporting_sdk  
- docgen_sdk  
- pptgen_sdk  
  
### Phase 7: Reproducibility and packaging  
- manifest_sdk  
- repro_sdk  
- packaging_sdk  
  
### Phase 8: Runtime exposure  
- workflow_service  
- approval_service  
- registry_service  
- memory_service  
- knowledge_service  
- rerun_service  
- monitoring_service  
- adk_agent_app  
- api_app  
- reviewer_app  
  
## 27. Final recommendation  
  
The recommended architecture for this project is:  
  
Google ADK + deterministic SDKs + authoritative MCP tools + reusable skills + durable workflow runtime + metadata registry + artifact store + memory store + knowledge store + reproducibility layer + monitoring layer + optional runtime apps  
  
The project shall not:  
- treat skills as a replacement for authoritative tools  
- treat MCP as a replacement for reasoning playbooks  
- bury document and presentation generation inside reporting without clear separation  
- rely on prompt history as official workflow state  
  
The project shall:  
- use skills for reusable reasoning and token-thrifty guidance  
- use MCP tools for authoritative reads, writes, retrieval, governance, workflow, and reproducibility  
- keep deterministic SDKs as the execution backbone  
- preserve strict governance and reproducibility from entry point to final approved model product  
