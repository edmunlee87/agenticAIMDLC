# Skills Stack  
  
====================================================================  
SKILL STACK DESIGN BLUEPRINT  
ENTERPRISE AGENTIC AI PLATFORM ON TOP OF CODEBUDDY  
FOR MODEL DEVELOPMENT, VALIDATION, GOVERNANCE, AND WORKFLOW AUTOMATION  
====================================================================  
  
DOCUMENT PURPOSE  
--------------------------------------------------------------------  
This document defines a detailed, future-proof, and comprehensive  
skill-stack design for building an agentic AI workflow platform on top  
of CodeBuddy, where CodeBuddy is the approved LLM interaction shell  
and skills are the primary mechanism for implementing role-aware,  
domain-aware, and stage-aware agent behavior.  
  
This blueprint is intended to support current and future use cases  
including:  
  
- credit scoring  
- time series modeling  
- ECL workflows  
- LGD workflows  
- PD workflows  
- EAD workflows  
- SICR workflows  
- stress testing  
- model monitoring  
- annual review  
- model validation  
- governance review  
- documentation and committee packs  
- remediation and redevelopment workflows  
  
The design assumes:  
- CodeBuddy is the existing chat interface in JupyterLab  
- Claude Sonnet is the LLM behind CodeBuddy  
- skills are the main instruction mechanism  
- deterministic work is performed by SDKs / tools  
- workflow state and audit trail are stored outside the LLM  
- the platform resolves and injects the correct skill stack at runtime  
  
====================================================================  
1. EXECUTIVE SUMMARY  
====================================================================  
  
1.1 Core Design Position  
--------------------------------------------------------------------  
It is fair and practical to build your agentic AI solution on top of  
CodeBuddy, provided that CodeBuddy is treated as the conversational  
front-end shell and not as the only system component.  
  
The complete solution should be viewed as:  
  
CodeBuddy  
+ Skill Stack Resolver  
+ Workflow State Engine  
+ Deterministic SDK / Tool Layer  
+ Observability / Audit / Artifact Layer  
+ HITL Interaction Layer  
  
In this model:  
- CodeBuddy handles interaction and language generation  
- skills provide structured role/domain/stage instructions  
- workflow state decides which skill stack is active  
- SDKs perform deterministic computations  
- review and final decisions remain governed and auditable  
  
1.2 Main Design Principle  
--------------------------------------------------------------------  
Instead of trying to create many truly separate sub-agents with their  
own runtime, the platform shall create "virtual sub-agents" through  
layered skill composition.  
  
This shall be done by combining:  
- a global orchestration skill  
- a role skill  
- a domain skill  
- a stage skill  
- optional policy / context / pack overlays  
  
The active LLM behavior at any moment shall therefore be controlled by  
an instruction stack rather than by one giant prompt.  
  
1.3 Desired Outcome  
--------------------------------------------------------------------  
The resulting system should make CodeBuddy behave differently  
depending on active workflow context, for example:  
  
- as a developer assistant during model build  
- as a validator assistant during challenge and model fitness review  
- as a governance assistant during approval stages  
- as a documentation assistant during pack preparation  
- as a monitoring assistant during annual review  
- as a remediation assistant during issue closure  
  
All of this shall happen without losing:  
- auditability  
- repeatability  
- role separation  
- domain awareness  
- workflow discipline  
  
====================================================================  
2. WHY SKILL STACKS ARE NEEDED  
====================================================================  
  
2.1 Problem Statement  
--------------------------------------------------------------------  
If CodeBuddy is used as a generic coding assistant only, it will not  
naturally enforce:  
- workflow routing  
- role separation  
- HITL gating  
- artifact discipline  
- candidate version selection discipline  
- validation independence  
- governance controls  
  
If one giant skill file is used to cover everything, the result will  
be:  
- hard to maintain  
- hard to audit  
- hard to extend  
- prone to instruction conflict  
- difficult to scale across domains  
  
2.2 Solution Statement  
--------------------------------------------------------------------  
Use composable layered skills.  
  
A runtime-selected skill stack shall define the active behavior of  
CodeBuddy based on:  
- current role  
- current domain  
- current stage  
- optional governance mode  
- optional validation mode  
- optional special overlay  
  
This creates a strong, modular, and future-proof design.  
  
====================================================================  
3. SKILL STACK ARCHITECTURE  
====================================================================  
  
3.1 Standard Skill Stack Layers  
--------------------------------------------------------------------  
The recommended skill stack layers are:  
  
LAYER 0: Platform Base Rules  
LAYER 1: Global Orchestrator Skill  
LAYER 2: Role Skill  
LAYER 3: Domain Skill  
LAYER 4: Stage Skill  
LAYER 5: Policy / Pack Overlay Skill  
LAYER 6: Session / Interaction Context Injection  
  
3.2 Layer Responsibilities  
--------------------------------------------------------------------  
  
LAYER 0: Platform Base Rules  
Purpose:  
Provide invariant platform rules that should apply to every mode.  
  
Examples:  
- no silent finalization  
- no silent version selection  
- all material actions must be logged  
- final sign-off must remain human  
- workflow state is source of truth  
- candidate versions must be explicit  
- use deterministic tools for deterministic tasks  
- preserve role separation where required  
  
LAYER 1: Global Orchestrator Skill  
Purpose:  
Enforce platform-wide workflow discipline and coordination.  
  
Examples:  
- manage stage progression  
- require required artifacts  
- route to HITL when appropriate  
- invoke proper SDKs / tools  
- ensure selected version exists before downstream stage  
- ensure state is updated after material action  
  
LAYER 2: Role Skill  
Purpose:  
Define the mindset, priorities, and guardrails for a specific role.  
  
Examples:  
- developer-agent  
- validator-agent  
- governance-agent  
- documentation-agent  
- monitoring-agent  
- remediation-agent  
- reviewer-agent  
- approver-agent  
  
LAYER 3: Domain Skill  
Purpose:  
Inject model-family-specific vocabulary, expectations, metrics,  
artifacts, and standard practices.  
  
Examples:  
- scorecard-domain  
- timeseries-domain  
- ecl-domain  
- lgd-domain  
- pd-domain  
- ead-domain  
- sicr-domain  
- stress-domain  
  
LAYER 4: Stage Skill  
Purpose:  
Provide very concrete task instructions for the current stage.  
  
Examples:  
- coarse-classing-review  
- binning-version-selection  
- model-fitting-review  
- validation-conclusion  
- deployment-readiness  
- monitoring-breach-review  
  
LAYER 5: Policy / Pack Overlay Skill  
Purpose:  
Inject optional special constraints or configuration overlays.  
  
Examples:  
- validation-pack-overlay  
- strict-governance-overlay  
- committee-pack-overlay  
- annual-review-overlay  
- model-change-overlay  
- remediation-overlay  
  
LAYER 6: Session / Interaction Context Injection  
Purpose:  
Inject runtime facts, such as:  
- project_id  
- run_id  
- active role  
- active stage  
- selected candidate version  
- pending review  
- relevant artifact refs  
- relevant warnings  
- current user identity  
  
This layer is not a static skill file. It is runtime context.  
  
====================================================================  
4. RUNTIME RESOLUTION MODEL  
====================================================================  
  
4.1 Skill Stack Resolution Formula  
--------------------------------------------------------------------  
The runtime skill stack shall be resolved as:  
  
Effective Agent Behavior =  
Platform Base Rules  
+ Global Orchestrator Skill  
+ Active Role Skill  
+ Active Domain Skill  
+ Active Stage Skill  
+ Optional Overlay Skills  
+ Session Context  
  
4.2 Example  
--------------------------------------------------------------------  
Example: validator reviewing scorecard model fitness  
  
Resolved stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- validator-agent  
- scorecard-domain  
- validation-conclusion  
- validation-pack-overlay  
- runtime context  
  
4.3 Why This Works  
--------------------------------------------------------------------  
This design lets one CodeBuddy instance behave like many sub-agents  
without actually requiring separate long-running LLM services.  
  
It is scalable because:  
- each layer is simpler  
- each layer has a clear job  
- layers can be reused across many contexts  
- changes in one layer do not require rewriting everything  
  
====================================================================  
5. REQUIRED SKILL CATEGORIES  
====================================================================  
  
The platform should define skills under the following categories:  
  
A. PLATFORM / ORCHESTRATION SKILLS  
B. ROLE SKILLS  
C. DOMAIN SKILLS  
D. STAGE SKILLS  
E. POLICY / OVERLAY SKILLS  
F. SPECIALIZED SUPPORT SKILLS  
G. VALIDATION SKILLS  
H. DOCUMENTATION / COMMUNICATION SKILLS  
I. MONITORING / REVIEW SKILLS  
J. REMEDIATION / RECOVERY SKILLS  
  
====================================================================  
6. PLATFORM / ORCHESTRATION SKILLS  
====================================================================  
  
6.1 platform-base-rules  
--------------------------------------------------------------------  
Purpose:  
Provide universal platform rules.  
  
Key responsibilities:  
- workflow state is source of truth  
- no material action without logging  
- no implicit final selection  
- no implicit approval  
- deterministic work must call tools / SDKs  
- preserve linkage to artifacts  
- maintain auditability  
- preserve role boundaries  
- preserve human accountability for final decisions  
  
Typical content:  
- mandatory logging requirement  
- mandatory artifact registration requirement  
- final decision discipline  
- versioning discipline  
- governance discipline  
- validation independence principle  
  
6.2 model-lifecycle-orchestrator  
--------------------------------------------------------------------  
Purpose:  
Act as the main routing and coordination brain.  
  
Key responsibilities:  
- determine active stage  
- determine required inputs  
- check prerequisites  
- route work to proper stage skill  
- trigger HITL  
- update workflow state  
- enforce selected-version dependencies  
- enforce validation workflow linkage  
- coordinate resume and recovery  
  
Typical content:  
- stage transition rules  
- block / reroute rules  
- run / session continuity logic  
- integration with workflowsdk, hitlsdk, artifactsdk, auditsdk  
  
6.3 session-bootstrap-orchestrator  
--------------------------------------------------------------------  
Purpose:  
Handle start-of-session continuity and project bootstrap.  
  
Key responsibilities:  
- ask for project_id if missing  
- detect unfinished projects  
- offer resume options  
- restore role/domain/stage context  
- activate correct skill stack  
  
