"""dq_sdk.models -- data quality check results and report contracts."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DQCheckType(str, Enum):
    """Category of a data quality check."""
    SCHEMA = "schema"
    MISSINGNESS = "missingness"
    CONSISTENCY = "consistency"
    DISTRIBUTION = "distribution"
    BUSINESS_RULE = "business_rule"
    REFERENTIAL = "referential"
    UNIQUENESS = "uniqueness"


class DQCheckStatus(str, Enum):
    """Outcome of a DQ check."""
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    SKIP = "skip"


class DQCheckResult(BaseModel):
    """Result of a single DQ check.

    Args:
        check_id: Unique check identifier.
        check_type: :class:`DQCheckType`.
        check_name: Human-readable check name.
        status: :class:`DQCheckStatus`.
        column_name: Column this check targets (empty = table-level).
        value: Computed metric value.
        threshold: Threshold used for pass/fail determination.
        message: Human-readable result message.
        is_blocking: Whether a FAIL on this check blocks further processing.
    """

    model_config = ConfigDict(frozen=True)

    check_id: str
    check_type: DQCheckType
    check_name: str
    status: DQCheckStatus = DQCheckStatus.PASS
    column_name: str = ""
    value: float | None = None
    threshold: float | None = None
    message: str = ""
    is_blocking: bool = False


class DQReport(BaseModel):
    """Aggregated data quality report for a dataset snapshot.

    Args:
        report_id: Unique report identifier.
        snapshot_id: Dataset snapshot this report covers.
        run_id: MDLC run.
        project_id: Project.
        check_results: All check results.
        pass_count: Number of passing checks.
        warn_count: Number of warning checks.
        fail_count: Number of failing checks.
        blocking_failures: Check IDs that are blocking failures.
        overall_status: Aggregated status.
        created_at: Report creation timestamp.
        created_by: Actor who ran the checks.
        artifact_id: Artifact ID storing this report.
    """

    model_config = ConfigDict(frozen=True)

    report_id: str
    snapshot_id: str
    run_id: str
    project_id: str
    check_results: list[DQCheckResult] = Field(default_factory=list)
    pass_count: int = 0
    warn_count: int = 0
    fail_count: int = 0
    blocking_failures: list[str] = Field(default_factory=list)
    overall_status: DQCheckStatus = DQCheckStatus.PASS
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""
    artifact_id: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
