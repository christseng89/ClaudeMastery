"""
Comprehensive test suite for Transaction models and API endpoints.

This test file includes:
- Unit tests for Transaction model (business logic and validation)
- Integration tests for API endpoints using FastAPI TestClient

Tests follow project conventions:
- Test functions use snake_case (pytest convention)
- Internal variables use camelCase (user preference)
- Decimal for financial amounts
"""

import sys
from pathlib import Path
from decimal import Decimal
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi.testclient import TestClient
from src.api.main import app
from src.api.models import Transaction, ValidationError

client = TestClient(app)


# ============================================================
# UNIT TESTS: Transaction Model
# ============================================================

def test_transaction_creation_success():
    """Test creating a valid Transaction instance."""
    print('\n' + '=' * 60)
    print('MODEL TEST: Transaction Creation (Valid Data)')
    print('=' * 60)

    amount = Decimal('25.50')
    category = 'groceries'
    description = 'Weekly shopping'

    transaction = Transaction(
        amount=amount,
        category=category,
        description=description
    )

    assert transaction.amount == amount
    assert transaction.category == category
    assert transaction.description == description
    assert transaction.id is None  # New transaction has no ID
    assert isinstance(transaction.date, datetime)

    print(f'✓ Transaction created: {transaction}')
    print(f'✓ Amount: {transaction.amount}')
    print(f'✓ Category: {transaction.category}')
    print(f'✓ Date: {transaction.date.isoformat()}')


def test_transaction_creation_with_id():
    """Test creating a Transaction with an ID."""
    print('\n' + '=' * 60)
    print('MODEL TEST: Transaction Creation (With ID)')
    print('=' * 60)

    transactionId = 42
    amount = Decimal('100.00')
    category = 'utilities'
    customDate = datetime(2026, 1, 10, 15, 30, 0)

    transaction = Transaction(
        amount=amount,
        category=category,
        transaction_id=transactionId,
        date=customDate
    )

    assert transaction.id == transactionId
    assert transaction.date == customDate

    print(f'✓ Transaction created with ID: {transaction.id}')
    print(f'✓ Custom date preserved: {transaction.date.isoformat()}')


def test_transaction_validation_negative_amount():
    """Test that negative amounts are rejected."""
    print('\n' + '=' * 60)
    print('MODEL TEST: Validation (Negative Amount)')
    print('=' * 60)

    try:
        transaction = Transaction(
            amount=Decimal('-10.00'),
            category='test'
        )
        assert False, 'Expected ValidationError for negative amount'
    except ValidationError as error:
        assert 'greater than zero' in str(error)
        print(f'✓ Negative amount rejected: {error}')


def test_transaction_validation_zero_amount():
    """Test that zero amount is rejected."""
    print('\n' + '=' * 60)
    print('MODEL TEST: Validation (Zero Amount)')
    print('=' * 60)

    try:
        transaction = Transaction(
            amount=Decimal('0.00'),
            category='test'
        )
        assert False, 'Expected ValidationError for zero amount'
    except ValidationError as error:
        assert 'greater than zero' in str(error)
        print(f'✓ Zero amount rejected: {error}')


def test_transaction_validation_empty_category():
    """Test that empty category is rejected."""
    print('\n' + '=' * 60)
    print('MODEL TEST: Validation (Empty Category)')
    print('=' * 60)

    try:
        transaction = Transaction(
            amount=Decimal('10.00'),
            category=''
        )
        assert False, 'Expected ValidationError for empty category'
    except ValidationError as error:
        assert 'empty' in str(error).lower()
        print(f'✓ Empty category rejected: {error}')


def test_transaction_validation_whitespace_category():
    """Test that whitespace-only category is rejected."""
    print('\n' + '=' * 60)
    print('MODEL TEST: Validation (Whitespace Category)')
    print('=' * 60)

    try:
        transaction = Transaction(
            amount=Decimal('10.00'),
            category='   '
        )
        assert False, 'Expected ValidationError for whitespace category'
    except ValidationError as error:
        assert 'empty' in str(error).lower() or 'whitespace' in str(error).lower()
        print(f'✓ Whitespace category rejected: {error}')


def test_transaction_string_to_decimal_conversion():
    """Test that string amounts are converted to Decimal."""
    print('\n' + '=' * 60)
    print('MODEL TEST: String to Decimal Conversion')
    print('=' * 60)

    transaction = Transaction(
        amount='99.99',  # String instead of Decimal
        category='test'
    )

    assert isinstance(transaction.amount, Decimal)
    assert transaction.amount == Decimal('99.99')

    print(f'✓ String "99.99" converted to Decimal: {transaction.amount}')


