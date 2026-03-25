"""Unit tests for runtime config enums."""

import pytest

from sdk.platform_core.runtime.config_models.enums import (
    AccessModeEnum,
    ActorRoleEnum,
    DomainEnum,
    EnvironmentNameEnum,
    InteractionModeEnum,
    RetryModeEnum,
    ReviewMissingBehaviorEnum,
    RuntimeModeEnum,
    StageClassEnum,
    StaleStateBehaviorEnum,
    TokenModeEnum,
    UIModeEnum,
    UnknownBehaviorEnum,
)


class TestAccessModeEnum:
    def test_all_values_unique(self) -> None:
        values = [e.value for e in AccessModeEnum]
        assert len(values) == len(set(values))

    def test_string_coercion(self) -> None:
        assert AccessModeEnum("READ_ONLY") is AccessModeEnum.READ_ONLY

    def test_invalid_value_raises(self) -> None:
        with pytest.raises(ValueError):
            AccessModeEnum("UNKNOWN")


class TestUIModeEnum:
    def test_all_values_unique(self) -> None:
        values = [e.value for e in UIModeEnum]
        assert len(values) == len(set(values))

    def test_three_panel_value(self) -> None:
        assert UIModeEnum.THREE_PANEL_REVIEW_WORKSPACE.value == "three_panel_review_workspace"


class TestInteractionModeEnum:
    def test_edit_and_finalize(self) -> None:
        assert InteractionModeEnum.EDIT_AND_FINALIZE.value == "edit_and_finalize"

    def test_invalid_raises(self) -> None:
        with pytest.raises(ValueError):
            InteractionModeEnum("garbage")


class TestTokenModeEnum:
    def test_four_modes(self) -> None:
        assert len(list(TokenModeEnum)) == 4

    def test_routing_only(self) -> None:
        assert TokenModeEnum.ROUTING_ONLY.value == "routing_only"


class TestEnvironmentNameEnum:
    def test_dev_prod_uat(self) -> None:
        assert EnvironmentNameEnum.DEV.value == "dev"
        assert EnvironmentNameEnum.PROD.value == "prod"
        assert EnvironmentNameEnum.UAT.value == "uat"


class TestStageClassEnum:
    def test_all_class_names(self) -> None:
        expected = {"build", "review", "selection", "approval", "monitoring",
                    "remediation", "validation", "bootstrap", "recovery"}
        actual = {e.value for e in StageClassEnum}
        assert actual == expected


class TestActorRoleEnum:
    def test_system_role(self) -> None:
        assert ActorRoleEnum.SYSTEM.value == "system"

    def test_all_roles_unique(self) -> None:
        values = [e.value for e in ActorRoleEnum]
        assert len(values) == len(set(values))


class TestRetryModeEnum:
    def test_exponential_backoff(self) -> None:
        assert RetryModeEnum.EXPONENTIAL_BACKOFF.value == "exponential_backoff"

    def test_none_mode(self) -> None:
        assert RetryModeEnum.NONE.value == "none"


class TestBehaviorEnums:
    def test_unknown_behavior_fail(self) -> None:
        assert UnknownBehaviorEnum.FAIL.value == "fail"

    def test_stale_state_auto_resume(self) -> None:
        assert StaleStateBehaviorEnum.AUTO_RESUME.value == "auto_resume"

    def test_review_missing_block(self) -> None:
        assert ReviewMissingBehaviorEnum.BLOCK.value == "block"

    def test_review_missing_escalate(self) -> None:
        assert ReviewMissingBehaviorEnum.ESCALATE.value == "escalate"
