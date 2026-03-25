"""Unit tests for WorkflowService and all Phase 1B helper components.

Uses the ``minimal_bundle`` fixture from
``tests/unit/platform_core/runtime/conftest.py`` (stage_a -> stage_b).
"""

from __future__ import annotations

import sys
import os

import pytest

# Allow the conftest from platform_core/runtime to be found
sys.path.insert(0, os.path.dirname(__file__))

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.config_models.enums import AccessModeEnum, StageClassEnum
from sdk.platform_core.runtime.config_models.routes import (
    FailureRouteEntry,
    FailureRoutesConfig,
    WorkflowRouteDefinition,
    WorkflowRoutesConfig,
)
from sdk.platform_core.runtime.config_models.stages import (
    StagePreconditionEntry,
    StagePreconditionsConfig,
    StageDefinition,
    StageRegistryConfig,
    StageToolMatrixConfig,
    StageToolMatrixEntry,
)
from sdk.platform_core.schemas.utilities import IDFactory
from sdk.workflowsdk.bootstrap import bootstrap_project_workflow
from sdk.workflowsdk.candidate import CandidateRegistry
from sdk.workflowsdk.models import (
    CandidateStatus,
    CandidateType,
    RecoveryPath,
    ReviewType,
    SelectionStatus,
    SessionStatus,
    UIMode,
    WorkflowMode,
)
from sdk.workflowsdk.recovery import CheckpointManager, RecoveryManager
from sdk.workflowsdk.routing_engine import RoutingEngine
from sdk.workflowsdk.selection import SelectionRegistry
from sdk.workflowsdk.service import WorkflowService
from sdk.workflowsdk.session import SessionManager
from sdk.workflowsdk.stage_registry import StageRegistryLoader, TransitionGuard
from sdk.workflowsdk.state_store import WorkflowStateStore


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def bundle(minimal_bundle: RuntimeConfigBundle) -> RuntimeConfigBundle:
    """Alias for the shared minimal_bundle fixture."""
    return minimal_bundle


@pytest.fixture()
def svc(bundle: RuntimeConfigBundle) -> WorkflowService:
    return WorkflowService(bundle)


@pytest.fixture()
def initialized_svc(svc: WorkflowService) -> WorkflowService:
    """WorkflowService with run_01 already bootstrapped at stage_a."""
    result = svc.initialize_run(
        run_id="run_01",
        project_id="proj_01",
        first_stage="stage_a",
        actor_id="analyst_01",
    )
    assert result.is_success
    return svc


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------


class TestBootstrap:
    def test_basic_bootstrap(self) -> None:
        store = WorkflowStateStore()
        ev = bootstrap_project_workflow(
            store=store,
            run_id="r1",
            project_id="p1",
            first_stage="stage_a",
        )
        assert ev.run_id == "r1"
        assert store.has_run("r1")

    def test_duplicate_run_raises(self) -> None:
        store = WorkflowStateStore()
        bootstrap_project_workflow(store=store, run_id="r1", project_id="p1", first_stage="s")
        with pytest.raises(ValueError, match="already initialised"):
            bootstrap_project_workflow(store=store, run_id="r1", project_id="p1", first_stage="s")

    def test_empty_run_id_raises(self) -> None:
        store = WorkflowStateStore()
        with pytest.raises(ValueError, match="run_id"):
            bootstrap_project_workflow(store=store, run_id="  ", project_id="p1", first_stage="s")

    def test_invalid_workflow_mode_raises(self) -> None:
        store = WorkflowStateStore()
        with pytest.raises(ValueError, match="workflow_mode"):
            bootstrap_project_workflow(
                store=store, run_id="r1", project_id="p1",
                first_stage="s", workflow_mode="bogus_mode"
            )


# ---------------------------------------------------------------------------
# WorkflowService — initialize_run
# ---------------------------------------------------------------------------


