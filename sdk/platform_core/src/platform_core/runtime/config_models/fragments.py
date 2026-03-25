"""Reusable config fragments composed into top-level config models.

Fragments represent small, self-contained pieces of configuration that appear
in multiple places (e.g., a RetryConfig appears on both stage configs and tool
group configs).
"""

from __future__ import annotations

from pydantic import Field, field_validator

from platform_core.runtime.config_models.base import ConfigModelBase
from platform_core.runtime.config_models.enums import BackoffMode


class RetryConfig(ConfigModelBase):
    """Retry policy for a stage, tool call, or service operation.

    Args:
        max_retries: Maximum number of retry attempts (0 = no retry). Default: 3.
        retry_on: List of error codes or exception class names to retry on.
            Empty list means retry on any transient error.
        backoff_mode: Backoff strategy. Default: ``exponential``.
        base_delay_seconds: Base delay in seconds for backoff calculation. Default: 1.0.
        max_delay_seconds: Cap on computed delay. Default: 60.0.
        jitter: Whether to add random jitter to avoid thundering herd. Default: True.
    """

    max_retries: int = 3
    retry_on: list[str] = Field(default_factory=list)
    backoff_mode: BackoffMode = BackoffMode.EXPONENTIAL
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    jitter: bool = True

    @field_validator("max_retries", mode="before")
    @classmethod
    def _non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("max_retries must be >= 0")
        return v

    @field_validator("base_delay_seconds", "max_delay_seconds", mode="before")
    @classmethod
    def _positive_delay(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("delay values must be > 0")
        return v


class SkillRef(ConfigModelBase):
    """Reference to a skill that can be resolved by the skill registry.

    Args:
        skill_id: Unique skill identifier used in the registry.
        version_constraint: PEP 440 version constraint (e.g. ``">=1.0,<2.0"``).
            Empty string means ``latest``.
        required: If ``True`` and the skill cannot be resolved, raise an error.
    """

    skill_id: str
    version_constraint: str = ""
    required: bool = True


class TokenBudget(ConfigModelBase):
    """Token budget limits for a UI/interaction mode.

    Args:
        context_tokens: Max tokens allocated for retrieved context. Default: 2000.
        completion_tokens: Max tokens for LLM completion. Default: 1000.
        total_tokens: Hard cap on total tokens per interaction. Default: 4000.
    """

    context_tokens: int = 2000
    completion_tokens: int = 1000
    total_tokens: int = 4000

    @field_validator("total_tokens", mode="after")
    @classmethod
    def _total_ge_parts(cls, v: int, info: object) -> int:  # type: ignore[override]
        data = getattr(info, "data", {})
        parts = data.get("context_tokens", 0) + data.get("completion_tokens", 0)
        if v < parts:
            raise ValueError(
                f"total_tokens ({v}) must be >= context_tokens + completion_tokens ({parts})"
            )
        return v


class ApprovalAuthorityConfig(ConfigModelBase):
    """Defines who can approve an action at a governance gate.

    Args:
        minimum_role: Minimum role required to approve.
        allow_self_approval: Whether the submitter may approve their own work.
            Should be ``False`` in production. Default: False.
        escalation_role: Role to escalate to if minimum_role approver is unavailable.
    """

    minimum_role: str
    allow_self_approval: bool = False
    escalation_role: str = ""
