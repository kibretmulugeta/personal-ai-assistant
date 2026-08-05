"""
Unit tests for RAG embedding provider factory and retrieval pipeline.
"""

import pytest
from packages.rag.embeddings.factory import EmbeddingFactory


@pytest.mark.asyncio
async def test_embedding_factory():
    """Verify embedding provider vector generation."""
    provider = EmbeddingFactory.get_provider("openai")
    vector = await provider.embed_query("Stroke lesion segmentation")

    assert len(vector) == provider.dimension
    assert isinstance(vector[0], float)


@pytest.mark.asyncio
async def test_embed_documents_batch():
    """Verify batch document embedding generation."""
    provider = EmbeddingFactory.get_provider("sentence_transformers")
    texts = ["Paragraph 1 about U-Net", "Paragraph 2 about Genetic Algorithms"]
    vectors = await provider.embed_documents(texts)

    assert len(vectors) == 2
    assert len(vectors[0]) == provider.dimension
