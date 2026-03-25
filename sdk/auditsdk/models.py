"""Audit SDK typed models.

Defines AuditRecord mapped to configs/schemas/audit_event.schema.json.
All records are immutable and append-only.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sdk.platform_core.schemas.base_model_base import BaseModelBase


class AuditRecord(BaseModelBase):
    """Immutable audit record for a governance-critical event.

    Maps to configs/schemas/audit_event.schema.json.

    Args:
        audit_id: Unique audit record identifier.
        audit_type: Type of audit event (decision/approval/exception/signoff/
            override/waiver/escalation/config_change).
        timestamp: UTC creation timestamp.
        actor: Actor who triggered this event.
        stage_name: Stage in which this event occurred.
        run_id: Parent run identifier.
        project_id: Parent project identifier.
        schema_version: Audit schema version.
        preceding_audit_id: Previous audit record for chaining.
        decision_payload: Structured decision payload (for decision type).
        approval_payload: Structured approval payload (for approval type).
        exception_payload: Structured exception payload (for exception type).
        reason: Human-readable reason / justification.
        immutable: Whether this record is locked (always True at creation).
    """

    audit_id: str
    audit_type: str
    timestamp: Optional[datetime] = None
    actor: str
    stage_name: Optional[str] = None
    run_id: Optional[str] = None
    project_id: Optional[str] = None
    schema_version: str = "1.0"
    preceding_audit_id: Optional[str] = None
    decision_payload: Optional[Dict[str, Any]] = None
    approval_payload: Optional[Dict[str, Any]] = None
    exception_payload: Optional[Dict[str, Any]] = None
    reason: str = ""
    immutable: bool = True


class AuditBundle(BaseModelBase):
    """Collection of audit records for export or review.

    Args:
        run_id: Run identifier for this bundle.
        project_id: Project identifier.
        records: Ordered list of AuditRecord dicts (chain order).
        total_count: Total number of records.
        exported_at: UTC export timestamp.
    """

    run_id: Optional[str] = None
    project_id: Optional[str] = None
    records: List[Dict[str, Any]] = []
    total_count: int = 0
    exported_at: Optional[datetime] = None


AUDIT_TYPES = frozenset({
    "decision",
    "approval",
    "exception",
    "signoff",
    "override",
    "waiver",
    "escalation",
    "config_change",
})
