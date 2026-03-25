"""Unit tests for the platform controller pack.

Covers:
- BaseController: resolve_stack, ensure_tool_allowed, build_response/error/blocked
- SessionController: open_session, resume_session, unknown action
- WorkflowController: run_stage, complete_stage, fail_stage, route_next, unknown action
- ReviewController: open_review, get_review_payload, submit_review_action, unknown action
- RecoveryController: get_recovery_options, apply_recovery, unknown action
- ControllerFactory: lazy creation of all controllers
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from unittest.mock import MagicMock, patch

import pytest

from sdk.platform_core.controllers import (
    ControllerFactory,
    RecoveryController,
    ReviewController,
    SessionController,
    WorkflowController,
)
from sdk.platform_core.runtime.resolvers.runtime_resolver import ResolvedStack
from sdk.platform_core.schemas.common_fragments import ActorRecord
from sdk.platform_core.schemas.payload_models import InteractionPayload
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_actor(role: str = "developer") -> ActorRecord:
    return ActorRecord(actor_id="actor_001", role=role)


def _make_payload(
    action: str,
    stage_name: str = "feature_engineering",
    parameters: Optional[Dict[str, Any]] = None,
    review_id: Optional[str] = None,
) -> InteractionPayload:
    return InteractionPayload(
        interaction_id=IDFactory.correlation_id(),
        stage_name=stage_name,
        run_id="run_test_001",
        project_id="proj_test",
        session_id="ses_test",
        trace_id="trc_test",
        actor=_make_actor(),
        timestamp=TimeProvider.now_iso(),
        interaction_type="test",
        action=action,
        parameters=parameters or {},
        review_id=review_id,
    )


def _make_ok_result(data: Optional[Dict] = None) -> MagicMock:
    result = MagicMock()
    result.is_success = True
    result.message = "ok"
    result.data = data or {}
    return result


def _make_fail_result(message: str = "fail") -> MagicMock:
    result = MagicMock()
    result.is_success = False
    result.message = message
    result.data = None
    return result


def _make_resolver(
    allowed_tools: list = None,
    blocked_tools: list = None,
    governance_flags: dict = None,
) -> MagicMock:
    stack = ResolvedStack(
        stage_name="feature_engineering",
        actor_role="developer",
        allowed_tools=allowed_tools or ["tool_a"],
        blocked_tools=blocked_tools or [],
        governance_flags=governance_flags or {"review_required": False},
        next_stages=["model_training"],
    )
    resolver = MagicMock()
    resolver.resolve.return_value = stack
    return resolver


# ---------------------------------------------------------------------------
# SessionController
# ---------------------------------------------------------------------------

class TestSessionController:
    def test_open_session_success(self) -> None:
        wf = MagicMock()
        wf.open_session.return_value = _make_ok_result(data={"session_id": "ses_new"})
        ctrl = SessionController(workflow_service=wf, resolver=_make_resolver())
        payload = _make_payload("open_session")
        envelope = ctrl.handle(payload)
        assert envelope.status == "success"
        assert envelope.data["session_id"] == "ses_new"

    def test_open_session_failure(self) -> None:
        wf = MagicMock()
        wf.open_session.return_value = _make_fail_result("Session already exists.")
        ctrl = SessionController(workflow_service=wf, resolver=_make_resolver())
        payload = _make_payload("open_session")
        envelope = ctrl.handle(payload)
        assert envelope.status == "error"
        assert "Session already exists" in envelope.message

    def test_resume_session_success(self) -> None:
        wf = MagicMock()
        wf.resume_session.return_value = _make_ok_result()
        ctrl = SessionController(workflow_service=wf, resolver=_make_resolver())
        payload = _make_payload(
            "resume_session",
            parameters={"session_id": "ses_existing"},
        )
        envelope = ctrl.handle(payload)
        assert envelope.status == "success"

    def test_resume_session_missing_id(self) -> None:
        wf = MagicMock()
        ctrl = SessionController(workflow_service=wf)
        # Build payload manually with no session_id to force the missing-id error path
        payload = InteractionPayload(
            interaction_id=IDFactory.correlation_id(),
            stage_name="feature_engineering",
            run_id="run_test",
            project_id="proj_test",
            session_id=None,
            actor=_make_actor(),
            timestamp=TimeProvider.now_iso(),
            interaction_type="test",
            action="resume_session",
        )
        envelope = ctrl.handle(payload)
        assert envelope.status == "error"
        assert "session_id" in envelope.message.lower()

    def test_unknown_action(self) -> None:
        ctrl = SessionController(workflow_service=MagicMock())
        envelope = ctrl.handle(_make_payload("bogus_action"))
        assert envelope.status == "error"
        assert "SessionController" in envelope.message


# ---------------------------------------------------------------------------
# WorkflowController
# ---------------------------------------------------------------------------

class TestWorkflowController:
    def test_run_stage_success(self) -> None:
        wf = MagicMock()
        wf.start_stage.return_value = _make_ok_result()
        ctrl = WorkflowController(workflow_service=wf, resolver=_make_resolver())
        envelope = ctrl.handle(_make_payload("run_stage"))
        assert envelope.status == "success"

    def test_run_stage_blocked_tool(self) -> None:
        wf = MagicMock()
        ctrl = WorkflowController(
            workflow_service=wf,
            resolver=_make_resolver(blocked_tools=["run_stage"]),
        )
        envelope = ctrl.handle(_make_payload("run_stage"))
        assert envelope.status == "blocked"

    def test_run_stage_service_failure(self) -> None:
        wf = MagicMock()
        wf.start_stage.return_value = _make_fail_result("Stage already active.")
        ctrl = WorkflowController(workflow_service=wf, resolver=_make_resolver())
        envelope = ctrl.handle(_make_payload("run_stage"))
        assert envelope.status == "error"

    def test_complete_stage_success(self) -> None:
        wf = MagicMock()
        wf.complete_stage.return_value = _make_ok_result()
        ctrl = WorkflowController(workflow_service=wf, resolver=_make_resolver())
        envelope = ctrl.handle(_make_payload("complete_stage", parameters={"artifact_ids": ["art_1"]}))
        assert envelope.status == "success"

    def test_fail_stage_success(self) -> None:
        wf = MagicMock()
        wf.fail_stage.return_value = _make_ok_result()
        ctrl = WorkflowController(workflow_service=wf, resolver=_make_resolver())
        envelope = ctrl.handle(_make_payload("fail_stage", parameters={"error_detail": "OOM"}))
        assert envelope.status == "success"
        assert "OOM" in (envelope.data or {}).get("error_detail", "")

    def test_route_next_success(self) -> None:
        wf = MagicMock()
        wf.route_next.return_value = _make_ok_result(data={"next_stage": "model_training"})
        ctrl = WorkflowController(workflow_service=wf, resolver=_make_resolver())
        envelope = ctrl.handle(_make_payload("route_next"))
        assert envelope.status == "success"
        assert envelope.next_stage == "model_training"

    def test_route_next_service_failure(self) -> None:
        wf = MagicMock()
        wf.route_next.return_value = _make_fail_result("No route defined.")
        ctrl = WorkflowController(workflow_service=wf, resolver=_make_resolver())
        envelope = ctrl.handle(_make_payload("route_next"))
        assert envelope.status == "error"

    def test_unknown_action(self) -> None:
        ctrl = WorkflowController(workflow_service=MagicMock())
        envelope = ctrl.handle(_make_payload("bogus_action"))
        assert envelope.status == "error"
        assert "WorkflowController" in envelope.message


# ---------------------------------------------------------------------------
# ReviewController
# ---------------------------------------------------------------------------

class TestReviewController:
    def test_open_review_success(self) -> None:
        hitl = MagicMock()
        hitl.create_review.return_value = _make_ok_result(data={"review_id": "rev_001"})
        ctrl = ReviewController(hitl_service=hitl, resolver=_make_resolver())
        payload = _make_payload(
            "open_review",
            parameters={"review_type": "generic", "summary_for_reviewer": "Please review."},
        )
        envelope = ctrl.handle(payload)
        assert envelope.status == "success"
        assert envelope.review_created is True
        assert envelope.review_id == "rev_001"

    def test_open_review_service_failure(self) -> None:
        hitl = MagicMock()
        hitl.create_review.return_value = _make_fail_result("Duplicate review.")
        ctrl = ReviewController(hitl_service=hitl, resolver=_make_resolver())
        envelope = ctrl.handle(_make_payload("open_review"))
        assert envelope.status == "error"

    def test_get_review_payload_success(self) -> None:
        hitl = MagicMock()
        hitl.build_review_payload.return_value = _make_ok_result(data={"payload": "data"})
        ctrl = ReviewController(hitl_service=hitl, resolver=_make_resolver())
        payload = _make_payload("get_review_payload", parameters={"review_id": "rev_001"})
        envelope = ctrl.handle(payload)
        assert envelope.status == "success"
        assert envelope.data["review_payload"]["payload"] == "data"

    def test_get_review_payload_missing_id(self) -> None:
        ctrl = ReviewController(hitl_service=MagicMock())
        envelope = ctrl.handle(_make_payload("get_review_payload"))  # no review_id
        assert envelope.status == "error"
        assert "review_id" in envelope.message.lower()

    def test_submit_review_action_success(self) -> None:
        hitl = MagicMock()
        hitl.submit_action.return_value = _make_ok_result(
            data={"decision_id": "dec_001", "audit_id": "aud_001"}
        )
        ctrl = ReviewController(hitl_service=hitl, resolver=_make_resolver())
        payload = _make_payload(
            "submit_review_action",
            parameters={
                "review_id": "rev_001",
                "review_action": "approve",
                "rationale": "Looks good.",
            },
        )
        envelope = ctrl.handle(payload)
        assert envelope.status == "success"

    def test_submit_review_action_missing_fields(self) -> None:
        ctrl = ReviewController(hitl_service=MagicMock())
        envelope = ctrl.handle(_make_payload("submit_review_action"))  # missing review_id + action
        assert envelope.status == "error"
        assert "required" in envelope.message.lower()

    def test_unknown_action(self) -> None:
        ctrl = ReviewController(hitl_service=MagicMock())
        envelope = ctrl.handle(_make_payload("bogus_action"))
        assert envelope.status == "error"
        assert "ReviewController" in envelope.message


# ---------------------------------------------------------------------------
# RecoveryController
# ---------------------------------------------------------------------------

class TestRecoveryController:
    def test_get_recovery_options_success(self) -> None:
        wf = MagicMock()
        wf.get_recovery_recommendation.return_value = _make_ok_result(
            data={"path": "retry"}
        )
        wf.validate_resume.return_value = _make_ok_result(data={"valid": True})
        ctrl = RecoveryController(workflow_service=wf, resolver=_make_resolver())
        envelope = ctrl.handle(_make_payload("get_recovery_options"))
        assert envelope.status == "success"
        assert "recommendation" in (envelope.data or {})

    def test_apply_recovery_success(self) -> None:
        wf = MagicMock()
        wf.apply_recovery.return_value = _make_ok_result(
            data={"current_stage": "data_preparation"}
        )
        ctrl = RecoveryController(workflow_service=wf, resolver=_make_resolver())
        payload = _make_payload(
            "apply_recovery",
            parameters={"recovery_path": "retry"},
        )
        envelope = ctrl.handle(payload)
        assert envelope.status == "success"
        assert envelope.data["restored_stage"] == "data_preparation"

    def test_apply_recovery_missing_path(self) -> None:
        ctrl = RecoveryController(workflow_service=MagicMock())
        envelope = ctrl.handle(_make_payload("apply_recovery"))  # no recovery_path
        assert envelope.status == "error"
        assert "recovery_path" in envelope.message.lower()

    def test_apply_recovery_service_failure(self) -> None:
        wf = MagicMock()
        wf.apply_recovery.return_value = _make_fail_result("Unsupported recovery path.")
        ctrl = RecoveryController(workflow_service=wf, resolver=_make_resolver())
        payload = _make_payload("apply_recovery", parameters={"recovery_path": "rollback"})
        envelope = ctrl.handle(payload)
        assert envelope.status == "error"

    def test_unknown_action(self) -> None:
        ctrl = RecoveryController(workflow_service=MagicMock())
        envelope = ctrl.handle(_make_payload("bogus_action"))
        assert envelope.status == "error"
        assert "RecoveryController" in envelope.message


# ---------------------------------------------------------------------------
# ControllerFactory
# ---------------------------------------------------------------------------

class TestControllerFactory:
    def _make_factory(self) -> ControllerFactory:
        from tests.unit.platform_core.runtime.conftest import minimal_bundle  # type: ignore[import]
        # Build the bundle using the conftest fixture function
        from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
        from sdk.platform_core.runtime.config_models.enums import AccessModeEnum, StageClassEnum
        from sdk.platform_core.runtime.config_models.governance import (
            DefaultGovernanceRules,
            GovernanceOverlaysConfig,
            GovernanceOverlaysSection,
        )
        from sdk.platform_core.runtime.config_models.retries import (
            RetryDefaults,
            RetryPoliciesConfig,
            RetryPoliciesSection,
        )
        from sdk.platform_core.runtime.config_models.roles import (
            RoleCapabilitiesConfig,
            RoleCapabilityDefinition,
        )
        from sdk.platform_core.runtime.config_models.routes import (
            WorkflowRouteDefinition,
            WorkflowRoutesConfig,
        )
        from sdk.platform_core.runtime.config_models.runtime_master import (
            RuntimeMasterConfig,
            RuntimeMasterSection,
        )
        from sdk.platform_core.runtime.config_models.stages import (
            StageDefinition,
            StageRegistryConfig,
            StageToolMatrixConfig,
            StageToolMatrixEntry,
        )
        from sdk.platform_core.runtime.config_models.tool_groups import (
            ToolGroupDefinition,
            ToolGroupsConfig,
        )
        from sdk.platform_core.runtime.config_models.ui import (
            InteractionModeDefinition,
            InteractionModesConfig,
            TokenModeDefinition,
            TokenModesConfig,
            UIModeDefinition,
            UIModesConfig,
        )
        from sdk.platform_core.runtime.config_models.enums import (
            InteractionModeEnum,
            TokenModeEnum,
            UIModeEnum,
        )

        stages = {
            "stage_a": StageDefinition(
                stage_name="stage_a",
                stage_class=StageClassEnum.BUILD,
                default_access_mode=AccessModeEnum.BUILD_ONLY,
            )
        }
        bundle = RuntimeConfigBundle(
            runtime_master=RuntimeMasterConfig(runtime=RuntimeMasterSection()),
            tool_groups=ToolGroupsConfig(
                groups={"grp_a": ToolGroupDefinition(group_name="grp_a", tools=["tool1"])}
            ),
            role_capabilities=RoleCapabilitiesConfig(
                roles={
                    "developer": RoleCapabilityDefinition(
                        role="developer",
                        allowed_tool_groups=["grp_a"],
                        blocked_tool_groups=[],
                        allowed_stages=["stage_a"],
                    )
                }
            ),
            ui_modes=UIModesConfig(
                modes={"ws": UIModeDefinition(mode=UIModeEnum.BOOTSTRAP_WORKSPACE)}
            ),
            interaction_modes=InteractionModesConfig(
                modes={"edit": InteractionModeDefinition(mode=InteractionModeEnum.EDIT_AND_FINALIZE)}
            ),
            token_modes=TokenModesConfig(
                modes={"full": TokenModeDefinition(mode=TokenModeEnum.FULL)}
            ),
            stage_registry=StageRegistryConfig(stages=stages),
            stage_tool_matrix=StageToolMatrixConfig(
                matrix={"stage_a": StageToolMatrixEntry(stage_name="stage_a", allowed_groups=["grp_a"])}
            ),
            governance_overlays=GovernanceOverlaysConfig(
                governance=GovernanceOverlaysSection(default_rules=DefaultGovernanceRules())
            ),
            retry_policies=RetryPoliciesConfig(
                retry_policies=RetryPoliciesSection(defaults=RetryDefaults())
            ),
            workflow_routes=WorkflowRoutesConfig(
                routes={"stage_a": WorkflowRouteDefinition(stage_name="stage_a")}
            ),
        )

        container = MagicMock()
        container.get.side_effect = lambda name: MagicMock()
        container.has.return_value = False
        return ControllerFactory(bundle=bundle, container=container)

    def test_factory_creates_session_controller(self) -> None:
        factory = self._make_factory()
        ctrl = factory.session()
        assert isinstance(ctrl, SessionController)

    def test_factory_creates_workflow_controller(self) -> None:
        factory = self._make_factory()
        ctrl = factory.workflow()
        assert isinstance(ctrl, WorkflowController)

    def test_factory_creates_review_controller(self) -> None:
        factory = self._make_factory()
        ctrl = factory.review()
        assert isinstance(ctrl, ReviewController)

    def test_factory_creates_recovery_controller(self) -> None:
        factory = self._make_factory()
        ctrl = factory.recovery()
        assert isinstance(ctrl, RecoveryController)

    def test_factory_caches_controllers(self) -> None:
        factory = self._make_factory()
        ctrl1 = factory.session()
        ctrl2 = factory.session()
        assert ctrl1 is ctrl2
