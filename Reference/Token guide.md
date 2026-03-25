# Token guide  
  
====================================================================  
TOKEN THRIFT GUIDE / REFERENCE  
FOR ENTERPRISE AGENTIC AI MODEL LIFECYCLE PLATFORM  
====================================================================  
  
PURPOSE  
--------------------------------------------------------------------  
This guide defines practical rules, patterns, and controls to keep  
token usage justified, reasonable, and efficient across the platform.  
  
This guide applies to:  
- CodeBuddy chat interactions  
- skill stack prompting  
- workflow orchestration  
- RAG / knowledge retrieval  
- HITL review generation  
- validation support  
- documentation drafting  
- monitoring and annual review  
- session resume and recovery  
  
PRINCIPLE  
--------------------------------------------------------------------  
Use tokens only where they materially improve:  
- correctness  
- governance  
- explainability  
- workflow continuity  
- decision quality  
  
Do not spend tokens on:  
- repeated context  
- repeated instructions  
- raw artifact dumps  
- unnecessary prose  
- duplicate summaries  
- low-value chat filler  
- full-history replay when compact state is enough  
  
====================================================================  
1. TOKEN GOVERNANCE PRINCIPLES  
====================================================================  
  
1.1 Token Use Must Be Justified  
--------------------------------------------------------------------  
Every major token-consuming action should have a reason:  
- needed to decide  
- needed to explain  
- needed to validate  
- needed to preserve continuity  
- needed to draft a governed output  
  
1.2 Prefer Structured Context Over Long Narrative  
--------------------------------------------------------------------  
Prefer:  
- IDs  
- short summaries  
- key metrics  
- compact warnings  
- selected facts  
- state fields  
  
Instead of:  
- long prose  
- repeated explanations  
- whole document copies  
  
1.3 Use Smallest Sufficient Context  
--------------------------------------------------------------------  
Always send the minimum context needed for the current task.  
  
1.4 Separate Exact Facts From Semantic Context  
--------------------------------------------------------------------  
Do not waste tokens using prose to restate structured facts that can  
be passed as compact fields.  
  
1.5 Avoid Prompt Bloat From Layering  
--------------------------------------------------------------------  
Skill stacking should be modular, but runtime prompt assembly must be  
compressed so repeated rules are not re-sent unnecessarily.  
  
====================================================================  
2. TOKEN USAGE TIERS  
====================================================================  
  
2.1 Tier A – Mandatory Token Spend  
--------------------------------------------------------------------  
Use tokens freely enough for:  
- final governed review summaries  
- validation conclusion support  
- model selection explanation  
- policy breach explanation  
- remediation recommendation with evidence  
- committee / audit ready wording  
  
2.2 Tier B – Controlled Token Spend  
--------------------------------------------------------------------  
Use compactly for:  
- candidate comparison  
- stage summaries  
- resume summaries  
- artifact summaries  
- monitoring breach triage  
- documentation drafting support  
  
2.3 Tier C – Minimal Token Spend  
--------------------------------------------------------------------  
Keep extremely small for:  
- workflow routing  
- state transitions  
- status refresh  
- repeated UI interactions  
- preview refreshes  
- event-driven updates  
- tool coordination  
  
====================================================================  
3. RUNTIME TOKEN BUDGETING  
====================================================================  
  
3.1 Suggested Query Modes  
--------------------------------------------------------------------  
Define standard context modes:  
  
A. micro_mode  
Use for:  
- routing  
- small clarifications  
- status updates  
- action confirmation  
Budget:  
- very small context only  
- exact facts only  
- no large retrieved text  
  
B. standard_mode  
Use for:  
- normal stage reasoning  
- review drafting  
- candidate comparison  
Budget:  
- compact facts  
- top summaries  
- selected warnings  
- one or two detailed snippets only if needed  
  
C. deep_review_mode  
Use for:  
- validation conclusion  
- governance review  
- committee note drafting  
- complex trade-off analysis  
Budget:  
- compact facts  
- top summaries  
- selected detailed evidence  
- still no raw dumping  
  
