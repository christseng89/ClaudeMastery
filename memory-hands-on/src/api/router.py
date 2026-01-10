"""
Transaction API router.

Follows API-specific conventions from src/CLAUDE.md:
- All route handlers are async
- Use FastAPI HTTPException
- Return Pydantic models (not raw dicts)
- Include operation summaries and response models
"""

import logging
from decimal import Decimal, InvalidOperation
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from .schemas import TransactionCreate, TransactionResponse, TransactionListResponse
from .storage import TransactionStorage

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/api/v1/transactions', tags=['transactions'])


def get_storage() -> TransactionStorage:
    """
    Dependency to get storage instance.

    Returns:
        TransactionStorage instance
    """
    if not hasattr(get_storage, 'storage'):
        get_storage.storage = TransactionStorage()
    return get_storage.storage


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionResponse,
    summary='Create new transaction',
    description='Add a new financial transaction with amount, category, and optional description'
)
async def create_transaction(
    transaction: TransactionCreate,
    storage: TransactionStorage = Depends(get_storage)
) -> TransactionResponse:
    """
    Create new transaction.

    Args:
        transaction: Transaction data (amount, category, description)
        storage: Storage service dependency

    Returns:
        Created transaction with generated ID and timestamp

    Raises:
        HTTPException: 400 if validation fails
    """
    try:
        # Add transaction to storage
        transaction_data = storage.add_transaction(
            amount=transaction.amount,
            category=transaction.category,
            description=transaction.description
        )

        # Convert to response model
        response = TransactionResponse(
            id=transaction_data['id'],
            amount=Decimal(transaction_data['amount']),
            category=transaction_data['category'],
            description=transaction_data['description'],
            date=transaction_data['date']
        )

        logger.info('Transaction created via API', extra={
            'transaction_id': response.id,
            'amount': str(response.amount),
            'category': response.category
        })

        return response

    except ValueError as error:
        logger.warning('Transaction validation failed', extra={'error': str(error)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.get(
    '/',
    response_model=TransactionListResponse,
    summary='List all transactions',
    description='Retrieve all financial transactions with count'
)
async def list_transactions(
    storage: TransactionStorage = Depends(get_storage)
) -> TransactionListResponse:
    """
    List all transactions.

    Args:
        storage: Storage service dependency

    Returns:
        List of all transactions with total count
    """
    transactions_data = storage.get_all_transactions()

    # Convert to response models
    transactions = [
        TransactionResponse(
            id=txn['id'],
            amount=Decimal(txn['amount']),
            category=txn['category'],
            description=txn['description'],
            date=txn['date']
        )
        for txn in transactions_data
    ]

    response = TransactionListResponse(
        transactions=transactions,
        total_count=storage.get_transaction_count()
    )

    logger.info('Transactions listed via API', extra={
        'transaction_count': response.total_count
    })

    return response


@router.get(
    '/{transaction_id}',
    response_model=TransactionResponse,
    summary='Get transaction by ID',
    description='Retrieve a specific transaction by its unique identifier'
)
async def get_transaction(
    transaction_id: int,
    storage: TransactionStorage = Depends(get_storage)
) -> TransactionResponse:
    """
    Get transaction by ID.

    Args:
        transaction_id: Transaction unique identifier
        storage: Storage service dependency

    Returns:
        Transaction data

    Raises:
        HTTPException: 404 if transaction not found
    """
    transaction_data = storage.get_transaction(transaction_id)

    if transaction_data is None:
        logger.warning('Transaction not found via API', extra={'transaction_id': transaction_id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Transaction {transaction_id} not found'
        )

    response = TransactionResponse(
        id=transaction_data['id'],
        amount=Decimal(transaction_data['amount']),
        category=transaction_data['category'],
        description=transaction_data['description'],
        date=transaction_data['date']
    )

    logger.info('Transaction retrieved via API', extra={'transaction_id': transaction_id})

    return response


@router.delete(
    '/{transaction_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete transaction',
    description='Remove a transaction by its unique identifier'
)
async def delete_transaction(
    transaction_id: int,
    storage: TransactionStorage = Depends(get_storage)
) -> None:
    """
    Delete transaction by ID.

    Args:
        transaction_id: Transaction unique identifier
        storage: Storage service dependency

    Returns:
        No content on success

    Raises:
        HTTPException: 404 if transaction not found
    """
    deleted = storage.delete_transaction(transaction_id)

    if not deleted:
        logger.warning('Transaction not found for deletion via API', extra={
            'transaction_id': transaction_id
        })
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Transaction {transaction_id} not found'
        )

    logger.info('Transaction deleted via API', extra={'transaction_id': transaction_id})
