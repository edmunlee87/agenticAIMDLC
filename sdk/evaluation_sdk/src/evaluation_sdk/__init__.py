"""evaluation_sdk -- model evaluation metrics, diagnostics, and comparison."""

from evaluation_sdk.models import EvaluationPack, MetricRecord, MetricStatus, ModelComparison, ModelDiagnostic
from evaluation_sdk.service import EvaluationService, compare_candidates, evaluate_metric

__all__ = [
    "EvaluationPack", "EvaluationService", "MetricRecord", "MetricStatus",
    "ModelComparison", "ModelDiagnostic", "compare_candidates", "evaluate_metric",
]
