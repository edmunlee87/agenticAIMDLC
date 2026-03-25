"""rag_sdk.models -- retrieval context and prompt pack contracts.

The RAG SDK operates in a token-budget-aware manner: retrieved chunks are
ranked and trimmed to fit within a per-mode token budget before being packed
into a prompt context.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StoreType(str, Enum):
    """Which store a retrieved chunk comes from."""
    KNOWLEDGE = "knowledge"
    DOCUMENT = "document"
    EVENT = "event"
    ARTIFACT = "artifact"


class RetrievedChunk(BaseModel):
    """A single retrieved context chunk.

    Args:
        chunk_id: Unique chunk identifier.
        store_type: :class:`StoreType`.
        source_id: ID of the source object (knowledge_object_id, artifact_id, etc.).
        title: Source title.
        content: Chunk content text.
        relevance_score: Retrieval relevance score (0.0–1.0).
        token_count: Estimated token count for this chunk.
        stage_name: Stage context for this chunk.
        model_type: Domain model type context.
        role_id: Role that this chunk is relevant for.
        retrieved_at: Retrieval timestamp.
    """

    model_config = ConfigDict(frozen=True)

    chunk_id: str
    store_type: StoreType
    source_id: str
    title: str = ""
    content: str
    relevance_score: float = 0.0
    token_count: int = 0
    stage_name: str = ""
    model_type: str = ""
    role_id: str = ""
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RetrievalQuery(BaseModel):
    """A retrieval query with context filters.

    Args:
        query_id: Unique query identifier.
        query_text: The query string.
        run_id: MDLC run issuing the query.
        project_id: Project.
        stage_name: Stage context for filtering.
        model_type: Domain model type for filtering.
        role_id: Role context for filtering.
        top_k: Maximum number of chunks to retrieve. Default: 10.
        token_budget: Maximum total tokens for retrieved context. Default: 2000.
        store_types: Which stores to query (empty = all).
    """

    model_config = ConfigDict(frozen=True)

    query_id: str
    query_text: str
    run_id: str
    project_id: str
    stage_name: str = ""
    model_type: str = ""
    role_id: str = ""
    top_k: int = 10
    token_budget: int = 2000
    store_types: list[StoreType] = Field(default_factory=list)


class PromptPack(BaseModel):
    """A trimmed, ordered set of retrieved chunks ready for prompt injection.

    Args:
        pack_id: Unique pack identifier.
        query_id: Source query ID.
        chunks: Ordered list of chunks (highest relevance first).
        total_tokens: Total token count across all included chunks.
        token_budget: Budget used for trimming.
        was_trimmed: True if some chunks were dropped to fit the budget.
        run_id: Run.
        project_id: Project.
        built_at: When the pack was assembled.
    """

    model_config = ConfigDict(frozen=True)

    pack_id: str
    query_id: str
    chunks: list[RetrievedChunk] = Field(default_factory=list)
    total_tokens: int = 0
    token_budget: int = 2000
    was_trimmed: bool = False
    run_id: str = ""
    project_id: str = ""
    built_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_context_string(self, separator: str = "\n\n---\n\n") -> str:
        """Render all chunks into a single context string for prompt injection.

        Args:
            separator: Separator between chunks. Default: ``"\\n\\n---\\n\\n"``.

        Returns:
            Context string.
        """
        parts = [f"[{c.store_type.value.upper()}] {c.title}\n{c.content}" for c in self.chunks]
        return separator.join(parts)
