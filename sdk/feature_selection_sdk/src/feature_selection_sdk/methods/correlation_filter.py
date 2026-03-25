"""Correlation filter -- remove highly correlated feature pairs."""

from __future__ import annotations

from typing import Any

import pandas as pd

from feature_selection_sdk.enums import SelectionMethod
from feature_selection_sdk.models import FeatureImportanceRecord, FeatureSelectionConfig
from feature_selection_sdk.methods.base import BaseSelectionMethod


class CorrelationFilterMethod(BaseSelectionMethod):
    """Remove one feature from each highly correlated pair.

    For each pair with |pearson r| > ``correlation_threshold``, the feature
    with the lower variance is dropped. This method assigns scores based on
    variance (higher variance = higher importance within a correlated group)
    and is best used as a pre-filter before wrapper or SHAP methods.
    """

    method = SelectionMethod.CORRELATION_FILTER

    def fit_score(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        estimator: Any | None = None,
    ) -> list[FeatureImportanceRecord]:
        """Compute correlation-based importance.

        Args:
            X: Feature matrix.
            y: Unused by this filter method.
            estimator: Ignored.

        Returns:
            Sorted :class:`FeatureImportanceRecord` list. Features that are
            dropped due to high correlation are flagged ``selected=False``.
        """
        threshold = self._config.correlation_threshold
        variances = X.var()
        corr_matrix = X.corr().abs()

        to_drop: set[str] = set()
        cols = list(X.columns)
        for i, col_i in enumerate(cols):
            if col_i in to_drop:
                continue
            for col_j in cols[i + 1 :]:
                if col_j in to_drop:
                    continue
                if corr_matrix.at[col_i, col_j] > threshold:
                    # Drop the feature with lower variance
                    loser = col_i if variances[col_i] <= variances[col_j] else col_j
                    to_drop.add(loser)

        scores = {col: float(variances[col]) for col in cols}
        records = self._rank_and_flag(scores, self._config.top_n_features)
        return [
            r.model_copy(update={"selected": r.feature_name not in to_drop})
            for r in records
        ]
