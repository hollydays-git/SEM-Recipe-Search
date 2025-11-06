from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routes import search, test_qdrant

app = FastAPI(title="Recipe Search API")

# ✅ CORS middleware (must pass the class, not a type)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers
app.include_router(search.router)
app.include_router(test_qdrant.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Recipe Search API"}
