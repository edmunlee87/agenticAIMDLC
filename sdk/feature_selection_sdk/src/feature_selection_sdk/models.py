"""Pydantic models for feature selection SDK inputs, outputs, and configuration."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from feature_selection_sdk.enums import (
    ImportanceAggregation,
    SelectionMethod,
    SelectionObjective,
    StabilityMetric,
)


class FeatureImportanceRecord(BaseModel):
    """Importance score for a single feature from one method.

    Args:
        feature_name: Column name.
        importance_score: Raw importance score (higher = more important).
        method: Selection method that produced this score.
        rank: Rank within this method (1 = most important).
        selected: Whether this feature was selected by this method.
        metadata: Method-specific supplementary data.
    """

    model_config = ConfigDict(frozen=True)

    feature_name: str
    importance_score: float
    method: SelectionMethod
    rank: int = 0
    selected: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class AggregatedImportance(BaseModel):
    """Cross-method aggregated importance for a single feature.

    Args:
        feature_name: Column name.
        aggregated_score: Score after aggregation across methods.
        vote_count: Number of methods that selected this feature.
        stability_score: Stability across bootstrap runs (0-1, 1 = perfectly stable).
        final_selected: Whether this feature passes the final selection criteria.
        method_scores: Map of method -> raw importance score.
    """

    model_config = ConfigDict(frozen=True)

    feature_name: str
    aggregated_score: float
    vote_count: int = 0
    stability_score: float = 0.0
    final_selected: bool = False
    method_scores: dict[str, float] = Field(default_factory=dict)


class FeatureSelectionConfig(BaseModel):
    """Configuration for a feature selection run.

    Args:
        objective: Prediction objective type.
        methods: Ordered list of selection methods to run.
        target_column: Target variable column name.
        candidate_columns: Columns to consider. Empty = all non-target columns.
        top_n_features: Hard cap on selected features. 0 = no cap.
        min_vote_count: Minimum number of methods a feature must be selected by.
        aggregation: How to aggregate cross-method importance scores.
        stability_n_bootstrap: Bootstrap iterations for stability selection. 0 = skip.
        stability_subsample_ratio: Fraction of rows per bootstrap iteration.
        stability_threshold: Minimum selection frequency to count as stable.
        stability_metric: Which stability metric to report.
        correlation_threshold: Max pairwise correlation; drop the less important feature.
        variance_threshold: Minimum variance to keep a feature.
        information_value_min: Minimum IV to keep a feature (0 = skip IV filter).
        random_seed: Fixed seed for reproducibility. Default: 42.
        sample_size: Row cap for heavy methods (SHAP, permutation). 0 = all rows.
    """

    model_config = ConfigDict(frozen=True)

    objective: SelectionObjective = SelectionObjective.BINARY_CLASSIFICATION
    methods: list[SelectionMethod] = Field(
        default_factory=lambda: [SelectionMethod.MUTUAL_INFORMATION, SelectionMethod.SHAP_IMPORTANCE]
    )
    target_column: str = "target"
    candidate_columns: list[str] = Field(default_factory=list)
    top_n_features: int = 0
    min_vote_count: int = 1
    aggregation: ImportanceAggregation = ImportanceAggregation.MEAN
    stability_n_bootstrap: int = 0
    stability_subsample_ratio: float = 0.8
    stability_threshold: float = 0.6
    stability_metric: StabilityMetric = StabilityMetric.SELECTION_FREQUENCY
    correlation_threshold: float = 0.95
    variance_threshold: float = 0.0
    information_value_min: float = 0.02
    random_seed: int = 42
    sample_size: int = 0

    @field_validator("stability_subsample_ratio", mode="before")
    @classmethod
    def _subsample_in_range(cls, v: float) -> float:
        if not (0.1 <= v <= 1.0):
            raise ValueError("stability_subsample_ratio must be between 0.1 and 1.0")
        return v

    @field_validator("correlation_threshold", mode="before")
    @classmethod
    def _corr_in_range(cls, v: float) -> float:
        if not (0.0 < v <= 1.0):
            raise ValueError("correlation_threshold must be in (0, 1]")
        return v


class FeatureSelectionResult(BaseModel):
    """Full output of a feature selection run.

    Args:
        run_id: Run identifier for traceability.
        stage_name: MDLC stage that triggered this run.
        config: The configuration used.
        feature_importances: Per-method importance records for all features.
        aggregated_importances: Cross-method aggregated importances.
        selected_features: Final ordered list of selected feature names.
        dropped_features: Features that were dropped and the primary reason.
        stability_summary: Stability metrics if stability selection was run.
        method_runtimes_seconds: Wall time per method.
        warnings: Non-blocking issues encountered during selection.
        artifact_id: ID of the registered artifact containing this result.
    """

    model_config = ConfigDict(frozen=True)

    run_id: str
    stage_name: str
    config: FeatureSelectionConfig
    feature_importances: list[FeatureImportanceRecord] = Field(default_factory=list)
    aggregated_importances: list[AggregatedImportance] = Field(default_factory=list)
    selected_features: list[str] = Field(default_factory=list)
    dropped_features: dict[str, str] = Field(default_factory=dict)
    stability_summary: dict[str, Any] = Field(default_factory=dict)
    method_runtimes_seconds: dict[str, float] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    artifact_id: str = ""
