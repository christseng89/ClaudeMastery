# Personal Finance Tracker CLI

A simple, practical command-line application for tracking personal financial transactions. Built as a hands-on learning project for the Claude Code Learning & Mastery Repository.

## Overview

This CLI application helps you manage your personal finances by tracking transactions with categories, amounts, and descriptions. All data is stored locally in JSON format, with automatic validation and persistence.

**Key Features:**
- Precise decimal arithmetic for financial calculations (no floating-point errors)
- Modern Click CLI framework with intuitive commands
- Automatic data persistence to JSON file
- Comprehensive input validation with clear error messages
- ISO-8601 timestamp generation
- Clean, formatted transaction display
- Full test coverage with pytest (26+ test cases)

## Quick Start

### Prerequisites

- Python 3.6 or higher (tested with Python 3.12.10)
- **click** package (install via pip)
- **pytest** package (for running tests, optional)

### Installation

1. Clone or download this directory
2. Install dependencies:
   ```bash
   pip install click

   # Optional: Install pytest for running tests
   pip install pytest
   ```
3. Make the script executable (optional):
   ```bash
   chmod +x finance_tracker.py
   ```
4. Run the application:
   ```bash
   python finance_tracker.py --help
   ```

## Usage

### Display Help

```bash
python finance_tracker.py --help
```

### Add Transaction (`add`)

Add a new financial transaction to your tracker.

**Required Options:**
- `--amount` (Decimal): The transaction amount (must be > 0, uses precise decimal arithmetic)
- `--category` (string): The transaction category (e.g., groceries, utilities, entertainment)

**Optional Options:**
- `--description` (string): Additional details about the transaction

**Examples:**

```bash
# Add transaction with description
python finance_tracker.py add --amount 25.50 --category groceries --description "Weekly grocery shopping"

# Add transaction without description
python finance_tracker.py add --amount 100.00 --category utilities

# Add entertainment expense
python finance_tracker.py add --amount 50.75 --category entertainment --description "Movie tickets"
```

**Output Example:**

```
==================================================
Transaction Added Successfully!
==================================================
Amount:      $25.50
Category:    groceries
Description: Weekly grocery shopping
Date:        2026-01-09T16:45:15.802209
==================================================
```

## Data Storage

### Transaction Format

Transactions are stored in `transactions.json` as a JSON array:

```json
[
  {
    "amount": "25.50",
    "category": "groceries",
    "description": "Weekly grocery shopping",
    "date": "2026-01-09T16:45:15.802209"
  },
  {
    "amount": "100.00",
    "category": "utilities",
    "description": "",
    "date": "2026-01-09T16:45:18.213945"
  }
]
```

**Fields:**
- `amount` (string): Transaction amount stored as string to preserve Decimal precision
- `category` (string): Transaction category
- `description` (string): Optional details (empty string if not provided)
- `date` (string): ISO-8601 formatted timestamp

### File Location

The `transactions.json` file is created automatically in the same directory as `finance_tracker.py` when you add your first transaction.

**Note:** This file is excluded from version control (`.gitignore`) to protect your personal financial data.

## Error Handling

### Validation Errors

The application validates all inputs and provides clear error messages:

**Invalid Amount (negative or zero):**
```bash
$ python finance_tracker.py add --amount -10 --category food
Validation Error: Amount must be greater than zero
```

**Empty Category:**
```bash
$ python finance_tracker.py add --amount 50 --category ""
Validation Error: Category cannot be empty
```

### Data File Recovery

If `transactions.json` becomes corrupted or is deleted:
- The application automatically recovers by starting with an empty transaction list
- Simply add a new transaction to recreate the file

## Architecture

### Project Structure

```
memory-hands-on/
├── finance_tracker.py       # Main application
├── test_finance_tracker.py  # Comprehensive test suite (pytest)
├── transactions.json        # Data storage (auto-created)
├── README.md               # This file
├── CLAUDE.md               # Claude Code guidance
├── .python-version         # Python version spec
├── .gitignore              # Git ignore rules
└── .claude/
    └── settings.local.json # Claude Code config
```

### Code Organization

**FinanceTracker Class:**
- Manages all financial transactions
- Handles data persistence
- Validates inputs
- Formats output displays

**ValidationError Exception:**
- Custom exception for input validation failures
- Provides clear, actionable error messages

**CLI Functions:**
- Uses Click framework with decorators (`@click.group()`, `@click.command()`)
- Command-line options with `@click.option()` for clean argument parsing
- Routes commands to appropriate handlers
- Handles exceptions and displays errors

## Technical Details

### Dependencies

**Runtime Dependencies:**
- **click** - Modern CLI framework with decorators and options
- **decimal** - Precise decimal arithmetic for financial calculations (standard library)
- **pathlib** - Modern file path operations (standard library)
- `json` - Data serialization and storage (standard library)
- `datetime` - Timestamp generation (standard library)
- `typing` - Type hints for better code clarity (standard library)

**Development Dependencies:**
- **pytest** - Test framework for comprehensive test coverage (26+ test cases)

**Installation:**
```bash
# Install runtime dependencies
pip install click

# Install development dependencies
pip install pytest
```

### Python Version

- **Minimum:** Python 3.6+
- **Recommended:** Python 3.12.10
- Tested with Python 3.12.10 on Windows 11

