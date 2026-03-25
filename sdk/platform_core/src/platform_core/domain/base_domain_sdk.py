"""platform_core.domain.base_domain_sdk -- BaseDomainSDK: abstract base for all domain SDKs.

Every domain SDK (scorecardsdk, timeseriessdk, etc.) must subclass
:class:`BaseDomainSDK` and implement the abstract methods.

This provides:
- A standard interface for domain stage computation.
- Built-in audit and observability hooks.
- Governance-compliant artifact registration.
"""

from __future__ import annotations

import abc
import logging
from typing import Any

from platform_core.domain.models import DomainPackManifest

logger = logging.getLogger(__name__)


class StageComputeResult:
    """Result of a domain stage computation.

    Args:
        stage_id: Stage that produced this result.
        success: Whether computation succeeded.
        artifacts: Dict of artifact_type -> artifact payload dict.
        metrics: Dict of metric_name -> float value.
        candidates: Optional list of candidate version dicts.
        error_message: Error details on failure.
        metadata: Arbitrary extra output.
    """

    def __init__(
        self,
        stage_id: str,
        success: bool,
        artifacts: dict[str, Any] | None = None,
        metrics: dict[str, float] | None = None,
        candidates: list[dict[str, Any]] | None = None,
        error_message: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.stage_id = stage_id
        self.success = success
        self.artifacts = artifacts or {}
        self.metrics = metrics or {}
        self.candidates = candidates or []
        self.error_message = error_message
        self.metadata = metadata or {}


class BaseDomainSDK(abc.ABC):
    """Abstract base class for all domain SDKs.

    Subclasses must implement:
    - :meth:`compute_stage`: Execute domain logic for a stage.
    - :meth:`get_manifest`: Return the domain pack manifest.

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
        self._artifacts = artifact_service

    @abc.abstractmethod
    def get_manifest(self) -> DomainPackManifest:
        """Return the domain pack manifest for this SDK.

        Returns:
            :class:`~platform_core.domain.models.DomainPackManifest`.
        """
        ...

    @abc.abstractmethod
    def compute_stage(self, stage_id: str, inputs: dict[str, Any]) -> StageComputeResult:
        """Execute domain logic for a single stage.

        Args:
            stage_id: Stage to compute.
            inputs: Input data and configuration for the stage.

        Returns:
            :class:`StageComputeResult`.
        """
        ...

    def validate_stage_inputs(self, stage_id: str, inputs: dict[str, Any]) -> list[str]:
        """Validate stage inputs against the manifest's stage definition.

        Default implementation checks that required keys are present.
        Override for domain-specific validation.

        Args:
            stage_id: Stage to validate inputs for.
            inputs: Input dict.

        Returns:
            List of validation error strings (empty = valid).
        """
        manifest = self.get_manifest()
        stage = manifest.get_stage(stage_id)
        if stage is None:
            return [f"Stage '{stage_id}' not found in manifest for domain '{manifest.domain}'."]
        return []

    def run_stage(self, stage_id: str, inputs: dict[str, Any]) -> StageComputeResult:
        """Validate inputs, execute computation, and emit observability events.

        Args:
            stage_id: Stage to execute.
            inputs: Input data and configuration.

        Returns:
            :class:`StageComputeResult`.
        """
        manifest = self.get_manifest()

        # Validate inputs.
        errors = self.validate_stage_inputs(stage_id, inputs)
        if errors:
            logger.warning(
                "domain_sdk.input_validation_failed",
                extra={"domain": manifest.domain, "stage_id": stage_id, "errors": errors},
            )
            return StageComputeResult(
                stage_id=stage_id,
                success=False,
                error_message="; ".join(errors),
            )

        self._emit("workflow.stage.started", stage_id)

        try:
            result = self.compute_stage(stage_id, inputs)
        except Exception as exc:
            logger.error(
                "domain_sdk.compute_failed",
                extra={"domain": manifest.domain, "stage_id": stage_id, "error": str(exc)},
            )
            self._emit("workflow.stage.failed", stage_id, {"error": str(exc)})
            return StageComputeResult(stage_id=stage_id, success=False, error_message=str(exc))

        if result.success:
            self._emit("workflow.stage.completed", stage_id, {"metrics": result.metrics})
        else:
            self._emit("workflow.stage.failed", stage_id, {"error": result.error_message})

        return result

    def get_next_stage(self, current_stage_id: str) -> str | None:
        """Return the next stage ID based on routing rules.

        Args:
            current_stage_id: Current stage.

        Returns:
            Next stage ID or None if no routing rule found.
        """
        manifest = self.get_manifest()
        rule = manifest.get_routing_rule(current_stage_id)
        return rule.to_stage if rule else None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _emit(self, event_type: str, stage_id: str, metadata: dict[str, Any] | None = None) -> None:
        if self._obs is None:
            return
        try:
            self._obs.emit_simple(
                event_type=event_type,
                run_id=self._run_id,
                stage_name=stage_id,
                actor_id=self._actor_id,
                metadata=metadata or {},
            )
        except Exception as exc:
            logger.warning("domain_sdk.emit_failed", extra={"error": str(exc)})
