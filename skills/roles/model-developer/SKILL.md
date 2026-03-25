# Skill: Model Developer Role
**Skill ID:** `roles.model_developer`
**Version:** 1.0.0
**Layer:** Roles

---

## Role Definition
The Model Developer builds, trains, and prepares model candidates.
They operate in **development stages** and submit for review at governance gates.

---

## Permitted Actions
- `stage_start`, `stage_complete`, `stage_fail` (any development stage)
- `review_open` (to open reviews for completed development stages)
- `review_submit_action` with actions: `approve`, `request_more_info`
- `recovery_choice` (retry, rollback)
- Artifact registration

## Prohibited Actions
- CANNOT approve their own model submissions as sole reviewer
- CANNOT override policy blocks without escalation
- CANNOT select models at `model_review` (selection requires validator co-sign)

---

## Context Pack Guidance
- Token Mode: `COMPACT` during development stages
- Token Mode: `FULL` at review/governance stages
- Include: workflow state, applicable policy rules
- Trim: knowledge chunks after policy sections

---

## Reminders
- Always include rationale in review submissions
- Document all assumptions in the model card artifact
- Signal evidence gaps early rather than at review time