### Type Hints

The codebase uses comprehensive type hints for improved code clarity and IDE support:
```python
from decimal import Decimal

def add_transaction(
    self,
    amount: Decimal,
    category: str,
    description: str = ""
) -> Dict[str, Any]:
    ...
```

## Development

### Running Tests

The project includes a comprehensive pytest test suite with 26+ test cases covering all functionality.

**Test File:** `test_finance_tracker.py`

**Test Coverage:**
- Initialization and file loading
- Amount validation (positive, negative, zero, type checking)
- Category validation (empty, whitespace, valid strings)
- Transaction addition (with/without description, multiple transactions)
- Data persistence across instances
- Display functionality
- Edge cases (large amounts, unicode, long descriptions, corrupted JSON)

**Running Tests:**
```bash
# Run all tests with verbose output
pytest test_finance_tracker.py -v

# Run specific test class
pytest test_finance_tracker.py::TestAmountValidation -v

# Run specific test function
pytest test_finance_tracker.py::test_add_transaction_with_description -v

# Run with coverage report (requires pytest-cov)
pytest test_finance_tracker.py --cov=finance_tracker --cov-report=term-missing
```

**Test Organization:**
- **Fixtures:** `testFile`, `tracker`, `populatedTracker`
- **Test Classes:** Organized by functionality (Initialization, Validation, Persistence, etc.)
- **All tests pass:** Ensures code quality and reliability

### Code Style

- **Decimal for money:** Always use `Decimal` for financial calculations (never float)
- **Click for CLI:** Modern CLI framework with decorators and options
- **pathlib for files:** Modern file path operations instead of `os.path`
- **Comprehensive docstrings:** All classes and methods documented
- **Type hints throughout:** Full type annotations for better code clarity
- **Clear naming:** Descriptive variable and function names
- **Separation of concerns:** Validation, storage, and display logic separated
- **Black formatting:** 88-character line length standard

### Future Enhancements

Potential features for learning exercises:
- **list** command: Display all transactions
- **delete** command: Remove transactions
- **summary** command: Calculate category totals
- **filter** command: Search by date range or category
- **export** command: Export to CSV format
- **import** command: Import transactions from file

## Learning Context

This project is part of the **Claude Code Learning & Mastery Repository** and specifically demonstrates:

1. **Memory Management**
   - Using CLAUDE.md for persistent project context
   - Session-specific memory with `#` commands
   - Project-level documentation patterns

2. **Testing with Pytest**
   - Comprehensive test coverage (26+ test cases)
   - Test fixtures and organization
   - TDD (Test-Driven Development) workflow
   - Edge case and error handling testing

3. **CLI Development**
   - Modern Click framework with decorators
   - Command structure with `@click.group()` and `@click.command()`
   - User-friendly error messages
   - Clean option parsing with `@click.option()`

4. **Financial Programming**
   - Decimal precision for money calculations
   - Avoiding floating-point errors
   - Storing decimal values as strings in JSON

5. **Data Persistence**
   - JSON storage patterns
   - File I/O with pathlib
   - Error recovery from corrupted data
   - Data validation

6. **Python Best Practices**
   - Type hints with Decimal, str, Dict types
   - Custom exceptions (ValidationError)
   - Comprehensive docstrings
   - Code organization and separation of concerns
   - Modern Python patterns (pathlib, Click, Decimal)

## Troubleshooting

### Common Issues

**Issue:** "No module named 'click'" error
- **Solution:** Install Click with `pip install click`

**Issue:** "No such file or directory" error
- **Solution:** Make sure you're in the correct directory containing `finance_tracker.py`

**Issue:** "Python not found" error
- **Solution:** Ensure Python 3.6+ is installed and in your PATH

**Issue:** Transaction not saved
- **Solution:** Check file permissions in the directory

**Issue:** Corrupted transactions.json
- **Solution:** Delete the file and it will be recreated on next transaction

**Issue:** Tests not running
- **Solution:** Install pytest with `pip install pytest` and run `pytest test_finance_tracker.py -v`

### Getting Help

For issues specific to this project:
1. Check the CLAUDE.md file for detailed guidance
2. Review error messages carefully - they provide actionable solutions
3. Verify Python version: `python --version`

For Claude Code questions:
- Visit: https://claude.ai/code
- Documentation in parent repository's Resources/ directory

## Contributing

This is a learning project. Feel free to:
- Fork and experiment with new features
- Add commands for practice (list, delete, summary, etc.)
- Improve error handling
- Enhance data validation
- Add export/import capabilities
- Write additional test cases

**Development Workflow:**
1. Write tests first (TDD approach)
2. Implement the feature
3. Run all tests: `pytest test_finance_tracker.py -v`
4. Ensure all tests pass before committing
5. Update documentation (README.md and CLAUDE.md)

Follow the commit conventions from the parent repository:
- Start with action verb (Add, Fix, Update, Refactor)
- Be specific about changes
- Reference learning context when relevant
- Run tests before committing

## License

Part of the Claude Code Learning & Mastery Repository.

## Related Projects

- **expense-tracker/**: Full-featured expense tracker with CLI and REST API
- **Resources/**: Memory management and Claude Code guides
- **Parent CLAUDE.md**: Overall repository guidance and patterns
