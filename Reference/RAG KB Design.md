# RAG KB Design  
  
====================================================================  
USER REQUIREMENT DOCUMENT (URD)  
GROWING KNOWLEDGE BASE AND TOKEN-THRIFTY RAG ARCHITECTURE  
FOR ENTERPRISE AGENTIC AI MODEL LIFECYCLE PLATFORM  
IN CML WITH S3 ACCESS  
====================================================================  
  
Project Name : Knowledge and RAG Platform for Agentic Model Lifecycle  
Version      : 1.0  
Date         : 2026-03-16  
Prepared For : Model Development, Model Validation, Governance,  
               Audit, Technology, Portfolio Analytics, Risk Methodology  
  
====================================================================  
1. PURPOSE  
====================================================================  
  
This document defines the requirements for a growing knowledge base  
and Retrieval-Augmented Generation (RAG) architecture to support an  
enterprise agentic AI platform for model lifecycle automation.  
  
The solution shall work in a CML environment with S3 access and shall  
be optimized for:  
- governed knowledge growth across projects  
- reuse of institutional, domain, project, and session knowledge  
- low-noise retrieval  
- strict token efficiency  
- strong linkage to workflow state, artifacts, findings, and decisions  
- support for model development, validation, governance, monitoring,  
  remediation, and documentation workflows  
  
The architecture shall be designed to be token-thrifty and suitable  
for practical use in enterprise environments where context-window  
efficiency and cost control are important.  
  
====================================================================  
2. OBJECTIVES  
====================================================================  
  
The knowledge and RAG platform shall:  
  
1. Provide a growing multi-layer knowledge base across all projects.  
2. Separate global, domain, project, and session knowledge.  
3. Support exact structured lookup and semantic retrieval together.  
4. Reduce token waste through scoped retrieval and compact summaries.  
5. Support development, validation, governance, monitoring, and  
   documentation use cases.  
6. Work inside CML with access to S3-backed storage.  
7. Preserve traceability from knowledge objects to source artifacts,  
   findings, and decisions.  
8. Support promotion of reusable knowledge from project level to  
   domain or global level.  
9. Prevent low-quality, stale, or superseded knowledge from polluting  
   retrieval.  
10. Provide a future-proof base for agentic memory and institutional  
    learning.  
  
====================================================================  
3. BACKGROUND AND PROBLEM STATEMENT  
====================================================================  
  
Agentic AI workflows in model lifecycle management require access to  
multiple forms of knowledge, including:  
- methodology notes  
- policy interpretations  
- development decisions  
- selected candidate version rationale  
- validation findings  
- remediation outcomes  
- committee conditions  
- monitoring outcomes  
- historical lessons learned  
- reusable code and documentation patterns  
  
A naive approach that dumps all documents and artifacts into a single  
vector store produces:  
- noisy retrieval  
- poor precision  
- repeated token waste  
- weak traceability  
- stale or conflicting results  
- reduced trust  
  
A more robust architecture is needed that:  
- organizes knowledge by scope and reuse value  
- separates exact structured facts from semantic summaries  
- grows naturally through workflow activity  
- supports compact retrieval suitable for token-thrifty operation  
  
====================================================================  
4. SCOPE  
====================================================================  
  
4.1 In Scope  
--------------------------------------------------------------------  
The solution shall cover:  
  
- enterprise knowledge object model  
- layered knowledge architecture  
- structured registry layer  
- semantic retrieval layer  
- ingestion pipelines  
- event-driven knowledge harvesting  
- promotion workflow for reusable knowledge  
- role/domain/stage-aware retrieval  
- retrieval optimization for token thrift  
- summarization strategy  
- CML deployment considerations  
- S3-backed persistence  
- governance and quality controls  
- support for development, validation, governance, monitoring, and  
  documentation use cases  
  
4.2 Out of Scope  
--------------------------------------------------------------------  
Unless explicitly approved, the following are out of scope:  
  
