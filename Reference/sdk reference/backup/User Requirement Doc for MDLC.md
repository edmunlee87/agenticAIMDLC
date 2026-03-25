User Requirement Doc for MDLC  
  
# User Requirement Document (URD)  
# MDLC Agentic AI Solution for ECL Models  
# Strict Governance, Durable State, Curated Memory, and Reproducibility via Model Manifest  
  
## 1. Purpose  
  
Build an editor-agnostic, governed, reproducible, token-thrifty agentic AI platform for the end-to-end model development lifecycle (MDLC) of ECL models in a regulated environment.  
  
The solution shall support:  
- IFRS 9 / regulatory ECL model development lifecycle  
- PD, LGD, EAD, SICR, staging, forward-looking overlays, and stress testing extensions  
- multi-version candidate model workflow  
- strict governance, audit, review, approval, and lineage  
- durable workflow state and pause/resume across long-running execution  
- deterministic SDK-driven execution  
- curated knowledge and governed memory  
- reproducibility through model manifest and rerun bundle  
- current deployment in CML  
- future migration to GCP  
- optional rich UI through AG-UI or custom frontend  
- agent runtime and orchestration through Google ADK  
  
## 2. Objectives  
  
The solution shall:  
1. Enable governed agentic execution for ECL MDLC, not just coding assistance.  
2. Support many candidate model versions across PD, LGD, EAD, SICR, and overlays.  
3. Minimize token usage by storing workflow state, lineage, evidence, memory, and artifacts outside LLM prompt context.  
4. Ensure all material actions are executed through deterministic, testable SDKs.  
5. Produce final approved model products that can be rerun by a human or machine with minimal ambiguity.  
6. Maintain strict auditability suitable for model governance, validation, internal audit, and regulatory review.  
7. Support human-in-the-loop checkpoints without losing state.  
8. Build reusable institutional knowledge over time without allowing uncontrolled memory sprawl.  
  
## 3. Scope  
  
### 3.1 In scope  
- ECL project intake and setup  
- problem framing  
- data preparation  
- data quality assessment  
- cohort and panel creation  
- feature engineering  
- macroeconomic variable preparation  
- candidate model development  
- diagnostics and validation  
- challenger comparison  
- documentation generation  
- governance review  
- approval workflow  
- final model packaging  
- reproducibility packaging  
- model manifest generation  
- registry and lineage  
- curated knowledge and memory  
- optional UI and reviewer interaction layer  
  
### 3.2 ECL model scope  
The platform shall cover at minimum:  
- PIT / TTC PD development  
- lifetime PD term structure logic  
- downturn / forward-looking / macro-linked LGD development  
- EAD and CCF style exposure modeling  
- SICR assessment logic, model-based and rule-based  
- stage allocation support  
- overlays and management adjustments  
- segmentation and pooling logic  
- stress testing extensions where relevant  
- portfolio-level and segment-level monitoring packs  
  
### 3.3 Out of scope  
- direct deployment into production booking systems in phase 1  
- fully autonomous model approval without human governance  
- unrestricted free-form code mutation by agents without policy control  
  
## 4. Target users  
  
Primary users:  
- model developers  
- model validators  
- model governance teams  
- ECL reporting teams  
- reviewers and approvers  
- quantitative analysts  
- data engineers  
- risk managers  
- audit and oversight teams  
  
Secondary users:  
- platform engineers  
- AI/ML engineering teams  
- documentation and reporting teams  
  
## 5. Guiding principles  
  
1. Deterministic execution first  
   Agents reason and orchestrate. SDKs execute.  
  
2. Governance first  
   No material action may bypass lineage, audit, approval, and policy controls.  
  
3. Artifact first  
   Outputs must be saved as structured, versioned artifacts rather than buried in chat history.  
  
4. State outside prompt  
   LLM context must not be the system of record for workflow state.  
  
5. Editor agnostic  
   Core logic must not depend on Jupyter, VS Code, or any single frontend.  
  
6. Reproducibility by construction  
   Final model product must be reproducible through model manifest, frozen config, dependency lock, and execution recipe.  
  
7. Memory must be curated  
   Knowledge growth is allowed, but only through source-linked, governed, confidence-tagged memory entries.  
  
8. Token thrift  
   Prompts should retrieve only compact summaries, decision-ready slices, and referenced evidence.  
  
## 6. High-level architecture  
  
### 6.1 Recommended architecture  
Target stack:  
- Google ADK for agent runtime and orchestration  
- deterministic domain SDKs for ECL business logic  
- governance SDK for approvals, audit, lineage, evidence, and policy gates  
- durable workflow/state layer using Temporal as primary recommendation  
- CML as current execution environment  
- S3 as artifact and bundle storage  
- relational metadata store for run state, candidate versions, lineage, approvals, manifest indexing, knowledge metadata  
- knowledge SDK for curated institutional knowledge  
- memory SDK for session/run/project/domain memory lifecycle  
- optional AG-UI or custom frontend for richer interaction  
  
### 6.2 Architecture layers  
  
#### Layer 1: Interaction layer  
Interfaces:  
- CLI  
- Python SDK  
- REST API  
- optional AG-UI frontend  
- optional notebook/IDE adapters  
  
#### Layer 2: Agent orchestration layer  
Implemented through ADK:  
- intake agent  
- planning agent  
- data assessment agent  
- feature engineering agent  
- modeling agent  
- validation-readiness agent  
- documentation agent  
- governance review agent  
- memory curator agent  
- workflow coordinator agent  
  
#### Layer 3: Durable workflow/state layer  
Implemented with Temporal:  
- workflow instance state  
- retries  
- pause/resume  
- human approval waiting  
- timeout and escalation  
- crash recovery  
- long-running execution continuity  
  
#### Layer 4: Deterministic SDK layer  
Contains all domain, governance, memory, and knowledge packages.  
  
#### Layer 5: Persistence layer  
- S3 for artifacts  
- metadata database for structured state and registry  
- knowledge store for curated memory and knowledge objects  
- optional vector index for semantic retrieval on curated content only  
  
#### Layer 6: Observability and audit layer  
- run tracing  
- tool call logs  
- agent decision logs  
- approval records  
- artifact lineage  
- reproducibility verification results  
- memory add/update/retire audit trail  
  
## 7. Why this architecture is recommended  
  
This architecture is recommended because it separates:  
- reasoning from execution  
- workflow state from prompt history  
- large artifacts from chat context  
- knowledge memory from raw conversational history  
- approval records from UI state  
- deterministic logic from agent variability  
  
This is essential for:  
- token thrift  
- strict governance  
- many model version experiments  
- reproducibility  
- long-lived ECL model programs  
- migration from CML to GCP  
  