def test_transaction_to_dict():
    """Test Transaction serialization to dictionary."""
    print('\n' + '=' * 60)
    print('MODEL TEST: toDict() Serialization')
    print('=' * 60)

    transaction = Transaction(
        amount=Decimal('42.50'),
        category='entertainment',
        description='Movie tickets',
        transaction_id=123,
        date=datetime(2026, 1, 14, 10, 30, 0)
    )

    transactionDict = transaction.toDict()

    assert transactionDict['id'] == 123
    assert transactionDict['amount'] == '42.50'  # Decimal as string
    assert transactionDict['category'] == 'entertainment'
    assert transactionDict['description'] == 'Movie tickets'
    assert transactionDict['date'] == '2026-01-14T10:30:00'  # ISO format

    print(f'✓ Transaction serialized to dict:')
    print(f'  - ID: {transactionDict["id"]}')
    print(f'  - Amount: {transactionDict["amount"]} (string)')
    print(f'  - Category: {transactionDict["category"]}')
    print(f'  - Date: {transactionDict["date"]} (ISO-8601)')


def test_transaction_from_dict():
    """Test Transaction deserialization from dictionary."""
    print('\n' + '=' * 60)
    print('MODEL TEST: fromDict() Deserialization')
    print('=' * 60)

    transactionData = {
        'id': 456,
        'amount': '75.25',
        'category': 'groceries',
        'description': 'Weekly shopping',
        'date': '2026-01-14T15:45:30'
    }

    transaction = Transaction.fromDict(transactionData)

    assert transaction.id == 456
    assert transaction.amount == Decimal('75.25')
    assert transaction.category == 'groceries'
    assert transaction.description == 'Weekly shopping'
    assert transaction.date == datetime(2026, 1, 14, 15, 45, 30)

    print(f'✓ Transaction deserialized from dict:')
    print(f'  - ID: {transaction.id}')
    print(f'  - Amount: {transaction.amount} (Decimal)')
    print(f'  - Category: {transaction.category}')
    print(f'  - Date: {transaction.date.isoformat()}')


def test_transaction_round_trip_serialization():
    """Test that toDict() and fromDict() preserve data."""
    print('\n' + '=' * 60)
    print('MODEL TEST: Round-trip Serialization')
    print('=' * 60)

    original = Transaction(
        amount=Decimal('123.45'),
        category='utilities',
        description='Internet bill',
        transaction_id=789,
        date=datetime(2026, 1, 1, 12, 0, 0)
    )

    # Serialize to dict
    transactionDict = original.toDict()

    # Deserialize back to Transaction
    restored = Transaction.fromDict(transactionDict)

    # Verify data preserved
    assert restored.id == original.id
    assert restored.amount == original.amount
    assert restored.category == original.category
    assert restored.description == original.description
    assert restored.date == original.date

    print(f'✓ Round-trip successful:')
    print(f'  Original:  {original}')
    print(f'  Restored:  {restored}')


def test_transaction_equality():
    """Test Transaction equality comparison."""
    print('\n' + '=' * 60)
    print('MODEL TEST: Equality Comparison')
    print('=' * 60)

    transaction1 = Transaction(
        amount=Decimal('50.00'),
        category='food',
        description='Lunch',
        transaction_id=100
    )

    transaction2 = Transaction(
        amount=Decimal('50.00'),
        category='food',
        description='Lunch',
        transaction_id=100
    )

    transaction3 = Transaction(
        amount=Decimal('50.00'),
        category='food',
        description='Dinner',  # Different description
        transaction_id=100
    )

    assert transaction1 == transaction2
    assert transaction1 != transaction3

    print(f'✓ Transactions with same data are equal')
    print(f'✓ Transactions with different data are not equal')


def test_transaction_large_amount():
    """Test Transaction with large amount."""
    print('\n' + '=' * 60)
    print('MODEL TEST: Large Amount Handling')
    print('=' * 60)

    largeAmount = Decimal('999999999.99')

    transaction = Transaction(
        amount=largeAmount,
        category='investment'
    )

    assert transaction.amount == largeAmount

    print(f'✓ Large amount handled correctly: ${largeAmount}')


def test_transaction_unicode_category():
    """Test Transaction with unicode characters in category."""
    print('\n' + '=' * 60)
    print('MODEL TEST: Unicode Category')
    print('=' * 60)

    unicodeCategory = '食料品'  # Japanese for groceries
    unicodeDescription = 'Café ☕'

    transaction = Transaction(
        amount=Decimal('15.00'),
        category=unicodeCategory,
        description=unicodeDescription
    )

    assert transaction.category == unicodeCategory
    assert transaction.description == unicodeDescription

    print(f'✓ Unicode category: {transaction.category}')
    print(f'✓ Unicode description: {transaction.description}')


