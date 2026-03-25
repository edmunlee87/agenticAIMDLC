"""Stage routing config models.

Defines transition rules between stages: conditions, guards, and edge metadata.
Loaded from ``configs/runtime/routes.yaml``.
"""

from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from platform_core.runtime.config_models.base import ConfigModelBase


class TransitionGuardConfig(ConfigModelBase):
    """A guard condition that must pass before a stage transition is allowed.

    Args:
        guard_id: Unique guard identifier.
        description: Human-readable description.
        condition_type: Type of check (e.g. ``"stage_completed"``, ``"gate_passed"``,
            ``"selection_present"``, ``"policy_check"``).
        condition_ref: Reference to the stage/gate/rule being checked.
        negate: If True, the guard passes when the condition is NOT met.
    """

    guard_id: str
    description: str = ""
    condition_type: str
    condition_ref: str
    negate: bool = False


class StageRouteConfig(ConfigModelBase):
    """A directed transition edge in the MDLC workflow graph.

    Args:
        route_id: Unique route identifier.
        from_stage: Source stage ID.
        to_stage: Target stage ID.
        guards: Ordered guards that must all pass for this transition.
        priority: Route priority; lower = higher priority. Default: 100.
        label: Display label for workflow visualization.
        is_error_path: Whether this route is an error/recovery path.
    """

    route_id: str
    from_stage: str
    to_stage: str
    guards: list[TransitionGuardConfig] = Field(default_factory=list)
    priority: int = 100
    label: str = ""
    is_error_path: bool = False

    @field_validator("route_id", "from_stage", "to_stage", mode="before")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("route_id, from_stage, and to_stage must be non-empty")
        return v

    @model_validator(mode="after")
    def _no_self_loops(self) -> "StageRouteConfig":
        if self.from_stage == self.to_stage:
            raise ValueError(
                f"Route '{self.route_id}': from_stage and to_stage must differ "
                f"(got '{self.from_stage}')"
            )
        return self


class RoutesConfig(ConfigModelBase):
    """Top-level routing configuration.

    Args:
        version: Config file version.
        routes: All transition routes indexed by route_id.
    """

    version: str = "1.0.0"
    routes: dict[str, StageRouteConfig] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _keys_match_route_ids(self) -> "RoutesConfig":
        for key, route in self.routes.items():
            if key != route.route_id:
                raise ValueError(
                    f"Routes dict key '{key}' does not match route_id '{route.route_id}'"
                )
        return self