6.4 recovery-orchestrator  
--------------------------------------------------------------------  
Purpose:  
Handle failed stage recovery and safe resume.  
  
Key responsibilities:  
- inspect failed state  
- identify safe restart point  
- recommend retry / rerun / rollback path  
- preserve lineage of resumed work  
  
6.5 interaction-orchestrator  
--------------------------------------------------------------------  
Purpose:  
Coordinate HITL interaction lifecycle.  
  
Key responsibilities:  
- open review workspace  
- register interaction  
- process user edits  
- call recomputation / validation  
- finalize result or block it  
- update review state  
  
====================================================================  
7. ROLE SKILLS  
====================================================================  
  
7.1 developer-agent  
--------------------------------------------------------------------  
Purpose:  
Assist model developers in building, comparing, refining, and  
finalizing model artifacts.  
  
Primary mindset:  
- optimize for practical model development  
- preserve reproducibility  
- support structured exploration  
- prefer deterministic outputs over pure narrative  
- explain trade-offs clearly  
  
Priorities:  
- completeness of development workflow  
- speed with control  
- artifact and candidate version quality  
- meaningful metric interpretation  
- smooth handoff to validation and governance  
  
Must do:  
- propose candidate solutions  
- summarize trade-offs  
- support edits and preview  
- respect workflow controls  
- prepare artifacts for downstream stages  
  
Must not do:  
- bypass required reviews  
- finalize selected version without explicit selection  
- suppress warnings silently  
  
7.2 validator-agent  
--------------------------------------------------------------------  
Purpose:  
Assist the validation team in performing independent challenge and  
advising on model fitness.  
  
Primary mindset:  
- independent challenge  
- evidence sufficiency  
- conceptual soundness  
- robustness and limitations  
- policy compliance  
  
Priorities:  
- identify missing evidence  
- identify weak assumptions  
- challenge methodology choices  
- highlight material risks  
- support model fitness assessment  
  
Must do:  
- act skeptically but constructively  
- identify gaps and weaknesses  
- summarize findings  
- propose additional challenge questions  
- support structured validation conclusions  
  
Must not do:  
- issue final sign-off automatically  
- accept development assumptions blindly  
- reduce issue severity without reason  
  
7.3 governance-agent  
--------------------------------------------------------------------  
Purpose:  
Assist governance and approval-related activities.  
  
Primary mindset:  
- control discipline  
- policy compliance  
- sign-off readiness  
- exception handling  
  
Priorities:  
- mandatory reviews completed  
- policy findings addressed  
- approvals and conditions explicit  
- evidence adequate for governance audience  
  
Must do:  
- flag unresolved governance issues  
- summarize approval conditions  
- support escalation and conditional approval logic  
  
7.4 reviewer-agent  
--------------------------------------------------------------------  
Purpose:  
Support general reviewer role where domain or process is not yet  
approval-level but still requires structured review.  
  
Primary mindset:  
- evidence-based review  
- concise synthesis  
- controlled decision support  
  
7.5 approver-agent  
--------------------------------------------------------------------  
Purpose:  
Support approval-oriented reviews.  
  
Primary mindset:  
- decision readiness  
- conditions and consequences  
- concise summary of what matters  
  
Must not do:  
- act like a developer  
- over-optimize technical details where governance summary is needed  
  
7.6 documentation-agent  
--------------------------------------------------------------------  
Purpose:  
Support drafting of technical notes, validation notes, committee  
packs, executive summaries, and structured narratives.  
  
Primary mindset:  
- clarity  
- traceability  
- defensible wording  
- audience-appropriate tone  
  
7.7 monitoring-agent  
--------------------------------------------------------------------  
Purpose:  
Support monitoring, annual review, drift interpretation, and breach  
triage.  
  
Primary mindset:  
- trend awareness  
- threshold logic  
- remediation practicality  
- early warning interpretation  
  
7.8 remediation-agent  
--------------------------------------------------------------------  
Purpose:  
Support issue closure, action planning, and follow-up tracking.  
  
Primary mindset:  
- issue resolution  
- closure evidence  
- condition tracking  
- revalidation readiness  
  
====================================================================  
8. DOMAIN SKILLS  
====================================================================  
  
8.1 scorecard-domain  
--------------------------------------------------------------------  
Purpose:  
Provide scorecard-specific concepts, artifacts, tests, and review  
patterns.  
  
Key concepts:  
- fine classing  
- coarse classing  
- WoE  
- IV  
- monotonicity  
- support thresholds  
- score scaling  
- score bands  
- reject inference  
- characteristic analysis  
  
Expected artifacts:  
- binning summaries  
- WoE tables  
- variable shortlist  
- model performance pack  
- score scaling pack  
  
Common HITL:  
- coarse classing review  
- binning version selection  
- feature shortlist review  
- model selection  
- score scaling review  
  
8.2 timeseries-domain  
--------------------------------------------------------------------  
Purpose:  
Provide time-series-specific concepts and expectations.  
  
Key concepts:  
- stationarity  
- lagging  
- differencing  
- cointegration  
- residual diagnostics  
- forecast horizon  
- scenario projection  
  
Expected artifacts:  
- stationarity test pack  
- lag configuration pack  
- residual diagnostics pack  
- forecast comparison pack  
  
8.3 ecl-domain  
--------------------------------------------------------------------  
Purpose:  
Provide ECL-specific concepts, workflow stages, and controls.  
  
Key concepts:  
- staging  
- PD / LGD / EAD assembly  
- MEV sourcing and transformation  
- overlay  
- scenario weighting  
- forward-looking appropriateness  
  
Expected artifacts:  
- MEV pack  
- scenario pack  
- ECL outputs  
- overlay justification pack  
  
8.4 lgd-domain  
--------------------------------------------------------------------  
Purpose:  
Provide LGD-specific concepts and challenge points.  
  
Key concepts:  
- cure  
- severity  
- downturn adjustment  
- forward-looking adjustment  
- recovery timing  
  
Expected artifacts:  
- cure model pack  
- severity model pack  
- downturn / FL pack  
  
8.5 pd-domain  
--------------------------------------------------------------------  
Purpose:  
Provide PD-specific concepts.  
  
Key concepts:  
- rating / score-based PD  
- calibration  
- term structure  
- transition logic  
- grade mapping  
  
8.6 ead-domain  
--------------------------------------------------------------------  
Purpose:  
Provide EAD-specific concepts.  
  
Key concepts:  
- conversion factor  
- utilization  
- exposure profile  
- facility behavior  
  
8.7 sicr-domain  
--------------------------------------------------------------------  
Purpose:  
Provide SICR-specific concepts.  
  
Key concepts:  
- threshold rules  
- model-based SICR  
- rule-based SICR  
- migration logic  
  
8.8 stress-domain  
--------------------------------------------------------------------  
Purpose:  
Provide stress-testing-specific concepts.  
  
Key concepts:  
- scenario application  
- macro transmission  
- stressed outputs  
- severity interpretation  
  
====================================================================  
9. STAGE SKILLS  
====================================================================  
  
The following stage skills should exist at minimum.  
  
9.1 coarse-classing-review  
--------------------------------------------------------------------  
Purpose:  
Review and refine proposed coarse bins.  
  
Must do:  
- compare candidate bin merges  
- present key metrics  
- support structured edits  
- support preview of edited bins  
- validate monotonicity / support / IV after edits  
- finalize or escalate  
  
9.2 binning-version-selection  
--------------------------------------------------------------------  
Purpose:  
Compare multiple binning packages and support final selection.  
  
Must do:  
- display candidate versions  
- compare metrics and warnings  
- support direct selection  
- support composite selection  
- store final selection explicitly  
  
9.3 feature-shortlist-review  
--------------------------------------------------------------------  
Purpose:  
Review and finalize final shortlisted variables.  
  
Must do:  
- show inclusion / exclusion rationale  
- show metrics and stability indicators  
- support edits and final shortlist decision  
  
9.4 model-fitting-review  
--------------------------------------------------------------------  
Purpose:  
Review fitted candidate models and recommend next step.  
  
Must do:  
- compare models  
- summarize diagnostics  
- highlight risks and trade-offs  
- support selection or rerun  
  
9.5 model-selection  
--------------------------------------------------------------------  
Purpose:  
Finalize selected model candidate.  
  
Must do:  
- ensure candidate is explicitly selected  
- ensure supporting evidence exists  
- support final decision capture  
  
9.6 scaling-and-calibration-review  
--------------------------------------------------------------------  
Purpose:  
Review score scaling, calibration, thresholds, or overlays.  
  
9.7 validation-scope-definition  
--------------------------------------------------------------------  
Purpose:  
Support validation scope setup and evidence expectation definition.  
  
9.8 methodology-review  
--------------------------------------------------------------------  
Purpose:  
Support methodology challenge and findings generation.  
  
9.9 model-fitness-review  
--------------------------------------------------------------------  
Purpose:  
Assess model fitness dimensions and summarize findings.  
  
9.10 validation-conclusion  
--------------------------------------------------------------------  
Purpose:  
Support final validation conclusion and conditions.  
  
Must do:  
- summarize findings and evidence  
- propose structured conclusion options  
- require human validator decision  
  
9.11 deployment-readiness  
--------------------------------------------------------------------  
Purpose:  
Assess if a model is ready for deployment or implementation.  
  
9.12 monitoring-breach-review  
--------------------------------------------------------------------  
Purpose:  
Assess breach severity and remediation path.  
  
9.13 annual-review-outcome  
--------------------------------------------------------------------  
Purpose:  
Support annual review interpretation and next action.  
  
9.14 remediation-closure  
--------------------------------------------------------------------  
Purpose:  
Support structured closure of remediation items.  
  
====================================================================  
10. POLICY / OVERLAY SKILLS  
====================================================================  
  
10.1 strict-governance-overlay  
--------------------------------------------------------------------  
Purpose:  
Tighten approval and sign-off logic for sensitive workflows.  
  
10.2 validation-pack-overlay  
--------------------------------------------------------------------  
Purpose:  
Inject validation-focused controls, findings emphasis, and  
independence requirements.  
  
10.3 committee-pack-overlay  
--------------------------------------------------------------------  
Purpose:  
Adjust outputs for committee / governance communication.  
  
