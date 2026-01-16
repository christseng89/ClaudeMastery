# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Claude Code Learning & Mastery Repository** - a comprehensive educational knowledge base designed to teach developers how to use Claude Code effectively. It combines documentation, working examples, and advanced patterns including custom agents and slash commands.

## Key Architecture Patterns

### Learning Documentation Structure

The root-level README files follow a numbered learning progression:

1. **README-1.1Introduction.md** - Language model landscape and Claude overview
2. **README-1.2BusinessFormula.md** - Business logic extraction use case
3. **README-2SlashCommand.md** - Custom slash command implementation
4. **README-3SubAgents.md** - Subagent architecture patterns
5. **README-4ApiDeveloperAgent.md** - API reviewer agent example
6. **README-5WorkflowWSubagentAndSlashCommand.md** - Advanced multi-agent workflows
7. **README-6Context.md** - Context and memory management
8. **README-8Hooks.md** - Hooks system and automation patterns

Read these in order for proper context when creating new learning materials.

### Custom Agent & Command System

**Custom Agents** (`.claude/agents/`):
- `api-reviewer.md` - Specialized API design review agent
- `restaurant-scout.md` - Travel planning and restaurant discovery
- `travel-activity-planner.md` - Activity and itinerary planning

**Custom Slash Commands** (`.claude/commands/`):
- `auto-commit.md` - Smart git commit message generation
- `security-review.md` - Security vulnerability analysis
- `api-review-and-commit-workflow.md` - Combined API review + commit workflow
- `review-pr.md` - Pull request review with arguments
- `merge-and-create-branch.md` - Branch management workflow
- `create-docs.md` - Documentation generation

When creating new commands or agents, follow the existing frontmatter patterns with `name`, `description`, `version`, and `allowed-tools`.

### Hooks System

**Hooks** are user-defined shell scripts that execute automatically at specific points during Claude Code's operation lifecycle. They enable workflow automation, policy enforcement, and external tool integration.

**Hook Scripts Location:** `~/.claude/scripts/`

**Key Hook Types:**
- **SessionStart/SessionEnd** - Session lifecycle management
- **UserPromptSubmit** - Prompt validation and context injection (blocking)
- **PreToolUse** - Tool execution validation and approval (blocking)
- **PostToolUse** - Post-execution automation (formatting, testing, logging)
- **Notification** - Custom notification handling
- **SubagentStop** - Subagent completion handling
- **PreCompact/Stop** - Context management and cleanup

**Implemented Hooks:**

1. **format-typescript.sh** - Automatic TypeScript/TSX formatting
   - Triggers: PostToolUse (Write, Edit, MultiEdit)
   - Uses prettier for code formatting
   - Provides success/failure feedback

2. **activity-logger.sh** - Tool usage logging and auditing
   - Triggers: PreToolUse (all tools)
   - Logs tool name, file path, project directory to daily log files
   - Location: `~/.claude/logs/YYYY-MM-DD.log`
   - Includes JSON parsing with jq and fallback handling

**Configuration:** Hooks are configured in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [{"type": "command", "command": "~/.claude/scripts/format-typescript.sh"}]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [{"type": "command", "command": "~/.claude/scripts/activity-logger.sh"}]
      }
    ]
  }
}
```

**Hook Script Structure:**
- Read JSON input from stdin containing tool information
- Parse with `jq` (with fallback for missing jq)
- Perform action (format, log, validate, etc.)
- Output feedback to stderr (to avoid interfering with hook output)
- Exit with status code (0 = success, non-zero = error)

**Best Practices:**
- Always check tool availability (jq, prettier, etc.)
- Use temp files for stdin processing to avoid piping issues
- Provide clear success/failure feedback to users
- Log to dedicated directories with appropriate permissions
- Restart Claude Code after modifying hook configuration

For comprehensive hook documentation, patterns, and examples, see **README-8Hooks.md**.

### Example Project: expense-tracker

The `expense-tracker/` directory contains a production-grade dual-implementation example:

**CLI Application** (`expense_tracker.py`):
- Model-View architecture (Expense, ExpenseTracker, ExpenseTrackerUI)
- JSON-based persistent storage
- Zero external dependencies
- Comprehensive validation with custom ValidationError

**REST API** (`api_main.py`):
- FastAPI framework with auto-generated OpenAPI docs
- JWT authentication (access + refresh tokens)
- SQLAlchemy ORM with SQLite database
- Pydantic schemas for validation
- Rate limiting and CORS configuration
- Soft deletes for audit trails
- Multi-criteria filtering and pagination

**Key Architecture:**
```
expense-tracker/
├── expense_tracker.py      # CLI: Model-View pattern, JSON storage
├── api_main.py            # FastAPI app: REST endpoints
├── models.py              # SQLAlchemy: User, Expense models
├── schemas.py             # Pydantic: Request/response validation
├── auth.py                # JWT + bcrypt authentication
├── database.py            # SQLAlchemy session management
├── config.py              # Settings with environment variable support
├── test_tracker.py        # CLI test suite
└── test_api.py            # API integration tests (30+ tests)
```

## Development Commands

### Expense Tracker - CLI

```bash
# Run CLI application
python expense_tracker.py

