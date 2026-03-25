"""artifactsdk — Artifact registration, validation, and lineage SDK.

Public API:
    ArtifactService  — primary service class
    ArtifactRecord   — immutable artifact registry entry
    ArtifactManifest — named artifact collection for reporting packs
    ArtifactLineageLink — directed lineage graph edge
    ChecksumRecord   — artifact integrity checksum
    InMemoryArtifactStore — pluggable in-process storage adapter
    ChecksumManager  — checksum computation and verification utility
"""

from .artifact_service import ArtifactService
from .models import (
    ArtifactLineageLink,
    ArtifactManifest,
    ArtifactRecord,
    ChecksumRecord,
)
from .storage_adapter import ChecksumManager, InMemoryArtifactStore

__all__ = [
    "ArtifactService",
    "ArtifactRecord",
    "ArtifactManifest",
    "ArtifactLineageLink",
    "ChecksumRecord",
    "InMemoryArtifactStore",
    "ChecksumManager",
]
