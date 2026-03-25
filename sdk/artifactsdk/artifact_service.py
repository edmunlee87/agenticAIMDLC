"""ArtifactService — primary artifact SDK service class.

Responsibilities:
- Register every material artifact with checksum, lineage, and governance fields.
- Retrieve and locate artifacts by ID or filter.
- Validate artifact integrity via checksum verification.
- Build artifact manifests for reporting / committee packs.
- Maintain a lineage graph of artifact relationships.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from sdk.platform_core.schemas.base_result import BaseResult
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider
from sdk.platform_core.services.base_service import BaseService

from .models import ArtifactLineageLink, ArtifactManifest, ArtifactRecord, ChecksumRecord
from .storage_adapter import ArtifactStorageAdapter, InMemoryArtifactStore

logger = logging.getLogger(__name__)

# Default artifact schema version applied to all registered records.
_DEFAULT_SCHEMA_VERSION = "1.0"


class ArtifactService(BaseService):
    """Artifact SDK service: register, retrieve, validate, and trace artifacts.

    Maintains an in-memory registry (backed by a pluggable storage adapter)
    and a lineage graph. Every registered artifact is immutable.

    Args:
        run_id: Default run_id for artifact registration.
        project_id: Default project_id for artifact registration.
        actor: Default producer actor identifier.
        storage_adapter: Pluggable storage backend (defaults to InMemoryArtifactStore).

    Examples:
        >>> svc = ArtifactService(run_id="run_001", project_id="proj_001", actor="analyst")
        >>> result = svc.register_artifact(
        ...     artifact_type="binning_summary",
        ...     artifact_name="var_age_bins_v1",
        ...     stage_name="coarse_classing",
        ...     uri_or_path="/artifacts/bins/var_age_v1.parquet",
        ... )
        >>> assert result.is_success
    """

    SDK_NAME: str = "artifactsdk"

    def __init__(
        self,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        actor: str = "system",
        storage_adapter: Optional[ArtifactStorageAdapter] = None,
    ) -> None:
        super().__init__(sdk_name=self.SDK_NAME)
        self._run_id = run_id or IDFactory.run_id()
        self._project_id = project_id or ""
        self._actor = actor
        self._storage: ArtifactStorageAdapter = storage_adapter or InMemoryArtifactStore()
        # In-memory indexes for fast lookup
        self._by_id: Dict[str, ArtifactRecord] = {}
        self._lineage_links: List[ArtifactLineageLink] = []
        # Version counter per (run_id, artifact_type) for auto-versioning
        self._version_counters: Dict[str, int] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register_artifact(
        self,
        artifact_type: str,
        artifact_name: str,
        stage_name: str,
        uri_or_path: Optional[str] = None,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        actor: Optional[str] = None,
        source_candidate_version_id: Optional[str] = None,
        lineage_parent_ids: Optional[List[str]] = None,
        storage_backend: str = "local",
        retention_policy: Optional[str] = None,
        access_control_ref: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        checksum: Optional[ChecksumRecord] = None,
        raw_bytes: Optional[bytes] = None,
        session_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> BaseResult:
        """Register an artifact and persist it to the storage backend.

        If ``raw_bytes`` is provided and ``checksum`` is None, a SHA-256
        checksum is computed automatically. Lineage links to
        ``lineage_parent_ids`` are recorded automatically.

        Args:
            artifact_type: Logical type (e.g. ``binning_summary``).
            artifact_name: Human-readable artifact name.
            stage_name: Stage that produced this artifact.
            uri_or_path: Storage URI or local path.
            run_id: Overrides service-level run_id.
            project_id: Overrides service-level project_id.
            actor: Overrides service-level actor.
            source_candidate_version_id: Candidate version that produced this.
            lineage_parent_ids: Parent artifact IDs (lineage graph).
            storage_backend: Backend name (local/s3/cml/gcs/azure_blob).
            retention_policy: Retention policy reference.
            access_control_ref: Access control policy reference.
            metadata: Domain-extensible metadata dict.
            checksum: Pre-computed checksum (optional if raw_bytes supplied).
            raw_bytes: Raw artifact bytes for auto-checksum computation.
            session_id: Session identifier.
            trace_id: Trace identifier.
            correlation_id: Correlation identifier.

        Returns:
            :class:`BaseResult` with ``data["artifact_id"]`` and
            ``data["version"]`` on success.
        """
        self._log_start("register_artifact", artifact_type=artifact_type)
        try:
            guard = self._require_fields(
                "register_artifact",
                artifact_type=artifact_type,
                artifact_name=artifact_name,
                stage_name=stage_name,
            )
            if guard:
                return guard

            effective_run_id = run_id or self._run_id
            effective_project_id = project_id or self._project_id
            effective_actor = actor or self._actor

            # Auto-compute checksum if raw bytes provided
            if raw_bytes is not None and checksum is None:
                from .storage_adapter import ChecksumManager
                checksum = ChecksumManager.compute_checksum(raw_bytes)

            # Version resolution
            version_key = f"{effective_run_id}/{artifact_type}"
            version_num = self._version_counters.get(version_key, 0) + 1
            self._version_counters[version_key] = version_num
            version = f"{version_num}.0"

            artifact_id = IDFactory.artifact_id()
            record = ArtifactRecord(
                artifact_id=artifact_id,
                artifact_type=artifact_type,
                artifact_name=artifact_name,
                stage_name=stage_name,
                producer_actor=effective_actor,
                project_id=effective_project_id,
                run_id=effective_run_id,
                timestamp=TimeProvider.now(),
                schema_version=_DEFAULT_SCHEMA_VERSION,
                version=version,
                uri_or_path=uri_or_path,
                checksum=checksum,
                session_id=session_id,
                trace_id=trace_id,
                correlation_id=correlation_id,
                source_candidate_version_id=source_candidate_version_id,
                lineage_parent_ids=lineage_parent_ids or [],
                storage_backend=storage_backend,
                retention_policy=retention_policy,
                access_control_ref=access_control_ref,
                metadata=metadata or {},
            )

            write_result = self._storage.write(artifact_id, record.to_dict())
            if not write_result.is_success:
                result = self._build_result(
                    function_name="register_artifact",
                    status="failure",
                    message=f"Storage write failed for artifact '{artifact_name}'.",
                    errors=write_result.errors,
                    agent_hint="Resolve storage backend error before retrying.",
                    workflow_hint="no_stage_change",
                    audit_hint="register_artifact_failure",
                    observability_hint="artifact_register_failed",
                )
                self._log_finish("register_artifact", result)
                return result

            self._by_id[artifact_id] = record

            # Record lineage links
            for parent_id in (lineage_parent_ids or []):
                self._lineage_links.append(
                    ArtifactLineageLink(
                        parent_id=parent_id,
                        child_id=artifact_id,
                        lineage_type="derived",
                        recorded_at=TimeProvider.now(),
                    )
                )

            result = self._build_result(
                function_name="register_artifact",
                status="success",
                message=f"Artifact '{artifact_id}' ({artifact_type}) registered.",
                data={
                    "artifact_id": artifact_id,
                    "artifact_type": artifact_type,
                    "artifact_name": artifact_name,
                    "version": version,
                    "stage_name": stage_name,
                },
                artifacts_created=[artifact_id],
                agent_hint=f"Artifact registered: {artifact_type} v{version} id={artifact_id}.",
                workflow_hint="no_stage_change",
                audit_hint="register_artifact_success",
                observability_hint="artifact_registered",
            )
        except Exception as exc:
            result = self._handle_exception("register_artifact", exc)
        self._log_finish("register_artifact", result)
        return result

    def get_artifact(self, artifact_id: str) -> BaseResult:
        """Retrieve a registered artifact record by ID.

        Args:
            artifact_id: Artifact identifier (``art_<uuid>``).

        Returns:
            :class:`BaseResult` with ``data["artifact"]`` on success.
        """
        self._log_start("get_artifact", artifact_id=artifact_id)
        record = self._by_id.get(artifact_id)
        if record is None:
            result = self._build_result(
                function_name="get_artifact",
                status="failure",
                message=f"Artifact '{artifact_id}' not found.",
                errors=[f"artifact_id not found: {artifact_id}"],
                agent_hint="Verify artifact_id. It may not have been registered yet.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="artifact_not_found",
            )
        else:
            result = self._build_result(
                function_name="get_artifact",
                status="success",
                message=f"Artifact '{artifact_id}' retrieved.",
                data={"artifact": record.to_dict()},
                agent_hint=f"Artifact {artifact_id} found: type={record.artifact_type}.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="artifact_retrieved",
            )
        self._log_finish("get_artifact", result)
        return result

    def locate_artifact(
        self,
        artifact_type: Optional[str] = None,
        stage_name: Optional[str] = None,
        run_id: Optional[str] = None,
        source_candidate_version_id: Optional[str] = None,
    ) -> BaseResult:
        """Search for artifacts matching filter criteria.

        All supplied filters are applied as AND conditions. If no filters are
        given, all registered artifacts are returned.

        Args:
            artifact_type: Filter by artifact type.
            stage_name: Filter by producing stage.
            run_id: Filter by run identifier.
            source_candidate_version_id: Filter by source candidate version.

        Returns:
            :class:`BaseResult` with ``data["artifacts"]`` and
            ``data["count"]`` on success.
        """
        self._log_start("locate_artifact")
        try:
            matches = list(self._by_id.values())
            if artifact_type:
                matches = [r for r in matches if r.artifact_type == artifact_type]
            if stage_name:
                matches = [r for r in matches if r.stage_name == stage_name]
            if run_id:
                matches = [r for r in matches if r.run_id == run_id]
            if source_candidate_version_id:
                matches = [
                    r for r in matches
                    if r.source_candidate_version_id == source_candidate_version_id
                ]
            result = self._build_result(
                function_name="locate_artifact",
                status="success",
                message=f"Located {len(matches)} artifact(s).",
                data={
                    "artifacts": [r.to_dict() for r in matches],
                    "count": len(matches),
                },
                agent_hint=f"{len(matches)} artifact(s) match supplied filters.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="artifact_located",
            )
        except Exception as exc:
            result = self._handle_exception("locate_artifact", exc)
        self._log_finish("locate_artifact", result)
        return result

    def validate_artifact(
        self,
        artifact_id: str,
        raw_bytes: Optional[bytes] = None,
    ) -> BaseResult:
        """Validate an artifact's integrity via checksum verification.

        If the artifact has no checksum, the result is a success with a warning.
        If ``raw_bytes`` is provided, the checksum is recomputed and compared.
        If ``raw_bytes`` is not provided, the checksum record is confirmed present.

        Args:
            artifact_id: Artifact to validate.
            raw_bytes: Optional raw bytes to recompute the checksum against.

        Returns:
            :class:`BaseResult` indicating validation pass/fail/warning.
        """
        self._log_start("validate_artifact", artifact_id=artifact_id)
        record = self._by_id.get(artifact_id)
        if record is None:
            result = self._build_result(
                function_name="validate_artifact",
                status="failure",
                message=f"Artifact '{artifact_id}' not found for validation.",
                errors=[f"artifact_id not found: {artifact_id}"],
                agent_hint="Artifact must be registered before validation.",
                workflow_hint="no_stage_change",
                audit_hint="validate_artifact_not_found",
                observability_hint="artifact_validate_failed",
            )
            self._log_finish("validate_artifact", result)
            return result

        if record.checksum is None:
            result = self._build_result(
                function_name="validate_artifact",
                status="warning",
                message=f"Artifact '{artifact_id}' has no checksum; integrity unverifiable.",
                warnings=["No checksum registered for this artifact."],
                data={"artifact_id": artifact_id, "checksum_present": False},
                agent_hint="Register artifact with raw_bytes or checksum for full integrity.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="artifact_no_checksum",
            )
            self._log_finish("validate_artifact", result)
            return result

        if raw_bytes is not None:
            from .storage_adapter import ChecksumManager
            valid = ChecksumManager.verify_checksum(raw_bytes, record.checksum)
            if not valid:
                result = self._build_result(
                    function_name="validate_artifact",
                    status="failure",
                    message=f"Checksum mismatch for artifact '{artifact_id}'.",
                    errors=[
                        f"Expected checksum {record.checksum.value} "
                        f"({record.checksum.algorithm}) does not match computed value."
                    ],
                    data={"artifact_id": artifact_id, "checksum_valid": False},
                    agent_hint="Artifact may be corrupted or tampered with.",
                    workflow_hint="block_stage_transition",
                    audit_hint="register_integrity_failure",
                    observability_hint="artifact_checksum_failed",
                )
                self._log_finish("validate_artifact", result)
                return result

        result = self._build_result(
            function_name="validate_artifact",
            status="success",
            message=f"Artifact '{artifact_id}' passed integrity validation.",
            data={"artifact_id": artifact_id, "checksum_valid": True},
            agent_hint="Artifact integrity confirmed.",
            workflow_hint="no_stage_change",
            audit_hint="skip_audit",
            observability_hint="artifact_validated",
        )
        self._log_finish("validate_artifact", result)
        return result

    def build_artifact_manifest(
        self,
        artifact_ids: List[str],
        manifest_type: str = "export_bundle",
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> BaseResult:
        """Build a named artifact manifest for reporting or committee packs.

        Validates that all supplied artifact IDs are registered. Missing IDs
        are reported as errors.

        Args:
            artifact_ids: Ordered list of artifact IDs to include.
            manifest_type: Manifest purpose (e.g. ``committee_pack``,
                ``validation_evidence``, ``export_bundle``).
            run_id: Run scope for this manifest.
            project_id: Project scope for this manifest.
            metadata: Optional manifest-level metadata.

        Returns:
            :class:`BaseResult` with ``data["manifest"]`` on success.
        """
        self._log_start("build_artifact_manifest", manifest_type=manifest_type)
        try:
            missing = [aid for aid in artifact_ids if aid not in self._by_id]
            if missing:
                result = self._build_result(
                    function_name="build_artifact_manifest",
                    status="failure",
                    message=f"Manifest build failed: {len(missing)} artifact(s) not found.",
                    errors=[f"Artifact IDs not registered: {missing}"],
                    agent_hint="Register all artifacts before building a manifest.",
                    workflow_hint="no_stage_change",
                    audit_hint="manifest_build_failure",
                    observability_hint="artifact_manifest_failed",
                )
                self._log_finish("build_artifact_manifest", result)
                return result

            manifest_id = IDFactory._generate("mfst")
            manifest = ArtifactManifest(
                manifest_id=manifest_id,
                manifest_type=manifest_type,
                artifact_ids=artifact_ids,
                artifact_count=len(artifact_ids),
                run_id=run_id or self._run_id,
                project_id=project_id or self._project_id,
                created_at=TimeProvider.now(),
                metadata=metadata or {},
            )
            result = self._build_result(
                function_name="build_artifact_manifest",
                status="success",
                message=f"Manifest '{manifest_id}' built with {len(artifact_ids)} artifact(s).",
                data={"manifest": manifest.to_dict()},
                agent_hint=f"Manifest {manifest_id} ({manifest_type}) ready.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="artifact_manifest_built",
            )
        except Exception as exc:
            result = self._handle_exception("build_artifact_manifest", exc)
        self._log_finish("build_artifact_manifest", result)
        return result

    def link_artifact_lineage(
        self,
        parent_ids: List[str],
        child_id: str,
        lineage_type: str = "derived",
    ) -> BaseResult:
        """Explicitly link parent artifacts to a child artifact.

        Validates that both parent and child artifact IDs are registered.
        Duplicate links are silently skipped.

        Args:
            parent_ids: Parent artifact IDs (upstream).
            child_id: Child artifact ID (downstream).
            lineage_type: Relationship type (e.g. ``derived``, ``transformed``,
                ``aggregated``, ``selected``).

        Returns:
            :class:`BaseResult` with ``data["links_added"]`` on success.
        """
        self._log_start("link_artifact_lineage", child_id=child_id)
        try:
            if child_id not in self._by_id:
                result = self._build_result(
                    function_name="link_artifact_lineage",
                    status="failure",
                    message=f"Child artifact '{child_id}' not found.",
                    errors=[f"child artifact_id not registered: {child_id}"],
                    agent_hint="Register the child artifact before linking lineage.",
                    workflow_hint="no_stage_change",
                    audit_hint="skip_audit",
                    observability_hint="artifact_lineage_failed",
                )
                self._log_finish("link_artifact_lineage", result)
                return result

            missing_parents = [pid for pid in parent_ids if pid not in self._by_id]
            warnings: List[str] = []
            if missing_parents:
                warnings.append(
                    f"Parent IDs not registered and skipped: {missing_parents}"
                )

            existing_pairs = {
                (lnk.parent_id, lnk.child_id) for lnk in self._lineage_links
            }
            links_added = 0
            for parent_id in parent_ids:
                if parent_id in self._by_id and (parent_id, child_id) not in existing_pairs:
                    self._lineage_links.append(
                        ArtifactLineageLink(
                            parent_id=parent_id,
                            child_id=child_id,
                            lineage_type=lineage_type,
                            recorded_at=TimeProvider.now(),
                        )
                    )
                    links_added += 1

            result = self._build_result(
                function_name="link_artifact_lineage",
                status="success",
                message=f"{links_added} lineage link(s) added for child '{child_id}'.",
                data={"child_id": child_id, "links_added": links_added},
                warnings=warnings,
                agent_hint=f"Lineage updated: {links_added} link(s) from {parent_ids} -> {child_id}.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="artifact_lineage_linked",
            )
        except Exception as exc:
            result = self._handle_exception("link_artifact_lineage", exc)
        self._log_finish("link_artifact_lineage", result)
        return result

    def get_artifact_lineage(self, artifact_id: str) -> BaseResult:
        """Return all lineage links involving a given artifact (as parent or child).

        Args:
            artifact_id: Artifact identifier to query lineage for.

        Returns:
            :class:`BaseResult` with ``data["as_parent"]`` (links where this
            artifact is the parent) and ``data["as_child"]`` (links where it
            is the child).
        """
        self._log_start("get_artifact_lineage", artifact_id=artifact_id)
        as_parent = [
            lnk.to_dict() for lnk in self._lineage_links if lnk.parent_id == artifact_id
        ]
        as_child = [
            lnk.to_dict() for lnk in self._lineage_links if lnk.child_id == artifact_id
        ]
        result = self._build_result(
            function_name="get_artifact_lineage",
            status="success",
            message=f"Lineage for artifact '{artifact_id}': {len(as_parent)} downstream, "
                    f"{len(as_child)} upstream link(s).",
            data={"artifact_id": artifact_id, "as_parent": as_parent, "as_child": as_child},
            agent_hint=f"Lineage graph: {len(as_parent)} downstream, {len(as_child)} upstream.",
            workflow_hint="no_stage_change",
            audit_hint="skip_audit",
            observability_hint="artifact_lineage_retrieved",
        )
        self._log_finish("get_artifact_lineage", result)
        return result
