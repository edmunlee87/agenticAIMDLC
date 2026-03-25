"""ControllerFactory -- wires controllers from the dependency container.

Example::

    from platform_core.controllers.factory import ControllerFactory

    factory = ControllerFactory(bundle, container)
    session_ctrl = factory.session()
    workflow_ctrl = factory.workflow()
    review_ctrl = factory.review()
    recovery_ctrl = factory.recovery()
"""

from __future__ import annotations

from platform_core.controllers.recovery import RecoveryController
from platform_core.controllers.review import ReviewController
from platform_core.controllers.session import SessionController
from platform_core.controllers.workflow import WorkflowController
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.runtime.resolver import RuntimeResolver
from platform_core.utils.dependency_container import DependencyContainer
from platform_core.utils.id_factory import IDFactory
from platform_core.utils.time_provider import TimeProvider


class ControllerFactory:
    """Creates and caches controller instances.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        container: :class:`~platform_core.utils.dependency_container.DependencyContainer`
            holding registered services (``workflow_service``, ``hitl_service``).
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
        self._id_factory = id_factory_
        self._time_provider = time_provider_
        self._resolver = RuntimeResolver(bundle)
        # Lazy-cached controller instances.
        self._session_ctrl: SessionController | None = None
        self._workflow_ctrl: WorkflowController | None = None
        self._review_ctrl: ReviewController | None = None
        self._recovery_ctrl: RecoveryController | None = None

    def session(self) -> SessionController:
        """Return (or create) the :class:`SessionController`."""
        if self._session_ctrl is None:
            self._session_ctrl = SessionController(
                self._bundle,
                workflow_service=self._container.get("workflow_service"),
                resolver=self._resolver,
                id_factory_=self._id_factory,
                time_provider_=self._time_provider,
            )
        return self._session_ctrl

    def workflow(self) -> WorkflowController:
        """Return (or create) the :class:`WorkflowController`."""
        if self._workflow_ctrl is None:
            self._workflow_ctrl = WorkflowController(
                self._bundle,
                workflow_service=self._container.get("workflow_service"),
                resolver=self._resolver,
                id_factory_=self._id_factory,
                time_provider_=self._time_provider,
            )
        return self._workflow_ctrl

    def review(self) -> ReviewController:
        """Return (or create) the :class:`ReviewController`."""
        if self._review_ctrl is None:
            self._review_ctrl = ReviewController(
                self._bundle,
                hitl_service=self._container.get("hitl_service"),
                resolver=self._resolver,
                id_factory_=self._id_factory,
                time_provider_=self._time_provider,
            )
        return self._review_ctrl

    def recovery(self) -> RecoveryController:
        """Return (or create) the :class:`RecoveryController`."""
        if self._recovery_ctrl is None:
            self._recovery_ctrl = RecoveryController(
                self._bundle,
                workflow_service=self._container.get("workflow_service"),
                resolver=self._resolver,
                id_factory_=self._id_factory,
                time_provider_=self._time_provider,
            )
        return self._recovery_ctrl