def test_transaction_whitespace_trimming():
    """Test that category and description are trimmed."""
    print('\n' + '=' * 60)
    print('MODEL TEST: Whitespace Trimming')
    print('=' * 60)

    transaction = Transaction(
        amount=Decimal('10.00'),
        category='  groceries  ',
        description='  Weekly shopping  '
    )

    assert transaction.category == 'groceries'
    assert transaction.description == 'Weekly shopping'

    print(f'✓ Category trimmed: "{transaction.category}"')
    print(f'✓ Description trimmed: "{transaction.description}"')


# ============================================================
# INTEGRATION TESTS: API Endpoints
# ============================================================

def test_health_check():
    """Test health check endpoint."""
    print('\n' + '=' * 60)
    print('TEST: Health Check')
    print('=' * 60)

    response = client.get('/health')
    assert response.status_code == 200

    data = response.json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'Personal Finance Tracker API'

    print(f'✓ Status: {response.status_code}')
    print(f'✓ Response: {data}')


def test_root_endpoint():
    """Test root endpoint."""
    print('\n' + '=' * 60)
    print('TEST: Root Endpoint')
    print('=' * 60)

    response = client.get('/')
    assert response.status_code == 200

    data = response.json()
    assert 'message' in data
    assert 'endpoints' in data

    print(f'✓ Status: {response.status_code}')
    print(f'✓ Message: {data["message"]}')
    print(f'✓ Endpoints: {data["endpoints"]}')


def test_create_transaction():
    """Test creating a transaction."""
    print('\n' + '=' * 60)
    print('TEST: Create Transaction')
    print('=' * 60)

    transaction_data = {
        'amount': 25.50,
        'category': 'groceries',
        'description': 'Weekly shopping'
    }

    response = client.post('/api/v1/transactions/', json=transaction_data)
    assert response.status_code == 201

    data = response.json()
    assert 'id' in data
    assert data['amount'] == '25.5'  # Decimal as string
    assert data['category'] == 'groceries'
    assert data['description'] == 'Weekly shopping'

    print(f'✓ Status: {response.status_code}')
    print(f'✓ Created transaction: {data}')

    return data['id']


def test_create_transaction_without_description():
    """Test creating a transaction without description."""
    print('\n' + '=' * 60)
    print('TEST: Create Transaction (No Description)')
    print('=' * 60)

    transaction_data = {
        'amount': 100.00,
        'category': 'utilities'
    }

    response = client.post('/api/v1/transactions/', json=transaction_data)
    assert response.status_code == 201

    data = response.json()
    assert data['description'] == ''

    print(f'✓ Status: {response.status_code}')
    print(f'✓ Created transaction: {data}')

    return data['id']


def test_create_transaction_invalid_amount():
    """Test creating a transaction with invalid amount."""
    print('\n' + '=' * 60)
    print('TEST: Create Transaction (Invalid Amount)')
    print('=' * 60)

    transaction_data = {
        'amount': -10.00,
        'category': 'test'
    }

    response = client.post('/api/v1/transactions/', json=transaction_data)
    assert response.status_code == 422  # Validation error

    print(f'✓ Status: {response.status_code} (Expected validation error)')
    print(f'✓ Error response: {response.json()}')


def test_create_transaction_empty_category():
    """Test creating a transaction with empty category."""
    print('\n' + '=' * 60)
    print('TEST: Create Transaction (Empty Category)')
    print('=' * 60)

    transaction_data = {
        'amount': 10.00,
        'category': ''
    }

    response = client.post('/api/v1/transactions/', json=transaction_data)
    assert response.status_code == 422  # Validation error

    print(f'✓ Status: {response.status_code} (Expected validation error)')
    print(f'✓ Error response: {response.json()}')


def test_list_transactions():
    """Test listing all transactions."""
    print('\n' + '=' * 60)
    print('TEST: List Transactions')
    print('=' * 60)

    response = client.get('/api/v1/transactions/')
    assert response.status_code == 200

    data = response.json()
    assert 'transactions' in data
    assert 'total_count' in data
    assert data['total_count'] >= 0

    print(f'✓ Status: {response.status_code}')
    print(f'✓ Total transactions: {data["total_count"]}')
    print(f'✓ Transactions: {data["transactions"]}')


def test_get_transaction(transaction_id):
    """Test getting a specific transaction."""
    print('\n' + '=' * 60)
    print(f'TEST: Get Transaction (ID: {transaction_id})')
    print('=' * 60)

    response = client.get(f'/api/v1/transactions/{transaction_id}')
    assert response.status_code == 200

    data = response.json()
    assert data['id'] == transaction_id

    print(f'✓ Status: {response.status_code}')
    print(f'✓ Transaction: {data}')


def test_get_nonexistent_transaction():
    """Test getting a nonexistent transaction."""
    print('\n' + '=' * 60)
    print('TEST: Get Nonexistent Transaction')
    print('=' * 60)

    response = client.get('/api/v1/transactions/99999')
    assert response.status_code == 404

    print(f'✓ Status: {response.status_code} (Expected not found)')
    print(f'✓ Error: {response.json()}')


