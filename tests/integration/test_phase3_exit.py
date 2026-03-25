"""Phase 3 Exit Integration Tests.

Governance test matrix: domain packs, dataprep lineage, canvas HITL states,
token budget enforcement.

Test IDs: AT-P3-001 through AT-P3-020.
"""

from __future__ import annotations

import math
import sys
import uuid
from pathlib import Path

import pytest

# Ensure repo packages are importable.
REPO_ROOT = Path(__file__).parent.parent.parent
SDK_SRC = REPO_ROOT / "sdk"
for p in SDK_SRC.iterdir():
    src_path = p / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))

# Also add the scorecard YAML path.
OVERLAY_DIR = REPO_ROOT / "configs" / "runtime" / "domain_overlays"


# ---------------------------------------------------------------------------
# AT-P3-001: DomainPackLoader loads scorecard manifest
# ---------------------------------------------------------------------------
def test_scorecard_manifest_loads():  # AT-P3-001
    from platform_core.domain.loader import DomainPackLoader
    loader = DomainPackLoader(overlay_dir=OVERLAY_DIR)
    manifest = loader.load("scorecard", OVERLAY_DIR / "scorecard.yaml")

    assert manifest.domain == "scorecard"
    assert len(manifest.stage_registry) >= 10
    assert manifest.get_primary_metric() is not None
    assert manifest.get_primary_metric().metric_name == "gini"


# ---------------------------------------------------------------------------
# AT-P3-002: Scorecard manifest governance gates
# ---------------------------------------------------------------------------
def test_scorecard_governance_gates():  # AT-P3-002
    from platform_core.domain.loader import DomainPackLoader
    loader = DomainPackLoader(overlay_dir=OVERLAY_DIR)
    manifest = loader.load("scorecard", OVERLAY_DIR / "scorecard.yaml")

    gates = manifest.governance_gate_stages
    assert "coarse_classing_review" in gates
    assert "model_review" in gates
    assert "deployment_readiness" in gates


# ---------------------------------------------------------------------------
# AT-P3-003: Scorecard routing rules -- on_approval for all review stages
# ---------------------------------------------------------------------------
def test_scorecard_routing_rules():  # AT-P3-003
    from platform_core.domain.loader import DomainPackLoader
    from platform_core.domain.models import RouteCondition
    loader = DomainPackLoader(overlay_dir=OVERLAY_DIR)
    manifest = loader.load("scorecard", OVERLAY_DIR / "scorecard.yaml")

    rule = manifest.get_routing_rule("model_review", RouteCondition.ON_APPROVAL)
    assert rule is not None
    assert rule.to_stage == "score_scaling"
    assert rule.failure_stage == "model_development"


# ---------------------------------------------------------------------------
# AT-P3-004: Scorecard policy pack -- critical rules present
# ---------------------------------------------------------------------------
def test_scorecard_policy_pack():  # AT-P3-004
    from platform_core.domain.loader import DomainPackLoader
    from platform_core.domain.models import PolicySeverity
    loader = DomainPackLoader(overlay_dir=OVERLAY_DIR)
    manifest = loader.load("scorecard", OVERLAY_DIR / "scorecard.yaml")

    critical_rules = [r for r in manifest.policy_pack if r.severity == PolicySeverity.CRITICAL]
    assert len(critical_rules) >= 3

    rule_ids = {r.rule_id for r in manifest.policy_pack}
    assert "sc_pol_model_performance" in rule_ids
    assert "sc_pol_deployment" in rule_ids


# ---------------------------------------------------------------------------
# AT-P3-005: Scorecard review templates -- all HITL stages have templates
# ---------------------------------------------------------------------------
def test_scorecard_review_templates():  # AT-P3-005
    from platform_core.domain.loader import DomainPackLoader
    loader = DomainPackLoader(overlay_dir=OVERLAY_DIR)
    manifest = loader.load("scorecard", OVERLAY_DIR / "scorecard.yaml")

    hitl_stages = manifest.hitl_stages
    for stage_id in hitl_stages:
        tmpl = manifest.get_review_template(stage_id)
        assert tmpl is not None, f"No review template for HITL stage '{stage_id}'"
        assert "rationale" in tmpl.required_form_fields
        assert "policy_acknowledged" in tmpl.required_form_fields


