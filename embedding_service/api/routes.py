from fastapi import APIRouter, HTTPException

from embedding_service.core.config import settings
from embedding_service.core.encoder import service

from .models import EmbedRequest, EmbedResponse

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "POST /embed with {'texts': [...]} to receive embeddings."}


@router.get("/health")
async def health():
    return {
        "model_path": settings.ONNX_MODEL_PATH,
        "tokenizer_name": settings.ONNX_TOKENIZER,
        "tokenizer_path": settings.ONNX_TOKENIZER_PATH,
        "prefix": settings.EMBEDDING_PREFIX,
        "max_length": settings.TOKENIZER_MAX_LENGTH,
    }


@router.post("/embed", response_model=EmbedResponse)
async def embed(request: EmbedRequest):
    normalize = settings.NORMALIZE_EMBEDDINGS if request.normalize is None else request.normalize
    prefix = settings.EMBEDDING_PREFIX if request.prefix is None else request.prefix

    try:
        vectors = service.encode(request.texts, prefix=prefix, normalize=normalize)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Failed to generate embeddings: {exc}") from exc

    return EmbedResponse(
        model=settings.ONNX_TOKENIZER,
        normalize=normalize,
        count=len(vectors),
        embeddings=vectors,
    )
