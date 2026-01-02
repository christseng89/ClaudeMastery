# Expense Tracker

A simple, elegant command-line expense tracker application built with Python. Track your expenses with categories, descriptions, and automatic date/time stamps, with built-in analytics to understand your spending patterns.

## Features

- **Add New Expenses**: Record expenses with amount, category, and description
- **View All Expenses**: Display all recorded expenses in a formatted table
- **Calculate Total Spending**: See your total spending and breakdown by category with percentages
- **Persistent Storage**: All data is automatically saved to a JSON file
- **Category Analytics**: Automatic spending breakdown by category
- **Data Validation**: Input validation to ensure data integrity

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd expense-tracker
   ```

## Usage

### Interactive Mode

Run the expense tracker with the interactive menu:

```bash
python expense_tracker.py
```

#### Menu Options

1. **Add New Expense**
   - Enter the amount (must be greater than 0)
   - Enter a category (e.g., Food, Transport, Entertainment, Bills)
   - Enter a description of the expense
   - The expense will be automatically saved with a timestamp

2. **View All Expenses**
   - Displays all expenses in a formatted table
   - Shows ID, date, category, amount, and description

3. **Calculate Total Spending**
   - Shows your total spending across all expenses
   - Provides a breakdown by category with percentages

4. **Exit**
   - Safely exit the application

### Programmatic Usage

You can also use the ExpenseTracker programmatically in your own Python scripts:

```python
from expense_tracker import ExpenseTracker, ValidationError

# Create tracker instance
tracker = ExpenseTracker()

# Add expenses
try:
    expense1 = tracker.add_expense(25.50, "Food", "Lunch at restaurant")
    expense2 = tracker.add_expense(50.00, "Transport", "Gas for car")
    print(f"Added expense {expense1.id}")
except ValidationError as e:
    print(f"Validation error: {e}")

# Get all expenses
expenses = tracker.get_all_expenses()
print(f"Total expenses: {len(expenses)}")

# Calculate total
total = tracker.calculate_total()
print(f"Total spending: ${total:.2f}")

# Get category breakdown
summaries = tracker.get_category_breakdown()
for summary in summaries:
    print(f"{summary.name}: ${summary.total:.2f} ({summary.percentage:.1f}%)")
```

## Data Storage

Expenses are stored in `expenses.json` in the same directory as the script. The file is automatically created on the first expense entry and updated whenever new expenses are added.

### Data Format

Each expense contains:
- **id**: Unique identifier (integer)
- **amount**: Expense amount (float)
- **category**: Category name (string)
- **description**: Expense description (string)
- **date**: Timestamp when the expense was added (YYYY-MM-DD HH:MM:SS)

## Example

```
$ python expense_tracker.py

==================================================
          EXPENSE TRACKER
==================================================
1. Add New Expense
2. View All Expenses
3. Calculate Total Spending
4. Exit
==================================================

Enter your choice (1-4): 1
Enter amount: $25.50
Enter category (e.g., Food, Transport, Entertainment): Food
Enter description: Lunch at restaurant

Expense added successfully! (ID: 1)
Data saved to expenses.json
```

## Architecture

The application follows a **Model-View** architecture pattern that separates business logic from presentation:

- **Model Layer**: Core business logic (`Expense`, `ExpenseTracker`)
  - Data validation and storage
  - Expense calculations and analytics
  - No UI concerns - pure business logic

- **View Layer**: User interface (`ExpenseTrackerUI`)
  - Menu display and user input
  - Formatting and presentation
  - No business logic - delegates to model layer

- **Data Structures**: Type-safe data objects
  - `CategorySummary`: Category spending analysis
  - `ValidationError`: Custom exception for validation failures

This separation makes the code:
- **More testable**: Business logic can be tested without UI
- **More maintainable**: Changes to UI don't affect business logic
- **More reusable**: The tracker can be used programmatically or with different UIs

## API Reference

### Expense Class

Represents a single expense entry with validation.

#### Constructor

```python
Expense(expense_id: int, amount: float, category: str, description: str, date: Optional[str] = None)
```

**Parameters:**
- `expense_id` (int): Unique identifier for the expense
- `amount` (float): Expense amount (must be positive)
- `category` (str): Expense category (cannot be empty)
- `description` (str): Expense description
- `date` (Optional[str]): Timestamp in 'YYYY-MM-DD HH:MM:SS' format (auto-generated if not provided)

**Raises:**
- `ValidationError`: If amount is ≤ 0 or category is empty

**Example:**
```python
from expense_tracker import Expense, ValidationError

# Create a valid expense
expense = Expense(1, 25.50, "Food", "Lunch at restaurant")

# Validation errors
try:
    bad_expense = Expense(2, -10, "Food", "Invalid")
except ValidationError as e:
    print(e)  # "Amount must be greater than 0"
