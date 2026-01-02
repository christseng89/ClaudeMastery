# Changelog

All notable changes to the Expense Tracker project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation coverage (100%)
- Complete API reference in README.md
- CONTRIBUTING.md with developer guidelines
- CHANGELOG.md for tracking project changes
- Docstrings for all classes, methods, and functions

### Changed
- Enhanced README.md with detailed examples and usage instructions

## [1.0.0] - 2026-01-02

### Added
- Core expense tracking functionality
- ExpenseTracker class with persistent JSON storage
- Add expense feature with validation
- View all expenses in formatted table
- Calculate total spending with category breakdown
- Automatic timestamping for all expenses
- Interactive menu-driven CLI interface
- Data validation (positive amounts, non-empty categories)
- Error handling for invalid inputs and corrupted files
- Test suite with automated testing script
- Project documentation (README.md)

### Features
- **Add Expenses**: Record expenses with amount, category, and description
- **View Expenses**: Display all expenses in a formatted table
- **Category Analytics**: Automatic breakdown by category with percentages
- **Persistent Storage**: JSON file storage for data persistence
- **Input Validation**: Comprehensive validation and error handling

### Technical Details
- Built with Python 3.6+ using standard library only
- No external dependencies required
- JSON-based data storage
- Type hints for better code clarity
- Comprehensive docstrings following PEP 257

## Version History

### [1.0.0] - Initial Release
First stable release of Expense Tracker with core functionality.

---

## Types of Changes

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

## How to Update This File

When making changes to the project:

1. Add entries under the **[Unreleased]** section
2. Use the appropriate change type (Added, Changed, Fixed, etc.)
3. Keep entries concise but descriptive
4. When releasing a new version:
   - Change **[Unreleased]** to the new version number and date
   - Create a new **[Unreleased]** section at the top
   - Follow semantic versioning (MAJOR.MINOR.PATCH)

Example entry:
```markdown
### Added
- New feature for filtering expenses by date range
- Export functionality to CSV format

### Fixed
- Bug in total calculation when expenses list is empty
- Incorrect percentage display for categories
```
