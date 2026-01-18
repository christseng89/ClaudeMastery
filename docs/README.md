# Documentation Directory

This directory contains supplementary documentation for the ClaudeMastery repository.

## Available Documentation

### GITHUB-WORKFLOWS.md

**Purpose**: Comprehensive guide for GitHub Actions workflows integrated with Claude Code

**Contents**:
- Workflow configuration and setup
- Required permissions and secrets
- Testing and troubleshooting procedures
- Common issues and solutions
- Best practices for CI/CD integration
- Migration guide from previous configurations

**When to use**:
- Setting up Claude Code GitHub Actions
- Troubleshooting workflow failures
- Understanding permission requirements
- Testing automated PR reviews
- Configuring interactive `@claude` mentions

## Related Documentation

### Root-Level Documentation

- **CLAUDE.md** - Primary repository guidance and conventions
- **README-*.md** - Numbered learning progression (1.1, 1.2, 2, 3, 4, 5, 6, 8)

### Resources Directory

- **6.1 Context Preservation.md** - Context management across sessions
- **6.2 A Deep Dive into Code Memory.md** - Memory architecture and patterns
- **6.3 Memory Access Commands.md** - Quick memory management reference

## Contributing Documentation

When adding new documentation to this directory:

1. **Create descriptive filenames** in UPPERCASE with hyphens (e.g., `TESTING-GUIDE.md`)
2. **Update this README** with a brief description of the new document
3. **Reference from CLAUDE.md** if it's a core pattern or frequently used guide
4. **Include practical examples** and code snippets where applicable
5. **Follow markdown best practices**:
   - Use headers hierarchically (h1 → h2 → h3)
   - Include a table of contents for long documents
   - Use code blocks with language specifiers
   - Add links to related documentation

## Documentation Standards

### Structure

```markdown
# Title

Brief overview of what this document covers.

## Section 1

Content...

### Subsection 1.1

Detailed content...

## Examples

Practical examples with code snippets...

## See Also

- Related doc 1
- Related doc 2
```

### Code Examples

Always specify the language for syntax highlighting:

````markdown
```yaml
name: Example Workflow
on: push
```

```python
def exampleFunction():
    return "formatted code"
```
````

### Links

- Use relative links for internal documentation
- Use absolute links for external resources
- Verify links work before committing

## Quick Reference

| Document | Purpose | Key Topics |
|----------|---------|------------|
| GITHUB-WORKFLOWS.md | GitHub Actions with Claude Code | Workflows, permissions, testing |

## Feedback

If documentation is unclear, incomplete, or incorrect:

1. Open an issue describing the problem
2. Tag it with the `documentation` label
3. Suggest improvements if possible
