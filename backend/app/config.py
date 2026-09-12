from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    LLM_API_KEY: str = "sk-placeholder"
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    LLM_BASE_URL: Optional[str] = "https://api.groq.com/openai/v1"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    SEMANTIC_WEIGHT: float = 0.65
    LEXICAL_WEIGHT: float = 0.35
    TOP_K: int = 10
    DATA_DIR: str = "data"
    INDEX_DIR: str = "data/index"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Auto-detect Groq keys
        if self.LLM_API_KEY and self.LLM_API_KEY.startswith("gsk_"):
            self.LLM_BASE_URL = "https://api.groq.com/openai/v1"
            if not self.LLM_MODEL or self.LLM_MODEL.startswith("gpt-"):
                self.LLM_MODEL = "llama-3.3-70b-versatile"
        elif self.LLM_API_KEY and self.LLM_API_KEY.startswith("sk-") and not self.LLM_API_KEY.startswith("sk-placeholder"):
            # If OpenAI key provided and user hasn't explicitly set custom base URL
            if self.LLM_BASE_URL == "https://api.groq.com/openai/v1":
                self.LLM_BASE_URL = "https://api.openai.com/v1"
                self.LLM_MODEL = "gpt-4o-mini"

settings = Settings()
