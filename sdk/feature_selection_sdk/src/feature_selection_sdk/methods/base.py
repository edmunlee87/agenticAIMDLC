"""Abstract base class for feature selection method implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np
import pandas as pd

from feature_selection_sdk.enums import SelectionMethod
from feature_selection_sdk.models import FeatureImportanceRecord, FeatureSelectionConfig


class BaseSelectionMethod(ABC):
    """Abstract base for a single feature selection method.

    Each method receives a fitted or unfitted estimator (or None for
    filter methods) and returns a list of :class:`FeatureImportanceRecord`
    instances ranked by importance.

    Args:
        config: Feature selection run configuration.
    """

    method: SelectionMethod  # subclasses must declare

    def __init__(self, config: FeatureSelectionConfig) -> None:
        self._config = config

    @abstractmethod
    def fit_score(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        estimator: Any | None = None,
    ) -> list[FeatureImportanceRecord]:
        """Compute feature importance scores.

        Args:
            X: Feature matrix (already subset to candidate_columns if applicable).
            y: Target series.
            estimator: Optional pre-fitted or unfitted sklearn-compatible estimator.
                Filter methods ignore this argument.

        Returns:
            List of :class:`FeatureImportanceRecord`, one per feature, sorted by
            importance descending.
        """

    def _sample(self, X: pd.DataFrame, y: pd.Series) -> tuple[pd.DataFrame, pd.Series]:
        """Apply sample_size cap if configured."""
        cap = self._config.sample_size
        if cap and len(X) > cap:
            rng = np.random.default_rng(self._config.random_seed)
            idx = rng.choice(len(X), size=cap, replace=False)
            return X.iloc[idx].reset_index(drop=True), y.iloc[idx].reset_index(drop=True)
        return X, y

    def _rank_and_flag(
        self,
        scores: dict[str, float],
        top_n: int,
    ) -> list[FeatureImportanceRecord]:
        """Convert raw scores dict into sorted, ranked, flagged FeatureImportanceRecord list.

        Args:
            scores: Feature name -> importance score mapping.
            top_n: How many features to flag as selected (0 = all with score > 0).

        Returns:
            Sorted list of :class:`FeatureImportanceRecord`.
        """
        sorted_items = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        n_select = top_n if top_n > 0 else len([v for v in scores.values() if v > 0])
        records = []
        for rank, (name, score) in enumerate(sorted_items, start=1):
            records.append(
                FeatureImportanceRecord(
                    feature_name=name,
                    importance_score=score,
                    method=self.method,
                    rank=rank,
                    selected=rank <= n_select,
                )
            )
        return records
