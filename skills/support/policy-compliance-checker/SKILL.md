# Skill: Policy Compliance Checker
**Skill ID:** `support.policy_compliance_checker`
**Version:** 1.0.0
**Layer:** Support

---

## Purpose
Evaluate all applicable domain policy rules against current metrics and process state.
Produce a structured compliance report for use in review decisions and audit records.

---

## When to Invoke
- Before approving any governance gate review.
- On demand by the validator or model risk role.
- As part of deployment readiness pre-flight.

---

## Evaluation Steps

For each rule in `DomainPackManifest.policy_pack` where `stage_id in rule.applies_to_stages`:
1. Retrieve current metrics from `EvaluationService`.
2. Evaluate `rule.condition_expression` (textual check, not executed; compare metric values).
3. Assign status: `PASS` | `FAIL` | `WARN` | `WAIVER_REQUIRED`.
4. If `FAIL` and `requires_waiver=False`: mark as BLOCKING.
5. If `FAIL` and `requires_waiver=True`: mark as WAIVER_REQUIRED.

---

## Output Format

```
Policy Compliance Report
-------------------------
Stage: model_review | Run: run_abc | Domain: scorecard

Rules Evaluated: 3

[PASS]           sc_pol_model_performance  -- Gini=0.52 >= 0.40, KS=0.38 >= 0.25, PSI=0.06 <= 0.20
[PASS]           sc_pol_model_documentation -- Model card completeness: 0.95 >= 0.90
[WAIVER_REQUIRED] sc_pol_woe_review        -- WoE non-monotone for variable 'age_band' (waiver on file: W-2024-001)

Blocking Failures: 0
Waiver Required: 1

Recommendation: Review is APPROVABLE with waiver W-2024-001 acknowledged.
```

---

## Integration
Pass this output as `policy_check_result` in the `StandardResponseEnvelope.GovernanceSummary`.
Include rule IDs and statuses in the audit trail.

---

## Token Guidance
- Token Mode: `COMPACT`.
- This skill produces a compact policy table; not full metric diagnostics.
