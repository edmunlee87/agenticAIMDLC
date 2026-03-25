"""Unit tests for platform skills.

Covers:
- PlatformBaseRules: check_before_complete, check_material_action_logged
- ModelLifecycleOrchestrator: execute_stage (completed, paused, blocked, failed)
- SessionBootstrapOrchestrator: bootstrap (new, resume, auto-discover)
- RecoveryOrchestrator: inspect_and_recommend, apply_recovery
"""

from __future__ import annotations

import sys
from typing import Any, Dict
from unittest.mock import MagicMock

import pytest

from skills.platform.shared.base_rules import PlatformBaseRules


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ok_bridge_response(data: Dict = None, next_stage: str = "") -> Dict[str, Any]:
    return {
        "status": "success",
        "message": "ok",
        "data": data or {},
        "next_stage": next_stage,
        "review_created": False,
        "review_id": None,
        "audit_ref": "aud_001",
        "event_ref": "evt_001",
        "governance_summary": None,
        "errors": [],
        "warnings": [],
        "agent_hint": "",
        "workflow_hint": "",
    }


def _fail_bridge_response(message: str = "fail") -> Dict[str, Any]:
    return {
        "status": "error",
        "message": message,
        "data": None,
        "next_stage": None,
        "review_created": False,
        "review_id": None,
        "audit_ref": None,
        "event_ref": None,
        "governance_summary": None,
        "errors": [message],
        "warnings": [],
        "agent_hint": "",
        "workflow_hint": "",
    }


def _make_bridge(responses: list) -> MagicMock:
    """Build a mock bridge that returns responses in order."""
    bridge = MagicMock()
    bridge.dispatch.side_effect = responses
    return bridge


# ---------------------------------------------------------------------------
# PlatformBaseRules
# ---------------------------------------------------------------------------

class TestPlatformBaseRules:
    def test_check_before_complete_passes_with_artifacts(self) -> None:
        rules = PlatformBaseRules()
        result = rules.check_before_complete(
            stage_name="feature_engineering",
            run_id="run_001",
            artifact_ids=["art_001"],
        )
        assert result.passed is True
        assert len(result.violations) == 0

    def test_check_before_complete_fails_without_artifacts(self) -> None:
        rules = PlatformBaseRules()
        result = rules.check_before_complete(
            stage_name="feature_engineering",
            run_id="run_001",
            artifact_ids=[],
        )
        assert result.passed is False
        assert any(v.rule_id == PlatformBaseRules.RULE_NO_SILENT_FINALIZATION for v in result.violations)

    def test_check_before_complete_fails_without_selection(self) -> None:
        rules = PlatformBaseRules()
        result = rules.check_before_complete(
            stage_name="candidate_selection",
            run_id="run_001",
            artifact_ids=["art_001"],
            requires_selection=True,
            selected_candidate_id=None,
        )
        assert result.passed is False
        assert any(v.rule_id == PlatformBaseRules.RULE_NO_IMPLICIT_SELECTION for v in result.violations)

    def test_check_before_complete_passes_with_selection(self) -> None:
        rules = PlatformBaseRules()
        result = rules.check_before_complete(
            stage_name="candidate_selection",
            run_id="run_001",
            artifact_ids=["art_001"],
            requires_selection=True,
            selected_candidate_id="candidate_001",
        )
        assert result.passed is True

    def test_check_material_action_logged_both_refs(self) -> None:
        rules = PlatformBaseRules()
        result = rules.check_material_action_logged(
            action_name="complete_stage",
            run_id="run_001",
            stage_name="feature_engineering",
            event_ref="evt_001",
            audit_ref="aud_001",
        )
        assert result.passed is True

    def test_check_material_action_logged_missing_event(self) -> None:
        rules = PlatformBaseRules()
        result = rules.check_material_action_logged(
            action_name="complete_stage",
            run_id="run_001",
            stage_name="feature_engineering",
            event_ref=None,
            audit_ref="aud_001",
        )
        assert len(result.violations) > 0

    def test_check_material_action_not_material(self) -> None:
        rules = PlatformBaseRules()
        result = rules.check_material_action_logged(
            action_name="ping",
            run_id="run_001",
            stage_name="x",
            event_ref=None,
            audit_ref=None,
            is_material=False,
        )
        assert result.passed is True

    def test_strict_mode_blocks_warnings(self) -> None:
        rules = PlatformBaseRules(strict_mode=True)
        result = rules.check_material_action_logged(
            action_name="complete_stage",
            run_id="run_001",
            stage_name="feature_engineering",
            event_ref=None,
            audit_ref="aud_001",
        )
        assert result.passed is False


