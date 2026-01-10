# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Personal Finance Tracker** with dual implementations - a hands-on practice project demonstrating Claude Code's memory and context management capabilities:

1. **CLI Application** (`finance_tracker.py`) - Command-line interface using Click
2. **REST API** (`src/api/`) - FastAPI-based web service

**Purpose**: This project serves as a practical example in the Claude Code Learning & Mastery Repository's memory management module (README-6). It demonstrates:
- Session-specific memory usage (temporary context with `#`)
- Project-level context preservation (this CLAUDE.md file)
- **Subdirectory memory hierarchy** (src/CLAUDE.md overrides root conventions)
- Working with persistent data structures
- CLI and API application development patterns

## Running the Application

### CLI Application

**Basic Usage:**

```bash
# Display help
python finance_tracker.py --help

# Add a transaction with description
python finance_tracker.py add --amount 25.50 --category groceries --description "Weekly grocery shopping"

# Add a transaction without description
python finance_tracker.py add --amount 100 --category utilities
```

**Commands:**

**add**: Add a new financial transaction
- `--amount` (required, float): Transaction amount (must be > 0)
- `--category` (required, string): Transaction category (cannot be empty)
- `--description` (optional, string): Additional transaction details

### REST API Application

**Start the API server:**

```bash
# From project root
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Access the API:**
- API Base: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

**API Usage:**

```bash
# Create transaction
curl -X POST http://localhost:8000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 25.50, "category": "groceries", "description": "Weekly shopping"}'

# List all transactions
curl http://localhost:8000/api/v1/transactions/

# Get specific transaction
curl http://localhost:8000/api/v1/transactions/1
```

**API Documentation:** See `src/api/README.md` for comprehensive API documentation.

## Architecture

### File Structure

```
memory-hands-on/
├── .claude/
│   └── settings.local.json       # Claude Code permissions and MCP config
├── src/                           # API implementation (subdirectory with own CLAUDE.md)
│   ├── CLAUDE.md                  # API-level memory configuration (overrides root)
│   ├── README.md                  # Installation and API usage guide
│   └── api/                       # FastAPI application
│       ├── __init__.py            # Package initialization
│       ├── main.py                # FastAPI app entry point
│       ├── router.py              # Transaction API endpoints
│       ├── schemas.py             # Pydantic models (v2 syntax)
│       ├── storage.py             # JSON storage service
│       ├── requirements.txt       # API dependencies (fastapi, uvicorn)
│       ├── test_api.py            # API test suite
│       └── README.md              # Comprehensive API documentation
├── .gitignore                     # Git ignore rules (excludes *.json data files)
├── .python-version                # Python version specification (3.12.10)
├── CLAUDE.md                      # This file - project guidance for Claude Code
├── README.md                      # User-facing CLI documentation
├── requirements.txt               # CLI runtime dependencies (click)
├── requirements-dev.txt           # CLI development dependencies (pytest)
├── finance_tracker.py             # CLI application (executable)
├── test_finance_tracker.py        # CLI test suite (pytest)
├── transactions.json              # CLI persistent storage (auto-created, gitignored)
└── api_transactions.json          # API persistent storage (auto-created, gitignored)
```

### Code Organization

#### CLI Application (`finance_tracker.py`)

**FinanceTracker Class**:
- `__init__()`: Initialize tracker and load existing transactions
- `_load_transactions()`: Load transactions from JSON file
- `_save_transactions()`: Persist transactions to JSON file
- `_validate_amount()`: Validate transaction amount (must be positive)
- `_validate_category()`: Validate category (cannot be empty)
- `add_transaction()`: Add new transaction with validation
- `display_transaction()`: Format and display transaction to user

**ValidationError Exception**: Custom exception for input validation errors

**CLI Functions**: Click-based command-line interface with group and command decorators

#### REST API Application (`src/api/`)

**main.py**: FastAPI application setup
- App initialization with CORS middleware
- Router inclusion
- Health check and root endpoints
- Structured logging configuration

**router.py**: Transaction API endpoints
- POST `/api/v1/transactions/` - Create transaction
- GET `/api/v1/transactions/` - List all transactions
- GET `/api/v1/transactions/{id}` - Get specific transaction
- DELETE `/api/v1/transactions/{id}` - Delete transaction
- Async route handlers with dependency injection

**schemas.py**: Pydantic v2 models
- `TransactionCreate` - Request validation schema
- `TransactionResponse` - Response serialization with field_serializer
- `TransactionListResponse` - List response wrapper
- **IMPORTANT**: Uses Pydantic v2 syntax (ConfigDict, @field_serializer)

**storage.py**: JSON storage service
- `TransactionStorage` class for CRUD operations
- Auto-incrementing ID generation
- JSON file persistence with error recovery
- Structured logging for all operations

### Data Structure

Each transaction is stored as a dictionary:
```python
{
  "amount": string,  # Decimal stored as string to preserve precision
  "category": string,
  "description": string,
  "date": ISO-8601 timestamp
}
```

### Storage Mechanism

- Transactions are persisted to `transactions.json` as a JSON array
- File is created automatically on first transaction
- All transactions are loaded on startup and saved after each add operation

### Validation Rules

- Amount must be a Decimal type and positive (> 0)
- Category cannot be empty or whitespace-only
- Category and description are trimmed of leading/trailing whitespace
- Timestamps are auto-generated using ISO-8601 format
- Decimal precision is preserved when storing amounts

## Development Notes

### Dependencies

#### CLI Application Dependencies

**Runtime Dependencies:**
- Python 3.6+ (uses type hints and f-strings)
- **click**: CLI framework with decorators and options
- **decimal**: Precise decimal arithmetic for financial calculations
- **pathlib**: Modern file path operations
- Standard library: `json`, `datetime`, `typing`

**Development Dependencies:**
- **pytest**: Test framework (required for running tests)

**Installation:**
```bash
# Install CLI runtime dependencies
pip install -r requirements.txt

