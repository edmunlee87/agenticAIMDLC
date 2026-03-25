"""DependencyContainer -- simple service locator for platform services.

Provides a minimal dependency injection container. Services are registered
by type and retrieved by type. Allows test doubles to be swapped in without
modifying call sites.
"""

from __future__ import annotations

from typing import Any, TypeVar

T = TypeVar("T")


class DependencyContainer:
    """Lightweight service registry.

    Services are registered once and retrieved by type. Raises ``KeyError``
    when a requested service has not been registered.

    Examples:
        >>> container = DependencyContainer()
        >>> container.register(MyService, MyService())
        >>> svc = container.get(MyService)
    """

    def __init__(self) -> None:
        self._registry: dict[type, Any] = {}

    def register(self, service_type: type[T], instance: T) -> None:
        """Register a service instance under its type key.

        Args:
            service_type: The type (class) to register under.
            instance: The service instance.
        """
        self._registry[service_type] = instance

    def get(self, service_type: type[T]) -> T:
        """Retrieve a registered service by its type.

        Args:
            service_type: The type to look up.

        Returns:
            The registered service instance.

        Raises:
            KeyError: If no instance is registered for ``service_type``.
        """
        if service_type not in self._registry:
            raise KeyError(
                f"No instance registered for {service_type.__name__}. "
                "Register it before calling get()."
            )
        return self._registry[service_type]  # type: ignore[return-value]

    def has(self, service_type: type) -> bool:
        """Return True if a service is registered for this type."""
        return service_type in self._registry

    def unregister(self, service_type: type) -> None:
        """Remove a registered service.

        Args:
            service_type: The type to unregister.
        """
        self._registry.pop(service_type, None)
