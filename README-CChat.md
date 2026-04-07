# Claude Chat

## Example

```prompt
List the top 10 largest banks in the US by assets in 2025 and show their revenues.
Show the results in a bar chart
```

## Prompt Components

### 1. Context

Set the scene, who is the AI, what's the situation?

**Example:**
You are a **Smart Home Energy Advisor** who helps homeowners reduce energy use.

---

### 2. Instruction

A clear statement of the desired goal.

**Example:**
When given a household prompt, **provide practical, prioritized advice**.

---

### 3. Input Data

The data or content to analyze.

**Example:**
You will receive a question about energy usage or device efficiency.

---

### 4. Output Indicator

Define the expected format and structure.

**Example:** Respond with:

1. A short, clear recommendation list (2–4 bullets)
2. One quick win that can be done today

## Prompt Engineering

```md
# 🧠 1. Zero-shot Prompting

**Definition:**
You give the model a task **without any examples**. It relies purely on its pre-trained knowledge.

## ✅ When to use

* Simple or well-known tasks
* You want fast, minimal prompts

## 📌 Example Prompt

```text
Summarize the following financial statement in 3 bullet points:

[Insert financial statement here]
```

## 💡 Another Example (your domain – Trade Finance)

```text
Explain the difference between MT700 and MT760 in SWIFT.
```text end

```

```md
# 🧠 2. Few-shot Prompting

**Definition:**
You provide **a few examples** to guide the model’s behavior, format, or reasoning.

## ✅ When to use

* You want **consistent format**
* Domain-specific logic (e.g., banking, ESG, CBPR+)
* Reduce ambiguity

## 📌 Example Prompt

```text
Classify the sentiment of the following sentences:

Sentence: "The service was excellent."
Sentiment: Positive

Sentence: "The system failed during peak hours."
Sentiment: Negative

Sentence: "The onboarding process was smooth."
Sentiment:
```

## 💡 Trade Finance Example

```text
Convert SWIFT MT messages to business meaning:

MT Message: MT103
Meaning: Customer Credit Transfer

MT Message: MT700
Meaning: Issue of Documentary Credit

MT Message: MT202
Meaning:
```text end
```

```md
# 🧠 3. Chain-of-Thought (CoT) Prompting

**Definition:**
You instruct the model to **reason step-by-step** before giving the final answer.

👉 This improves performance on:

* Complex logic
* Calculations
* Multi-step workflows

---

## ✅ When to use

* Financial calculations
* Compliance analysis
* Architecture design
* AI agent workflows (your use case 👍)

---

## 📌 Basic CoT Prompt

```text
A company has revenue of $1M, costs of $600K, and taxes of $100K.

Think step by step and calculate the net profit.
```

---

## 📌 Structured CoT Prompt (Better)

```text
Analyze the following scenario step by step:

Company Financials:
- Revenue: $1,000,000
- Costs: $600,000
- Taxes: $100,000

Steps:
1. Calculate gross profit
2. Subtract taxes
3. Provide final net profit

Final Answer:
```

---

## 💡 ESG - Trade Finance / AI Architecture Example (Advanced)

```text
A bank wants to implement ESG scoring into its trade finance system.

Think step by step:
1. Identify data sources (internal + external ESG APIs)
2. Define how ESG score integrates into LC workflow
3. Suggest architecture (microservices + API layer)
4. Identify risks and compliance considerations

Final Answer:
Provide a structured solution.
```text end
```

```md
# 🔥 Bonus: Chain-of-Thought + Few-shot (Best Practice)

👉 This is what top AI teams use

```text
Example 1:
Problem: A = 10, B = 5
Step-by-step:
- Add: 10 + 5 = 15
Answer: 15

Example 2:
Problem: A = 20, B = 3
Step-by-step:
- Add: 20 + 3 = 23
Answer: 23

Now solve:

Problem: A = 7, B = 8
Step-by-step:
```text end
```

```md
# 🚀 Quick Comparison

| Type             | Use Case                 | Strength      | Weakness        |
| ---------------- | ------------------------ | ------------- | --------------- |
| Zero-shot        | Simple tasks             | Fast, minimal | Less control    |
| Few-shot         | Formatting, domain logic | Consistency   | Longer prompt   |
| Chain-of-Thought | Complex reasoning        | Accuracy      | Slower, verbose |

---

# 🎯 Pro Tip (Based on your use cases)

For your **AI Agent / Banking / ESG / CBPR+ work**, best pattern is:

👉 **Few-shot + Chain-of-Thought + Structured Output**

Example:

```text
Role: Trade Finance AI Advisor

Instructions:
- Think step by step
- Follow the format strictly

Output:
1. Analysis
2. Recommendation
3. Risks
```text end
```
