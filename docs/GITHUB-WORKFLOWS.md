# GitHub Workflows for Claude Code

This document provides comprehensive guidance on the GitHub Actions workflows configured for Claude Code integration in this repository.

## Overview

This repository uses two Claude Code workflows:

1. **claude.yml** - Interactive mode for issue/PR comments with `@claude` mentions
2. **claude-code-review.yml** - Automated PR reviews when PRs are opened or updated

## Workflow Files

### 1. claude.yml - Interactive Claude Code

**Purpose**: Responds to `@claude` mentions in issues, PR comments, and reviews.

**Triggers**:
- `issue_comment.created` - When someone comments on an issue
- `pull_request_review_comment.created` - When someone comments on a PR file
- `issues.opened` or `issues.assigned` - When issues are created or assigned
- `pull_request_review.submitted` - When a PR review is submitted

**Key Features**:
- Conditional execution only when `@claude` is mentioned
- Full git history access (`fetch-depth: 0`) for better context
- Write permissions to create commits and comments
- Access to CI/CD results via `actions: read` permission

**Required Secrets**:
- `ANTHROPIC_API_KEY` - Your Anthropic API key (starts with `sk-ant-`)

### 2. claude-code-review.yml - Automated PR Reviews

**Purpose**: Automatically reviews pull requests for code quality, security, and best practices.

**Triggers**:
- `pull_request.opened` - When a new PR is created
- `pull_request.synchronize` - When commits are pushed to an existing PR
- `pull_request.ready_for_review` - When a draft PR is marked ready
- `pull_request.reopened` - When a closed PR is reopened

**Key Features**:
- Automated review with custom prompt
- Repository-specific guidelines from CLAUDE.md
- Focus on security, performance, and maintainability
- Specific attention to expense-tracker application patterns

**Optional Configuration**:
- Filter by file paths (currently commented out)
- Filter by PR author or contributor status

## Required Permissions

Both workflows require these GitHub permissions:

```yaml
permissions:
  contents: write        # Create commits and modify files
  pull-requests: write   # Comment on PRs and create reviews
  issues: write          # Comment on issues
  id-token: write        # Authentication
  actions: read          # Read CI/CD workflow results
```

### Why Write Permissions Are Required

- **contents: write** - Allows Claude to create commits when implementing fixes
- **pull-requests: write** - Enables commenting on PRs with review feedback
- **issues: write** - Enables commenting on issues with responses
- **actions: read** - Allows Claude to analyze CI/CD failures and test results

## Setup Instructions

### Prerequisites

1. **Repository admin access** to configure secrets and workflows
2. **Anthropic API key** from https://console.anthropic.com/

### Step 1: Add GitHub Secrets

1. Navigate to repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the following:
   - **Name**: `ANTHROPIC_API_KEY`
   - **Value**: Your Anthropic API key (e.g., `sk-ant-api03-...`)
4. Click **Add secret**

### Step 2: Update Workflow Files

**IMPORTANT**: Due to security restrictions, workflow files in `.github/workflows/` cannot be modified by Claude Code directly. You must manually update them.

1. Review the fixed workflow files:
   - `.github/workflows/claude.yml.fixed`
   - `.github/workflows/claude-code-review.yml.fixed`

