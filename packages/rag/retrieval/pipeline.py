"""
RAG Retrieval Pipeline & Source Attribution module.
Assembles context strings for LLMs and generates structured citations.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models.document import DocumentChunk
from packages.database.repositories.document_repo import DocumentRepository
from packages.rag.embeddings.base import BaseEmbeddingProvider
from packages.rag.retrieval.vector_store import VectorStore


class SourceAttribution(BaseModel):
    """Citation metadata for a retrieved document chunk."""

    document_id: str = Field(..., description="Document UUID string")
    filename: str = Field(..., description="Document filename")
    chunk_index: int = Field(..., description="Chunk index within document")
    similarity_score: float = Field(..., description="Similarity distance score")
    snippet: str = Field(..., description="Excerpt snippet")


class RetrievalResult(BaseModel):
    """Result of RAG retrieval pipeline."""

    context_text: str = Field(..., description="Assembled context text string")
    sources: List[SourceAttribution] = Field(default_factory=list, description="Source attributions")


class RetrievalPipeline:
    """RAG Retrieval Pipeline executing similarity search, context assembly, and attribution."""

    def __init__(self, session: AsyncSession, embedding_provider: BaseEmbeddingProvider) -> None:
        self.session = session
        self.vector_store = VectorStore(session=session, embedding_provider=embedding_provider)
        self.doc_repo = DocumentRepository(session=session)

    async def retrieve_context(
        self, query: str, top_k: int = 5
    ) -> RetrievalResult:
        """Search similar chunks, assemble LLM context string, and extract source citations."""
        results = await self.vector_store.similarity_search(query=query, top_k=top_k)
        if not results:
            return RetrievalResult(context_text="", sources=[])

        context_blocks: List[str] = []
        sources: List[SourceAttribution] = []

        # Cache document filename lookups
        doc_names: Dict[str, str] = {}

        for chunk, dist in results:
            doc_id_str = str(chunk.document_id)
            if doc_id_str not in doc_names:
                doc = await self.doc_repo.get_by_id(chunk.document_id)
                doc_names[doc_id_str] = doc.filename if doc else "Document"

            fname = doc_names[doc_id_str]
            context_blocks.append(f"[Source: {fname} (Chunk #{chunk.chunk_index})]\n{chunk.content}")

            sources.append(
                SourceAttribution(
                    document_id=doc_id_str,
                    filename=fname,
                    chunk_index=chunk.chunk_index,
                    similarity_score=round(float(dist), 4),
                    snippet=chunk.content[:150] + "..." if len(chunk.content) > 150 else chunk.content,
                )
            )

        assembled_context = "\n\n".join(context_blocks)
        return RetrievalResult(context_text=assembled_context, sources=sources)
