"""
OpenRouter LLM Adapter implementation using HTTPX AsyncClient (OpenAI-compatible endpoint).
"""

from typing import AsyncGenerator, List, Any
from packages.llm.base import BaseLLMAdapter, LLMMessage, LLMResponse
from packages.llm.openai_adapter import OpenAIAdapter


class OpenRouterAdapter(BaseLLMAdapter):
    """OpenRouter API adapter providing access to 100+ open and proprietary models."""

    def __init__(self, model_name: str = "meta-llama/llama-3.1-70b-instruct", api_key: str = "") -> None:
        super().__init__(model_name=model_name, api_key=api_key)
        self.openai_delegate = OpenAIAdapter(model_name=model_name, api_key=api_key)
        self.openai_delegate.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> LLMResponse:
        return await self.openai_delegate.generate(
            messages=messages, temperature=temperature, max_tokens=max_tokens, **kwargs
        )

    async def stream(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> AsyncGenerator[str, None]:
        async for token in self.openai_delegate.stream(
            messages=messages, temperature=temperature, max_tokens=max_tokens, **kwargs
        ):
            yield token