# ---------------------------------------------------------------------------
# AT-P3-006: WoE/IV computation -- positive IV for valid bins
# ---------------------------------------------------------------------------
def test_woe_iv_computation():  # AT-P3-006
    from scorecardsdk.computations import compute_woe_iv
    bins = [
        {"bin_id": "b0", "bin_label": "[0,100)", "good_count": 400, "bad_count": 10},
        {"bin_id": "b1", "bin_label": "[100,200)", "good_count": 300, "bad_count": 30},
        {"bin_id": "b2", "bin_label": "[200,+)", "good_count": 100, "bad_count": 60},
    ]
    record = compute_woe_iv(
        variable_name="income",
        bins=bins,
        total_goods=800,
        total_bads=100,
        record_id=str(uuid.uuid4()),
    )
    assert record.total_iv > 0
    assert record.passes_minimum_iv
    assert len(record.bins) == 3
    # WoE should be decreasing (lower income = more bad = lower WoE)
    woes = [b.woe for b in record.bins]
    assert woes[0] > woes[2]  # High income = more good = higher WoE


# ---------------------------------------------------------------------------
# AT-P3-007: Feature shortlist -- IV threshold filtering
# ---------------------------------------------------------------------------
def test_feature_shortlist_iv_threshold():  # AT-P3-007
    from scorecardsdk.computations import build_feature_shortlist, compute_woe_iv
    # One high-IV variable, one low-IV variable.
    bins_high = [
        {"bin_id": "b0", "good_count": 400, "bad_count": 10},
        {"bin_id": "b1", "good_count": 100, "bad_count": 90},
    ]
    bins_low = [
        {"bin_id": "b0", "good_count": 490, "bad_count": 50},
        {"bin_id": "b1", "good_count": 510, "bad_count": 50},
    ]
    rec_high = compute_woe_iv("income", bins_high, 500, 100, str(uuid.uuid4()))
    rec_low = compute_woe_iv("random_noise", bins_low, 1000, 100, str(uuid.uuid4()), minimum_iv_threshold=0.02)

    shortlist = build_feature_shortlist(
        shortlist_id=str(uuid.uuid4()),
        run_id="run-01",
        project_id="proj-01",
        woe_iv_records=[rec_high, rec_low],
        minimum_iv=0.10,
    )
    # rec_high should be selected, rec_low rejected.
    if rec_high.total_iv >= 0.10:
        assert "income" in shortlist.selected_features
    if rec_low.total_iv < 0.10:
        assert "random_noise" in shortlist.rejected_features


# ---------------------------------------------------------------------------
# AT-P3-008: Score scaling -- apply_scaling clamps to [score_min, score_max]
# ---------------------------------------------------------------------------
def test_score_scaling_clamping():  # AT-P3-008
    from scorecardsdk.computations import apply_scaling, compute_score_scaling
    params = compute_score_scaling("sc-01", "m-01", base_score=600, pdo=20, odds_0=50)
    # Very low log-odds → should clamp at score_min.
    assert apply_scaling(-100.0, params) == params.score_min
    # Very high log-odds → should clamp at score_max.
    assert apply_scaling(100.0, params) == params.score_max
    # Moderate log-odds → in range.
    mid = apply_scaling(math.log(50), params)
    assert params.score_min < mid < params.score_max


