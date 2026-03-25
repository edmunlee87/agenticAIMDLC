"""Unit tests for ConfigService."""

from pathlib import Path

import pytest

from sdk.config_sdk.config_service import ConfigService
from sdk.config_sdk.models import ConfigLoadRequest, ConfigVersionRecord

CONFIGS_ROOT = str(Path(__file__).parents[3] / "configs" / "runtime")


class TestConfigServiceLoadConfig:
    def test_load_success(self) -> None:
        svc = ConfigService()
        result = svc.load_config(ConfigLoadRequest(base_path=CONFIGS_ROOT))
        assert result.is_success
        assert result.data is not None
        assert "version" in result.data

    def test_load_populates_version(self) -> None:
        svc = ConfigService()
        result = svc.load_config(ConfigLoadRequest(base_path=CONFIGS_ROOT))
        version = result.data["version"]
        assert version["schema_version"] == "1.0.0"
        assert version["environment"] == "dev"

    def test_load_bad_path_returns_failure(self) -> None:
        svc = ConfigService()
        result = svc.load_config(ConfigLoadRequest(base_path="/nonexistent/path"))
        assert not result.is_success
        assert len(result.errors) > 0
        assert result.audit_hint == "write_audit"

    def test_agent_hint_populated_on_success(self) -> None:
        svc = ConfigService()
        result = svc.load_config(ConfigLoadRequest(base_path=CONFIGS_ROOT))
        assert result.agent_hint != ""

    def test_sdk_name(self) -> None:
        svc = ConfigService()
        result = svc.load_config(ConfigLoadRequest(base_path=CONFIGS_ROOT))
        assert result.sdk_name == "config_sdk"
        assert result.function_name == "load_config"

    def test_file_hashes_populated(self) -> None:
        svc = ConfigService()
        result = svc.load_config(ConfigLoadRequest(base_path=CONFIGS_ROOT))
        hashes = result.data["version"]["file_hashes"]
        assert len(hashes) > 0
        for key, val in hashes.items():
            assert key.endswith(".yaml") or key.endswith(".yml")
            assert len(val) == 16  # sha256 hex[:16]


class TestConfigServiceValidateConfig:
    def test_validate_success(self) -> None:
        svc = ConfigService()
        result = svc.validate_config(CONFIGS_ROOT)
        assert result.is_success

    def test_validate_bad_path_fails(self) -> None:
        svc = ConfigService()
        result = svc.validate_config("/not/a/real/path")
        assert not result.is_success
        assert result.errors


class TestConfigServiceResolveConfig:
    def test_resolve_without_load_fails(self) -> None:
        svc = ConfigService()
        result = svc.resolve_config("session_bootstrap")
        assert not result.is_success
        assert "load_config" in result.message

    def test_resolve_after_load_succeeds(self) -> None:
        svc = ConfigService()
        svc.load_config(ConfigLoadRequest(base_path=CONFIGS_ROOT))
        result = svc.resolve_config("session_bootstrap", role="developer")
        assert result.is_success

    def test_resolve_unknown_stage_fails(self) -> None:
        svc = ConfigService()
        svc.load_config(ConfigLoadRequest(base_path=CONFIGS_ROOT))
        result = svc.resolve_config("stage_that_does_not_exist")
        assert not result.is_success


class TestConfigServiceGetConfigVersion:
    def test_version_without_load_fails(self) -> None:
        svc = ConfigService()
        result = svc.get_config_version()
        assert not result.is_success

    def test_version_after_load_succeeds(self) -> None:
        svc = ConfigService()
        svc.load_config(ConfigLoadRequest(base_path=CONFIGS_ROOT))
        result = svc.get_config_version()
        assert result.is_success
        assert "version" in result.data


class TestConfigServiceDiffConfig:
    def test_diff_same_path_zero_changes(self) -> None:
        svc = ConfigService()
        result = svc.diff_config(CONFIGS_ROOT, CONFIGS_ROOT)
        assert result.is_success
        assert result.data["diffs"] == []

    def test_diff_invalid_path_fails(self) -> None:
        svc = ConfigService()
        result = svc.diff_config(CONFIGS_ROOT, "/nonexistent")
        assert not result.is_success
