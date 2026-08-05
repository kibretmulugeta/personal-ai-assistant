"""
Ollama Local Model Adapter implementation using HTTPX AsyncClient.
"""

import json
from typing import AsyncGenerator, List, Any
import httpx

from packages.llm.base import BaseLLMAdapter, LLMMessage, LLMResponse


class OllamaAdapter(BaseLLMAdapter):
    """Ollama local model adapter supporting Llama 3, Mistral, Qwen, DeepSeek local models."""

    def __init__(self, model_name: str = "llama3:latest", base_url: str = "http://localhost:11434") -> None:
        super().__init__(model_name=model_name, api_key="")
        self.base_url = f"{base_url.rstrip('/')}/api/chat"

    async def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> LLMResponse:
        payload = {
            "model": self.model_name,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(self.base_url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                content = data.get("message", {}).get("content", "")

                return LLMResponse(
                    content=content,
                    tokens_used=data.get("eval_count", 0),
                    model_name=self.model_name,
                    raw_response=data,
                )
        except Exception as e:
            last_msg = messages[-1].content if messages else ""
            return LLMResponse(
                content=f"[Ollama Offline Fallback ({str(e)})] Echo: {last_msg}",
                tokens_used=0,
                model_name=self.model_name,
            )

    async def stream(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> AsyncGenerator[str, None]:
        payload = {
            "model": self.model_name,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": True,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream("POST", self.base_url, json=payload) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                                token = chunk.get("message", {}).get("content", "")
                                if token:
                                    yield token
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            last_msg = messages[-1].content if messages else ""
            yield f"[Ollama Offline Stream Fallback ({str(e)})] Response to: {last_msg}"
