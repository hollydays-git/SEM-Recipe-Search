from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Semantic Recipe Search"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "recipes"

    class Config:
        env_file = ".env"

settings = Settings()