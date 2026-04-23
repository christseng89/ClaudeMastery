# Claude Chat

## Measuring AI’s ability to complete long tasks

<https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/>

- Linear scale
- 80% success

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

## 3.1 📌 Basic CoT Prompt

```text
A company has revenue of $1M, costs of $600K, and taxes of $100K.

Think step by step and calculate the net profit.
```

---

## 3.2 📌 Structured CoT Prompt (Better)

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

## 3.3 💡 ESG - Trade Finance / AI Architecture Example (Advanced)

```text
You are a Trade Finance and SCF expert tasked with integrating a 3rd party ESG solution. A bank wants to implement ESG scoring into its Trade Finance and SCF system.

Think step by step:
1. Identify data sources (internal + external ESG APIs)
2. Define how ESG score integrates into LC workflow
3. Using a 3rd party ESG API integration, outline the scoring process
4. Suggest architecture (microservices + API layer)
5. Identify risks and compliance considerations

Final Answer:
Provide a structured solution.
```text end
```

```md
## 3.4 🔥 Bonus: Chain-of-Thought + Few-shot (Best Practice)

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
## 3.5 🚀 Quick Comparison

| Type             | Use Case                 | Strength      | Weakness        |
| ---------------- | ------------------------ | ------------- | --------------- |
| Zero-shot        | Simple tasks             | Fast, minimal | Less control    |
| Few-shot         | Formatting, domain logic | Consistency   | Longer prompt   |
| Chain-of-Thought | Complex reasoning        | Accuracy      | Slower, verbose |

---

## 3.6 🎯 Pro Tip (Based on your use cases)

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

---

## 🔬 Deep Research Mode in Claude

```prompt
Context:

You are a Ph.D. researcher specializing in next-generation electric vehicle (EV) technologies. Your organization is seeking a comprehensive, forward-looking briefing on state-of-the-art battery innovations that are expected to significantly impact EV performance, charging speed, safety, and sustainability over the 2025–2030 horizon.

Instruction:

Conduct an in-depth review and synthesis of emerging EV battery technologies projected to reach technical or commercial maturity between 2025 and 2030. Your focus should include, but is not limited to, the following areas:

    ● Solid-state batteries (including lithium metal and composite variants)
    ● Next-generation electrolytes supporting ultra-fast charging
    ● High-performance sodium-ion and sodium solid-state batteries
    ● Battery-swapping technologies and evolving recycling ecosystems

Include analysis of:

    ● Key performance metrics (energy density, cycle life, charging speed, safety improvements)
    ● Commercialization timelines and scalability
    ● Notable industry players and research institutions driving development
    ● Critical challenges and readiness levels (TRLs)

Input:
 This is a standalone task. No external input will be provided.

Output:
 Deliver a detailed briefing report that includes:

    ● Technology name and associated company/institution
    ● Breakthrough or innovation summary
    ● Quantitative performance indicators (e.g., Wh/Kg, charge time, safety benchmarks)
    ● Implementation timeline and current stage of commercialization

The goal is to equip stakeholders with a clear understanding of transformative battery technologies shaping the EV landscape by 2030.
```

## Claude Chat for Creative Writing

```text
● Creative writing:
    ● Write a professional e-mail to Richard Marino who is the owner of a famous Italian restaurant in Toronto, Canada, offering content creation services to his restaurant. Highlight my value in content creation and marketing.

    ● Write a professional email to Richard Marino, who is the owner of a famous Italian restaurant in Toronto, Canada, offering content creation services to his restaurant. Highlight my value in improving their audience reach, mention 2 examples of content I can deliver, and end with a clear invitation to connect.

    ● Turn this into a poem
    ● Turn this into an Instagram post with hashtags
```

## Claude Chat for Brainstorming

```text
● Brainstorm ideas:
    ● Imagine you are on Tesla’s innovation team in the year 2030. Brainstorm 5 futuristic features that could make riding in a fully autonomous Tesla not just convenient, but genuinely fun, immersive, and memorable for passengers.

```

Output:

- EV_Battery_Briefing_EN.docx
- EV_Battery_Briefing_CN.docx

## Develop Dashboards Using Claude Front End Design Skill

```text
● Data Analysis & Dashboard Visualization
    ● Create 10 different data visualizations to highlight various aspects of the dataset. Include interactive charts. “Upload Cancer datasets”
```

Input: cancer.csv

Output: cancer_dashboard.html

## Extract Nvidia Financial Data from PDF to Excel and PowerPoint

```text
● Information Extraction & Research Assistance:
    ● What are the main revenue sources for Nvidia? “Attach Nvidia-10K-Report.pdf”
        ● Convert it into PowerPoint 
        ● Put the results in Excel

    ● Extract the balance sheet from the 10K document and summarize it in a tabular format.
        ● Convert it into PowerPoint 
        ● Put the results in Excel
```

- Input: Nvidia-10K-Report.pdf

## Financial Data Analysis and One Pager Summary Generation with PPTX Skills

```text
● Financial Data Analysis:
    ● Analyze this company’s financial and identify potential liquidity risks. (attach “Financial_Statement.csv” file)
    ● 流动比率 营运资本 资产负债率 净利润率 公式是甚麼? 如何算出的?
    ● Convert all the above mentioned into a Powerpoint
```

Input: Financial_Statement.csv
Output: Financial_Statement_风险分析报告.pptx

## Learn with Claude Chat

```text
嗨 Claude！你可以設計一些反思練習嗎？如果你需要我提供更多資訊，請先直接問我 1–2 個關鍵問題。如果你覺得我應該提供更多背景資訊請直接問我 1–2 個關鍵問題，然後再根據我的回答設計反思練習。
```

```text
一個自己公司開發的參數驅動系統  (UI + JS + MS) 設參後交易測試時一堆BUGS，工作負擔過重。 如何使用AI來更有效的處理問題? 例如使用 Source code + 參數規格 等?
```

```text
● Problem-Solving
    ● Show a detailed step-by-step solution to this problem, and show the equations  “attach problem_solving.pdf”
```

## Code with Claude Chat

```text
Fix the bug in this code below and explain the issue. 

● </>Code: Debugging

    def add_numbers(num1, num2):
        """Returns the sum of two numbers."""
        return num1 + num2

    # Usage:
    result = add_numbers(5, 10
    print(f"The sum is: {result}")

```

```result
# ✅ 完整修正後的程式碼
def add_numbers(num1, num2):
    """Returns the sum of two numbers."""
    return num1 + num2

# Usage:
result = add_numbers(5, 10)  # ← 補上右括號
print(f"The sum is: {result}")
```

```text
● Creative Image Generation (Try with Gemini for comparison):
    ● Generate an epic panoramic illustration featuring the New Seven Wonders of the World together in one majestic landscape: the Great Wall of China winding across distant mountains, the rose-red cliffs of Petra with its carved Treasury, the towering Christ the Redeemer statue overlooking the scene, Machu Picchu perched high in the Andes with misty clouds, the pyramid of Chichen Itza rising in the foreground, the grand Roman Colosseum standing strong, and the glowing white Taj Mahal reflecting in a pool. The Great Pyramid of Giza is shown nearby under golden sunlight as an honorary wonder. The entire scene is unified in a dramatic, cinematic style with vibrant colors, warm light, and awe-inspiring scale.

```
