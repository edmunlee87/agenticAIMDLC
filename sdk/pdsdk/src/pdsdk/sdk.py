"""pdsdk.sdk -- PDSDK: concrete domain SDK for PD models."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from platform_core.domain.base_domain_sdk import BaseDomainSDK, StageComputeResult
from platform_core.domain.loader import DomainPackLoader
from platform_core.domain.models import DomainPackManifest

_MANIFEST_PATH = Path(__file__).parent.parent.parent.parent.parent.parent / "configs" / "runtime" / "domain_overlays" / "pd.yaml"


class PDSDK(BaseDomainSDK):
    """Domain SDK for PD models."""

    def __init__(self, run_id: str, project_id: str, actor_id: str = "",
                 manifest_path: str | Path | None = None, **kwargs: Any) -> None:
        super().__init__(run_id, project_id, actor_id, **kwargs)
        self._manifest_path = Path(manifest_path) if manifest_path else _MANIFEST_PATH
        self._manifest: DomainPackManifest | None = None
        self._loader = DomainPackLoader()

    def get_manifest(self) -> DomainPackManifest:
        """Return the PD domain pack manifest."""
        if self._manifest is None:
            self._manifest = self._loader.load("pd", self._manifest_path)
        return self._manifest

    def compute_stage(self, stage_id: str, inputs: dict[str, Any]) -> StageComputeResult:
        """Execute PD domain computation.

        Args:
            stage_id: Stage to compute.
            inputs: Stage inputs.

        Returns:
            :class:~platform_core.domain.base_domain_sdk.StageComputeResult.
        """
        if stage_id == "data_preparation":
            return StageComputeResult(
                stage_id=stage_id, success=True,
                artifacts={"dataset_snapshot": {"snapshot_id": str(uuid.uuid4())}},
            )
        if stage_id == "model_development":
            candidates = inputs.get("candidates", [])
            return StageComputeResult(
                stage_id=stage_id, success=True,
                artifacts={"model_candidate_set": candidates},
                candidates=candidates,
            )
        return StageComputeResult(stage_id=stage_id, success=True,
                                   metadata={"note": f"Stage '{stage_id}' is a review/governance stage."})
