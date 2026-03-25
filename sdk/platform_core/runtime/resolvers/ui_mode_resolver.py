"""UIModeResolver — resolves effective UI and interaction modes for a stage.

Uses the StageConfigResolver for stage-level defaults, then falls back to
ui_modes.yaml / interaction_modes.yaml in the bundle.
"""

from __future__ import annotations

from typing import Optional

from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.runtime.config_models.enums import InteractionModeEnum, UIModeEnum


class UIModeResolver:
    """Resolves effective UI layout mode and interaction mode for a stage.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
    """

    def __init__(self, bundle: RuntimeConfigBundle) -> None:
        self._bundle = bundle

    def resolve_ui_mode(self, stage_name: str) -> str:
        """Return effective UI mode for a stage.

        Lookup priority:
        1. Stage-level override from ``StageDefinition.default_access_mode``
           (best-effort inference from stage class → ui_mode)
        2. Stage class → ``default_for_stage_classes`` in ui_modes.yaml
        3. Hard fallback: ``"minimal"``

        Args:
            stage_name: Name of the stage.

        Returns:
            UI mode string (e.g. ``"minimal"``, ``"full"``, ``"canvas"``).
        """
        stage_class = self._get_stage_class(stage_name)
        if stage_class and self._bundle.ui_modes:
            for mode_name, mode_def in self._bundle.ui_modes.modes.items():
                if stage_class in mode_def.default_for_stage_classes:
                    return mode_name
        # Fall back to first defined mode or the raw enum value
        if self._bundle.ui_modes:
            return next(iter(self._bundle.ui_modes.modes))
        return UIModeEnum.BOOTSTRAP_WORKSPACE.value

    def resolve_interaction_mode(self, stage_name: str) -> str:
        """Return effective interaction mode for a stage.

        Lookup priority:
        1. Stage class → ``default_for_stage_classes`` in interaction_modes.yaml
        2. Hard fallback: ``"chat"``

        Args:
            stage_name: Name of the stage.

        Returns:
            Interaction mode string (e.g. ``"chat"``, ``"form"``, ``"mixed"``).
        """
        stage_class = self._get_stage_class(stage_name)
        if stage_class and self._bundle.interaction_modes:
            for mode_name, mode_def in self._bundle.interaction_modes.modes.items():
                if stage_class in mode_def.default_for_stage_classes:
                    return mode_name
        if self._bundle.interaction_modes:
            return next(iter(self._bundle.interaction_modes.modes))
        return InteractionModeEnum.EDIT_AND_FINALIZE.value

    def resolve_token_mode(self, stage_name: str) -> Optional[str]:
        """Return the recommended token budget mode for the stage's UI mode.

        Args:
            stage_name: Name of the stage.

        Returns:
            Token mode string or None.
        """
        ui_mode_name = self.resolve_ui_mode(stage_name)
        if self._bundle.ui_modes:
            mode_def = self._bundle.ui_modes.modes.get(ui_mode_name)
            if mode_def and mode_def.token_budget_hint:
                hint = mode_def.token_budget_hint
                return hint.value if hasattr(hint, "value") else str(hint)
        return None

    def _get_stage_class(self, stage_name: str) -> Optional[str]:
        if not self._bundle.stage_registry:
            return None
        stage_def = self._bundle.stage_registry.stages.get(stage_name)
        if stage_def is None:
            return None
        sc = stage_def.stage_class
        return sc.value if hasattr(sc, "value") else str(sc)
