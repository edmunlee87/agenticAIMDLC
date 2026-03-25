"""ModelLifecycleOrchestrator — drives a single MDLC stage lifecycle.

Responsibilities:
1. Resolve current stage and check prerequisites.
2. Invoke stage-level tools via the agent/jupyter bridge.
3. Enforce PlatformBaseRules pre-completion checks.
4. Trigger HITL review when governance flags require it.
5. Persist outcomes (artifacts, events, audit) and route to next stage.

This orchestrator handles ONE stage at a time. The caller (typically the
session-bootstrap-orchestrator) drives the stage loop.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from skills.platform.shared.base_rules import BaseRulesResult, PlatformBaseRules

logger = logging.getLogger(__name__)


@dataclass
class StageOutcome:
    """Result of a single stage lifecycle execution.

    Attributes:
        stage_name: Stage that was executed.
        status: ``"completed"``, ``"paused_for_review"``, ``"failed"``, or ``"blocked"``.
        next_stage: Next stage to proceed to (empty if terminal or paused).
        review_id: Review ID if paused for HITL.
        artifact_ids: Artifact IDs produced during this stage.
        event_ref: Observability event reference.
        audit_ref: Audit record reference.
        error: Error message if status is ``"failed"``.
        base_rule_result: Result of platform base-rule checks.
    """

    stage_name: str
    status: str
    next_stage: str = ""
    review_id: str = ""
    artifact_ids: List[str] = field(default_factory=list)
    event_ref: Optional[str] = None
    audit_ref: Optional[str] = None
    error: str = ""
    base_rule_result: Optional[BaseRulesResult] = None


class ModelLifecycleOrchestrator:
    """Orchestrates a single MDLC stage from start to completion.

    Integrates with:
    - AgentBridge / JupyterBridge for tool dispatch.
    - PlatformBaseRules for pre-completion guardrails.
    - WorkflowController (via bridge) for stage transitions.
    - ReviewController (via bridge) for HITL triggers.

    Args:
        bridge: :class:`AgentBridge` or :class:`JupyterBridge`.
        base_rules: :class:`PlatformBaseRules` instance.
        strict_mode: Pass-through for base_rules strict_mode.
    """

    def __init__(
        self,
        bridge: Any,
        base_rules: Optional[PlatformBaseRules] = None,
        strict_mode: bool = False,
    ) -> None:
        self._bridge = bridge
        self._rules = base_rules or PlatformBaseRules(strict_mode=strict_mode)

    def execute_stage(
        self,
        *,
        stage_name: str,
        run_id: str,
        project_id: str,
        actor_id: str,
        actor_role: str,
        session_id: Optional[str] = None,
        artifact_ids: Optional[List[str]] = None,
        requires_selection: bool = False,
        selected_candidate_id: Optional[str] = None,
        governance_flags: Optional[Dict[str, Any]] = None,
        extra_parameters: Optional[Dict[str, Any]] = None,
    ) -> StageOutcome:
        """Execute a single stage lifecycle.

        Args:
            stage_name: Name of the stage to execute.
            run_id: Active run identifier.
            project_id: Active project identifier.
            actor_id: Actor's unique ID.
            actor_role: Actor's role string.
            session_id: Active session identifier.
            artifact_ids: Artifact IDs to register for this stage.
            requires_selection: Whether a candidate selection is required.
            selected_candidate_id: Explicitly selected candidate version ID.
            governance_flags: Runtime governance flags (from resolved_stack).
            extra_parameters: Additional parameters for tool calls.

        Returns:
            :class:`StageOutcome`.
        """
        artifact_ids = artifact_ids or []
        governance_flags = governance_flags or {}
        extra_parameters = extra_parameters or {}

        # Step 1: Run the stage.
        run_resp = self._dispatch(
            tool_name="platform_run_stage",
            stage_name=stage_name,
            run_id=run_id,
            project_id=project_id,
            actor_id=actor_id,
            actor_role=actor_role,
            session_id=session_id,
            parameters=extra_parameters,
        )
        event_ref = run_resp.get("event_ref")
        audit_ref = run_resp.get("audit_ref")

        if run_resp.get("status") not in ("success", "ok"):
            return StageOutcome(
                stage_name=stage_name,
                status="failed",
                error=run_resp.get("message", "Stage run failed."),
                event_ref=event_ref,
                audit_ref=audit_ref,
            )

        # Step 2: Check governance gate — review required?
        gov_summary = run_resp.get("governance_summary") or {}
        if governance_flags.get("review_required") or gov_summary.get("blocking_reasons"):
            review_resp = self._dispatch(
                tool_name="platform_open_review",
                stage_name=stage_name,
                run_id=run_id,
                project_id=project_id,
                actor_id=actor_id,
                actor_role=actor_role,
                session_id=session_id,
                parameters={
                    "review_type": "generic",
                    "summary_for_reviewer": f"Governance review required for stage '{stage_name}'.",
                    "evidence_refs": artifact_ids,
                },
            )
            review_id = review_resp.get("review_id") or (review_resp.get("data") or {}).get("review_id", "")
            logger.info(
                "model_lifecycle_orchestrator.paused_for_review",
                extra={"stage_name": stage_name, "review_id": review_id},
            )
            return StageOutcome(
                stage_name=stage_name,
                status="paused_for_review",
                review_id=review_id,
                artifact_ids=artifact_ids,
                event_ref=event_ref,
                audit_ref=audit_ref,
            )

        # Step 3: Pre-completion base-rule checks.
        rule_result = self._rules.check_before_complete(
            stage_name=stage_name,
            run_id=run_id,
            artifact_ids=artifact_ids,
            selected_candidate_id=selected_candidate_id,
            requires_selection=requires_selection,
        )

        if not rule_result.passed:
            logger.warning(
                "model_lifecycle_orchestrator.base_rule_violation",
                extra={
                    "stage_name": stage_name,
                    "violations": [v.rule_id for v in rule_result.blocking_violations],
                },
            )
            return StageOutcome(
                stage_name=stage_name,
                status="blocked",
                error="; ".join(v.description for v in rule_result.blocking_violations),
                base_rule_result=rule_result,
                event_ref=event_ref,
                audit_ref=audit_ref,
            )

        # Step 4: Complete the stage.
        complete_resp = self._dispatch(
            tool_name="platform_complete_stage",
            stage_name=stage_name,
            run_id=run_id,
            project_id=project_id,
            actor_id=actor_id,
            actor_role=actor_role,
            session_id=session_id,
            parameters={"artifact_ids": artifact_ids},
        )
        event_ref = complete_resp.get("event_ref") or event_ref
        audit_ref = complete_resp.get("audit_ref") or audit_ref

        if complete_resp.get("status") not in ("success", "ok"):
            return StageOutcome(
                stage_name=stage_name,
                status="failed",
                error=complete_resp.get("message", "Stage complete failed."),
                artifact_ids=artifact_ids,
                event_ref=event_ref,
                audit_ref=audit_ref,
                base_rule_result=rule_result,
            )

        # Step 5: Route to next stage.
        route_resp = self._dispatch(
            tool_name="platform_route_next",
            stage_name=stage_name,
            run_id=run_id,
            project_id=project_id,
            actor_id=actor_id,
            actor_role=actor_role,
            session_id=session_id,
        )
        next_stage = (route_resp.get("data") or {}).get("next_stage") or route_resp.get("next_stage") or ""

        logger.info(
            "model_lifecycle_orchestrator.stage_completed",
            extra={"stage_name": stage_name, "next_stage": next_stage or "terminal"},
        )

        return StageOutcome(
            stage_name=stage_name,
            status="completed",
            next_stage=next_stage,
            artifact_ids=artifact_ids,
            event_ref=event_ref,
            audit_ref=audit_ref,
            base_rule_result=rule_result,
        )

    def _dispatch(
        self,
        tool_name: str,
        stage_name: str,
        run_id: str,
        project_id: str,
        actor_id: str,
        actor_role: str,
        session_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self._bridge.dispatch({
            "tool_name": tool_name,
            "args": {
                "stage_name": stage_name,
                "run_id": run_id,
                "project_id": project_id,
                "actor_id": actor_id,
                "actor_role": actor_role,
                "session_id": session_id,
                "parameters": parameters or {},
            },
        })