- fully automated internet crawling  
- unrestricted open-ended memory without governance  
- storing hidden chain-of-thought style reasoning  
- replacing structured registries with vector search only  
- autonomous knowledge promotion without controls  
- external cloud services that are not compatible with CML / S3  
  constraints  
  
====================================================================  
5. DESIGN PRINCIPLES  
====================================================================  
  
The solution shall follow these principles:  
  
5.1 Layered Knowledge  
--------------------------------------------------------------------  
Knowledge shall be organized by scope and reuse level rather than one  
flat store.  
  
5.2 Structured + Semantic Duality  
--------------------------------------------------------------------  
The platform shall combine structured registries for exact facts with  
semantic retrieval for meaning-based search.  
  
5.3 Event-Driven Growth  
--------------------------------------------------------------------  
Knowledge shall grow from workflow events, decisions, findings,  
selections, and curated documents.  
  
5.4 Traceability  
--------------------------------------------------------------------  
Every knowledge object shall be linkable to source artifacts, runs,  
reviews, findings, or decisions.  
  
5.5 Token Thrift  
--------------------------------------------------------------------  
Retrieval shall be selective, filtered, compact, and optimized for low  
token consumption.  
  
5.6 Quality over Quantity  
--------------------------------------------------------------------  
Only high-value, classified, and governable knowledge shall be  
promoted into reusable memory layers.  
  
5.7 Reusability with Boundaries  
--------------------------------------------------------------------  
Knowledge shall support promotion from session to project, project to  
domain, and domain to global, but not all knowledge shall be promoted.  
  
5.8 Future Proofing  
--------------------------------------------------------------------  
The architecture shall support future graph reasoning, benchmark  
comparison, and richer memory management without redesign.  
  
====================================================================  
6. TARGET ENVIRONMENT  
====================================================================  
  
6.1 Runtime Environment  
--------------------------------------------------------------------  
The platform shall be designed to run in CML.  
  
6.2 Storage Environment  
--------------------------------------------------------------------  
The platform shall use S3-accessible storage for:  
- raw documents  
- chunked knowledge payloads  
- summaries  
- embeddings  
- exported registries  
- manifests  
- audit snapshots where applicable  
  
6.3 Execution Constraints  
--------------------------------------------------------------------  
The design shall assume:  
- enterprise-controlled environment  
- limited outbound connectivity  
- preference for Python-based implementation  
- need for reproducible and supportable deployment  
- need for compatibility with existing SDK and workflow platform  
  
6.4 Language and Tooling Fit  
--------------------------------------------------------------------  
The implementation shall be optimized for Python and PySpark-friendly  
ecosystems, while remaining efficient in notebook and service modes.  
  
====================================================================  
7. KNOWLEDGE ARCHITECTURE  
====================================================================  
  
7.1 Layered Knowledge Model  
--------------------------------------------------------------------  
The knowledge architecture shall have four main tiers:  
  
Tier 1: Global Institutional Knowledge  
Tier 2: Domain Knowledge  
Tier 3: Project Knowledge  
Tier 4: Session / Interaction Memory  
  
7.2 Tier 1 – Global Institutional Knowledge  
--------------------------------------------------------------------  
Purpose:  
Store reusable knowledge relevant across the enterprise platform.  
  
Examples:  
- policy interpretations  
- common methodology standards  
- validation SOP  
- governance SOP  
- standard review templates  
- regulator themes  
- accepted remediation patterns  
- glossary  
- common reporting wording  
- standard metric interpretation notes  
  
Characteristics:  
- high governance  
- strong review and approval  
- reusable across domains and projects  
- lower churn than project memory  
  
7.3 Tier 2 – Domain Knowledge  
--------------------------------------------------------------------  
Purpose:  
Store reusable knowledge for a specific model family or domain.  
  
Examples:  
- scorecard best practices  
- binning guidance  
- WoE / IV interpretation notes  
- time series residual diagnostic guidance  
- ECL overlay patterns  
- LGD cure / severity practices  
- validation patterns by model family  
- domain artifact dictionary  
  
