"""
Dynamic LLM Factory creating active provider adapter instance based on configuration settings.
"""

from typing import Optional
from apps.backend.app.core.config import settings
from packages.llm.anthropic_adapter import AnthropicAdapter
from packages.llm.base import BaseLLMAdapter
from packages.llm.gemini_adapter import GeminiAdapter
from packages.llm.groq_adapter import GroqAdapter
from packages.llm.ollama_adapter import OllamaAdapter
from packages.llm.openai_adapter import OpenAIAdapter
from packages.llm.openrouter_adapter import OpenRouterAdapter


class LLMFactory:
    """Factory for instantiating LLM adapters."""

    @staticmethod
    def get_adapter(provider_name: Optional[str] = None) -> BaseLLMAdapter:
        """Instantiate and return an LLM provider adapter.

        Args:
            provider_name: Optional explicit provider name ('openai', 'anthropic', 'google_gemini', etc.).
                          Defaults to settings.ACTIVE_LLM_PROVIDER.

        Returns:
            An instance of BaseLLMAdapter.
        """
        provider = (provider_name or settings.ACTIVE_LLM_PROVIDER).lower()

        if provider == "openai":
            return OpenAIAdapter(
                model_name="gpt-4o-mini",
                api_key=settings.OPENAI_API_KEY or "",
            )
        elif provider == "anthropic":
            return AnthropicAdapter(
                model_name="claude-3-5-sonnet-20240620",
                api_key=settings.ANTHROPIC_API_KEY or "",
            )
        elif provider in ["google_gemini", "gemini"]:
            return GeminiAdapter(
                model_name="gemini-1.5-flash",
                api_key=settings.GEMINI_API_KEY or "",
            )
        elif provider == "groq":
            return GroqAdapter(
                model_name="llama-3.1-70b-versatile",
                api_key=settings.GROQ_API_KEY or "",
            )
        elif provider == "openrouter":
            return OpenRouterAdapter(
                model_name="meta-llama/llama-3.1-70b-instruct",
                api_key=settings.OPENROUTER_API_KEY or "",
            )
        elif provider == "ollama":
            return OllamaAdapter(
                model_name="llama3:latest",
                base_url=settings.OLLAMA_BASE_URL,
            )
        else:
            # Fallback to OpenAI adapter
            return OpenAIAdapter(
                model_name="gpt-4o-mini",
                api_key=settings.OPENAI_API_KEY or "",
            )
