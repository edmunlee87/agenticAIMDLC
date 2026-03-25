"""Standardized result and error types shared across all MDLC SDK packages.

All SDK service methods return BaseResult or a subclass. Never raise unchecked
exceptions from SDK public methods; always wrap in a failure BaseResult.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ErrorDetail:
    """Structured error with a stable code, a human message, and optional detail.

    Args:
        code: Machine-stable error identifier (e.g. ``ERR_CONFIG_MISSING_KEY``).
        message: Human-readable description.
        detail: Additional context (stack trace, raw exception message, etc.).
    """

    code: str
    message: str
    detail: str = ""


@dataclass(frozen=True)
class BaseResult(Generic[T]):
    """Generic result container. Every SDK service method returns this.

    Use :meth:`ResultFactory.ok` and :meth:`ResultFactory.fail` to construct.

    Args:
        ok: ``True`` when the operation succeeded.
        value: The operation output (present when ``ok=True``).
        error: Error detail (present when ``ok=False``).
        warnings: Non-blocking issues to surface to callers.
    """

    ok: bool
    value: T | None = None
    error: ErrorDetail | None = None
    warnings: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        """Alias for ``ok`` for compatibility with result types that use ``success``."""
        return self.ok

    @property
    def data(self) -> T | None:
        """Alias for ``value`` for compatibility with SDK result conventions."""
        return self.value

    def unwrap(self) -> T:
        """Return ``value`` or raise ``RuntimeError`` if the result is a failure.

        Raises:
            RuntimeError: When ``ok=False`` -- includes the error code and message.
        """
        if not self.ok or self.value is None:
            code = self.error.code if self.error else "UNKNOWN"
            msg = self.error.message if self.error else "No value"
            raise RuntimeError(f"[{code}] {msg}")
        return self.value


@dataclass(frozen=True)
class ValidationResultBase(Generic[T]):
    """Result of a schema or business-rule validation pass.

    Args:
        valid: ``True`` when the subject passes all checks.
        subject: The validated object (may be present even on failure).
        violations: List of validation failure messages (empty when ``valid=True``).
        warnings: Non-blocking findings.
        metadata: Arbitrary key-value context for callers.
    """

    valid: bool
    subject: T | None = None
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class ResultFactory:
    """Convenience factory for constructing :class:`BaseResult` instances.

    Examples:
        >>> result = ResultFactory.ok(42)
        >>> result.ok
        True

        >>> result = ResultFactory.fail("ERR_NOT_FOUND", "Item not found")
        >>> result.ok
        False
    """

    @staticmethod
    def ok(value: T, warnings: list[str] | None = None) -> BaseResult[T]:
        """Construct a successful result.

        Args:
            value: The successful output.
            warnings: Optional non-blocking warnings.

        Returns:
            A :class:`BaseResult` with ``ok=True``.
        """
        return BaseResult(ok=True, value=value, warnings=warnings or [])

    @staticmethod
    def fail(
        code: str,
        message: str,
        detail: str = "",
        warnings: list[str] | None = None,
    ) -> BaseResult[Any]:
        """Construct a failure result.

        Args:
            code: Stable error code.
            message: Human-readable error message.
            detail: Optional raw detail (stack trace, etc.).
            warnings: Optional non-blocking warnings accumulated before failure.

        Returns:
            A :class:`BaseResult` with ``ok=False``.
        """
        return BaseResult(
            ok=False,
            error=ErrorDetail(code=code, message=message, detail=detail),
            warnings=warnings or [],
        )