```

#### Methods

##### to_dict()

```python
def to_dict(self) -> Dict
```

Convert expense to dictionary for JSON serialization.

**Returns:**
- `Dict`: Dictionary with keys 'id', 'amount', 'category', 'description', 'date'

**Example:**
```python
expense = Expense(1, 25.50, "Food", "Lunch")
data = expense.to_dict()
# {'id': 1, 'amount': 25.50, 'category': 'Food', 'description': 'Lunch', 'date': '2026-01-02 14:30:00'}
```

##### from_dict()

```python
@classmethod
def from_dict(cls, data: Dict) -> Expense
```

Create an Expense object from a dictionary (deserialization).

**Parameters:**
- `data` (Dict): Dictionary containing expense data

**Returns:**
- `Expense`: New Expense instance

**Example:**
```python
data = {'id': 1, 'amount': 25.50, 'category': 'Food', 'description': 'Lunch', 'date': '2026-01-02 14:30:00'}
expense = Expense.from_dict(data)
```

---

### ExpenseTracker Class

Core business logic for expense tracking with persistent storage.

#### Constructor

```python
ExpenseTracker(data_file: str = 'expenses.json')
```

**Parameters:**
- `data_file` (str): Path to JSON file for storing expenses. Defaults to 'expenses.json'

**Example:**
```python
from expense_tracker import ExpenseTracker

tracker = ExpenseTracker()  # Uses 'expenses.json'
# or with custom file
tracker = ExpenseTracker(data_file='my_expenses.json')
```

#### Methods

##### add_expense()

```python
def add_expense(self, amount: float, category: str, description: str) -> Expense
```

Add a new expense to the tracker.

**Parameters:**
- `amount` (float): Expense amount (must be > 0)
- `category` (str): Expense category (cannot be empty)
- `description` (str): Expense description

**Returns:**
- `Expense`: The created Expense object

**Raises:**
- `ValidationError`: If amount or category are invalid

**Side Effects:**
- Adds expense to internal list
- Auto-generates unique ID (handles gaps from deletions)
- Adds current timestamp
- Saves to file immediately

**Example:**
```python
from expense_tracker import ExpenseTracker, ValidationError

tracker = ExpenseTracker()

# Add valid expense
expense = tracker.add_expense(25.50, "Food", "Lunch at restaurant")
print(f"Added expense ID {expense.id}")

# Handle validation errors
try:
    tracker.add_expense(-10, "Food", "Invalid")
except ValidationError as e:
    print(f"Error: {e}")
```

##### get_all_expenses()

```python
def get_all_expenses(self) -> List[Expense]
```

Get all expenses.

**Returns:**
- `List[Expense]`: Copy of all Expense objects

**Note:** Returns a copy to prevent external modification of internal state.

**Example:**
```python
expenses = tracker.get_all_expenses()
print(f"Total expenses: {len(expenses)}")

for expense in expenses:
    print(f"{expense.category}: ${expense.amount}")
```

##### calculate_total()

```python
def calculate_total(self) -> float
```

Calculate total spending across all expenses.

**Returns:**
- `float`: Total amount spent

**Example:**
```python
total = tracker.calculate_total()
print(f"Total spending: ${total:.2f}")
```

##### get_category_breakdown()

```python
def get_category_breakdown(self) -> List[CategorySummary]
```

Calculate spending breakdown by category.

**Returns:**
- `List[CategorySummary]`: List of category summaries sorted by amount (descending)

**CategorySummary attributes:**
- `name` (str): Category name
- `total` (float): Total spent in category
- `percentage` (float): Percentage of total spending

**Example:**
```python
summaries = tracker.get_category_breakdown()

for summary in summaries:
    print(f"{summary.name}: ${summary.total:.2f} ({summary.percentage:.1f}%)")

# Output:
# Entertainment: $100.00 (52.3%)
# Transport: $50.00 (26.1%)
# Food: $41.25 (21.6%)
```

---

### ExpenseTrackerUI Class

User interface for interactive expense tracking.

#### Constructor

```python
ExpenseTrackerUI(tracker: ExpenseTracker)
```

**Parameters:**
- `tracker` (ExpenseTracker): ExpenseTracker instance to use

**Example:**
```python
from expense_tracker import ExpenseTracker, ExpenseTrackerUI

tracker = ExpenseTracker()
ui = ExpenseTrackerUI(tracker)
```

#### Methods

##### run()

```python
def run(self) -> None
```

Run the main application loop.

Displays menu and handles user choices until exit is selected.

**Example:**
```python
tracker = ExpenseTracker()
ui = ExpenseTrackerUI(tracker)
ui.run()  # Starts interactive menu
```

##### handle_add_expense()

```python
def handle_add_expense(self) -> None
```

Handle the 'Add Expense' user action.

Prompts for amount, category, and description, then adds the expense.

##### handle_view_expenses()

```python
def handle_view_expenses(self) -> None
```

Display all expenses in a formatted table.

**Output Format:**
```
================================================================================
ID    Date                 Category        Amount     Description
================================================================================
1     2026-01-02 10:30:00  Food            $25.50     Lunch at restaurant
================================================================================
```

##### handle_calculate_total()

```python
def handle_calculate_total(self) -> None
```

Display total spending and category breakdown.

**Output Format:**
```
Total Spending: $191.25