Characteristics:  
- reusable within domain  
- curated with domain ownership  
- moderately dynamic  
  
7.4 Tier 3 – Project Knowledge  
--------------------------------------------------------------------  
Purpose:  
Store project-specific rationale, assumptions, decisions, and  
summaries.  
  
Examples:  
- selected model rationale  
- selected binning rationale  
- project assumptions  
- issue summaries  
- validation findings  
- final conclusions  
- committee conditions  
- project-specific thresholds  
- meeting and review summaries  
  
Characteristics:  
- high relevance within one project  
- low reuse outside project unless promoted  
- supports resume, continuity, and project memory  
  
7.5 Tier 4 – Session / Interaction Memory  
--------------------------------------------------------------------  
Purpose:  
Store short-lived but useful interaction context.  
  
Examples:  
- latest user edits  
- current review context  
- temporary comparison summaries  
- open questions  
- pending preview result  
- latest review comments  
  
Characteristics:  
- highly dynamic  
- short-lived  
- not automatically reusable  
- may later be summarized into project knowledge  
  
====================================================================  
8. KNOWLEDGE OBJECT MODEL  
====================================================================  
  
8.1 Purpose  
--------------------------------------------------------------------  
All knowledge in the platform shall be represented as governed  
knowledge objects rather than raw undifferentiated text only.  
  
8.2 Core Knowledge Object Structure  
--------------------------------------------------------------------  
Each knowledge object should support:  
  
- knowledge_id  
- knowledge_type  
- scope  
- domain  
- project_id if applicable  
- run_id if applicable  
- stage_name if applicable  
- title  
- short_summary  
- detailed_summary  
- full_text_ref or inline_text  
- tags  
- source_refs  
- linked_artifact_ids  
- linked_review_ids  
- linked_decision_ids  
- linked_finding_ids  
- linked_conclusion_ids  
- created_by  
- created_timestamp  
- effective_status  
- promotion_status  
- quality_status  
- superseded_flag  
- last_reviewed_timestamp  
  
8.3 Knowledge Types  
--------------------------------------------------------------------  
The platform shall support knowledge types such as:  
  
- policy  
- methodology  
- decision  
- artifact_summary  
- finding  
- remediation  
- validation_conclusion  
- monitoring_outcome  
- committee_feedback  
- regulatory_feedback  
- code_pattern  
- template  
- glossary  
- lesson_learned  
- interaction_summary  
- benchmark_pattern  
  
8.4 Scope Classification  
--------------------------------------------------------------------  
Each object shall be classified as one of:  
  
- session_only  
- project_only  
- domain_reusable  
- global_reusable  
  
8.5 Quality Status  
--------------------------------------------------------------------  
Each object shall support statuses such as:  
  
- draft  
- captured  
- reviewed  
- approved_for_project_use  
- approved_for_domain_reuse  
- approved_for_global_reuse  
- superseded  
- archived  
  
====================================================================  
9. DUAL-STORE DESIGN  
====================================================================  
  
9.1 Structured Registry Layer  
--------------------------------------------------------------------  
Purpose:  
Store exact facts, identifiers, relationships, and current status.  
  
Examples of structured records:  
- project registry  
- run registry  
- artifact registry  
- decision registry  
- review registry  
- candidate version registry  
- validation finding registry  
- validation conclusion registry  
- knowledge registry metadata  
  
Use cases:  
- exact lookup  
- lineage traversal  
- dependency resolution  
- current-state validation  
- governance checks  
  
9.2 Semantic Retrieval Layer  
--------------------------------------------------------------------  
Purpose:  
Store semantic summaries and retrievable chunks for meaning-based  
search.  
  
Examples:  
- policy note chunks  
- methodology summaries  
- decision rationale summaries  
- validation findings summaries  
- review summaries  
- reusable lessons learned  
- committee feedback summaries  
  
Use cases:  
- semantic retrieval  
- prompt grounding  
- related-case search  
- documentation drafting  
- challenge generation  
  
