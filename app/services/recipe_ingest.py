from typing import Dict

from qdrant_client.http import models as qmodels

from app.core.config import settings
from app.core.embedding_client import embedding_client
from app.core.logging import get_logger
from app.core.pg_service import pg_service
from app.core.qdrant_service import qdrant
from app.schemas.recipes import RecipeCreateRequest

logger = get_logger(__name__)


def build_embedding_text(payload: RecipeCreateRequest) -> str:
    parts = [payload.title]
    if payload.cover_url:
        parts.append(f"image: {payload.cover_url}")
    parts.append(f"difficulty: {payload.difficulty}")
    if payload.cooking_time is not None:
        parts.append(f"cooking_time: {payload.cooking_time} minutes")
    if payload.steps:
        for step in payload.steps:
            block_texts = [block.value for block in step.blocks if block.type == "text"]
            if block_texts:
                parts.append(f"step {step.step_number}: {' '.join(block_texts)}")
    return " | ".join(parts)


async def create_recipe(payload: RecipeCreateRequest) -> Dict:
    logger.info("Creating recipe '%s'", payload.title)
    recipe = await pg_service.insert_recipe(
        title=payload.title,
        cover_url=payload.cover_url,
        difficulty=payload.difficulty,
        cooking_time=payload.cooking_time,
        popularity=payload.popularity,
    )

    if payload.steps:
        await pg_service.insert_recipe_steps(
            recipe["id"],
            [step.model_dump() for step in payload.steps],
        )
        logger.debug("Stored %d steps for recipe %s", len(payload.steps), recipe["id"])

    embedding_text = build_embedding_text(payload)
    vectors = await embedding_client.embed([embedding_text])
    if not vectors:
        raise RuntimeError("Embedding service returned empty response")

    qdrant.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=[
            qmodels.PointStruct(
                id=recipe["id"],
                vector=vectors[0],
                payload={"title": recipe["title"]},
            )
        ],
    )
    logger.info("Recipe %s indexed in Qdrant", recipe["id"])

    return recipe