## 8. Core architectural decisions  
  
### 8.1 Google ADK  
ADK shall be used as the agent runtime and orchestration layer, not as the holder of business logic.  
  
It shall manage:  
- agent definitions  
- routing  
- context assembly  
- tool calling  
- multi-agent coordination  
- workflow-aware orchestration  
  
### 8.2 Temporal  
Temporal shall be the preferred durable workflow/state layer because it aligns well with:  
- long-running governed workflows  
- human approval checkpoints  
- recoverability  
- explicit workflow/activity structure  
- resumable orchestration  
  
### 8.3 S3  
S3 shall be used for:  
- datasets  
- feature artifacts  
- model files  
- metrics  
- plots  
- reports  
- documentation bundles  
- approval packs  
- manifests  
- rerun bundles  
- serialized memory exports where required  
  
S3 shall not be the primary workflow state engine.  
  
### 8.4 Metadata store  
A structured metadata store shall hold:  
- project registry  
- run registry  
- stage registry  
- candidate registry  
- config versions  
- dataset snapshots  
- feature set lineage  
- approval history  
- manifest index  
- artifact index  
- memory index  
- knowledge index  
- reproducibility fingerprints  
  
### 8.5 Memory and knowledge separation  
The platform shall distinguish between:  
- memory: contextual, scoped, operationally useful retained information  
- knowledge: curated, reusable, semi-authoritative or authoritative domain content  
  
Memory is dynamic and often run or project scoped.  
Knowledge is curated and reusable across runs and projects.  
  
## 9. Logical package design  
  
All packages must be callable from:  
- Python  
- CLI  
- API  
- agent tool interfaces  
  
### 9.1 Core control packages  
  
#### 9.1.1 governance_sdk  
Purpose:  
- policy control  
- stage gating  
- approval management  
- audit trail  
- exception registry  
- authority checks  
- usage restrictions  
- sign-off tracking  
  
Key functions:  
- create_approval_request  
- record_decision  
- validate_authority  
- freeze_candidate  
- publish_approved_state  
- generate_governance_summary  
- register_policy_exception  
  
#### 9.1.2 workflow_sdk  
Purpose:  
- workflow contracts  
- stage definitions  
- transition rules  
- orchestration adapters for ADK and Temporal  
- retry policy definitions  
- workflow resume semantics  
  
Key functions:  
- initialize_run  
- move_stage  
- set_pending_approval  
- resume_workflow  
- mark_failed  
- mark_complete  
- emit_transition_event  
  
#### 9.1.3 registry_sdk  
Purpose:  
- project, run, candidate, artifact, dataset, manifest, knowledge, and memory registry  
  
Key functions:  
- create_project  
- create_run  
- register_candidate  
- update_candidate_status  
- register_artifact  
- register_manifest  
- register_memory_entry  
- register_knowledge_entry  
- query_lineage  
  
#### 9.1.4 observability_sdk  
Purpose:  
- structured logging  
- agent action trace  
- tool trace  
- token tracking  
- latency and cost tracking  
- execution diagnostics  
  
### 9.2 ECL domain execution packages  
  
#### 9.2.1 ecl_data_prep_sdk  
Purpose:  
- dataset extraction  
- contract/entity/customer level assembly  
- observation/performance window building  
- cohort and panel creation  
- default/cure/redefault preparation  
- stage and delinquency join logic  
- macro join preparation  
- snapshot writing  
  
Outputs:  
- dataset_snapshot_id  
- panel_snapshot_id  
- cohort_summary  
- schema summary  
- artifact URIs  
  
#### 9.2.2 dq_sdk  
Purpose:  
- schema checks  
- completeness checks  
- type consistency  
- leakage checks  
- temporal consistency  
- join integrity  
- outlier screening  
- business rule checks  
- reporting date integrity  
- cohort consistency checks  
  
Outputs:  
- dq_report  
- issue_list  
- severity classification  
- pass/fail flags  
  
#### 9.2.3 feature_sdk  
Purpose:  
- feature engineering  
- lags  
- differencing  
- standardization  
- WOE/binning where relevant  
- transformation specs  
- macro variable preparation  
- interaction features  
- feature set assembly  
- feature metadata generation  
  
Outputs:  
- feature_set_id  
- transform_spec  
- feature_lineage  
- feature_diagnostics  
  
#### 9.2.4 pd_model_sdk  
Purpose:  
- PD candidate model fitting  
- hazard models  
- logistic / scorecard style models  
- term structure logic  
- marginal and cumulative PD derivation  
- PIT/TTC alignment logic  
- macro incorporation  
  
Outputs:  
- candidate_id  
- model_uri  
- coefficient tables  
- fit summaries  
- PD curves  
- candidate metrics  
  
#### 9.2.5 lgd_model_sdk  
Purpose:  
- LGD candidate model fitting  
- workout / cohort style LGD preparation  
- cure and severity decomposition  
- macro-linked LGD logic  
- ECM / time-series linked logic where relevant  
- segmentation and pooling support  
  
Outputs:  
- candidate_id  
- model_uri  
- diagnostics  
- candidate metrics  
- output tables  
  
#### 9.2.6 ead_model_sdk  
Purpose:  
- EAD / CCF candidate model fitting  
- utilization dynamics  
- exposure conversion logic  
- facility-level feature processing  
- segmentation logic  
  
Outputs:  
- candidate_id  
- model_uri  
- diagnostics  
- candidate metrics  
  
#### 9.2.7 sicr_sdk  
Purpose:  
- SICR model and rules execution  
- relative and absolute PD comparison logic  
- origination vs reporting month comparison  
- rule-based and model-based SICR evaluation  
- threshold impact and backtesting support  
  
Outputs:  
- sicr_rule_set_id  
- candidate results  
- threshold summary  
- challenge pack inputs  
  
#### 9.2.8 overlay_sdk  
Purpose:  
- management overlay preparation  
- overlay rationale documentation support  
- scenario adjustments  
- post-model adjustment tracking  
- attribution support  
  
Outputs:  
- overlay_pack  
- rationale_summary  
- governance flags  
  
#### 9.2.9 evaluation_sdk  
Purpose:  
- discrimination  
- calibration  
- ranking metrics  
- stability  
- drift  
- robustness  
- segmentation comparisons  
- champion/challenger comparison  
  
Outputs:  
- evaluation report  
- metric tables  
- shortlist recommendation inputs  
  
#### 9.2.10 validation_sdk  
Purpose:  
- validator-friendly test execution  
- threshold checks  
- methodological challenge pack  
- model limitations summary  
- test evidence generation  
  
