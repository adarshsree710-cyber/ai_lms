"""
config/settings.py
Loads all environment variables with defaults and type validation.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Server
    PORT:        int  = 8000
    NODE_ENV:    str  = "development"

    # Database
    MONGODB_URI: str  = "mongodb://localhost:27017/elearning"

    # Auth
    JWT_SECRET:  str  = "change_this_secret_in_production"

    # Anthropic AI
    ANTHROPIC_API_KEY: str = ""
    AI_MODEL:          str = "claude-sonnet-4-20250514"
    AI_MAX_TOKENS:     int = 1000

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
