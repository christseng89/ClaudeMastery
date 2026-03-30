# Prompt 3: Practice — Build a Wellness Coach Agent

Build a **Wellness Coach** agent that suggests one simple health habit per week.

- **Agent name:** "Wellness Coach"
- **Model:** `gpt-5-mini`
- **Behavior:** Suggests exactly ONE realistic health habit per reply, never repeats previous suggestions, supportive tone
- **Memory:** Use `SQLiteSession` so it remembers across messages
- **Test with two messages:**
  - Message 1: `"My name is Tamara. I work long hours at a desk and feel low energy in the afternoon. Suggest one simple health habit I can try next week."`
  - Message 2: `"Assume I successfully followed your first habit for one week. Suggest a NEW habit for the following week that builds on my progress (do not repeat the previous habit)."`


# Solution:

```
Context: Building a Jupyter notebook using the OpenAI Agents SDK to create a wellness coaching agent with memory.

Instruction: Create a notebook called "wellness_coach.ipynb" with a Wellness Coach agent that suggests exactly one small, realistic habit per reply. It should remember past suggestions and never repeat them. Before choosing a model, search online to verify the latest available OpenAI models. Use the exact model specified — do not substitute without confirming.

Input:
- Agent name: "Wellness Coach"
- Model: gpt-5-mini
- Memory: SQLiteSession
- Test message 1: "My name is Tamara. I work long hours at a desk and feel low energy in the afternoon. Suggest one simple health habit I can try next week."
- Test message 2: "Assume I successfully followed your first habit for one week. Suggest a NEW habit for the following week that builds on my progress (do not repeat the previous habit)."

Output: A complete .ipynb notebook with environment setup, agent with memory, and two test messages in the same session. Set the notebook kernel to "venv".
```


