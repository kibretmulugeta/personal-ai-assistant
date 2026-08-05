"""
Generic Async Base Repository providing CRUD abstractions.
Decouples database operations from business logic.
"""

from typing import Generic, List, Optional, Type, TypeVar, Any
import uuid
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from packages.database.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Generic async repository interface for basic database CRUD operations."""

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        """
        Args:
            model: The SQLAlchemy model class.
            session: The active async database session.
        """
        self.model = model
        self.session = session

    async def get_by_id(self, id_val: uuid.UUID) -> Optional[ModelType]:
        """Fetch a single record by its UUID primary key."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id_val)
        )
        return result.scalars().first()

    async def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """Fetch multiple records with pagination parameters."""
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        """Count total rows in the table."""
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()

    async def create(self, **kwargs: Any) -> ModelType:
        """Instantiate and persist a new model record."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(
        self, id_val: uuid.UUID, **kwargs: Any
    ) -> Optional[ModelType]:
        """Update fields of an existing record by UUID."""
        await self.session.execute(
            update(self.model)
            .where(self.model.id == id_val)
            .values(**kwargs)
        )
        await self.session.flush()
        return await self.get_by_id(id_val)

    async def delete(self, id_val: uuid.UUID) -> bool:
        """Delete a record by its UUID primary key."""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id_val)
        )
        await self.session.flush()
        return result.rowcount > 0
