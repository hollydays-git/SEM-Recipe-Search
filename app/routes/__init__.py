from fastapi import APIRouter
from app.routes import health, recipes, search

router = APIRouter()
router.include_router(search.router)
router.include_router(health.router)
router.include_router(recipes.router)
