from fastapi import APIRouter
from app.routes import search, test_qdrant

router = APIRouter()
router.include_router(search.router)
router.include_router(test_qdrant.router)