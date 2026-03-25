# Data Prep SDK  
  
====================================================================  
USER REQUIREMENT DOCUMENT (URD)  
DATA PREPARATION SDK  
FOR CREDIT RISK MODELING AND AGENTIC AI WORKFLOW AUTOMATION  
====================================================================  
  
Project Name : dataprepsdk  
Version      : 1.0  
Date         : 2026-03-16  
Prepared For : Model Development, Model Validation, Governance,  
               Audit, Technology, Portfolio Analytics, Risk Methodology  
  
====================================================================  
1. PURPOSE  
====================================================================  
  
This document defines the requirements for a top-of-the-class Data  
Preparation SDK designed for credit risk modeling and seamless use by  
agentic AI workflows.  
  
The SDK shall provide a governed, config-driven, reusable, and  
template-based framework to prepare model-ready training datasets for  
different analytical data structures including:  
  
- cross-sectional data  
- panel / longitudinal data  
- time series data  
- event / spell data  
- cohort-based data  
- behavioral snapshot data  
- account-customer linked data  
- transaction-aggregated data  
- macroeconomic feature data  
- hybrid modeling datasets  
  
The SDK shall support both:  
- pre-prepared source data  
- raw / semi-prepared source data requiring lineage-driven preparation  
  
The SDK shall be designed so that:  
- agents can invoke it deterministically  
- users can define lineage and preparation behavior through config  
- output datasets are standardized, traceable, reproducible, and ready  
  for downstream modeling, validation, monitoring, and reporting  
  
====================================================================  
2. OBJECTIVES  
====================================================================  
  
The SDK shall:  
  
1. Standardize data preparation for credit risk modeling workflows.  
2. Support multiple data structures used in credit risk use cases.  
3. Allow config-driven lineage and transformation rules.  
4. Allow agentic AI to prepare training data through deterministic  
   function calls.  
5. Produce governed, auditable, and reproducible outputs.  
6. Support standard templates only, to preserve consistency.  
7. Reduce manual and repeated preparation work across projects.  
8. Support future extension across scorecard, IFRS 9 ECL, LGD, PD,  
   EAD, SICR, stress testing, monitoring, and validation use cases.  
9. Produce outputs that are top-of-the-class in usability,  
   traceability, modularity, and future-proof design.  
10. Integrate cleanly with workflow automation, HITL, validation, and  
    knowledge / RAG layers.  
  
====================================================================  
3. BACKGROUND AND PROBLEM STATEMENT  
====================================================================  
  
Credit risk modeling projects often spend significant effort on data  
preparation. Common problems include:  
  
- inconsistent dataset definitions across projects  
- non-standardized training sample creation  
- manual joins and transformations  
- unclear lineage from raw source to final model dataset  
- repeated code for common preparation logic  
- difficult reproduction of prior datasets  
- ambiguity in panel, time series, and cross-sectional sample logic  
- weak controls on target generation and observation window logic  
- inconsistent treatment of customer-account hierarchies  
- lack of deterministic interfaces for agentic AI  
  
A standard, template-based, config-driven SDK is required so that:  
- the same logic can be reused  
- users can define lineage through config  
- agents can invoke preparation steps reliably  
- datasets remain traceable and governed  
  
====================================================================  
4. SCOPE  
====================================================================  
  
4.1 In Scope  
--------------------------------------------------------------------  
The SDK shall cover:  
  
- dataset definition  
- source ingestion contract  
- lineage-driven preparation  
- standard preparation templates  
- sample construction by data structure  
- observation window generation  
- target window generation  
- train / test / oot split preparation  
- cohort construction  
- panel flattening / expansion  
- time-series sequence preparation  
- feature alignment  
- entity-level / account-level / contract-level integration  
- macroeconomic merge preparation  
- target alignment  
- leakage checks  
- snapshot generation  
- metadata and lineage output  
- quality checks at preparation stage  
- deterministic agent-safe interfaces  
  
4.2 Supported Data Structures  
--------------------------------------------------------------------  
The SDK shall support at minimum:  
  
- cross-sectional  
- panel / longitudinal  
- time series  
- spell / event-history  
- cohort snapshot  
- repeated snapshot by month / quarter  
- hierarchical linked data  
- macro-augmented supervised data  
  
4.3 Out of Scope  
--------------------------------------------------------------------  
Unless explicitly approved, the following are out of scope:  
  
- unrestricted user-defined arbitrary transformation scripting inside  
  the template execution path  
- non-template free-form preparation flows  
- direct replacement of full ETL platform  
- ungoverned ad hoc data wrangling with no lineage capture  
- model fitting logic itself  
  
====================================================================  
5. DESIGN PRINCIPLES  
====================================================================  
  
The SDK shall follow these principles:  
  
