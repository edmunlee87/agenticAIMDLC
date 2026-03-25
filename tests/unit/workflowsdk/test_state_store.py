"""Unit tests for WorkflowStateStore and _replay."""

from __future__ import annotations

import pytest

from sdk.platform_core.schemas.enums import StageStatusEnum
from sdk.platform_core.schemas.utilities import IDFactory
from sdk.workflowsdk.models import (
    BlockReason,
    InteractionMode,
    UIMode,
    WorkflowEvent,
    WorkflowEventType,
    WorkflowMode,
)
from sdk.workflowsdk.state_store import WorkflowStateStore, _replay


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_event(
    run_id: str,
    event_type: WorkflowEventType,
    stage_name: str,
    project_id: str = "proj_x",
    payload: dict | None = None,
) -> WorkflowEvent:
    return WorkflowEvent(
        event_id=IDFactory.event_id(),
        event_type=event_type,
        run_id=run_id,
        project_id=project_id,
        stage_name=stage_name,
        payload=payload or {},
    )


@pytest.fixture()
def store() -> WorkflowStateStore:
    return WorkflowStateStore()


@pytest.fixture()
def init_event(store: WorkflowStateStore) -> WorkflowEvent:
    ev = _make_event(
        "run_01",
        WorkflowEventType.WORKFLOW_INITIALIZED,
        "stage_a",
        payload={"workflow_mode": "development", "active_domain": "credit_risk"},
    )
    store.append_event(ev)
    return ev


# ---------------------------------------------------------------------------
# WorkflowStateStore — write
# ---------------------------------------------------------------------------


class TestAppendEvent:
    def test_append_succeeds(self, store: WorkflowStateStore, init_event: WorkflowEvent) -> None:
        assert store.event_count("run_01") == 1

    def test_run_not_present_before_append(self, store: WorkflowStateStore) -> None:
        assert not store.has_run("missing_run")

    def test_has_run_after_append(self, store: WorkflowStateStore, init_event: WorkflowEvent) -> None:
        assert store.has_run("run_01")

    def test_duplicate_event_id_raises(
        self, store: WorkflowStateStore, init_event: WorkflowEvent
    ) -> None:
        # Same event_id — duplicate
        dup = WorkflowEvent(
            event_id=init_event.event_id,
            event_type=WorkflowEventType.STAGE_STARTED,
            run_id="run_01",
            project_id="proj_x",
            stage_name="stage_a",
        )
        with pytest.raises(ValueError, match="Duplicate event_id"):
            store.append_event(dup)

    def test_multiple_runs_isolated(self, store: WorkflowStateStore) -> None:
        for run_id in ["runA", "runB"]:
            store.append_event(
                _make_event(run_id, WorkflowEventType.WORKFLOW_INITIALIZED, "s1")
            )
        assert store.event_count("runA") == 1
        assert store.event_count("runB") == 1


# ---------------------------------------------------------------------------
# WorkflowStateStore — read
# ---------------------------------------------------------------------------


class TestGetEvents:
    def test_get_events_all(self, store: WorkflowStateStore, init_event: WorkflowEvent) -> None:
        store.append_event(
            _make_event("run_01", WorkflowEventType.STAGE_STARTED, "stage_a")
        )
        events = store.get_events("run_01")
        assert len(events) == 2

    def test_get_events_filter_type(self, store: WorkflowStateStore, init_event: WorkflowEvent) -> None:
        store.append_event(
            _make_event("run_01", WorkflowEventType.STAGE_STARTED, "stage_a")
        )
        events = store.get_events("run_01", event_type=WorkflowEventType.STAGE_STARTED)
        assert len(events) == 1
        assert events[0].event_type == WorkflowEventType.STAGE_STARTED

    def test_get_events_filter_stage(self, store: WorkflowStateStore, init_event: WorkflowEvent) -> None:
        store.append_event(
            _make_event("run_01", WorkflowEventType.STAGE_STARTED, "stage_b")
        )
        events = store.get_events("run_01", stage_name="stage_b")
        assert len(events) == 1

    def test_get_events_limit(self, store: WorkflowStateStore, init_event: WorkflowEvent) -> None:
        for _ in range(4):
            store.append_event(
                _make_event("run_01", WorkflowEventType.STAGE_STARTED, "stage_a")
            )
        limited = store.get_events("run_01", limit=2)
        assert len(limited) == 2

    def test_get_events_missing_run_raises(self, store: WorkflowStateStore) -> None:
        with pytest.raises(KeyError):
            store.get_events("nope")

    def test_list_runs(self, store: WorkflowStateStore) -> None:
        store.append_event(_make_event("r1", WorkflowEventType.WORKFLOW_INITIALIZED, "s"))
        store.append_event(_make_event("r2", WorkflowEventType.WORKFLOW_INITIALIZED, "s"))
        runs = store.list_runs()
        assert "r1" in runs
        assert "r2" in runs