9.3 Combined Retrieval Strategy  
--------------------------------------------------------------------  
RAG shall not rely solely on semantic retrieval.  
  
Preferred query pattern:  
1. retrieve exact structured context first  
2. retrieve scoped semantic summaries second  
3. rerank and compress  
4. inject compact context to the agent  
  
====================================================================  
10. EVENT-DRIVEN KNOWLEDGE GROWTH  
====================================================================  
  
10.1 Principle  
--------------------------------------------------------------------  
The knowledge base shall grow through workflow events and curated  
ingestion rather than only manual document loading.  
  
10.2 Material Workflow Events for Knowledge Harvesting  
--------------------------------------------------------------------  
Knowledge objects should be created or updated from events such as:  
  
- candidate version selected  
- model selected  
- validation finding created  
- validation conclusion finalized  
- remediation closed  
- deployment readiness approved / rejected  
- monitoring breach disposition finalized  
- annual review finalized  
- major override approved  
- committee condition recorded  
- methodology challenge recorded  
  
10.3 Event-Driven Harvesting Flow  
--------------------------------------------------------------------  
For each material event, the system shall:  
  
1. identify the event as knowledge-worthy  
2. gather exact structured facts  
3. generate short and detailed summaries  
4. classify scope and reusability  
5. link to source objects  
6. store in semantic layer  
7. register metadata in structured layer  
  
10.4 Example  
--------------------------------------------------------------------  
If a binning version is finalized:  
- create a decision_summary knowledge object  
- store short summary of why version B was selected  
- link to review_id, decision_id, artifact_ids  
- classify as project_only initially  
  
====================================================================  
11. INGESTION PIPELINES  
====================================================================  
  
11.1 Document Ingestion Pipeline  
--------------------------------------------------------------------  
Purpose:  
Ingest policies, methodology notes, templates, documentation, and  
reference files.  
  
Steps:  
- read source from S3 or supported repository  
- parse text  
- chunk intelligently  
- tag and classify  
- summarize  
- embed  
- store chunked semantic payloads  
- register metadata  
  
11.2 Workflow Event Ingestion Pipeline  
--------------------------------------------------------------------  
Purpose:  
Convert workflow outcomes into governed knowledge objects.  
  
Steps:  
- listen to material event types  
- enrich with registry data  
- summarize  
- classify scope  
- embed summary  
- register object and links  
  
11.3 Human-Curated Ingestion Pipeline  
--------------------------------------------------------------------  
Purpose:  
Allow curated lessons, approved notes, and promoted knowledge to enter  
the KB.  
  
Steps:  
- submit curated knowledge  
- review / approve  
- classify scope  
- register and embed  
- publish for reuse  
  
11.4 Validation Knowledge Ingestion Pipeline  
--------------------------------------------------------------------  
Purpose:  
Capture validation findings, conclusions, challenge notes, and  
accepted remediation patterns.  
  
Steps:  
- detect validation object lifecycle event  
- summarize finding / conclusion / remediation  
- classify project or domain reuse status  
- link to evidence  
- store and register  
  
====================================================================  
12. SUMMARIZATION STRATEGY  
====================================================================  
  
12.1 Token-Thrifty Principle  
--------------------------------------------------------------------  
The system shall avoid sending full raw documents whenever a compact  
summary is sufficient.  
  
12.2 Required Summary Levels  
--------------------------------------------------------------------  
For major objects, the system should maintain:  
  
- short_summary  
- detailed_summary  
- full_text_ref  
  
12.3 Summary Usage  
--------------------------------------------------------------------  
- short_summary for retrieval ranking and compact prompt grounding  
- detailed_summary for richer context when needed  
- full_text only when drill-down is required  
  
12.4 Summary Targets  
--------------------------------------------------------------------  
Create summaries for:  
- artifacts  
- reviews  
- decisions  
- findings  
- conclusions  
- committee feedback  
- remediation outcomes  
- annual review outcomes  
  
