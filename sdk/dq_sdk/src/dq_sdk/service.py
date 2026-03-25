"""dq_sdk.service -- DQService: run checks and produce DQReport."""

from __future__ import annotations

import logging
from typing import Any

from dq_sdk.models import DQCheckResult, DQCheckStatus, DQReport

logger = logging.getLogger(__name__)


class DQService:
    """Runs DQ checks and assembles :class:`~dq_sdk.models.DQReport` objects.

    Args:
        observability_service: Optional observability service.
    """

    def __init__(self, observability_service: Any = None) -> None:
        self._obs = observability_service
        self._reports: dict[str, DQReport] = {}

    def run_report(
        self,
        report_id: str,
        snapshot_id: str,
        run_id: str,
        project_id: str,
        check_results: list[DQCheckResult],
        created_by: str = "",
        artifact_id: str = "",
    ) -> Any:
        """Assemble and store a DQ report from pre-computed check results.

        Args:
            report_id: Unique report identifier.
            snapshot_id: Dataset snapshot this report covers.
            run_id: MDLC run.
            project_id: Project.
            check_results: List of :class:`DQCheckResult`.
            created_by: Actor who ran the checks.
            artifact_id: Artifact ID storing this report.

        Returns:
            Result with :class:`DQReport`.
        """
        try:
            pass_count = sum(1 for c in check_results if c.status == DQCheckStatus.PASS)
            warn_count = sum(1 for c in check_results if c.status == DQCheckStatus.WARN)
            fail_count = sum(1 for c in check_results if c.status == DQCheckStatus.FAIL)
            blocking = [c.check_id for c in check_results if c.is_blocking and c.status == DQCheckStatus.FAIL]

            if blocking:
                overall = DQCheckStatus.FAIL
            elif fail_count > 0 or warn_count > 0:
                overall = DQCheckStatus.WARN
            else:
                overall = DQCheckStatus.PASS

            report = DQReport(
                report_id=report_id,
                snapshot_id=snapshot_id,
                run_id=run_id,
                project_id=project_id,
                check_results=check_results,
                pass_count=pass_count,
                warn_count=warn_count,
                fail_count=fail_count,
                blocking_failures=blocking,
                overall_status=overall,
                created_by=created_by,
                artifact_id=artifact_id,
            )
            self._reports[report_id] = report
            logger.info("dq_service.report_created", extra={"report_id": report_id, "overall": overall})
            return self._ok(report)
        except Exception as exc:
            return self._fail("ERR_REPORT", str(exc))

    def get_report(self, report_id: str) -> Any:
        """Retrieve a DQ report.

        Args:
            report_id: Report identifier.

        Returns:
            Result with :class:`DQReport`.
        """
        r = self._reports.get(report_id)
        if r is None:
            return self._fail("ERR_NOT_FOUND", f"Report '{report_id}' not found.")
        return self._ok(r)

    def health_check(self) -> dict[str, Any]:
        """Return health status."""
        return {"status": "ok", "service": "DQService", "report_count": len(self._reports)}

    @staticmethod
    def _ok(data: Any) -> Any:
        class _R:
            def __init__(self, d: Any) -> None:
                self.success = True; self.data = d; self.error_code = None
        return _R(data)

    @staticmethod
    def _fail(code: str, msg: str) -> Any:
        class _R:
            def __init__(self, c: str, m: str) -> None:
                self.success = False; self.data = None; self.error_code = c; self.error_message = m
        return _R(code, msg)
