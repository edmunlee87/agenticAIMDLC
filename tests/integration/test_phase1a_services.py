"""Phase 1A integration tests for core utility SDKs.

Verifies that config_sdk, registry_sdk, observabilitysdk, auditsdk, and
artifactsdk work together correctly through representative workflows.

Scope per the plan:
- config_sdk -> registry_sdk wiring
- observability event write + query
- audit record chain reconstruction
- artifact register + lineage + manifest
- cross-SDK governance field propagation

All tests use in-memory stores for determinism.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from sdk.auditsdk.audit_service import AuditService
from sdk.artifactsdk.artifact_service import ArtifactService
from sdk.config_sdk.config_service import ConfigService
from sdk.config_sdk.models import ConfigLoadRequest
from sdk.observabilitysdk.observability_service import ObservabilityService
from sdk.registry_sdk.registry_service import RegistryService


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

CONFIGS_ROOT = str(Path(__file__).parent.parent.parent / "configs" / "runtime")


@pytest.fixture()
def config_svc() -> ConfigService:
    return ConfigService()


@pytest.fixture()
def registry_svc() -> RegistryService:
    return RegistryService(run_id="run_int_001")


@pytest.fixture()
def obs_svc() -> ObservabilityService:
    return ObservabilityService(run_id="run_int_001")


@pytest.fixture()
def audit_svc() -> AuditService:
    return AuditService(run_id="run_int_001", actor="integration_test")


@pytest.fixture()
def artifact_svc() -> ArtifactService:
    return ArtifactService(
        run_id="run_int_001",
        project_id="proj_int_001",
        actor="integration_test",
    )


# ---------------------------------------------------------------------------
# 1. config_sdk -> registry_sdk wiring
# ---------------------------------------------------------------------------

class TestConfigRegistryWiring:
    """config_sdk loads bundle; registry_sdk registers entities referencing it."""

    def test_load_config_and_register_run(
        self, config_svc: ConfigService, registry_svc: RegistryService
    ) -> None:
        cfg_result = config_svc.load_config(ConfigLoadRequest(base_path=CONFIGS_ROOT))
        assert cfg_result.is_success, cfg_result.errors

        version_result = config_svc.get_config_version()
        assert version_result.is_success
        config_version = version_result.data["version"]["schema_version"]

        # register project first (required by register_run)
        registry_svc.register_project(
            project_id="proj_cfg_001",
            project_name="Config Wiring Test",
            domain="generic",
            owner="analyst_01",
        )
        run_result = registry_svc.register_run(
            run_id="run_cfg_001",
            project_id="proj_cfg_001",
            actor="analyst_01",
            config_version=config_version,
        )
        assert run_result.is_success

        run = registry_svc.get_run("run_cfg_001")
        assert run.is_success
        assert run.data["run"]["config_version"] == config_version

    def test_config_diff_same_directory(self, config_svc: ConfigService) -> None:
        diff = config_svc.diff_config(CONFIGS_ROOT, CONFIGS_ROOT)
        assert diff.is_success
        assert diff.data["diffs"] == []

    def test_get_config_version_without_load_fails(self, config_svc: ConfigService) -> None:
        result = config_svc.get_config_version()
        assert not result.is_success
        assert len(result.errors) > 0

    def test_validate_config(self, config_svc: ConfigService) -> None:
        result = config_svc.validate_config(CONFIGS_ROOT)
        assert result.is_success


# ---------------------------------------------------------------------------
# 2. Observability: event write + query
# ---------------------------------------------------------------------------

class TestObservabilityEventWriteQuery:
    def test_write_and_query_events(self, obs_svc: ObservabilityService) -> None:
        trace = obs_svc.create_trace(
            run_id="run_int_001",
            skill_name="data_prep_skill",
            stage_name="data_preparation",
        )
        assert trace.is_success
        trace_id = trace.data["trace_id"]

        for event_type in [
            "stage_started",
            "skill_started",
            "skill_completed",
            "stage_completed",
        ]:
            write = obs_svc.write_event(
                event_type=event_type,
                stage_name="data_preparation",
                run_id="run_int_001",
                parent_event_id=trace_id,
            )
            assert write.is_success, f"write_event failed for {event_type}: {write.errors}"

        # query returns trace + 4 events = 5 total
        query = obs_svc.query_events(run_id="run_int_001")
        assert query.is_success
        assert query.data["count"] == 5

    def test_query_events_by_type_filter(self, obs_svc: ObservabilityService) -> None:
        trace = obs_svc.create_trace(
            run_id="run_int_002",
            skill_name="model_skill",
            stage_name="model_fitting",
        )
        trace_id = trace.data["trace_id"]
        obs_svc.write_event("stage_started", stage_name="model_fitting", run_id="run_int_002", parent_event_id=trace_id)
        obs_svc.write_event("skill_started", stage_name="model_fitting", run_id="run_int_002", parent_event_id=trace_id)
        obs_svc.write_event(
            "skill_failed",
            stage_name="model_fitting",
            run_id="run_int_002",
            parent_event_id=trace_id,
            error_detail="timeout",
            status="failure",
        )

        result = obs_svc.query_events(run_id="run_int_002", event_type="skill_failed")
        assert result.is_success
        assert result.data["count"] == 1

    def test_replay_run(self, obs_svc: ObservabilityService) -> None:
        trace = obs_svc.create_trace(
            run_id="run_replay",
            skill_name="replay_skill",
            stage_name="session_bootstrap",
        )
        trace_id = trace.data["trace_id"]
        obs_svc.write_event("stage_started", stage_name="session_bootstrap", run_id="run_replay", parent_event_id=trace_id)
        obs_svc.write_event("stage_completed", stage_name="session_bootstrap", run_id="run_replay", parent_event_id=trace_id)

        replay = obs_svc.replay_run(run_id="run_replay")
        assert replay.is_success
        assert replay.data["count"] == 3  # trace + 2 events


# ---------------------------------------------------------------------------
# 3. Audit: record chain reconstruction
# ---------------------------------------------------------------------------

class TestAuditRecordChain:
    def test_chain_reconstruction(self, audit_svc: AuditService) -> None:
        r1 = audit_svc.register_decision("data_preparation", run_id="run_int_001", reason="Data validated.")
        r2 = audit_svc.register_approval(
            "model_fitting", approver="governance_01", run_id="run_int_001", reason="Model approved."
        )
        r3 = audit_svc.register_signoff(
            "deployment_readiness", signatory="cro_01", run_id="run_int_001", reason="Cleared for deployment."
        )

        leaf_id = r3.data["audit_id"]
        chain_result = audit_svc.get_audit_chain(leaf_id)
        assert chain_result.is_success
        chain = chain_result.data["chain"]
        assert len(chain) == 3
        assert chain[0]["audit_id"] == r1.data["audit_id"]
        assert chain[1]["preceding_audit_id"] == r1.data["audit_id"]
        assert chain[-1]["audit_id"] == leaf_id

    def test_export_and_filter_bundle(self, audit_svc: AuditService) -> None:
        audit_svc.register_decision("stage_a", run_id="run_a")
        audit_svc.register_decision("stage_b", run_id="run_b")
        audit_svc.register_approval("stage_b", approver="app_01", run_id="run_b")

        bundle_a = audit_svc.export_audit_bundle(run_id="run_a")
        assert bundle_a.is_success
        assert bundle_a.data["bundle"]["total_count"] == 1

        bundle_b = audit_svc.export_audit_bundle(run_id="run_b")
        assert bundle_b.data["bundle"]["total_count"] == 2

    def test_audit_types_coverage(self, audit_svc: AuditService) -> None:
        audit_svc.register_decision("s", run_id="run_types")
        audit_svc.register_approval("s", approver="app", run_id="run_types")
        audit_svc.register_exception("s", run_id="run_types")
        audit_svc.register_signoff("s", signatory="sig", run_id="run_types")
        bundle = audit_svc.export_audit_bundle(run_id="run_types")
        assert bundle.data["bundle"]["total_count"] == 4


# ---------------------------------------------------------------------------
# 4. Artifact: register + lineage + manifest
# ---------------------------------------------------------------------------

class TestArtifactRegisterLineageManifest:
    def test_register_and_validate(self, artifact_svc: ArtifactService) -> None:
        payload = b"binning_table_binary"
        result = artifact_svc.register_artifact(
            artifact_type="binning_summary",
            artifact_name="var_age_bins",
            stage_name="coarse_classing",
            uri_or_path="/artifacts/bins.parquet",
            raw_bytes=payload,
        )
        assert result.is_success
        artifact_id = result.data["artifact_id"]

        val = artifact_svc.validate_artifact(artifact_id, raw_bytes=payload)
        assert val.is_success
        assert val.data["checksum_valid"] is True

    def test_lineage_chain(self, artifact_svc: ArtifactService) -> None:
        raw = artifact_svc.register_artifact(
            artifact_type="raw_dataset", artifact_name="raw_data", stage_name="data_ingestion"
        )
        bins = artifact_svc.register_artifact(
            artifact_type="binning_summary",
            artifact_name="bins_v1",
            stage_name="coarse_classing",
            lineage_parent_ids=[raw.data["artifact_id"]],
        )
        model = artifact_svc.register_artifact(
            artifact_type="model_object",
            artifact_name="logistic_v1",
            stage_name="model_fitting",
            lineage_parent_ids=[bins.data["artifact_id"]],
        )

        lineage = artifact_svc.get_artifact_lineage(bins.data["artifact_id"])
        assert lineage.is_success
        assert len(lineage.data["as_parent"]) == 1
        assert lineage.data["as_parent"][0]["child_id"] == model.data["artifact_id"]
        assert len(lineage.data["as_child"]) == 1
        assert lineage.data["as_child"][0]["parent_id"] == raw.data["artifact_id"]

    def test_build_committee_pack_manifest(self, artifact_svc: ArtifactService) -> None:
        ids = []
        for artifact_type in ["binning_summary", "model_object", "score_output", "validation_report"]:
            r = artifact_svc.register_artifact(
                artifact_type=artifact_type,
                artifact_name=f"{artifact_type}_v1",
                stage_name="model_fitting",
            )
            ids.append(r.data["artifact_id"])

        manifest = artifact_svc.build_artifact_manifest(
            artifact_ids=ids,
            manifest_type="committee_pack",
            metadata={"committee": "model_risk_committee"},
        )
        assert manifest.is_success
        bundle = manifest.data["manifest"]
        assert bundle["artifact_count"] == 4
        assert bundle["manifest_type"] == "committee_pack"

    def test_locate_artifacts_multi_filter(self, artifact_svc: ArtifactService) -> None:
        artifact_svc.register_artifact(
            artifact_type="model_object",
            artifact_name="model_a",
            stage_name="model_fitting",
            source_candidate_version_id="cnd_001",
        )
        artifact_svc.register_artifact(
            artifact_type="model_object",
            artifact_name="model_b",
            stage_name="model_fitting",
            source_candidate_version_id="cnd_002",
        )
        result = artifact_svc.locate_artifact(
            artifact_type="model_object",
            source_candidate_version_id="cnd_001",
        )
        assert result.is_success
        assert result.data["count"] == 1
        assert result.data["artifacts"][0]["source_candidate_version_id"] == "cnd_001"


# ---------------------------------------------------------------------------
# 5. Cross-SDK governance field propagation
# ---------------------------------------------------------------------------

class TestCrossSDKGovernanceFieldPropagation:
    """End-to-end mini workflow verifying governance fields flow across SDKs."""

    def test_run_lifecycle_with_governance_fields(
        self,
        registry_svc: RegistryService,
        obs_svc: ObservabilityService,
        audit_svc: AuditService,
        artifact_svc: ArtifactService,
    ) -> None:
        run_id = "run_gov_001"
        project_id = "proj_gov_001"
        actor = "analyst_01"
        stage = "coarse_classing"

        # Register project + run
        registry_svc.register_project(
            project_id=project_id,
            project_name="Governance Test Project",
            domain="credit_risk",
            owner=actor,
        )
        registry_svc.register_run(
            run_id=run_id,
            project_id=project_id,
            actor=actor,
            domain="credit_risk",
        )

        # Emit lifecycle events
        trace = obs_svc.create_trace(
            run_id=run_id,
            skill_name="coarse_classing_skill",
            stage_name=stage,
        )
        assert trace.is_success
        trace_id = trace.data["trace_id"]
        obs_svc.write_event("stage_started", stage_name=stage, run_id=run_id, parent_event_id=trace_id)
        obs_svc.write_event("artifact_registered", stage_name=stage, run_id=run_id, parent_event_id=trace_id)
        obs_svc.write_event("hitl_review_created", stage_name=stage, run_id=run_id, parent_event_id=trace_id)

        # Register artifact with governance fields
        art = artifact_svc.register_artifact(
            artifact_type="binning_summary",
            artifact_name="var_age_bins",
            stage_name=stage,
            run_id=run_id,
            project_id=project_id,
            actor=actor,
            trace_id=trace_id,
            metadata={"analyst": actor, "domain": "credit_risk"},
        )
        assert art.is_success
        artifact_id = art.data["artifact_id"]
        assert artifact_id in art.artifacts_created

        # Audit the decision
        decision = audit_svc.register_decision(
            stage_name=stage,
            run_id=run_id,
            project_id=project_id,
            actor=actor,
            reason="Coarse classing bins accepted by analyst.",
            decision_payload={"artifact_id": artifact_id},
        )
        assert decision.is_success

        # Audit approval
        approval = audit_svc.register_approval(
            stage_name=stage,
            approver="model_risk_officer",
            run_id=run_id,
            project_id=project_id,
            reason="Bins reviewed and approved.",
        )
        assert approval.is_success

        # Verify audit chain depth
        chain = audit_svc.get_audit_chain(approval.data["audit_id"])
        assert chain.is_success
        assert chain.data["length"] == 2

        # Verify observability completeness (trace + 3 events = 4)
        events = obs_svc.query_events(run_id=run_id)
        assert events.is_success
        assert events.data["count"] == 4

        # Verify artifact is locatable with governance fields intact
        located = artifact_svc.locate_artifact(run_id=run_id, artifact_type="binning_summary")
        assert located.is_success
        assert located.data["count"] == 1
        stored_record = located.data["artifacts"][0]
        assert stored_record["trace_id"] == trace_id
        assert stored_record["metadata"]["analyst"] == actor

    def test_observability_lineage_from_multiple_events(
        self, obs_svc: ObservabilityService
    ) -> None:
        trace = obs_svc.create_trace(
            run_id="run_lin_obs",
            skill_name="lineage_skill",
            stage_name="model_fitting",
        )
        trace_id = trace.data["trace_id"]
        e1 = obs_svc.write_event(
            "stage_started",
            stage_name="model_fitting",
            run_id="run_lin_obs",
            parent_event_id=trace_id,
        )
        e2 = obs_svc.write_event(
            "skill_completed",
            stage_name="model_fitting",
            run_id="run_lin_obs",
            parent_event_id=e1.data["event_id"],
        )

        lineage = obs_svc.build_event_lineage(e2.data["event_id"])
        assert lineage.is_success
        chain = lineage.data["lineage"]["chain"]
        assert len(chain) >= 1
