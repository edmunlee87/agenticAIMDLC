"""Standalone platform utilities: ResultFactory, DependencyContainer, IDFactory, TimeProvider.

These utilities have no base class in the platform hierarchy (standalone).
They provide common cross-cutting capabilities used by services, controllers, and bridges.
"""

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

from .base_result import BaseResult, ValidationResultBase
from .common_fragments import ErrorRecord, WarningRecord

T = TypeVar("T", bound=BaseResult)


class IDFactory:
    """Factory for generating deterministic or random unique identifiers.

    All IDs are prefixed by type for easy identification in logs and schemas.

    Examples:
        IDFactory.run_id()       -> "run_abc12345..."
        IDFactory.trace_id()     -> "trc_abc12345..."
        IDFactory.review_id()    -> "rev_abc12345..."
    """

    @staticmethod
    def _generate(prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex}"

    @staticmethod
    def run_id() -> str:
        """Generate a new run ID."""
        return IDFactory._generate("run")

    @staticmethod
    def session_id() -> str:
        """Generate a new session ID."""
        return IDFactory._generate("ses")

    @staticmethod
    def trace_id() -> str:
        """Generate a new trace ID."""
        return IDFactory._generate("trc")

    @staticmethod
    def correlation_id() -> str:
        """Generate a new correlation ID."""
        return IDFactory._generate("cor")

    @staticmethod
    def review_id() -> str:
        """Generate a new review ID."""
        return IDFactory._generate("rev")

    @staticmethod
    def audit_id() -> str:
        """Generate a new audit ID."""
        return IDFactory._generate("aud")

    @staticmethod
    def event_id() -> str:
        """Generate a new event ID."""
        return IDFactory._generate("evt")

    @staticmethod
    def artifact_id() -> str:
        """Generate a new artifact ID."""
        return IDFactory._generate("art")

    @staticmethod
    def candidate_version_id() -> str:
        """Generate a new candidate version ID."""
        return IDFactory._generate("cnd")

    @staticmethod
    def selection_id() -> str:
        """Generate a new version selection ID."""
        return IDFactory._generate("sel")

    @staticmethod
    def interaction_id() -> str:
        """Generate a new interaction ID."""
        return IDFactory._generate("int")

    @staticmethod
    def context_id() -> str:
        """Generate a new runtime context ID."""
        return IDFactory._generate("ctx")

    @staticmethod
    def stack_id() -> str:
        """Generate a new resolved stack ID."""
        return IDFactory._generate("stk")

    @staticmethod
    def envelope_id() -> str:
        """Generate a new response envelope ID."""
        return IDFactory._generate("env")

    @staticmethod
    def checkpoint_id() -> str:
        """Generate a new checkpoint ID."""
        return IDFactory._generate("chk")


class TimeProvider:
    """Provides consistent, timezone-aware timestamps.

    Uses UTC by default. Can be overridden in tests for deterministic behavior.

    Examples:
        TimeProvider.now()            -> datetime (UTC)
        TimeProvider.now_iso()        -> "2025-01-15T10:30:00+00:00"
    """

    _override: Optional[Callable[[], datetime]] = None

    @classmethod
    def now(cls) -> datetime:
        """Return the current UTC datetime.

        Returns:
            Timezone-aware UTC datetime.
        """
        if cls._override:
            return cls._override()
        return datetime.now(tz=timezone.utc)

    @classmethod
    def now_iso(cls) -> str:
        """Return the current UTC datetime as an ISO 8601 string.

        Returns:
            ISO 8601 datetime string with timezone offset.
        """
        return cls.now().isoformat()

    @classmethod
    def set_override(cls, provider: Optional[Callable[[], datetime]]) -> None:
        """Override the time provider for testing.

        Args:
            provider: Callable returning a datetime, or None to reset.
        """
        cls._override = provider


