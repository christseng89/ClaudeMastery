#!/usr/bin/env python3
"""
Personal Finance Tracker CLI
A command-line application for tracking personal financial transactions.
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class FinanceTracker:
    """Manages personal finance transactions with persistent storage."""

    def __init__(self, data_file: str = "transactions.json"):
        """
        Initialize the finance tracker.

        Args:
            data_file: Path to JSON file for storing transactions
        """
        self.data_file = data_file
        self.transactions = self._load_transactions()

    def _load_transactions(self) -> List[Dict]:
        """
        Load transactions from JSON file.

        Returns:
            List of transaction dictionaries
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_transactions(self) -> None:
        """Save transactions to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.transactions, f, indent=2)

    def _validate_amount(self, amount: float) -> None:
        """
        Validate transaction amount.

        Args:
            amount: Amount to validate

        Raises:
            ValidationError: If amount is invalid
        """
        if not isinstance(amount, (int, float)):
            raise ValidationError("Amount must be a number")
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero")

    def _validate_category(self, category: str) -> None:
        """
        Validate transaction category.

        Args:
            category: Category to validate

        Raises:
            ValidationError: If category is invalid
        """
        if not category or not category.strip():
            raise ValidationError("Category cannot be empty")

    def add_transaction(
        self,
        amount: float,
        category: str,
        description: Optional[str] = None
    ) -> Dict:
        """
        Add a new financial transaction.

        Args:
            amount: The transaction amount
            category: The transaction category
            description: Optional additional details

        Returns:
            The created transaction dictionary

        Raises:
            ValidationError: If inputs are invalid
        """
        # Validate inputs
        self._validate_amount(amount)
        self._validate_category(category)

        transaction = {
            "amount": amount,
            "category": category.strip(),
            "description": description.strip() if description else "",
            "date": datetime.now().isoformat()
        }

        self.transactions.append(transaction)
        self._save_transactions()

        return transaction

    def display_transaction(self, transaction: Dict) -> None:
        """
        Display a transaction to the user.

        Args:
            transaction: Transaction dictionary to display
        """
        print("\n" + "=" * 50)
        print("Transaction Added Successfully!")
        print("=" * 50)
        print(f"Amount:      ${transaction['amount']:.2f}")
        print(f"Category:    {transaction['category']}")
        if transaction['description']:
            print(f"Description: {transaction['description']}")
        print(f"Date:        {transaction['date']}")
        print("=" * 50 + "\n")


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Personal Finance Tracker CLI - Track your financial transactions",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser(
        'add',
        help='Add a new financial transaction'
    )
    add_parser.add_argument(
        '--amount',
        type=float,
        required=True,
        help='The transaction amount (e.g., 25.50)'
    )
    add_parser.add_argument(
        '--category',
        type=str,
        required=True,
        help='The transaction category (e.g., groceries, utilities, entertainment)'
    )
    add_parser.add_argument(
        '--description',
        type=str,
        required=False,
        help='Additional details about the transaction'
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    tracker = FinanceTracker()

    if args.command == 'add':
        try:
            transaction = tracker.add_transaction(
                amount=args.amount,
                category=args.category,
                description=args.description
            )
            tracker.display_transaction(transaction)
        except ValidationError as e:
            print(f"\nValidation Error: {e}\n")
            return
        except Exception as e:
            print(f"\nError adding transaction: {e}\n")
            return


if __name__ == "__main__":
    main()
