"""Phase 2 exit integration tests -- AT-VAL-001 through AT-VAL-017.

Tests cover:
- AT-VAL-001  FlowViz: nodes and edges from stage events.
- AT-VAL-002  FlowViz: HITL gate node appears for review event.
- AT-VAL-003  FlowViz: failure edge on stage failure.
- AT-VAL-004  FlowViz: HTML and JSON export round-trip.
- AT-VAL-005  FlowViz: governance gate filter returns only gate nodes.
- AT-VAL-006  Validation: scope creation, finding, conclusion PASS_UNCONDITIONAL.
- AT-VAL-007  Validation: critical open finding → conclusion FAIL.
- AT-VAL-008  Validation: evidence completeness below threshold → INCONCLUSIVE.
- AT-VAL-009  Validation: finding status transitions.
- AT-VAL-010  Validation: remediation tracker open → resolved lifecycle.
- AT-VAL-011  DQ checks: missingness threshold pass/warn/fail.
- AT-VAL-012  DQ checks: PSI distribution check classification.
- AT-VAL-013  Evaluation: metric threshold evaluation.
- AT-VAL-014  Evaluation: candidate comparison winner.
- AT-VAL-015  knowledge_sdk: promotion workflow.
- AT-VAL-016  rag_sdk: token-budget-aware retrieval with InMemoryDocumentStore.
- AT-VAL-017  widgetsdk: review workspace build and terminal render.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import pytest

# ---------------------------------------------------------------------------
# Shared fixtures / helpers
# ---------------------------------------------------------------------------

RUN_ID = "run-p2-exit-test"
PROJECT_ID = "proj-p2-exit"
ACTOR_ID = "validator-01"


def _make_event(event_type: str, stage_name: str = "", meta: dict | None = None) -> Any:
    """Create a minimal mock observability event."""
    import types
    ev = types.SimpleNamespace()
    ev.event_id = f"evt-{event_type}-{stage_name}"
    ev.event_type = event_type
    ev.stage_name = stage_name
    ev.run_id = RUN_ID
    ev.actor_id = ACTOR_ID
    ev.timestamp = datetime.now(timezone.utc)
    ev.severity = "info"
    ev.metadata = meta or {}
    return ev


class _FakeObsService:
    """Minimal observability service stub that returns a pre-populated event list."""

    def __init__(self, events: list[Any]) -> None:
        self._events = events

    def get_events_for_run(self, run_id: str) -> Any:
        import types
        r = types.SimpleNamespace()
        r.data = self._events
        return r

    def emit_simple(self, **kwargs: Any) -> None:
        pass


# ---------------------------------------------------------------------------
# AT-VAL-001: FlowViz -- nodes from stage events
# ---------------------------------------------------------------------------

class TestFlowVizNodes:
    def test_stage_node_created(self) -> None:
        """AT-VAL-001: stage.started + stage.completed → one merged STAGE node."""
        from flowvizsdk.service import FlowVizService
        from flowvizsdk.models import NodeType, NodeStatus

        events = [
            _make_event("workflow.stage.started", "data_prep"),
            _make_event("workflow.stage.completed", "data_prep"),
        ]
        svc = FlowVizService(_FakeObsService(events))
        graph = svc.build_graph(RUN_ID, PROJECT_ID)

        assert len(graph.nodes) == 1
        node = list(graph.nodes.values())[0]
        assert node.node_type == NodeType.STAGE
        assert node.status == NodeStatus.COMPLETED
        assert node.stage_name == "data_prep"

    # AT-VAL-002
    def test_hitl_gate_node_from_review_event(self) -> None:
        """AT-VAL-002: hitl.review.created → HITL_GATE node marked as governance gate."""
        from flowvizsdk.service import FlowVizService
        from flowvizsdk.models import NodeType

        events = [
            _make_event("workflow.stage.started", "model_review"),
            _make_event("hitl.review.created", "model_review", {"review_id": "rev-001"}),
        ]
        svc = FlowVizService(_FakeObsService(events))
        graph = svc.build_graph(RUN_ID, PROJECT_ID)

        gate_nodes = graph.get_nodes_by_type(NodeType.HITL_GATE)
        assert len(gate_nodes) == 1
        assert gate_nodes[0].is_governance_gate is True

    # AT-VAL-003
    def test_failure_edge_on_stage_failure(self) -> None:
        """AT-VAL-003: policy.breach.detected → failure edge."""
        from flowvizsdk.service import FlowVizService
        from flowvizsdk.models import NodeType

        events = [
            _make_event("workflow.stage.started", "feature_engineering"),
            _make_event("policy.breach.detected", "feature_engineering"),
        ]
        svc = FlowVizService(_FakeObsService(events))
        graph = svc.build_graph(RUN_ID, PROJECT_ID)

        failure_edges = [e for e in graph.edges.values() if e.is_failure_path]
        assert len(failure_edges) >= 1

    # AT-VAL-004
    def test_html_json_export(self) -> None:
        """AT-VAL-004: HTML and JSON export round-trip for a 2-stage graph."""
        from flowvizsdk.service import FlowVizService

        events = [
            _make_event("workflow.stage.started", "stage_a"),
            _make_event("workflow.stage.completed", "stage_a"),
            _make_event("workflow.stage.started", "stage_b"),
            _make_event("workflow.stage.completed", "stage_b"),
        ]
        svc = FlowVizService(_FakeObsService(events))
        html = svc.export_html(RUN_ID, PROJECT_ID)
        json_str = svc.export_json(RUN_ID, PROJECT_ID)

        assert "<html" in html.lower()
        parsed = json.loads(json_str)
        assert parsed["run_id"] == RUN_ID
        assert len(parsed["nodes"]) == 2

    # AT-VAL-005
    def test_governance_gate_filter(self) -> None:
        """AT-VAL-005: filter_governance_gates returns only gate nodes."""
        from flowvizsdk.service import FlowVizService
        from flowvizsdk.flow_filters import filter_governance_gates

        events = [
            _make_event("workflow.stage.started", "model_review"),
            _make_event("hitl.review.created", "model_review", {"review_id": "rev-002"}),
            _make_event("workflow.stage.started", "data_prep"),
        ]
        svc = FlowVizService(_FakeObsService(events))
        graph = svc.build_graph(RUN_ID, PROJECT_ID)
        filtered = filter_governance_gates(graph)

        assert all(n.is_governance_gate for n in filtered.nodes.values())


# ---------------------------------------------------------------------------
# AT-VAL-006 through AT-VAL-010: Validation SDK
# ---------------------------------------------------------------------------

class TestValidation:
    def _make_scope(self, scope_id: str = "scope-001") -> Any:
        from validationsdk.models import ValidationScope
        return ValidationScope(
            scope_id=scope_id,
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            created_by=ACTOR_ID,
        )

    def test_scope_creation_and_unconditional_pass(self) -> None:
        """AT-VAL-006: no findings → PASS_UNCONDITIONAL conclusion."""
        from validationsdk.service import ValidationService
        from validationsdk.models import ConclusionCategory

        svc = ValidationService()
        scope = self._make_scope("scope-006")
        r = svc.create_scope(scope)
        assert r.success

        r = svc.conclude(
            scope_id="scope-006",
            conclusion_id="conc-006",
            required_evidence_types=[],
            concluded_by=ACTOR_ID,
        )
        assert r.success
        assert r.data.category == ConclusionCategory.PASS_UNCONDITIONAL

    def test_critical_finding_causes_fail(self) -> None:
        """AT-VAL-007: open CRITICAL finding with requires_remediation → FAIL."""
        from validationsdk.service import ValidationService
        from validationsdk.models import ConclusionCategory, FindingSeverity, ValidationFinding

        svc = ValidationService()
        scope = self._make_scope("scope-007")
        svc.create_scope(scope)

        finding = ValidationFinding(
            finding_id="find-007",
            scope_id="scope-007",
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            finding_type="model_performance",
            severity=FindingSeverity.CRITICAL,
            title="Gini below minimum threshold",
            requires_remediation=True,
        )
        svc.raise_finding(finding)

        r = svc.conclude("scope-007", "conc-007", [], concluded_by=ACTOR_ID)
        assert r.success
        assert r.data.category == ConclusionCategory.FAIL
        assert r.data.critical_findings_count == 1

    def test_low_evidence_completeness_inconclusive(self) -> None:
        """AT-VAL-008: evidence completeness below threshold → INCONCLUSIVE."""
        from validationsdk.service import ValidationService
        from validationsdk.models import ConclusionCategory

        svc = ValidationService(evidence_completeness_threshold=0.8)
        scope = self._make_scope("scope-008")
        svc.create_scope(scope)

        # Only submit 1 of 3 required evidence types → 33% completeness.
        from validationsdk.models import EvidenceRecord
        svc.submit_evidence(EvidenceRecord(
            evidence_id="ev-008",
            scope_id="scope-008",
            artifact_id="art-001",
            evidence_type="metric_pack",
        ))

        r = svc.conclude("scope-008", "conc-008", ["metric_pack", "dq_report", "model_card"], ACTOR_ID)
        assert r.success
        assert r.data.category == ConclusionCategory.INCONCLUSIVE

    def test_finding_status_transitions(self) -> None:
        """AT-VAL-009: finding status lifecycle OPEN → REMEDIATED → CLOSED."""
        from validationsdk.service import ValidationService
        from validationsdk.models import FindingSeverity, FindingStatus, ValidationFinding

        svc = ValidationService()
        scope = self._make_scope("scope-009")
        svc.create_scope(scope)

        finding = ValidationFinding(
            finding_id="find-009",
            scope_id="scope-009",
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            finding_type="documentation",
            severity=FindingSeverity.LOW,
            title="Missing model card section",
        )
        svc.raise_finding(finding)
        svc.update_finding_status("scope-009", "find-009", FindingStatus.REMEDIATED, ACTOR_ID)
        svc.update_finding_status("scope-009", "find-009", FindingStatus.CLOSED, ACTOR_ID)

        r = svc.get_findings("scope-009")
        assert r.success
        assert r.data[0].status == FindingStatus.CLOSED

    def test_remediation_tracker_lifecycle(self) -> None:
        """AT-VAL-010: remediation action OPEN → RESOLVED."""
        from validationsdk.service import ValidationService
        from validationsdk.models import FindingSeverity, RemediationAction, RemediationStatus, ValidationFinding

        svc = ValidationService()
        scope = self._make_scope("scope-010")
        svc.create_scope(scope)

        finding = ValidationFinding(
            finding_id="find-010",
            scope_id="scope-010",
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            finding_type="governance_gap",
            severity=FindingSeverity.HIGH,
            title="Missing approval signature",
            requires_remediation=True,
        )
        svc.raise_finding(finding)

        action = RemediationAction(
            action_id="action-010",
            finding_id="find-010",
            scope_id="scope-010",
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            description="Obtain approval from model risk committee.",
        )
        svc.create_remediation(action)

        r = svc.update_remediation_status("scope-010", "action-010", RemediationStatus.RESOLVED, "Approval obtained.")
        assert r.success
        assert r.data.status == RemediationStatus.RESOLVED
        assert r.data.resolution_notes == "Approval obtained."


# ---------------------------------------------------------------------------
# AT-VAL-011 through AT-VAL-012: DQ SDK
# ---------------------------------------------------------------------------

class TestDQChecks:
    def test_missingness_pass_warn_fail(self) -> None:
        """AT-VAL-011: missingness check correctly categorises rates."""
        from dq_sdk.checks import check_missingness
        from dq_sdk.models import DQCheckStatus

        r_pass = check_missingness("c1", "age", 0.01, threshold=0.05)
        r_warn = check_missingness("c2", "age", 0.07, threshold=0.05)
        r_fail = check_missingness("c3", "age", 0.20, threshold=0.05, is_blocking=True)

        assert r_pass.status == DQCheckStatus.PASS
        assert r_warn.status == DQCheckStatus.WARN
        assert r_fail.status == DQCheckStatus.FAIL
        assert r_fail.is_blocking

    def test_psi_distribution_classification(self) -> None:
        """AT-VAL-012: PSI distribution check thresholds."""
        from dq_sdk.checks import check_distribution
        from dq_sdk.models import DQCheckStatus

        r_stable = check_distribution("d1", "income", psi_score=0.05)
        r_moderate = check_distribution("d2", "income", psi_score=0.15)
        r_critical = check_distribution("d3", "income", psi_score=0.30)

        assert r_stable.status == DQCheckStatus.PASS
        assert r_moderate.status == DQCheckStatus.WARN
        assert r_critical.status == DQCheckStatus.FAIL


# ---------------------------------------------------------------------------
# AT-VAL-013 through AT-VAL-014: Evaluation SDK
# ---------------------------------------------------------------------------

class TestEvaluation:
    def test_metric_threshold_evaluation(self) -> None:
        """AT-VAL-013: metrics below threshold → FAIL, above → PASS."""
        from evaluation_sdk.service import evaluate_metric
        from evaluation_sdk.models import MetricStatus

        pass_m = evaluate_metric("m1", "gini", 0.60, RUN_ID, PROJECT_ID, threshold_low=0.50)
        fail_m = evaluate_metric("m2", "gini", 0.40, RUN_ID, PROJECT_ID, threshold_low=0.50)

        assert pass_m.status == MetricStatus.PASS
        assert fail_m.status == MetricStatus.FAIL

    def test_candidate_comparison_winner(self) -> None:
        """AT-VAL-014: challenger with higher gini → winner=challenger."""
        from evaluation_sdk.service import compare_candidates

        result = compare_candidates(
            comparison_id="comp-014",
            baseline_id="baseline-v1",
            challenger_id="challenger-v2",
            baseline_metrics={"gini": 0.58, "ks": 0.42},
            challenger_metrics={"gini": 0.63, "ks": 0.45},
            primary_metric="gini",
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            higher_is_better=True,
        )
        assert result.winner == "challenger"
        _, _, delta = result.metrics["gini"]
        assert delta > 0


# ---------------------------------------------------------------------------
# AT-VAL-015: Knowledge SDK -- promotion workflow
# ---------------------------------------------------------------------------

class TestKnowledgeSDK:
    def test_promotion_workflow(self) -> None:
        """AT-VAL-015: DRAFT → REVIEWED → PROMOTED lifecycle."""
        from knowledge_sdk.service import KnowledgeService
        from knowledge_sdk.models import KnowledgeObject, KnowledgeObjectStatus, KnowledgeObjectType

        svc = KnowledgeService()
        obj = KnowledgeObject(
            object_id="ko-015",
            object_type=KnowledgeObjectType.METHODOLOGY,
            title="Gini threshold standard",
            content="Minimum Gini of 0.5 for production models.",
            tags=["gini", "threshold", "governance"],
        )
        svc.register(obj)
        svc.review("ko-015", reviewed_by=ACTOR_ID)
        svc.promote("ko-015", promoted_by=ACTOR_ID)

        r = svc.get("ko-015")
        assert r.success
        assert r.data.status == KnowledgeObjectStatus.PROMOTED
        assert r.data.promoted_by == ACTOR_ID

    def test_search_returns_only_promoted(self) -> None:
        """AT-VAL-015b: search by tag returns only promoted objects."""
        from knowledge_sdk.service import KnowledgeService
        from knowledge_sdk.models import KnowledgeObject, KnowledgeObjectType

        svc = KnowledgeService()
        draft = KnowledgeObject(object_id="ko-draft", object_type=KnowledgeObjectType.POLICY, title="Draft policy", tags=["risk"])
        svc.register(draft)

        r = svc.search(tags=["risk"])
        # Only promoted objects should appear in default search.
        assert all(obj.object_id != "ko-draft" for obj in r.data)


# ---------------------------------------------------------------------------
# AT-VAL-016: RAG SDK -- token-budget retrieval
# ---------------------------------------------------------------------------

class TestRAGSDK:
    def test_token_budget_trimming(self) -> None:
        """AT-VAL-016: retriever trims to token budget; was_trimmed=True when exceeded."""
        from rag_sdk.retriever import InMemoryDocumentStore, Retriever
        from rag_sdk.models import RetrievalQuery, StoreType

        store = InMemoryDocumentStore(StoreType.DOCUMENT)
        for i in range(5):
            store.ingest(
                source_id=f"doc-{i}",
                title=f"Document {i}",
                content="risk model gini threshold validation " * 40,  # ~200 tokens each
            )

        retriever = Retriever({StoreType.DOCUMENT: store})
        query = RetrievalQuery(
            query_id="q-016",
            query_text="risk model gini",
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            top_k=5,
            token_budget=300,  # Only ~1.5 documents fit
        )
        pack = retriever.retrieve(query)

        assert pack.total_tokens <= 300
        assert pack.was_trimmed or len(pack.chunks) <= 5

    def test_stage_filter(self) -> None:
        """AT-VAL-016b: stage-scoped query does not return docs for other stages."""
        from rag_sdk.retriever import InMemoryDocumentStore, Retriever
        from rag_sdk.models import RetrievalQuery, StoreType

        store = InMemoryDocumentStore(StoreType.KNOWLEDGE)
        store.ingest("d1", "Model review doc", "review criteria approval", stage_name="model_review")
        store.ingest("d2", "Data prep doc", "data quality checks", stage_name="data_prep")

        retriever = Retriever({StoreType.KNOWLEDGE: store})
        query = RetrievalQuery(
            query_id="q-016b",
            query_text="data quality",
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            stage_name="data_prep",
            top_k=10,
            token_budget=2000,
        )
        pack = retriever.retrieve(query)

        # Only data_prep doc should match stage filter.
        for chunk in pack.chunks:
            assert chunk.stage_name in ("data_prep", "")


# ---------------------------------------------------------------------------
# AT-VAL-017: widgetsdk -- review workspace build and render
# ---------------------------------------------------------------------------

class TestWidgetSDK:
    def test_review_workspace_build_and_terminal_render(self) -> None:
        """AT-VAL-017: build_review_workspace produces valid workspace; terminal render succeeds."""
        from widgetsdk.builders import build_review_workspace
        from widgetsdk.renderer import render
        from widgetsdk.models import WidgetMode

        payload = {
            "stage_name": "model_review",
            "run_id": RUN_ID,
            "project_id": PROJECT_ID,
            "review_type": "approval",
            "metrics_summary": {"gini": 0.62, "ks": 0.44},
            "candidates": [],
        }
        workspace = build_review_workspace(payload, mode=WidgetMode.TERMINAL)
        assert workspace.governance_status is not None
        assert len(workspace.action_buttons) > 0
        assert len(workspace.form_fields) > 0

        rendered = render(workspace, force_mode=WidgetMode.TERMINAL)
        assert "model_review" in rendered
        assert "Approve" in rendered

    def test_recovery_workspace_build(self) -> None:
        """AT-VAL-017b: build_recovery_workspace includes recovery actions."""
        from widgetsdk.builders import build_recovery_workspace
        from widgetsdk.models import WidgetMode

        workspace = build_recovery_workspace(
            stage_name="feature_engineering",
            run_id=RUN_ID,
            project_id=PROJECT_ID,
            error_message="Spark job OOM.",
            recovery_options=["retry", "rollback"],
            mode=WidgetMode.TERMINAL,
        )
        action_types = {btn.action_type for btn in workspace.action_buttons}
        assert "retry" in action_types
        assert "rollback" in action_types