Spending by Category:
----------------------------------------
Entertainment           $100.00 ( 52.3%)
Transport                $50.00 ( 26.1%)
Food                     $41.25 ( 21.6%)
----------------------------------------
```

---

### Supporting Classes

#### CategorySummary

```python
@dataclass
class CategorySummary:
    name: str
    total: float
    percentage: float
```

Data class representing spending summary for a category.

#### ValidationError

```python
class ValidationError(Exception):
    pass
```

Custom exception raised when expense validation fails.

## Testing

A comprehensive test script is included to verify functionality:

```bash
python test_tracker.py
```

The test script validates:
- ✅ Tracker initialization
- ✅ Expense object creation with validation
- ✅ Adding expenses and ID generation
- ✅ Validation error handling (negative amounts, empty categories)
- ✅ Viewing expenses through UI
- ✅ Total calculation accuracy
- ✅ Category breakdown functionality
- ✅ Data persistence across sessions
- ✅ ID generation after reload (handles gaps correctly)
- ✅ Automatic cleanup of test files

**Example output:**
```
Testing Expense Tracker...
--------------------------------------------------
✓ Tracker initialized
✓ Added 4 expenses
✓ Expense object works correctly
✓ Validation correctly rejects negative amounts
✓ Validation correctly rejects empty categories
...
All tests passed successfully!
```

## Tips

- Use consistent category names for better reporting (e.g., always use "Food" not "food" or "Groceries")
- Add detailed descriptions to remember what each expense was for
- Regularly review your spending using option 3 to identify spending patterns
- Back up your `expenses.json` file periodically to prevent data loss

## Project Structure

```
expense-tracker/
├── expense_tracker.py       # Main application (370 lines)
│   ├── Expense              # Expense entity with validation
│   ├── ExpenseTracker       # Core business logic
│   ├── ExpenseTrackerUI     # User interface layer
│   ├── CategorySummary      # Data class for analytics
│   └── ValidationError      # Custom exception
├── test_tracker.py          # Comprehensive test suite (110 lines)
├── expenses.json            # Data storage (auto-created)
├── README.md                # This documentation
├── CONTRIBUTING.md          # Contribution guidelines
├── CHANGELOG.md             # Version history
├── .claude/                 # Claude Code configuration
│   ├── settings.local.json  # Local settings
│   └── commands/            # Custom commands
│       ├── expense-refactor.md
│       └── expense-report-docs.md
└── .gitignore              # Git ignore rules
```

### Code Organization

**expense_tracker.py** structure:
- **Lines 1-18**: Imports and constants
- **Lines 21-31**: Supporting classes (CategorySummary, ValidationError)
- **Lines 34-100**: Expense class (data model)
- **Lines 103-231**: ExpenseTracker class (business logic)
- **Lines 234-356**: ExpenseTrackerUI class (presentation)
- **Lines 358-370**: Main entry point

## Error Handling

The application includes comprehensive validation and error handling:

### Validation Errors (ValidationError exception)
- **Invalid amounts**: Must be greater than 0
  ```python
  ValidationError: Amount must be greater than 0
  ```
- **Empty categories**: Category field cannot be blank
  ```python
  ValidationError: Category cannot be empty
  ```

### Data Errors
- **Corrupted JSON files**: Gracefully handles decode errors and starts fresh
- **Missing files**: Creates new data file automatically
- **Type errors**: Catches and reports unexpected data types

### User Input Errors
- **Non-numeric amounts**: Caught and reported with clear message
  ```
  Error: Invalid amount. Please enter a number.
  ```
- **Invalid menu choices**: Prompts user to enter valid options (1-4)

### ID Generation
- **Handles deletion gaps**: Uses `max(id) + 1` instead of `len() + 1` to avoid duplicate IDs

## Recent Improvements

**Version 2.0 - Major Refactoring (January 2026)**

The codebase underwent a significant refactoring to improve code quality:

- ✅ **Separated Concerns**: Split business logic from UI into distinct classes
- ✅ **Added Domain Model**: Created `Expense` class for better encapsulation
- ✅ **Fixed ID Bug**: Corrected ID generation to handle deletion gaps
- ✅ **Enhanced Validation**: Centralized validation with custom `ValidationError` exception
- ✅ **Full Type Hints**: Added comprehensive type annotations throughout
- ✅ **Removed Magic Numbers**: Extracted constants for better maintainability
- ✅ **100% Documentation**: Every class and method has detailed docstrings
- ✅ **Improved Testability**: Business logic can now be tested independently

**Benefits:**
- More maintainable code structure
- Easier to test and extend
- Better error handling
- Clearer separation of responsibilities
- Can be used programmatically without UI

## Future Enhancements

Potential features for future versions:

- Delete or edit existing expenses
- Filter expenses by date range or category
- Search functionality for descriptions
- Export reports to CSV or PDF
- Budget tracking and alerts
- Monthly/yearly spending summaries
- Multi-currency support
- Recurring expense tracking
- Data visualization (charts and graphs)
- REST API wrapper for web/mobile apps

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly using `test_tracker.py`
5. Submit a pull request

Please ensure your code follows Python best practices and includes appropriate documentation.

## License

This project is open source and available for personal use and modification.

## Support

For issues, questions, or suggestions, please create an issue in the repository or contact the maintainers.
