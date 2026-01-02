#!/usr/bin/env python3
"""
Simple Expense Tracker Application
Allows users to track expenses with amount, category, and description.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

# Constants
DEFAULT_DATA_FILE = 'expenses.json'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
TABLE_WIDTH = 80
CATEGORY_WIDTH = 40
JSON_INDENT = 2


@dataclass
class CategorySummary:
    """Summary of spending for a specific category."""
    name: str
    total: float
    percentage: float


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class Expense:
    """
    Represents a single expense entry.

    Attributes:
        id (int): Unique identifier for the expense
        amount (float): Expense amount
        category (str): Expense category
        description (str): Expense description
        date (str): Timestamp when expense was recorded
    """

    def __init__(self, expense_id: int, amount: float, category: str,
                 description: str, date: Optional[str] = None):
        """
        Initialize an Expense object.

        Args:
            expense_id: Unique identifier for the expense
            amount: Expense amount (must be positive)
            category: Expense category (cannot be empty)
            description: Expense description
            date: Timestamp (defaults to current time if not provided)

        Raises:
            ValidationError: If amount or category are invalid
        """
        self.id = expense_id
        self.amount = self._validate_amount(amount)
        self.category = self._validate_category(category)
        self.description = description
        self.date = date or datetime.now().strftime(DATE_FORMAT)

    @staticmethod
    def _validate_amount(amount: float) -> float:
        """Validate that amount is positive."""
        if amount <= 0:
            raise ValidationError("Amount must be greater than 0")
        return amount

    @staticmethod
    def _validate_category(category: str) -> str:
        """Validate that category is not empty."""
        if not category or not category.strip():
            raise ValidationError("Category cannot be empty")
        return category.strip()

    def to_dict(self) -> Dict:
        """Convert expense to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Expense':
        """Create an Expense object from a dictionary."""
        return cls(
            expense_id=data['id'],
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            date=data['date']
        )