class TestInitializeRun:
    def test_success(self, svc: WorkflowService) -> None:
        r = svc.initialize_run(
            run_id="r1", project_id="p1", first_stage="stage_a"
        )
        assert r.is_success
        assert r.data["run_id"] == "r1"
        assert r.data["first_stage"] == "stage_a"

    def test_duplicate_run_is_failure(self, initialized_svc: WorkflowService) -> None:
        r = initialized_svc.initialize_run(
            run_id="run_01", project_id="proj_01", first_stage="stage_a"
        )
        assert not r.is_success

    def test_invalid_mode_is_failure(self, svc: WorkflowService) -> None:
        r = svc.initialize_run(
            run_id="r2", project_id="p1", first_stage="stage_a",
            workflow_mode="not_a_mode"
        )
        assert not r.is_success


# ---------------------------------------------------------------------------
# WorkflowService — get_state
# ---------------------------------------------------------------------------


class TestGetState:
    def test_initial_state(self, initialized_svc: WorkflowService) -> None:
        r = initialized_svc.get_state("run_01", "proj_01")
        assert r.is_success
        state = r.data["state"]
        assert state["current_stage"] == "stage_a"
        assert state["workflow_mode"] == "development"

    def test_missing_run_is_failure(self, svc: WorkflowService) -> None:
        r = svc.get_state("no_such_run", "proj_01")
        assert not r.is_success


# ---------------------------------------------------------------------------
# WorkflowService — stage transitions
# ---------------------------------------------------------------------------


class TestStartStage:
    def test_start_valid_stage(self, initialized_svc: WorkflowService) -> None:
        # stage_a has no prerequisites in minimal_bundle
        r = initialized_svc.start_stage(
            run_id="run_01", project_id="proj_01", stage_name="stage_a"
        )
        assert r.is_success
        assert r.data["stage_name"] == "stage_a"

    def test_start_stage_updates_state(self, initialized_svc: WorkflowService) -> None:
        initialized_svc.start_stage(
            run_id="run_01", project_id="proj_01", stage_name="stage_a"
        )
        state_r = initialized_svc.get_state("run_01", "proj_01")
        from sdk.platform_core.schemas.enums import StageStatusEnum
        assert state_r.data["state"]["stages"]["stage_a"]["status"] == StageStatusEnum.RUNNING.value


class TestCompleteStage:
    def test_complete_stage(self, initialized_svc: WorkflowService) -> None:
        initialized_svc.start_stage(
            run_id="run_01", project_id="proj_01", stage_name="stage_a"
        )
        r = initialized_svc.complete_stage(
            run_id="run_01", project_id="proj_01", stage_name="stage_a",
            artifact_ids=["art_1"],
        )
        assert r.is_success
        assert r.data["next_stage"] == "stage_b"

    def test_complete_terminal_stage_returns_none(
        self, initialized_svc: WorkflowService
    ) -> None:
        initialized_svc.start_stage(
            run_id="run_01", project_id="proj_01", stage_name="stage_a"
        )
        initialized_svc.complete_stage(
            run_id="run_01", project_id="proj_01", stage_name="stage_a"
        )
        initialized_svc.start_stage(
            run_id="run_01", project_id="proj_01", stage_name="stage_b"
        )
        r = initialized_svc.complete_stage(
            run_id="run_01", project_id="proj_01", stage_name="stage_b"
        )
        assert r.is_success
        # stage_b has no on_success route → terminal
        assert r.data["next_stage"] is None


class TestFailStage:
    def test_fail_stage_returns_recovery(self, initialized_svc: WorkflowService) -> None:
        initialized_svc.start_stage(
            run_id="run_01", project_id="proj_01", stage_name="stage_a"
        )
        r = initialized_svc.fail_stage(
            run_id="run_01", project_id="proj_01", stage_name="stage_a",
            error_detail="Out of memory",
        )
        assert not r.is_success  # status=failure for a failed stage
        assert "recovery_path" in r.data
        assert r.data["recovery_path"] in {p.value for p in RecoveryPath}


# ---------------------------------------------------------------------------
# StageRegistryLoader
# ---------------------------------------------------------------------------


