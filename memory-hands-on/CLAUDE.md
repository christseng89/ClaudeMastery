# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Personal Finance Tracker CLI** - a hands-on practice project demonstrating Claude Code's memory and context management capabilities. It's a simple yet functional command-line application for tracking personal financial transactions with categories, amounts, and descriptions.

**Purpose**: This project serves as a practical example in the Claude Code Learning & Mastery Repository's memory management module (README-6). It demonstrates:
- Session-specific memory usage (temporary context with `#`)
- Project-level context preservation (this CLAUDE.md file)
- Working with persistent data structures
- CLI application development patterns

## Running the Application

### Basic Usage

```bash
# Display help
python finance_tracker.py --help

# Add a transaction with description
python finance_tracker.py add --amount 25.50 --category groceries --description "Weekly grocery shopping"

# Add a transaction without description
python finance_tracker.py add --amount 100 --category utilities
```

### Commands

**add**: Add a new financial transaction
- `--amount` (required, float): Transaction amount (must be > 0)
- `--category` (required, string): Transaction category (cannot be empty)
- `--description` (optional, string): Additional transaction details

## Architecture

### File Structure

```
memory-hands-on/
├── .claude/
│   └── settings.local.json       # Claude Code permissions and MCP config
├── .gitignore                     # Git ignore rules (excludes transactions.json)
├── .python-version                # Python version specification (3.12.10)
├── CLAUDE.md                      # This file - project guidance for Claude Code
├── README.md                      # User-facing project documentation
├── finance_tracker.py             # Main application (executable)
├── test_finance_tracker.py        # Comprehensive test suite (pytest)
└── transactions.json              # Persistent storage (auto-created, gitignored)
```

### Code Organization

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
# Install runtime dependencies
pip install click

# Install development dependencies
pip install pytest
```

### Testing

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

## Claude Code Configuration

### Permissions (.claude/settings.local.json)

This project configures specific permissions for Claude Code:

```json
{
  "permissions": {
    "allow": [
      "Bash(cat:*)",
      "Bash(python finance_tracker.py:*)"
    ]
  },
  "disabledMcpjsonServers": [
    "weather"
  ]
}
```

**Permissions Explained:**
- `Bash(cat:*)`: Allows reading file contents for inspection
- `Bash(python finance_tracker.py:*)`: Allows running the finance tracker with any arguments
- `disabledMcpjsonServers`: Weather MCP server is disabled (not needed for this project)

### Python Environment

**Python Version**: 3.12.10 (specified in `.python-version`)

**Setting Up:**
```bash
# Install dependencies
pip install click pytest

# Run the application
python finance_tracker.py --help

# Run tests
pytest test_finance_tracker.py -v
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
