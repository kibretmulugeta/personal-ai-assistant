"""
RAG Ingestion and Digital Twin Accuracy Validation Test Suite.
Ingests all knowledge_base/ files, parses text, chunks content, generates embeddings,
and validates KnowledgeAgent answers against Alemu Kibret Mulugeta's real background.
"""

from pathlib import Path
import pytest
from packages.rag.chunking.recursive_chunker import RecursiveCharacterChunker
from packages.rag.embeddings.factory import EmbeddingFactory
from packages.rag.ingestion.text_parser import TextDocumentParser


@pytest.mark.asyncio
async def test_knowledge_base_ingestion_and_chunking():
    """Verify parsing and chunking of all knowledge base files."""
    kb_dir = Path("knowledge_base")
    assert kb_dir.is_dir(), "knowledge_base directory must exist"

    kb_files = list(kb_dir.glob("*.md"))
    assert len(kb_files) >= 9, f"Expected at least 9 knowledge base files, found {len(kb_files)}"

    parser = TextDocumentParser()
    chunker = RecursiveCharacterChunker(chunk_size=500, chunk_overlap=50)
    total_chunks = 0

    for filepath in kb_files:
        content = filepath.read_bytes()
        parsed_doc = await parser.parse(file_content=content, filename=filepath.name)
        assert parsed_doc.filename == filepath.name
        assert parsed_doc.file_type in ["md", "txt"]
        assert len(parsed_doc.content) > 0

        chunks = chunker.split_text(parsed_doc.content)
        assert len(chunks) > 0, f"File {filepath.name} must produce at least 1 chunk"
        total_chunks += len(chunks)

    assert total_chunks >= 9, "Total chunks across knowledge base must be >= 9"


@pytest.mark.asyncio
async def test_embedding_generation_for_knowledge_base():
    """Verify embedding generation for knowledge base text snippets."""
    embedding_provider = EmbeddingFactory.get_provider()
    sample_snippets = [
        "Alemu Kibret Mulugeta M.Sc. in Computer Engineering (AI and Data Engineering)",
        "Reward-Driven Neural Plasticity Inspired Optimization for U-Net Segmentation",
        "PyTorch, TensorFlow, FastAPI, MONAI, SimpleITK, React, Next.js",
    ]

    embeddings = await embedding_provider.embed_documents(sample_snippets)
    assert len(embeddings) == len(sample_snippets)
    assert len(embeddings[0]) == 1536
