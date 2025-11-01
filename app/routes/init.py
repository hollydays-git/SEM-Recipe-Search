from fastapi import APIRouter

router = APIRouter(prefix="/init", tags=["init"])

@router.post("/")
def initialize_collection():
    return {"status": "Qdrant initialization placeholder"}
