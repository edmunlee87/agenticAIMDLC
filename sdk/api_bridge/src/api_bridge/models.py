"""api_bridge.models -- REST adapter request/response envelope contracts."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class APIRequest(BaseModel):
    """Inbound REST API request envelope.

    Args:
        interaction_type: The interaction type string (maps to InteractionType enum).
        run_id: MDLC run context.
        project_id: Project context.
        actor_id: Actor issuing the request.
        trace_id: Distributed trace ID for observability.
        payload: The request body payload dict.
        auth_claims: Extracted auth claims (role_id, etc.).
    """

    model_config = ConfigDict(extra="allow")

    interaction_type: str
    run_id: str = ""
    project_id: str = ""
    actor_id: str = ""
    trace_id: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)
    auth_claims: dict[str, Any] = Field(default_factory=dict)


class APIResponse(BaseModel):
    """Outbound REST API response envelope.

    Args:
        success: True if the request succeeded.
        status_code: HTTP status code.
        data: Response data dict.
        error_code: Error code on failure.
        error_message: Human-readable error on failure.
        trace_id: Distributed trace ID (echoed from request).
    """

    model_config = ConfigDict(frozen=True)

    success: bool
    status_code: int = 200
    data: Any = None
    error_code: str | None = None
    error_message: str | None = None
    trace_id: str = ""
