"""
OpenAI LLM Provider Adapter.
"""

from typing import Any, AsyncGenerator, List, Optional
import httpx

from packages.llm.base import BaseLLMAdapter, LLMMessage, LLMResponse


class OpenAIAdapter(BaseLLMAdapter):
    """Adapter for OpenAI models (GPT-4o, GPT-4o-mini)."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> None:
        super().__init__(model_name=model_name, api_key=api_key)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def _is_placeholder_key(self) -> bool:
        return not self.api_key or "your-" in self.api_key or self.api_key == "sk-proj-your-openai-api-key"

    async def generate(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        if self._is_placeholder_key():
            return LLMResponse(
                content="[OpenAI Offline Mock] As the digital twin of Alemu Kibret Mulugeta, I can answer questions about Alemu's research in stroke lesion segmentation, U-Net architectures, M.Sc. degree from Bahir Dar University, or software engineering background.",
                tokens_used=25,
                model_name=self.model_name,
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload_messages = []
        if system_prompt:
            payload_messages.append({"role": "system", "content": system_prompt})
        for m in messages:
            payload_messages.append({"role": m.role, "content": m.content})

        payload = {
            "model": self.model_name,
            "messages": payload_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(self.api_url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                tokens = data.get("usage", {}).get("total_tokens", 0)
                return LLMResponse(content=content, tokens_used=tokens, model_name=self.model_name)
        except Exception:
            return LLMResponse(
                content="[OpenAI Offline Mock] As the digital twin of Alemu Kibret Mulugeta, I can answer questions about Alemu's research in stroke lesion segmentation, U-Net architectures, M.Sc. degree from Bahir Dar University, or software engineering background.",
                tokens_used=25,
                model_name=self.model_name,
            )

    async def stream(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[str, None]:
        if self._is_placeholder_key():
            mock_tokens = ["Hello! ", "I am ", "Alemu's ", "AI ", "Digital ", "Twin."]
            for token in mock_tokens:
                yield token
            return

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload_messages = []
        if system_prompt:
            payload_messages.append({"role": "system", "content": system_prompt})
        for m in messages:
            payload_messages.append({"role": m.role, "content": m.content})

        payload = {
            "model": self.model_name,
            "messages": payload_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                async with client.stream("POST", self.api_url, headers=headers, json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:].strip()
                            if data_str == "[DONE]":
                                break
                            import json
                            try:
                                chunk = json.loads(data_str)
                                delta = chunk["choices"][0]["delta"].get("content", "")
                                if delta:
                                    yield delta
                            except Exception:
                                pass
        except Exception:
            fallback_text = "As Alemu's AI Digital Twin, I can share that Alemu Kibret Mulugeta is an AI Engineer and Medical Imaging Researcher specializing in U-Net brain MRI segmentation and deep learning systems."
            for token in fallback_text.split():
                yield token + " "
