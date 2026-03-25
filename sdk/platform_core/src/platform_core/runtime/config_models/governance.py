"""Governance and policy overlay config models.

Defines policy rules, governance packs, and overlay engine configuration.
Loaded from ``configs/runtime/governance.yaml``.
"""

from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from platform_contracts.enums import GovernanceSeverity
from platform_core.runtime.config_models.base import ConfigModelBase
from platform_core.runtime.config_models.enums import PolicyMode


class PolicyRuleConfig(ConfigModelBase):
    """A single governance/policy rule.

    Args:
        rule_id: Unique, stable rule identifier.
        rule_category: Logical grouping (e.g. ``"data_quality"``, ``"model_risk"``).
        description: Human-readable rule description.
        severity: Default severity when this rule triggers a finding.
        is_blocking: Whether a finding on this rule blocks stage transition.
        applies_to_stages: Stage IDs this rule applies to (empty = all stages).
        applies_to_domains: Domain IDs this rule applies to (empty = all domains).
        waiver_eligible: Whether a waiver may bypass this rule.
        evaluation_hint: Optional JSON Pointer or expression hint for evaluators.
    """

    rule_id: str
    rule_category: str = ""
    description: str = ""
    severity: GovernanceSeverity = GovernanceSeverity.MEDIUM
    is_blocking: bool = False
    applies_to_stages: list[str] = Field(default_factory=list)
    applies_to_domains: list[str] = Field(default_factory=list)
    waiver_eligible: bool = True
    evaluation_hint: str = ""

    @field_validator("rule_id", mode="before")
    @classmethod
    def _non_empty_id(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("rule_id must be non-empty")
        return v


class PolicyPackConfig(ConfigModelBase):
    """A versioned collection of policy rules forming a governance pack.

    Args:
        pack_id: Unique policy pack identifier.
        version: Semantic version of this pack.
        description: Pack description.
        policy_mode: Enforcement mode for this pack.
        rules: Map of rule_id -> PolicyRuleConfig.
    """

    pack_id: str
    version: str = "1.0.0"
    description: str = ""
    policy_mode: PolicyMode = PolicyMode.STRICT
    rules: dict[str, PolicyRuleConfig] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _keys_match_rule_ids(self) -> "PolicyPackConfig":
        for key, rule in self.rules.items():
            if key != rule.rule_id:
                raise ValueError(
                    f"Policy pack '{self.pack_id}': rules dict key '{key}' "
                    f"does not match rule_id '{rule.rule_id}'"
                )
        return self


class GovernanceOverlayRule(ConfigModelBase):
    """A single overlay rule that modifies effective policy in a specific context.

    Args:
        overlay_id: Unique overlay identifier.
        applies_when: Dict of context key/value conditions that trigger this overlay
            (e.g. ``{"active_domain": "credit_risk", "validation_mode": true}``).
        pack_id_overrides: Additional policy pack IDs to activate.
        severity_overrides: Rule-level severity overrides (rule_id -> new severity).
        blocking_overrides: Rule-level blocking overrides (rule_id -> bool).
    """

    overlay_id: str
    applies_when: dict[str, str | bool | int] = Field(default_factory=dict)
    pack_id_overrides: list[str] = Field(default_factory=list)
    severity_overrides: dict[str, GovernanceSeverity] = Field(default_factory=dict)
    blocking_overrides: dict[str, bool] = Field(default_factory=dict)


class GovernanceConfig(ConfigModelBase):
    """Top-level governance configuration.

    Args:
        version: Config file version.
        default_policy_pack_id: Policy pack loaded by default.
        policy_packs: All available policy packs.
        overlay_rules: Ordered overlay rules evaluated against runtime context.
        breach_action: What to do when a blocking rule fires.
            ``"block"`` = prevent transition (default).
            ``"escalate"`` = route to escalation review.
            ``"notify"`` = emit warning only.
    """

    version: str = "1.0.0"
    default_policy_pack_id: str = "default"
    policy_packs: dict[str, PolicyPackConfig] = Field(default_factory=dict)
    overlay_rules: list[GovernanceOverlayRule] = Field(default_factory=list)
    breach_action: str = "block"

    @field_validator("breach_action", mode="before")
    @classmethod
    def _valid_breach_action(cls, v: str) -> str:
        valid = {"block", "escalate", "notify"}
        if v not in valid:
            raise ValueError(f"breach_action must be one of {sorted(valid)}, got '{v}'")
        return v

    @model_validator(mode="after")
    def _default_pack_exists(self) -> "GovernanceConfig":
        if self.default_policy_pack_id and self.policy_packs:
            if self.default_policy_pack_id not in self.policy_packs:
                raise ValueError(
                    f"default_policy_pack_id '{self.default_policy_pack_id}' "
                    "not found in policy_packs"
                )
        return self