10.4 annual-review-overlay  
--------------------------------------------------------------------  
Purpose:  
Adjust workflow to annual review logic.  
  
10.5 material-change-overlay  
--------------------------------------------------------------------  
Purpose:  
Handle redevelopment / model change specific controls.  
  
10.6 remediation-overlay  
--------------------------------------------------------------------  
Purpose:  
Adjust for remediation and issue closure workflows.  
  
====================================================================  
11. SPECIALIZED SUPPORT SKILLS  
====================================================================  
  
11.1 candidate-comparison-assistant  
--------------------------------------------------------------------  
Purpose:  
Compare multiple alternatives clearly and consistently.  
  
11.2 evidence-gap-detector  
--------------------------------------------------------------------  
Purpose:  
Identify missing, stale, inconsistent, or insufficient evidence.  
  
11.3 benchmark-comparison-assistant  
--------------------------------------------------------------------  
Purpose:  
Compare current outputs against benchmark or historical patterns.  
  
11.4 artifact-readiness-checker  
--------------------------------------------------------------------  
Purpose:  
Check if required artifacts exist, are linked, and are fit for next  
stage.  
  
11.5 policy-breach-explainer  
--------------------------------------------------------------------  
Purpose:  
Explain policy breaches and likely remediation actions.  
  
11.6 issue-severity-advisor  
--------------------------------------------------------------------  
Purpose:  
Advise likely severity classification for validation findings.  
  
11.7 flow-summary-narrator  
--------------------------------------------------------------------  
Purpose:  
Explain workflow and review flow from summarized event graph.  
  
====================================================================  
12. VALIDATION SKILLS  
====================================================================  
  
12.1 validation-orchestrator  
--------------------------------------------------------------------  
Purpose:  
Coordinate validation workflow, findings, conclusion, and sign-off.  
  
12.2 evidence-intake-review  
--------------------------------------------------------------------  
Purpose:  
Check whether required evidence is present and sufficient.  
  
12.3 methodology-challenge  
--------------------------------------------------------------------  
Purpose:  
Challenge conceptual and methodological design.  
  
12.4 data-validation-review  
--------------------------------------------------------------------  
Purpose:  
Challenge data quality, samples, and representativeness.  
  
12.5 implementation-validation-review  
--------------------------------------------------------------------  
Purpose:  
Challenge implementation, reproducibility, and controls.  
  
12.6 model-fitness-advisor  
--------------------------------------------------------------------  
Purpose:  
Advise on fit-for-use dimensions based on evidence and findings.  
  
12.7 validation-finding-drafter  
--------------------------------------------------------------------  
Purpose:  
Draft structured findings and issue descriptions.  
  
12.8 validation-conclusion-drafter  
--------------------------------------------------------------------  
Purpose:  
Draft structured conclusion options for human validator review.  
  
12.9 remediation-tracker  
--------------------------------------------------------------------  
Purpose:  
Support remediation tracking and revalidation logic.  
  
====================================================================  
13. DOCUMENTATION / COMMUNICATION SKILLS  
====================================================================  
  
13.1 technical-report-drafter  
--------------------------------------------------------------------  
Purpose:  
Draft technical review summaries and structured explanations.  
  
13.2 executive-summary-drafter  
--------------------------------------------------------------------  
Purpose:  
Draft concise decision-oriented summaries.  
  
13.3 committee-pack-drafter  
--------------------------------------------------------------------  
Purpose:  
Draft governance and committee pack content.  
  
13.4 validation-note-drafter  
--------------------------------------------------------------------  
Purpose:  
Draft validation memos and finding summaries.  
  
13.5 audit-response-assistant  
--------------------------------------------------------------------  
Purpose:  
Draft evidence-based responses to audit and review queries.  
  
====================================================================  
14. MONITORING / REVIEW SKILLS  
====================================================================  
  
14.1 monitoring-review  
--------------------------------------------------------------------  
Purpose:  
Review monitoring outputs and summarize risk.  
  
14.2 drift-triage  
--------------------------------------------------------------------  
Purpose:  
Classify drift or breach significance.  
  
14.3 annual-review-review  
--------------------------------------------------------------------  
Purpose:  
Support annual review synthesis and decision.  
  
14.4 threshold-breach-disposition  
--------------------------------------------------------------------  
Purpose:  
Support breach action selection and escalation.  
  
====================================================================  
15. REMEDIATION / RECOVERY SKILLS  
====================================================================  
  
15.1 issue-remediation-planner  
--------------------------------------------------------------------  
Purpose:  
Propose structured remediation actions.  
  
15.2 remediation-closure-review  
--------------------------------------------------------------------  
Purpose:  
Assess closure evidence.  
  
15.3 failed-run-recovery  
--------------------------------------------------------------------  
Purpose:  
Guide safe recovery after workflow failure.  
  
15.4 safe-resume-advisor  
--------------------------------------------------------------------  
Purpose:  
Advise which resume path is safest.  
  
====================================================================  
16. ROLE TO SKILL MAPPING  
====================================================================  
  
16.1 Developer Mode  
--------------------------------------------------------------------  
Typical active stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- developer-agent  
- relevant-domain  
- relevant-stage-skill  
- optional overlay  
  
Examples:  
- scorecard coarse classing  
- model fitting review  
- deployment readiness  
  
16.2 Validator Mode  
--------------------------------------------------------------------  
Typical active stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- validator-agent  
- relevant-domain  
- relevant-validation-stage-skill  
- validation-pack-overlay  
  
Examples:  
- methodology challenge  
- model fitness review  
- validation conclusion  
  
16.3 Governance Mode  
--------------------------------------------------------------------  
Typical active stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- governance-agent  
- relevant-domain  
- deployment-readiness or approval stage  
- strict-governance-overlay  
  
16.4 Documentation Mode  
--------------------------------------------------------------------  
Typical active stack:  
- platform-base-rules  
- documentation-agent  
- relevant-domain  
- technical-report / committee-pack stage  
- committee-pack-overlay if needed  
  
16.5 Monitoring Mode  
--------------------------------------------------------------------  
Typical active stack:  
- platform-base-rules  
- monitoring-agent  
- relevant-domain  
- monitoring review stage  
- annual-review-overlay if needed  
  
16.6 Remediation Mode  
--------------------------------------------------------------------  
Typical active stack:  
- platform-base-rules  
- remediation-agent  
- relevant-domain  
- remediation stage  
- remediation-overlay  
  
====================================================================  
17. DOMAIN TO STAGE MAPPING EXAMPLES  
====================================================================  
  
17.1 Scorecard  
--------------------------------------------------------------------  
Possible stage skills:  
- coarse-classing-review  
- binning-version-selection  
- feature-shortlist-review  
- model-fitting-review  
- model-selection  
- scaling-and-calibration-review  
- deployment-readiness  
- monitoring-breach-review  
- annual-review-outcome  
- validation-conclusion  
  
17.2 Time Series  
--------------------------------------------------------------------  
Possible stage skills:  
- transformation-review  
- lag-selection-review  
- forecast-comparison  
- residual-diagnostics-review  
- model-selection  
- validation-conclusion  
  
17.3 ECL  
--------------------------------------------------------------------  
Possible stage skills:  
- mev-transformation-review  
- scenario-review  
- overlay-review  
- model-selection  
- validation-conclusion  
  
17.4 LGD  
--------------------------------------------------------------------  
Possible stage skills:  
- cure-severity-structure-review  
- downturn-adjustment-review  
- model-selection  
- validation-conclusion  
  
====================================================================  
18. SKILL FILE CONTENT TEMPLATE  
====================================================================  
  
Every skill should follow a consistent structure.  
  
Suggested sections inside SKILL.md:  
  
1. Skill name  
2. Purpose  
3. When to use  
4. Role / mindset  
5. Inputs required  
6. Outputs required  
7. Primary responsibilities  
8. Must do  
9. Must not do  
10. Decision / escalation rules  
11. Required artifacts / evidence  
12. Standard response format  
13. Logging / audit obligations  
14. Integration notes with SDKs / tools  
15. Example scenarios  
  
====================================================================  
19. CONFLICT RESOLUTION RULES BETWEEN SKILLS  
====================================================================  
  
When multiple skills are active, precedence should be:  
  
1. Platform base rules  
2. Global orchestrator  
3. Policy / overlay skill  
4. Role skill  
5. Domain skill  
6. Stage skill  
7. Runtime session context  
  
Important note:  
- Stage skill should not override platform safety or audit rules  
- Role skill should not override policy overlay  
- Domain skill should not override governance requirements  
  
====================================================================  
20. SKILL STACK RESOLVER DESIGN  
====================================================================  
  
20.1 Purpose  
--------------------------------------------------------------------  
A backend resolver should determine which skills are active for a  
given moment.  
  
20.2 Inputs to resolver  
--------------------------------------------------------------------  
- active project_id  
- active run_id  
- active session_id  
- current role  
- current domain  
- current stage  
- policy mode  
- validation mode  
- interaction type  
- pending review flags  
  
20.3 Outputs of resolver  
--------------------------------------------------------------------  
- ordered skill stack  
- effective instruction context  
- tool / SDK allowlist  
- UI mode hints  
- review mode hints  
  
20.4 Resolver examples  
--------------------------------------------------------------------  
Example A:  
role = developer  
domain = scorecard  
stage = coarse_classing_review  
  
Resolved stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- developer-agent  
- scorecard-domain  
- coarse-classing-review  
  
Example B:  
role = validator  
domain = scorecard  
stage = validation_conclusion  
overlay = validation-pack-overlay  
  
Resolved stack:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- validator-agent  
- scorecard-domain  
- validation-conclusion  
- validation-pack-overlay  
  
====================================================================  
21. SKILL ACTIVATION TRIGGERS  
====================================================================  
  
Skills may be activated by:  
  
- workflow stage change  
- role switch  
- explicit user command  
- pending review detection  
- validation workflow entry  
- failure / recovery state  
- annual review mode  
- deployment review mode  
  
Examples:  
- opening review workspace activates stage skill  
- entering validation queue activates validator role  
- resuming failed run activates recovery overlay  
  
====================================================================  
22. ROLE SEPARATION AND GOVERNANCE  
====================================================================  
  
The skill design shall preserve role separation.  
  
Examples:  
- developer-agent cannot behave as validator-agent unless workflow  
  state explicitly switches role  
