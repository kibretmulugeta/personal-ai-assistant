"""
Unit tests for function calling tools and Central ToolRegistry.
"""

import pytest
from packages.tools.registry import tool_registry


@pytest.mark.asyncio
async def test_download_resume_tool():
    """Test download_resume tool execution."""
    res = await tool_registry.execute_tool("download_resume")
    assert res.success is True
    assert res.tool_name == "download_resume"
    assert "download_url" in res.data


@pytest.mark.asyncio
async def test_list_projects_tool():
    """Test list_projects tool execution."""
    res = await tool_registry.execute_tool("list_projects")
    assert res.success is True
    assert "projects" in res.data
    assert len(res.data["projects"]) >= 2


@pytest.mark.asyncio
async def test_submit_contact_form_tool():
    """Test submit_contact_form tool execution."""
    res = await tool_registry.execute_tool("submit_contact_form")
    assert res.success is True
    assert res.data["action"] == "open_contact_modal"


@pytest.mark.asyncio
async def test_invalid_tool():
    """Test execution of non-existent tool."""
    res = await tool_registry.execute_tool("non_existent_tool")
    assert res.success is False