Outputs:  
- validation pack  
- exception list  
- breach summary  
- reviewer notes scaffold  
  
#### 9.2.11 reporting_sdk  
Purpose:  
- charts  
- summary tables  
- stakeholder reports  
- committee visuals  
- model monitoring pack inputs  
- stage movement and ECL attribution support  
  
#### 9.2.12 docgen_sdk  
Purpose:  
- formal model documentation  
- technical paper  
- methodology note  
- implementation note  
- validation response pack  
- committee note  
- handover pack  
  
### 9.3 Reproducibility packages  
  
#### 9.3.1 manifest_sdk  
Purpose:  
- generate model manifest  
- generate execution recipe  
- freeze resolved config  
- compute hashes  
- link artifact references  
- validate manifest completeness  
  
#### 9.3.2 repro_sdk  
Purpose:  
- rerun model from manifest  
- compare rerun outputs  
- validate tolerance  
- rebuild key artifacts  
- generate reproducibility report  
  
#### 9.3.3 packaging_sdk  
Purpose:  
- create final model product bundle  
- package config, code refs, recipe, manifest, outputs, evidence  
- publish immutable release bundle  
  
### 9.4 Memory and knowledge packages  
  
#### 9.4.1 memory_sdk  
Purpose:  
Manage scoped, governed retained context for agentic workflows without making prompt history the system of record.  
  
Memory scopes:  
- session memory  
- run memory  
- project memory  
- domain memory  
- institutional memory  
  
Memory entry types:  
- decision memory  
- assumption memory  
- issue memory  
- rejection memory  
- preference memory  
- execution memory  
- exception memory  
- summary memory  
- reviewer feedback memory  
  
Required capabilities:  
- add memory entry  
- update memory entry  
- retire stale memory entry  
- version memory entry  
- score confidence  
- tag scope and owner  
- attach source references  
- mark authoritative vs advisory  
- mark active vs deprecated  
- retrieve relevant memory slices  
- summarize memory by scope  
- compress run history into reusable memory  
- maintain full audit trail of memory lifecycle  
  
Suggested internal modules:  
- memory_sdk/contracts/  
  - enums.py  
  - request_models.py  
  - response_models.py  
  - memory_models.py  
- memory_sdk/store/  
  - memory_repository.py  
  - vector_index.py  
  - metadata_index.py  
- memory_sdk/curation/  
  - deduplicator.py  
  - conflict_resolver.py  
  - confidence_scorer.py  
  - retirement_policy.py  
  - summarizer.py  
- memory_sdk/retrieval/  
  - scope_retriever.py  
  - semantic_retriever.py  
  - metadata_filter.py  
  - ranker.py  
- memory_sdk/governance/  
  - audit_logger.py  
  - retention_policy.py  
  - access_control.py  
  - approval_policy.py  
  
Memory fields:  
- memory_id  
- memory_type  
- scope_type  
- scope_id  
- title  
- summary  
- body  
- source_type  
- source_ref  
- created_by  
- created_at  
- last_updated_at  
- confidence_score  
- authority_level  
- status  
- superseded_by  
- tags  
  
Design rules:  
- memory must never be blindly appended from every conversation  
- memory addition can be auto-suggested but must be policy-controlled  
- only high-value, source-linked items should persist beyond a session  
- run memory may be compressed into project memory after run closure  
- stale memory must be retired or superseded  
  
Use cases:  
- store why candidate 12 was rejected  
- store a reviewer preference for calibration priority  
- store approved SICR threshold rationale  
- store validator challenge and accepted response  
- store repeated data issue pattern in a portfolio  
  
#### 9.4.2 knowledge_sdk  
Purpose:  
Manage curated reusable domain knowledge used across projects, agents, and workflows.  
  
Knowledge categories:  
- policy and standards knowledge  
- methodology knowledge  
- portfolio/domain knowledge  
- model inventory knowledge  
- validation challenge knowledge  
- implementation knowledge  
- reporting and committee knowledge  
- known issue and workaround knowledge  
  
Required capabilities:  
- ingest knowledge item  
- curate knowledge item  
- approve knowledge item  
- version knowledge item  
- retire obsolete knowledge item  
- link knowledge to source documents and artifacts  
- classify knowledge by topic and authority  
- retrieve knowledge slices by context  
- generate knowledge summaries for prompts  
- maintain lineage from knowledge item to source evidence  
  
Suggested internal modules:  
- knowledge_sdk/contracts/  
  - enums.py  
  - request_models.py  
  - response_models.py  
  - knowledge_models.py  
- knowledge_sdk/ingestion/  
  - doc_ingestor.py  
  - artifact_ingestor.py  
  - structured_ingestor.py  
- knowledge_sdk/curation/  
  - classifier.py  
  - normalizer.py  
  - conflict_resolver.py  
  - approver.py  
  - version_manager.py  
- knowledge_sdk/retrieval/  
  - topic_retriever.py  
  - semantic_retriever.py  
  - citation_builder.py  
  - contextual_ranker.py  
- knowledge_sdk/governance/  
  - audit_logger.py  
  - access_control.py  
  - publication_policy.py  
  - deprecation_policy.py  
  
Knowledge item fields:  
- knowledge_id  
- category  
- topic  
- title  
- summary  
- body  
- source_type  
- source_ref  
- source_version  
- authority_level  
- approval_status  
- approved_by  
- effective_date  
- expiry_or_review_date  
- tags  
- related_knowledge_ids  
  
Design rules:  
- knowledge must come from curated sources, not raw chat alone  
- knowledge must be versioned and source-linked  
- conflicting knowledge must be flagged, not silently merged  
- knowledge used in agent prompts should be rendered as compact summaries with references  
- policy knowledge and methodology knowledge should have higher authority tagging  
  
Use cases:  
- store approved bank standard for macro variable treatment  
- store accepted model validation precedent for recursive LGD logic  
- store portfolio-specific default definition  
- store approved feature shortlist principles for specific asset classes  
- store committee-agreed threshold logic for SICR or overlay governance  
  
#### 9.4.3 rag_sdk  
Purpose:  
Provide retrieval services over curated knowledge and memory only.  
  
Required capabilities:  
- chunking strategy for curated documents  
- embedding generation  
- semantic search  
- metadata filtering  
- authority-aware ranking  
- prompt assembly helpers  
- citation-ready retrieval output  
  
Design rule:  
RAG shall not retrieve uncontrolled raw content by default. Retrieval should prioritize curated knowledge, approved memory, and registered artifacts.  
  
## 10. Packages required to be developed  
  
The following internal packages shall be developed and installed as part of the platform:  
  
