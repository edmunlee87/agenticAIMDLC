# Skill: Deployment Readiness Stage
**Skill ID:** `stages.deployment_readiness`
**Version:** 1.0.0
**Layer:** Stages
**Applies To:** All domains with a `deployment_readiness` stage

---

## Purpose
Final governance gate before model deployment.
Three roles must approve: model_risk, it_change_management, and senior_management (or domain equivalent).

---

## Pre-Deployment Checklist
Confirm ALL items before approval:

**Performance**
- [ ] Primary metric meets policy threshold (e.g. Gini >= 0.40)
- [ ] No metric degradation > policy limit from test to OOT
- [ ] PSI within acceptable range (< 0.20)

**Documentation**
- [ ] Model card completeness >= 90%
- [ ] All governance gate reviews completed and approved
- [ ] Validation conclusion is `VALIDATED` or `CONDITIONALLY_VALIDATED`

**Process**
- [ ] No open CRITICAL findings in the validation system
- [ ] IT change management ticket approved
- [ ] Deployment config reviewed (monitoring thresholds, alert rules)

**Compliance**
- [ ] No protected attributes without waiver
- [ ] All waivers documented with rationale and approver

---

## Review Workflow

### Panel A: Evidence Pack
- `selected_model`, `evaluation_pack`, `score_scaling_table`
- `validation_conclusion`, open findings list
- `deployment_approval` (IT change management)

### Panel B: Final Approval Form
Required fields:
- `rationale`: summary of deployment decision
- `deployment_date`: target go-live date
- `monitoring_owner`: team responsible post-deployment
- `policy_acknowledged`: True
- `conditions`: post-deployment conditions if any

### Panel C: Actions
- `approve` → deploy
- `reject` → return to model_review
- `escalate` → senior management / board-level review

---

## Post-Approval
After approval:
1. Register `deployment_record` artifact.
2. Emit `workflow.stage.completed` for `deployment_readiness`.
3. Transition to `deployed` (terminal stage).
4. Trigger monitoring setup.
