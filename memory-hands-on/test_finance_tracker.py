#!/usr/bin/env python3
"""
Test suite for Personal Finance Tracker CLI.
Tests all core functionality including validation, persistence, and display.
"""

import json
from decimal import Decimal
from pathlib import Path

import pytest

from finance_tracker import FinanceTracker, ValidationError


@pytest.fixture
def testFile(tmp_path):
    """Create a temporary test file path."""
    return tmp_path / "test_transactions.json"


@pytest.fixture
def tracker(testFile):
    """Create a FinanceTracker instance with test file."""
    return FinanceTracker(data_file=str(testFile))


@pytest.fixture
def populatedTracker(testFile):
    """Create a tracker with pre-existing transactions."""
    # Create test data
    testData = [
        {
            "amount": "25.50",
            "category": "groceries",
            "description": "Weekly shopping",
            "date": "2026-01-09T10:00:00",
        },
        {
            "amount": "100.00",
            "category": "utilities",
            "description": "",
            "date": "2026-01-09T11:00:00",
        },
    ]

    # Write test data to file
    with testFile.open("w") as f:
        json.dump(testData, f)

    return FinanceTracker(data_file=str(testFile))


class TestFinanceTrackerInitialization:
    """Test FinanceTracker initialization and file loading."""

    def test_initialization_with_no_file(self, tracker):
        """Test initialization when no data file exists."""
        assert tracker.transactions == []
        assert isinstance(tracker.data_file, Path)

    def test_initialization_loads_existing_transactions(self, populatedTracker):
        """Test that existing transactions are loaded on initialization."""
        assert len(populatedTracker.transactions) == 2
        assert populatedTracker.transactions[0]["category"] == "groceries"
        assert populatedTracker.transactions[1]["category"] == "utilities"

    def test_initialization_with_corrupted_json(self, testFile):
        """Test initialization recovers from corrupted JSON file."""
        # Write invalid JSON
        with testFile.open("w") as f:
            f.write("{invalid json content")

        tracker = FinanceTracker(data_file=str(testFile))
        assert tracker.transactions == []


class TestAmountValidation:
    """Test amount validation logic."""

    def test_valid_amount(self, tracker):
        """Test that valid amounts pass validation."""
        # Should not raise exception
        tracker._validate_amount(Decimal("25.50"))
        tracker._validate_amount(Decimal("100"))
        tracker._validate_amount(Decimal("0.01"))

    def test_negative_amount_rejected(self, tracker):
        """Test that negative amounts are rejected."""
        with pytest.raises(ValidationError, match="Amount must be greater than zero"):
            tracker._validate_amount(Decimal("-10.00"))

    def test_zero_amount_rejected(self, tracker):
        """Test that zero amount is rejected."""
        with pytest.raises(ValidationError, match="Amount must be greater than zero"):
            tracker._validate_amount(Decimal("0"))

    def test_non_decimal_amount_rejected(self, tracker):
        """Test that non-Decimal types are rejected."""
        with pytest.raises(ValidationError, match="Amount must be a Decimal"):
            tracker._validate_amount(25.50)  # float
        with pytest.raises(ValidationError, match="Amount must be a Decimal"):
            tracker._validate_amount("25.50")  # string
        with pytest.raises(ValidationError, match="Amount must be a Decimal"):
            tracker._validate_amount(25)  # int


class TestCategoryValidation:
    """Test category validation logic."""

    def test_valid_category(self, tracker):
        """Test that valid categories pass validation."""
        # Should not raise exception
        tracker._validate_category("groceries")
        tracker._validate_category("utilities")
        tracker._validate_category("a")  # single character is valid

    def test_empty_category_rejected(self, tracker):
        """Test that empty categories are rejected."""
        with pytest.raises(ValidationError, match="Category cannot be empty"):
            tracker._validate_category("")

    def test_whitespace_only_category_rejected(self, tracker):
        """Test that whitespace-only categories are rejected."""
        with pytest.raises(ValidationError, match="Category cannot be empty"):
            tracker._validate_category("   ")
        with pytest.raises(ValidationError, match="Category cannot be empty"):
            tracker._validate_category("\t\n")


