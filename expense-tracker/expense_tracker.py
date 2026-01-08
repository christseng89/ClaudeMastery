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

    def __init__(self, expenseId: int, amount: float, category: str,
                 description: str, date: Optional[str] = None):
        """
        Initialize an Expense object.

        Args:
            expenseId: Unique identifier for the expense
            amount: Expense amount (must be positive)
            category: Expense category (cannot be empty)
            description: Expense description
            date: Timestamp (defaults to current time if not provided)

        Raises:
            ValidationError: If amount or category are invalid
        """
        self.id = expenseId
        self.amount = self._validateAmount(amount)
        self.category = self._validateCategory(category)
        self.description = description
        self.date = date or datetime.now().strftime(DATE_FORMAT)

    @staticmethod
    def _validateAmount(amount: float) -> float:
        """Validate that amount is positive."""
        if amount <= 0:
            raise ValidationError("Amount must be greater than 0")
        return amount

    @staticmethod
    def _validateCategory(category: str) -> str:
        """Validate that category is not empty."""
        if not category or not category.strip():
            raise ValidationError("Category cannot be empty")
        return category.strip()

    def toDict(self) -> Dict[str, any]:
        """Convert expense to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date
        }

    @classmethod
    def fromDict(cls, data: Dict[str, any]) -> 'Expense':
        """Create an Expense object from a dictionary."""
        return cls(
            expenseId=data['id'],
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
        dataFile (str): Path to the JSON file storing expense data
        expenses (List[Expense]): List of Expense objects loaded from file
    """

    def __init__(self, dataFile: str = DEFAULT_DATA_FILE):
        """
        Initialize the ExpenseTracker with a data file.

        Args:
            dataFile: Path to JSON file for storing expenses
        """
        self.dataFile = dataFile
        self.expenses: List[Expense] = self._loadExpenses()

    def _loadExpenses(self) -> List[Expense]:
        """
        Load expenses from JSON file.

        Returns:
            List of Expense objects loaded from file, or empty list if file
            doesn't exist or is corrupted
        """
        if not os.path.exists(self.dataFile):
            return []

        try:
            with open(self.dataFile, 'r') as f:
                data = json.load(f)
                return [Expense.fromDict(item) for item in data]
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Warning: Could not read {self.dataFile}. Starting fresh.")
            return []

    def _saveExpenses(self) -> None:
        """Save expenses to JSON file."""
        with open(self.dataFile, 'w') as f:
            data = [expense.toDict() for expense in self.expenses]
            json.dump(data, f, indent=JSON_INDENT)

    def _generateNextId(self) -> int:
        """
        Generate the next available expense ID.

        Returns:
            Next available ID (handles gaps from deletions)
        """
        if not self.expenses:
            return 1
        return max(expense.id for expense in self.expenses) + 1

    def addExpense(self, amount: float, category: str, description: str) -> Expense:
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
            expenseId=self._generateNextId(),
            amount=amount,
            category=category,
            description=description
        )
        self.expenses.append(expense)
        self._saveExpenses()
        return expense

    def getAllExpenses(self) -> List[Expense]:
        """
        Get all expenses.

        Returns:
            List of all Expense objects
        """
        return self.expenses.copy()

    def calculateTotal(self) -> float:
        """
        Calculate total spending across all expenses.

        Returns:
            Total amount spent
        """
        return sum(expense.amount for expense in self.expenses)

    def getCategoryBreakdown(self) -> List[CategorySummary]:
        """
        Calculate spending breakdown by category.

        Returns:
            List of CategorySummary objects sorted by amount (descending)
        """
        if not self.expenses:
            return []

        categoryTotals: Dict[str, float] = {}
        for expense in self.expenses:
            categoryTotals[expense.category] = (
                categoryTotals.get(expense.category, 0) + expense.amount
            )

        total = self.calculateTotal()
        summaries = [
            CategorySummary(
                name=category,
                total=amount,
                percentage=(amount / total) * 100 if total > 0 else 0
            )
            for category, amount in categoryTotals.items()
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
    def _printSeparator(char: str = "=", width: int = TABLE_WIDTH) -> None:
        """Print a separator line."""
        print(char * width)

    @staticmethod
    def _formatCurrency(amount: float) -> str:
        """Format amount as currency string."""
        return f"${amount:.2f}"

    def displayMenu(self) -> None:
        """Display the main menu."""
        print("\n" + "=" * self.MENU_WIDTH)
        print("          EXPENSE TRACKER")
        print("=" * self.MENU_WIDTH)
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Calculate Total Spending")
        print("4. Exit")
        print("=" * self.MENU_WIDTH)

    def getMenuChoice(self) -> str:
        """Get and return user's menu choice."""
        return input("\nEnter your choice (1-4): ").strip()

    def handleAddExpense(self) -> None:
        """Handle the 'Add Expense' user action."""
        try:
            amount = float(input("Enter amount: $"))
            category = input("Enter category (e.g., Food, Transport, Entertainment): ").strip()
            description = input("Enter description: ").strip()

            expense = self.tracker.addExpense(amount, category, description)
            print(f"\nExpense added successfully! (ID: {expense.id})")
            print(f"Data saved to {self.tracker.dataFile}")

        except ValueError:
            print("Error: Invalid amount. Please enter a number.")
        except ValidationError as e:
            print(f"Error: {e}")

    def handleViewExpenses(self) -> None:
        """Display all expenses in a formatted table."""
        expenses = self.tracker.getAllExpenses()

        if not expenses:
            print("\nNo expenses recorded yet.")
            return

        print()
        self._printSeparator()
        print(f"{'ID':<5} {'Date':<20} {'Category':<15} {'Amount':<10} {'Description':<30}")
        self._printSeparator()

        for expense in expenses:
            print(f"{expense.id:<5} "
                  f"{expense.date:<20} "
                  f"{expense.category:<15} "
                  f"{self._formatCurrency(expense.amount):<10} "
                  f"{expense.description:<30}")

        self._printSeparator()

    def handleCalculateTotal(self) -> None:
        """Display total spending and category breakdown."""
        if not self.tracker.getAllExpenses():
            print("\nNo expenses to calculate.")
            return

        total = self.tracker.calculateTotal()
        print(f"\nTotal Spending: {self._formatCurrency(total)}")

        summaries = self.tracker.getCategoryBreakdown()
        if summaries:
            print("\nSpending by Category:")
            self._printSeparator("-", CATEGORY_WIDTH)
            for summary in summaries:
                print(f"{summary.name:<20} "
                      f"{self._formatCurrency(summary.total):>10} "
                      f"({summary.percentage:>5.1f}%)")
            self._printSeparator("-", CATEGORY_WIDTH)

    def run(self) -> None:
        """
        Run the main application loop.

        Displays menu and handles user choices until exit is selected.
        """
        while True:
            self.displayMenu()
            choice = self.getMenuChoice()

            if choice == '1':
                self.handleAddExpense()
            elif choice == '2':
                self.handleViewExpenses()
            elif choice == '3':
                self.handleCalculateTotal()
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