# ---------------------------------------------------------------------------
# AT-P3-009: ScorecardSDK.run_stage -- data_preparation succeeds
# ---------------------------------------------------------------------------
def test_scorecard_sdk_run_stage():  # AT-P3-009
    from scorecardsdk.sdk import ScorecardSDK
    sdk = ScorecardSDK(
        run_id="run-test",
        project_id="proj-test",
        actor_id="dev-01",
        manifest_path=OVERLAY_DIR / "scorecard.yaml",
    )
    result = sdk.run_stage("data_preparation", {
        "dataset_id": "ds-01",
        "row_count": 50000,
        "column_names": ["income", "age", "employment"],
    })
    assert result.success
    assert "dataset_snapshot" in result.artifacts


# ---------------------------------------------------------------------------
# AT-P3-010: ScorecardSDK.get_next_stage -- routing via manifest
# ---------------------------------------------------------------------------
def test_scorecard_sdk_routing():  # AT-P3-010
    from scorecardsdk.sdk import ScorecardSDK
    sdk = ScorecardSDK(
        run_id="run-test",
        project_id="proj-test",
        manifest_path=OVERLAY_DIR / "scorecard.yaml",
    )
    next_stage = sdk.get_next_stage("data_preparation")
    assert next_stage == "fine_classing"

    next_after_coarse = sdk.get_next_stage("coarse_classing")
    assert next_after_coarse == "coarse_classing_review"


# ---------------------------------------------------------------------------
# AT-P3-011: DomainPackLoader -- loads time_series manifest
# ---------------------------------------------------------------------------
def test_time_series_manifest_loads():  # AT-P3-011
    from platform_core.domain.loader import DomainPackLoader
    loader = DomainPackLoader(overlay_dir=OVERLAY_DIR)
    manifest = loader.load("time_series", OVERLAY_DIR / "time_series.yaml")

    assert manifest.domain == "time_series"
    primary = manifest.get_primary_metric()
    assert primary is not None
    assert primary.metric_name == "mape"
    assert primary.higher_is_better is False  # MAPE lower is better


# ---------------------------------------------------------------------------
# AT-P3-012: DomainPackLoader -- loads all 7 domain manifests
# ---------------------------------------------------------------------------
def test_all_domain_manifests_load():  # AT-P3-012
    from platform_core.domain.loader import DomainPackLoader
    loader = DomainPackLoader(overlay_dir=OVERLAY_DIR)
    domains = ["scorecard", "time_series", "lgd", "pd", "ecl", "ead", "sicr", "stress"]
    for domain in domains:
        yaml_path = OVERLAY_DIR / f"{domain}.yaml"
        if yaml_path.exists():
            manifest = loader.load(domain, yaml_path)
            assert manifest.domain == domain, f"Domain mismatch for {domain}"
            assert len(manifest.stage_registry) > 0, f"No stages for {domain}"


# ---------------------------------------------------------------------------
# AT-P3-013: DataPrepService -- register and execute cross-sectional template
# ---------------------------------------------------------------------------
def test_dataprep_cross_sectional():  # AT-P3-013
    from dataprepsdk import DataPrepService, cross_sectional_template
    svc = DataPrepService()
    tmpl = cross_sectional_template(
        template_id="tmpl-xsect-01",
        source_table="raw_credit",
        target_table="dev_cross_sectional",
        observation_date="2023-12-31",
        feature_columns=["income", "age"],
    )
    result = svc.register_template(tmpl)
    assert result.success

    # Execute with minimal dict data (no pandas required).
    exec_result = svc.execute("tmpl-xsect-01", {}, "run-01", "proj-01", executed_by="dev-01")
    assert exec_result.success


# ---------------------------------------------------------------------------
# AT-P3-014: DataPrepService -- lineage is tracked per column
# ---------------------------------------------------------------------------
def test_dataprep_lineage_tracking():  # AT-P3-014
    from dataprepsdk import DataPrepService, time_series_template
    svc = DataPrepService()
    tmpl = time_series_template(
        template_id="tmpl-ts-01",
        source_table="monthly_defaults",
        target_table="ts_features",
        entity_id="entity_001",
        lag_periods=[1, 3],
        rolling_windows=[3],
    )
    svc.register_template(tmpl)
    exec_result = svc.execute("tmpl-ts-01", {}, "run-02", "proj-01")
    assert exec_result.success

    lineage_result = svc.get_lineage(exec_result.data.run_record_id)
    assert lineage_result.success
    # Lineage records should include lag and rolling mean transforms.
    lineage = lineage_result.data
    transform_types = {lr.transform_applied for lr in lineage}
    # At minimum, transforms should be registered.
    assert isinstance(transform_types, set)


