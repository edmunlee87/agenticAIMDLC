"""Registry SDK typed models.

Defines the core domain models for projects, runs, skills, SDKs, policies,
and validation records managed by RegistryService.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sdk.platform_core.schemas.base_model_base import BaseModelBase


class ProjectRecord(BaseModelBase):
    """Registry record for a model development project.

    Args:
        project_id: Unique project identifier.
        project_name: Human-readable project name.
        domain: Model domain (scorecard, time_series, etc.).
        owner: Actor responsible for this project.
        description: Optional description.
        created_at: UTC creation timestamp.
        status: Current status (active/archived/suspended).
        tags: Arbitrary key-value metadata.
        run_ids: Ordered list of run IDs associated with this project.
        governance_context_ref: Reference to active policy context.
    """

    project_id: str
    project_name: str
    domain: str
    owner: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    status: str = "active"
    tags: Dict[str, str] = {}
    run_ids: List[str] = []
    governance_context_ref: Optional[str] = None


class RunRecord(BaseModelBase):
    """Registry record for a single execution run within a project.

    Args:
        run_id: Unique run identifier.
        project_id: Parent project identifier.
        actor: Actor who initiated the run.
        started_at: UTC run start timestamp.
        ended_at: UTC run end timestamp (None if in progress).
        status: Run status (running/completed/failed/suspended).
        current_stage: Current or final stage name.
        config_version: Schema version from loaded config bundle.
        environment: Deployment environment name.
        domain: Model domain for this run.
        artifact_ids: Artifact IDs produced during this run.
        session_ids: Session IDs associated with this run.
        tags: Arbitrary key-value metadata.
    """

    run_id: str
    project_id: str
    actor: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    status: str = "running"
    current_stage: Optional[str] = None
    config_version: Optional[str] = None
    environment: Optional[str] = None
    domain: Optional[str] = None
    artifact_ids: List[str] = []
    session_ids: List[str] = []
    tags: Dict[str, str] = {}


class SkillMetadata(BaseModelBase):
    """Metadata record for a registered platform skill.

    Args:
        skill_name: Unique skill identifier (kebab-case).
        skill_category: Category (platform/role/domain/stage/support).
        description: Human-readable description.
        version: Semantic version string.
        applicable_stages: Stage names this skill can act in.
        applicable_domains: Domains this skill applies to.
        applicable_roles: Roles this skill is available to.
        tool_dependencies: Tool groups this skill requires.
        schema_version: SKILL.md schema version.
    """

    skill_name: str
    skill_category: str = "platform"
    description: Optional[str] = None
    version: str = "0.1.0"
    applicable_stages: List[str] = []
    applicable_domains: List[str] = []
    applicable_roles: List[str] = []
    tool_dependencies: List[str] = []
    schema_version: str = "1.0"


class SDKMetadata(BaseModelBase):
    """Metadata record for a registered platform SDK.

    Args:
        sdk_name: Unique SDK name (e.g. "artifactsdk").
        sdk_layer: Integer layer number (1-7) per layering model.
        primary_service_class: Fully-qualified primary service class path.
        version: SDK version string.
        public_methods: List of public method names.
        dependencies: SDK names this SDK depends on.
        tool_registry_keys: Tool keys registered by this SDK.
    """

    sdk_name: str
    sdk_layer: int = 1
    primary_service_class: Optional[str] = None
    version: str = "0.1.0"
    public_methods: List[str] = []
    dependencies: List[str] = []
    tool_registry_keys: List[str] = []
