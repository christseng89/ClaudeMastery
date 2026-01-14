# MCP Server

## MCP Server with Sequential Thinking

<https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking>

### Overview

The Sequential Thinking MCP server provides a structured, step-by-step thinking process for dynamic and reflective problem-solving. It enables breaking down complex problems into manageable steps with capacity for revision and exploring alternative reasoning paths.

### Features

- **Break down complex problems** into manageable steps
- **Revise and refine thoughts** as understanding deepens
- **Branch into alternative paths** of reasoning
- **Track thought progression** with indexing (thoughtNumber, totalThoughts)
- **Adjust dynamically** the total number of thoughts as analysis progresses
- **Generate and verify** solution hypotheses iteratively
- **Maintain context** over multiple reasoning steps

### Tool: sequential_thinking

The server provides a single tool called `sequential_thinking` that facilitates detailed thinking processes.

**Parameters:**

- `thought` (string) - The content of the current thinking step
- `nextThoughtNeeded` (boolean) - Whether another thought step is needed
- `thoughtNumber` (integer) - The index of the current thought
- `totalThoughts` (integer) - The model's current estimate of total steps
- `isRevision` (boolean, optional) - Marks this thought as a revision
- `revisesThought` (integer, optional) - Specifies which thought number is being revised
- `branchFromThought` (integer, optional) - Specifies the thought to branch from
- `branchId` (string, optional) - An identifier for a specific reasoning branch

### Common Use Cases

- **Complex problem decomposition** - Breaking architectural decisions into steps
- **Planning with course correction** - Iterative refinement of strategies
- **Exploratory reasoning** - Testing multiple approaches in parallel branches
- **Debugging and root cause analysis** - Systematic investigation of issues
- **Algorithm design** - Step-by-step logic development with verification

### Installation

```bash
claude
claude mcp add sequential-thinking --scope project -- npx -y @modelcontextprotocol/server-sequential-thinking

quit

claude
/mcp

   s quential-thinking · ◯ connecting…. Hangs on fix it.

quit
claude
/mcp

   sequential-thinking · ✔ connected

/clear
/auto-commit 

Can you refactor the code in memory-hands-on/src/api directory to add models. Please use MCP server, sequential_thinking.

```

### Configuration

**Optional Environment Variable:**

- `DISABLE_THOUGHT_LOGGING=true` - Disable logging of thought information

### Example Usage

After installation and restart, you can use the sequential_thinking tool:

```python
# Example 1: Initial problem breakdown
sequential_thinking({
    "thought": "Need to optimize database queries for the expense tracker API",
    "thoughtNumber": 1,
    "totalThoughts": 5,
    "nextThoughtNeeded": True
})

# Example 2: Revising a previous thought
sequential_thinking({
    "thought": "Actually, indexing on user_id and date columns would be most effective",
    "thoughtNumber": 3,
    "totalThoughts": 5,
    "isRevision": True,
    "revisesThought": 2,
    "nextThoughtNeeded": True
})

# Example 3: Exploring alternative approach
sequential_thinking({
    "thought": "Alternative: Use query result caching instead of database optimization",
    "thoughtNumber": 4,
    "totalThoughts": 6,
    "branchFromThought": 2,
    "branchId": "caching-approach",
    "nextThoughtNeeded": True
})
```

### Benefits

- Structures AI reasoning into clear, traceable steps
- Enables iterative refinement without losing context
- Supports exploring multiple solution paths
- Improves problem-solving for complex scenarios
- Makes the AI's thought process transparent and auditable
