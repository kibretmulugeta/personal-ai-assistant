"""
Database models subpackage initialization.
Exports all SQLAlchemy models for Alembic auto-generation and application usage.
"""

from packages.database.models.base import Base, BaseModel
from packages.database.models.contact import ContactSubmission
from packages.database.models.conversation import Conversation, Message
from packages.database.models.document import Document, DocumentChunk

__all__ = [
    "Base",
    "BaseModel",
    "Conversation",
    "Message",
    "Document",
    "DocumentChunk",
    "ContactSubmission",
]
