"""Unit tests for PolicyService — policy pack, evaluation, and governance overlay."""

from __future__ import annotations

import pytest

from sdk.auditsdk.audit_service import AuditService
from sdk.observabilitysdk.observability_service import ObservabilityService
from sdk.platform_core.schemas.enums import PolicyResultEnum, SeverityEnum
from sdk.policysdk.models import (
    PolicyEvaluationResult,
    PolicyFinding,
    PolicyPack,
    PolicyRule,
    PolicyRuleType,
)
from sdk.policysdk.service import PolicyService

from tests.unit.workflowsdk.conftest import minimal_bundle  # noqa: F401


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def obs_svc() -> ObservabilityService:
    return ObservabilityService()


@pytest.fixture()
def svc(minimal_bundle, obs_svc: ObservabilityService) -> PolicyService:  # type: ignore[no-untyped-def]
    return PolicyService(bundle=minimal_bundle, obs=obs_svc, environment="dev")


@pytest.fixture()
def prod_svc(minimal_bundle, obs_svc: ObservabilityService) -> PolicyService:  # type: ignore[no-untyped-def]
    return PolicyService(bundle=minimal_bundle, obs=obs_svc, environment="production")


def _make_pack(
    pack_id: str = "pack_001",
    domain: str = "",
    rules: list | None = None,
) -> PolicyPack:
    return PolicyPack(
        pack_id=pack_id,
        name="Test Pack",
        domain=domain,
        rules=rules or [],
    )


def _gini_rule(
    threshold: float = 0.3,
    operator: str = "gte",
    severity: SeverityEnum = SeverityEnum.HIGH,
    is_blocking: bool = False,
    is_mandatory_review: bool = False,
    stage_scope: list | None = None,
) -> PolicyRule:
    return PolicyRule(
        rule_id="gini_min",
        rule_type=PolicyRuleType.METRIC_THRESHOLD,
        metric_name="gini",
        threshold=threshold,
        operator=operator,
        severity=severity,
        is_blocking=is_blocking,
        is_mandatory_review=is_mandatory_review,
        stage_scope=stage_scope or [],
    )


# ---------------------------------------------------------------------------
# TestLoadPolicyPack
# ---------------------------------------------------------------------------


class TestLoadPolicyPack:
    def test_load_pack_success(self, svc: PolicyService) -> None:
        pack = _make_pack()
        r = svc.load_policy_pack(pack)
        assert r.is_success
        assert r.data["pack_id"] == "pack_001"

    def test_get_pack_by_domain(self, svc: PolicyService) -> None:
        pack = _make_pack(domain="credit")
        svc.load_policy_pack(pack)
        retrieved = svc.get_pack("credit")
        assert retrieved is not None
        assert retrieved.pack_id == "pack_001"

    def test_generic_pack_fallback(self, svc: PolicyService) -> None:
        pack = _make_pack(domain="")  # generic
        svc.load_policy_pack(pack)
        assert svc.get_pack("credit") is not None  # falls back to generic
        assert svc.get_pack("") is not None

    def test_unknown_domain_returns_none(self, svc: PolicyService) -> None:
        assert svc.get_pack("unknown") is None

    def test_domain_pack_overrides_generic(self, svc: PolicyService) -> None:
        generic = _make_pack(pack_id="gen", domain="")
        specific = _make_pack(pack_id="spec", domain="credit")
        svc.load_policy_pack(generic)
        svc.load_policy_pack(specific)
        assert svc.get_pack("credit").pack_id == "spec"  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# TestEvaluateMetricSet
# ---------------------------------------------------------------------------


