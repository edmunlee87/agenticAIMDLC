"""token_sdk.context_builder -- assembles ContextPack from sections with budget trimming.

The builder:
1. Collects mandatory sections (never trimmed).
2. Sorts optional sections by priority (ascending = higher priority).
3. Fills up to the budget, dropping low-priority sections.
4. Records trimmed section IDs for transparency.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from token_sdk.models import ContextPack, ContextSection, TokenMode

logger = logging.getLogger(__name__)

_CHARS_PER_TOKEN = 4  # Conservative estimate


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // _CHARS_PER_TOKEN)


class ContextBuilder:
    """Assembles a :class:`~token_sdk.models.ContextPack` from sections within a token budget.

    Args:
        run_id: MDLC run.
        project_id: Project.
        stage_name: Current stage.
        role_id: Actor role.
        token_mode: :class:`TokenMode`. Default: FULL.
        budget_registry: Optional :class:`~token_sdk.budget_registry.BudgetRegistry`.
    """

    def __init__(
        self,
        run_id: str = "",
        project_id: str = "",
        stage_name: str = "",
        role_id: str = "",
        token_mode: TokenMode = TokenMode.FULL,
        budget_registry: Any = None,
    ) -> None:
        self._run_id = run_id
        self._project_id = project_id
        self._stage_name = stage_name
        self._role_id = role_id
        self._token_mode = token_mode
        self._budget_registry = budget_registry
        self._sections: list[ContextSection] = []

    def add_section(
        self,
        section_id: str,
        title: str,
        content: str,
        priority: int = 50,
        source_type: str = "general",
        is_mandatory: bool = False,
    ) -> "ContextBuilder":
        """Add a section to the builder.

        Args:
            section_id: Unique section identifier.
            title: Section title.
            content: Section content.
            priority: Priority (lower = higher priority, retained first). Default: 50.
            source_type: Content source category. Default: ``"general"``.
            is_mandatory: Never trimmed if True. Default: False.

        Returns:
            Self (for chaining).
        """
        token_count = _estimate_tokens(content)
        self._sections.append(ContextSection(
            section_id=section_id,
            title=title,
            content=content,
            priority=priority,
            token_count=token_count,
            source_type=source_type,
            is_mandatory=is_mandatory,
        ))
        return self

    def add_workflow_state(self, state_dict: dict[str, Any]) -> "ContextBuilder":
        """Add a compressed workflow state section.

        Args:
            state_dict: Dict of state fields.

        Returns:
            Self.
        """
        lines = [f"{k}: {v}" for k, v in state_dict.items()]
        return self.add_section(
            section_id="workflow_state",
            title="Current Workflow State",
            content="\n".join(lines),
            priority=5,
            source_type="state",
            is_mandatory=True,
        )

    def add_policy_summary(self, policies: list[dict[str, Any]]) -> "ContextBuilder":
        """Add applicable policy rules summary.

        Args:
            policies: List of policy dict records.

        Returns:
            Self.
        """
        if not policies:
            return self
        lines = [f"- [{p.get('severity', '?').upper()}] {p.get('rule_id', '')}: {p.get('description', '')}" for p in policies]
        return self.add_section(
            section_id="policy_summary",
            title="Applicable Policy Rules",
            content="\n".join(lines),
            priority=10,
            source_type="policy",
            is_mandatory=True,
        )

    def add_knowledge_chunks(self, chunks: list[Any]) -> "ContextBuilder":
        """Add retrieved knowledge chunks.

        Args:
            chunks: List of :class:`~rag_sdk.models.RetrievedChunk` or dict objects.

        Returns:
            Self.
        """
        for i, chunk in enumerate(chunks):
            title = str(getattr(chunk, "title", None) or (chunk.get("title", "") if isinstance(chunk, dict) else ""))
            content = str(getattr(chunk, "content", None) or (chunk.get("content", "") if isinstance(chunk, dict) else str(chunk)))
            self.add_section(
                section_id=f"knowledge_{i}",
                title=title or f"Knowledge {i + 1}",
                content=content,
                priority=40 + i,
                source_type="knowledge",
            )
        return self

    def add_review_payload_summary(self, payload: dict[str, Any]) -> "ContextBuilder":
        """Add a compressed review payload summary.

        Args:
            payload: Review payload dict.

        Returns:
            Self.
        """
        lines = [
            f"Stage: {payload.get('stage_name', '')}",
            f"Review Type: {payload.get('review_type', '')}",
            f"Run: {payload.get('run_id', '')}",
        ]
        candidates = payload.get("candidates", [])
        if candidates:
            lines.append(f"Candidates: {len(candidates)}")
        metrics = payload.get("metrics_summary", {})
        if metrics:
            lines.extend(f"  {k}: {v}" for k, v in (metrics if isinstance(metrics, dict) else {}).items())
        return self.add_section(
            section_id="review_payload",
            title="Review Payload Summary",
            content="\n".join(lines),
            priority=15,
            source_type="state",
            is_mandatory=True,
        )

    def build(self, pack_type: str = "general") -> ContextPack:
        """Assemble the :class:`~token_sdk.models.ContextPack`, trimming to budget.

        Args:
            pack_type: Pack type for budget resolution. Default: ``"general"``.

        Returns:
            :class:`ContextPack`.
        """
        budget = self._resolve_budget(pack_type)

        mandatory = [s for s in self._sections if s.is_mandatory]
        optional = sorted(
            [s for s in self._sections if not s.is_mandatory],
            key=lambda s: s.priority,
        )

        included: list[ContextSection] = []
        trimmed_ids: list[str] = []
        total_tokens = sum(s.token_count for s in mandatory)
        included.extend(mandatory)

        for section in optional:
            if total_tokens + section.token_count <= budget:
                included.append(section)
                total_tokens += section.token_count
            else:
                trimmed_ids.append(section.section_id)

        was_trimmed = len(trimmed_ids) > 0
        if was_trimmed:
            logger.info(
                "context_builder.trimmed",
                extra={
                    "pack_type": pack_type,
                    "budget": budget,
                    "total_tokens": total_tokens,
                    "trimmed_count": len(trimmed_ids),
                },
            )

        return ContextPack(
            pack_id=str(uuid.uuid4()),
            pack_type=pack_type,
            run_id=self._run_id,
            project_id=self._project_id,
            stage_name=self._stage_name,
            role_id=self._role_id,
            token_mode=self._token_mode,
            sections=included,
            total_tokens=total_tokens,
            budget=budget,
            was_trimmed=was_trimmed,
            trimmed_section_ids=trimmed_ids,
        )

    def _resolve_budget(self, pack_type: str) -> int:
        if self._budget_registry is not None:
            return self._budget_registry.get_budget(self._token_mode, pack_type, self._stage_name)
        from token_sdk.budget_registry import BudgetRegistry
        return BudgetRegistry().get_budget(self._token_mode, pack_type, self._stage_name)
