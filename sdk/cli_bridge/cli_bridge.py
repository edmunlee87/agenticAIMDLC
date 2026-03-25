"""cli_bridge -- command-line adapter for the MDLC platform.

Translates CLI command strings or pre-parsed argument dicts into
:class:`InteractionPayload` and formats :class:`StandardResponseEnvelope`
for human-readable terminal output.

Components:
- ``command_router``: maps sub-commands to controller + action pairs
- ``argument_parser``: parses CLI tokens into structured argument dicts
- ``output_formatter``: renders envelopes as terminal-friendly text
"""

from __future__ import annotations

import logging
import shlex
from typing import Any, Dict, List, Optional, Tuple

from sdk.platform_core.bridges.base_bridge import BaseBridge
from sdk.platform_core.schemas.payload_models import (
    InteractionPayload,
    StandardResponseEnvelope,
)
from sdk.platform_core.schemas.utilities import IDFactory

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Command table: command string → (controller, action, required_args)
# ---------------------------------------------------------------------------

_COMMAND_TABLE: Dict[str, Dict[str, Any]] = {
    "session open": {
        "controller": "session",
        "action": "open_session",
        "required": ["project_id", "run_id"],
    },
    "session resume": {
        "controller": "session",
        "action": "resume_session",
        "required": ["project_id", "run_id", "session_id"],
    },
    "stage start": {
        "controller": "workflow",
        "action": "run_stage",
        "required": ["stage_name", "run_id"],
    },
    "stage complete": {
        "controller": "workflow",
        "action": "complete_stage",
        "required": ["stage_name", "run_id"],
    },
    "stage fail": {
        "controller": "workflow",
        "action": "fail_stage",
        "required": ["stage_name", "run_id"],
    },
    "route next": {
        "controller": "workflow",
        "action": "route_next",
        "required": ["run_id"],
    },
    "review open": {
        "controller": "review",
        "action": "open_review",
        "required": ["stage_name", "run_id"],
    },
    "review get": {
        "controller": "review",
        "action": "get_review_payload",
        "required": ["review_id", "run_id"],
    },
    "review submit": {
        "controller": "review",
        "action": "submit_review_action",
        "required": ["review_id", "run_id"],
    },
    "recovery options": {
        "controller": "recovery",
        "action": "get_recovery_options",
        "required": ["run_id"],
    },
    "recovery apply": {
        "controller": "recovery",
        "action": "apply_recovery",
        "required": ["run_id"],
    },
}