class TestEvaluateMetricSet:
    def test_pass_when_metric_above_threshold(self, svc: PolicyService) -> None:
        svc.load_policy_pack(_make_pack(rules=[_gini_rule(threshold=0.3)]))
        r = svc.evaluate_metric_set({"gini": 0.45}, "stage_a", "run_1", "proj_1")
        assert r.is_success
        ev = r.data["evaluation"]
        assert ev["outcome"] == PolicyResultEnum.PASS.value

    def test_breach_when_metric_below_threshold(self, svc: PolicyService) -> None:
        svc.load_policy_pack(_make_pack(rules=[_gini_rule(threshold=0.3)]))
        r = svc.evaluate_metric_set({"gini": 0.2}, "stage_a", "run_1", "proj_1")
        assert r.is_success
        ev = r.data["evaluation"]
        assert ev["outcome"] == PolicyResultEnum.BREACH.value
        assert ev["n_breaches"] == 1

    def test_blocked_when_blocking_rule_breached(self, svc: PolicyService) -> None:
        svc.load_policy_pack(
            _make_pack(rules=[_gini_rule(threshold=0.3, is_blocking=True)])
        )
        r = svc.evaluate_metric_set({"gini": 0.1}, "stage_a", "run_1", "proj_1")
        assert r.is_success
        ev = r.data["evaluation"]
        assert ev["outcome"] == PolicyResultEnum.BLOCKED.value
        assert ev["blocking"] is True

    def test_no_pack_returns_pass(self, svc: PolicyService) -> None:
        r = svc.evaluate_metric_set({"gini": 0.0}, "stage_a", "run_1", "proj_1")
        assert r.is_success
        ev = r.data["evaluation"]
        assert ev["outcome"] == PolicyResultEnum.PASS.value

    def test_multiple_rules_mixed_outcome(self, svc: PolicyService) -> None:
        rules = [
            _gini_rule(threshold=0.3, severity=SeverityEnum.HIGH),
            PolicyRule(
                rule_id="ks_min",
                rule_type=PolicyRuleType.METRIC_THRESHOLD,
                metric_name="ks",
                threshold=0.2,
                operator="gte",
                severity=SeverityEnum.MEDIUM,
            ),
        ]
        svc.load_policy_pack(_make_pack(rules=rules))
        r = svc.evaluate_metric_set(
            {"gini": 0.1, "ks": 0.35}, "stage_a", "run_1", "proj_1"
        )
        assert r.is_success
        ev = r.data["evaluation"]
        assert ev["n_breaches"] == 1  # only gini breached
        assert ev["outcome"] == PolicyResultEnum.BREACH.value

    def test_stage_scoped_rule_filters_out(self, svc: PolicyService) -> None:
        rule = _gini_rule(threshold=0.3, stage_scope=["model_fitting"])
        svc.load_policy_pack(_make_pack(rules=[rule]))
        # stage_a is not in scope — rule should not apply
        r = svc.evaluate_metric_set({"gini": 0.0}, "stage_a", "run_1", "proj_1")
        assert r.is_success
        ev = r.data["evaluation"]
        assert ev["n_breaches"] == 0

    def test_missing_metric_breaches_blocking_rule(self, svc: PolicyService) -> None:
        rule = _gini_rule(threshold=0.3, is_blocking=True)
        svc.load_policy_pack(_make_pack(rules=[rule]))
        r = svc.evaluate_metric_set({}, "stage_a", "run_1", "proj_1")
        assert r.is_success
        ev = r.data["evaluation"]
        assert ev["n_breaches"] == 1

    def test_mandatory_review_rule_always_fires(self, svc: PolicyService) -> None:
        rule = PolicyRule(
            rule_id="man_rev",
            rule_type=PolicyRuleType.MANDATORY_REVIEW,
            severity=SeverityEnum.HIGH,
            is_mandatory_review=True,
        )
        svc.load_policy_pack(_make_pack(rules=[rule]))
        r = svc.evaluate_metric_set({}, "stage_a", "run_1", "proj_1")
        ev = r.data["evaluation"]
        assert ev["requires_human_review"] is True
        assert ev["n_breaches"] == 1


# ---------------------------------------------------------------------------
# TestDetectBreaches
# ---------------------------------------------------------------------------


class TestDetectBreaches:
    def test_detect_breaches_only(self, svc: PolicyService) -> None:
        rules = [
            _gini_rule(threshold=0.3),
            PolicyRule(
                rule_id="ks_min",
                rule_type=PolicyRuleType.METRIC_THRESHOLD,
                metric_name="ks",
                threshold=0.2,
                operator="gte",
                severity=SeverityEnum.MEDIUM,
            ),
        ]
        svc.load_policy_pack(_make_pack(rules=rules))
        r = svc.detect_breaches({"gini": 0.1, "ks": 0.35}, "stage_a", "run_1", "proj_1")
        assert r.is_success
        assert r.data["n_breaches"] == 1
        assert all(b["is_breach"] for b in r.data["breaches"])


