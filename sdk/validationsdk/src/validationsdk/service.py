"""validationsdk.service -- ValidationService: public facade for validation lifecycle.

Wires together:
- :class:`~validationsdk.finding_registry.FindingRegistry`
- :class:`~validationsdk.evidence_store.EvidenceStore`
- :class:`~validationsdk.conclusion_engine.ConclusionEngine`
- :class:`~validationsdk.remediation_tracker.RemediationTracker`

All public methods return :class:`~platform_contracts.results.BaseResult`.
"""

from __future__ import annotations

import logging
from typing import Any

from validationsdk.conclusion_engine import ConclusionEngine
from validationsdk.evidence_store import EvidenceStore
from validationsdk.finding_registry import FindingRegistry
from validationsdk.models import (
    ConclusionCategory,
    EvidenceRecord,
    FindingStatus,
    RemediationAction,
    RemediationStatus,
    ValidationConclusion,
    ValidationFinding,
    ValidationRun,
    ValidationScope,
)
from validationsdk.remediation_tracker import RemediationTracker

logger = logging.getLogger(__name__)


def _ok(data: Any = None) -> Any:
    try:
        from platform_contracts.results import BaseResult, ResultFactory
        return ResultFactory.ok(data)
    except ImportError:
        class _R:
            def __init__(self, d: Any) -> None:
                self.success = True
                self.data = d
                self.error_code = None
                self.error_message = None
        return _R(data)


def _fail(code: str, msg: str) -> Any:
    try:
        from platform_contracts.results import ResultFactory
        return ResultFactory.fail(code, msg)
    except ImportError:
        class _R:
            def __init__(self, c: str, m: str) -> None:
                self.success = False
                self.data = None
                self.error_code = c
                self.error_message = m
        return _R(code, msg)