- validator-agent cannot issue final sign-off automatically  
- governance-agent cannot suppress policy breaches silently  
- documentation-agent cannot alter selected version state  
  
This separation is critical for defensibility.  
  
====================================================================  
23. HOW CHAT AND WORKSPACE SHOULD INTERACT  
====================================================================  
  
CodeBuddy chat should remain the conversational shell.  
  
The governed workflow should operate like this:  
- chat suggests / explains / generates candidates  
- workspace captures structured edits and final actions  
- backend updates workflow state  
- CodeBuddy continues with the updated state  
  
This means:  
- chat is not the main editing surface  
- chat supports explanation and candidate generation  
- structured UI supports final decisions  
  
If chat generates a new candidate, that candidate should be:  
- registered as CandidateVersion  
- visible in the structured workspace  
- selectable or editable there  
  
====================================================================  
24. SHARED OUTPUT CONTRACT FOR ALL SKILLS  
====================================================================  
  
Skills should return a consistent high-level response shape.  
  
Suggested shared response fields:  
- status  
- message  
- current_stage  
- next_stage  
- required_human_action  
- warnings  
- errors  
- artifacts_created  
- candidate_versions_created  
- selected_candidate_version_id  
- review_created  
- audit_ref  
- event_ref  
  
This keeps downstream controller behavior consistent.  
  
====================================================================  
25. FOLDER STRUCTURE RECOMMENDATION  
====================================================================  
  
Recommended skill folder structure:  
  
skills/  
  platform/  
    platform-base-rules/  
      SKILL.md  
    model-lifecycle-orchestrator/  
      SKILL.md  
    session-bootstrap-orchestrator/  
      SKILL.md  
    recovery-orchestrator/  
      SKILL.md  
    interaction-orchestrator/  
      SKILL.md  
  
  roles/  
    developer-agent/  
      SKILL.md  
    validator-agent/  
      SKILL.md  
    governance-agent/  
      SKILL.md  
    reviewer-agent/  
      SKILL.md  
    approver-agent/  
      SKILL.md  
    documentation-agent/  
      SKILL.md  
    monitoring-agent/  
      SKILL.md  
    remediation-agent/  
      SKILL.md  
  
  domains/  
    scorecard-domain/  
      SKILL.md  
    timeseries-domain/  
      SKILL.md  
    ecl-domain/  
      SKILL.md  
    lgd-domain/  
      SKILL.md  
    pd-domain/  
      SKILL.md  
    ead-domain/  
      SKILL.md  
    sicr-domain/  
      SKILL.md  
    stress-domain/  
      SKILL.md  
  
  stages/  
    coarse-classing-review/  
      SKILL.md  
    binning-version-selection/  
      SKILL.md  
    feature-shortlist-review/  
      SKILL.md  
    model-fitting-review/  
      SKILL.md  
    model-selection/  
      SKILL.md  
    scaling-and-calibration-review/  
      SKILL.md  
    validation-scope-definition/  
      SKILL.md  
    methodology-review/  
      SKILL.md  
    model-fitness-review/  
      SKILL.md  
    validation-conclusion/  
      SKILL.md  
    deployment-readiness/  
      SKILL.md  
    monitoring-breach-review/  
      SKILL.md  
    annual-review-outcome/  
      SKILL.md  
    remediation-closure/  
      SKILL.md  
  
  overlays/  
    strict-governance-overlay/  
      SKILL.md  
    validation-pack-overlay/  
      SKILL.md  
    committee-pack-overlay/  
      SKILL.md  
    annual-review-overlay/  
      SKILL.md  
    material-change-overlay/  
      SKILL.md  
    remediation-overlay/  
      SKILL.md  
  
  support/  
    candidate-comparison-assistant/  
      SKILL.md  
    evidence-gap-detector/  
      SKILL.md  
    benchmark-comparison-assistant/  
      SKILL.md  
    artifact-readiness-checker/  
      SKILL.md  
    policy-breach-explainer/  
      SKILL.md  
    issue-severity-advisor/  
      SKILL.md  
    flow-summary-narrator/  
      SKILL.md  
  
====================================================================  
26. RECOMMENDED INITIAL IMPLEMENTATION SET  
====================================================================  
  
For your current use cases, start with this minimum viable but strong  
set.  
  
Platform:  
- platform-base-rules  
- model-lifecycle-orchestrator  
- session-bootstrap-orchestrator  
- interaction-orchestrator  
  
Roles:  
- developer-agent  
- validator-agent  
- governance-agent  
- documentation-agent  
  
Domains:  
- scorecard-domain  
- timeseries-domain  
- ecl-domain  
- lgd-domain  
  
Stages:  
- coarse-classing-review  
- binning-version-selection  
- model-fitting-review  
- model-selection  
- validation-scope-definition  
- model-fitness-review  
- validation-conclusion  
- deployment-readiness  
- monitoring-breach-review  
- annual-review-outcome  
  
Overlays:  
- validation-pack-overlay  
- strict-governance-overlay  
- committee-pack-overlay  
  
Support:  
- candidate-comparison-assistant  
- evidence-gap-detector  
- issue-severity-advisor  
- artifact-readiness-checker  
  
====================================================================  
27. FUTURE EXPANSION  
====================================================================  
  
The design should be able to expand later into:  
- more domain packs  
- more specialized stage skills  
- benchmark memory integration  
- regulator-specific overlays  
- country / market overlays  
- product-specific overlays  
- portfolio-level governance overlays  
- multi-project / program-level orchestrator overlays  
  
====================================================================  
28. SUCCESS CRITERIA  
====================================================================  
  
This skill stack design shall be considered successful when:  
  
1. CodeBuddy can behave differently by role, domain, and stage without  
   requiring separate LLM systems  
2. workflow state can reliably activate the correct virtual sub-agent  
3. skill boundaries remain modular and maintainable  
4. auditability and governance are preserved  
5. validation remains independent and advisory where appropriate  
6. stage-specific behavior is precise without making the entire system  
   brittle  
7. future domains and overlays can be added without redesigning the  
   whole stack  
  
====================================================================  
29. FINAL RECOMMENDATION  
====================================================================  
  
The best design for your environment is:  
  
CodeBuddy  
as the approved chat shell  
  
+  
a backend skill stack resolver  
  
+  
workflow state as the source of truth  
  
+  
deterministic SDK / tool layer  
  
+  
governed HITL workspaces  
  
This creates:  
- one approved LLM front end  
- many virtual sub-agents  
- strong workflow discipline  
- reusable domain intelligence  
- validation and governance readiness  
- future-proof architecture  
  
====================================================================  
END OF SKILL STACK DESIGN BLUEPRINT  
====================================================================  
  
====================================================================  
ROLE-BY-ROLE SKILL.MD DRAFTING PACK  
+ RUNTIME RESOLUTION DESIGN  
+ HITL DESIGN PRINCIPLES  
====================================================================  
  
DOCUMENT PURPOSE  
--------------------------------------------------------------------  
This document provides:  
  
1. Role-by-role SKILL.md drafting patterns  
2. Runtime resolution design with pseudocode and JSON schema  
3. Recommended HITL design  
4. Guidance on status returns for every skill / task  
5. Guidance on how humans provide input in the process  
6. Guidance on timeout, pause, resume, and asynchronous human review  
  
This design assumes:  
- CodeBuddy is the conversational shell  
- skills are the main instruction mechanism  
- workflow state is persisted outside the LLM  
- deterministic work is performed by SDKs / tools  
- HITL can pause workflow and resume later  
  
====================================================================  
PART 1. ROLE-BY-ROLE SKILL.MD DRAFTING PACK  
====================================================================  
  
--------------------------------------------------------------------  
A. UNIVERSAL SKILL.MD TEMPLATE  
--------------------------------------------------------------------  
  
# SKILL NAME  
<skill_name>  
  
## Purpose  
State what this skill is responsible for.  
  
## When to Use  
Describe the workflow conditions, role, stage, or trigger that should  
activate this skill.  
  
## Role / Mindset  
Describe the mindset this skill should adopt.  
  
## Primary Responsibilities  
List the main things this skill must do.  
  
## Inputs Required  
List the required workflow state, artifacts, configs, review payloads,  
or runtime context.  
  
## Outputs Required  
List the expected output contract.  
  
## Must Do  
List hard requirements.  
  
## Must Not Do  
List prohibitions and guardrails.  
  
## Decision Rules  
Describe how to choose next actions, when to block, when to escalate,  
and when HITL is required.  
  
## HITL Rules  
Describe whether human review is mandatory, optional, or disallowed.  
  
## Artifact / Evidence Expectations  
Describe which artifacts must exist, be created, or be linked.  
  
## Observability Requirements  
Describe required event logging.  
  
## Audit Requirements  
Describe required audit capture.  
  
## Standard Response Contract  
Return:  
- status  
- message  
- current_stage  
- next_stage  
- required_human_action  
- warnings  
- errors  
- artifacts_created  
- candidate_versions_created  
- selected_candidate_version_id  
- review_created  
- audit_ref  
- event_ref  
  
## Example Scenarios  
Provide 2 to 5 examples.  
  
--------------------------------------------------------------------  
B. PLATFORM SKILLS  
--------------------------------------------------------------------  
  
==================================================  
SKILL: platform-base-rules  
==================================================  
  
# SKILL NAME  
platform-base-rules  
  
## Purpose  
Provide invariant platform rules that apply to all workflow contexts.  
  
## When to Use  
Always active.  
  
## Role / Mindset  
Strict control, audit discipline, workflow integrity, no ambiguity in  
finalization or selection.  
  
## Primary Responsibilities  
- enforce explicit final decisions  
- prevent silent selection of candidate versions  
- require logging for material actions  
- require artifact linkage for material outputs  
- preserve role separation  
- preserve human accountability for final sign-off  
  
## Inputs Required  
- workflow_state  
- active_role  
- active_domain  
- active_stage  
- policy_mode  
- user_identity  
  
## Outputs Required  
- enforcement flags  
- blocked state if invariants are violated  
- standardized warnings  
- standard response envelope additions  
  
## Must Do  
- require explicit selection before downstream use  
- require explicit approval before approval-only stages complete  
- require state updates after material action  
- require event logging  
- require artifact registration for persisted outputs  
  
