"""Config SDK typed models.

Defines the request/response payloads for ConfigService operations.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sdk.platform_core.schemas.base_model_base import BaseModelBase
from sdk.platform_core.schemas.utilities import TimeProvider


class ConfigLoadRequest(BaseModelBase):
    """Request to load a runtime config bundle.

    Args:
        base_path: Absolute or repo-relative path to configs/runtime/.
        environment: Override environment name (dev/uat/prod).
        domain: Optional domain name to load a domain overlay.
        role: Optional actor role for role overlay resolution.
        run_id: Optional run_id for audit correlation.
        actor: Actor requesting the load.
    """

    base_path: str
    environment: Optional[str] = None
    domain: Optional[str] = None
    role: Optional[str] = None
    run_id: Optional[str] = None
    actor: str = "system"


class ConfigDiffEntry(BaseModelBase):
    """A single config difference entry.

    Args:
        key_path: Dot-delimited path to the changed key.
        old_value: Previous value (None if added).
        new_value: New value (None if removed).
        change_type: one of 'added', 'removed', 'changed'.
    """

    key_path: str
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    change_type: str = "changed"


class ConfigVersionRecord(BaseModelBase):
    """Version metadata for a loaded config bundle.

    Args:
        schema_version: The schema_version from runtime_master.yaml.
        environment: Resolved environment name.
        loaded_at: UTC timestamp of when the bundle was loaded.
        file_hashes: Map of config file name to content hash.
        overlays_applied: Names of overlays that were merged in.
    """

    schema_version: str
    environment: str
    loaded_at: datetime
    file_hashes: Dict[str, str] = {}
    overlays_applied: List[str] = []