# ---------------------------------------------------------------------------
# ModelLifecycleOrchestrator
# ---------------------------------------------------------------------------

class TestModelLifecycleOrchestrator:
    def _make_orchestrator(self, bridge: Any) -> Any:
        import importlib.util, os
        mod_name = "model_lifecycle_skill"
        if mod_name not in sys.modules:
            spec = importlib.util.spec_from_file_location(
                mod_name,
                os.path.join(
                    os.path.dirname(__file__),
                    "../../../../skills/platform/model-lifecycle-orchestrator/skill.py",
                ),
            )
            mod = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = mod
            spec.loader.exec_module(mod)
        else:
            mod = sys.modules[mod_name]
        return mod.ModelLifecycleOrchestrator(bridge=bridge)

    def test_execute_stage_completed(self) -> None:
        bridge = _make_bridge([
            _ok_bridge_response(),  # run_stage
            _ok_bridge_response(data={"next_stage": "model_training"}),  # complete_stage
            _ok_bridge_response(data={"next_stage": "model_training"}),  # route_next
        ])
        orch = self._make_orchestrator(bridge)
        outcome = orch.execute_stage(
            stage_name="feature_engineering",
            run_id="run_001",
            project_id="proj_001",
            actor_id="agent_01",
            actor_role="developer",
            artifact_ids=["art_001"],
        )
        assert outcome.status == "completed"
        assert outcome.next_stage == "model_training"

    def test_execute_stage_blocked_no_artifacts(self) -> None:
        bridge = _make_bridge([_ok_bridge_response()])
        orch = self._make_orchestrator(bridge)
        outcome = orch.execute_stage(
            stage_name="feature_engineering",
            run_id="run_001",
            project_id="proj_001",
            actor_id="agent_01",
            actor_role="developer",
            artifact_ids=[],  # triggers R001
        )
        assert outcome.status == "blocked"
        assert "artifact" in outcome.error.lower()

    def test_execute_stage_paused_for_review(self) -> None:
        run_response = _ok_bridge_response()
        run_response["governance_summary"] = {"blocking_reasons": ["review_required"]}
        bridge = _make_bridge([
            run_response,
            _ok_bridge_response(data={"review_id": "rev_001"}),  # open_review
        ])
        orch = self._make_orchestrator(bridge)
        outcome = orch.execute_stage(
            stage_name="model_validation",
            run_id="run_001",
            project_id="proj_001",
            actor_id="agent_01",
            actor_role="developer",
            artifact_ids=["art_001"],
        )
        assert outcome.status == "paused_for_review"

    def test_execute_stage_run_failed(self) -> None:
        bridge = _make_bridge([_fail_bridge_response("Stage already running.")])
        orch = self._make_orchestrator(bridge)
        outcome = orch.execute_stage(
            stage_name="feature_engineering",
            run_id="run_001",
            project_id="proj_001",
            actor_id="agent_01",
            actor_role="developer",
            artifact_ids=["art_001"],
        )
        assert outcome.status == "failed"
        assert "already running" in outcome.error


# ---------------------------------------------------------------------------
# SessionBootstrapOrchestrator
# ---------------------------------------------------------------------------

