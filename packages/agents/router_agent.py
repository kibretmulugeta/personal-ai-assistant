"""
Router Agent implementation responsible for intent classification and request routing.
"""

import json
from typing import Any
from packages.agents.base import AgentDecision, BaseAgent
from packages.llm.base import LLMMessage
from packages.prompts.router_prompts import ROUTER_INTENT_SYSTEM_PROMPT


class RouterAgent(BaseAgent):
    """Router Agent classifying user intent into KNOWLEDGE, ACTION, or GENERAL routes."""

    async def process(self, input_text: str, **kwargs: Any) -> AgentDecision:
        """Classify input text into target route."""
        text_lower = input_text.lower().strip()

        # Fast rule-based keyword routing for common action intent
        if any(w in text_lower for w in ["resume", "cv", "download resume", "download cv"]):
            return AgentDecision(
                route="ACTION",
                confidence=0.98,
                reasoning="Keyword match for resume/CV download request",
                action_name="download_resume",
            )
        if any(w in text_lower for w in ["contact", "email", "send message", "get in touch", "hire"]):
            return AgentDecision(
                route="ACTION",
                confidence=0.95,
                reasoning="Keyword match for contact request",
                action_name="submit_contact_form",
            )
        if any(w in text_lower for w in ["projects", "portfolio", "github"]):
            return AgentDecision(
                route="ACTION",
                confidence=0.90,
                reasoning="Keyword match for projects list request",
                action_name="list_projects",
            )

        # Fallback to LLM classification
        try:
            messages = [
                LLMMessage(role="system", content=ROUTER_INTENT_SYSTEM_PROMPT),
                LLMMessage(role="user", content=input_text),
            ]
            response = await self.llm_adapter.generate(messages=messages, temperature=0.1)
            raw_content = response.content.strip()

            # Strip possible markdown code fence
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:-3].strip()
            elif raw_content.startswith("```"):
                raw_content = raw_content[3:-3].strip()

            data = json.loads(raw_content)
            return AgentDecision(
                route=data.get("route", "KNOWLEDGE"),
                confidence=data.get("confidence", 0.85),
                reasoning=data.get("reasoning", "LLM classified intent"),
                action_name=data.get("action_name"),
            )
        except Exception:
            # Safe default fallback to KNOWLEDGE route
            return AgentDecision(
                route="KNOWLEDGE",
                confidence=0.70,
                reasoning="Default fallback route for general inquiry",
            )
