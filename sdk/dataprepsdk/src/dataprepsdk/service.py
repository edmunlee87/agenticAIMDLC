"""dataprepsdk.service -- DataPrepService: public facade for data preparation."""

from __future__ import annotations

import logging
from typing import Any

from dataprepsdk.executor import DataPrepExecutor
from dataprepsdk.models import DataPrepRun, DataPrepTemplate
from dataprepsdk.template_registry import TemplateRegistry

logger = logging.getLogger(__name__)


class DataPrepService:
    """Public facade wiring together TemplateRegistry and DataPrepExecutor.

    Args:
        observability_service: Optional observability service.
        artifact_service: Optional artifact service.
    """

    def __init__(
        self,
        observability_service: Any = None,
        artifact_service: Any = None,
    ) -> None:
        self._registry = TemplateRegistry()
        self._executor = DataPrepExecutor(observability_service, artifact_service)
        self._runs: dict[str, DataPrepRun] = {}

    def register_template(self, template: DataPrepTemplate) -> Any:
        """Register a data preparation template.

        Args:
            template: :class:`DataPrepTemplate` to register.

        Returns:
            Result with template_id.
        """
        try:
            self._registry.register(template)
            return self._ok(template.template_id)
        except Exception as exc:
            return self._fail("ERR_REGISTER", str(exc))

    def execute(
        self,
        template_id: str,
        data: Any,
        run_id: str,
        project_id: str,
        executed_by: str = "",
        engine: str = "pandas",
        template_version: str | None = None,
    ) -> Any:
        """Execute a registered template.

        Args:
            template_id: Template to execute.
            data: Input data object.
            run_id: MDLC run identifier.
            project_id: Project identifier.
            executed_by: Actor triggering execution.
            engine: Execution engine. Default: ``"pandas"``.
            template_version: Specific version to execute. Default: latest.

        Returns:
            Result with :class:`DataPrepRun`.
        """
        try:
            template = self._registry.get(template_id, template_version)
        except KeyError as exc:
            return self._fail("ERR_NOT_FOUND", str(exc))

        run = self._executor.execute(template, data, run_id, project_id, executed_by, engine)
        self._runs[run.run_record_id] = run

        if not run.success:
            return self._fail("ERR_EXECUTION", run.error_message)
        return self._ok(run)

    def get_run(self, run_record_id: str) -> Any:
        """Retrieve a data prep run record.

        Args:
            run_record_id: Run record identifier.

        Returns:
            Result with :class:`DataPrepRun`.
        """
        run = self._runs.get(run_record_id)
        if run is None:
            return self._fail("ERR_NOT_FOUND", f"Run '{run_record_id}' not found.")
        return self._ok(run)

    def get_lineage(self, run_record_id: str) -> Any:
        """Return column-level lineage for a run.

        Args:
            run_record_id: Run record identifier.

        Returns:
            Result with list of :class:`~dataprepsdk.models.DataPrepLineageRecord`.
        """
        run = self._runs.get(run_record_id)
        if run is None:
            return self._fail("ERR_NOT_FOUND", f"Run '{run_record_id}' not found.")
        return self._ok(run.lineage)

    def list_templates(self) -> Any:
        """Return all registered templates.

        Returns:
            Result with list of :class:`DataPrepTemplate`.
        """
        return self._ok(self._registry.list_all())

    def health_check(self) -> dict[str, Any]:
        """Return health status."""
        return {
            "status": "ok",
            "service": "DataPrepService",
            "template_count": len(self._registry.list_all()),
            "run_count": len(self._runs),
        }

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
