"""Permutation importance feature selection method (model-agnostic)."""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.model_selection import cross_val_score

from feature_selection_sdk.enums import SelectionMethod
from feature_selection_sdk.models import FeatureImportanceRecord, FeatureSelectionConfig
from feature_selection_sdk.methods.base import BaseSelectionMethod


class PermutationImportanceMethod(BaseSelectionMethod):
    """Model-agnostic permutation importance.

    Works with any sklearn-compatible estimator. Fits the estimator on the
    full sample (or capped sample), then measures the drop in score when
    each feature's values are randomly shuffled.

    Requires a pre-fitted or fittable estimator to be passed via ``fit_score``.
    If no estimator is provided, raises ``ValueError``.
    """

    method = SelectionMethod.PERMUTATION_IMPORTANCE

    def __init__(self, config: FeatureSelectionConfig, n_repeats: int = 5) -> None:
        super().__init__(config)
        self._n_repeats = n_repeats

    def fit_score(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        estimator: Any | None = None,
    ) -> list[FeatureImportanceRecord]:
        """Compute permutation importance.

        Args:
            X: Feature matrix.
            y: Target series.
            estimator: Sklearn-compatible estimator (will be fit if not already).
                Raises ``ValueError`` if None.

        Returns:
            Sorted :class:`FeatureImportanceRecord` list.
        """
        if estimator is None:
            raise ValueError(
                "PermutationImportanceMethod requires an estimator. "
                "Pass a fitted or fittable sklearn-compatible estimator."
            )

        X_s, y_s = self._sample(X, y)

        # Fit if the estimator has not been fitted yet.
        try:
            estimator.predict(X_s.iloc[:1])
        except Exception:
            estimator.fit(X_s, y_s)

        result = permutation_importance(
            estimator,
            X_s,
            y_s,
            n_repeats=self._n_repeats,
            random_state=self._config.random_seed,
        )

        scores = {
            col: float(mean)
            for col, mean in zip(X_s.columns, result.importances_mean)
        }
        return self._rank_and_flag(scores, self._config.top_n_features)
