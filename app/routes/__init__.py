from fastapi import APIRouter
from app.routes import search, health

router = APIRouter()
router.include_router(search.router)
router.include_router(health.router)