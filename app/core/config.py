"""
Application configuration module
Handles all environment variables and settings
"""
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "User Management API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FastAPI User Management with JWT Authentication"

    # Database Settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/userdb"
    DATABASE_ECHO: bool = False

    # Security Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS Settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]

    # Redis Settings (Optional)
    REDIS_URL: Optional[str] = None
    CACHE_EXPIRE_SECONDS: int = 300

    # Pagination
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
