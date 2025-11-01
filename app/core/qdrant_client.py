from qdrant_client import QdrantClient
from app.core.config import settings

qdrant = QdrantClient(url=settings.QDRANT_URL)
