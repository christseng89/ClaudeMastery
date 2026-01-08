# Expense Tracker REST API

A modern, secure RESTful API for tracking personal expenses built with FastAPI, featuring JWT authentication, SQLite database, pagination, filtering, and comprehensive documentation.

## 🚀 Features

### Core Functionality
- ✅ **Complete CRUD Operations** for expenses
- ✅ **JWT Authentication** with access and refresh tokens
- ✅ **User Management** with secure password hashing
- ✅ **SQLite Database** with SQLAlchemy ORM
- ✅ **Soft Deletes** for data recovery and audit trails

### Advanced Features
- 📄 **Pagination** - Efficient handling of large datasets
- 🔍 **Filtering** - By category, date range, and amount
- 📊 **Sorting** - By date, amount, or category
- 📈 **Summary Statistics** - Category breakdown and spending analysis
- 🛡️ **Rate Limiting** - Protection against API abuse
- 🌐 **CORS Support** - Cross-origin resource sharing enabled
- 📝 **Automatic API Documentation** - Swagger UI and ReDoc

### Security
- 🔐 **JWT Token Authentication** with access and refresh token validation
- 🔒 **Password Hashing** with bcrypt
- 🚫 **User Isolation** - Users can only access their own data
- ⚡ **Input Validation** - Pydantic schemas for request validation
- 🛑 **Rate Limiting** - Configurable request limits
- 🔒 **Enforced SECRET_KEY Validation** - Production-ready security
- 🛡️ **SQL Injection Protection** - Explicit field mapping
- ⏱️ **Timing Attack Prevention** - Constant-time authentication
- 🔐 **Token Type Validation** - Prevents token misuse
- 🔒 **HTTPS Enforcement** - Production security middleware

## 📋 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login and get tokens | No |
| GET | `/api/v1/auth/me` | Get current user info | Yes |

### Expenses

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/expenses` | Create new expense | Yes |
| GET | `/api/v1/expenses` | List expenses (paginated) | Yes |
| GET | `/api/v1/expenses/{id}` | Get specific expense | Yes |
| PUT | `/api/v1/expenses/{id}` | Update expense | Yes |
| DELETE | `/api/v1/expenses/{id}` | Delete expense (soft) | Yes |
| GET | `/api/v1/expenses/summary` | Get spending summary | Yes |

### Health Check

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health` | API health status | No |

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Steps

1. **Clone the repository** (or navigate to the project directory)
   ```bash
   cd expense-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment configuration** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the API server**
   ```bash
   python api_main.py
   ```

   Or with uvicorn:
   ```bash
   uvicorn api_main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation where you can test endpoints directly.

## 🔧 Configuration

### Environment Variables

The API uses environment-based configuration for flexibility and security. Create a `.env` file in the project root:

```env
# Application
APP_NAME=Expense Tracker API
VERSION=1.0.0
API_V1_PREFIX=/api/v1

# Database
DATABASE_URL=sqlite:///./expense_tracker.db

# Security
# CRITICAL: In production, SECRET_KEY MUST be at least 32 characters
# Generate a secure key with: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-generated-secret-key-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ENVIRONMENT=development  # Options: development, production

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

### Security Configuration Notes

**SECRET_KEY Requirements:**
- **Development/Testing**: A secure random key is auto-generated if not provided
- **Production**: MUST be explicitly set and at least 32 characters
- **Generation**: Use `python -c "import secrets; print(secrets.token_urlsafe(32))"` to generate a secure key
- **Validation**: Weak or default keys are rejected in production mode

**ENVIRONMENT Variable:**
- Set to `production` to enable strict security validation
- Set to `development` (default) for local testing with relaxed requirements
- Production mode enforces:
  - Mandatory SECRET_KEY configuration
  - Minimum 32-character SECRET_KEY length
  - Rejection of common weak keys
  - HTTPS enforcement via middleware

**Example SECRET_KEY Generation:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Output: xK8dJ9_vLmNpQ2rSt4uVwXyZ0123456789AbCdEfGhIjK
```

## 📝 Usage Examples

### 1. Register a New User

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
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "is_active": true,
  "created_at": "2026-01-07T10:30:00"
}
```

### 2. Login

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

### 3. Create an Expense

```bash
curl -X POST "http://localhost:8000/api/v1/expenses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "amount": 45.50,
    "category": "Food",
    "description": "Dinner at restaurant"
  }'
```

**Response:**
```json
{
  "id": 1,
  "amount": 45.50,
  "category": "Food",
  "description": "Dinner at restaurant",
  "date": "2026-01-07T18:30:00",
  "created_at": "2026-01-07T18:30:00",
  "user_id": 1
}
```

### 4. List Expenses with Filtering

```bash
curl -X GET "http://localhost:8000/api/v1/expenses?page=1&page_size=20&category=Food&from_date=2026-01-01&sort_by=amount&sort_order=desc" \
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
      "description": "Dinner at restaurant",
      "date": "2026-01-07T18:30:00",
      "created_at": "2026-01-07T18:30:00",
      "user_id": 1
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

### 5. Get Expense Summary

