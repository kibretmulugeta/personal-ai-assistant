"""
Sentence Transformers / BGE / E5 Local Embedding Provider implementation.
"""

from typing import List
from packages.rag.embeddings.base import BaseEmbeddingProvider

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False


class SentenceTransformerEmbeddingProvider(BaseEmbeddingProvider):
    """Local Sentence Transformers embedding provider for BGE, E5, or MiniLM models."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5", dimension: int = 1536) -> None:
        super().__init__(dimension=dimension)
        self.model_name = model_name
        self.model = None
        if HAS_SENTENCE_TRANSFORMERS:
            try:
                self.model = SentenceTransformer(model_name)
            except Exception:
                self.model = None

    def _mock_vector(self, text: str) -> List[float]:
        import random
        seed = sum(ord(c) for c in text[:100]) if text else 42
        rng = random.Random(seed)
        vec = [rng.uniform(-0.1, 0.1) for _ in range(self.dimension)]
        norm = sum(x * x for x in vec) ** 0.5
        return [x / norm for x in vec]

    async def embed_query(self, text: str) -> List[float]:
        if self.model:
            vector = self.model.encode(text).tolist()
            # Pad or truncate to self.dimension if necessary
            if len(vector) < self.dimension:
                vector.extend([0.0] * (self.dimension - len(vector)))
            return vector[: self.dimension]
        return self._mock_vector(text)

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self.model and texts:
            vectors = self.model.encode(texts).tolist()
            padded = []
            for v in vectors:
                if len(v) < self.dimension:
                    v.extend([0.0] * (self.dimension - len(v)))
                padded.append(v[: self.dimension])
            return padded
        return [self._mock_vector(t) for t in texts]