# Install CLI development dependencies (includes pytest)
pip install -r requirements-dev.txt

# Or install manually
pip install click    # Runtime
pip install pytest   # Development
```

**Dependency Files:**
- `requirements.txt`: Contains CLI runtime dependencies (click>=8.0.0)
- `requirements-dev.txt`: Contains CLI development dependencies and includes requirements.txt

#### REST API Dependencies

**Runtime Dependencies:**
- Python 3.6+ (recommended 3.12.10)
- **fastapi>=0.109.0**: Web framework with Pydantic v2 support
- **uvicorn[standard]>=0.27.0**: ASGI server for running FastAPI
- **pydantic 2.x**: Data validation (included with FastAPI)
- Standard library: `decimal`, `json`, `logging`, `pathlib`, `datetime`, `typing`

**CRITICAL - Pydantic v2 Compatibility:**
- This API requires Pydantic v2 (e.g., 2.5.3)
- Using Pydantic v1 syntax will cause 500 Internal Server Error
- The `schemas.py` file uses v2 syntax: `ConfigDict` and `@field_serializer`

**Installation:**
```bash
# Install API dependencies from project root
pip install -r src/api/requirements.txt

# Verify Pydantic version
python -c "import pydantic; print(pydantic.__version__)"  # Should be 2.x.x
```

**Dependency Files:**
- `src/api/requirements.txt`: Contains API dependencies (fastapi, uvicorn)

### Testing

#### CLI Application Tests

**Test Framework**: pytest with comprehensive test coverage

**Test File**: `test_finance_tracker.py` - 26+ test cases covering:
- Initialization and file loading
- Amount validation (positive, negative, zero, type checking)
- Category validation (empty, whitespace, valid strings)
- Transaction addition (with/without description, multiple transactions)
- Data persistence across instances
- Display functionality
- Edge cases (large amounts, unicode, long descriptions)
- Error recovery from corrupted JSON

**Test Structure:**
- **Fixtures**: `testFile`, `tracker`, `populatedTracker` (uses camelCase per user preference)
- **Test Classes**: Organized by functionality (Initialization, Validation, Persistence, etc.)
- **Test Functions**: Use snake_case (pytest convention): `test_add_transaction_with_description()`
- **Internal Variables**: Use camelCase: `testData`, `savedData`, `largeAmount`

**Running Tests:**
```bash
# Run all tests with verbose output
pytest test_finance_tracker.py -v

# Run specific test class
pytest test_finance_tracker.py::TestAmountValidation -v

# Run specific test function
pytest test_finance_tracker.py::test_add_transaction_with_description -v

# Run with coverage report (if pytest-cov installed)
pytest test_finance_tracker.py --cov=finance_tracker --cov-report=term-missing
```

**Test Coverage:**
- ✅ All public methods tested
- ✅ All validation rules tested
- ✅ Success and error paths tested
- ✅ Data persistence verified
- ✅ Edge cases covered

#### REST API Tests

**Test Framework**: Custom test runner with assertions

**Test File**: `src/api/test_api.py` - Comprehensive test cases covering:
- Health check endpoint
- Root endpoint information
- Create transactions (with and without description)
- Validation errors (invalid amount, empty category)
- List all transactions
- Get specific transaction by ID
- Get nonexistent transaction (404 error)
- Delete transaction
- Delete nonexistent transaction (404 error)

**Running Tests:**
```bash
# Run API tests from project root
python src/api/test_api.py