class TestStageRegistryLoader:
    def test_get_known_stage(self, bundle: RuntimeConfigBundle) -> None:
        loader = StageRegistryLoader(bundle)
        defn = loader.get("stage_a")
        assert defn.stage_name == "stage_a"

    def test_get_unknown_raises(self, bundle: RuntimeConfigBundle) -> None:
        loader = StageRegistryLoader(bundle)
        with pytest.raises(KeyError):
            loader.get("no_such_stage")

    def test_exists(self, bundle: RuntimeConfigBundle) -> None:
        loader = StageRegistryLoader(bundle)
        assert loader.exists("stage_a")
        assert not loader.exists("nope")

    def test_all_stage_names(self, bundle: RuntimeConfigBundle) -> None:
        loader = StageRegistryLoader(bundle)
        names = loader.all_stage_names()
        assert "stage_a" in names
        assert "stage_b" in names

    def test_no_preconditions_returns_empty(self, bundle: RuntimeConfigBundle) -> None:
        loader = StageRegistryLoader(bundle)
        # minimal_bundle has no stage_preconditions
        assert loader.required_prior_stages("stage_b") == []


# ---------------------------------------------------------------------------
# TransitionGuard
# ---------------------------------------------------------------------------


class TestTransitionGuard:
    def test_valid_transition_returns_none(self, bundle: RuntimeConfigBundle) -> None:
        loader = StageRegistryLoader(bundle)
        guard = TransitionGuard(loader)
        from sdk.workflowsdk.models import WorkflowState
        state = WorkflowState(run_id="r", project_id="p")
        result = guard.validate(target_stage="stage_a", state=state)
        assert result is None

    def test_unknown_stage_is_invalid(self, bundle: RuntimeConfigBundle) -> None:
        loader = StageRegistryLoader(bundle)
        guard = TransitionGuard(loader)
        from sdk.workflowsdk.models import WorkflowState, BlockReason
        state = WorkflowState(run_id="r", project_id="p")
        reason = guard.validate(target_stage="nonexistent", state=state)
        assert reason == BlockReason.INVALID_TRANSITION

    def test_prerequisite_not_met(self) -> None:
        """TransitionGuard blocks when a required prior stage is not completed."""
        from sdk.platform_core.runtime.config_models.governance import (
            DefaultGovernanceRules, GovernanceOverlaysConfig, GovernanceOverlaysSection
        )
        from sdk.platform_core.runtime.config_models.retries import (
            RetryDefaults, RetryPoliciesConfig, RetryPoliciesSection
        )
        from sdk.platform_core.runtime.config_models.roles import (
            RoleCapabilitiesConfig, RoleCapabilityDefinition
        )
        from sdk.platform_core.runtime.config_models.runtime_master import (
            RuntimeMasterConfig, RuntimeMasterSection
        )
        from sdk.platform_core.runtime.config_models.tool_groups import (
            ToolGroupDefinition, ToolGroupsConfig
        )
        from sdk.platform_core.runtime.config_models.ui import (
            InteractionModeDefinition, InteractionModesConfig,
            TokenModeDefinition, TokenModesConfig,
            UIModeDefinition, UIModesConfig,
        )
        from sdk.platform_core.runtime.config_models.enums import (
            InteractionModeEnum, TokenModeEnum, UIModeEnum
        )
        from sdk.workflowsdk.models import BlockReason, WorkflowState

        stages = {
            "gate": StageDefinition(stage_name="gate", stage_class=StageClassEnum.BUILD),
            "after_gate": StageDefinition(stage_name="after_gate", stage_class=StageClassEnum.BUILD),
        }
        preconditions = StagePreconditionsConfig(
            preconditions={
                "after_gate": StagePreconditionEntry(
                    stage_name="after_gate",
                    required_prior_stages=["gate"],
                ),
            }
        )
        tool_groups = ToolGroupsConfig(
            groups={"grp": ToolGroupDefinition(group_name="grp", tools=["t1"])}
        )
        bundle = RuntimeConfigBundle(
            runtime_master=RuntimeMasterConfig(runtime=RuntimeMasterSection()),
            tool_groups=tool_groups,
            role_capabilities=RoleCapabilitiesConfig(
                roles={"developer": RoleCapabilityDefinition(
                    role="developer", allowed_tool_groups=["grp"],
                    blocked_tool_groups=[], allowed_stages=["gate", "after_gate"],
                )}
            ),
            ui_modes=UIModesConfig(modes={"ws": UIModeDefinition(mode=UIModeEnum.BOOTSTRAP_WORKSPACE)}),
            interaction_modes=InteractionModesConfig(modes={"e": InteractionModeDefinition(mode=InteractionModeEnum.EDIT_AND_FINALIZE)}),
            token_modes=TokenModesConfig(modes={"f": TokenModeDefinition(mode=TokenModeEnum.FULL)}),
            stage_registry=StageRegistryConfig(stages=stages),
            stage_tool_matrix=StageToolMatrixConfig(matrix={
                "gate": StageToolMatrixEntry(stage_name="gate", allowed_groups=["grp"]),
                "after_gate": StageToolMatrixEntry(stage_name="after_gate", allowed_groups=["grp"]),
            }),
            governance_overlays=GovernanceOverlaysConfig(
                governance=GovernanceOverlaysSection(default_rules=DefaultGovernanceRules())
            ),
            retry_policies=RetryPoliciesConfig(
                retry_policies=RetryPoliciesSection(defaults=RetryDefaults())
            ),
            workflow_routes=WorkflowRoutesConfig(routes={
                "gate": WorkflowRouteDefinition(stage_name="gate", on_success="after_gate"),
                "after_gate": WorkflowRouteDefinition(stage_name="after_gate"),
            }),
            stage_preconditions=preconditions,
        )
        loader = StageRegistryLoader(bundle)
        guard = TransitionGuard(loader)

        # "gate" is not completed — after_gate should be blocked
        state = WorkflowState(run_id="r", project_id="p")
        reason = guard.validate(target_stage="after_gate", state=state)
        assert reason == BlockReason.PREREQUISITE_NOT_MET


