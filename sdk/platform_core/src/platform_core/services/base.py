"""Base service classes for the MDLC platform service layer.

All SDK facade services extend :class:`BaseService`. Specialised base classes
(:class:`BaseStorageService`, :class:`BaseRegistryService`, etc.) extend it
further for specific service concerns.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from platform_contracts.results import BaseResult
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.utils.id_factory import IDFactory, id_factory
from platform_core.utils.time_provider import TimeProvider, time_provider


class BaseService(ABC):
    """Root base class for all MDLC platform services.

    Subclasses must implement :meth:`health_check` to verify connectivity
    and availability of their backing stores.

    Args:
        bundle: The active :class:`RuntimeConfigBundle`.
        id_factory_: Optional :class:`IDFactory` for testing. Defaults to module singleton.
        time_provider_: Optional :class:`TimeProvider` for testing. Defaults to module singleton.
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        id_factory_: IDFactory | None = None,
        time_provider_: TimeProvider | None = None,
    ) -> None:
        self._bundle = bundle
        self._id_factory = id_factory_ or id_factory
        self._time_provider = time_provider_ or time_provider
        self._logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )

    @abstractmethod
    def health_check(self) -> BaseResult[dict[str, Any]]:
        """Verify service connectivity and backing store availability.

        Returns:
            A :class:`BaseResult` containing a health status dict with at least
            ``{"status": "ok"}`` on success or ``{"status": "degraded", ...}`` on failure.
        """


class BaseStorageService(BaseService, ABC):
    """Base for services that own a backing store (files, DB, object store).

    Subclasses: ArtifactStorageAdapter, EventStorageAdapter.
    """

    @abstractmethod
    def get_storage_uri(self) -> str:
        """Return the root URI of this service's backing store."""


class BaseRegistryService(BaseService, ABC):
    """Base for registry services (project, run, skill, policy registries).

    Subclasses: ProjectRegistryService, RunRegistryService.
    """

    @abstractmethod
    def register(self, record: Any) -> BaseResult[str]:
        """Register a record and return its assigned ID.

        Args:
            record: The record to register.

        Returns:
            :class:`BaseResult` containing the assigned record ID.
        """

    @abstractmethod
    def get(self, record_id: str) -> BaseResult[Any]:
        """Retrieve a record by its ID.

        Args:
            record_id: The record identifier.

        Returns:
            :class:`BaseResult` containing the record, or a failure if not found.
        """


class BaseReviewComponent(BaseService, ABC):
    """Base for HITL review components.

    Subclasses: ReviewPayloadService, ActionValidationService, DecisionCaptureService.
    """

    @abstractmethod
    def is_action_permitted(self, action: str, review_id: str, actor_role: str) -> bool:
        """Check whether an action is in the allowed_actions of the open review.

        Args:
            action: The action string to check.
            review_id: The open review's identifier.
            actor_role: The acting role.

        Returns:
            True if the action is permitted.
        """


class BaseSparkService(BaseService, ABC):
    """Base for services that use PySpark for heavy data processing.

    Subclasses: SparkDataPrepService.
    """

    @abstractmethod
    def get_spark_app_name(self) -> str:
        """Return the Spark application name for this service."""
