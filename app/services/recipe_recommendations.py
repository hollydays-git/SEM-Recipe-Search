from typing import Any, Dict, List, Optional

from qdrant_client.http import models as qmodels

from app.core.config import settings
from app.core.embedding_client import embedding_client
from app.core.logging import get_logger
from app.core.pg_service import pg_service
from app.core.qdrant_service import qdrant

logger = get_logger(__name__)


def _build_embedding_text(recipe: Dict[str, Any]) -> str:
    parts = [recipe.get("title", "")]
    cover = recipe.get("cover_url")
    if cover:
        parts.append(f"image: {cover}")
    difficulty = recipe.get("difficulty")
    if difficulty:
        parts.append(f"difficulty: {difficulty}")
    cooking_time = recipe.get("cooking_time")
    if cooking_time is not None:
        parts.append(f"cooking_time: {cooking_time} minutes")
    steps = recipe.get("steps") or []
    for step in steps:
        block_texts = []
        for block in step.get("blocks", []):
            if block.get("type") == "text" and block.get("value"):
                block_texts.append(block["value"])
        if block_texts:
            parts.append(f"step {step.get('step_number')}: {' '.join(block_texts)}")
    return " | ".join(part for part in parts if part)


def _point_id_to_int(point_id: Any) -> Optional[int]:
    if point_id is None:
        return None
    if isinstance(point_id, int):
        return point_id
    try:
        return int(point_id)
    except (TypeError, ValueError):
        return None


async def fetch_similar_recipes(recipe_id: int, limit: int = 5) -> Optional[List[Dict[str, Any]]]:
    base_recipe = await pg_service.fetch_recipe_by_id(recipe_id)
    if not base_recipe:
        return None

    text = _build_embedding_text(base_recipe)
    if not text.strip():
        logger.warning("No text available to build embedding for recipe %s", recipe_id)
        return []

    vectors = await embedding_client.embed_queries([text])
    if not vectors:
        raise RuntimeError("Embedding service returned empty response")
    vector = vectors[0]

    filter_condition = qmodels.Filter(
        must_not=[qmodels.HasIdCondition(has_id=[recipe_id])]
    )

    search_response = qdrant.query_points(
        collection_name=settings.QDRANT_COLLECTION,
        query=vector,
        limit=limit,
        with_payload=False,
        query_filter=filter_condition,
    )

    points = getattr(search_response, "points", []) or []
    id_order: List[int] = []
    scores: Dict[int, float] = {}
    for point in points:
        pid = _point_id_to_int(point.id)
        if pid is None:
            continue
        id_order.append(pid)
        scores[pid] = point.score

    if not id_order:
        return []

    recipes = await pg_service.fetch_recipes_by_ids(id_order)
    recipes_map = {recipe["id"]: recipe for recipe in recipes}

    ordered_results: List[Dict[str, Any]] = []
    for pid in id_order:
        recipe = recipes_map.get(pid)
        if not recipe:
            continue
        recipe_with_score = recipe.copy()
        recipe_with_score["score"] = round(scores.get(pid, 0.0), 3)
        ordered_results.append(recipe_with_score)

    return ordered_results
