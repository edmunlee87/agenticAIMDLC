"""Feature selection SDK enumerations."""

from enum import Enum


class SelectionMethod(str, Enum):
    """Available feature selection methods."""

    SHAP_IMPORTANCE = "shap_importance"
    PERMUTATION_IMPORTANCE = "permutation_importance"
    MUTUAL_INFORMATION = "mutual_information"
    RECURSIVE_FEATURE_ELIMINATION = "recursive_feature_elimination"
    LASSO_REGULARIZATION = "lasso_regularization"
    CORRELATION_FILTER = "correlation_filter"
    VARIANCE_THRESHOLD = "variance_threshold"
    STABILITY_SELECTION = "stability_selection"
    BORUTA = "boruta"
    INFORMATION_VALUE = "information_value"


class SelectionObjective(str, Enum):
    """Target objective for feature selection."""

    BINARY_CLASSIFICATION = "binary_classification"
    MULTICLASS_CLASSIFICATION = "multiclass_classification"
    REGRESSION = "regression"
    SURVIVAL = "survival"
    RANKING = "ranking"


class ImportanceAggregation(str, Enum):
    """How to aggregate importances across models or bootstrap runs."""

    MEAN = "mean"
    MEDIAN = "median"
    MIN = "min"
    PERCENTILE_25 = "percentile_25"


class StabilityMetric(str, Enum):
    """Stability scoring metric for stability selection."""

    KUNCHEVA_INDEX = "kuncheva_index"
    JACCARD_MEAN = "jaccard_mean"
    SELECTION_FREQUENCY = "selection_frequency"
