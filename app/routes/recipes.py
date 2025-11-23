from fastapi import APIRouter, HTTPException, Query

from app.core.pg_service import pg_service
from app.schemas.recipes import RecipeCreateRequest
from app.services import recipe_ingest, recipe_recommendations

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/")
async def list_recipes(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    recipes = await pg_service.fetch_recipes(limit=limit, offset=offset)
    return {"items": recipes, "limit": limit, "offset": offset}


@router.get("/search")
async def search_recipes(query: str = Query(..., min_length=1), limit: int = Query(20, ge=1, le=50)):
    results = await pg_service.search_recipes(query=query.strip(), limit=limit)
    return {"items": results, "limit": limit, "query": query}


@router.get("/{recipe_id}")
async def get_recipe(recipe_id: int):
    recipe = await pg_service.fetch_recipe_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/", status_code=201)
async def create_recipe(payload: RecipeCreateRequest):
    recipe = await recipe_ingest.create_recipe(payload)
    return recipe


@router.get("/{recipe_id}/similar")
async def similar_recipes(recipe_id: int, limit: int = Query(5, ge=1, le=20)):
    results = await recipe_recommendations.fetch_similar_recipes(recipe_id, limit)
    if results is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"items": results, "limit": limit}