Core packages:  
- governance_sdk  
- workflow_sdk  
- registry_sdk  
- observability_sdk  
  
ECL execution packages:  
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
- reporting_sdk  
- docgen_sdk  
  
Reproducibility packages:  
- manifest_sdk  
- repro_sdk  
- packaging_sdk  
  
Memory and knowledge packages:  
- memory_sdk  
- knowledge_sdk  
- rag_sdk  
  
Optional support packages:  
- api_sdk  
- ui_adapter_sdk  
- scheduler_adapter_sdk  
- authz_sdk  
  
## 11. Third-party packages and runtime dependencies  
  
The exact pinned versions will be finalized during technical design, but the platform shall plan for the following categories of external packages.  
  
### 11.1 Agent and workflow runtime  
- google-adk or the chosen ADK runtime package set  
- temporalio  
  
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
- psycopg2 or equivalent database driver  
- alembic  
  
### 11.4 Modeling and statistics  
- scikit-learn  
- statsmodels  
- scipy  
- optbinning  
- xgboost or lightgbm if approved for certain use cases  
- lifelines if survival utilities are needed  
- mlflow if experiment tracking is required  
  
### 11.5 Documents and reporting  
- jinja2  
- matplotlib  
- plotly if interactive charts are needed  
- python-docx  
- pptx generation package if PowerPoint output is required  
- openpyxl for spreadsheet artifact generation  
  
### 11.6 Retrieval and text processing  
- sentence-transformers or approved embedding library  
- faiss-cpu or approved vector backend  
- rapidfuzz  
- unstructured or equivalent only if document ingestion is needed and approved  
  
### 11.7 Testing and quality  
- pytest  
- pytest-mock  
- coverage  
- mypy  
- ruff  
  
### 11.8 Configuration and serialization  
- pyyaml  
- tomli or standard library tomllib depending on Python version  
- orjson if approved for performance  
  
## 12. Functional requirements  
  
### 12.1 Project intake and setup  
The platform shall:  
- register new ECL projects  
- assign project id  
- capture business objective  
- capture model family: PD, LGD, EAD, SICR, overlay  
- capture portfolio and segment scope  
- capture governance classification  
- define workflow template and mandatory checkpoints  
  
### 12.2 Workflow planning  
The platform shall:  
- create an MDLC execution plan  
- identify mandatory stages  
- define required inputs and outputs  
- attach policy checks  
- define required approvals  
- define memory and knowledge retrieval rules per stage  
  
### 12.3 Multi-version candidate model management  
The platform shall:  
- support many candidate versions per run  
- maintain candidate ids and statuses  
- compare candidates across features, windows, methods, constraints, and segments  
- shortlist candidates  
- freeze selected candidate  
- keep full rejected/abandoned history  
  
### 12.4 Durable workflow state  
The platform shall:  
- survive restart and interruption  
- resume from last committed workflow step  
- wait for human approval without losing context  
- support retry and timeout handling  
- keep stage state outside prompt context  
  
### 12.5 Human-in-the-loop governance  
The platform shall:  
- allow mandatory approval steps  
- allow challenge and feedback capture  
- allow reject / rework / approve decisions  
- store reviewer notes and timestamps  
- enforce role-based approval policies  
  
### 12.6 Artifact generation  
The platform shall:  
- save all material outputs as artifacts  
- assign artifact ids and URIs  
- classify artifacts by type  
- link artifacts to candidates, runs, manifests, and knowledge entries when relevant  
  
### 12.7 Model manifest and rerun  
The platform shall produce a final model manifest that includes:  
- project id  
- run id  
- candidate id  
- model id  
- dataset snapshot reference  
- feature set reference  
- config version  
- code version reference  
- environment and dependency lock reference  
- artifact references  
- execution recipe  
- governance status  
- hashes and fingerprints  
  
The platform shall allow a human or automated process to rerun the model from the manifest.  
  
### 12.8 Memory and knowledge  
The platform shall:  
- store curated domain knowledge  
- store project-level decisions  
- store validator challenges and accepted responses  
- store reviewer preferences where policy allows  
- retrieve relevant prior decisions by scope  
- keep memory and knowledge source-linked and governed  
- retire stale memory and obsolete knowledge  
- prevent uncontrolled accumulation  
  
## 13. Non-functional requirements  
  
### 13.1 Governance  
- every material action must be traceable  
- every stage transition must be recorded  
- every approval must be durable  
- every memory or knowledge change must be auditable  
- every final artifact must be attributable  
- system of record must be outside chat transcript  
  
### 13.2 Reproducibility  
- rerun must be possible from manifest and recipe  
- rerun must reproduce expected outputs within tolerance  
- dependencies and config must be frozen or immutably referenced  
- datasets must be snapshot referenced  
  
### 13.3 Token thrift  
- prompts must contain summaries and references rather than full raw outputs  
- memory retrieval must be scope-limited  
- knowledge retrieval must be authority-aware  
- full workflow history must not be replayed unnecessarily  
  
### 13.4 Security and access  
- access must be role-based  
- approval actions must be attributable  
- sensitive artifacts must be controlled by policy  
- memory and knowledge access must honor scope and authority  
  
### 13.5 Extensibility  
- new model families must be pluggable  
- new workflow templates must be configurable  
- new validation tests must be modular  
- new memory rules and knowledge categories must be configurable  
- new UI frontends must not require core rewrite  
  
### 13.6 Portability  
- core services must run in CML now  
- architecture must support future migration to GCP  
- migration must not require redesign of core contracts  
  
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
- KnowledgeVersion  
- MemoryRetentionEvent  
  
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
  
### 14.3 Workflow state fields  
Each workflow instance shall at minimum track:  
- current stage  
- stage status  
- prior completed stages  
- pending approvals  
- retry count  
- failure reason  
- last committed checkpoint  
- stage output summary  
- active candidate set  
- shortlisted candidate set  
- final candidate id if frozen  
  
## 15. Memory and knowledge operational design  
  
### 15.1 Memory lifecycle  
1. event occurs  
2. candidate memory entry proposed  
3. policy check applied  
4. memory stored with scope and confidence  
5. retrieval eligible based on scope and authority  
6. periodic summarization and deduplication  
7. retirement or supersession when stale  
  
### 15.2 Knowledge lifecycle  
1. source artifact or document ingested  
2. candidate knowledge extracted  
3. domain classification applied  
4. curator review or approval applied  
5. knowledge published with authority level  
6. knowledge versioned over time  
7. obsolete knowledge deprecated, not silently deleted  
  
