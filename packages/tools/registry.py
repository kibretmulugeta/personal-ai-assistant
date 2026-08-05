"""
Central Tool Registry managing tool registration and execution lookup.
"""

from typing import Any, Dict, List, Optional
from packages.tools.base import BaseTool, ToolResult
from packages.tools.contact_tools import (
    OpenSocialProfileTool,
    ScheduleMeetingTool,
    SubmitContactFormTool,
)
from packages.tools.project_tools import (
    FetchGitHubRepositoryTool,
    FetchProjectDemoTool,
    GetLatestPublicationsTool,
    ListProjectsTool,
)
from packages.tools.resume_tools import DownloadCVTool, DownloadResumeTool


class ToolRegistry:
    """Registry maintaining active action tools for Function Calling."""

    def __init__(self) -> None:
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        """Register built-in system tools."""
        tools: List[BaseTool] = [
            DownloadResumeTool(),
            DownloadCVTool(),
            ListProjectsTool(),
            FetchProjectDemoTool(),
            FetchGitHubRepositoryTool(),
            GetLatestPublicationsTool(),
            SubmitContactFormTool(),
            ScheduleMeetingTool(),
            OpenSocialProfileTool(),
        ]
        for t in tools:
            self._tools[t.name] = t

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Fetch registered tool by name."""
        return self._tools.get(name)

    async def execute_tool(self, name: str, **kwargs: Any) -> ToolResult:
        """Execute tool function by name."""
        tool = self.get_tool(name)
        if not tool:
            return ToolResult(
                success=False,
                tool_name=name,
                message=f"Requested tool '{name}' is not registered.",
            )
        return await tool.execute(**kwargs)


# Singleton instance
tool_registry = ToolRegistry()
