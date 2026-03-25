"""AuditService -- immutable decision chain with checksum verification.

All governance decisions, approvals, exceptions, and stage transitions pass
through AuditService. Records are chained via ``preceding_audit_id`` and
each is checksummed at write time.

Querying supports full chain reconstruction, project/run filters, and
tamper detection.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

from platform_contracts.enums import AuditType
from platform_contracts.fragments import ActorRecord, PolicyContextRef
from platform_contracts.results import BaseResult, ResultFactory
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.services.base import BaseService
from platform_core.utils.id_factory import IDFactory, id_factory
from platform_core.utils.time_provider import TimeProvider, time_provider

from auditsdk.models import AuditRecord

logger = logging.getLogger(__name__)


class AuditService(BaseService):
    """Immutable governance audit trail with decision chaining.

    Maintains an append-only store of :class:`~auditsdk.models.AuditRecord`
    objects, each checksummed and chained to the previous record in the same
    project.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        id_factory_: Injectable :class:`IDFactory`.
        time_provider_: Injectable :class:`TimeProvider`.
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        id_factory_: IDFactory | None = None,
        time_provider_: TimeProvider | None = None,
    ) -> None:
        super().__init__(bundle=bundle, id_factory_=id_factory_, time_provider_=time_provider_)
        self._store: dict[str, AuditRecord] = {}
        # project_id -> last audit_id (for chaining)
        self._chain_tail: dict[str, str] = {}
        # run_id -> [audit_ids], project_id -> [audit_ids]
        self._idx_run: dict[str, list[str]] = defaultdict(list)
        self._idx_project: dict[str, list[str]] = defaultdict(list)

    # ------------------------------------------------------------------
    # Write API
    # ------------------------------------------------------------------

    def record(
        self,
        audit_type: AuditType,
        actor: ActorRecord,
        stage_name: str,
        run_id: str,
        project_id: str,
        payload: dict[str, Any] | None = None,
        session_id: str = "",
        trace_id: str = "",
        correlation_id: str = "",
        policy_context: PolicyContextRef | None = None,
        skill_version: str = "",
        tool_version: str = "",
        environment: str = "",
    ) -> BaseResult[str]:
        """Create, checksum, chain, and store an audit record.

        Args:
            audit_type: Type of governance action.
            actor: Acting subject.
            stage_name: Active MDLC stage.
            run_id: Active run.
            project_id: Active project.
            payload: Structured type-specific payload.
            session_id: UI/agent session.
            trace_id: Distributed trace ID.
            correlation_id: Business correlation ID.
            policy_context: Active policy context reference.
            skill_version: Active skill version.
            tool_version: Active tool version.
            environment: Deployment environment.

        Returns:
            :class:`BaseResult` containing the new ``audit_id``.
        """
        audit_id = self._id_factory.audit_id()
        preceding = self._chain_tail.get(project_id, "")

        # Build without checksum first to compute it.
        record_without_checksum = AuditRecord(
            audit_id=audit_id,
            audit_type=audit_type,
            timestamp=self._time_provider.now(),
            actor=actor,
            stage_name=stage_name,
            run_id=run_id,
            project_id=project_id,
            session_id=session_id,
            trace_id=trace_id,
            correlation_id=correlation_id,
            policy_context=policy_context,
            preceding_audit_id=preceding,
            payload=payload or {},
            skill_version=skill_version,
            tool_version=tool_version,
            environment=environment,
        )
        checksum = record_without_checksum.compute_checksum()
        # Re-create with checksum embedded (Pydantic frozen model requires new instance).
        record = record_without_checksum.model_copy(update={"checksum": checksum})

        self._store[audit_id] = record
        self._chain_tail[project_id] = audit_id
        self._idx_run[run_id].append(audit_id)
        self._idx_project[project_id].append(audit_id)

        self._logger.info(
            "audit.record_written",
            extra={
                "audit_id": audit_id,
                "audit_type": audit_type,
                "project_id": project_id,
                "run_id": run_id,
                "stage_name": stage_name,
                "preceding": preceding or "ROOT",
            },
        )
        return ResultFactory.ok(audit_id)

    # ------------------------------------------------------------------
    # Query API
    # ------------------------------------------------------------------

    def get_record(self, audit_id: str) -> BaseResult[AuditRecord]:
        """Retrieve a single audit record by ID."""
        record = self._store.get(audit_id)
        if record is None:
            return ResultFactory.fail("ERR_AUDIT_NOT_FOUND", f"Audit record '{audit_id}' not found.")
        return ResultFactory.ok(record)

    def get_chain_for_project(self, project_id: str) -> BaseResult[list[AuditRecord]]:
        """Return the full ordered audit chain for a project.

        Args:
            project_id: Project identifier.

        Returns:
            :class:`BaseResult` containing the audit chain in insertion order.
        """
        ids = self._idx_project.get(project_id, [])
        records = [self._store[aid] for aid in ids if aid in self._store]
        return ResultFactory.ok(records)

    def get_chain_for_run(self, run_id: str) -> BaseResult[list[AuditRecord]]:
        """Return audit records for a specific run."""
        ids = self._idx_run.get(run_id, [])
        records = [self._store[aid] for aid in ids if aid in self._store]
        return ResultFactory.ok(records)

    def verify_chain_integrity(self, project_id: str) -> BaseResult[dict[str, Any]]:
        """Verify all checksums in a project's audit chain.

        Args:
            project_id: Project identifier.

        Returns:
            :class:`BaseResult` with ``{"valid": bool, "n_records": int, "tampered_ids": list}``.
        """
        chain_result = self.get_chain_for_project(project_id)
        if not chain_result.success:
            return chain_result  # type: ignore[return-value]

        chain = chain_result.data
        tampered = []
        for record in chain:
            if not record.verify_checksum():
                tampered.append(record.audit_id)
                self._logger.error(
                    "audit.checksum_mismatch",
                    extra={"audit_id": record.audit_id, "project_id": project_id},
                )

        return ResultFactory.ok({
            "valid": len(tampered) == 0,
            "n_records": len(chain),
            "tampered_ids": tampered,
            "project_id": project_id,
        })

    def health_check(self) -> BaseResult[dict[str, Any]]:
        """Return store health statistics."""
        return ResultFactory.ok({
            "status": "ok",
            "n_records": len(self._store),
            "n_projects": len(self._idx_project),
            "n_runs": len(self._idx_run),
        })
