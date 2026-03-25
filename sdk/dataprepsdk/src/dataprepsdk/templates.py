"""dataprepsdk.templates -- built-in template factory functions.

Pre-configured templates for the five standard template types.
Each factory returns a :class:`~dataprepsdk.models.DataPrepTemplate`
that can be registered in a :class:`~dataprepsdk.template_registry.TemplateRegistry`
and further customised before use.
"""

from __future__ import annotations

from dataprepsdk.models import ColumnTransform, DataPrepTemplate, TemplateType


def cross_sectional_template(
    template_id: str,
    source_table: str,
    target_table: str,
    observation_date: str,
    entity_id_col: str = "entity_id",
    target_col: str = "default_flag",
    feature_columns: list[str] | None = None,
    filters: list[str] | None = None,
    max_rows: int = 0,
    seed: int = 42,
) -> DataPrepTemplate:
    """Create a cross-sectional (one row per entity at a fixed date) template.

    Args:
        template_id: Unique template ID.
        source_table: Input source table identifier.
        target_table: Output table name.
        observation_date: ISO date string for the snapshot date.
        entity_id_col: Entity identifier column. Default: ``"entity_id"``.
        target_col: Target label column. Default: ``"default_flag"``.
        feature_columns: Feature column names.
        filters: Optional SQL-like filter expressions.
        max_rows: Row cap. Default: 0 (no cap).
        seed: Random seed. Default: 42.

    Returns:
        :class:`DataPrepTemplate`.
    """
    return DataPrepTemplate(
        template_id=template_id,
        name=f"Cross-Sectional: {source_table}",
        template_type=TemplateType.CROSS_SECTIONAL,
        source_table=source_table,
        target_table=target_table,
        observation_date_col="observation_date",
        entity_id_col=entity_id_col,
        target_col=target_col,
        feature_columns=feature_columns or [],
        filters=[f"observation_date == '{observation_date}'"] + (filters or []),
        max_rows=max_rows,
        seed=seed,
        metadata={"observation_date": observation_date},
    )


def panel_template(
    template_id: str,
    source_table: str,
    target_table: str,
    start_date: str,
    end_date: str,
    time_col: str = "observation_date",
    entity_id_col: str = "entity_id",
    target_col: str = "default_flag",
    feature_columns: list[str] | None = None,
    filters: list[str] | None = None,
    max_rows: int = 0,
    seed: int = 42,
) -> DataPrepTemplate:
    """Create a longitudinal panel (multiple time periods per entity) template.

    Args:
        template_id: Unique template ID.
        source_table: Input source table.
        target_table: Output table.
        start_date: Panel start date (ISO format).
        end_date: Panel end date (ISO format).
        time_col: Time column name. Default: ``"observation_date"``.
        entity_id_col: Entity column. Default: ``"entity_id"``.
        target_col: Target column. Default: ``"default_flag"``.
        feature_columns: Feature column names.
        filters: Additional filter expressions.
        max_rows: Row cap. Default: 0.
        seed: Random seed. Default: 42.

    Returns:
        :class:`DataPrepTemplate`.
    """
    return DataPrepTemplate(
        template_id=template_id,
        name=f"Panel: {source_table} ({start_date}/{end_date})",
        template_type=TemplateType.PANEL,
        source_table=source_table,
        target_table=target_table,
        observation_date_col=time_col,
        entity_id_col=entity_id_col,
        target_col=target_col,
        feature_columns=feature_columns or [],
        filters=[
            f"{time_col} >= '{start_date}'",
            f"{time_col} <= '{end_date}'",
        ] + (filters or []),
        observation_period=f"{start_date}/{end_date}",
        max_rows=max_rows,
        seed=seed,
    )


