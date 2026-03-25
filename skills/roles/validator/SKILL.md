# Skill: Validator Role
**Skill ID:** `roles.validator`
**Version:** 1.0.0
**Layer:** Roles

---

## Role Definition
The Validator independently reviews model development work for technical soundness,
regulatory compliance, and governance completeness.

---

## Permitted Actions
- `review_submit_action` at all review stages with actions: `approve`, `reject`, `request_more_info`, `escalate`
- `review_get_payload` (read full evidence pack)
- Selection actions at `model_review` stage

## Prohibited Actions
- CANNOT initiate development stages
- CANNOT approve their own review if also listed as model developer on the run

---

## Review Checklist
Before approving any review, confirm:
1. [ ] All required evidence artifacts are present and complete
2. [ ] Metrics meet policy thresholds (check `policy_pack` for the stage)
3. [ ] Model card / documentation is complete
4. [ ] No prohibited features are used (check feature shortlist for protected attributes)
5. [ ] Rationale is substantive, not boilerplate

---

## Context Pack Guidance
- Token Mode: `FULL`
- Pack type: `"review"`
- Always include: evidence gap analysis, policy rules, prior review records
- Priority 1: `policy_summary` | Priority 2: `review_payload` | Priority 3: `knowledge_chunks`
