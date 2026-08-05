"""
Unit tests for LLM Factory and provider adapter instantiation/streaming.
"""

import pytest
from packages.llm.base import LLMMessage
from packages.llm.factory import LLMFactory
from packages.llm.openai_adapter import OpenAIAdapter


@pytest.mark.asyncio
async def test_llm_factory_default():
    """Verify default adapter returned by LLMFactory."""
    adapter = LLMFactory.get_adapter()
    assert adapter is not None


@pytest.mark.asyncio
async def test_openai_adapter_mock_generate():
    """Verify OpenAI adapter generate mock output when API key is empty."""
    adapter = OpenAIAdapter(model_name="gpt-4o-mini", api_key="")
    messages = [LLMMessage(role="user", content="Hello Alemu")]

    response = await adapter.generate(messages)
    assert response.content is not None
    assert "Mock" in response.content or "Received" in response.content


@pytest.mark.asyncio
async def test_openai_adapter_mock_stream():
    """Verify OpenAI adapter stream mock tokens."""
    adapter = OpenAIAdapter(model_name="gpt-4o-mini", api_key="")
    messages = [LLMMessage(role="user", content="Tell me about your research")]

    tokens = []
    async for token in adapter.stream(messages):
        tokens.append(token)

    full_text = "".join(tokens)
    assert len(tokens) > 0
    assert "Hello" in full_text or "Alemu" in full_text
