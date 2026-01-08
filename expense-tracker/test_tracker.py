#!/usr/bin/env python3
"""
Simple test script for Expense Tracker
"""

from expense_tracker import ExpenseTracker, ExpenseTrackerUI, ValidationError
import os


def testExpenseTracker() -> None:
    """
    Test the ExpenseTracker functionality.

    Creates a temporary test file, adds sample expenses, tests viewing
    and calculation features, verifies data persistence, and cleans up
    test files automatically.
    """
    # Use a test file so we don't overwrite actual data
    testFile = 'test_expenses.json'

    # Clean up any existing test file
    if os.path.exists(testFile):
        os.remove(testFile)

    print("Testing Expense Tracker...")
    print("-" * 50)

    # Create tracker instance
    tracker = ExpenseTracker(dataFile=testFile)
    print("✓ Tracker initialized")

    # Test adding expenses
    print("\nAdding test expenses...")
    expense1 = tracker.addExpense(25.50, "Food", "Lunch at restaurant")
    expense2 = tracker.addExpense(50.00, "Transport", "Gas for car")
    expense3 = tracker.addExpense(15.75, "Food", "Groceries")
    expense4 = tracker.addExpense(100.00, "Entertainment", "Concert tickets")
    print("✓ Added 4 expenses")

    # Test expense object
    print("\nTesting Expense object...")
    assert expense1.amount == 25.50
    assert expense1.category == "Food"
    assert expense1.description == "Lunch at restaurant"
    assert expense1.id == 1
    print("✓ Expense object works correctly")

    # Test validation
    print("\nTesting validation...")
    try:
        tracker.addExpense(-10, "Food", "Invalid")
        print("✗ Validation failed - negative amount accepted")
    except ValidationError:
        print("✓ Validation correctly rejects negative amounts")

    try:
        tracker.addExpense(10, "", "Invalid")
        print("✗ Validation failed - empty category accepted")
    except ValidationError:
        print("✓ Validation correctly rejects empty categories")

    # Test viewing expenses through UI
    print("\nViewing all expenses:")
    ui = ExpenseTrackerUI(tracker)
    ui.handleViewExpenses()

    # Test calculating total
    print("\nCalculating total spending:")
    total = tracker.calculateTotal()
    expectedTotal = 25.50 + 50.00 + 15.75 + 100.00
    assert total == expectedTotal, f"Expected {expectedTotal}, got {total}"
    print(f"✓ Total calculated correctly: ${total:.2f}")

    # Test category breakdown
    print("\nTesting category breakdown:")
    summaries = tracker.getCategoryBreakdown()
    assert len(summaries) == 3  # Food, Transport, Entertainment
    print(f"✓ Found {len(summaries)} categories")

    # Display using UI
    ui.handleCalculateTotal()

    # Test getAllExpenses
    print("\nTesting getAllExpenses...")
    expenses = tracker.getAllExpenses()
    assert len(expenses) == 4
    print(f"✓ Retrieved {len(expenses)} expenses")

    # Verify data persistence
    print("\nTesting data persistence...")
    tracker2 = ExpenseTracker(dataFile=testFile)
    print(f"✓ Loaded {len(tracker2.expenses)} expenses from file")
    assert len(tracker2.expenses) == 4

    # Test ID generation after reload
    print("\nTesting ID generation...")
    expense5 = tracker2.addExpense(30.00, "Food", "Dinner")
    assert expense5.id == 5
    print(f"✓ New expense has correct ID: {expense5.id}")

    # Clean up test file
    if os.path.exists(testFile):
        os.remove(testFile)
        print(f"✓ Test file cleaned up")

    print("\n" + "=" * 50)
    print("All tests passed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    testExpenseTracker()