5.1 Template-Driven  
--------------------------------------------------------------------  
Preparation shall be based on standard templates rather than unlimited  
free-form pipelines.  
  
5.2 Config-Driven  
--------------------------------------------------------------------  
Users shall define preparation behavior through configuration,  
especially lineage, mapping, observation logic, split rules, and  
template parameters.  
  
5.3 Deterministic  
--------------------------------------------------------------------  
The SDK shall expose deterministic functions suitable for agentic AI  
tool invocation.  
  
5.4 Traceable  
--------------------------------------------------------------------  
Every output dataset shall be linked back to:  
- source datasets  
- preparation config  
- template used  
- transformation steps  
- generated target rules  
- sample selection logic  
  
5.5 Reusable  
--------------------------------------------------------------------  
The same template framework shall support many credit risk use cases.  
  
5.6 Governed  
--------------------------------------------------------------------  
Only approved standard templates shall be supported in the governed  
execution path.  
  
5.7 Modular  
--------------------------------------------------------------------  
The SDK shall separate ingestion, lineage, sampling, alignment,  
targeting, splitting, and output packaging.  
  
5.8 Agent-Friendly  
--------------------------------------------------------------------  
Inputs and outputs shall be bounded, inspectable, and schema-driven.  
  
====================================================================  
6. TARGET USERS  
====================================================================  
  
The SDK shall support:  
  
- model developers  
- credit risk analysts  
- portfolio analytics users  
- model validators  
- data engineering support users  
- agentic AI orchestrators  
- workflow controllers  
- governance reviewers through metadata outputs  
  
====================================================================  
7. PRIMARY USE CASES  
====================================================================  
  
7.1 Credit Scorecard Development  
--------------------------------------------------------------------  
Prepare cross-sectional or snapshot-based supervised datasets at:  
- application date  
- observation month  
- behavioral snapshot month  
  
7.2 IFRS 9 PD Modeling  
--------------------------------------------------------------------  
Prepare panel / cohort / repeated snapshot datasets aligned to:  
- reporting date  
- origination date  
- performance window  
- forward-looking feature alignment  
  
7.3 LGD Modeling  
--------------------------------------------------------------------  
Prepare contract-level or default-event-aligned data with:  
- recovery aggregation  
- cure / non-cure segmentation  
- severity alignment  
- workout period logic  
  
7.4 EAD Modeling  
--------------------------------------------------------------------  
Prepare exposure utilization datasets with:  
- observation point  
- conversion horizon  
- facility characteristics  
- usage history aggregation  
  
7.5 SICR Assessment  
--------------------------------------------------------------------  
Prepare origination-vs-reporting comparison datasets with:  
- relative change fields  
- absolute threshold fields  
- stage comparison features  
  
7.6 Time Series / Macro Models  
--------------------------------------------------------------------  
Prepare time series modeling data with:  
- lag structures  
- differencing-ready output  
- aligned target horizons  
- train / validation / forecast partitions  
  
7.7 Validation and Reproduction  
--------------------------------------------------------------------  
Recreate a prior model dataset from config, template, and lineage  
reference.  
  
====================================================================  
8. STANDARD TEMPLATE STRATEGY  
====================================================================  
  
8.1 Principle  
--------------------------------------------------------------------  
The SDK shall support only approved standard templates in the  
governed path.  
  
8.2 Template Families  
--------------------------------------------------------------------  
The SDK shall support template families such as:  
  
- cross_sectional_training_template  
- panel_training_template  
- time_series_training_template  
- event_history_training_template  
- cohort_snapshot_template  
- repeated_snapshot_template  
- hierarchical_join_template  
- macro_merge_template  
- target_alignment_template  
- train_test_oot_split_template  
  
8.3 Template Governance  
--------------------------------------------------------------------  
Each template shall have:  
- template_id  
- template_name  
- template_version  
- supported domains  
- supported grain  
- required input contract  
- output contract  
- parameter schema  
- quality checks  
- lineage rules  
  
8.4 No Free-Form Bypass Rule  
--------------------------------------------------------------------  
Agentic execution shall not bypass the approved template framework in  
normal governed mode.  
  
====================================================================  
9. DATA GRAIN AND ENTITY SUPPORT  
====================================================================  
  
The SDK shall support data at different business grains including:  
  
- contract_reference  
- account_id  
- facility_id  
- application_id  
- entity_code / customer_id  
- customer-month  
- account-month  
- contract-month  
- default-event  
- observation date  
- reporting date  
- cohort date  
  
The SDK shall support controlled transformation between grains where  
defined by standard templates.  
  
====================================================================  
10. SOURCE DATA AND LINEAGE CONFIGURATION  
====================================================================  
  
10.1 Source Modes  
--------------------------------------------------------------------  
The SDK shall support two source modes:  
  
