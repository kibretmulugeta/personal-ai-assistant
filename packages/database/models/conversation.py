"""
Conversation and Message models for storing user interactions with the Digital Twin.
"""

from typing import List, Optional
from sqlalchemy import String, Text, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from packages.database.models.base import BaseModel


class Conversation(BaseModel):
    """Represents a chat session with the AI Assistant."""

    __tablename__ = "conversations"

    session_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, default=dict, nullable=True)

    # Relationships
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )


class Message(BaseModel):
    """Represents an individual message exchanged within a conversation."""

    __tablename__ = "messages"

    conversation_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # user | assistant | system | tool
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tokens_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, default=dict, nullable=True)

    # Relationship
    conversation: Mapped["Conversation"] = relationship(
        "Conversation", back_populates="messages"
    )
