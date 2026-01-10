"""
Pydantic schemas for request/response validation.

Follows API-specific conventions from src/CLAUDE.md:
- Use Decimal for financial precision
- JSON encoders for Decimal and datetime
- Response models inherit from BaseModel with from_attributes
"""

from pydantic import BaseModel, Field, field_validator, field_serializer, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional


class TransactionCreate(BaseModel):
    """Request schema for creating a transaction."""

    amount: Decimal = Field(..., description='Transaction amount (must be positive)', gt=0)
    category: str = Field(..., description='Transaction category', min_length=1)
    description: Optional[str] = Field('', description='Optional transaction details')

    @field_validator('category')
    @classmethod
    def validate_category(cls, value: str) -> str:
        """Ensure category is not empty or whitespace."""
        stripped = value.strip()
        if not stripped:
            raise ValueError('Category cannot be empty or whitespace')
        return stripped

    @field_validator('description')
    @classmethod
    def validate_description(cls, value: Optional[str]) -> str:
        """Strip whitespace from description."""
        if value is None:
            return ''
        return value.strip()


class TransactionResponse(BaseModel):
    """Response schema for transaction data."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='Transaction unique identifier')
    amount: Decimal = Field(..., description='Transaction amount')
    category: str = Field(..., description='Transaction category')
    description: str = Field(..., description='Transaction details')
    date: datetime = Field(..., description='Transaction timestamp (ISO-8601)')

    @field_serializer('amount')
    def serialize_amount(self, value: Decimal) -> str:
        """Serialize Decimal to string to preserve precision."""
        return str(value)

    @field_serializer('date')
    def serialize_date(self, value: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return value.isoformat()


class TransactionListResponse(BaseModel):
    """Response schema for list of transactions."""

    model_config = ConfigDict(from_attributes=True)

    transactions: list[TransactionResponse] = Field(..., description='List of transactions')
    total_count: int = Field(..., description='Total number of transactions')


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    detail: str = Field(..., description='Error message')
    error_code: Optional[str] = Field(None, description='Optional error code')
