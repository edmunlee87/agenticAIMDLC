"""Unit tests for ArtifactService."""

import pytest

from sdk.artifactsdk.artifact_service import ArtifactService
from sdk.artifactsdk.models import ChecksumRecord
from sdk.artifactsdk.storage_adapter import ChecksumManager, InMemoryArtifactStore


@pytest.fixture()
def svc() -> ArtifactService:
    return ArtifactService(run_id="run_001", project_id="proj_001", actor="analyst")


def _register_one(svc: ArtifactService, **kwargs) -> str:
    """Helper: register an artifact and return its artifact_id."""
    defaults = dict(
        artifact_type="model_object",
        artifact_name="logistic_v1",
        stage_name="model_fitting",
    )
    defaults.update(kwargs)
    result = svc.register_artifact(**defaults)
    assert result.is_success
    return result.data["artifact_id"]


class TestRegisterArtifact:
    def test_basic_registration(self, svc: ArtifactService) -> None:
        result = svc.register_artifact(
            artifact_type="binning_summary",
            artifact_name="var_age_bins",
            stage_name="coarse_classing",
            uri_or_path="/artifacts/bins.parquet",
        )
        assert result.is_success
        assert "artifact_id" in result.data
        assert result.data["artifact_type"] == "binning_summary"
        assert result.data["version"] == "1.0"
        assert result.sdk_name == "artifactsdk"
        assert result.function_name == "register_artifact"

    def test_artifact_id_in_artifacts_created(self, svc: ArtifactService) -> None:
        result = svc.register_artifact(
            artifact_type="woe_table",
            artifact_name="woe_v1",
            stage_name="coarse_classing",
        )
        assert result.data["artifact_id"] in result.artifacts_created

    def test_auto_checksum_from_raw_bytes(self, svc: ArtifactService) -> None:
        payload = b"model_binary_payload"
        result = svc.register_artifact(
            artifact_type="model_object",
            artifact_name="logistic_v1",
            stage_name="model_fitting",
            raw_bytes=payload,
        )
        assert result.is_success
        artifact_id = result.data["artifact_id"]
        record = svc._by_id[artifact_id]
        assert record.checksum is not None
        assert record.checksum.algorithm == "SHA-256"
        expected = ChecksumManager.compute_checksum(payload).value
        assert record.checksum.value == expected

    def test_explicit_checksum(self, svc: ArtifactService) -> None:
        cs = ChecksumRecord(value="abc123deadbeef", algorithm="SHA-256")
        result = svc.register_artifact(
            artifact_type="score_output",
            artifact_name="scores_v1",
            stage_name="scoring",
            checksum=cs,
        )
        record = svc._by_id[result.data["artifact_id"]]
        assert record.checksum.value == "abc123deadbeef"

    def test_missing_required_fields_fails(self, svc: ArtifactService) -> None:
        result = svc.register_artifact(
            artifact_type="",
            artifact_name="",
            stage_name="",
        )
        assert not result.is_success
        assert len(result.errors) > 0

    def test_version_increments_per_type(self, svc: ArtifactService) -> None:
        r1 = svc.register_artifact(
            artifact_type="model_object",
            artifact_name="logistic_v1",
            stage_name="model_fitting",
        )
        r2 = svc.register_artifact(
            artifact_type="model_object",
            artifact_name="logistic_v2",
            stage_name="model_fitting",
        )
        assert r1.data["version"] == "1.0"
        assert r2.data["version"] == "2.0"

    def test_lineage_parent_ids_stored(self, svc: ArtifactService) -> None:
        parent_id = _register_one(svc, artifact_type="raw_data")
        result = svc.register_artifact(
            artifact_type="binning_summary",
            artifact_name="bins_v1",
            stage_name="coarse_classing",
            lineage_parent_ids=[parent_id],
        )
        child_id = result.data["artifact_id"]
        links = [lnk for lnk in svc._lineage_links if lnk.child_id == child_id]
        assert len(links) == 1
        assert links[0].parent_id == parent_id

    def test_storage_write_failure_returns_failure(self) -> None:
        failing_store = InMemoryArtifactStore(simulate_write_failure=True)
        svc = ArtifactService(storage_adapter=failing_store)
        result = svc.register_artifact(
            artifact_type="model_object",
            artifact_name="logistic_v1",
            stage_name="model_fitting",
        )
        assert not result.is_success
        assert len(result.errors) > 0


