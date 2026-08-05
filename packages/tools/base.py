"""
Abstract Base Tool interface and ToolResult model.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    """Execution output from a tool call."""

    success: bool = Field(default=True)
    tool_name: str = Field(...)
    message: str = Field(...)
    data: Dict[str, Any] = Field(default_factory=dict)


class BaseTool(ABC):
    """Abstract base class for function calling tools."""

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute tool function asynchronously."""
        pass
