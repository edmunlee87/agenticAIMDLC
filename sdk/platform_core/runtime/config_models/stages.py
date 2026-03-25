"""Stage registry and stage tool matrix Pydantic config models.

Defines the canonical stage registry (all 38+ stages), per-stage tool matrices,
and stage preconditions loaded from the configs/runtime/ YAML pack.
"""

from typing import Dict, List, Optional

from pydantic import field_validator, model_validator

from .base import RuntimeConfigBase
from .enums import AccessModeEnum, StageClassEnum


class StageDefinition(RuntimeConfigBase):
    """Definition of a single stage in the platform.

    Attributes:
        stage_name: Unique identifier for this stage.
        stage_class: Governance classification of this stage.
        description: Human-readable description.
        domain: Optional domain this stage belongs to (None = platform-wide).
        requires_review: Whether this stage requires a HITL review.
        requires_approval: Whether this stage requires formal approval.
        requires_audit: Whether every action must generate an audit record.
        auto_continue_allowed: Whether the workflow can continue without human input.
        default_access_mode: Default access mode for actors entering this stage.
        skill_stack_hints: Suggested skill identifiers for this stage.
        artifact_expectations: Artifact types expected to be produced.
        is_terminal: Whether this is a terminal stage (workflow ends here).
    """

    stage_name: str
    stage_class: StageClassEnum
    description: Optional[str] = None
    domain: Optional[str] = None
    requires_review: bool = False
    requires_approval: bool = False
    requires_audit: bool = True
    auto_continue_allowed: bool = True
    default_access_mode: AccessModeEnum = AccessModeEnum.BUILD_ONLY
    skill_stack_hints: List[str] = []
    artifact_expectations: List[str] = []
    is_terminal: bool = False

    @field_validator("stage_name")
    @classmethod
    def validate_non_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("stage_name must not be blank")
        return v

    @model_validator(mode="after")
    def validate_approval_requires_review(self) -> "StageDefinition":
        if self.requires_approval and not self.requires_review:
            raise ValueError(
                f"Stage '{self.stage_name}': requires_approval=True implies requires_review=True"
            )
        return self

    @model_validator(mode="after")
    def validate_auto_continue_not_with_approval(self) -> "StageDefinition":
        if self.requires_approval and self.auto_continue_allowed:
            raise ValueError(
                f"Stage '{self.stage_name}': auto_continue_allowed must be False when requires_approval=True"
            )
        return self


class StageRegistryConfig(RuntimeConfigBase):
    """Complete stage registry, keyed by stage_name.

    Loaded from configs/runtime/stage_registry.yaml.
    Contains the canonical 38+ stages of the Agentic AI MDLC platform.
    """

    stages: Dict[str, StageDefinition]

    @field_validator("stages")
    @classmethod
    def validate_non_empty(cls, v: Dict[str, StageDefinition]) -> Dict[str, StageDefinition]:
        if not v:
            raise ValueError("stage registry must define at least one stage")
        return v


class StageToolMatrixEntry(RuntimeConfigBase):
    """Per-stage tool group allowance/blockage configuration.

    Attributes:
        stage_name: The stage this entry applies to.
        allowed_groups: Tool groups allowed in this stage.
        blocked_groups: Tool groups explicitly blocked in this stage.
        required_groups: Tool groups that must be available (if absent, config is invalid).
    """

    stage_name: str
    allowed_groups: List[str] = []
    blocked_groups: List[str] = []
    required_groups: List[str] = []

    @model_validator(mode="after")
    def validate_no_overlap(self) -> "StageToolMatrixEntry":
        overlap = set(self.allowed_groups) & set(self.blocked_groups)
        if overlap:
            raise ValueError(
                f"Stage '{self.stage_name}': groups cannot be both allowed and blocked: {overlap}"
            )
        return self


class StageToolMatrixConfig(RuntimeConfigBase):
    """Per-stage tool matrix config, keyed by stage_name.

    Loaded from configs/runtime/stage_tool_matrix.yaml.
    """

    matrix: Dict[str, StageToolMatrixEntry]


class StagePreconditionEntry(RuntimeConfigBase):
    """Preconditions that must be satisfied before entering a stage.

    Attributes:
        stage_name: The stage this precondition applies to.
        required_prior_stages: Stages that must be completed before this stage.
        required_artifact_types: Artifact types that must exist in the registry.
        required_selection_stages: Stages where a VersionSelection must exist.
        required_flags: Workflow state flags that must be set to True.
        blocking_conditions: Conditions that block entry even if prior stages passed.
    """

    stage_name: str
    required_prior_stages: List[str] = []
    required_artifact_types: List[str] = []
    required_selection_stages: List[str] = []
    required_flags: List[str] = []
    blocking_conditions: List[str] = []


class StagePreconditionsConfig(RuntimeConfigBase):
    """All stage preconditions, keyed by stage_name.

    Loaded from configs/runtime/stage_preconditions.yaml.
    """

    preconditions: Dict[str, StagePreconditionEntry] = {}
