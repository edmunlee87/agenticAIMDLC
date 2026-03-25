"""Domain configuration models.

Defines domain-specific settings including active SDK packs, applicable policy
packs, and domain-specific stage overrides.
Loaded from ``configs/runtime/domain.yaml``.
"""

from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from platform_core.runtime.config_models.base import ConfigModelBase


class DomainStageOverride(ConfigModelBase):
    """Stage override for a specific domain.

    Args:
        stage_id: Stage to override.
        skill_stack_additions: Additional skill IDs to append to base stack.
        tool_allowlist_additions: Additional tool IDs to allow.
        governance_gate_additions: Additional gate IDs to enforce.
    """

    stage_id: str
    skill_stack_additions: list[str] = Field(default_factory=list)
    tool_allowlist_additions: list[str] = Field(default_factory=list)
    governance_gate_additions: list[str] = Field(default_factory=list)


class DomainConfig(ConfigModelBase):
    """Configuration for a specific model development domain.

    Args:
        domain_id: Unique domain identifier (e.g. ``"credit_risk"``).
        display_name: Human-readable domain name.
        description: Domain description.
        sdk_pack_ids: IDs of domain SDK packages loaded for this domain.
        policy_pack_ids: Additional policy packs activated for this domain.
        stage_overrides: Per-stage overrides specific to this domain.
        domain_skill_id: Skill ID for the domain-level orchestrator skill.
    """

    domain_id: str
    display_name: str = ""
    description: str = ""
    sdk_pack_ids: list[str] = Field(default_factory=list)
    policy_pack_ids: list[str] = Field(default_factory=list)
    stage_overrides: list[DomainStageOverride] = Field(default_factory=list)
    domain_skill_id: str = ""

    @field_validator("domain_id", mode="before")
    @classmethod
    def _non_empty_id(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("domain_id must be non-empty")
        return v


class DomainsConfig(ConfigModelBase):
    """Top-level domain configuration.

    Args:
        version: Config file version.
        domains: Map of domain_id -> DomainConfig.
        default_domain_id: Domain used when runtime context lacks an active_domain.
    """

    version: str = "1.0.0"
    domains: dict[str, DomainConfig] = Field(default_factory=dict)
    default_domain_id: str = "generic"

    @model_validator(mode="after")
    def _keys_match_domain_ids(self) -> "DomainsConfig":
        for key, domain in self.domains.items():
            if key != domain.domain_id:
                raise ValueError(
                    f"Domains dict key '{key}' does not match domain_id '{domain.domain_id}'"
                )
        return self
