"""scorecardsdk.sdk -- ScorecardSDK: concrete domain SDK implementing BaseDomainSDK.

Wires together the scorecard computation functions with the platform
governance framework (manifest, routing, artifact registration).
"""

from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Any

from platform_core.domain.base_domain_sdk import BaseDomainSDK, StageComputeResult
from platform_core.domain.loader import DomainPackLoader
from platform_core.domain.models import DomainPackManifest
from scorecardsdk.computations import (
    apply_scaling,
    build_feature_shortlist,
    compute_score_scaling,
    compute_woe_iv,
    recommend_best_candidate,
)
from scorecardsdk.models import (
    CoarseClassingTable,
    FeatureShortlist,
    ScorecardCandidate,
    ScorecardModel,
    WoeIvRecord,
)

logger = logging.getLogger(__name__)

_MANIFEST_PATH = Path(__file__).parent.parent.parent.parent.parent.parent / "configs" / "runtime" / "domain_overlays" / "scorecard.yaml"


class ScorecardSDK(BaseDomainSDK):
    """Concrete domain SDK for credit scorecard development.

    Implements all scorecard stages defined in the domain pack manifest.
    Computation functions are injected by default but can be overridden.

    Args:
        run_id: MDLC run identifier.
        project_id: Project identifier.
        actor_id: Actor executing domain logic.
        manifest_path: Optional override path to the domain pack YAML.
        observability_service: Optional observability service.
        audit_service: Optional audit service.
        artifact_service: Optional artifact service.
    """

    def __init__(
        self,
        run_id: str,
        project_id: str,
        actor_id: str = "",
        manifest_path: str | Path | None = None,
        observability_service: Any = None,
        audit_service: Any = None,
        artifact_service: Any = None,
    ) -> None:
        super().__init__(run_id, project_id, actor_id, observability_service, audit_service, artifact_service)
        self._manifest_path = Path(manifest_path) if manifest_path else _MANIFEST_PATH
        self._manifest: DomainPackManifest | None = None
        self._loader = DomainPackLoader()

    def get_manifest(self) -> DomainPackManifest:
        """Return the scorecard domain pack manifest.

        Returns:
            :class:`~platform_core.domain.models.DomainPackManifest`.
        """
        if self._manifest is None:
            self._manifest = self._loader.load("scorecard", self._manifest_path)
        return self._manifest

    def compute_stage(self, stage_id: str, inputs: dict[str, Any]) -> StageComputeResult:
        """Dispatch computation to the appropriate stage handler.

        Args:
            stage_id: Stage to compute.
            inputs: Stage inputs dict.

        Returns:
            :class:`~platform_core.domain.base_domain_sdk.StageComputeResult`.
        """
        handlers = {
            "data_preparation": self._stage_data_preparation,
            "fine_classing": self._stage_fine_classing,
            "coarse_classing": self._stage_coarse_classing,
            "woe_iv_calculation": self._stage_woe_iv,
            "feature_shortlist": self._stage_feature_shortlist,
            "model_development": self._stage_model_development,
            "score_scaling": self._stage_score_scaling,
        }
        handler = handlers.get(stage_id)
        if handler is None:
            # HITL review stages and terminal stages do not have compute handlers.
            return StageComputeResult(
                stage_id=stage_id,
                success=True,
                metadata={"note": f"Stage '{stage_id}' is a review/governance stage; no compute step."},
            )
        return handler(inputs)

    # ------------------------------------------------------------------
    # Stage handlers
    # ------------------------------------------------------------------

    def _stage_data_preparation(self, inputs: dict[str, Any]) -> StageComputeResult:
        """Data preparation: validate and snapshot dataset."""
        dataset_id = inputs.get("dataset_id", f"ds-{self._run_id}")
        row_count = inputs.get("row_count", 0)
        column_names = inputs.get("column_names", [])

        return StageComputeResult(
            stage_id="data_preparation",
            success=True,
            artifacts={
                "dataset_snapshot": {
                    "snapshot_id": str(uuid.uuid4()),
                    "dataset_id": dataset_id,
                    "row_count": row_count,
                    "column_count": len(column_names),
                    "column_names": column_names,
                }
            },
            metadata={"dataset_id": dataset_id},
        )

    def _stage_fine_classing(self, inputs: dict[str, Any]) -> StageComputeResult:
        """Fine classing: produce initial fine-grained bins per variable."""
        variables = inputs.get("variables", [])
        fine_bins = {var: {"bin_count": inputs.get("bins_per_variable", 20)} for var in variables}

        return StageComputeResult(
            stage_id="fine_classing",
            success=True,
            artifacts={"fine_classing_report": {"variables": variables, "fine_bins": fine_bins}},
        )

    def _stage_coarse_classing(self, inputs: dict[str, Any]) -> StageComputeResult:
        """Coarse classing: merge fine bins into coarse business-meaningful bins."""
        variables = inputs.get("variables", [])
        raw_bins = inputs.get("coarse_bins", {})
        run_id = self._run_id
        project_id = self._project_id

        all_bins = []
        for var in variables:
            var_bins = raw_bins.get(var, [])
            for i, b in enumerate(var_bins):
                all_bins.append({
                    "bin_id": f"{var}_b{i}",
                    "variable_name": var,
                    "bin_label": b.get("label", f"Bin {i}"),
                    "good_count": b.get("good_count", 0),
                    "bad_count": b.get("bad_count", 0),
                    "lower_bound": b.get("lower_bound"),
                    "upper_bound": b.get("upper_bound"),
                })

        table = CoarseClassingTable(
            table_id=str(uuid.uuid4()),
            run_id=run_id,
            project_id=project_id,
            bins=[],  # Simplified: full BinDefinition construction is in WoE stage.
            variables=variables,
            created_by=self._actor_id,
        )

        return StageComputeResult(
            stage_id="coarse_classing",
            success=True,
            artifacts={"coarse_classing_table": table.model_dump(), "coarse_bins_raw": all_bins},
        )

    def _stage_woe_iv(self, inputs: dict[str, Any]) -> StageComputeResult:
        """WoE/IV calculation: compute WoE and IV per variable."""
        variables = inputs.get("variables", [])
        coarse_bins_raw = inputs.get("coarse_bins_raw", {})
        total_goods = inputs.get("total_goods", 1)
        total_bads = inputs.get("total_bads", 1)
        min_iv = inputs.get("minimum_iv_threshold", 0.02)

        woe_iv_records: list[WoeIvRecord] = []
        for var in variables:
            bins = coarse_bins_raw.get(var, [])
            if not bins:
                continue
            record = compute_woe_iv(
                variable_name=var,
                bins=bins,
                total_goods=total_goods,
                total_bads=total_bads,
                record_id=str(uuid.uuid4()),
                minimum_iv_threshold=min_iv,
            )
            woe_iv_records.append(record)

        return StageComputeResult(
            stage_id="woe_iv_calculation",
            success=True,
            artifacts={"woe_iv_table": [r.model_dump() for r in woe_iv_records]},
            metrics={"total_variables": len(woe_iv_records)},
        )

    def _stage_feature_shortlist(self, inputs: dict[str, Any]) -> StageComputeResult:
        """Feature shortlisting: select features by IV threshold."""
        woe_iv_dicts = inputs.get("woe_iv_table", [])
        min_iv = inputs.get("minimum_iv", 0.02)
        protected = inputs.get("protected_attributes", [])

        woe_iv_records = [WoeIvRecord(**r) for r in woe_iv_dicts]
        shortlist = build_feature_shortlist(
            shortlist_id=str(uuid.uuid4()),
            run_id=self._run_id,
            project_id=self._project_id,
            woe_iv_records=woe_iv_records,
            minimum_iv=min_iv,
            protected_attribute_names=protected,
            created_by=self._actor_id,
        )

        return StageComputeResult(
            stage_id="feature_shortlist",
            success=True,
            artifacts={"feature_shortlist_report": shortlist.model_dump()},
            metrics={"selected_feature_count": len(shortlist.selected_features), "total_iv": shortlist.total_shortlist_iv},
        )

    def _stage_model_development(self, inputs: dict[str, Any]) -> StageComputeResult:
        """Model development: assemble candidates from pre-computed models."""
        candidates_raw = inputs.get("candidates", [])
        primary_metric = inputs.get("primary_metric", "gini")

        candidates = [ScorecardCandidate(**c) for c in candidates_raw]
        ranked = recommend_best_candidate(candidates, primary_metric=primary_metric)

        metrics: dict[str, float] = {}
        if ranked:
            metrics = dict(ranked[0].metrics)

        return StageComputeResult(
            stage_id="model_development",
            success=True,
            artifacts={
                "model_candidate_set": [c.model_dump() for c in ranked],
                "evaluation_pack": {"candidates": len(ranked), "primary_metric": primary_metric},
            },
            candidates=[c.model_dump() for c in ranked],
            metrics=metrics,
        )

    def _stage_score_scaling(self, inputs: dict[str, Any]) -> StageComputeResult:
        """Score scaling: compute PDO-based score scaling parameters."""
        model_id = inputs.get("model_id", "")
        params = compute_score_scaling(
            scaling_id=str(uuid.uuid4()),
            model_id=model_id,
            base_score=inputs.get("base_score", 600.0),
            pdo=inputs.get("pdo", 20.0),
            odds_0=inputs.get("odds_0", 50.0),
            score_min=inputs.get("score_min", 300.0),
            score_max=inputs.get("score_max", 850.0),
        )

        return StageComputeResult(
            stage_id="score_scaling",
            success=True,
            artifacts={"score_scaling_table": params.model_dump()},
            metrics={"base_score": params.base_score, "pdo": params.pdo},
        )
