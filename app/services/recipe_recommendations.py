from typing import Any, Dict, List, Optional

from qdrant_client.http import models as qmodels

from app.core.config import settings
from app.core.logging import get_logger
from app.core.pg_service import pg_service
from app.core.qdrant_service import qdrant

logger = get_logger(__name__)


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


    retrieved = qdrant.retrieve(
        collection_name=settings.QDRANT_COLLECTION,
        ids=[recipe_id],
        with_vectors=True,
        with_payload=False,
    )
    if not retrieved:
        logger.warning("Recipe %s is missing from Qdrant", recipe_id)
        return []

    vector = retrieved[0].vector
    if not vector:
        logger.warning("Recipe %s has no stored vector in Qdrant", recipe_id)
        return []
    if isinstance(vector, dict):
        try:
            vector = next(iter(vector.values()))
        except StopIteration:
            logger.warning("Recipe %s has empty vector payload", recipe_id)
            return []

    search_response = qdrant.query_points(
        collection_name=settings.QDRANT_COLLECTION,
        query=vector,
        limit=limit,
        with_payload=False,
        query_filter=qmodels.Filter(
            must_not=[qmodels.HasIdCondition(has_id=[recipe_id])]
        ),
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


async def fetch_similar_recipes_by_id(recipe_id: int, limit: int = 5) -> Optional[List[Dict[str, Any]]]:
    return await fetch_similar_recipes(recipe_id=recipe_id, limit=limit)