### 15.3 Retrieval rules  
Prompt assembly shall prioritize:  
1. current stage state  
2. run memory  
3. project memory  
4. approved project/domain knowledge  
5. relevant artifact summaries  
  
Prompt assembly shall avoid:  
- full raw memory dumps  
- low-confidence deprecated items  
- obsolete knowledge versions unless explicitly requested  
  
## 16. Model manifest requirements  
  
The model manifest shall be a required final artifact for any selected or approved ECL model.  
  
### 16.1 Manifest contents  
  
Identity:  
- model product name  
- project id  
- run id  
- candidate id  
- model id  
- model family  
- portfolio scope  
- status  
  
Versioning:  
- manifest version  
- workflow version  
- config version  
- code commit or release tag  
- package versions  
  
Data lineage:  
- source dataset refs  
- dataset snapshot id  
- observation and performance windows  
- sampling and filters  
- DQ report ref  
  
Feature lineage:  
- feature set id  
- transformation steps  
- mapping specs  
- final feature list  
- feature selection rationale ref  
  
Model specification:  
- algorithm  
- objective  
- hyperparameters  
- constraints  
- segmentation logic  
- random seed  
- fitting procedure ref  
  
Artifact references:  
- model object URI  
- metrics URI  
- coefficient URI  
- plots URI  
- validation pack URI  
- documentation pack URI  
- governance pack URI  
  
Reproduction instructions:  
- entrypoint command  
- required parameters  
- dependency lock ref  
- environment ref  
- expected outputs  
- rerun validation logic  
  
Governance:  
- created by  
- reviewed by  
- approved by  
- approval date  
- exceptions  
- limitations  
- usage boundaries  
  
Fingerprints:  
- config hash  
- dataset hash  
- feature hash  
- artifact hashes  
- manifest hash  
  
## 17. Flow simulation: entry point to final model product  
  
### 17.1 Concise flow  
  
1. User starts ECL project  
2. Intake agent captures scope and creates project record  
3. Planning agent creates workflow plan and checkpoint requirements  
4. Workflow engine opens run_id  
5. ecl_data_prep_sdk builds dataset snapshot  
6. dq_sdk validates dataset and produces DQ report  
7. feature_sdk builds one or more feature sets and macro prep specs  
8. pd_model_sdk / lgd_model_sdk / ead_model_sdk / sicr_sdk fit multiple candidates  
9. evaluation_sdk compares candidates  
10. agent summarizes trade-offs for shortlist decision  
11. human reviewer approves shortlist or requests rework  
12. validation_sdk runs detailed validator-facing checks on shortlisted candidates  
13. reporting_sdk and docgen_sdk generate technical and governance packs  
14. governance_sdk routes approval package  
15. human approver approves or returns with conditions  
16. manifest_sdk freezes selected candidate into model manifest  
17. packaging_sdk publishes final model product bundle  
18. repro_sdk validates rerun from manifest  
19. registry_sdk marks model product as approved and reproducible  
20. knowledge_sdk and memory_sdk curate reusable lessons and decisions  
  
### 17.2 Final product definition  
The final model product shall contain:  
- final model manifest  
- frozen config bundle  
- execution recipe  
- reproducibility report  
- model object  
- metric pack  
- validation pack  
- documentation pack  
- governance approval evidence  
- artifact index  
  
## 18. Acceptance criteria  
  
The solution shall be accepted only if all of the following are met:  
1. An ECL project can be created and run end-to-end through governed workflow stages.  
2. Multiple candidate model versions can be built, compared, and shortlisted.  
3. Workflow state survives restart and resumes correctly after interruption.  
4. Human approval can pause and resume a run without losing context.  
5. Artifacts are stored with linked lineage and indexed in registry.  
6. Final selected model generates a complete manifest.  
7. A human can rerun the model using the manifest and recipe without ambiguity.  
8. Rerun produces expected outputs within defined tolerance.  
9. Memory and knowledge entries are auditable, source-linked, and scope-controlled.  
10. The platform can be used without dependence on a notebook-only interface.  
  
## 19. Recommended implementation phases  
  
### Phase 1: Backbone  
Deliver:  
- ADK orchestration  
- metadata registry  
- S3 artifact management  
- deterministic SDK skeletons  
- basic project/run/candidate flow  
- memory_sdk and knowledge_sdk contracts  
  
### Phase 2: Durable governance  
Deliver:  
- Temporal-based durable workflow layer  
- approval pause/resume  
- structured audit and lineage  
- memory retention and retirement policies  
- knowledge publication and deprecation policies  
  
### Phase 3: ECL domain execution  
Deliver:  
- ECL data prep  
- DQ  
- feature engineering  
- PD/LGD/EAD/SICR candidate building  
- evaluation and validation packs  
  
### Phase 4: Final model product  
Deliver:  
- manifest SDK  
- repro SDK  
- packaging SDK  
- final model product bundle  
- rerun validation report  
  
### Phase 5: Knowledge and UI  
Deliver:  
- curated memory and knowledge services  
- RAG over curated content  
- optional AG-UI or custom frontend  
- reviewer inbox  
- run monitor  
- knowledge explorer  
  
## 20. Final recommendation  
  
The recommended architecture for this ECL MDLC agentic AI solution is:  
  
Google ADK + Temporal + deterministic ECL SDKs + governance SDK + metadata registry + S3 artifact store + memory SDK + knowledge SDK + RAG SDK + manifest/reproducibility layer + optional AG-UI/custom UI  
  
This architecture best satisfies:  
- strict governance  
- multi-version ECL model workflow  
- token thrift  
- durable state management  
- human approval control  
- reproducibility via model manifest  
- curated growing knowledge  
- editor-agnostic operation  
- migration path from CML to GCP  
  
  
# Appendix A: Recommended Repository and Package Structure  
# MDLC Agentic AI Solution for ECL Models  
  
