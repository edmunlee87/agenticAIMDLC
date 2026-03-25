"""RuntimeConfigLoader -- loads, merges, and validates the full runtime config pack.

Loads all YAML base files from ``configs/runtime/``, applies active overlays
(environment, role, domain), deep-merges them, and validates the result into
a :class:`~platform_core.runtime.config_models.bundle.RuntimeConfigBundle`.

Design:
- Config load is logged as a structured audit entry (config_load event).
- Overlays are applied in order: environment -> domain -> role.
- Each merge step logs which keys changed (config_override events).
- Validation errors fail fast with a clear message including the file path.
"""

from __future__ import annotations

import copy
import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.runtime.config_models.domain import DomainsConfig
from platform_core.runtime.config_models.environment import EnvironmentConfig
from platform_core.runtime.config_models.governance import GovernanceConfig
from platform_core.runtime.config_models.roles import RolesConfig
from platform_core.runtime.config_models.routes import RoutesConfig
from platform_core.runtime.config_models.stages import StagesConfig
from platform_core.runtime.config_models.tool_groups import ToolGroupConfig
from platform_core.runtime.config_models.ui import UIConfig

logger = logging.getLogger(__name__)

# Names of the seven base YAML files that must exist in the config root.
_BASE_FILES: dict[str, str] = {
    "tool_groups": "tool_groups.yaml",
    "roles": "roles.yaml",
    "stages": "stages.yaml",
    "routes": "routes.yaml",
    "governance": "governance.yaml",
    "ui": "ui.yaml",
    "domain": "domain.yaml",
    "environment": "environment.yaml",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file and return a plain dict.

    Args:
        path: Absolute path to the YAML file.

    Returns:
        Parsed YAML content as a dict.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file content is not a YAML mapping.
    """
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(content, dict):
        raise ValueError(f"Config file must be a YAML mapping, got {type(content)}: {path}")
    return content


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge ``override`` into a copy of ``base``.

    Scalar values in ``override`` replace those in ``base``; nested dicts are
    merged recursively. Lists are replaced (not concatenated) by the override.

    Args:
        base: Base configuration dict.
        override: Override values to merge in.

    Returns:
        New merged dict without modifying the inputs.
    """
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _dict_checksum(data: dict[str, Any]) -> str:
    """Compute a stable SHA-256 checksum of a config dict."""
    serialized = json.dumps(data, sort_keys=True, default=str).encode()
    return hashlib.sha256(serialized).hexdigest()[:16]


class RuntimeConfigLoader:
    """Loads, overlays, and validates the MDLC runtime configuration pack.

    Usage::

        loader = RuntimeConfigLoader(config_root=Path("configs/runtime"))
        bundle = loader.load(environment="production", active_domain="credit_risk")

    Args:
        config_root: Root directory containing the base YAML files.
            Defaults to ``configs/runtime`` relative to the current working directory.

    Raises:
        FileNotFoundError: If config_root or a required base file is missing.
        ValidationError: If any config file fails Pydantic validation.
        ValueError: If a YAML file is not a valid mapping.
    """

    def __init__(self, config_root: Path | None = None) -> None:
        self._config_root: Path = config_root or (Path.cwd() / "configs" / "runtime")
        self._cache: dict[str, RuntimeConfigBundle] = {}

    def load(
        self,
        environment: str | None = None,
        active_domain: str | None = None,
        active_role: str | None = None,
        force_reload: bool = False,
    ) -> RuntimeConfigBundle:
        """Load and return the validated RuntimeConfigBundle.

        Applies overlays in order: environment -> domain -> role.

        Args:
            environment: Active environment name (e.g. ``"production"``).
                If None, the value from ``environment.yaml`` is used.
            active_domain: Active domain ID. If provided, loads the corresponding
                domain overlay from ``domain_overlays/{active_domain}.yaml`` (if present).
            active_role: Active role ID. If provided, loads the corresponding
                role overlay from ``role_overlays/{active_role}.yaml`` (if present).
            force_reload: Bypass cache and reload from disk.

        Returns:
            Fully validated :class:`RuntimeConfigBundle`.

        Raises:
            FileNotFoundError: Required base config file missing.
            ValidationError: Config data fails schema validation.
        """
        cache_key = f"{environment}|{active_domain}|{active_role}"
        if not force_reload and cache_key in self._cache:
            logger.debug(
                "config.cache_hit",
                extra={"cache_key": cache_key},
            )
            return self._cache[cache_key]

        start = time.monotonic()
        raw = self._load_base_files()
        raw = self._apply_environment_overlay(raw, environment)
        raw = self._apply_domain_overlay(raw, active_domain)
        raw = self._apply_role_overlay(raw, active_role)

        bundle = self._build_bundle(raw)
        elapsed_ms = round((time.monotonic() - start) * 1000)

        logger.info(
            "config.loaded",
            extra={
                "environment": environment,
                "active_domain": active_domain,
                "active_role": active_role,
                "elapsed_ms": elapsed_ms,
                "bundle_checksum": _dict_checksum(raw),
            },
        )

        self._cache[cache_key] = bundle
        return bundle

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_base_files(self) -> dict[str, dict[str, Any]]:
        """Load all base YAML files into a keyed dict."""
        raw: dict[str, dict[str, Any]] = {}
        for key, filename in _BASE_FILES.items():
            path = self._config_root / filename
            data = _load_yaml(path)
            raw[key] = data
            logger.debug(
                "config.file_loaded",
                extra={"key": key, "path": str(path), "source": "file"},
            )
        return raw

    def _apply_environment_overlay(
        self,
        raw: dict[str, dict[str, Any]],
        environment: str | None,
    ) -> dict[str, dict[str, Any]]:
        """Merge environment overlay if it exists."""
        if not environment:
            return raw
        overlay_path = (
            self._config_root / "environment_overlays" / f"{environment}.yaml"
        )
        if not overlay_path.exists():
            logger.debug(
                "config.overlay_missing",
                extra={"overlay_type": "environment", "environment": environment},
            )
            return raw
        overlay_data = _load_yaml(overlay_path)
        merged = dict(raw)
        merged["environment"] = _deep_merge(raw.get("environment", {}), overlay_data)
        logger.info(
            "config.overlay_applied",
            extra={"overlay_type": "environment", "environment": environment},
        )
        return merged

    def _apply_domain_overlay(
        self,
        raw: dict[str, dict[str, Any]],
        active_domain: str | None,
    ) -> dict[str, dict[str, Any]]:
        """Merge domain overlay if it exists."""
        if not active_domain:
            return raw
        overlay_path = (
            self._config_root / "domain_overlays" / f"{active_domain}.yaml"
        )
        if not overlay_path.exists():
            return raw
        overlay_data = _load_yaml(overlay_path)
        if not overlay_data:
            return raw
        merged = dict(raw)
        # Domain overlays can patch any top-level key.
        for key, value in overlay_data.items():
            if isinstance(value, dict):
                merged[key] = _deep_merge(raw.get(key, {}), value)
            else:
                merged[key] = value
        logger.info(
            "config.overlay_applied",
            extra={"overlay_type": "domain", "active_domain": active_domain},
        )
        return merged

    def _apply_role_overlay(
        self,
        raw: dict[str, dict[str, Any]],
        active_role: str | None,
    ) -> dict[str, dict[str, Any]]:
        """Merge role overlay if it exists."""
        if not active_role:
            return raw
        overlay_path = (
            self._config_root / "role_overlays" / f"{active_role}.yaml"
        )
        if not overlay_path.exists():
            return raw
        overlay_data = _load_yaml(overlay_path)
        if not overlay_data:
            return raw
        merged = dict(raw)
        for key, value in overlay_data.items():
            if isinstance(value, dict):
                merged[key] = _deep_merge(raw.get(key, {}), value)
        logger.info(
            "config.overlay_applied",
            extra={"overlay_type": "role", "active_role": active_role},
        )
        return merged

    def _build_bundle(self, raw: dict[str, dict[str, Any]]) -> RuntimeConfigBundle:
        """Validate all raw dicts and assemble the RuntimeConfigBundle."""
        try:
            tool_groups_data = raw.get("tool_groups", {})
            tool_groups = {
                k: ToolGroupConfig.model_validate(v)
                for k, v in tool_groups_data.get("groups", {}).items()
            }
            roles = RolesConfig.model_validate(raw.get("roles", {}))
            stages = StagesConfig.model_validate(raw.get("stages", {}))
            routes = RoutesConfig.model_validate(raw.get("routes", {}))
            governance = GovernanceConfig.model_validate(raw.get("governance", {}))
            ui = UIConfig.model_validate(raw.get("ui", {}))
            domains = DomainsConfig.model_validate(raw.get("domain", {}))
            environment = EnvironmentConfig.model_validate(raw.get("environment", {}))

            return RuntimeConfigBundle(
                roles=roles,
                stages=stages,
                routes=routes,
                governance=governance,
                tool_groups=tool_groups,
                ui=ui,
                domains=domains,
                environment=environment,
            )
        except ValidationError as exc:
            logger.error("config.validation_failed", extra={"error": str(exc)})
            raise
