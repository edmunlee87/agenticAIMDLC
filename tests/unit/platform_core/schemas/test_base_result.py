"""Unit tests for BaseResult and ValidationResultBase."""

import pytest

from sdk.platform_core.schemas.base_result import BaseResult, ValidationResultBase


class TestBaseResult:
    def test_defaults(self) -> None:
        result = BaseResult()
        assert result.status == "success"
        assert result.is_success is True
        assert result.has_warnings is False
        assert result.requires_human_review is False

    def test_failure_status(self) -> None:
        result = BaseResult(status="failure", message="Something went wrong")
        assert result.is_success is False

    def test_blocked_requires_human_review(self) -> None:
        result = BaseResult(status="blocked")
        assert result.requires_human_review is True

    def test_agent_hint_with_review_requires_human_review(self) -> None:
        result = BaseResult(agent_hint="Please create a review for the data quality issue.")
        assert result.requires_human_review is True

    def test_warnings(self) -> None:
        result = BaseResult(warnings=["minor issue"])
        assert result.has_warnings is True

    def test_recommended_next_action(self) -> None:
        result = BaseResult(agent_hint="Proceed to feature engineering. Then run selection.")
        assert result.recommended_next_action == "Proceed to feature engineering"

    def test_recommended_next_action_empty_hint(self) -> None:
        result = BaseResult()
        assert result.recommended_next_action is None

    def test_recommended_next_stage(self) -> None:
        result = BaseResult(workflow_hint="transition next_stage=feature_engineering done")
        assert result.recommended_next_stage == "feature_engineering"

    def test_recommended_next_stage_no_hint(self) -> None:
        result = BaseResult()
        assert result.recommended_next_stage is None

    def test_to_envelope_dict_keys(self) -> None:
        result = BaseResult(
            status="success",
            sdk_name="artifactsdk",
            function_name="write_artifact",
            data={"artifact_id": "abc123"},
        )
        d = result.to_envelope_dict()
        assert d["sdk_name"] == "artifactsdk"
        assert d["data"]["artifact_id"] == "abc123"
        assert "artifacts_created" in d

    def test_artifacts_created(self) -> None:
        result = BaseResult(artifacts_created=["artifact_001", "artifact_002"])
        assert len(result.artifacts_created) == 2

    def test_references(self) -> None:
        result = BaseResult(references={"review_id": "rev_001", "audit_id": "aud_001"})
        assert result.references["review_id"] == "rev_001"


class TestValidationResultBase:
    def test_defaults(self) -> None:
        result = ValidationResultBase()
        assert result.is_valid is True
        assert result.fail_count == 0
        assert result.pass_count == 0

    def test_validation_summary_all_pass(self) -> None:
        result = ValidationResultBase(
            is_valid=True,
            passed_rules=["rule_1", "rule_2"],
            failed_rules=[],
        )
        assert result.validation_summary == "2/2 rules passed, 0 failed."

    def test_validation_summary_mixed(self) -> None:
        result = ValidationResultBase(
            is_valid=False,
            passed_rules=["rule_1"],
            failed_rules=["rule_2", "rule_3"],
        )
        assert result.validation_summary == "1/3 rules passed, 2 failed."

    def test_invalid_requires_human_review(self) -> None:
        result = ValidationResultBase(is_valid=False)
        assert result.requires_human_review is True

    def test_valid_no_review(self) -> None:
        result = ValidationResultBase(is_valid=True, status="success")
        assert result.requires_human_review is False

    def test_fail_count(self) -> None:
        result = ValidationResultBase(failed_rules=["r1", "r2", "r3"])
        assert result.fail_count == 3

    def test_inherits_base_result_properties(self) -> None:
        result = ValidationResultBase(status="failure", is_valid=False)
        assert result.is_success is False
        assert result.requires_human_review is True

    def test_rule_details(self) -> None:
        result = ValidationResultBase(
            rule_details=[{"rule_id": "r1", "passed": False, "reason": "threshold exceeded"}]
        )
        assert result.rule_details is not None
        assert result.rule_details[0]["rule_id"] == "r1"
