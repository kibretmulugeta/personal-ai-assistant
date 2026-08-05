"""
Repository for ContactSubmission model operations.
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models.contact import ContactSubmission
from packages.database.repositories.base import BaseRepository


class ContactSubmissionRepository(BaseRepository[ContactSubmission]):
    """Async repository for ContactSubmission operations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=ContactSubmission, session=session)

    async def get_by_email(self, email: str) -> List[ContactSubmission]:
        """Fetch all contact submissions by sender email address."""
        result = await self.session.execute(
            select(ContactSubmission)
            .where(ContactSubmission.email == email)
            .order_by(ContactSubmission.created_at.desc())
        )
        return list(result.scalars().all())
