# FastAPI Web API

**INHERITS FROM:** Root CLAUDE.md
**OVERRIDES:** Specific conventions listed below

---

## MEMORY LAB: API-Level Memory Configuration

This API-level CLAUDE.md demonstrates how subdirectory memory **overrides** root conventions for API-specific needs.

## Architecture: Clean Separation of Concerns

The API follows a layered architecture with clear separation between models, schemas, storage, and routing:

```
Request Flow:
HTTP Request → Pydantic Schema (API validation)
            → Transaction Model (business validation)
            → Storage Layer (persistence)
            → Transaction Model (business object)
            → Pydantic Schema (API response)
            → HTTP Response

Layer Responsibilities:
- models.py    : Business logic and domain validation
- schemas.py   : API contracts (Pydantic request/response)
- storage.py   : Data persistence (JSON file operations)
- router.py    : HTTP endpoint handling (FastAPI routes)
- main.py      : Application setup (CORS, routers, config)
```

### Domain Models (models.py)

Business logic layer with Transaction domain model:

```python
from decimal import Decimal
from datetime import datetime
from typing import Dict, Any, Optional

class ValidationError(Exception):
    """Custom exception for transaction validation errors."""
    pass

class Transaction:
    """
    Transaction domain model with business logic.

    Responsibilities:
    - Validate business rules (amount > 0, category non-empty)
    - Handle type conversion (string → Decimal)
    - Provide serialization (toDict/fromDict)
    - Trim whitespace from inputs
    """

    def __init__(
        self,
        amount: Decimal,
        category: str,
        description: str = '',
        transaction_id: Optional[int] = None,
        date: Optional[datetime] = None
    ):
        self.id = transaction_id
        self.amount = self._validateAmount(amount)
        self.category = self._validateCategory(category)
        self.description = description.strip() if description else ''
        self.date = date if date else datetime.now()

    def toDict(self) -> Dict[str, Any]:
        """Serialize to dictionary for JSON storage."""
        return {
            'id': self.id,
            'amount': str(self.amount),  # Preserve precision
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat()
        }

    @classmethod
    def fromDict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Deserialize from dictionary."""
        return cls(
            amount=Decimal(data['amount']),
            category=data['category'],
            description=data.get('description', ''),
            transaction_id=data.get('id'),
            date=datetime.fromisoformat(data['date']) if 'date' in data else None
        )
```

**Key Principles:**
- Domain models contain business logic, NOT API concerns
- Validation happens at construction time (fail-fast)
- Use Decimal for financial amounts (user preference)
- Serialization methods preserve data integrity
- CamelCase for method names (toDict, fromDict)

## API-Specific Conventions

### Async Everything

All route handlers must be async:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/transactions")

@router.post("/", status_code=201)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_async_db)
) -> TransactionResponse:
    """Create new transaction. Use JSON structure and store it local to the project"""
    result = await json
    return result

```

### Storage Layer (storage.py)

The storage layer works with Transaction model objects, not dictionaries:

```python
from .models import Transaction, ValidationError

class TransactionStorage:
    """Handles JSON persistence for Transaction objects."""

    def add_transaction(
        self,
        amount: Decimal,
        category: str,
        description: str = ''
    ) -> Transaction:
        """
        Add transaction and return Transaction object.

        The Transaction constructor handles validation.
        Storage is responsible only for persistence and ID generation.
        """
        transactionId = self._next_id
        self._next_id += 1

        transaction = Transaction(
            amount=amount,
            category=category,
            description=description,
            transaction_id=transactionId,
            date=datetime.now()
        )

        self._transactions.append(transaction)
        self._save_transactions()
        return transaction

    def get_transaction(self, transaction_id: int) -> Optional[Transaction]:
        """Return Transaction object or None."""
        for transaction in self._transactions:
            if transaction.id == transaction_id:
                return transaction
        return None
```

**Key Principles:**
- Storage works with Transaction objects, not dicts
- Business validation happens in Transaction constructor
- Storage only handles persistence and ID generation
- Use toDict()/fromDict() for JSON serialization

### Router Layer (router.py)

Router converts between Transaction models and Pydantic schemas:

```python
from .models import Transaction, ValidationError
from .schemas import TransactionResponse

@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    storage: TransactionStorage = Depends(get_storage)
) -> TransactionResponse:
    """
    Convert: Pydantic schema → Transaction model → Pydantic schema
    """
    try:
        # Storage returns Transaction model
        transactionModel = storage.add_transaction(
            amount=transaction.amount,
            category=transaction.category,
            description=transaction.description
        )

        # Convert Transaction model to Pydantic response schema
        return TransactionResponse(
            id=transactionModel.id,
            amount=transactionModel.amount,
            category=transactionModel.category,
            description=transactionModel.description,
            date=transactionModel.date
        )
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
```

**Key Principles:**
- Router is the translation layer between HTTP and domain
- Pydantic schemas for API contracts (validation + serialization)
- Transaction models for business logic
- Never pass Pydantic models to storage

## Response Models (Pydantic Schemas)

Always use Pydantic v2 schemas for API contracts (NOT domain models):

```python
from pydantic import BaseModel, Field, field_serializer, ConfigDict
from decimal import Decimal
from datetime import datetime

