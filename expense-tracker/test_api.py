"""
Comprehensive API tests for Expense Tracker REST API.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, getDb
from api_main import app
from models import User, Expense
from auth import getPasswordHash

# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_expense_tracker.db"
testEngine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=testEngine)


@pytest.fixture(scope="function")
def testDb():
    """Create test database and tables for each test."""
    Base.metadata.create_all(bind=testEngine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=testEngine)


@pytest.fixture(scope="function")
def client(testDb):
    """Create test client with test database."""
    def overrideGetDb():
        try:
            yield testDb
        finally:
            testDb.close()

    app.dependency_overrides[getDb] = overrideGetDb
    with TestClient(app) as testClient:
        yield testClient
    app.dependency_overrides.clear()


@pytest.fixture
def testUser(testDb):
    """Create a test user in the database."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=getPasswordHash("TestPass123"),
        is_active=True
    )
    testDb.add(user)
    testDb.commit()
    testDb.refresh(user)
    return user


@pytest.fixture
def authHeaders(client, testUser):
    """Get authentication headers with valid JWT token."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "TestPass123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def testExpense(testDb, testUser):
    """Create a test expense in the database."""
    expense = Expense(
        amount=50.00,
        category="Food",
        description="Lunch",
        user_id=testUser.id
    )
    testDb.add(expense)
    testDb.commit()
    testDb.refresh(expense)
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


def test_register_duplicate_email(client, testUser):
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


def test_register_duplicate_username(client, testUser):
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


def test_login_success(client, testUser):
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


def test_login_wrong_password(client, testUser):
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


def test_get_current_user(client, authHeaders):
    """Test getting current user information."""
    response = client.get("/api/v1/auth/me", headers=authHeaders)
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

def test_create_expense_success(client, authHeaders):
    """Test successful expense creation."""
    response = client.post(
        "/api/v1/expenses",
        headers=authHeaders,
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


def test_create_expense_invalid_amount(client, authHeaders):
    """Test creating expense with invalid amount fails."""
    response = client.post(
        "/api/v1/expenses",
        headers=authHeaders,
        json={
            "amount": -10.00,  # Negative amount
            "category": "Transport",
            "description": "Taxi ride"
        }
    )
    assert response.status_code == 422  # Validation error


def test_list_expenses(client, authHeaders, testExpense):
    """Test listing expenses."""
    response = client.get("/api/v1/expenses", headers=authHeaders)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert data["total"] >= 1


def test_list_expenses_pagination(client, authHeaders, testDb, testUser):
    """Test expense list pagination."""
    # Create multiple expenses
    for i in range(25):
        expense = Expense(
            amount=10.00 + i,
            category="Test",
            description=f"Test expense {i}",
            user_id=testUser.id
        )
        testDb.add(expense)
    testDb.commit()

    # Test first page
    response = client.get(
        "/api/v1/expenses?page=1&page_size=10",
        headers=authHeaders
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["total"] == 25


def test_list_expenses_filter_by_category(client, authHeaders, testDb, testUser):
    """Test filtering expenses by category."""
    # Create expenses with different categories
    categories = ["Food", "Transport", "Entertainment"]
    for cat in categories:
        expense = Expense(
            amount=50.00,
            category=cat,
            description=f"{cat} expense",
            user_id=testUser.id
        )
        testDb.add(expense)
    testDb.commit()

    response = client.get(
        "/api/v1/expenses?category=Food",
        headers=authHeaders
    )
    assert response.status_code == 200
    data = response.json()
    assert all(item["category"] == "Food" for item in data["items"])


def test_list_expenses_filter_by_date(client, authHeaders, testExpense):
    """Test filtering expenses by date range."""
    response = client.get(
        "/api/v1/expenses?from_date=2026-01-01&to_date=2026-12-31",
        headers=authHeaders
    )
    assert response.status_code == 200


def test_get_expense_success(client, authHeaders, testExpense):
    """Test getting a specific expense."""
    response = client.get(
        f"/api/v1/expenses/{testExpense.id}",
        headers=authHeaders
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == testExpense.id
    assert data["amount"] == testExpense.amount


def test_get_expense_not_found(client, authHeaders):
    """Test getting non-existent expense returns 404."""
    response = client.get("/api/v1/expenses/9999", headers=authHeaders)
    assert response.status_code == 404


def test_update_expense_success(client, authHeaders, testExpense):
    """Test updating an expense."""
    response = client.put(
        f"/api/v1/expenses/{testExpense.id}",
        headers=authHeaders,
        json={"amount": 75.00, "description": "Updated lunch"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 75.00
    assert data["description"] == "Updated lunch"
    assert data["category"] == "Food"  # Unchanged


def test_update_expense_not_found(client, authHeaders):
    """Test updating non-existent expense returns 404."""
    response = client.put(
        "/api/v1/expenses/9999",
        headers=authHeaders,
        json={"amount": 75.00}
    )
    assert response.status_code == 404


def test_delete_expense_success(client, authHeaders, testExpense):
    """Test deleting an expense."""
    expenseId = testExpense.id  # Store ID before deletion
    response = client.delete(
        f"/api/v1/expenses/{expenseId}",
        headers=authHeaders
    )
    assert response.status_code == 204

    # Verify it's not accessible anymore
    response = client.get(
        f"/api/v1/expenses/{expenseId}",
        headers=authHeaders
    )
    assert response.status_code == 404


def test_delete_expense_not_found(client, authHeaders):
    """Test deleting non-existent expense returns 404."""
    response = client.delete("/api/v1/expenses/9999", headers=authHeaders)
    assert response.status_code == 404


# ============================================================================
# Summary Tests
# ============================================================================

def test_get_expense_summary(client, authHeaders, testDb, testUser):
    """Test getting expense summary."""
    # Create multiple expenses
    expensesData = [
        {"amount": 50.00, "category": "Food"},
        {"amount": 30.00, "category": "Food"},
        {"amount": 20.00, "category": "Transport"},
    ]

    for expData in expensesData:
        expense = Expense(
            amount=expData["amount"],
            category=expData["category"],
            description="Test",
            user_id=testUser.id
        )
        testDb.add(expense)
    testDb.commit()

    response = client.get("/api/v1/expenses/summary", headers=authHeaders)
    assert response.status_code == 200
    data = response.json()

    assert data["total_spending"] == 100.00
    assert data["total_expenses"] == 3
    assert len(data["categories"]) == 2

    # Check Food category
    foodCategory = next(c for c in data["categories"] if c["category"] == "Food")
    assert foodCategory["total"] == 80.00
    assert foodCategory["percentage"] == 80.0
    assert foodCategory["count"] == 2


def test_get_expense_summary_with_date_filter(client, authHeaders, testExpense):
    """Test getting expense summary with date filtering."""
    response = client.get(
        "/api/v1/expenses/summary?from_date=2026-01-01&to_date=2026-12-31",
        headers=authHeaders
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_spending" in data
    assert "categories" in data


# ============================================================================
# User Isolation Tests
# ============================================================================

def test_user_cannot_access_other_user_expenses(client, testDb):
    """Test that users cannot access expenses belonging to other users."""
    # Create two users
    user1 = User(
        email="user1@example.com",
        username="user1",
        hashed_password=getPasswordHash("Pass123"),
        is_active=True
    )
    user2 = User(
        email="user2@example.com",
        username="user2",
        hashed_password=getPasswordHash("Pass123"),
        is_active=True
    )
    testDb.add_all([user1, user2])
    testDb.commit()
    testDb.refresh(user1)
    testDb.refresh(user2)

    # Create expense for user1
    expense = Expense(
        amount=100.00,
        category="Test",
        description="User1's expense",
        user_id=user1.id
    )
    testDb.add(expense)
    testDb.commit()
    testDb.refresh(expense)

    # Login as user2
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "user2", "password": "Pass123"}
    )
    user2Token = response.json()["access_token"]
    user2Headers = {"Authorization": f"Bearer {user2Token}"}

    # Try to access user1's expense
    response = client.get(
        f"/api/v1/expenses/{expense.id}",
        headers=user2Headers
    )
    assert response.status_code == 404  # Should not find it


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
