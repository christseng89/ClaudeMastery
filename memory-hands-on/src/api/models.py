"""
Domain models for transaction business logic.

Separates business logic from API schemas and storage implementation.
Follows conventions from src/CLAUDE.md:
- Use Decimal for financial calculations (user preference)
- CamelCase for internal variables
- Comprehensive docstrings and type hints
"""

from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Dict, Any, Optional


class ValidationError(Exception):
    """Custom exception for transaction validation errors."""
    pass


class Transaction:
    """
    Transaction domain model with business logic and validation.

    This class represents a financial transaction with amount, category,
    description, and timestamp. It handles validation and provides methods
    for serialization/deserialization.

    Attributes:
        id: Transaction unique identifier (None for new transactions)
        amount: Transaction amount as Decimal for precision
        category: Transaction category (cannot be empty)
        description: Optional transaction details
        date: Transaction timestamp (auto-generated if not provided)
    """

    def __init__(
        self,
        amount: Decimal,
        category: str,
        description: str = '',
        transaction_id: Optional[int] = None,
        date: Optional[datetime] = None
    ):
        """
        Initialize a Transaction instance.

        Args:
            amount: Transaction amount (must be positive Decimal)
            category: Transaction category (cannot be empty)
            description: Optional transaction details
            transaction_id: Unique identifier (None for new transactions)
            date: Transaction timestamp (auto-generated if None)

        Raises:
            ValidationError: If amount or category validation fails
        """
        self.id = transaction_id
        self.amount = self._validateAmount(amount)
        self.category = self._validateCategory(category)
        self.description = description.strip() if description else ''
        self.date = date if date else datetime.now()

    def _validateAmount(self, amount: Decimal) -> Decimal:
        """
        Validate transaction amount.

        Args:
            amount: Amount to validate

        Returns:
            Validated Decimal amount

        Raises:
            ValidationError: If amount is not positive
        """
        if not isinstance(amount, Decimal):
            try:
                amount = Decimal(str(amount))
            except (InvalidOperation, ValueError, TypeError):
                raise ValidationError('Amount must be a valid number')

        if amount <= 0:
            raise ValidationError('Amount must be greater than zero')

        return amount

    def _validateCategory(self, category: str) -> str:
        """
        Validate transaction category.

        Args:
            category: Category to validate

        Returns:
            Validated and stripped category string

        Raises:
            ValidationError: If category is empty or whitespace
        """
        if not isinstance(category, str):
            raise ValidationError('Category must be a string')

        strippedCategory = category.strip()
        if not strippedCategory:
            raise ValidationError('Category cannot be empty or whitespace')

        return strippedCategory

    def toDict(self) -> Dict[str, Any]:
        """
        Convert transaction to dictionary for serialization.

        Returns:
            Dictionary with transaction data using single quotes for keys
            (API convention from src/CLAUDE.md)
        """
        return {
            'id': self.id,
            'amount': str(self.amount),  # Store as string to preserve precision
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat()
        }

    @classmethod
    def fromDict(cls, data: Dict[str, Any]) -> 'Transaction':
        """
        Create Transaction instance from dictionary.

        Args:
            data: Dictionary with transaction data

        Returns:
            Transaction instance

        Raises:
            ValidationError: If data is invalid or missing required fields
        """
        try:
            amount = Decimal(data['amount'])
            category = data['category']
            description = data.get('description', '')
            transactionId = data.get('id')

            # Parse ISO format date string
            dateStr = data.get('date')
            date = datetime.fromisoformat(dateStr) if dateStr else None

            return cls(
                amount=amount,
                category=category,
                description=description,
                transaction_id=transactionId,
                date=date
            )
        except KeyError as error:
            raise ValidationError(f'Missing required field: {error}')
        except (InvalidOperation, ValueError) as error:
            raise ValidationError(f'Invalid data format: {error}')

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f'Transaction(id={self.id}, amount={self.amount}, '
            f'category={self.category!r}, date={self.date.isoformat()})'
        )

    def __eq__(self, other: Any) -> bool:
        """
        Compare transactions for equality.

        Args:
            other: Another object to compare with

        Returns:
            True if transactions have same id and data
        """
        if not isinstance(other, Transaction):
            return False

        return (
            self.id == other.id and
            self.amount == other.amount and
            self.category == other.category and
            self.description == other.description
        )
