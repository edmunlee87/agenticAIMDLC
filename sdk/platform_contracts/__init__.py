"""Platform Contracts SDK.

Documents and enforces SDK public API discipline, tool registry schema,
and meta-model governance conventions for the entire MDLC platform.
"""

from sdk.platform_contracts.api_discipline import SDKPublicAPIDiscipline
from sdk.platform_contracts.meta_model_governance import (
    ChangeType,
    SchemaChangeRecord,
)
from sdk.platform_contracts.tool_registry_schema import (
    ToolFailureMode,
    ToolRegistryEntry,
)

__version__ = "0.1.0"

__all__ = [
    "SDKPublicAPIDiscipline",
    "ChangeType",
    "SchemaChangeRecord",
    "ToolFailureMode",
    "ToolRegistryEntry",
]
