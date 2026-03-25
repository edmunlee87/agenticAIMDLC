"""scorecardsdk.computations -- pure computation functions for scorecard development.

All functions are:
- Deterministic (no random state unless seed is passed).
- Side-effect free (no I/O, no logging).
- Fully typed.

These are the engine functions consumed by :class:`~scorecardsdk.sdk.ScorecardSDK`.
"""

from __future__ import annotations

import math
from typing import Any

from scorecardsdk.models import (
    BinDefinition,
    CoarseClassingTable,
    FeatureShortlist,
    ScorecardCandidate,
    ScorecardModel,
    ScoreScalingParams,
    WoeIvRecord,
)


# ---------------------------------------------------------------------------
# WoE / IV
# ---------------------------------------------------------------------------

_EPSILON = 1e-7  # Avoid log(0)


def compute_woe_iv(
    variable_name: str,
    bins: list[dict[str, Any]],
    total_goods: int,
    total_bads: int,
    record_id: str,
    minimum_iv_threshold: float = 0.02,
) -> WoeIvRecord:
    """Compute WoE and IV for a variable's binned distribution.

    WoE = ln(% Goods / % Bads) per bin.
    IV = sum((% Goods - % Bads) * WoE) across bins.

    Args:
        variable_name: Variable name.
        bins: List of dicts with ``good_count``, ``bad_count``, and bin metadata.
        total_goods: Total good count in population.
        total_bads: Total bad count in population.
        record_id: Unique WoeIvRecord ID.
        minimum_iv_threshold: Minimum IV for the variable to pass. Default: 0.02.

    Returns:
        :class:`WoeIvRecord` with computed WoE, IV, and monotonicity flag.
    """
    bin_defs: list[BinDefinition] = []
    total_iv = 0.0
    prev_woe: float | None = None
    is_monotone = True

    for i, b in enumerate(bins):
        g = max(b.get("good_count", 0), 0)
        bd = max(b.get("bad_count", 0), 0)
        pct_good = (g / total_goods) if total_goods > 0 else _EPSILON
        pct_bad = (bd / total_bads) if total_bads > 0 else _EPSILON
        pct_good = max(pct_good, _EPSILON)
        pct_bad = max(pct_bad, _EPSILON)

        woe = math.log(pct_good / pct_bad)
        iv_contrib = (pct_good - pct_bad) * woe
        total_iv += iv_contrib

        if prev_woe is not None and woe < prev_woe:
            is_monotone = False
        prev_woe = woe

        count = g + bd
        bin_defs.append(
            BinDefinition(
                bin_id=b.get("bin_id", f"bin_{i}"),
                variable_name=variable_name,
                bin_label=b.get("bin_label", f"Bin {i}"),
                lower_bound=b.get("lower_bound"),
                upper_bound=b.get("upper_bound"),
                category_values=b.get("category_values", []),
                count=count,
                good_count=g,
                bad_count=bd,
                bad_rate=bd / count if count > 0 else 0.0,
                woe=round(woe, 6),
                iv_contribution=round(iv_contrib, 6),
                is_special=b.get("is_special", False),
            )
        )

    return WoeIvRecord(
        record_id=record_id,
        variable_name=variable_name,
        total_iv=round(total_iv, 6),
        bins=bin_defs,
        is_monotone=is_monotone,
        passes_minimum_iv=total_iv >= minimum_iv_threshold,
        minimum_iv_threshold=minimum_iv_threshold,
    )


# ---------------------------------------------------------------------------
# Feature shortlisting
# ---------------------------------------------------------------------------

