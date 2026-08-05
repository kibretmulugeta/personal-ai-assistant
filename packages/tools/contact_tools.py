"""
Contact form submission, meeting scheduler, and social media profile tools.
"""

from typing import Any
from packages.tools.base import BaseTool, ToolResult


class SubmitContactFormTool(BaseTool):
    """Tool for submitting visitor contact messages."""

    def __init__(self) -> None:
        super().__init__(
            name="submit_contact_form",
            description="Submits a contact inquiry directly to Alemu Kibret Mulugeta.",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        return ToolResult(
            success=True,
            tool_name=self.name,
            message="You can submit your contact request directly using the embedded form below.",
            data={"action": "open_contact_modal", "endpoint": "/api/v1/contact/submit"},
        )


class ScheduleMeetingTool(BaseTool):
    """Tool for scheduling a professional discussion or meeting."""

    def __init__(self) -> None:
        super().__init__(
            name="schedule_meeting",
            description="Provides meeting calendar link to schedule a discussion with Alemu.",
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        return ToolResult(
            success=True,
            tool_name=self.name,
            message="You can schedule a meeting with Alemu Kibret Mulugeta through the calendar link below.",
            data={"calendar_url": "https://cal.com/alemukibret"},
        )


class OpenSocialProfileTool(BaseTool):
    """Tool for retrieving social and professional profile links."""

    def __init__(self) -> None:
        super().__init__(
            name="open_social_profile",
            description="Returns professional social profile links (LinkedIn, GitHub, Google Scholar).",
        )

    async def execute(self, platform: str = "linkedin", **kwargs: Any) -> ToolResult:
        profiles = {
            "github": "https://github.com/alemukibret",
            "linkedin": "https://linkedin.com/in/alemukibret",
            "google_scholar": "https://scholar.google.com/citations?user=alemukibret",
        }
        target_url = profiles.get(platform.lower(), profiles["linkedin"])
        return ToolResult(
            success=True,
            tool_name=self.name,
            message=f"Here is the link to Alemu Kibret Mulugeta's {platform.capitalize()} profile.",
            data={"platform": platform, "url": target_url},
        )
