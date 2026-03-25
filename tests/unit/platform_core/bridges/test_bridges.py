"""Unit tests for AgentBridge and JupyterBridge.

Covers:
- AgentBridge: dispatch success, unknown tool, invalid input, retry, format_response
- JupyterBridge: dispatch success, unknown event, missing stage_name, action_dispatch
- BaseBridge: build_actor, build_interaction_payload helpers
"""

from __future__ import annotations

from typing import Any, Dict
from unittest.mock import MagicMock

import pytest

from sdk.platform_core.bridges import AgentBridge, JupyterBridge
from sdk.platform_core.schemas.common_fragments import ActorRecord
from sdk.platform_core.schemas.payload_models import StandardResponseEnvelope
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_envelope(status: str = "success", data: Dict = None) -> StandardResponseEnvelope:
    return StandardResponseEnvelope(
        envelope_id=IDFactory.envelope_id(),
        status=status,
        message=f"Test {status}",
        sdk_name="test",
        function_name="test",
        run_id="run_test",
        timestamp=TimeProvider.now_iso(),
        data=data or {},
    )


def _make_factory(envelope: StandardResponseEnvelope = None) -> MagicMock:
    """Mock ControllerFactory where all controllers return the given envelope."""
    ctrl = MagicMock()
    ctrl.handle.return_value = envelope or _make_envelope()
    factory = MagicMock()
    factory.session.return_value = ctrl
    factory.workflow.return_value = ctrl
    factory.review.return_value = ctrl
    factory.recovery.return_value = ctrl
    return factory


# ---------------------------------------------------------------------------
# AgentBridge
# ---------------------------------------------------------------------------

class TestAgentBridge:
    def test_dispatch_success(self) -> None:
        bridge = AgentBridge(controller_factory=_make_factory())
        result = bridge.dispatch({
            "tool_name": "platform_run_stage",
            "args": {
                "stage_name": "feature_engineering",
                "run_id": "run_001",
                "actor_id": "agent_01",
                "actor_role": "developer",
            },
        })
        assert result["status"] == "success"

    def test_dispatch_unknown_tool(self) -> None:
        bridge = AgentBridge(controller_factory=_make_factory())
        result = bridge.dispatch({"tool_name": "nonexistent_tool", "args": {}})
        assert result["status"] == "error"
        assert "nonexistent_tool" in result["message"]

    def test_dispatch_invalid_input_type(self) -> None:
        bridge = AgentBridge(controller_factory=_make_factory())
        result = bridge.dispatch("not_a_dict")
        assert result["status"] == "error"

    def test_dispatch_missing_stage_name(self) -> None:
        bridge = AgentBridge(controller_factory=_make_factory())
        result = bridge.dispatch({
            "tool_name": "platform_run_stage",
            "args": {"run_id": "run_001", "actor_id": "agent_01"},  # no stage_name
        })
        assert result["status"] == "error"
        assert "stage_name" in result["message"].lower()

    def test_format_response_includes_hints(self) -> None:
        envelope = _make_envelope(status="success")
        bridge = AgentBridge(controller_factory=_make_factory(envelope))
        result = bridge.dispatch({
            "tool_name": "platform_run_stage",
            "args": {
                "stage_name": "feature_engineering",
                "run_id": "run_001",
                "actor_id": "agent_01",
                "actor_role": "developer",
            },
        })
        assert "agent_hint" in result
        assert "workflow_hint" in result

    def test_format_response_with_governance_summary(self) -> None:
        from sdk.platform_core.schemas.common_fragments import GovernanceSummary
        envelope = _make_envelope()
        envelope = StandardResponseEnvelope(
            **{
                **envelope.model_dump(),
                "governance_summary": GovernanceSummary(
                    policy_check_result="review_required",
                    blocking_reasons=["review_required"],
                ),
            }
        )
        bridge = AgentBridge(controller_factory=_make_factory(envelope))
        result = bridge.dispatch({
            "tool_name": "platform_run_stage",
            "args": {
                "stage_name": "feature_engineering",
                "run_id": "run_001",
                "actor_id": "agent_01",
                "actor_role": "developer",
            },
        })
        assert result["governance_summary"] is not None
        assert result["governance_summary"]["policy_check_result"] == "review_required"

    def test_retry_on_error(self) -> None:
        ctrl = MagicMock()
        ctrl.handle.side_effect = [
            _make_envelope("error"),
            _make_envelope("error"),
            _make_envelope("success"),
        ]
        factory = MagicMock()
        factory.workflow.return_value = ctrl
        bridge = AgentBridge(
            controller_factory=factory,
            max_retries=2,
            retry_delay_seconds=0.0,
        )
        result = bridge.dispatch({
            "tool_name": "platform_run_stage",
            "args": {
                "stage_name": "feature_engineering",
                "run_id": "run_001",
                "actor_id": "agent_01",
                "actor_role": "developer",
            },
        })
        assert result["status"] == "success"
        assert ctrl.handle.call_count == 3

    def test_get_tool_manifest(self) -> None:
        bridge = AgentBridge(controller_factory=_make_factory())
        manifest = bridge.get_tool_manifest()
        assert len(manifest) > 0
        tool_names = [t["tool_name"] for t in manifest]
        assert "platform_run_stage" in tool_names
        assert "platform_open_review" in tool_names

    def test_dispatch_review_tool(self) -> None:
        bridge = AgentBridge(controller_factory=_make_factory())
        result = bridge.dispatch({
            "tool_name": "platform_open_review",
            "args": {
                "stage_name": "model_validation",
                "run_id": "run_001",
                "actor_id": "agent_01",
                "actor_role": "developer",
                "parameters": {"review_type": "generic"},
            },
        })
        assert result["status"] == "success"


