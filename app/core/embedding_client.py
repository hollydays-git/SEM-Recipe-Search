from typing import List, Optional

import httpx

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmbeddingClient:
    """Async client for the standalone embedding service."""

    def __init__(self) -> None:
        self._client: Optional[httpx.AsyncClient] = None

    async def connect(self) -> None:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=settings.EMBEDDING_SERVICE_URL,
                timeout=30,
            )
            logger.info("Embedding client connected to %s", settings.EMBEDDING_SERVICE_URL)

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.info("Embedding client closed")

    async def embed(self, texts: List[str], prefix: Optional[str] = None) -> List[List[float]]:
        if not texts:
            return []
        if self._client is None:
            raise RuntimeError("Embedding client is not connected")

        payload = {
            "texts": texts,
            "prefix": prefix if prefix is not None else settings.EMBEDDING_SERVICE_PREFIX,
            "normalize": settings.EMBEDDING_SERVICE_NORMALIZE,
        }
        logger.debug("Requesting embeddings for %d texts", len(texts))
        response = await self._client.post("/embed", json=payload)
        response.raise_for_status()
        data = response.json()
        embeddings = data.get("embeddings")
        if embeddings is None:
            raise ValueError("Embedding service response missing 'embeddings'")
        logger.debug("Received %d embeddings", len(embeddings))
        return embeddings

    async def embed_queries(self, texts: List[str]) -> List[List[float]]:
        return await self.embed(texts, prefix="query:")


embedding_client = EmbeddingClient()
