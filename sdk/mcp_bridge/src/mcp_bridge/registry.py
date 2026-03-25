"""mcp_bridge.registry -- MCP tool registry.

Registers platform tools with their MCP-compatible schemas (JSON Schema).
The registry enables MCP clients (Claude, Cursor, etc.) to discover and
call MDLC platform tools via the MCP protocol.
"""

from __future__ import annotations

import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class MCPToolDefinition:
    """Descriptor for a single MCP-compatible tool.

    Args:
        tool_name: Unique tool name (snake_case).
        description: Human-readable tool description.
        input_schema: JSON Schema dict describing the tool's input parameters.
        handler: Python callable that executes the tool.
        requires_roles: Optional list of role IDs required to call this tool.
    """

    def __init__(
        self,
        tool_name: str,
        description: str,
        input_schema: dict[str, Any],
        handler: Callable[..., Any],
        requires_roles: list[str] | None = None,
    ) -> None:
        self.tool_name = tool_name
        self.description = description
        self.input_schema = input_schema
        self.handler = handler
        self.requires_roles = requires_roles or []

    def to_mcp_schema(self) -> dict[str, Any]:
        """Return MCP-compatible tool schema.

        Returns:
            Dict conforming to MCP tool descriptor format.
        """
        return {
            "name": self.tool_name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }


class MCPToolRegistry:
    """Registry of MCP-compatible tools for the MDLC platform.

    Args:
        dispatcher: :class:`~agent_bridge.dispatcher.AgentDispatcher` instance
            used to resolve interaction-type tools.
    """

    def __init__(self, dispatcher: Any = None) -> None:
        self._dispatcher = dispatcher
        self._tools: dict[str, MCPToolDefinition] = {}
        self._register_platform_tools()

    def register(self, tool: MCPToolDefinition) -> None:
        """Register a tool definition.

        Args:
            tool: :class:`MCPToolDefinition` to register.
        """
        self._tools[tool.tool_name] = tool
        logger.info("mcp_tool_registry.registered", extra={"tool_name": tool.tool_name})

    def get(self, tool_name: str) -> MCPToolDefinition | None:
        """Retrieve a tool by name.

        Args:
            tool_name: Tool name.

        Returns:
            :class:`MCPToolDefinition` or None.
        """
        return self._tools.get(tool_name)

    def list_tools(self) -> list[dict[str, Any]]:
        """Return all tool schemas for MCP discovery.

        Returns:
            List of MCP tool schema dicts.
        """
        return [t.to_mcp_schema() for t in self._tools.values()]

    def call(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Execute a tool by name.

        Args:
            tool_name: Tool to execute.
            arguments: Tool input arguments.

        Returns:
            Tool result.

        Raises:
            KeyError: If tool not found.
            Exception: If tool execution fails.
        """
        tool = self._tools.get(tool_name)
        if tool is None:
            raise KeyError(f"MCP tool '{tool_name}' not registered.")
        logger.info("mcp_tool_registry.call", extra={"tool_name": tool_name})
        return tool.handler(**arguments)

    # ------------------------------------------------------------------
    # Built-in platform tool registrations
    # ------------------------------------------------------------------

    def _register_platform_tools(self) -> None:
        """Register the standard MDLC platform tools."""
        self._register_session_tools()
        self._register_workflow_tools()
        self._register_review_tools()
        self._register_recovery_tools()

    def _register_session_tools(self) -> None:
        self.register(MCPToolDefinition(
            tool_name="mdlc_open_session",
            description="Open a new MDLC workflow session.",
            input_schema={
                "type": "object",
                "properties": {
                    "run_id": {"type": "string", "description": "MDLC run identifier."},
                    "project_id": {"type": "string", "description": "Project identifier."},
                    "actor_id": {"type": "string", "description": "Actor opening the session."},
                    "domain": {"type": "string", "description": "Domain pack name (e.g. 'scorecard')."},
                },
                "required": ["run_id", "project_id", "actor_id"],
            },
            handler=self._dispatch_tool("session_open"),
        ))

    def _register_workflow_tools(self) -> None:
        for action in ["stage_start", "stage_complete", "stage_fail", "route_next"]:
            label = action.replace("_", " ").title()
            self.register(MCPToolDefinition(
                tool_name=f"mdlc_{action}",
                description=f"Execute MDLC action: {label}.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "run_id": {"type": "string"},
                        "project_id": {"type": "string"},
                        "actor_id": {"type": "string"},
                        "stage_name": {"type": "string"},
                    },
                    "required": ["run_id", "project_id", "actor_id"],
                },
                handler=self._dispatch_tool(action),
            ))

    def _register_review_tools(self) -> None:
        for action in ["review_open", "review_get_payload", "review_submit_action"]:
            self.register(MCPToolDefinition(
                tool_name=f"mdlc_{action}",
                description=f"MDLC HITL review action: {action.replace('_', ' ')}.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "run_id": {"type": "string"},
                        "project_id": {"type": "string"},
                        "actor_id": {"type": "string"},
                        "review_id": {"type": "string"},
                        "action": {"type": "string"},
                        "rationale": {"type": "string"},
                    },
                    "required": ["run_id", "project_id", "actor_id"],
                },
                handler=self._dispatch_tool(action),
            ))

    def _register_recovery_tools(self) -> None:
        for action in ["recovery_options", "recovery_choice"]:
            self.register(MCPToolDefinition(
                tool_name=f"mdlc_{action}",
                description=f"MDLC recovery action: {action.replace('_', ' ')}.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "run_id": {"type": "string"},
                        "project_id": {"type": "string"},
                        "actor_id": {"type": "string"},
                        "recovery_path": {"type": "string"},
                    },
                    "required": ["run_id", "project_id", "actor_id"],
                },
                handler=self._dispatch_tool(action),
            ))

    def _dispatch_tool(self, interaction_type: str) -> Callable[..., Any]:
        """Create a handler that dispatches via the AgentDispatcher.

        Args:
            interaction_type: Interaction type string.

        Returns:
            Callable handler.
        """
        def handler(**kwargs: Any) -> Any:
            if self._dispatcher is None:
                return {"error": "No dispatcher configured."}
            try:
                from platform_contracts.enums import InteractionType
                from platform_core.schemas.payloads import InteractionPayload
                itype = InteractionType(interaction_type)
                payload = InteractionPayload(
                    interaction_type=itype,
                    run_id=kwargs.get("run_id", ""),
                    project_id=kwargs.get("project_id", ""),
                    actor_id=kwargs.get("actor_id", ""),
                    **{k: v for k, v in kwargs.items() if k not in ("run_id", "project_id", "actor_id")},
                )
                envelope = self._dispatcher.dispatch(payload)
                return envelope.model_dump() if hasattr(envelope, "model_dump") else vars(envelope)
            except Exception as exc:
                logger.error("mcp_tool.dispatch_error", extra={"tool": interaction_type, "error": str(exc)})
                return {"success": False, "error": str(exc)}
        return handler
