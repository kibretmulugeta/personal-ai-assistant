"""
Action Agent implementation integrating central ToolRegistry.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from packages.agents.base import BaseAgent
from packages.tools.registry import tool_registry


class ActionResult(BaseModel):
    """Result payload from an Action Agent execution."""

    success: bool = Field(default=True)
    action_name: str = Field(...)
    message: str = Field(...)
    data: Dict[str, Any] = Field(default_factory=dict)


class ActionAgent(BaseAgent):
    """Action Agent orchestrating tool execution via ToolRegistry."""

    async def process(
        self,
        input_text: str,
        action_name: Optional[str] = None,
        action_args: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> ActionResult:
        """Execute specified action or resolve tool call."""
        action = action_name or "download_resume"
        args = action_args or {}

        res = await tool_registry.execute_tool(action, **args)
        return ActionResult(
            success=res.success,
            action_name=res.tool_name,
            message=res.message,
            data=res.data,
        )
