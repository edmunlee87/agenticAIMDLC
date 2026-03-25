"""Config SDK.

Provides ConfigService for loading, validating, resolving, and diffing
platform runtime config bundles.
"""

from sdk.config_sdk.config_service import ConfigService
from sdk.config_sdk.models import (
    ConfigDiffEntry,
    ConfigLoadRequest,
    ConfigVersionRecord,
)

__version__ = "0.1.0"

__all__ = [
    "ConfigService",
    "ConfigDiffEntry",
    "ConfigLoadRequest",
    "ConfigVersionRecord",
]
