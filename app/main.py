from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.embedding_client import embedding_client
from app.core.logging import get_logger
from app.core.pg_service import pg_service
from app.routes import health, recipes, search

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application services")
    await pg_service.connect()
    await embedding_client.connect()
    try:
        yield
    finally:
        logger.info("Shutting down application services")
        await pg_service.close()
        await embedding_client.close()


app = FastAPI(title="Recipe Search API", lifespan=lifespan)

# CORS middleware (must pass the class, not a type)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(search.router)
app.include_router(health.router)
app.include_router(recipes.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Recipe Search API"}
