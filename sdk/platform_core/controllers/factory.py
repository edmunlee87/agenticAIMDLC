"""ControllerFactory — wires controllers from the dependency container.

Usage::

    from sdk.platform_core.controllers.factory import ControllerFactory

    factory = ControllerFactory(bundle=bundle, container=container)
    session_ctrl = factory.session()
    workflow_ctrl = factory.workflow()
    review_ctrl = factory.review()
    recovery_ctrl = factory.recovery()
"""

from __future__ import annotations

from typing import Any, Optional

from sdk.platform_core.controllers.recovery_controller import RecoveryController
from sdk.platform_core.controllers.review_controller import ReviewController
from sdk.platform_core.controllers.session_controller import SessionController
from sdk.platform_core.controllers.workflow_controller import WorkflowController
from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.resolvers.runtime_resolver import RuntimeResolver


class ControllerFactory:
    """Creates and caches controller instances.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        container: :class:`DependencyContainer` with registered services.
        environment: Deployment environment for governance strictness.
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        container: Any,
        environment: str = "dev",
    ) -> None:
        self._bundle = bundle
        self._container = container
        self._resolver = RuntimeResolver(bundle=bundle, environment=environment)
        self._session_ctrl: Optional[SessionController] = None
        self._workflow_ctrl: Optional[WorkflowController] = None
        self._review_ctrl: Optional[ReviewController] = None
        self._recovery_ctrl: Optional[RecoveryController] = None

    def session(self) -> SessionController:
        """Return (or create) the :class:`SessionController`.

        Returns:
            :class:`SessionController`.
        """
        if self._session_ctrl is None:
            self._session_ctrl = SessionController(
                workflow_service=self._container.get("workflow_service"),
                resolver=self._resolver,
                dependencies=self._container,
            )
        return self._session_ctrl

    def workflow(self) -> WorkflowController:
        """Return (or create) the :class:`WorkflowController`.

        Returns:
            :class:`WorkflowController`.
        """
        if self._workflow_ctrl is None:
            self._workflow_ctrl = WorkflowController(
                workflow_service=self._container.get("workflow_service"),
                resolver=self._resolver,
                dependencies=self._container,
            )
        return self._workflow_ctrl

    def review(self) -> ReviewController:
        """Return (or create) the :class:`ReviewController`.

        Returns:
            :class:`ReviewController`.
        """
        if self._review_ctrl is None:
            self._review_ctrl = ReviewController(
                hitl_service=self._container.get("hitl_service"),
                resolver=self._resolver,
                dependencies=self._container,
            )
        return self._review_ctrl

    def recovery(self) -> RecoveryController:
        """Return (or create) the :class:`RecoveryController`.

        Returns:
            :class:`RecoveryController`.
        """
        if self._recovery_ctrl is None:
            self._recovery_ctrl = RecoveryController(
                workflow_service=self._container.get("workflow_service"),
                resolver=self._resolver,
                dependencies=self._container,
            )
        return self._recovery_ctrl
