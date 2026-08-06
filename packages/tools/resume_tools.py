"""
Resume and Curriculum Vitae download tools.
"""

from typing import Any
from packages.tools.base import BaseTool, ToolResult


class DownloadResumeTool(BaseTool):
    """Tool for requesting Kibret Mulugeta Alemu's professional resume."""

    def __init__(self) -> None:
        super().__init__(
            name="download_resume",
            description="Provides download link for Kibret Mulugeta Alemu's professional resume.",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        return ToolResult(
            success=True,
            tool_name=self.name,
            message="You can download Kibret Mulugeta Alemu's professional resume using the link below.",
            data={
                "download_url": "https://interactive-portfolio-pied-three.vercel.app/api/resume/download",
                "filename": "Kibret_Mulugeta_Alemu_Resume.pdf",
                "format": "PDF",
                "version": "2026-v1",
            },
        )


class DownloadCVTool(BaseTool):
    """Tool for requesting Kibret Mulugeta Alemu's academic CV."""

    def __init__(self) -> None:
        super().__init__(
            name="download_cv",
            description="Provides download link for Kibret Mulugeta Alemu's complete academic CV.",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        return ToolResult(
            success=True,
            tool_name=self.name,
            message="You can download Kibret Mulugeta Alemu's academic Curriculum Vitae using the link below.",
            data={
                "download_url": "https://interactive-portfolio-pied-three.vercel.app/api/resume/download",
                "filename": "Kibret_Mulugeta_Alemu_Academic_CV.pdf",
                "format": "PDF",
            },
        )
