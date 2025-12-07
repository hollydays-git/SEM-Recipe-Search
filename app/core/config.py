from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Semantic Recipe Search"
    QDRANT_URL: str
    QDRANT_COLLECTION: str
    QDRANT_API_KEY: str
    POSTGRES_DSN: str
    POSTGRES_POOL_MIN_SIZE: int
    POSTGRES_MAX_SIZE: int
    EMBEDDING_SERVICE_URL: str
    EMBEDDING_SERVICE_PREFIX: str = "passage:"
    EMBEDDING_SERVICE_NORMALIZE: bool = True

    model_config = SettingsConfigDict(env_file='.env', extra='allow')

settings = Settings()
