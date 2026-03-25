"""Runtime resolver pack -- orchestrates all sub-resolvers to produce a RuntimeDecision.

:class:`RuntimeResolver` is the single entry point called by every controller before
dispatching SDK calls. It accepts a :class:`~platform_core.schemas.payloads.RuntimeContext`
and returns a :class:`RuntimeDecision` containing:

- Effective tool allowlist for the current stage/role.
- Resolved UI mode and interaction mode.
- Resolved token mode.
- Active governance constraints.
- Retry policy.
- Whether a human review is required.

Sub-resolvers (each independently testable):
- :class:`AllowlistResolver`
- :class:`GovernanceRuleResolver`
- :class:`UIModeResolver`
- :class:`InteractionModeResolver`
- :class:`TokenModeResolver`
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from platform_contracts.enums import InteractionMode, TokenMode, UIMode
from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.runtime.config_models.stages import StageConfig
from platform_core.schemas.payloads import RuntimeContext

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# RuntimeDecision -- the output of the resolver pack
# ---------------------------------------------------------------------------


class GovernanceConstraints(BaseModel):
    """Resolved governance constraints for the current runtime context."""

    model_config = ConfigDict(frozen=True)

    requires_human_review: bool = False
    auto_continue_allowed: bool = True
    approval_required: bool = False
    active_policy_violations_blocking: bool = False


class RetryPolicy(BaseModel):
    """Resolved retry policy for the current stage."""

    model_config = ConfigDict(frozen=True)

    max_attempts: int = 3
    backoff_seconds: float = 2.0
    backoff_multiplier: float = 2.0
    max_backoff_seconds: float = 60.0


class RuntimeDecision(BaseModel):
    """The complete output of a :class:`RuntimeResolver` invocation.

    Args:
        stage_name: Stage being resolved.
        active_role: Resolved role.
        active_domain: Resolved domain.
        tool_allowlist: Tools allowed for this stage/role combination.
        ui_mode: Resolved UI mode.
        interaction_mode: Resolved interaction mode.
        token_mode: Resolved token mode.
        governance_constraints: Resolved governance constraints.
        retry_policy: Resolved retry policy.
        extra: Arbitrary additional resolved data.
    """

    model_config = ConfigDict(frozen=True)

    stage_name: str
    active_role: str
    active_domain: str
    tool_allowlist: list[str] = Field(default_factory=list)
    ui_mode: UIMode = UIMode.STAGE_PROGRESS
    interaction_mode: InteractionMode = InteractionMode.NONE
    token_mode: TokenMode = TokenMode.STANDARD
    governance_constraints: GovernanceConstraints = Field(default_factory=GovernanceConstraints)
    retry_policy: RetryPolicy = Field(default_factory=RetryPolicy)
    extra: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Sub-resolvers
# ---------------------------------------------------------------------------


class AllowlistResolver:
    """Resolves the effective tool allowlist for a stage/role/domain.

    Resolution order:
    1. Stage allowlist: expand stage.tool_allowlist.include_groups + explicit_allow.
    2. Apply explicit_block to remove blocked tools.
    3. Add domain-level tool_allowlist_additions for this stage.
    4. Role-level explicit_allow additions.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._bundle = bundle
        # Expand tool group to tool_ids.
        self._groups: dict[str, list[str]] = {
            gid: list(cfg.tool_ids) for gid, cfg in bundle.tool_groups.items()
        }

    def _expand_allowlist(self, allowlist_cfg: Any) -> tuple[list[str], set[str]]:
        """Expand a ToolAllowlistConfig into (allowed_tools, blocked_tools).

        Args:
            allowlist_cfg: :class:`~platform_core.runtime.config_models.tool_groups.ToolAllowlistConfig`.

        Returns:
            Tuple of (allowed, blocked) tool id lists.
        """
        tools: list[str] = []
        for group_id in (allowlist_cfg.include_groups or []):
            tools.extend(self._groups.get(group_id, []))
        tools.extend(allowlist_cfg.explicit_allow or [])

        blocked: set[str] = set(allowlist_cfg.explicit_block or [])
        for group_id in (allowlist_cfg.exclude_groups or []):
            blocked.update(self._groups.get(group_id, []))

        return tools, blocked

    def resolve(self, stage_def: StageConfig | None, role: str, domain: str) -> list[str]:
        """Return effective tool allowlist for stage/role/domain.

        Args:
            stage_def: Active stage config (None -> empty list).
            role: Actor's role.
            domain: Active domain identifier.

        Returns:
            Deduplicated tool identifier list (respects block).
        """
        if stage_def is None:
            return []

        tools, blocked = self._expand_allowlist(stage_def.tool_allowlist)

        # Domain additions.
        domain_cfg = self._bundle.domains.domains.get(domain)
        if domain_cfg is not None:
            for override in domain_cfg.stage_overrides:
                if override.stage_id == stage_def.stage_id:
                    tools.extend(override.tool_allowlist_additions)

        # Role explicit_allow additions.
        role_cfg = self._bundle.roles.roles.get(role)
        if role_cfg is not None:
            role_tools, role_blocked = self._expand_allowlist(role_cfg.tool_allowlist)
            tools.extend(role_tools)
            blocked.update(role_blocked)

        # Deduplicate and remove blocked.
        seen: list[str] = []
        seen_set: set[str] = set()
        for t in tools:
            if t not in blocked and t not in seen_set:
                seen.append(t)
                seen_set.add(t)
        return seen