# ---------------------------------------------------------------------------
# RoutingEngine
# ---------------------------------------------------------------------------


class TestRoutingEngine:
    def test_next_stage_on_success(self, bundle: RuntimeConfigBundle) -> None:
        engine = RoutingEngine(bundle)
        assert engine.next_stage("stage_a", "on_success") == "stage_b"

    def test_terminal_stage_returns_none(self, bundle: RuntimeConfigBundle) -> None:
        engine = RoutingEngine(bundle)
        assert engine.next_stage("stage_b", "on_success") is None

    def test_unknown_stage_returns_none(self, bundle: RuntimeConfigBundle) -> None:
        engine = RoutingEngine(bundle)
        assert engine.next_stage("no_stage", "on_success") is None

    def test_invalid_outcome_raises(self, bundle: RuntimeConfigBundle) -> None:
        engine = RoutingEngine(bundle)
        with pytest.raises(ValueError, match="Unknown outcome"):
            engine.next_stage("stage_a", "on_magic")

    def test_failure_routes_empty_by_default(self, bundle: RuntimeConfigBundle) -> None:
        engine = RoutingEngine(bundle)
        assert engine.failure_routes_for("stage_a") == []


# ---------------------------------------------------------------------------
# CandidateRegistry
# ---------------------------------------------------------------------------


class TestCandidateRegistry:
    def test_register(self) -> None:
        reg = CandidateRegistry()
        cand = reg.register(
            stage_name="stage_a",
            candidate_type=CandidateType.MODEL_VERSION,
            run_id="r1",
            project_id="p1",
            version_label="v1",
        )
        assert cand.candidate_id.startswith("cnd_")
        assert cand.status == CandidateStatus.PENDING_REVIEW

    def test_mark_selected(self) -> None:
        reg = CandidateRegistry()
        c1 = reg.register(
            stage_name="s", candidate_type=CandidateType.MODEL_VERSION,
            run_id="r", project_id="p",
        )
        c2 = reg.register(
            stage_name="s", candidate_type=CandidateType.MODEL_VERSION,
            run_id="r", project_id="p",
        )
        reg.mark_selected(c1.candidate_id)
        assert reg.get(c1.candidate_id).status == CandidateStatus.SELECTED
        assert reg.get(c2.candidate_id).status == CandidateStatus.SUPERSEDED

    def test_mark_rejected(self) -> None:
        reg = CandidateRegistry()
        c = reg.register(
            stage_name="s", candidate_type=CandidateType.BINNING_VERSION,
            run_id="r", project_id="p",
        )
        reg.mark_rejected(c.candidate_id)
        assert reg.get(c.candidate_id).status == CandidateStatus.REJECTED

    def test_get_selected(self) -> None:
        reg = CandidateRegistry()
        c = reg.register(
            stage_name="s", candidate_type=CandidateType.MODEL_VERSION,
            run_id="r", project_id="p",
        )
        assert reg.get_selected("s") is None
        reg.mark_selected(c.candidate_id)
        assert reg.get_selected("s").candidate_id == c.candidate_id

    def test_missing_candidate_raises(self) -> None:
        reg = CandidateRegistry()
        with pytest.raises(KeyError):
            reg.get("cnd_missing")

    def test_empty_fields_raise(self) -> None:
        reg = CandidateRegistry()
        with pytest.raises(ValueError):
            reg.register(
                stage_name="",
                candidate_type=CandidateType.MODEL_VERSION,
                run_id="r", project_id="p",
            )


