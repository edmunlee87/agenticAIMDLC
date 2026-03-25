"""ConfigService -- facade for loading, caching, and serving runtime config.

Wraps :class:`~platform_core.runtime.config_loader.RuntimeConfigLoader` with
a service interface that:
- Records structured :class:`~config_sdk.models.ConfigLoadEvent` entries for
  every load and override.
- Exposes a point-in-time :class:`~config_sdk.models.ConfigSnapshot` for auditing.
- Supports runtime key-level overrides with source/reason tracking.
- Provides a ``health_check`` verifying the config files are loadable.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from platform_contracts.results import BaseResult, ResultFactory
from platform_core.runtime.config_loader import RuntimeConfigLoader
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.runtime.config_models.enums import ConfigLoadSource
from platform_core.services.base import BaseService
from platform_core.utils.id_factory import IDFactory, id_factory
from platform_core.utils.time_provider import TimeProvider, time_provider

from config_sdk.models import ConfigLoadEvent, ConfigSnapshot

logger = logging.getLogger(__name__)


class ConfigService(BaseService):
    """Service facade for the MDLC runtime configuration pack.

    Loads the :class:`~platform_core.runtime.config_models.bundle.RuntimeConfigBundle`
    via :class:`~platform_core.runtime.config_loader.RuntimeConfigLoader`, records
    provenance events, and serves config to all other SDKs.

    Args:
        config_root: Path to ``configs/runtime/`` directory.
        bundle: Pre-built bundle (optional; if omitted, loaded from ``config_root``).
        id_factory_: Injectable :class:`IDFactory`.
        time_provider_: Injectable :class:`TimeProvider`.

    Examples:
        >>> svc = ConfigService(config_root=Path("configs/runtime"))
        >>> result = svc.load(environment="production", active_domain="credit_risk")
        >>> bundle = result.unwrap()
    """

    def __init__(
        self,
        config_root: Path | None = None,
        bundle: RuntimeConfigBundle | None = None,
        id_factory_: IDFactory | None = None,
        time_provider_: TimeProvider | None = None,
    ) -> None:
        # ConfigService is special: it is the first service instantiated so it
        # bootstraps without an existing bundle. Pass an empty bundle if needed.
        effective_bundle = bundle or RuntimeConfigBundle()
        super().__init__(
            bundle=effective_bundle,
            id_factory_=id_factory_,
            time_provider_=time_provider_,
        )
        self._config_root = config_root or (Path.cwd() / "configs" / "runtime")
        self._loader = RuntimeConfigLoader(config_root=self._config_root)
        self._load_events: list[ConfigLoadEvent] = []
        self._current_snapshot: ConfigSnapshot | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(
        self,
        environment: str | None = None,
        active_domain: str | None = None,
        active_role: str | None = None,
        run_id: str = "",
        force_reload: bool = False,
    ) -> BaseResult[RuntimeConfigBundle]:
        """Load and return the validated RuntimeConfigBundle.

        Records a :class:`ConfigLoadEvent` for every top-level config section loaded.

        Args:
            environment: Target environment (e.g. ``"production"``).
            active_domain: Active domain ID for overlay application.
            active_role: Active role ID for overlay application.
            run_id: Current run ID for audit event correlation.
            force_reload: Bypass the loader cache.

        Returns:
            :class:`BaseResult` containing the :class:`RuntimeConfigBundle`.
        """
        try:
            bundle = self._loader.load(
                environment=environment,
                active_domain=active_domain,
                active_role=active_role,
                force_reload=force_reload,
            )
        except (FileNotFoundError, ValidationError) as exc:
            self._logger.error("config_service.load_failed", extra={"error": str(exc)})
            return ResultFactory.fail(
                "ERR_CONFIG_LOAD_FAILED",
                f"Failed to load runtime config: {exc}",
                detail=str(exc),
            )

        # Record a single load event summarising this cycle.
        event = ConfigLoadEvent(
            event_id=self._id_factory.audit_id(),
            timestamp=self._time_provider.now(),
            run_id=run_id,
            actor="config_service",
            config_key_path="runtime_config_bundle",
            new_value={"environment": environment, "domain": active_domain, "role": active_role},
            source=ConfigLoadSource.FILE,
        )
        self._load_events.append(event)
        self._logger.info(
            "config_service.loaded",
            extra={
                "environment": environment,
                "active_domain": active_domain,
                "n_stages": len(bundle.stages.stages),
                "n_roles": len(bundle.roles.roles),
            },
        )

        # Rebuild snapshot.
        self._current_snapshot = ConfigSnapshot(
            snapshot_id=self._id_factory.audit_id(),
            taken_at=self._time_provider.now(),
            environment=environment or "",
            active_domain=active_domain or "",
            active_role=active_role or "",
            bundle_checksum=self._bundle_checksum(bundle),
            load_events=list(self._load_events),
        )

        # Keep the service's internal bundle in sync.
        object.__setattr__(self, "_bundle", bundle)
        return ResultFactory.ok(bundle)

    def get_bundle(self) -> BaseResult[RuntimeConfigBundle]:
        """Return the currently loaded bundle.

        Returns:
            :class:`BaseResult` with the bundle, or failure if not yet loaded.
        """
        if self._bundle is None or not self._bundle.stages.stages:
            return ResultFactory.fail(
                "ERR_CONFIG_NOT_LOADED",
                "Config has not been loaded yet. Call load() first.",
            )
        return ResultFactory.ok(self._bundle)

    def get_snapshot(self) -> BaseResult[ConfigSnapshot]:
        """Return the most recent config snapshot.

        Returns:
            :class:`BaseResult` containing the :class:`ConfigSnapshot`.
        """
        if self._current_snapshot is None:
            return ResultFactory.fail(
                "ERR_NO_SNAPSHOT",
                "No config snapshot available. Call load() first.",
            )
        return ResultFactory.ok(self._current_snapshot)

    def record_override(
        self,
        config_key_path: str,
        old_value: Any,
        new_value: Any,
        source: ConfigLoadSource = ConfigLoadSource.CLI,
        actor: str = "system",
        run_id: str = "",
        reason: str = "",
    ) -> None:
        """Record a runtime key-level override without reloading.

        This does NOT mutate the bundle -- it records that an external process
        has applied an override, for audit traceability. Actual override of
        the live bundle must be handled by the caller.

        Args:
            config_key_path: Dot-separated config key path.
            old_value: Value before the override.
            new_value: New override value.
            source: Override source.
            actor: Actor applying the override.
            run_id: Run ID for correlation.
            reason: Human-readable reason.
        """
        event = ConfigLoadEvent(
            event_id=self._id_factory.audit_id(),
            timestamp=self._time_provider.now(),
            run_id=run_id,
            actor=actor,
            config_key_path=config_key_path,
            old_value=old_value,
            new_value=new_value,
            source=source,
            reason=reason,
        )
        self._load_events.append(event)
        self._logger.info(
            "config_service.override_recorded",
            extra={
                "key": config_key_path,
                "source": source,
                "actor": actor,
                "reason": reason,
            },
        )

    def health_check(self) -> BaseResult[dict[str, Any]]:
        """Verify config files are present and loadable.

        Returns:
            :class:`BaseResult` with ``{"status": "ok", "config_root": ..., "n_base_files": ...}``.
        """
        base_files = [
            "tool_groups.yaml", "roles.yaml", "stages.yaml", "routes.yaml",
            "governance.yaml", "ui.yaml", "domain.yaml", "environment.yaml",
        ]
        missing = [f for f in base_files if not (self._config_root / f).exists()]
        if missing:
            return ResultFactory.fail(
                "ERR_CONFIG_FILES_MISSING",
                f"Missing config files: {missing}",
            )
        return ResultFactory.ok({
            "status": "ok",
            "config_root": str(self._config_root),
            "n_base_files": len(base_files),
        })

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _bundle_checksum(bundle: RuntimeConfigBundle) -> str:
        data = {
            "n_stages": len(bundle.stages.stages),
            "n_roles": len(bundle.roles.roles),
            "n_routes": len(bundle.routes.routes),
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:12]
