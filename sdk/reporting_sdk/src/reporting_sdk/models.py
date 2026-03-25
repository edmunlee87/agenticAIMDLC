"""reporting_sdk.models -- report pack contracts for technical, executive, and committee reports."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ReportType(str, Enum):
    """Category of report."""
    TECHNICAL = "technical"
    EXECUTIVE = "executive"
    COMMITTEE = "committee"
    VALIDATION = "validation"
    MONITORING = "monitoring"


class ReportStatus(str, Enum):
    """Lifecycle status of a report."""
    DRAFT = "draft"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    PUBLISHED = "published"


class ReportSection(BaseModel):
    """A single section in a report.

    Args:
        section_id: Unique section identifier.
        title: Section title.
        content: Section body (markdown or structured text).
        evidence_refs: Artifact IDs supporting this section.
        order: Display order (lower = earlier).
    """

    model_config = ConfigDict(frozen=True)

    section_id: str
    title: str
    content: str = ""
    evidence_refs: list[str] = Field(default_factory=list)
    order: int = 0


class ReportPack(BaseModel):
    """A complete report pack for a model/run.

    Args:
        report_id: Unique report identifier.
        report_type: :class:`ReportType`.
        title: Report title.
        run_id: MDLC run.
        project_id: Project.
        candidate_id: Candidate version being reported on.
        sections: Ordered list of report sections.
        status: :class:`ReportStatus`.
        authors: Actor IDs who authored this report.
        reviewers: Actor IDs who reviewed this report.
        created_at: Creation timestamp.
        published_at: Publication timestamp (if published).
        artifact_id: Artifact ID storing the rendered report.
        metadata: Additional metadata.
    """

    model_config = ConfigDict(frozen=True)

    report_id: str
    report_type: ReportType
    title: str
    run_id: str
    project_id: str
    candidate_id: str = ""
    sections: list[ReportSection] = Field(default_factory=list)
    status: ReportStatus = ReportStatus.DRAFT
    authors: list[str] = Field(default_factory=list)
    reviewers: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    published_at: datetime | None = None
    artifact_id: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def ordered_sections(self) -> list[ReportSection]:
        """Return sections sorted by order field."""
        return sorted(self.sections, key=lambda s: s.order)
