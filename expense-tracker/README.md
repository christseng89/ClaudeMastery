# Expense Tracker

A simple command-line expense tracker application built with Python. Track your expenses with categories, descriptions, and automatic date/time stamps.

## Features

- **Add New Expenses**: Record expenses with amount, category, and description
- **View All Expenses**: Display all recorded expenses in a formatted table
- **Calculate Total Spending**: See your total spending and breakdown by category
- **Persistent Storage**: All data is automatically saved to a JSON file

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
- **id**: Unique identifier
- **amount**: Expense amount (float)
- **category**: Category name (string)
- **description**: Expense description (string)
- **date**: Timestamp when the expense was added

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

## Tips

- Use consistent category names for better reporting
- Add detailed descriptions to remember what each expense was for
- Regularly review your spending using option 3

## Project Structure

```
expense-tracker/
├── expense_tracker.py   # Main application file
├── expenses.json        # Data file (created automatically)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Future Enhancements

Potential features for future versions:
- Delete or edit existing expenses
- Filter expenses by date range or category
- Export reports to CSV or PDF
- Budget tracking and alerts
- Monthly/yearly spending summaries

## License

This project is open source and available for personal use.
