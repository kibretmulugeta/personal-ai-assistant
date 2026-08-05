"""
Resume and Curriculum Vitae download tools.
"""

from typing import Any
from packages.tools.base import BaseTool, ToolResult


class DownloadResumeTool(BaseTool):
    """Tool for requesting Alemu Kibret Mulugeta's professional resume."""

    def __init__(self) -> None:
        super().__init__(
            name="download_resume",
            description="Provides download link for Alemu Kibret Mulugeta's professional resume.",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        return ToolResult(
            success=True,
            tool_name=self.name,
            message="You can download Alemu Kibret Mulugeta's professional resume below.",
            data={
                "download_url": "/api/v1/assets/Alemu_Kibret_Resume.pdf",
                "filename": "Alemu_Kibret_Resume.pdf",
                "format": "PDF",
                "version": "2026-v1",
            },
        )


class DownloadCVTool(BaseTool):
    """Tool for requesting Alemu Kibret Mulugeta's academic CV."""

    def __init__(self) -> None:
        super().__init__(
            name="download_cv",
            description="Provides download link for Alemu Kibret Mulugeta's complete academic CV.",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        return ToolResult(
            success=True,
            tool_name=self.name,
            message="You can download Alemu Kibret Mulugeta's academic Curriculum Vitae below.",
            data={
                "download_url": "/api/v1/assets/Alemu_Kibret_Academic_CV.pdf",
                "filename": "Alemu_Kibret_Academic_CV.pdf",
                "format": "PDF",
            },
        )
