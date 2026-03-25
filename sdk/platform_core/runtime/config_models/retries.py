"""Retry policy Pydantic config models.

Defines retry behavior for tools and the overall workflow on failure.
Loaded from configs/runtime/retry_policies.yaml.
"""

from typing import Dict, List, Optional

from pydantic import field_validator

from .base import RuntimeConfigBase
from .enums import RetryModeEnum


class RetryDefaults(RuntimeConfigBase):
    """Platform-wide default retry settings.

    Attributes:
        retry_mode: Default retry strategy.
        max_retries: Default maximum retry count.
        initial_delay_ms: Initial delay between retries in milliseconds.
        max_delay_ms: Maximum delay cap for exponential backoff.
        jitter: Whether to add jitter to retry delays.
    """

    retry_mode: RetryModeEnum = RetryModeEnum.NONE
    max_retries: int = 0
    initial_delay_ms: int = 1000
    max_delay_ms: int = 30000
    jitter: bool = True

    @field_validator("max_retries")
    @classmethod
    def validate_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("max_retries must be >= 0")
        return v

    @field_validator("initial_delay_ms", "max_delay_ms")
    @classmethod
    def validate_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("delay values must be positive")
        return v


class ToolRetryRule(RuntimeConfigBase):
    """Per-tool retry rule override.

    Attributes:
        tool_name: The tool/method name this rule applies to.
        retry_mode: Retry strategy for this tool.
        max_retries: Max retries for this tool.
        retryable_errors: Error codes/types that trigger a retry.
        non_retryable_errors: Error codes/types that should never retry.
    """

    tool_name: str
    retry_mode: RetryModeEnum = RetryModeEnum.FIXED
    max_retries: int = 3
    retryable_errors: List[str] = []
    non_retryable_errors: List[str] = []

    @field_validator("max_retries")
    @classmethod
    def validate_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("max_retries must be >= 0")
        return v


class RetryPoliciesSection(RuntimeConfigBase):
    """Container for retry defaults and per-tool rules.

    Attributes:
        defaults: Platform-wide retry defaults.
        tool_rules: Per-tool retry overrides.
    """

    defaults: RetryDefaults = RetryDefaults()
    tool_rules: List[ToolRetryRule] = []

    def get_rule_for_tool(self, tool_name: str) -> Optional[ToolRetryRule]:
        """Return the retry rule for a specific tool, or None if not found."""
        return next((r for r in self.tool_rules if r.tool_name == tool_name), None)


class RetryPoliciesConfig(RuntimeConfigBase):
    """Root retry policies config.

    Loaded from configs/runtime/retry_policies.yaml.
    """

    retry_policies: RetryPoliciesSection
