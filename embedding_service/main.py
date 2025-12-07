from fastapi import FastAPI

from embedding_service.api import router

app = FastAPI(title="Recipe Embedding API")
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8100)