A. Pre-Prepared Source Mode  
The input source is already mostly prepared and only requires standard  
template application.  
  
B. Lineage-Driven Source Mode  
The SDK shall assemble final training data based on lineage config and  
source mappings defined by the user.  
  
10.2 Lineage Config Purpose  
--------------------------------------------------------------------  
The lineage configuration shall define:  
- source datasets  
- join keys  
- grain mapping  
- date alignment  
- feature source mapping  
- target source mapping  
- filtering rules  
- as-of logic  
- aggregation rules  
- split logic  
  
10.3 Lineage Config Principle  
--------------------------------------------------------------------  
Users may define preparation through config, but the execution path  
shall remain constrained to approved template logic.  
  
====================================================================  
11. DATA STRUCTURE-SPECIFIC REQUIREMENTS  
====================================================================  
  
11.1 Cross-Sectional Data  
--------------------------------------------------------------------  
The SDK shall support creation of single-observation-per-unit datasets.  
  
Examples:  
- application scorecard  
- annual borrower snapshot  
- one-row-per-customer snapshot  
  
Capabilities:  
- select observation date  
- align target horizon  
- merge static and derived features  
- handle one-row-per-entity output  
- generate train / test / oot partitions  
  
11.2 Panel / Longitudinal Data  
--------------------------------------------------------------------  
The SDK shall support repeated observations across time for the same  
entity.  
  
Examples:  
- customer-month PD dataset  
- account-month behavior dataset  
- reporting-month repeated snapshot  
  
Capabilities:  
- define panel entity  
- define time index  
- construct repeated observations  
- handle missing periods as configured  
- align lagged features  
- align future target window  
- support balanced / unbalanced panels  
  
11.3 Time Series Data  
--------------------------------------------------------------------  
The SDK shall support sequence-style and aggregate time series data.  
  
Examples:  
- macroeconomic forecast model  
- portfolio default rate time series  
- vintage / cohort series  
  
Capabilities:  
- define time index  
- define target series  
- support lag-ready output  
- support differencing-ready output  
- train / validation / forecast horizon partitioning  
- support exogenous feature alignment  
  
11.4 Event / Spell Data  
--------------------------------------------------------------------  
The SDK shall support event-history or spell-based data.  
  
Examples:  
- default spell  
- cure spell  
- delinquency spell  
- survival / hazard modeling setup  
  
Capabilities:  
- define spell ID  
- define entry and exit  
- define event indicator  
- construct person-period or entity-period dataset  
- support censoring flags  
- align time-varying covariates  
  
11.5 Cohort Snapshot Data  
--------------------------------------------------------------------  
The SDK shall support cohort-based setup.  
  
Examples:  
- origination cohort  
- reporting cohort  
- default cohort  
- workout cohort  
  
Capabilities:  
- define cohort date  
- derive cohort members  
- list date sequence from cohort to reporting / performance horizon  
- align target outcomes to cohort  
  
11.6 Hierarchical Data  
--------------------------------------------------------------------  
The SDK shall support linked customer-account-contract preparation.  
  
Capabilities:  
- define parent-child mappings  
- aggregate child features to parent  
- preserve hierarchy metadata  
- choose retained grain for output  
  
====================================================================  
12. TARGET GENERATION REQUIREMENTS  
====================================================================  
  
12.1 Principle  
--------------------------------------------------------------------  
The SDK shall support target alignment using standard template logic.  
  
12.2 Target Types  
--------------------------------------------------------------------  
Supported target types may include:  
- binary default flag  
- delinquency event flag  
- cure flag  
- loss rate  
- recovery rate  
- exposure conversion  
- stage movement  
- time-to-event  
- macro forecast target  
  
12.3 Target Window Logic  
--------------------------------------------------------------------  
The SDK shall support:  
- fixed future horizon  
- rolling horizon  
- observation-to-performance window  
- reporting-to-future window  
- origination-to-outcome window  
- event-aligned target generation  
  
12.4 Leakage Control  
--------------------------------------------------------------------  
The SDK shall include checks to prevent future leakage in feature and  
target alignment.  
  
====================================================================  
13. OBSERVATION WINDOW REQUIREMENTS  
====================================================================  
  
The SDK shall support standard observation logic such as:  
  
- as-of-date snapshot  
- monthly observation  
- quarter-end observation  
- cohort observation  
- origination-date observation  
- rolling lookback window  
- fixed lookback window  
- dynamic lookback based on data availability  
  
====================================================================  
14. SAMPLE SPLIT REQUIREMENTS  
====================================================================  
  
The SDK shall support preparation of:  
- development sample  
- validation sample  
- test sample  
- out-of-time sample  
- holdout sample  
- backtest sample where relevant  
  
Split rules shall be configurable but template-governed.  
  