# ---------------------------------------------------------------------------
# SelectionRegistry
# ---------------------------------------------------------------------------


class TestSelectionRegistry:
    def test_record_selection(self) -> None:
        reg = SelectionRegistry()
        sel = reg.record_selection(
            stage_name="s", run_id="r", project_id="p",
            selected_candidate_id="cnd_1", selected_by="ana_01",
        )
        assert sel.selection_id.startswith("sel_")
        assert sel.status == SelectionStatus.ACTIVE

    def test_supersedes_previous(self) -> None:
        reg = SelectionRegistry()
        s1 = reg.record_selection(
            stage_name="s", run_id="r", project_id="p",
            selected_candidate_id="cnd_1", selected_by="ana",
        )
        reg.record_selection(
            stage_name="s", run_id="r", project_id="p",
            selected_candidate_id="cnd_2", selected_by="ana",
        )
        assert reg.get(s1.selection_id).status == SelectionStatus.SUPERSEDED

    def test_active_for_stage(self) -> None:
        reg = SelectionRegistry()
        reg.record_selection(
            stage_name="s", run_id="r", project_id="p",
            selected_candidate_id="cnd_1", selected_by="ana",
        )
        active = reg.active_for_stage("s")
        assert active is not None
        assert active.selected_candidate_id == "cnd_1"

    def test_stages_with_active_selection(self) -> None:
        reg = SelectionRegistry()
        reg.record_selection(
            stage_name="stage_x", run_id="r", project_id="p",
            selected_candidate_id="cnd_1", selected_by="ana",
        )
        stages = reg.stages_with_active_selection()
        assert "stage_x" in stages

    def test_revoke(self) -> None:
        reg = SelectionRegistry()
        sel = reg.record_selection(
            stage_name="s", run_id="r", project_id="p",
            selected_candidate_id="cnd_1", selected_by="ana",
        )
        reg.revoke(sel.selection_id, reason="Policy breach")
        assert reg.get(sel.selection_id).status == SelectionStatus.REVOKED

    def test_revoke_non_active_raises(self) -> None:
        reg = SelectionRegistry()
        sel = reg.record_selection(
            stage_name="s", run_id="r", project_id="p",
            selected_candidate_id="cnd_1", selected_by="ana",
        )
        reg.revoke(sel.selection_id)
        with pytest.raises(ValueError, match="cannot be revoked"):
            reg.revoke(sel.selection_id)


# ---------------------------------------------------------------------------
# SessionManager
# ---------------------------------------------------------------------------


