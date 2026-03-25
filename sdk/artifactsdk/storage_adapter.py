"""Artifact storage adapter: abstract interface + in-memory implementation.

Storage adapters decouple ArtifactService from specific backends.
Production adapters (S3, CML, GCS, Azure Blob) implement the same interface.
"""

from __future__ import annotations

import hashlib
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from sdk.platform_core.schemas.base_result import BaseResult
from sdk.platform_core.services.base_service import BaseStorageService

from .models import ArtifactRecord, ChecksumRecord

logger = logging.getLogger(__name__)


class ArtifactStorageAdapter(BaseStorageService):
    """Abstract storage adapter for persisting artifact records.

    Sub-classes implement backend-specific storage (local, S3, CML, GCS,
    Azure Blob). The adapter is responsible for storing serialized artifact
    records; the ArtifactService manages checksums and lineage.

    Concrete implementations must override: ``write``, ``read``, ``exists``.
    """

    SDK_NAME: str = "artifactsdk.storage"

    def __init__(self) -> None:
        super().__init__(sdk_name=self.SDK_NAME)


class InMemoryArtifactStore(ArtifactStorageAdapter):
    """In-process artifact store for unit tests and development.

    Thread-safety: Single-threaded use only.

    Args:
        simulate_write_failure: If True, every write returns failure (for testing).
    """

    def __init__(self, simulate_write_failure: bool = False) -> None:
        super().__init__()
        self._store: Dict[str, Dict[str, Any]] = {}
        self._simulate_write_failure = simulate_write_failure

    def write(
        self,
        key: str,
        data: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> BaseResult:
        """Persist an artifact record under ``key``.

        Args:
            key: Artifact ID (``art_<uuid>``).
            data: Serialized artifact record dict.
            metadata: Optional storage-layer metadata.

        Returns:
            Success or failure BaseResult.
        """
        if self._simulate_write_failure:
            return self._build_result(
                function_name="write",
                status="failure",
                message=f"Simulated write failure for key '{key}'.",
                errors=["Storage backend write failure (simulated)."],
            )
        self._store[key] = {"data": data, "metadata": metadata or {}}
        return self._build_result(
            function_name="write",
            status="success",
            message=f"Artifact '{key}' written to in-memory store.",
            data={"key": key},
        )

    def read(self, key: str) -> BaseResult:
        """Retrieve a stored artifact record.

        Args:
            key: Artifact ID.

        Returns:
            Success BaseResult with ``data["record"]``, or failure if not found.
        """
        if key not in self._store:
            return self._build_result(
                function_name="read",
                status="failure",
                message=f"Artifact key '{key}' not found in store.",
                errors=[f"Key not found: {key}"],
            )
        return self._build_result(
            function_name="read",
            status="success",
            message=f"Artifact '{key}' retrieved.",
            data={"record": self._store[key]["data"]},
        )

    def exists(self, key: str) -> bool:
        """Check if an artifact key is present in the store.

        Args:
            key: Artifact ID.

        Returns:
            True if present.
        """
        return key in self._store


class ChecksumManager:
    """Utility for computing and verifying artifact checksums.

    Only SHA-256 is supported at this time; additional algorithms can be added
    by extending the ``SUPPORTED_ALGORITHMS`` set.

    Examples:
        >>> cs = ChecksumManager.compute_checksum(b"payload")
        >>> assert cs.algorithm == "SHA-256"
    """

    SUPPORTED_ALGORITHMS = frozenset({"SHA-256"})

    @staticmethod
    def compute_checksum(
        data: bytes,
        algorithm: str = "SHA-256",
    ) -> ChecksumRecord:
        """Compute a checksum for a raw byte payload.

        Args:
            data: Raw bytes to hash.
            algorithm: Hash algorithm (default: ``"SHA-256"``).

        Returns:
            :class:`ChecksumRecord` with algorithm and hex digest.

        Raises:
            ValueError: If algorithm is not in SUPPORTED_ALGORITHMS.
        """
        if algorithm not in ChecksumManager.SUPPORTED_ALGORITHMS:
            raise ValueError(
                f"Unsupported checksum algorithm '{algorithm}'. "
                f"Supported: {sorted(ChecksumManager.SUPPORTED_ALGORITHMS)}"
            )
        digest = hashlib.sha256(data).hexdigest()
        return ChecksumRecord(algorithm=algorithm, value=digest)

    @staticmethod
    def verify_checksum(data: bytes, expected: ChecksumRecord) -> bool:
        """Verify that data matches an expected checksum.

        Args:
            data: Raw bytes to verify.
            expected: Expected :class:`ChecksumRecord`.

        Returns:
            True if the computed checksum matches the expected value.
        """
        computed = ChecksumManager.compute_checksum(data, expected.algorithm)
        return computed.value == expected.value