# Or run with pytest if pytest-asyncio is installed
pytest src/api/test_api.py -v
```

**Test Output:**
```
============================================================
PERSONAL FINANCE TRACKER API - TEST SUITE
============================================================

✓ Health check endpoint working
✓ Root endpoint provides API info
✓ Create transaction with description
✓ Create transaction without description
...
✓ All validation tests passed
✓ All CRUD operations tested

============================================================
ALL TESTS PASSED! ✓
============================================================
```

**Important Notes:**
- API tests require the server to NOT be running (tests start their own instance)
- Tests use FastAPI's TestClient for in-memory testing
- Temporary test database is cleaned up after each test

## Claude Code Configuration

### Permissions (.claude/settings.local.json)

This project configures specific permissions for Claude Code:

```json
{
  "permissions": {
    "allow": [
      "Bash(cat:*)",
      "Bash(python finance_tracker.py:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(pytest:*)",
      "Bash(pip install:*)",
      "Bash(curl:*)",
      "Bash(python -m json.tool:*)",
      "Bash(python -c:*)",
      "Bash(netstat:*)",
      "Bash(taskkill:*)",
      "Bash(python test_api_manual.py:*)",
      "Bash(python src/api/test_api.py:*)",
      "Bash(python -m uvicorn:*)"
    ]
  },
  "disabledMcpjsonServers": [
    "weather"
  ]
}
```

**Permissions Explained:**
- `Bash(cat:*)`: Read file contents for inspection
- `Bash(python finance_tracker.py:*)`: Run CLI finance tracker
- `Bash(git add:*)` and `Bash(git commit:*)`: Version control operations
- `Bash(pytest:*)`: Run test suites
- `Bash(pip install:*)`: Install Python dependencies
- `Bash(curl:*)`: Test API endpoints
- `Bash(python -m uvicorn:*)`: Start FastAPI server
- `Bash(netstat:*)` and `Bash(taskkill:*)`: Process management for API debugging
- `disabledMcpjsonServers`: Weather MCP server is disabled (not needed for this project)

### Python Environment

**Python Version**: 3.12.10 (specified in `.python-version`)

**Setting Up:**
```bash
# CLI Application
pip install -r requirements.txt          # CLI runtime dependencies
pip install -r requirements-dev.txt      # CLI + development dependencies
python finance_tracker.py --help         # Run CLI
pytest test_finance_tracker.py -v        # Test CLI

# REST API Application
pip install -r src/api/requirements.txt  # API dependencies (fastapi, uvicorn)
python -m uvicorn src.api.main:app --reload --port 8000  # Run API
python src/api/test_api.py               # Test API
```

## Development Workflow

### Making Changes

When modifying this project:

1. **Read before editing**: Always read `finance_tracker.py` before making changes
2. **Write tests first**: Add test cases for new functionality (TDD approach)
3. **Run tests**: Execute `pytest test_finance_tracker.py -v` after changes
4. **Test manually**: Run commands to verify behavior
5. **Check data file**: Inspect `transactions.json` to verify persistence
6. **Follow conventions**: Maintain existing code style (docstrings, type hints, naming conventions)

### Adding New Features

If extending the application (common learning exercises):

**New Commands** (e.g., `list`, `delete`, `summary`):
1. Write test cases for the new command in `test_finance_tracker.py`
2. Add Click command decorator in `finance_tracker.py`
3. Add method to `FinanceTracker` class
4. Run tests: `pytest test_finance_tracker.py -v`
5. Update CLAUDE.md with new command documentation
6. Test manually with various scenarios

**New Validations**:
1. Write test cases for validation logic (success and error paths)
2. Add validation method to `FinanceTracker` class (prefix with `_validate_`)
3. Raise `ValidationError` with clear message
4. Update docstrings
5. Run tests to verify error handling

**Data Model Changes**:
1. Write migration tests for backward compatibility
2. Update transaction dictionary structure
3. Consider backward compatibility with existing `transactions.json`
4. Run full test suite to verify no breakage
5. Update documentation in CLAUDE.md and README.md

## Error Handling

### Custom Exceptions

**ValidationError**: Used for all input validation failures
- Raised by `_validate_amount()` and `_validate_category()`
- Caught in `main()` and displayed to user
- Clear, actionable error messages

### Error Scenarios

| Error Type | Cause | Message | Fix |
|------------|-------|---------|-----|
| ValidationError | Amount ≤ 0 | "Amount must be greater than zero" | Use positive number |
| ValidationError | Empty category | "Category cannot be empty" | Provide category string |
| JSONDecodeError | Corrupted data file | Silent recovery (returns []) | Delete `transactions.json` |
| IOError | File access issues | Silent recovery (returns []) | Check file permissions |

## Example Outputs

### Successful Transaction

```bash
$ python finance_tracker.py add --amount 25.50 --category groceries --description "Weekly shopping"

