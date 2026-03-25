"""Unit tests for api_bridge and cli_bridge.

Covers:
- ApiBridge: route matching, auth hooks, request mapping, response formatting.
- CliBridge: argument parsing, command routing, output formatting.
"""

from __future__ import annotations

import types
from typing import Any


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _make_envelope(
    status: str = "ok",
    message: str = "ok",
    data: Any = None,
) -> Any:
    """Create a minimal mock StandardResponseEnvelope."""
    env = types.SimpleNamespace()
    env.status = status
    env.message = message
    env.data = data
    env.next_stage = None
    env.review_created = False
    env.review_id = None
    env.audit_ref = None
    env.event_ref = None
    env.warnings = []
    env.errors = []
    env.agent_hint = ""
    env.workflow_hint = ""
    env.governance_summary = None
    return env


class _FakeController:
    def __init__(self, envelope: Any) -> None:
        self._env = envelope

    def handle(self, payload: Any) -> Any:
        return self._env


class _FakeFactory:
    def __init__(self, envelope: Any) -> None:
        self._env = envelope

    def session(self) -> _FakeController:
        return _FakeController(self._env)

    def workflow(self) -> _FakeController:
        return _FakeController(self._env)

    def review(self) -> _FakeController:
        return _FakeController(self._env)

    def recovery(self) -> _FakeController:
        return _FakeController(self._env)


# ---------------------------------------------------------------------------
# ApiBridge tests
# ---------------------------------------------------------------------------

class TestApiBridge:
    def _bridge(self, envelope_status: str = "ok") -> Any:
        from sdk.api_bridge.api_bridge import ApiBridge
        env = _make_envelope(status=envelope_status)
        factory = _FakeFactory(env)
        return ApiBridge(
            controller_factory=factory,
            known_tokens={"tok-valid": {"actor_id": "svc-01", "actor_role": "developer"}},
        )

    def test_valid_post_stage_start(self) -> None:
        bridge = self._bridge()
        resp = bridge.dispatch({
            "method": "POST",
            "path": "/runs/run-001/stages/feature_engineering/start",
            "headers": {"Authorization": "Bearer tok-valid"},
            "body": {"project_id": "proj-001"},
        })
        assert resp["status_code"] == 200
        assert resp["body"]["status"] == "ok"

    def test_auth_failure_returns_401(self) -> None:
        bridge = self._bridge()
        resp = bridge.dispatch({
            "method": "POST",
            "path": "/runs/run-001/stages/feature_engineering/start",
            "headers": {},
            "body": {},
        })
        assert resp["status_code"] == 401
        assert resp["body"]["error_code"] == "unauthorized"

    def test_unknown_route_returns_404(self) -> None:
        bridge = self._bridge()
        resp = bridge.dispatch({
            "method": "GET",
            "path": "/unknown/endpoint",
            "headers": {},
            "body": {"actor_id": "u1", "actor_role": "developer"},
        })
        assert resp["status_code"] == 404

    def test_inline_actor_bypasses_token(self) -> None:
        bridge = self._bridge()
        resp = bridge.dispatch({
            "method": "POST",
            "path": "/sessions",
            "headers": {},
            "body": {
                "actor_id": "svc-internal",
                "actor_role": "orchestrator",
                "project_id": "proj-001",
                "run_id": "run-001",
            },
        })
        assert resp["status_code"] == 200

    def test_error_envelope_gives_422(self) -> None:
        bridge = self._bridge(envelope_status="error")
        resp = bridge.dispatch({
            "method": "POST",
            "path": "/sessions",
            "headers": {},
            "body": {
                "actor_id": "u1",
                "actor_role": "developer",
                "project_id": "p",
                "run_id": "r",
            },
        })
        assert resp["status_code"] == 422

    def test_get_routes_returns_list(self) -> None:
        bridge = self._bridge()
        routes = bridge.get_routes()
        assert len(routes) > 0
        assert all("method" in r and "path" in r for r in routes)

    def test_invalid_raw_input_returns_400(self) -> None:
        bridge = self._bridge()
        resp = bridge.dispatch("not-a-dict")
        assert resp["status_code"] == 400

    def test_validate_bearer_token_unknown(self) -> None:
        from sdk.api_bridge.api_bridge import validate_bearer_token
        assert validate_bearer_token("bad-token", {"valid": {"actor_id": "x", "actor_role": "y"}}) is None

    def test_validate_bearer_token_known(self) -> None:
        from sdk.api_bridge.api_bridge import validate_bearer_token
        result = validate_bearer_token("tok-abc", {"tok-abc": {"actor_id": "a", "actor_role": "dev"}})
        assert result is not None
        assert result["actor_id"] == "a"


# ---------------------------------------------------------------------------
# CliBridge tests
# ---------------------------------------------------------------------------

