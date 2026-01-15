#!/bin/bash
# TypeScript formatting hook script

# Read JSON input from Claude Code
input_json=$(cat)

# Extract file path from the JSON input using jq
file_path=$(echo "$input_json" | jq -r '.tool_input.file_path // empty')

# Check if we got a valid file path
if [[ -z "$file_path" ]]; then
  exit 0
fi

# Check if the file is a TypeScript file
if [[ "$file_path" =~ \.(ts|tsx)$ ]]; then
  # Check if prettier is installed
  if ! command -v prettier &> /dev/null; then
    echo "Warning: prettier is not installed. Install with: npm install -g prettier" >&2
    exit 1
  fi

  # Check if file exists
  if [[ ! -f "$file_path" ]]; then
    echo "Warning: File $file_path does not exist" >&2
    exit 1
  fi

  # Run prettier on the TypeScript file
  if prettier --write "$file_path" 2>/dev/null; then
    echo "✅ Formatted TypeScript file: $file_path"
    exit 0
  else
    echo "❌ Error: Failed to format $file_path with prettier" >&2
    exit 1
  fi
else
  # Not a TypeScript file, just exit successfully
  exit 0
fi