Supported split styles:  
- random split  
- time-based split  
- cohort-based split  
- entity-based split  
- policy-defined split  
  
====================================================================  
15. FEATURE ALIGNMENT REQUIREMENTS  
====================================================================  
  
The SDK shall support:  
- static feature merge  
- dynamic feature merge  
- lag-ready output  
- time-varying covariate alignment  
- macro feature alignment  
- hierarchical aggregation  
- missing-value policy application as defined by template  
- controlled feature inclusion / exclusion from config  
  
====================================================================  
16. DATA QUALITY AND PREPARATION CHECKS  
====================================================================  
  
The SDK shall perform preparation-stage checks such as:  
- required columns present  
- grain uniqueness validation  
- join key availability  
- duplicate key checks  
- target availability check  
- observation window validity  
- target leakage check  
- split coverage check  
- null ratio summary  
- time index continuity checks where relevant  
- cohort membership consistency checks  
  
These checks are not a replacement for a full DQ platform, but shall  
ensure data preparation integrity.  
  
====================================================================  
17. OUTPUT REQUIREMENTS  
====================================================================  
  
17.1 Primary Outputs  
--------------------------------------------------------------------  
The SDK shall produce:  
  
- prepared training dataset  
- metadata manifest  
- lineage manifest  
- preparation summary  
- split summary  
- target definition summary  
- quality check summary  
  
17.2 Output Metadata  
--------------------------------------------------------------------  
Each output shall store:  
- dataset_id  
- template_id  
- template_version  
- config_id / config_hash  
- source datasets used  
- grain  
- data structure type  
- target definition  
- split definition  
- created_timestamp  
- created_by  
- run_id if applicable  
  
17.3 Optional Outputs  
--------------------------------------------------------------------  
The SDK should support:  
- feature dictionary extract  
- entity coverage summary  
- time coverage summary  
- leakage report  
- sample balance report  
  
====================================================================  
18. AGENTIC AI REQUIREMENTS  
====================================================================  
  
18.1 Principle  
--------------------------------------------------------------------  
The SDK shall expose deterministic interfaces suitable for agentic AI.  
  
18.2 Agent Use Cases  
--------------------------------------------------------------------  
Agents shall be able to:  
- identify the required data structure  
- select an approved preparation template  
- validate config completeness  
- run preparation  
- inspect outputs  
- route to HITL if required  
- summarize preparation result  
- reproduce prior dataset from config and lineage references  
  
18.3 Agent Guardrails  
--------------------------------------------------------------------  
Agents shall not:  
- execute unapproved free-form preparation logic in governed mode  
- silently ignore lineage errors  
- silently relax target or split definitions  
- bypass template validation  
  
====================================================================  
19. HUMAN-IN-THE-LOOP REQUIREMENTS  
====================================================================  
  
The SDK shall support optional HITL where required for:  
- ambiguous grain mapping  
- unresolved lineage mapping  
- unsupported source conditions  
- special split approval  
- target definition override  
- leakage warning disposition  
- hierarchy aggregation choice where policy requires review  
  
====================================================================  
20. STANDARD CONFIGURATION REQUIREMENTS  
====================================================================  
  
20.1 Config Philosophy  
--------------------------------------------------------------------  
All preparation behavior shall be driven by structured config.  
  
20.2 Core Config Sections  
--------------------------------------------------------------------  
The config should include sections such as:  
- project_info  
- source_registry  
- lineage_mapping  
- template_selection  
- grain_definition  
- entity_definition  
- time_definition  
- target_definition  
- feature_definition  
- split_definition  
- quality_rules  
- output_definition  
  
20.3 Config Validation  
--------------------------------------------------------------------  
The SDK shall validate config completeness and consistency before  
execution.  
  
====================================================================  
21. PROPOSED MODULE DESIGN  
====================================================================  
  
21.1 dataprepsdk Core Modules  
--------------------------------------------------------------------  
Suggested modules:  
  
- template_registry  
- template_executor  
- source_reader  
- lineage_resolver  
- grain_manager  
- entity_mapper  
- time_aligner  
- target_builder  
- feature_aligner  
- split_builder  
- sample_builder  
- quality_checker  
- metadata_builder  
- lineage_builder  
- output_writer  
- manifest_builder  
- leakage_checker  
- config_validator  
  
21.2 Optional Helper Modules  
--------------------------------------------------------------------  
- hierarchy_aggregator  
- panel_constructor  
- cohort_builder  
- spell_builder  
- macro_merge_engine  
- reproducibility_loader  
  
====================================================================  
22. STANDARD FUNCTIONAL INTERFACES  
====================================================================  
  
The SDK should expose functions such as:  
  
