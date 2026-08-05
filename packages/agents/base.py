"""
Base Agent abstractions for Multi-Agent System architecture.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from packages.llm.base import BaseLLMAdapter


class AgentDecision(BaseModel):
    """Routing decision produced by the Router Agent."""

    route: str = Field(..., description="Route target: 'KNOWLEDGE', 'ACTION', 'GENERAL'")
    confidence: float = Field(default=1.0, description="Routing confidence score between 0.0 and 1.0")
    reasoning: str = Field(default="", description="Reasoning behind routing decision")
    action_name: Optional[str] = Field(default=None, description="Action name if route is 'ACTION'")
    action_args: Dict[str, Any] = Field(default_factory=dict, description="Extracted parameters for action execution")


class BaseAgent(ABC):
    """Abstract Base Agent for all specialized agents."""

    def __init__(self, llm_adapter: BaseLLMAdapter) -> None:
        self.llm_adapter = llm_adapter

    @abstractmethod
    async def process(self, input_text: str, **kwargs: Any) -> Any:
        """Process user input asynchronously."""
        pass
