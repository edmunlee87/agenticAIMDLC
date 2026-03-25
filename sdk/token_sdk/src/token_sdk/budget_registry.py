"""token_sdk.budget_registry -- per-mode, per-stage token budget configuration.

Budgets are config-driven with defaults.  They can be overridden per stage
or per role in the runtime config overlay.
"""

from __future__ import annotations

from token_sdk.models import TokenMode

# Default budgets (tokens) per :class:`TokenMode`.
_DEFAULT_BUDGETS: dict[TokenMode, int] = {
    TokenMode.FULL: 8000,
    TokenMode.COMPACT: 3000,
    TokenMode.MINIMAL: 1000,
}

# Per-pack-type multipliers applied on top of mode budgets.
_PACK_MULTIPLIERS: dict[str, float] = {
    "routing": 0.5,
    "review": 1.0,
    "validation": 0.75,
    "drafting": 1.25,
    "general": 1.0,
}


class BudgetRegistry:
    """Resolves token budgets for a given mode, pack type, and stage.

    Args:
        overrides: Optional dict of ``"<mode>.<pack_type>"`` -> budget int
            to override defaults.
    """

    def __init__(self, overrides: dict[str, int] | None = None) -> None:
        self._overrides = overrides or {}

    def get_budget(
        self,
        token_mode: TokenMode,
        pack_type: str = "general",
        stage_name: str = "",
    ) -> int:
        """Resolve the token budget for a context assembly.

        Lookup order:
        1. Stage-specific override: ``"<stage>.<mode>.<pack_type>"``.
        2. Mode + pack_type override: ``"<mode>.<pack_type>"``.
        3. Mode override: ``"<mode>"``.
        4. Computed default: base budget * pack multiplier.

        Args:
            token_mode: :class:`TokenMode`.
            pack_type: Pack type string. Default: ``"general"``.
            stage_name: Stage name for stage-specific overrides. Default: ``""``.

        Returns:
            Token budget as int.
        """
        if stage_name:
            key = f"{stage_name}.{token_mode.value}.{pack_type}"
            if key in self._overrides:
                return self._overrides[key]

        key = f"{token_mode.value}.{pack_type}"
        if key in self._overrides:
            return self._overrides[key]

        key = token_mode.value
        if key in self._overrides:
            return self._overrides[key]

        base = _DEFAULT_BUDGETS.get(token_mode, 4000)
        multiplier = _PACK_MULTIPLIERS.get(pack_type, 1.0)
        return int(base * multiplier)