- validate_template_request(...)  
- validate_config(...)  
- resolve_lineage(...)  
- build_prepared_dataset(...)  
- build_cross_sectional_dataset(...)  
- build_panel_dataset(...)  
- build_time_series_dataset(...)  
- build_event_history_dataset(...)  
- build_cohort_dataset(...)  
- build_split(...)  
- generate_target(...)  
- generate_manifests(...)  
- reproduce_dataset(...)  
  
All material functions should return standardized status envelopes.  
  
====================================================================  
23. STANDARD RESPONSE CONTRACT  
====================================================================  
  
Every material SDK task should return:  
  
- status  
- message  
- template_id  
- template_version  
- dataset_id  
- data_structure_type  
- grain  
- warnings  
- errors  
- artifacts_created  
- manifests_created  
- quality_summary_ref  
- lineage_summary_ref  
- next_recommended_action  
  
Suggested statuses:  
- success  
- success_with_warning  
- blocked  
- failed  
- invalid_config  
- invalid_lineage  
- needs_human_review  
  
====================================================================  
24. REPRODUCIBILITY REQUIREMENTS  
====================================================================  
  
The SDK shall support exact or near-exact reproduction of a prior  
prepared dataset based on:  
- template ID and version  
- preparation config  
- source references  
- lineage manifest  
- split definition  
- target definition  
- dataset manifest  
  
====================================================================  
25. VALIDATION SUPPORT REQUIREMENTS  
====================================================================  
  
The SDK shall produce sufficient metadata so model validation can  
understand:  
- source lineage  
- grain logic  
- sample construction logic  
- target construction logic  
- split logic  
- major filters applied  
- warnings raised during preparation  
  
====================================================================  
26. GOVERNANCE REQUIREMENTS  
====================================================================  
  
The SDK shall support governance by:  
- restricting preparation to standard templates  
- validating config schema  
- preserving manifests  
- preserving lineage  
- preserving warnings and exceptions  
- allowing review of deviations / overrides where applicable  
  
====================================================================  
27. PERFORMANCE AND SCALABILITY REQUIREMENTS  
====================================================================  
  
The SDK shall be designed for efficient use in enterprise data  
preparation flows.  
  
It should support:  
- Python execution  
- PySpark-friendly integration  
- scalable reading and joining strategies  
- partition-aware output writing where relevant  
- efficient repeated rebuild through manifests and cached references  
- avoidance of unnecessary full reload where possible  
  
====================================================================  
28. CML AND S3 ENVIRONMENT REQUIREMENTS  
====================================================================  
  
The implementation shall be suitable for CML with S3 access.  
  
It should support:  
- reading source datasets from S3  
- writing prepared outputs to S3  
- writing manifests and metadata to S3  
- configuration-driven path resolution  
- reproducible object naming  
- local execution within constrained enterprise environments  
  
====================================================================  
29. INTEGRATION REQUIREMENTS  
====================================================================  
  
The SDK shall integrate with:  
- workflowsdk  
- artifactsdk  
- observabilitysdk  
- auditsdk  
- validation workflows  
- knowledge / RAG layer  
- reporting_sdk  
- domain SDKs such as scorecardsdk, pdsdk, lgdsdk, eadsdk, eclsdk  
  
====================================================================  
30. FUTURE-PROOFING REQUIREMENTS  
====================================================================  
  
The SDK shall be extensible for future support of:  
- new standard templates  
- more granular hierarchy logic  
- more advanced time-window logic  
- synthetic sample generation interfaces  
- benchmark dataset generation  
- monitoring dataset preparation  
- validation challenger dataset preparation  
- additional domain-specific target frameworks  
  
====================================================================  
31. NON-FUNCTIONAL REQUIREMENTS  
====================================================================  
  
The SDK shall be:  
  
- modular  
- traceable  
- reproducible  
- config-driven  
- deterministic  
- agent-friendly  
- governance-ready  
- validation-friendly  
- maintainable  
- extensible  
- performant within enterprise constraints  
  
====================================================================  
32. IMPLEMENTATION PHASES  
====================================================================  
  
32.1 Phase 1  
--------------------------------------------------------------------  
Build:  
- template registry  
- config schema and validator  
- source reader  
- lineage resolver  
- cross-sectional template  
- panel template  
- time-series template  
- metadata manifest  
- lineage manifest  
- output writer  
- standard response envelope  
  
32.2 Phase 2  
--------------------------------------------------------------------  
Add:  
- event / spell template  
- cohort snapshot template  
- hierarchy aggregator  
- leakage checker  
- quality summaries  
- reproducibility loader  
- agent integration wrappers  
  
32.3 Phase 3  
--------------------------------------------------------------------  
Add:  
- advanced hierarchy templates  
- monitoring dataset templates  
- validation challenger templates  
- benchmark preparation patterns  
- richer macro merge support  
  
====================================================================  
33. SUCCESS CRITERIA  
====================================================================  
  