==================================================
Transaction Added Successfully!
==================================================
Amount:      $25.50
Category:    groceries
Description: Weekly shopping
Date:        2026-01-09T16:45:15.802209
==================================================
```

### Validation Error

```bash
$ python finance_tracker.py add --amount -10 --category food

Validation Error: Amount must be greater than zero
```

### Data File Contents (transactions.json)

```json
[
  {
    "amount": 25.5,
    "category": "groceries",
    "description": "Weekly grocery shopping",
    "date": "2026-01-09T16:45:15.802209"
  },
  {
    "amount": 100.0,
    "category": "utilities",
    "description": "",
    "date": "2026-01-09T16:45:18.213945"
  }
]
```

## Memory Management Context

### Session-Specific Memory

Use the `#` command in Claude Code to add temporary context for the current session:

```bash
# use snake_case for all new functions
# prioritize data validation over performance
# always display transaction confirmation
```

This memory persists only for the current conversation and is ideal for:
- Temporary coding style preferences
- Short-term requirements or constraints
- Session-specific testing scenarios

### Project-Level Memory

This CLAUDE.md file serves as persistent, project-level context that:
- Loads automatically when working in this directory
- Provides consistent guidance across all sessions
- Documents architecture, conventions, and workflows
- Serves as the "source of truth" for the project

**When to update CLAUDE.md:**
- Adding new features or commands
- Changing data structures or validation rules
- Documenting new error scenarios
- Adding development workflows or conventions

## Git Configuration

### Ignored Files (.gitignore)

```gitignore
# Data files - contains user's personal financial data
transactions.json

# Python artifacts
__pycache__/
*.py[cod]
*$py.class

# Virtual environments (if created)
venv/
env/

# IDE files
.vscode/
.idea/
```

**Why ignore transactions.json?**
- Contains user's personal financial data (privacy)
- Each developer should have their own test data
- Prevents merge conflicts on data files
- Demonstrates proper gitignore practices

### Commit Conventions

Follow the parent repository's commit style:
- Start with action verb: Add, Fix, Update, Refactor
- Be specific about what changed
- Reference the learning context when relevant

**Examples:**
```
Add list command to finance tracker CLI
Fix validation error handling in transaction entry
Update CLAUDE.md with memory management examples
```

## Learning Objectives

This project helps developers practice:

1. **Memory Management**: Using `#` for temporary context vs CLAUDE.md for persistent guidance
2. **Testing with Pytest**: Comprehensive test coverage, fixtures, test organization, TDD workflow
3. **CLI Development**: Click framework, decorators, options, arguments
4. **Data Persistence**: JSON storage, file I/O, error recovery
5. **Validation Patterns**: Custom exceptions, type checking, data sanitization
6. **Decimal Precision**: Using Decimal for financial calculations (user preference)
7. **Code Organization**: Class structure, separation of concerns, documentation
8. **Naming Conventions**: Hybrid naming (camelCase fixtures, snake_case test functions)
9. **Git Best Practices**: Ignoring sensitive data, commit messages, file structure

## Related Documentation

- **Parent Repository**: `../CLAUDE.md` - Overall learning repository guidance
- **Memory Guides**: `../Resources/6.x` - Deep dive into Claude Code memory system
- **README.md**: User-facing documentation (getting started, usage examples)

## Quick Reference

### Common Commands

```bash
# Install dependencies
pip install -r requirements.txt          # Runtime only
pip install -r requirements-dev.txt      # Runtime + development

# Help
python finance_tracker.py --help

# Add with description
python finance_tracker.py add --amount 50.00 --category entertainment --description "Movie night"

# Add without description
python finance_tracker.py add --amount 100.00 --category utilities

# Run all tests
pytest test_finance_tracker.py -v

# Run specific test class
pytest test_finance_tracker.py::TestAmountValidation -v

# View data file
cat transactions.json
```

### Common Tasks for Claude Code

```bash
# Add a transaction
python finance_tracker.py add --amount 25.50 --category groceries --description "Weekly shopping"

# Run tests after making changes
pytest test_finance_tracker.py -v

# View stored transactions
cat transactions.json
```

### Inspection Commands

```bash
# Check Python version
python --version

# Run tests with verbose output
pytest test_finance_tracker.py -v

# Count transactions
cat transactions.json | grep -c "amount"

# View recent transactions
cat transactions.json
```