class GovernanceRuleResolver:
    """Resolves governance constraints from a stage's governance gates.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._bundle = bundle

    def resolve(self, stage_def: StageConfig | None) -> GovernanceConstraints:
        """Resolve governance constraints for a stage.

        Args:
            stage_def: Active stage config (None -> permissive defaults).

        Returns:
            Resolved :class:`GovernanceConstraints`.
        """
        if stage_def is None:
            return GovernanceConstraints()

        requires_review = any(g.requires_review for g in stage_def.governance_gates)
        approval_required = any(g.requires_approval for g in stage_def.governance_gates)

        return GovernanceConstraints(
            requires_human_review=requires_review,
            auto_continue_allowed=not requires_review,
            approval_required=approval_required,
        )


class UIModeResolver:
    """Resolves UIMode from stage properties."""

    def resolve(self, stage_def: StageConfig | None) -> UIMode:
        """Return UIMode for the given stage.

        Args:
            stage_def: Stage definition (or None for unknown stage).

        Returns:
            Appropriate :class:`UIMode`.
        """
        if stage_def is None:
            return UIMode.IDLE
        if stage_def.is_terminal:
            return UIMode.READONLY
        if any(g.requires_review for g in stage_def.governance_gates):
            return UIMode.REVIEW_3PANEL
        if stage_def.requires_selection:
            return UIMode.SELECTION_CARDS
        return UIMode.STAGE_PROGRESS


class InteractionModeResolver:
    """Resolves InteractionMode from governance constraints."""

    def resolve(self, constraints: GovernanceConstraints) -> InteractionMode:
        """Return interaction mode given governance constraints.

        Args:
            constraints: Resolved :class:`GovernanceConstraints`.

        Returns:
            Appropriate :class:`InteractionMode`.
        """
        if constraints.approval_required:
            return InteractionMode.APPROVAL_REQUIRED
        if constraints.requires_human_review:
            return InteractionMode.REVIEW_REQUIRED
        return InteractionMode.NONE


class TokenModeResolver:
    """Resolves token budget mode from stage properties."""

    def resolve(
        self, stage_def: StageConfig | None, validation_mode: bool = False
    ) -> TokenMode:
        """Return token mode for a stage.

        Args:
            stage_def: Stage config.
            validation_mode: True when running in validation workflow mode.

        Returns:
            Appropriate :class:`TokenMode`.
        """
        if stage_def is None:
            return TokenMode.STANDARD
        if validation_mode or any(g.requires_review for g in stage_def.governance_gates):
            return TokenMode.DEEP_REVIEW
        if stage_def.is_terminal:
            return TokenMode.MICRO
        return TokenMode.STANDARD


# ---------------------------------------------------------------------------
# RuntimeResolver -- the orchestrator
# ---------------------------------------------------------------------------


class RuntimeResolver:
    """Orchestrates all sub-resolvers to produce a :class:`RuntimeDecision`.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._bundle = bundle
        self._allowlist_resolver = AllowlistResolver(bundle)
        self._governance_resolver = GovernanceRuleResolver(bundle)
        self._ui_resolver = UIModeResolver()
        self._interaction_resolver = InteractionModeResolver()
        self._token_resolver = TokenModeResolver()

    def resolve(self, context: RuntimeContext) -> RuntimeDecision:
        """Resolve all runtime parameters for a controller invocation.

        Args:
            context: :class:`RuntimeContext` from the controller.

        Returns:
            :class:`RuntimeDecision` with all resolved parameters.
        """
        stage_name = context.stage_name
        role = context.active_role
        domain = context.active_domain
        stage_def = self._bundle.stages.stages.get(stage_name)

        # 1. Tool allowlist.
        allowlist = self._allowlist_resolver.resolve(stage_def, role, domain)

        # 2. Governance constraints.
        governance = self._governance_resolver.resolve(stage_def)

        # 3. Retry policy from stage config.
        retry = RetryPolicy()
        if stage_def is not None:
            rc = stage_def.retry_config
            retry = RetryPolicy(
                max_attempts=rc.max_retries,
                backoff_seconds=float(rc.base_delay_seconds),
                max_backoff_seconds=float(rc.max_delay_seconds),
            )

        # 4. UI mode.
        ui_mode = self._ui_resolver.resolve(stage_def)

        # 5. Interaction mode.
        interaction_mode = self._interaction_resolver.resolve(governance)

        # 6. Token mode.
        token_mode = self._token_resolver.resolve(stage_def, validation_mode=context.validation_mode)

        decision = RuntimeDecision(
            stage_name=stage_name,
            active_role=role,
            active_domain=domain,
            tool_allowlist=allowlist,
            ui_mode=ui_mode,
            interaction_mode=interaction_mode,
            token_mode=token_mode,
            governance_constraints=governance,
            retry_policy=retry,
        )

        logger.debug(
            "runtime_resolver.resolved",
            extra={
                "stage_name": stage_name,
                "role": role,
                "domain": domain,
                "ui_mode": ui_mode,
                "n_tools": len(allowlist),
            },
        )
        return decision
