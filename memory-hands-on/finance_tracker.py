#!/usr/bin/env python3
"""
Personal Finance Tracker CLI
A command-line application for tracking personal financial transactions.
"""

import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional

import click


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


class FinanceTracker:
    """Manages personal finance transactions with persistent storage."""

    def __init__(self, data_file: str = "transactions.json") -> None:
        """
        Initialize the finance tracker.

        Args:
            data_file: Path to JSON file for storing transactions
        """
        self.data_file = Path(data_file)
        self.transactions = self._load_transactions()

    def _load_transactions(self) -> List[Dict]:
        """
        Load transactions from JSON file.

        Returns:
            List of transaction dictionaries
        """
        if self.data_file.exists():
            try:
                with self.data_file.open("r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_transactions(self) -> None:
        """Save transactions to JSON file."""
        with self.data_file.open("w") as f:
            json.dump(self.transactions, f, indent=2)

    def _validate_amount(self, amount: Decimal) -> None:
        """
        Validate transaction amount.

        Args:
            amount: Amount to validate

        Raises:
            ValidationError: If amount is invalid
        """
        if not isinstance(amount, Decimal):
            raise ValidationError("Amount must be a Decimal")
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
        self, amount: Decimal, category: str, description: Optional[str] = None
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
            "amount": str(amount),  # Store as string to preserve precision
            "category": category.strip(),
            "description": description.strip() if description else "",
            "date": datetime.now().isoformat(),
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
        amount = Decimal(transaction["amount"])
        click.echo("\n" + "=" * 50)
        click.echo("Transaction Added Successfully!")
        click.echo("=" * 50)
        click.echo(f"Amount:      ${amount:.2f}")
        click.echo(f"Category:    {transaction['category']}")
        if transaction["description"]:
            click.echo(f"Description: {transaction['description']}")
        click.echo(f"Date:        {transaction['date']}")
        click.echo("=" * 50 + "\n")


@click.group()
def cli() -> None:
    """Personal Finance Tracker CLI - Track your financial transactions."""
    pass


@cli.command()
@click.option(
    "--amount",
    type=str,
    required=True,
    help="The transaction amount (e.g., 25.50)",
)
@click.option(
    "--category",
    type=str,
    required=True,
    help="The transaction category (e.g., groceries, utilities, entertainment)",
)
@click.option(
    "--description",
    type=str,
    required=False,
    help="Additional details about the transaction",
)
def add(amount: str, category: str, description: Optional[str]) -> None:
    """Add a new financial transaction."""
    tracker = FinanceTracker()

    try:
        # Convert string amount to Decimal
        decimal_amount = Decimal(amount)
        transaction = tracker.add_transaction(
            amount=decimal_amount, category=category, description=description
        )
        tracker.display_transaction(transaction)
    except ValidationError as e:
        click.echo(f"\nValidation Error: {e}\n", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"\nError adding transaction: {e}\n", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