class TestSessionManager:
    def test_create_session(self) -> None:
        mgr = SessionManager()
        s = mgr.create(run_id="r", project_id="p", created_by="ana")
        assert s.session_id.startswith("ses_")
        assert s.status == SessionStatus.ACTIVE

    def test_active_for_run(self) -> None:
        mgr = SessionManager()
        mgr.create(run_id="r", project_id="p")
        active = mgr.active_for_run("r")
        assert active is not None
        assert active.status == SessionStatus.ACTIVE

    def test_new_session_suspends_existing(self) -> None:
        mgr = SessionManager()
        s1 = mgr.create(run_id="r", project_id="p")
        mgr.create(run_id="r", project_id="p")
        assert mgr.get(s1.session_id).status == SessionStatus.SUSPENDED

    def test_suspend_and_resume(self) -> None:
        mgr = SessionManager()
        s = mgr.create(run_id="r", project_id="p")
        mgr.suspend(s.session_id)
        assert mgr.get(s.session_id).status == SessionStatus.SUSPENDED
        mgr.resume(s.session_id)
        assert mgr.get(s.session_id).status == SessionStatus.ACTIVE

    def test_close_session(self) -> None:
        mgr = SessionManager()
        s = mgr.create(run_id="r", project_id="p")
        mgr.close(s.session_id)
        assert mgr.get(s.session_id).status == SessionStatus.CLOSED

    def test_close_twice_raises(self) -> None:
        mgr = SessionManager()
        s = mgr.create(run_id="r", project_id="p")
        mgr.close(s.session_id)
        with pytest.raises(ValueError, match="already closed"):
            mgr.close(s.session_id)

    def test_resume_non_suspended_raises(self) -> None:
        mgr = SessionManager()
        s = mgr.create(run_id="r", project_id="p")
        with pytest.raises(ValueError, match="cannot be resumed"):
            mgr.resume(s.session_id)


# ---------------------------------------------------------------------------
# CheckpointManager
# ---------------------------------------------------------------------------


class TestCheckpointManager:
    def _make_state(self, run_id: str = "r1", event_count: int = 5):
        from sdk.workflowsdk.models import WorkflowState
        return WorkflowState(
            run_id=run_id,
            project_id="p1",
            current_stage="stage_a",
            event_count=event_count,
        )

    def test_save_checkpoint(self) -> None:
        mgr = CheckpointManager()
        state = self._make_state()
        rec = mgr.save(state, session_id="ses_1")
        assert rec.checkpoint_id.startswith("chk_")
        assert rec.is_valid
        assert rec.state_json != ""

    def test_latest_valid(self) -> None:
        mgr = CheckpointManager()
        state = self._make_state()
        rec = mgr.save(state)
        assert mgr.latest_valid("r1").checkpoint_id == rec.checkpoint_id

    def test_max_checkpoints_invalidates_oldest(self) -> None:
        mgr = CheckpointManager(max_checkpoints_per_run=2)
        s = self._make_state()
        r1 = mgr.save(s)
        r2 = mgr.save(s)
        r3 = mgr.save(s)
        # r1 should now be invalid
        assert not mgr.get(r1.checkpoint_id).is_valid
        assert mgr.get(r2.checkpoint_id).is_valid
        assert mgr.get(r3.checkpoint_id).is_valid

    def test_restore_state(self) -> None:
        mgr = CheckpointManager()
        state = self._make_state(event_count=42)
        rec = mgr.save(state)
        restored = rec.restore_state()
        assert restored.event_count == 42
        assert restored.run_id == "r1"

    def test_missing_checkpoint_raises(self) -> None:
        mgr = CheckpointManager()
        with pytest.raises(KeyError):
            mgr.get("chk_nope")


# ---------------------------------------------------------------------------
# RecoveryManager
# ---------------------------------------------------------------------------


class TestRecoveryManager:
    def _make_state_with_stage(self, stage_name: str, attempt: int):
        from sdk.platform_core.schemas.enums import StageStatusEnum
        from sdk.workflowsdk.models import StageRecord, WorkflowState
        return WorkflowState(
            run_id="r", project_id="p",
            stages={
                stage_name: StageRecord(
                    stage_name=stage_name,
                    status=StageStatusEnum.FAILED,
                    attempt_count=attempt,
                )
            },
        )

    def test_first_attempt_recommends_retry(self) -> None:
        rm = RecoveryManager()
        state = self._make_state_with_stage("s", attempt=1)
        assert rm.recommend(state, failed_stage="s") == RecoveryPath.RETRY

    def test_exceeds_max_recommends_rollback(self) -> None:
        rm = RecoveryManager()
        state = self._make_state_with_stage("s", attempt=4)
        assert rm.recommend(state, failed_stage="s") == RecoveryPath.ROLLBACK

    def test_no_stage_record_recommends_rerun(self) -> None:
        from sdk.workflowsdk.models import WorkflowState
        rm = RecoveryManager()
        state = WorkflowState(run_id="r", project_id="p")
        assert rm.recommend(state, failed_stage="s") == RecoveryPath.RERUN

    def test_previously_completed_recommends_resume(self) -> None:
        from sdk.platform_core.schemas.enums import StageStatusEnum
        from sdk.workflowsdk.models import StageRecord, WorkflowState
        rm = RecoveryManager()
        state = WorkflowState(
            run_id="r", project_id="p",
            stages={
                "s": StageRecord(
                    stage_name="s",
                    status=StageStatusEnum.COMPLETED,
                    attempt_count=1,
                )
            },
        )
        assert rm.recommend(state, failed_stage="s") == RecoveryPath.RESUME

    def test_describe_returns_string(self) -> None:
        rm = RecoveryManager()
        desc = rm.describe(RecoveryPath.RETRY)
        assert isinstance(desc, str)
        assert len(desc) > 0


