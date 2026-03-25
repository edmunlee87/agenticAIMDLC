"""rag_sdk.retriever -- dual-store retrieval and token-budget-aware ranking.

The retriever is store-agnostic: each registered store must implement the
``DocumentStore`` protocol (duck-typed).  Built-in adapters are provided
for the knowledge_sdk store and a simple in-memory document store.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any, Protocol, runtime_checkable

from rag_sdk.models import PromptPack, RetrievalQuery, RetrievedChunk, StoreType

logger = logging.getLogger(__name__)

# Conservative token-per-character ratio for budget estimation.
_CHARS_PER_TOKEN = 4


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // _CHARS_PER_TOKEN)


@runtime_checkable
class DocumentStore(Protocol):
    """Protocol that all RAG document stores must implement."""

    def query(
        self,
        query_text: str,
        top_k: int,
        stage_name: str,
        model_type: str,
        role_id: str,
    ) -> list[RetrievedChunk]:
        """Return ranked chunks for a query."""
        ...


class InMemoryDocumentStore:
    """A simple in-memory document store for testing and lightweight use.

    Args:
        store_type: :class:`StoreType` this store represents. Default: DOCUMENT.
    """

    def __init__(self, store_type: StoreType = StoreType.DOCUMENT) -> None:
        self._store_type = store_type
        self._documents: list[dict[str, Any]] = []

    def ingest(
        self,
        source_id: str,
        title: str,
        content: str,
        stage_name: str = "",
        model_type: str = "",
        role_id: str = "",
    ) -> None:
        """Ingest a document into the store.

        Args:
            source_id: Source object identifier.
            title: Document title.
            content: Document content.
            stage_name: Stage relevance filter.
            model_type: Domain model type filter.
            role_id: Role relevance filter.
        """
        self._documents.append({
            "source_id": source_id,
            "title": title,
            "content": content,
            "stage_name": stage_name,
            "model_type": model_type,
            "role_id": role_id,
        })

    def query(
        self,
        query_text: str,
        top_k: int,
        stage_name: str = "",
        model_type: str = "",
        role_id: str = "",
    ) -> list[RetrievedChunk]:
        """Simple keyword-overlap retrieval (BM25-like fallback).

        Args:
            query_text: Query string.
            top_k: Maximum number of results.
            stage_name: Stage filter (empty = no filter).
            model_type: Model type filter (empty = no filter).
            role_id: Role filter (empty = no filter).

        Returns:
            Ranked list of :class:`RetrievedChunk`.
        """
        query_words = set(query_text.lower().split())
        scored: list[tuple[float, dict[str, Any]]] = []
        for doc in self._documents:
            # Apply context filters
            if stage_name and doc["stage_name"] and doc["stage_name"] != stage_name:
                continue
            if model_type and doc["model_type"] and doc["model_type"] != model_type:
                continue
            if role_id and doc["role_id"] and doc["role_id"] != role_id:
                continue
            # Keyword overlap score
            doc_words = set((doc["title"] + " " + doc["content"]).lower().split())
            overlap = len(query_words & doc_words)
            if overlap > 0:
                scored.append((overlap / len(query_words), doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        chunks: list[RetrievedChunk] = []
        for score, doc in scored[:top_k]:
            content = doc["content"]
            chunks.append(
                RetrievedChunk(
                    chunk_id=str(uuid.uuid4()),
                    store_type=self._store_type,
                    source_id=doc["source_id"],
                    title=doc["title"],
                    content=content,
                    relevance_score=score,
                    token_count=_estimate_tokens(content),
                    stage_name=doc["stage_name"],
                    model_type=doc["model_type"],
                    role_id=doc["role_id"],
                )
            )
        return chunks


class KnowledgeStoreAdapter:
    """Adapts :class:`~knowledge_sdk.service.KnowledgeService` to the DocumentStore protocol.

    Args:
        knowledge_service: :class:`~knowledge_sdk.service.KnowledgeService` instance.
    """

    def __init__(self, knowledge_service: Any) -> None:
        self._ks = knowledge_service

    def query(
        self,
        query_text: str,
        top_k: int,
        stage_name: str = "",
        model_type: str = "",
        role_id: str = "",
    ) -> list[RetrievedChunk]:
        """Retrieve promoted knowledge objects matching the query.

        Args:
            query_text: Query string.
            top_k: Maximum results.
            stage_name: Stage filter.
            model_type: Model type filter.
            role_id: Role filter.

        Returns:
            Ranked list of :class:`RetrievedChunk`.
        """
        result = self._ks.search(
            stage_name=stage_name or None,
            model_type=model_type or None,
        )
        objects = result.data if result.success else []
        query_words = set(query_text.lower().split())
        scored: list[tuple[float, Any]] = []
        for obj in objects:
            doc_words = set((obj.title + " " + obj.content).lower().split())
            overlap = len(query_words & doc_words)
            if overlap > 0:
                scored.append((overlap / max(1, len(query_words)), obj))
        scored.sort(key=lambda x: x[0], reverse=True)
        chunks: list[RetrievedChunk] = []
        for score, obj in scored[:top_k]:
            chunks.append(
                RetrievedChunk(
                    chunk_id=str(uuid.uuid4()),
                    store_type=StoreType.KNOWLEDGE,
                    source_id=obj.object_id,
                    title=obj.title,
                    content=obj.content,
                    relevance_score=score,
                    token_count=_estimate_tokens(obj.content),
                    stage_name=obj.stage_name,
                    model_type=obj.model_type,
                )
            )
        return chunks


class Retriever:
    """Multi-store retriever with token-budget-aware prompt packing.

    Args:
        stores: Dict of :class:`StoreType` → store implementing the DocumentStore protocol.
    """

    def __init__(self, stores: dict[StoreType, Any] | None = None) -> None:
        self._stores: dict[StoreType, Any] = stores or {}

    def register_store(self, store_type: StoreType, store: Any) -> None:
        """Register a document store.

        Args:
            store_type: :class:`StoreType` identifier.
            store: Store implementing the DocumentStore protocol.
        """
        self._stores[store_type] = store

    def retrieve(self, query: RetrievalQuery) -> PromptPack:
        """Retrieve and pack context for a query.

        Args:
            query: :class:`RetrievalQuery` with all context and budget parameters.

        Returns:
            :class:`PromptPack` with trimmed, ranked chunks.
        """
        target_stores = query.store_types or list(self._stores.keys())
        all_chunks: list[RetrievedChunk] = []

        for stype in target_stores:
            store = self._stores.get(stype)
            if store is None:
                logger.warning("retriever.store_not_found", extra={"store_type": stype})
                continue
            try:
                chunks = store.query(
                    query_text=query.query_text,
                    top_k=query.top_k,
                    stage_name=query.stage_name,
                    model_type=query.model_type,
                    role_id=query.role_id,
                )
                all_chunks.extend(chunks)
            except Exception as exc:
                logger.warning("retriever.store_error", extra={"store_type": stype, "error": str(exc)})

        # Sort all chunks by relevance score descending.
        all_chunks.sort(key=lambda c: c.relevance_score, reverse=True)

        # Apply token budget: take top chunks that fit within budget.
        packed: list[RetrievedChunk] = []
        total_tokens = 0
        was_trimmed = False
        for chunk in all_chunks[:query.top_k]:
            if total_tokens + chunk.token_count > query.token_budget:
                was_trimmed = True
                break
            packed.append(chunk)
            total_tokens += chunk.token_count

        pack_id = str(uuid.uuid4())
        logger.info(
            "retriever.pack_built",
            extra={
                "pack_id": pack_id,
                "query_id": query.query_id,
                "chunks": len(packed),
                "total_tokens": total_tokens,
                "was_trimmed": was_trimmed,
            },
        )
        return PromptPack(
            pack_id=pack_id,
            query_id=query.query_id,
            chunks=packed,
            total_tokens=total_tokens,
            token_budget=query.token_budget,
            was_trimmed=was_trimmed,
            run_id=query.run_id,
            project_id=query.project_id,
        )