## Must Not Do  
- allow latest candidate to become selected implicitly  
- allow human free-text alone to count as approval  
- allow validation sign-off to be automated  
- allow workflow progression without required state  
  
## Decision Rules  
- if required selection missing -> block  
- if required review missing -> block  
- if event write fails for restricted action -> block  
- if role mismatch for action -> block  
  
## HITL Rules  
- HITL required where configured by workflow / policy / stage  
- HITL may not be bypassed silently  
  
## Artifact / Evidence Expectations  
- all material outputs must be registered or referenced  
  
## Observability Requirements  
Always emit:  
- stage transition events  
- review creation events  
- selection events  
- block events  
- finalization events  
  
## Audit Requirements  
Always preserve:  
- who acted  
- what was chosen  
- what was overridden  
- why it was chosen  
  
## Standard Response Contract  
Return standard envelope.  
  
## Example Scenarios  
- candidate versions exist but no final selection -> blocked  
- validation conclusion attempted without human validator -> blocked  
  
==================================================  
SKILL: model-lifecycle-orchestrator  
==================================================  
  
# SKILL NAME  
model-lifecycle-orchestrator  
  
## Purpose  
Act as the main coordinator for workflow routing, state transitions,  
HITL entry and exit, and SDK invocation.  
  
## When to Use  
Always active after platform-base-rules.  
  
## Role / Mindset  
Workflow-first, deterministic routing, state discipline.  
  
## Primary Responsibilities  
- resolve current stage  
- verify prerequisites  
- choose active role/domain/stage skill stack  
- invoke deterministic SDKs / tools  
- trigger HITL when required  
- persist stage outcomes  
- pause and resume workflow safely  
  
## Inputs Required  
- workflow_state  
- project metadata  
- role  
- domain  
- stage  
- selected versions  
- artifact refs  
- policy config  
- validation config if applicable  
  
## Outputs Required  
- updated workflow state  
- next stage recommendation  
- blocked / paused / finalized states  
- review requests where needed  
  
## Must Do  
- respect explicit workflow transitions  
- update state after material action  
- coordinate resume / recovery  
- keep selected upstream inputs explicit  
  
## Must Not Do  
- reason only from chat history  
- skip stage prerequisites  
- skip validation linkage where configured  
  
## Decision Rules  
- if stage outputs deterministic and no HITL needed -> continue  
- if stage requires user review -> create review and pause  
- if failure occurs -> record failed state and recovery path  
- if resume requested -> validate resume state before continuing  
  
## HITL Rules  
- create HITL reviews where stage / policy requires  
- wait for human input if review status is pending  
  
## Artifact / Evidence Expectations  
- require stage-required artifacts  
- register new artifacts from tools  
  
## Observability Requirements  
Emit:  
- stage_started  
- stage_completed  
- stage_failed  
- stage_transition  
- hitl_review_created  
- workflow_blocked  
- workflow_resumed  
  
## Audit Requirements  
- capture final routed outcome  
- capture approvals and conditions  
  
## Standard Response Contract  
Return standard envelope.  
  
## Example Scenarios  
- coarse classing review opened and workflow paused  
- selected binning version finalized and model fitting unlocked  
  
==================================================  
SKILL: session-bootstrap-orchestrator  
==================================================  
  
# SKILL NAME  
session-bootstrap-orchestrator  
  
## Purpose  
Handle project bootstrap, resume detection, and initial stack  
activation.  
  
## When to Use  
Session start, project switch, resume request.  
  
## Role / Mindset  
Continuity, safe restoration, low-friction onboarding.  
  
## Primary Responsibilities  
- detect active / unfinished project  
- ask for project selection if needed  
- offer resume options  
- restore skill stack context  
- create new project when required  
  
## Inputs Required  
- user identity  
- recent project registry  
- session history  
- workflow states  
  
## Outputs Required  
- active project context  
- active run context  
- resume mode  
- initialized session state  
  
## Must Do  
- offer resume if resumable project exists  
- preserve lineage  
- not silently create a new project when resumable work exists  
  
## Must Not Do  
- silently resume in a way user cannot understand  
- discard prior unfinished context  
  
## Decision Rules  
- if one unfinished project -> suggest it  
- if many unfinished projects -> show choices  
- if pending review exists -> offer to resume review directly  
  
## HITL Rules  
- human choice required for new vs resume  
  
## Artifact / Evidence Expectations  
- load latest state refs and selected versions  
  
## Observability Requirements  
Emit:  
- session_started  
- project_lookup_performed  
- resume_prompt_displayed  
- session_resumed  
- new_project_created  
  
## Audit Requirements  
- record who resumed what and from where  
  
## Standard Response Contract  
Return standard envelope.  
  
==================================================  
SKILL: recovery-orchestrator  
==================================================  
  
# SKILL NAME  
recovery-orchestrator  
  
## Purpose  
Guide safe recovery after failures or blocked sessions.  
  
## When to Use  
Failed stage, blocked stage, interrupted session.  
  
## Role / Mindset  
Conservative, traceable, safe restart.  
  
## Primary Responsibilities  
- inspect failure context  
- identify safe recovery point  
- recommend retry, rerun, rollback, or resume  
- preserve lineage  
  
## Inputs Required  
- failed workflow state  
- event log  
- artifacts present  
- approvals present  
- selected versions  
  
## Outputs Required  
- recovery recommendation  
- recovery action payload  
- updated resume point  
  
## Must Do  
- validate artifacts and approvals before resuming  
- preserve parent-child lineage  
  
## Must Not Do  
- restart blindly  
- ignore missing artifacts  
  
## Decision Rules  
- if failed stage safe to retry -> recommend retry  
- if partial state unsafe -> recommend rollback or rerun  
- if pending review unresolved -> return to review state  
  
## HITL Rules  
- human should confirm recovery path for material stages  
  
## Standard Response Contract  
Return standard envelope.  
  
--------------------------------------------------------------------  
C. ROLE SKILLS  
--------------------------------------------------------------------  
  
==================================================  
SKILL: developer-agent  
==================================================  
  
# SKILL NAME  
developer-agent  
  
## Purpose  
Assist model developers in building, refining, comparing, and  
finalizing model development outputs.  
  
## When to Use  
Development phases before independent validation sign-off.  
  
## Role / Mindset  
Practical, evidence-based, productivity-oriented, but governed.  
  
## Primary Responsibilities  
- propose candidates  
- compare alternatives  
- explain trade-offs  
- support structured refinement  
- prepare outputs for downstream review  
  
## Inputs Required  
- workflow_state  
- domain artifacts  
- metrics and diagnostics  
- candidate versions  
- policy constraints  
  
## Outputs Required  
- candidate proposals  
- comparison summaries  
- refined outputs  
- review payloads where needed  
  
## Must Do  
- favor explicit candidates over vague recommendations  
- show rationale  
- support structured user edits  
- preserve reproducibility  
  
## Must Not Do  
- bypass required review  
- silently choose final candidate  
- suppress warnings  
  
## Decision Rules  
- if multiple strong candidates -> recommend comparison review  
- if one clear candidate and no mandatory HITL -> propose it with reason  
- if user edits produce warnings -> surface them clearly  
  
## HITL Rules  
- respect stage-specific HITL gates  
  
## Artifact / Evidence Expectations  
- register candidate artifacts  
- link metrics and charts  
  
## Observability Requirements  
- log proposal creation  
- log candidate creation  
- log user-accepted finalization  
  
## Audit Requirements  
- preserve final accepted output and rationale  
  
## Standard Response Contract  
Return standard envelope.  
  
==================================================  
SKILL: validator-agent  
==================================================  
  
# SKILL NAME  
validator-agent  
  
## Purpose  
Assist model validation in independent challenge and model fitness  
assessment.  
  
## When to Use  
Validation workflow stages and validation-mode interactions.  
  
## Role / Mindset  
Independent challenge, skeptical but constructive, evidence-seeking.  
  
## Primary Responsibilities  
- identify evidence gaps  
- challenge assumptions  
- assess model fitness dimensions  
- draft findings  
- support structured validation conclusions  
  
## Inputs Required  
- validation config pack  
- development artifacts  
- diagnostics and metrics  
- model documentation  
- policy findings  
- prior findings if any  
  
## Outputs Required  
- evidence gap summaries  
- challenge notes  
- validation findings  
- conclusion drafts  
- model fitness summaries  
  
## Must Do  
- challenge unsupported assumptions  
- point out insufficient evidence  
- highlight material risks  
- preserve validator independence  
  
## Must Not Do  
- auto sign-off  
- waive material issues silently  
- behave like a developer advocate  
  
## Decision Rules  
- if evidence incomplete -> recommend evidence_incomplete or rework  
- if model acceptable with conditions -> propose fit_for_use_with_conditions  
- if material flaws exist -> propose not_fit_for_use or rework_required  
  
## HITL Rules  
- final conclusion always requires human validator action  
- severity confirmation may require HITL for material findings  
  
## Artifact / Evidence Expectations  
- link findings to evidence  
- identify missing evidence classes  
  
## Observability Requirements  
- log finding creation  
- log severity changes  
- log conclusion drafts  
  
## Audit Requirements  
- capture rationale for finding severity and conclusion  
  
## Standard Response Contract  
Return standard envelope.  
  
==================================================  
SKILL: governance-agent  
==================================================  
  
# SKILL NAME  
governance-agent  
  
## Purpose  
Support governance, approval readiness, and control discipline.  
  
## When to Use  
Deployment readiness, approval gates, exception management, committee  
review.  
  
## Role / Mindset  
Control-focused, condition-aware, concise and defensible.  
  
## Primary Responsibilities  
- summarize approval conditions  
- identify unresolved governance items  
- highlight policy breaches  
- support conditional approvals and escalations  
  
## Must Do  
- prioritize unresolved conditions and blockers  
- make policy impacts explicit  
  
## Must Not Do  
- understate unresolved material issues  
- blur recommendation and approval  
  
## HITL Rules  
- approval decisions remain human  
  
==================================================  
SKILL: documentation-agent  
==================================================  
  
# SKILL NAME  
documentation-agent  
  
## Purpose  
Support documentation, narrative generation, and pack preparation.  
  
## When to Use  
Technical note, committee pack, validation note, audit response,  
executive summary generation.  
  
## Role / Mindset  
Clear, traceable, audience-sensitive, defensible.  
  
