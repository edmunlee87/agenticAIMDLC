"""
platform_contracts
==================
Shared contracts, enums, result types, and common fragments for the MDLC framework.

All other SDK packages depend on this package; it has no internal MDLC dependencies.
"""

from platform_contracts.enums import (
    AuditType,
    CandidateType,
    EnvironmentType,
    GovernanceSeverity,
    InteractionMode,
    InteractionType,
    PolicyCheckResult,
    ReviewType,
    RoleType,
    StageStatus,
    TokenMode,
    UIMode,
    WorkflowMode,
)
from platform_contracts.results import BaseResult, ErrorDetail, ResultFactory, ValidationResultBase

__all__ = [
    # Enums
    "AuditType",
    "CandidateType",
    "EnvironmentType",
    "GovernanceSeverity",
    "InteractionMode",
    "InteractionType",
    "PolicyCheckResult",
    "ReviewType",
    "RoleType",
    "StageStatus",
    "TokenMode",
    "UIMode",
    "WorkflowMode",
    # Results
    "BaseResult",
    "ErrorDetail",
    "ResultFactory",
    "ValidationResultBase",
]