class TestAddTransaction:
    """Test adding transactions."""

    def test_add_transaction_with_description(self, tracker, testFile):
        """Test adding a complete transaction with description."""
        transaction = tracker.add_transaction(
            amount=Decimal("25.50"),
            category="groceries",
            description="Weekly shopping",
        )

        # Verify transaction structure
        assert transaction["amount"] == "25.50"
        assert transaction["category"] == "groceries"
        assert transaction["description"] == "Weekly shopping"
        assert "date" in transaction

        # Verify transaction is in memory
        assert len(tracker.transactions) == 1
        assert tracker.transactions[0] == transaction

        # Verify transaction is persisted to file
        with testFile.open("r") as f:
            savedData = json.load(f)
        assert len(savedData) == 1
        assert savedData[0]["category"] == "groceries"

    def test_add_transaction_without_description(self, tracker, testFile):
        """Test adding a transaction without description."""
        transaction = tracker.add_transaction(
            amount=Decimal("100.00"), category="utilities", description=None
        )

        assert transaction["amount"] == "100.00"
        assert transaction["category"] == "utilities"
        assert transaction["description"] == ""

    def test_add_transaction_trims_whitespace(self, tracker):
        """Test that category and description whitespace is trimmed."""
        transaction = tracker.add_transaction(
            amount=Decimal("50.00"),
            category="  entertainment  ",
            description="  Movie night  ",
        )

        assert transaction["category"] == "entertainment"
        assert transaction["description"] == "Movie night"

    def test_add_multiple_transactions(self, tracker, testFile):
        """Test adding multiple transactions in sequence."""
        tracker.add_transaction(Decimal("25.50"), "groceries", "Shopping")
        tracker.add_transaction(Decimal("100.00"), "utilities", None)
        tracker.add_transaction(Decimal("50.00"), "entertainment", "Movies")

        assert len(tracker.transactions) == 3

        # Verify all are persisted
        with testFile.open("r") as f:
            savedData = json.load(f)
        assert len(savedData) == 3

    def test_add_transaction_with_invalid_amount(self, tracker):
        """Test that invalid amount raises ValidationError."""
        with pytest.raises(ValidationError):
            tracker.add_transaction(
                amount=Decimal("-10.00"), category="groceries", description="Test"
            )

        # Verify no transaction was added
        assert len(tracker.transactions) == 0

    def test_add_transaction_with_invalid_category(self, tracker):
        """Test that invalid category raises ValidationError."""
        with pytest.raises(ValidationError):
            tracker.add_transaction(
                amount=Decimal("25.50"), category="", description="Test"
            )

        # Verify no transaction was added
        assert len(tracker.transactions) == 0

    def test_add_transaction_preserves_decimal_precision(self, tracker):
        """Test that Decimal precision is preserved in storage."""
        transaction = tracker.add_transaction(
            amount=Decimal("123.456"), category="test", description=None
        )

        # Verify precision is maintained
        assert transaction["amount"] == "123.456"
        storedAmount = Decimal(transaction["amount"])
        assert storedAmount == Decimal("123.456")


class TestTransactionPersistence:
    """Test transaction persistence to file system."""

    def test_transactions_persist_across_instances(self, testFile):
        """Test that transactions persist when creating new tracker instance."""
        # Create first tracker and add transaction
        tracker1 = FinanceTracker(data_file=str(testFile))
        tracker1.add_transaction(Decimal("25.50"), "groceries", "Shopping")

        # Create second tracker - should load the transaction
        tracker2 = FinanceTracker(data_file=str(testFile))
        assert len(tracker2.transactions) == 1
        assert tracker2.transactions[0]["category"] == "groceries"

    def test_file_created_on_first_save(self, testFile):
        """Test that data file is created when first transaction is added."""
        assert not testFile.exists()

        tracker = FinanceTracker(data_file=str(testFile))
        tracker.add_transaction(Decimal("25.50"), "groceries", None)

        assert testFile.exists()


class TestDisplayTransaction:
    """Test transaction display functionality."""

    def test_display_transaction_with_description(self, tracker, capsys):
        """Test displaying transaction with description."""
        transaction = {
            "amount": "25.50",
            "category": "groceries",
            "description": "Weekly shopping",
            "date": "2026-01-09T10:00:00",
        }

        tracker.display_transaction(transaction)
        captured = capsys.readouterr()

        assert "Transaction Added Successfully!" in captured.out
        assert "$25.50" in captured.out
        assert "groceries" in captured.out
        assert "Weekly shopping" in captured.out
        assert "2026-01-09T10:00:00" in captured.out

    def test_display_transaction_without_description(self, tracker, capsys):
        """Test displaying transaction without description."""
        transaction = {
            "amount": "100.00",
            "category": "utilities",
            "description": "",
            "date": "2026-01-09T11:00:00",
        }

        tracker.display_transaction(transaction)
        captured = capsys.readouterr()

        assert "Transaction Added Successfully!" in captured.out
        assert "$100.00" in captured.out
        assert "utilities" in captured.out
        # Description line should not appear
        assert "Description:" not in captured.out


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_large_amount(self, tracker):
        """Test handling of very large amounts."""
        largeAmount = Decimal("999999999.99")
        transaction = tracker.add_transaction(
            amount=largeAmount, category="investment", description=None
        )

        assert transaction["amount"] == "999999999.99"

    def test_very_small_amount(self, tracker):
        """Test handling of very small amounts."""
        smallAmount = Decimal("0.01")
        transaction = tracker.add_transaction(
            amount=smallAmount, category="test", description=None
        )

        assert transaction["amount"] == "0.01"

    def test_unicode_in_category_and_description(self, tracker):
        """Test handling of unicode characters."""
        transaction = tracker.add_transaction(
            amount=Decimal("50.00"),
            category="café",
            description="Lunch at café with friends 🍽️",
        )

        assert transaction["category"] == "café"
        assert "🍽️" in transaction["description"]

    def test_long_description(self, tracker):
        """Test handling of very long descriptions."""
        longDescription = "A" * 1000  # 1000 character description
        transaction = tracker.add_transaction(
            amount=Decimal("25.50"), category="test", description=longDescription
        )

        assert len(transaction["description"]) == 1000