mdlc_agentic_ai/  
  pyproject.toml  
  README.md  
  Makefile  
  .env.example  
  
  configs/  
    platform/  
      app.yaml  
      logging.yaml  
      storage.yaml  
      auth.yaml  
      temporal.yaml  
      adk.yaml  
    workflows/  
      ecl_pd_workflow.yaml  
      ecl_lgd_workflow.yaml  
      ecl_ead_workflow.yaml  
      sicr_workflow.yaml  
      overlay_workflow.yaml  
    policies/  
      approval_policy.yaml  
      memory_policy.yaml  
      knowledge_policy.yaml  
      artifact_policy.yaml  
      rerun_policy.yaml  
    portfolios/  
      sg_cc.yaml  
      sg_cl.yaml  
      hk_cc.yaml  
  
  src/  
    governance_sdk/  
    workflow_sdk/  
    registry_sdk/  
    observability_sdk/  
  
    ecl_data_prep_sdk/  
    dq_sdk/  
    feature_sdk/  
    pd_model_sdk/  
    lgd_model_sdk/  
    ead_model_sdk/  
    sicr_sdk/  
    overlay_sdk/  
    evaluation_sdk/  
    validation_sdk/  
    reporting_sdk/  
    docgen_sdk/  
  
    manifest_sdk/  
    repro_sdk/  
    packaging_sdk/  
  
    memory_sdk/  
    knowledge_sdk/  
    rag_sdk/  
  
    adk_app/  
      agents/  
        intake_agent/  
        planning_agent/  
        data_assessment_agent/  
        feature_agent/  
        modeling_agent/  
        validation_agent/  
        documentation_agent/  
        governance_agent/  
        memory_curator_agent/  
        workflow_coordinator_agent/  
      tools/  
        governance_tools.py  
        registry_tools.py  
        workflow_tools.py  
        memory_tools.py  
        knowledge_tools.py  
        ecl_tools.py  
      prompts/  
      runtime/  
      sessions/  
  
    api_app/  
      main.py  
      routers/  
      dependencies/  
      schemas/  
      services/  
  
    temporal_app/  
      workflows/  
      activities/  
      workers/  
      signals/  
  
  tests/  
    unit/  
    integration/  
    replay/  
    e2e/  
  
  docs/  
    urd/  
    architecture/  
    workflows/  
    manifests/  
    runbooks/  
  
  scripts/  
    bootstrap_env.py  
    create_project.py  
    create_run.py  
    rerun_from_manifest.py  
    publish_model_product.py  
  
  notebooks/  
    demos/  
    poc/  
    diagnostics/  
  
  sql/  
    ddl/  
    views/  
    seeds/  
  
  templates/  
    manifests/  
    reports/  
    docs/  
    approvals/  
  
# Appendix B: Package Dependency Direction  
  
Lowest-level foundational packages:  
- observability_sdk  
- registry_sdk  
- governance_sdk  
- workflow_sdk  
  
Domain execution packages:  
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
- reporting_sdk  
- docgen_sdk  
  
Reproducibility packages:  
- manifest_sdk  
- repro_sdk  
- packaging_sdk  
  
Knowledge layer:  
- memory_sdk  
- knowledge_sdk  
- rag_sdk  
  
Orchestration layer:  
- adk_app  
- temporal_app  
- api_app  
  
Dependency rule:  
- ADK agents may call SDKs through tool wrappers  
- Temporal activities may call deterministic SDKs directly  
- Domain SDKs must not depend on ADK  
- Domain SDKs must not depend on UI code  
- Manifest and repro SDKs may depend on registry and artifact metadata  
- Memory and knowledge SDKs may depend on registry, observability, and storage abstractions only  
  
# Appendix C: Package-by-Package Interface Expectations  
  
## governance_sdk  
Required interfaces:  
- request_approval(payload) -> approval_id  
- record_approval_decision(approval_id, decision_payload) -> decision_record  
- validate_stage_transition(run_id, from_stage, to_stage) -> validation_result  
- freeze_candidate(run_id, candidate_id) -> freeze_result  
- register_policy_exception(payload) -> exception_id  
- get_governance_status(run_id) -> governance_status  
  
## workflow_sdk  
Required interfaces:  
- create_workflow_run(project_id, workflow_type, payload) -> run_id  
- get_run_state(run_id) -> run_state  
- advance_stage(run_id, stage_name, payload) -> stage_result  
- pause_for_approval(run_id, approval_payload) -> pause_result  
- resume_run(run_id, signal_payload) -> resume_result  
- fail_run(run_id, error_payload) -> fail_result  
- complete_run(run_id, result_payload) -> completion_result  
  
## registry_sdk  
Required interfaces:  
- create_project(payload) -> project_id  
- create_run(payload) -> run_id  
- register_dataset_snapshot(payload) -> dataset_snapshot_id  
- register_feature_set(payload) -> feature_set_id  
- register_candidate(payload) -> candidate_id  
- register_artifact(payload) -> artifact_id  
- register_manifest(payload) -> manifest_id  
- register_memory_entry(payload) -> memory_id  
- register_knowledge_entry(payload) -> knowledge_id  
- search_registry(filters) -> search_result  
  
## observability_sdk  
Required interfaces:  
- log_event(payload)  
- log_tool_call(payload)  
- log_agent_decision(payload)  
- log_memory_event(payload)  
- log_knowledge_event(payload)  
- log_rerun_event(payload)  
- get_run_trace(run_id) -> trace_bundle  
  
## ecl_data_prep_sdk  
Required interfaces:  
- build_dataset_snapshot(payload) -> dataset_snapshot_result  
- build_panel_dataset(payload) -> panel_result  
- build_cohort_dataset(payload) -> cohort_result  
- generate_data_summary(payload) -> summary_result  
  
## dq_sdk  
Required interfaces:  
- run_schema_checks(payload) -> dq_result  
- run_temporal_checks(payload) -> dq_result  
- run_join_integrity_checks(payload) -> dq_result  
- run_ecl_business_rule_checks(payload) -> dq_result  
- compile_dq_pack(payload) -> dq_pack_result  
  
## feature_sdk  
Required interfaces:  
- create_feature_set(payload) -> feature_set_result  
- transform_macro_variables(payload) -> macro_transform_result  
- create_woe_mappings(payload) -> woe_result  
- create_feature_lineage(payload) -> lineage_result  
  
## pd_model_sdk  
Required interfaces:  
- fit_candidate(payload) -> candidate_result  
- generate_pd_term_structure(payload) -> term_structure_result  
- evaluate_pd_candidate(payload) -> evaluation_result  
  
## lgd_model_sdk  
Required interfaces:  
- fit_candidate(payload) -> candidate_result  
- generate_lgd_outputs(payload) -> lgd_result  
- evaluate_lgd_candidate(payload) -> evaluation_result  
  
## ead_model_sdk  
Required interfaces:  
- fit_candidate(payload) -> candidate_result  
- generate_ead_outputs(payload) -> ead_result  
- evaluate_ead_candidate(payload) -> evaluation_result  
  
## sicr_sdk  
Required interfaces:  
- run_sicr_rules(payload) -> sicr_result  
- fit_sicr_candidate(payload) -> candidate_result  
- compare_origination_vs_reporting(payload) -> comparison_result  
- generate_threshold_impact(payload) -> threshold_result  
  
## overlay_sdk  
Required interfaces:  
- create_overlay_pack(payload) -> overlay_result  
- assess_overlay_rationale(payload) -> rationale_result  
  
