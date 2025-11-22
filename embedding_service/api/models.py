from typing import List, Optional
from pydantic import BaseModel, Field

class EmbedRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, description="Texts to encode")
    prefix: Optional[str] = Field(None, description="Override default prefix (e.g. 'query:' or 'passage:')")
    normalize: Optional[bool] = Field(None, description="Override default normalization flag")

class EmbedResponse(BaseModel):
    model: str
    normalize: bool
    count: int
    embeddings: List[List[float]]
