"""Unit tests for ObservabilityService."""

import pytest

from sdk.observabilitysdk.event_store import InMemoryEventStore
from sdk.observabilitysdk.observability_service import ObservabilityService
from sdk.observabilitysdk.models import TokenUsage


@pytest.fixture()
def svc() -> ObservabilityService:
    return ObservabilityService(run_id="run_001", actor="test_actor")


@pytest.fixture()
def failing_store() -> InMemoryEventStore:
    return InMemoryEventStore(fail_on_write=True)


class TestCreateTrace:
    def test_create_trace_success(self, svc: ObservabilityService) -> None:
        result = svc.create_trace(
            skill_name="model-lifecycle-orchestrator",
            stage_name="session_bootstrap",
            run_id="run_001",
            project_id="proj_001",
        )
        assert result.is_success
        assert "trace_id" in result.data

    def test_trace_id_in_store(self, svc: ObservabilityService) -> None:
        result = svc.create_trace(
            skill_name="skill_a",
            stage_name="stage_a",
        )
        trace_id = result.data["trace_id"]
        event = svc._store.get_by_id(trace_id)
        assert event is not None
        assert event.event_type == "trace_start"


class TestWriteEvent:
    def test_write_event_success(self, svc: ObservabilityService) -> None:
        result = svc.write_event(
            event_type="skill_start",
            stage_name="session_bootstrap",
            run_id="run_001",
        )
        assert result.is_success
        assert "event_id" in result.data

    def test_event_stored(self, svc: ObservabilityService) -> None:
        result = svc.write_event(event_type="skill_start")
        event_id = result.data["event_id"]
        event = svc._store.get_by_id(event_id)
        assert event is not None
        assert event.event_type == "skill_start"

    def test_write_with_token_usage(self, svc: ObservabilityService) -> None:
        usage = TokenUsage(prompt_tokens=1024, completion_tokens=256, total_tokens=1280)
        result = svc.write_event(
            event_type="skill_finish",
            token_usage=usage,
        )
        assert result.is_success
        event = svc._store.get_by_id(result.data["event_id"])
        assert event.token_usage is not None
        assert event.token_usage.total_tokens == 1280

    def test_governance_gate_hit_stored(self, svc: ObservabilityService) -> None:
        svc.write_event(event_type="policy_check_failed", governance_gate_hit=True)
        events = svc._store.query(filters={"governance_gate_hit": True})
        assert len(events) == 1

    def test_review_created_stored(self, svc: ObservabilityService) -> None:
        svc.write_event(event_type="review_created", review_created=True)
        events = svc._store.query(filters={"review_created": True})
        assert len(events) == 1


class TestWriteFailureBlocking:
    def test_write_failure_blocks_service(self, failing_store: InMemoryEventStore) -> None:
        svc = ObservabilityService(event_store=failing_store)
        result = svc.write_event(event_type="skill_start")
        assert result.status == "blocked"
        assert svc._write_blocked is True

    def test_subsequent_writes_blocked(self, failing_store: InMemoryEventStore) -> None:
        svc = ObservabilityService(event_store=failing_store)
        svc.write_event(event_type="skill_start")
        result = svc.write_event(event_type="skill_finish")
        assert result.status == "blocked"
        assert "blocked" in result.message.lower()

    def test_blocked_result_has_escalate_hint(self, failing_store: InMemoryEventStore) -> None:
        svc = ObservabilityService(event_store=failing_store)
        svc.write_event(event_type="skill_start")
        result = svc.write_event(event_type="skill_finish")
        assert result.audit_hint == "escalate"


class TestQueryEvents:
    def test_query_all(self, svc: ObservabilityService) -> None:
        svc.write_event(event_type="skill_start", run_id="run_001")
        svc.write_event(event_type="skill_finish", run_id="run_001")
        result = svc.query_events(run_id="run_001")
        assert result.is_success
        assert result.data["count"] == 2

    def test_query_by_event_type(self, svc: ObservabilityService) -> None:
        svc.write_event(event_type="skill_start")
        svc.write_event(event_type="skill_finish")
        result = svc.query_events(event_type="skill_start")
        assert result.data["count"] == 1

    def test_query_by_stage(self, svc: ObservabilityService) -> None:
        svc.write_event(event_type="skill_start", stage_name="stage_a")
        svc.write_event(event_type="skill_start", stage_name="stage_b")
        result = svc.query_events(stage_name="stage_a")
        assert result.data["count"] == 1

    def test_query_empty_returns_zero(self, svc: ObservabilityService) -> None:
        result = svc.query_events(run_id="nonexistent_run")
        assert result.is_success
        assert result.data["count"] == 0


class TestReplayRun:
    def test_replay_returns_sorted(self, svc: ObservabilityService) -> None:
        for etype in ["skill_start", "stage_transition", "skill_finish"]:
            svc.write_event(event_type=etype, run_id="run_replay")
        result = svc.replay_run("run_replay")
        assert result.is_success
        assert result.data["count"] == 3

    def test_replay_empty_run(self, svc: ObservabilityService) -> None:
        result = svc.replay_run("empty_run")
        assert result.is_success
        assert result.data["count"] == 0


class TestBuildEventLineage:
    def test_lineage_chain(self, svc: ObservabilityService) -> None:
        trace_result = svc.create_trace("skill_a", "stage_a")
        trace_id = trace_result.data["trace_id"]
        child_result = svc.write_event(
            event_type="skill_start",
            parent_event_id=trace_id,
        )
        child_id = child_result.data["event_id"]
        lineage_result = svc.build_event_lineage(child_id)
        assert lineage_result.is_success
        lineage = lineage_result.data["lineage"]
        assert trace_id in lineage["chain"]
        assert child_id in lineage["chain"]

    def test_lineage_single_event(self, svc: ObservabilityService) -> None:
        evt_result = svc.write_event(event_type="skill_finish")
        evt_id = evt_result.data["event_id"]
        lineage_result = svc.build_event_lineage(evt_id)
        assert lineage_result.is_success
        assert len(lineage_result.data["lineage"]["chain"]) == 1

    def test_lineage_unknown_event(self, svc: ObservabilityService) -> None:
        result = svc.build_event_lineage("nonexistent_id")
        assert result.is_success
        assert result.data["lineage"]["chain"] == []