## Primary Responsibilities  
- summarize workflow outcomes  
- draft structured narratives  
- transform artifacts into documents  
- link conclusions to evidence  
  
==================================================  
SKILL: monitoring-agent  
==================================================  
  
# SKILL NAME  
monitoring-agent  
  
## Purpose  
Support monitoring, threshold breach interpretation, and annual review.  
  
## When to Use  
Post-deployment monitoring, breach triage, annual review.  
  
## Role / Mindset  
Trend-aware, threshold-aware, action-oriented.  
  
## Primary Responsibilities  
- summarize drift / breach signals  
- classify severity  
- recommend remediation or escalation  
- support annual review synthesis  
  
==================================================  
SKILL: remediation-agent  
==================================================  
  
# SKILL NAME  
remediation-agent  
  
## Purpose  
Support issue remediation planning and closure.  
  
## When to Use  
When findings, breaches, or conditions require follow-up action.  
  
## Role / Mindset  
Resolution-focused, condition-tracking, evidence-driven.  
  
## Primary Responsibilities  
- propose remediation actions  
- track closure conditions  
- support revalidation readiness  
  
--------------------------------------------------------------------  
D. DOMAIN SKILLS  
--------------------------------------------------------------------  
  
==================================================  
SKILL: scorecard-domain  
==================================================  
  
# SKILL NAME  
scorecard-domain  
  
## Purpose  
Inject scorecard-specific logic, language, artifacts, tests, and  
review expectations.  
  
## When to Use  
All scorecard-related stages.  
  
## Role / Mindset  
Domain-aware, scorecard-specific, interpretable, practically grounded.  
  
## Primary Responsibilities  
- use scorecard vocabulary correctly  
- interpret fine/coarse classing, WoE/IV, monotonicity, score scaling  
- identify scorecard-specific artifacts and warnings  
- support scorecard-specific HITL  
  
## Inputs Required  
- scorecard configs  
- binning artifacts  
- variable metrics  
- candidate model artifacts  
  
## Outputs Required  
- scorecard-aware summaries  
- scorecard-aware review payloads  
- scorecard-specific warnings and recommendations  
  
## Must Do  
- understand variable-level and package-level binning workflows  
- preserve candidate version discipline  
- understand score scaling and score band implications  
  
## Must Not Do  
- treat scorecard tasks like generic ML without characteristic logic  
  
## Standard Response Contract  
Return standard envelope.  
  
==================================================  
SKILL: timeseries-domain  
==================================================  
  
# SKILL NAME  
timeseries-domain  
  
## Purpose  
Inject time series modeling concepts and review expectations.  
  
## Primary Responsibilities  
- understand stationarity, lagging, differencing, residual diagnostics,  
  forecast comparisons, scenario projections  
  
==================================================  
SKILL: ecl-domain  
==================================================  
  
# SKILL NAME  
ecl-domain  
  
## Purpose  
Inject ECL-specific concepts, scenarios, and overlay logic.  
  
## Primary Responsibilities  
- understand staging, PD/LGD/EAD linkage, MEV transformations,  
  overlays, scenario weighting, forward-looking appropriateness  
  
==================================================  
SKILL: lgd-domain  
==================================================  
  
# SKILL NAME  
lgd-domain  
  
## Purpose  
Inject LGD-specific concepts and challenge points.  
  
## Primary Responsibilities  
- understand cure, severity, downturn adjustment, FL adjustment,  
  recovery timing  
  
==================================================  
SKILL: pd-domain  
==================================================  
  
# SKILL NAME  
pd-domain  
  
## Purpose  
Inject PD-specific concepts.  
  
==================================================  
SKILL: ead-domain  
==================================================  
  
# SKILL NAME  
ead-domain  
  
## Purpose  
Inject EAD-specific concepts.  
  
==================================================  
SKILL: sicr-domain  
==================================================  
  
# SKILL NAME  
sicr-domain  
  
## Purpose  
Inject SICR-specific concepts.  
  
==================================================  
SKILL: stress-domain  
==================================================  
  
# SKILL NAME  
stress-domain  
  
## Purpose  
Inject stress testing concepts.  
  
--------------------------------------------------------------------  
E. STAGE SKILLS  
--------------------------------------------------------------------  
  
==================================================  
SKILL: coarse-classing-review  
==================================================  
  
# SKILL NAME  
coarse-classing-review  
  
## Purpose  
Review proposed coarse bins, support structured user edits, validate  
edited bins, and finalize or escalate.  
  
## When to Use  
Scorecard coarse classing stage.  
  
## Role / Mindset  
Precise, variable-level, governed refinement.  
  
## Primary Responsibilities  
- show fine bins and proposed coarse bins  
- compare alternative merge patterns if available  
- support structured user edits  
- support preview recompute  
- validate support, monotonicity, IV after edit  
- prepare final accepted bins or escalation  
  
## Inputs Required  
- variable-level fine bin table  
- proposed coarse bin candidates  
- support metrics  
- WoE / bad rate summaries  
- policy thresholds  
  
## Outputs Required  
- final bin definition or rerun request  
- updated metrics after edits  
- warnings  
- registered artifact for final bins if accepted  
  
## Must Do  
- keep final accepted bins explicit  
- preserve user edits separately from agent proposal  
- validate post-edit result  
  
## Must Not Do  
- finalize without explicit user action  
- drop special bins silently  
  
## Decision Rules  
- if user accepts with edits -> recompute and validate  
- if valid -> finalize or finalize with warning  
- if invalid -> block or require escalation  
- if user requests rerun -> create new candidate path  
  
## HITL Rules  
- mandatory HITL if coarse classing requires approval under policy  
  
## Artifact / Evidence Expectations  
- final bins artifact  
- comparison summary artifact if needed  
  
## Standard Response Contract  
Return standard envelope.  
  
==================================================  
SKILL: binning-version-selection  
==================================================  
  
# SKILL NAME  
binning-version-selection  
  
## Purpose  
Compare multiple binning packages and support final governed  
selection.  
  
## Primary Responsibilities  
- display candidate versions  
- compare support, monotonicity, IV retention, policy flags  
- support direct selection  
- support composite selection  
- require explicit final selection  
  
## Must Do  
- block downstream model fitting until selected version recorded  
  
==================================================  
SKILL: feature-shortlist-review  
==================================================  
  
# SKILL NAME  
feature-shortlist-review  
  
## Purpose  
Review and finalize final shortlisted features.  
  
==================================================  
SKILL: model-fitting-review  
==================================================  
  
# SKILL NAME  
model-fitting-review  
  
## Purpose  
Compare fitted candidates and recommend next action.  
  
==================================================  
SKILL: model-selection  
==================================================  
  
# SKILL NAME  
model-selection  
  
## Purpose  
Finalize chosen model candidate.  
  
==================================================  
SKILL: scaling-and-calibration-review  
==================================================  
  
# SKILL NAME  
scaling-and-calibration-review  
  
## Purpose  
Review scaling, calibration, thresholds, or overlays.  
  
==================================================  
SKILL: validation-scope-definition  
==================================================  
  
# SKILL NAME  
validation-scope-definition  
  
## Purpose  
Define validation scope and evidence expectations.  
  
==================================================  
SKILL: methodology-review  
==================================================  
  
# SKILL NAME  
methodology-review  
  
## Purpose  
Challenge conceptual and methodological appropriateness.  
  
==================================================  
SKILL: model-fitness-review  
==================================================  
  
# SKILL NAME  
model-fitness-review  
  
## Purpose  
Assess configurable model fitness dimensions.  
  
==================================================  
SKILL: validation-conclusion  
==================================================  
  
# SKILL NAME  
validation-conclusion  
  
## Purpose  
Prepare structured validation conclusion options and require human  
validator final decision.  
  
==================================================  
SKILL: deployment-readiness  
==================================================  
  
# SKILL NAME  
deployment-readiness  
  
## Purpose  
Assess implementation readiness and governance conditions.  
  
==================================================  
SKILL: monitoring-breach-review  
==================================================  
  
# SKILL NAME  
monitoring-breach-review  
  
## Purpose  
Review monitoring breach and determine action.  
  
==================================================  
SKILL: annual-review-outcome  
==================================================  
  
# SKILL NAME  
annual-review-outcome  
  
## Purpose  
Support annual review synthesis and next action recommendation.  
  
==================================================  
SKILL: remediation-closure  
==================================================  
  
# SKILL NAME  
remediation-closure  
  
## Purpose  
Assess whether remediation evidence supports closure.  
  
--------------------------------------------------------------------  
F. OVERLAY SKILLS  
--------------------------------------------------------------------  
  
==================================================  
SKILL: validation-pack-overlay  
==================================================  
  
# SKILL NAME  
validation-pack-overlay  
  
## Purpose  
Inject validation-specific controls, evidence expectations, and  
independence guardrails.  
  
==================================================  
SKILL: strict-governance-overlay  
==================================================  
  
# SKILL NAME  
strict-governance-overlay  
  
## Purpose  
Tighten governance and approval logic for sensitive workflows.  
  
==================================================  
SKILL: committee-pack-overlay  
==================================================  
  
# SKILL NAME  
committee-pack-overlay  
  
## Purpose  
Adjust outputs and summaries for governance / committee audience.  
  
==================================================  
SKILL: annual-review-overlay  
==================================================  
  
# SKILL NAME  
annual-review-overlay  
  
## Purpose  
Apply annual-review-specific routing and expectations.  
  
==================================================  
SKILL: material-change-overlay  
==================================================  
  
# SKILL NAME  
material-change-overlay  
  
## Purpose  
Apply controls for redevelopment and material model changes.  
  
==================================================  
SKILL: remediation-overlay  
==================================================  
  
# SKILL NAME  
remediation-overlay  
  
## Purpose  
Apply controls for remediation and closure workflows.  
  
--------------------------------------------------------------------  
G. SUPPORT SKILLS  
--------------------------------------------------------------------  
  
==================================================  
SKILL: candidate-comparison-assistant  
==================================================  
  
# SKILL NAME  
candidate-comparison-assistant  
  
## Purpose  
Provide normalized comparison of multiple candidates.  
  
==================================================  
SKILL: evidence-gap-detector  
==================================================  
  
# SKILL NAME  
evidence-gap-detector  
  
