"""Artifact SDK typed models.

Maps to configs/schemas/artifact_registry.schema.json.
All records are immutable once registered; lineage tracked via lineage_parent_ids.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sdk.platform_core.schemas.base_model_base import BaseModelBase


class ChecksumRecord(BaseModelBase):
    """SHA-256 (or configurable) checksum for artifact integrity verification.

    Args:
        algorithm: Hash algorithm used (default: SHA-256).
        value: Hex-encoded hash value.
    """

    algorithm: str = "SHA-256"
    value: str


class ArtifactRecord(BaseModelBase):
    """Immutable artifact registry entry.

    Represents every material output produced by the platform, traceable to
    stage, actor, run, project, and candidate version.

    Args:
        artifact_id: Unique artifact identifier (``art_<uuid>``).
        artifact_type: Logical type (e.g. ``binning_summary``, ``model_object``).
        artifact_name: Human-readable name.
        stage_name: Stage that produced the artifact.
        producer_actor: Actor (user/system) that produced the artifact.
        project_id: Parent project identifier.
        run_id: Parent run identifier.
        timestamp: UTC creation timestamp.
        schema_version: Schema version for forward-compatibility.
        version: Artifact version string within the run (default: ``"1.0"``).
        uri_or_path: Storage URI or local path.
        checksum: Integrity checksum record.
        session_id: Optional session identifier.
        trace_id: Optional trace identifier for observability linking.
        correlation_id: Optional cross-service correlation ID.
        source_candidate_version_id: Candidate version that produced this artifact.
        lineage_parent_ids: Parent artifact IDs in the lineage graph.
        storage_backend: Storage backend (local / s3 / cml / gcs / azure_blob).
        retention_policy: Retention policy reference string.
        access_control_ref: Access control policy reference.
        metadata: Domain-extensible metadata dictionary.
    """

    artifact_id: str
    artifact_type: str
    artifact_name: str
    stage_name: str
    producer_actor: str
    project_id: str
    run_id: str
    timestamp: Optional[datetime] = None
    schema_version: str = "1.0"
    version: str = "1.0"
    uri_or_path: Optional[str] = None
    checksum: Optional[ChecksumRecord] = None
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None
    source_candidate_version_id: Optional[str] = None
    lineage_parent_ids: List[str] = []
    storage_backend: str = "local"
    retention_policy: Optional[str] = None
    access_control_ref: Optional[str] = None
    metadata: Dict[str, Any] = {}

    # Immutability guard — set once, never mutated after registration.
    immutable: bool = True


class ArtifactLineageLink(BaseModelBase):
    """A directed edge in the artifact lineage graph.

    Args:
        parent_id: Parent artifact ID (upstream).
        child_id: Child artifact ID (downstream).
        lineage_type: Relationship type (e.g. ``derived``, ``transformed``,
            ``aggregated``, ``selected``).
        recorded_at: UTC timestamp when the link was recorded.
    """

    parent_id: str
    child_id: str
    lineage_type: str = "derived"
    recorded_at: Optional[datetime] = None


class ArtifactManifest(BaseModelBase):
    """A named collection of artifacts, used for reporting/committee packs.

    Args:
        manifest_id: Unique manifest identifier.
        manifest_type: Purpose (e.g. ``committee_pack``, ``validation_evidence``,
            ``export_bundle``).
        artifact_ids: Ordered list of artifact IDs in this manifest.
        artifact_count: Total artifact count.
        run_id: Run scope for the manifest.
        project_id: Project scope for the manifest.
        created_at: UTC creation timestamp.
        metadata: Optional manifest-level metadata.
    """

    manifest_id: str
    manifest_type: str
    artifact_ids: List[str]
    artifact_count: int
    run_id: Optional[str] = None
    project_id: Optional[str] = None
    created_at: Optional[datetime] = None
    metadata: Dict[str, Any] = {}
