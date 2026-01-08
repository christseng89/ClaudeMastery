"""
FastAPI main application for Expense Tracker REST API.
"""
from fastapi import FastAPI, Depends, HTTPException, status, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from typing import Optional, List
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import math

from config import settings
from database import get_db, init_db
from models import User, Expense
from schemas import (
    UserCreate, UserResponse, UserLogin, Token,
    ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseListResponse,
    ExpenseSummary, CategorySummary, ErrorResponse
)
from auth import (
    get_password_hash, authenticate_user, create_access_token,
    create_refresh_token, get_current_active_user
)

# ============================================================================
# Application Setup
# ============================================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="A RESTful API for tracking personal expenses with JWT authentication",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Rate Limiter Setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    """Initialize database tables on application startup."""
    init_db()


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.post(
    f"{settings.API_V1_PREFIX}/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"]
)
@limiter.limit("5/minute")
def register_user(
    request: Request,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    - **email**: Valid email address
    - **username**: Unique username (3-50 characters)
    - **password**: Strong password (min 8 chars, 1 digit, 1 uppercase)
    """
    # Check if email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if username already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post(
    f"{settings.API_V1_PREFIX}/auth/login",
    response_model=Token,
    tags=["Authentication"]
)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def login(
    request: Request,
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login and receive access and refresh tokens.

    - **username**: Your username
    - **password**: Your password
    """
    user = authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    refresh_token = create_refresh_token(data={"sub": user.username, "user_id": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@app.get(
    f"{settings.API_V1_PREFIX}/auth/me",
    response_model=UserResponse,
    tags=["Authentication"]
)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current authenticated user information."""
    return current_user


# ============================================================================
# Expense Endpoints
# ============================================================================

@app.post(
    f"{settings.API_V1_PREFIX}/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Expenses"]
)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def create_expense(
    request: Request,
    expense: ExpenseCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new expense.

    - **amount**: Expense amount (must be positive)
    - **category**: Category name (e.g., Food, Transport)
    - **description**: Expense description
    """
    db_expense = Expense(
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        user_id=current_user.id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


@app.get(
    f"{settings.API_V1_PREFIX}/expenses",
    response_model=ExpenseListResponse,
    tags=["Expenses"]
)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def list_expenses(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    category: Optional[str] = Query(None, description="Filter by category"),
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    min_amount: Optional[float] = Query(None, ge=0, description="Minimum amount"),
    max_amount: Optional[float] = Query(None, ge=0, description="Maximum amount"),
    sort_by: str = Query("date", enum=["date", "amount", "category"], description="Sort field"),
    sort_order: str = Query("desc", enum=["asc", "desc"], description="Sort order"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of expenses with filtering and sorting.

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **category**: Filter by category name
    - **from_date**: Filter expenses from this date
    - **to_date**: Filter expenses until this date
    - **min_amount**: Filter expenses with amount >= this value
    - **max_amount**: Filter expenses with amount <= this value
    - **sort_by**: Sort by field (date, amount, category)
    - **sort_order**: Sort order (asc, desc)
    """
    # Build query
    query = db.query(Expense).filter(
        Expense.user_id == current_user.id,
        Expense.is_deleted == False
    )

    # Apply filters
    if category:
        query = query.filter(Expense.category.ilike(f"%{category}%"))

    if from_date:
        try:
            from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
            query = query.filter(Expense.date >= from_datetime)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid from_date format. Use YYYY-MM-DD"
            )

    if to_date:
        try:
            to_datetime = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)
            query = query.filter(Expense.date < to_datetime)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid to_date format. Use YYYY-MM-DD"
            )

    if min_amount is not None:
        query = query.filter(Expense.amount >= min_amount)

    if max_amount is not None:
        query = query.filter(Expense.amount <= max_amount)

    # Apply sorting
    sort_column = getattr(Expense, sort_by)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    expenses = query.offset(offset).limit(page_size).all()

    # Calculate total pages
    pages = math.ceil(total / page_size) if total > 0 else 0

    return {
        "items": expenses,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages
    }


@app.get(
    f"{settings.API_V1_PREFIX}/expenses/summary",
    response_model=ExpenseSummary,
    tags=["Expenses"]
)
def get_expense_summary(
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get expense summary with category breakdown.

    - **from_date**: Optional start date for filtering
    - **to_date**: Optional end date for filtering
    """
    # Build query
    query = db.query(Expense).filter(
        Expense.user_id == current_user.id,
        Expense.is_deleted == False
    )

    # Apply date filters
    if from_date:
        try:
            from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
            query = query.filter(Expense.date >= from_datetime)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid from_date format. Use YYYY-MM-DD"
            )

    if to_date:
        try:
            to_datetime = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)
            query = query.filter(Expense.date < to_datetime)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid to_date format. Use YYYY-MM-DD"
            )

    expenses = query.all()

    if not expenses:
        return {
            "total_spending": 0,
            "total_expenses": 0,
            "categories": [],
            "date_range": {
                "from": from_date,
                "to": to_date
            }
        }

    # Calculate totals
    total_spending = sum(e.amount for e in expenses)
    total_expenses = len(expenses)

    # Calculate category breakdown
    category_totals = {}
    category_counts = {}

    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
        category_counts[expense.category] = category_counts.get(expense.category, 0) + 1

    categories = [
        CategorySummary(
            category=cat,
            total=total,
            percentage=(total / total_spending * 100) if total_spending > 0 else 0,
            count=category_counts[cat]
        )
        for cat, total in category_totals.items()
    ]

    # Sort by total amount descending
    categories.sort(key=lambda x: x.total, reverse=True)

    return {
        "total_spending": total_spending,
        "total_expenses": total_expenses,
        "categories": categories,
        "date_range": {
            "from": from_date,
            "to": to_date
        }
    }


@app.get(
    f"{settings.API_V1_PREFIX}/expenses/{{expense_id}}",
    response_model=ExpenseResponse,
    tags=["Expenses"]
)
def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific expense by ID."""
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id,
        Expense.is_deleted == False
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return expense


@app.put(
    f"{settings.API_V1_PREFIX}/expenses/{{expense_id}}",
    response_model=ExpenseResponse,
    tags=["Expenses"]
)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def update_expense(
    request: Request,
    expense_id: int,
    expense_update: ExpenseUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing expense.

    All fields are optional. Only provided fields will be updated.
    """
    db_expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id,
        Expense.is_deleted == False
    ).first()

    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    # Update only provided fields
    update_data = expense_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_expense, field, value)

    db.commit()
    db.refresh(db_expense)

    return db_expense


@app.delete(
    f"{settings.API_V1_PREFIX}/expenses/{{expense_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Expenses"]
)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def delete_expense(
    request: Request,
    expense_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete an expense (soft delete).

    The expense is marked as deleted but remains in the database for audit purposes.
    """
    db_expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id,
        Expense.is_deleted == False
    ).first()

    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    # Soft delete
    db_expense.is_deleted = True
    db.commit()

    return None


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler for consistent error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "path": str(request.url)
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler for unexpected errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "path": str(request.url)
            }
        }
    )


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