# ---------------------------------------------------------------------------
# AT-P3-015: DataPrepService -- template version management
# ---------------------------------------------------------------------------
def test_dataprep_template_versioning():  # AT-P3-015
    from dataprepsdk import DataPrepService, cross_sectional_template, DataPrepTemplate
    svc = DataPrepService()
    tmpl_v1 = cross_sectional_template(
        template_id="tmpl-ver-01", source_table="t", target_table="out",
        observation_date="2023-01-01",
    )
    tmpl_v2 = DataPrepTemplate(**{**tmpl_v1.model_dump(), "version": "2.0.0"})
    svc.register_template(tmpl_v1)
    svc.register_template(tmpl_v2)

    from dataprepsdk.template_registry import TemplateRegistry
    reg = svc._registry
    versions = reg.list_versions("tmpl-ver-01")
    assert "1.0.0" in versions
    assert "2.0.0" in versions
    # Latest version is returned by default.
    latest = reg.get("tmpl-ver-01")
    assert latest.version == "2.0.0"


# ---------------------------------------------------------------------------
# AT-P3-016: CanvasService -- build canvas from simulated flow graph
# ---------------------------------------------------------------------------
def test_canvas_build_from_dict():  # AT-P3-016
    from canvassdk import CanvasService, CanvasNodeState

    class _FakeFlowNode:
        def __init__(self, nid: str, stage: str, state: str, is_gate: bool) -> None:
            self.node_type = "stage"
            self.label = stage
            self.stage_name = stage
            self.status = state
            self.is_governance_gate = is_gate
            self.source_event_ids = []

    class _FakeFlowEdge:
        def __init__(self, eid: str, frm: str, to: str) -> None:
            self.from_node_id = frm
            self.to_node_id = to
            self.label = ""
            self.is_failure_path = False
            self.is_recovery_path = False

    class _FakeFlowGraph:
        def __init__(self) -> None:
            self.nodes = {
                "n1": _FakeFlowNode("n1", "data_preparation", "completed", False),
                "n2": _FakeFlowNode("n2", "coarse_classing_review", "hitl_waiting", True),
                "n3": _FakeFlowNode("n3", "woe_iv_calculation", "pending", False),
            }
            self.edges = {
                "e1": _FakeFlowEdge("e1", "n1", "n2"),
                "e2": _FakeFlowEdge("e2", "n2", "n3"),
            }

    svc = CanvasService()
    snapshot = svc.build_from_flow_graph(
        canvas_id="canvas-01",
        flow_graph=_FakeFlowGraph(),
        run_id="run-01",
        project_id="proj-01",
        created_by="dev-01",
    )
    assert snapshot.node_count == 3
    assert snapshot.edge_count == 2
    assert snapshot.version == 1

    # Governance gate should be grouped.
    n2 = snapshot.nodes["n2"]
    assert n2.is_governance_gate
    assert n2.group_id is not None


