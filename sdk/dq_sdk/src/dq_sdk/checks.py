"""dq_sdk.checks -- built-in DQ check implementations.

Each check is a callable ``(data: Any, config: dict) -> DQCheckResult``.
Data can be a pandas DataFrame, a dict of column stats, or raw scalars.
"""

from __future__ import annotations

import logging
from typing import Any

from dq_sdk.models import DQCheckResult, DQCheckStatus, DQCheckType

logger = logging.getLogger(__name__)


def check_missingness(
    check_id: str,
    column_name: str,
    missing_fraction: float,
    threshold: float = 0.05,
    is_blocking: bool = True,
) -> DQCheckResult:
    """Check that missing rate for a column is below threshold.

    Args:
        check_id: Check identifier.
        column_name: Column being checked.
        missing_fraction: Observed missing rate (0.0–1.0).
        threshold: Maximum acceptable missing rate. Default: 0.05.
        is_blocking: Whether failure blocks processing. Default: True.

    Returns:
        :class:`DQCheckResult`.
    """
    if missing_fraction <= threshold:
        status = DQCheckStatus.PASS
        msg = f"Missing rate {missing_fraction:.2%} within threshold {threshold:.2%}."
    elif missing_fraction <= threshold * 2:
        status = DQCheckStatus.WARN
        msg = f"Missing rate {missing_fraction:.2%} approaching threshold {threshold:.2%}."
    else:
        status = DQCheckStatus.FAIL
        msg = f"Missing rate {missing_fraction:.2%} exceeds threshold {threshold:.2%}."

    return DQCheckResult(
        check_id=check_id,
        check_type=DQCheckType.MISSINGNESS,
        check_name=f"missingness__{column_name}",
        status=status,
        column_name=column_name,
        value=missing_fraction,
        threshold=threshold,
        message=msg,
        is_blocking=is_blocking and status == DQCheckStatus.FAIL,
    )


def check_uniqueness(
    check_id: str,
    column_name: str,
    duplicate_fraction: float,
    threshold: float = 0.0,
    is_blocking: bool = False,
) -> DQCheckResult:
    """Check that duplicate rate for a column is below threshold.

    Args:
        check_id: Check identifier.
        column_name: Column being checked.
        duplicate_fraction: Fraction of duplicate values (0.0–1.0).
        threshold: Maximum acceptable duplicate rate. Default: 0.0.
        is_blocking: Whether failure blocks processing. Default: False.

    Returns:
        :class:`DQCheckResult`.
    """
    status = DQCheckStatus.PASS if duplicate_fraction <= threshold else DQCheckStatus.FAIL
    return DQCheckResult(
        check_id=check_id,
        check_type=DQCheckType.UNIQUENESS,
        check_name=f"uniqueness__{column_name}",
        status=status,
        column_name=column_name,
        value=duplicate_fraction,
        threshold=threshold,
        message=f"Duplicate rate {duplicate_fraction:.2%} (threshold {threshold:.2%}).",
        is_blocking=is_blocking and status == DQCheckStatus.FAIL,
    )


def check_distribution(
    check_id: str,
    column_name: str,
    psi_score: float,
    warn_threshold: float = 0.1,
    fail_threshold: float = 0.2,
    is_blocking: bool = False,
) -> DQCheckResult:
    """Check that Population Stability Index is within acceptable range.

    Args:
        check_id: Check identifier.
        column_name: Column being checked.
        psi_score: Computed PSI score.
        warn_threshold: PSI threshold for warning. Default: 0.1.
        fail_threshold: PSI threshold for failure. Default: 0.2.
        is_blocking: Whether failure blocks processing. Default: False.

    Returns:
        :class:`DQCheckResult`.
    """
    if psi_score <= warn_threshold:
        status = DQCheckStatus.PASS
        msg = f"PSI {psi_score:.3f} stable."
    elif psi_score <= fail_threshold:
        status = DQCheckStatus.WARN
        msg = f"PSI {psi_score:.3f} moderate shift."
    else:
        status = DQCheckStatus.FAIL
        msg = f"PSI {psi_score:.3f} significant shift."

    return DQCheckResult(
        check_id=check_id,
        check_type=DQCheckType.DISTRIBUTION,
        check_name=f"psi__{column_name}",
        status=status,
        column_name=column_name,
        value=psi_score,
        threshold=fail_threshold,
        message=msg,
        is_blocking=is_blocking and status == DQCheckStatus.FAIL,
    )


def check_business_rule(
    check_id: str,
    rule_name: str,
    passes: bool,
    message: str = "",
    is_blocking: bool = True,
) -> DQCheckResult:
    """Check a boolean business rule.

    Args:
        check_id: Check identifier.
        rule_name: Name of the business rule.
        passes: Whether the rule passes.
        message: Human-readable description of the outcome.
        is_blocking: Whether failure blocks processing. Default: True.

    Returns:
        :class:`DQCheckResult`.
    """
    status = DQCheckStatus.PASS if passes else DQCheckStatus.FAIL
    return DQCheckResult(
        check_id=check_id,
        check_type=DQCheckType.BUSINESS_RULE,
        check_name=rule_name,
        status=status,
        message=message or f"Business rule '{rule_name}' {'passed' if passes else 'failed'}.",
        is_blocking=is_blocking and not passes,
    )
