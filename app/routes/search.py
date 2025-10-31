from fastapi import APIRouter, Query

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/")
def search_recipes(q: str = Query(..., description="Search query")):
    # Mock response
    results = [
        {"name": "Apple Pie", "similarity": 0.89},
        {"name": "Spicy Malaysian Chicken", "similarity": 0.83},
    ]
    return {"query": q, "results": results}