3.2 Budget Allocation Rule  
--------------------------------------------------------------------  
Suggested token budget split per request:  
  
- 20% system / skill / instruction  
- 20% structured runtime context  
- 25% retrieved knowledge  
- 20% active artifact / metrics summaries  
- 15% response generation headroom  
  
This is only a guide, but it keeps retrieval from overwhelming output.  
  
====================================================================  
4. SKILL STACK TOKEN OPTIMIZATION  
====================================================================  
  
4.1 Do Not Concatenate Raw Full Skills Blindly  
--------------------------------------------------------------------  
Do not inject every full skill file in every request.  
  
Instead:  
- use compact resolved skill summaries  
- keep invariant rules in a base system layer  
- inject only active role/domain/stage instructions  
- omit inactive skills  
  
4.2 Create Runtime-Compressed Skill Views  
--------------------------------------------------------------------  
For each skill, maintain:  
  
- full skill spec  
- runtime compact skill summary  
  
Use the compact version in normal calls.  
  
Example compact role summary:  
- role: validator  
- priorities: independent challenge, evidence sufficiency, model fitness  
- must_not: final sign-off without human validator, silent waiver  
  
4.3 Reuse Stable Base Rules  
--------------------------------------------------------------------  
Stable platform rules should sit in the most persistent instruction  
layer possible and should not be repeatedly expanded.  
  
4.4 Stage Skill Must Be Specific  
--------------------------------------------------------------------  
Stage skill content should be narrow:  
- current task  
- current outputs  
- current decision rules  
- current HITL rules  
  
Do not inject unrelated domain or project detail into the stage skill.  
  
====================================================================  
5. WORKFLOW ORCHESTRATION TOKEN OPTIMIZATION  
====================================================================  
  
5.1 Route With State, Not Narrative  
--------------------------------------------------------------------  
The orchestrator should read compact state fields such as:  
- current_stage  
- pending_review  
- blocked_reason  
- selected_candidate_version_id  
- required_human_action  
  
Do not ask the LLM to rediscover workflow state from prior chat.  
  
5.2 Use State Deltas  
--------------------------------------------------------------------  
On each step, pass only what changed when possible.  
  
Example:  
- new candidate created  
- selected version changed  
- review status changed  
- finding severity changed  
  
Not:  
- full workflow recap every turn  
  
5.3 Store Workflow Memory Outside the Prompt  
--------------------------------------------------------------------  
All durable workflow memory should live in:  
- workflow_state  
- review registry  
- artifact registry  
- decision registry  
- finding registry  
  
Only a compact subset should be injected into the prompt.  
  
====================================================================  
6. RAG TOKEN OPTIMIZATION  
====================================================================  
  
6.1 Retrieve Less, Better  
--------------------------------------------------------------------  
Use:  
- role filter  
- domain filter  
- project filter  
- stage filter  
- quality filter  
- superseded filter  
- recency filter  
  
Do not retrieve broad mixed-scope results.  
  
6.2 Short Summary First  
--------------------------------------------------------------------  
Retrieval order should be:  
1. exact structured facts  
2. short summaries  
3. detailed summaries only if needed  
4. raw chunks only as last resort  
  
6.3 Top-K Discipline  
--------------------------------------------------------------------  
Use very small top-k by default.  
  
Suggested default:  
- top 3 short summaries  
- at most 1 to 2 detailed summaries  
- 0 raw full chunks unless explicitly needed  
  
6.4 No Redundant Related Chunks  
--------------------------------------------------------------------  
Do not send five chunks saying the same thing in different wording.  
  
6.5 Prefer Curated Knowledge Objects Over Raw Documents  
--------------------------------------------------------------------  
A reviewed decision summary is usually much more token-efficient than  
re-sending the full source artifact.  
  
6.6 Use Query Intent Routing  
--------------------------------------------------------------------  
Different query types need different retrieval packages.  
  
