"""
Comprehensive API test suite using FastAPI TestClient.

This test file demonstrates the API functionality and serves as
automated testing for all endpoints.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


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
    """Run all test functions."""
    print('\n' + '=' * 60)
    print('PERSONAL FINANCE TRACKER API - TEST SUITE')
    print('=' * 60)

    try:
        # Basic endpoints
        test_health_check()
        test_root_endpoint()

        # Create transactions
        txn_id_1 = test_create_transaction()
        txn_id_2 = test_create_transaction_without_description()

        # Validation errors
        test_create_transaction_invalid_amount()
        test_create_transaction_empty_category()

        # List and get
        test_list_transactions()
        test_get_transaction(txn_id_1)
        test_get_nonexistent_transaction()

        # Delete
        test_delete_transaction(txn_id_2)
        test_delete_nonexistent_transaction()

        # Final summary
        print('\n' + '=' * 60)
        print('ALL TESTS PASSED! ✓')
        print('=' * 60)
        print('\nThe Personal Finance Tracker API is working correctly.')
        print('All endpoints tested successfully.')

    except AssertionError as error:
        print(f'\n✗ TEST FAILED: {error}')
        raise
    except Exception as error:
        print(f'\n✗ UNEXPECTED ERROR: {error}')
        raise


if __name__ == '__main__':
    run_all_tests()
