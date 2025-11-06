from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Semantic Recipe Search"
    QDRANT_URL: str
    QDRANT_COLLECTION: str
    QDRANT_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()