"""Meta-model governance — schema versioning and backward compatibility rules.

Any change to a JSON schema or Pydantic model that appears in
``configs/schemas/`` or ``sdk/platform_core/schemas/`` must go through the
:class:`SchemaChangeRecord` process defined here.

Versioning convention
---------------------
* Schema versions follow ``MAJOR.MINOR`` (e.g. ``"1.0"``, ``"1.1"``).
* **MAJOR** bump: breaking change — field removed, type changed, required
  constraint added to an existing field, enum value removed.
* **MINOR** bump: backward-compatible change — field added (optional),
  enum value added, description updated, constraint relaxed.

Impact assessment checklist
----------------------------
Before merging any MAJOR schema bump, the following must be completed:

1. ``migration_notes`` must be non-empty.
2. All SDKs that reference the schema must have updated tests.
3. A ``SchemaChangeRecord`` entry must be appended to
   ``configs/schemas/CHANGELOG.jsonl`` (append-only).
4. The ``ReviewPayload.structured_edit_schema`` version fields must be
   incremented wherever the schema is used.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sdk.platform_core.schemas.base_model_base import BaseModelBase


class ChangeType(str, Enum):
    """Classification of a schema change."""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


class SchemaChangeRecord(BaseModelBase):
    """Immutable record of a schema change event.

    Args:
        schema_name: JSON/Pydantic schema file name without extension
            (e.g. ``"artifact_registry"``).
        from_version: Previous ``MAJOR.MINOR`` version string.
        to_version: New ``MAJOR.MINOR`` version string.
        change_type: :class:`ChangeType` classification.
        changed_by: Actor (human or service) that made the change.
        timestamp: UTC ISO-8601 timestamp of the change.
        migration_notes: Human-readable notes on how existing data
            records should be migrated.  **Required** for ``MAJOR``
            changes.
        impacted_sdks: List of SDK names that reference this schema and
            were updated.
        review_ref: Optional HITL review ID that approved the change.
        audit_ref: Optional audit event ID generated for the change.

    Raises:
        ValueError: If ``change_type`` is MAJOR and ``migration_notes``
            is empty.

    Examples:
        >>> record = SchemaChangeRecord(
        ...     schema_name="artifact_registry",
        ...     from_version="1.0",
        ...     to_version="2.0",
        ...     change_type=ChangeType.MAJOR,
        ...     changed_by="platform_team",
        ...     timestamp=datetime.utcnow(),
        ...     migration_notes="Field 'uri' renamed to 'uri_or_path'.",
        ...     impacted_sdks=["artifactsdk"],
        ... )
    """

    schema_name: str
    from_version: str
    to_version: str
    change_type: ChangeType
    changed_by: str
    timestamp: datetime
    migration_notes: str = ""
    impacted_sdks: list[str] = []
    review_ref: Optional[str] = None
    audit_ref: Optional[str] = None

    def model_post_init(self, __context: object) -> None:
        """Enforce migration notes requirement for major changes.

        Raises:
            ValueError: If change_type is MAJOR and migration_notes is empty.
        """
        if self.change_type == ChangeType.MAJOR and not self.migration_notes:
            raise ValueError(
                "migration_notes must not be empty for MAJOR schema changes"
            )