class TransactionResponse(BaseModel):
    """Response schema with Pydantic v2 syntax."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal
    category: str
    transaction_type: str
    date: datetime

    @field_serializer('amount')
    def serialize_amount(self, value: Decimal) -> str:
        """Serialize Decimal to string to preserve precision."""
        return str(value)

    @field_serializer('date')
    def serialize_date(self, value: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return value.isoformat()
```

**IMPORTANT - Pydantic v2 Compatibility:**
- Use `model_config = ConfigDict(from_attributes=True)` instead of `class Config`
- Use `@field_serializer` decorators instead of `json_encoders`
- The old v1 syntax (`json_encoders`) will cause 500 Internal Server Error



## Error Handling

Use HTTP exceptions:

```python
from fastapi import HTTPException, status

# Not found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Transaction {transaction_id} not found"
)

# Validation error
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid transaction amount"
)
```

## API Documentation

FastAPI auto-generates docs at:

- Swagger UI: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc  

Always include:

- Operation summary  
- Parameter descriptions  
- Response model  
- Possible error codes  

## Development Server

```bash
uvicorn src.api.main:app --reload --port 8000
```

## Testing Strategy

The test suite includes both unit tests (models) and integration tests (API):

### Model Unit Tests (14 tests)

Test business logic independently of HTTP:

```python
from src.api.models import Transaction, ValidationError
from decimal import Decimal

def test_transaction_validation_negative_amount():
    """Test that negative amounts are rejected."""
    try:
        transaction = Transaction(
            amount=Decimal('-10.00'),
            category='test'
        )
        assert False, 'Expected ValidationError'
    except ValidationError as error:
        assert 'greater than zero' in str(error)
```

**Model Test Categories:**
- Creation tests (valid data, with ID, custom date)
- Validation tests (negative/zero amount, empty/whitespace category)
- Data conversion tests (string → Decimal)
- Serialization tests (toDict, fromDict, round-trip)
- Equality tests
- Edge cases (large amounts, unicode, whitespace trimming)

### API Integration Tests (11 tests)

Test HTTP endpoints with FastAPI TestClient:

```python
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_create_transaction():
    """Test creating a transaction via API."""
    response = client.post(
        '/api/v1/transactions/',
        json={'amount': 25.50, 'category': 'groceries', 'description': 'Weekly shopping'}
    )
    assert response.status_code == 201
    data = response.json()
    assert data['amount'] == '25.5'
```

**API Test Categories:**
- Health and root endpoints
- Create transactions (with/without description)
- Validation errors (Pydantic catches invalid input)
- List and get operations
- Delete operations
- 404 error handling

**Test Naming Conventions:**
- Test functions: `snake_case` (pytest convention)
- Internal variables: `camelCase` (user preference)
- Clear, descriptive names: `test_transaction_validation_negative_amount()`

**Run Tests:**
```bash
# From project root
python src/api/test_api.py

# Expected output: 25 tests passed (14 model + 11 API)
```

---

## MEMORY LAB: API Overrides Root Conventions

### Override 1: String Quotes (OVERRIDES ROOT)

**API RULE:** Use **single quotes** for dictionary keys and API responses.

```python
# Correct (API convention - OVERRIDES root's double quotes)
response_data = {
    'transaction_id': transaction.id,
    'amount': float(transaction.amount),
    'status': 'success'
}

# Root says double quotes, but API overrides for JSON consistency

```

### Override 2: Error Handling (OVERRIDES ROOT)

**API RULE:** Use FastAPI `HTTPException` instead of standard exceptions.

```python
from fastapi import HTTPException, status

# Correct (API convention - OVERRIDES root's ValueError)
if transaction_id not in storage:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transaction {transaction_id} not found"
    )

# Root uses ValueError, but API needs HTTP-aware exceptions

```

### Override 3: Logging (OVERRIDES ROOT)

**API RULE:** Use Python's `logging` module with structured logs.

```python
import logging

logger = logging.getLogger(__name__)

# Correct (API convention - OVERRIDES root's print statements)
logger.info("Transaction created", extra={
    "transaction_id": txn_id,
    "amount": amount,
    "user_id": user_id
})

# Root uses print(), but API needs structured logging for production

```

### Inherited 4: Variable Naming (FROM ROOT)

**INHERITED:** Still use descriptive names, minimum 3 characters.

```python
# Correct (inherits from root)
transaction_data = await get_transaction(transaction_id)
user_request = TransactionCreate(**request_body)

# Still incorrect (root rule applies)
txn = await get_transaction(id)  # Too short
```

### Override 5: Return Types (API-SPECIFIC)

**API RULE:** Always return Pydantic models, never raw dicts.

```python
# Correct (API-specific rule)
@router.get("/{transaction_id}")
async def get_transaction(transaction_id: int) -> TransactionResponse:
    return TransactionResponse(**transaction_data)
```

```python
# Incorrect — don't return raw dicts in API
async def get_transaction(transaction_id: int) -> dict:
    return {"id": 1, "amount": 50.00}  # Should be Pydantic model
```

**Summary:** API memory overrides root for HTTP-specific concerns (exceptions, logging, response format) but inherits general coding standards (variable naming, type safety).