# Run CLI tests
python test_tracker.py
```

### Expense Tracker - REST API

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi sqlalchemy pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] uvicorn slowapi python-multipart

# Start API server
python api_main.py
# Or with uvicorn
uvicorn api_main:app --reload --host 0.0.0.0 --port 8000

# Run API tests
pytest test_api.py -v

# Access documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc

# Health check
curl http://localhost:8000/health
```

### Claude Code Operations

**Custom slash commands** are invoked within Claude conversations:
```bash
/auto-commit                    # Generate smart commit message
/security-review                # Analyze security vulnerabilities
/review-pr 123 High John       # Review PR with arguments
/api-review-and-commit-workflow # API review + commit
```

**Custom agents** are referenced with `@` notation in prompts:
```bash
@api-reviewer [review the expense API endpoints]
@restaurant-scout [find family restaurants in Taipei]
@travel-activity-planner [plan 3-day Tokyo itinerary]
```

## Important Conventions

### Code Style and Naming

**Python Naming Convention - Internal vs External:**

This repository follows a **hybrid naming convention** that balances internal code consistency with external API contract stability:

**Internal Code (camelCase):**
- **Local variables**: `currentUser`, `dbExpense`, `hashedPassword`, `totalSpending`
- **Function names**: `addExpense()`, `getAllExpenses()`, `calculateTotal()`, `authenticateUser()`
- **Private methods**: `_loadExpenses()`, `_saveExpenses()`, `_validateAmount()`, `_generateNextId()`
- **Function parameters** (non-API): `expenseId`, `categoryTotals`, `fromDatetime`, `toDatetime`
- **Class attributes** (internal): `self.dataFile`, `self.expenses`

**External API Contracts (snake_case - MUST NOT CHANGE):**
- **FastAPI path parameters**: `expense_id` in `/expenses/{expense_id}` must match function parameter
- **Query parameters**: `page_size`, `from_date`, `to_date`, `sort_by`, `sort_order` (match URL query strings)
- **Request body fields**: `user_login` (Pydantic model field names)
- **Database columns**: `user_id`, `is_deleted`, `created_at`, `hashed_password` (SQLAlchemy models)
- **JSON response fields**: `access_token`, `refresh_token`, `total_spending` (Pydantic schemas)

**Why This Matters:**
```python
# ✅ CORRECT: Path parameter matches URL template
@app.get("/expenses/{expense_id}")
def getExpense(expense_id: int, currentUser: User = Depends(getCurrentActiveUser)):
    dbExpense = db.query(Expense).filter(Expense.id == expense_id).first()
    return dbExpense

# ❌ WRONG: Path parameter doesn't match URL template
@app.get("/expenses/{expense_id}")
def getExpense(expenseId: int):  # FastAPI cannot bind this!
    ...

# ✅ CORRECT: Query parameter matches URL query string
def listExpenses(page_size: int = Query(20)):  # Matches ?page_size=20
    itemsPerPage = page_size  # Internal variable can use camelCase
    ...

# ❌ WRONG: Query parameter won't match URL
def listExpenses(pageSize: int = Query(20)):  # Won't match ?page_size=20
    ...
```

**Additional Python Standards:**
- Comprehensive docstrings for all classes and methods
- Type hints throughout (Python 3.8+)
- Custom exceptions for domain errors (e.g., ValidationError)

**API Design:**
- RESTful conventions with proper HTTP methods (GET, POST, PUT, DELETE)
- Versioned endpoints: `/api/v1/` prefix
- Pagination: page-based with customizable size (default: 20, max: 100)
- Filtering: multi-criteria with query parameters
- Error responses: consistent JSON structure with `error.code`, `error.message`, `error.path`
- Rate limiting: 60 requests/minute default, configurable per endpoint

### Configuration Management

**Settings Priority:**
1. Environment variables (`.env` file)
2. Configuration class defaults (`config.py`)
3. Hardcoded fallbacks

