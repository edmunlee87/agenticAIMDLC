"""platform_core.domain.base_domain_sdk -- abstract base class for domain SDKs.

All domain-specific SDK implementations (scorecardsdk, time_series, etc.) must
subclass :class:`BaseDomainSDK` and implement :meth:`get_manifest` and
:meth:`compute_stage`.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from platform_core.domain.models import DomainPackManifest, RouteCondition


class StageComputeResult(BaseModel):
    """Result of a single stage computation.

    Args:
        stage_id: Stage that was computed.
        success: Whether computation succeeded.
        artifacts: Produced artifacts keyed by artifact type.
        metrics: Numeric metrics produced by this stage.
        candidates: List of candidate model dicts (model selection stages only).
        metadata: Arbitrary metadata.
        error: Error message if ``success=False``.
    """

    model_config = ConfigDict(frozen=True)

    stage_id: str
    success: bool = True
    artifacts: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, float] = Field(default_factory=dict)
    candidates: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: str = ""


class BaseDomainSDK(ABC):
    """Abstract base class for domain-specific SDK implementations.

    Subclasses must implement :meth:`get_manifest` and :meth:`compute_stage`.
    All other convenience methods delegate to the manifest.

    Args:
        run_id: MDLC run identifier.
        project_id: Project identifier.
        actor_id: Actor executing domain logic.
        observability_service: Optional observability service.
        audit_service: Optional audit service.
        artifact_service: Optional artifact service.
    """

    def __init__(
        self,
        run_id: str,
        project_id: str,
        actor_id: str = "",
        observability_service: Any = None,
        audit_service: Any = None,
        artifact_service: Any = None,
    ) -> None:
        self._run_id = run_id
        self._project_id = project_id
        self._actor_id = actor_id
        self._obs = observability_service
        self._audit = audit_service
        self._artifact = artifact_service
        self._logger = logging.getLogger(self.__class__.__module__ + "." + self.__class__.__name__)

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    def get_manifest(self) -> DomainPackManifest:
        """Return the domain pack manifest.

        Returns:
            :class:`~platform_core.domain.models.DomainPackManifest`.
        """

    @abstractmethod
    def compute_stage(self, stage_id: str, inputs: dict[str, Any]) -> StageComputeResult:
        """Dispatch computation to the appropriate stage handler.

        Args:
            stage_id: Stage identifier.
            inputs: Stage input dict.

        Returns:
            :class:`StageComputeResult`.
        """

    # ------------------------------------------------------------------
    # Convenience façade (delegating to manifest)
    # ------------------------------------------------------------------

    def run_stage(self, stage_id: str, inputs: dict[str, Any]) -> StageComputeResult:
        """Run a stage with structured logging and error handling.

        Args:
            stage_id: Stage identifier.
            inputs: Stage inputs.

        Returns:
            :class:`StageComputeResult`.
        """
        self._logger.info(
            "domain_sdk.run_stage",
            extra={"run_id": self._run_id, "stage_id": stage_id},
        )
        try:
            result = self.compute_stage(stage_id, inputs)
        except Exception as exc:
            self._logger.exception("domain_sdk.run_stage.failed", extra={"stage_id": stage_id, "error": str(exc)})
            result = StageComputeResult(stage_id=stage_id, success=False, error=str(exc))
        return result

    def get_next_stage(self, from_stage: str) -> str | None:
        """Return the next stage on success routing.

        Args:
            from_stage: Source stage ID.

        Returns:
            Target stage ID or None.
        """
        return self.get_manifest().get_next_stage(from_stage)

    def get_hitl_stages(self) -> list[str]:
        """Return HITL stage IDs from the manifest.

        Returns:
            List of stage ID strings.
        """
        return self.get_manifest().hitl_stages

    def get_governance_gates(self) -> list[str]:
        """Return governance gate stage IDs from the manifest.

        Returns:
            List of stage ID strings.
        """
        return self.get_manifest().governance_gate_stages

    def health_check(self) -> dict[str, Any]:
        """Return domain SDK health status.

        Returns:
            Health dict with ``status`` and ``domain``.
        """
        manifest = self.get_manifest()
        return {
            "status": "ok",
            "domain": manifest.domain,
            "stage_count": len(manifest.stage_registry),
            "run_id": self._run_id,
        }
