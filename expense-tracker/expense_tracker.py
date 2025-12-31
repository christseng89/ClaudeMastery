#!/usr/bin/env python3
"""
Simple Expense Tracker Application
Allows users to track expenses with amount, category, and description.
"""

import json
import os
from datetime import datetime
from typing import List, Dict


class ExpenseTracker:
    def __init__(self, data_file='expenses.json'):
        self.data_file = data_file
        self.expenses = self.load_expenses()

    def load_expenses(self) -> List[Dict]:
        """Load expenses from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not read {self.data_file}. Starting fresh.")
                return []
        return []

    def save_expenses(self):
        """Save expenses to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.expenses, f, indent=2)
        print(f"Data saved to {self.data_file}")

    def add_expense(self, amount: float, category: str, description: str):
        """Add a new expense."""
        expense = {
            'id': len(self.expenses) + 1,
            'amount': amount,
            'category': category,
            'description': description,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.expenses.append(expense)
        self.save_expenses()
        print(f"\nExpense added successfully! (ID: {expense['id']})")

    def view_expenses(self):
        """Display all expenses."""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return

        print("\n" + "=" * 80)
        print(f"{'ID':<5} {'Date':<20} {'Category':<15} {'Amount':<10} {'Description':<30}")
        print("=" * 80)

        for expense in self.expenses:
            print(f"{expense['id']:<5} "
                  f"{expense['date']:<20} "
                  f"{expense['category']:<15} "
                  f"${expense['amount']:<9.2f} "
                  f"{expense['description']:<30}")

        print("=" * 80)

    def calculate_total(self):
        """Calculate and display total spending."""
        if not self.expenses:
            print("\nNo expenses to calculate.")
            return

        total = sum(expense['amount'] for expense in self.expenses)
        print(f"\nTotal Spending: ${total:.2f}")

        # Also show breakdown by category
        categories = {}
        for expense in self.expenses:
            cat = expense['category']
            categories[cat] = categories.get(cat, 0) + expense['amount']

        if categories:
            print("\nSpending by Category:")
            print("-" * 40)
            for category, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total) * 100
                print(f"{category:<20} ${amount:>10.2f} ({percentage:>5.1f}%)")
            print("-" * 40)


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n" + "=" * 50)
        print("          EXPENSE TRACKER")
        print("=" * 50)
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Calculate Total Spending")
        print("4. Exit")
        print("=" * 50)

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == '1':
            try:
                amount = float(input("Enter amount: $"))
                category = input("Enter category (e.g., Food, Transport, Entertainment): ").strip()
                description = input("Enter description: ").strip()

                if amount <= 0:
                    print("Error: Amount must be greater than 0")
                    continue

                if not category:
                    print("Error: Category cannot be empty")
                    continue

                tracker.add_expense(amount, category, description)
            except ValueError:
                print("Error: Invalid amount. Please enter a number.")

        elif choice == '2':
            tracker.view_expenses()

        elif choice == '3':
            tracker.calculate_total()

        elif choice == '4':
            print("\nThank you for using Expense Tracker!")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
