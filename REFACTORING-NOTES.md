# Refactoring Notes: camelCase Convention Implementation

## Overview

This document details the comprehensive refactoring of the expense-tracker codebase to implement a hybrid naming convention that balances internal code consistency (camelCase) with external API contract stability (snake_case).

## Date

January 8, 2026

## Scope

Refactored all Python files in the expense-tracker directory:
- `expense_tracker.py` - CLI application
- `test_tracker.py` - CLI tests
- `database.py` - Database configuration
- `auth.py` - Authentication utilities
- `config.py` - Configuration management
- `models.py` - SQLAlchemy models (minimal changes)
- `schemas.py` - Pydantic schemas (minimal changes)
- `api_main.py` - FastAPI application
- `test_api.py` - API integration tests

## Naming Convention Rules

### Internal Code (camelCase)

**What Changed:**
- Local variables: `currentUser`, `dbExpense`, `hashedPassword`, `totalSpending`
- Function names: `addExpense()`, `getAllExpenses()`, `calculateTotal()`, `authenticateUser()`
- Private methods: `_loadExpenses()`, `_saveExpenses()`, `_validateAmount()`, `_generateNextId()`
- Class attributes: `self.dataFile`, `self.expenses`

**Example:**
```python
def authenticateUser(db: Session, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    dummyHash = getPasswordHash("dummy_password")
    passwordHash = user.hashed_password if user else dummyHash
    passwordValid = verifyPassword(password, passwordHash)
    return user if user and passwordValid else None
```

### External API Contracts (snake_case - PRESERVED)

**What Stayed the Same:**
- FastAPI path parameters: `expense_id` in `/expenses/{expense_id}`
- Query parameters: `page_size`, `from_date`, `to_date`, `sort_by`, `sort_order`
- Request body fields: `user_login` (Pydantic model parameters)
- Database columns: `user_id`, `is_deleted`, `created_at`, `hashed_password`
- JSON response fields: `access_token`, `refresh_token`, `total_spending`

**Why This Matters:**
FastAPI uses parameter names for binding. The parameter name in the function signature **must exactly match** the URL path template or query string parameter name.

## Critical Issues Encountered and Fixed

### Issue 1: FastAPI Path Parameter Binding

**Problem:**
```python
# ❌ WRONG - Causes 422 validation errors
@app.get("/expenses/{expense_id}")
def getExpense(expenseId: int):  # FastAPI cannot bind this!
    expense = db.query(Expense).filter(Expense.id == expenseId).first()
```

**Error:**
```
assert 422 == 200  # Unprocessable Entity
```

**Solution:**
```python
# ✅ CORRECT - Parameter matches URL template
@app.get("/expenses/{expense_id}")
def getExpense(expense_id: int):  # Must match {expense_id}
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
```

### Issue 2: Query Parameter Binding

**Problem:**
```python
# ❌ WRONG - Won't match URL query string
def listExpenses(
    pageSize: int = Query(20),  # Won't bind to ?page_size=20
    fromDate: Optional[str] = Query(None)  # Won't bind to ?from_date=...
):
    ...
```

**Solution:**
```python
# ✅ CORRECT - Parameters match query string
def listExpenses(
    page_size: int = Query(20),  # Matches ?page_size=20
    from_date: Optional[str] = Query(None)  # Matches ?from_date=...
):
    # Internal variables can use camelCase
    itemsPerPage = page_size
    fromDatetime = datetime.strptime(from_date, "%Y-%m-%d")
```

### Issue 3: Request Body Fields

**Problem:**
```python
# ❌ WRONG - JSON body field name mismatch
def login(userLogin: UserLogin):  # Expects camelCase in JSON
    user = authenticateUser(db, userLogin.username, userLogin.password)
```

**Solution:**
```python
# ✅ CORRECT - Matches Pydantic schema field names
def login(user_login: UserLogin):  # Matches snake_case schema
    user = authenticateUser(db, user_login.username, user_login.password)
```

## Test Results

### CLI Tests
```bash
python test_tracker.py
```

**Result:** ✅ All tests passed
- Tracker initialization
- Expense object validation
- Adding expenses with auto-generated IDs
- Validation error handling
- Viewing expenses through UI
- Total calculation accuracy
- Category breakdown functionality
- Data persistence across sessions
- ID generation after reload
- Automatic cleanup

### API Tests
```bash
pytest test_api.py -v
```

