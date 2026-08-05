"""
Abstract Base Embedding Provider interface.
"""

from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingProvider(ABC):
    """Abstract interface for text embedding models."""

    def __init__(self, dimension: int = 1536) -> None:
        self.dimension = dimension

    @abstractmethod
    async def embed_query(self, text: str) -> List[float]:
        """Generate embedding vector for a search query string.

        Args:
            text: Query string.

        Returns:
            List of floats representing dense embedding vector.
        """
        pass

    @abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embedding vectors for a list of document chunk texts.

        Args:
            texts: List of text strings.

        Returns:
            List of dense embedding float vectors.
        """
        pass
