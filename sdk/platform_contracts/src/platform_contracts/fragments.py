"""Common Pydantic fragment models used across all payload schemas.

Fragments are embedded in payload models and map 1:1 to the JSON Schema
``$ref`` definitions in ``configs/schemas/``. Every schema in the MDLC
framework embeds at least :class:`ActorRecord` and :class:`PolicyContextRef`.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ActorRecord(BaseModel):
    """Identity and delegation chain of the actor who triggered an event.

    Args:
        actor_id: Unique, stable identifier for the actor (user or system).
        role: Active role at the time of the event (see :class:`~platform_contracts.enums.RoleType`).
        display_name: Human-readable name for audit reports.
        delegation_chain: Ordered list of actor_ids in the delegation chain
            (index 0 = original delegator, last = actual actor).
    """

    actor_id: str
    role: str
    display_name: str = ""
    delegation_chain: list[str] = Field(default_factory=list)

    model_config = {"frozen": True}


class PolicyContextRef(BaseModel):
    """Snapshot of the active policy context at the time of an event.

    Args:
        policy_mode: Mode label (e.g. ``"strict"``, ``"advisory"``).
        environment: Deployment environment (see :class:`~platform_contracts.enums.EnvironmentType`).
        domain: Business domain (e.g. ``"credit_risk"``).
        active_policy_pack_id: Identifier of the loaded policy pack.
    """

    policy_mode: str = ""
    environment: str = ""
    domain: str = ""
    active_policy_pack_id: str = ""

    model_config = {"frozen": True}


class PolicyViolationRef(BaseModel):
    """Reference to an active policy violation.

    Args:
        violation_id: Unique violation identifier.
        rule_ref: Policy rule identifier.
        severity: Violation severity level.
        detected_at: ISO-8601 timestamp when detected.
        waiver_id: Active waiver ID if the violation is waived.
    """

    violation_id: str
    rule_ref: str
    severity: str
    detected_at: datetime | None = None
    waiver_id: str = ""

    model_config = {"frozen": True}


class PolicyFindingRef(BaseModel):
    """Lightweight finding reference embedded in candidate versions and responses.

    Args:
        finding_id: Unique finding identifier.
        severity: Severity level.
        rule_ref: Source policy rule identifier.
        description: Human-readable description of the finding.
    """

    finding_id: str
    severity: str
    rule_ref: str
    description: str = ""

    model_config = {"frozen": True}


class GovernanceFlags(BaseModel):
    """Boolean governance state flags carried in workflow state and runtime context.

    Args:
        requires_escalation: Stage cannot proceed without escalation.
        has_open_policy_violations: At least one active violation exists.
        has_active_waiver: At least one violation has an active waiver.
        is_in_remediation: Workflow is currently in a remediation sub-cycle.
    """

    requires_escalation: bool = False
    has_open_policy_violations: bool = False
    has_active_waiver: bool = False
    is_in_remediation: bool = False

    model_config = {"frozen": True}


class ArtifactRef(BaseModel):
    """Lightweight reference to a registered artifact.

    Args:
        artifact_id: Unique artifact identifier.
        artifact_type: Semantic type (e.g. ``"model_binary"``, ``"metrics_report"``).
        label: Human-readable label.
        uri: Storage URI.
        checksum: Content hash (algorithm:value, e.g. ``"sha256:abc123"``).
    """

    artifact_id: str
    artifact_type: str
    label: str = ""
    uri: str = ""
    checksum: str = ""

    model_config = {"frozen": True}
