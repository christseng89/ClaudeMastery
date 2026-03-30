# Prompt 1: Build a Finance Advisor Agent (No Memory)

Copy and paste the following into Claude Code:

```
Context: Building a Jupyter notebook using the OpenAI Agents SDK to create a personal finance advisor.

Instruction: Create a notebook called "finance_advisor_no_memory.ipynb" with a finance advisor agent that tracks spending by category and gives budget advice. Do NOT add memory/session — each query should be independent. Before choosing a model, search online to verify the latest available OpenAI models. Use the exact model specified — do not substitute without confirming.

Input:
- Agent name: "Finance Advisor"
- Model: gpt-5-mini
- Test query 1: "I spent $120 on groceries, $40 on Uber, and $60 on restaurants this week."
- Test query 2: "My weekly budget is $250. Based on everything I told you so far, where can I cut spending next week?"

Output: A complete .ipynb file with environment setup (dotenv), agent definition, and two test queries in separate cells. Set the notebook kernel to "venv" so it auto-selects the virtual environment kernel in VS Code.
```
