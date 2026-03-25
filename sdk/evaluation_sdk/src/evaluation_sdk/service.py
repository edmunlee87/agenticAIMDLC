"""evaluation_sdk.service -- EvaluationService: evaluate metrics against thresholds."""

from __future__ import annotations

import logging
from typing import Any

from evaluation_sdk.models import EvaluationPack, MetricRecord, MetricStatus, ModelComparison, ModelDiagnostic

logger = logging.getLogger(__name__)


def evaluate_metric(
    metric_id: str,
    metric_name: str,
    value: float,
    run_id: str,
    project_id: str,
    stage_name: str = "",
    dataset_split: str = "test",
    threshold_low: float | None = None,
    threshold_high: float | None = None,
) -> MetricRecord:
    """Evaluate a single metric against optional thresholds.

    Args:
        metric_id: Unique metric ID.
        metric_name: Metric name.
        value: Computed value.
        run_id: MDLC run.
        project_id: Project.
        stage_name: Stage.
        dataset_split: Dataset split. Default: ``"test"``.
        threshold_low: Minimum acceptable value.
        threshold_high: Maximum acceptable value.

    Returns:
        :class:`MetricRecord` with computed status.
    """
    if threshold_low is None and threshold_high is None:
        status = MetricStatus.NOT_EVALUATED
    elif (threshold_low is not None and value < threshold_low) or \
         (threshold_high is not None and value > threshold_high):
        status = MetricStatus.FAIL
    else:
        status = MetricStatus.PASS

    return MetricRecord(
        metric_id=metric_id,
        metric_name=metric_name,
        value=value,
        threshold_low=threshold_low,
        threshold_high=threshold_high,
        status=status,
        dataset_split=dataset_split,
        stage_name=stage_name,
        run_id=run_id,
        project_id=project_id,
    )


def compare_candidates(
    comparison_id: str,
    baseline_id: str,
    challenger_id: str,
    baseline_metrics: dict[str, float],
    challenger_metrics: dict[str, float],
    primary_metric: str,
    run_id: str,
    project_id: str,
    higher_is_better: bool = True,
) -> ModelComparison:
    """Compare two candidate versions on a metric set.

    Args:
        comparison_id: Unique comparison ID.
        baseline_id: Baseline candidate version ID.
        challenger_id: Challenger candidate version ID.
        baseline_metrics: Dict of metric_name -> value for baseline.
        challenger_metrics: Dict of metric_name -> value for challenger.
        primary_metric: Metric used to determine winner.
        run_id: MDLC run.
        project_id: Project.
        higher_is_better: If True, higher primary metric value wins. Default: True.

    Returns:
        :class:`ModelComparison`.
    """
    all_metrics = set(baseline_metrics) | set(challenger_metrics)
    metrics: dict[str, tuple[float, float, float]] = {}
    for name in all_metrics:
        bv = baseline_metrics.get(name, float("nan"))
        cv = challenger_metrics.get(name, float("nan"))
        metrics[name] = (bv, cv, cv - bv)

    b_primary = baseline_metrics.get(primary_metric, 0.0)
    c_primary = challenger_metrics.get(primary_metric, 0.0)
    if higher_is_better:
        winner = "challenger" if c_primary > b_primary else ("baseline" if b_primary > c_primary else "tie")
    else:
        winner = "challenger" if c_primary < b_primary else ("baseline" if b_primary < c_primary else "tie")

    return ModelComparison(
        comparison_id=comparison_id,
        baseline_candidate_id=baseline_id,
        challenger_candidate_id=challenger_id,
        metrics=metrics,
        winner=winner,
        run_id=run_id,
        project_id=project_id,
    )


class EvaluationService:
    """Manages evaluation packs and metric history.

    Args:
        observability_service: Optional observability service.
    """

    def __init__(self, observability_service: Any = None) -> None:
        self._obs = observability_service
        self._packs: dict[str, EvaluationPack] = {}

    def register_pack(self, pack: EvaluationPack) -> Any:
        """Register an evaluation pack.

        Args:
            pack: :class:`EvaluationPack` to register.

        Returns:
            Result with pack_id.
        """
        try:
            self._packs[pack.pack_id] = pack
            logger.info("evaluation_service.pack_registered", extra={"pack_id": pack.pack_id, "overall_pass": pack.overall_pass})
            return self._ok(pack.pack_id)
        except Exception as exc:
            return self._fail("ERR_REGISTER", str(exc))

    def get_pack(self, pack_id: str) -> Any:
        """Retrieve an evaluation pack.

        Args:
            pack_id: Pack identifier.

        Returns:
            Result with :class:`EvaluationPack`.
        """
        pack = self._packs.get(pack_id)
        if pack is None:
            return self._fail("ERR_NOT_FOUND", f"Pack '{pack_id}' not found.")
        return self._ok(pack)

    def list_packs_for_run(self, run_id: str) -> Any:
        """Return all evaluation packs for a run.

        Args:
            run_id: Run identifier.

        Returns:
            Result with list of :class:`EvaluationPack`.
        """
        packs = [p for p in self._packs.values() if p.run_id == run_id]
        return self._ok(packs)

    def health_check(self) -> dict[str, Any]:
        """Return health status."""
        return {"status": "ok", "service": "EvaluationService", "pack_count": len(self._packs)}

    @staticmethod
    def _ok(data: Any) -> Any:
        class _R:
            def __init__(self, d: Any) -> None:
                self.success = True; self.data = d; self.error_code = None
        return _R(data)

    @staticmethod
    def _fail(code: str, msg: str) -> Any:
        class _R:
            def __init__(self, c: str, m: str) -> None:
                self.success = False; self.data = None; self.error_code = c; self.error_message = m
        return _R(code, msg)
