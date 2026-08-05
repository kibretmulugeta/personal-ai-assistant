"""
Project exploration, GitHub repository, and academic publication tools.
"""

from typing import Any
from packages.tools.base import BaseTool, ToolResult


class ListProjectsTool(BaseTool):
    """Tool for listing Alemu Kibret Mulugeta's engineering and research projects."""

    def __init__(self) -> None:
        super().__init__(
            name="list_projects",
            description="Returns a list of featured research and engineering projects.",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        projects = [
            {
                "id": "stroke-lesion-segmentation",
                "title": "Stroke Lesion Segmentation via Hybrid U-Net & Metaheuristics",
                "category": "Medical AI & Computer Vision",
                "tech_stack": ["PyTorch", "U-Net", "Genetic Algorithms", "Python"],
                "description": "Deep learning network for segmenting ischemic stroke lesions in medical brain MRI scans.",
            },
            {
                "id": "personal-ai-digital-twin",
                "title": "Personal Portfolio AI Assistant (Digital Twin)",
                "category": "Production AI & Full-Stack Systems",
                "tech_stack": ["FastAPI", "PostgreSQL", "pgvector", "React", "Docker", "RAG"],
                "description": "Standalone personal digital twin assistant service with RAG and multi-agent routing.",
            },
            {
                "id": "medical-image-enhancement",
                "title": "Neural Preprocessing Pipeline for MRI Artifact Reduction",
                "category": "Computer Vision",
                "tech_stack": ["TensorFlow", "Scikit-Learn", "OpenCV"],
                "description": "Image enhancement and noise suppression module for high-contrast medical imaging.",
            },
        ]
        return ToolResult(
            success=True,
            tool_name=self.name,
            message="Here are Alemu Kibret Mulugeta's featured research and software engineering projects.",
            data={"projects": projects},
        )


class FetchProjectDemoTool(BaseTool):
    """Tool for fetching project details and live demo URL."""

    def __init__(self) -> None:
        super().__init__(
            name="fetch_project_demo",
            description="Fetches live demo link and detailed documentation for a specific project.",
        )

    async def execute(self, project_id: str = "stroke-lesion-segmentation", **kwargs: Any) -> ToolResult:
        return ToolResult(
            success=True,
            tool_name=self.name,
            message=f"Project details and live demo for '{project_id}'.",
            data={
                "project_id": project_id,
                "demo_url": f"https://alemukibret.dev/projects/{project_id}",
                "github_url": f"https://github.com/alemukibret/{project_id}",
            },
        )


class FetchGitHubRepositoryTool(BaseTool):
    """Tool for fetching GitHub repository details."""

    def __init__(self) -> None:
        super().__init__(
            name="fetch_github_repository",
            description="Returns GitHub profile or repository URL.",
        )

    async def execute(self, project_name: str = "", **kwargs: Any) -> ToolResult:
        repo_url = f"https://github.com/alemukibret/{project_name}" if project_name else "https://github.com/alemukibret"
        return ToolResult(
            success=True,
            tool_name=self.name,
            message=f"GitHub repository details for '{project_name or 'profile'}'.",
            data={"github_url": repo_url, "owner": "alemukibret"},
        )


class GetLatestPublicationsTool(BaseTool):
    """Tool for retrieving academic publications and research papers."""

    def __init__(self) -> None:
        super().__init__(
            name="get_latest_publications",
            description="Returns research papers and academic publications by Alemu Kibret Mulugeta.",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        publications = [
            {
                "title": "Optimized U-Net Architectures for Ischemic Stroke Lesion Segmentation using Genetic Algorithms",
                "authors": "Alemu Kibret Mulugeta et al.",
                "year": 2025,
                "institution": "Bahir Dar University",
                "focus": "Medical Image Segmentation & Metaheuristic Optimization",
            }
        ]
        return ToolResult(
            success=True,
            tool_name=self.name,
            message="Here are Alemu Kibret Mulugeta's academic research publications.",
            data={"publications": publications},
        )
