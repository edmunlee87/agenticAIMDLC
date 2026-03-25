"""Registry SDK data models.

All registry records are immutable and versioned. Every record carries
full governance provenance fields.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProjectRecord(BaseModel):
    """A registered model development project.

    Args:
        project_id: Unique project identifier.
        name: Human-readable project name.
        description: Project description.
        domain: Business domain (e.g. ``"credit_risk"``).
        owner_id: Actor ID of the project owner.
        created_at: Creation timestamp.
        metadata: Arbitrary key-value metadata.
        status: Lifecycle status of the project.
    """

    model_config = ConfigDict(frozen=True)

    project_id: str
    name: str
    description: str = ""
    domain: str = ""
    owner_id: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict)
    status: str = "active"

    @field_validator("project_id", "name", mode="before")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("project_id and name must be non-empty")
        return v


class RunRecord(BaseModel):
    """A versioned execution run within a project.

    Args:
        run_id: Unique run identifier.
        project_id: Parent project.
        session_id: UI/agent session that started this run.
        run_version: Monotonic version counter within the project.
        triggered_by: Actor ID who triggered the run.
        started_at: Run start timestamp.
        ended_at: Run end timestamp (None if still active).
        status: Current run status.
        active_stage: Current MDLC stage name.
        config_snapshot_id: Config snapshot ID at run start.
        metadata: Arbitrary metadata.
    """

    model_config = ConfigDict(frozen=True)

    run_id: str
    project_id: str
    session_id: str = ""
    run_version: int = 1
    triggered_by: str = ""
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime | None = None
    status: str = "active"
    active_stage: str = ""
    config_snapshot_id: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class SkillRecord(BaseModel):
    """A registered platform or domain skill.

    Args:
        skill_id: Unique skill identifier.
        display_name: Human-readable name.
        skill_type: ``"platform"``, ``"domain"``, ``"role"``, ``"stage"``, ``"overlay"``.
        version: Semver string.
        description: Skill description.
        compatible_stages: Stages this skill can be used in (empty = all).
        registered_at: Registration timestamp.
    """

    model_config = ConfigDict(frozen=True)

    skill_id: str
    display_name: str = ""
    skill_type: str = "platform"
    version: str = "0.1.0"
    description: str = ""
    compatible_stages: list[str] = Field(default_factory=list)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
