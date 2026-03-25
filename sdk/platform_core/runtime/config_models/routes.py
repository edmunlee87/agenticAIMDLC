"""Workflow routes and failure routes Pydantic config models.

Defines stage routing logic: what stage follows on success/failure/review/approval,
and how failure recovery is routed.
Loaded from configs/runtime/workflow_routes.yaml and failure_routes.yaml.
"""

from typing import Dict, List, Optional

from pydantic import field_validator

from .base import RuntimeConfigBase


class FailureRouteEntry(RuntimeConfigBase):
    """A failure route for a specific stage and error type.

    Attributes:
        stage_name: The stage where the failure occurs.
        error_type: Error type/code this route handles. Use '*' for catch-all.
        recovery_action: Recovery action to recommend (retry, rerun, rollback, escalate).
        target_stage: Stage to route to after recovery (if applicable).
        requires_human_decision: Whether a human must decide the recovery path.
        audit_required: Whether this failure route requires an audit record.
    """

    stage_name: str
    error_type: str = "*"
    recovery_action: str
    target_stage: Optional[str] = None
    requires_human_decision: bool = True
    audit_required: bool = True

    @field_validator("recovery_action")
    @classmethod
    def validate_recovery_action(cls, v: str) -> str:
        allowed = {"retry", "rerun", "rollback", "escalate", "resume", "skip", "manual"}
        if v not in allowed:
            raise ValueError(f"recovery_action must be one of {allowed}, got: {v!r}")
        return v


class FailureRoutesConfig(RuntimeConfigBase):
    """All failure routes, keyed by stage_name.

    Values are lists because multiple error types can have different routes.
    Loaded from configs/runtime/failure_routes.yaml.
    """

    routes: Dict[str, List[FailureRouteEntry]] = {}

    def get_routes_for_stage(self, stage_name: str) -> List[FailureRouteEntry]:
        """Return failure routes for a stage, including catch-all routes."""
        return self.routes.get(stage_name, [])


class WorkflowRouteDefinition(RuntimeConfigBase):
    """Routing definition for a stage transition outcome.

    Attributes:
        stage_name: Source stage.
        on_success: Stage to route to on success.
        on_review_required: Stage or action when review is required.
        on_pass: Stage to route to when validation passes.
        on_fail: Stage to route to when validation fails.
        on_approved: Stage to route to after approval.
        on_rejected: Stage to route to after rejection.
        on_auto_continue: Stage for auto-continue path.
        on_remediation_required: Stage for remediation path.
    """

    stage_name: str
    on_success: Optional[str] = None
    on_review_required: Optional[str] = None
    on_pass: Optional[str] = None
    on_fail: Optional[str] = None
    on_approved: Optional[str] = None
    on_rejected: Optional[str] = None
    on_auto_continue: Optional[str] = None
    on_remediation_required: Optional[str] = None

    @field_validator("stage_name")
    @classmethod
    def validate_non_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("stage_name must not be blank")
        return v


class WorkflowRoutesConfig(RuntimeConfigBase):
    """All workflow stage routes, keyed by stage_name.

    Loaded from configs/runtime/workflow_routes.yaml.
    """

    routes: Dict[str, WorkflowRouteDefinition]

    @field_validator("routes")
    @classmethod
    def validate_non_empty(cls, v: Dict[str, WorkflowRouteDefinition]) -> Dict[str, WorkflowRouteDefinition]:
        if not v:
            raise ValueError("workflow routes must define at least one route")
        return v
