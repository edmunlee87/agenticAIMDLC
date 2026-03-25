"""Recursive Feature Elimination (RFE) method."""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.feature_selection import RFE

from feature_selection_sdk.enums import SelectionMethod
from feature_selection_sdk.models import FeatureImportanceRecord, FeatureSelectionConfig
from feature_selection_sdk.methods.base import BaseSelectionMethod


class RFEMethod(BaseSelectionMethod):
    """Recursive Feature Elimination with a linear coefficient or tree importance signal.

    Requires a pre-fittable estimator that exposes either ``coef_`` or
    ``feature_importances_`` after fitting (e.g. LogisticRegression,
    GradientBoostingClassifier).
    """

    method = SelectionMethod.RECURSIVE_FEATURE_ELIMINATION

    def fit_score(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        estimator: Any | None = None,
    ) -> list[FeatureImportanceRecord]:
        """Run RFE and return ranking.

        Args:
            X: Feature matrix.
            y: Target series.
            estimator: Sklearn estimator exposing ``coef_`` or ``feature_importances_``.
                Raises ``ValueError`` if None.

        Returns:
            Sorted :class:`FeatureImportanceRecord` list. Importance score is
            ``1 / ranking_`` (lower ranking = higher importance).
        """
        if estimator is None:
            raise ValueError("RFEMethod requires an estimator.")

        X_s, y_s = self._sample(X, y)
        n_to_select = self._config.top_n_features or max(1, len(X_s.columns) // 2)

        rfe = RFE(estimator=estimator, n_features_to_select=n_to_select)
        rfe.fit(X_s, y_s)

        # ranking_ is 1-indexed; rank 1 = selected. Invert for score (higher = better).
        scores = {
            col: float(1.0 / rank)
            for col, rank in zip(X_s.columns, rfe.ranking_)
        }
        records = self._rank_and_flag(scores, self._config.top_n_features)
        # Override selected to match RFE's mask exactly
        rfe_selected = set(X_s.columns[rfe.support_])
        return [
            r.model_copy(update={"selected": r.feature_name in rfe_selected})
            for r in records
        ]
