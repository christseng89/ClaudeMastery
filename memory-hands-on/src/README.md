# Personal Finance Tracker - src/

This directory contains the **FastAPI REST API implementation** of the Personal Finance Tracker. This is a "Memory Lab" exercise demonstrating how API-level memory configuration (via `CLAUDE.md`) overrides root conventions.

## Overview

The `src/` directory contains a production-ready REST API built with FastAPI that provides:
- RESTful endpoints for managing financial transactions
- Precise Decimal arithmetic for financial calculations
- JSON-based persistent storage
- Comprehensive input validation
- Structured logging
- Auto-generated OpenAPI documentation

## Project Structure

```
src/
├── CLAUDE.md                    # API-level memory configuration (overrides root)
├── README.md                    # This file
├── __init__.py                  # Package initialization
└── api/
    ├── __init__.py              # API package initialization
    ├── main.py                  # FastAPI application entry point
    ├── router.py                # Transaction API endpoints (CRUD)
    ├── schemas.py               # Pydantic request/response models
    ├── storage.py               # JSON storage service
    ├── requirements.txt         # API dependencies
    ├── test_api.py             # Comprehensive test suite
    └── README.md               # Detailed API documentation
```

## Quick Start

### Prerequisites

- Python 3.6 or higher (recommended: 3.12.10)
- pip package manager

### Installation

**Step 1: Navigate to the project root**
```bash
cd D:/development/ClaudeCodeLearning/ClaudeMastery/memory-hands-on
```

**Step 2: Install API dependencies**
```bash
pip install -r src/api/requirements.txt
```

This installs:
- `fastapi>=0.109.0` - Modern web framework
- `uvicorn[standard]>=0.27.0` - ASGI server with all features

**Alternative: Install manually**
```bash
pip install fastapi uvicorn[standard]
```

### Running the API

**Option 1: Using uvicorn directly (Recommended)**
```bash
# From project root
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Option 2: Using Python module syntax**
```bash
# From project root
python -m uvicorn src.api.main:app --reload --port 8000
```

**Option 3: Development mode with auto-reload**
```bash
# From project root
uvicorn src.api.main:app --reload --log-level info
```

### Accessing the API

Once the server is running, access:

- **API Base URL**: http://localhost:8000
- **Interactive Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Testing the API

**Run the comprehensive test suite:**
```bash
# From project root
python src/api/test_api.py
```

**Expected output:**
```
============================================================
PERSONAL FINANCE TRACKER API - TEST SUITE
============================================================

TEST: Health Check
✓ Status: 200
✓ Response: {'status': 'healthy', ...}

[... more tests ...]

============================================================
ALL TESTS PASSED! ✓
============================================================
```

**The test suite covers:**
- ✓ Health check and root endpoint
- ✓ Create transactions (with and without description)
- ✓ Validation errors (invalid amount, empty category)
- ✓ List all transactions
- ✓ Get specific transaction
- ✓ Get nonexistent transaction (404)
- ✓ Delete transaction
- ✓ Delete nonexistent transaction (404)

## Basic Usage Examples

### Using cURL

**Create a transaction:**
```bash
curl -X POST http://localhost:8000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 25.50, "category": "groceries", "description": "Weekly shopping"}'
```

**List all transactions:**
```bash
curl http://localhost:8000/api/v1/transactions/
```

**Get specific transaction:**
```bash
curl http://localhost:8000/api/v1/transactions/1
```

**Delete transaction:**
```bash
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

# List all transactions
response = httpx.get(f"{base_url}/api/v1/transactions/")
print(response.json())
```

### Interactive Testing with Swagger UI

1. Start the server: `uvicorn src.api.main:app --reload`
2. Open browser: http://localhost:8000/docs
3. Click on an endpoint to expand it
4. Click **"Try it out"**
5. Enter request data in the form
6. Click **"Execute"**
7. View the response below

## API Endpoints

### System Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| GET | `/health` | Health check and version info | 200 |
| GET | `/` | API information and available endpoints | 200 |

### Transaction Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| POST | `/api/v1/transactions/` | Create new transaction | 201 |
| GET | `/api/v1/transactions/` | List all transactions | 200 |
| GET | `/api/v1/transactions/{id}` | Get specific transaction | 200, 404 |
| DELETE | `/api/v1/transactions/{id}` | Delete transaction | 204, 404 |

## Data Storage

Transactions are stored in **`api_transactions.json`** in the project root directory.

**Note:** This is separate from the CLI version's `transactions.json` file.

**Transaction format:**
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

## Development

### Running Tests During Development

```bash
# Run all tests
python src/api/test_api.py

# Check if server is running
curl http://localhost:8000/health
```

### Stopping the Server

- **Terminal**: Press `Ctrl+C`
- **Background process**: Find and kill the process:

```bash
# Windows
netstat -ano | findstr :8000
taskkill //F //PID <PID>

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Changing the Port

```bash
# Use a different port
uvicorn src.api.main:app --reload --port 8001

# Then access at http://localhost:8001
```

## Memory Lab Context

This API demonstrates **API-level memory configuration** that overrides root conventions:

### Root Conventions (Inherited)
- ✓ Descriptive variable names (minimum 3 characters)
- ✓ Type hints throughout
- ✓ Comprehensive docstrings