class TestCliBridge:
    def _bridge(self, envelope_status: str = "ok") -> Any:
        from sdk.cli_bridge.cli_bridge import CliBridge
        env = _make_envelope(status=envelope_status, message="Stage started.")
        factory = _FakeFactory(env)
        return CliBridge(controller_factory=factory)

    def test_string_command_dispatches(self) -> None:
        bridge = self._bridge()
        out = bridge.dispatch("stage start --stage-name prep --run-id r001 --project-id proj001")
        assert "[OK]" in out
        assert "Stage started" in out

    def test_dict_command_dispatches(self) -> None:
        bridge = self._bridge()
        out = bridge.dispatch({
            "command": "stage start",
            "stage_name": "prep",
            "run_id": "r001",
            "project_id": "proj001",
        })
        assert "[OK]" in out

    def test_unknown_command_returns_error(self) -> None:
        bridge = self._bridge()
        out = bridge.dispatch("unknown command --foo bar")
        assert "[ERROR]" in out

    def test_missing_required_arg(self) -> None:
        bridge = self._bridge()
        out = bridge.dispatch("stage start --run-id r001")
        assert "[ERROR]" in out
        assert "stage_name" in out or "stage-name" in out

    def test_error_envelope_output(self) -> None:
        bridge = self._bridge(envelope_status="error")
        out = bridge.dispatch({
            "command": "stage start",
            "stage_name": "prep",
            "run_id": "r001",
        })
        assert "[ERROR]" in out

    def test_get_help(self) -> None:
        bridge = self._bridge()
        help_text = bridge.get_help()
        assert "stage start" in help_text
        assert "session open" in help_text

    def test_invalid_raw_input_type(self) -> None:
        bridge = self._bridge()
        out = bridge.dispatch(42)
        assert "[ERROR]" in out


class TestParseArguments:
    def test_two_part_command(self) -> None:
        from sdk.cli_bridge.cli_bridge import parse_arguments
        cmd, args = parse_arguments(["stage", "start", "--stage-name", "prep", "--run-id", "r1"])
        assert cmd == "stage start"
        assert args["stage_name"] == "prep"
        assert args["run_id"] == "r1"

    def test_flag_argument(self) -> None:
        from sdk.cli_bridge.cli_bridge import parse_arguments
        cmd, args = parse_arguments(["session", "open", "--verbose"])
        assert cmd == "session open"
        assert args["verbose"] is True

    def test_empty_tokens_raises(self) -> None:
        from sdk.cli_bridge.cli_bridge import parse_arguments
        import pytest
        with pytest.raises(ValueError):
            parse_arguments([])


# ---------------------------------------------------------------------------
# Sidebars tests
# ---------------------------------------------------------------------------

class TestSidebars:
    def test_build_workflow_tree(self) -> None:
        from widgetsdk.sidebars import build_workflow_tree, WorkflowTreeNodeStatus

        stages = [
            {"name": "data_prep", "status": "completed"},
            {"name": "feature_engineering", "status": "in_progress"},
            {"name": "model_training", "status": "pending"},
        ]
        sidebar = build_workflow_tree("run-001", "proj-001", stages, active_stage="feature_engineering")
        assert sidebar.active_node_id == "stage-feature_engineering"
        project_node = sidebar.tree[0]
        children = project_node.children
        statuses = {c.node_id: c.status for c in children}
        assert statuses["stage-data_prep"] == WorkflowTreeNodeStatus.COMPLETED
        assert statuses["stage-feature_engineering"] == WorkflowTreeNodeStatus.IN_PROGRESS
        assert children[1].is_active is True

    def test_build_agent_console(self) -> None:
        from widgetsdk.sidebars import build_agent_console

        console = build_agent_console(
            run_id="run-001",
            project_id="proj-001",
            stage_name="model_review",
            messages=[{"message_id": "m1", "role": "agent", "content": "Review ready."}],
            token_budget_used=1024,
        )
        assert len(console.chat_messages) == 1
        assert console.token_budget_used == 1024
        assert len(console.console_actions) > 0

    def test_build_bottom_panel(self) -> None:
        from widgetsdk.sidebars import build_bottom_panel

        panel = build_bottom_panel(
            run_id="run-001",
            project_id="proj-001",
            stage_name="data_prep",
            status_message="Running DQ checks...",
            progress_pct=45.0,
        )
        assert panel.progress_pct == 45.0
        assert panel.status_message == "Running DQ checks..."

    def test_render_sidebar_terminal(self) -> None:
        from widgetsdk.sidebars import build_workflow_tree, render_sidebar_terminal

        stages = [{"name": "prep", "status": "completed"}]
        sidebar = build_workflow_tree("r1", "p1", stages)
        rendered = render_sidebar_terminal(sidebar)
        assert "LEFT SIDEBAR" in rendered
        assert "Prep" in rendered

    def test_render_right_sidebar_terminal(self) -> None:
        from widgetsdk.sidebars import build_agent_console, render_sidebar_terminal

        console = build_agent_console(
            "r1", "p1", messages=[{"message_id": "m1", "role": "user", "content": "Hello"}]
        )
        rendered = render_sidebar_terminal(console)
        assert "RIGHT SIDEBAR" in rendered

    def test_render_bottom_panel_terminal(self) -> None:
        from widgetsdk.sidebars import build_bottom_panel, render_sidebar_terminal

        panel = build_bottom_panel("r1", "p1", progress_pct=80.0)
        rendered = render_sidebar_terminal(panel)
        assert "BOTTOM PANEL" in rendered
        assert "80" in rendered