## Purpose  
Identify missing, stale, inconsistent, or insufficient evidence.  
  
==================================================  
SKILL: benchmark-comparison-assistant  
==================================================  
  
# SKILL NAME  
benchmark-comparison-assistant  
  
## Purpose  
Compare outputs against historical or benchmark patterns.  
  
==================================================  
SKILL: artifact-readiness-checker  
==================================================  
  
# SKILL NAME  
artifact-readiness-checker  
  
## Purpose  
Check whether required artifacts exist and are fit for next stage.  
  
==================================================  
SKILL: issue-severity-advisor  
==================================================  
  
# SKILL NAME  
issue-severity-advisor  
  
## Purpose  
Suggest likely severity class for findings.  
  
====================================================================  
PART 2. RUNTIME RESOLUTION DESIGN  
====================================================================  
  
--------------------------------------------------------------------  
30. RUNTIME RESOLUTION PURPOSE  
--------------------------------------------------------------------  
The runtime resolver shall determine which skill stack is active at  
any moment.  
  
This shall allow CodeBuddy to behave like different virtual sub-agents  
depending on:  
- role  
- domain  
- stage  
- overlays  
- pending reviews  
- validation mode  
- interaction type  
  
--------------------------------------------------------------------  
31. REQUIRED RUNTIME INPUTS  
--------------------------------------------------------------------  
  
The resolver should read:  
  
- user_id  
- user_role  
- project_id  
- run_id  
- session_id  
- active_domain  
- active_stage  
- stage_class  
- workflow_mode  
- validation_mode  
- pending_review_type  
- policy_mode  
- selected_candidate_version_id  
- candidate_versions_present_flag  
- failure_state flag  
- remediation_mode flag  
- annual_review_mode flag  
  
--------------------------------------------------------------------  
32. REQUIRED RUNTIME OUTPUTS  
--------------------------------------------------------------------  
  
The resolver should produce:  
  
- ordered_skill_stack  
- active_tool_allowlist  
- ui_mode  
- review_mode  
- interaction_mode  
- required_artifacts  
- required_evidence_classes  
- mandatory_human_action flag  
- output_contract_type  
  
--------------------------------------------------------------------  
33. RUNTIME RESOLUTION JSON SCHEMA (LOGICAL)  
--------------------------------------------------------------------  
  
Suggested structure:  
  
{  
  "project_id": "proj_001",  
  "run_id": "run_001",  
  "session_id": "sess_001",  
  "active_role": "developer",  
  "active_domain": "scorecard",  
  "active_stage": "coarse_classing_review",  
  "stage_class": "review",  
  "workflow_mode": "development",  
  "validation_mode": false,  
  "policy_mode": "standard",  
  "pending_review_type": "coarse_classing",  
  "selected_candidate_version_id": null,  
  "candidate_versions_present": true,  
  "overlays": [  
    "strict-governance-overlay"  
  ],  
  "resolved_skills": [  
    "platform-base-rules",  
    "model-lifecycle-orchestrator",  
    "developer-agent",  
    "scorecard-domain",  
    "coarse-classing-review",  
    "strict-governance-overlay"  
  ],  
  "tool_allowlist": [  
    "workflowsdk",  
    "hitlsdk",  
    "scorecardsdk",  
    "evaluation_sdk",  
    "artifactsdk",  
    "observabilitysdk",  
    "auditsdk"  
  ],  
  "ui_mode": "three_panel_review_workspace",  
  "interaction_mode": "edit_and_finalize",  
  "required_human_action": true  
}  
  
--------------------------------------------------------------------  
34. RUNTIME RESOLUTION PSEUDOCODE  
--------------------------------------------------------------------  
  
def resolve_skill_stack(context):  
    skills = []  
  
    # Layer 0  
    skills.append("platform-base-rules")  
  
    # Layer 1  
    skills.append("model-lifecycle-orchestrator")  
  
    # Role  
    role_map = {  
        "developer": "developer-agent",  
        "validator": "validator-agent",  
        "governance": "governance-agent",  
        "reviewer": "reviewer-agent",  
        "approver": "approver-agent",  
        "documentation": "documentation-agent",  
        "monitoring": "monitoring-agent",  
        "remediation": "remediation-agent"  
    }  
    skills.append(role_map[context["active_role"]])  
  
    # Domain  
    domain_map = {  
        "scorecard": "scorecard-domain",  
        "timeseries": "timeseries-domain",  
        "ecl": "ecl-domain",  
        "lgd": "lgd-domain",  
        "pd": "pd-domain",  
        "ead": "ead-domain",  
        "sicr": "sicr-domain",  
        "stress": "stress-domain"  
    }  
    skills.append(domain_map[context["active_domain"]])  
  
    # Stage  
    stage_map = {  
        "coarse_classing_review": "coarse-classing-review",  
        "binning_version_selection": "binning-version-selection",  
        "feature_shortlist_review": "feature-shortlist-review",  
        "model_fitting_review": "model-fitting-review",  
        "model_selection": "model-selection",  
        "scaling_calibration_review": "scaling-and-calibration-review",  
        "validation_scope_definition": "validation-scope-definition",  
        "methodology_review": "methodology-review",  
        "model_fitness_review": "model-fitness-review",  
        "validation_conclusion": "validation-conclusion",  
        "deployment_readiness": "deployment-readiness",  
        "monitoring_breach_review": "monitoring-breach-review",  
        "annual_review_outcome": "annual-review-outcome",  
        "remediation_closure": "remediation-closure"  
    }  
    if context["active_stage"] in stage_map:  
        skills.append(stage_map[context["active_stage"]])  
  
    # Overlays  
    for overlay in context.get("overlays", []):  
        skills.append(overlay)  
  
    return skills  
  
  
def resolve_tool_allowlist(context):  
    tools = [  
        "workflowsdk",  
        "hitlsdk",  
        "observabilitysdk",  
        "auditsdk",  
        "artifactsdk"  
    ]  
  
    domain_tools = {  
        "scorecard": ["scorecardsdk", "evaluation_sdk", "feature_sdk"],  
        "timeseries": ["timeseriessdk", "evaluation_sdk", "feature_sdk"],  
        "ecl": ["eclsdk", "evaluation_sdk", "feature_sdk"],  
        "lgd": ["lgdsdk", "evaluation_sdk"],  
        "pd": ["pdsdk", "evaluation_sdk"],  
        "ead": ["eadsdk", "evaluation_sdk"],  
        "sicr": ["sicr_sdk", "evaluation_sdk"],  
        "stress": ["stresssdk", "evaluation_sdk"]  
    }  
  
    tools.extend(domain_tools.get(context["active_domain"], []))  
  
    if context.get("validation_mode", False):  
        tools.append("validationsdk")  
  
    return sorted(set(tools))  
  
  
def resolve_ui_mode(context):  
    if context["active_stage"] in [  
        "coarse_classing_review",  
        "binning_version_selection",  
        "model_fitness_review",  
        "validation_conclusion",  
        "deployment_readiness"  
    ]:  
        return "three_panel_review_workspace"  
  
    if context["active_stage"] in ["annual_review_outcome", "monitoring_breach_review"]:  
        return "dashboard_review_workspace"  
  
    return "standard_chat_plus_context"  
  
  
def build_effective_runtime_config(context):  
    return {  
        "resolved_skills": resolve_skill_stack(context),  
        "tool_allowlist": resolve_tool_allowlist(context),  
        "ui_mode": resolve_ui_mode(context),  
        "interaction_mode": determine_interaction_mode(context),  
        "required_human_action": determine_required_human_action(context)  
    }  
  
--------------------------------------------------------------------  
35. INTERACTION MODE RESOLUTION PSEUDOCODE  
--------------------------------------------------------------------  
  
def determine_interaction_mode(context):  
    if context["active_stage"] == "coarse_classing_review":  
        return "edit_and_finalize"  
  
    if context["active_stage"] == "binning_version_selection":  
        return "candidate_comparison_and_selection"  
  
    if context["active_stage"] == "validation_conclusion":  
        return "review_and_conclude"  
  
    if context["active_stage"] == "deployment_readiness":  
        return "approval_review"  
  
    if context["active_stage"] == "monitoring_breach_review":  
        return "triage_and_disposition"  
  
    return "chat_assisted_guidance"  
  
  
def determine_required_human_action(context):  
    mandatory_hitl_stages = {  
        "coarse_classing_review",  
        "binning_version_selection",  
        "validation_conclusion",  
        "deployment_readiness"  
    }  
  
    if context["active_stage"] in mandatory_hitl_stages:  
        return True  
  
    if context.get("pending_review_type"):  
        return True  
  
    return False  
  
--------------------------------------------------------------------  
36. STATE TRANSITION PSEUDOCODE FOR HITL  
--------------------------------------------------------------------  
  
def handle_human_interaction(payload):  
    # 1. Validate payload shape  
    validate_interaction_payload(payload)  
  
    # 2. Log interaction submitted  
    log_event("interaction_action_submitted", payload)  
  
    # 3. Route to deterministic validation / recomputation  
    result = recompute_and_validate(payload)  
  
    # 4. If preview action, return preview  
    if payload["action"] in ["preview_changes", "compare_candidates"]:  
        result["interaction_state"] = "preview_generated"  
        return result  
  
    # 5. If final action, enforce post-edit validation  
    if payload["action"] in [  
        "accept",  
        "accept_with_edits",  
        "approve_version",  
        "approve_version_with_overrides",  
        "create_composite_version",  
        "finalize_validation_conclusion"  
    ]:  
        if result["status"] == "invalid_needs_review":  
            return result  
  
        persist_final_decision(payload, result)  
        update_workflow_state(payload, result)  
        log_event("interaction_finalized", payload)  
        return result  
  
    # 6. Handle rerun / escalate  
    if payload["action"] == "reject_and_rerun":  
        create_rerun(payload)  
        return {"status": "rerun_created"}  
  
    if payload["action"] == "escalate":  
        create_escalation_review(payload)  
        return {"status": "escalated"}  
  
--------------------------------------------------------------------  
37. JSON SCHEMA EXAMPLES  
--------------------------------------------------------------------  
  