# ---------------------------------------------------------------------------
# TestGetStageControls
# ---------------------------------------------------------------------------


class TestGetStageControls:
    def test_controls_for_stage_with_rules(self, svc: PolicyService) -> None:
        rule = _gini_rule(threshold=0.3, is_mandatory_review=True, stage_scope=["stage_a"])
        svc.load_policy_pack(_make_pack(rules=[rule]))
        r = svc.get_stage_controls("stage_a")
        assert r.is_success
        controls = r.data["controls"]
        assert controls["review_required"] is True
        assert controls["auto_continue_allowed"] is False

    def test_controls_for_stage_with_no_rules(self, svc: PolicyService) -> None:
        rule = _gini_rule(stage_scope=["model_fitting"])
        svc.load_policy_pack(_make_pack(rules=[rule]))
        r = svc.get_stage_controls("stage_a")
        assert r.is_success
        controls = r.data["controls"]
        assert controls["review_required"] is False
        assert controls["auto_continue_allowed"] is True


# ---------------------------------------------------------------------------
# TestRequiresHumanReview
# ---------------------------------------------------------------------------


class TestRequiresHumanReview:
    def test_returns_true_for_mandatory_review_breach(self, svc: PolicyService) -> None:
        rule = _gini_rule(threshold=0.3, is_mandatory_review=True)
        svc.load_policy_pack(_make_pack(rules=[rule]))
        assert svc.requires_human_review({"gini": 0.1}, "stage_a") is True

    def test_returns_false_for_passing_metric(self, svc: PolicyService) -> None:
        rule = _gini_rule(threshold=0.3, is_mandatory_review=True)
        svc.load_policy_pack(_make_pack(rules=[rule]))
        assert svc.requires_human_review({"gini": 0.45}, "stage_a") is False

    def test_returns_false_when_no_pack(self, svc: PolicyService) -> None:
        assert svc.requires_human_review({"gini": 0.0}, "stage_a") is False


# ---------------------------------------------------------------------------
# TestApprovalRequirements
# ---------------------------------------------------------------------------


class TestApprovalRequirements:
    def test_high_severity_requires_approver(self, svc: PolicyService) -> None:
        r = svc.get_approval_requirements(SeverityEnum.HIGH)
        assert r.is_success
        assert "approver" in r.data["required_roles"]
        assert "governance" in r.data["required_roles"]

    def test_critical_severity_requires_governance(self, svc: PolicyService) -> None:
        r = svc.get_approval_requirements(SeverityEnum.CRITICAL)
        assert r.is_success
        assert "governance" in r.data["required_roles"]
        assert "developer" not in r.data["required_roles"]

    def test_can_actor_approve_validator_medium(self, svc: PolicyService) -> None:
        assert svc.can_actor_approve("validator", SeverityEnum.MEDIUM) is True

    def test_developer_cannot_approve_critical(self, svc: PolicyService) -> None:
        assert svc.can_actor_approve("developer", SeverityEnum.CRITICAL) is False


# ---------------------------------------------------------------------------
# TestEscalation
# ---------------------------------------------------------------------------


