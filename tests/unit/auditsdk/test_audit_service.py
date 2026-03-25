"""Unit tests for AuditService."""

import pytest

from sdk.auditsdk.audit_service import AuditService
from sdk.auditsdk.models import AUDIT_TYPES


@pytest.fixture()
def svc() -> AuditService:
    return AuditService(run_id="run_001", actor="system")


class TestWriteAuditRecord:
    def test_write_valid_type(self, svc: AuditService) -> None:
        result = svc.write_audit_record(
            audit_type="decision",
            stage_name="model_fitting",
            run_id="run_001",
            reason="Analyst selected best-fit model.",
        )
        assert result.is_success
        assert "audit_id" in result.data

    def test_invalid_audit_type_fails(self, svc: AuditService) -> None:
        result = svc.write_audit_record(audit_type="unknown_type")
        assert not result.is_success
        assert len(result.errors) > 0

    def test_all_valid_types_work(self, svc: AuditService) -> None:
        for audit_type in AUDIT_TYPES:
            result = svc.write_audit_record(
                audit_type=audit_type,
                stage_name="test_stage",
            )
            assert result.is_success, f"Failed for type: {audit_type}"

    def test_sdk_name_and_function(self, svc: AuditService) -> None:
        result = svc.write_audit_record(audit_type="decision")
        assert result.sdk_name == "auditsdk"
        assert result.function_name == "write_audit_record"

    def test_record_is_chained(self, svc: AuditService) -> None:
        r1 = svc.write_audit_record(audit_type="decision")
        r2 = svc.write_audit_record(audit_type="approval", actor="approver_01")
        a1_id = r1.data["audit_id"]
        a2_id = r2.data["audit_id"]
        record_2 = svc._by_id[a2_id]
        assert record_2.preceding_audit_id == a1_id

    def test_immutable_flag_always_true(self, svc: AuditService) -> None:
        result = svc.write_audit_record(audit_type="signoff", actor="signatory_01")
        audit_id = result.data["audit_id"]
        record = svc._by_id[audit_id]
        assert record.immutable is True


class TestRegisterDecision:
    def test_register_decision(self, svc: AuditService) -> None:
        result = svc.register_decision(
            stage_name="model_fitting",
            run_id="run_001",
            project_id="proj_001",
            reason="Best AUC/KS.",
            decision_payload={"selected_model": "logistic_v3"},
        )
        assert result.is_success
        audit_id = result.data["audit_id"]
        record = svc._by_id[audit_id]
        assert record.audit_type == "decision"
        assert record.decision_payload == {"selected_model": "logistic_v3"}


class TestRegisterApproval:
    def test_register_approval(self, svc: AuditService) -> None:
        result = svc.register_approval(
            stage_name="governance_review",
            approver="governance_officer_01",
            run_id="run_001",
            reason="Policy checks passed.",
        )
        assert result.is_success
        audit_id = result.data["audit_id"]
        record = svc._by_id[audit_id]
        assert record.actor == "governance_officer_01"
        assert record.audit_type == "approval"


class TestRegisterException:
    def test_register_exception(self, svc: AuditService) -> None:
        result = svc.register_exception(
            stage_name="data_quality_check",
            run_id="run_001",
            reason="Sample size too small but approved with waiver.",
            exception_payload={"waiver_ref": "waiver_001"},
        )
        assert result.is_success
        record = svc._by_id[result.data["audit_id"]]
        assert record.exception_payload == {"waiver_ref": "waiver_001"}


class TestRegisterSignoff:
    def test_register_signoff(self, svc: AuditService) -> None:
        result = svc.register_signoff(
            stage_name="final_deployment",
            signatory="cro_officer_01",
            run_id="run_001",
            reason="Model approved for production.",
        )
        assert result.is_success
        record = svc._by_id[result.data["audit_id"]]
        assert record.audit_type == "signoff"


class TestExportAuditBundle:
    def test_export_all(self, svc: AuditService) -> None:
        svc.register_decision("stage_a", run_id="run_001")
        svc.register_approval("stage_b", approver="approver", run_id="run_001")
        result = svc.export_audit_bundle(run_id="run_001")
        assert result.is_success
        bundle = result.data["bundle"]
        assert bundle["total_count"] == 2

    def test_export_filtered_by_run(self, svc: AuditService) -> None:
        svc.register_decision("stage_a", run_id="run_001")
        svc.register_decision("stage_b", run_id="run_002")
        result = svc.export_audit_bundle(run_id="run_001")
        assert result.data["bundle"]["total_count"] == 1

    def test_export_empty_run(self, svc: AuditService) -> None:
        result = svc.export_audit_bundle(run_id="nonexistent_run")
        assert result.is_success
        assert result.data["bundle"]["total_count"] == 0


class TestGetAuditChain:
    def test_chain_reconstruction(self, svc: AuditService) -> None:
        r1 = svc.register_decision("stage_a")
        r2 = svc.register_approval("stage_b", approver="app_01")
        r3 = svc.register_signoff("stage_c", signatory="sig_01")
        leaf_id = r3.data["audit_id"]
        chain_result = svc.get_audit_chain(leaf_id)
        assert chain_result.is_success
        chain = chain_result.data["chain"]
        assert len(chain) == 3
        assert chain[0]["audit_id"] == r1.data["audit_id"]
        assert chain[-1]["audit_id"] == leaf_id

    def test_chain_single_record(self, svc: AuditService) -> None:
        r1 = svc.register_decision("stage_a")
        chain_result = svc.get_audit_chain(r1.data["audit_id"])
        assert chain_result.data["length"] == 1

    def test_chain_unknown_leaf(self, svc: AuditService) -> None:
        chain_result = svc.get_audit_chain("nonexistent_audit_id")
        assert chain_result.is_success
        assert chain_result.data["chain"] == []
