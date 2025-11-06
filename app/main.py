from fastapi import FastAPI
from app.core.config import settings
from app.routes import router as api_router

app = FastAPI(title=settings.APP_NAME)

# Include all routes
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "API is running"}
