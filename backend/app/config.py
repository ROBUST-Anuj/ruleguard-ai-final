from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    LLM_API_KEY: str = "sk-placeholder"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_BASE_URL: Optional[str] = "https://api.openai.com/v1"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    SEMANTIC_WEIGHT: float = 0.65
    LEXICAL_WEIGHT: float = 0.35
    TOP_K: int = 10
    DATA_DIR: str = "data"
    INDEX_DIR: str = "data/index"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
