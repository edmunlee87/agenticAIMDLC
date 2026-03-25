"""token_sdk.models -- token budget and context pack contracts.

Token budgets are per-interaction-mode; context packs are assembled to fit
within the budget, with overflow trimmed deterministically (highest-priority
content first).
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TokenMode(str, Enum):
    """Token usage mode."""
    FULL = "full"
    COMPACT = "compact"
    MINIMAL = "minimal"


class ContextSection(BaseModel):
    """A single section in a context pack.

    Args:
        section_id: Unique section identifier.
        title: Section title.
        content: Section content text.
        priority: Lower number = higher priority (retained first when trimming).
        token_count: Estimated token count.
        source_type: Content source category (``"state"``, ``"policy"``, ``"knowledge"``, etc.).
        is_mandatory: If True, this section is never trimmed regardless of budget.
    """

    model_config = ConfigDict(frozen=True)

    section_id: str
    title: str
    content: str
    priority: int = 50
    token_count: int = 0
    source_type: str = "general"
    is_mandatory: bool = False


class ContextPack(BaseModel):
    """An assembled, budget-constrained context pack for LLM injection.

    Args:
        pack_id: Unique pack identifier.
        pack_type: Category (``"routing"``, ``"review"``, ``"validation"``, ``"drafting"``).
        run_id: MDLC run.
        project_id: Project.
        stage_name: Current stage.
        role_id: Current actor role.
        token_mode: :class:`TokenMode`.
        sections: Ordered sections (priority ascending = included first).
        total_tokens: Actual total tokens across all included sections.
        budget: Token budget applied.
        was_trimmed: True if sections were dropped to fit budget.
        trimmed_section_ids: IDs of sections dropped.
        built_at: Assembly timestamp.
    """

    model_config = ConfigDict(frozen=True)

    pack_id: str
    pack_type: str = "general"
    run_id: str = ""
    project_id: str = ""
    stage_name: str = ""
    role_id: str = ""
    token_mode: TokenMode = TokenMode.FULL
    sections: list[ContextSection] = Field(default_factory=list)
    total_tokens: int = 0
    budget: int = 4000
    was_trimmed: bool = False
    trimmed_section_ids: list[str] = Field(default_factory=list)
    built_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def render(self, separator: str = "\n\n---\n\n") -> str:
        """Render all sections into a single context string.

        Args:
            separator: Separator between sections.

        Returns:
            Combined context string.
        """
        return separator.join(f"## {s.title}\n{s.content}" for s in self.sections)


class TokenUsageRecord(BaseModel):
    """A telemetry record for a single LLM invocation's token usage.

    Args:
        usage_id: Unique record identifier.
        run_id: MDLC run.
        project_id: Project.
        stage_name: Stage context.
        role_id: Actor role.
        interaction_type: Interaction type string.
        token_mode: :class:`TokenMode`.
        context_tokens: Tokens consumed by the context pack.
        completion_tokens: Tokens consumed by the model completion.
        total_tokens: Total tokens for this invocation.
        budget: Budget that was applied.
        was_over_budget: True if context exceeded budget before trimming.
        recorded_at: Telemetry timestamp.
    """

    model_config = ConfigDict(frozen=True)

    usage_id: str
    run_id: str = ""
    project_id: str = ""
    stage_name: str = ""
    role_id: str = ""
    interaction_type: str = ""
    token_mode: TokenMode = TokenMode.FULL
    context_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    budget: int = 4000
    was_over_budget: bool = False
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