Examples:  
  
Routing question:  
- only workflow state  
- no semantic retrieval  
  
Candidate comparison:  
- exact candidate metrics  
- top 2 comparison summaries  
- no full methodology notes unless needed  
  
Validation conclusion:  
- exact findings  
- evidence completeness summary  
- top 2 prior reusable validation patterns  
- no extra project chatter  
  
Documentation drafting:  
- template  
- approved wording block  
- current project summary  
- final decision/finding summaries  
  
====================================================================  
7. HITL TOKEN OPTIMIZATION  
====================================================================  
  
7.1 Let UI Carry Heavy Display Load  
--------------------------------------------------------------------  
Use the UI to display:  
- charts  
- tables  
- candidate comparison  
- metrics grids  
- evidence links  
  
Do not force the LLM to re-narrate what the UI already shows.  
  
7.2 Send Structured User Input Back  
--------------------------------------------------------------------  
When the user edits something, send:  
- selected action  
- structured edits  
- short rationale  
  
Do not send the whole visible screen back to the LLM.  
  
7.3 Preview Recompute Should Be Small  
--------------------------------------------------------------------  
Preview calls should usually include:  
- edited fields  
- compact before/after metrics  
- warning summary  
  
Not:  
- full review payload again  
  
7.4 Separate Exploration From Finalization  
--------------------------------------------------------------------  
Use small tokens for:  
- "preview this change"  
- "compare candidate A vs B"  
  
Use larger tokens only for:  
- final explanation  
- final acceptance note  
- escalation note  
- validation conclusion  
  
====================================================================  
8. VALIDATION TOKEN OPTIMIZATION  
====================================================================  
  
8.1 Validation Should Pull Findings, Not Full Project History  
--------------------------------------------------------------------  
For validation tasks, retrieve:  
- active findings  
- evidence completeness  
- required validation dimensions  
- selected supporting summaries  
  
Not:  
- full development history  
- every candidate ever created  
- full chat history  
  
8.2 Use Structured Model Fitness Matrix  
--------------------------------------------------------------------  
Pass model fitness as compact dimensions:  
  
- conceptual_soundness: pass/warn/fail + one line  
- data_suitability: pass/warn/fail + one line  
- calibration_quality: pass/warn/fail + one line  
- implementation_readiness: pass/warn/fail + one line  
  
This is far more token-thrifty than full narrative.  
  
8.3 Reuse Approved Validation Phrases  
--------------------------------------------------------------------  
Store reusable approved wording for:  
- fit_for_use  
- fit_for_use_with_conditions  
- rework_required  
- evidence_incomplete  
  
This avoids redrafting from scratch each time.  
  
====================================================================  
9. DOCUMENTATION TOKEN OPTIMIZATION  
====================================================================  
  
9.1 Draft From Structured Inputs  
--------------------------------------------------------------------  
Documentation generation should use:  
- template ID  
- section outline  
- compact project summary  
- selected findings/decisions  
- approved wording blocks  
  
Not:  
- raw full retrieved context dump  
  
9.2 Generate Section by Section  
--------------------------------------------------------------------  
Draft large documents sectionally, not in one huge generation.  
  
9.3 Use Snippet Libraries  
--------------------------------------------------------------------  
Maintain libraries for:  
- validation wording  
- governance wording  
- limitation wording  
- methodology explanation  
- monitoring summary wording  
  
9.4 Cache Reusable Draft Blocks  
--------------------------------------------------------------------  
If a summary has already been approved and stored, reuse it.  
  
====================================================================  
10. CHAT / CODEBUDDY TOKEN OPTIMIZATION  
====================================================================  
  
10.1 Use Chat for Clarification, Not Memory Storage  
--------------------------------------------------------------------  
Do not rely on long chat history as memory.  
Use:  
- workflow state  
- knowledge objects  
- registry lookups  
- compact context injections  
  
10.2 Summarize Long Conversations  
--------------------------------------------------------------------  
If a discussion becomes long, create:  
- interaction summary  
- decision summary  
- open questions summary  
  
