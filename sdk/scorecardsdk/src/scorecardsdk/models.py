"""scorecardsdk.models -- scorecard-specific data contracts.

Models cover the core scorecard development artefacts:
- :class:`BinDefinition` -- a single WoE bin.
- :class:`CoarseClassingTable` -- merged binning result for a variable.
- :class:`WoeIvRecord` -- WoE/IV statistics for a binned variable.
- :class:`FeatureShortlist` -- selected features with IV and WoE validated.
- :class:`ScorecardModel` -- a trained logistic regression scorecard.
- :class:`ScoreScalingParams` -- parameters for converting log-odds to scorecard points.
- :class:`ScorecardCandidate` -- a candidate model version for selection review.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BinDefinition(BaseModel):
    """A single WoE bin for a variable.

    Args:
        bin_id: Unique bin identifier.
        variable_name: Variable this bin belongs to.
        bin_label: Human-readable bin label (e.g. ``"[0, 100)"``).
        lower_bound: Numeric lower bound (None = open).
        upper_bound: Numeric upper bound (None = open).
        category_values: List of category values (for categorical variables).
        count: Number of observations in this bin.
        good_count: Number of good observations.
        bad_count: Number of bad observations.
        bad_rate: Bad rate in this bin.
        woe: Weight of Evidence value.
        iv_contribution: IV contribution of this bin.
        is_special: Whether this is a special value bin (e.g. missing).
    """

    model_config = ConfigDict(frozen=True)

    bin_id: str
    variable_name: str
    bin_label: str = ""
    lower_bound: float | None = None
    upper_bound: float | None = None
    category_values: list[str] = Field(default_factory=list)
    count: int = 0
    good_count: int = 0
    bad_count: int = 0
    bad_rate: float = 0.0
    woe: float = 0.0
    iv_contribution: float = 0.0
    is_special: bool = False


class CoarseClassingTable(BaseModel):
    """Coarse classing result for a set of variables.

    Args:
        table_id: Unique identifier.
        run_id: MDLC run.
        project_id: Project.
        bins: All bin definitions keyed by ``variable_name + '_' + bin_id``.
        variables: Variables included in this table.
        created_at: Creation timestamp.
        created_by: Actor.
        metadata: Extra metadata.
    """

    model_config = ConfigDict(frozen=True)

    table_id: str
    run_id: str
    project_id: str
    bins: list[BinDefinition] = Field(default_factory=list)
    variables: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)

    def bins_for_variable(self, variable_name: str) -> list[BinDefinition]:
        """Return all bins for a variable.

        Args:
            variable_name: Variable name.

        Returns:
            List of :class:`BinDefinition`.
        """
        return [b for b in self.bins if b.variable_name == variable_name]


class WoeIvRecord(BaseModel):
    """WoE/IV statistics for a single variable.

    Args:
        record_id: Unique identifier.
        variable_name: Variable.
        total_iv: Total Information Value.
        bins: Bin-level WoE details.
        is_monotone: Whether WoE is monotone across bins.
        passes_minimum_iv: Whether IV exceeds minimum threshold.
        minimum_iv_threshold: Threshold used for pass/fail (default: 0.02).
    """

    model_config = ConfigDict(frozen=True)

    record_id: str
    variable_name: str
    total_iv: float = 0.0
    bins: list[BinDefinition] = Field(default_factory=list)
    is_monotone: bool = True
    passes_minimum_iv: bool = True
    minimum_iv_threshold: float = 0.02

    @field_validator("passes_minimum_iv", mode="before")
    @classmethod
    def _check_iv(cls, v: bool) -> bool:
        return v


class FeatureShortlist(BaseModel):
    """Selected features after IV screening and correlation check.

    Args:
        shortlist_id: Unique identifier.
        run_id: MDLC run.
        project_id: Project.
        selected_features: List of selected feature names.
        iv_scores: Dict of feature_name -> total_iv.
        rejected_features: Features rejected with reason.
        contains_protected_attributes: Whether protected attributes are included.
        total_shortlist_iv: Sum of IV across selected features.
        created_at: Creation timestamp.
        created_by: Actor.
    """

    model_config = ConfigDict(frozen=True)

    shortlist_id: str
    run_id: str
    project_id: str
    selected_features: list[str] = Field(default_factory=list)
    iv_scores: dict[str, float] = Field(default_factory=dict)
    rejected_features: dict[str, str] = Field(default_factory=dict)  # feature -> reason
    contains_protected_attributes: bool = False
    total_shortlist_iv: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""


class ScorecardModel(BaseModel):
    """A trained logistic regression scorecard model.

    Args:
        model_id: Unique model identifier.
        run_id: MDLC run.
        project_id: Project.
        feature_shortlist_id: FeatureShortlist used for training.
        coefficients: Dict of feature_name -> logistic regression coefficient.
        intercept: Model intercept.
        metrics: Evaluation metrics dict.
        training_snapshot_id: Training dataset snapshot ID.
        test_snapshot_id: Test dataset snapshot ID.
        oot_snapshot_id: OOT dataset snapshot ID.
        created_at: Creation timestamp.
        created_by: Actor.
    """

    model_config = ConfigDict(frozen=True)

    model_id: str
    run_id: str
    project_id: str
    feature_shortlist_id: str = ""
    coefficients: dict[str, float] = Field(default_factory=dict)
    intercept: float = 0.0
    metrics: dict[str, float] = Field(default_factory=dict)
    training_snapshot_id: str = ""
    test_snapshot_id: str = ""
    oot_snapshot_id: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""


class ScoreScalingParams(BaseModel):
    """Parameters for converting log-odds to scorecard points.

    Uses the standard double-the-odds scaling:
    Score = PDO * (log-odds - log-odds_0) / ln(2) + base_score.

    Args:
        scaling_id: Unique identifier.
        model_id: Source model ID.
        base_score: Score at odds_0.
        pdo: Points-to-double-the-odds.
        odds_0: Reference odds (good:bad ratio at base_score).
        score_min: Minimum score (floor).
        score_max: Maximum score (cap).
        created_at: Creation timestamp.
    """

    model_config = ConfigDict(frozen=True)

    scaling_id: str
    model_id: str
    base_score: float = 600.0
    pdo: float = 20.0
    odds_0: float = 50.0
    score_min: float = 300.0
    score_max: float = 850.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ScorecardCandidate(BaseModel):
    """A candidate scorecard model version for selection review.

    Args:
        candidate_id: Unique identifier.
        model_id: Source :class:`ScorecardModel` ID.
        run_id: MDLC run.
        project_id: Project.
        version_label: Human-readable version label.
        metrics: Key metrics for this candidate.
        feature_count: Number of features used.
        is_recommended: Whether this candidate is auto-recommended.
        rationale: Recommendation rationale.
        created_at: Creation timestamp.
    """

    model_config = ConfigDict(frozen=True)

    candidate_id: str
    model_id: str
    run_id: str
    project_id: str
    version_label: str = ""
    metrics: dict[str, float] = Field(default_factory=dict)
    feature_count: int = 0
    is_recommended: bool = False
    rationale: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