12.5 Compression Rules  
--------------------------------------------------------------------  
Summaries should:  
- remove repetition  
- preserve key metrics and decisions  
- keep linked references  
- avoid long prose when bullet-style structured summaries are enough  
- include only material facts  
  
====================================================================  
13. TOKEN-THRIFT OPTIMIZATION REQUIREMENTS  
====================================================================  
  
13.1 General Principle  
--------------------------------------------------------------------  
The solution shall optimize retrieval and prompt construction to  
minimize unnecessary token usage.  
  
13.2 Retrieval Scoping  
--------------------------------------------------------------------  
Every retrieval should support filters such as:  
- scope  
- role  
- domain  
- project_id  
- model_family  
- stage_name  
- approval status  
- quality status  
- superseded flag  
- recency  
  
13.3 Compact Retrieval First  
--------------------------------------------------------------------  
The platform shall prefer:  
- short summaries first  
- detailed summaries second  
- full chunks only when necessary  
  
13.4 Top-K Discipline  
--------------------------------------------------------------------  
The system shall use small and controlled retrieval windows rather  
than broad retrieval by default.  
  
13.5 Prompt Packaging  
--------------------------------------------------------------------  
The RAG layer shall package retrieved context in compact structured  
format such as:  
- exact facts  
- top summaries  
- linked IDs  
- unresolved warnings  
- key evidence only  
  
13.6 Avoid Redundant Retrieval  
--------------------------------------------------------------------  
The platform shall cache and reuse already selected compact context  
within a run or interaction when safe.  
  
13.7 Query Intent Routing  
--------------------------------------------------------------------  
Different query intents shall retrieve different context packages.  
  
Examples:  
- explanation query -> short summary + 1 detailed rationale  
- validation challenge query -> findings + evidence gaps + policy note  
- model selection query -> candidate comparison summaries + selected  
  version state  
- documentation drafting query -> approved wording + project summary +  
  conclusion summary  
  
13.8 Long Artifact Handling  
--------------------------------------------------------------------  
Long documents shall be chunked and summarized hierarchically.  
The system should avoid passing many large chunks to the LLM when  
summary objects already exist.  
  
13.9 RAG Output Budgeting  
--------------------------------------------------------------------  
The retrieval layer should support token budgets per query mode.  
  
Examples:  
- micro context mode  
- standard context mode  
- deep review mode  
  
13.10 No Raw Dumping Rule  
--------------------------------------------------------------------  
The system shall not dump entire retrieved objects into prompts unless  
explicitly necessary.  
  
====================================================================  
14. ROLE-AWARE RETRIEVAL  
====================================================================  
  
14.1 Principle  
--------------------------------------------------------------------  
Different roles shall retrieve different knowledge.  
  
14.2 Developer Retrieval  
--------------------------------------------------------------------  
Developers should retrieve:  
- project decisions  
- project artifacts  
- domain methodology notes  
- prior accepted project rationale  
- selected code patterns  
- active stage guidance  
  
14.3 Validator Retrieval  
--------------------------------------------------------------------  
Validators should retrieve:  
- validation config pack  
- findings  
- evidence completeness notes  
- challenge patterns  
- policy interpretations  
- model fitness precedents  
- domain validation lessons  
  
14.4 Governance Retrieval  
--------------------------------------------------------------------  
Governance users should retrieve:  
- policy packs  
- approval conditions  
- unresolved issues  
- committee conditions  
- summary packs only  
  
14.5 Documentation Retrieval  
--------------------------------------------------------------------  
Documentation flows should retrieve:  
- approved wording templates  
- project summaries  
- decisions  
- findings  
- conclusions  
- committee wording patterns  
  
14.6 Monitoring Retrieval  
--------------------------------------------------------------------  
Monitoring flows should retrieve:  
- prior monitoring outcomes  
- threshold definitions  
- remediation actions  
- annual review summaries  
  
====================================================================  
15. STAGE-AWARE RETRIEVAL  
====================================================================  
  