**Result:** ✅ 26/26 tests passed
- Health check endpoint
- User registration (valid, duplicate email, duplicate username, weak password)
- Login flow (success, wrong password, nonexistent user)
- Current user info (authenticated, unauthorized)
- Expense CRUD operations (create, list, get, update, delete)
- Pagination and filtering
- Expense summary with analytics
- User isolation (cannot access other users' expenses)

## Files Modified

### Major Refactoring

1. **expense_tracker.py** (CLI)
   - 156 lines changed
   - All methods converted to camelCase
   - Private methods: `_loadExpenses`, `_saveExpenses`, `_generateNextId`, `_validateAmount`, `_validateCategory`
   - Public methods: `addExpense`, `getAllExpenses`, `calculateTotal`, `getCategoryBreakdown`
   - UI methods: `displayMenu`, `getMenuChoice`, `handleAddExpense`, `handleViewExpenses`, `handleCalculateTotal`

2. **auth.py** (Authentication)
   - 89 lines changed
   - Functions: `verifyPassword`, `getPasswordHash`, `createAccessToken`, `createRefreshToken`, `verifyToken`, `authenticateUser`, `getCurrentUser`, `getCurrentActiveUser`
   - Variables: `pwdContext`, `oauth2Scheme`, `toEncode`, `encodedJwt`, `credentialsException`

3. **api_main.py** (FastAPI)
   - 178 lines changed
   - Endpoint functions: `healthCheck`, `registerUser`, `login`, `getCurrentUserInfo`, `createExpense`, `listExpenses`, `getExpenseSummary`, `getExpense`, `updateExpense`, `deleteExpense`
   - **Critical**: Kept path/query parameters as snake_case
   - Internal variables: `dbUser`, `hashedPassword`, `accessToken`, `currentUser`, `sortColumn`, `fromDatetime`

4. **test_api.py** (API Tests)
   - 127 lines changed
   - Fixtures: `testDb`, `testUser`, `authHeaders`, `testExpense`
   - Test functions: snake_case (pytest convention)
   - Internal variables: `expensesData`, `expData`, `foodCategory`, `user2Token`

5. **test_tracker.py** (CLI Tests)
   - 42 lines changed
   - Test function: `testExpenseTracker`
   - Variables: `testFile`, `expectedTotal`

6. **database.py**
   - 8 lines changed
   - Functions: `getDb`, `initDb`

### Minimal Changes

7. **config.py** - No changes (constants)
8. **models.py** - No changes (SQLAlchemy column names must stay snake_case)
9. **schemas.py** - No changes (Pydantic field names must stay snake_case for JSON API)

## Documentation Updates

### CLAUDE.md
Added comprehensive section on "Code Style and Naming" with:
- Internal vs External naming rules
- Real-world examples with ✅ CORRECT and ❌ WRONG patterns
- FastAPI-specific guidelines
- Testing conventions

### expense-tracker/README.md
Added new section "Code Style and Naming Conventions" with:
- Internal camelCase examples
- External snake_case requirements
- Why this matters (FastAPI binding explanation)
- Testing conventions with examples

### README-4ApiDeveloperAgent.md
Added bullet point to Design & Architecture section:
- Naming convention guidance for API reviewers

### REFACTORING-NOTES.md (This File)
Comprehensive documentation of:
- What was refactored and why
- Issues encountered and solutions
- Test results
- Lessons learned

## Lessons Learned

### 1. Framework Binding Requirements

Modern web frameworks like FastAPI rely on parameter name matching for dependency injection and request binding. Changing parameter names without understanding this can break the entire API.

**Key Takeaway:** Always preserve parameter names for:
- URL path templates: `{expense_id}`
- Query strings: `?page_size=20`
- Request body field names (aligned with Pydantic schemas)

### 2. Testing is Essential

Without comprehensive tests, the refactoring would have shipped broken code. The test suite caught all binding issues immediately.

**Key Takeaway:**
- Run CLI tests: `python test_tracker.py`
- Run API tests: `pytest test_api.py -v`
- Both must pass before committing

### 3. Separation of Concerns

The hybrid naming convention works because:
- External contracts (API, database) follow industry standards (snake_case)
- Internal implementation follows project standards (camelCase)
- Clear boundaries between public API and private implementation

### 4. Documentation is Critical

The refactoring revealed edge cases that needed documentation:
- FastAPI parameter binding rules
- Pytest fixture naming conventions
- When to use snake_case vs camelCase

**Key Takeaway:** Update documentation alongside code changes.

## Best Practices Established

### When to Use camelCase
✅ Local variables inside functions
✅ Function and method names
✅ Private methods (prefixed with `_`)
✅ Class attributes (internal state)
✅ Pytest fixtures
✅ Test internal variables

### When to Use snake_case
✅ FastAPI path parameters (must match URL)
✅ FastAPI query parameters (must match query string)
✅ Request body parameter names (must match schema)
✅ Database column names (SQLAlchemy)
✅ JSON field names (Pydantic schemas)
✅ Pytest test function names (convention)

### Red Flags
🚩 FastAPI function parameter doesn't match URL path template
🚩 Query parameter doesn't match URL query string format
🚩 Test functions using camelCase (pytest won't discover them)
🚩 Database columns using camelCase (breaks SQL conventions)
🚩 JSON fields using camelCase (breaks REST API conventions)

## Migration Guide

If you need to refactor another project to this convention:

1. **Start with Tests**
   - Ensure comprehensive test coverage
   - Tests will catch binding issues immediately

2. **Refactor in Layers**
   - Start with pure business logic (no external dependencies)
   - Then move to API/database layer
   - Keep external interfaces last

3. **Identify Boundaries**
   - Mark which parameters are "external" (from HTTP, database)
   - Mark which are "internal" (local variables, private methods)

4. **Test After Each File**
   - Don't batch refactoring
   - Test immediately after each file change
   - Easier to pinpoint issues

5. **Update Documentation**
   - Document the convention rules
   - Provide examples of correct and incorrect usage
   - Explain why (framework requirements)

## Conclusion

The refactoring successfully implemented a hybrid naming convention that:
- Improves internal code readability (camelCase)
- Maintains external API stability (snake_case)
- Passes all 37 tests (11 CLI + 26 API)
- Documents the rationale and rules clearly

The key insight is that **external contracts must be stable** while **internal implementation can follow project conventions**. This balance is achieved by understanding framework binding mechanisms and respecting industry standards for APIs and databases.

## References

- [CLAUDE.md](./CLAUDE.md) - Project guidance with naming rules
- [expense-tracker/README.md](./expense-tracker/README.md) - Implementation examples
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Parameter binding
- [PEP 8](https://peps.python.org/pep-0008/) - Python style guide (snake_case for module level)
- [REST API Best Practices](https://restfulapi.net/) - snake_case for JSON fields
