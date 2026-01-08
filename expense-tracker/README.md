# Expense Tracker

A comprehensive expense tracking solution with both a command-line interface and a RESTful API. Built with Python, it provides flexible expense management with categories, descriptions, automatic timestamps, user authentication, and advanced analytics.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [REST API](#rest-api) - For web/mobile applications
  - [Command-Line Interface](#command-line-interface) - For local terminal use
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Recent Improvements](#recent-improvements)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

## Which Version Should I Use?

### Use the REST API if you:
- Want to build a web or mobile frontend
- Need multi-user support with authentication
- Require remote access to expense data
- Want to integrate with other applications
- Need advanced filtering, pagination, and analytics

### Use the Command-Line Interface if you:
- Prefer working in the terminal
- Want a simple, single-user solution
- Don't need a web interface
- Want zero external dependencies
- Need quick local expense tracking

Both versions can coexist and use different data stores (API uses SQLite, CLI uses JSON).

## Features

### Command-Line Interface
- **Add New Expenses**: Record expenses with amount, category, and description
- **View All Expenses**: Display all recorded expenses in a formatted table
- **Calculate Total Spending**: See your total spending and breakdown by category with percentages
- **Persistent Storage**: All data is automatically saved to a JSON file
- **Category Analytics**: Automatic spending breakdown by category
- **Data Validation**: Input validation to ensure data integrity

### REST API
- **JWT Authentication**: Secure user registration and login with access and refresh tokens
- **Full CRUD Operations**: Create, read, update, and delete expenses
- **Advanced Filtering**: Filter expenses by category, date range, and amount
- **Pagination & Sorting**: Efficient data retrieval with customizable page sizes and sort options
- **Expense Analytics**: Category-based spending summaries with percentages
- **Rate Limiting**: Protection against API abuse
- **SQLite Database**: Persistent storage with SQLAlchemy ORM
- **Soft Deletes**: Expense records retained for audit purposes
- **API Documentation**: Interactive Swagger UI and ReDoc documentation

## Requirements

### Command-Line Interface
- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

### REST API
- Python 3.8 or higher
- FastAPI - Modern web framework for building APIs
- SQLAlchemy - SQL toolkit and ORM
- Pydantic - Data validation using Python type annotations
- python-jose[cryptography] - JWT token encoding/decoding
- passlib[bcrypt] - Password hashing
- uvicorn - ASGI server
- slowapi - Rate limiting for FastAPI

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd expense-tracker
   ```

### For Command-Line Interface
No additional installation needed - just run the script directly.

### For REST API

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install fastapi sqlalchemy pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] uvicorn slowapi python-multipart
   ```

3. (Optional) Create a `.env` file for custom configuration:
   ```env
   DATABASE_URL=sqlite:///./expense_tracker.db
   SECRET_KEY=your-secure-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   RATE_LIMIT_PER_MINUTE=60
   ```

## Usage

---

## REST API

### Quick Start

1. Start the API server:
   ```bash
   python api_main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn api_main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Access the interactive API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. Health check:
   ```bash
   curl http://localhost:8000/health
   ```

### Authentication Flow

#### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePass123"
  }'
```

**Response:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "id": 1,
  "is_active": true,
  "created_at": "2026-01-08T10:30:00"
}
```

#### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Get Current User Info

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Expense Endpoints

#### Create an Expense

```bash
curl -X POST "http://localhost:8000/api/v1/expenses" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 45.50,
    "category": "Food",
    "description": "Dinner at Italian restaurant"
  }'
```

**Response:**
```json
{
  "id": 1,
  "amount": 45.50,
  "category": "Food",
  "description": "Dinner at Italian restaurant",
  "date": "2026-01-08T19:30:00",
  "created_at": "2026-01-08T19:30:00",
  "user_id": 1
}
```

#### List Expenses (with Pagination & Filtering)

```bash
# Basic list
curl -X GET "http://localhost:8000/api/v1/expenses" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# With filters
curl -X GET "http://localhost:8000/api/v1/expenses?category=Food&from_date=2026-01-01&to_date=2026-01-31&min_amount=10&max_amount=100&page=1&page_size=20&sort_by=date&sort_order=desc" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "amount": 45.50,
      "category": "Food",
      "description": "Dinner at Italian restaurant",
      "date": "2026-01-08T19:30:00",
      "created_at": "2026-01-08T19:30:00",
      "user_id": 1
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

