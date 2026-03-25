"""RecoveryOrchestrator — failure inspection and recovery recommendation.

Responsibilities:
1. Inspect the current run's failure state from workflowsdk.
2. Derive a recovery recommendation (retry / rerun / rollback / skip).
3. Optionally apply the recommendation via the RecoveryController.
4. Emit an observability event and audit record for the recovery action.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class RecoveryRecommendation:
    """Structured recovery recommendation.

    Attributes:
        recommended_path: Recommended recovery path string.
        confidence: Score 0.0–1.0 indicating recommendation confidence.
        rationale: Human-readable explanation of the recommendation.
        alternative_paths: Other valid recovery paths.
        requires_manual_review: Whether a manual review is strongly advised.
    """

    recommended_path: str
    confidence: float = 1.0
    rationale: str = ""
    alternative_paths: List[str] = field(default_factory=list)
    requires_manual_review: bool = False


@dataclass
class RecoveryResult:
    """Result of the recovery orchestrator run.

    Attributes:
        success: True if recovery was successfully applied.
        recommendation: Recovery recommendation that was provided.
        applied: True if the recommendation was applied.
        restored_stage: Stage restored to after recovery.
        error: Error message if not successful.
        event_ref: Observability event reference.
        audit_ref: Audit record reference.
    """

    success: bool
    recommendation: Optional[RecoveryRecommendation] = None
    applied: bool = False
    restored_stage: str = ""
    error: str = ""
    event_ref: Optional[str] = None
    audit_ref: Optional[str] = None


class RecoveryOrchestrator:
    """Orchestrates failure inspection and recovery.

    Args:
        bridge: :class:`AgentBridge` or :class:`JupyterBridge`.
    """

    _RETRY_CONFIDENCE_THRESHOLD = 0.7

    def __init__(self, bridge: Any) -> None:
        self._bridge = bridge

    def inspect_and_recommend(
        self,
        *,
        run_id: str,
        project_id: str,
        actor_id: str,
        actor_role: str,
        stage_name: str,
        session_id: Optional[str] = None,
        failure_detail: Optional[str] = None,
    ) -> RecoveryRecommendation:
        """Inspect failure state and return a recovery recommendation.

        Queries workflowsdk via the bridge's get_recovery_options action.

        Args:
            run_id: Active run identifier.
            project_id: Active project identifier.
            actor_id: Actor identifier.
            actor_role: Actor role string.
            stage_name: Stage that failed.
            session_id: Active session identifier.
            failure_detail: Human-readable failure description.

        Returns:
            :class:`RecoveryRecommendation`.
        """
        resp = self._bridge.dispatch({
            "tool_name": "platform_get_recovery_options",
            "args": {
                "stage_name": stage_name,
                "run_id": run_id,
                "project_id": project_id,
                "actor_id": actor_id,
                "actor_role": actor_role,
                "session_id": session_id,
            },
        })

        recommendation_data = (resp.get("data") or {}).get("recommendation") or {}
        resume_validation = (resp.get("data") or {}).get("resume_validation") or {}

        # Derive recommendation from workflow state.
        path = self._derive_path(
            recommendation_data=recommendation_data,
            resume_validation=resume_validation,
            failure_detail=failure_detail,
        )

        return RecoveryRecommendation(
            recommended_path=path,
            confidence=self._estimate_confidence(path, resume_validation),
            rationale=self._build_rationale(path, failure_detail),
            alternative_paths=self._alternatives(path),
            requires_manual_review=(
                recommendation_data.get("requires_review") is True
                or resume_validation.get("requires_review") is True
            ),
        )

    def apply_recovery(
        self,
        *,
        run_id: str,
        project_id: str,
        actor_id: str,
        actor_role: str,
        stage_name: str,
        session_id: Optional[str] = None,
        recovery_path: Optional[str] = None,
        auto_apply: bool = False,
    ) -> RecoveryResult:
        """Inspect failure and optionally apply the recommended recovery.

        Args:
            run_id: Active run identifier.
            project_id: Active project identifier.
            actor_id: Actor identifier.
            actor_role: Actor role string.
            stage_name: Stage that failed.
            session_id: Active session identifier.
            recovery_path: Explicit recovery path (or None to use recommendation).
            auto_apply: If True, apply the recommendation automatically.

        Returns:
            :class:`RecoveryResult`.
        """
        recommendation = self.inspect_and_recommend(
            run_id=run_id,
            project_id=project_id,
            actor_id=actor_id,
            actor_role=actor_role,
            stage_name=stage_name,
            session_id=session_id,
        )

        path_to_apply = recovery_path or recommendation.recommended_path

        should_apply = (
            auto_apply
            and not recommendation.requires_manual_review
            and recommendation.confidence >= self._RETRY_CONFIDENCE_THRESHOLD
        ) or bool(recovery_path)

        if not should_apply:
            return RecoveryResult(
                success=True,
                recommendation=recommendation,
                applied=False,
            )

        resp = self._bridge.dispatch({
            "tool_name": "platform_apply_recovery",
            "args": {
                "stage_name": stage_name,
                "run_id": run_id,
                "project_id": project_id,
                "actor_id": actor_id,
                "actor_role": actor_role,
                "session_id": session_id,
                "parameters": {"recovery_path": path_to_apply},
            },
        })

        if resp.get("status") not in ("success", "ok"):
            return RecoveryResult(
                success=False,
                recommendation=recommendation,
                applied=False,
                error=resp.get("message", "Recovery application failed."),
                event_ref=resp.get("event_ref"),
                audit_ref=resp.get("audit_ref"),
            )

        restored_stage = (resp.get("data") or {}).get("restored_stage") or stage_name
        logger.info(
            "recovery_orchestrator.applied",
            extra={
                "run_id": run_id,
                "path": path_to_apply,
                "restored_stage": restored_stage,
            },
        )

        return RecoveryResult(
            success=True,
            recommendation=recommendation,
            applied=True,
            restored_stage=restored_stage,
            event_ref=resp.get("event_ref"),
            audit_ref=resp.get("audit_ref"),
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _derive_path(
        self,
        recommendation_data: Dict[str, Any],
        resume_validation: Dict[str, Any],
        failure_detail: Optional[str],
    ) -> str:
        """Derive the best recovery path from available data.

        Priority: recommendation from workflowsdk > resume validation > default retry.
        """
        if recommendation_data.get("path"):
            return recommendation_data["path"]
        if resume_validation.get("can_resume"):
            return "retry"
        return "retry"

    def _estimate_confidence(self, path: str, resume_validation: Dict[str, Any]) -> float:
        if path == "retry" and resume_validation.get("can_resume"):
            return 0.9
        if path == "retry":
            return 0.6
        if path in ("rerun", "rollback"):
            return 0.8
        return 0.5

    def _build_rationale(self, path: str, failure_detail: Optional[str]) -> str:
        base = {
            "retry": "Resume from the last checkpoint. Safe for idempotent stages.",
            "rerun": "Re-run the stage from scratch. Use when checkpoint is corrupted.",
            "rollback": "Roll back to the previous stable stage and re-execute.",
            "skip": "Skip this stage. Only safe for non-critical optional stages.",
        }.get(path, "Apply the selected recovery path.")
        if failure_detail:
            return f"{base} Failure detail: {failure_detail}"
        return base

    def _alternatives(self, path: str) -> List[str]:
        all_paths = ["retry", "rerun", "rollback", "skip"]
        return [p for p in all_paths if p != path]