def time_series_template(
    template_id: str,
    source_table: str,
    target_table: str,
    entity_id: str,
    date_col: str = "date",
    target_col: str = "target",
    lag_periods: list[int] | None = None,
    rolling_windows: list[int] | None = None,
    feature_columns: list[str] | None = None,
    max_rows: int = 0,
    seed: int = 42,
) -> DataPrepTemplate:
    """Create a time-series template with lag and rolling window features.

    Args:
        template_id: Unique template ID.
        source_table: Input table.
        target_table: Output table.
        entity_id: The specific entity to build the series for.
        date_col: Date column. Default: ``"date"``.
        target_col: Target column. Default: ``"target"``.
        lag_periods: List of lag periods to generate. Default: ``[1, 3, 6]``.
        rolling_windows: Rolling mean window sizes. Default: ``[3, 6, 12]``.
        feature_columns: Additional raw feature columns.
        max_rows: Row cap. Default: 0.
        seed: Random seed. Default: 42.

    Returns:
        :class:`DataPrepTemplate`.
    """
    lags = lag_periods or [1, 3, 6]
    windows = rolling_windows or [3, 6, 12]
    transforms: list[ColumnTransform] = []

    for period in lags:
        transforms.append(ColumnTransform(
            column_name=target_col,
            transform_type="lag",
            params={"periods": period},
        ))
    for window in windows:
        transforms.append(ColumnTransform(
            column_name=target_col,
            transform_type="rolling_mean",
            params={"window": window},
        ))

    return DataPrepTemplate(
        template_id=template_id,
        name=f"Time Series: {source_table} ({entity_id})",
        template_type=TemplateType.TIME_SERIES,
        source_table=source_table,
        target_table=target_table,
        observation_date_col=date_col,
        entity_id_col="entity_id",
        target_col=target_col,
        feature_columns=feature_columns or [],
        transforms=transforms,
        filters=[f"entity_id == '{entity_id}'"],
        max_rows=max_rows,
        seed=seed,
    )


def event_history_template(
    template_id: str,
    source_table: str,
    target_table: str,
    entity_id_col: str = "entity_id",
    event_date_col: str = "event_date",
    event_type_col: str = "event_type",
    lookback_days: int = 365,
    feature_columns: list[str] | None = None,
    seed: int = 42,
) -> DataPrepTemplate:
    """Create an event-history template for time-to-event modelling.

    Args:
        template_id: Unique template ID.
        source_table: Input table.
        target_table: Output table.
        entity_id_col: Entity column.
        event_date_col: Event date column.
        event_type_col: Event type column.
        lookback_days: History lookback window in days. Default: 365.
        feature_columns: Feature columns.
        seed: Random seed. Default: 42.

    Returns:
        :class:`DataPrepTemplate`.
    """
    return DataPrepTemplate(
        template_id=template_id,
        name=f"Event History: {source_table}",
        template_type=TemplateType.EVENT_HISTORY,
        source_table=source_table,
        target_table=target_table,
        observation_date_col=event_date_col,
        entity_id_col=entity_id_col,
        feature_columns=feature_columns or [],
        time_window_days=lookback_days,
        seed=seed,
    )


def cohort_snapshot_template(
    template_id: str,
    source_table: str,
    target_table: str,
    cohort_date: str,
    outcome_date: str,
    entity_id_col: str = "entity_id",
    target_col: str = "default_flag",
    feature_columns: list[str] | None = None,
    filters: list[str] | None = None,
    seed: int = 42,
) -> DataPrepTemplate:
    """Create a cohort snapshot template (origination cohort with outcome at fixed horizon).

    Args:
        template_id: Unique template ID.
        source_table: Input table.
        target_table: Output table.
        cohort_date: Cohort origination date (ISO format).
        outcome_date: Outcome observation date (ISO format).
        entity_id_col: Entity column.
        target_col: Target column.
        feature_columns: Feature columns.
        filters: Additional filter expressions.
        seed: Random seed.

    Returns:
        :class:`DataPrepTemplate`.
    """
    return DataPrepTemplate(
        template_id=template_id,
        name=f"Cohort Snapshot: {source_table} cohort={cohort_date} outcome={outcome_date}",
        template_type=TemplateType.COHORT_SNAPSHOT,
        source_table=source_table,
        target_table=target_table,
        entity_id_col=entity_id_col,
        target_col=target_col,
        feature_columns=feature_columns or [],
        filters=[f"cohort_date == '{cohort_date}'"] + (filters or []),
        observation_period=f"{cohort_date}/{outcome_date}",
        seed=seed,
        metadata={"cohort_date": cohort_date, "outcome_date": outcome_date},
    )