The SDK shall be considered successful when:  
  
1. agents can prepare training datasets through deterministic SDK  
   calls  
2. users can define lineage-driven preparation through config  
3. only approved standard templates are used in governed mode  
4. cross-sectional, panel, time-series, and other required data  
   structures are supported cleanly  
5. output datasets are reproducible and traceable  
6. manifests and lineage are sufficient for validation and audit  
7. the SDK integrates seamlessly into the wider agentic AI platform  
8. the SDK materially reduces repeated manual data preparation work  
9. the SDK is regarded as top-of-the-class for practical enterprise  
   model data preparation  
  
====================================================================  
34. APPENDIX – PROPOSED REQUIREMENT IDS  
====================================================================  
  
DPREP-FR-001  
Support template-driven data preparation for credit risk modeling.  
  
DPREP-FR-002  
Support config-driven lineage and preparation behavior.  
  
DPREP-FR-003  
Support cross-sectional dataset preparation.  
  
DPREP-FR-004  
Support panel / longitudinal dataset preparation.  
  
DPREP-FR-005  
Support time-series dataset preparation.  
  
DPREP-FR-006  
Support event / spell dataset preparation.  
  
DPREP-FR-007  
Support cohort-based dataset preparation.  
  
DPREP-FR-008  
Support hierarchical entity-linked dataset preparation.  
  
DPREP-FR-009  
Support target generation and leakage control.  
  
DPREP-FR-010  
Support train / test / oot split preparation.  
  
DPREP-FR-011  
Support manifest and lineage output generation.  
  
DPREP-FR-012  
Support deterministic agent-safe interfaces.  
  
DPREP-FR-013  
Support reproducibility from config and lineage references.  
  
DPREP-FR-014  
Support CML execution with S3 access.  
  
DPREP-FR-015  
Restrict governed execution to approved standard templates.  
  
DPREP-NFR-001  
The SDK shall be modular and extensible.  
  
DPREP-NFR-002  
The SDK shall be reproducible and traceable.  
  
DPREP-NFR-003  
The SDK shall be suitable for enterprise-scale workflows.  
  
====================================================================  
END OF URD  
====================================================================  
  
====================================================================  
URD ADDENDUM  
SPARK-FIRST EXECUTION REQUIREMENTS  
FOR DATAPREPSDK  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This addendum updates the Data Preparation SDK URD to make Spark the  
primary and governed execution environment for data preparation.  
  
The SDK shall be designed so that all material dataset preparation for  
enterprise credit risk modeling is conducted in a Spark environment,  
with Python orchestration and PySpark execution as the standard path.  
  
====================================================================  
A. REVISED CORE PRINCIPLE  
====================================================================  
  
A.1 Spark-First Principle  
--------------------------------------------------------------------  
The Data Preparation SDK shall be Spark-first.  
  
This means:  
- all governed large-scale data preparation shall execute in Spark  
- PySpark shall be the standard implementation interface  
- Python-only execution may exist only for lightweight metadata,  
  config, control, validation, and orchestration tasks  
- final dataset building, joins, aggregations, windowing, panel  
  construction, cohort construction, split creation, and major feature  
  alignment shall be Spark-based  
  
A.2 Reason for Spark-First Design  
--------------------------------------------------------------------  
Spark-first execution is required because the SDK is intended for:  
  
- enterprise-scale credit risk data  
- repeated model dataset rebuilding  
- panel and cohort construction at scale  
- efficient joins across multiple large sources  
- integration with CML and S3-backed storage  
- reproducible large-scale preparation workflows  
  
====================================================================  
B. SECTIONS TO UPDATE IN THE MAIN URD  
====================================================================  
  
--------------------------------------------------------------------  
B.1 Update Section 1 PURPOSE  
--------------------------------------------------------------------  
Replace or enhance wording to state:  
  
"The SDK shall provide a governed, config-driven, reusable,  
template-based, and Spark-first framework to prepare model-ready  
training datasets for credit risk modeling."  
  
--------------------------------------------------------------------  
B.2 Update Section 2 OBJECTIVES  
--------------------------------------------------------------------  
Add objective:  
  
11. Execute all material data preparation in a Spark environment using  
    PySpark as the standard governed execution path.  
  
--------------------------------------------------------------------  
B.3 Update Section 5 DESIGN PRINCIPLES  
--------------------------------------------------------------------  
Add new principle:  
  
5.9 Spark-Native Execution  
--------------------------------------------------------------------  
The SDK shall be designed primarily for Spark execution, with PySpark  
as the standard implementation path for large-scale dataset  
preparation.  
  
--------------------------------------------------------------------  
B.4 Update Section 17 OUTPUT REQUIREMENTS  
--------------------------------------------------------------------  
Add requirement:  
  
