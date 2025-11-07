from fastapi import APIRouter
from app.core.qdrant_service import qdrant

router = APIRouter(prefix="/health", tags=["system"])

@router.get("/qdrant")
def test_connection():
    try:
        collections = qdrant.get_collections()
        return {"status": "ok", "collections": collections}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
