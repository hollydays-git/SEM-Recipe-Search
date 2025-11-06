from fastapi import APIRouter, Query
from app.core.qdrant_client import qdrant
from app.core.config import settings
from sentence_transformers import SentenceTransformer

router = APIRouter()

# initialize the model (once)
model = SentenceTransformer("all-mpnet-base-v2")

@router.get("/recipes/match")
async def match_recipes(query: str = Query(..., description="User input text")):
    """
    Match recipes based on user-provided text input (e.g. ingredients or description).
    """

    # encode the input text into a vector
    query_vector = model.encode(query).tolist()

    # search similar recipes in Qdrant
    results = qdrant.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=query_vector,
        limit=5
    )

    # format response
    response = [
        {
            "id": hit.id,
            "score": hit.score,
            "recipe_name": hit.payload.get("title"),
            "ingredients": hit.payload.get("ingredients"),
            "instructions": hit.payload.get("instructions"),
            "image_url": hit.payload.get("image_url")
        }
        for hit in results
    ]

    return {"query": query, "results": response}
