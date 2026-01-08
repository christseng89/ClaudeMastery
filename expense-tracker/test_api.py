"""
Comprehensive API tests for Expense Tracker REST API.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from api_main import app
from models import User, Expense
from auth import get_password_hash

# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_expense_tracker.db"
test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def test_db():
    """Create test database and tables for each test."""
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create test client with test database."""
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(test_db):
    """Create a test user in the database."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("TestPass123"),
        is_active=True
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers with valid JWT token."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "TestPass123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_expense(test_db, test_user):
    """Create a test expense in the database."""
    expense = Expense(
        amount=50.00,
        category="Food",
        description="Lunch",
        user_id=test_user.id
    )
    test_db.add(expense)
    test_db.commit()
    test_db.refresh(expense)
    return expense


# ============================================================================
# Health Check Tests
# ============================================================================

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ============================================================================
# Authentication Tests
# ============================================================================

def test_register_user_success(client):
    """Test successful user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "SecurePass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data


def test_register_duplicate_email(client, test_user):
    """Test registration with duplicate email fails."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "different",
            "password": "SecurePass123"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["error"]["message"]


def test_register_duplicate_username(client, test_user):
    """Test registration with duplicate username fails."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "different@example.com",
            "username": "testuser",
            "password": "SecurePass123"
        }
    )
    assert response.status_code == 400
    assert "Username already taken" in response.json()["error"]["message"]


