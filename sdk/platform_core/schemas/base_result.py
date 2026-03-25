"""BaseResult and ValidationResultBase: standard return contracts for all SDK methods.

Every material SDK public method returns BaseResult (or ValidationResultBase for
validation-style methods). Controllers normalize to StandardResponseEnvelope at
the workflow boundary.

Design rules per enhancement v0.2:
- All material methods return BaseResult or ValidationResult.
- Every important method includes agent_hint, workflow_hint, audit_hint, observability_hint.
- Controller boundary returns StandardResponseEnvelope with audit_ref and event_ref.
"""

from typing import Any, Dict, List, Optional

from .base_model_base import BaseModelBase


class BaseResult(BaseModelBase):
    """Standard return contract for all SDK public methods.

    Attributes:
        status: Outcome status. One of: success, warning, failure, blocked, pending.
        message: Human-readable summary of the result.
        sdk_name: Name of the SDK producing this result.
        function_name: Name of the function producing this result.
        data: Primary result payload (SDK-specific structure).
        warnings: Non-blocking issues to surface.
        errors: Blocking errors encountered.
        artifacts_created: Artifact IDs created as part of this operation.
        references: Cross-references (review_id, audit_id, event_id, etc.).
        agent_hint: Guidance for the orchestrating agent on what to do next.
        workflow_hint: Guidance on workflow state changes to apply.
        audit_hint: Instructions for audit record creation.
        observability_hint: Instructions for observability event emission.
    """

    status: str = "success"
    message: str = ""
    sdk_name: str = ""
    function_name: str = ""
    data: Optional[Dict[str, Any]] = None
    warnings: List[str] = []
    errors: List[str] = []
    artifacts_created: List[str] = []
    references: Dict[str, str] = {}

    # Agent-interpretable hints
    agent_hint: str = ""
    workflow_hint: str = ""
    audit_hint: str = ""
    observability_hint: str = ""

    @property
    def is_success(self) -> bool:
        """Return True if status is 'success'."""
        return self.status == "success"

    @property
    def has_warnings(self) -> bool:
        """Return True if any warnings are present."""
        return len(self.warnings) > 0

    @property
    def requires_human_review(self) -> bool:
        """Return True if agent_hint indicates a review is needed."""
        return "review" in self.agent_hint.lower() or self.status == "blocked"

    @property
    def recommended_next_action(self) -> Optional[str]:
        """Extract the first recommended action from agent_hint if present."""
        if self.agent_hint:
            return self.agent_hint.split(".")[0].strip()
        return None

    @property
    def recommended_next_stage(self) -> Optional[str]:
        """Extract the recommended next stage from workflow_hint if present."""
        if "next_stage=" in self.workflow_hint:
            try:
                return self.workflow_hint.split("next_stage=")[1].split()[0]
            except IndexError:
                return None
        return None

    def to_envelope_dict(self) -> Dict[str, Any]:
        """Return a dict suitable for embedding in a StandardResponseEnvelope."""
        return {
            "status": self.status,
            "message": self.message,
            "sdk_name": self.sdk_name,
            "function_name": self.function_name,
            "data": self.data,
            "warnings": self.warnings,
            "errors": self.errors,
            "artifacts_created": self.artifacts_created,
            "references": self.references,
        }


class ValidationResultBase(BaseResult):
    """Extended return contract for validation-style methods.

    Adds is_valid, failed_rules, passed_rules, and derived summary properties.

    Attributes:
        is_valid: Overall validation outcome.
        failed_rules: List of rule identifiers that failed.
        passed_rules: List of rule identifiers that passed.
        rule_details: Optional per-rule detail dicts.
    """

    is_valid: bool = True
    failed_rules: List[str] = []
    passed_rules: List[str] = []
    rule_details: Optional[List[Dict[str, Any]]] = None

    @property
    def fail_count(self) -> int:
        """Return the number of failed rules."""
        return len(self.failed_rules)

    @property
    def pass_count(self) -> int:
        """Return the number of passed rules."""
        return len(self.passed_rules)

    @property
    def validation_summary(self) -> str:
        """Return a concise human-readable validation summary.

        Returns:
            Summary string like "3/5 rules passed, 2 failed."
        """
        total = self.fail_count + self.pass_count
        return f"{self.pass_count}/{total} rules passed, {self.fail_count} failed."

    @property
    def requires_human_review(self) -> bool:
        """Return True if validation failed or status indicates blocking."""
        return not self.is_valid or super().requires_human_review
