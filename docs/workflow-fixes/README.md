# Fixed Workflow Files

This directory contains corrected versions of the GitHub Actions workflow files for Claude Code integration.

## Why These Files Are Here

Due to GitHub App security restrictions, Claude Code cannot directly modify files in the `.github/workflows/` directory. These fixed versions must be **manually copied** by a repository administrator.

## Files

### claude.yml

Fixed version of `.github/workflows/claude.yml` with:
- ✅ Write permissions (`contents: write`, `pull-requests: write`, `issues: write`)
- ✅ Full git history access (`fetch-depth: 0`)
- ✅ Proper CI/CD integration (`actions: read`)

### claude-code-review.yml

Fixed version of `.github/workflows/claude-code-review.yml` with:
- ✅ Write permissions for all necessary scopes
- ✅ Full git history access for better context
- ✅ Removed outdated plugin configuration
- ✅ Added comprehensive review prompt following CLAUDE.md guidelines

## How to Apply These Fixes

### Option 1: Manual Copy (Recommended)

```bash
# Navigate to repository root
cd /path/to/ClaudeMastery

# Backup current workflows
cp .github/workflows/claude.yml .github/workflows/claude.yml.backup
cp .github/workflows/claude-code-review.yml .github/workflows/claude-code-review.yml.backup

# Apply fixes
cp docs/workflow-fixes/claude.yml .github/workflows/claude.yml
cp docs/workflow-fixes/claude-code-review.yml .github/workflows/claude-code-review.yml

# Review changes
git diff .github/workflows/

# Commit if satisfied
git add .github/workflows/
git commit -m "Fix GitHub workflows for Claude Code integration

- Add write permissions for contents, pull-requests, and issues
- Increase fetch-depth to 0 for full git history
- Remove outdated plugin configurations from claude-code-review.yml
- Add comprehensive review prompt following CLAUDE.md guidelines
- Enable actions: read for CI/CD result access

Fixes #4"

git push
```

### Option 2: Manual Edit

Alternatively, you can manually edit the workflow files in `.github/workflows/` using the changes documented below.

## Key Changes

### 1. Permissions (Both Files)

**Before**:
```yaml
permissions:
  contents: read
  pull-requests: read
  issues: read
  id-token: write
```

**After**:
```yaml
permissions:
  contents: write        # Changed from read
  pull-requests: write   # Changed from read
  issues: write          # Changed from read
  id-token: write
  actions: read          # Added
```

### 2. Checkout Depth (Both Files)

**Before**:
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 1
```

**After**:
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0   # Full git history
```

### 3. Remove Plugin Configuration (claude-code-review.yml Only)

**Remove these lines**:
```yaml
plugin_marketplaces: 'https://github.com/anthropics/claude-code.git'
plugins: 'code-review@claude-code-plugins'
prompt: '/code-review:code-review ${{ github.repository }}/pull/${{ github.event.pull_request.number }}'
```

**Replace with**:
```yaml
prompt: |
  Review this pull request for:
  1. Code quality and best practices
  2. Security vulnerabilities (especially for Python FastAPI code)
  3. Performance issues
  4. Maintainability and readability
  5. Test coverage
  6. Documentation completeness

  Focus on the expense-tracker application if changes are in that directory.
  Follow the repository's CLAUDE.md guidelines, particularly:
  - Python naming conventions (camelCase for internal, snake_case for API contracts)
  - Security patterns for JWT authentication
  - Testing conventions

  Provide specific, actionable feedback with file paths and line numbers.
```

## Verification

After applying the fixes, verify they work:

1. **Test Interactive Mode**:
   - Create a test issue
   - Comment: `@claude list all Python files in this repository`
   - Verify Claude responds

2. **Test Automated Review**:
   - Create a test branch with a small change
   - Open a pull request
   - Verify Claude posts an automated review

3. **Check Workflow Runs**:
   - Navigate to **Actions** tab
   - Verify workflows complete successfully
   - Check for permission errors in logs

## Troubleshooting

If workflows still fail after applying fixes:

1. **Check Secrets**: Verify `ANTHROPIC_API_KEY` is configured in repository settings
2. **Review Logs**: Check workflow run logs in Actions tab for specific errors
3. **Validate YAML**: Ensure no syntax errors were introduced during copy
4. **Clear Cache**: Sometimes GitHub caches old workflow configurations; try triggering a new run

## Related Documentation

- **docs/GITHUB-WORKFLOWS.md** - Comprehensive workflow documentation
- **CLAUDE.md** - Repository guidelines and conventions
- [Claude Code Action Setup Guide](https://github.com/anthropics/claude-code-action/blob/main/docs/setup.md)

## Why Can't Claude Fix This Automatically?

GitHub restricts workflow file modifications for security reasons. This prevents malicious code from modifying CI/CD pipelines through automated tools. Even GitHub Apps with broad permissions cannot modify workflow files without explicit `workflows: write` permission, which is not granted to the Claude GitHub App for security.

This is a security feature, not a bug. Manual review of workflow changes ensures repository administrators maintain control over CI/CD automation.
