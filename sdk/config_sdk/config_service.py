"""ConfigService — primary config SDK service class.

Responsibilities:
- Load and validate a full RuntimeConfigBundle from disk.
- Resolve effective stage config (stage + role + domain overlays).
- Diff two config bundles.
- Return config version metadata.
- Emit structured audit log entries for every load, override, and fallback.
"""

from __future__ import annotations

import hashlib
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sdk.platform_core.runtime.config_loader import (
    ConfigLoadError,
    RuntimeConfigLoader,
    StageConfigResolver,
)
from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.schemas.base_result import BaseResult
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider
from sdk.platform_core.services.base_service import BaseService

from .models import ConfigDiffEntry, ConfigLoadRequest, ConfigVersionRecord

logger = logging.getLogger(__name__)

# Sentinel to detect "not provided" vs explicit None
_SENTINEL: object = object()


class ConfigService(BaseService):
    """Config SDK service: load, validate, resolve, and diff runtime configs.

    This is the single public service class for config_sdk. All material
    methods return :class:`~platform_core.schemas.BaseResult`.

    Args:
        run_id: Optional run identifier for audit correlation.
        actor: Actor identifier (user or service) performing config operations.

    Examples:
        >>> svc = ConfigService()
        >>> result = svc.load_config(ConfigLoadRequest(base_path="configs/runtime"))
        >>> assert result.is_success
    """

    SDK_NAME: str = "config_sdk"

    def __init__(
        self,
        run_id: Optional[str] = None,
        actor: str = "system",
    ) -> None:
        super().__init__(sdk_name=self.SDK_NAME)
        self._run_id = run_id or IDFactory.run_id()
        self._actor = actor
        self._bundle: Optional[RuntimeConfigBundle] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_config(self, request: ConfigLoadRequest) -> BaseResult:
        """Load and validate a RuntimeConfigBundle from the given base_path.

        Emits a structured audit log entry on load. If validation fails the
        bundle is NOT cached and a failure BaseResult is returned.

        Args:
            request: :class:`ConfigLoadRequest` specifying path and overrides.

        Returns:
            :class:`BaseResult` with ``data["bundle"]`` on success and
            ``data["version"]`` containing :class:`ConfigVersionRecord`.

        Raises:
            Nothing — all errors are caught and returned as BaseResult failures.
        """
        self._log_start("load_config", base_path=request.base_path)
        try:
            loader = RuntimeConfigLoader(base_path=request.base_path)
            bundle = loader.load()
            self._bundle = bundle
            version = self._build_version_record(bundle, request.base_path)
            self._audit_log(
                event="config_load",
                key_path="bundle",
                new_value={"schema_version": version.schema_version, "environment": version.environment},
                source=request.base_path,
                actor=request.actor or self._actor,
                run_id=request.run_id or self._run_id,
            )
            result = self._build_result(
                function_name="load_config",
                status="success",
                message=f"Config loaded from {request.base_path}",
                data={"version": version.to_dict()},
                agent_hint="Config bundle loaded and validated. Proceed with runtime resolution.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="config_load",
            )
        except (ConfigLoadError, Exception) as exc:
            logger.exception("Config load failed: %s", exc)
            result = self._build_result(
                function_name="load_config",
                status="failure",
                message=f"Config load failed: {exc}",
                errors=[str(exc)],
                agent_hint="Config validation failed. Review YAML files and Pydantic models.",
                workflow_hint="no_stage_change",
                audit_hint="write_audit",
                observability_hint="config_load_failed",
            )
        self._log_finish("load_config", result)
        return result

    def validate_config(self, base_path: str) -> BaseResult:
        """Validate config files at the given path without caching the bundle.

        Useful as a dry-run before applying a config change.

        Args:
            base_path: Path to the configs/runtime directory.

        Returns:
            :class:`BaseResult` with ``is_success=True`` if validation passes.
        """
        self._log_start("validate_config", base_path=base_path)
        try:
            loader = RuntimeConfigLoader(base_path=base_path)
            loader.load()
            result = self._build_result(
                function_name="validate_config",
                status="success",
                message="Config validation passed.",
                agent_hint="Config is valid. Safe to reload.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="config_validated",
            )
        except Exception as exc:
            result = self._build_result(
                function_name="validate_config",
                status="failure",
                message=f"Config validation failed: {exc}",
                errors=[str(exc)],
                agent_hint="Config is invalid. Fix errors before reloading.",
                workflow_hint="no_stage_change",
                audit_hint="write_audit",
                observability_hint="config_validation_failed",
            )
        self._log_finish("validate_config", result)
        return result

    def resolve_config(
        self,
        stage_name: str,
        role: str = "developer",
        domain: Optional[str] = None,
    ) -> BaseResult:
        """Resolve the effective config for a stage/role/domain combination.

        Requires a prior successful :meth:`load_config` call.

        Args:
            stage_name: Stage to resolve effective config for.
            role: Actor role for overlay resolution.
            domain: Optional domain for domain overlay resolution.

        Returns:
            :class:`BaseResult` with ``data["effective_config"]`` containing
            the resolved :class:`~platform_core.runtime.config_loader.EffectiveStageConfig`.
        """
        self._log_start("resolve_config", stage_name=stage_name)
        if self._bundle is None:
            result = self._build_result(
                function_name="resolve_config",
                status="failure",
                message="No bundle loaded. Call load_config() first.",
                errors=["Bundle not initialized."],
                agent_hint="Load config before resolving stage config.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="config_resolve_failed",
            )
            self._log_finish("resolve_config", result)
            return result
        try:
            resolver = StageConfigResolver(self._bundle)
            effective = resolver.resolve(stage_name=stage_name, role=role, domain=domain)
            result = self._build_result(
                function_name="resolve_config",
                status="success",
                message=f"Resolved config for stage '{stage_name}'.",
                data={"effective_config": effective.__dict__ if hasattr(effective, "__dict__") else str(effective)},
                agent_hint=f"Effective config resolved for stage={stage_name}, role={role}.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="config_resolved",
            )
        except Exception as exc:
            result = self._build_result(
                function_name="resolve_config",
                status="failure",
                message=f"Config resolution failed for stage '{stage_name}': {exc}",
                errors=[str(exc)],
                agent_hint="Stage config resolution failed. Verify stage_name is registered.",
                workflow_hint="no_stage_change",
                audit_hint="write_audit",
                observability_hint="config_resolve_failed",
            )
        self._log_finish("resolve_config", result)
        return result

    def diff_config(
        self, base_path_a: str, base_path_b: str
    ) -> BaseResult:
        """Compare two config directories and return a list of differences.

        Args:
            base_path_a: Path to the first configs/runtime directory.
            base_path_b: Path to the second configs/runtime directory.

        Returns:
            :class:`BaseResult` with ``data["diffs"]`` containing a list of
            :class:`ConfigDiffEntry` dicts describing each change.
        """
        self._log_start("diff_config", base_path_a=base_path_a, base_path_b=base_path_b)
        try:
            loader_a = RuntimeConfigLoader(base_path=base_path_a)
            loader_b = RuntimeConfigLoader(base_path=base_path_b)
            bundle_a = loader_a.load()
            bundle_b = loader_b.load()
            diffs = self._compute_flat_diff(
                bundle_a.model_dump(), bundle_b.model_dump()
            )
            result = self._build_result(
                function_name="diff_config",
                status="success",
                message=f"Found {len(diffs)} config differences.",
                data={"diffs": [d.to_dict() for d in diffs]},
                agent_hint=f"{len(diffs)} config diffs found between {base_path_a} and {base_path_b}.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="config_diff",
            )
        except Exception as exc:
            result = self._build_result(
                function_name="diff_config",
                status="failure",
                message=f"Config diff failed: {exc}",
                errors=[str(exc)],
                agent_hint="Config diff failed. Verify both paths are valid config roots.",
                workflow_hint="no_stage_change",
                audit_hint="write_audit",
                observability_hint="config_diff_failed",
            )
        self._log_finish("diff_config", result)
        return result

    def get_config_version(self) -> BaseResult:
        """Return the version metadata of the currently loaded bundle.

        Returns:
            :class:`BaseResult` with ``data["version"]`` containing a
            :class:`ConfigVersionRecord` dict, or failure if no bundle loaded.
        """
        self._log_start("get_config_version")
        if self._bundle is None:
            result = self._build_result(
                function_name="get_config_version",
                status="failure",
                message="No bundle loaded. Call load_config() first.",
                errors=["Bundle not initialized."],
                agent_hint="Load config before querying version.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="config_version_failed",
            )
        else:
            version = self._build_version_record(self._bundle, base_path="<cached>")
            result = self._build_result(
                function_name="get_config_version",
                status="success",
                message="Config version retrieved.",
                data={"version": version.to_dict()},
                agent_hint=f"Config version is {version.schema_version} / env={version.environment}.",
                workflow_hint="no_stage_change",
                audit_hint="skip_audit",
                observability_hint="config_version",
            )
        self._log_finish("get_config_version", result)
        return result

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_version_record(
        self, bundle: RuntimeConfigBundle, base_path: str
    ) -> ConfigVersionRecord:
        env_str = str(bundle.runtime_master.runtime.environment)
        schema_ver = bundle.runtime_master.runtime.schema_version
        overlays_applied: List[str] = list(bundle.domain_overlays.keys())
        if bundle.environment_overlay:
            overlays_applied.append(f"env:{env_str}")
        file_hashes = self._hash_config_files(base_path)
        return ConfigVersionRecord(
            schema_version=schema_ver,
            environment=env_str,
            loaded_at=TimeProvider.now(),
            file_hashes=file_hashes,
            overlays_applied=overlays_applied,
        )

    @staticmethod
    def _hash_config_files(base_path: str) -> Dict[str, str]:
        result: Dict[str, str] = {}
        if not os.path.isdir(base_path):
            return result
        for root, _dirs, files in os.walk(base_path):
            for fname in files:
                if fname.endswith(".yaml") or fname.endswith(".yml"):
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, "rb") as fh:
                            digest = hashlib.sha256(fh.read()).hexdigest()[:16]
                        rel = os.path.relpath(fpath, base_path).replace("\\", "/")
                        result[rel] = digest
                    except OSError:
                        pass
        return result

    @staticmethod
    def _compute_flat_diff(
        a: Dict[str, Any], b: Dict[str, Any], prefix: str = ""
    ) -> List[ConfigDiffEntry]:
        diffs: List[ConfigDiffEntry] = []
        all_keys = set(a.keys()) | set(b.keys())
        for key in sorted(all_keys):
            full_key = f"{prefix}.{key}" if prefix else key
            a_val = a.get(key, _SENTINEL)
            b_val = b.get(key, _SENTINEL)
            if a_val is _SENTINEL:
                diffs.append(ConfigDiffEntry(key_path=full_key, new_value=b_val, change_type="added"))
            elif b_val is _SENTINEL:
                diffs.append(ConfigDiffEntry(key_path=full_key, old_value=a_val, change_type="removed"))
            elif isinstance(a_val, dict) and isinstance(b_val, dict):
                diffs.extend(
                    ConfigService._compute_flat_diff(a_val, b_val, prefix=full_key)
                )
            elif a_val != b_val:
                diffs.append(
                    ConfigDiffEntry(
                        key_path=full_key,
                        old_value=a_val,
                        new_value=b_val,
                        change_type="changed",
                    )
                )
        return diffs

    @staticmethod
    def _audit_log(
        event: str,
        key_path: str,
        new_value: Any,
        source: str,
        actor: str,
        run_id: str,
        old_value: Any = None,
        reason: str = "",
    ) -> None:
        """Emit a structured audit log entry for config operations.

        Fields logged per the platform audit logging standard:
        timestamp, actor, run_id, config key path, old/new values, source, reason.
        """
        logger.info(
            "AUDIT config_event",
            extra={
                "timestamp": TimeProvider.now().isoformat(),
                "event": event,
                "actor": actor,
                "run_id": run_id,
                "key_path": key_path,
                "old_value": old_value,
                "new_value": new_value,
                "source": source,
                "reason": reason,
            },
        )
