"""PlatformBaseRules — enforces platform-level governance guardrails.

Enforces:
1. No silent finalization: every stage completion must have a registered artifact.
2. No implicit selection: version selection must be explicit before finalization.
3. All material actions logged: any action marked as material must emit an
   observability event AND write an audit record.

Used as a pre/post-hook by orchestrators before dispatching to controllers.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class BaseRuleViolation:
    """Represents a single base-rule violation.

    Attributes:
        rule_id: Rule identifier.
        description: Human-readable violation description.
        severity: ``"warning"`` or ``"error"`` (error = blocking).
        context: Additional context for debugging.
    """

    rule_id: str
    description: str
    severity: str = "error"
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BaseRulesResult:
    """Result of a platform base-rules check.

    Attributes:
        passed: True if no blocking violations exist.
        violations: List of all detected violations.
    """

    passed: bool
    violations: List[BaseRuleViolation] = field(default_factory=list)

    @property
    def blocking_violations(self) -> List[BaseRuleViolation]:
        """Return only error-severity (blocking) violations."""
        return [v for v in self.violations if v.severity == "error"]


class PlatformBaseRules:
    """Enforces platform-wide governance guardrails.

    Rules checked:
    - ``R001`` NO_SILENT_FINALIZATION: stages must not complete without artifacts.
    - ``R002`` NO_IMPLICIT_SELECTION: version selection must be explicit.
    - ``R003`` MATERIAL_ACTIONS_LOGGED: material actions must be observable + audited.

    Args:
        strict_mode: When True, warnings also block. Defaults to False.
    """

    RULE_NO_SILENT_FINALIZATION = "R001"
    RULE_NO_IMPLICIT_SELECTION = "R002"
    RULE_MATERIAL_ACTIONS_LOGGED = "R003"

    def __init__(self, strict_mode: bool = False) -> None:
        self._strict_mode = strict_mode

    def check_before_complete(
        self,
        *,
        stage_name: str,
        run_id: str,
        artifact_ids: List[str],
        selected_candidate_id: Optional[str] = None,
        requires_selection: bool = False,
    ) -> BaseRulesResult:
        """Check rules that must pass before a stage can be marked complete.

        Args:
            stage_name: Stage being completed.
            run_id: Active run identifier.
            artifact_ids: Artifact IDs registered for this stage.
            selected_candidate_id: Selected candidate version (if applicable).
            requires_selection: Whether this stage requires a selection.

        Returns:
            :class:`BaseRulesResult`.
        """
        violations: List[BaseRuleViolation] = []

        # R001: No silent finalization.
        if not artifact_ids:
            violations.append(
                BaseRuleViolation(
                    rule_id=self.RULE_NO_SILENT_FINALIZATION,
                    description=(
                        f"Stage '{stage_name}' cannot be completed without "
                        "at least one registered artifact. Register outputs "
                        "via artifactsdk before calling complete_stage."
                    ),
                    severity="error",
                    context={"stage_name": stage_name, "run_id": run_id},
                )
            )

        # R002: No implicit selection.
        if requires_selection and not selected_candidate_id:
            violations.append(
                BaseRuleViolation(
                    rule_id=self.RULE_NO_IMPLICIT_SELECTION,
                    description=(
                        f"Stage '{stage_name}' requires an explicit candidate "
                        "version selection. Call workflowsdk.select_candidate_version "
                        "before completing this stage."
                    ),
                    severity="error",
                    context={"stage_name": stage_name, "run_id": run_id},
                )
            )

        passed = not any(v.severity == "error" for v in violations)
        if self._strict_mode:
            passed = len(violations) == 0

        result = BaseRulesResult(passed=passed, violations=violations)
        if not result.passed:
            logger.warning(
                "platform_base_rules.check_failed",
                extra={
                    "stage_name": stage_name,
                    "run_id": run_id,
                    "violations": [v.rule_id for v in violations],
                },
            )
        return result

    def check_material_action_logged(
        self,
        *,
        action_name: str,
        run_id: str,
        stage_name: str,
        event_ref: Optional[str],
        audit_ref: Optional[str],
        is_material: bool = True,
    ) -> BaseRulesResult:
        """Check that a material action has both an event and audit record.

        Args:
            action_name: Name of the action.
            run_id: Active run identifier.
            stage_name: Stage the action occurred in.
            event_ref: Observability event ID (or None if not emitted).
            audit_ref: Audit record ID (or None if not written).
            is_material: Whether this action is considered material.

        Returns:
            :class:`BaseRulesResult`.
        """
        if not is_material:
            return BaseRulesResult(passed=True)

        violations: List[BaseRuleViolation] = []

        if not event_ref:
            violations.append(
                BaseRuleViolation(
                    rule_id=self.RULE_MATERIAL_ACTIONS_LOGGED,
                    description=(
                        f"Material action '{action_name}' at stage '{stage_name}' "
                        "must emit an observability event. Ensure observabilitysdk "
                        "is configured and write_event was called."
                    ),
                    severity="warning",
                    context={"action_name": action_name, "stage_name": stage_name, "run_id": run_id},
                )
            )

        if not audit_ref:
            violations.append(
                BaseRuleViolation(
                    rule_id=self.RULE_MATERIAL_ACTIONS_LOGGED,
                    description=(
                        f"Material action '{action_name}' at stage '{stage_name}' "
                        "must write an audit record. Ensure auditsdk is configured "
                        "and write_audit_record was called."
                    ),
                    severity="warning",
                    context={"action_name": action_name, "stage_name": stage_name, "run_id": run_id},
                )
            )

        passed = not any(v.severity == "error" for v in violations)
        if self._strict_mode:
            passed = len(violations) == 0

        return BaseRulesResult(passed=passed, violations=violations)
