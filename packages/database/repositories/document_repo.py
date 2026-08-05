"""
Repository for Document and DocumentChunk model operations, including pgvector similarity search.
"""

from typing import List, Optional, Tuple
import uuid
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models.document import Document, DocumentChunk
from packages.database.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """Async repository for Document management."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Document, session=session)

    async def get_by_checksum(self, checksum: str) -> Optional[Document]:
        result = await self.session.execute(
            select(Document).where(Document.checksum == checksum)
        )
        return result.scalars().first()

    async def get_with_chunks(self, document_id: uuid.UUID) -> Optional[Document]:
        result = await self.session.execute(
            select(Document)
            .options(selectinload(Document.chunks))
            .where(Document.id == document_id)
        )
        return result.scalars().first()


class DocumentChunkRepository(BaseRepository[DocumentChunk]):
    """Async repository for DocumentChunk operations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=DocumentChunk, session=session)

    async def search_similar_chunks(
        self, query_vector: List[float], top_k: int = 5
    ) -> List[Tuple[DocumentChunk, float]]:
        """Perform vector similarity search using pgvector cosine distance if available."""
        if hasattr(DocumentChunk.embedding, "cosine_distance"):
            distance_col = DocumentChunk.embedding.cosine_distance(query_vector).label("distance")
            result = await self.session.execute(
                select(DocumentChunk, distance_col)
                .order_by(distance_col)
                .limit(top_k)
            )
            return [(row[0], float(row[1])) for row in result.all()]
        else:
            result = await self.session.execute(
                select(DocumentChunk).limit(top_k)
            )
            return [(chunk, 0.0) for chunk in result.scalars().all()]