```bash
curl -X GET "http://localhost:8000/api/v1/expenses/summary?from_date=2026-01-01&to_date=2026-01-31" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "total_spending": 150.75,
  "total_expenses": 5,
  "categories": [
    {
      "category": "Food",
      "total": 80.50,
      "percentage": 53.4,
      "count": 3
    },
    {
      "category": "Transport",
      "total": 45.25,
      "percentage": 30.0,
      "count": 2
    }
  ],
  "date_range": {
    "from": "2026-01-01",
    "to": "2026-01-31"
  }
}
```

### 6. Update an Expense

```bash
curl -X PUT "http://localhost:8000/api/v1/expenses/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "amount": 50.00,
    "description": "Updated dinner cost"
  }'
```

### 7. Delete an Expense

```bash
curl -X DELETE "http://localhost:8000/api/v1/expenses/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:** 204 No Content

## 🧪 Running Tests

Run the comprehensive test suite:

```bash
# Run all tests
pytest test_api.py -v

# Run with coverage
pytest test_api.py --cov=. --cov-report=html

# Run specific test
pytest test_api.py::test_create_expense_success -v
```

The test suite includes:
- ✅ Authentication tests (register, login, token validation)
- ✅ CRUD operation tests
- ✅ Pagination and filtering tests
- ✅ User isolation tests
- ✅ Error handling tests
- ✅ Validation tests

## 🏗️ Project Structure

```
expense-tracker/
├── api_main.py          # FastAPI application and endpoints
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for validation
├── auth.py              # JWT authentication utilities
├── database.py          # Database configuration
├── config.py            # Application settings
├── requirements.txt     # Python dependencies
├── test_api.py          # Comprehensive API tests
├── .env                 # Environment variables (not in git)
├── .env.example         # Example environment file
├── expense_tracker.db   # SQLite database (auto-created)
└── API_README.md        # This file
```

## 🔒 Security Best Practices

### Recent Security Enhancements (January 2026)

The API has been hardened with the following critical security fixes:

1. **✅ SECRET_KEY Validation**
   - Production environments now require a minimum 32-character SECRET_KEY
   - Common weak keys are rejected automatically
   - Development mode auto-generates secure keys for testing

2. **✅ SQL Injection Prevention**
   - Explicit field mapping replaces dynamic attribute access
   - Sort parameters are validated against a whitelist
   - Prevents malicious field access through query parameters

3. **✅ Timing Attack Protection**
   - Constant-time authentication prevents username enumeration
   - Password verification always takes the same time regardless of user existence
   - Mitigates timing-based security reconnaissance

4. **✅ Token Type Validation**
   - Access and refresh tokens are strictly validated by type
   - Prevents refresh tokens from being used as access tokens
   - Enhanced JWT security with type enforcement

5. **✅ HTTPS Enforcement**
   - Production mode automatically redirects HTTP to HTTPS
   - Prevents token interception over insecure connections
   - Middleware-based enforcement for all routes

### Production Security Checklist

1. **Set ENVIRONMENT=production** in your `.env` file
2. **Generate and set a strong SECRET_KEY** (minimum 32 characters)
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
3. **Use HTTPS** - The API will automatically enforce this in production mode
4. **Set secure CORS origins** - Never use wildcards (`*`) in production
5. **Configure appropriate rate limiting** for your traffic patterns
6. **Regular security updates** - Keep dependencies updated
7. **Use environment variables** - Never commit secrets to version control
8. **Database security** - Use PostgreSQL with SSL in production
9. **Monitor and log** - Implement comprehensive audit logging
10. **Regular backups** - Implement automated backup strategies

## 📊 Query Parameters Reference

### List Expenses Endpoint

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `page` | int | Page number (default: 1) | `page=2` |
| `page_size` | int | Items per page (default: 20, max: 100) | `page_size=50` |
| `category` | string | Filter by category (case-insensitive) | `category=Food` |
| `from_date` | string | Start date (YYYY-MM-DD) | `from_date=2026-01-01` |
| `to_date` | string | End date (YYYY-MM-DD) | `to_date=2026-01-31` |
| `min_amount` | float | Minimum expense amount | `min_amount=10.00` |
| `max_amount` | float | Maximum expense amount | `max_amount=100.00` |
| `sort_by` | string | Sort field (date, amount, category) | `sort_by=amount` |
| `sort_order` | string | Sort order (asc, desc) | `sort_order=desc` |

## 🚀 Production Deployment

### Using Docker (Recommended)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t expense-tracker-api .
docker run -p 8000:8000 expense-tracker-api
```

### Using Gunicorn + Uvicorn

```bash
pip install gunicorn
gunicorn api_main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🐛 Troubleshooting

### Database locked error
- Close any connections to the SQLite database
- Use PostgreSQL for production with concurrent access

### Rate limit exceeded
- Adjust `RATE_LIMIT_PER_MINUTE` in config
- Implement IP whitelisting if needed

### CORS errors
- Add your frontend URL to `CORS_ORIGINS`
- Ensure you're using the correct protocol (http/https)

## 📚 Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM for database operations
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation
- **[python-jose](https://python-jose.readthedocs.io/)** - JWT token handling
- **[passlib](https://passlib.readthedocs.io/)** - Password hashing
- **[SlowAPI](https://github.com/laurentS/slowapi)** - Rate limiting
- **[pytest](https://pytest.org/)** - Testing framework

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues, questions, or contributions, please open an issue in the repository.

---

**Built with ❤️ using FastAPI**
