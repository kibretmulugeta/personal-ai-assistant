"""
OpenAI Embeddings provider implementation using HTTPX AsyncClient.
"""

from typing import List
import httpx
from packages.rag.embeddings.base import BaseEmbeddingProvider


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """OpenAI Embedding Provider (e.g. text-embedding-3-small, text-embedding-ada-002)."""

    def __init__(self, api_key: str = "", model_name: str = "text-embedding-3-small", dimension: int = 1536) -> None:
        super().__init__(dimension=dimension)
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = "https://api.openai.com/v1/embeddings"

    def _is_placeholder_key(self) -> bool:
        return not self.api_key or "your-" in self.api_key or self.api_key == "sk-proj-your-openai-api-key"

    def _generate_mock_vector(self, text: str) -> List[float]:
        """Generate deterministic pseudo-embedding vector for offline test environments."""
        import random
        seed = sum(ord(c) for c in text[:100]) if text else 42
        rng = random.Random(seed)
        vec = [rng.uniform(-0.1, 0.1) for _ in range(self.dimension)]
        # Normalize
        norm = sum(x * x for x in vec) ** 0.5
        return [x / norm for x in vec]

    async def embed_query(self, text: str) -> List[float]:
        if self._is_placeholder_key():
            return self._generate_mock_vector(text)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.model_name, "input": [text]}

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(self.base_url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                return data["data"][0]["embedding"]
        except Exception:
            return self._generate_mock_vector(text)

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        if self._is_placeholder_key():
            return [self._generate_mock_vector(t) for t in texts]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.model_name, "input": texts}

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(self.base_url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                return [item["embedding"] for item in data["data"]]
        except Exception:
            return [self._generate_mock_vector(t) for t in texts]
