from fastapi import APIRouter, Query, HTTPException
from app.core.qdrant_service import qdrant
from app.core.config import settings
from sentence_transformers import SentenceTransformer

router = APIRouter()

# load the same model that was used for creating embeddings
model = SentenceTransformer("intfloat/e5-base-v2")


@router.get("/recipes/match")
async def match_recipes(query: str = Query(..., description="Text input (ingredients, description, etc.)")):
    """
    Find recipes that are semantically similar to the user’s query.
    """

    # basic cleanup
    clean_query = query.strip().lower()
    if not clean_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        # e5 models expect a prefix and normalized embeddings
        formatted_query = f"query: {clean_query}"
        query_vector = model.encode(
            [formatted_query],
            normalize_embeddings=True
        )[0].tolist()

        # search in qdrant
        results = qdrant.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=query_vector,
            limit=5
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    # if nothing found
    if not results:
        return {
            "query": query,
            "results": [],
            "message": "No similar recipes found. Try changing your keywords."
        }

    # format the output
    response = [
        {
            "id": hit.id,
            "score": round(hit.score, 3),
            "recipe_name": hit.payload.get("title"),
            "ingredients": hit.payload.get("ingredients"),
            "instructions": hit.payload.get("instructions"),
            "image_url": hit.payload.get("image_url"),
        }
        for hit in results
    ]

    return {"query": query, "results": response}
