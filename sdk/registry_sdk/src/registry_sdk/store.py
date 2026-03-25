"""In-memory registry store with pluggable persistence protocol.

The store is the single source of truth for project, run, and skill records.
By default it is in-memory (sufficient for tests and single-node operation).
Swap the backing by implementing :class:`RegistryStoreProtocol`.
"""

from __future__ import annotations

from typing import Any, Protocol, TypeVar

from platform_contracts.results import BaseResult, ResultFactory

T = TypeVar("T")


class RegistryStoreProtocol(Protocol[T]):
    """Protocol that any registry backing store must satisfy."""

    def put(self, record_id: str, record: T) -> None: ...
    def get(self, record_id: str) -> T | None: ...
    def list_all(self) -> list[T]: ...
    def exists(self, record_id: str) -> bool: ...


class InMemoryStore:
    """Thread-unsafe in-memory store for development and testing.

    Args:
        name: Store name (used in error messages).
    """

    def __init__(self, name: str = "store") -> None:
        self._name = name
        self._data: dict[str, Any] = {}

    def put(self, record_id: str, record: Any) -> None:
        """Insert or replace a record by ID."""
        self._data[record_id] = record

    def get(self, record_id: str) -> Any | None:
        """Return record or None if not found."""
        return self._data.get(record_id)

    def list_all(self) -> list[Any]:
        """Return all stored records."""
        return list(self._data.values())

    def exists(self, record_id: str) -> bool:
        """Return True if the record ID exists."""
        return record_id in self._data

    def query(self, **filters: Any) -> list[Any]:
        """Return records matching all provided field=value filters.

        Args:
            **filters: Field name -> value pairs to match against record attributes.

        Returns:
            Matching records list.
        """
        results = []
        for record in self._data.values():
            if all(
                getattr(record, field, None) == value
                for field, value in filters.items()
            ):
                results.append(record)
        return results
