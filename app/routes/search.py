from fastapi import APIRouter, Query
from app.core.qdrant_client import qdrant
from app.core.config import settings
from sentence_transformers import SentenceTransformer

router = APIRouter()

# Use the same model used for uploading recipe embeddings
model = SentenceTransformer("intfloat/e5-base-v2")

@router.get("/recipes/match")
async def match_recipes(query: str = Query(..., description="User input text (e.g. ingredients or description)")):
    """
    Match recipes based on user-provided text input (semantic search).
    """

    # IMPORTANT: E5 model requires prefix and normalization
    formatted_query = f"query: {query}"
    query_vector = model.encode([formatted_query], normalize_embeddings=True)[0].tolist()

    # Search in Qdrant
    results = qdrant.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=query_vector,
        limit=5
    )

    # Format the response
    response = [
        {
            "id": hit.id,
            "score": hit.score,
            "recipe_name": hit.payload.get("title"),
            "ingredients": hit.payload.get("ingredients"),
            "instructions": hit.payload.get("instructions"),
            "image_url": hit.payload.get("image_url"),
        }
        for hit in results
    ]

    return {"query": query, "results": response}

