from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    ONNX_MODEL_PATH: str
    ONNX_TOKENIZER_PATH: str
    ONNX_TOKENIZER: str
    EMBEDDING_PREFIX: str
    TOKENIZER_MAX_LENGTH: int
    NORMALIZE_EMBEDDINGS: bool
    ORT_INTRA_OP_THREADS: int
    ORT_INTER_OP_THREADS: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="allow",
    )

    @field_validator("ONNX_MODEL_PATH", "ONNX_TOKENIZER_PATH", mode="before")
    @classmethod
    def resolve_path(cls, value: str) -> str:
        path = Path(value)
        if not path.is_absolute():
            path = (BASE_DIR / path).resolve()
        return str(path)


settings = Settings()
