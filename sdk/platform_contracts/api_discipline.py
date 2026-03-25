"""SDK Public API Discipline — Reference module.

This module documents and enforces the conventions that ALL SDKs in this
monorepo must follow.  It is not a runtime module; it is a canonical
reference that tooling, code-review, and tests should validate against.

Layering (bottom → top)
------------------------
1. ``sdk/platform_core``        — core contracts, schemas, base classes
2. Foundation SDKs              — config_sdk, registry_sdk, observabilitysdk,
                                   auditsdk, artifactsdk
3. Workflow / HITL SDKs         — workflowsdk, hitlsdk, policysdk
4. Runtime / Resolver           — platform_core runtime pack
5. Data / analytics SDKs        — dataset_sdk, dq_sdk, feature_sdk, …
6. Domain / lifecycle SDKs      — scorecardsdk, eclsdk, lgdsdk, …
7. Bridges                      — agent_bridge, jupyter_bridge, api_bridge,
                                   cli_bridge, mcp_bridge

Each layer may depend only on layers below it.

Per-SDK conventions
-------------------
* Each SDK exposes **one primary service class** per concern (e.g.
  ``ArtifactService``, ``WorkflowStateStore``).
* All public domain models extend :class:`~platform_core.schemas.BaseModelBase`.
* All material method return values are :class:`~platform_core.schemas.BaseResult`
  or :class:`~platform_core.schemas.ValidationResultBase`.
* Every material method populates at minimum the four agent hints:

  - ``agent_hint``       — free-text guidance for the LLM/orchestrator
  - ``workflow_hint``    — recommended next stage or action for the workflow
  - ``audit_hint``       — signal to the audit layer (``"write_audit"`` /
                           ``"skip_audit"`` / ``"escalate"``)
  - ``observability_hint`` — event type to emit (maps to ``EventTypeEnum``)

Import order within every SDK module
--------------------------------------
1. Standard library (``import os``, ``from typing import …``)
2. Third-party (``import pydantic``, ``import yaml``)
3. ``platform_core`` (``from sdk.platform_core.schemas import …``)
4. Peer SDK (``from sdk.registry_sdk import …``)
5. SDK-local (``from .models import …``)

Controller boundary envelope
-----------------------------
Every controller method **must** return a
:class:`~platform_core.schemas.StandardResponseEnvelope`.  The envelope must
include at minimum:

* ``status``                  — one of ``StatusEnum``
* ``run_id``                  — propagated from ``RuntimeContext``
* ``audit_ref``               — populated after :meth:`_write_audit_if_needed`
* ``event_ref``               — populated after :meth:`_emit_event_if_needed`
* ``governance_summary``      — built from resolved constraints
* ``workflow_state_patch``    — diff to apply to ``WorkflowState`` (may be empty)
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, ClassVar


class SDKPublicAPIDiscipline(metaclass=ABCMeta):
    """Abstract marker enforcing SDK public API discipline.

    Args:
        sdk_name: Canonical name of the SDK (e.g. ``"artifactsdk"``).

    Attributes:
        SDK_NAME: Class-level name constant.  Must be overridden.
        LAYER: Integer layer (1–7) per the layering model above.

    Examples:
        >>> class MyService(SDKPublicAPIDiscipline):
        ...     SDK_NAME: ClassVar[str] = "my_sdk"
        ...     LAYER: ClassVar[int] = 2
    """

    SDK_NAME: ClassVar[str]
    LAYER: ClassVar[int]

    def __init__(self, sdk_name: str) -> None:
        self._sdk_name = sdk_name

    @abstractmethod
    def health_check(self) -> dict[str, Any]:
        """Return a health/readiness dict for the SDK.

        Returns:
            dict with keys ``sdk_name``, ``status`` (``"ok"``/``"degraded"``),
            and ``details``.
        """
