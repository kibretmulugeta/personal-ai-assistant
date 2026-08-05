"""
Anthropic Claude Adapter implementation using HTTPX AsyncClient.
"""

import json
from typing import AsyncGenerator, List, Any
import httpx

from packages.llm.base import BaseLLMAdapter, LLMMessage, LLMResponse


class AnthropicAdapter(BaseLLMAdapter):
    """Anthropic API adapter supporting Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku."""

    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620", api_key: str = "") -> None:
        super().__init__(model_name=model_name, api_key=api_key)
        self.base_url = "https://api.anthropic.com/v1/messages"

    async def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> LLMResponse:
        if not self.api_key:
            last_msg = messages[-1].content if messages else ""
            return LLMResponse(
                content=f"[Anthropic Offline Mock] Received: {last_msg}",
                tokens_used=10,
                model_name=self.model_name,
            )

        system_prompt = "\n".join([m.content for m in messages if m.role == "system"])
        user_msgs = [{"role": m.role if m.role != "system" else "user", "content": m.content} for m in messages if m.role != "system"]

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": user_msgs,
            "system": system_prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(self.base_url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = data["content"][0]["text"]
            tokens = data.get("usage", {}).get("input_tokens", 0) + data.get("usage", {}).get("output_tokens", 0)

            return LLMResponse(
                content=content,
                tokens_used=tokens,
                model_name=self.model_name,
                raw_response=data,
            )

    async def stream(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> AsyncGenerator[str, None]:
        if not self.api_key:
            last_msg = messages[-1].content if messages else ""
            mock_tokens = f"[Anthropic Offline Stream] Response to: {last_msg}".split()
            for token in mock_tokens:
                yield token + " "
            return

        system_prompt = "\n".join([m.content for m in messages if m.role == "system"])
        user_msgs = [{"role": m.role if m.role != "system" else "user", "content": m.content} for m in messages if m.role != "system"]

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": user_msgs,
            "system": system_prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", self.base_url, headers=headers, json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        try:
                            event = json.loads(data_str)
                            if event.get("type") == "content_block_delta":
                                yield event["delta"].get("text", "")
                        except json.JSONDecodeError:
                            continue
