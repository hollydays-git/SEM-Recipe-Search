from fastapi import APIRouter, HTTPException, Query

from app.core.logging import get_logger
from app.core.pg_service import pg_service

router = APIRouter()
logger = get_logger(__name__)

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
        results = await pg_service.fuzzy_match_recipes(clean_query, limit=5)
    except Exception as e:
        logger.exception("Search failed for query '%s'", query)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    if not results:
        return {
            "query": query,
            "results": [],
            "message": "No similar recipes found. Try changing your keywords."
        }

    formatted = []
    for row in results:
        item = row.copy()
        score = item.pop("score", None)
        if score is not None:
            item["score"] = round(score, 3)
        formatted.append(item)

    return {"query": query, "results": formatted}
