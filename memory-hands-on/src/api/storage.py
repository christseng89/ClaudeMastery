"""
JSON storage service for transactions.

Follows API-specific conventions from src/CLAUDE.md:
- Use Python logging module
- Single quotes for dictionary keys
- Async operations where beneficial
"""

import json
import logging
from pathlib import Path
from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class TransactionStorage:
    """Handles JSON file storage for transactions."""

    def __init__(self, data_file: str = 'api_transactions.json'):
        """
        Initialize storage with data file path.

        Args:
            data_file: Path to JSON storage file
        """
        self.data_file = Path(data_file)
        self._next_id = 1
        self._load_transactions()
        logger.info('Transaction storage initialized', extra={'data_file': str(self.data_file)})

    def _load_transactions(self) -> None:
        """Load transactions from JSON file."""
        if not self.data_file.exists():
            logger.info('Data file does not exist, starting with empty storage')
            self._transactions = []
            return

        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self._transactions = data

                # Calculate next ID
                if self._transactions:
                    # Handle transactions that might not have 'id' field (backward compatibility)
                    existing_ids = [txn.get('id', 0) for txn in self._transactions if 'id' in txn]
                    if existing_ids:
                        max_id = max(existing_ids)
                        self._next_id = max_id + 1
                    else:
                        # No transactions have IDs, start fresh
                        self._transactions = []

                logger.info('Transactions loaded successfully', extra={
                    'transaction_count': len(self._transactions),
                    'next_id': self._next_id
                })
        except (json.JSONDecodeError, IOError) as error:
            logger.error('Failed to load transactions, starting fresh', extra={
                'error': str(error),
                'error_type': type(error).__name__
            })
            self._transactions = []

    def _save_transactions(self) -> None:
        """Save transactions to JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(self._transactions, file, indent=2, ensure_ascii=False)

            logger.info('Transactions saved successfully', extra={
                'transaction_count': len(self._transactions)
            })
        except IOError as error:
            logger.error('Failed to save transactions', extra={
                'error': str(error),
                'error_type': type(error).__name__
            })
            raise

    def add_transaction(
        self,
        amount: Decimal,
        category: str,
        description: str = ''
    ) -> Dict[str, Any]:
        """
        Add a new transaction to storage.

        Args:
            amount: Transaction amount (Decimal for precision)
            category: Transaction category
            description: Optional transaction details

        Returns:
            Dictionary with transaction data including generated ID

        Note:
            Uses single quotes for dictionary keys (API convention)
        """
        transaction_id = self._next_id
        self._next_id += 1

        transaction_data = {
            'id': transaction_id,
            'amount': str(amount),  # Store as string to preserve Decimal precision
            'category': category.strip(),
            'description': description.strip(),
            'date': datetime.now().isoformat()
        }

        self._transactions.append(transaction_data)
        self._save_transactions()

        logger.info('Transaction added', extra={
            'transaction_id': transaction_id,
            'amount': str(amount),
            'category': category
        })

        return transaction_data

    def get_transaction(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """
        Get transaction by ID.

        Args:
            transaction_id: Transaction unique identifier

        Returns:
            Transaction dictionary or None if not found
        """
        for transaction in self._transactions:
            if transaction['id'] == transaction_id:
                logger.info('Transaction retrieved', extra={'transaction_id': transaction_id})
                return transaction

        logger.warning('Transaction not found', extra={'transaction_id': transaction_id})
        return None

    def get_all_transactions(self) -> List[Dict[str, Any]]:
        """
        Get all transactions.

        Returns:
            List of all transaction dictionaries
        """
        logger.info('Retrieving all transactions', extra={
            'transaction_count': len(self._transactions)
        })
        return self._transactions.copy()

    def delete_transaction(self, transaction_id: int) -> bool:
        """
        Delete transaction by ID.

        Args:
            transaction_id: Transaction unique identifier

        Returns:
            True if deleted, False if not found
        """
        for index, transaction in enumerate(self._transactions):
            if transaction['id'] == transaction_id:
                self._transactions.pop(index)
                self._save_transactions()

                logger.info('Transaction deleted', extra={'transaction_id': transaction_id})
                return True

        logger.warning('Transaction not found for deletion', extra={'transaction_id': transaction_id})
        return False

    def get_transaction_count(self) -> int:
        """
        Get total count of transactions.

        Returns:
            Number of transactions in storage
        """
        return len(self._transactions)
