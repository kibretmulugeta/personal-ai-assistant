"""
Dynamic prompt template helper for combining persona, retrieved context, and conversation history.
"""

from typing import List, Optional
from packages.llm.base import LLMMessage
from packages.prompts.persona import DIGITAL_TWIN_PERSONA


def build_system_prompt(retrieved_context: Optional[str] = None) -> str:
    """Build system prompt with optional RAG context injection."""
    system_prompt = DIGITAL_TWIN_PERSONA
    if retrieved_context and retrieved_context.strip():
        system_prompt += (
            f"\n\n### RETRIEVED KNOWLEDGE CONTEXT\n"
            f"Use the following authoritative context to answer the user's inquiry:\n"
            f"'''\n{retrieved_context}\n'''\n"
        )
    return system_prompt


def build_prompt_messages(
    user_message: str,
    history: Optional[List[LLMMessage]] = None,
    retrieved_context: Optional[str] = None,
) -> List[LLMMessage]:
    """Construct full list of LLM prompt messages including system persona, history, and current message."""
    messages = [LLMMessage(role="system", content=build_system_prompt(retrieved_context))]
    if history:
        messages.extend(history)
    messages.append(LLMMessage(role="user", content=user_message))
    return messages
