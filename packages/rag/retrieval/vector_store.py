"""
Vector Store manager handling chunk persistence and pgvector similarity querying.
"""

from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models.document import Document, DocumentChunk
from packages.database.repositories.document_repo import (
    DocumentChunkRepository,
    DocumentRepository,
)
from packages.rag.chunking.recursive_chunker import TextChunk
from packages.rag.embeddings.base import BaseEmbeddingProvider
from packages.rag.ingestion.base import ParsedDocument


class VectorStore:
    """Manages document chunk persistence and similarity queries."""

    def __init__(self, session: AsyncSession, embedding_provider: BaseEmbeddingProvider) -> None:
        self.session = session
        self.embedding_provider = embedding_provider
        self.doc_repo = DocumentRepository(session=session)
        self.chunk_repo = DocumentChunkRepository(session=session)

    async def ingest_parsed_document(
        self, parsed_doc: ParsedDocument, text_chunks: List[TextChunk]
    ) -> Document:
        """Store parsed document record and embedded chunks into database."""
        # Check for duplicate document
        existing = await self.doc_repo.get_by_checksum(parsed_doc.checksum)
        if existing:
            return existing

        # Create Document record
        doc_record = await self.doc_repo.create(
            filename=parsed_doc.filename,
            file_type=parsed_doc.file_type,
            storage_path=f"storage/{parsed_doc.filename}",
            checksum=parsed_doc.checksum,
            status="indexed",
            metadata_json=parsed_doc.metadata,
        )

        if text_chunks:
            texts = [c.content for c in text_chunks]
            embeddings = await self.embedding_provider.embed_documents(texts)

            for chunk, emb in zip(text_chunks, embeddings):
                await self.chunk_repo.create(
                    document_id=doc_record.id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    embedding=emb,
                    metadata_json=chunk.metadata,
                )

        return doc_record

    async def similarity_search(
        self, query: str, top_k: int = 5
    ) -> List[Tuple[DocumentChunk, float]]:
        """Perform semantic similarity search on query vector."""
        query_vector = await self.embedding_provider.embed_query(query)
        return await self.chunk_repo.search_similar_chunks(query_vector=query_vector, top_k=top_k)
