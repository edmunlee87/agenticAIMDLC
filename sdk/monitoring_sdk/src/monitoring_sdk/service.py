"""monitoring_sdk.service -- MonitoringService: drift detection, alerts, periodic review."""

from __future__ import annotations

import logging
from typing import Any

from monitoring_sdk.models import AlertStatus, DriftRecord, DriftSeverity, MonitoringAlert

logger = logging.getLogger(__name__)


def classify_drift(value: float, moderate_threshold: float = 0.1, high_threshold: float = 0.2, critical_threshold: float = 0.3) -> DriftSeverity:
    """Classify PSI/CSI value into a :class:`DriftSeverity`.

    Args:
        value: Drift statistic.
        moderate_threshold: Default: 0.1.
        high_threshold: Default: 0.2.
        critical_threshold: Default: 0.3.

    Returns:
        :class:`DriftSeverity`.
    """
    if value < moderate_threshold:
        return DriftSeverity.NONE
    if value < high_threshold:
        return DriftSeverity.MODERATE
    if value < critical_threshold:
        return DriftSeverity.HIGH
    return DriftSeverity.CRITICAL


class MonitoringService:
    """Records drift observations and manages monitoring alerts.

    Args:
        observability_service: Optional observability service.
    """

    def __init__(self, observability_service: Any = None) -> None:
        self._obs = observability_service
        self._drifts: dict[str, DriftRecord] = {}
        self._alerts: dict[str, MonitoringAlert] = {}
        self._by_run: dict[str, list[str]] = {}

    def record_drift(self, record: DriftRecord) -> Any:
        """Record a drift observation.

        Args:
            record: :class:`DriftRecord` to store.

        Returns:
            Result with drift_id.
        """
        try:
            self._drifts[record.drift_id] = record
            self._by_run.setdefault(record.run_id, []).append(record.drift_id)
            logger.info("monitoring_service.drift_recorded", extra={"drift_id": record.drift_id, "severity": record.severity})
            return self._ok(record.drift_id)
        except Exception as exc:
            return self._fail("ERR_DRIFT", str(exc))

    def raise_alert(self, alert: MonitoringAlert) -> Any:
        """Register a monitoring alert.

        Args:
            alert: :class:`MonitoringAlert` to register.

        Returns:
            Result with alert_id.
        """
        try:
            self._alerts[alert.alert_id] = alert
            logger.info("monitoring_service.alert_raised", extra={"alert_id": alert.alert_id, "severity": alert.severity})
            return self._ok(alert.alert_id)
        except Exception as exc:
            return self._fail("ERR_ALERT", str(exc))

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str = "") -> Any:
        """Acknowledge a monitoring alert.

        Args:
            alert_id: Alert to acknowledge.
            acknowledged_by: Actor acknowledging.

        Returns:
            Result with updated :class:`MonitoringAlert`.
        """
        alert = self._alerts.get(alert_id)
        if alert is None:
            return self._fail("ERR_NOT_FOUND", f"Alert '{alert_id}' not found.")
        updated = alert.model_copy(update={"status": AlertStatus.ACKNOWLEDGED})
        self._alerts[alert_id] = updated
        return self._ok(updated)

    def get_open_alerts(self, run_id: str | None = None) -> Any:
        """Return all open alerts, optionally filtered by run.

        Args:
            run_id: Optional run filter.

        Returns:
            Result with list of :class:`MonitoringAlert`.
        """
        alerts = [a for a in self._alerts.values() if a.status == AlertStatus.OPEN]
        if run_id:
            alerts = [a for a in alerts if a.run_id == run_id]
        return self._ok(alerts)

    def get_drift_for_run(self, run_id: str) -> Any:
        """Return all drift records for a run.

        Args:
            run_id: Run identifier.

        Returns:
            Result with list of :class:`DriftRecord`.
        """
        ids = self._by_run.get(run_id, [])
        return self._ok([self._drifts[i] for i in ids if i in self._drifts])

    def needs_periodic_review(self, run_id: str) -> bool:
        """Return True if any open alert requires a periodic review.

        Args:
            run_id: Run identifier.

        Returns:
            Boolean.
        """
        return any(
            a.status == AlertStatus.OPEN and a.requires_periodic_review and a.run_id == run_id
            for a in self._alerts.values()
        )

    def health_check(self) -> dict[str, Any]:
        """Return health status."""
        return {"status": "ok", "service": "MonitoringService", "drift_count": len(self._drifts)}

    @staticmethod
    def _ok(data: Any) -> Any:
        class _R:
            def __init__(self, d: Any) -> None:
                self.success = True; self.data = d
        return _R(data)

    @staticmethod
    def _fail(code: str, msg: str) -> Any:
        class _R:
            def __init__(self, c: str, m: str) -> None:
                self.success = False; self.data = None; self.error_code = c; self.error_message = m
        return _R(code, msg)
