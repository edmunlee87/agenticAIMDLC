"""evaluation_sdk.models -- model evaluation metric and comparison contracts."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MetricStatus(str, Enum):
    """Threshold check status for a metric."""
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    NOT_EVALUATED = "not_evaluated"


class MetricRecord(BaseModel):
    """A single evaluated metric.

    Args:
        metric_id: Unique identifier.
        metric_name: Human-readable name (e.g. ``"gini"``, ``"auc"``).
        value: Numeric metric value.
        threshold_low: Minimum acceptable value (None = no lower bound).
        threshold_high: Maximum acceptable value (None = no upper bound).
        status: :class:`MetricStatus` based on threshold comparison.
        dataset_split: Which data split this was computed on.
        stage_name: Stage that produced this metric.
        run_id: MDLC run.
        project_id: Project.
        computed_at: Computation timestamp.
        metadata: Arbitrary extra metadata.
    """

    model_config = ConfigDict(frozen=True)

    metric_id: str
    metric_name: str
    value: float
    threshold_low: float | None = None
    threshold_high: float | None = None
    status: MetricStatus = MetricStatus.NOT_EVALUATED
    dataset_split: str = "test"
    stage_name: str = ""
    run_id: str = ""
    project_id: str = ""
    computed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict)


class ModelDiagnostic(BaseModel):
    """A model diagnostic record (e.g. PSI, CSI, KS statistic).

    Args:
        diagnostic_id: Unique identifier.
        diagnostic_name: Name (e.g. ``"ks_statistic"``, ``"psi_score"``).
        value: Numeric diagnostic value.
        interpretation: Human-readable interpretation.
        severity: ``"ok"`` | ``"warn"`` | ``"critical"``.
        stage_name: Stage.
        run_id: Run.
        project_id: Project.
    """

    model_config = ConfigDict(frozen=True)

    diagnostic_id: str
    diagnostic_name: str
    value: float
    interpretation: str = ""
    severity: str = "ok"
    stage_name: str = ""
    run_id: str = ""
    project_id: str = ""
    computed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ModelComparison(BaseModel):
    """Comparison of two candidate model versions on a metric set.

    Args:
        comparison_id: Unique identifier.
        baseline_candidate_id: Baseline candidate version ID.
        challenger_candidate_id: Challenger candidate version ID.
        metrics: Dict of metric_name -> (baseline_value, challenger_value, delta).
        winner: Which candidate is better (``"baseline"`` | ``"challenger"`` | ``"tie"``).
        scope: Comparison scope (e.g. ``"development"``).
        run_id: Run.
        project_id: Project.
        created_at: Creation timestamp.
    """

    model_config = ConfigDict(frozen=True)

    comparison_id: str
    baseline_candidate_id: str
    challenger_candidate_id: str
    metrics: dict[str, tuple[float, float, float]] = Field(default_factory=dict)
    winner: str = "tie"
    scope: str = "development"
    run_id: str = ""
    project_id: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EvaluationPack(BaseModel):
    """Bundled evaluation output: metrics + diagnostics + comparisons.

    Args:
        pack_id: Unique pack identifier.
        candidate_id: Candidate version being evaluated.
        run_id: MDLC run.
        project_id: Project.
        metrics: All metric records.
        diagnostics: All diagnostic records.
        comparison: Optional model comparison.
        overall_pass: True if all threshold checks pass.
        artifact_id: Artifact ID storing this pack.
    """

    model_config = ConfigDict(frozen=True)

    pack_id: str
    candidate_id: str
    run_id: str
    project_id: str
    metrics: list[MetricRecord] = Field(default_factory=list)
    diagnostics: list[ModelDiagnostic] = Field(default_factory=list)
    comparison: ModelComparison | None = None
    overall_pass: bool = True
    artifact_id: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
