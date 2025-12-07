"""
Application settings and configuration
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # Application
    PROJECT_NAME: str = "FastAPI User Management API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DB_ECHO: bool = False

    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]

    # First Superuser
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis"
    FIRST_SUPERUSER_FULLNAME: str = "Admin User"

    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @validator("ALLOWED_METHODS", pre=True)
    def parse_methods(cls, v):
        if isinstance(v, str) and v != "*":
            return [method.strip() for method in v.split(",")]
        return ["*"] if v == "*" else v

    @validator("ALLOWED_HEADERS", pre=True)
    def parse_headers(cls, v):
        if isinstance(v, str) and v != "*":
            return [header.strip() for header in v.split(",")]
        return ["*"] if v == "*" else v

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
