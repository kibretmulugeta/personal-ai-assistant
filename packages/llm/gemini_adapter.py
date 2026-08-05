"""
Google Gemini Adapter implementation using HTTPX AsyncClient.
"""

import json
from typing import AsyncGenerator, List, Any
import httpx

from packages.llm.base import BaseLLMAdapter, LLMMessage, LLMResponse


class GeminiAdapter(BaseLLMAdapter):
    """Google Gemini API adapter supporting Gemini 1.5 Pro, Gemini 1.5 Flash."""

    def __init__(self, model_name: str = "gemini-3.5-flash", api_key: str = "") -> None:
        super().__init__(model_name=model_name, api_key=api_key)
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

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
                content=f"[Gemini Offline Mock] Received: {last_msg}",
                tokens_used=10,
                model_name=self.model_name,
            )

        url = f"{self.base_url}?key={self.api_key}"
        contents = []
        for m in messages:
            role = "user" if m.role in ["user", "system"] else "model"
            contents.append({"role": role, "parts": [{"text": m.content}]})

        payload = {
            "contents": contents,
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = data["candidates"][0]["content"]["parts"][0]["text"]

            return LLMResponse(
                content=content,
                tokens_used=0,
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
            mock_tokens = f"[Gemini Offline Stream] Response to: {last_msg}".split()
            for token in mock_tokens:
                yield token + " "
            return

        stream_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:streamGenerateContent?key={self.api_key}&alt=sse"
        contents = []
        for m in messages:
            role = "user" if m.role in ["user", "system"] else "model"
            contents.append({"role": role, "parts": [{"text": m.content}]})

        payload = {
            "contents": contents,
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", stream_url, json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        try:
                            chunk_data = json.loads(data_str)
                            parts = chunk_data["candidates"][0]["content"]["parts"]
                            for part in parts:
                                if "text" in part:
                                    yield part["text"]
                        except json.JSONDecodeError:
                            continue