class ValidationService:
    """Public facade for the full validation lifecycle.

    Args:
        observability_service: Optional :class:`~observabilitysdk.service.ObservabilityService`.
        audit_service: Optional :class:`~auditsdk.service.AuditService`.
        evidence_completeness_threshold: Threshold for inconclusive conclusion. Default: 0.6.
        strict_mode: When True, HIGH findings also cause FAIL. Default: False.
    """

    def __init__(
        self,
        observability_service: Any = None,
        audit_service: Any = None,
        evidence_completeness_threshold: float = 0.6,
        strict_mode: bool = False,
    ) -> None:
        self._obs = observability_service
        self._audit = audit_service
        self._engine = ConclusionEngine(evidence_completeness_threshold, strict_mode)
        # scope_id → registry/store/tracker
        self._scopes: dict[str, ValidationScope] = {}
        self._finding_registries: dict[str, FindingRegistry] = {}
        self._evidence_stores: dict[str, EvidenceStore] = {}
        self._remediation_trackers: dict[str, RemediationTracker] = {}
        self._conclusions: dict[str, ValidationConclusion] = {}
        self._runs: dict[str, ValidationRun] = {}

    # ------------------------------------------------------------------
    # Scope management
    # ------------------------------------------------------------------

    def create_scope(self, scope: ValidationScope) -> Any:
        """Register a new validation scope.

        Args:
            scope: :class:`ValidationScope` to register.

        Returns:
            Result with the scope_id.
        """
        try:
            if scope.scope_id in self._scopes:
                return _fail("ERR_SCOPE_EXISTS", f"Scope '{scope.scope_id}' already exists.")
            self._scopes[scope.scope_id] = scope
            self._finding_registries[scope.scope_id] = FindingRegistry(scope.scope_id)
            self._evidence_stores[scope.scope_id] = EvidenceStore(scope.scope_id)
            self._remediation_trackers[scope.scope_id] = RemediationTracker(scope.scope_id)
            run = ValidationRun(
                validation_run_id=scope.scope_id,
                scope=scope,
            )
            self._runs[scope.scope_id] = run

            self._emit("validation.scope.created", scope.run_id, scope.scope_id)
            logger.info("validation_service.scope_created", extra={"scope_id": scope.scope_id})
            return _ok(scope.scope_id)
        except Exception as exc:
            return _fail("ERR_CREATE_SCOPE", str(exc))

    def get_scope(self, scope_id: str) -> Any:
        """Retrieve a validation scope.

        Args:
            scope_id: Scope identifier.

        Returns:
            Result with :class:`ValidationScope`.
        """
        scope = self._scopes.get(scope_id)
        if scope is None:
            return _fail("ERR_NOT_FOUND", f"Scope '{scope_id}' not found.")
        return _ok(scope)

    # ------------------------------------------------------------------
    # Evidence
    # ------------------------------------------------------------------

    def submit_evidence(self, record: EvidenceRecord) -> Any:
        """Submit evidence for a scope.

        Args:
            record: :class:`EvidenceRecord` to submit.

        Returns:
            Result with the evidence_id.
        """
        try:
            store = self._evidence_stores.get(record.scope_id)
            if store is None:
                return _fail("ERR_SCOPE_NOT_FOUND", f"Scope '{record.scope_id}' not found.")
            store.submit(record)
            self._update_run_evidence(record.scope_id, record.evidence_id)
            self._emit("validation.evidence.submitted", record.scope_id, record.scope_id)
            return _ok(record.evidence_id)
        except Exception as exc:
            return _fail("ERR_SUBMIT_EVIDENCE", str(exc))

    def get_evidence_completeness(self, scope_id: str, required_types: list[str]) -> Any:
        """Compute evidence completeness for a scope.

        Args:
            scope_id: Scope identifier.
            required_types: Required evidence type strings.

        Returns:
            Result with completeness score (float 0.0–1.0).
        """
        store = self._evidence_stores.get(scope_id)
        if store is None:
            return _fail("ERR_NOT_FOUND", f"Scope '{scope_id}' not found.")
        return _ok(store.completeness(required_types))

    # ------------------------------------------------------------------
    # Findings
    # ------------------------------------------------------------------

    def raise_finding(self, finding: ValidationFinding) -> Any:
        """Register a new finding.

        Args:
            finding: :class:`ValidationFinding` to register.

        Returns:
            Result with the finding_id.
        """
        try:
            registry = self._finding_registries.get(finding.scope_id)
            if registry is None:
                return _fail("ERR_SCOPE_NOT_FOUND", f"Scope '{finding.scope_id}' not found.")
            registry.register(finding)
            self._update_run_findings(finding.scope_id, finding.finding_id)
            self._emit("validation.finding.raised", finding.run_id, finding.scope_id)
            return _ok(finding.finding_id)
        except Exception as exc:
            return _fail("ERR_RAISE_FINDING", str(exc))

    def update_finding_status(
        self,
        scope_id: str,
        finding_id: str,
        new_status: FindingStatus,
        updated_by: str = "",
        notes: str = "",
    ) -> Any:
        """Transition a finding to a new status.

        Args:
            scope_id: Scope identifier.
            finding_id: Finding identifier.
            new_status: Target :class:`FindingStatus`.
            updated_by: Actor making the change.
            notes: Optional notes.

        Returns:
            Result with updated :class:`ValidationFinding`.
        """
        try:
            registry = self._finding_registries.get(scope_id)
            if registry is None:
                return _fail("ERR_NOT_FOUND", f"Scope '{scope_id}' not found.")
            updated = registry.update_status(finding_id, new_status, updated_by, notes)
            return _ok(updated)
        except KeyError:
            return _fail("ERR_NOT_FOUND", f"Finding '{finding_id}' not found.")
        except Exception as exc:
            return _fail("ERR_UPDATE_FINDING", str(exc))

    def get_findings(self, scope_id: str) -> Any:
        """Return all findings for a scope.

        Args:
            scope_id: Scope identifier.

        Returns:
            Result with list of :class:`ValidationFinding`.
        """
        registry = self._finding_registries.get(scope_id)
        if registry is None:
            return _fail("ERR_NOT_FOUND", f"Scope '{scope_id}' not found.")
        return _ok(registry.list_all())

    # ------------------------------------------------------------------
    # Remediation
    # ------------------------------------------------------------------

    def create_remediation(self, action: RemediationAction) -> Any:
        """Register a remediation action.

        Args:
            action: :class:`RemediationAction` to register.

        Returns:
            Result with action_id.
        """
        try:
            tracker = self._remediation_trackers.get(action.scope_id)
            if tracker is None:
                return _fail("ERR_SCOPE_NOT_FOUND", f"Scope '{action.scope_id}' not found.")
            tracker.create(action)
            return _ok(action.action_id)
        except Exception as exc:
            return _fail("ERR_CREATE_REMEDIATION", str(exc))

    def update_remediation_status(
        self,
        scope_id: str,
        action_id: str,
        new_status: RemediationStatus,
        resolution_notes: str = "",
    ) -> Any:
        """Transition a remediation action to a new status.

        Args:
            scope_id: Scope identifier.
            action_id: Action identifier.
            new_status: Target :class:`RemediationStatus`.
            resolution_notes: Notes on resolution.

        Returns:
            Result with updated :class:`RemediationAction`.
        """
        try:
            tracker = self._remediation_trackers.get(scope_id)
            if tracker is None:
                return _fail("ERR_NOT_FOUND", f"Scope '{scope_id}' not found.")
            updated = tracker.update_status(action_id, new_status, resolution_notes)
            return _ok(updated)
        except KeyError:
            return _fail("ERR_NOT_FOUND", f"Action '{action_id}' not found.")
        except Exception as exc:
            return _fail("ERR_UPDATE_REMEDIATION", str(exc))

    # ------------------------------------------------------------------
    # Conclusion
    # ------------------------------------------------------------------

    def conclude(
        self,
        scope_id: str,
        conclusion_id: str,
        required_evidence_types: list[str],
        concluded_by: str = "",
        audit_id: str = "",
    ) -> Any:
        """Derive and store a validation conclusion.

        Args:
            scope_id: Scope to conclude.
            conclusion_id: Unique conclusion identifier.
            required_evidence_types: Evidence types needed for completeness score.
            concluded_by: Actor drawing the conclusion.
            audit_id: Backing audit record.

        Returns:
            Result with :class:`ValidationConclusion`.
        """
        try:
            scope = self._scopes.get(scope_id)
            if scope is None:
                return _fail("ERR_NOT_FOUND", f"Scope '{scope_id}' not found.")

            registry = self._finding_registries[scope_id]
            store = self._evidence_stores[scope_id]
            completeness = store.completeness(required_evidence_types)
            findings = registry.list_all()

            conclusion = self._engine.derive(
                conclusion_id=conclusion_id,
                scope_id=scope_id,
                run_id=scope.run_id,
                project_id=scope.project_id,
                findings=findings,
                evidence_completeness_score=completeness,
                concluded_by=concluded_by,
                audit_id=audit_id,
            )
            self._conclusions[scope_id] = conclusion

            # Update run record.
            run = self._runs[scope_id]
            updated_run = run.model_copy(update={
                "conclusion": conclusion,
                "status": "concluded",
            })
            self._runs[scope_id] = updated_run

            self._emit("validation.conclusion.derived", scope.run_id, scope_id)
            logger.info(
                "validation_service.concluded",
                extra={
                    "scope_id": scope_id,
                    "category": conclusion.category,
                    "completeness": completeness,
                },
            )
            return _ok(conclusion)
        except Exception as exc:
            return _fail("ERR_CONCLUDE", str(exc))

    def get_conclusion(self, scope_id: str) -> Any:
        """Retrieve the conclusion for a scope.

        Args:
            scope_id: Scope identifier.

        Returns:
            Result with :class:`ValidationConclusion` (or None if not yet concluded).
        """
        conclusion = self._conclusions.get(scope_id)
        if conclusion is None:
            return _fail("ERR_NOT_CONCLUDED", f"Scope '{scope_id}' has not been concluded yet.")
        return _ok(conclusion)

    def get_run(self, scope_id: str) -> Any:
        """Return the full :class:`ValidationRun` for a scope.

        Args:
            scope_id: Scope identifier.

        Returns:
            Result with :class:`ValidationRun`.
        """
        run = self._runs.get(scope_id)
        if run is None:
            return _fail("ERR_NOT_FOUND", f"No validation run for scope '{scope_id}'.")
        return _ok(run)

    def health_check(self) -> dict[str, Any]:
        """Return health status.

        Returns:
            Dict with status and scope count.
        """
        return {"status": "ok", "service": "ValidationService", "scope_count": len(self._scopes)}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _emit(self, event_type: str, run_id: str, scope_id: str) -> None:
        if self._obs is None:
            return
        try:
            self._obs.emit_simple(
                event_type=event_type,
                run_id=run_id,
                stage_name="validation",
                metadata={"scope_id": scope_id},
            )
        except Exception as exc:
            logger.warning("validation_service.emit_failed", extra={"error": str(exc)})

    def _update_run_evidence(self, scope_id: str, evidence_id: str) -> None:
        run = self._runs.get(scope_id)
        if run and evidence_id not in run.evidence_ids:
            self._runs[scope_id] = run.model_copy(
                update={"evidence_ids": [*run.evidence_ids, evidence_id]}
            )

    def _update_run_findings(self, scope_id: str, finding_id: str) -> None:
        run = self._runs.get(scope_id)
        if run and finding_id not in run.finding_ids:
            self._runs[scope_id] = run.model_copy(
                update={"finding_ids": [*run.finding_ids, finding_id]}
            )
