from fastapi import FastAPI
from app.routes import search,init

app = FastAPI(title="Semantic Recipe Search API")

app.include_router(search.router)
app.include_router(init.router)

@app.get("/")
def read_root():
    return {"message": "API is running 🚀"}