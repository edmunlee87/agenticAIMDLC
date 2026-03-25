# Skill: Model Review Stage
**Skill ID:** `stages.model_review`
**Version:** 1.0.0
**Layer:** Stages
**Applies To:** All domains with a `model_review` stage

---

## Purpose
Guide the model reviewer through the evidence-based selection of the best candidate model.
Enforce policy thresholds before accepting a selection decision.

---

## Pre-Review Checks
Before the review workspace opens, verify:
1. `model_candidate_set` artifact exists and has at least 1 candidate.
2. `evaluation_pack` artifact exists with metrics for all candidates.
3. Primary metric is defined in domain `metrics_pack`.
4. All required roles are available.

If any check fails → surface `ERR_MISSING_EVIDENCE` and block review opening.

---

## Review Workflow

### Panel A: Evidence
Show:
- Candidate comparison table (all metrics, all splits)
- Recommended candidate (highlighted)
- Domain primary metric threshold
- Policy rule list for this stage

### Panel B: Selection Form
Required fields:
- `selected_candidate_id` (candidate selected by reviewer)
- `rationale` (substantive, not boilerplate)
- `policy_acknowledged` (True)
- `conditions` (optional: conditions to monitor post-deployment)

### Panel C: Actions
- `select` → validate policy → complete review
- `reject_all` → requires rationale → triggers recovery
- `request_more_info` → pauses review, returns to development stage

---

## Policy Enforcement
After selection, run all policy rules with `applies_to_stages: [model_review]`:
- If any CRITICAL rule fails: BLOCK selection, surface blocking_reasons.
- If any HIGH rule fails with `requires_waiver: true`: require escalation.
- If all pass: complete review and route forward.

---

## Audit Requirements
The audit trail entry for this stage must include:
- `selected_candidate_id`
- `rationale`
- `policy_check_result`
- `actor_id` + `actor_role`
- `timestamp`
- `blocking_reasons` (empty list if none)
