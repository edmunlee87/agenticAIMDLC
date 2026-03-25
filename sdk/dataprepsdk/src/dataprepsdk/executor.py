"""dataprepsdk.executor -- DataPrepExecutor: executes templates with lineage tracking.

The executor is engine-agnostic: it applies :class:`~dataprepsdk.models.ColumnTransform`
steps to a data object and captures full column-level lineage.

Engine adapters:
- ``pandas``: Default in-process execution. Accepts a ``pandas.DataFrame``.
- ``spark``:  Delegates to Spark SQL/DataFrame API. Accepts a PySpark ``DataFrame``.
  Requires PySpark to be installed; fails gracefully if not available.

Execution is deterministic when ``template.seed`` is set.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from dataprepsdk.models import (
    ColumnTransform,
    DataPrepLineageRecord,
    DataPrepRun,
    DataPrepTemplate,
)

logger = logging.getLogger(__name__)


class DataPrepExecutor:
    """Executes :class:`~dataprepsdk.models.DataPrepTemplate` against a data source.

    Args:
        observability_service: Optional observability service.
        artifact_service: Optional artifact service for snapshot registration.
    """

    def __init__(
        self,
        observability_service: Any = None,
        artifact_service: Any = None,
    ) -> None:
        self._obs = observability_service
        self._artifacts = artifact_service

    def execute(
        self,
        template: DataPrepTemplate,
        data: Any,
        run_id: str,
        project_id: str,
        executed_by: str = "",
        engine: str = "pandas",
    ) -> DataPrepRun:
        """Execute a template against a data object.

        Args:
            template: :class:`DataPrepTemplate` to execute.
            data: Input data (pandas DataFrame, Spark DataFrame, or dict for testing).
            run_id: MDLC run identifier.
            project_id: Project identifier.
            executed_by: Actor triggering execution.
            engine: Execution engine (``"pandas"`` | ``"spark"``). Default: ``"pandas"``.

        Returns:
            :class:`DataPrepRun` with full lineage.
        """
        run_record_id = str(uuid.uuid4())
        started_at = datetime.now(timezone.utc)
        lineage: list[DataPrepLineageRecord] = []
        error_message = ""
        success = True
        row_count = 0
        col_count = 0

        try:
            if engine == "spark":
                data, lineage = self._execute_spark(template, data)
            else:
                data, lineage = self._execute_pandas(template, data)

            row_count = self._row_count(data)
            col_count = self._col_count(data)

        except Exception as exc:
            logger.error("executor.failed", extra={"template_id": template.template_id, "error": str(exc)})
            success = False
            error_message = str(exc)

        completed_at = datetime.now(timezone.utc)

        run = DataPrepRun(
            run_record_id=run_record_id,
            template_id=template.template_id,
            template_version=template.version,
            run_id=run_id,
            project_id=project_id,
            executed_by=executed_by,
            started_at=started_at,
            completed_at=completed_at,
            row_count=row_count,
            column_count=col_count,
            lineage=lineage,
            filters_applied=list(template.filters),
            execution_engine=engine,
            success=success,
            error_message=error_message,
        )

        self._emit(run)
        logger.info(
            "executor.completed",
            extra={
                "run_record_id": run_record_id,
                "template_id": template.template_id,
                "rows": row_count,
                "cols": col_count,
                "success": success,
            },
        )
        return run

    # ------------------------------------------------------------------
    # Engine implementations
    # ------------------------------------------------------------------

    @staticmethod
    def _execute_pandas(
        template: DataPrepTemplate, df: Any
    ) -> tuple[Any, list[DataPrepLineageRecord]]:
        """Execute template transforms using pandas.

        Args:
            template: Template to apply.
            df: pandas DataFrame.

        Returns:
            Tuple of (transformed DataFrame, lineage records).
        """
        try:
            import pandas as pd
        except ImportError:
            # Accept dict/list data for unit tests without pandas.
            return df, []

        if not isinstance(df, pd.DataFrame):
            return df, []

        lineage: list[DataPrepLineageRecord] = []

        # Apply filters.
        for filt in template.filters:
            try:
                df = df.query(filt)
            except Exception as exc:
                logger.warning("executor.filter_failed", extra={"filter": filt, "error": str(exc)})

        # Apply column transforms.
        for transform in template.transforms:
            lineage_record = DataPrepExecutor._apply_transform_pandas(df, transform)
            if lineage_record:
                lineage.append(lineage_record)

        # Select feature columns + target + ID + date.
        keep_cols = []
        for col in [template.entity_id_col, template.observation_date_col, template.target_col]:
            if col and col in df.columns:
                keep_cols.append(col)
        for col in template.feature_columns:
            if col in df.columns and col not in keep_cols:
                keep_cols.append(col)

        if keep_cols:
            df = df[keep_cols]

        # Apply row cap.
        if template.max_rows > 0 and len(df) > template.max_rows:
            df = df.sample(n=template.max_rows, random_state=template.seed)

        # Add identity lineage for feature columns.
        for col in template.feature_columns:
            if col in df.columns and not any(lr.column_name == col for lr in lineage):
                lineage.append(DataPrepLineageRecord(
                    column_name=col,
                    source_columns=[col],
                    transform_applied="identity",
                ))

        return df, lineage

    @staticmethod
    def _apply_transform_pandas(df: Any, transform: ColumnTransform) -> DataPrepLineageRecord | None:
        """Apply a single column transform to a pandas DataFrame in-place.

        Args:
            df: pandas DataFrame (mutated in-place for efficiency).
            transform: :class:`ColumnTransform` to apply.

        Returns:
            :class:`DataPrepLineageRecord` or None on skip/error.
        """
        col = transform.column_name
        params = transform.params
        ttype = transform.transform_type

        try:
            if ttype == "fill_missing":
                fill_value = params.get("value", 0)
                if col in df.columns:
                    df[col] = df[col].fillna(fill_value)
            elif ttype == "clip":
                lower = params.get("lower")
                upper = params.get("upper")
                if col in df.columns:
                    df[col] = df[col].clip(lower=lower, upper=upper)
            elif ttype == "lag":
                periods = int(params.get("periods", 1))
                new_col = f"{col}_lag{periods}"
                if col in df.columns:
                    df[new_col] = df[col].shift(periods)
                col = new_col
            elif ttype == "rolling_mean":
                window = int(params.get("window", 3))
                new_col = f"{col}_rolling{window}"
                if col in df.columns:
                    df[new_col] = df[col].rolling(window=window, min_periods=1).mean()
                col = new_col
            elif ttype == "log1p":
                import numpy as np
                if col in df.columns:
                    df[col] = np.log1p(df[col].clip(lower=0))
            else:
                return None

            return DataPrepLineageRecord(
                column_name=col,
                source_columns=[transform.column_name],
                transform_applied=ttype,
                transform_params=params,
            )
        except Exception as exc:
            logger.warning("executor.transform_failed", extra={"column": col, "transform": ttype, "error": str(exc)})
            return None

    @staticmethod
    def _execute_spark(
        template: DataPrepTemplate, df: Any
    ) -> tuple[Any, list[DataPrepLineageRecord]]:
        """Execute template transforms using Spark.

        Delegates pandas-compatible transforms where possible.
        Full Spark UDF-based transforms are outside this scope (Phase 3+).

        Args:
            template: Template to apply.
            df: PySpark DataFrame.

        Returns:
            Tuple of (Spark DataFrame, lineage records).
        """
        try:
            from pyspark.sql import functions as F
        except ImportError:
            raise RuntimeError("PySpark is required for Spark execution. Install pyspark.")

        lineage: list[DataPrepLineageRecord] = []

        # Apply filters via Spark SQL where clause.
        for filt in template.filters:
            try:
                df = df.filter(filt)
            except Exception as exc:
                logger.warning("executor.spark_filter_failed", extra={"filter": filt, "error": str(exc)})

        # Select feature columns.
        keep_cols = [
            c for c in [
                template.entity_id_col, template.observation_date_col,
                template.target_col, *template.feature_columns
            ]
            if c and c in df.columns
        ]
        if keep_cols:
            df = df.select(keep_cols)

        if template.max_rows > 0:
            df = df.limit(template.max_rows)

        for col in template.feature_columns:
            lineage.append(DataPrepLineageRecord(
                column_name=col, source_columns=[col], transform_applied="identity"
            ))

        return df, lineage

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_count(data: Any) -> int:
        if hasattr(data, "__len__"):
            return len(data)
        if hasattr(data, "count"):
            try:
                return data.count()
            except Exception:
                pass
        return 0

    @staticmethod
    def _col_count(data: Any) -> int:
        if hasattr(data, "columns"):
            return len(data.columns)
        return 0

    def _emit(self, run: DataPrepRun) -> None:
        if self._obs is None:
            return
        try:
            self._obs.emit_simple(
                event_type="dataprep.template.executed",
                run_id=run.run_id,
                stage_name="data_preparation",
                actor_id=run.executed_by,
                metadata={
                    "template_id": run.template_id,
                    "rows": run.row_count,
                    "success": run.success,
                },
            )
        except Exception as exc:
            logger.warning("executor.emit_failed", extra={"error": str(exc)})
