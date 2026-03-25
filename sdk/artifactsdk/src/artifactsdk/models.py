"""Artifact SDK data models.

An :class:`ArtifactRecord` is the immutable catalog entry for any material
MDLC output (datasets, models, reports, configs, schemas, etc.). The record
includes full governance provenance and a content hash for integrity checks.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ArtifactType(str, Enum):
    DATASET = "dataset"
    MODEL = "model"
    FEATURE_SET = "feature_set"
    REPORT = "report"
    SCHEMA = "schema"
    CONFIG = "config"
    EVALUATION = "evaluation"
    DOCUMENT = "document"
    PRESENTATION = "presentation"
    OTHER = "other"


class ArtifactStatus(str, Enum):
    DRAFT = "draft"
    PROMOTED = "promoted"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"
    REJECTED = "rejected"


class ArtifactRecord(BaseModel):
    """Immutable catalog entry for a versioned MDLC artifact.

    Args:
        artifact_id: Unique artifact identifier.
        artifact_type: Logical type of the artifact.
        name: Human-readable artifact name.
        version: Monotonic version string (e.g. ``"1.0.0"``).
        uri: Storage URI (file path, S3 key, ADLS path, etc.).
        content_hash: SHA-256 hash of the artifact content.
        content_size_bytes: Artifact content size.
        created_at: Creation timestamp.
        created_by: Actor ID who created the artifact.
        run_id: Run that produced the artifact.
        project_id: Owning project.
        stage_name: MDLC stage that produced the artifact.
        status: Lifecycle status.
        schema_version: Schema version of the artifact metadata.
        lineage_artifact_ids: Parent artifact IDs (for lineage tracking).
        tags: Searchable key-value tags.
        metadata: Arbitrary structured metadata.
    """

    model_config = ConfigDict(frozen=True)

    artifact_id: str
    artifact_type: ArtifactType
    name: str
    version: str = "1.0.0"
    uri: str = ""
    content_hash: str = ""
    content_size_bytes: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""
    run_id: str = ""
    project_id: str = ""
    stage_name: str = ""
    status: ArtifactStatus = ArtifactStatus.DRAFT
    schema_version: str = "1.0.0"
    lineage_artifact_ids: list[str] = Field(default_factory=list)
    tags: dict[str, str] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("artifact_id", "name", mode="before")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("artifact_id and name must be non-empty")
        return v