def test_delete_transaction(transaction_id):
    """Test deleting a transaction."""
    print('\n' + '=' * 60)
    print(f'TEST: Delete Transaction (ID: {transaction_id})')
    print('=' * 60)

    response = client.delete(f'/api/v1/transactions/{transaction_id}')
    assert response.status_code == 204

    print(f'✓ Status: {response.status_code} (Deleted successfully)')

    # Verify deletion
    response = client.get(f'/api/v1/transactions/{transaction_id}')
    assert response.status_code == 404

    print(f'✓ Verified: Transaction no longer exists')


def test_delete_nonexistent_transaction():
    """Test deleting a nonexistent transaction."""
    print('\n' + '=' * 60)
    print('TEST: Delete Nonexistent Transaction')
    print('=' * 60)

    response = client.delete('/api/v1/transactions/99999')
    assert response.status_code == 404

    print(f'✓ Status: {response.status_code} (Expected not found)')
    print(f'✓ Error: {response.json()}')


def run_all_tests():
    """Run all test functions including model and API tests."""
    print('\n' + '=' * 60)
    print('PERSONAL FINANCE TRACKER - COMPREHENSIVE TEST SUITE')
    print('=' * 60)

    modelTestsPassed = 0
    apiTestsPassed = 0

    try:
        # ============================================================
        # MODEL TESTS: Transaction Business Logic
        # ============================================================
        print('\n' + '=' * 60)
        print('SECTION 1: TRANSACTION MODEL TESTS')
        print('=' * 60)

        # Creation tests
        test_transaction_creation_success()
        modelTestsPassed += 1
        test_transaction_creation_with_id()
        modelTestsPassed += 1

        # Validation tests
        test_transaction_validation_negative_amount()
        modelTestsPassed += 1
        test_transaction_validation_zero_amount()
        modelTestsPassed += 1
        test_transaction_validation_empty_category()
        modelTestsPassed += 1
        test_transaction_validation_whitespace_category()
        modelTestsPassed += 1

        # Data conversion tests
        test_transaction_string_to_decimal_conversion()
        modelTestsPassed += 1

        # Serialization tests
        test_transaction_to_dict()
        modelTestsPassed += 1
        test_transaction_from_dict()
        modelTestsPassed += 1
        test_transaction_round_trip_serialization()
        modelTestsPassed += 1

        # Equality tests
        test_transaction_equality()
        modelTestsPassed += 1

        # Edge case tests
        test_transaction_large_amount()
        modelTestsPassed += 1
        test_transaction_unicode_category()
        modelTestsPassed += 1
        test_transaction_whitespace_trimming()
        modelTestsPassed += 1

        print('\n' + '=' * 60)
        print(f'MODEL TESTS COMPLETE: {modelTestsPassed} tests passed ✓')
        print('=' * 60)

        # ============================================================
        # API TESTS: Integration Testing
        # ============================================================
        print('\n' + '=' * 60)
        print('SECTION 2: API ENDPOINT TESTS')
        print('=' * 60)

        # Basic endpoints
        test_health_check()
        apiTestsPassed += 1
        test_root_endpoint()
        apiTestsPassed += 1

        # Create transactions
        txn_id_1 = test_create_transaction()
        apiTestsPassed += 1
        txn_id_2 = test_create_transaction_without_description()
        apiTestsPassed += 1

        # Validation errors
        test_create_transaction_invalid_amount()
        apiTestsPassed += 1
        test_create_transaction_empty_category()
        apiTestsPassed += 1

        # List and get
        test_list_transactions()
        apiTestsPassed += 1
        test_get_transaction(txn_id_1)
        apiTestsPassed += 1
        test_get_nonexistent_transaction()
        apiTestsPassed += 1

        # Delete
        test_delete_transaction(txn_id_2)
        apiTestsPassed += 1
        test_delete_nonexistent_transaction()
        apiTestsPassed += 1

        print('\n' + '=' * 60)
        print(f'API TESTS COMPLETE: {apiTestsPassed} tests passed ✓')
        print('=' * 60)

        # Final summary
        print('\n' + '=' * 60)
        print('ALL TESTS PASSED! ✓')
        print('=' * 60)
        print(f'\nTest Summary:')
        print(f'  • Model Tests:    {modelTestsPassed} passed')
        print(f'  • API Tests:      {apiTestsPassed} passed')
        print(f'  • Total Tests:    {modelTestsPassed + apiTestsPassed} passed')
        print('\nThe Personal Finance Tracker is working correctly.')
        print('All model business logic and API endpoints tested successfully.')

    except AssertionError as error:
        print(f'\n✗ TEST FAILED: {error}')
        raise
    except Exception as error:
        print(f'\n✗ UNEXPECTED ERROR: {error}')
        raise


if __name__ == '__main__':
    run_all_tests()
