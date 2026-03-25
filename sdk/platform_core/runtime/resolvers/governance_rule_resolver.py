"""GovernanceRuleResolver — resolves governance requirements for a stage+role context.

Delegates conditional rule evaluation to :class:`GovernanceOverlayEngine` when
``policysdk`` is available. Falls back to simple default-rules lookup otherwise.
"""

from __future__ import annotations

from typing import Any, Dict, List

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.config_models.governance import DefaultGovernanceRules


class GovernanceRuleResolver:
    """Resolves effective governance requirements for a stage and applies
    conditional governance rules at runtime.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        environment: Deployment environment (affects strictness).
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        environment: str = "dev",
    ) -> None:
        self._bundle = bundle
        self._environment = environment
        self._overlays = (
            bundle.governance_overlays.governance
            if bundle.governance_overlays
            else None
        )

    def get_default_rules(self) -> DefaultGovernanceRules:
        """Return the platform-wide default governance rules.

        Returns:
            :class:`DefaultGovernanceRules` instance.
        """
        if self._overlays:
            return self._overlays.default_rules
        return DefaultGovernanceRules()

    def get_stage_governance(self, stage_name: str) -> Dict[str, Any]:
        """Return effective governance settings for a stage.

        Merges: default rules → stage-specific override.

        Args:
            stage_name: Stage to resolve governance for.

        Returns:
            Dict with keys: ``review_required``, ``approval_required``,
            ``audit_required``, ``auto_continue_allowed``.
        """
        defaults = self.get_default_rules()
        base: Dict[str, Any] = {
            "review_required": defaults.require_review_before_finalization,
            "approval_required": False,
            "audit_required": defaults.require_audit_for_all_approvals,
            "auto_continue_allowed": not defaults.block_auto_continue_on_breach,
        }
        if self._overlays:
            stage_rule_map = {r.stage_name: r for r in self._overlays.stage_rules}
            if stage_name in stage_rule_map:
                sr = stage_rule_map[stage_name]
                if sr.requires_review is not None:
                    base["review_required"] = sr.requires_review
                if sr.requires_approval is not None:
                    base["approval_required"] = sr.requires_approval
                if sr.audit_required is not None:
                    base["audit_required"] = sr.audit_required
                if sr.auto_continue_allowed is not None:
                    base["auto_continue_allowed"] = sr.auto_continue_allowed
        # Production enforcement
        if self._environment == "production":
            if defaults.require_review_before_finalization:
                base["review_required"] = True
            if defaults.require_audit_for_all_approvals:
                base["audit_required"] = True
            if defaults.block_auto_continue_on_breach:
                base["auto_continue_allowed"] = False
        return base

    def apply_conditional_rules(
        self,
        runtime_facts: Dict[str, Any],
        allowed_tools: List[str],
        blocked_tools: List[str],
    ) -> Dict[str, Any]:
        """Apply conditional governance rules to the tool lists.

        Evaluates each conditional rule; when the ``when`` clause matches the
        ``runtime_facts``, applies the ``then`` clause (force_block_tools,
        force_allow_tools).

        Args:
            runtime_facts: Dict containing runtime state flags.
            allowed_tools: Current allowed tool list.
            blocked_tools: Current blocked tool list.

        Returns:
            Dict with ``allowed_tools`` and ``blocked_tools`` after applying
            conditional rules.
        """
        if not self._overlays:
            return {"allowed_tools": list(allowed_tools), "blocked_tools": list(blocked_tools)}

        allowed_set = set(allowed_tools)
        blocked_set = set(blocked_tools)
        stage_name = runtime_facts.get("stage_name", "")

        for rule in self._overlays.conditional_rules:
            # Stage scope filter
            if rule.applies_to_stages and stage_name not in rule.applies_to_stages:
                continue
            if self._when_matches(rule.when.model_dump(), runtime_facts):
                then = rule.then
                for t in (then.force_allow_tools or []):
                    allowed_set.add(t)
                for t in (then.force_block_tools or []):
                    blocked_set.add(t)

        return {
            "allowed_tools": sorted(allowed_set),
            "blocked_tools": sorted(blocked_set),
        }

    def _when_matches(
        self, when_clause: Dict[str, Any], facts: Dict[str, Any]
    ) -> bool:
        """Return True if all conditions in ``when_clause`` are satisfied by ``facts``.

        Args:
            when_clause: Serialized ``ConditionalWhenClause`` dict.
            facts: Runtime facts dict.

        Returns:
            True when all non-None conditions match.
        """
        for key, expected in when_clause.items():
            # None means "no constraint" for Optional fields
            if expected is None:
                continue
            if key == "stage_access_mode_in":
                # Empty list means "no constraint on access mode"
                if not expected:
                    continue
                access = facts.get("access_mode", facts.get("stage_access_mode"))
                if access not in expected:
                    return False
                continue
            if key == "environment_is":
                if self._environment != expected:
                    return False
                continue
            if facts.get(key) != expected:
                return False
        return True
