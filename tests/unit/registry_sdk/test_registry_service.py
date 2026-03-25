"""Unit tests for RegistryService."""

import pytest

from sdk.registry_sdk.models import SDKMetadata, SkillMetadata
from sdk.registry_sdk.registry_service import RegistryService


@pytest.fixture()
def svc() -> RegistryService:
    return RegistryService(run_id="run_test_001", actor="test_actor")


@pytest.fixture()
def svc_with_project(svc: RegistryService) -> RegistryService:
    svc.register_project(
        project_id="proj_001",
        project_name="Test Project",
        domain="scorecard",
        owner="analyst_01",
    )
    return svc


class TestRegisterProject:
    def test_register_success(self, svc: RegistryService) -> None:
        result = svc.register_project(
            project_id="proj_001",
            project_name="Basel Scorecard",
            domain="scorecard",
            owner="analyst_01",
        )
        assert result.is_success
        assert result.data["project_id"] == "proj_001"

    def test_duplicate_project_fails(self, svc: RegistryService) -> None:
        svc.register_project("proj_001", "A", "scorecard", "analyst_01")
        result = svc.register_project("proj_001", "B", "lgd", "analyst_02")
        assert not result.is_success
        assert "Duplicate" in result.errors[0]

    def test_tags_stored(self, svc: RegistryService) -> None:
        svc.register_project(
            "proj_tag",
            "Tagged Project",
            "generic",
            "owner",
            tags={"team": "credit_risk"},
        )
        get_result = svc.get_project("proj_tag")
        assert get_result.data["project"]["tags"]["team"] == "credit_risk"

    def test_sdk_name_and_function(self, svc: RegistryService) -> None:
        result = svc.register_project("p", "N", "generic", "o")
        assert result.sdk_name == "registry_sdk"
        assert result.function_name == "register_project"


class TestGetProject:
    def test_get_existing(self, svc_with_project: RegistryService) -> None:
        result = svc_with_project.get_project("proj_001")
        assert result.is_success
        assert result.data["project"]["project_id"] == "proj_001"

    def test_get_nonexistent(self, svc: RegistryService) -> None:
        result = svc.get_project("nonexistent")
        assert not result.is_success
        assert "not found" in result.message.lower()


class TestRegisterRun:
    def test_register_run_success(self, svc_with_project: RegistryService) -> None:
        result = svc_with_project.register_run(
            run_id="run_001",
            project_id="proj_001",
            actor="analyst_01",
            environment="dev",
            domain="scorecard",
        )
        assert result.is_success
        assert result.data["run_id"] == "run_001"

    def test_run_linked_to_project(self, svc_with_project: RegistryService) -> None:
        svc_with_project.register_run("run_002", "proj_001", "analyst_01")
        proj = svc_with_project.get_project("proj_001")
        assert "run_002" in proj.data["project"]["run_ids"]

    def test_duplicate_run_fails(self, svc_with_project: RegistryService) -> None:
        svc_with_project.register_run("run_001", "proj_001", "analyst_01")
        result = svc_with_project.register_run("run_001", "proj_001", "analyst_01")
        assert not result.is_success

    def test_run_for_unknown_project_fails(self, svc: RegistryService) -> None:
        result = svc.register_run("run_001", "nonexistent_project", "analyst_01")
        assert not result.is_success
        assert "not found" in result.message.lower()

    def test_workflow_hint_contains_stage(self, svc_with_project: RegistryService) -> None:
        result = svc_with_project.register_run("run_003", "proj_001", "analyst_01")
        assert "session_bootstrap" in result.workflow_hint


class TestGetRun:
    def test_get_existing_run(self, svc_with_project: RegistryService) -> None:
        svc_with_project.register_run("run_001", "proj_001", "analyst_01")
        result = svc_with_project.get_run("run_001")
        assert result.is_success
        assert result.data["run"]["project_id"] == "proj_001"

    def test_get_missing_run(self, svc: RegistryService) -> None:
        result = svc.get_run("nonexistent_run")
        assert not result.is_success


class TestSkillSDKMetadata:
    def test_register_skill(self, svc: RegistryService) -> None:
        meta = SkillMetadata(
            skill_name="model-lifecycle-orchestrator",
            skill_category="platform",
            description="Top-level orchestrator.",
            applicable_stages=["session_bootstrap"],
        )
        result = svc.register_skill_metadata(meta)
        assert result.is_success
        assert result.data["skill_name"] == "model-lifecycle-orchestrator"

    def test_register_sdk(self, svc: RegistryService) -> None:
        meta = SDKMetadata(
            sdk_name="artifactsdk",
            sdk_layer=2,
            primary_service_class="sdk.artifactsdk.ArtifactService",
            public_methods=["write_artifact", "read_artifact"],
        )
        result = svc.register_sdk_metadata(meta)
        assert result.is_success


class TestSearchRegistry:
    def test_search_all_projects(self, svc_with_project: RegistryService) -> None:
        result = svc_with_project.search_registry("project")
        assert result.is_success
        assert result.data["count"] == 1

    def test_search_with_filter(self, svc: RegistryService) -> None:
        svc.register_project("p1", "A", "scorecard", "owner1")
        svc.register_project("p2", "B", "lgd", "owner2")
        result = svc.search_registry("project", filters={"domain": "lgd"})
        assert result.is_success
        assert result.data["count"] == 1
        assert result.data["results"][0]["domain"] == "lgd"

    def test_search_empty_store(self, svc: RegistryService) -> None:
        result = svc.search_registry("run")
        assert result.is_success
        assert result.data["count"] == 0

    def test_search_unknown_entity_type(self, svc: RegistryService) -> None:
        result = svc.search_registry("unknown_entity")
        assert not result.is_success
        assert "entity_type" in result.errors[0].lower()
