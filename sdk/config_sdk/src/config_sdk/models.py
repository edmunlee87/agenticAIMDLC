"""Config SDK data models.

Defines the immutable result types and audit records produced by ConfigService.
All config load/override events are recorded as :class:`ConfigLoadEvent` entries.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from platform_core.runtime.config_models.enums import ConfigLoadSource


class ConfigLoadEvent(BaseModel):
    """Structured audit record for a single config key load or override.

    Emitted for every config load, override, and default-fallback so the
    runtime config provenance is fully traceable.

    Args:
        event_id: Unique event identifier.
        timestamp: When the load event occurred (UTC).
        run_id: Active run ID at the time of load (if available).
        actor: Actor who triggered the load (service name or user ID).
        config_key_path: Dot-separated path to the config key (e.g. ``"stages.model_training.timeout_minutes"``).
        old_value: Prior value before override (None for initial loads).
        new_value: New value loaded.
        source: Where the value came from.
        reason: Optional human-readable reason for an override.
    """

    model_config = ConfigDict(frozen=True)

    event_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    run_id: str = ""
    actor: str = "system"
    config_key_path: str
    old_value: Any = None
    new_value: Any
    source: ConfigLoadSource = ConfigLoadSource.FILE
    reason: str = ""

    @field_validator("config_key_path", mode="before")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("config_key_path must be non-empty")
        return v


class ConfigSnapshot(BaseModel):
    """Point-in-time snapshot of the active runtime configuration.

    Args:
        snapshot_id: Unique snapshot identifier.
        taken_at: UTC timestamp of the snapshot.
        environment: Active environment name.
        active_domain: Active domain at snapshot time.
        active_role: Active role at snapshot time.
        bundle_checksum: SHA-256 prefix of the serialised bundle.
        load_events: All load/override events recorded during this load cycle.
    """

    model_config = ConfigDict(frozen=True)

    snapshot_id: str
    taken_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    environment: str = ""
    active_domain: str = ""
    active_role: str = ""
    bundle_checksum: str = ""
    load_events: list[ConfigLoadEvent] = Field(default_factory=list)
