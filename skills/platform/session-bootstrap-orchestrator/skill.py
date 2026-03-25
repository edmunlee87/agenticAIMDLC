"""SessionBootstrapOrchestrator — project discovery and session bootstrapping.

Responsibilities:
1. Inspect the registry for an existing project/run to resume.
2. If an existing session exists, prompt for resumption.
3. If no session exists, open a fresh project+run+session.
4. Return the active session context for downstream orchestrators.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class BootstrapContext:
    """Context established during session bootstrap.

    Attributes:
        project_id: Active project identifier.
        run_id: Active run identifier.
        session_id: Active session identifier.
        stage_name: Current stage to start from.
        actor_id: Actor identifier.
        actor_role: Actor role.
        is_resumed: True if this is a resumed session (vs. new).
        metadata: Additional bootstrap metadata.
    """

    project_id: str
    run_id: str
    session_id: str
    stage_name: str
    actor_id: str
    actor_role: str
    is_resumed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BootstrapResult:
    """Result of the bootstrap orchestrator.

    Attributes:
        success: True if bootstrap succeeded.
        context: Established session context.
        error: Error message if not successful.
        resume_prompt: Human-readable message describing the resume choice.
    """

    success: bool
    context: Optional[BootstrapContext] = None
    error: str = ""
    resume_prompt: str = ""


class SessionBootstrapOrchestrator:
    """Orchestrates project/session bootstrap with auto-discovery and resume.

    Args:
        bridge: :class:`AgentBridge` or :class:`JupyterBridge`.
        registry_service: Optional registry service for project/run lookup.
    """

    def __init__(
        self,
        bridge: Any,
        registry_service: Optional[Any] = None,
    ) -> None:
        self._bridge = bridge
        self._registry = registry_service

    def bootstrap(
        self,
        *,
        actor_id: str,
        actor_role: str,
        project_id: Optional[str] = None,
        run_id: Optional[str] = None,
        session_id: Optional[str] = None,
        initial_stage: str = "data_preparation",
        force_new: bool = False,
    ) -> BootstrapResult:
        """Bootstrap a session: discover existing or open new.

        If ``session_id`` is provided and ``force_new=False``, attempts
        to resume the existing session. Otherwise opens a new session.

        Args:
            actor_id: Actor's unique identifier.
            actor_role: Actor's role string.
            project_id: Optional project ID (generated if absent).
            run_id: Optional run ID (generated if absent).
            session_id: Optional existing session to resume.
            initial_stage: Starting stage for new sessions.
            force_new: Force open a new session even if one exists.

        Returns:
            :class:`BootstrapResult`.
        """
        from sdk.platform_core.schemas.utilities import IDFactory

        effective_run_id = run_id or IDFactory.run_id()
        effective_project_id = project_id or IDFactory.correlation_id()

        # Try resume path.
        if session_id and not force_new:
            return self._try_resume(
                session_id=session_id,
                run_id=effective_run_id,
                project_id=effective_project_id,
                actor_id=actor_id,
                actor_role=actor_role,
                stage_name=initial_stage,
            )

        # Auto-discover from registry.
        if self._registry and not force_new and run_id:
            discovered = self._discover_session(run_id=effective_run_id)
            if discovered:
                return self._try_resume(
                    session_id=discovered,
                    run_id=effective_run_id,
                    project_id=effective_project_id,
                    actor_id=actor_id,
                    actor_role=actor_role,
                    stage_name=initial_stage,
                )

        # Open fresh session.
        return self._open_new_session(
            run_id=effective_run_id,
            project_id=effective_project_id,
            actor_id=actor_id,
            actor_role=actor_role,
            stage_name=initial_stage,
        )

    def _try_resume(
        self,
        *,
        session_id: str,
        run_id: str,
        project_id: str,
        actor_id: str,
        actor_role: str,
        stage_name: str,
    ) -> BootstrapResult:
        resp = self._bridge.dispatch({
            "tool_name": "platform_resume_session",
            "args": {
                "stage_name": stage_name,
                "run_id": run_id,
                "project_id": project_id,
                "actor_id": actor_id,
                "actor_role": actor_role,
                "parameters": {"session_id": session_id},
            },
        })
        if resp.get("status") not in ("success", "ok"):
            logger.warning(
                "session_bootstrap.resume_failed",
                extra={"session_id": session_id, "error": resp.get("message")},
            )
            # Fall back to fresh session.
            return self._open_new_session(
                run_id=run_id,
                project_id=project_id,
                actor_id=actor_id,
                actor_role=actor_role,
                stage_name=stage_name,
            )

        effective_session_id = (
            (resp.get("data") or {}).get("session_id") or session_id
        )
        logger.info(
            "session_bootstrap.resumed",
            extra={"session_id": effective_session_id, "stage_name": stage_name},
        )
        return BootstrapResult(
            success=True,
            context=BootstrapContext(
                project_id=project_id,
                run_id=run_id,
                session_id=effective_session_id,
                stage_name=stage_name,
                actor_id=actor_id,
                actor_role=actor_role,
                is_resumed=True,
            ),
            resume_prompt=f"Resuming session '{effective_session_id}' at stage '{stage_name}'.",
        )

    def _open_new_session(
        self,
        *,
        run_id: str,
        project_id: str,
        actor_id: str,
        actor_role: str,
        stage_name: str,
    ) -> BootstrapResult:
        resp = self._bridge.dispatch({
            "tool_name": "platform_open_session",
            "args": {
                "stage_name": stage_name,
                "run_id": run_id,
                "project_id": project_id,
                "actor_id": actor_id,
                "actor_role": actor_role,
            },
        })
        if resp.get("status") not in ("success", "ok"):
            return BootstrapResult(
                success=False,
                error=resp.get("message", "Failed to open new session."),
            )

        new_session_id = (resp.get("data") or {}).get("session_id") or ""
        logger.info(
            "session_bootstrap.opened",
            extra={"session_id": new_session_id, "stage_name": stage_name},
        )
        return BootstrapResult(
            success=True,
            context=BootstrapContext(
                project_id=project_id,
                run_id=run_id,
                session_id=new_session_id,
                stage_name=stage_name,
                actor_id=actor_id,
                actor_role=actor_role,
                is_resumed=False,
            ),
        )

    def _discover_session(self, run_id: str) -> Optional[str]:
        """Attempt to find an existing open session for run_id in the registry.

        Args:
            run_id: Run identifier to search for.

        Returns:
            Session ID string if found, None otherwise.
        """
        try:
            result = self._registry.get_run(run_id=run_id)
            if result.is_success and result.data:
                return result.data.get("active_session_id")
        except Exception as exc:
            logger.debug("session_bootstrap.discovery_error: %s", exc)
        return None