class ExpenseTracker:
    """
    A class to manage personal expense tracking with persistent storage.

    This class provides methods to add, view, and analyze expenses stored
    in a JSON file. Each expense includes an amount, category, description,
    and automatic timestamp.

    Attributes:
        data_file (str): Path to the JSON file storing expense data
        expenses (List[Expense]): List of Expense objects loaded from file
    """

    def __init__(self, data_file: str = DEFAULT_DATA_FILE):
        """
        Initialize the ExpenseTracker with a data file.

        Args:
            data_file: Path to JSON file for storing expenses
        """
        self.data_file = data_file
        self.expenses: List[Expense] = self._load_expenses()

    def _load_expenses(self) -> List[Expense]:
        """
        Load expenses from JSON file.

        Returns:
            List of Expense objects loaded from file, or empty list if file
            doesn't exist or is corrupted
        """
        if not os.path.exists(self.data_file):
            return []

        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return [Expense.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Warning: Could not read {self.data_file}. Starting fresh.")
            return []

    def _save_expenses(self) -> None:
        """Save expenses to JSON file."""
        with open(self.data_file, 'w') as f:
            data = [expense.to_dict() for expense in self.expenses]
            json.dump(data, f, indent=JSON_INDENT)

    def _generate_next_id(self) -> int:
        """
        Generate the next available expense ID.

        Returns:
            Next available ID (handles gaps from deletions)
        """
        if not self.expenses:
            return 1
        return max(expense.id for expense in self.expenses) + 1

    def add_expense(self, amount: float, category: str, description: str) -> Expense:
        """
        Add a new expense to the tracker.

        Args:
            amount: Expense amount
            category: Expense category
            description: Expense description

        Returns:
            The created Expense object

        Raises:
            ValidationError: If amount or category are invalid
        """
        expense = Expense(
            expense_id=self._generate_next_id(),
            amount=amount,
            category=category,
            description=description
        )
        self.expenses.append(expense)
        self._save_expenses()
        return expense

    def get_all_expenses(self) -> List[Expense]:
        """
        Get all expenses.

        Returns:
            List of all Expense objects
        """
        return self.expenses.copy()

    def calculate_total(self) -> float:
        """
        Calculate total spending across all expenses.

        Returns:
            Total amount spent
        """
        return sum(expense.amount for expense in self.expenses)

    def get_category_breakdown(self) -> List[CategorySummary]:
        """
        Calculate spending breakdown by category.

        Returns:
            List of CategorySummary objects sorted by amount (descending)
        """
        if not self.expenses:
            return []

        category_totals: Dict[str, float] = {}
        for expense in self.expenses:
            category_totals[expense.category] = (
                category_totals.get(expense.category, 0) + expense.amount
            )

        total = self.calculate_total()
        summaries = [
            CategorySummary(
                name=category,
                total=amount,
                percentage=(amount / total) * 100 if total > 0 else 0
            )
            for category, amount in category_totals.items()
        ]

        return sorted(summaries, key=lambda x: x.total, reverse=True)


class ExpenseTrackerUI:
    """
    User interface for the Expense Tracker application.

    Handles all user interactions, input/output, and display formatting.
    Separates presentation logic from business logic.
    """

    MENU_WIDTH = 50

    def __init__(self, tracker: ExpenseTracker):
        """
        Initialize the UI with an ExpenseTracker instance.

        Args:
            tracker: ExpenseTracker instance to use for operations
        """
        self.tracker = tracker

    @staticmethod
    def _print_separator(char: str = "=", width: int = TABLE_WIDTH) -> None:
        """Print a separator line."""
        print(char * width)

    @staticmethod
    def _format_currency(amount: float) -> str:
        """Format amount as currency string."""
        return f"${amount:.2f}"

    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "=" * self.MENU_WIDTH)
        print("          EXPENSE TRACKER")
        print("=" * self.MENU_WIDTH)
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Calculate Total Spending")
        print("4. Exit")
        print("=" * self.MENU_WIDTH)

    def get_menu_choice(self) -> str:
        """Get and return user's menu choice."""
        return input("\nEnter your choice (1-4): ").strip()

    def handle_add_expense(self) -> None:
        """Handle the 'Add Expense' user action."""
        try:
            amount = float(input("Enter amount: $"))
            category = input("Enter category (e.g., Food, Transport, Entertainment): ").strip()
            description = input("Enter description: ").strip()

            expense = self.tracker.add_expense(amount, category, description)
            print(f"\nExpense added successfully! (ID: {expense.id})")
            print(f"Data saved to {self.tracker.data_file}")

        except ValueError:
            print("Error: Invalid amount. Please enter a number.")
        except ValidationError as e:
            print(f"Error: {e}")

    def handle_view_expenses(self) -> None:
        """Display all expenses in a formatted table."""
        expenses = self.tracker.get_all_expenses()

        if not expenses:
            print("\nNo expenses recorded yet.")
            return

        print()
        self._print_separator()
        print(f"{'ID':<5} {'Date':<20} {'Category':<15} {'Amount':<10} {'Description':<30}")
        self._print_separator()

        for expense in expenses:
            print(f"{expense.id:<5} "
                  f"{expense.date:<20} "
                  f"{expense.category:<15} "
                  f"{self._format_currency(expense.amount):<10} "
                  f"{expense.description:<30}")

        self._print_separator()

    def handle_calculate_total(self) -> None:
        """Display total spending and category breakdown."""
        if not self.tracker.get_all_expenses():
            print("\nNo expenses to calculate.")
            return

        total = self.tracker.calculate_total()
        print(f"\nTotal Spending: {self._format_currency(total)}")

        summaries = self.tracker.get_category_breakdown()
        if summaries:
            print("\nSpending by Category:")
            self._print_separator("-", CATEGORY_WIDTH)
            for summary in summaries:
                print(f"{summary.name:<20} "
                      f"{self._format_currency(summary.total):>10} "
                      f"({summary.percentage:>5.1f}%)")
            self._print_separator("-", CATEGORY_WIDTH)

    def run(self) -> None:
        """
        Run the main application loop.

        Displays menu and handles user choices until exit is selected.
        """
        while True:
            self.display_menu()
            choice = self.get_menu_choice()

            if choice == '1':
                self.handle_add_expense()
            elif choice == '2':
                self.handle_view_expenses()
            elif choice == '3':
                self.handle_calculate_total()
            elif choice == '4':
                print("\nThank you for using Expense Tracker!")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 4.")


def main():
    """
    Main entry point for the interactive expense tracker application.

    Creates an ExpenseTracker instance and launches the UI.
    """
    tracker = ExpenseTracker()
    ui = ExpenseTrackerUI(tracker)
    ui.run()


if __name__ == "__main__":
    main()