def parse_arguments(tokens: List[str]) -> Tuple[str, Dict[str, Any]]:
    """Parse CLI tokens into a command key and argument dict.

    Supports ``--key value`` and ``--flag`` style arguments.
    The command is derived from the first 1-2 positional tokens.

    Args:
        tokens: List of CLI tokens (e.g. from ``shlex.split``).

    Returns:
        Tuple of ``(command_key, args_dict)``.

    Raises:
        ValueError: If no command tokens are found.

    Examples:
        >>> parse_arguments(["stage", "start", "--stage-name", "prep", "--run-id", "r1"])
        ("stage start", {"stage_name": "prep", "run_id": "r1"})
    """
    if not tokens:
        raise ValueError("No tokens provided.")

    positional: List[str] = []
    args: Dict[str, Any] = {}
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.startswith("--"):
            key = tok[2:].replace("-", "_")
            if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                args[key] = tokens[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            positional.append(tok)
            i += 1

    if not positional:
        raise ValueError("No command positional tokens found.")

    # Try 2-part command first, then 1-part.
    if len(positional) >= 2 and f"{positional[0]} {positional[1]}" in _COMMAND_TABLE:
        command = f"{positional[0]} {positional[1]}"
    elif positional[0] in _COMMAND_TABLE:
        command = positional[0]
    else:
        # Provide unknown command with remaining tokens for diagnostics.
        command = " ".join(positional[:2]) if len(positional) >= 2 else positional[0]

    return command, args


def format_envelope(envelope: StandardResponseEnvelope, verbose: bool = False) -> str:
    """Format :class:`StandardResponseEnvelope` for terminal output.

    Args:
        envelope: Controller response envelope.
        verbose: Include full data payload. Default: False.

    Returns:
        Human-readable terminal string.
    """
    icon = {"ok": "[OK]", "error": "[ERROR]", "review_required": "[REVIEW]"}.get(
        envelope.status, f"[{envelope.status.upper()}]"
    )
    lines: List[str] = [f"{icon} {envelope.message}"]
    if envelope.next_stage:
        lines.append(f"  Next stage  : {envelope.next_stage}")
    if envelope.review_created and envelope.review_id:
        lines.append(f"  Review ID   : {envelope.review_id}")
    if envelope.audit_ref:
        lines.append(f"  Audit ref   : {envelope.audit_ref}")
    if envelope.event_ref:
        lines.append(f"  Event ref   : {envelope.event_ref}")
    if envelope.warnings:
        for w in envelope.warnings:
            lines.append(f"  [WARN] {w}")
    if envelope.errors:
        for e in envelope.errors:
            lines.append(f"  [ERR]  {e}")
    if envelope.agent_hint:
        lines.append(f"  Hint        : {envelope.agent_hint}")
    if verbose and envelope.data:
        lines.append(f"  Data        : {envelope.data}")
    return "\n".join(lines)


class CliBridge(BaseBridge):
    """Command-line adapter bridge for the MDLC platform.

    Accepts CLI-style input (either a command string or pre-parsed dict) and
    returns formatted terminal output.

    Input formats::

        # String (will be tokenised with shlex.split)
        "stage start --stage-name feature_engineering --run-id run-abc123 --project-id proj-xyz"

        # Pre-parsed dict
        {
            "command": "stage start",
            "actor_id": "user_01",
            "actor_role": "developer",
            "stage_name": "feature_engineering",
            "run_id": "run-abc123",
            "project_id": "proj-xyz"
        }

    Args:
        controller_factory: :class:`ControllerFactory` instance.
        verbose: Enable verbose data output. Default: False.
        logger: Optional logger override.
    """

    def __init__(
        self,
        controller_factory: Any,
        verbose: bool = False,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        super().__init__(controller_factory=controller_factory, logger=logger)
        self._verbose = verbose

    def dispatch(self, raw_input: Any) -> str:
        """Accept CLI input, dispatch to controller, return terminal output.

        Args:
            raw_input: Command string or pre-parsed dict.

        Returns:
            Human-readable terminal output string.
        """
        try:
            payload = self.build_payload(raw_input)
        except ValueError as exc:
            return f"[ERROR] {exc}\n  Use 'help' to list available commands."

        command, args = self._extract_command_and_args(raw_input)
        mapping = _COMMAND_TABLE.get(command)
        if mapping is None:
            return (
                f"[ERROR] Unknown command: {command!r}\n"
                f"  Available commands: {', '.join(_COMMAND_TABLE.keys())}"
            )

        controller = self._resolve_controller(mapping["controller"])
        if controller is None:
            return f"[ERROR] Controller '{mapping['controller']}' unavailable."

        try:
            envelope = controller.handle(payload)
        except Exception as exc:
            self._logger.exception("CliBridge.dispatch: controller error: %s", exc)
            return f"[ERROR] Internal error: {exc}"

        return self.format_response(envelope)

    def build_payload(self, raw_input: Any) -> InteractionPayload:
        """Build :class:`InteractionPayload` from CLI input.

        Args:
            raw_input: Command string or pre-parsed dict.

        Returns:
            :class:`InteractionPayload`.

        Raises:
            ValueError: If required fields are missing or command is unknown.
        """
        command, args = self._extract_command_and_args(raw_input)
        mapping = _COMMAND_TABLE.get(command)
        if mapping is None:
            raise ValueError(
                f"Unknown command: {command!r}. "
                f"Available: {list(_COMMAND_TABLE.keys())}"
            )

        # Check required args.
        missing = [r for r in mapping["required"] if not args.get(r)]
        if missing:
            flags = ", ".join("--" + m.replace("_", "-") for m in missing)
            raise ValueError(f"Command '{command}' requires: {flags}")

        actor_id = args.get("actor_id") or "cli_user"
        actor_role = args.get("actor_role") or "developer"
        stage_name = args.get("stage_name") or ""
        actor = self._build_actor(actor_id=actor_id, role=actor_role)

        return self._build_interaction_payload(
            stage_name=stage_name,
            interaction_type="cli",
            action=mapping["action"],
            actor=actor,
            run_id=args.get("run_id"),
            project_id=args.get("project_id"),
            session_id=args.get("session_id"),
            trace_id=args.get("trace_id"),
            correlation_id=args.get("correlation_id") or IDFactory.correlation_id(),
            parameters=args.get("parameters"),
            review_id=args.get("review_id"),
            policy_acknowledgments=args.get("policy_acknowledgments"),
        )

    def format_response(self, envelope: StandardResponseEnvelope) -> str:
        """Format :class:`StandardResponseEnvelope` as terminal output.

        Args:
            envelope: Controller response envelope.

        Returns:
            Human-readable terminal string.
        """
        return format_envelope(envelope, verbose=self._verbose)

    def get_help(self) -> str:
        """Return help text listing available commands.

        Returns:
            Formatted help string.
        """
        lines = ["MDLC CLI Bridge — Available commands:", ""]
        for cmd, spec in _COMMAND_TABLE.items():
            required = ", ".join(f"--{r.replace('_', '-')}" for r in spec["required"])
            lines.append(f"  {cmd:<22} [{spec['controller']}.{spec['action']}]  required: {required}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_command_and_args(raw_input: Any) -> Tuple[str, Dict[str, Any]]:
        if isinstance(raw_input, str):
            tokens = shlex.split(raw_input)
            return parse_arguments(tokens)
        if isinstance(raw_input, dict):
            command = raw_input.get("command", "")
            args = {k: v for k, v in raw_input.items() if k != "command"}
            return command, args
        raise ValueError(f"raw_input must be a str or dict, got {type(raw_input).__name__}")

    def _resolve_controller(self, controller_name: str) -> Any:
        dispatch = {
            "session": self._factory.session,
            "workflow": self._factory.workflow,
            "review": self._factory.review,
            "recovery": self._factory.recovery,
        }
        factory_fn = dispatch.get(controller_name)
        return factory_fn() if factory_fn else None
