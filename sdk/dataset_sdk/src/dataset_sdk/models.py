"""dataset_sdk.models -- dataset registry and snapshot contracts."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DatasetSplitType(str, Enum):
    """Named split type for a dataset."""
    TRAIN = "train"
    TEST = "test"
    VALIDATION = "validation"
    OOT = "oot"
    HOLDOUT = "holdout"
    FULL = "full"


class DatasetSnapshot(BaseModel):
    """Immutable snapshot of a dataset at a point in time.

    Args:
        snapshot_id: Unique snapshot identifier.
        dataset_id: Parent dataset identifier.
        run_id: MDLC run that produced this snapshot.
        project_id: Project.
        split_type: :class:`DatasetSplitType`.
        row_count: Number of rows.
        column_count: Number of columns.
        column_names: List of column names.
        artifact_id: Artifact ID (in artifactsdk) storing the actual data.
        schema_version: Snapshot schema version.
        created_at: Creation timestamp.
        created_by: Actor who created the snapshot.
        lineage_refs: Upstream snapshot IDs that fed this snapshot.
        metadata: Arbitrary metadata.
    """

    model_config = ConfigDict(frozen=True)

    snapshot_id: str
    dataset_id: str
    run_id: str
    project_id: str
    split_type: DatasetSplitType = DatasetSplitType.FULL
    row_count: int = 0
    column_count: int = 0
    column_names: list[str] = Field(default_factory=list)
    artifact_id: str = ""
    schema_version: str = "1.0.0"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""
    lineage_refs: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DatasetRecord(BaseModel):
    """Registry entry for a dataset (parent of one or more snapshots).

    Args:
        dataset_id: Unique dataset identifier.
        project_id: Project.
        name: Human-readable name.
        description: Dataset description.
        model_type: Domain model type this dataset belongs to.
        snapshot_ids: All snapshot IDs registered under this dataset.
        created_at: Registration timestamp.
        created_by: Actor who registered the dataset.
    """

    model_config = ConfigDict(frozen=True)

    dataset_id: str
    project_id: str
    name: str = ""
    description: str = ""
    model_type: str = "generic"
    snapshot_ids: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""
