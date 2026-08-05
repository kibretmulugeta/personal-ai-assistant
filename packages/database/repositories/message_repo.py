"""
Repository for Message model operations.
"""

from typing import List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models.conversation import Message
from packages.database.repositories.base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """Async repository for Message operations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Message, session=session)

    async def get_by_conversation_id(
        self, conversation_id: uuid.UUID, limit: int = 50
    ) -> List[Message]:
        """Fetch messages belonging to a conversation ordered chronologically."""
        result = await self.session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())
