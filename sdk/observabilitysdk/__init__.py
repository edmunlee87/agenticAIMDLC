"""Observability SDK.

Provides ObservabilityService for creating traces, writing skill events,
querying event history, and building event lineage.
"""

from sdk.observabilitysdk.event_store import EventStoreAdapter, InMemoryEventStore
from sdk.observabilitysdk.models import EventLineage, SkillEvent, TokenUsage
from sdk.observabilitysdk.observability_service import ObservabilityService

__version__ = "0.1.0"

__all__ = [
    "ObservabilityService",
    "SkillEvent",
    "TokenUsage",
    "EventLineage",
    "EventStoreAdapter",
    "InMemoryEventStore",
]
