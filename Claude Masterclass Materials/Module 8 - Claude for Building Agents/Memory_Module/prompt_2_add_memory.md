# Prompt 2: Add Memory to the Agent

Copy and paste the following into Claude Code:

```
Context: We have "finance_advisor_no_memory.ipynb" with a working Finance Advisor agent that has no memory. The agent forgets everything between queries.

Instruction: Add a new "Task 3" section that demonstrates memory using SQLiteSession. Keep the existing no-memory section for comparison. The agent should now remember expenses from the first message when answering the second. Before choosing a model, search online to verify the latest available OpenAI models. Use the exact model specified — do not substitute without confirming.

Input:
- Same two test queries, now with memory enabled:
  1. "I spent $120 on groceries, $40 on Uber, and $60 on restaurants this week."
  2. "My weekly budget is $250. Based on everything I told you so far, where can I cut spending next week?"

Output: Updated notebook with a new section showing side-by-side comparison — without memory vs. with memory.
```
