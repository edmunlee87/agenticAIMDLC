"""RecoveryOrchestratorSkill -- auto-surfaces recovery options on workflow failure.

Responsibilities:
1. Fetch recovery recommendations from the workflow service.
2. Select the recommended path (or accept a manually specified override).
3. Apply the recovery.
4. Return a :class:`RecoveryOutcome` with the restored stage.

Usage::

    from skills.platform.recovery_orchestrator.skill import RecoveryOrchestratorSkill, RecoveryRequest

    skill = RecoveryOrchestratorSkill(dispatcher, request)
    outcome = skill.run()
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from platform_contracts.enums import InteractionType

logger = logging.getLogger(__name__)


@dataclass
class RecoveryRequest:
    """Inputs for the recovery orchestrator.

    Attributes:
        project_id: MDLC project identifier.
        run_id: Run that has failed.
        actor_id: Actor requesting recovery.
        role: Actor's MDLC role.
        stage_name: Stage where failure occurred.
        session_id: Active session ID.
        override_path: Explicit recovery path (overrides recommendation).
            Must be a :class:`~workflowsdk.models.RecoveryPath` value string.
    """

    project_id: str
    run_id: str
    actor_id: str
    role: str
    stage_name: str
    session_id: str = ""
    override_path: str = ""


@dataclass
class RecoveryOutcome:
    """Result of a recovery orchestration.

    Attributes:
        success: True if recovery applied.
        applied_path: Recovery path that was applied.
        restored_stage: Stage the workflow is restored to.
        error: Error message if unsuccessful.
    """

    success: bool
    applied_path: str = ""
    restored_stage: str = ""
    error: str = ""


class RecoveryOrchestratorSkill:
    """Drives the recovery flow for a failed run.

    Args:
        dispatcher: :class:`~agent_bridge.dispatcher.AgentDispatcher`.
        request: :class:`RecoveryRequest`.
    """

    def __init__(self, dispatcher: Any, request: RecoveryRequest) -> None:
        self._dispatcher = dispatcher
        self._request = request

    def run(self) -> RecoveryOutcome:
        """Fetch options, choose a path, and apply recovery.

        Returns:
            :class:`RecoveryOutcome`.
        """
        # 1. Get recovery options.
        opts_resp = self._dispatch(
            "get_recovery_options",
            InteractionType.RECOVERY_CHOICE,
        )
        if opts_resp.get("status") != "ok":
            return RecoveryOutcome(
                success=False,
                error=opts_resp.get("message", "get_recovery_options failed."),
            )

        recommendation = (opts_resp.get("data") or {}).get("recommendation", "retry")
        chosen_path = self._request.override_path or (
            recommendation if isinstance(recommendation, str) else "retry"
        )

        logger.info(
            "recovery_orchestrator.applying",
            extra={
                "run_id": self._request.run_id,
                "recommendation": recommendation,
                "chosen_path": chosen_path,
            },
        )

        # 2. Apply recovery.
        apply_resp = self._dispatch(
            "apply_recovery",
            InteractionType.RECOVERY_CHOICE,
            {"recovery_path": chosen_path},
        )
        if apply_resp.get("status") != "ok":
            return RecoveryOutcome(
                success=False,
                applied_path=chosen_path,
                error=apply_resp.get("message", "apply_recovery failed."),
            )

        data = apply_resp.get("data") or {}
        return RecoveryOutcome(
            success=True,
            applied_path=data.get("applied_path", chosen_path),
            restored_stage=data.get("restored_stage", ""),
        )

    # ------------------------------------------------------------------

    def _dispatch(
        self,
        action: str,
        interaction_type: InteractionType,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        from platform_contracts.fragments import ActorRecord
        from platform_core.utils.id_factory import id_factory
        from platform_core.utils.time_provider import time_provider

        payload = {
            "project_id": self._request.project_id,
            "run_id": self._request.run_id,
            "session_id": self._request.session_id,
            "trace_id": id_factory.audit_id("trace"),
            "correlation_id": id_factory.audit_id("corr"),
            "actor": ActorRecord(actor_id=self._request.actor_id, role=self._request.role).model_dump(),
            "timestamp": time_provider.now().isoformat(),
            "stage_name": self._request.stage_name,
            "interaction_type": interaction_type.value,
            "action": action,
            "data": data or {},
        }
        return self._dispatcher.dispatch(payload)
