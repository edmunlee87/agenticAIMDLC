"""token_sdk.telemetry -- token usage telemetry recorder and reporter."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from token_sdk.models import TokenMode, TokenUsageRecord

logger = logging.getLogger(__name__)


class TokenTelemetry:
    """Records and reports token usage across LLM invocations.

    Args:
        observability_service: Optional observability service for event emission.
    """

    def __init__(self, observability_service: Any = None) -> None:
        self._obs = observability_service
        self._records: list[TokenUsageRecord] = []

    def record(
        self,
        run_id: str,
        project_id: str,
        stage_name: str,
        role_id: str,
        interaction_type: str,
        token_mode: TokenMode,
        context_tokens: int,
        completion_tokens: int,
        budget: int,
    ) -> TokenUsageRecord:
        """Record a single LLM invocation's token usage.

        Args:
            run_id: MDLC run.
            project_id: Project.
            stage_name: Stage context.
            role_id: Actor role.
            interaction_type: Interaction type string.
            token_mode: :class:`TokenMode`.
            context_tokens: Context token count.
            completion_tokens: Completion token count.
            budget: Budget that was applied.

        Returns:
            :class:`TokenUsageRecord`.
        """
        total = context_tokens + completion_tokens
        rec = TokenUsageRecord(
            usage_id=str(uuid.uuid4()),
            run_id=run_id,
            project_id=project_id,
            stage_name=stage_name,
            role_id=role_id,
            interaction_type=interaction_type,
            token_mode=token_mode,
            context_tokens=context_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total,
            budget=budget,
            was_over_budget=context_tokens > budget,
        )
        self._records.append(rec)

        logger.info(
            "token_telemetry.recorded",
            extra={
                "run_id": run_id,
                "stage_name": stage_name,
                "total_tokens": total,
                "was_over_budget": rec.was_over_budget,
            },
        )

        self._emit(rec)
        return rec

    def get_summary(self, run_id: str | None = None) -> dict[str, Any]:
        """Return token usage summary statistics.

        Args:
            run_id: Optional run filter.

        Returns:
            Dict with total_tokens, avg_tokens, over_budget_count, record_count.
        """
        records = [r for r in self._records if run_id is None or r.run_id == run_id]
        if not records:
            return {"total_tokens": 0, "avg_tokens": 0, "over_budget_count": 0, "record_count": 0}

        totals = [r.total_tokens for r in records]
        return {
            "record_count": len(records),
            "total_tokens": sum(totals),
            "avg_tokens": sum(totals) / len(records),
            "max_tokens": max(totals),
            "over_budget_count": sum(1 for r in records if r.was_over_budget),
            "by_stage": {
                stage: sum(r.total_tokens for r in records if r.stage_name == stage)
                for stage in {r.stage_name for r in records}
            },
        }

    def get_records(self, run_id: str | None = None) -> list[TokenUsageRecord]:
        """Return all token usage records.

        Args:
            run_id: Optional run filter.

        Returns:
            List of :class:`TokenUsageRecord`.
        """
        return [r for r in self._records if run_id is None or r.run_id == run_id]

    def _emit(self, rec: TokenUsageRecord) -> None:
        if self._obs is None:
            return
        try:
            self._obs.emit_simple(
                event_type="token.usage.recorded",
                run_id=rec.run_id,
                stage_name=rec.stage_name,
                metadata={
                    "total_tokens": rec.total_tokens,
                    "token_mode": rec.token_mode.value,
                    "was_over_budget": rec.was_over_budget,
                },
            )
        except Exception as exc:
            logger.warning("token_telemetry.emit_failed", extra={"error": str(exc)})
