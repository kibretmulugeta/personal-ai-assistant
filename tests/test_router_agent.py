"""
Unit tests for Router Agent intent classification logic.
"""

import pytest
from packages.agents.router_agent import RouterAgent
from packages.llm.openai_adapter import OpenAIAdapter


@pytest.mark.asyncio
async def test_router_agent_keyword_action():
    """Test fast keyword routing for resume download."""
    adapter = OpenAIAdapter(model_name="gpt-4o-mini", api_key="")
    router_agent = RouterAgent(llm_adapter=adapter)

    decision = await router_agent.process("Can I download your resume?")
    assert decision.route == "ACTION"
    assert decision.action_name == "download_resume"


@pytest.mark.asyncio
async def test_router_agent_keyword_contact():
    """Test fast keyword routing for contact request."""
    adapter = OpenAIAdapter(model_name="gpt-4o-mini", api_key="")
    router_agent = RouterAgent(llm_adapter=adapter)

    decision = await router_agent.process("How can I contact Alemu?")
    assert decision.route == "ACTION"
    assert decision.action_name == "submit_contact_form"


@pytest.mark.asyncio
async def test_router_agent_fallback_knowledge():
    """Test fallback classification to KNOWLEDGE route."""
    adapter = OpenAIAdapter(model_name="gpt-4o-mini", api_key="")
    router_agent = RouterAgent(llm_adapter=adapter)

    decision = await router_agent.process("Tell me about your M.Sc. thesis on U-Net stroke segmentation.")
    assert decision.route in ["KNOWLEDGE", "ACTION"]
