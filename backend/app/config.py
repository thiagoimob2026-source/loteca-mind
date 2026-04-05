from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # Gemini
    GEMINI_API_KEY: str = ""

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # Football API (Phase 2)
    FOOTBALL_API_KEY: str = ""

    # App
    APP_NAME: str = "Loteca Mind"
    DEBUG: bool = True
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
