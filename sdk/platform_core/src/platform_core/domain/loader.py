"""platform_core.domain.loader -- DomainPackLoader: loads and validates domain pack YAML files.

The loader validates every manifest against the :class:`~platform_core.domain.models.DomainPackManifest`
Pydantic schema, emits structured audit log on load, and caches manifests by domain.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

from platform_core.domain.models import (
    ArtifactDefinition,
    DomainPackManifest,
    MetricDefinition,
    PolicyRule,
    ReviewTemplate,
    RoutingRule,
    RouteCondition,
    SkillPackDefinition,
    StageClass,
    StageDefinition,
)

logger = logging.getLogger(__name__)


class DomainPackValidationError(Exception):
    """Raised when a domain pack YAML fails schema validation."""


class DomainPackLoader:
    """Loads, validates, and caches :class:`~platform_core.domain.models.DomainPackManifest` objects.

    Args:
        overlay_dir: Directory containing domain overlay YAML files.
            Default: ``configs/runtime/domain_overlays``.
    """

    def __init__(self, overlay_dir: str | Path | None = None) -> None:
        self._overlay_dir = Path(overlay_dir) if overlay_dir else self._default_overlay_dir()
        self._cache: dict[str, DomainPackManifest] = {}

    def load(self, domain: str, yaml_path: str | Path | None = None) -> DomainPackManifest:
        """Load a domain pack manifest.

        Tries the following locations in order:
        1. Explicit ``yaml_path`` if provided.
        2. ``<overlay_dir>/<domain>.yaml``.

        Args:
            domain: Domain identifier (e.g. ``"scorecard"``).
            yaml_path: Optional explicit path to the domain pack YAML.

        Returns:
            Validated :class:`DomainPackManifest`.

        Raises:
            FileNotFoundError: If the YAML file cannot be found.
            DomainPackValidationError: If validation fails.
        """
        if domain in self._cache:
            return self._cache[domain]

        path = self._resolve_path(domain, yaml_path)
        raw = self._read_yaml(path)
        manifest = self._parse(raw, source=str(path))
        self._cache[domain] = manifest

        logger.info(
            "domain_pack_loader.loaded",
            extra={
                "domain": domain,
                "source": str(path),
                "stage_count": len(manifest.stage_registry),
                "schema_version": manifest.schema_version,
            },
        )
        return manifest

    def load_all(self) -> dict[str, DomainPackManifest]:
        """Load all YAML files in the overlay directory.

        Returns:
            Dict of domain → :class:`DomainPackManifest`.
        """
        if not self._overlay_dir.exists():
            logger.warning("domain_pack_loader.overlay_dir_missing", extra={"path": str(self._overlay_dir)})
            return {}

        manifests: dict[str, DomainPackManifest] = {}
        for yaml_file in self._overlay_dir.glob("*.yaml"):
            domain = yaml_file.stem
            try:
                manifests[domain] = self.load(domain, yaml_file)
            except Exception as exc:
                logger.error("domain_pack_loader.load_failed", extra={"domain": domain, "error": str(exc)})
        return manifests

    def get_cached(self, domain: str) -> DomainPackManifest | None:
        """Return a cached manifest without loading.

        Args:
            domain: Domain identifier.

        Returns:
            :class:`DomainPackManifest` or None.
        """
        return self._cache.get(domain)

    def invalidate(self, domain: str | None = None) -> None:
        """Invalidate cached manifests.

        Args:
            domain: Specific domain to invalidate, or None to clear all.
        """
        if domain:
            self._cache.pop(domain, None)
        else:
            self._cache.clear()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _resolve_path(self, domain: str, yaml_path: str | Path | None) -> Path:
        if yaml_path:
            p = Path(yaml_path)
            if not p.exists():
                raise FileNotFoundError(f"Domain pack YAML not found: {p}")
            return p
        candidate = self._overlay_dir / f"{domain}.yaml"
        if not candidate.exists():
            raise FileNotFoundError(
                f"Domain pack YAML not found for domain '{domain}' at '{candidate}'."
            )
        return candidate

    @staticmethod
    def _read_yaml(path: Path) -> dict[str, Any]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not isinstance(data, dict):
                raise DomainPackValidationError(f"YAML root must be a mapping, got {type(data).__name__}")
            return data
        except yaml.YAMLError as exc:
            raise DomainPackValidationError(f"YAML parse error in '{path}': {exc}") from exc

    @classmethod
    def _parse(cls, raw: dict[str, Any], source: str = "") -> DomainPackManifest:
        """Parse raw YAML dict into a validated :class:`DomainPackManifest`.

        Args:
            raw: Raw YAML dict.
            source: Source path (for error messages).

        Returns:
            :class:`DomainPackManifest`.

        Raises:
            DomainPackValidationError: On validation failure.
        """
        try:
            domain = raw.get("domain", "")
            if not domain:
                raise DomainPackValidationError(f"Missing required field 'domain' in {source}")

            stage_registry = [
                StageDefinition(
                    stage_id=s["stage_id"],
                    label=s.get("label", ""),
                    stage_class=StageClass(s.get("stage_class", "development")),
                    is_terminal=s.get("is_terminal", False),
                    requires_hitl=s.get("requires_hitl", False),
                    governance_gate=s.get("governance_gate", False),
                    tool_groups=s.get("tool_groups") or [],
                    artifact_types=s.get("artifact_types") or [],
                    policy_pack_ids=s.get("policy_pack_ids") or [],
                )
                for s in (raw.get("stage_registry") or [])
            ]

            routing_rules = [
                RoutingRule(
                    from_stage=r["from_stage"],
                    to_stage=r["to_stage"],
                    condition=RouteCondition(r.get("condition", "on_success")),
                    failure_stage=r.get("failure_stage"),
                )
                for r in (raw.get("routing_rules") or [])
            ]

            metrics_pack = [
                MetricDefinition(
                    metric_name=m["metric_name"],
                    display_name=m.get("display_name", ""),
                    description=m.get("description", ""),
                    higher_is_better=m.get("higher_is_better", True),
                    threshold_low=m.get("threshold_low"),
                    threshold_high=m.get("threshold_high"),
                    warn_threshold_low=m.get("warn_threshold_low"),
                    dataset_splits=m.get("dataset_splits") or ["test"],
                    is_primary=m.get("is_primary", False),
                )
                for m in (raw.get("metrics_pack") or [])
            ]

            policy_pack = [
                PolicyRule(
                    rule_id=p["rule_id"],
                    name=p.get("name", ""),
                    description=p.get("description", ""),
                    severity=p.get("severity", "medium"),
                    applies_to_stages=p.get("applies_to_stages") or [],
                    condition_expression=p.get("condition_expression", ""),
                    requires_waiver=p.get("requires_waiver", False),
                )
                for p in (raw.get("policy_pack") or [])
            ]

            artifact_pack = [
                ArtifactDefinition(
                    artifact_type=a["artifact_type"],
                    display_name=a.get("display_name", ""),
                    description=a.get("description", ""),
                    produced_at_stage=a.get("produced_at_stage", ""),
                    schema_ref=a.get("schema_ref"),
                    is_audit_required=a.get("is_audit_required", False),
                )
                for a in (raw.get("artifact_pack") or [])
            ]

            review_templates = [
                ReviewTemplate(
                    template_id=t["template_id"],
                    stage_id=t["stage_id"],
                    review_type=t.get("review_type", "approval"),
                    panel_a_evidence_types=t.get("panel_a_evidence_types") or [],
                    required_form_fields=t.get("required_form_fields") or ["rationale", "policy_acknowledged"],
                    action_types=t.get("action_types") or ["approve", "reject", "escalate"],
                    required_roles=t.get("required_roles") or [],
                )
                for t in (raw.get("review_templates") or [])
            ]

            sp_raw = raw.get("skill_pack") or {}
            skill_pack = SkillPackDefinition(
                domain_skill=sp_raw.get("domain_skill", ""),
                stage_skills=sp_raw.get("stage_skills") or {},
            )

            return DomainPackManifest(
                domain=domain,
                description=raw.get("description", ""),
                model_class=raw.get("model_class", ""),
                regulatory_scope=raw.get("regulatory_scope") or [],
                schema_version=raw.get("schema_version", "1.0.0"),
                stage_registry=stage_registry,
                routing_rules=routing_rules,
                metrics_pack=metrics_pack,
                policy_pack=policy_pack,
                artifact_pack=artifact_pack,
                review_templates=review_templates,
                skill_pack=skill_pack,
                domain_overlay=raw.get("domain_overlay") or {},
                test_pack=raw.get("test_pack") or {},
            )

        except DomainPackValidationError:
            raise
        except Exception as exc:
            raise DomainPackValidationError(f"Failed to parse domain pack at '{source}': {exc}") from exc

    @staticmethod
    def _default_overlay_dir() -> Path:
        """Resolve the default overlay directory relative to the workspace root."""
        # Walk up from this file to find the configs directory.
        here = Path(__file__).resolve()
        for parent in here.parents:
            candidate = parent / "configs" / "runtime" / "domain_overlays"
            if candidate.exists():
                return candidate
        # Fallback: relative to CWD.
        return Path("configs/runtime/domain_overlays")
