# Skill: Workflow Orchestrator
**Skill ID:** `platform.workflow_orchestrator`
**Version:** 1.0.0
**Layer:** Platform
**Applies To:** All MDLC runs

---

## Purpose
Drive the end-to-end MDLC workflow lifecycle for a single run.
Open the session, iterate through stages, handle failures, and pause at governance gates for HITL review.

---

## Context Requirements
Before invoking this skill, the context pack MUST include:
- **Workflow State**: current stage, run_id, project_id, actor_id
- **Domain Pack**: active domain (e.g. `scorecard`) and its stage registry
- **Runtime Decision**: resolved tool allowlist, UI mode, governance constraints

Inject via `ContextBuilder.add_workflow_state()` and `ContextBuilder.add_policy_summary()`.

---

## Behaviour Instructions

### On Session Open
1. Call `mdlc_open_session` with run_id, project_id, actor_id, domain.
2. Log session envelope to audit trail.
3. Identify the first stage from the domain pack's `stage_registry`.

### On Each Stage
1. Call `mdlc_stage_start` for the current stage.
2. Invoke the domain SDK's `run_stage(stage_id, inputs)` computation.
3. If `result.success == False`: call `mdlc_stage_fail` and invoke `RecoveryOrchestratorSkill`.
4. If `result.success == True`:
   - Register all artifacts from `result.artifacts`.
   - If stage is a governance gate: invoke `ReviewOrchestratorSkill`. Pause and wait.
   - Otherwise: call `mdlc_stage_complete` and `mdlc_route_next`.

### On Recovery
Delegate entirely to `RecoveryOrchestratorSkill`. Do not proceed until recovery is confirmed.

### On Run Completion
Emit a `workflow.run.completed` event. Update run status.

---

## Governance Constraints
- NEVER skip a governance gate stage without explicit HITL approval.
- NEVER auto-approve reviews.
- ALL stage transitions must emit observability events.
- Audit trail entry required for every state change.

---

## Token Guidance
- Use `TokenMode.COMPACT` for stage compute steps.
- Use `TokenMode.FULL` for governance gate / review stages.
- Trim knowledge context first; policy and state sections are mandatory.

---

## Error Handling
| Error | Response |
|-------|----------|
| Stage compute failure | Invoke RecoveryOrchestratorSkill immediately |
| HITL timeout | Escalate via `hitl.review.escalated` event |
| Missing artifacts | Raise `ERR_MISSING_ARTIFACT` and block stage completion |
| Policy breach | Block stage, surface blocking_reasons to reviewer |
