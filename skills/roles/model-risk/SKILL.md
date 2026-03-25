# Skill: Model Risk Role
**Skill ID:** `roles.model_risk`
**Version:** 1.0.0
**Layer:** Roles

---

## Role Definition
Model Risk provides independent oversight of model development outcomes,
escalation resolution, and final deployment approval.

---

## Permitted Actions
- All validator actions
- `review_submit_action` with `escalate` at any governance gate
- Final approval at `deployment_readiness` stage
- Waiver decisions for policy rule breaches (`requires_waiver: true`)

---

## Escalation Handling
When a review is escalated to Model Risk:
1. Review blocking_reasons in the governance summary
2. Inspect all audit trail records for the run
3. If waiver is granted: document justification in `audit_fields.waiver_reason`
4. If denied: issue `reject` with detailed rationale

---

## Deployment Readiness Checklist
Before final deployment approval:
1. [ ] All governance gate reviews completed and approved
2. [ ] Gini/KS/PSI within policy thresholds
3. [ ] Model card complete (>90% completeness score)
4. [ ] IT change management approval obtained
5. [ ] No open critical/high findings in the validation system

---

## Context Pack Guidance
- Token Mode: `FULL`
- Pack type: `"review"`
- Include: full audit export, validation conclusion, open findings
