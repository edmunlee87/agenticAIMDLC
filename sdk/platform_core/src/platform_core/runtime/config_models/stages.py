"""Stage configuration models.

Defines the structure, skill requirements, governance gates, and routing
metadata for each MDLC workflow stage.
Loaded from ``configs/runtime/stages.yaml``.
"""

from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from platform_core.runtime.config_models.base import ConfigModelBase
from platform_core.runtime.config_models.enums import AccessMode
from platform_core.runtime.config_models.fragments import RetryConfig, SkillRef
from platform_core.runtime.config_models.tool_groups import ToolAllowlistConfig


class StageGovernanceGate(ConfigModelBase):
    """Governance gate configuration for a stage.

    Args:
        gate_id: Unique gate identifier.
        requires_review: HITL review required before passing this gate.
        review_type: The ReviewType identifier for the required review.
        requires_approval: Formal approval by an authority required.
        approval_role: Role required for approval.
        mandatory_evidence: List of artifact_type identifiers that must exist.
        policy_rule_refs: Policy rules that must pass at this gate.
        allow_waiver: Whether a policy waiver may bypass this gate.
    """

    gate_id: str
    requires_review: bool = False
    review_type: str = ""
    requires_approval: bool = False
    approval_role: str = ""
    mandatory_evidence: list[str] = Field(default_factory=list)
    policy_rule_refs: list[str] = Field(default_factory=list)
    allow_waiver: bool = False

    @model_validator(mode="after")
    def _review_type_if_review_required(self) -> "StageGovernanceGate":
        if self.requires_review and not self.review_type.strip():
            raise ValueError(
                f"Gate '{self.gate_id}': review_type must be set when requires_review=True"
            )
        return self


class StageConfig(ConfigModelBase):
    """Full configuration for a named MDLC workflow stage.

    Args:
        stage_id: Unique stage identifier (snake_case).
        display_name: Human-readable stage name.
        description: Stage description.
        phase: Top-level MDLC phase this stage belongs to (e.g. ``"development"``).
        stage_group: Sub-group within the phase.
        entry_conditions: Conditions (stage_ids) that must be completed before entry.
        exit_conditions: Conditions (stage_ids or gate_ids) that must pass for exit.
        skill_stack: Ordered skill references for this stage.
        tool_allowlist: SDK/tool allowlist for automated steps of this stage.
        governance_gates: Ordered list of governance gates on the exit path.
        access_mode: Default access mode for this stage.
        retry_config: Retry policy for automated operations in this stage.
        produces_candidate_versions: Whether this stage produces CandidateVersion objects.
        requires_selection: Whether a human must select a CandidateVersion to exit.
        is_terminal: Whether this is a terminal stage (no outbound transitions).
        timeout_minutes: Timeout in minutes; 0 = no timeout. Default: 0.
    """

    stage_id: str
    display_name: str = ""
    description: str = ""
    phase: str = ""
    stage_group: str = ""
    entry_conditions: list[str] = Field(default_factory=list)
    exit_conditions: list[str] = Field(default_factory=list)
    skill_stack: list[SkillRef] = Field(default_factory=list)
    tool_allowlist: ToolAllowlistConfig = Field(default_factory=ToolAllowlistConfig)
    governance_gates: list[StageGovernanceGate] = Field(default_factory=list)
    access_mode: AccessMode = AccessMode.BUILD_ONLY
    retry_config: RetryConfig = Field(default_factory=RetryConfig)
    produces_candidate_versions: bool = False
    requires_selection: bool = False
    is_terminal: bool = False
    timeout_minutes: int = 0

    @field_validator("stage_id", mode="before")
    @classmethod
    def _non_empty_id(cls, v: str) -> str:
        if not str(v).strip():
            raise ValueError("stage_id must be non-empty")
        return v

    @model_validator(mode="after")
    def _selection_requires_candidates(self) -> "StageConfig":
        if self.requires_selection and not self.produces_candidate_versions:
            raise ValueError(
                f"Stage '{self.stage_id}': requires_selection=True but "
                "produces_candidate_versions=False. Set produces_candidate_versions=True."
            )
        return self


class StagesConfig(ConfigModelBase):
    """Top-level wrapper for the stages YAML config file.

    Args:
        version: Config file version.
        stages: Map of stage_id -> StageConfig.
    """

    version: str = "1.0.0"
    stages: dict[str, StageConfig] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _keys_match_stage_ids(self) -> "StagesConfig":
        for key, stage in self.stages.items():
            if key != stage.stage_id:
                raise ValueError(
                    f"Stages dict key '{key}' does not match stage_id '{stage.stage_id}'"
                )
        return self
