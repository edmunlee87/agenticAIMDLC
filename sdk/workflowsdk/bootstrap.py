"""Project and run bootstrap for workflowsdk.

:func:`bootstrap_project_workflow` creates the initial
:class:`~sdk.workflowsdk.models.WorkflowEvent` that seeds the event log for a
new run.  It enforces mandatory governance fields and writes the
``workflow.initialized`` event via :class:`~sdk.workflowsdk.state_store.WorkflowStateStore`.

Design contract:
    - Returns the seeded :class:`~sdk.workflowsdk.models.WorkflowEvent` on
      success or raises on validation failure.
    - The main :class:`~sdk.workflowsdk.service.WorkflowService` wraps the
      call in :class:`~sdk.platform_core.base_classes.base.BaseResult`.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from sdk.platform_core.schemas.utilities import IDFactory
from sdk.workflowsdk.models import (
    WorkflowEvent,
    WorkflowEventType,
    WorkflowMode,
)
from sdk.workflowsdk.state_store import WorkflowStateStore

logger = logging.getLogger(__name__)

_VALID_MODES = {m.value for m in WorkflowMode}


def bootstrap_project_workflow(
    *,
    store: WorkflowStateStore,
    run_id: str,
    project_id: str,
    first_stage: str,
    actor_id: str = "system",
    actor_role: str = "system",
    workflow_mode: str = WorkflowMode.DEVELOPMENT.value,
    active_domain: str = "generic",
    session_id: str = "",
    trace_id: str = "",
) -> WorkflowEvent:
    """Seed the event log with a ``workflow.initialized`` event.

    Args:
        store: The :class:`WorkflowStateStore` to write into.
        run_id: Unique run identifier.
        project_id: Owning project identifier.
        first_stage: Name of the first MDLC stage.
        actor_id: Actor triggering the bootstrap.
        actor_role: Role of the actor.
        workflow_mode: :class:`~sdk.workflowsdk.models.WorkflowMode` value
            string (default ``"development"``).
        active_domain: Domain pack name (default ``"generic"``).
        session_id: Optional active session identifier.
        trace_id: Optional distributed trace identifier.

    Returns:
        The appended :class:`WorkflowEvent`.

    Raises:
        ValueError: If *run_id* already exists in the store, or if mandatory
            fields are empty or *workflow_mode* is invalid.
    """
    if not run_id.strip():
        raise ValueError("run_id must be non-empty.")
    if not project_id.strip():
        raise ValueError("project_id must be non-empty.")
    if not first_stage.strip():
        raise ValueError("first_stage must be non-empty.")
    if workflow_mode not in _VALID_MODES:
        raise ValueError(
            f"Invalid workflow_mode '{workflow_mode}'. "
            f"Must be one of: {sorted(_VALID_MODES)}."
        )
    if store.has_run(run_id):
        raise ValueError(
            f"Run '{run_id}' is already initialised. "
            "Cannot bootstrap an existing run."
        )

    event_id = IDFactory.event_id()
    event = WorkflowEvent(
        event_id=event_id,
        event_type=WorkflowEventType.WORKFLOW_INITIALIZED,
        run_id=run_id,
        project_id=project_id,
        stage_name=first_stage,
        actor_id=actor_id,
        actor_role=actor_role,
        session_id=session_id,
        trace_id=trace_id,
        timestamp=datetime.now(timezone.utc),
        payload={
            "workflow_mode": workflow_mode,
            "active_domain": active_domain,
            "first_stage": first_stage,
        },
    )
    store.append_event(event)

    logger.info(
        "Workflow bootstrapped: run_id=%s project_id=%s first_stage=%s mode=%s actor=%s",
        run_id,
        project_id,
        first_stage,
        workflow_mode,
        actor_id,
    )
    return event
