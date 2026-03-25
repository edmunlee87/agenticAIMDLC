"""api_bridge -- REST adapter for the MDLC platform.

Translates incoming HTTP-like request dicts into :class:`InteractionPayload`
and formats :class:`StandardResponseEnvelope` for REST consumers.

Components:
- ``request_mapper``: maps HTTP method + path + body to interaction payload
- ``response_mapper``: formats envelope to REST response dict
- ``auth_hooks``: validates bearer tokens and resolves actor context
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from sdk.platform_core.bridges.base_bridge import BaseBridge
from sdk.platform_core.schemas.common_fragments import ActorRecord
from sdk.platform_core.schemas.payload_models import (
    InteractionPayload,
    StandardResponseEnvelope,
)
from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Route table: (method, path_template) → (controller, action)
# ---------------------------------------------------------------------------

_ROUTE_TABLE: List[tuple[str, str, str, str]] = [
    ("POST", "/sessions", "session", "open_session"),
    ("PUT", "/sessions/{session_id}/resume", "session", "resume_session"),
    ("POST", "/runs/{run_id}/stages/{stage_name}/start", "workflow", "run_stage"),
    ("POST", "/runs/{run_id}/stages/{stage_name}/complete", "workflow", "complete_stage"),
    ("POST", "/runs/{run_id}/stages/{stage_name}/fail", "workflow", "fail_stage"),
    ("POST", "/runs/{run_id}/route", "workflow", "route_next"),
    ("POST", "/runs/{run_id}/reviews", "review", "open_review"),
    ("GET", "/runs/{run_id}/reviews/{review_id}", "review", "get_review_payload"),
    ("POST", "/runs/{run_id}/reviews/{review_id}/actions", "review", "submit_review_action"),
    ("GET", "/runs/{run_id}/recovery-options", "recovery", "get_recovery_options"),
    ("POST", "/runs/{run_id}/recovery", "recovery", "apply_recovery"),
]


def _match_route(
    method: str,
    path: str,
) -> Optional[tuple[str, str, Dict[str, str]]]:
    """Match an HTTP method + path against the route table.

    Args:
        method: HTTP method (GET, POST, PUT, etc.).
        path: URL path string.

    Returns:
        ``(controller, action, path_params)`` or None if no match.
    """
    path_parts = path.strip("/").split("/")
    for rt_method, rt_template, controller, action in _ROUTE_TABLE:
        if rt_method.upper() != method.upper():
            continue
        template_parts = rt_template.strip("/").split("/")
        if len(template_parts) != len(path_parts):
            continue
        params: Dict[str, str] = {}
        matched = True
        for tp, pp in zip(template_parts, path_parts):
            if tp.startswith("{") and tp.endswith("}"):
                params[tp[1:-1]] = pp
            elif tp != pp:
                matched = False
                break
        if matched:
            return controller, action, params
    return None


def validate_bearer_token(
    token: Optional[str],
    known_tokens: Optional[Dict[str, Dict[str, str]]] = None,
) -> Optional[Dict[str, str]]:
    """Validate a bearer token and return actor context.

    In production this would call an auth service. This implementation
    provides a configurable lookup table for testing and local use.

    Args:
        token: Bearer token string (without ``"Bearer "`` prefix).
        known_tokens: Mapping of token → actor_dict. Default: empty (all tokens rejected).

    Returns:
        Actor dict with ``actor_id`` and ``actor_role``, or None if invalid.
    """
    if not token:
        return None
    if known_tokens and token in known_tokens:
        return known_tokens[token]
    return None


class ApiBridge(BaseBridge):
    """REST adapter bridge for the MDLC platform.

    Translates HTTP-like request dicts into controller dispatch calls.

    Expected ``raw_input`` format::

        {
            "method": "POST",
            "path": "/runs/run-abc123/stages/feature_engineering/start",
            "headers": {"Authorization": "Bearer <token>"},
            "body": {
                "project_id": "proj-xyz",
                "actor_id": "svc-account-01",
                "actor_role": "developer",
                "parameters": {...}
            }
        }

    Args:
        controller_factory: :class:`ControllerFactory` instance.
        known_tokens: Optional token → actor_dict map for auth validation.
        logger: Optional logger override.
    """

    def __init__(
        self,
        controller_factory: Any,
        known_tokens: Optional[Dict[str, Dict[str, str]]] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        super().__init__(controller_factory=controller_factory, logger=logger)
        self._known_tokens = known_tokens or {}

    def dispatch(self, raw_input: Any) -> Dict[str, Any]:
        """Receive HTTP-like request dict, dispatch to controller, return REST response.

        Args:
            raw_input: Request dict with ``method``, ``path``, ``headers``, ``body``.

        Returns:
            REST response dict with ``status_code``, ``body``, ``request_id``.
        """
        if not isinstance(raw_input, dict):
            return self._rest_error(400, "invalid_input", "raw_input must be a dict.")

        method = raw_input.get("method", "GET").upper()
        path = raw_input.get("path", "")
        headers: Dict[str, str] = raw_input.get("headers") or {}
        body: Dict[str, Any] = raw_input.get("body") or {}
        request_id = raw_input.get("request_id") or IDFactory.correlation_id()

        # Auth hook: validate bearer token.
        actor_ctx = self._auth_hook(headers, body)
        if actor_ctx is None:
            return self._rest_error(401, "unauthorized", "Invalid or missing bearer token.", request_id=request_id)

        # Route matching.
        match = _match_route(method, path)
        if match is None:
            return self._rest_error(404, "not_found", f"No route for {method} {path!r}.", request_id=request_id)

        controller_name, action, path_params = match

        try:
            payload = self._build_from_request(
                method=method,
                path=path,
                path_params=path_params,
                action=action,
                actor_ctx=actor_ctx,
                body=body,
                request_id=request_id,
            )
        except (ValueError, KeyError) as exc:
            return self._rest_error(400, "bad_request", str(exc), request_id=request_id)

        controller = self._resolve_controller(controller_name)
        if controller is None:
            return self._rest_error(503, "service_unavailable", f"Controller '{controller_name}' unavailable.", request_id=request_id)

        try:
            envelope = controller.handle(payload)
        except Exception as exc:
            self._logger.exception("ApiBridge.dispatch: controller error: %s", exc)
            return self._rest_error(500, "internal_error", str(exc), request_id=request_id)

        return self.format_response(envelope, request_id=request_id)

    def build_payload(self, raw_input: Any) -> InteractionPayload:
        """Build :class:`InteractionPayload` from a request dict.

        Args:
            raw_input: Request dict.

        Returns:
            :class:`InteractionPayload`.

        Raises:
            ValueError: If routing or required fields fail.
        """
        method = raw_input.get("method", "GET").upper()
        path = raw_input.get("path", "")
        headers = raw_input.get("headers") or {}
        body = raw_input.get("body") or {}
        request_id = raw_input.get("request_id") or IDFactory.correlation_id()

        actor_ctx = self._auth_hook(headers, body) or {"actor_id": "anonymous", "actor_role": "viewer"}
        match = _match_route(method, path)
        if match is None:
            raise ValueError(f"No route for {method} {path!r}.")
        controller_name, action, path_params = match
        return self._build_from_request(
            method=method,
            path=path,
            path_params=path_params,
            action=action,
            actor_ctx=actor_ctx,
            body=body,
            request_id=request_id,
        )

    def format_response(
        self,
        envelope: StandardResponseEnvelope,
        request_id: str = "",
    ) -> Dict[str, Any]:
        """Translate :class:`StandardResponseEnvelope` to a REST response dict.

        Args:
            envelope: Controller response envelope.
            request_id: Original request correlation ID.

        Returns:
            REST response dict with ``status_code``, ``body``, ``request_id``.
        """
        status_code = 200
        if envelope.status == "error":
            status_code = 422
        elif envelope.status == "review_required":
            status_code = 202

        return {
            "status_code": status_code,
            "request_id": request_id,
            "body": {
                "status": envelope.status,
                "message": envelope.message,
                "data": envelope.data,
                "next_stage": envelope.next_stage,
                "review_created": envelope.review_created,
                "review_id": envelope.review_id,
                "audit_ref": envelope.audit_ref,
                "event_ref": envelope.event_ref,
                "warnings": envelope.warnings,
                "errors": envelope.errors,
                "agent_hint": envelope.agent_hint or "",
                "governance_summary": (
                    envelope.governance_summary.model_dump()
                    if envelope.governance_summary
                    else None
                ),
            },
        }

    def get_routes(self) -> List[Dict[str, str]]:
        """Return list of registered routes.

        Returns:
            List of dicts with ``method``, ``path``, ``controller``, ``action``.
        """
        return [
            {"method": m, "path": p, "controller": c, "action": a}
            for m, p, c, a in _ROUTE_TABLE
        ]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _auth_hook(
        self,
        headers: Dict[str, str],
        body: Dict[str, Any],
    ) -> Optional[Dict[str, str]]:
        """Extract and validate actor context from headers or body.

        Checks ``Authorization: Bearer <token>`` header first, then falls back
        to inline ``actor_id`` / ``actor_role`` fields in the request body
        (for internal service-to-service calls without token auth).

        Args:
            headers: HTTP headers dict.
            body: Request body dict.

        Returns:
            Actor dict or None if auth fails.
        """
        auth_header = headers.get("Authorization") or headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            actor = validate_bearer_token(token, self._known_tokens)
            if actor:
                return actor

        # Fallback: service-to-service with explicit actor fields in body.
        actor_id = body.get("actor_id")
        actor_role = body.get("actor_role")
        if actor_id and actor_role:
            return {"actor_id": str(actor_id), "actor_role": str(actor_role)}

        return None

    def _build_from_request(
        self,
        *,
        method: str,
        path: str,
        path_params: Dict[str, str],
        action: str,
        actor_ctx: Dict[str, str],
        body: Dict[str, Any],
        request_id: str,
    ) -> InteractionPayload:
        actor = self._build_actor(
            actor_id=actor_ctx.get("actor_id", "anonymous"),
            role=actor_ctx.get("actor_role", "viewer"),
            display_name=actor_ctx.get("display_name"),
        )
        stage_name = path_params.get("stage_name") or body.get("stage_name") or ""
        run_id = path_params.get("run_id") or body.get("run_id")
        return self._build_interaction_payload(
            stage_name=stage_name,
            interaction_type="rest_api",
            action=action,
            actor=actor,
            run_id=run_id,
            project_id=body.get("project_id"),
            session_id=path_params.get("session_id") or body.get("session_id"),
            trace_id=body.get("trace_id"),
            correlation_id=request_id,
            parameters=body.get("parameters"),
            review_id=path_params.get("review_id") or body.get("review_id"),
            policy_acknowledgments=body.get("policy_acknowledgments"),
        )

    def _resolve_controller(self, controller_name: str) -> Any:
        dispatch = {
            "session": self._factory.session,
            "workflow": self._factory.workflow,
            "review": self._factory.review,
            "recovery": self._factory.recovery,
        }
        factory_fn = dispatch.get(controller_name)
        return factory_fn() if factory_fn else None

    @staticmethod
    def _rest_error(
        status_code: int,
        code: str,
        message: str,
        request_id: str = "",
    ) -> Dict[str, Any]:
        return {
            "status_code": status_code,
            "request_id": request_id,
            "body": {
                "status": "error",
                "error_code": code,
                "message": message,
                "data": None,
                "next_stage": None,
                "review_created": False,
                "review_id": None,
                "audit_ref": None,
                "event_ref": None,
                "warnings": [],
                "errors": [f"{code}: {message}"],
                "agent_hint": "",
                "governance_summary": None,
            },
        }
