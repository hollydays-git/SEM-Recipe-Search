from typing import Any, Dict, List, Optional

import asyncpg

from app.core.config import settings

class PgService:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                dsn=settings.POSTGRES_DSN,
                min_size=settings.POSTGRES_POOL_MIN_SIZE,
                max_size=settings.POSTGRES_MAX_SIZE,
            )

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def fetch_recipes(self, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Карточки для списка (без тяжёлых данных)."""
        query = """
            SELECT id, title, cover_url, difficulty, cooking_time, popularity
            FROM recipes
            ORDER BY popularity DESC NULLS LAST, id
            LIMIT $1 OFFSET $2
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, limit, offset)
        return [dict(row) for row in rows]


    async def fetch_recipes_by_ids(self, ids: List[int]) -> List[Dict[str, Any]]:
        """
        Используется для Qdrant → Postgres — сохраняем порядок как пришёл.
        """
        if not ids:
            return []

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, title, cover_url, difficulty, cooking_time, popularity
                FROM recipes
                WHERE id = ANY($1)
                """,
                ids,
            )

        mapped = {row["id"]: dict(row) for row in rows}
        return [mapped[rid] for rid in ids if rid in mapped]

    async def search_recipes(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        pattern = f"%{query}%"
        sql = """
            SELECT id, title, cover_url, difficulty, cooking_time, popularity
            FROM recipes
            WHERE title ILIKE $1
            ORDER BY popularity DESC NULLS LAST, id
            LIMIT $2
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, pattern, limit)
        return [dict(row) for row in rows]

    async def fuzzy_match_recipes(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        sql = """
            SELECT
                id,
                title,
                cover_url,
                difficulty,
                cooking_time,
                popularity,
                similarity(lower(title), lower($1)) AS score
            FROM recipes
            WHERE title % $1 OR title ILIKE '%' || $1 || '%'
            ORDER BY score DESC NULLS LAST, popularity DESC NULLS LAST, id
            LIMIT $2
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, query, limit)
        return [dict(row) for row in rows]

    async def fetch_recipe_by_id(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """Основная карточка + шаги/блоки."""
        recipe = await self._fetch_recipe_meta(recipe_id)
        if not recipe:
            return None

        steps = await self._fetch_recipe_steps(recipe_id)
        recipe["steps"] = steps
        return recipe

    async def _fetch_recipe_meta(self, recipe_id: int):
        query = """
            SELECT id, title, cover_url, difficulty, cooking_time, popularity
            FROM recipes
            WHERE id = $1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, recipe_id)
        return dict(row) if row else None

    async def _fetch_recipe_steps(self, recipe_id: int) -> List[Dict[str, Any]]:
        """Шаги + блоки в нужном порядке."""
        query = """
            SELECT
                rs.id AS step_id,
                rs.step_number,
                rsb.id AS block_id,
                rsb.block_order,
                rsb.block_type,
                rsb.value,
                rsb.metadata
            FROM recipe_steps rs
            LEFT JOIN recipe_step_blocks rsb ON rsb.step_id = rs.id
            WHERE rs.recipe_id = $1
            ORDER BY rs.step_number, rsb.block_order
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, recipe_id)

        steps: Dict[int, Dict[str, Any]] = {}
        for row in rows:
            step = steps.setdefault(
                row["step_id"],
                {"step_number": row["step_number"], "blocks": []},
            )
            if row["block_id"] is not None:
                step["blocks"].append(
                    {
                        "id": row["block_id"],
                        "order": row["block_order"],
                        "type": row["block_type"],
                        "value": row["value"],
                        "metadata": row["metadata"],
                    }
                )

        ordered_ids = sorted(steps.keys(), key=lambda step_id: steps[step_id]["step_number"])
        return [steps[step_id] for step_id in ordered_ids]

    async def insert_recipe(self, *, title: str, cover_url: Optional[str], difficulty: str,
                            cooking_time: Optional[int], popularity: Optional[int]) -> Dict[str, Any]:
        query = """
            INSERT INTO recipes (title, cover_url, difficulty, cooking_time, popularity)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, title, cover_url, difficulty, cooking_time, popularity
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                title,
                cover_url,
                difficulty,
                cooking_time,
                popularity,
            )
        return dict(row)

    async def insert_recipe_steps(self, recipe_id: int, steps: List[Dict[str, Any]]) -> None:
        if not steps:
            return

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for step in steps:
                    row = await conn.fetchrow(
                        """
                        INSERT INTO recipe_steps (recipe_id, step_number)
                        VALUES ($1, $2)
                        RETURNING id
                        """,
                        recipe_id,
                        step["step_number"],
                    )
                    step_id = row["id"]
                    blocks = step.get("blocks") or []
                    for order, block in enumerate(blocks, start=1):
                        await conn.execute(
                            """
                            INSERT INTO recipe_step_blocks (step_id, block_order, block_type, value, metadata)
                            VALUES ($1, $2, $3, $4, $5)
                            """,
                            step_id,
                            order,
                            block["type"],
                            block["value"],
                            block.get("metadata"),
                        )


pg_service = PgService()
