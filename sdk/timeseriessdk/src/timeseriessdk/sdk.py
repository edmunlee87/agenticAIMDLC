"""timeseriessdk.sdk -- TimeSeriesSDK: concrete domain SDK for time-series models."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from platform_core.domain.base_domain_sdk import BaseDomainSDK, StageComputeResult
from platform_core.domain.loader import DomainPackLoader
from platform_core.domain.models import DomainPackManifest

_MANIFEST_PATH = Path(__file__).parent.parent.parent.parent.parent.parent / "configs" / "runtime" / "domain_overlays" / "time_series.yaml"


class TimeSeriesSDK(BaseDomainSDK):
    """Domain SDK for time-series forecasting models.

    Args:
        run_id: MDLC run identifier.
        project_id: Project identifier.
        actor_id: Actor executing domain logic.
        manifest_path: Optional override path to the domain pack YAML.
        observability_service: Optional observability service.
        audit_service: Optional audit service.
        artifact_service: Optional artifact service.
    """

    def __init__(self, run_id: str, project_id: str, actor_id: str = "",
                 manifest_path: str | Path | None = None, **kwargs: Any) -> None:
        super().__init__(run_id, project_id, actor_id, **kwargs)
        self._manifest_path = Path(manifest_path) if manifest_path else _MANIFEST_PATH
        self._manifest: DomainPackManifest | None = None
        self._loader = DomainPackLoader()

    def get_manifest(self) -> DomainPackManifest:
        """Return the time-series domain pack manifest."""
        if self._manifest is None:
            self._manifest = self._loader.load("time_series", self._manifest_path)
        return self._manifest

    def compute_stage(self, stage_id: str, inputs: dict[str, Any]) -> StageComputeResult:
        """Execute time-series domain computation for a stage.

        Args:
            stage_id: Stage to compute.
            inputs: Stage inputs.

        Returns:
            :class:`~platform_core.domain.base_domain_sdk.StageComputeResult`.
        """
        if stage_id == "data_preparation":
            return StageComputeResult(
                stage_id=stage_id, success=True,
                artifacts={"dataset_snapshot": {"snapshot_id": str(uuid.uuid4())}},
            )
        if stage_id == "feature_engineering":
            features = inputs.get("lag_features", []) + inputs.get("window_features", [])
            return StageComputeResult(
                stage_id=stage_id, success=True,
                artifacts={"feature_set": {"features": features}},
                metrics={"feature_count": len(features)},
            )
        if stage_id == "model_development":
            candidates = inputs.get("candidates", [])
            return StageComputeResult(
                stage_id=stage_id, success=True,
                artifacts={"model_candidate_set": candidates},
                candidates=candidates,
            )
        # Review/governance stages
        return StageComputeResult(stage_id=stage_id, success=True,
                                   metadata={"note": f"Stage '{stage_id}' is a review stage."})