15.1 Principle  
--------------------------------------------------------------------  
Retrieval shall be stage-aware to improve precision and reduce tokens.  
  
15.2 Examples  
--------------------------------------------------------------------  
Coarse Classing Review:  
- current variable artifact summary  
- candidate version summaries  
- scorecard domain note on monotonicity and support  
- project-specific prior edits on same variable if any  
  
Binning Version Selection:  
- candidate version comparison summaries  
- scorecard policy thresholds  
- prior project decision patterns  
- unresolved warnings  
  
Validation Conclusion:  
- active findings  
- evidence completeness status  
- validation config pack  
- fitness framework summary  
- similar prior conclusion patterns in the same domain  
  
Deployment Readiness:  
- unresolved governance issues  
- validation conclusion  
- implementation evidence  
- prior conditions  
- required sign-off rules  
  
====================================================================  
16. PROMOTION WORKFLOW  
====================================================================  
  
16.1 Principle  
--------------------------------------------------------------------  
Knowledge shall move upward in scope through explicit promotion.  
  
16.2 Promotion Path  
--------------------------------------------------------------------  
Typical path:  
- session_only  
- project_only  
- domain_reusable  
- global_reusable  
  
16.3 Promotion Rules  
--------------------------------------------------------------------  
Knowledge should be promoted only if:  
- it is accurate  
- it has clear source linkage  
- it is not superseded  
- it is reusable  
- it has sufficient review / approval status  
  
16.4 Promotion Candidates  
--------------------------------------------------------------------  
Good promotion candidates include:  
- validated methodology lessons  
- reusable validation challenge patterns  
- approved remediation patterns  
- recurring regulator concern summaries  
- approved documentation wording  
- accepted benchmark patterns  
  
16.5 Non-Promotion Candidates  
--------------------------------------------------------------------  
Do not auto-promote:  
- temporary experiments  
- superseded candidate rationale  
- raw chat noise  
- incomplete drafts  
- unresolved findings  
  
====================================================================  
17. KNOWLEDGE QUALITY CONTROL  
====================================================================  
  
17.1 Quality Requirements  
--------------------------------------------------------------------  
The knowledge layer shall support:  
  
- owner  
- source traceability  
- superseded flag  
- last reviewed date  
- quality status  
- approval status  
- reuse approval level  
  
17.2 Superseded Knowledge Handling  
--------------------------------------------------------------------  
Superseded knowledge shall not be retrieved by default.  
  
17.3 Staleness Controls  
--------------------------------------------------------------------  
The platform should support warnings for stale knowledge objects.  
  
17.4 Duplicate and Near-Duplicate Control  
--------------------------------------------------------------------  
The platform should reduce duplicate semantic entries where possible.  
  
====================================================================  
18. KNOWLEDGE GOVERNANCE  
====================================================================  
  
18.1 Governance Principle  
--------------------------------------------------------------------  
Knowledge that influences decisions shall be governed.  
  
18.2 Governance Controls  
--------------------------------------------------------------------  
The platform shall support:  
- ownership  
- approval level  
- promotion rights  
- archival rules  
- supersession rules  
- visibility rules by role  
  
18.3 Role Separation  
--------------------------------------------------------------------  
Development-generated knowledge shall not automatically become  
validation-approved or global reusable knowledge.  
  
====================================================================  
19. CML AND S3 IMPLEMENTATION REQUIREMENTS  
====================================================================  
  
19.1 CML Compatibility  
--------------------------------------------------------------------  
The solution shall be implementable in a CML environment.  
  
19.2 S3 Usage  
--------------------------------------------------------------------  
S3 shall be used for:  
- source documents  
- chunk payloads  
- embedding payloads  
- summary payloads  
- export snapshots  
- manifests  
  
19.3 Metadata Persistence  
--------------------------------------------------------------------  
Structured registry metadata may be stored in:  
- relational database  
- lightweight metadata store  
- object-backed metadata files  
depending on environment constraints  
  
