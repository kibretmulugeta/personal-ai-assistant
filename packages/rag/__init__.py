"""
RAG package initialization.
"""

from packages.rag.chunking import RecursiveCharacterChunker
from packages.rag.embeddings import EmbeddingFactory
from packages.rag.ingestion import (
    DOCXDocumentParser,
    PDFDocumentParser,
    TextDocumentParser,
)
from packages.rag.retrieval import RetrievalPipeline, VectorStore

__all__ = [
    "PDFDocumentParser",
    "DOCXDocumentParser",
    "TextDocumentParser",
    "RecursiveCharacterChunker",
    "EmbeddingFactory",
    "VectorStore",
    "RetrievalPipeline",
]
