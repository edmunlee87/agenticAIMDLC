"""monitoring_sdk.models -- model monitoring drift and alert contracts."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DriftSeverity(str, Enum):
    """Severity of detected drift."""
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    """Lifecycle status of a monitoring alert."""
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class DriftRecord(BaseModel):
    """A single drift observation for a model/feature.

    Args:
        drift_id: Unique drift identifier.
        run_id: MDLC run this drift belongs to.
        project_id: Project.
        metric_name: Drift metric (e.g. ``"psi"``, ``"csi"``, ``"ks"``).
        feature_name: Feature or model output being tracked.
        reference_period: Reference period label (e.g. ``"2023-Q1"``).
        monitoring_period: Current monitoring period label.
        value: Drift statistic value.
        threshold: Threshold used for classification.
        severity: :class:`DriftSeverity`.
        observed_at: When drift was detected.
        metadata: Additional metadata.
    """

    model_config = ConfigDict(frozen=True)

    drift_id: str
    run_id: str
    project_id: str
    metric_name: str
    feature_name: str = ""
    reference_period: str = ""
    monitoring_period: str = ""
    value: float
    threshold: float
    severity: DriftSeverity = DriftSeverity.NONE
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict)


class MonitoringAlert(BaseModel):
    """An alert triggered by model monitoring.

    Args:
        alert_id: Unique alert identifier.
        run_id: Run.
        project_id: Project.
        drift_id: Drift record that triggered this alert.
        alert_type: Category (e.g. ``"drift"``, ``"threshold"``, ``"periodic_review"``).
        title: Short alert title.
        description: Detailed description.
        severity: :class:`DriftSeverity`.
        status: :class:`AlertStatus`.
        triggered_at: When the alert was raised.
        resolved_at: When the alert was resolved.
        assigned_to: Actor responsible for resolution.
        requires_periodic_review: Whether this triggers a mandatory periodic review.
    """

    model_config = ConfigDict(frozen=True)

    alert_id: str
    run_id: str
    project_id: str
    drift_id: str = ""
    alert_type: str = "drift"
    title: str = ""
    description: str = ""
    severity: DriftSeverity = DriftSeverity.LOW
    status: AlertStatus = AlertStatus.OPEN
    triggered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: datetime | None = None
    assigned_to: str = ""
    requires_periodic_review: bool = False
