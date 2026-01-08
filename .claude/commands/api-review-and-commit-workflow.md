# API Review and Commit Workflow

You are tasked with orchestrating a complete API review, testing, and git commit workflow.

## Workflow Steps

### Step 1: Launch API Reviewer Agent

- Use the Task tool with the following parameters:
  - `subagent_type`: "api-reviewer"
  - `description`: "Review expense tracker API"
  - `prompt`: "Review all API endpoints, request/response schemas, and API documentation in the expense-tracker application. Analysis for best practices, security vulnerabilities, usability issues, and design patterns. Provide specific, actionable recommendations for improvements with code examples where applicable."

### Step 2: Process and Present Findings

- Wait for the api-reviewer agent to complete
- Analysis the findings and categories them:
  - Critical security issues
  - Design/architecture concerns
  - Best practice violations
  - Usability improvements
- Present a clear summary to the user with:
  - Number of issues found by category
  - Specific file locations affected
  - Priority recommendations

### Step 3: User Confirmation

- Ask the user if they want to proceed with fixes and commit
- If critical issues are found, recommend addressing them first
- Wait for user approval before proceeding
- Options:
  1. Fix critical issues first, then test and commit (Recommended)
  2. Proceed with commit as-is (Not recommended if critical issues exist)
  3. Review specific issues in detail before deciding

### Step 4: Fix Critical Issues (If User Approves)

- If user chooses to fix issues, implement all critical security fixes
- Use TodoWrite to track progress on each fix
- Mark each task as completed when done

### Step 5: Run Tests Before Commit

**CRITICAL: Always run tests before committing changes**

- Navigate to expense-tracker directory
- Run pytest: `cd expense-tracker && python -m pytest test_api.py -v`
- Check exit code and verify all tests pass
- If tests fail:
  - Investigate and fix the failures
  - Do NOT proceed to commit until tests pass
  - Common issues to check:
    - Missing dependencies (install with pip)
    - Configuration errors (check .env or config.py)
    - Database issues (check database initialization)

### Step 6: Verify API Startup

- Test that the API can start successfully
- Run: `cd expense-tracker && timeout 5 python api_main.py 2>&1 || true`
- Verify the server starts without errors
- Look for: "Uvicorn running on" and "Application startup complete"
- If startup fails:
  - Check for configuration issues
  - Verify all imports work correctly
  - Do NOT proceed to commit until API starts successfully

### Step 7: Update Documentation

**If tests and API startup succeed:**

- Read the current README.md in the expense-tracker directory
- Update README.md to document:
  - Security improvements made
  - New configuration requirements (e.g., SECRET_KEY validation)
  - Environment variable changes
  - Any breaking changes
- Keep documentation clear and concise
- Include code examples where helpful

### Step 8: Execute Git Commit

- Once all tests pass and documentation is updated:
  - Use the Skill tool to execute: `/auto-commit` or the Skill tool with `skill: "auto-commit"`
  - Allow the git commit workflow to complete
  - Verify the commit was created successfully

### Step 9: Final Confirmation

- Confirm final status to the user with:
  - Number of issues fixed
  - Test results summary
  - Commit hash and message
  - Next steps or recommendations

## Important Guidelines

- **NEVER skip the testing steps** - Tests must pass before committing
- Always wait for each step to fully complete before proceeding
- Never skip the user confirmation step
- If the api-reviewer agent fails, do not proceed to git commit
- If tests fail, do not proceed to commit - fix issues first
- If API startup fails, do not proceed to commit - fix issues first
- Provide clear, actionable feedback at each stage
- Use TodoWrite tool to track progress throughout the workflow

## Error Handling

- If pytest fails due to missing modules: Install them with pip
- If config validation fails: Check SECRET_KEY and other required env variables
- If tests fail: Investigate the specific test failures and fix the code
- If API won't start: Check configuration and import errors
- Always provide clear error messages and suggested fixes to the user