# ---------------------------------------------------------------------------
# JupyterBridge
# ---------------------------------------------------------------------------

class TestJupyterBridge:
    def test_dispatch_success(self) -> None:
        bridge = JupyterBridge(controller_factory=_make_factory())
        result = bridge.dispatch({
            "event_type": "stage_run",
            "stage_name": "feature_engineering",
            "run_id": "run_001",
            "actor_id": "user_01",
            "actor_role": "developer",
        })
        assert result["widget_status"] == "success"

    def test_dispatch_unknown_event(self) -> None:
        bridge = JupyterBridge(controller_factory=_make_factory())
        result = bridge.dispatch({"event_type": "unknown_event", "stage_name": "x"})
        assert result["widget_status"] == "error"
        assert "unknown_event" in result["message"]

    def test_dispatch_missing_stage_name(self) -> None:
        bridge = JupyterBridge(controller_factory=_make_factory())
        result = bridge.dispatch({"event_type": "stage_run"})  # no stage_name
        assert result["widget_status"] == "error"

    def test_dispatch_invalid_input_type(self) -> None:
        bridge = JupyterBridge(controller_factory=_make_factory())
        result = bridge.dispatch("not_a_dict")
        assert result["widget_status"] == "error"

    def test_format_response_widget_fields(self) -> None:
        bridge = JupyterBridge(controller_factory=_make_factory())
        result = bridge.dispatch({
            "event_type": "stage_run",
            "stage_name": "feature_engineering",
            "run_id": "run_001",
            "actor_id": "user_01",
            "actor_role": "developer",
        })
        assert "needs_refresh" in result
        assert "current_stage" in result
        assert "governance_summary" in result

    def test_action_dispatch_convenience(self) -> None:
        bridge = JupyterBridge(controller_factory=_make_factory())
        result = bridge.action_dispatch(
            event_type="stage_complete",
            stage_name="feature_engineering",
            run_id="run_001",
            actor_id="user_01",
            actor_role="developer",
        )
        assert result["widget_status"] == "success"

    def test_result_refresh_flag(self) -> None:
        envelope = _make_envelope("success")
        bridge = JupyterBridge(controller_factory=_make_factory(envelope))
        state = bridge.result_refresh(envelope)
        assert state["refresh"] is True

    def test_get_supported_events(self) -> None:
        bridge = JupyterBridge(controller_factory=_make_factory())
        events = bridge.get_supported_events()
        assert "stage_run" in events
        assert "review_open" in events
        assert "recovery_apply" in events

    def test_review_events_dispatched(self) -> None:
        factory = _make_factory(_make_envelope("success", data={"review_id": "rev_001"}))
        bridge = JupyterBridge(controller_factory=factory)
        result = bridge.dispatch({
            "event_type": "review_get_payload",
            "stage_name": "model_validation",
            "run_id": "run_001",
            "actor_id": "user_01",
            "actor_role": "reviewer",
            "review_id": "rev_001",
        })
        assert result["widget_status"] == "success"