## evaluation_sdk  
Required interfaces:  
- compare_candidates(payload) -> comparison_result  
- generate_shortlist_recommendation(payload) -> shortlist_result  
- compile_metric_pack(payload) -> metric_pack_result  
  
## validation_sdk  
Required interfaces:  
- run_validation_tests(payload) -> validation_result  
- generate_validation_pack(payload) -> validation_pack_result  
- summarize_limitations(payload) -> limitation_result  
  
## reporting_sdk  
Required interfaces:  
- generate_charts(payload) -> chart_bundle  
- generate_summary_tables(payload) -> table_bundle  
- generate_stakeholder_pack(payload) -> reporting_bundle  
  
## docgen_sdk  
Required interfaces:  
- generate_methodology_note(payload) -> doc_result  
- generate_implementation_note(payload) -> doc_result  
- generate_committee_pack(payload) -> doc_result  
- generate_handover_pack(payload) -> doc_result  
  
## manifest_sdk  
Required interfaces:  
- build_manifest(payload) -> manifest_result  
- validate_manifest(payload) -> validation_result  
- build_execution_recipe(payload) -> recipe_result  
- compute_fingerprints(payload) -> fingerprint_result  
  
## repro_sdk  
Required interfaces:  
- rerun_from_manifest(payload) -> rerun_result  
- compare_rerun_vs_expected(payload) -> comparison_result  
- build_reproducibility_report(payload) -> repro_report  
  
## packaging_sdk  
Required interfaces:  
- build_model_product_bundle(payload) -> bundle_result  
- publish_model_product(payload) -> publish_result  
  
## memory_sdk  
Required interfaces:  
- add_memory(payload) -> memory_id  
- update_memory(memory_id, payload) -> update_result  
- retire_memory(memory_id, payload) -> retire_result  
- retrieve_memory(payload) -> memory_results  
- summarize_scope_memory(payload) -> summary_result  
- compress_run_memory(payload) -> compression_result  
  
## knowledge_sdk  
Required interfaces:  
- ingest_knowledge(payload) -> knowledge_id  
- curate_knowledge(payload) -> curation_result  
- approve_knowledge(payload) -> approval_result  
- retire_knowledge(payload) -> retirement_result  
- retrieve_knowledge(payload) -> knowledge_results  
- summarize_knowledge(payload) -> summary_result  
  
## rag_sdk  
Required interfaces:  
- index_curated_content(payload) -> index_result  
- search_curated_content(payload) -> retrieval_result  
- build_prompt_context(payload) -> prompt_context_result  
  
# Appendix D: Minimum Metadata Tables  
  
Core tables:  
- project  
- workflow_template  
- run  
- run_stage  
- candidate_model  
- dataset_snapshot  
- feature_set  
- artifact  
- approval_request  
- approval_decision  
- manifest  
- rerun_execution  
  
Memory and knowledge tables:  
- memory_entry  
- memory_version  
- memory_event  
- knowledge_entry  
- knowledge_version  
- knowledge_event  
- knowledge_source_link  
- retrieval_log  
  
Useful fields by table:  
  
project:  
- project_id  
- project_name  
- project_type  
- portfolio_code  
- status  
- created_at  
  
run:  
- run_id  
- project_id  
- workflow_type  
- current_stage  
- run_status  
- started_at  
- ended_at  
  
candidate_model:  
- candidate_id  
- run_id  
- model_family  
- model_method  
- config_hash  
- dataset_snapshot_id  
- feature_set_id  
- status  
- selected_flag  
  
artifact:  
- artifact_id  
- run_id  
- candidate_id  
- artifact_type  
- artifact_uri  
- checksum  
- created_at  
  
manifest:  
- manifest_id  
- run_id  
- candidate_id  
- manifest_uri  
- manifest_hash  
- status  
- created_at  
  
memory_entry:  
- memory_id  
- scope_type  
- scope_id  
- memory_type  
- title  
- summary  
- source_ref  
- confidence_score  
- authority_level  
- status  
  
knowledge_entry:  
- knowledge_id  
- category  
- topic  
- title  
- summary  
- source_ref  
- authority_level  
- approval_status  
- effective_date  
- retirement_date  
  
# Appendix E: Entry Point Simulation  
  
Example entrypoint:  
1. user creates ECL PD project for SG credit cards  
2. system creates project_id = PRJ_ECL_PD_SG_CC_001  
3. planning agent chooses workflow template = ecl_pd_workflow  
4. Temporal workflow creates run_id = RUN_20260325_001  
5. ecl_data_prep_sdk generates dataset snapshot DS_001  
6. dq_sdk generates dq pack DQ_001  
7. feature_sdk generates feature sets FS_001, FS_002, FS_003  
8. pd_model_sdk fits candidates CAND_001 to CAND_012  
9. evaluation_sdk generates shortlist recommendation  
10. human reviewer shortlists CAND_004 and CAND_009  
11. validation_sdk runs deeper tests on CAND_004 and CAND_009  
12. governance_sdk records approval to freeze CAND_004  
13. manifest_sdk generates MAN_001  
14. packaging_sdk builds final model product bundle PROD_001  
15. repro_sdk reruns from MAN_001 and confirms reproducibility  
16. registry_sdk marks final state as APPROVED_REPRODUCIBLE  
17. knowledge_sdk stores reusable approved knowledge  
18. memory_sdk compresses run memory into project memory summary  
  
# Appendix F: Installation Sequence  
  
Recommended sequence:  
  
Stage 1:  
- observability_sdk  
- registry_sdk  
- governance_sdk  
- workflow_sdk  
  
Stage 2:  
- memory_sdk  
- knowledge_sdk  
- rag_sdk  
  
Stage 3:  
- ecl_data_prep_sdk  
- dq_sdk  
- feature_sdk  
  
Stage 4:  
- pd_model_sdk  
- lgd_model_sdk  
- ead_model_sdk  
- sicr_sdk  
- overlay_sdk  
  
Stage 5:  
- evaluation_sdk  
- validation_sdk  
- reporting_sdk  
- docgen_sdk  
  
Stage 6:  
- manifest_sdk  
- repro_sdk  
- packaging_sdk  
  
Stage 7:  
- temporal_app  
- adk_app  
- api_app  
  
# Appendix G: Definition of Done for Final Model Product  
  
A final model product is complete only if:  
- one candidate is formally frozen  
- all required artifacts are registered  
- manifest is generated and validated  
- dependency lock and environment reference exist  
- governance approval status is recorded  
- rerun from manifest passes tolerance checks  
- handover documentation is generated  
- memory and knowledge updates are completed per policy  
  
