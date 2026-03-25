"""reporting_sdk.service -- ReportingService: report assembly and lifecycle."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from reporting_sdk.models import ReportPack, ReportStatus, ReportType, ReportSection

logger = logging.getLogger(__name__)


class ReportingService:
    """Assembles and manages :class:`~reporting_sdk.models.ReportPack` objects.

    Args:
        observability_service: Optional observability service.
    """

    def __init__(self, observability_service: Any = None) -> None:
        self._obs = observability_service
        self._reports: dict[str, ReportPack] = {}

    def create_report(self, pack: ReportPack) -> Any:
        """Register a new report pack.

        Args:
            pack: :class:`ReportPack` to register.

        Returns:
            Result with report_id.
        """
        try:
            self._reports[pack.report_id] = pack
            logger.info("reporting_service.report_created", extra={"report_id": pack.report_id, "type": pack.report_type})
            return self._ok(pack.report_id)
        except Exception as exc:
            return self._fail("ERR_CREATE", str(exc))

    def add_section(self, report_id: str, section: ReportSection) -> Any:
        """Add a section to an existing draft report.

        Args:
            report_id: Report to update.
            section: :class:`ReportSection` to add.

        Returns:
            Result with updated :class:`ReportPack`.
        """
        pack = self._reports.get(report_id)
        if pack is None:
            return self._fail("ERR_NOT_FOUND", f"Report '{report_id}' not found.")
        if pack.status != ReportStatus.DRAFT:
            return self._fail("ERR_FROZEN", f"Report '{report_id}' is not in DRAFT status.")

        updated = pack.model_copy(update={"sections": [*pack.sections, section]})
        self._reports[report_id] = updated
        return self._ok(updated)

    def update_status(self, report_id: str, new_status: ReportStatus, actor: str = "") -> Any:
        """Transition a report to a new status.

        Args:
            report_id: Report to update.
            new_status: Target :class:`ReportStatus`.
            actor: Actor making the change.

        Returns:
            Result with updated :class:`ReportPack`.
        """
        pack = self._reports.get(report_id)
        if pack is None:
            return self._fail("ERR_NOT_FOUND", f"Report '{report_id}' not found.")
        update: dict[str, Any] = {"status": new_status}
        if new_status == ReportStatus.PUBLISHED:
            update["published_at"] = datetime.now(timezone.utc)
        updated = pack.model_copy(update=update)
        self._reports[report_id] = updated
        logger.info("reporting_service.status_updated", extra={"report_id": report_id, "status": new_status, "actor": actor})
        return self._ok(updated)

    def get_report(self, report_id: str) -> Any:
        """Retrieve a report pack.

        Args:
            report_id: Report identifier.

        Returns:
            Result with :class:`ReportPack`.
        """
        pack = self._reports.get(report_id)
        if pack is None:
            return self._fail("ERR_NOT_FOUND", f"Report '{report_id}' not found.")
        return self._ok(pack)

    def render_markdown(self, report_id: str) -> Any:
        """Render a report as a markdown string.

        Args:
            report_id: Report identifier.

        Returns:
            Result with markdown string.
        """
        result = self.get_report(report_id)
        if not result.success:
            return result
        pack: ReportPack = result.data
        lines = [f"# {pack.title}", f"*Type: {pack.report_type.value} | Status: {pack.status.value}*", ""]
        for section in pack.ordered_sections:
            lines.append(f"## {section.title}")
            lines.append(section.content)
            if section.evidence_refs:
                lines.append(f"*Evidence: {', '.join(section.evidence_refs)}*")
            lines.append("")
        return self._ok("\n".join(lines))

    def list_for_run(self, run_id: str) -> Any:
        """Return all reports for a run.

        Args:
            run_id: Run identifier.

        Returns:
            Result with list of :class:`ReportPack`.
        """
        return self._ok([p for p in self._reports.values() if p.run_id == run_id])

    def health_check(self) -> dict[str, Any]:
        """Return health status."""
        return {"status": "ok", "service": "ReportingService", "report_count": len(self._reports)}

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
