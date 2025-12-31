#!/usr/bin/env python3
"""
Simple test script for Expense Tracker
"""

from expense_tracker import ExpenseTracker
import os

def test_expense_tracker():
    # Use a test file so we don't overwrite actual data
    test_file = 'test_expenses.json'

    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)

    print("Testing Expense Tracker...")
    print("-" * 50)

    # Create tracker instance
    tracker = ExpenseTracker(data_file=test_file)
    print("✓ Tracker initialized")

    # Test adding expenses
    print("\nAdding test expenses...")
    tracker.add_expense(25.50, "Food", "Lunch at restaurant")
    tracker.add_expense(50.00, "Transport", "Gas for car")
    tracker.add_expense(15.75, "Food", "Groceries")
    tracker.add_expense(100.00, "Entertainment", "Concert tickets")
    print("✓ Added 4 expenses")

    # Test viewing expenses
    print("\nViewing all expenses:")
    tracker.view_expenses()

    # Test calculating total
    print("\nCalculating total spending:")
    tracker.calculate_total()

    # Verify data persistence
    print("\n\nTesting data persistence...")
    tracker2 = ExpenseTracker(data_file=test_file)
    print(f"✓ Loaded {len(tracker2.expenses)} expenses from file")

    # Clean up test file
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"✓ Test file cleaned up")

    print("\n" + "=" * 50)
    print("All tests passed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    test_expense_tracker()
