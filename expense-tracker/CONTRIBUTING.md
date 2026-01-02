# Contributing to Expense Tracker

Thank you for your interest in contributing to the Expense Tracker project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions. We aim to create a welcoming environment for all contributors.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/expense-tracker.git
   cd expense-tracker
   ```
3. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.6 or higher
- Git

### Installation

1. No external dependencies are required (the project uses only Python standard library)
2. Verify your Python version:
   ```bash
   python --version
   ```

### Running the Application

```bash
python expense_tracker.py
```

### Running Tests

```bash
python test_tracker.py
```

## Code Style Guidelines

This project follows **PEP 8** - the Python Enhancement Proposal for style guidelines.

### Key Style Points

1. **Indentation**: Use 4 spaces per indentation level (no tabs)

2. **Line Length**: Maximum line length of 79 characters for code, 72 for docstrings/comments

3. **Imports**:
   - Group imports in this order: standard library, third-party, local
   - Use absolute imports
   - One import per line

4. **Naming Conventions**:
   - Classes: `CapitalizedWords` (e.g., `ExpenseTracker`)
   - Functions/Methods: `lowercase_with_underscores` (e.g., `add_expense`)
   - Constants: `UPPERCASE_WITH_UNDERSCORES` (e.g., `MAX_AMOUNT`)
   - Private methods: prefix with single underscore (e.g., `_internal_method`)

5. **Docstrings**:
   - Use triple quotes `"""`
   - Include for all public modules, classes, functions, and methods
   - Follow Google or NumPy docstring format
   - Include Args, Returns, and Raises sections where applicable

   Example:
   ```python
   def add_expense(self, amount: float, category: str, description: str):
       """
       Add a new expense to the tracker.

       Args:
           amount (float): The expense amount (must be positive)
           category (str): The expense category
           description (str): Description of the expense

       Returns:
           None
       """
   ```

6. **Type Hints**: Use type hints for function parameters and return values where helpful

7. **Comments**:
   - Write clear, concise comments
   - Avoid obvious comments
   - Update comments when code changes

### Code Formatting

To check your code style:

```bash
# Install flake8 (optional but recommended)
pip install flake8

# Run style check
flake8 expense_tracker.py test_tracker.py
```

## Testing

### Running Tests

Always run tests before submitting changes:

```bash
python test_tracker.py
```

### Writing Tests

When adding new features:

1. Add test cases to `test_tracker.py` or create new test files
2. Test both success cases and error conditions
3. Ensure tests clean up after themselves (delete temporary files)
4. Verify that existing tests still pass

Example test structure:
```python
def test_new_feature():
    """Test description."""
    # Setup
    tracker = ExpenseTracker(data_file='test.json')

    # Execute
    result = tracker.new_feature()

    # Verify
    assert result == expected_value

    # Cleanup
    os.remove('test.json')
```

## Making Changes

### Before You Start

1. Check existing issues to avoid duplicate work
2. For major changes, open an issue first to discuss the approach
3. Keep changes focused - one feature or fix per pull request

### Development Workflow

1. **Write Code**: Make your changes following the style guidelines

2. **Add Docstrings**: Document all new functions, classes, and methods

3. **Update Tests**: Add or update tests for your changes

4. **Run Tests**: Ensure all tests pass
   ```bash
   python test_tracker.py
   ```

5. **Update Documentation**: Update README.md if needed

6. **Commit Changes**: Write clear, descriptive commit messages
   ```bash
   git add .
   git commit -m "Add feature: expense filtering by date range"
   ```

### Commit Message Guidelines

- Use present tense: "Add feature" not "Added feature"
- Use imperative mood: "Fix bug" not "Fixes bug"
- First line should be 50 characters or less
- Add detailed description after a blank line if needed

Examples:
```
Add expense filtering by date range

Implements a new method filter_by_date() that allows users to
view expenses within a specific date range. Includes validation
for date formats and error handling.
```

## Pull Request Process

1. **Update Your Branch**: Ensure your branch is up to date with main
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Push Your Changes**:
   ```bash
   git push origin your-feature-branch
   ```

3. **Create Pull Request**:
   - Go to the GitHub repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template with:
     - Description of changes
     - Related issue numbers (if applicable)
     - Testing performed
     - Screenshots (if UI changes)

4. **PR Requirements**:
   - All tests must pass
   - Code follows style guidelines
   - Documentation is updated
   - Commit messages are clear
   - No merge conflicts

5. **Review Process**:
   - Maintainers will review your PR
   - Address any requested changes
   - Once approved, your PR will be merged

## Issue Reporting

### Bug Reports

When reporting bugs, include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**:
   - Python version
   - Operating system
   - Any relevant details
6. **Error Messages**: Full error messages or stack traces
7. **Screenshots**: If applicable

Example:
```markdown
**Bug**: Expense total calculation incorrect with multiple categories

**Steps to Reproduce**:
1. Add expense: $50 Food
2. Add expense: $30 Transport
3. Run "Calculate Total"

**Expected**: Total should be $80
**Actual**: Total shows $50

**Environment**: Python 3.9, Windows 10
```

### Feature Requests

When suggesting features, include:

1. **Description**: Clear description of the feature
2. **Use Case**: Why this feature would be useful
3. **Proposed Solution**: How you think it should work
4. **Alternatives**: Any alternative solutions you've considered

## Questions?

If you have questions:

- Check existing issues and pull requests
- Open a new issue with the "question" label
- Reach out to the maintainers

## Recognition

Contributors will be acknowledged in:
- Project README.md
- Release notes
- GitHub contributors page

Thank you for contributing to Expense Tracker!
