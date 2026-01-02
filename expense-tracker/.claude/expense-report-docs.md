---
description: Generate and maintain comprehensive documentation from code
argument-hint: --api or --readme or --check
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(test:*), Bash(grep:*), Bash(find:*), Bash(head:*), Bash(wc:*), Bash(python:*)
---

# Expense Report Documentation

Generate and maintain documentation from code, keeping it in sync with implementation.

## Usage Examples

**Basic documentation generation:**
/expense-report-docs

**Generate API documentation:**
/expense-report-docs --api

**Check documentation coverage:**
/expense-report-docs --check

**Generate README:**
/expense-report-docs --readme

**Help and options:**
/expense-report-docs --help

## Implementation

If $ARGUMENTS contains "help" or "--help":
Display this usage information and exit.

Parse documentation options from $ARGUMENTS (--generate, --api, --readme, --check, or specific module/file).

## 1. Analyze Current Documentation

Check existing documentation:
!find . -name "*.md" | grep -v node_modules | head -20
!test -f README.md && echo "README exists" || echo "No README.md found"
!find . -name "*.py" -exec grep -L '"""' {} \; | wc -l

## 2. Generate Documentation

Based on the arguments and project type, generate appropriate documentation.

For Python projects, extract docstrings:
!python -c "import ast; import os; [print(f'{f}: {len([n for n in ast.walk(ast.parse(open(f).read())) if isinstance(n, ast.FunctionDef) and ast.get_docstring(n)])} documented functions') for f in os.listdir('.') if f.endswith('.py')]" 2>/dev/null

## 3. API Documentation

If --api flag is present, analyze API endpoints:
!grep -r -E "@(app|router)\.(get|post|put|delete|patch)" --include="*.py" 2>/dev/null | head -20

## 4. Check Documentation Coverage

Count undocumented functions:
!find . -name "*.py" -exec grep -E "^def |^class " {} \; | wc -l
!find . -name "*.py" -exec grep -A1 -E "^def |^class " {} \; | grep '"""' | wc -l

Think step by step about documentation needs and:

1. Identify what documentation is missing
2. Generate appropriate documentation based on code analysis
3. Create templates for missing documentation
4. Ensure examples are included

Generate documentation based on the flag provided:

### For README.md (--readme flag)

Create a comprehensive README with these sections:

- Project title and description
- Installation instructions (from package.json or requirements.txt)
- Usage examples (from main entry points)
- API Reference with function/class documentation
- Parameters, return types, and examples extracted from docstrings
- Contributing guidelines reference
- License information

### For API Documentation (--api flag)

Create API.md with:

- Endpoint listing (HTTP method and path)
- Description of what each endpoint does
- Parameters (query/path/body)
- Response format examples in JSON
- cURL examples for testing

### For Coverage Report (--check flag)

Generate a formatted report showing:

📄 DOCUMENTATION COVERAGE REPORT
───────────────────────────────

Overall Coverage: X%

✅ DOCUMENTED (X/Y)

- List documented modules with function counts
- List documented API endpoints

❌ MISSING DOCUMENTATION (X/Y)

- List undocumented functions with file and line number
- List undocumented classes with file and line number

🔧 QUICK FIXES

- Prioritized list of documentation tasks
- Specific functions/classes that need docstrings
- Missing API endpoint documentation

🧩 TEMPLATES TO ADD

- README.md sections that are missing
- API.md if no API documentation exists
- CONTRIBUTING.md if missing development setup

## Output Format

Present all documentation in clean markdown format. Use proper headers, code blocks, and formatting. Include examples where relevant. Ensure all generated documentation is accurate and matches the actual code implementation.