# ---------------------------------------------------------------------------
# _replay
# ---------------------------------------------------------------------------


class TestReplay:
    def _build_events(self, run_id: str = "r1", project_id: str = "p1") -> list[WorkflowEvent]:
        return [
            WorkflowEvent(
                event_id=IDFactory.event_id(),
                event_type=WorkflowEventType.WORKFLOW_INITIALIZED,
                run_id=run_id,
                project_id=project_id,
                stage_name="stage_a",
                payload={"workflow_mode": "development", "active_domain": "credit_risk"},
            ),
            WorkflowEvent(
                event_id=IDFactory.event_id(),
                event_type=WorkflowEventType.STAGE_STARTED,
                run_id=run_id,
                project_id=project_id,
                stage_name="stage_a",
            ),
        ]

    def test_initialized_sets_mode(self) -> None:
        events = [
            WorkflowEvent(
                event_id=IDFactory.event_id(),
                event_type=WorkflowEventType.WORKFLOW_INITIALIZED,
                run_id="r", project_id="p", stage_name="s1",
                payload={"workflow_mode": "validation", "active_domain": "time_series"},
            )
        ]
        state = _replay(events, "r", "p")
        assert state.workflow_mode == WorkflowMode.VALIDATION
        assert state.active_domain == "time_series"
        assert state.current_stage == "s1"
        assert state.event_count == 1

    def test_stage_started_sets_running(self) -> None:
        events = self._build_events()
        state = _replay(events, "r1", "p1")
        assert state.stages["stage_a"].status == StageStatusEnum.RUNNING
        assert state.stages["stage_a"].attempt_count == 1
        assert state.ui_mode == UIMode.STAGE_PROGRESS

    def test_stage_completed(self) -> None:
        events = self._build_events()
        events.append(WorkflowEvent(
            event_id=IDFactory.event_id(),
            event_type=WorkflowEventType.STAGE_COMPLETED,
            run_id="r1", project_id="p1", stage_name="stage_a",
            payload={"artifact_ids": ["art_1"]},
        ))
        state = _replay(events, "r1", "p1")
        assert state.stages["stage_a"].status == StageStatusEnum.COMPLETED
        assert "art_1" in state.stages["stage_a"].artifact_ids
        assert state.interaction_mode == InteractionMode.NONE

    def test_stage_failed(self) -> None:
        events = self._build_events()
        events.append(WorkflowEvent(
            event_id=IDFactory.event_id(),
            event_type=WorkflowEventType.STAGE_FAILED,
            run_id="r1", project_id="p1", stage_name="stage_a",
            payload={"error_detail": "OOM error"},
        ))
        state = _replay(events, "r1", "p1")
        assert state.stages["stage_a"].status == StageStatusEnum.FAILED
        assert state.stages["stage_a"].error_detail == "OOM error"
        assert state.ui_mode == UIMode.RECOVERY_PROMPT
        assert state.interaction_mode == InteractionMode.RECOVERY_REQUIRED

    def test_stage_blocked_review(self) -> None:
        events = self._build_events()
        events.append(WorkflowEvent(
            event_id=IDFactory.event_id(),
            event_type=WorkflowEventType.STAGE_BLOCKED,
            run_id="r1", project_id="p1", stage_name="stage_a",
            payload={"block_reason": "review_pending"},
        ))
        state = _replay(events, "r1", "p1")
        assert state.stages["stage_a"].status == StageStatusEnum.WAITING_REVIEW
        assert state.stages["stage_a"].block_reason == BlockReason.REVIEW_PENDING
        assert state.ui_mode == UIMode.REVIEW_3PANEL
        assert state.interaction_mode == InteractionMode.REVIEW_REQUIRED

    def test_stage_blocked_selection_missing(self) -> None:
        events = self._build_events()
        events.append(WorkflowEvent(
            event_id=IDFactory.event_id(),
            event_type=WorkflowEventType.STAGE_BLOCKED,
            run_id="r1", project_id="p1", stage_name="stage_a",
            payload={"block_reason": "selection_missing"},
        ))
        state = _replay(events, "r1", "p1")
        assert state.interaction_mode == InteractionMode.SELECTION_REQUIRED

    def test_retry_increments_attempt_count(self) -> None:
        events = self._build_events()
        events.append(WorkflowEvent(
            event_id=IDFactory.event_id(),
            event_type=WorkflowEventType.STAGE_FAILED,
            run_id="r1", project_id="p1", stage_name="stage_a",
            payload={"error_detail": "err"},
        ))
        events.append(WorkflowEvent(
            event_id=IDFactory.event_id(),
            event_type=WorkflowEventType.STAGE_STARTED,
            run_id="r1", project_id="p1", stage_name="stage_a",
        ))
        state = _replay(events, "r1", "p1")
        assert state.stages["stage_a"].attempt_count == 2

    def test_review_opened_sets_review_id(self) -> None:
        events = self._build_events()
        events.append(WorkflowEvent(
            event_id=IDFactory.event_id(),
            event_type=WorkflowEventType.REVIEW_OPENED,
            run_id="r1", project_id="p1", stage_name="stage_a",
            payload={"review_id": "rev_123"},
        ))
        state = _replay(events, "r1", "p1")
        assert state.stages["stage_a"].review_id == "rev_123"

    def test_candidate_selected_updates_stage(self) -> None:
        events = self._build_events()
        events.append(WorkflowEvent(
            event_id=IDFactory.event_id(),
            event_type=WorkflowEventType.CANDIDATE_SELECTED,
            run_id="r1", project_id="p1", stage_name="stage_a",
            payload={"candidate_id": "cnd_abc"},
        ))
        state = _replay(events, "r1", "p1")
        assert state.stages["stage_a"].selected_candidate_id == "cnd_abc"
        assert state.interaction_mode == InteractionMode.NONE

    def test_session_created_sets_session_id(self) -> None:
        events = self._build_events()
        events.append(WorkflowEvent(
            event_id=IDFactory.event_id(),
            event_type=WorkflowEventType.SESSION_CREATED,
            run_id="r1", project_id="p1", stage_name="stage_a",
            payload={"session_id": "ses_xyz"},
        ))
        state = _replay(events, "r1", "p1")
        assert state.session_id == "ses_xyz"

    def test_session_closed_clears_session_id(self) -> None:
        events = self._build_events()
        events.append(WorkflowEvent(
            event_id=IDFactory.event_id(),
            event_type=WorkflowEventType.SESSION_CREATED,
            run_id="r1", project_id="p1", stage_name="stage_a",
            payload={"session_id": "ses_xyz"},
        ))
        events.append(WorkflowEvent(
            event_id=IDFactory.event_id(),
            event_type=WorkflowEventType.SESSION_CLOSED,
            run_id="r1", project_id="p1", stage_name="stage_a",
            payload={},
        ))
        state = _replay(events, "r1", "p1")
        assert state.session_id == ""

    def test_last_event_id_is_tracked(self) -> None:
        events = self._build_events()
        state = _replay(events, "r1", "p1")
        assert state.last_event_id == events[-1].event_id
        assert state.event_count == len(events)

    def test_empty_event_list(self) -> None:
        state = _replay([], "r1", "p1")
        assert state.event_count == 0
        assert state.current_stage == ""
