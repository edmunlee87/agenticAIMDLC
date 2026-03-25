"""Stability selection via bootstrap subsampling.

Runs a configured selection method on ``n_bootstrap`` sub-samples of the
data and aggregates the selection frequency for each feature. Features that
are selected in at least ``stability_threshold`` fraction of runs are deemed
stable.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

import numpy as np
import pandas as pd

from feature_selection_sdk.enums import StabilityMetric
from feature_selection_sdk.models import FeatureSelectionConfig
from feature_selection_sdk.methods.base import BaseSelectionMethod

logger = logging.getLogger(__name__)


def kuncheva_index(
    selected_a: set[str],
    selected_b: set[str],
    total_features: int,
) -> float:
    """Compute the Kuncheva stability index between two feature subsets.

    Returns a value in [-1, 1] where 1 = identical subsets.

    Args:
        selected_a: First selected feature set.
        selected_b: Second selected feature set.
        total_features: Total number of candidate features (n).

    Returns:
        Kuncheva index in [-1, 1].
    """
    k_a = len(selected_a)
    k_b = len(selected_b)
    if k_a == 0 or k_b == 0:
        return 0.0
    r = len(selected_a & selected_b)
    k = (k_a + k_b) / 2
    n = total_features
    expected = k * k / n
    denom = k - expected
    return float((r - expected) / denom) if denom != 0 else 1.0


def run_stability_selection(
    method: BaseSelectionMethod,
    X: pd.DataFrame,
    y: pd.Series,
    config: FeatureSelectionConfig,
    estimator: Any | None = None,
) -> dict[str, Any]:
    """Run bootstrap stability selection and return a stability summary.

    Args:
        method: Fitted :class:`BaseSelectionMethod` instance.
        X: Full feature matrix.
        y: Target series.
        config: Selection configuration.
        estimator: Optional estimator for wrapper methods.

    Returns:
        Dict with keys:
        - ``selection_frequencies``: feature -> fraction of runs selected (0-1).
        - ``stable_features``: features with frequency >= stability_threshold.
        - ``kuncheva_mean``: Mean pairwise Kuncheva index across all bootstrap pairs.
        - ``n_bootstrap``: Number of bootstrap iterations actually run.
    """
    n_bootstrap = config.stability_n_bootstrap
    subsample = config.stability_subsample_ratio
    threshold = config.stability_threshold
    seed = config.random_seed
    rng = np.random.default_rng(seed)

    n_rows = len(X)
    sub_size = max(2, int(n_rows * subsample))
    selection_counts: dict[str, int] = defaultdict(int)
    all_selected_sets: list[set[str]] = []

    for i in range(n_bootstrap):
        idx = rng.choice(n_rows, size=sub_size, replace=False)
        X_sub = X.iloc[idx].reset_index(drop=True)
        y_sub = y.iloc[idx].reset_index(drop=True)

        try:
            records = method.fit_score(X_sub, y_sub, estimator=estimator)
            selected = {r.feature_name for r in records if r.selected}
        except Exception as exc:
            logger.warning(
                "stability_selection.bootstrap_failed",
                extra={"iteration": i, "error": str(exc)},
            )
            continue

        for feat in selected:
            selection_counts[feat] += 1
        all_selected_sets.append(selected)

    total_candidates = len(X.columns)
    freq = {
        feat: selection_counts[feat] / n_bootstrap
        for feat in X.columns
    }
    stable = {feat for feat, f in freq.items() if f >= threshold}

    # Kuncheva pairwise mean
    ki_scores: list[float] = []
    sets = all_selected_sets
    for a_idx in range(len(sets)):
        for b_idx in range(a_idx + 1, len(sets)):
            ki_scores.append(kuncheva_index(sets[a_idx], sets[b_idx], total_candidates))
    kuncheva_mean = float(np.mean(ki_scores)) if ki_scores else 0.0

    return {
        "selection_frequencies": freq,
        "stable_features": sorted(stable),
        "kuncheva_mean": round(kuncheva_mean, 4),
        "n_bootstrap": n_bootstrap,
        "threshold": threshold,
    }
