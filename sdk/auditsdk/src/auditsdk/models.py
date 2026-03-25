"""Audit SDK data models.

AuditRecord is the primary model -- immutable, tamper-evident, and chained
via ``preceding_audit_id`` to form an ordered decision chain.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from platform_contracts.enums import AuditType
from platform_contracts.fragments import ActorRecord, PolicyContextRef


class AuditRecord(BaseModel):
    """Immutable audit record for decisions, approvals, exceptions, and governance actions.

    Chained via ``preceding_audit_id`` so the full decision trail is
    reconstructable in insertion order.

    Args:
        audit_id: Unique audit record identifier.
        audit_type: Type of governance action.
        timestamp: UTC timestamp of the action.
        actor: Who performed the action.
        stage_name: MDLC stage at the time of the action.
        run_id: Run the action belongs to.
        project_id: Project the action belongs to.
        session_id: UI/agent session.
        trace_id: Distributed trace ID.
        correlation_id: Business correlation ID.
        policy_context: Active policy context.
        schema_version: Schema semver.
        preceding_audit_id: Links to the prior record in the decision chain.
        payload: Type-specific payload (see AuditType for expected keys).
        skill_version: Skill version active at audit time.
        tool_version: Tool version active at audit time.
        environment: Deployment environment.
        immutable: Always True -- signals that this record must not be altered.
        checksum: SHA-256 hash of the record content (excluding ``checksum``).
    """

    model_config = ConfigDict(frozen=True)

    audit_id: str
    audit_type: AuditType
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor: ActorRecord
    stage_name: str
    run_id: str
    project_id: str
    session_id: str = ""
    trace_id: str = ""
    correlation_id: str = ""
    policy_context: PolicyContextRef | None = None
    schema_version: str = "1.0.0"
    preceding_audit_id: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)
    skill_version: str = ""
    tool_version: str = ""
    environment: str = ""
    immutable: bool = True
    checksum: str = ""

    @field_validator("audit_id", "stage_name", "run_id", "project_id", mode="before")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("audit_id, stage_name, run_id, project_id must be non-empty")
        return v

    def compute_checksum(self) -> str:
        """Compute SHA-256 of this record's content (excluding checksum field).

        Returns:
            Hex-encoded SHA-256 checksum string.
        """
        data = self.model_dump(exclude={"checksum"})
        serialized = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def verify_checksum(self) -> bool:
        """Return True if the stored checksum matches the computed checksum.

        Returns:
            True when the record has not been tampered with.
        """
        if not self.checksum:
            return False
        return self.checksum == self.compute_checksum()
