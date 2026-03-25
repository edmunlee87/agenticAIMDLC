"""Environment configuration models.

Defines environment-specific settings like storage paths, feature flags,
and deployment metadata.
Loaded from ``configs/runtime/environment.yaml`` and environment-specific
overlays in ``configs/runtime/environment_overlays/``.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from platform_contracts.enums import EnvironmentType
from platform_core.runtime.config_models.base import ConfigModelBase


class StorageConfig(ConfigModelBase):
    """Storage backend configuration for an environment.

    Args:
        artifact_store_uri: Root URI for artifact storage.
        audit_store_uri: Root URI for the append-only audit store.
        event_store_uri: Root URI for the observability event store.
        workflow_state_uri: Root URI for workflow state persistence.
        config_store_uri: Root URI for config YAML file storage.
    """

    artifact_store_uri: str = "file://./artifacts"
    audit_store_uri: str = "file://./audit"
    event_store_uri: str = "file://./events"
    workflow_state_uri: str = "file://./workflow_state"
    config_store_uri: str = "file://./configs"


class FeatureFlagsConfig(ConfigModelBase):
    """Feature flags controlling optional runtime behaviour.

    Args:
        enable_rag: Enable RAG retrieval for agent context. Default: False.
        enable_spark_dataprep: Enable PySpark-backed data preparation. Default: False.
        enable_mcp_bridge: Enable the MCP agent bridge. Default: False.
        strict_policy_mode: Force strict policy mode regardless of domain config. Default: False.
        dry_run: Log actions without persisting state changes. Default: False.
    """

    enable_rag: bool = False
    enable_spark_dataprep: bool = False
    enable_mcp_bridge: bool = False
    strict_policy_mode: bool = False
    dry_run: bool = False


class EnvironmentConfig(ConfigModelBase):
    """Full environment-specific configuration.

    Args:
        environment: Deployment environment type.
        storage: Storage backend URIs.
        feature_flags: Runtime feature toggles.
        extra: Open-ended map for environment-specific custom settings.
            Keys must be prefixed with the owning component id.
    """

    environment: EnvironmentType = EnvironmentType.DEV
    storage: StorageConfig = Field(default_factory=StorageConfig)
    feature_flags: FeatureFlagsConfig = Field(default_factory=FeatureFlagsConfig)
    extra: dict[str, str | bool | int | float] = Field(default_factory=dict)
