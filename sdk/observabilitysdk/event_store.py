"""Pluggable event store adapter interface and in-memory implementation.

The EventStoreAdapter defines the interface that ObservabilityService uses
to write and query events. The InMemoryEventStore is the default in-process
implementation. Production code can swap in a Kafka/S3/Delta backend.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

from .models import SkillEvent


class EventStoreAdapter(ABC):
    """Abstract interface for event storage backends.

    All implementations must be append-only (no updates/deletes).
    """

    @abstractmethod
    def append(self, event: SkillEvent) -> None:
        """Append an event to the store.

        Args:
            event: The :class:`SkillEvent` to append.

        Raises:
            RuntimeError: If the write fails (used to block restricted actions).
        """

    @abstractmethod
    def query(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 1000,
    ) -> List[SkillEvent]:
        """Return events matching the given field filters.

        Args:
            filters: Dict of field -> value exact-match filters.
            limit: Maximum number of events to return.

        Returns:
            List of matching :class:`SkillEvent` objects.
        """

    @abstractmethod
    def get_by_id(self, event_id: str) -> Optional[SkillEvent]:
        """Retrieve a single event by event_id.

        Args:
            event_id: Unique event identifier.

        Returns:
            :class:`SkillEvent` or None.
        """


class InMemoryEventStore(EventStoreAdapter):
    """In-memory append-only event store (default, non-persistent).

    Stores events in an ordered list. Not suitable for production use.
    Swap with a persistent adapter for durability.

    Args:
        max_size: Maximum number of events to retain (0 = unlimited).
        fail_on_write: If True, all appends raise RuntimeError (for failure-mode testing).
    """

    def __init__(self, max_size: int = 0, fail_on_write: bool = False) -> None:
        self._events: List[SkillEvent] = []
        self._index: Dict[str, SkillEvent] = {}
        self._max_size = max_size
        self._fail_on_write = fail_on_write

    def append(self, event: SkillEvent) -> None:
        if self._fail_on_write:
            raise RuntimeError("Event store write simulated failure.")
        if self._max_size and len(self._events) >= self._max_size:
            raise RuntimeError(
                f"Event store at capacity: max_size={self._max_size}"
            )
        self._events.append(event)
        self._index[event.event_id] = event

    def query(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 1000,
    ) -> List[SkillEvent]:
        results = self._events
        if filters:
            results = [
                e for e in results
                if all(getattr(e, k, None) == v for k, v in filters.items())
            ]
        return results[:limit]

    def get_by_id(self, event_id: str) -> Optional[SkillEvent]:
        return self._index.get(event_id)

    @property
    def count(self) -> int:
        """Return the total number of stored events."""
        return len(self._events)
