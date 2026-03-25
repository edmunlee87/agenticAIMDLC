"""dataprepsdk.models -- data preparation template and lineage contracts.

Templates are config-driven, reproducible recipes for constructing
analysis-ready datasets.  Each execution produces an immutable
:class:`DataPrepRun` record capturing full lineage.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TemplateType(str, Enum):
    """Category of data preparation template."""
    CROSS_SECTIONAL = "cross_sectional"
    PANEL = "panel"
    TIME_SERIES = "time_series"
    EVENT_HISTORY = "event_history"
    COHORT_SNAPSHOT = "cohort_snapshot"


class ColumnTransform(BaseModel):
    """A single column-level transformation step.

    Args:
        column_name: Target column name.
        transform_type: Type (e.g. ``"clip"``, ``"fill_missing"``, ``"encode_woe"``,
            ``"lag"``, ``"rolling_mean"``).
        params: Transformation parameters.
    """

    model_config = ConfigDict(frozen=True)

    column_name: str
    transform_type: str
    params: dict[str, Any] = Field(default_factory=dict)


class DataPrepTemplate(BaseModel):
    """A versioned, reusable data preparation recipe.

    Args:
        template_id: Unique template identifier.
        name: Human-readable template name.
        template_type: :class:`TemplateType`.
        version: Semantic version.
        description: Template description.
        source_table: Input source table or dataset identifier.
        target_table: Output table name.
        observation_date_col: Column containing the observation date.
        entity_id_col: Column containing the entity identifier.
        target_col: Target/label column.
        feature_columns: Ordered list of feature column names.
        transforms: Ordered list of column transformations.
        filters: SQL-like filter expressions to apply.
        time_window_days: Lookback window in days (for time-based templates).
        observation_period: Observation period label (e.g. ``"2023-01-01/2023-12-31"``).
        seed: Random seed for reproducible sampling.
        max_rows: Maximum row cap (0 = no cap).
        metadata: Arbitrary metadata.
    """

    model_config = ConfigDict(frozen=True)

    template_id: str
    name: str = ""
    template_type: TemplateType = TemplateType.CROSS_SECTIONAL
    version: str = "1.0.0"
    description: str = ""
    source_table: str = ""
    target_table: str = ""
    observation_date_col: str = "observation_date"
    entity_id_col: str = "entity_id"
    target_col: str = "default_flag"
    feature_columns: list[str] = Field(default_factory=list)
    transforms: list[ColumnTransform] = Field(default_factory=list)
    filters: list[str] = Field(default_factory=list)
    time_window_days: int = 0
    observation_period: str = ""
    seed: int = 42
    max_rows: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)


class DataPrepLineageRecord(BaseModel):
    """Lineage record for one column produced during data prep execution.

    Args:
        column_name: Output column name.
        source_columns: Input column names.
        transform_applied: Transform type applied.
        transform_params: Parameters used.
    """

    model_config = ConfigDict(frozen=True)

    column_name: str
    source_columns: list[str] = Field(default_factory=list)
    transform_applied: str = "identity"
    transform_params: dict[str, Any] = Field(default_factory=dict)


class DataPrepRun(BaseModel):
    """Immutable record of a data preparation template execution.

    Args:
        run_record_id: Unique execution record identifier.
        template_id: Template used.
        template_version: Version of the template executed.
        run_id: MDLC run.
        project_id: Project.
        executed_by: Actor who triggered execution.
        started_at: Execution start timestamp.
        completed_at: Execution end timestamp.
        output_snapshot_id: Dataset snapshot ID produced.
        output_artifact_id: Artifact ID storing the output.
        row_count: Number of rows in output.
        column_count: Number of columns in output.
        lineage: Column-level lineage records.
        filters_applied: Filters that were applied.
        execution_engine: Engine used (``"spark"`` | ``"pandas"`` | ``"dask"``).
        success: Whether execution succeeded.
        error_message: Error details on failure.
        metadata: Arbitrary metadata.
    """

    model_config = ConfigDict(frozen=True)

    run_record_id: str
    template_id: str
    template_version: str = "1.0.0"
    run_id: str
    project_id: str
    executed_by: str = ""
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None
    output_snapshot_id: str = ""
    output_artifact_id: str = ""
    row_count: int = 0
    column_count: int = 0
    lineage: list[DataPrepLineageRecord] = Field(default_factory=list)
    filters_applied: list[str] = Field(default_factory=list)
    execution_engine: str = "pandas"
    success: bool = True
    error_message: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