19.4 Local Processing Strategy  
--------------------------------------------------------------------  
Chunking, summarization, tagging, and embedding orchestration shall be  
performable from CML jobs or services.  
  
19.5 Access Pattern  
--------------------------------------------------------------------  
The design shall minimize repeated large reads from S3 by using:  
- manifests  
- compact metadata  
- caching where appropriate  
- precomputed summaries  
  
====================================================================  
20. PACKAGE / SDK DESIGN  
====================================================================  
  
20.1 Proposed Packages  
--------------------------------------------------------------------  
The architecture should introduce at minimum:  
  
- knowledge_sdk  
- rag_sdk  
  
20.2 knowledge_sdk Responsibilities  
--------------------------------------------------------------------  
- knowledge object creation  
- knowledge classification  
- promotion workflow  
- governance states  
- metadata registry integration  
- summary storage linkage  
  
Suggested modules:  
- knowledge_object  
- knowledge_registry  
- promotion_manager  
- quality_manager  
- status_manager  
- knowledge_linker  
- knowledge_export  
  
20.3 rag_sdk Responsibilities  
--------------------------------------------------------------------  
- chunking  
- embedding orchestration  
- semantic retrieval  
- reranking  
- retrieval filters  
- prompt context packaging  
- token budget control  
  
Suggested modules:  
- chunker  
- embedder  
- retriever  
- reranker  
- query_router  
- context_compressor  
- prompt_packager  
- token_budget_manager  
  
20.4 Integration with Existing Platform  
--------------------------------------------------------------------  
The solution shall integrate with:  
- workflowsdk  
- artifactsdk  
- observabilitysdk  
- auditsdk  
- validationsdk  
- reporting_sdk  
- domain SDKs  
  
====================================================================  
21. QUERY AND RETRIEVAL FLOW  
====================================================================  
  
21.1 Standard Retrieval Flow  
--------------------------------------------------------------------  
1. identify current role/domain/stage/project  
2. retrieve exact structured context  
3. query semantic KB with filters  
4. rerank results  
5. compress into compact context pack  
6. return to agent / skill layer  
  
21.2 Context Pack Output  
--------------------------------------------------------------------  
The retrieval layer should return:  
- exact facts  
- top short summaries  
- selected detailed summaries if needed  
- linked source IDs  
- unresolved warnings or caveats  
- token budget usage metadata  
  
====================================================================  
22. EXAMPLE KNOWLEDGE FLOWS  
====================================================================  
  
22.1 Coarse Classing Finalization  
--------------------------------------------------------------------  
Input events:  
- user finalizes coarse bins  
- review closed  
- artifact registered  
  
Outputs:  
- project knowledge object: final coarse classing rationale  
- linked artifact summary  
- optional domain lesson candidate if reusable  
  
22.2 Validation Conclusion  
--------------------------------------------------------------------  
Input events:  
- validation findings finalized  
- conclusion approved  
  
Outputs:  
- project knowledge object: validation conclusion summary  
- domain lesson candidate: recurring weakness pattern if reusable  
  
22.3 Monitoring Breach Resolution  
--------------------------------------------------------------------  
Input events:  
- monitoring breach reviewed  
- remediation action selected  
  
Outputs:  
- project monitoring outcome summary  
- domain remediation pattern candidate if repeatable  
  
====================================================================  
23. SECURITY AND ACCESS  
====================================================================  
  
23.1 Principle  
--------------------------------------------------------------------  
Knowledge visibility shall be role-aware and scope-aware.  
  
23.2 Access Controls  
--------------------------------------------------------------------  
The solution shall support restrictions by:  
- role  
- project  
- domain  
- approval status  
- sensitivity flag  
  
23.3 Write Controls  
--------------------------------------------------------------------  
Only authorized processes or roles shall promote knowledge to  
higher-scope layers.  
  
====================================================================  
24. NON-FUNCTIONAL REQUIREMENTS  
====================================================================  
  
24.1 Modularity  
--------------------------------------------------------------------  
The solution shall be modular and separable into SDKs / services.  
  