Prepared datasets shall be produced from Spark DataFrames and written  
using governed Spark output patterns.  
  
--------------------------------------------------------------------  
B.5 Update Section 21 PROPOSED MODULE DESIGN  
--------------------------------------------------------------------  
Add Spark-specific module emphasis:  
- spark_source_reader  
- spark_lineage_resolver  
- spark_grain_manager  
- spark_time_aligner  
- spark_target_builder  
- spark_feature_aligner  
- spark_split_builder  
- spark_sample_builder  
- spark_quality_checker  
- spark_output_writer  
  
--------------------------------------------------------------------  
B.6 Update Section 27 PERFORMANCE AND SCALABILITY REQUIREMENTS  
--------------------------------------------------------------------  
Replace with stronger language:  
  
The SDK shall be designed for Spark-native scalable execution and  
shall optimize for:  
- distributed joins  
- partition-aware reading and writing  
- efficient window functions  
- scalable aggregation  
- minimized data shuffling where possible  
- reusable intermediate preparation stages where appropriate  
  
--------------------------------------------------------------------  
B.7 Update Section 28 CML AND S3 ENVIRONMENT REQUIREMENTS  
--------------------------------------------------------------------  
Replace or enhance to state:  
  
The implementation shall be designed for CML running Spark / PySpark  
workloads with S3 access for source and output data.  
  
====================================================================  
C. NEW SECTION – SPARK EXECUTION REQUIREMENTS  
====================================================================  
  
====================================================================  
28A. SPARK EXECUTION REQUIREMENTS  
====================================================================  
  
28A.1 Primary Execution Environment  
--------------------------------------------------------------------  
The Data Preparation SDK shall use Spark as the primary execution  
engine for governed data preparation.  
  
28A.2 Standard Programming Interface  
--------------------------------------------------------------------  
PySpark shall be the standard implementation interface exposed by the  
SDK.  
  
28A.3 Spark DataFrame Standard  
--------------------------------------------------------------------  
All material preparation stages shall operate on Spark DataFrames as  
the standard internal dataset object.  
  
Examples of material stages:  
- source ingestion  
- lineage-based joins  
- filtering  
- grain alignment  
- panel construction  
- cohort construction  
- event / spell construction  
- time index alignment  
- target generation  
- feature alignment  
- train / test / oot split construction  
- final dataset packaging  
  
28A.4 Python-Only Tasks  
--------------------------------------------------------------------  
Python-only logic may be used for:  
- config parsing  
- schema validation  
- metadata generation  
- manifest generation  
- lightweight control logic  
- orchestration  
- small-scale result summarization  
  
Python-only logic shall not be the governed standard path for large  
dataset transformation.  
  
28A.5 Spark-Specific Functional Requirements  
--------------------------------------------------------------------  
The SDK shall support Spark-based:  
- joins  
- aggregations  
- window calculations  
- lag-ready dataset generation  
- partition-aware writing  
- hierarchical aggregation  
- panel expansion / flattening  
- as-of-date filtering  
- cohort date derivation  
- event alignment  
- split tagging  
  
28A.6 Spark Template Execution  
--------------------------------------------------------------------  
Each approved template shall execute through Spark-native preparation  
logic.  
  
Examples:  
- cross_sectional_training_template -> Spark DataFrame snapshot build  
- panel_training_template -> Spark DataFrame repeated observation build  
- time_series_training_template -> Spark time-indexed build  
- event_history_training_template -> Spark person-period build  
- cohort_snapshot_template -> Spark cohort derivation build  
  
28A.7 Spark Quality Checks  
--------------------------------------------------------------------  
Preparation-stage quality checks shall run in Spark where possible for:  
- duplicate key checks  
- null counts  
- join match rates  
- grain uniqueness  
- observation count summaries  
- split coverage summaries  
- leakage checks requiring data scan  
  
28A.8 Spark Output Standard  
--------------------------------------------------------------------  
Prepared outputs shall be written from Spark DataFrames to governed  
storage locations, typically on S3, using standardized write logic.  
  
28A.9 Spark Reproducibility  
--------------------------------------------------------------------  
The SDK shall capture sufficient metadata so that Spark-based dataset  
generation can be reproduced consistently using:  
- template version  
- config version  
- source references  
- transformation manifest  
- split definition  
- output path metadata  
  
28A.10 Spark Performance Controls  
--------------------------------------------------------------------  
The SDK should support performance controls such as:  
- repartition / coalesce strategy where appropriate  
- controlled cache / persist usage  
- partition pruning support  
- selective column projection  
- join strategy hints where governed and safe  
- minimized repeated scans where possible  
  
28A.11 Spark Environment Compatibility  
--------------------------------------------------------------------  
The SDK shall be designed for compatibility with Spark execution in  
CML and with S3-backed datasets used in enterprise environments.  
  
