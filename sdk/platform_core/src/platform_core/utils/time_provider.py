"""TimeProvider -- injectable clock for deterministic time in tests.

All platform code that needs ``datetime.now()`` should call
:meth:`TimeProvider.now` rather than ``datetime.now(timezone.utc)`` directly.
This makes time injectable and testable without monkey-patching.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol


class ClockProtocol(Protocol):
    """Protocol for a clock that returns the current UTC datetime."""

    def now(self) -> datetime:
        """Return the current UTC datetime."""
        ...


class RealClock:
    """Production clock. Returns ``datetime.now(timezone.utc)``."""

    def now(self) -> datetime:
        """Return the real current UTC timestamp."""
        return datetime.now(timezone.utc)


class TimeProvider:
    """Injectable time provider. Use :meth:`now` throughout platform code.

    Args:
        clock: A :class:`ClockProtocol` implementation. Defaults to :class:`RealClock`.

    Examples:
        Production use::

            tp = TimeProvider()
            ts = tp.now()

        Test use::

            from datetime import datetime, timezone
            class FixedClock:
                def now(self): return datetime(2026, 1, 1, tzinfo=timezone.utc)
            tp = TimeProvider(clock=FixedClock())
    """

    def __init__(self, clock: ClockProtocol | None = None) -> None:
        self._clock: ClockProtocol = clock or RealClock()

    def now(self) -> datetime:
        """Return the current UTC datetime from the injected clock."""
        return self._clock.now()

    def now_iso(self) -> str:
        """Return the current UTC datetime as an ISO-8601 string."""
        return self.now().isoformat()


# Module-level singleton for production use.
time_provider = TimeProvider()
