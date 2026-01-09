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
│   └── settings.local.json    # Claude Code permissions and MCP config
├── .gitignore                  # Git ignore rules (excludes transactions.json)
├── .python-version             # Python version specification (3.12.10)
├── CLAUDE.md                   # This file - project guidance for Claude Code
├── README.md                   # User-facing project documentation
├── finance_tracker.py          # Main application (executable)
└── transactions.json           # Persistent storage (auto-created, gitignored)
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

**main()**: CLI entry point using argparse for command-line parsing

### Data Structure

Each transaction is stored as a dictionary:
```python
{
  "amount": float,
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

- Amount must be a positive number (> 0)
- Category cannot be empty or whitespace-only
- Category and description are trimmed of leading/trailing whitespace
- Timestamps are auto-generated using ISO-8601 format

## Development Notes

### Dependencies

- Python 3.6+ (uses type hints and f-strings)
- Standard library only (no external dependencies)
  - `argparse`: CLI parsing
  - `json`: Data persistence
  - `datetime`: Timestamp generation
  - `os`: File operations

### Testing Scenarios

The application has been tested with:
- Adding transactions with and without descriptions
- Invalid amounts (negative, zero)
- Empty categories (whitespace-only)
- Persistence across multiple runs
- JSON file creation and updates

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

**Why No Virtual Environment?**
- This project uses **zero external dependencies** (standard library only)
- No `requirements.txt` or `pyproject.toml` needed
- Simplifies setup for learning purposes
- Works with any Python 3.6+ installation

**Setting Up:**
```bash
# No setup needed - just run!
python finance_tracker.py --help
```

## Development Workflow

### Making Changes

When modifying this project:

1. **Read before editing**: Always read `finance_tracker.py` before making changes
2. **Test immediately**: Run commands after changes to verify behavior
3. **Check data file**: Inspect `transactions.json` to verify persistence
4. **Follow conventions**: Maintain existing code style (docstrings, type hints)

### Adding New Features

If extending the application (common learning exercises):

**New Commands** (e.g., `list`, `delete`, `summary`):
1. Add subparser in `main()` function
2. Add method to `FinanceTracker` class
3. Update CLAUDE.md with new command documentation
4. Test with various scenarios

**New Validations**:
1. Add validation method to `FinanceTracker` class (prefix with `_validate_`)
2. Raise `ValidationError` with clear message
3. Update docstrings
4. Test error cases

**Data Model Changes**:
1. Update transaction dictionary structure
2. Consider backward compatibility with existing `transactions.json`
3. Update documentation in CLAUDE.md and README.md

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
2. **CLI Development**: Argparse, command structures, user interaction
3. **Data Persistence**: JSON storage, file I/O, error recovery
4. **Validation Patterns**: Custom exceptions, type checking, data sanitization
5. **Code Organization**: Class structure, separation of concerns, documentation
6. **Git Best Practices**: Ignoring sensitive data, commit messages, file structure

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

# View data file
cat transactions.json
```

### Common Tasks for Claude Code

```bash
# Add a transaction
python finance_tracker.py add --amount 25.50 --category groceries --description "Weekly shopping"

# View stored transactions
cat transactions.json
```

### Inspection Commands

```bash
# Check Python version
python --version

# Count transactions
cat transactions.json | grep -c "amount"

# View recent transactions (last 5 objects)
cat transactions.json
```
