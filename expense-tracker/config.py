"""
Configuration settings for the Expense Tracker API.
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator, model_validator
from typing import Optional
import secrets


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Expense Tracker API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./expense_tracker.db"

    # Security
    # Default secure key for development/testing - will be validated based on ENVIRONMENT
    SECRET_KEY: str = secrets.token_urlsafe(32)
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

    @model_validator(mode='after')
    def validate_production_secret_key(self) -> 'Settings':
        """Validate SECRET_KEY is secure for production environments."""
        # Only enforce strict validation in production
        if self.ENVIRONMENT == "production":
            if not self.SECRET_KEY or len(self.SECRET_KEY) < 32:
                raise ValueError(
                    'SECRET_KEY must be set and at least 32 characters for production. '
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
            if self.SECRET_KEY.lower() in weak_keys:
                raise ValueError('SECRET_KEY must not be a default/example value in production')

        return self

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
