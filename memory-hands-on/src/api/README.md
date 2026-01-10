# Personal Finance Tracker API

A FastAPI-based REST API for tracking personal financial transactions with categories, amounts, and descriptions.

## Overview

This API application helps you manage your personal finances by tracking transactions with precise decimal arithmetic. Built as a "Memory Lab" exercise demonstrating API-level memory configuration that overrides root conventions.

**Key Features:**
- RESTful API with FastAPI framework
- Precise Decimal arithmetic for financial calculations
- JSON-based persistent storage (api_transactions.json)
- Comprehensive input validation with Pydantic schemas
- Structured logging for production readiness
- Async route handlers for performance
- Auto-generated OpenAPI documentation

## Quick Start

### Installation

1. Install dependencies:
```bash
cd src/api
pip install -r requirements.txt
```

2. Run the application:
```bash
# From project root
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python -m uvicorn src.api.main:app --reload --port 8000
```

3. Access the API:
- API Base: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
# From project root
python src/api/test_api.py
```

## API Endpoints

### Health & Info

**GET /health**
- Check API health status
- Returns: `{"status": "healthy", "service": "...", "version": "..."}`

**GET /**
- Get API information and available endpoints
- Returns: API details with documentation links

### Transactions

**POST /api/v1/transactions/**
- Create a new transaction
- Request Body:
  ```json
  {
    "amount": 25.50,
    "category": "groceries",
    "description": "Weekly shopping"
  }
  ```
- Response (201 Created):
  ```json
  {
    "id": 1,
    "amount": "25.5",
    "category": "groceries",
    "description": "Weekly shopping",
    "date": "2026-01-10T18:42:00.178601"
  }
  ```

**GET /api/v1/transactions/**
- List all transactions
- Response (200 OK):
  ```json
  {
    "transactions": [...],
    "total_count": 10
  }
  ```

**GET /api/v1/transactions/{id}**
- Get a specific transaction by ID
- Response (200 OK): Transaction object
- Response (404 Not Found): If transaction doesn't exist

**DELETE /api/v1/transactions/{id}**
- Delete a transaction by ID
- Response (204 No Content): Successfully deleted
- Response (404 Not Found): If transaction doesn't exist

## Usage Examples

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Create transaction
curl -X POST http://localhost:8000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 25.50, "category": "groceries", "description": "Weekly shopping"}'

# List all transactions
curl http://localhost:8000/api/v1/transactions/

# Get specific transaction
curl http://localhost:8000/api/v1/transactions/1

# Delete transaction
curl -X DELETE http://localhost:8000/api/v1/transactions/1
```

### Using Python (httpx)

```python
import httpx

base_url = "http://localhost:8000"

# Create transaction
response = httpx.post(
    f"{base_url}/api/v1/transactions/",
    json={
        "amount": 25.50,
        "category": "groceries",
        "description": "Weekly shopping"
    }
)
print(response.json())

# List transactions
response = httpx.get(f"{base_url}/api/v1/transactions/")
print(response.json())
```

### Using FastAPI TestClient

```python
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

# Create transaction
response = client.post(
    "/api/v1/transactions/",
    json={"amount": 25.50, "category": "groceries", "description": "test"}
)
assert response.status_code == 201
print(response.json())
```

## Data Storage

### Storage File

Transactions are stored in `api_transactions.json` in the project root directory.

**Note:** This is separate from the CLI version's `transactions.json` file.

### Transaction Format

```json
[
  {
    "id": 1,
    "amount": "25.5",
    "category": "groceries",
    "description": "Weekly shopping",
    "date": "2026-01-10T18:42:00.178601"
  }
]
```

**Fields:**
- `id` (integer): Unique transaction identifier (auto-generated)
- `amount` (string): Transaction amount stored as string to preserve Decimal precision
- `category` (string): Transaction category (required, non-empty)
- `description` (string): Optional transaction details (empty string if not provided)
- `date` (string): ISO-8601 formatted timestamp (auto-generated)

## API-Specific Conventions

