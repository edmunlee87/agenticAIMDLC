"""StageConfigResolver -- resolves effective stage config for a given runtime context.

Merges base stage config with domain-specific overrides and returns the fully
resolved :class:`~platform_core.runtime.config_models.stages.StageConfig` for
the current context. Used by the RuntimeResolver to build a ResolvedStack.
"""

from __future__ import annotations

import logging

from platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from platform_core.runtime.config_models.stages import StageConfig
from platform_core.runtime.config_models.tool_groups import ToolAllowlistConfig

logger = logging.getLogger(__name__)


class StageConfigResolver:
    """Resolves the effective stage configuration for a runtime context.

    Applies domain-specific stage overrides to the base stage configuration.

    Args:
        bundle: The loaded :class:`RuntimeConfigBundle`.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._bundle = bundle

    def resolve(self, stage_id: str, active_domain: str) -> StageConfig:
        """Return the effective StageConfig for ``stage_id`` and ``active_domain``.

        Domain stage overrides are merged in: additional skill IDs, tool IDs,
        and governance gate IDs from the domain config are appended to the base
        stage config. A new immutable StageConfig is returned (original is not
        mutated).

        Args:
            stage_id: Stage identifier.
            active_domain: Active domain identifier.

        Returns:
            Resolved :class:`StageConfig` with domain overrides applied.

        Raises:
            KeyError: If ``stage_id`` is not found in the bundle.
        """
        stages = self._bundle.stages.stages
        if stage_id not in stages:
            raise KeyError(
                f"StageConfigResolver: unknown stage_id '{stage_id}'. "
                f"Known stages: {sorted(stages)}"
            )

        base_stage = stages[stage_id]
        domain_cfg = self._bundle.domains.domains.get(active_domain)

        if domain_cfg is None:
            logger.debug(
                "stage_resolver.domain_not_found",
                extra={"stage_id": stage_id, "active_domain": active_domain},
            )
            return base_stage

        overrides = [o for o in domain_cfg.stage_overrides if o.stage_id == stage_id]
        if not overrides:
            return base_stage

        override = overrides[0]  # take the first matching override per domain

        # Merge tool allowlist additions
        existing_allow = list(base_stage.tool_allowlist.explicit_allow)
        extra_tools = [
            t for t in override.tool_allowlist_additions
            if t not in existing_allow and t not in base_stage.tool_allowlist.explicit_block
        ]
        merged_allowlist = ToolAllowlistConfig(
            include_groups=list(base_stage.tool_allowlist.include_groups),
            exclude_groups=list(base_stage.tool_allowlist.exclude_groups),
            explicit_allow=existing_allow + extra_tools,
            explicit_block=list(base_stage.tool_allowlist.explicit_block),
        )

        resolved = base_stage.model_copy(
            update={"tool_allowlist": merged_allowlist},
        )

        logger.debug(
            "stage_resolver.resolved",
            extra={
                "stage_id": stage_id,
                "active_domain": active_domain,
                "added_tools": extra_tools,
            },
        )
        return resolved

    def effective_allowlist(self, stage_id: str, active_domain: str) -> set[str]:
        """Return the effective set of allowed tool IDs for the stage/domain.

        Expands tool groups from the bundle, then applies explicit allow/block lists.

        Args:
            stage_id: Stage identifier.
            active_domain: Active domain identifier.

        Returns:
            Set of permitted tool ID strings.
        """
        resolved_stage = self.resolve(stage_id, active_domain)
        allowlist_cfg = resolved_stage.tool_allowlist
        tool_groups = self._bundle.tool_groups

        allowed: set[str] = set()

        for group_id in allowlist_cfg.include_groups:
            group = tool_groups.get(group_id)
            if group:
                allowed.update(group.tool_ids)
            else:
                logger.warning(
                    "stage_resolver.unknown_tool_group",
                    extra={"group_id": group_id, "stage_id": stage_id},
                )

        for group_id in allowlist_cfg.exclude_groups:
            group = tool_groups.get(group_id)
            if group:
                allowed -= set(group.tool_ids)

        allowed.update(allowlist_cfg.explicit_allow)
        allowed -= set(allowlist_cfg.explicit_block)

        return allowed
