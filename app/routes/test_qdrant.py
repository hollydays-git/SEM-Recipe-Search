from fastapi import APIRouter
from app.core.qdrant_client import qdrant

router = APIRouter(prefix="/test-qdrant", tags=["test"])

@router.get("/")
def test_connection():
    try:
        collections = qdrant.get_collections()
        return {"status": "ok", "collections": collections}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
