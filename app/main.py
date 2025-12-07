from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routes import search, health

app = FastAPI(title="Recipe Search API")

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

@app.get("/")
def root():
    return {"message": "Welcome to the Recipe Search API"}

import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
