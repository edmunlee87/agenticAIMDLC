"""ArtifactService -- versioned artifact lifecycle management.

Handles registration, storage, promotion, and lineage tracking for all
material MDLC artifacts. All writes produce an immutable :class:`ArtifactRecord`
with content hash, provenance, and lineage links.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

from platform_contracts.results import BaseResult, ResultFactory
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.services.base import BaseService
from platform_core.utils.id_factory import IDFactory, id_factory
from platform_core.utils.time_provider import TimeProvider, time_provider

from artifactsdk.models import ArtifactRecord, ArtifactStatus, ArtifactType
from artifactsdk.storage import ArtifactStorageProtocol, FilesystemStorage, compute_content_hash

logger = logging.getLogger(__name__)


class ArtifactService(BaseService):
    """Artifact lifecycle service with versioning and lineage.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        storage: Backing storage implementation. Defaults to :class:`FilesystemStorage`.
        id_factory_: Injectable :class:`IDFactory`.
        time_provider_: Injectable :class:`TimeProvider`.
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        storage: ArtifactStorageProtocol | None = None,
        id_factory_: IDFactory | None = None,
        time_provider_: TimeProvider | None = None,
    ) -> None:
        super().__init__(bundle=bundle, id_factory_=id_factory_, time_provider_=time_provider_)
        self._storage = storage or FilesystemStorage()
        self._catalog: dict[str, ArtifactRecord] = {}
        # Indexes
        self._idx_run: dict[str, list[str]] = defaultdict(list)
        self._idx_project: dict[str, list[str]] = defaultdict(list)
        self._idx_type: dict[str, list[str]] = defaultdict(list)

    # ------------------------------------------------------------------
    # Write API
    # ------------------------------------------------------------------

    def register(
        self,
        artifact_type: ArtifactType,
        name: str,
        content: bytes,
        run_id: str,
        project_id: str,
        stage_name: str = "",
        created_by: str = "",
        version: str = "1.0.0",
        lineage_artifact_ids: list[str] | None = None,
        tags: dict[str, str] | None = None,
        metadata: dict[str, Any] | None = None,
        uri_hint: str = "",
    ) -> BaseResult[ArtifactRecord]:
        """Persist content and register an :class:`ArtifactRecord`.

        Args:
            artifact_type: Logical artifact type.
            name: Human-readable artifact name.
            content: Raw artifact bytes.
            run_id: Producing run ID.
            project_id: Owning project ID.
            stage_name: Producing MDLC stage.
            created_by: Actor ID.
            version: Version string.
            lineage_artifact_ids: Parent artifact IDs for lineage.
            tags: Searchable tags.
            metadata: Arbitrary metadata.
            uri_hint: Storage filename hint.

        Returns:
            :class:`BaseResult` containing the registered :class:`ArtifactRecord`.
        """
        artifact_id = self._id_factory.artifact_id()
        content_hash = compute_content_hash(content)
        uri = self._storage.write(artifact_id, content, uri_hint=uri_hint or name)

        record = ArtifactRecord(
            artifact_id=artifact_id,
            artifact_type=artifact_type,
            name=name,
            version=version,
            uri=uri,
            content_hash=content_hash,
            content_size_bytes=len(content),
            created_at=self._time_provider.now(),
            created_by=created_by,
            run_id=run_id,
            project_id=project_id,
            stage_name=stage_name,
            lineage_artifact_ids=lineage_artifact_ids or [],
            tags=tags or {},
            metadata=metadata or {},
        )
        self._catalog[artifact_id] = record
        self._idx_run[run_id].append(artifact_id)
        self._idx_project[project_id].append(artifact_id)
        self._idx_type[artifact_type.value].append(artifact_id)

        self._logger.info(
            "artifact.registered",
            extra={
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "name": name,
                "size_bytes": len(content),
                "run_id": run_id,
            },
        )
        return ResultFactory.ok(record)

    def register_record(self, record: ArtifactRecord) -> BaseResult[ArtifactRecord]:
        """Register a pre-built :class:`ArtifactRecord` without content storage.

        Use when the artifact is already in external storage and only the
        catalog entry needs to be created.

        Args:
            record: Pre-built artifact record.

        Returns:
            :class:`BaseResult` containing the registered record.
        """
        if record.artifact_id in self._catalog:
            return ResultFactory.fail(
                "ERR_ARTIFACT_EXISTS",
                f"Artifact '{record.artifact_id}' already in catalog.",
            )
        self._catalog[record.artifact_id] = record
        self._idx_run[record.run_id].append(record.artifact_id)
        self._idx_project[record.project_id].append(record.artifact_id)
        self._idx_type[record.artifact_type.value].append(record.artifact_id)
        return ResultFactory.ok(record)

    def promote(self, artifact_id: str, actor: str = "") -> BaseResult[ArtifactRecord]:
        """Promote a DRAFT artifact to PROMOTED status.

        Args:
            artifact_id: Artifact to promote.
            actor: Actor performing the promotion.

        Returns:
            :class:`BaseResult` containing the updated :class:`ArtifactRecord`.
        """
        return self._update_status(artifact_id, ArtifactStatus.PROMOTED, actor)

    def archive(self, artifact_id: str, actor: str = "") -> BaseResult[ArtifactRecord]:
        """Archive an artifact."""
        return self._update_status(artifact_id, ArtifactStatus.ARCHIVED, actor)

    def supersede(self, artifact_id: str, actor: str = "") -> BaseResult[ArtifactRecord]:
        """Mark an artifact as superseded by a newer version."""
        return self._update_status(artifact_id, ArtifactStatus.SUPERSEDED, actor)

    # ------------------------------------------------------------------
    # Read API
    # ------------------------------------------------------------------

    def get_record(self, artifact_id: str) -> BaseResult[ArtifactRecord]:
        """Retrieve a catalog record by ID."""
        record = self._catalog.get(artifact_id)
        if record is None:
            return ResultFactory.fail("ERR_ARTIFACT_NOT_FOUND", f"Artifact '{artifact_id}' not found.")
        return ResultFactory.ok(record)

    def read_content(self, artifact_id: str) -> BaseResult[bytes]:
        """Read artifact bytes from storage.

        Args:
            artifact_id: Artifact to read.

        Returns:
            :class:`BaseResult` containing the raw bytes.
        """
        record = self._catalog.get(artifact_id)
        if record is None:
            return ResultFactory.fail("ERR_ARTIFACT_NOT_FOUND", f"Artifact '{artifact_id}' not found.")
        try:
            content = self._storage.read(record.uri)
        except FileNotFoundError as exc:
            return ResultFactory.fail("ERR_ARTIFACT_NOT_IN_STORAGE", str(exc))
        return ResultFactory.ok(content)

    def list_for_run(self, run_id: str) -> BaseResult[list[ArtifactRecord]]:
        """List all artifacts produced by a run."""
        ids = self._idx_run.get(run_id, [])
        records = [self._catalog[aid] for aid in ids if aid in self._catalog]
        return ResultFactory.ok(records)

    def list_for_project(
        self,
        project_id: str,
        artifact_type: ArtifactType | None = None,
        status: ArtifactStatus | None = None,
    ) -> BaseResult[list[ArtifactRecord]]:
        """List artifacts for a project with optional filters."""
        ids = self._idx_project.get(project_id, [])
        records = [self._catalog[aid] for aid in ids if aid in self._catalog]
        if artifact_type:
            records = [r for r in records if r.artifact_type == artifact_type]
        if status:
            records = [r for r in records if r.status == status]
        return ResultFactory.ok(records)

    def verify_content_hash(self, artifact_id: str) -> BaseResult[bool]:
        """Verify that storage content matches the registered content hash.

        Args:
            artifact_id: Artifact to verify.

        Returns:
            :class:`BaseResult` containing ``True`` if hash matches.
        """
        record = self._catalog.get(artifact_id)
        if record is None:
            return ResultFactory.fail("ERR_ARTIFACT_NOT_FOUND", f"Artifact '{artifact_id}' not found.")
        if not record.content_hash:
            return ResultFactory.ok(True)  # No hash recorded -- nothing to verify.
        content_result = self.read_content(artifact_id)
        if not content_result.success:
            return content_result  # type: ignore[return-value]
        actual_hash = compute_content_hash(content_result.data)
        return ResultFactory.ok(actual_hash == record.content_hash)

    def health_check(self) -> BaseResult[dict[str, Any]]:
        """Return catalog health statistics."""
        return ResultFactory.ok({
            "status": "ok",
            "n_artifacts": len(self._catalog),
            "n_projects": len(self._idx_project),
            "n_runs": len(self._idx_run),
        })

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _update_status(
        self, artifact_id: str, new_status: ArtifactStatus, actor: str
    ) -> BaseResult[ArtifactRecord]:
        record = self._catalog.get(artifact_id)
        if record is None:
            return ResultFactory.fail("ERR_ARTIFACT_NOT_FOUND", f"Artifact '{artifact_id}' not found.")
        updated = record.model_copy(update={"status": new_status})
        self._catalog[artifact_id] = updated
        self._logger.info(
            "artifact.status_updated",
            extra={"artifact_id": artifact_id, "status": new_status, "actor": actor},
        )
        return ResultFactory.ok(updated)
