# Skill: Review Orchestrator
**Skill ID:** `platform.review_orchestrator`
**Version:** 1.0.0
**Layer:** Platform

---

## Purpose
Manage the full HITL review lifecycle: open a review, present evidence to the reviewer,
collect a structured decision, validate it against policy, and transition the workflow accordingly.

---

## Context Requirements
- `review_id`, `stage_name`, `run_id`, `project_id`, `actor_id`
- Domain review template (from `DomainPackManifest.get_review_template(stage_id)`)
- Applicable policy rules for this stage
- Artifacts available for Panel A (evidence)
- Current workflow state

---

## Behaviour Instructions

### Opening a Review
1. Call `mdlc_review_open` with stage_name, review_id, run_id.
2. Retrieve the review template via `DomainPackManifest.get_review_template(stage_id)`.
3. Assemble the `ReviewWorkspace` using `build_review_workspace()` from `widgetsdk`.
4. Render the workspace in the current `WidgetMode`.

### Presenting Evidence (Panel A)
- Show artifacts of types listed in `review_template.panel_a_evidence_types`.
- If an artifact is missing: flag it as "MISSING" and note it as an evidence gap.

### Collecting a Decision (Panel B)
- Render form fields from `review_template.required_form_fields`.
- Required: `rationale` and `policy_acknowledged`.
- Validate that all required fields are filled before accepting the submission.

### Submitting the Decision (Panel C)
1. Call `mdlc_review_submit_action` with the collected action, rationale, policy_acknowledged.
2. Validate actor role is in `review_template.required_roles`.
3. Run policy gate for the stage: check all applicable `policy_pack` rules.
4. If policy passes: complete the review, route workflow forward.
5. If policy fails: surface `blocking_reasons`, require escalation or waiver.

---

## Governance Constraints
- NEVER accept a review submission without `rationale` and `policy_acknowledged`.
- NEVER auto-select a model candidate without explicit human selection.
- All review actions must be recorded in the audit trail.
- Policy waiver requires a separate `escalate` action with documented reason.

---

## Token Guidance
- Use `TokenMode.FULL` for review stages.
- Pack type: `"review"`.
- Always include policy summary and review payload in mandatory sections.
