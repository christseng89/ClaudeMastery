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

Run the expense tracker:

```bash
python expense_tracker.py
```

### Menu Options

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

## API Reference

### ExpenseTracker Class

The main class that handles all expense tracking functionality.

#### Constructor

```python
ExpenseTracker(data_file='expenses.json')
```

**Parameters:**
- `data_file` (str): Path to the JSON file for storing expenses. Defaults to 'expenses.json'

**Example:**
```python
tracker = ExpenseTracker()
# or with custom file
tracker = ExpenseTracker(data_file='my_expenses.json')
```

#### Methods

##### load_expenses()

```python
def load_expenses(self) -> List[Dict]
```

Load expenses from JSON file. Called automatically during initialization.

**Returns:**
- `List[Dict]`: List of expense dictionaries

**Behavior:**
- Returns empty list if file doesn't exist
- Handles JSON decode errors gracefully
- Prints warning if file is corrupted

**Example:**
```python
expenses = tracker.load_expenses()
# Returns: [{'id': 1, 'amount': 25.50, 'category': 'Food', ...}, ...]
```

##### save_expenses()

```python
def save_expenses(self)
```

Save current expenses to JSON file with indentation.

**Side Effects:**
- Writes to the data file specified in constructor
- Prints confirmation message
- Creates file if it doesn't exist

**Example:**
```python
tracker.save_expenses()
# Output: "Data saved to expenses.json"
```

##### add_expense()

```python
def add_expense(self, amount: float, category: str, description: str)
```

Add a new expense to the tracker.

**Parameters:**
- `amount` (float): The expense amount (must be positive)
- `category` (str): The expense category (e.g., "Food", "Transport")
- `description` (str): Description of the expense

**Returns:**
- None

**Side Effects:**
- Adds expense to internal list
- Auto-generates unique ID
- Adds current timestamp
- Saves to file immediately
- Prints success message with ID

**Example:**
```python
tracker.add_expense(25.50, "Food", "Lunch at restaurant")
# Output: "Expense added successfully! (ID: 1)"
#         "Data saved to expenses.json"
```

##### view_expenses()

```python
def view_expenses(self)
```

Display all expenses in a formatted table.

**Returns:**
- None

**Output Format:**
- Header with column names (ID, Date, Category, Amount, Description)
- Formatted rows with aligned columns
- Border decorations for readability

**Example:**
```python
tracker.view_expenses()
# Output:
# ================================================================================
# ID    Date                 Category        Amount     Description
# ================================================================================
# 1     2026-01-02 10:30:00  Food            $25.50     Lunch at restaurant
# ================================================================================
```

##### calculate_total()

```python
def calculate_total(self)
```

Calculate and display total spending with category breakdown.

**Returns:**
- None

**Output:**
- Total spending across all expenses
- Per-category spending amounts
- Percentage breakdown for each category
- Categories sorted by spending (highest first)

**Example:**
```python
tracker.calculate_total()
# Output:
# Total Spending: $191.25
#
# Spending by Category:
# ----------------------------------------
# Entertainment        $100.00 ( 52.3%)
# Transport            $ 50.00 ( 26.1%)
# Food                 $ 41.25 ( 21.6%)
# ----------------------------------------
```

## Testing

A test script is included to verify functionality:

```bash
python test_tracker.py
```

The test script will:
- Create a test instance with a temporary data file
- Add sample expenses
- Test viewing and calculation features
- Verify data persistence
- Clean up test files automatically

## Tips

- Use consistent category names for better reporting (e.g., always use "Food" not "food" or "Groceries")
- Add detailed descriptions to remember what each expense was for
- Regularly review your spending using option 3 to identify spending patterns
- Back up your `expenses.json` file periodically to prevent data loss

## Project Structure

```
expense-tracker/
├── expense_tracker.py       # Main application file with ExpenseTracker class
├── test_tracker.py          # Test script for functionality verification
├── expenses.json            # Data file (created automatically)
├── .claude/                 # Claude Code configuration
│   ├── settings.local.json  # Local project settings
│   └── commands/            # Custom commands
│       └── expense-report-docs.md
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Error Handling

The application includes validation and error handling for:

- **Invalid amounts**: Must be greater than 0
- **Empty categories**: Category field cannot be blank
- **Invalid input types**: Non-numeric amounts are caught and reported
- **Corrupted data files**: Gracefully handles JSON decode errors
- **Invalid menu choices**: Prompts user to enter valid options

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
