"""
Repositories subpackage initialization.
Exports generic and concrete repository classes.
"""

from packages.database.repositories.base import BaseRepository
from packages.database.repositories.contact_repo import ContactSubmissionRepository
from packages.database.repositories.conversation_repo import ConversationRepository
from packages.database.repositories.document_repo import (
    DocumentChunkRepository,
    DocumentRepository,
)
from packages.database.repositories.message_repo import MessageRepository

__all__ = [
    "BaseRepository",
    "ConversationRepository",
    "MessageRepository",
    "DocumentRepository",
    "DocumentChunkRepository",
    "ContactSubmissionRepository",
]