### API Overrides (From src/CLAUDE.md)
- ✓ **Single quotes** for dictionary keys (overrides root's double quotes)
- ✓ **FastAPI HTTPException** (overrides root's ValueError)
- ✓ **Structured logging** (overrides root's print statements)
- ✓ **Pydantic models** for responses (not raw dicts)
- ✓ **Async route handlers** (all endpoints are async)

**Why this matters:** This shows how subdirectory `CLAUDE.md` files can customize conventions for specific contexts (API vs CLI vs other modules) while inheriting common patterns from the root.

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Install dependencies
```bash
pip install -r src/api/requirements.txt
```

### Issue: "Port 8000 already in use"

**Solution:** Kill existing process or use different port
```bash
# Check what's using port 8000 (Windows)
netstat -ano | findstr :8000

# Kill the process
taskkill //F //PID <PID>

# Or use a different port
uvicorn src.api.main:app --port 8001
```

### Issue: "ImportError: cannot import name 'app'"

**Solution:** Run from project root directory
```bash
cd D:/development/ClaudeCodeLearning/ClaudeMastery/memory-hands-on
uvicorn src.api.main:app --reload
```

### Issue: Tests fail

**Solution:** Ensure you're in the correct directory and dependencies are installed
```bash
# Check current directory
pwd

# Install dependencies
pip install -r src/api/requirements.txt

# Run tests from project root
python src/api/test_api.py
```

### Issue: "api_transactions.json" is locked or corrupted

**Solution:** Delete the file and restart
```bash
rm api_transactions.json
uvicorn src.api.main:app --reload
```

## Common Commands Reference

### Installation
```bash
# Install all dependencies
pip install -r src/api/requirements.txt

# Verify installation
python -c "import fastapi; print(fastapi.__version__)"
```

### Running
```bash
# Development mode (auto-reload on code changes)
uvicorn src.api.main:app --reload

# Production mode (no reload)
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Custom host and port
uvicorn src.api.main:app --host 127.0.0.1 --port 8080
```

### Testing
```bash
# Run all tests
python src/api/test_api.py

# Health check
curl http://localhost:8000/health

# Create test transaction
curl -X POST http://localhost:8000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 100.00, "category": "test", "description": "Test transaction"}'
```

### Debugging
```bash
# Start with debug logging
uvicorn src.api.main:app --reload --log-level debug

# Check server status
curl http://localhost:8000/health

# View transaction data file
cat api_transactions.json
```

## API Features

### ✅ Implemented
- [x] Create transaction (POST)
- [x] List transactions (GET)
- [x] Get transaction by ID (GET)
- [x] Delete transaction (DELETE)
- [x] Input validation (Pydantic)
- [x] Error handling (HTTPException)
- [x] Structured logging
- [x] Auto-generated OpenAPI docs
- [x] Health check endpoint
- [x] Comprehensive test suite
- [x] Decimal precision for amounts

### 🔮 Potential Enhancements
- [ ] Update transaction (PUT)
- [ ] Filter transactions by category
- [ ] Date range filtering
- [ ] Transaction summaries/analytics
- [ ] User authentication (JWT)
- [ ] Database backend (SQLite/PostgreSQL)
- [ ] Rate limiting
- [ ] API versioning (v2)

## Documentation

### Detailed Documentation
- **API Details**: `src/api/README.md` - Comprehensive API documentation
- **API Conventions**: `src/CLAUDE.md` - API-specific memory configuration
- **Root Project**: `../README.md` - CLI version documentation
- **Root Conventions**: `../CLAUDE.md` - Project-level guidance

### External Resources
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Pydantic Documentation**: https://docs.pydantic.dev
- **Uvicorn Documentation**: https://www.uvicorn.org

## Architecture Summary

**Framework**: FastAPI (async web framework)
**Server**: Uvicorn (ASGI server)
**Validation**: Pydantic (data validation)
**Storage**: JSON file (api_transactions.json)
**Testing**: FastAPI TestClient + custom test suite

**Key Design Patterns:**
- Dependency Injection (storage service)
- Request/Response schemas (Pydantic models)
- RESTful API design
- Structured logging
- Comprehensive error handling

## Related Components

This API is part of the **Personal Finance Tracker** project which includes:

1. **CLI Application** (`../finance_tracker.py`) - Command-line interface
2. **REST API** (`src/api/`) - This FastAPI implementation
3. **Test Suites** - Both CLI and API have comprehensive tests
4. **Documentation** - Multiple README files at different levels

Both implementations demonstrate different aspects of Claude Code's memory system:
- CLI uses root-level conventions
- API uses API-specific overrides (this directory)

---

## Quick Start Summary

```bash
# 1. Install dependencies
pip install -r src/api/requirements.txt

# 2. Start the server
uvicorn src.api.main:app --reload

# 3. Access Swagger UI
# Open browser: http://localhost:8000/docs

# 4. Run tests
python src/api/test_api.py
```

**That's it!** Your Personal Finance Tracker API is ready to use. 🚀

---

**Version**: 1.0.0
**Last Updated**: 2026-01-10
**Framework**: FastAPI
**Python**: 3.6+