def build_feature_shortlist(
    shortlist_id: str,
    run_id: str,
    project_id: str,
    woe_iv_records: list[WoeIvRecord],
    minimum_iv: float = 0.02,
    maximum_correlation: float = 0.7,
    protected_attribute_names: list[str] | None = None,
    created_by: str = "",
) -> FeatureShortlist:
    """Select features based on IV thresholds.

    Features are excluded if:
    - total_iv < minimum_iv.
    - The variable is a protected attribute (flagged, not auto-excluded).

    Correlation exclusion is noted but not computed here (requires data);
    pass pre-filtered records to enforce correlation exclusion.

    Args:
        shortlist_id: Unique shortlist ID.
        run_id: MDLC run.
        project_id: Project.
        woe_iv_records: WoE/IV records for all candidate variables.
        minimum_iv: Minimum total IV for inclusion. Default: 0.02.
        maximum_correlation: Maximum pairwise Pearson correlation (documentation). Default: 0.7.
        protected_attribute_names: List of protected attribute variable names.
        created_by: Actor.

    Returns:
        :class:`FeatureShortlist`.
    """
    protected = set(protected_attribute_names or [])
    selected: list[str] = []
    iv_scores: dict[str, float] = {}
    rejected: dict[str, str] = {}

    for rec in woe_iv_records:
        if rec.total_iv < minimum_iv:
            rejected[rec.variable_name] = f"IV {rec.total_iv:.4f} below minimum {minimum_iv}"
            continue
        selected.append(rec.variable_name)
        iv_scores[rec.variable_name] = rec.total_iv

    total_shortlist_iv = sum(iv_scores.values())
    contains_protected = bool(protected & set(selected))

    return FeatureShortlist(
        shortlist_id=shortlist_id,
        run_id=run_id,
        project_id=project_id,
        selected_features=selected,
        iv_scores=iv_scores,
        rejected_features=rejected,
        contains_protected_attributes=contains_protected,
        total_shortlist_iv=round(total_shortlist_iv, 6),
        created_by=created_by,
    )


# ---------------------------------------------------------------------------
# Score scaling
# ---------------------------------------------------------------------------

def compute_score_scaling(
    scaling_id: str,
    model_id: str,
    base_score: float = 600.0,
    pdo: float = 20.0,
    odds_0: float = 50.0,
    score_min: float = 300.0,
    score_max: float = 850.0,
) -> ScoreScalingParams:
    """Create score scaling parameters.

    Score = base_score + (PDO / ln(2)) * (log-odds - ln(odds_0)).

    Args:
        scaling_id: Unique scaling ID.
        model_id: Source model ID.
        base_score: Score at odds_0. Default: 600.
        pdo: Points to double the odds. Default: 20.
        odds_0: Reference odds at base_score. Default: 50.
        score_min: Score floor. Default: 300.
        score_max: Score cap. Default: 850.

    Returns:
        :class:`ScoreScalingParams`.
    """
    return ScoreScalingParams(
        scaling_id=scaling_id,
        model_id=model_id,
        base_score=base_score,
        pdo=pdo,
        odds_0=odds_0,
        score_min=score_min,
        score_max=score_max,
    )


def apply_scaling(log_odds: float, params: ScoreScalingParams) -> float:
    """Apply score scaling to a log-odds value.

    Args:
        log_odds: Log-odds value (output from logistic regression).
        params: :class:`ScoreScalingParams`.

    Returns:
        Scaled scorecard score (clipped to [score_min, score_max]).
    """
    factor = params.pdo / math.log(2)
    raw_score = params.base_score + factor * (log_odds - math.log(params.odds_0))
    return max(params.score_min, min(params.score_max, raw_score))


# ---------------------------------------------------------------------------
# Candidate recommendation
# ---------------------------------------------------------------------------

def recommend_best_candidate(
    candidates: list[ScorecardCandidate],
    primary_metric: str = "gini",
    higher_is_better: bool = True,
) -> list[ScorecardCandidate]:
    """Return candidates sorted by primary metric with the best one marked as recommended.

    Args:
        candidates: List of :class:`ScorecardCandidate`.
        primary_metric: Metric name to rank by. Default: ``"gini"``.
        higher_is_better: Default: True.

    Returns:
        Sorted list of :class:`ScorecardCandidate` with the top one marked ``is_recommended=True``.
    """
    if not candidates:
        return []

    sorted_cands = sorted(
        candidates,
        key=lambda c: c.metrics.get(primary_metric, 0.0),
        reverse=higher_is_better,
    )

    result = []
    for i, cand in enumerate(sorted_cands):
        result.append(cand.model_copy(update={
            "is_recommended": i == 0,
            "rationale": f"Best {primary_metric}: {cand.metrics.get(primary_metric, 0.0):.4f}" if i == 0 else cand.rationale,
        }))
    return result
