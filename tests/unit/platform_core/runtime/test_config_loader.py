"""Unit tests for RuntimeConfigLoader and StageConfigResolver."""

import os
import textwrap
from pathlib import Path

import pytest
import yaml

from sdk.platform_core.runtime.config_loader import (
    ConfigLoadError,
    RuntimeConfigLoader,
)


CONFIGS_ROOT = Path(__file__).parents[4] / "configs" / "runtime"


class TestRuntimeConfigLoaderIntegration:
    """Integration tests that load the actual runtime YAML pack."""

    @pytest.mark.skipif(
        not CONFIGS_ROOT.exists(),
        reason="configs/runtime directory not found",
    )
    def test_load_bundle_succeeds(self) -> None:
        loader = RuntimeConfigLoader(base_path=str(CONFIGS_ROOT))
        bundle = loader.load()
        assert bundle is not None
        assert bundle.stage_registry is not None
        assert len(bundle.stage_registry.stages) > 0

    @pytest.mark.skipif(
        not CONFIGS_ROOT.exists(),
        reason="configs/runtime directory not found",
    )
    def test_all_stages_have_class(self) -> None:
        loader = RuntimeConfigLoader(base_path=str(CONFIGS_ROOT))
        bundle = loader.load()
        for stage_name, stage in bundle.stage_registry.stages.items():
            assert stage.stage_class is not None, f"{stage_name} missing stage_class"

    @pytest.mark.skipif(
        not CONFIGS_ROOT.exists(),
        reason="configs/runtime directory not found",
    )
    def test_tool_matrix_stages_in_registry(self) -> None:
        loader = RuntimeConfigLoader(base_path=str(CONFIGS_ROOT))
        bundle = loader.load()
        registry_stages = set(bundle.stage_registry.stages.keys())
        for stage_name in bundle.stage_tool_matrix.matrix.keys():
            assert stage_name in registry_stages, (
                f"Stage '{stage_name}' in tool matrix not in registry"
            )


class TestConfigLoadError:
    def test_missing_file_raises(self, tmp_path: Path) -> None:
        loader = RuntimeConfigLoader(base_path=str(tmp_path / "nonexistent"))
        with pytest.raises((ConfigLoadError, Exception)):
            loader.load()

    def test_invalid_yaml_raises(self, tmp_path: Path) -> None:
        bad_yaml = tmp_path / "runtime_master.yaml"
        bad_yaml.write_text("runtime:\n  environment: [invalid: yaml: structure:")
        loader = RuntimeConfigLoader(base_path=str(tmp_path))
        with pytest.raises((ConfigLoadError, Exception)):
            loader.load()

    def test_valid_schema_version_in_yaml(self, tmp_path: Path) -> None:
        """A minimal runtime_master.yaml with invalid semver must fail."""
        master = textwrap.dedent("""\
            runtime:
              environment: dev
              schema_version: "invalid_version"
              runtime_mode: development
        """)
        (tmp_path / "runtime_master.yaml").write_text(master)
        loader = RuntimeConfigLoader(base_path=str(tmp_path))
        with pytest.raises(Exception):
            loader.load()
