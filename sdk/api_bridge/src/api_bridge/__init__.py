"""api_bridge -- REST adapter bridging HTTP to AgentDispatcher."""

from api_bridge.adapter import APIAdapter
from api_bridge.models import APIRequest, APIResponse

__all__ = ["APIAdapter", "APIRequest", "APIResponse"]