# ---------------------------------------------------------------------------
# WorkflowService — candidate and selection
# ---------------------------------------------------------------------------


class TestWorkflowServiceCandidates:
    def test_register_candidate(self, initialized_svc: WorkflowService) -> None:
        r = initialized_svc.register_candidate(
            stage_name="stage_a",
            candidate_type=CandidateType.MODEL_VERSION,
            run_id="run_01",
            project_id="proj_01",
            version_label="v1",
            summary="Model with Gini=0.72",
        )
        assert r.is_success
        assert "candidate_id" in r.data

    def test_record_selection(self, initialized_svc: WorkflowService) -> None:
        rc = initialized_svc.register_candidate(
            stage_name="stage_a",
            candidate_type=CandidateType.MODEL_VERSION,
            run_id="run_01",
            project_id="proj_01",
        )
        cid = rc.data["candidate_id"]
        rs = initialized_svc.record_selection(
            stage_name="stage_a",
            run_id="run_01",
            project_id="proj_01",
            candidate_id=cid,
            selected_by="analyst_01",
            rationale="Best Gini",
        )
        assert rs.is_success
        assert "selection_id" in rs.data


# ---------------------------------------------------------------------------
# WorkflowService — session and recovery
# ---------------------------------------------------------------------------


class TestWorkflowServiceSession:
    def test_create_and_close_session(self, initialized_svc: WorkflowService) -> None:
        r = initialized_svc.create_session(
            run_id="run_01", project_id="proj_01", created_by="ana"
        )
        assert r.is_success
        sid = r.data["session_id"]
        rc = initialized_svc.close_session(sid)
        assert rc.is_success

    def test_save_checkpoint(self, initialized_svc: WorkflowService) -> None:
        r = initialized_svc.save_checkpoint("run_01", "proj_01")
        assert r.is_success
        assert "checkpoint_id" in r.data

    def test_recommend_recovery(self, initialized_svc: WorkflowService) -> None:
        initialized_svc.start_stage(
            run_id="run_01", project_id="proj_01", stage_name="stage_a"
        )
        initialized_svc.fail_stage(
            run_id="run_01", project_id="proj_01",
            stage_name="stage_a", error_detail="Crash",
        )
        r = initialized_svc.recommend_recovery(
            "run_01", "proj_01", "stage_a"
        )
        assert r.is_success
        assert r.data["recovery_path"] in {p.value for p in RecoveryPath}


# ---------------------------------------------------------------------------
# WorkflowService — stage registry queries
# ---------------------------------------------------------------------------


class TestWorkflowServiceRegistry:
    def test_list_stages(self, svc: WorkflowService) -> None:
        r = svc.list_stages()
        assert r.is_success
        assert "stage_a" in r.data["stages"]
        assert r.data["count"] == 2

    def test_get_stage_definition(self, svc: WorkflowService) -> None:
        r = svc.get_stage_definition("stage_a")
        assert r.is_success
        assert r.data["stage"]["stage_name"] == "stage_a"

    def test_get_unknown_stage_is_failure(self, svc: WorkflowService) -> None:
        r = svc.get_stage_definition("not_a_stage")
        assert not r.is_success