**Critical Settings to Configure:**
- `SECRET_KEY` - Must be changed in production (JWT signing)
- `DATABASE_URL` - SQLite default, can use PostgreSQL/MySQL
- `CORS_ORIGINS` - Restrict to frontend domains in production
- `RATE_LIMIT_PER_MINUTE` - Adjust based on expected load

### Security Patterns

**Authentication:**
- JWT tokens: separate access (30 min) and refresh (7 days) tokens
- Password hashing: bcrypt with salt rounds
- Token validation: verify signature, expiration, and user status
- Protected routes: dependency injection pattern with `get_current_user`

**Data Protection:**
- Soft deletes: `is_deleted` flag for audit trails
- No cascade deletes: preserve referential integrity
- Input validation: Pydantic schemas prevent injection
- Rate limiting: prevent brute force and abuse

**Security Checklist for New Features:**
- Never commit `.env` files or secrets
- Validate all user input with Pydantic schemas
- Use parameterized queries (SQLAlchemy ORM handles this)
- Apply rate limiting to authentication endpoints
- Test with invalid tokens and expired credentials

### Testing Conventions

**Test Naming:**
- **Test functions**: Use snake_case for pytest discovery: `test_create_expense_success()`
- **Fixtures**: Use camelCase: `testDb`, `testUser`, `authHeaders`, `testExpense`
- **Internal variables**: Use camelCase: `expenseId`, `expensesData`, `foodCategory`, `user2Headers`

**CLI Tests** (`test_tracker.py`):
- Unit tests for business logic (Expense, ExpenseTracker)
- Validation error testing
- Data persistence verification
- Automatic cleanup of test files
- Uses camelCase for variables: `testFile`, `expectedTotal`

**API Tests** (`test_api.py`):
- Integration tests with FastAPI TestClient
- Fixtures for database setup/teardown
- Auth flow testing (register → login → protected endpoints)
- Edge cases: invalid tokens, missing fields, unauthorized access
- Response format validation
- Fixtures use camelCase: `testDb()`, `testUser()`, `authHeaders()`

**Run Tests Before Committing:**
```bash
python test_tracker.py        # CLI tests (all should pass)
pytest test_api.py -v         # API tests with verbose output (26 tests)
```

**Test Structure Example:**
```python
# Fixture with camelCase
@pytest.fixture
def testUser(testDb):
    user = User(email="test@example.com", username="testuser")
    testDb.add(user)
    return user

# Test function with snake_case (pytest convention)
def test_create_expense_success(client, authHeaders):
    # Internal variables use camelCase
    expenseData = {"amount": 25.50, "category": "Food"}
    response = client.post("/api/v1/expenses", json=expenseData, headers=authHeaders)
    assert response.status_code == 201
```

### Git Workflow

**Branch Strategy:**
- `main` branch for stable code
- Feature branches for new work
- Descriptive commit messages following project style

**Recent Commit Patterns:**
- "Advanced Workflow with Subagent and Slash Command"
- "Fix config for development mode and add comprehensive workflow"
- "Fix critical security vulnerabilities in expense tracker API"
- "Add database files to gitignore"

Follow this style: start with action verb (Add, Fix, Update, Refactor), be specific, reference security issues explicitly.

## File Organization Logic