37.1 Runtime Context  
--------------------------------------------------------------------  
{  
  "project_id": "scorecard_proj_01",  
  "run_id": "run_001",  
  "session_id": "sess_001",  
  "active_role": "developer",  
  "active_domain": "scorecard",  
  "active_stage": "coarse_classing_review",  
  "stage_class": "review",  
  "workflow_mode": "development",  
  "validation_mode": false,  
  "policy_mode": "standard",  
  "pending_review_type": "coarse_classing",  
  "selected_candidate_version_id": null,  
  "candidate_versions_present": true,  
  "overlays": []  
}  
  
37.2 Resolved Runtime Config  
--------------------------------------------------------------------  
{  
  "resolved_skills": [  
    "platform-base-rules",  
    "model-lifecycle-orchestrator",  
    "developer-agent",  
    "scorecard-domain",  
    "coarse-classing-review"  
  ],  
  "tool_allowlist": [  
    "workflowsdk",  
    "hitlsdk",  
    "scorecardsdk",  
    "evaluation_sdk",  
    "feature_sdk",  
    "artifactsdk",  
    "observabilitysdk",  
    "auditsdk"  
  ],  
  "ui_mode": "three_panel_review_workspace",  
  "interaction_mode": "edit_and_finalize",  
  "required_human_action": true  
}  
  
37.3 Interaction Payload  
--------------------------------------------------------------------  
{  
  "project_id": "scorecard_proj_01",  
  "run_id": "run_001",  
  "session_id": "sess_001",  
  "review_id": "rev_cc_001",  
  "stage_name": "coarse_classing_review",  
  "interaction_type": "edit_and_finalize",  
  "action": "accept_with_edits",  
  "actor_id": "user_123",  
  "actor_role": "developer",  
  "structured_edits": {  
    "groups": [  
      {"label": "Bin 1", "source_bins": [1]},  
      {"label": "Bin 2", "source_bins": [2, 3]},  
      {"label": "Bin 3", "source_bins": [4]},  
      {"label": "Missing", "source_bins": ["MISSING"]}  
    ]  
  },  
  "user_comment": "Merged middle bins to improve support."  
}  
  
37.4 Response Envelope  
--------------------------------------------------------------------  
{  
  "status": "valid_with_warning",  
  "message": "Edited bins are acceptable, but one group remains near the minimum support threshold.",  
  "current_stage": "coarse_classing_review",  
  "next_stage": "woe_iv_review",  
  "required_human_action": true,  
  "warnings": [  
    "One group support is near threshold."  
  ],  
  "errors": [],  
  "artifacts_created": [  
    "artifact://coarse_bins_v3"  
  ],  
  "candidate_versions_created": [],  
  "selected_candidate_version_id": null,  
  "review_created": null,  
  "audit_ref": "audit://run_001/rev_cc_001",  
  "event_ref": "event://evt_101"  
}  
  
====================================================================  
PART 3. HITL DESIGN RECOMMENDATIONS  
====================================================================  
  
--------------------------------------------------------------------  
38. SHOULD EVERY SKILL OR TASK RETURN STATUS?  
--------------------------------------------------------------------  
  
Short answer:  
Yes, every material skill / task should return a status.  
  
Reason:  
Without a standardized status, the orchestrator cannot reliably:  
- route to the next stage  
- know whether to pause  
- know whether human input is needed  
- know whether to retry  
- know whether to block  
- know whether to finalize  
  
So every skill should return a normalized status envelope.  
  
--------------------------------------------------------------------  
39. RECOMMENDED STANDARD STATUS ENUM  
--------------------------------------------------------------------  
  
Every material skill should return one of these statuses:  
  
- success  
- success_with_warning  
- blocked  
- failed  
- pending_human_review  
- preview_ready  
- rerun_requested  
- escalated  
- paused  
- resumed  
- finalized  
- invalid_input  
- invalid_needs_review  
  
Suggested rule:  
- deterministic stage completion -> success / success_with_warning  
- HITL creation -> pending_human_review  
- preview interaction -> preview_ready  
- validation failure -> invalid_needs_review  
- hard failure -> failed  
- unmet prerequisite -> blocked  
  
--------------------------------------------------------------------  
40. STANDARD RESPONSE ENVELOPE  
--------------------------------------------------------------------  
  
Every skill / task should return:  
  
- status  
- message  
- current_stage  
- next_stage  
- required_human_action  
- warnings  
- errors  
- artifacts_created  
- candidate_versions_created  
- selected_candidate_version_id  
- review_created  
- audit_ref  
- event_ref  
  
Optional:  
- updated_metrics  
- updated_test_results  
- validation_finding_ids  
- validation_conclusion_id  
- workflow_state_patch  
  
This standardization is one of the most important design choices.  
  
--------------------------------------------------------------------  
41. HOW SHOULD HUMAN INPUT BE PART OF THE PROCESS?  
--------------------------------------------------------------------  
  
Human input should not be treated as random chat only.  
  
Best practice:  
human input should enter through a structured interaction contract.  
  
Use:  
- structured selection  
- structured edits  
- bounded action choice  
- optional rationale text  
  
Examples:  
- choose candidate version  
- edit bin groups  
- choose validation severity  
- select final conclusion  
- approve with conditions  
- reject and rerun  
  
Narrative input should support the structured input, not replace it.  
  
--------------------------------------------------------------------  
42. WHERE HUMAN INPUT FITS IN THE FLOW  
--------------------------------------------------------------------  
  
Standard flow:  
  
1. agent proposes or summarizes result  
2. workflow creates review / interaction state  
3. UI workspace opens  
4. human provides structured input  
5. controller converts input to payload  
6. agent / SDK validates and recomputes if needed  
7. system returns preview or final validation result  
8. human confirms final action  
9. workflow updates state and continues  
  
So human input is a first-class event in the process, not an  
afterthought.  
  
--------------------------------------------------------------------  
43. WILL HITL TIME OUT?  
--------------------------------------------------------------------  
  
Best practice:  
Yes, HITL should support timeout concept, but timeout should not mean  
auto-approval.  
  
Recommended timeout behavior:  
- the review may become stale or overdue  
- reminders may be triggered  
- escalation may be triggered  
- workflow remains paused or blocked  
- review can be resumed later  
  
What should NOT happen:  
- automatic final approval because timeout expired  
- automatic final rejection without rule-based policy  
- silent discard of pending review  
  
--------------------------------------------------------------------  
44. RECOMMENDED HITL TIMEOUT STATES  
--------------------------------------------------------------------  
  
A review / interaction should support:  
  
- pending_review  
- in_progress  
- awaiting_preview_confirmation  
- overdue  
- escalated_due_to_timeout  
- expired_needs_recreation  
- closed  
  
Suggested rules:  
- if timeout threshold reached -> mark overdue  
- if policy says escalate -> escalate_due_to_timeout  
- if context becomes stale or superseded -> expired_needs_recreation  
  
--------------------------------------------------------------------  
45. SHOULD THE LLM SESSION ITSELF TIME OUT?  
--------------------------------------------------------------------  
  
The LLM call can time out technically, but the HITL process should not  
depend on the chat session remaining open.  
  
Best design:  
- persist review state outside the LLM  
- persist interaction payloads outside the chat  
- allow the human to come back later  
- allow the resolver to rebuild context and resume  
  
So:  
- chat timeout is fine  
- workflow review timeout is governed separately  
- review state should survive chat/session restart  
  
--------------------------------------------------------------------  
46. RECOMMENDED HITL DESIGN PATTERN  
--------------------------------------------------------------------  
  
Best pattern:  
interactive structured editor + preview + final confirmation  
  
For governed workflows, use:  
- Panel A = proposal and evidence  
- Panel B = structured editing workspace  
- Panel C = actions and status  
- optional chat sidecar = explanation / alternative generation  
  
This is much better than:  
- plain yes/no popup  
- plain chat-only editing  
- free-text-only approval  
  
--------------------------------------------------------------------  
47. WHAT HAPPENS AFTER HUMAN INPUT?  
--------------------------------------------------------------------  
  
After human input:  
- validate payload  
- log interaction event  
- recompute affected metrics if needed  
- rerun policy checks if needed  
- rerun validation checks if needed  
- refresh artifacts / previews if needed  
- return standard response envelope  
- if final action valid -> finalize and continue  
- if not valid -> remain in review or escalate  
  
--------------------------------------------------------------------  
48. HUMAN INPUT CONTRACT EXAMPLE  
--------------------------------------------------------------------  
  
{  
  "project_id": "proj_001",  
  "run_id": "run_001",  
  "session_id": "sess_001",  
  "review_id": "rev_001",  
  "stage_name": "coarse_classing_review",  
  "interaction_type": "edit_and_finalize",  
  "action": "accept_with_edits",  
  "actor_id": "user_123",  
  "actor_role": "developer",  
  "structured_edits": {  
    "groups": [  
      {"label": "Bin 1", "source_bins": [1]},  
      {"label": "Bin 2", "source_bins": [2, 3]},  
      {"label": "Bin 3", "source_bins": [4]}  
    ]  
  },  
  "user_comment": "Merged bins 2 and 3 for better support.",  
  "timestamp": "2026-03-15T10:30:00+08:00"  
}  
  
--------------------------------------------------------------------  
49. SHOULD ALL TASKS BE SYNCHRONOUS?  
--------------------------------------------------------------------  
  
No.  
  
Recommended split:  
  
Synchronous:  
- preview recompute  
- small validations  
- structured response generation  
- review creation  
  
Asynchronous / pause-resume:  
- waiting for human review  
- waiting for approver  
- waiting for validation evidence  
- waiting for remediation closure  
  
This means the workflow engine must support:  
- pause  
- persist  
- resume  
- overdue handling  
- escalation on timeout  
  
--------------------------------------------------------------------  
50. FINAL HITL RECOMMENDATION  
--------------------------------------------------------------------  
  
Best answer for your environment:  
  
1. Every material skill / task should return a standardized status.  
2. Human input should be structured and part of workflow state.  
3. HITL should pause workflow cleanly and resume later.  
4. Timeout should create overdue / escalation behavior, not silent  
   approval.  
5. Chat should support explanation and alternative generation.  
6. Structured workspace should support final editing and finalization.  
7. Workflow state, not chat history, should be the source of truth.  
  
====================================================================  
END OF ROLE-BY-ROLE SKILL PACK  
+ RUNTIME RESOLUTION DESIGN  
+ HITL DESIGN RECOMMENDATION  
====================================================================  
