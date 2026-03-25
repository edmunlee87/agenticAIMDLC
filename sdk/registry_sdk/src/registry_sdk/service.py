"""RegistryService -- project, run, and skill registration facade.

Provides deterministic, auditable registration of all material MDLC objects.
All writes are logged as structured events and protected from duplicate IDs.
"""

from __future__ import annotations

import logging
from typing import Any

from platform_contracts.results import BaseResult, ResultFactory
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.services.base import BaseService
from platform_core.utils.id_factory import IDFactory, id_factory
from platform_core.utils.time_provider import TimeProvider, time_provider

from registry_sdk.models import ProjectRecord, RunRecord, SkillRecord
from registry_sdk.store import InMemoryStore

logger = logging.getLogger(__name__)


class RegistryService(BaseService):
    """Registry facade for projects, runs, and skills.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        project_store: Backing store for project records. Defaults to :class:`InMemoryStore`.
        run_store: Backing store for run records.
        skill_store: Backing store for skill records.
        id_factory_: Injectable :class:`IDFactory`.
        time_provider_: Injectable :class:`TimeProvider`.

    Examples:
        >>> svc = RegistryService(bundle=bundle)
        >>> result = svc.register_project(ProjectRecord(project_id="p1", name="My Model"))
        >>> project_id = result.unwrap()
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        project_store: InMemoryStore | None = None,
        run_store: InMemoryStore | None = None,
        skill_store: InMemoryStore | None = None,
        id_factory_: IDFactory | None = None,
        time_provider_: TimeProvider | None = None,
    ) -> None:
        super().__init__(bundle=bundle, id_factory_=id_factory_, time_provider_=time_provider_)
        self._projects = project_store or InMemoryStore("projects")
        self._runs = run_store or InMemoryStore("runs")
        self._skills = skill_store or InMemoryStore("skills")

    # ------------------------------------------------------------------
    # Project operations
    # ------------------------------------------------------------------

    def register_project(self, record: ProjectRecord) -> BaseResult[str]:
        """Register a new project.

        Args:
            record: Project record to register.

        Returns:
            :class:`BaseResult` containing the ``project_id``.
        """
        if self._projects.exists(record.project_id):
            return ResultFactory.fail(
                "ERR_PROJECT_EXISTS",
                f"Project '{record.project_id}' is already registered.",
            )
        self._projects.put(record.project_id, record)
        self._logger.info(
            "registry.project_registered",
            extra={"project_id": record.project_id, "domain": record.domain},
        )
        return ResultFactory.ok(record.project_id)

    def get_project(self, project_id: str) -> BaseResult[ProjectRecord]:
        """Retrieve a project by ID.

        Args:
            project_id: Project identifier.

        Returns:
            :class:`BaseResult` containing the :class:`ProjectRecord`.
        """
        record = self._projects.get(project_id)
        if record is None:
            return ResultFactory.fail(
                "ERR_PROJECT_NOT_FOUND",
                f"Project '{project_id}' not found.",
            )
        return ResultFactory.ok(record)

    def list_projects(self, domain: str | None = None) -> BaseResult[list[ProjectRecord]]:
        """List all registered projects, optionally filtered by domain.

        Args:
            domain: Filter by domain ID.

        Returns:
            :class:`BaseResult` containing a list of :class:`ProjectRecord`.
        """
        if domain:
            records = self._projects.query(domain=domain)
        else:
            records = self._projects.list_all()
        return ResultFactory.ok(records)

    # ------------------------------------------------------------------
    # Run operations
    # ------------------------------------------------------------------

    def register_run(self, record: RunRecord) -> BaseResult[str]:
        """Register a new execution run.

        Args:
            record: Run record to register.

        Returns:
            :class:`BaseResult` containing the ``run_id``.
        """
        if not self._projects.exists(record.project_id):
            return ResultFactory.fail(
                "ERR_PROJECT_NOT_FOUND",
                f"Cannot register run: project '{record.project_id}' not found.",
            )
        if self._runs.exists(record.run_id):
            return ResultFactory.fail(
                "ERR_RUN_EXISTS",
                f"Run '{record.run_id}' is already registered.",
            )
        self._runs.put(record.run_id, record)
        self._logger.info(
            "registry.run_registered",
            extra={"run_id": record.run_id, "project_id": record.project_id},
        )
        return ResultFactory.ok(record.run_id)

    def get_run(self, run_id: str) -> BaseResult[RunRecord]:
        """Retrieve a run by ID."""
        record = self._runs.get(run_id)
        if record is None:
            return ResultFactory.fail("ERR_RUN_NOT_FOUND", f"Run '{run_id}' not found.")
        return ResultFactory.ok(record)

    def list_runs(self, project_id: str) -> BaseResult[list[RunRecord]]:
        """List all runs for a project."""
        if not self._projects.exists(project_id):
            return ResultFactory.fail(
                "ERR_PROJECT_NOT_FOUND", f"Project '{project_id}' not found."
            )
        records = self._runs.query(project_id=project_id)
        return ResultFactory.ok(records)

    def update_run_stage(self, run_id: str, active_stage: str, status: str = "active") -> BaseResult[str]:
        """Update the active stage on a run record (creates a new immutable record).

        Args:
            run_id: Run identifier.
            active_stage: New active stage name.
            status: New status string.

        Returns:
            :class:`BaseResult` with the run_id on success.
        """
        existing = self._runs.get(run_id)
        if existing is None:
            return ResultFactory.fail("ERR_RUN_NOT_FOUND", f"Run '{run_id}' not found.")
        updated = existing.model_copy(update={"active_stage": active_stage, "status": status})
        self._runs.put(run_id, updated)
        self._logger.info(
            "registry.run_stage_updated",
            extra={"run_id": run_id, "active_stage": active_stage, "status": status},
        )
        return ResultFactory.ok(run_id)

    # ------------------------------------------------------------------
    # Skill operations
    # ------------------------------------------------------------------

    def register_skill(self, record: SkillRecord) -> BaseResult[str]:
        """Register a skill.

        Args:
            record: Skill record.

        Returns:
            :class:`BaseResult` containing the ``skill_id``.
        """
        self._skills.put(record.skill_id, record)
        self._logger.info(
            "registry.skill_registered",
            extra={"skill_id": record.skill_id, "skill_type": record.skill_type},
        )
        return ResultFactory.ok(record.skill_id)

    def get_skill(self, skill_id: str) -> BaseResult[SkillRecord]:
        """Retrieve a skill by ID."""
        record = self._skills.get(skill_id)
        if record is None:
            return ResultFactory.fail("ERR_SKILL_NOT_FOUND", f"Skill '{skill_id}' not found.")
        return ResultFactory.ok(record)

    def health_check(self) -> BaseResult[dict[str, Any]]:
        """Return store health statistics."""
        return ResultFactory.ok({
            "status": "ok",
            "n_projects": len(self._projects.list_all()),
            "n_runs": len(self._runs.list_all()),
            "n_skills": len(self._skills.list_all()),
        })
