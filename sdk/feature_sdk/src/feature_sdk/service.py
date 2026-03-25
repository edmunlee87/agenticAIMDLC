"""feature_sdk.service -- FeatureService: feature registry and lineage."""

from __future__ import annotations

import logging
from typing import Any

from feature_sdk.models import FeatureMetadata, FeatureSet

logger = logging.getLogger(__name__)


class FeatureService:
    """Registry for features and feature sets.

    Args:
        observability_service: Optional observability service.
    """

    def __init__(self, observability_service: Any = None) -> None:
        self._obs = observability_service
        self._features: dict[str, FeatureMetadata] = {}
        self._feature_sets: dict[str, FeatureSet] = {}

    def register_feature(self, feature: FeatureMetadata) -> Any:
        """Register a feature.

        Args:
            feature: :class:`FeatureMetadata` to register.

        Returns:
            Result with feature_id.
        """
        try:
            self._features[feature.feature_id] = feature
            return self._ok(feature.feature_id)
        except Exception as exc:
            return self._fail("ERR_REGISTER", str(exc))

    def register_feature_set(self, feature_set: FeatureSet) -> Any:
        """Register a versioned feature set.

        Args:
            feature_set: :class:`FeatureSet` to register.

        Returns:
            Result with feature_set_id.
        """
        try:
            self._feature_sets[feature_set.feature_set_id] = feature_set
            return self._ok(feature_set.feature_set_id)
        except Exception as exc:
            return self._fail("ERR_REGISTER_SET", str(exc))

    def get_feature(self, feature_id: str) -> Any:
        """Retrieve a feature.

        Args:
            feature_id: Feature identifier.

        Returns:
            Result with :class:`FeatureMetadata`.
        """
        f = self._features.get(feature_id)
        if f is None:
            return self._fail("ERR_NOT_FOUND", f"Feature '{feature_id}' not found.")
        return self._ok(f)

    def get_feature_set(self, feature_set_id: str) -> Any:
        """Retrieve a feature set.

        Args:
            feature_set_id: Feature set identifier.

        Returns:
            Result with :class:`FeatureSet`.
        """
        fs = self._feature_sets.get(feature_set_id)
        if fs is None:
            return self._fail("ERR_NOT_FOUND", f"Feature set '{feature_set_id}' not found.")
        return self._ok(fs)

    def get_lineage(self, feature_id: str) -> Any:
        """Return the full lineage chain for a feature (BFS from feature_id upstream).

        Args:
            feature_id: Starting feature identifier.

        Returns:
            Result with ordered list of :class:`FeatureMetadata` (root first).
        """
        visited: list[FeatureMetadata] = []
        queue = [feature_id]
        seen: set[str] = set()
        while queue:
            fid = queue.pop(0)
            if fid in seen:
                continue
            seen.add(fid)
            f = self._features.get(fid)
            if f:
                visited.insert(0, f)
                queue.extend(f.lineage_refs)
        return self._ok(visited)

    def health_check(self) -> dict[str, Any]:
        """Return health status."""
        return {"status": "ok", "service": "FeatureService", "feature_count": len(self._features)}

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