Then continue from the summary, not the full transcript.  
  
10.3 Distinguish Chat Modes  
--------------------------------------------------------------------  
Chat modes should include:  
- quick answer mode  
- governed review mode  
- drafting mode  
- deep validation mode  
  
Each mode should have different token budgets.  
  
====================================================================  
11. KNOWLEDGE BASE TOKEN OPTIMIZATION  
====================================================================  
  
11.1 Store Multiple Summary Levels  
--------------------------------------------------------------------  
Every important knowledge object should have:  
- short_summary  
- detailed_summary  
- source_ref  
  
11.2 Promote Summaries, Not Raw Noise  
--------------------------------------------------------------------  
Do not promote raw chat content to reusable memory.  
Promote:  
- reviewed lessons  
- approved wording  
- final decisions  
- reusable findings patterns  
  
11.3 Keep Session Memory Short  
--------------------------------------------------------------------  
Session memory should be brief and highly current.  
Old session context should be summarized or dropped.  
  
11.4 Use Superseded Filtering  
--------------------------------------------------------------------  
Never retrieve superseded knowledge by default.  
  
====================================================================  
12. ARTIFACT TOKEN OPTIMIZATION  
====================================================================  
  
12.1 Create Artifact Summaries  
--------------------------------------------------------------------  
For every large artifact, maintain:  
- one-line summary  
- short summary  
- key metrics  
- key warnings  
- linked full artifact reference  
  
12.2 Use Artifact Manifests  
--------------------------------------------------------------------  
Pass manifests like:  
- artifact type  
- version  
- key sections available  
- summary  
instead of loading the full artifact into context.  
  
12.3 Selective Section Retrieval  
--------------------------------------------------------------------  
If detailed review is needed, retrieve only the relevant section.  
  
====================================================================  
13. RESPONSE STYLE OPTIMIZATION  
====================================================================  
  
13.1 Default to Compact Professional Style  
--------------------------------------------------------------------  
Responses should be:  
- direct  
- structured  
- evidence-led  
- not verbose unless required  
  
13.2 Prefer Lists of Facts Over Long Paragraphs  
--------------------------------------------------------------------  
For internal reasoning prompts and compact summaries, fact blocks are  
often cheaper than prose.  
  
13.3 Avoid Repeating Context  
--------------------------------------------------------------------  
Do not restate:  
- project identity  
- role  
- stage  
- already displayed metrics  
unless needed for the conclusion.  
  
====================================================================  
14. TOKEN-SPEND DECISION RULES  
====================================================================  
  
14.1 When Higher Token Spend Is Justified  
--------------------------------------------------------------------  
Spend more tokens when:  
- final decision is being drafted  
- governance sign-off is near  
- validation conclusion is being formed  
- complex trade-off must be explained  
- ambiguity is materially risky  
- documentation output is a final deliverable  
  
14.2 When Higher Token Spend Is Not Justified  
--------------------------------------------------------------------  
Do not spend more tokens for:  
- simple routing  
- status checks  
- repetitive previews  
- UI refreshes  
- unchanged context  
- artifact existence checks  
- restating structured fields  
  
====================================================================  
15. ANTI-PATTERNS TO AVOID  
====================================================================  
  
Do not do the following:  
  
- inject full project history every turn  
- inject full skill files every turn  
- retrieve many large chunks "just in case"  
- ask the LLM to infer workflow state from chat alone  
- include full artifacts when summaries are enough  
- re-explain charts already displayed in UI  
- regenerate approved wording repeatedly  
- keep long session memory unsummarized  
- promote noisy or low-quality knowledge into reusable KB  
- use chat transcript as the primary database  
  
====================================================================  
16. RECOMMENDED COMPACT CONTEXT PACKS  
====================================================================  
  
16.1 Routing Pack  
--------------------------------------------------------------------  
Contents:  
- project_id  
- run_id  
- current_stage  
- pending_review  
- blocked_reason  
- selected_candidate_version_id  
  
