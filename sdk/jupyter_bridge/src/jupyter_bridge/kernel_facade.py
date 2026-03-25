"""JupyterKernelFacade -- single object exposed in notebooks.

Provides a convenience API that notebook users call directly::

    from jupyter_bridge import kernel_facade as mdlc

    mdlc.setup(bundle, container)

    # Start a workflow run
    state = mdlc.open_session(project_id="proj_01", run_id="run_abc", actor_id="ds@example.com", role="modeller")
    mdlc.start_stage("data_preparation")
    mdlc.show_state()

The facade delegates to :class:`~agent_bridge.dispatcher.AgentDispatcher` under
the hood, ensuring identical governance semantics in both Jupyter and agent modes.
"""

from __future__ import annotations

import logging
from typing import Any

from platform_contracts.enums import InteractionType
from platform_contracts.fragments import ActorRecord
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.utils.dependency_container import DependencyContainer
from platform_core.utils.id_factory import IDFactory, id_factory as _default_id_factory
from platform_core.utils.time_provider import TimeProvider, time_provider as _default_tp

logger = logging.getLogger(__name__)

try:
    from agent_bridge.dispatcher import AgentDispatcher
    from platform_core.controllers.factory import ControllerFactory
    _DISPATCHER_AVAILABLE = True
except ImportError:
    _DISPATCHER_AVAILABLE = False


class JupyterKernelFacade:
    """Notebook-friendly MDLC client.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        container: :class:`DependencyContainer` with all services.
        id_factory_: Injectable :class:`IDFactory`.
        time_provider_: Injectable :class:`TimeProvider`.
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        container: DependencyContainer,
        id_factory_: IDFactory | None = None,
        time_provider_: TimeProvider | None = None,
    ) -> None:
        self._bundle = bundle
        self._container = container
        self._id_factory = id_factory_ or _default_id_factory
        self._tp = time_provider_ or _default_tp
        self._dispatcher: Any = None
        self._session_id: str = ""
        self._run_id: str = ""
        self._project_id: str = ""
        self._actor: ActorRecord | None = None
        self._trace_id: str = ""

        if _DISPATCHER_AVAILABLE:
            factory = ControllerFactory(bundle, container, id_factory_=id_factory_, time_provider_=time_provider_)
            self._dispatcher = AgentDispatcher(factory)

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def open_session(
        self,
        project_id: str,
        run_id: str,
        actor_id: str,
        role: str,
        domain: str = "generic",
    ) -> dict[str, Any]:
        """Open a new MDLC session.

        Args:
            project_id: Project identifier.
            run_id: Run identifier (leave blank to auto-generate).
            actor_id: User/actor identifier.
            role: Actor's MDLC role.
            domain: Domain name (default ``"generic"``).

        Returns:
            Serialised ``StandardResponseEnvelope`` dict.
        """
        self._project_id = project_id
        self._run_id = run_id or self._id_factory.run_id(project_id)
        self._trace_id = self._id_factory.audit_id("trace")
        self._actor = ActorRecord(actor_id=actor_id, role=role)
        return self._dispatch("open_session", "bootstrap", InteractionType.SESSION_COMMAND, {
            "domain": domain,
        })

    def resume_session(self, session_id: str) -> dict[str, Any]:
        """Resume a suspended session.

        Args:
            session_id: Session identifier to resume.

        Returns:
            Serialised ``StandardResponseEnvelope`` dict.
        """
        self._session_id = session_id
        return self._dispatch("resume_session", "bootstrap", InteractionType.SESSION_COMMAND, {
            "session_id": session_id,
        })

    # ------------------------------------------------------------------
    # Workflow
    # ------------------------------------------------------------------

    def start_stage(self, stage_name: str) -> dict[str, Any]:
        """Transition workflow to ``stage_name``.

        Args:
            stage_name: Target MDLC stage.

        Returns:
            Serialised ``StandardResponseEnvelope`` dict.
        """
        return self._dispatch("start_stage", stage_name, InteractionType.STAGE_ACTION)

    def complete_stage(self, stage_name: str, artifact_ids: list[str] | None = None) -> dict[str, Any]:
        """Mark ``stage_name`` complete.

        Args:
            stage_name: Stage to mark complete.
            artifact_ids: Optional list of produced artifact IDs.

        Returns:
            Serialised ``StandardResponseEnvelope`` dict.
        """
        return self._dispatch("complete_stage", stage_name, InteractionType.STAGE_ACTION, {
            "artifact_ids": artifact_ids or [],
        })

    def route_next(self) -> dict[str, Any]:
        """Ask the routing engine for the next stage.

        Returns:
            Serialised ``StandardResponseEnvelope`` dict.
        """
        return self._dispatch("route_next", "", InteractionType.STAGE_ACTION)

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def show_state(self) -> None:
        """Print / display the current workflow state."""
        from jupyter_bridge.display import show_workflow_state
        ws = self._container.get("workflow_service")
        result = ws.get_state(self._run_id)
        show_workflow_state(result.data if result.success else None)

    def show_response(self, response: dict[str, Any]) -> None:
        """Pretty-print a response envelope dict.

        Args:
            response: Dict returned by any facade method.
        """
        from jupyter_bridge.display import show_response_envelope
        show_response_envelope(response)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _dispatch(
        self,
        action: str,
        stage_name: str,
        interaction_type: InteractionType,
        extra_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self._dispatcher is None:
            return {"status": "failed", "message": "Dispatcher not available (missing agent_bridge dependency)."}

        if self._actor is None:
            return {"status": "failed", "message": "Call open_session() before any other method."}

        payload: dict[str, Any] = {
            "project_id": self._project_id,
            "run_id": self._run_id,
            "session_id": self._session_id,
            "trace_id": self._trace_id,
            "correlation_id": self._id_factory.audit_id("corr"),
            "actor": self._actor.model_dump(),
            "timestamp": self._tp.now().isoformat(),
            "stage_name": stage_name,
            "interaction_type": interaction_type.value,
            "action": action,
            "data": extra_data or {},
        }

        response = self._dispatcher.dispatch(payload)
        if response.get("session_id"):
            self._session_id = response["session_id"]
        return response
