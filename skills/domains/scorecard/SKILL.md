# Skill: Scorecard Domain
**Skill ID:** `domains.scorecard`
**Version:** 1.0.0
**Layer:** Domains

---

## Domain Overview
Credit scorecard development using logistic regression with WoE/IV feature transformation.
Produces a points-based scorecard calibrated to population odds.

Regulatory scope: IFRS9, Basel III, SR 11-7.

---

## Stage Guidance

### data_preparation
- Validate against `sc_pol_data_quality`: all blocking DQ failures must be resolved.
- Output: `dataset_snapshot` + `dq_report` artifacts.

### fine_classing
- Produce initial 15-25 bins per continuous variable.
- Flag low-variance and near-constant variables for exclusion.

### coarse_classing
- Merge fine bins to 5-8 meaningful groups per variable.
- Preserve business logic (e.g. do not merge "0 balance" with "1-100" balance bins).
- Output: `coarse_classing_table` + `binning_candidate_set`.

### coarse_classing_review (HITL)
- Review template: `coarse_classing_review_tmpl`.
- Required evidence: coarse classing table, DQ report.
- Check: monotonicity of bad rates across bins, business interpretation.

### woe_iv_calculation
- Compute WoE and IV per variable.
- Flag non-monotone WoE patterns for review.
- Minimum IV threshold: 0.02 (below = auto-reject).

### woe_iv_review (HITL)
- Policy `sc_pol_woe_review`: monotonicity violations require waiver.
- Review non-monotone variables individually with business justification.

### feature_shortlist
- Minimum total IV: 0.30 across selected features.
- Maximum pairwise correlation: 0.70.
- Flag protected attributes and require waiver if included.

### feature_shortlist_review (HITL)
- Critical: `sc_pol_feature_review` -- protected attributes require compliance sign-off.

### model_development
- Train logistic regression on selected features with WoE-encoded values.
- Generate candidates with Gini, KS, AUC-ROC metrics on test and OOT splits.
- Recommend best candidate by Gini.

### model_review (HITL)
- Policy: Gini >= 0.40 test, KS >= 0.25, PSI <= 0.20.
- Selection required; auto-recommendation is advisory only.
- Reviewer selects final model; model card review included.

### score_scaling
- Standard PDO scaling: base_score=600, pdo=20, odds_0=50.
- Score range: 300-850.
- Validate calibration: expected vs. observed bad rates by score band.

### deployment_readiness (HITL)
- All three roles required: model_risk, it_change_management, senior_management.
- Must pass `sc_pol_model_performance`, `sc_pol_model_documentation`, `sc_pol_deployment`.

---

## Token Guidance
- COMPACT for development stages (fine_classing, coarse_classing, woe_iv, feature_shortlist).
- FULL for all review stages.

---

## Domain-Specific Checks
| Policy Rule | Stage | Waiver Available |
|-------------|-------|-----------------|
| `sc_pol_data_quality` | data_preparation | No |
| `sc_pol_woe_review` | woe_iv_review | Yes |
| `sc_pol_feature_review` | feature_shortlist_review | Yes |
| `sc_pol_model_performance` | model_review | No |
| `sc_pol_deployment` | deployment_readiness | No |
