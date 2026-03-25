"""validationsdk.conclusion_engine -- derives a ValidationConclusion from findings.

Rules (in priority order):
1. Any OPEN CRITICAL finding that requires_remediation → FAIL.
2. Any OPEN finding that requires_remediation and is HIGH → FAIL (in production mode).
3. Open HIGH/CRITICAL findings present but waivable → PASS_WITH_CONDITIONS.
4. Evidence completeness < threshold → INCONCLUSIVE.
5. All findings CLOSED / REMEDIATED / WAIVED → PASS_UNCONDITIONAL.
6. Open informational / medium findings only → PASS_WITH_CONDITIONS.
"""

from __future__ import annotations

import logging
from typing import Any

from validationsdk.models import (
    ConclusionCategory,
    FindingStatus,
    FindingSeverity,
    ValidationConclusion,
    ValidationFinding,
)

logger = logging.getLogger(__name__)

# Default thresholds (can be overridden per invocation)
_DEFAULT_EVIDENCE_COMPLETENESS_THRESHOLD = 0.6
_DEFAULT_STRICT_MODE = False


class ConclusionEngine:
    """Derives a :class:`~validationsdk.models.ValidationConclusion` from findings.

    Args:
        evidence_completeness_threshold: Minimum completeness score for
            a non-inconclusive conclusion. Default: 0.6.
        strict_mode: When True, HIGH findings with requires_remediation also
            cause FAIL (not just CRITICAL). Default: False.
    """

    def __init__(
        self,
        evidence_completeness_threshold: float = _DEFAULT_EVIDENCE_COMPLETENESS_THRESHOLD,
        strict_mode: bool = _DEFAULT_STRICT_MODE,
    ) -> None:
        self._threshold = evidence_completeness_threshold
        self._strict = strict_mode

    def derive(
        self,
        conclusion_id: str,
        scope_id: str,
        run_id: str,
        project_id: str,
        findings: list[ValidationFinding],
        evidence_completeness_score: float,
        concluded_by: str = "",
        audit_id: str = "",
        extra_metadata: dict[str, Any] | None = None,
    ) -> ValidationConclusion:
        """Derive a conclusion from the current finding set.

        Args:
            conclusion_id: Unique conclusion identifier.
            scope_id: Scope being concluded.
            run_id: MDLC run.
            project_id: Project.
            findings: All findings in scope.
            evidence_completeness_score: Pre-computed completeness score (0.0–1.0).
            concluded_by: Actor drawing the conclusion.
            audit_id: Backing audit record ID.
            extra_metadata: Optional extra metadata.

        Returns:
            Derived :class:`ValidationConclusion`.
        """
        open_findings = [f for f in findings if f.status == FindingStatus.OPEN]
        critical_open = [
            f for f in open_findings
            if f.severity == FindingSeverity.CRITICAL and f.requires_remediation
        ]
        high_open_requiring_remed = [
            f for f in open_findings
            if f.severity == FindingSeverity.HIGH and f.requires_remediation
        ]
        blocking_any = [f for f in open_findings if f.requires_remediation]

        conditions: list[str] = []
        category: ConclusionCategory

        if critical_open:
            category = ConclusionCategory.FAIL
            conditions = [f"Critical finding '{f.finding_id}' requires remediation." for f in critical_open]
        elif self._strict and high_open_requiring_remed:
            category = ConclusionCategory.FAIL
            conditions = [f"High finding '{f.finding_id}' requires remediation (strict mode)." for f in high_open_requiring_remed]
        elif evidence_completeness_score < self._threshold:
            category = ConclusionCategory.INCONCLUSIVE
            conditions = [f"Evidence completeness {evidence_completeness_score:.0%} below threshold {self._threshold:.0%}."]
        elif blocking_any:
            category = ConclusionCategory.PASS_WITH_CONDITIONS
            conditions = [f"Finding '{f.finding_id}' ({f.severity.value}) requires remediation." for f in blocking_any]
        elif open_findings:
            category = ConclusionCategory.PASS_WITH_CONDITIONS
            conditions = [f"Finding '{f.finding_id}' ({f.severity.value}) remains open." for f in open_findings[:5]]
        else:
            category = ConclusionCategory.PASS_UNCONDITIONAL

        logger.info(
            "conclusion_engine.derived",
            extra={
                "conclusion_id": conclusion_id,
                "category": category,
                "open_count": len(open_findings),
                "critical_count": len(critical_open),
            },
        )

        return ValidationConclusion(
            conclusion_id=conclusion_id,
            scope_id=scope_id,
            run_id=run_id,
            project_id=project_id,
            category=category,
            summary=self._summary(category, open_findings),
            conditions=conditions,
            open_findings_count=len(open_findings),
            critical_findings_count=len(critical_open),
            concluded_by=concluded_by,
            audit_id=audit_id,
            evidence_completeness_score=evidence_completeness_score,
            metadata=extra_metadata or {},
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _summary(category: ConclusionCategory, open_findings: list[ValidationFinding]) -> str:
        if category == ConclusionCategory.PASS_UNCONDITIONAL:
            return "Validation passed with no open findings."
        if category == ConclusionCategory.PASS_WITH_CONDITIONS:
            return f"Validation passed with {len(open_findings)} open finding(s) to be addressed."
        if category == ConclusionCategory.FAIL:
            return f"Validation failed. {len(open_findings)} open finding(s) require remediation."
        if category == ConclusionCategory.INCONCLUSIVE:
            return "Validation inconclusive: insufficient evidence to draw a conclusion."
        return "Validation outcome escalated for senior review."
