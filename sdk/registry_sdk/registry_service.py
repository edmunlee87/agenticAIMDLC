"""RegistryService — primary registry SDK service class.

Responsibilities:
- Register and retrieve projects, runs, skills, and SDKs.
- Search the registry by various filters.
- Maintain in-memory stores (pluggable to persistent backends later).
- All material methods return BaseResult.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Optional

from sdk.platform_core.schemas.base_result import BaseResult
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider
from sdk.platform_core.services.base_service import BaseRegistryService

from .models import ProjectRecord, RunRecord, SDKMetadata, SkillMetadata

logger = logging.getLogger(__name__)


class RegistryService(BaseRegistryService):
    """Registry SDK service: register and retrieve platform entities.

    Manages in-memory registries for projects, runs, skills, and SDKs.
    All stores are keyed by their primary identifier.

    Args:
        run_id: Optional run_id for audit correlation.
        actor: Actor identifier.

    Examples:
        >>> svc = RegistryService()
        >>> result = svc.register_project(
        ...     project_id="proj_001",
        ...     project_name="LGD Basel IV",
        ...     domain="lgd",
        ...     owner="analyst_01",
        ... )
        >>> assert result.is_success
    """

    SDK_NAME: str = "registry_sdk"

    def __init__(
        self,
        run_id: Optional[str] = None,
        actor: str = "system",
    ) -> None:
        super().__init__(sdk_name=self.SDK_NAME)
        self._run_id = run_id or IDFactory.run_id()
        self._actor = actor
        self._projects: Dict[str, ProjectRecord] = {}
        self._runs: Dict[str, RunRecord] = {}
        self._skills: Dict[str, SkillMetadata] = {}
        self._sdks: Dict[str, SDKMetadata] = {}

    # ------------------------------------------------------------------
    # Project registry
    # ------------------------------------------------------------------

    def register_project(
        self,
        project_id: str,
        project_name: str,
        domain: str,
        owner: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ) -> BaseResult:
        """Register a new project in the registry.

        Args:
            project_id: Unique project identifier.
            project_name: Human-readable name.
            domain: Model domain.
            owner: Actor who owns this project.
            description: Optional description.
            tags: Optional metadata tags.

        Returns:
            :class:`BaseResult` with ``data["project_id"]`` on success.
        """
        self._log_start("register_project", project_id=project_id)
        try:
            if project_id in self._projects:
                result = self._build_result(
                    function_name="register_project",
                    status="failure",
                    message=f"Project '{project_id}' is already registered.",
                    errors=[f"Duplicate project_id: {project_id}"],
                    agent_hint="Use a unique project_id or call get_project instead.",
                    workflow_hint="no_stage_change",
                    audit_hint="skip_audit",
                    observability_hint="registry_duplicate",
                )
                self._log_finish("register_project", result)
                return result
            record = ProjectRecord(
                project_id=project_id,
                project_name=project_name,
                domain=domain,
                owner=owner,
                description=description,
                created_at=TimeProvider.now(),
                tags=tags or {},
            )
            self._projects[project_id] = record
            result = self._build_result(
                function_name="register_project",
                status="success",
                message=f"Project '{project_id}' registered.",
                data={"project_id": project_id},
                agent_hint="Project registered. Proceed with register_run.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="registry_project_registered",
            )
        except Exception as exc:
            result = self._handle_exception("register_project", exc)
        self._log_finish("register_project", result)
        return result

    def get_project(self, project_id: str) -> BaseResult:
        """Retrieve a project record by project_id.

        Args:
            project_id: Unique project identifier.

        Returns:
            :class:`BaseResult` with ``data["project"]`` containing the
            :class:`ProjectRecord` dict, or failure if not found.
        """
        self._log_start("get_project", project_id=project_id)
        record = self._projects.get(project_id)
        if record is None:
            result = self._build_result(
                function_name="get_project",
                status="failure",
                message=f"Project '{project_id}' not found.",
                errors=[f"Unknown project_id: {project_id}"],
                agent_hint="Verify the project_id or call register_project first.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="registry_not_found",
            )
        else:
            result = self._build_result(
                function_name="get_project",
                status="success",
                message=f"Project '{project_id}' retrieved.",
                data={"project": record.to_dict()},
                agent_hint=f"Project domain={record.domain}, owner={record.owner}.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="registry_project_retrieved",
            )
        self._log_finish("get_project", result)
        return result

    # ------------------------------------------------------------------
    # Run registry
    # ------------------------------------------------------------------

    def register_run(
        self,
        run_id: str,
        project_id: str,
        actor: str,
        config_version: Optional[str] = None,
        environment: Optional[str] = None,
        domain: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ) -> BaseResult:
        """Register a new run within a project.

        Args:
            run_id: Unique run identifier.
            project_id: Parent project identifier.
            actor: Actor initiating the run.
            config_version: Config schema_version used for this run.
            environment: Deployment environment.
            domain: Model domain.
            tags: Optional metadata tags.

        Returns:
            :class:`BaseResult` with ``data["run_id"]`` on success.
        """
        self._log_start("register_run", run_id=run_id)
        try:
            if project_id not in self._projects:
                result = self._build_result(
                    function_name="register_run",
                    status="failure",
                    message=f"Project '{project_id}' not found.",
                    errors=[f"Cannot register run for unknown project: {project_id}"],
                    agent_hint="Register the project before registering a run.",
                    workflow_hint="no_stage_change",
                    audit_hint="skip_audit",
                    observability_hint="registry_not_found",
                )
                self._log_finish("register_run", result)
                return result
            if run_id in self._runs:
                result = self._build_result(
                    function_name="register_run",
                    status="failure",
                    message=f"Run '{run_id}' is already registered.",
                    errors=[f"Duplicate run_id: {run_id}"],
                    agent_hint="Use a unique run_id.",
                    workflow_hint="no_stage_change",
                    audit_hint="skip_audit",
                    observability_hint="registry_duplicate",
                )
                self._log_finish("register_run", result)
                return result
            record = RunRecord(
                run_id=run_id,
                project_id=project_id,
                actor=actor,
                started_at=TimeProvider.now(),
                config_version=config_version,
                environment=environment,
                domain=domain,
                tags=tags or {},
            )
            self._runs[run_id] = record
            # Link run to project
            self._projects[project_id].run_ids.append(run_id)
            result = self._build_result(
                function_name="register_run",
                status="success",
                message=f"Run '{run_id}' registered under project '{project_id}'.",
                data={"run_id": run_id},
                agent_hint="Run registered. Proceed with workflow bootstrap.",
                workflow_hint="transition next_stage=session_bootstrap",
                audit_hint="skip_audit",
                observability_hint="registry_run_registered",
            )
        except Exception as exc:
            result = self._handle_exception("register_run", exc)
        self._log_finish("register_run", result)
        return result

    def get_run(self, run_id: str) -> BaseResult:
        """Retrieve a run record by run_id.

        Args:
            run_id: Unique run identifier.

        Returns:
            :class:`BaseResult` with ``data["run"]`` on success.
        """
        self._log_start("get_run", run_id=run_id)
        record = self._runs.get(run_id)
        if record is None:
            result = self._build_result(
                function_name="get_run",
                status="failure",
                message=f"Run '{run_id}' not found.",
                errors=[f"Unknown run_id: {run_id}"],
                agent_hint="Verify the run_id.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="registry_not_found",
            )
        else:
            result = self._build_result(
                function_name="get_run",
                status="success",
                message=f"Run '{run_id}' retrieved.",
                data={"run": record.to_dict()},
                agent_hint=f"Run project={record.project_id}, status={record.status}.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="registry_run_retrieved",
            )
        self._log_finish("get_run", result)
        return result

    # ------------------------------------------------------------------
    # Skill / SDK metadata registry
    # ------------------------------------------------------------------

    def register_skill_metadata(self, metadata: SkillMetadata) -> BaseResult:
        """Register or overwrite a skill metadata record.

        Args:
            metadata: :class:`SkillMetadata` instance.

        Returns:
            :class:`BaseResult` with ``data["skill_name"]`` on success.
        """
        self._log_start("register_skill_metadata", skill_name=metadata.skill_name)
        self._skills[metadata.skill_name] = metadata
        result = self._build_result(
            function_name="register_skill_metadata",
            status="success",
            message=f"Skill '{metadata.skill_name}' metadata registered.",
            data={"skill_name": metadata.skill_name},
            agent_hint=f"Skill {metadata.skill_name} registered in category {metadata.skill_category}.",
            workflow_hint="no_stage_change",
            audit_hint="skip_audit",
            observability_hint="registry_skill_registered",
        )
        self._log_finish("register_skill_metadata", result)
        return result

    def register_sdk_metadata(self, metadata: SDKMetadata) -> BaseResult:
        """Register or overwrite an SDK metadata record.

        Args:
            metadata: :class:`SDKMetadata` instance.

        Returns:
            :class:`BaseResult` with ``data["sdk_name"]`` on success.
        """
        self._log_start("register_sdk_metadata", sdk_name=metadata.sdk_name)
        self._sdks[metadata.sdk_name] = metadata
        result = self._build_result(
            function_name="register_sdk_metadata",
            status="success",
            message=f"SDK '{metadata.sdk_name}' metadata registered.",
            data={"sdk_name": metadata.sdk_name},
            agent_hint=f"SDK {metadata.sdk_name} layer={metadata.sdk_layer} registered.",
            workflow_hint="no_stage_change",
            audit_hint="skip_audit",
            observability_hint="registry_sdk_registered",
        )
        self._log_finish("register_sdk_metadata", result)
        return result

    # ------------------------------------------------------------------
    # BaseRegistryService abstract method implementations
    # ------------------------------------------------------------------

    def register(self, entity_type: str, entity_id: str, payload: Dict[str, Any]) -> BaseResult:
        """Generic register dispatch. Delegates to type-specific methods."""
        self._log_start("register", entity_type=entity_type, entity_id=entity_id)
        try:
            if entity_type == "project":
                result = self.register_project(
                    project_id=entity_id,
                    project_name=payload.get("project_name", entity_id),
                    domain=payload.get("domain", "generic"),
                    owner=payload.get("owner", self._actor),
                    description=payload.get("description"),
                    tags=payload.get("tags"),
                )
            elif entity_type == "run":
                result = self.register_run(
                    run_id=entity_id,
                    project_id=payload["project_id"],
                    actor=payload.get("actor", self._actor),
                )
            else:
                result = self._build_result(
                    function_name="register",
                    status="failure",
                    message=f"Unsupported entity_type for generic register: {entity_type}",
                    errors=[f"Unsupported: {entity_type}"],
                    agent_hint="Use type-specific register methods.",
                    workflow_hint="no_stage_change",
                    audit_hint="skip_audit",
                    observability_hint="registry_unsupported",
                )
        except Exception as exc:
            result = self._handle_exception("register", exc)
        return result

    def get(self, entity_type: str, entity_id: str) -> BaseResult:
        """Generic get dispatch. Delegates to type-specific methods."""
        if entity_type == "project":
            return self.get_project(entity_id)
        if entity_type == "run":
            return self.get_run(entity_id)
        return self._build_result(
            function_name="get",
            status="failure",
            message=f"Unsupported entity_type: {entity_type}",
            errors=[f"Unsupported: {entity_type}"],
            agent_hint="Use one of: project, run.",
            workflow_hint="no_stage_change",
            audit_hint="skip_audit",
            observability_hint="registry_unsupported",
        )

    def search(self, entity_type: str, filters: Dict[str, Any]) -> BaseResult:
        """Generic search dispatch. Delegates to search_registry."""
        return self.search_registry(entity_type=entity_type, filters=filters)

    def search_registry(
        self,
        entity_type: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> BaseResult:
        """Search the registry for entities matching the given filters.

        Args:
            entity_type: One of 'project', 'run', 'skill', 'sdk'.
            filters: Dict of field -> value filters. Supports exact match only.

        Returns:
            :class:`BaseResult` with ``data["results"]`` as a list of matching
            entity dicts.
        """
        self._log_start("search_registry", entity_type=entity_type)
        entity_map: Dict[str, Dict[str, Any]] = {
            "project": {k: v.to_dict() for k, v in self._projects.items()},
            "run": {k: v.to_dict() for k, v in self._runs.items()},
            "skill": {k: v.to_dict() for k, v in self._skills.items()},
            "sdk": {k: v.to_dict() for k, v in self._sdks.items()},
        }
        if entity_type not in entity_map:
            result = self._build_result(
                function_name="search_registry",
                status="failure",
                message=f"Unknown entity_type '{entity_type}'.",
                errors=[f"entity_type must be one of: {list(entity_map.keys())}"],
                agent_hint="Use one of: project, run, skill, sdk.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="registry_search_failed",
            )
            self._log_finish("search_registry", result)
            return result
        store = entity_map[entity_type]
        results = list(store.values())
        if filters:
            results = [
                r for r in results
                if all(r.get(k) == v for k, v in filters.items())
            ]
        result = self._build_result(
            function_name="search_registry",
            status="success",
            message=f"Found {len(results)} {entity_type} records.",
            data={"results": results, "count": len(results)},
            agent_hint=f"{len(results)} {entity_type} records match filters.",
            workflow_hint="no_stage_change",
            audit_hint="skip_audit",
            observability_hint="registry_search",
        )
        self._log_finish("search_registry", result)
        return result