# Appendix H: Recommended Next Deliverables  
  
1. package-by-package technical design document  
2. metadata ERD  
3. manifest JSON/YAML schema  
4. Temporal workflow design  
5. ADK agent/tool contract design  
6. memory and knowledge policy specification  
7. MVP implementation plan for ECL PD workflow  
  
  
# Naming Convention for MDLC Agentic AI Platform  
  
## 1. Naming principles  
  
Use names based on the role of the component, not force everything into "sdk".  
  
Recommended categories:  
- *_sdk       -> reusable developer library/package  
- *_service   -> deployed backend/service component  
- *_app       -> user-facing or runtime application  
- *_engine    -> execution or processing engine  
- *_store     -> persistence/storage component  
- *_adapter   -> integration bridge to external systems  
- *_registry  -> metadata or catalog component  
- *_policy    -> policy/config/rules package  
- *_runtime   -> orchestration/runtime host  
  
## 2. Recommended platform naming structure  
  
### 2.1 Reusable SDK packages  
These are importable Python packages with stable interfaces.  
  
Core / control SDKs:  
- governance_sdk  
- workflow_sdk  
- registry_sdk  
- observability_sdk  
- manifest_sdk  
- repro_sdk  
- packaging_sdk  
- memory_sdk  
- knowledge_sdk  
  
Domain SDKs:  
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
- reporting_sdk  
- docgen_sdk  
  
Optional integration SDKs:  
- api_sdk  
- ui_adapter_sdk  
- scheduler_adapter_sdk  
- authz_sdk  
  
### 2.2 Services  
These are deployed operational components.  
  
Recommended:  
- workflow_service  
- registry_service  
- knowledge_service  
- memory_service  
- artifact_service  
- rerun_service  
- approval_service  
  
### 2.3 Applications  
These are runtime-facing or user-facing applications.  
  
Recommended:  
- adk_agent_app  
- api_app  
- reviewer_app  
- admin_app  
- ui_app  
  
### 2.4 Engines  
These are internal execution-heavy components.  
  
Recommended:  
- retrieval_engine  
- evaluation_engine  
- orchestration_engine  
- prompt_assembly_engine  
- artifact_packaging_engine  
  
### 2.5 Stores / registries  
These are persistence components.  
  
Recommended:  
- artifact_store  
- metadata_store  
- memory_store  
- knowledge_store  
- model_registry  
  
### 2.6 Adapters  
These connect to external infrastructure.  
  
Recommended:  
- s3_adapter  
- temporal_adapter  
- cml_adapter  
- gcp_adapter  
- adk_adapter  
  
## 3. Recommended wording for the URD  
  
Use this wording:  
  
"The platform consists of reusable SDKs, operational services, runtime applications, storage components, and integration adapters."  
  
Do not say:  
"All components are SDKs."  
  
## 4. Recommended package map for your platform  
  
### Reusable SDKs  
- governance_sdk  
- workflow_sdk  
- registry_sdk  
- observability_sdk  
  
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
- reporting_sdk  
- docgen_sdk  
  
- manifest_sdk  
- repro_sdk  
- packaging_sdk  
  
- memory_sdk  
- knowledge_sdk  
  
### Services  
- workflow_service  
- registry_service  
- approval_service  
- memory_service  
- knowledge_service  
- rerun_service  
  
### Applications  
- adk_agent_app  
- api_app  
- reviewer_app  
  
### Engines  
- retrieval_engine  
- prompt_assembly_engine  
  
### Stores  
- artifact_store  
- metadata_store  
- memory_store  
- knowledge_store  
- model_registry  
  
### Adapters  
- temporal_adapter  
- s3_adapter  
- cml_adapter  
- gcp_adapter  
  
## 5. Best-practice interpretation  
  
### SDK  
Use when:  
- imported by Python code  
- reusable across projects  
- contract-first  
- testable as a library  
  
### Service  
Use when:  
- deployed independently  
- exposes API or worker behavior  
- owns operational lifecycle  
  
### App  
Use when:  
- user interacts with it directly  
- it hosts runtime or UI behavior  
  
### Engine  
Use when:  
- focused on processing logic  
- often hidden behind SDK/service layer  
  
### Store / Registry  
Use when:  
- persistence and lookup are primary purpose  
  
## 6. My recommendation for your project  
  
Use this structure in the URD:  
  
1. Platform applications  
   - adk_agent_app  
   - api_app  
   - reviewer_app  
  
2. Core services  
   - workflow_service  
   - approval_service  
   - registry_service  
   - memory_service  
   - knowledge_service  
   - rerun_service  
  
3. Reusable SDKs  
   - governance_sdk  
   - workflow_sdk  
   - registry_sdk  
   - observability_sdk  
   - all ECL domain SDKs  
   - manifest_sdk  
   - repro_sdk  
   - packaging_sdk  
   - memory_sdk  
   - knowledge_sdk  
  
4. Infrastructure adapters  
   - temporal_adapter  
   - s3_adapter  
   - cml_adapter  
   - gcp_adapter  
  
5. Storage components  
   - artifact_store  
   - metadata_store  
   - memory_store  
   - knowledge_store  
   - model_registry  
  
## 7. Recommended rename examples  
  
Old:  
- temporal_app  
  
Better:  
- workflow_service  
or  
- temporal_runtime  
  
Old:  
- api_app  
  
This is okay, but if backend-only:  
- api_service  
  
Old:  
- rag_sdk  
  
Better:  
- retrieval_engine  
or  
- retrieval_sdk  
or  
- knowledge_retrieval_sdk  
  
My preference:  
- keep `rag_sdk` out of the formal architecture name  
- use `knowledge_retrieval_sdk` if it is a library  
- use `retrieval_engine` if it is an internal processing component  
  
## 8. Suggested final naming standard  
  
Preferred final names:  
  
Applications:  
- adk_agent_app  
- api_app  
- reviewer_app  
  
Services:  
- workflow_service  
- approval_service  
- registry_service  
- memory_service  
- knowledge_service  
- rerun_service  
  
SDKs:  
- governance_sdk  
- workflow_sdk  
- registry_sdk  
- observability_sdk  
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
- reporting_sdk  
- docgen_sdk  
- manifest_sdk  
- repro_sdk  
- packaging_sdk  
- memory_sdk  
- knowledge_sdk  
- knowledge_retrieval_sdk  
  
Adapters:  
- temporal_adapter  
- s3_adapter  
- cml_adapter  
- gcp_adapter  
  
Stores:  
- artifact_store  
- metadata_store  
- memory_store  
- knowledge_store  
- model_registry  