class ResultFactory:
    """Factory for constructing BaseResult instances with standard patterns.

    Simplifies result creation in SDK service methods while ensuring all
    required fields (sdk_name, function_name, hints) are populated.

    Examples:
        ResultFactory.success("config_sdk", "load_config", data={"config": cfg})
        ResultFactory.failure("config_sdk", "load_config", errors=["File not found"])
    """

    @staticmethod
    def success(
        sdk_name: str,
        function_name: str,
        data: Optional[Dict[str, Any]] = None,
        message: str = "Operation completed successfully.",
        warnings: Optional[List[str]] = None,
        artifacts_created: Optional[List[str]] = None,
        references: Optional[Dict[str, str]] = None,
        agent_hint: str = "",
        workflow_hint: str = "",
        audit_hint: str = "",
        observability_hint: str = "",
    ) -> BaseResult:
        """Build a success BaseResult.

        Args:
            sdk_name: Name of the SDK producing this result.
            function_name: Name of the function producing this result.
            data: Primary result payload.
            message: Human-readable success message.
            warnings: Non-blocking warnings to surface.
            artifacts_created: Artifact IDs produced.
            references: Cross-references (review_id, audit_id, event_id, etc.).
            agent_hint: Agent-facing guidance string.
            workflow_hint: Workflow state guidance string.
            audit_hint: Audit record creation guidance.
            observability_hint: Observability event emission guidance.

        Returns:
            BaseResult with status="success".
        """
        return BaseResult(
            status="success",
            message=message,
            sdk_name=sdk_name,
            function_name=function_name,
            data=data,
            warnings=warnings or [],
            errors=[],
            artifacts_created=artifacts_created or [],
            references=references or {},
            agent_hint=agent_hint,
            workflow_hint=workflow_hint,
            audit_hint=audit_hint,
            observability_hint=observability_hint,
        )

    @staticmethod
    def failure(
        sdk_name: str,
        function_name: str,
        errors: Optional[List[str]] = None,
        message: str = "Operation failed.",
        data: Optional[Dict[str, Any]] = None,
        agent_hint: str = "",
        workflow_hint: str = "",
        audit_hint: str = "",
        observability_hint: str = "",
    ) -> BaseResult:
        """Build a failure BaseResult.

        Args:
            sdk_name: Name of the SDK producing this result.
            function_name: Name of the function producing this result.
            errors: List of error messages.
            message: Human-readable failure message.
            data: Optional partial result payload.
            agent_hint: Agent-facing guidance string.
            workflow_hint: Workflow state guidance string.
            audit_hint: Audit record creation guidance.
            observability_hint: Observability event emission guidance.

        Returns:
            BaseResult with status="failure".
        """
        return BaseResult(
            status="failure",
            message=message,
            sdk_name=sdk_name,
            function_name=function_name,
            data=data,
            warnings=[],
            errors=errors or ["Unknown error occurred."],
            artifacts_created=[],
            references={},
            agent_hint=agent_hint,
            workflow_hint=workflow_hint,
            audit_hint=audit_hint,
            observability_hint=observability_hint,
        )

    @staticmethod
    def blocked(
        sdk_name: str,
        function_name: str,
        reason: str,
        blocking_context: Optional[Dict[str, Any]] = None,
        agent_hint: str = "",
        workflow_hint: str = "",
    ) -> BaseResult:
        """Build a blocked BaseResult.

        Args:
            sdk_name: Name of the SDK producing this result.
            function_name: Name of the function producing this result.
            reason: Human-readable blocking reason.
            blocking_context: Optional context about what is blocking.
            agent_hint: Agent-facing guidance string.
            workflow_hint: Workflow state guidance string.

        Returns:
            BaseResult with status="blocked".
        """
        return BaseResult(
            status="blocked",
            message=f"Operation blocked: {reason}",
            sdk_name=sdk_name,
            function_name=function_name,
            data=blocking_context,
            warnings=[],
            errors=[reason],
            artifacts_created=[],
            references={},
            agent_hint=agent_hint or f"Resolve blocking condition: {reason}",
            workflow_hint=workflow_hint,
        )

    @staticmethod
    def warning(
        sdk_name: str,
        function_name: str,
        warnings: List[str],
        data: Optional[Dict[str, Any]] = None,
        message: str = "Operation completed with warnings.",
        agent_hint: str = "",
        workflow_hint: str = "",
        audit_hint: str = "",
        observability_hint: str = "",
    ) -> BaseResult:
        """Build a warning BaseResult (success with non-blocking issues).

        Args:
            sdk_name: Name of the SDK producing this result.
            function_name: Name of the function producing this result.
            warnings: List of warning messages.
            data: Primary result payload.
            message: Human-readable message.
            agent_hint: Agent-facing guidance string.
            workflow_hint: Workflow state guidance string.
            audit_hint: Audit record creation guidance.
            observability_hint: Observability event emission guidance.

        Returns:
            BaseResult with status="warning".
        """
        return BaseResult(
            status="warning",
            message=message,
            sdk_name=sdk_name,
            function_name=function_name,
            data=data,
            warnings=warnings,
            errors=[],
            artifacts_created=[],
            references={},
            agent_hint=agent_hint,
            workflow_hint=workflow_hint,
            audit_hint=audit_hint,
            observability_hint=observability_hint,
        )


class DependencyContainer:
    """Simple dependency injection container for platform services.

    Services register themselves at startup; other services retrieve dependencies
    without hard-coding concrete implementations.

    Thread-safety: Not thread-safe by default. Use one container per request
    context or ensure registration happens before concurrent access.

    Examples:
        container = DependencyContainer()
        container.register("observability", ObservabilityService())
        svc = container.get("observability", ObservabilityService)
    """

    def __init__(self) -> None:
        self._registry: Dict[str, Any] = {}

    def register(self, name: str, instance: Any) -> None:
        """Register a service instance under a name.

        Args:
            name: Service name/key.
            instance: Service instance to register.
        """
        self._registry[name] = instance

    def get(self, name: str, expected_type: Optional[Type] = None) -> Any:
        """Retrieve a registered service by name.

        Args:
            name: Service name/key.
            expected_type: Optional type check; raises TypeError if mismatch.

        Returns:
            The registered service instance.

        Raises:
            KeyError: If the service name is not registered.
            TypeError: If expected_type is provided and does not match.
        """
        if name not in self._registry:
            raise KeyError(f"Service '{name}' is not registered in DependencyContainer")
        instance = self._registry[name]
        if expected_type and not isinstance(instance, expected_type):
            raise TypeError(
                f"Service '{name}' expected type {expected_type.__name__}, "
                f"got {type(instance).__name__}"
            )
        return instance

    def has(self, name: str) -> bool:
        """Check if a service is registered.

        Args:
            name: Service name/key.

        Returns:
            True if registered, False otherwise.
        """
        return name in self._registry

    def all_names(self) -> List[str]:
        """Return all registered service names.

        Returns:
            Sorted list of registered service names.
        """
        return sorted(self._registry.keys())