This API follows conventions defined in `src/CLAUDE.md` that **override** root conventions:

### 1. Async Everything
All route handlers are async for better performance:
```python
@router.post("/")
async def create_transaction(...) -> TransactionResponse:
    ...
```

### 2. Pydantic Response Models
Always return Pydantic models, never raw dictionaries:
```python
# Correct
return TransactionResponse(**transaction_data)

# Incorrect
return {"id": 1, "amount": 25.50}
```

### 3. FastAPI HTTPException
Use FastAPI's HTTPException for errors:
```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Transaction {transaction_id} not found"
)
```

### 4. Structured Logging
Use Python's logging module with structured logs:
```python
logger.info('Transaction created', extra={
    'transaction_id': transaction_id,
    'amount': str(amount)
})
```

### 5. Single Quotes for Dictionary Keys
API convention uses single quotes (overrides root's double quotes):
```python
response_data = {
    'transaction_id': transaction.id,
    'status': 'success'
}
```

## Architecture

### Project Structure

```
src/api/
├── __init__.py              # Package initialization
├── main.py                  # FastAPI application entry point
├── router.py                # Transaction API endpoints
├── schemas.py               # Pydantic request/response models
├── storage.py               # JSON storage service
├── requirements.txt         # API dependencies
├── test_api.py             # Comprehensive test suite
└── README.md               # This file
```

### Code Organization

**main.py**: FastAPI application
- App initialization
- CORS configuration
- Router inclusion
- Health check and root endpoints

**router.py**: Transaction endpoints
- All CRUD operations
- Async route handlers
- Dependency injection for storage
- Comprehensive error handling

**schemas.py**: Pydantic models
- TransactionCreate (request)
- TransactionResponse (response)
- TransactionListResponse
- ErrorResponse
- Field validation

**storage.py**: JSON storage service
- Load/save transactions
- Auto-increment ID generation
- Transaction CRUD operations
- Structured logging

## Validation Rules

### Amount
- Must be a positive Decimal (> 0)
- Stored as string to preserve precision
- Example: `25.50`, `100.00`, `123.456`

### Category
- Required field
- Cannot be empty or whitespace-only
- Trimmed of leading/trailing whitespace
- Examples: `"groceries"`, `"utilities"`, `"entertainment"`

### Description
- Optional field
- Defaults to empty string if not provided
- Trimmed of leading/trailing whitespace

### Date
- Auto-generated ISO-8601 timestamp
- Format: `"2026-01-10T18:42:00.178601"`
- Cannot be set manually

## Error Responses

### 400 Bad Request
Validation error or invalid input:
```json
{
  "detail": "Amount must be greater than zero"
}
```

### 404 Not Found
Transaction not found:
```json
{
  "detail": "Transaction 123 not found"
}
```

### 422 Unprocessable Entity
Pydantic validation error:
```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "amount"],
      "msg": "Input should be greater than 0",
      "input": -10.0
    }
  ]
}
```

### 500 Internal Server Error
Unexpected server error (logged automatically)

## Testing

### Test Suite

Run the comprehensive test suite:
```bash
python src/api/test_api.py
```

**Tests Include:**
- Health check and root endpoint
- Create transactions (with and without description)
- Validation errors (invalid amount, empty category)
- List all transactions
- Get specific transaction
- Get nonexistent transaction (404)
- Delete transaction
- Delete nonexistent transaction (404)

**Expected Output:**
```
============================================================
PERSONAL FINANCE TRACKER API - TEST SUITE
============================================================

[... test results ...]

============================================================
ALL TESTS PASSED! ✓
============================================================
```

### Manual Testing

Use the Swagger UI at http://localhost:8000/docs for interactive testing:
1. Expand an endpoint
2. Click "Try it out"
3. Enter request data
4. Click "Execute"
5. View response

## Development

### Dependencies

**Runtime:**
- fastapi>=0.109.0 - Web framework
- uvicorn[standard]>=0.27.0 - ASGI server
- pydantic - Data validation (included with FastAPI)

**Standard Library:**
- decimal - Precise decimal arithmetic
- json - Data serialization
- logging - Structured logging
- pathlib - Modern file operations
- datetime - Timestamp generation

### Code Style

- **Async everywhere**: All route handlers are async
- **Pydantic models**: All request/response use schemas
- **Type hints**: Full type annotations throughout
- **Structured logging**: Use logger with extra fields
- **Decimal for money**: Never use float for amounts
- **Single quotes**: Dictionary keys use single quotes (API convention)
- **Comprehensive docstrings**: All classes and methods documented

### Configuration

**CORS Settings:**
- Currently allows all origins (`allow_origins=['*']`)
- **Production**: Specify allowed origins explicitly

**Logging:**
- Level: INFO
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Output: stdout

**Storage:**
- Default file: `api_transactions.json`
- Location: Project root directory
- Format: JSON array

## Memory Lab Context

This API demonstrates **API-level memory configuration** that overrides root conventions:

### Root Conventions (Inherited)
- Descriptive variable names (minimum 3 characters)
- Type hints throughout
- Comprehensive docstrings

### API Overrides (From src/CLAUDE.md)
- ✓ Use single quotes for dictionary keys (not double)
- ✓ Use FastAPI HTTPException (not ValueError)
- ✓ Use structured logging (not print statements)
- ✓ Return Pydantic models (not raw dicts)
- ✓ All route handlers must be async

This pattern shows how subdirectory CLAUDE.md files can override parent conventions for specific contexts (API vs CLI vs other).

## Troubleshooting

### Issue: Port 8000 already in use
**Solution:** Kill existing uvicorn process or use a different port:
```bash
# Windows
netstat -ano | findstr :8000
taskkill //F //PID <PID>

# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn src.api.main:app --port 8001
```

### Issue: Import errors
**Solution:** Run from project root or set PYTHONPATH:
```bash
# Run from project root
cd D:\development\ClaudeCodeLearning\ClaudeMastery\memory-hands-on
uvicorn src.api.main:app --reload

# Or set PYTHONPATH
export PYTHONPATH=/path/to/memory-hands-on
uvicorn src.api.main:app --reload
```

### Issue: Tests fail
**Solution:** Ensure dependencies installed and run from correct directory:
```bash
pip install -r src/api/requirements.txt
python src/api/test_api.py
```

### Issue: api_transactions.json locked or corrupted
**Solution:** Delete the file and restart:
```bash
rm api_transactions.json
uvicorn src.api.main:app --reload
```

### Issue: Internal Server Error (500) on all endpoints
**Cause:** Pydantic v1 vs v2 syntax mismatch

**Symptoms:**
- All API endpoints return 500 Internal Server Error
- Health endpoint works but transaction endpoints fail
- No detailed error message in response

**Solution:** Ensure Pydantic v2 syntax is used in `schemas.py`:

```python
# ✓ CORRECT - Pydantic v2 syntax
from pydantic import BaseModel, field_serializer, ConfigDict

class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: Decimal
    date: datetime

    @field_serializer('amount')
    def serialize_amount(self, value: Decimal) -> str:
        return str(value)

# ✗ WRONG - Pydantic v1 syntax (deprecated)
class TransactionResponse(BaseModel):
    class Config:  # This causes 500 errors in Pydantic v2!
        from_attributes = True
        json_encoders = {Decimal: lambda v: str(v)}
```

**Check your version:**
```bash
python -c "import pydantic; print(pydantic.__version__)"
# Should be 2.x.x (e.g., 2.5.3)
```

## Related Documentation

- **src/CLAUDE.md** - API-specific conventions and memory configuration
- **Root CLAUDE.md** - Project-level guidance
- **Root README.md** - CLI version documentation
- **FastAPI Docs** - https://fastapi.tiangolo.com

## License

Part of the Claude Code Learning & Mastery Repository.

---

**API Version:** 1.0.0
**Last Updated:** 2026-01-10
**Framework:** FastAPI
**Python Version:** 3.6+