2. Manually copy the contents to the actual workflow files:
   ```bash
   # Backup current workflows
   cp .github/workflows/claude.yml .github/workflows/claude.yml.backup
   cp .github/workflows/claude-code-review.yml .github/workflows/claude-code-review.yml.backup

   # Apply fixes
   cp .github/workflows/claude.yml.fixed .github/workflows/claude.yml
   cp .github/workflows/claude-code-review.yml.fixed .github/workflows/claude-code-review.yml

   # Commit changes
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

### Step 3: Verify Setup

1. **Test Interactive Mode** (claude.yml):
   - Create a test issue
   - Comment with: `@claude what files are in this repository?`
   - Wait for Claude to respond with a comment

2. **Test Automated Review** (claude-code-review.yml):
   - Create a test branch with a small code change
   - Open a pull request
   - Wait for Claude to automatically post a review

## Testing and Troubleshooting

### Manual Testing Checklist

- [ ] `ANTHROPIC_API_KEY` secret is configured
- [ ] Workflow files have correct permissions (write access)
- [ ] `@claude` mention triggers claude.yml workflow
- [ ] PR creation triggers claude-code-review.yml workflow
- [ ] Claude successfully posts comments on issues
- [ ] Claude successfully posts reviews on PRs
- [ ] Claude can access full git history (fetch-depth: 0)
- [ ] Claude can read CI/CD results (if applicable)

### Common Issues and Solutions

#### Issue 1: Claude doesn't respond to `@claude` mentions

**Symptoms**: Workflow runs but no comment appears

**Causes**:
- Missing write permissions (`pull-requests: write` or `issues: write`)
- Invalid or missing `ANTHROPIC_API_KEY`
- Workflow conditional logic filtering out the trigger

**Solutions**:
1. Verify permissions in workflow file:
   ```yaml
   permissions:
     pull-requests: write
     issues: write
   ```
2. Check secret configuration in repository settings
3. Review workflow run logs in Actions tab

#### Issue 2: Automated PR review doesn't trigger

**Symptoms**: claude-code-review.yml workflow doesn't run

**Causes**:
- Workflow file path restrictions filtering out changes
- PR is in draft mode (unless `ready_for_review` trigger is enabled)
- Workflow file syntax errors

**Solutions**:
1. Check file path filters (commented out by default):
   ```yaml
   # paths:
   #   - "src/**/*.ts"
   ```
2. Mark draft PRs as "Ready for review"
3. Validate YAML syntax using GitHub Actions validator

#### Issue 3: Plugin/marketplace errors

**Symptoms**: Error about `plugin_marketplaces` or `plugins` not found

**Cause**: Outdated configuration from previous Claude Code versions

**Solution**: Remove these lines from claude-code-review.yml:
```yaml
# ❌ REMOVE these lines
plugin_marketplaces: 'https://github.com/anthropics/claude-code.git'
plugins: 'code-review@claude-code-plugins'
```

#### Issue 4: Insufficient git history

**Symptoms**: Claude mentions it can't access certain files or commits

**Cause**: `fetch-depth: 1` only fetches the latest commit

**Solution**: Change to full history:
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Fetch full history
```

### Debugging Workflow Runs

1. Navigate to **Actions** tab in GitHub repository
2. Click on the failed workflow run
3. Expand the "Run Claude Code" or "Run Claude Code Review" step
4. Review logs for error messages
5. Check for:
   - Authentication errors (invalid API key)
   - Permission errors (missing write access)
   - Rate limiting errors (too many API calls)
   - Network errors (timeouts, connection issues)

### Workflow Run Logs

Example successful run:
```
Run anthropics/claude-code-action@v1
Initializing Claude Code...
✓ API key validated
✓ Repository context loaded
✓ Processing request: "@claude review this code"
✓ Response posted to issue #42
```

Example failed run (missing permissions):
```
Run anthropics/claude-code-action@v1
Initializing Claude Code...
✓ API key validated
✓ Repository context loaded
✗ Error: Resource not accessible by integration
  Missing permission: pull-requests: write
```

## Testing Coverage

### Automated Workflow Testing

Currently, there are **no automated tests** for the GitHub workflows themselves. Testing is manual and relies on:

1. Creating test issues/PRs
2. Triggering workflows manually
3. Verifying Claude's responses

### Recommended Testing Approach

**For Development**:
1. Create a test issue with `@claude echo "test"`
2. Verify Claude responds within 1-2 minutes
3. Check response quality and formatting

**For Code Review**:
1. Create a test branch with intentional issues:
   - Security vulnerability (e.g., hardcoded secret)
   - Code style violation (e.g., snake_case in Python internal code)
   - Missing tests
2. Open PR and wait for automated review
3. Verify Claude identifies the issues

**For CI/CD Integration**:
1. Create a PR with failing tests
2. Verify Claude can access test results
3. Ask Claude: `@claude why did the tests fail?`

### Test Cases

| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| TC-01 | Issue comment with `@claude` | Claude responds with a comment |
| TC-02 | PR comment with `@claude` | Claude responds on the PR |
| TC-03 | New PR opened | Automated review posted |
| TC-04 | PR synchronized (new commits) | Updated review or new comments |
| TC-05 | Request code changes | Claude creates commits |
| TC-06 | Ask about test failures | Claude analyzes CI logs |
| TC-07 | Security review request | Claude identifies vulnerabilities |
| TC-08 | Style guide compliance | Claude follows CLAUDE.md conventions |