24.2 Token Efficiency  
--------------------------------------------------------------------  
The solution shall optimize for low token usage by default.  
  
24.3 Traceability  
--------------------------------------------------------------------  
The solution shall preserve source linkage and lineage.  
  
24.4 Extensibility  
--------------------------------------------------------------------  
The knowledge model shall support future categories and graph  
relations.  
  
24.5 Maintainability  
--------------------------------------------------------------------  
The system shall support governed updates and pruning.  
  
24.6 Reliability  
--------------------------------------------------------------------  
Knowledge ingestion and retrieval shall support retry and recovery.  
  
24.7 Quality  
--------------------------------------------------------------------  
The platform shall minimize stale, duplicate, and superseded retrieval.  
  
====================================================================  
25. IMPLEMENTATION PHASES  
====================================================================  
  
25.1 Phase 1  
--------------------------------------------------------------------  
Build:  
- knowledge object model  
- structured registry metadata  
- project/domain/global/session scope model  
- document ingestion pipeline  
- workflow event ingestion pipeline  
- short and detailed summary generation  
- scoped retrieval filters  
- compact prompt packaging  
- CML + S3 storage integration  
- token budget manager  
- initial knowledge_sdk  
- initial rag_sdk  
  
25.2 Phase 2  
--------------------------------------------------------------------  
Add:  
- promotion workflow  
- quality states  
- superseded handling  
- validation knowledge capture  
- role-aware retrieval  
- stage-aware retrieval  
- caching and context reuse  
- retrieval analytics  
  
25.3 Phase 3  
--------------------------------------------------------------------  
Add:  
- graph-style linkage enhancements  
- benchmark knowledge layer  
- recurring issue pattern mining  
- institutional lessons dashboard  
- richer remediation pattern library  
  
====================================================================  
26. SUCCESS CRITERIA  
====================================================================  
  
The implementation shall be considered successful when:  
  
1. knowledge can be stored across global, domain, project, and session  
   layers  
2. workflow events naturally grow the knowledge base  
3. structured and semantic retrieval work together  
4. retrieval is precise and token-thrifty  
5. role-aware and stage-aware retrieval improves relevance  
6. validation, governance, development, and monitoring use cases are  
   all supported  
7. CML deployment with S3 access is practical  
8. reusable knowledge can be promoted safely  
9. stale and superseded knowledge does not dominate retrieval  
10. agents can answer with compact, relevant, and traceable context  
  
====================================================================  
27. APPENDIX – PROPOSED REQUIREMENT IDS  
====================================================================  
  
KB-FR-001  
Support a layered growing knowledge base with global, domain, project,  
and session scopes.  
  
KB-FR-002  
Support governed knowledge objects with structured metadata and  
source linkage.  
  
KB-FR-003  
Support structured registry plus semantic retrieval dual-store  
architecture.  
  
KB-FR-004  
Support document ingestion, workflow event ingestion, and human-  
curated ingestion pipelines.  
  
KB-FR-005  
Support event-driven knowledge harvesting from material workflow  
events.  
  
KB-FR-006  
Support promotion workflow across knowledge scopes.  
  
KB-FR-007  
Support role-aware retrieval.  
  
KB-FR-008  
Support stage-aware retrieval.  
  
KB-FR-009  
Support compact summary levels and token-thrifty context packaging.  
  
KB-FR-010  
Support CML-compatible execution with S3-backed storage.  
  
KB-FR-011  
Support knowledge quality states, supersession, and reuse approval.  
  
KB-FR-012  
Support knowledge_sdk and rag_sdk aligned with the wider platform.  
  
KB-FR-013  
Support validation-specific knowledge capture and retrieval.  
  
KB-NFR-001  
The architecture shall be token-thrifty by default.  
  
KB-NFR-002  
The architecture shall be modular and future-proof.  
  
KB-NFR-003  
The architecture shall preserve traceability and governance.  
  
====================================================================  
END OF URD  
====================================================================  