class TestSessionBootstrapOrchestrator:
    def _make_bootstrap(self, bridge: Any, registry: Any = None) -> Any:
        import importlib.util, os
        mod_name = "session_bootstrap_skill"
        if mod_name not in sys.modules:
            spec = importlib.util.spec_from_file_location(
                mod_name,
                os.path.join(
                    os.path.dirname(__file__),
                    "../../../../skills/platform/session-bootstrap-orchestrator/skill.py",
                ),
            )
            mod = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = mod
            spec.loader.exec_module(mod)
        else:
            mod = sys.modules[mod_name]
        return mod.SessionBootstrapOrchestrator(bridge=bridge, registry_service=registry)

    def test_bootstrap_new_session(self) -> None:
        bridge = _make_bridge([
            _ok_bridge_response(data={"session_id": "ses_new"}),
        ])
        orch = self._make_bootstrap(bridge)
        result = orch.bootstrap(
            actor_id="agent_01",
            actor_role="developer",
            run_id="run_001",
            project_id="proj_001",
        )
        assert result.success is True
        assert result.context.is_resumed is False
        assert result.context.session_id == "ses_new"

    def test_bootstrap_resumes_existing_session(self) -> None:
        bridge = _make_bridge([
            _ok_bridge_response(data={"session_id": "ses_existing"}),
        ])
        orch = self._make_bootstrap(bridge)
        result = orch.bootstrap(
            actor_id="agent_01",
            actor_role="developer",
            run_id="run_001",
            project_id="proj_001",
            session_id="ses_existing",
        )
        assert result.success is True
        assert result.context.is_resumed is True

    def test_bootstrap_falls_back_on_resume_failure(self) -> None:
        bridge = _make_bridge([
            _fail_bridge_response("Session not found."),   # resume fails
            _ok_bridge_response(data={"session_id": "ses_new"}),  # open new
        ])
        orch = self._make_bootstrap(bridge)
        result = orch.bootstrap(
            actor_id="agent_01",
            actor_role="developer",
            run_id="run_001",
            project_id="proj_001",
            session_id="ses_missing",
        )
        assert result.success is True
        assert result.context.is_resumed is False

    def test_bootstrap_fails_when_open_fails(self) -> None:
        bridge = _make_bridge([_fail_bridge_response("Cannot open session.")])
        orch = self._make_bootstrap(bridge)
        result = orch.bootstrap(
            actor_id="agent_01",
            actor_role="developer",
            run_id="run_001",
            project_id="proj_001",
        )
        assert result.success is False
        assert "Cannot open session" in result.error


# ---------------------------------------------------------------------------
# RecoveryOrchestrator
# ---------------------------------------------------------------------------

class TestRecoveryOrchestrator:
    def _make_recovery(self, bridge: Any) -> Any:
        import importlib.util, os
        mod_name = "recovery_orchestrator_skill"
        if mod_name not in sys.modules:
            spec = importlib.util.spec_from_file_location(
                mod_name,
                os.path.join(
                    os.path.dirname(__file__),
                    "../../../../skills/platform/recovery-orchestrator/skill.py",
                ),
            )
            mod = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = mod
            spec.loader.exec_module(mod)
        else:
            mod = sys.modules[mod_name]
        return mod.RecoveryOrchestrator(bridge=bridge)

    def test_inspect_and_recommend_retry(self) -> None:
        bridge = _make_bridge([
            _ok_bridge_response(data={"recommendation": {"path": "retry"}, "resume_validation": {"can_resume": True}}),
        ])
        orch = self._make_recovery(bridge)
        rec = orch.inspect_and_recommend(
            run_id="run_001",
            project_id="proj_001",
            actor_id="agent_01",
            actor_role="developer",
            stage_name="feature_engineering",
        )
        assert rec.recommended_path == "retry"
        assert rec.confidence > 0.5

    def test_apply_recovery_success(self) -> None:
        bridge = _make_bridge([
            _ok_bridge_response(data={"recommendation": {"path": "retry"}, "resume_validation": {"can_resume": True}}),
            _ok_bridge_response(data={"restored_stage": "feature_engineering"}),
        ])
        orch = self._make_recovery(bridge)
        result = orch.apply_recovery(
            run_id="run_001",
            project_id="proj_001",
            actor_id="agent_01",
            actor_role="developer",
            stage_name="feature_engineering",
            recovery_path="retry",
        )
        assert result.success is True
        assert result.applied is True
        assert result.restored_stage == "feature_engineering"

    def test_apply_recovery_failure(self) -> None:
        bridge = _make_bridge([
            _ok_bridge_response(data={"recommendation": {"path": "retry"}}),
            _fail_bridge_response("Recovery not supported."),
        ])
        orch = self._make_recovery(bridge)
        result = orch.apply_recovery(
            run_id="run_001",
            project_id="proj_001",
            actor_id="agent_01",
            actor_role="developer",
            stage_name="feature_engineering",
            recovery_path="retry",
        )
        assert result.success is False
        assert "Recovery not supported" in result.error

    def test_apply_recovery_no_auto_apply(self) -> None:
        bridge = _make_bridge([
            _ok_bridge_response(data={"recommendation": {"path": "retry"}}),
        ])
        orch = self._make_recovery(bridge)
        result = orch.apply_recovery(
            run_id="run_001",
            project_id="proj_001",
            actor_id="agent_01",
            actor_role="developer",
            stage_name="feature_engineering",
            auto_apply=False,  # no auto-apply, no explicit path
        )
        assert result.success is True
        assert result.applied is False