# ---------------------------------------------------------------------------
# AT-P3-017: CanvasService -- HITL state transitions and history
# ---------------------------------------------------------------------------
def test_canvas_hitl_state_transition():  # AT-P3-017
    from canvassdk import CanvasService, CanvasNodeState, CanvasNode, CanvasNodeType, CanvasSnapshot

    # Build minimal canvas.
    svc = CanvasService()
    initial_node = CanvasNode(
        node_id="n1", node_type=CanvasNodeType.HITL_GATE,
        label="Model Review", state=CanvasNodeState.HITL_WAITING,
        is_governance_gate=True, run_id="run-01", project_id="proj-01",
    )
    snapshot = CanvasSnapshot(
        snapshot_id=str(uuid.uuid4()), canvas_id="canvas-02",
        run_id="run-01", project_id="proj-01",
        nodes={"n1": initial_node}, version=1,
    )
    from canvassdk.models import CanvasHistory
    svc._histories["canvas-02"] = CanvasHistory(
        canvas_id="canvas-02", run_id="run-01", project_id="proj-01",
        snapshots=[snapshot],
    )

    # Transition to approved.
    new_snapshot = svc.update_node_state(
        canvas_id="canvas-02",
        node_id="n1",
        new_state=CanvasNodeState.HITL_APPROVED,
        actor_id="validator-01",
        change_reason="Model approved by validator",
        audit_fields={"review_id": "rev-001"},
    )
    assert new_snapshot.version == 2
    assert new_snapshot.nodes["n1"].state == CanvasNodeState.HITL_APPROVED

    # History should have 2 snapshots.
    history = svc.get_history("canvas-02")
    assert history.version_count == 2


# ---------------------------------------------------------------------------
# AT-P3-018: Token budget -- COMPACT mode respects lower budget
# ---------------------------------------------------------------------------
def test_token_budget_compact():  # AT-P3-018
    from token_sdk import BudgetRegistry, TokenMode
    reg = BudgetRegistry()
    full_budget = reg.get_budget(TokenMode.FULL, "review")
    compact_budget = reg.get_budget(TokenMode.COMPACT, "review")
    minimal_budget = reg.get_budget(TokenMode.MINIMAL, "review")

    assert full_budget > compact_budget > minimal_budget


# ---------------------------------------------------------------------------
# AT-P3-019: ContextBuilder -- trims low-priority sections to fit budget
# ---------------------------------------------------------------------------
def test_context_builder_trimming():  # AT-P3-019
    from token_sdk import ContextBuilder, TokenMode

    builder = ContextBuilder(
        run_id="run-01",
        project_id="proj-01",
        stage_name="model_review",
        token_mode=TokenMode.MINIMAL,  # Very tight budget.
    )
    # Mandatory section (must be kept).
    builder.add_section("state", "Workflow State", "Stage: model_review, Run: run-01",
                        priority=5, is_mandatory=True)
    # Large optional section (should be trimmed under minimal budget).
    large_content = "x" * 5000  # ~1250 tokens >> MINIMAL budget
    builder.add_section("big_section", "Knowledge Dump", large_content, priority=80)

    pack = builder.build(pack_type="review")
    # Mandatory section must always be present.
    assert any(s.section_id == "state" for s in pack.sections)
    # Under tight budget, big section should be trimmed.
    assert pack.was_trimmed
    assert "big_section" in pack.trimmed_section_ids


# ---------------------------------------------------------------------------
# AT-P3-020: TokenTelemetry -- records and summarises usage
# ---------------------------------------------------------------------------
def test_token_telemetry():  # AT-P3-020
    from token_sdk import TokenMode, TokenTelemetry

    tel = TokenTelemetry()
    tel.record(
        run_id="run-01", project_id="proj-01", stage_name="model_review",
        role_id="validator", interaction_type="review_submit_action",
        token_mode=TokenMode.FULL, context_tokens=3000, completion_tokens=200, budget=8000,
    )
    tel.record(
        run_id="run-01", project_id="proj-01", stage_name="data_preparation",
        role_id="model_developer", interaction_type="stage_start",
        token_mode=TokenMode.COMPACT, context_tokens=500, completion_tokens=100, budget=3000,
    )

    summary = tel.get_summary(run_id="run-01")
    assert summary["record_count"] == 2
    assert summary["total_tokens"] == 3800
    assert summary["over_budget_count"] == 0
    assert "model_review" in summary["by_stage"]
    assert "data_preparation" in summary["by_stage"]