class TestGetArtifact:
    def test_get_registered_artifact(self, svc: ArtifactService) -> None:
        artifact_id = _register_one(svc)
        result = svc.get_artifact(artifact_id)
        assert result.is_success
        assert result.data["artifact"]["artifact_id"] == artifact_id

    def test_get_unknown_artifact_fails(self, svc: ArtifactService) -> None:
        result = svc.get_artifact("art_nonexistent")
        assert not result.is_success
        assert len(result.errors) > 0


class TestLocateArtifact:
    def test_locate_by_type(self, svc: ArtifactService) -> None:
        _register_one(svc, artifact_type="model_object")
        _register_one(svc, artifact_type="binning_summary", stage_name="coarse_classing")
        result = svc.locate_artifact(artifact_type="model_object")
        assert result.is_success
        assert result.data["count"] == 1

    def test_locate_by_stage(self, svc: ArtifactService) -> None:
        _register_one(svc, stage_name="scoring")
        _register_one(svc, stage_name="model_fitting")
        result = svc.locate_artifact(stage_name="scoring")
        assert result.data["count"] == 1

    def test_locate_all(self, svc: ArtifactService) -> None:
        _register_one(svc)
        _register_one(svc, artifact_type="score_output")
        result = svc.locate_artifact()
        assert result.data["count"] == 2

    def test_locate_with_run_id_filter(self, svc: ArtifactService) -> None:
        _register_one(svc, run_id="run_001")
        _register_one(svc, run_id="run_002")
        result = svc.locate_artifact(run_id="run_002")
        assert result.data["count"] == 1

    def test_locate_returns_empty_list_for_no_match(self, svc: ArtifactService) -> None:
        result = svc.locate_artifact(artifact_type="nonexistent_type")
        assert result.is_success
        assert result.data["count"] == 0


class TestValidateArtifact:
    def test_validate_with_matching_bytes(self, svc: ArtifactService) -> None:
        payload = b"artifact_bytes"
        result = svc.register_artifact(
            artifact_type="model_object",
            artifact_name="model_v1",
            stage_name="fitting",
            raw_bytes=payload,
        )
        artifact_id = result.data["artifact_id"]
        val = svc.validate_artifact(artifact_id, raw_bytes=payload)
        assert val.is_success
        assert val.data["checksum_valid"] is True

    def test_validate_with_wrong_bytes_fails(self, svc: ArtifactService) -> None:
        payload = b"artifact_bytes"
        result = svc.register_artifact(
            artifact_type="model_object",
            artifact_name="model_v1",
            stage_name="fitting",
            raw_bytes=payload,
        )
        artifact_id = result.data["artifact_id"]
        val = svc.validate_artifact(artifact_id, raw_bytes=b"tampered_bytes")
        assert not val.is_success
        assert val.data["checksum_valid"] is False

    def test_validate_no_checksum_returns_warning(self, svc: ArtifactService) -> None:
        artifact_id = _register_one(svc)
        val = svc.validate_artifact(artifact_id)
        assert val.status == "warning"
        assert len(val.warnings) > 0

    def test_validate_unknown_id_fails(self, svc: ArtifactService) -> None:
        val = svc.validate_artifact("art_unknown")
        assert not val.is_success

    def test_validate_with_checksum_no_bytes(self, svc: ArtifactService) -> None:
        cs = ChecksumRecord(value="abc123", algorithm="SHA-256")
        result = svc.register_artifact(
            artifact_type="model_object",
            artifact_name="model_v1",
            stage_name="fitting",
            checksum=cs,
        )
        artifact_id = result.data["artifact_id"]
        val = svc.validate_artifact(artifact_id)
        assert val.is_success
        assert val.data["checksum_valid"] is True


