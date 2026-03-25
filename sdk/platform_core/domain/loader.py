"""platform_core.domain.loader -- loads domain pack YAML files into DomainPackManifest.

The loader parses the structured YAML contract and constructs a fully-validated
:class:`~platform_core.domain.models.DomainPackManifest` instance.

All loaded manifests are cached by domain name for fast subsequent access.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from platform_core.domain.models import (
    ArtifactSpec,
    DomainPackManifest,
    MetricSpec,
    PolicyRule,
    PolicySeverity,
    RouteCondition,
    RoutingRule,
    ReviewTemplate,
    StageSpec,
)

logger = logging.getLogger(__name__)


class DomainPackLoader:
    """Loads domain pack YAML files into :class:`~platform_core.domain.models.DomainPackManifest`.

    Args:
        overlay_dir: Base directory to look up YAML files (optional hint for logging).
    """

    def __init__(self, overlay_dir: Path | str | None = None) -> None:
        self._overlay_dir = Path(overlay_dir) if overlay_dir else None
        self._cache: dict[str, DomainPackManifest] = {}

    def load(
        self,
        domain: str,
        yaml_path: Path | str,
    ) -> DomainPackManifest:
        """Load and parse a domain pack YAML file.

        The result is cached by domain name; subsequent calls with the same
        domain name return the cached manifest unless ``force_reload=True``.

        Args:
            domain: Domain identifier string (e.g. ``"scorecard"``).
            yaml_path: Path to the YAML file.

        Returns:
            Parsed :class:`~platform_core.domain.models.DomainPackManifest`.

        Raises:
            FileNotFoundError: If the YAML file does not exist.
            ValueError: If the YAML is malformed or missing required keys.
        """
        if domain in self._cache:
            return self._cache[domain]

        yaml_path = Path(yaml_path)
        if not yaml_path.exists():
            raise FileNotFoundError(f"Domain pack YAML not found: {yaml_path}")

        try:
            import yaml
        except ImportError as exc:
            raise ImportError("PyYAML is required to load domain packs: pip install pyyaml") from exc

        with yaml_path.open("r", encoding="utf-8") as fh:
            raw: dict[str, Any] = yaml.safe_load(fh) or {}

        manifest = self._parse(domain, raw)
        self._cache[domain] = manifest

        logger.info(
            "domain_loader.loaded",
            extra={
                "domain": domain,
                "stages": len(manifest.stage_registry),
                "metrics": len(manifest.metrics_pack),
                "policy_rules": len(manifest.policy_pack),
            },
        )
        return manifest

    def invalidate(self, domain: str) -> None:
        """Remove a cached manifest, forcing a fresh load on next access.

        Args:
            domain: Domain name to invalidate.
        """
        self._cache.pop(domain, None)

    # ------------------------------------------------------------------
    # Private parsing helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse(domain: str, raw: dict[str, Any]) -> DomainPackManifest:
        """Parse a raw YAML dict into a :class:`DomainPackManifest`.

        Args:
            domain: Domain identifier (used as canonical name).
            raw: Raw YAML dict.

        Returns:
            :class:`DomainPackManifest`.
        """
        stage_registry = [
            StageSpec(
                stage_id=s["stage_id"],
                label=s.get("label", ""),
                stage_class=s.get("stage_class", "development"),
                requires_hitl=bool(s.get("requires_hitl", False)),
                governance_gate=bool(s.get("governance_gate", False)),
                is_terminal=bool(s.get("is_terminal", False)),
                tool_groups=list(s.get("tool_groups") or []),
                artifact_types=list(s.get("artifact_types") or []),
                policy_pack_ids=list(s.get("policy_pack_ids") or []),
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
            MetricSpec(
                metric_name=m["metric_name"],
                display_name=m.get("display_name", ""),
                description=m.get("description", ""),
                higher_is_better=bool(m.get("higher_is_better", True)),
                threshold_low=m.get("threshold_low"),
                threshold_high=m.get("threshold_high"),
                warn_threshold_low=m.get("warn_threshold_low"),
                dataset_splits=list(m.get("dataset_splits") or []),
                is_primary=bool(m.get("is_primary", False)),
            )
            for m in (raw.get("metrics_pack") or [])
        ]

        policy_pack = [
            PolicyRule(
                rule_id=p["rule_id"],
                name=p.get("name", ""),
                description=p.get("description", ""),
                severity=PolicySeverity(p.get("severity", "high")),
                applies_to_stages=list(p.get("applies_to_stages") or []),
                condition_expression=p.get("condition_expression", ""),
                requires_waiver=bool(p.get("requires_waiver", False)),
            )
            for p in (raw.get("policy_pack") or [])
        ]

        artifact_pack = [
            ArtifactSpec(
                artifact_type=a["artifact_type"],
                display_name=a.get("display_name", ""),
                produced_at_stage=a.get("produced_at_stage", ""),
                is_audit_required=bool(a.get("is_audit_required", False)),
            )
            for a in (raw.get("artifact_pack") or [])
        ]

        review_templates = [
            ReviewTemplate(
                template_id=t["template_id"],
                stage_id=t.get("stage_id", ""),
                review_type=t.get("review_type", "approval"),
                panel_a_evidence_types=list(t.get("panel_a_evidence_types") or []),
                required_form_fields=list(t.get("required_form_fields") or []),
                action_types=list(t.get("action_types") or []),
                required_roles=list(t.get("required_roles") or []),
            )
            for t in (raw.get("review_templates") or [])
        ]

        return DomainPackManifest(
            domain=raw.get("domain", domain),
            description=raw.get("description", ""),
            model_class=raw.get("model_class", ""),
            regulatory_scope=list(raw.get("regulatory_scope") or []),
            schema_version=str(raw.get("schema_version", "1.0.0")),
            stage_registry=stage_registry,
            routing_rules=routing_rules,
            metrics_pack=metrics_pack,
            policy_pack=policy_pack,
            artifact_pack=artifact_pack,
            review_templates=review_templates,
            skill_pack=dict(raw.get("skill_pack") or {}),
            test_pack=dict(raw.get("test_pack") or {}),
        )
