"""dataset_sdk.service -- DatasetService: registry and snapshot management."""

from __future__ import annotations

import logging
from typing import Any

from dataset_sdk.models import DatasetRecord, DatasetSnapshot

logger = logging.getLogger(__name__)


class DatasetService:
    """Registry for datasets and their immutable snapshots.

    Args:
        observability_service: Optional observability service for event emission.
    """

    def __init__(self, observability_service: Any = None) -> None:
        self._obs = observability_service
        self._datasets: dict[str, DatasetRecord] = {}
        self._snapshots: dict[str, DatasetSnapshot] = {}
        self._by_dataset: dict[str, list[str]] = {}

    def register_dataset(self, record: DatasetRecord) -> Any:
        """Register a new dataset.

        Args:
            record: :class:`DatasetRecord` to register.

        Returns:
            Result with dataset_id.
        """
        try:
            if record.dataset_id in self._datasets:
                return self._fail("ERR_EXISTS", f"Dataset '{record.dataset_id}' already exists.")
            self._datasets[record.dataset_id] = record
            self._by_dataset[record.dataset_id] = []
            return self._ok(record.dataset_id)
        except Exception as exc:
            return self._fail("ERR_REGISTER", str(exc))

    def register_snapshot(self, snapshot: DatasetSnapshot) -> Any:
        """Register a dataset snapshot.

        Args:
            snapshot: :class:`DatasetSnapshot` to register.

        Returns:
            Result with snapshot_id.
        """
        try:
            if snapshot.dataset_id not in self._datasets:
                return self._fail("ERR_DATASET_NOT_FOUND", f"Dataset '{snapshot.dataset_id}' not found.")
            if snapshot.snapshot_id in self._snapshots:
                return self._fail("ERR_EXISTS", f"Snapshot '{snapshot.snapshot_id}' already exists.")
            self._snapshots[snapshot.snapshot_id] = snapshot
            self._by_dataset[snapshot.dataset_id].append(snapshot.snapshot_id)
            # Update dataset record with new snapshot_id
            ds = self._datasets[snapshot.dataset_id]
            self._datasets[snapshot.dataset_id] = ds.model_copy(
                update={"snapshot_ids": [*ds.snapshot_ids, snapshot.snapshot_id]}
            )
            return self._ok(snapshot.snapshot_id)
        except Exception as exc:
            return self._fail("ERR_SNAPSHOT", str(exc))

    def get_dataset(self, dataset_id: str) -> Any:
        """Retrieve a dataset record.

        Args:
            dataset_id: Dataset identifier.

        Returns:
            Result with :class:`DatasetRecord`.
        """
        ds = self._datasets.get(dataset_id)
        if ds is None:
            return self._fail("ERR_NOT_FOUND", f"Dataset '{dataset_id}' not found.")
        return self._ok(ds)

    def get_snapshot(self, snapshot_id: str) -> Any:
        """Retrieve a snapshot.

        Args:
            snapshot_id: Snapshot identifier.

        Returns:
            Result with :class:`DatasetSnapshot`.
        """
        snap = self._snapshots.get(snapshot_id)
        if snap is None:
            return self._fail("ERR_NOT_FOUND", f"Snapshot '{snapshot_id}' not found.")
        return self._ok(snap)

    def list_snapshots_for_dataset(self, dataset_id: str) -> Any:
        """Return all snapshots for a dataset.

        Args:
            dataset_id: Dataset identifier.

        Returns:
            Result with list of :class:`DatasetSnapshot`.
        """
        ids = self._by_dataset.get(dataset_id, [])
        return self._ok([self._snapshots[i] for i in ids if i in self._snapshots])

    def health_check(self) -> dict[str, Any]:
        """Return health status."""
        return {"status": "ok", "service": "DatasetService", "dataset_count": len(self._datasets)}

    @staticmethod
    def _ok(data: Any) -> Any:
        class _R:
            def __init__(self, d: Any) -> None:
                self.success = True; self.data = d; self.error_code = None
        return _R(data)

    @staticmethod
    def _fail(code: str, msg: str) -> Any:
        class _R:
            def __init__(self, c: str, m: str) -> None:
                self.success = False; self.data = None; self.error_code = c; self.error_message = m
        return _R(code, msg)
