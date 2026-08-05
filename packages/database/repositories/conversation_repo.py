"""
Repository for Conversation model operations.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models.conversation import Conversation
from packages.database.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    """Async repository for Conversation operations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Conversation, session=session)

    async def get_by_session_id(self, session_id: str) -> Optional[Conversation]:
        """Retrieve conversation by visitor session ID."""
        result = await self.session.execute(
            select(Conversation).where(Conversation.session_id == session_id)
        )
        return result.scalars().first()

    async def get_with_messages(self, session_id: str) -> Optional[Conversation]:
        """Retrieve conversation with eager-loaded messages."""
        result = await self.session.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.session_id == session_id)
        )
        return result.scalars().first()

    async def list_recent_sessions(self, limit: int = 50) -> List[Conversation]:
        """List recently updated conversations."""
        result = await self.session.execute(
            select(Conversation)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