### Root Level
- **README-*.md** - Numbered learning progression (1.1, 1.2, 2, 3, 4, 5, 6, 8)
- **CLAUDE.md** - This file (project guidance)
- **.claude/** - Claude Code configuration
- **expense-tracker/** - Working example project
- **Resources/** - Supplementary learning materials
- **Travel Examples/** - Real-world application demonstrations

### .claude Directory Structure

```
.claude/
├── settings.local.json    # Tool permissions, MCP server config, and hooks configuration
├── agents/               # Custom subagent definitions
│   ├── api-reviewer.md
│   ├── restaurant-scout.md
│   └── travel-activity-planner.md
└── commands/            # Custom slash command definitions
    ├── auto-commit.md
    ├── security-review.md
    └── api-review-and-commit-workflow.md

~/.claude/
├── scripts/             # Hook scripts (user-level)
│   ├── format-typescript.sh    # Auto-format TypeScript files
│   └── activity-logger.sh      # Log tool usage to daily files
└── logs/               # Activity logs generated by hooks
    └── YYYY-MM-DD.log  # Daily activity logs
```

**Project-Specific Commands:**
The expense-tracker also has `.claude/commands/` for domain-specific workflows.

### Tool Permissions

The `.claude/settings.local.json` defines allowed tools. Current permissions include:
- Git operations: `git add`, `git commit`
- Python execution: various `python` and `pip` commands
- MCP tools: weather API access
- Web tools: `WebSearch`

When creating new workflows that require additional tools, add them to `settings.local.json`.

## Common Development Patterns

### Adding New Learning Documentation

1. Follow the numbering scheme (README-N.md)
2. Include practical examples (code snippets or working demos)
3. Reference existing patterns (agents, commands, expense-tracker)
4. Use markdown tables for reference information
5. Add diagrams with mermaid when explaining architecture

### Creating Custom Agents

1. Add `.md` file to `.claude/agents/`
2. Include frontmatter: name, description, version, allowed-tools
3. Define system prompt with role, capabilities, and constraints
4. Specify tool usage patterns and response format
5. Add examples demonstrating agent capabilities
6. Update this CLAUDE.md with agent description

### Creating Custom Slash Commands

1. Add `.md` file to `.claude/commands/`
2. Include frontmatter with command metadata
3. Write clear instructions for command execution
4. Specify expected inputs and outputs
5. Handle error cases and edge conditions
6. Test command with various scenarios

### Extending Expense Tracker

**For CLI:**
- Maintain Model-View separation
- Add new methods to `ExpenseTracker` for business logic
- Add UI methods to `ExpenseTrackerUI` for presentation
- Update `test_tracker.py` with new test cases
- Document new methods with comprehensive docstrings

**For API:**
- Add models to `models.py` (SQLAlchemy)
- Add schemas to `schemas.py` (Pydantic)
- Add endpoints to `api_main.py` following REST conventions
- Update `auth.py` for new authentication requirements
- Add tests to `test_api.py` covering happy path and errors
- Update API documentation strings for OpenAPI

## Database Schema (API Only)

**Users Table:**
- id (Integer, PK)
- email (String, Unique, Indexed)
- username (String, Unique, Indexed)
- hashed_password (String)
- is_active (Boolean)
- created_at (DateTime)
- updated_at (DateTime)

**Expenses Table:**
- id (Integer, PK)
- amount (Float)
- category (String, Indexed)
- description (String)
- date (DateTime, Indexed)
- created_at (DateTime)
- updated_at (DateTime)
- is_deleted (Boolean) - Soft delete flag
- user_id (Integer, FK to Users)

**Relationships:**
- User.expenses: One-to-Many relationship with Expense
- Expense.user: Many-to-One relationship with User

## API Endpoint Reference

### Authentication Endpoints
- `POST /api/v1/auth/register` - Create new user account
- `POST /api/v1/auth/login` - Login and receive JWT tokens
- `GET /api/v1/auth/me` - Get current authenticated user info

### Expense Endpoints
- `POST /api/v1/expenses` - Create new expense
- `GET /api/v1/expenses` - List expenses (paginated, filterable)
- `GET /api/v1/expenses/summary` - Get spending analytics
- `GET /api/v1/expenses/{id}` - Get specific expense
- `PUT /api/v1/expenses/{id}` - Update expense
- `DELETE /api/v1/expenses/{id}` - Soft delete expense

### System Endpoints
- `GET /health` - Health check and version info

**Query Parameters for Listing:**
- `page`, `page_size` - Pagination controls
- `category` - Filter by expense category
- `from_date`, `to_date` - Date range filtering (YYYY-MM-DD)
- `min_amount`, `max_amount` - Amount range filtering
- `sort_by` - Sort field (date, amount, category)
- `sort_order` - Sort direction (asc, desc)

## Context and Memory Management

The **Resources/** directory contains guides on Claude Code's memory system:

- **6.1 Context Preservation.md** - How context is maintained across sessions
- **6.2 A Deep Dive into Code Memory.md** - Memory architecture and patterns
- **6.3 Memory Access Commands.md** - Quick memory management commands

**Key Memory Commands:**
- `#` (hash) - Add temporary session-specific context (e.g., `# use camelCase for all Python files`)
- `/memory` - View currently loaded memory (project and user memory)

Memory guidance applies when working in this repository - follow the camelCase convention established in session context.

## Recent Development Focus

Based on recent commits, the project is currently focused on:

1. **Hooks system** - Automated workflows with PreToolUse/PostToolUse hooks for formatting, logging, and validation
2. **Advanced workflow patterns** - Multi-agent systems with slash commands
3. **Security hardening** - Fixing vulnerabilities in expense tracker API
4. **Development mode configuration** - Proper environment setup
5. **Documentation** - Comprehensive guides and examples

When contributing, align with these themes and maintain the educational focus.

## MCP Server Integration

The repository includes MCP (Model Context Protocol) server configuration in `.mcp.json`:

**Enabled Servers:**

1. **MCP US Weather Server** - Provides weather forecast and alert tools
   - **Configuration**: Node.js server running from local build
   - **Tools:**
     - `mcp__weather__get-forecast(latitude, longitude)` - Get weather forecast for coordinates
     - `mcp__weather__get-alerts(state)` - Get weather alerts for US states (2-letter code)

2. **Puppeteer MCP Server** - Provides headless browser automation capabilities
   - **Configuration**: `npx -y @modelcontextprotocol/server-puppeteer`
   - **Capabilities:**
     - Take screenshots of web pages
     - Navigate to URLs and interact with pages
     - Click elements and fill forms
     - Extract page content and DOM elements
     - Execute JavaScript in browser context
     - Full headless Chrome/Chromium control
   - **Common Use Cases:**
     - Web scraping and data extraction
     - Automated testing and quality assurance
     - Screenshot generation for documentation
     - Form submission and workflow automation
     - Dynamic content rendering and capture

3. **Sequential Thinking MCP Server** - Provides structured, step-by-step reasoning capabilities
   - **Configuration**: `npx -y @modelcontextprotocol/server-sequential-thinking`
   - **Tool:** `sequential_thinking` - Facilitates detailed thinking process for problem-solving
   - **Capabilities:**
     - Break complex problems into manageable steps
     - Revise and refine thoughts as understanding deepens
     - Branch into alternative reasoning paths
     - Track thought progression with indexing
     - Support iterative refinement and hypothesis validation
   - **Parameters:**
     - `thought` (string) - Current thinking step content
     - `nextThoughtNeeded` (boolean) - Whether another step is needed
     - `thoughtNumber` (integer) - Current thought index
     - `totalThoughts` (integer) - Estimated total steps needed
     - `isRevision` (boolean) - Marks thought as revision
     - `revisesThought` (integer) - Which thought is being revised
     - `branchFromThought` (integer) - Branching point for alternative paths
     - `branchId` (string) - Identifier for reasoning branch
   - **Common Use Cases:**
     - Complex problem decomposition and analysis
     - Planning with room for course correction
     - Exploratory reasoning with multiple approaches
     - Maintaining context over multi-step reasoning
     - Debugging and root cause analysis
   - **Optional Configuration:**
     - `DISABLE_THOUGHT_LOGGING=true` - Disable logging of thought information

**Usage Examples:**
```python
# Weather tools
mcp__weather__get-forecast(latitude=40.7128, longitude=-74.0060)  # NYC forecast
mcp__weather__get-alerts(state="NY")  # New York weather alerts

# Puppeteer tools (exact tool names depend on server implementation)
# Navigate to a page and take screenshot
# Fill forms and click buttons
# Extract data from rendered pages

# Sequential thinking tool - structured problem-solving
# Example: Breaking down a complex architectural decision
sequential_thinking({
    "thought": "Need to choose between monolithic vs microservices architecture",
    "thoughtNumber": 1,
    "totalThoughts": 5,
    "nextThoughtNeeded": True
})

# Example: Revising a previous thought with new information
sequential_thinking({
    "thought": "Actually, given the team size of 3, microservices adds unnecessary complexity",
    "thoughtNumber": 3,
    "totalThoughts": 5,
    "isRevision": True,
    "revisesThought": 2,
    "nextThoughtNeeded": True
})

# Example: Exploring an alternative approach
sequential_thinking({
    "thought": "Alternative: Start with modular monolith for easier refactoring later",
    "thoughtNumber": 4,
    "totalThoughts": 6,
    "branchFromThought": 2,
    "branchId": "alternative-architecture",
    "nextThoughtNeeded": True
})
```

**Adding New MCP Servers:**
1. Use `claude mcp add <server-name> "<command>" --scope project`
2. Update this documentation section with server details
3. Restart Claude Code to load the new server
4. Test the server tools to verify functionality

When adding new MCP servers, update `.mcp.json` and document their tools in this section.

## Project Goals and Philosophy

This repository demonstrates:

1. **Progressive Learning** - From basics (README-1.x) to advanced patterns (README-5)
2. **Practical Examples** - Working code (expense-tracker) not just theory
3. **Extensibility** - Custom agents and commands show Claude Code's flexibility
4. **Best Practices** - Security, testing, documentation, architecture patterns
5. **Real-World Applications** - Travel planning examples show practical use cases

When making changes, maintain this educational focus and ensure code serves as a teaching example.