class TestBuildArtifactManifest:
    def test_build_valid_manifest(self, svc: ArtifactService) -> None:
        a1 = _register_one(svc, artifact_type="model_object")
        a2 = _register_one(svc, artifact_type="score_output")
        result = svc.build_artifact_manifest(
            artifact_ids=[a1, a2],
            manifest_type="committee_pack",
        )
        assert result.is_success
        bundle = result.data["manifest"]
        assert bundle["artifact_count"] == 2
        assert bundle["manifest_type"] == "committee_pack"

    def test_build_manifest_with_missing_id_fails(self, svc: ArtifactService) -> None:
        a1 = _register_one(svc)
        result = svc.build_artifact_manifest(
            artifact_ids=[a1, "art_nonexistent"],
            manifest_type="committee_pack",
        )
        assert not result.is_success
        assert len(result.errors) > 0

    def test_empty_manifest_is_valid(self, svc: ArtifactService) -> None:
        result = svc.build_artifact_manifest(artifact_ids=[], manifest_type="empty_pack")
        assert result.is_success
        assert result.data["manifest"]["artifact_count"] == 0


class TestLinkArtifactLineage:
    def test_link_explicit_lineage(self, svc: ArtifactService) -> None:
        parent_id = _register_one(svc, artifact_type="raw_data")
        child_id = _register_one(svc, artifact_type="binning_summary")
        result = svc.link_artifact_lineage(
            parent_ids=[parent_id], child_id=child_id, lineage_type="derived"
        )
        assert result.is_success
        assert result.data["links_added"] == 1

    def test_duplicate_link_skipped(self, svc: ArtifactService) -> None:
        parent_id = _register_one(svc, artifact_type="raw_data")
        child_id = _register_one(svc, artifact_type="binning_summary")
        svc.link_artifact_lineage([parent_id], child_id)
        result = svc.link_artifact_lineage([parent_id], child_id)
        assert result.is_success
        assert result.data["links_added"] == 0

    def test_unknown_child_fails(self, svc: ArtifactService) -> None:
        parent_id = _register_one(svc)
        result = svc.link_artifact_lineage([parent_id], "art_unknown_child")
        assert not result.is_success

    def test_unknown_parent_warns(self, svc: ArtifactService) -> None:
        child_id = _register_one(svc)
        result = svc.link_artifact_lineage(["art_unknown_parent"], child_id)
        assert result.is_success
        assert result.data["links_added"] == 0
        assert len(result.warnings) > 0


class TestGetArtifactLineage:
    def test_lineage_retrieval(self, svc: ArtifactService) -> None:
        parent_id = _register_one(svc, artifact_type="raw_data")
        child_id = _register_one(
            svc, artifact_type="binning_summary", lineage_parent_ids=[parent_id]
        )
        result = svc.get_artifact_lineage(parent_id)
        assert result.is_success
        assert len(result.data["as_parent"]) == 1
        assert result.data["as_parent"][0]["child_id"] == child_id

    def test_lineage_empty_for_isolated_artifact(self, svc: ArtifactService) -> None:
        artifact_id = _register_one(svc)
        result = svc.get_artifact_lineage(artifact_id)
        assert result.is_success
        assert result.data["as_parent"] == []
        assert result.data["as_child"] == []


class TestChecksumManager:
    def test_compute_checksum_stable(self) -> None:
        cs1 = ChecksumManager.compute_checksum(b"hello")
        cs2 = ChecksumManager.compute_checksum(b"hello")
        assert cs1.value == cs2.value

    def test_verify_checksum_match(self) -> None:
        cs = ChecksumManager.compute_checksum(b"data")
        assert ChecksumManager.verify_checksum(b"data", cs) is True

    def test_verify_checksum_mismatch(self) -> None:
        cs = ChecksumManager.compute_checksum(b"data")
        assert ChecksumManager.verify_checksum(b"different", cs) is False

    def test_unsupported_algorithm_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported checksum algorithm"):
            ChecksumManager.compute_checksum(b"data", algorithm="MD5")
