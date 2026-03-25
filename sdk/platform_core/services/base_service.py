"""BaseService and service layer base classes.

Provides the foundation for all platform SDK services.
SDKs inherit from the appropriate base and implement their specific logic.

Inheritance hierarchy:
    BaseService
        BaseStorageService
        BaseRegistryService
        BaseReviewComponent
        BaseSparkService (requires pyspark)

Design rules:
- One main service class per SDK.
- All material methods return BaseResult or ValidationResultBase.
- Composition preferred over deep inheritance.
- All exceptions are caught and returned as failure results, never raised silently.
"""

import logging
import traceback
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type

from ..schemas.base_result import BaseResult, ValidationResultBase
from ..schemas.common_fragments import ActorRecord
from ..schemas.utilities import IDFactory, ResultFactory, TimeProvider


class BaseService(ABC):
    """Root base class for all platform SDK services.

    Provides lifecycle helpers: _build_result, _get_dependency, _require_fields,
    _handle_exception, _log_start, _log_finish.

    Concrete services inherit from BaseService (or a sub-base) and implement
    their domain-specific public methods.

    Args:
        sdk_name: Name of the SDK this service belongs to.
        dependencies: Optional DependencyContainer for service dependencies.
        logger: Optional logger override. Defaults to module logger.
    """

    def __init__(
        self,
        sdk_name: str,
        dependencies: Optional[Any] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._sdk_name = sdk_name
        self._dependencies = dependencies
        self._logger = logger or logging.getLogger(f"platform.{sdk_name}")

    def _build_result(
        self,
        function_name: str,
        status: str = "success",
        message: str = "",
        data: Optional[Dict[str, Any]] = None,
        warnings: Optional[List[str]] = None,
        errors: Optional[List[str]] = None,
        artifacts_created: Optional[List[str]] = None,
        references: Optional[Dict[str, str]] = None,
        agent_hint: str = "",
        workflow_hint: str = "",
        audit_hint: str = "",
        observability_hint: str = "",
    ) -> BaseResult:
        """Construct a BaseResult with sdk_name pre-populated.

        Args:
            function_name: Calling function name.
            status: Result status.
            message: Human-readable message.
            data: Primary result payload.
            warnings: Non-blocking warnings.
            errors: Blocking errors.
            artifacts_created: Artifact IDs produced.
            references: Cross-references.
            agent_hint: Agent guidance hint.
            workflow_hint: Workflow state guidance.
            audit_hint: Audit creation guidance.
            observability_hint: Event emission guidance.

        Returns:
            Populated BaseResult.
        """
        return BaseResult(
            status=status,
            message=message,
            sdk_name=self._sdk_name,
            function_name=function_name,
            data=data,
            warnings=warnings or [],
            errors=errors or [],
            artifacts_created=artifacts_created or [],
            references=references or {},
            agent_hint=agent_hint,
            workflow_hint=workflow_hint,
            audit_hint=audit_hint,
            observability_hint=observability_hint,
        )

    def _get_dependency(self, name: str, expected_type: Optional[Type] = None) -> Any:
        """Retrieve a dependency from the container.

        Args:
            name: Dependency name.
            expected_type: Optional type check.

        Returns:
            Dependency instance.

        Raises:
            RuntimeError: If no container is configured.
            KeyError: If dependency is not registered.
        """
        if self._dependencies is None:
            raise RuntimeError(
                f"[{self._sdk_name}] No DependencyContainer configured. "
                "Inject dependencies via constructor."
            )
        return self._dependencies.get(name, expected_type)

    def _require_fields(self, context: str, **fields: Any) -> Optional[BaseResult]:
        """Validate that required fields are non-None and non-empty.

        Returns a failure result if any field is missing; None if all pass.

        Args:
            context: Human-readable context for the error message.
            **fields: Field name to value mappings to validate.

        Returns:
            Failure BaseResult if any field is missing, None otherwise.
        """
        missing = [name for name, val in fields.items() if val is None or val == ""]
        if missing:
            return ResultFactory.failure(
                self._sdk_name,
                context,
                errors=[f"Required field(s) missing: {', '.join(missing)}"],
                message=f"Validation failed: missing required fields for {context}.",
            )
        return None

    def _handle_exception(
        self, function_name: str, exc: Exception, context: Optional[str] = None
    ) -> BaseResult:
        """Convert an exception to a failure BaseResult.

        Logs the exception with stack trace and returns a structured failure.

        Args:
            function_name: Name of the function that raised the exception.
            exc: The exception to handle.
            context: Optional context string for the error message.

        Returns:
            Failure BaseResult.
        """
        error_detail = traceback.format_exc()
        msg = f"Unexpected error in {self._sdk_name}.{function_name}"
        if context:
            msg = f"{msg}: {context}"
        self._logger.error(
            msg,
            extra={
                "sdk_name": self._sdk_name,
                "function_name": function_name,
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            },
        )
        return ResultFactory.failure(
            self._sdk_name,
            function_name,
            errors=[f"{type(exc).__name__}: {exc}"],
            message=msg,
        )

    def _log_start(self, function_name: str, run_id: Optional[str] = None, **kwargs: Any) -> None:
        """Log the start of a service function call.

        Args:
            function_name: Name of the function starting.
            run_id: Optional run identifier.
            **kwargs: Additional context key-value pairs to include.
        """
        self._logger.info(
            "Starting %s.%s",
            self._sdk_name,
            function_name,
            extra={"sdk_name": self._sdk_name, "function_name": function_name, "run_id": run_id, **kwargs},
        )

    def _log_finish(
        self,
        function_name: str,
        result: BaseResult,
        run_id: Optional[str] = None,
    ) -> None:
        """Log the completion of a service function call.

        Args:
            function_name: Name of the function completing.
            result: The result to log.
            run_id: Optional run identifier.
        """
        level = logging.INFO if result.is_success else logging.WARNING
        self._logger.log(
            level,
            "Finished %s.%s: status=%s",
            self._sdk_name,
            function_name,
            result.status,
            extra={
                "sdk_name": self._sdk_name,
                "function_name": function_name,
                "status": result.status,
                "run_id": run_id,
                "warnings_count": len(result.warnings),
                "errors_count": len(result.errors),
            },
        )


class BaseStorageService(BaseService):
    """Base for storage adapter services.

    Sub-classes implement backend-specific read/write operations while
    inheriting standard error handling and result construction from BaseService.

    Concrete implementations: ArtifactStorageAdapter, EventStorageAdapter.
    """

    @abstractmethod
    def write(self, key: str, data: Any, metadata: Optional[Dict[str, Any]] = None) -> BaseResult:
        """Write data to the storage backend.

        Args:
            key: Storage key (path, ID, etc.).
            data: Data to write.
            metadata: Optional metadata to store alongside data.

        Returns:
            BaseResult indicating success or failure.
        """

    @abstractmethod
    def read(self, key: str) -> BaseResult:
        """Read data from the storage backend.

        Args:
            key: Storage key to read from.

        Returns:
            BaseResult with data in result.data.
        """

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if a key exists in the storage backend.

        Args:
            key: Storage key to check.

        Returns:
            True if the key exists.
        """


class BaseRegistryService(BaseService):
    """Base for registry services that maintain lookup indexes.

    Sub-classes implement domain-specific registration and retrieval while
    inheriting standard service helpers from BaseService.

    Concrete implementations: ProjectRegistryService, RunRegistryService.
    """

    @abstractmethod
    def register(self, entity_type: str, entity_id: str, payload: Dict[str, Any]) -> BaseResult:
        """Register an entity in the registry.

        Args:
            entity_type: Type of entity being registered.
            entity_id: Unique identifier for the entity.
            payload: Entity data to register.

        Returns:
            BaseResult.
        """

    @abstractmethod
    def get(self, entity_type: str, entity_id: str) -> BaseResult:
        """Retrieve an entity from the registry.

        Args:
            entity_type: Type of entity to retrieve.
            entity_id: Unique identifier for the entity.

        Returns:
            BaseResult with entity data in result.data.
        """

    @abstractmethod
    def search(self, entity_type: str, filters: Dict[str, Any]) -> BaseResult:
        """Search for entities matching the given filters.

        Args:
            entity_type: Type of entity to search.
            filters: Filter criteria.

        Returns:
            BaseResult with matching entities in result.data['results'].
        """


class BaseReviewComponent(BaseService):
    """Base for HITL review sub-components.

    Sub-classes implement specific review lifecycle concerns:
    ReviewPayloadService, ActionValidationService, DecisionCaptureService.
    """

    @abstractmethod
    def process(
        self,
        review_id: str,
        actor: ActorRecord,
        payload: Dict[str, Any],
    ) -> BaseResult:
        """Process a review action.

        Args:
            review_id: The review being processed.
            actor: The actor performing the action.
            payload: Action-specific payload data.

        Returns:
            BaseResult.
        """


class BaseSparkService(BaseService):
    """Base for PySpark-backed service implementations.

    Sub-classes receive a Spark session and implement heavy data operations
    using the DataFrame API. The Spark session is injected to support testing.

    Args:
        sdk_name: Name of the SDK this service belongs to.
        spark_session: Optional SparkSession instance.
        dependencies: Optional DependencyContainer.
        logger: Optional logger override.
    """

    def __init__(
        self,
        sdk_name: str,
        spark_session: Optional[Any] = None,
        dependencies: Optional[Any] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        super().__init__(sdk_name, dependencies, logger)
        self._spark = spark_session

    def _require_spark(self, function_name: str) -> Optional[BaseResult]:
        """Validate that a Spark session is available.

        Returns a failure result if Spark is not configured; None if available.

        Args:
            function_name: Calling function name.

        Returns:
            Failure BaseResult if Spark is not configured, None otherwise.
        """
        if self._spark is None:
            return ResultFactory.failure(
                self._sdk_name,
                function_name,
                errors=["SparkSession is required but not configured."],
                message="Spark session not available. Inject SparkSession via constructor.",
            )
        return None

    @abstractmethod
    def execute(
        self, input_data: Any, config: Optional[Dict[str, Any]] = None
    ) -> BaseResult:
        """Execute the primary Spark operation.

        Args:
            input_data: Input DataFrame or data reference.
            config: Optional execution configuration.

        Returns:
            BaseResult with output data reference and lineage metadata.
        """
