from typing import List, Literal, Optional

from pydantic import BaseModel, Field

Difficulty = Literal["easy", "medium", "hard"]


class StepBlock(BaseModel):
    type: Literal["text", "image"]
    value: str
    metadata: Optional[dict] = None


class RecipeStep(BaseModel):
    step_number: int = Field(..., ge=1)
    blocks: List[StepBlock]


class RecipeCreateRequest(BaseModel):
    title: str
    cover_url: Optional[str] = None
    difficulty: Difficulty
    cooking_time: Optional[int] = Field(None, ge=0)
    popularity: Optional[int] = Field(0, ge=0)
    steps: List[RecipeStep] = Field(default_factory=list)
