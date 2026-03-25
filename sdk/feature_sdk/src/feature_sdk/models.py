"""feature_sdk.models -- feature metadata and lineage contracts."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FeatureMetadata(BaseModel):
    """Metadata for a single feature.

    Args:
        feature_id: Unique feature identifier.
        feature_name: Human-readable name.
        dtype: Data type (e.g. ``"float64"``, ``"int32"``, ``"categorical"``).
        description: Feature description.
        source_dataset_id: Dataset this feature originates from.
        transformation: Description of any transformation applied.
        lineage_refs: Upstream feature IDs that feed into this feature.
        is_target: Whether this feature is the model target. Default: False.
        is_protected: Whether this is a protected attribute. Default: False.
        run_id: MDLC run.
        project_id: Project.
        created_at: Registration timestamp.
        created_by: Actor who registered the feature.
        metadata: Arbitrary extra metadata.
    """

    model_config = ConfigDict(frozen=True)

    feature_id: str
    feature_name: str
    dtype: str = ""
    description: str = ""
    source_dataset_id: str = ""
    transformation: str = ""
    lineage_refs: list[str] = Field(default_factory=list)
    is_target: bool = False
    is_protected: bool = False
    run_id: str = ""
    project_id: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class FeatureSet(BaseModel):
    """An immutable, versioned set of features.

    Args:
        feature_set_id: Unique identifier.
        name: Human-readable name.
        version: Semantic version.
        feature_ids: Ordered list of feature IDs in this set.
        snapshot_id: Dataset snapshot this feature set was derived from.
        run_id: MDLC run.
        project_id: Project.
        artifact_id: Artifact ID storing the feature matrix.
        created_at: Creation timestamp.
        created_by: Actor.
    """

    model_config = ConfigDict(frozen=True)

    feature_set_id: str
    name: str = ""
    version: str = "1.0.0"
    feature_ids: list[str] = Field(default_factory=list)
    snapshot_id: str = ""
    run_id: str = ""
    project_id: str = ""
    artifact_id: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""