====================================================================  
D. NEW SECTION – SPARK MODULE ARCHITECTURE  
====================================================================  
  
====================================================================  
21A. SPARK MODULE ARCHITECTURE  
====================================================================  
  
Suggested Spark-first modules:  
  
- spark_session_manager  
  Manage Spark session access, context checks, and Spark config hooks.  
  
- spark_source_reader  
  Read source datasets from governed locations into Spark DataFrames.  
  
- spark_lineage_resolver  
  Resolve lineage mapping and join plan into Spark transformation flow.  
  
- spark_grain_manager  
  Enforce and transform data grain using Spark logic.  
  
- spark_entity_mapper  
  Handle entity-level, account-level, contract-level mapping.  
  
- spark_time_aligner  
  Align observation date, reporting date, cohort date, and target date  
  using Spark transformations.  
  
- spark_target_builder  
  Generate model targets using Spark rules and window logic.  
  
- spark_feature_aligner  
  Align and merge features using Spark DataFrame operations.  
  
- spark_panel_constructor  
  Build repeated-observation panel datasets.  
  
- spark_cohort_builder  
  Build cohort-based datasets.  
  
- spark_spell_builder  
  Build event-history or spell datasets.  
  
- spark_split_builder  
  Build train / test / oot flags at scale.  
  
- spark_quality_checker  
  Run preparation-stage scalable data checks.  
  
- spark_output_writer  
  Write final prepared DataFrames and summaries to governed storage.  
  
- spark_manifest_builder  
  Build metadata and lineage summaries for Spark outputs.  
  
====================================================================  
E. NEW SECTION – AGENTIC AI IMPLICATIONS  
====================================================================  
  
====================================================================  
18A. AGENTIC AI REQUIREMENTS FOR SPARK EXECUTION  
====================================================================  
  
18A.1 Agent Role  
--------------------------------------------------------------------  
Agents shall orchestrate Spark-based preparation through deterministic  
SDK calls rather than attempt free-form data wrangling logic.  
  
18A.2 Agent-Safe Interfaces  
--------------------------------------------------------------------  
The SDK shall expose Spark-governed functions such as:  
- build_cross_sectional_dataset_spark(...)  
- build_panel_dataset_spark(...)  
- build_time_series_dataset_spark(...)  
- build_event_history_dataset_spark(...)  
- build_cohort_dataset_spark(...)  
- build_split_spark(...)  
- run_quality_checks_spark(...)  
  
18A.3 Agent Guardrails  
--------------------------------------------------------------------  
Agents shall not:  
- bypass Spark templates for governed large-scale preparation  
- substitute ad hoc pandas workflows for required Spark execution  
- finalize dataset outputs without Spark lineage metadata  
  
18A.4 Agent Output Summary  
--------------------------------------------------------------------  
After Spark execution, the SDK should return compact summaries for the  
agent, such as:  
- row counts  
- grain summary  
- split summary  
- target coverage  
- warning counts  
- output dataset reference  
- manifest references  
  
This keeps agent interactions token-thrifty while the heavy work stays  
in Spark.  
  
====================================================================  
F. UPDATED REQUIREMENT IDS  
====================================================================  
  
Add the following requirement IDs:  
  
DPREP-FR-016  
The SDK shall execute all material governed data preparation in a  
Spark environment.  
  
DPREP-FR-017  
The SDK shall use PySpark as the standard implementation interface for  
large-scale data preparation.  
  
DPREP-FR-018  
The SDK shall use Spark DataFrames as the standard internal dataset  
object for material preparation stages.  
  
DPREP-FR-019  
The SDK shall provide Spark-native templates for cross-sectional,  
panel, time-series, event-history, and cohort-based dataset  
preparation.  
  
DPREP-FR-020  
The SDK shall perform scalable preparation-stage data checks in Spark  
where applicable.  
  
DPREP-FR-021  
The SDK shall write final outputs from Spark DataFrames to governed  
storage, including S3-backed destinations.  
  
DPREP-FR-022  
The SDK shall expose deterministic Spark-governed interfaces suitable  
for agentic AI orchestration.  
  
DPREP-NFR-004  
The SDK shall be Spark-first and scalable for enterprise credit risk  
data preparation workloads.  
  
====================================================================  
G. FINAL RECOMMENDATION  
====================================================================  
  
For this project, the cleanest design is:  
  
- Python for orchestration and config control  
- PySpark for all governed material data preparation  
- S3 for source/output storage  
- standard templates only  
- deterministic interfaces for agent calls  
- lineage and manifest capture by default  
  
This will make the SDK much more aligned with your actual enterprise  
environment and much stronger for agentic AI automation.  
  
====================================================================  
END OF SPARK-FIRST URD ADDENDUM  
====================================================================  
