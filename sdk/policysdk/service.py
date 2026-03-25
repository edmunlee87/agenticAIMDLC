"""PolicyService — policy pack loader, metric evaluation, and governance overlay engine.

The public interface:
- :meth:`load_policy_pack`: register a :class:`PolicyPack` for a domain.
- :meth:`evaluate_metric_set`: evaluate all applicable rules against a metrics dict.
- :meth:`detect_breaches`: return only breach findings from an evaluation.
- :meth:`get_stage_controls`: rules applicable to a given stage.
- :meth:`requires_human_review`: True if any mandatory-review rule triggered.
- :meth:`get_approval_requirements`: return roles required to approve a stage.
- :meth:`can_actor_approve`: check actor role against approval requirements.
- :meth:`should_escalate`: True if severity threshold requires escalation.
- :meth:`is_waivable`: True if all breaches in an evaluation are waivable.
- :meth:`health_check`: service health statistics.

Governance overlay engine applies rules in order:
1. Default rules (always applied).
2. Stage-specific rules (stage_name in rule's stage_scope, or scope empty).
3. Role-specific overrides (actor_role in rule's role_scope, or scope empty).
4. Environment-aware strictness (prod enforces all gates; dev may relax).

All evaluations are emitted to observability.
"""

from __future__ import annotations

import logging
import operator as _op
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sdk.auditsdk.audit_service import AuditService
from sdk.observabilitysdk.observability_service import ObservabilityService
from sdk.platform_core.runtime.config_models.bundle import RuntimeConfigBundle
from sdk.platform_core.schemas.base_result import BaseResult
from sdk.platform_core.schemas.enums import PolicyResultEnum, SeverityEnum
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider
from sdk.platform_core.services.base_service import BaseService
from sdk.policysdk.models import (
    PolicyEvaluationResult,
    PolicyFinding,
    PolicyPack,
    PolicyRule,
    PolicyRuleType,
)

_SDK_NAME = "policysdk"
logger = logging.getLogger(f"platform.{_SDK_NAME}")

# Roles authorised to approve each severity tier (platform RoleEnum values).
_APPROVAL_AUTHORITY: Dict[str, List[str]] = {
    SeverityEnum.LOW.value: ["developer", "validator", "approver"],
    SeverityEnum.MEDIUM.value: ["validator", "approver", "governance"],
    SeverityEnum.HIGH.value: ["approver", "governance"],
    SeverityEnum.CRITICAL.value: ["governance"],
}

_OPS: Dict[str, Any] = {
    "gte": _op.ge,
    "lte": _op.le,
    "gt": _op.gt,
    "lt": _op.lt,
    "eq": _op.eq,
    "ne": _op.ne,
}


