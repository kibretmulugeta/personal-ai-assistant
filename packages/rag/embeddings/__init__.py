"""
Embeddings subpackage initialization.
"""

from packages.rag.embeddings.base import BaseEmbeddingProvider
from packages.rag.embeddings.factory import EmbeddingFactory

__all__ = ["BaseEmbeddingProvider", "EmbeddingFactory"]