Use for:  
- next-step determination  
- orchestration  
  
16.2 Review Pack  
--------------------------------------------------------------------  
Contents:  
- review_id  
- stage_name  
- recommendation summary  
- top metrics  
- warnings  
- selected artifacts refs  
- allowed actions  
  
Use for:  
- HITL reviews  
- preview updates  
  
16.3 Validation Pack  
--------------------------------------------------------------------  
Contents:  
- validation_run_id  
- active findings summary  
- evidence completeness summary  
- top fitness dimension summary  
- allowed conclusion categories  
  
Use for:  
- validation review  
- conclusion drafting  
  
16.4 Drafting Pack  
--------------------------------------------------------------------  
Contents:  
- template ID  
- section outline  
- approved wording snippets  
- compact project summary  
- key decisions/findings/conclusions  
  
Use for:  
- report drafting  
- committee notes  
  
====================================================================  
17. SUGGESTED METRICS FOR TOKEN GOVERNANCE  
====================================================================  
  
Track at least:  
  
- average prompt tokens by use case  
- average completion tokens by use case  
- retrieval chunks per query  
- summary-to-raw ratio  
- % of calls using micro / standard / deep mode  
- token cost per finalized review  
- token cost per validation conclusion  
- repeated context ratio  
- cache hit ratio for reusable summaries  
- % of superseded knowledge retrieved  
- % of retrievals resolved from project scope only  
  
====================================================================  
18. PRACTICAL RULES BY COMPONENT  
====================================================================  
  
18.1 Orchestrator  
--------------------------------------------------------------------  
- use state, not history  
- only inject current stage context  
- no large retrieval unless reasoning actually needs it  
  
18.2 HITL  
--------------------------------------------------------------------  
- structured payload in  
- compact status out  
- UI displays detail, LLM handles judgment support  
  
18.3 Validation  
--------------------------------------------------------------------  
- retrieve active findings and required evidence only  
- use dimension matrix  
- avoid whole project replay  
  
18.4 Documentation  
--------------------------------------------------------------------  
- use snippet libraries  
- draft by section  
- do not redraft unchanged sections  
  
18.5 Knowledge Base  
--------------------------------------------------------------------  
- store short summaries  
- promote selectively  
- filter aggressively before retrieval  
  
====================================================================  
19. TOKEN THRIFT CHECKLIST  
====================================================================  
  
Before sending context to the LLM, ask:  
  
1. Is this context needed for the current stage?  
2. Can exact facts replace narrative?  
3. Is there a short summary already available?  
4. Is any retrieved knowledge superseded or stale?  
5. Are there duplicate chunks saying the same thing?  
6. Can UI carry this information instead of prompt text?  
7. Is this a micro, standard, or deep review call?  
8. Is the expected response worth the token spend?  
9. Can we reuse prior approved wording?  
10. Can we reuse a cached context pack?  
  
====================================================================  
20. RECOMMENDED IMPLEMENTATION CONTROLS  
====================================================================  
  
Implement:  
- token_budget_manager in rag_sdk  
- context_compressor in rag_sdk  
- summary cache in knowledge_sdk  
- mode-based prompt packaging  
- retrieval filters by default  
- context pack builders  
- usage telemetry dashboard  
- high-token call review thresholds  
  
====================================================================  
21. SUCCESS CRITERIA  
====================================================================  
  
This guide is considered successfully implemented when:  
  
1. the platform uses compact context by default  
2. retrieval is scoped and low-noise  
3. token use rises only when decision complexity justifies it  
4. repeated context is minimized  
5. workflow routing stays lightweight  
6. validation and governance still receive enough evidence  
7. documentation drafting avoids unnecessary rework  
8. knowledge retrieval remains traceable and efficient  
9. token usage can be measured and governed  
10. overall usage is thrifty, justified, and reasonable  
  
====================================================================  
END OF TOKEN THRIFT GUIDE  
====================================================================  
