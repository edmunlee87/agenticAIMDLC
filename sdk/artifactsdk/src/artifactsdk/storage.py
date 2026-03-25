"""Artifact storage abstraction.

The default implementation is filesystem-based. Swap out by implementing
:class:`ArtifactStorageProtocol`.
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
from pathlib import Path
from typing import Any, Protocol

logger = logging.getLogger(__name__)


class ArtifactStorageProtocol(Protocol):
    """Protocol that any artifact backend must satisfy."""

    def write(self, artifact_id: str, content: bytes, uri_hint: str = "") -> str:
        """Persist content and return its resolved URI."""
        ...

    def read(self, uri: str) -> bytes:
        """Read artifact bytes from the storage URI."""
        ...

    def exists(self, uri: str) -> bool:
        """Return True if the URI is reachable."""
        ...

    def delete(self, uri: str) -> None:
        """Remove artifact from storage."""
        ...


class FilesystemStorage:
    """Local filesystem artifact storage.

    Args:
        base_path: Root directory for artifact storage.
    """

    def __init__(self, base_path: Path | None = None) -> None:
        self._base = base_path or (Path.cwd() / "artifacts")
        self._base.mkdir(parents=True, exist_ok=True)

    def write(self, artifact_id: str, content: bytes, uri_hint: str = "") -> str:
        """Write content to ``<base_path>/<artifact_id>/<uri_hint>`` and return the path.

        Args:
            artifact_id: Artifact identifier (used as subdirectory).
            content: Raw artifact bytes.
            uri_hint: Optional filename. Defaults to ``"content.bin"``.

        Returns:
            Resolved filesystem path string.
        """
        dest_dir = self._base / artifact_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        filename = uri_hint or "content.bin"
        dest = dest_dir / filename
        dest.write_bytes(content)
        logger.debug("artifact_storage.written", extra={"path": str(dest)})
        return str(dest)

    def read(self, uri: str) -> bytes:
        """Read and return artifact bytes.

        Args:
            uri: Filesystem path to the artifact.

        Returns:
            Raw bytes of the artifact content.

        Raises:
            FileNotFoundError: If the URI does not exist.
        """
        path = Path(uri)
        if not path.exists():
            raise FileNotFoundError(f"Artifact not found at URI: {uri}")
        return path.read_bytes()

    def exists(self, uri: str) -> bool:
        """Return True if the artifact file exists."""
        return Path(uri).exists()

    def delete(self, uri: str) -> None:
        """Delete the artifact file (and parent directory if empty).

        Args:
            uri: Filesystem path to the artifact.
        """
        path = Path(uri)
        if path.exists():
            path.unlink()
            try:
                path.parent.rmdir()
            except OSError:
                pass  # Parent not empty — leave it.


def compute_content_hash(content: bytes) -> str:
    """Return the SHA-256 hex digest of ``content``.

    Args:
        content: Bytes to hash.

    Returns:
        Hex-encoded SHA-256 checksum.
    """
    return hashlib.sha256(content).hexdigest()
