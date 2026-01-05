# Claude Code Slash Command

<https://code.claude.com/docs/en/slash-commands>

## Custom Slash Command & Frontmatter

### Custom Slash Commands

<https://code.claude.com/docs/en/slash-commands#custom-slash-commands>

#### **Syntax**

```note
/<command-name> [arguments]
```

```bash
# Create a personal command
mkdir -p .claude/commands
cat << 'EOF' > .claude/commands/security-review.md
Review this code for security vulnerabilities:
EOF

cat << 'EOF' > .claude/commands/review-pr.md
Print this statement - Review PR #$1 with priority $2 and assign to $3
EOF

```

## Slash Command for Expense Tracker Report Documentation

```bash
# Use the personal command in expense-tracker project
mkdir -p expense-tracker/.claude/commands

cat << 'EOF' > expense-tracker/.claude/commands/expense-tracker-doc.md
---
description: Generate and maintain comprehensive documentation from code
argument-hint: --api or --readme or --check
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(test:*), Bash(grep:*), Bash(find:*), Bash(head:*), Bash(wc:*), Bash(python:*)
---

# Expense Report Documentation

Generate and maintain documentation from code, keeping it in sync with implementation.

## Usage Examples

**Basic documentation generation:**
/expense-tracker-doc

**Generate API documentation:**
/expense-tracker-doc --api

**Check documentation coverage:**
/expense-tracker-doc --check

**Generate README:**
/expense-tracker-doc --readme

**Help and options:**
/expense-tracker-doc --help

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
EOF

```

### Run the Expense Report Documentation Command

```cmd
cd expense-tracker
claude
  /expense-tracker-doc --readme
  /expense-tracker-doc --check

/clear  
quit
```

## Slash Command - Refactor Expense Tracker Code

```bash
cat << 'EOF' > expense-tracker/.claude/commands/expense-tracker-refactor.md
---
description: Refactor Python code for better quality
argument-hint: [file-path]
allowed-tools: Bash(cat:*), Bash(python:*), Bash(pytest:*)
---

# Refactor Python Code: $ARGUMENTS

Refactor the Python file to improve code quality and readability.

If $ARGUMENTS is empty:
Refactor the entire codebase

## Steps

1. **Read the file:** `cat $ARGUMENTS`

2. **Analyze the code** and identify issues:

   - Long functions (over 50 lines)
   - Duplicate code
   - Complex nested loops
   - Missing docstrings
   - Poor variable names
   - Magic numbers

3. **Create improved version** with:

   - Object Oriented approach
   - Clear function names
   - Extracted repeated code
   - Better variable names
   - Type hints
   - Constants for magic numbers

4. **Run tests** to ensure nothing broke: `pytest tests/ -v`

5. **Show before/after comparison**

## Refactoring Checklist

Functions are small (under 50 lines)
Each function does one thing
Good variable and function names
Docstrings added
Type hints included
No duplicate code
Tests still pass
EOF
```

## Test the Refactor Command

```cmd
cd expense-tracker
claude
  /expense-tracker-refactor expense_tracker.py 
  /expense-tracker-doc --check
  /expense-tracker-doc --readme

  /clear
  quit
```

## Git Slash Command

```bash
cat << 'EOF' > expense-tracker/.claude/commands/expense-git.md
---
description: Quick git commit workflow
allowed-tools: Bash(git:*), Bash(pytest:*)
---

# Quick Commit

1. Refactor code
2. Run tests: `pytest -v`
3. Update Readme.md
4. If tests pass:
   - cd ..
   - Show status: `git status`
   - Stage all: `git add .`
   - Ask for commit message
   - Commit: `git commit -m "{message}"`
   - Push: `git push`
5. Done!
EOF
```

```cmd
claude
  /expense-git
  /clear
  quit
```

## Slash Command for MCP - Hands On

<https://code.claude.com/docs/en/slash-commands#mcp-slash-commands>

```bash
cat <<'EOF' > .mcp.json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": [
        "d:\\development\\mcp-servers\\quickstart-resources\\weather-server-typescript\\build\\index.js"
      ]
    }
  }
}
EOF
```

```bash
claude

  /mcp
  #  1. Use this and all future MCP servers in this project 

  #   Tool name: get-alerts
  #   Full name: mcp__weather__get-alerts

  
  mcp__weather__get-alerts NY

  mcp__weather__get-forecast {
    latitude: 40.7128,
    longitude: -74.006
  }

```

## Slash Command Workflow - Hands On

<https://code.claude.com/docs/en/slash-commands#slash-command-workflow>

```bash
cat << 'EOF' > expense-tracker/.claude/commands/expense-tracker-workflow.md
---
description: Run complete workflow - refactor code then generate documentation
argument-hint: [file-path]
allowed-tools: Bash(cat:*), Bash(python:*), Bash(pytest:*), Bash(ls:*), Bash(grep:*), Bash(find:*)
---

# Full Workflow: Refactor + Documentation

Execute the complete development workflow for: $ARGUMENTS

If $ARGUMENTS is empty, process the entire codebase.

## Workflow Steps

### Phase 1: Code Refactoring
Run the below slash command
/expense-tracker-refactor [file] | Refactor Python code for better quality |

### Phase 2: Documentation Generation
Run the below slash commands sequentially
/expense-tracker-doc --check | Check documentation coverage |
/expense-tracker-doc | Generate all documentation |
EOF

cd expense-tracker
claude
  /expense-tracker-workflow 
  /clear
  quit

cd ..
claude
  
```

## SubAgents & Skills

<https://code.claude.com/docs/en/sub-agents>
<https://code.claude.com/docs/en/skills>
