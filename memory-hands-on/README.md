# Personal Finance Tracker CLI

A simple, practical command-line application for tracking personal financial transactions. Built as a hands-on learning project for the Claude Code Learning & Mastery Repository.

## Overview

This CLI application helps you manage your personal finances by tracking transactions with categories, amounts, and descriptions. All data is stored locally in JSON format, with automatic validation and persistence.

**Key Features:**
- Zero external dependencies (Python standard library only)
- Automatic data persistence to JSON file
- Input validation with clear error messages
- ISO-8601 timestamp generation
- Clean, formatted transaction display

## Quick Start

### Prerequisites

- Python 3.6 or higher (tested with Python 3.12.10)
- No additional packages required

### Installation

1. Clone or download this directory
2. Make the script executable (optional):
   ```bash
   chmod +x finance_tracker.py
   ```
3. Run the application:
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
- `--amount` (float): The transaction amount (must be > 0)
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

**Fields:**
- `amount` (float): Transaction amount
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

**Main Function:**
- Parses command-line arguments using `argparse`
- Routes commands to appropriate handlers
- Handles exceptions and displays errors

## Technical Details

### Dependencies

This project uses only Python standard library modules:
- `argparse` - Command-line interface parsing
- `json` - Data serialization and storage
- `datetime` - Timestamp generation
- `os` - File system operations
- `typing` - Type hints for better code clarity

**No pip installation required!**

### Python Version

- **Minimum:** Python 3.6+
- **Recommended:** Python 3.12.10
- Tested with Python 3.12.10 on Windows 11

### Type Hints

The codebase uses comprehensive type hints for improved code clarity and IDE support:
```python
def add_transaction(
    self,
    amount: float,
    category: str,
    description: Optional[str] = None
) -> Dict:
    ...
```

## Development

### Running Tests

Currently, manual testing is performed. Future enhancements may include:
- Unit tests with `unittest` or `pytest`
- Integration tests for CLI commands
- Data persistence tests

### Code Style

- Comprehensive docstrings for all classes and methods
- Type hints throughout
- Clear variable and function names
- Separation of concerns (validation, storage, display)

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

2. **CLI Development**
   - Argument parsing with argparse
   - Command structure design
   - User-friendly error messages

3. **Data Persistence**
   - JSON storage patterns
   - File I/O error handling
   - Data validation

4. **Python Best Practices**
   - Type hints
   - Custom exceptions
   - Docstrings
   - Code organization

## Troubleshooting

### Common Issues

**Issue:** "No such file or directory" error
- **Solution:** Make sure you're in the correct directory containing `finance_tracker.py`

**Issue:** "Python not found" error
- **Solution:** Ensure Python 3.6+ is installed and in your PATH

**Issue:** Transaction not saved
- **Solution:** Check file permissions in the directory

**Issue:** Corrupted transactions.json
- **Solution:** Delete the file and it will be recreated on next transaction

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
- Add commands for practice
- Improve error handling
- Enhance data validation
- Add export/import capabilities

Follow the commit conventions from the parent repository:
- Start with action verb (Add, Fix, Update, Refactor)
- Be specific about changes
- Reference learning context when relevant

## License

Part of the Claude Code Learning & Mastery Repository.

## Related Projects

- **expense-tracker/**: Full-featured expense tracker with CLI and REST API
- **Resources/**: Memory management and Claude Code guides
- **Parent CLAUDE.md**: Overall repository guidance and patterns
