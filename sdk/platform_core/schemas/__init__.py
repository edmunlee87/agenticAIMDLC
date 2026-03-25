"""Platform core schemas package.

Exports all core contract classes, payload models, common fragments,
and standalone utilities for use by SDKs and controllers.

Import order for consumers:
    from platform_core.schemas import BaseModelBase, BaseResult, ValidationResultBase
    from platform_core.schemas import RuntimeContext, ResolvedStack
    from platform_core.schemas import InteractionPayload, ReviewPayload, StandardResponseEnvelope
    from platform_core.schemas import ActorRecord, ArtifactRef, GovernanceSummary
    from platform_core.schemas import ResultFactory, IDFactory, TimeProvider, DependencyContainer
"""

from .base_model_base import BaseModelBase
from .base_result import BaseResult, ValidationResultBase
from .common_fragments import (
    ActorRecord,
    ArtifactRef,
    CandidateSummary,
    ErrorRecord,
    GovernanceSummary,
    MetricResult,
    PolicyContextRef,
    ReviewSuggestion,
    WarningRecord,
)
from .payload_models import (
    InteractionPayload,
    ResolvedStack,
    ReviewPayload,
    RuntimeContext,
    StandardResponseEnvelope,
)
from .utilities import (
    DependencyContainer,
    IDFactory,
    ResultFactory,
    TimeProvider,
)

__all__ = [
    "BaseModelBase",
    "BaseResult",
    "ValidationResultBase",
    "ActorRecord",
    "ArtifactRef",
    "CandidateSummary",
    "ErrorRecord",
    "GovernanceSummary",
    "MetricResult",
    "PolicyContextRef",
    "ReviewSuggestion",
    "WarningRecord",
    "RuntimeContext",
    "ResolvedStack",
    "InteractionPayload",
    "ReviewPayload",
    "StandardResponseEnvelope",
    "ResultFactory",
    "IDFactory",
    "TimeProvider",
    "DependencyContainer",
]
