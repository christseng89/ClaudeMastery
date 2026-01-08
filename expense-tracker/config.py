"""
Configuration settings for the Expense Tracker API.
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Expense Tracker API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./expense_tracker.db"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENVIRONMENT: str = "development"

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate SECRET_KEY is secure."""
        if not v or len(v) < 32:
            raise ValueError(
                'SECRET_KEY must be set and at least 32 characters. '
                'Generate one with: python -c "import secrets; print(secrets.token_urlsafe(32))"'
            )
        # Check for common weak values
        weak_keys = [
            'your-secret-key-change-this-in-production',
            'change-this',
            'secret',
            'password',
            'admin'
        ]
        if v.lower() in weak_keys:
            raise ValueError('SECRET_KEY must not be a default/example value')
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
