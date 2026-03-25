"""AuditService — primary audit SDK service class.

Responsibilities:
- Write immutable, append-only audit records.
- Register decisions, approvals, exceptions, and sign-offs.
- Chain audit records via preceding_audit_id.
- Export audit bundles for a run.
- Reconstruct audit chains.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from sdk.platform_core.schemas.base_result import BaseResult
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider
from sdk.platform_core.services.base_service import BaseService

from .models import AUDIT_TYPES, AuditBundle, AuditRecord

logger = logging.getLogger(__name__)


class AuditService(BaseService):
    """Audit SDK service: write and retrieve immutable audit records.

    Maintains an append-only in-memory audit log, indexed by audit_id,
    run_id, and project_id. Records are chained via preceding_audit_id.

    Args:
        run_id: Optional run_id for audit correlation.
        actor: Actor identifier.

    Examples:
        >>> svc = AuditService()
        >>> result = svc.register_decision(
        ...     stage_name="model_fitting",
        ...     run_id="run_001",
        ...     project_id="proj_001",
        ...     reason="Analyst selected best-fit model.",
        ... )
        >>> assert result.is_success
    """

    SDK_NAME: str = "auditsdk"

    def __init__(
        self,
        run_id: Optional[str] = None,
        actor: str = "system",
    ) -> None:
        super().__init__(sdk_name=self.SDK_NAME)
        self._run_id = run_id or IDFactory.run_id()
        self._actor = actor
        # Append-only stores
        self._records: List[AuditRecord] = []
        self._by_id: Dict[str, AuditRecord] = {}
        # Last audit ID for chaining
        self._last_audit_id: Optional[str] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def write_audit_record(
        self,
        audit_type: str,
        actor: Optional[str] = None,
        stage_name: Optional[str] = None,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        reason: str = "",
        decision_payload: Optional[Dict[str, Any]] = None,
        approval_payload: Optional[Dict[str, Any]] = None,
        exception_payload: Optional[Dict[str, Any]] = None,
        preceding_audit_id: Optional[str] = None,
    ) -> BaseResult:
        """Write an immutable audit record of any type.

        Args:
            audit_type: One of the AUDIT_TYPES set.
            actor: Overrides service-level actor.
            stage_name: Stage where this event occurred.
            run_id: Run identifier.
            project_id: Project identifier.
            reason: Human-readable justification.
            decision_payload: Decision-specific structured data.
            approval_payload: Approval-specific structured data.
            exception_payload: Exception-specific structured data.
            preceding_audit_id: Explicit chain link (uses last record if None).

        Returns:
            :class:`BaseResult` with ``data["audit_id"]`` on success.
        """
        self._log_start("write_audit_record", audit_type=audit_type)
        try:
            if audit_type not in AUDIT_TYPES:
                result = self._build_result(
                    function_name="write_audit_record",
                    status="failure",
                    message=f"Invalid audit_type '{audit_type}'.",
                    errors=[f"audit_type must be one of: {sorted(AUDIT_TYPES)}"],
                    agent_hint="Use a valid audit_type.",
                    workflow_hint="no_stage_change",
                    audit_hint="skip_audit",
                    observability_hint="audit_invalid_type",
                )
                self._log_finish("write_audit_record", result)
                return result
            audit_id = IDFactory._generate("aud")
            record = AuditRecord(
                audit_id=audit_id,
                audit_type=audit_type,
                timestamp=TimeProvider.now(),
                actor=actor or self._actor,
                stage_name=stage_name,
                run_id=run_id or self._run_id,
                project_id=project_id,
                preceding_audit_id=preceding_audit_id or self._last_audit_id,
                reason=reason,
                decision_payload=decision_payload,
                approval_payload=approval_payload,
                exception_payload=exception_payload,
            )
            self._records.append(record)
            self._by_id[audit_id] = record
            self._last_audit_id = audit_id
            result = self._build_result(
                function_name="write_audit_record",
                status="success",
                message=f"Audit record '{audit_id}' ({audit_type}) written.",
                data={"audit_id": audit_id, "audit_type": audit_type},
                agent_hint=f"Audit record {audit_type} written. audit_id={audit_id}.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="audit_written",
                references={"preceding_audit_id": record.preceding_audit_id or ""},
            )
        except Exception as exc:
            result = self._handle_exception("write_audit_record", exc)
        self._log_finish("write_audit_record", result)
        return result

    def register_decision(
        self,
        stage_name: str,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        reason: str = "",
        decision_payload: Optional[Dict[str, Any]] = None,
        actor: Optional[str] = None,
    ) -> BaseResult:
        """Register a decision audit record.

        Args:
            stage_name: Stage where the decision was made.
            run_id: Run identifier.
            project_id: Project identifier.
            reason: Decision rationale.
            decision_payload: Structured decision data.
            actor: Actor who made the decision.

        Returns:
            :class:`BaseResult` with ``data["audit_id"]``.
        """
        return self.write_audit_record(
            audit_type="decision",
            actor=actor,
            stage_name=stage_name,
            run_id=run_id,
            project_id=project_id,
            reason=reason,
            decision_payload=decision_payload,
        )

    def register_approval(
        self,
        stage_name: str,
        approver: str,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        reason: str = "",
        approval_payload: Optional[Dict[str, Any]] = None,
    ) -> BaseResult:
        """Register an approval audit record.

        Args:
            stage_name: Stage where approval was granted.
            approver: Actor granting approval.
            run_id: Run identifier.
            project_id: Project identifier.
            reason: Approval rationale.
            approval_payload: Structured approval data.

        Returns:
            :class:`BaseResult` with ``data["audit_id"]``.
        """
        return self.write_audit_record(
            audit_type="approval",
            actor=approver,
            stage_name=stage_name,
            run_id=run_id,
            project_id=project_id,
            reason=reason,
            approval_payload=approval_payload,
        )

    def register_exception(
        self,
        stage_name: str,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        reason: str = "",
        exception_payload: Optional[Dict[str, Any]] = None,
        actor: Optional[str] = None,
    ) -> BaseResult:
        """Register an exception audit record.

        Args:
            stage_name: Stage where the exception occurred.
            run_id: Run identifier.
            project_id: Project identifier.
            reason: Exception justification.
            exception_payload: Structured exception data.
            actor: Actor registering the exception.

        Returns:
            :class:`BaseResult` with ``data["audit_id"]``.
        """
        return self.write_audit_record(
            audit_type="exception",
            actor=actor,
            stage_name=stage_name,
            run_id=run_id,
            project_id=project_id,
            reason=reason,
            exception_payload=exception_payload,
        )

    def register_signoff(
        self,
        stage_name: str,
        signatory: str,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        reason: str = "",
    ) -> BaseResult:
        """Register a sign-off audit record.

        Args:
            stage_name: Stage being signed off.
            signatory: Actor performing the sign-off.
            run_id: Run identifier.
            project_id: Project identifier.
            reason: Sign-off notes.

        Returns:
            :class:`BaseResult` with ``data["audit_id"]``.
        """
        return self.write_audit_record(
            audit_type="signoff",
            actor=signatory,
            stage_name=stage_name,
            run_id=run_id,
            project_id=project_id,
            reason=reason,
        )

    def export_audit_bundle(
        self,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> BaseResult:
        """Export all audit records for a run/project as an AuditBundle.

        Args:
            run_id: Filter by run_id (None = all records).
            project_id: Filter by project_id (None = all records).

        Returns:
            :class:`BaseResult` with ``data["bundle"]`` containing an
            :class:`AuditBundle` dict.
        """
        self._log_start("export_audit_bundle", run_id=run_id)
        try:
            records = self._records
            if run_id:
                records = [r for r in records if r.run_id == run_id]
            if project_id:
                records = [r for r in records if r.project_id == project_id]
            bundle = AuditBundle(
                run_id=run_id,
                project_id=project_id,
                records=[r.to_dict() for r in records],
                total_count=len(records),
                exported_at=TimeProvider.now(),
            )
            result = self._build_result(
                function_name="export_audit_bundle",
                status="success",
                message=f"Exported {bundle.total_count} audit records.",
                data={"bundle": bundle.to_dict()},
                agent_hint=f"Audit bundle ready: {bundle.total_count} records.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="audit_bundle_exported",
            )
        except Exception as exc:
            result = self._handle_exception("export_audit_bundle", exc)
        self._log_finish("export_audit_bundle", result)
        return result

    def get_audit_chain(self, leaf_audit_id: str) -> BaseResult:
        """Reconstruct the audit chain from leaf back to root.

        Follows preceding_audit_id links until no prior record exists.

        Args:
            leaf_audit_id: Starting (most recent) audit ID.

        Returns:
            :class:`BaseResult` with ``data["chain"]`` as an ordered list of
            AuditRecord dicts from root to leaf.
        """
        self._log_start("get_audit_chain", audit_id=leaf_audit_id)
        chain: List[Dict[str, Any]] = []
        current_id: Optional[str] = leaf_audit_id
        visited: set = set()
        while current_id and current_id not in visited:
            visited.add(current_id)
            record = self._by_id.get(current_id)
            if record is None:
                break
            chain.append(record.to_dict())
            current_id = record.preceding_audit_id
        chain.reverse()
        result = self._build_result(
            function_name="get_audit_chain",
            status="success",
            message=f"Audit chain of {len(chain)} records.",
            data={"chain": chain, "length": len(chain)},
            agent_hint=f"Chain depth={len(chain)} from leaf={leaf_audit_id}.",
            workflow_hint="no_stage_change",
            audit_hint="skip_audit",
            observability_hint="audit_chain_retrieved",
        )
        self._log_finish("get_audit_chain", result)
        return result