## Best Practices

### 1. Security

- **Never commit API keys** to workflow files
- Always use `${{ secrets.ANTHROPIC_API_KEY }}`
- Rotate API keys regularly (every 90 days recommended)
- Use repository secrets, not environment secrets for private repos
- Review Claude's proposed changes before merging

### 2. Performance

- Use `fetch-depth: 0` only when full history is needed
- Consider file path filters to limit review scope
- Use author filters to avoid reviewing internal team PRs
- Monitor API usage to stay within rate limits

### 3. Workflow Design

- Keep prompts specific and actionable
- Reference repository guidelines (CLAUDE.md)
- Provide context about coding standards
- Use conditional logic to prevent unnecessary runs
- Test workflows on draft PRs before enabling for all PRs

### 4. Integration with Repository

- Align automated reviews with CLAUDE.md conventions
- Focus reviews on areas with custom patterns (expense-tracker)
- Integrate with existing test suites (pytest, CI/CD)
- Document workflow behavior in this file

## Advanced Configuration

### Custom Slash Commands in Workflows

You can invoke repository-specific slash commands in workflow prompts:

```yaml
prompt: |
  @claude analyze this PR using /security-review
  Then run /auto-commit if changes are needed
```

### MCP Server Integration

Claude Code workflows can access MCP servers configured in `.mcp.json`:

```yaml
claude_args: '--mcp-config .mcp.json'
```

This enables:
- Weather data access (MCP US Weather Server)
- Browser automation (Puppeteer MCP Server)
- Structured reasoning (Sequential Thinking MCP Server)

### Multi-Step Workflows

For complex automation, chain multiple actions:

```yaml
prompt: |
  1. Review the expense-tracker API endpoints
  2. Check for security vulnerabilities
  3. Run tests: pytest test_api.py -v
  4. If tests pass, create a summary comment
  5. If tests fail, identify and fix the issues
```

## Migration Notes

### From Previous Configuration

**What Changed**:

1. **Removed**: Outdated plugin configuration
   - `plugin_marketplaces` - No longer supported
   - `plugins` - No longer supported
   - `/code-review:code-review` syntax - Replaced with direct prompts

2. **Added**: Write permissions
   - `contents: write` (was `read`)
   - `pull-requests: write` (was `read`)
   - `issues: write` (was `read`)

3. **Updated**: Checkout depth
   - `fetch-depth: 0` (was `1`) for full git history

4. **Enhanced**: Review prompts
   - Repository-specific guidelines
   - Security focus for Python/FastAPI code
   - Reference to CLAUDE.md conventions

**Migration Steps**:

1. Backup existing workflows
2. Apply fixes from `.fixed` files
3. Test on a draft PR or test issue
4. Monitor first few production runs
5. Adjust prompts based on feedback

## Support and Resources

### Documentation

- [Claude Code Action GitHub](https://github.com/anthropics/claude-code-action)
- [Setup Guide](https://github.com/anthropics/claude-code-action/blob/main/docs/setup.md)
- [Usage Documentation](https://github.com/anthropics/claude-code-action/blob/main/docs/usage.md)
- [Configuration Reference](https://github.com/anthropics/claude-code-action/blob/main/docs/configuration.md)
- [Claude Code CLI Docs](https://code.claude.com/docs/en/cli-reference)

### Troubleshooting

- [FAQ](https://github.com/anthropics/claude-code-action/blob/main/docs/faq.md)
- [GitHub Discussions](https://github.com/anthropics/claude-code-action/discussions)
- [Issue Tracker](https://github.com/anthropics/claude-code-action/issues)

### Repository-Specific

- **CLAUDE.md** - Repository guidelines and conventions
- **README-8Hooks.md** - Hooks system documentation
- **README-5WorkflowWSubagentAndSlashCommand.md** - Advanced workflow patterns

## Changelog

### 2026-01-18 - Fixed Workflow Configuration

- Fixed permissions in both workflows (added write access)
- Removed outdated plugin configuration
- Updated fetch-depth for full git history
- Added comprehensive review prompt for automated reviews
- Created this documentation file
- Added `.fixed` versions of workflow files
- Documented testing procedures and troubleshooting

### Previous Version (Before Fix)

- Read-only permissions (prevented commenting)
- Shallow git history (fetch-depth: 1)
- Outdated plugin references
- Generic/missing review prompts
