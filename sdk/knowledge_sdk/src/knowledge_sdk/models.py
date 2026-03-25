"""knowledge_sdk.models -- knowledge object model and promotion workflow contracts.

Knowledge objects are curated, versioned artifacts that capture distilled
insights, policies, templates, and decisions for reuse across MDLC runs.
They follow a draft → reviewed → promoted → deprecated lifecycle.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeObjectType(str, Enum):
    """Category of a knowledge object."""
    POLICY = "policy"
    TEMPLATE = "template"
    METHODOLOGY = "methodology"
    DECISION_RECORD = "decision_record"
    FINDINGS_SUMMARY = "findings_summary"
    BENCHMARK = "benchmark"
    GLOSSARY_TERM = "glossary_term"
    RUNBOOK = "runbook"


class KnowledgeObjectStatus(str, Enum):
    """Promotion lifecycle status."""
    DRAFT = "draft"
    REVIEWED = "reviewed"
    PROMOTED = "promoted"
    DEPRECATED = "deprecated"


class KnowledgeObject(BaseModel):
    """An immutable, versioned knowledge object.

    Args:
        object_id: Unique identifier.
        object_type: :class:`KnowledgeObjectType`.
        title: Human-readable title.
        content: Full content (markdown or plain text).
        version: Semantic version string.
        status: :class:`KnowledgeObjectStatus`.
        project_id: Project scope (empty = global).
        model_type: Domain model type scope (empty = global).
        stage_name: Stage scope (empty = any stage).
        role_ids: Roles that can access this object (empty = all).
        tags: Searchable tags.
        source_run_id: Run that produced this knowledge.
        source_artifact_id: Artifact ID backing this object.
        author: Author actor ID.
        reviewed_by: Reviewer actor ID.
        promoted_by: Actor who promoted this object.
        created_at: Creation timestamp.
        promoted_at: Promotion timestamp.
        deprecated_at: Deprecation timestamp.
        superseded_by: ID of the superseding knowledge object.
        metadata: Arbitrary metadata.
    """

    model_config = ConfigDict(frozen=True)

    object_id: str
    object_type: KnowledgeObjectType
    title: str
    content: str = ""
    version: str = "1.0.0"
    status: KnowledgeObjectStatus = KnowledgeObjectStatus.DRAFT
    project_id: str = ""
    model_type: str = ""
    stage_name: str = ""
    role_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    source_run_id: str = ""
    source_artifact_id: str = ""
    author: str = ""
    reviewed_by: str = ""
    promoted_by: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    promoted_at: datetime | None = None
    deprecated_at: datetime | None = None
    superseded_by: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
