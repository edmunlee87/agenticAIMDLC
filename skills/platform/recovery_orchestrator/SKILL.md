# Skill: Recovery Orchestrator
**Skill ID:** `platform.recovery_orchestrator`
**Version:** 1.0.0
**Layer:** Platform

---

## Purpose
When a stage fails, present recovery options to the human-in-the-loop and
execute the chosen recovery path while maintaining full audit traceability.

---

## Context Requirements
- `run_id`, `project_id`, `actor_id`
- Failed stage name and error details
- Available recovery paths from `RecoveryService`

---

## Behaviour Instructions

### On Stage Failure
1. Call `mdlc_recovery_options` to retrieve available recovery paths.
2. Present recovery options using `build_recovery_workspace()` from `widgetsdk`.
3. Include error summary, failure context, and available paths.
4. Wait for human selection.

### On Recovery Choice
1. Call `mdlc_recovery_choice` with selected path.
2. Emit `workflow.stage.recovered` event.
3. Return control to `WorkflowOrchestratorSkill` with the recovery result.

### Recovery Paths (standard)
| Path | Condition |
|------|-----------|
| `retry` | Transient failure; max 3 retries with backoff |
| `rollback_to_prev_stage` | Deterministic failure needing re-work |
| `override_and_continue` | Requires HITL approval + rationale |
| `escalate` | Blocks for senior review |

---

## Governance Constraints
- `override_and_continue` requires explicit rationale and role validation.
- All recovery choices are audit-logged.
- Recovery from a governance gate requires senior_management role.
