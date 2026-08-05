"""
FastAPI Dependency Injection providers for database sessions, authentication, LLM adapters, and multi-agent services.
"""

from typing import AsyncGenerator, Optional
from fastapi import Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from packages.agents.action_agent import ActionAgent
from packages.agents.knowledge_agent import KnowledgeAgent
from packages.agents.router_agent import RouterAgent
from packages.auth.api_key import validate_api_key
from packages.auth.jwt import decode_access_token
from packages.database.session import get_async_session
from packages.llm.base import BaseLLMAdapter
from packages.llm.factory import LLMFactory


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injector yielding database session."""
    async for session in get_async_session():
        yield session


def get_llm_adapter() -> BaseLLMAdapter:
    """Dependency injector providing the active LLM provider adapter."""
    return LLMFactory.get_adapter()


def get_router_agent(
    llm_adapter: BaseLLMAdapter = Depends(get_llm_adapter),
) -> RouterAgent:
    """Dependency injector providing RouterAgent instance."""
    return RouterAgent(llm_adapter=llm_adapter)


def get_knowledge_agent(
    llm_adapter: BaseLLMAdapter = Depends(get_llm_adapter),
) -> KnowledgeAgent:
    """Dependency injector providing KnowledgeAgent instance."""
    return KnowledgeAgent(llm_adapter=llm_adapter)


def get_action_agent(
    llm_adapter: BaseLLMAdapter = Depends(get_llm_adapter),
) -> ActionAgent:
    """Dependency injector providing ActionAgent instance."""
    return ActionAgent(llm_adapter=llm_adapter)


def verify_api_key_dep(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
) -> bool:
    """Dependency validating X-API-Key header."""
    return validate_api_key(x_api_key)


def verify_token_dep(
    authorization: Optional[str] = Header(None, alias="Authorization"),
) -> dict:
    """Dependency validating Bearer JWT access token."""
    if not authorization or not authorization.startswith("Bearer "):
        # For development ease, yield a default visitor session payload
        return {"sub": "guest_session", "type": "access_token"}
    token = authorization.split(" ")[1]
    return decode_access_token(token)