#### Get Expense Summary

```bash
# Overall summary
curl -X GET "http://localhost:8000/api/v1/expenses/summary" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Summary with date filter
curl -X GET "http://localhost:8000/api/v1/expenses/summary?from_date=2026-01-01&to_date=2026-01-31" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "total_spending": 245.75,
  "total_expenses": 8,
  "categories": [
    {
      "category": "Food",
      "total": 125.50,
      "percentage": 51.1,
      "count": 4
    },
    {
      "category": "Transport",
      "total": 75.00,
      "percentage": 30.5,
      "count": 2
    },
    {
      "category": "Entertainment",
      "total": 45.25,
      "percentage": 18.4,
      "count": 2
    }
  ],
  "date_range": {
    "from": "2026-01-01",
    "to": "2026-01-31"
  }
}
```

#### Get Single Expense

```bash
curl -X GET "http://localhost:8000/api/v1/expenses/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Update an Expense

```bash
curl -X PUT "http://localhost:8000/api/v1/expenses/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00,
    "description": "Updated: Dinner at Italian restaurant"
  }'
```

#### Delete an Expense

```bash
curl -X DELETE "http://localhost:8000/api/v1/expenses/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### API Endpoints Reference

#### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register a new user | No |
| POST | `/api/v1/auth/login` | Login and get tokens | No |
| GET | `/api/v1/auth/me` | Get current user info | Yes |

#### Expenses
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/expenses` | Create a new expense | Yes |
| GET | `/api/v1/expenses` | List expenses (paginated) | Yes |
| GET | `/api/v1/expenses/summary` | Get expense summary | Yes |
| GET | `/api/v1/expenses/{id}` | Get specific expense | Yes |
| PUT | `/api/v1/expenses/{id}` | Update an expense | Yes |
| DELETE | `/api/v1/expenses/{id}` | Delete an expense (soft) | Yes |

#### System
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health` | Health check | No |

### Query Parameters

#### List Expenses (`GET /api/v1/expenses`)
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 20, max: 100)
- `category` (string): Filter by category name
- `from_date` (string): Start date in YYYY-MM-DD format
- `to_date` (string): End date in YYYY-MM-DD format
- `min_amount` (float): Minimum expense amount
- `max_amount` (float): Maximum expense amount
- `sort_by` (string): Sort field - `date`, `amount`, or `category` (default: `date`)
- `sort_order` (string): Sort order - `asc` or `desc` (default: `desc`)

#### Get Summary (`GET /api/v1/expenses/summary`)
- `from_date` (string): Start date in YYYY-MM-DD format
- `to_date` (string): End date in YYYY-MM-DD format

### Configuration

The API can be configured using environment variables or a `.env` file:

```env
# Application
APP_NAME=Expense Tracker API
VERSION=1.0.0
API_V1_PREFIX=/api/v1

# Database
DATABASE_URL=sqlite:///./expense_tracker.db

# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

**Security Notes:**
- Always change `SECRET_KEY` in production to a strong random value
- Use environment variables for sensitive configuration
- Enable HTTPS in production
- Configure CORS origins appropriately for your frontend

### Database

The API uses SQLite by default with SQLAlchemy ORM. The database file `expense_tracker.db` is automatically created on first run.

**Database Schema:**

**Users Table:**
- `id`: Integer (Primary Key)
- `email`: String (Unique)
- `username`: String (Unique)
- `hashed_password`: String
- `is_active`: Boolean
- `created_at`: DateTime
- `updated_at`: DateTime

**Expenses Table:**
- `id`: Integer (Primary Key)
- `amount`: Float
- `category`: String (Indexed)
- `description`: String
- `date`: DateTime (Indexed)
- `created_at`: DateTime
- `updated_at`: DateTime
- `is_deleted`: Boolean (Soft delete flag)
- `user_id`: Integer (Foreign Key to Users)

### Error Handling

The API returns consistent error responses:

```json
{
  "error": {
    "code": 400,
    "message": "Email already registered",
    "path": "/api/v1/auth/register"
  }
}
```

**Common HTTP Status Codes:**
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `204 No Content`: Successful deletion
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Rate Limiting

The API implements rate limiting to prevent abuse:
- Default: 60 requests per minute per IP address
- Registration endpoint: 5 requests per minute
- Can be configured via `RATE_LIMIT_PER_MINUTE` environment variable

When rate limit is exceeded, you'll receive a `429 Too Many Requests` response.

### Testing the API

A test suite is included for API endpoints:

```bash
pytest test_api.py -v
```

Or test manually using the interactive documentation at `/docs`.

---

## Command-Line Interface

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
├── expense_tracker.py       # CLI application (370 lines)
│   ├── Expense              # Expense entity with validation
│   ├── ExpenseTracker       # Core business logic
│   ├── ExpenseTrackerUI     # User interface layer
│   ├── CategorySummary      # Data class for analytics
│   └── ValidationError      # Custom exception
├── api_main.py              # FastAPI application (550 lines)
│   └── REST API endpoints and error handlers
├── models.py                # SQLAlchemy database models
│   ├── User                 # User model with authentication
│   └── Expense              # Expense model with relationships
├── schemas.py               # Pydantic validation schemas
│   ├── UserCreate, UserResponse, UserLogin
│   ├── Token, TokenData
│   ├── ExpenseCreate, ExpenseUpdate, ExpenseResponse
│   └── ExpenseSummary, CategorySummary
├── auth.py                  # Authentication utilities
│   ├── Password hashing (bcrypt)
│   ├── JWT token management
│   └── User authentication dependencies
├── database.py              # Database configuration
│   └── SQLAlchemy setup and session management
├── config.py                # Application configuration
│   └── Settings with environment variable support
├── test_tracker.py          # CLI test suite
├── test_api.py              # API test suite
├── expenses.json            # CLI data storage (auto-created)
├── expense_tracker.db       # API SQLite database (auto-created)
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (optional)
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

**expense_tracker.py** (CLI) structure:
- **Lines 1-18**: Imports and constants
- **Lines 21-31**: Supporting classes (CategorySummary, ValidationError)
- **Lines 34-100**: Expense class (data model)
- **Lines 103-231**: ExpenseTracker class (business logic)
- **Lines 234-356**: ExpenseTrackerUI class (presentation)
- **Lines 358-370**: Main entry point

**api_main.py** (REST API) structure:
- **Lines 1-28**: Imports and dependencies
- **Lines 30-60**: Application setup (FastAPI, CORS, rate limiting)
- **Lines 62-74**: Health check endpoint
- **Lines 76-175**: Authentication endpoints (register, login, get user)
- **Lines 177-503**: Expense endpoints (CRUD operations)
- **Lines 505-537**: Error handlers
- **Lines 539-551**: Main entry point

**Other modules:**
- **models.py**: SQLAlchemy database models (User, Expense)
- **schemas.py**: Pydantic request/response schemas
- **auth.py**: JWT authentication and password hashing
- **database.py**: Database configuration and session management
- **config.py**: Application settings and environment variables

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

**Version 3.0 - REST API (January 2026)**

Added a comprehensive REST API for web and mobile applications:

- ✅ **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- ✅ **JWT Authentication**: Secure user authentication with access and refresh tokens
- ✅ **SQLAlchemy ORM**: Database abstraction with SQLite backend
- ✅ **Advanced Filtering**: Multi-criteria expense filtering and sorting
- ✅ **Pagination**: Efficient data retrieval with customizable page sizes
- ✅ **Analytics API**: Category-based spending summaries with percentages
- ✅ **Rate Limiting**: Protection against API abuse
- ✅ **Soft Deletes**: Audit trail for deleted expenses
- ✅ **Error Handling**: Consistent error response format
- ✅ **Interactive Docs**: Auto-generated Swagger UI and ReDoc documentation

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
- Multi-platform support via REST API

## Future Enhancements

Potential features for future versions:

**Command-Line Interface:**
- Export reports to CSV or PDF
- Data visualization (charts and graphs) in terminal

**REST API:**
- Budget tracking and alerts
- Monthly/yearly spending summaries
- Multi-currency support
- Recurring expense tracking
- Data export endpoints (CSV, PDF)
- Expense attachments (receipts)
- Expense tags and notes
- Expense categories management
- User profile management
- Email notifications
- Two-factor authentication
- OAuth2 social login
- WebSocket support for real-time updates

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