class TestEscalation:
    def _evaluation_with_severity(
        self, svc: PolicyService, severity: SeverityEnum, is_breach: bool = True
    ) -> PolicyEvaluationResult:
        rule = PolicyRule(
            rule_id="r1",
            rule_type=PolicyRuleType.METRIC_THRESHOLD,
            metric_name="gini",
            threshold=0.3,
            operator="gte",
            severity=severity,
        )
        svc.load_policy_pack(_make_pack(rules=[rule]))
        r = svc.evaluate_metric_set(
            {"gini": 0.1 if is_breach else 0.5}, "stage_a", "run_1", "proj_1"
        )
        eval_id = r.data["evaluation_id"]
        return svc._evaluations[eval_id]

    def test_should_escalate_critical(self, svc: PolicyService) -> None:
        ev = self._evaluation_with_severity(svc, SeverityEnum.CRITICAL)
        assert svc.should_escalate(ev) is True

    def test_should_not_escalate_medium_dev(self, svc: PolicyService) -> None:
        ev = self._evaluation_with_severity(svc, SeverityEnum.MEDIUM)
        assert svc.should_escalate(ev) is False

    def test_should_escalate_high_production(self, prod_svc: PolicyService) -> None:
        rule = PolicyRule(
            rule_id="r1",
            rule_type=PolicyRuleType.METRIC_THRESHOLD,
            metric_name="gini",
            threshold=0.3,
            operator="gte",
            severity=SeverityEnum.HIGH,
        )
        prod_svc.load_policy_pack(_make_pack(rules=[rule]))
        r = prod_svc.evaluate_metric_set({"gini": 0.1}, "stage_a", "run_1", "proj_1")
        ev = prod_svc._evaluations[r.data["evaluation_id"]]
        assert prod_svc.should_escalate(ev) is True

    def test_should_not_escalate_high_dev(self, svc: PolicyService) -> None:
        ev = self._evaluation_with_severity(svc, SeverityEnum.HIGH)
        assert svc.should_escalate(ev) is False


# ---------------------------------------------------------------------------
# TestWaiver
# ---------------------------------------------------------------------------


class TestWaiver:
    def test_all_waivable(self, svc: PolicyService) -> None:
        rule = PolicyRule(
            rule_id="r1",
            rule_type=PolicyRuleType.METRIC_THRESHOLD,
            metric_name="gini",
            threshold=0.3,
            operator="gte",
            severity=SeverityEnum.MEDIUM,
            is_waivable=True,
        )
        svc.load_policy_pack(_make_pack(rules=[rule]))
        r = svc.evaluate_metric_set({"gini": 0.1}, "stage_a", "run_1", "proj_1")
        ev = svc._evaluations[r.data["evaluation_id"]]
        assert svc.is_waivable(ev) is True

    def test_not_waivable_when_one_unwaivable(self, svc: PolicyService) -> None:
        rules = [
            PolicyRule(
                rule_id="r1",
                rule_type=PolicyRuleType.METRIC_THRESHOLD,
                metric_name="gini",
                threshold=0.3,
                operator="gte",
                severity=SeverityEnum.HIGH,
                is_waivable=False,
            ),
        ]
        svc.load_policy_pack(_make_pack(rules=rules))
        r = svc.evaluate_metric_set({"gini": 0.1}, "stage_a", "run_1", "proj_1")
        ev = svc._evaluations[r.data["evaluation_id"]]
        assert svc.is_waivable(ev) is False


# ---------------------------------------------------------------------------
# TestHealthCheck
# ---------------------------------------------------------------------------


class TestHealthCheck:
    def test_health_check(self, svc: PolicyService) -> None:
        svc.load_policy_pack(_make_pack())
        r = svc.health_check()
        assert r.is_success
        assert r.data["n_packs"] == 1
        assert r.data["environment"] == "dev"

    def test_health_check_tracks_evaluations(self, svc: PolicyService) -> None:
        svc.load_policy_pack(_make_pack())
        svc.evaluate_metric_set({"gini": 0.5}, "stage_a", "r1", "p1")
        r = svc.health_check()
        assert r.data["n_evaluations"] == 1


# ---------------------------------------------------------------------------
# TestPolicyRuleValidation
# ---------------------------------------------------------------------------


class TestPolicyRuleValidation:
    def test_invalid_operator_raises(self) -> None:
        import pytest
        with pytest.raises(Exception, match="Invalid operator"):
            PolicyRule(
                rule_id="r1",
                rule_type=PolicyRuleType.METRIC_THRESHOLD,
                operator="invalid_op",
            )

    def test_valid_operators(self) -> None:
        for op in ("gte", "lte", "gt", "lt", "eq", "ne"):
            rule = PolicyRule(
                rule_id=f"r_{op}",
                rule_type=PolicyRuleType.METRIC_THRESHOLD,
                operator=op,
            )
            assert rule.operator == op
