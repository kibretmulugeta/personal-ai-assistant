"""
Pydantic schemas for chat requests, SSE events, and WebSocket messages.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChatMessageSchema(BaseModel):
    """Message item schema."""
    role: str = Field(..., description="Role: 'user', 'assistant', 'system', 'tool'")
    content: str = Field(..., description="Message content string")


class SourceAttributionSchema(BaseModel):
    """Source attribution citation item."""
    document_id: str
    filename: str
    chunk_index: int
    similarity_score: float
    snippet: str


class ChatRequest(BaseModel):
    """Chat message submission payload."""
    message: str = Field(..., min_length=1, description="Visitor query text")
    session_id: Optional[str] = Field(default=None, description="Visitor chat session ID")
    history: Optional[List[ChatMessageSchema]] = Field(default_factory=list, description="Recent message history")


class ChatResponse(BaseModel):
    """Standard REST response payload."""
    response: str = Field(..., description="Assistant text response")
    route: str = Field(..., description="Chosen agent route ('KNOWLEDGE', 'ACTION', 'GENERAL')")
    session_id: str = Field(..., description="Conversation session ID")
    action: Optional[Dict[str, Any]] = Field(default=None, description="Action execution details if triggered")
    sources: List[SourceAttributionSchema] = Field(default_factory=list, description="RAG source citations")
    tokens_used: int = Field(default=0, description="Total tokens consumed")
