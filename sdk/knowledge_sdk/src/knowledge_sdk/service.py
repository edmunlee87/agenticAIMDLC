"""knowledge_sdk.service -- KnowledgeService: knowledge object registry and promotion workflow."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from knowledge_sdk.models import KnowledgeObject, KnowledgeObjectStatus, KnowledgeObjectType

logger = logging.getLogger(__name__)


class KnowledgeService:
    """Registry and promotion workflow for :class:`~knowledge_sdk.models.KnowledgeObject` objects.

    Args:
        observability_service: Optional observability service.
    """

    def __init__(self, observability_service: Any = None) -> None:
        self._obs = observability_service
        self._objects: dict[str, KnowledgeObject] = {}
        self._history: dict[str, list[KnowledgeObject]] = {}
        self._tag_index: dict[str, list[str]] = {}

    def register(self, obj: KnowledgeObject) -> Any:
        """Register a new knowledge object.

        Args:
            obj: :class:`KnowledgeObject` to register.

        Returns:
            Result with object_id.
        """
        try:
            if obj.object_id in self._objects:
                return self._fail("ERR_EXISTS", f"Knowledge object '{obj.object_id}' already exists.")
            self._objects[obj.object_id] = obj
            self._history[obj.object_id] = [obj]
            for tag in obj.tags:
                self._tag_index.setdefault(tag, []).append(obj.object_id)
            logger.info("knowledge_service.registered", extra={"object_id": obj.object_id, "type": obj.object_type})
            return self._ok(obj.object_id)
        except Exception as exc:
            return self._fail("ERR_REGISTER", str(exc))

    def promote(self, object_id: str, promoted_by: str) -> Any:
        """Promote a knowledge object from REVIEWED → PROMOTED.

        Args:
            object_id: Object to promote.
            promoted_by: Actor performing promotion.

        Returns:
            Result with updated :class:`KnowledgeObject`.
        """
        obj = self._objects.get(object_id)
        if obj is None:
            return self._fail("ERR_NOT_FOUND", f"Object '{object_id}' not found.")
        if obj.status != KnowledgeObjectStatus.REVIEWED:
            return self._fail("ERR_STATUS", f"Object must be REVIEWED before promotion (current: {obj.status}).")
        updated = obj.model_copy(update={
            "status": KnowledgeObjectStatus.PROMOTED,
            "promoted_by": promoted_by,
            "promoted_at": datetime.now(timezone.utc),
        })
        self._objects[object_id] = updated
        self._history[object_id].append(updated)
        logger.info("knowledge_service.promoted", extra={"object_id": object_id, "promoted_by": promoted_by})
        return self._ok(updated)

    def review(self, object_id: str, reviewed_by: str) -> Any:
        """Mark a DRAFT knowledge object as REVIEWED.

        Args:
            object_id: Object to review.
            reviewed_by: Actor performing review.

        Returns:
            Result with updated :class:`KnowledgeObject`.
        """
        obj = self._objects.get(object_id)
        if obj is None:
            return self._fail("ERR_NOT_FOUND", f"Object '{object_id}' not found.")
        if obj.status != KnowledgeObjectStatus.DRAFT:
            return self._fail("ERR_STATUS", f"Object must be DRAFT to review (current: {obj.status}).")
        updated = obj.model_copy(update={"status": KnowledgeObjectStatus.REVIEWED, "reviewed_by": reviewed_by})
        self._objects[object_id] = updated
        self._history[object_id].append(updated)
        return self._ok(updated)

    def deprecate(self, object_id: str, superseded_by: str | None = None) -> Any:
        """Deprecate a knowledge object.

        Args:
            object_id: Object to deprecate.
            superseded_by: ID of superseding object (optional).

        Returns:
            Result with updated :class:`KnowledgeObject`.
        """
        obj = self._objects.get(object_id)
        if obj is None:
            return self._fail("ERR_NOT_FOUND", f"Object '{object_id}' not found.")
        updated = obj.model_copy(update={
            "status": KnowledgeObjectStatus.DEPRECATED,
            "deprecated_at": datetime.now(timezone.utc),
            "superseded_by": superseded_by,
        })
        self._objects[object_id] = updated
        self._history[object_id].append(updated)
        return self._ok(updated)

    def search(
        self,
        tags: list[str] | None = None,
        model_type: str | None = None,
        stage_name: str | None = None,
        object_type: KnowledgeObjectType | None = None,
        status: KnowledgeObjectStatus = KnowledgeObjectStatus.PROMOTED,
    ) -> Any:
        """Search the knowledge registry.

        Args:
            tags: Filter by any of these tags.
            model_type: Filter by model type.
            stage_name: Filter by stage name.
            object_type: Filter by knowledge object type.
            status: Filter by status. Default: PROMOTED.

        Returns:
            Result with list of matching :class:`KnowledgeObject`.
        """
        results = list(self._objects.values())

        if status:
            results = [o for o in results if o.status == status]
        if tags:
            tag_set = set(tags)
            results = [o for o in results if tag_set & set(o.tags)]
        if model_type:
            results = [o for o in results if not o.model_type or o.model_type == model_type]
        if stage_name:
            results = [o for o in results if not o.stage_name or o.stage_name == stage_name]
        if object_type:
            results = [o for o in results if o.object_type == object_type]

        return self._ok(results)

    def get(self, object_id: str) -> Any:
        """Retrieve a knowledge object.

        Args:
            object_id: Object identifier.

        Returns:
            Result with :class:`KnowledgeObject`.
        """
        obj = self._objects.get(object_id)
        if obj is None:
            return self._fail("ERR_NOT_FOUND", f"Object '{object_id}' not found.")
        return self._ok(obj)

    def health_check(self) -> dict[str, Any]:
        """Return health status."""
        return {"status": "ok", "service": "KnowledgeService", "object_count": len(self._objects)}

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
