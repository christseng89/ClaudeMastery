"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime
from typing import Optional, List


# ============================================================================
# User Schemas
# ============================================================================

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(min_length=8, max_length=100)

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


# ============================================================================
# Token Schemas
# ============================================================================

class Token(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data payload."""
    username: Optional[str] = None
    user_id: Optional[int] = None


# ============================================================================
# Expense Schemas
# ============================================================================

class ExpenseBase(BaseModel):
    """Base expense schema."""
    amount: float = Field(gt=0, description="Amount must be greater than 0")
    category: str = Field(min_length=1, max_length=50, description="Category name")
    description: str = Field(max_length=200, description="Expense description")


class ExpenseCreate(ExpenseBase):
    """Schema for creating an expense."""
    pass


class ExpenseUpdate(BaseModel):
    """Schema for updating an expense (all fields optional)."""
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)


class ExpenseResponse(ExpenseBase):
    """Schema for expense response."""
    id: int
    date: datetime
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class ExpenseListResponse(BaseModel):
    """Schema for paginated expense list response."""
    items: List[ExpenseResponse]
    total: int
    page: int
    page_size: int
    pages: int


# ============================================================================
# Summary Schemas
# ============================================================================

class CategorySummary(BaseModel):
    """Schema for category spending summary."""
    category: str
    total: float
    percentage: float
    count: int


class ExpenseSummary(BaseModel):
    """Schema for overall expense summary."""
    total_spending: float
    total_expenses: int
    categories: List[CategorySummary]
    date_range: dict


# ============================================================================
# Error Schemas
# ============================================================================

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: dict

    class Config:
        json_schema_extra = {
            "example": {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Amount must be greater than 0",
                    "field": "amount"
                }
            }
        }
