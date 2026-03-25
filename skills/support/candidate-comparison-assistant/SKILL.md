# Skill: Candidate Comparison Assistant
**Skill ID:** `support.candidate_comparison_assistant`
**Version:** 1.0.0
**Layer:** Support

---

## Purpose
Help the reviewer compare model candidates objectively and identify the optimal selection
based on primary metric, stability, simplicity, and policy compliance.

---

## When to Invoke
Invoked by `ReviewOrchestratorSkill` during any `model_review` or `selection` review type.

---

## Comparison Steps

1. **Rank by primary metric** on test split.
2. **Check OOT stability**: flag candidates with Gini degradation > policy limit.
3. **Check PSI**: flag candidates with PSI > 0.20 as unstable.
4. **Feature count**: prefer simpler models (fewer features) when metrics are within 2%.
5. **Policy compliance**: any candidate failing CRITICAL policy rules is ineligible.
6. **Produce recommendation**: recommended candidate with supporting rationale.

---

## Output Format
Return a structured comparison summary:

```
Candidate Comparison Summary
-----------------------------
Recommended: <candidate_id> (<version_label>)
Reason: <primary_metric>=<value> on test, OOT degradation=<value>, PSI=<value>

All Candidates (ranked by <primary_metric>):
| Rank | Candidate | Gini (Test) | Gini (OOT) | PSI | Features | Eligible |
|------|-----------|-------------|------------|-----|----------|---------|
| 1    | cand_001  | 0.521       | 0.498      | 0.05| 12       | Yes     |
| 2    | cand_002  | 0.510       | 0.475      | 0.08| 15       | Yes     |
...

Ineligible Candidates:
- cand_003: CRITICAL policy failure (Gini < 0.40 on OOT)
```

---

## Token Guidance
- This skill produces a compact summary (not full model diagnostics).
- Token Mode: `COMPACT`.
- Output is injected as a knowledge section in the review context pack.
