"""cli_bridge.router -- CLI command router and output formatter.

Provides a minimal CLI entry point that maps sub-commands to interaction types
and delegates to the AgentDispatcher.  Output is formatted as JSON or
human-readable tables depending on the ``--format`` flag.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from typing import Any

logger = logging.getLogger(__name__)


class CLIRouter:
    """Routes CLI commands to the AgentDispatcher.

    Args:
        dispatcher: :class:`~agent_bridge.dispatcher.AgentDispatcher` instance.
    """

    # Sub-command → InteractionType string mapping
    _COMMAND_MAP: dict[str, str] = {
        "open-session": "session_open",
        "resume-session": "session_resume",
        "start-stage": "stage_start",
        "complete-stage": "stage_complete",
        "fail-stage": "stage_fail",
        "route-next": "route_next",
        "open-review": "review_open",
        "submit-review": "review_submit_action",
        "recovery-options": "recovery_options",
        "apply-recovery": "recovery_choice",
        "health": "health",
    }

    def __init__(self, dispatcher: Any) -> None:
        self._dispatcher = dispatcher

    def build_parser(self) -> argparse.ArgumentParser:
        """Build the argument parser for the MDLC CLI.

        Returns:
            :class:`argparse.ArgumentParser`.
        """
        parser = argparse.ArgumentParser(
            prog="mdlc",
            description="MDLC Agentic AI Platform CLI",
        )
        parser.add_argument("--format", choices=["json", "table"], default="json", help="Output format. Default: json.")
        parser.add_argument("--run-id", default="", help="MDLC run ID.")
        parser.add_argument("--project-id", default="", help="Project ID.")
        parser.add_argument("--actor-id", default="", help="Actor ID.")
        parser.add_argument("--trace-id", default="", help="Trace ID.")

        sub = parser.add_subparsers(dest="command", help="Command")
        for cmd in self._COMMAND_MAP:
            sub_parser = sub.add_parser(cmd, help=f"Execute {cmd}.")
            sub_parser.add_argument("--data", default="{}", help="JSON payload data.")

        return parser

    def run(self, args: list[str] | None = None) -> int:
        """Parse arguments and execute the CLI command.

        Args:
            args: Argument list. Defaults to ``sys.argv[1:]``.

        Returns:
            Exit code (0 = success, 1 = error).
        """
        parser = self.build_parser()
        parsed = parser.parse_args(args)

        if not parsed.command:
            parser.print_help()
            return 0

        if parsed.command == "health":
            print(json.dumps({"status": "ok"}, indent=2))
            return 0

        interaction_type_str = self._COMMAND_MAP.get(parsed.command)
        if not interaction_type_str:
            print(f"Unknown command: {parsed.command}", file=sys.stderr)
            return 1

        try:
            extra_data: dict[str, Any] = json.loads(getattr(parsed, "data", "{}"))
        except json.JSONDecodeError as exc:
            print(f"Invalid --data JSON: {exc}", file=sys.stderr)
            return 1

        try:
            from platform_contracts.enums import InteractionType
            from platform_core.schemas.payloads import InteractionPayload

            interaction_type = InteractionType(interaction_type_str)
            payload = InteractionPayload(
                interaction_type=interaction_type,
                run_id=parsed.run_id,
                project_id=parsed.project_id,
                actor_id=parsed.actor_id,
                trace_id=parsed.trace_id,
                **extra_data,
            )
            envelope = self._dispatcher.dispatch(payload)
            output = envelope.model_dump() if hasattr(envelope, "model_dump") else vars(envelope)

            if parsed.format == "json":
                print(json.dumps(output, indent=2, default=str))
            else:
                self._print_table(output)
            return 0

        except Exception as exc:
            logger.error("cli_router.error", extra={"error": str(exc)})
            print(json.dumps({"success": False, "error": str(exc)}, indent=2))
            return 1

    @staticmethod
    def _print_table(data: dict[str, Any]) -> None:
        """Print a dict as a simple key: value table.

        Args:
            data: Dict to print.
        """
        for k, v in data.items():
            print(f"{k:<30} {v}")
