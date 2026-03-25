"""Mutual information feature selection method."""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression

from feature_selection_sdk.enums import SelectionMethod, SelectionObjective
from feature_selection_sdk.models import FeatureImportanceRecord, FeatureSelectionConfig
from feature_selection_sdk.methods.base import BaseSelectionMethod


class MutualInformationMethod(BaseSelectionMethod):
    """Filter method using mutual information between each feature and the target.

    Uses ``sklearn.feature_selection.mutual_info_classif`` for classification
    objectives and ``mutual_info_regression`` for regression objectives.
    Deterministic via ``random_state`` from config.
    """

    method = SelectionMethod.MUTUAL_INFORMATION

    def fit_score(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        estimator: Any | None = None,
    ) -> list[FeatureImportanceRecord]:
        """Compute mutual information scores.

        Args:
            X: Feature matrix.
            y: Target series.
            estimator: Ignored -- filter method.

        Returns:
            Sorted :class:`FeatureImportanceRecord` list.
        """
        X_s, y_s = self._sample(X, y)

        regression_objectives = {SelectionObjective.REGRESSION, SelectionObjective.SURVIVAL}
        if self._config.objective in regression_objectives:
            scores_arr = mutual_info_regression(
                X_s.values,
                y_s.values,
                random_state=self._config.random_seed,
            )
        else:
            scores_arr = mutual_info_classif(
                X_s.values,
                y_s.values,
                random_state=self._config.random_seed,
            )

        scores = {col: float(score) for col, score in zip(X_s.columns, scores_arr)}
        return self._rank_and_flag(scores, self._config.top_n_features)
