# Claude Code Memory - Hands On

## 🧠 當「使用者記憶（User Memory）」具有優先權時

使用者層級的記憶(MEMORY TYPES)在以下情況下會具有優先權：

### 1️⃣ CLAUDE.md 未涵蓋的內容

當專案記憶（CLAUDE.md）沒有定義相關規則時，系統會使用你的個人偏好來補足空白。

### 2️⃣ 你在對話中明確覆寫

如果你在對話中明確指示：

> 「忽略專案設定，使用我的偏好」

那麼使用者記憶會覆蓋專案設定。

### 3️⃣ 個人工作流程偏好

包含你偏好的：

* 資訊呈現方式
* 溝通風格
* 工作習慣

## ✅ 最佳實踐（Best Practice）

可以這樣理解記憶的優先順序：

### 👤 User Memory（使用者記憶）

➡ 你的個人預設與偏好設定

### 📄 CLAUDE.md（專案記憶）

➡ 不可妥協的專案標準，會覆蓋你的個人預設

### 💬 Conversation（即時對話）

➡ 即時上下文，優先權最高，可覆蓋所有設定

## 📊 優先順序總結

```mermaid
flowchart TD
    A[**最高**優先權<br/>**Conversation**<br/>對話即時指令]
    B[CLAUDE.md<br/>**專案規範**]
    C[**最低**優先權<br/>**User Memory**<br/>個人偏好]

    A --> B --> C
```

## 🎯 總結優先權順序

最高優先 ↑

1. Conversation（即時對話）
2. IDE Selection（選取內容）
3. Project CLAUDE.md（專案規範）
4. User Memory（個人偏好）
5. System Defaults（系統預設）

最低優先 ↓

## Hands-On 練習

RESOURCES: <https://github.com/firstlink/claude-code/blob/main/claude-code-memory/README.md>

```bash
mkdir -p memory-hands-on && cd memory-hands-on

cat << 'EOF' > README.md
# Personal Finance Tracker CLI

A command-line application for tracking personal finances built.

## Overview

This CLI application helps you manage your personal finances by tracking transactions with categories, amounts, and descriptions.


#### 1. Add Transaction (`add`)

Add a new financial transaction to your tracker.

**Required Options:**
- `--amount` (float): The transaction amount
- `--category` (string): The transaction category (e.g., groceries, utilities, entertainment)

**Optional Options:**
- `--description` (string): Additional details about the transaction

**Functionality:**
- Creates a transaction dictionary containing:
  - amount
  - category
  - description
  - date
- Displays the added transaction to the user

**Usage Example:**
```bash
EOF

```

```bash
claude

/init

Refer to the README.md to implement the Personal Finance Tracker CLI application.
```

```cmd
cd memory-hands-on
pyenv global 3.12.10
pyenv local 3.12.10
python finance_tracker.py add --amount 100.12 --category foods --description "Grocery shopping"
```

## Project with User Memory

```bash
cat << 'EOF' > ~/.claude/CLAUDE.md
# My Personal Python Preferences

## Code Style

- Use Black formatter with 88 character line length
- Use isort for import sorting
- Type hints required for all functions
- Use pathlib instead of os.path

## CLI Development with Click

- Use click.group() for command organization
- Always include help text with """docstrings"""
- Use click.option() for optional flags
- Use click.argument() for required positional args

## Decimal for Money

Always use Decimal for financial calculations, never float:

```python
from decimal import import Decimal

# Correct
amount = Decimal('10.50')

# Wrong - floating point errors
amount = float(10.50)
```

## Testing

- Use pytest for all tests
- Test files: test_*.py
- Run with: pytest -v

## Common Commands

```bash
# Format code
black . && isort .

# Run tests
pytest -v

# Type check
mypy src/
```
EOF
```

```bash
claude
/clear

Use the user memory to update the python code in this directory and test it. 
/clear

I do NO see python test files. You missed testing coverage as part of user memory. Fix it.
/clear
/auto-commit

Update the project README.md in this directory.
/clear
/auto-commit


Generate requirements.txt for this project and update CLAUDE.md and README.md accordingly.
/clear
/auto-commit

```

```cmd
pytest test_finance_tracker.py -v
```

## Project Sub Directory Memory

```bash
cd memory-hands-on
mkdir -p src/api

cat << 'EOF' > src/api/README.md
# Personal Finance Tracker

A API based application for tracking personal finances built.

## Overview

This API application helps you manage your personal finances by tracking transactions with categories, amounts, and descriptions.

### 1. Add Transaction (`add`)

Add a new financial transaction to your tracker.

**Required Options:**
- `--amount` (float): The transaction amount
- `--category` (string): The transaction category (e.g., groceries, utilities, entertainment)

**Optional Options:**

- `--description` (string): Additional details about the transaction

**Functionality:**

- Creates a transaction dictionary containing:
  - amount
  - category
  - description
  - date
- Displays the added transaction to the user

**Usage Example:**

```bash
EOF
```

```bash
cat << 'EOF' > src/CLAUDE.md
# FastAPI Web API

**INHERITS FROM:** Root CLAUDE.md  
**OVERRIDES:** Specific conventions listed below

---

## 🧠 MEMORY LAB: API-Level Memory Configuration

This API-level CLAUDE.md demonstrates how subdirectory memory **overrides** root conventions for API-specific needs.

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

````

## Response Models

Always use Pydantic schemas for responses:

```python
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    category: str
    transaction_type: str
    date: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v),
            datetime: lambda v: v.isoformat()
        }

````

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
````

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
````

---

## 🧠 MEMORY LAB: API Overrides Root Conventions

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

````

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

````

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

````

### Inherited 4: Variable Naming (FROM ROOT)

**INHERITED:** Still use descriptive names, minimum 3 characters.

```python
# Correct (inherits from root)
transaction_data = await get_transaction(transaction_id)
user_request = TransactionCreate(**request_body)

# Still incorrect (root rule applies)
txn = await get_transaction(id)  # Too short
````

### Override 5: Return Types (API-SPECIFIC)

**API RULE:** Always return Pydantic models, never raw dicts.

```python
# Correct (API-specific rule)
@router.get("/{transaction_id}")
async def get_transaction(transaction_id: int) -> TransactionResponse:
    return TransactionResponse(**transaction_data)
````

```python
# Incorrect — don't return raw dicts in API
async def get_transaction(transaction_id: int) -> dict:
    return {"id": 1, "amount": 50.00}  # Should be Pydantic model
````

**Summary:** API memory overrides root for HTTP-specific concerns (exceptions, logging, response format) but inherits general coding standards (variable naming, type safety).
EOF

```

### Run Claude to use Project Sub Directory Memory

```bash
claude
  use /src/api memory to create the project using README.md file.
  give me a README.md in src folder for the installation, test, and execution instructions.

/clear  
```

```cmd
cd memory-hands-on
pip install -r src/api/requirements.txt

python src/api/test_api.py
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

```

### Test the API Endpoints

```bash
start http://localhost:8000
start http://localhost:8000/docs
start http://localhost:8000/health

curl -X POST http://localhost:8000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 25.50, "category": "groceries", "description": "Weekly shopping"}'

curl http://localhost:8000/api/v1/transactions/
curl http://localhost:8000/api/v1/transactions/1
curl -X DELETE http://localhost:8000/api/v1/transactions/1

```