class PolicyService(BaseService):
    """Policy evaluation and governance overlay engine.

    Args:
        bundle: Active :class:`RuntimeConfigBundle`.
        obs: :class:`ObservabilityService` for logging evaluations.
        audit: Optional :class:`AuditService` for waiver/exception records.
        environment: Deployment environment — affects strictness
            (``"production"`` enforces all gates; ``"dev"`` may relax some).

    Examples:
        >>> from sdk.policysdk.models import PolicyPack, PolicyRule, PolicyRuleType
        >>> from sdk.platform_core.schemas.enums import SeverityEnum
        >>> svc = PolicyService(bundle=bundle, obs=obs_svc)
        >>> pack = PolicyPack(
        ...     pack_id="pack_001", name="Credit Scorecard Pack",
        ...     rules=[PolicyRule(rule_id="r1", rule_type=PolicyRuleType.METRIC_THRESHOLD,
        ...                       metric_name="gini", threshold=0.3, operator="gte",
        ...                       severity=SeverityEnum.HIGH, is_blocking=True)],
        ... )
        >>> svc.load_policy_pack(pack)
        >>> result = svc.evaluate_metric_set({"gini": 0.25}, stage_name="model_fitting",
        ...                                   run_id="r1", project_id="p1")
    """

    def __init__(
        self,
        bundle: RuntimeConfigBundle,
        obs: ObservabilityService,
        audit: Optional[AuditService] = None,
        environment: str = "dev",
    ) -> None:
        super().__init__(sdk_name=_SDK_NAME)
        self._bundle = bundle
        self._obs = obs
        self._audit = audit
        self._environment = environment
        # domain -> PolicyPack (last registered wins per domain)
        self._packs: Dict[str, PolicyPack] = {}
        # evaluation_id -> PolicyEvaluationResult
        self._evaluations: Dict[str, PolicyEvaluationResult] = {}

    # ------------------------------------------------------------------
    # Pack management
    # ------------------------------------------------------------------

    def load_policy_pack(self, pack: PolicyPack) -> BaseResult:
        """Register a :class:`PolicyPack` for use in evaluations.

        Args:
            pack: Policy pack to register.

        Returns:
            :class:`BaseResult` with ``data["pack_id"]`` on success.
        """
        fn = "load_policy_pack"
        try:
            key = pack.domain or "generic"
            self._packs[key] = pack
            logger.info(
                "policysdk.pack_loaded: pack_id=%s domain=%s n_rules=%d",
                pack.pack_id,
                pack.domain,
                len(pack.rules),
            )
            result = self._build_result(
                fn,
                status="success",
                message=f"Policy pack '{pack.pack_id}' loaded for domain '{key}'.",
                data={"pack_id": pack.pack_id, "domain": key, "n_rules": len(pack.rules)},
                audit_hint="policy pack registered",
                observability_hint="policy.pack.loaded",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def get_pack(self, domain: str = "") -> Optional[PolicyPack]:
        """Return the policy pack for a domain, falling back to generic.

        Args:
            domain: Domain key.

        Returns:
            :class:`PolicyPack` or None if no pack is registered.
        """
        return self._packs.get(domain) or self._packs.get("generic")

    # ------------------------------------------------------------------
    # Metric evaluation
    # ------------------------------------------------------------------

    def evaluate_metric_set(
        self,
        metrics: Dict[str, float],
        stage_name: str,
        run_id: str,
        project_id: str,
        domain: str = "",
        actor_role: str = "",
        session_id: str = "",
        trace_id: str = "",
    ) -> BaseResult:
        """Evaluate all applicable rules against a metrics dict.

        Applies rules in order: default -> stage-scoped -> role-scoped ->
        environment-scoped.  Each rule is evaluated independently; findings
        are aggregated into a :class:`PolicyEvaluationResult`.

        Args:
            metrics: Dict of ``metric_name -> float`` values.
            stage_name: Active MDLC stage.
            run_id: Active run.
            project_id: Owning project.
            domain: Active domain (used to select policy pack).
            actor_role: Actor's active role.
            session_id: Active session.
            trace_id: Distributed trace ID.

        Returns:
            :class:`BaseResult` with ``data["evaluation"]`` (dict) on success.
        """
        fn = "evaluate_metric_set"
        self._log_start(fn, run_id=run_id, stage_name=stage_name)
        try:
            pack = self.get_pack(domain)
            rules = pack.rules if pack else []

            findings: List[PolicyFinding] = []
            for rule in rules:
                finding = self._evaluate_rule(rule, metrics, stage_name, actor_role)
                if finding is not None:
                    findings.append(finding)

            breaches = [f for f in findings if f.is_breach]
            warnings = [f for f in findings if not f.is_breach]
            n_breaches = len(breaches)
            n_warnings = len(warnings)

            requires_review = any(
                f.is_breach and _rule_by_id(rules, f.rule_id) is not None
                and _rule_by_id(rules, f.rule_id).is_mandatory_review  # type: ignore[union-attr]
                for f in breaches
            )
            is_blocking = any(
                f.is_breach and _rule_by_id(rules, f.rule_id) is not None
                and _rule_by_id(rules, f.rule_id).is_blocking  # type: ignore[union-attr]
                for f in breaches
            )

            if n_breaches == 0:
                outcome = PolicyResultEnum.PASS
            elif is_blocking:
                outcome = PolicyResultEnum.BLOCKED
            else:
                outcome = PolicyResultEnum.BREACH

            evaluation_id = IDFactory.correlation_id()
            evaluation = PolicyEvaluationResult(
                evaluation_id=evaluation_id,
                run_id=run_id,
                project_id=project_id,
                stage_name=stage_name,
                timestamp=TimeProvider.now(),
                outcome=outcome,
                findings=findings,
                n_breaches=n_breaches,
                n_warnings=n_warnings,
                requires_human_review=requires_review,
                blocking=is_blocking,
            )
            self._evaluations[evaluation_id] = evaluation

            # Emit observability event
            obs_status = "blocked" if is_blocking else ("breach" if n_breaches else "pass")
            self._obs.write_event(
                event_type="policy.evaluation.completed",
                stage_name=stage_name,
                run_id=run_id,
                project_id=project_id,
                session_id=session_id or None,
                actor="system",
                status=obs_status,
                governance_gate_hit=bool(n_breaches),
                payload={
                    "evaluation_id": evaluation_id,
                    "outcome": _enum_str(outcome),
                    "n_breaches": n_breaches,
                    "requires_review": requires_review,
                    "blocking": is_blocking,
                },
            )

            result = self._build_result(
                fn,
                status="success",
                message=(
                    f"Policy evaluation '{_enum_str(outcome)}' for stage '{stage_name}': "
                    f"{n_breaches} breach(es), {n_warnings} warning(s)."
                ),
                data={"evaluation": evaluation.to_dict(), "evaluation_id": evaluation_id},
                audit_hint="policy evaluation completed",
                observability_hint="policy.evaluation.completed",
                workflow_hint=f"policy:{_enum_str(outcome)} stage:{stage_name}",
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        self._log_finish(fn, result)
        return result

    def detect_breaches(
        self,
        metrics: Dict[str, float],
        stage_name: str,
        run_id: str,
        project_id: str,
        domain: str = "",
    ) -> BaseResult:
        """Return only breach findings from an evaluation.

        Args:
            metrics: Metric dict.
            stage_name: Active stage.
            run_id: Active run.
            project_id: Owning project.
            domain: Active domain.

        Returns:
            :class:`BaseResult` with ``data["breaches"]`` (list of finding dicts).
        """
        fn = "detect_breaches"
        try:
            eval_r = self.evaluate_metric_set(
                metrics, stage_name=stage_name, run_id=run_id,
                project_id=project_id, domain=domain,
            )
            if not eval_r.is_success:
                return eval_r
            eval_dict = eval_r.data["evaluation"]
            breaches = [f for f in eval_dict.get("findings", []) if f.get("is_breach")]
            result = self._build_result(
                fn,
                status="success",
                message=f"{len(breaches)} breach(es) detected for stage '{stage_name}'.",
                data={
                    "breaches": breaches,
                    "n_breaches": len(breaches),
                    "evaluation_id": eval_r.data["evaluation_id"],
                },
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    # ------------------------------------------------------------------
    # Policy gate queries
    # ------------------------------------------------------------------

    def get_stage_controls(self, stage_name: str, domain: str = "") -> BaseResult:
        """Return control settings derived from all rules applicable to a stage.

        Returns a summary dict with: ``review_required``, ``approval_required``,
        ``audit_required``, ``auto_continue_allowed``, and the list of applicable rules.

        Args:
            stage_name: Stage name.
            domain: Active domain.

        Returns:
            :class:`BaseResult` with ``data["controls"]`` dict.
        """
        fn = "get_stage_controls"
        try:
            pack = self.get_pack(domain)
            rules = [
                r for r in (pack.rules if pack else [])
                if not r.stage_scope or stage_name in r.stage_scope
            ]
            review_required = any(r.is_mandatory_review for r in rules)
            approval_required = any(
                r.rule_type == PolicyRuleType.APPROVAL_AUTHORITY for r in rules
            )
            audit_required = any(r.is_blocking for r in rules)
            auto_continue_allowed = not any(r.is_blocking or r.is_mandatory_review for r in rules)

            result = self._build_result(
                fn,
                status="success",
                message=f"{len(rules)} rule(s) applicable to stage '{stage_name}'.",
                data={
                    "controls": {
                        "stage_name": stage_name,
                        "review_required": review_required,
                        "approval_required": approval_required,
                        "audit_required": audit_required,
                        "auto_continue_allowed": auto_continue_allowed,
                    },
                    "rules": [r.to_dict() for r in rules],
                    "n_rules": len(rules),
                },
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def requires_human_review(
        self,
        metrics: Dict[str, float],
        stage_name: str,
        domain: str = "",
    ) -> bool:
        """Return True if the metrics trigger any mandatory-review rule.

        Args:
            metrics: Metric dict.
            stage_name: Active stage.
            domain: Active domain.

        Returns:
            True if HITL review is required.
        """
        pack = self.get_pack(domain)
        if not pack:
            return False
        for rule in pack.rules:
            if not rule.is_mandatory_review:
                continue
            if rule.stage_scope and stage_name not in rule.stage_scope:
                continue
            finding = self._evaluate_rule(rule, metrics, stage_name, actor_role="")
            if finding and finding.is_breach:
                return True
        return False

    def get_approval_requirements(self, max_severity: SeverityEnum) -> BaseResult:
        """Return roles required to approve a finding of the given severity.

        Args:
            max_severity: Highest breach severity in the evaluation.

        Returns:
            :class:`BaseResult` with ``data["required_roles"]`` list.
        """
        fn = "get_approval_requirements"
        try:
            sev_val = _enum_str(max_severity)
            roles = list(_APPROVAL_AUTHORITY.get(sev_val, []))
            result = self._build_result(
                fn,
                status="success",
                message=f"Approval requirements for severity '{sev_val}': {roles}.",
                data={"required_roles": roles, "severity": sev_val},
            )
        except Exception as exc:
            result = self._handle_exception(fn, exc)
        return result

    def can_actor_approve(self, actor_role: str, max_severity: SeverityEnum) -> bool:
        """Return True if ``actor_role`` can approve findings of ``max_severity``.

        Args:
            actor_role: Actor's platform role string.
            max_severity: Highest breach severity.

        Returns:
            True when actor role is in the required approval roles for the severity.
        """
        sev_val = _enum_str(max_severity)
        return actor_role in _APPROVAL_AUTHORITY.get(sev_val, [])

    def should_escalate(self, evaluation: PolicyEvaluationResult) -> bool:
        """Return True if the evaluation severity requires escalation.

        Escalation is required when:
        - Any breach has CRITICAL severity (all environments).
        - Any breach has HIGH severity in production.

        Args:
            evaluation: Completed :class:`PolicyEvaluationResult`.

        Returns:
            True when escalation is required.
        """
        for finding in evaluation.findings:
            if not finding.is_breach:
                continue
            sev = _enum_str(finding.severity)
            if sev == SeverityEnum.CRITICAL.value:
                return True
            if sev == SeverityEnum.HIGH.value and self._environment == "production":
                return True
        return False

    def is_waivable(self, evaluation: PolicyEvaluationResult) -> bool:
        """Return True if ALL breach findings are individually waivable.

        Args:
            evaluation: Completed :class:`PolicyEvaluationResult`.

        Returns:
            True when every breach has ``is_waivable=True``.
        """
        return all(f.is_waivable for f in evaluation.findings if f.is_breach)

    def health_check(self) -> BaseResult:
        """Return service health statistics.

        Returns:
            :class:`BaseResult` with ``data["n_packs"]``, ``data["n_evaluations"]``,
            and ``data["environment"]``.
        """
        fn = "health_check"
        return self._build_result(
            fn,
            status="success",
            message="PolicyService healthy.",
            data={
                "status": "ok",
                "n_packs": len(self._packs),
                "n_evaluations": len(self._evaluations),
                "environment": self._environment,
                "domains": list(self._packs.keys()),
            },
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _evaluate_rule(
        self,
        rule: PolicyRule,
        metrics: Dict[str, float],
        stage_name: str,
        actor_role: str,
    ) -> Optional[PolicyFinding]:
        """Evaluate a single rule against a metrics dict.

        Args:
            rule: Rule to evaluate.
            metrics: Metrics being evaluated.
            stage_name: Active stage (for scope filtering).
            actor_role: Actor role (for scope filtering).

        Returns:
            :class:`PolicyFinding` if the rule applies, or None if filtered out.
        """
        # Stage scope filter.
        if rule.stage_scope and stage_name not in rule.stage_scope:
            return None
        # Role scope filter.
        if rule.role_scope and actor_role and actor_role not in rule.role_scope:
            return None
        # Environment scope filter.
        if rule.environment_scope and self._environment not in rule.environment_scope:
            return None

        is_breach = False
        observed_value: Optional[float] = None

        if rule.rule_type == PolicyRuleType.METRIC_THRESHOLD and rule.metric_name:
            observed_value = metrics.get(rule.metric_name)
            if observed_value is not None and rule.threshold is not None:
                op_fn = _OPS.get(rule.operator, _op.ge)
                # Rule PASSES when metric satisfies the threshold; breach when it fails.
                is_breach = not op_fn(observed_value, rule.threshold)
            elif observed_value is None:
                # Missing metric — breach for mandatory/blocking rules.
                is_breach = rule.is_blocking or rule.is_mandatory_review
        elif rule.rule_type == PolicyRuleType.MANDATORY_REVIEW:
            # Process rule: always fires (no metric comparison needed).
            is_breach = True

        description = rule.description or (
            f"Rule '{rule.rule_id}': metric '{rule.metric_name}' "
            f"(observed={observed_value}) vs threshold {rule.threshold} ({rule.operator})"
        )
        return PolicyFinding(
            finding_id=IDFactory.correlation_id(),
            rule_id=rule.rule_id,
            rule_type=rule.rule_type,
            severity=rule.severity,
            description=description,
            is_breach=is_breach,
            observed_value=observed_value,
            threshold_value=rule.threshold,
            is_waivable=rule.is_waivable,
            stage_name=stage_name,
            metric_name=rule.metric_name,
            evaluated_at=TimeProvider.now(),
        )


def _rule_by_id(rules: List[PolicyRule], rule_id: str) -> Optional[PolicyRule]:
    return next((r for r in rules if r.rule_id == rule_id), None)


def _enum_str(v: Any) -> str:
    """Safely extract string value from enum or plain string."""
    return v.value if hasattr(v, "value") else str(v)