def test_register_weak_password(client):
    """Test registration with weak password fails."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "weak@example.com",
            "username": "weakuser",
            "password": "weak"  # Too short, no uppercase, no digit
        }
    )
    assert response.status_code == 422  # Validation error


def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "TestPass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Test login with wrong password fails."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "WrongPass123"}
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """Test login with non-existent user fails."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "nonexistent", "password": "TestPass123"}
    )
    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    """Test getting current user information."""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_get_current_user_unauthorized(client):
    """Test getting current user without token fails."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


# ============================================================================
# Expense CRUD Tests
# ============================================================================

def test_create_expense_success(client, auth_headers):
    """Test successful expense creation."""
    response = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "amount": 25.50,
            "category": "Transport",
            "description": "Taxi ride"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 25.50
    assert data["category"] == "Transport"
    assert data["description"] == "Taxi ride"
    assert "id" in data
    assert "date" in data


def test_create_expense_unauthorized(client):
    """Test creating expense without authentication fails."""
    response = client.post(
        "/api/v1/expenses",
        json={
            "amount": 25.50,
            "category": "Transport",
            "description": "Taxi ride"
        }
    )
    assert response.status_code == 401


def test_create_expense_invalid_amount(client, auth_headers):
    """Test creating expense with invalid amount fails."""
    response = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "amount": -10.00,  # Negative amount
            "category": "Transport",
            "description": "Taxi ride"
        }
    )
    assert response.status_code == 422  # Validation error


def test_list_expenses(client, auth_headers, test_expense):
    """Test listing expenses."""
    response = client.get("/api/v1/expenses", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert data["total"] >= 1


def test_list_expenses_pagination(client, auth_headers, test_db, test_user):
    """Test expense list pagination."""
    # Create multiple expenses
    for i in range(25):
        expense = Expense(
            amount=10.00 + i,
            category="Test",
            description=f"Test expense {i}",
            user_id=test_user.id
        )
        test_db.add(expense)
    test_db.commit()

    # Test first page
    response = client.get(
        "/api/v1/expenses?page=1&page_size=10",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["total"] == 25


def test_list_expenses_filter_by_category(client, auth_headers, test_db, test_user):
    """Test filtering expenses by category."""
    # Create expenses with different categories
    categories = ["Food", "Transport", "Entertainment"]
    for cat in categories:
        expense = Expense(
            amount=50.00,
            category=cat,
            description=f"{cat} expense",
            user_id=test_user.id
        )
        test_db.add(expense)
    test_db.commit()

    response = client.get(
        "/api/v1/expenses?category=Food",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert all(item["category"] == "Food" for item in data["items"])


def test_list_expenses_filter_by_date(client, auth_headers, test_expense):
    """Test filtering expenses by date range."""
    response = client.get(
        "/api/v1/expenses?from_date=2026-01-01&to_date=2026-12-31",
        headers=auth_headers
    )
    assert response.status_code == 200


def test_get_expense_success(client, auth_headers, test_expense):
    """Test getting a specific expense."""
    response = client.get(
        f"/api/v1/expenses/{test_expense.id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_expense.id
    assert data["amount"] == test_expense.amount


def test_get_expense_not_found(client, auth_headers):
    """Test getting non-existent expense returns 404."""
    response = client.get("/api/v1/expenses/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_expense_success(client, auth_headers, test_expense):
    """Test updating an expense."""
    response = client.put(
        f"/api/v1/expenses/{test_expense.id}",
        headers=auth_headers,
        json={"amount": 75.00, "description": "Updated lunch"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 75.00
    assert data["description"] == "Updated lunch"
    assert data["category"] == "Food"  # Unchanged


def test_update_expense_not_found(client, auth_headers):
    """Test updating non-existent expense returns 404."""
    response = client.put(
        "/api/v1/expenses/9999",
        headers=auth_headers,
        json={"amount": 75.00}
    )
    assert response.status_code == 404


def test_delete_expense_success(client, auth_headers, test_expense):
    """Test deleting an expense."""
    expense_id = test_expense.id  # Store ID before deletion
    response = client.delete(
        f"/api/v1/expenses/{expense_id}",
        headers=auth_headers
    )
    assert response.status_code == 204

    # Verify it's not accessible anymore
    response = client.get(
        f"/api/v1/expenses/{expense_id}",
        headers=auth_headers
    )
    assert response.status_code == 404


def test_delete_expense_not_found(client, auth_headers):
    """Test deleting non-existent expense returns 404."""
    response = client.delete("/api/v1/expenses/9999", headers=auth_headers)
    assert response.status_code == 404


# ============================================================================
# Summary Tests
# ============================================================================

def test_get_expense_summary(client, auth_headers, test_db, test_user):
    """Test getting expense summary."""
    # Create multiple expenses
    expenses_data = [
        {"amount": 50.00, "category": "Food"},
        {"amount": 30.00, "category": "Food"},
        {"amount": 20.00, "category": "Transport"},
    ]

    for exp_data in expenses_data:
        expense = Expense(
            amount=exp_data["amount"],
            category=exp_data["category"],
            description="Test",
            user_id=test_user.id
        )
        test_db.add(expense)
    test_db.commit()

    response = client.get("/api/v1/expenses/summary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert data["total_spending"] == 100.00
    assert data["total_expenses"] == 3
    assert len(data["categories"]) == 2

    # Check Food category
    food_category = next(c for c in data["categories"] if c["category"] == "Food")
    assert food_category["total"] == 80.00
    assert food_category["percentage"] == 80.0
    assert food_category["count"] == 2


def test_get_expense_summary_with_date_filter(client, auth_headers, test_expense):
    """Test getting expense summary with date filtering."""
    response = client.get(
        "/api/v1/expenses/summary?from_date=2026-01-01&to_date=2026-12-31",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_spending" in data
    assert "categories" in data


# ============================================================================
# User Isolation Tests
# ============================================================================

def test_user_cannot_access_other_user_expenses(client, test_db):
    """Test that users cannot access expenses belonging to other users."""
    # Create two users
    user1 = User(
        email="user1@example.com",
        username="user1",
        hashed_password=get_password_hash("Pass123"),
        is_active=True
    )
    user2 = User(
        email="user2@example.com",
        username="user2",
        hashed_password=get_password_hash("Pass123"),
        is_active=True
    )
    test_db.add_all([user1, user2])
    test_db.commit()
    test_db.refresh(user1)
    test_db.refresh(user2)

    # Create expense for user1
    expense = Expense(
        amount=100.00,
        category="Test",
        description="User1's expense",
        user_id=user1.id
    )
    test_db.add(expense)
    test_db.commit()
    test_db.refresh(expense)

    # Login as user2
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "user2", "password": "Pass123"}
    )
    user2_token = response.json()["access_token"]
    user2_headers = {"Authorization": f"Bearer {user2_token}"}

    # Try to access user1's expense
    response = client.get(
        f"/api/v1/expenses/{expense.id}",
        headers=user2_headers
    )
    assert response.status_code == 404  # Should not find it


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
