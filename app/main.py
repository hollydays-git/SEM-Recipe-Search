from fastapi import FastAPI
from app.routes import search

app = FastAPI(title="Semantic Recipe Search API")

app.include_router(search.router)

@app.get("/")
def read_root():
    return {"message": "API is running 🚀"}