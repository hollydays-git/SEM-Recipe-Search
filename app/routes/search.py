from fastapi import APIRouter, Query
from sentence_transformers import SentenceTransformer
from app.core.qdrant_client import  qdrant
from app.core.config import settings

router = APIRouter(prefix="/search", tags=["search"])
model = SentenceTransformer("all-MiniLM-L6-v2")


@router.get("/")
def search_recipes(q: str = Query(..., description="Search query")):

    #create embedding from user query
    query_vector = model.encode(q).tolist()

    #search in qdrant
    search_result = qdrant.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=query_vector,
        limit=5
    )

    #format result
    results = [
        {
            "name": hit.payload.get("name", "Unknown"),
            "score": hit.score
        } for hit in search_result
    ]

    return {"query": q, "results": results}
