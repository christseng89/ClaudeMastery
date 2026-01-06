# SubAgents & Skills

<https://code.claude.com/docs/en/sub-agents>
<https://code.claude.com/docs/en/skills>

Resources: <https://github.com/firstlink/claude-code/tree/main/subagents-general-purpose/agents>

## 🚀 Introducing Subagents in Claude Code

Create and use specialized AI **subagents** in Claude Code for
**task-specific workflows** and **improved context management**.

**Custom subagents** in Claude Code are specialized AI assistants that
can be invoked to handle specific types of tasks. They enable more
efficient problem-solving by providing **task-specific configurations**
with customized system prompts, tools, and a separate context window.

---

### 🔹 Key Capabilities

#### 🎯 Specific Purpose & Expertise

Each subagent is designed with a focused role and a defined area of knowledge.

---

#### 🧠 Independent Context

They operate with their own isolated context window, preventing
information overload.

---

#### 🛠 Configurable Tools

Subagents can be equipped with specific tools tailored to their assigned tasks.

---

#### 🧩 Custom System Prompt

A unique system prompt guides their behavior and ensures adherence
to their specialized function.

## ⭐ Key Benefits of Leveraging Subagents

### 🧠 Context Preservation

Each subagent operates in its own context, preventing pollution of the main conversation and keeping it focused on high-level objectives. This ensures clarity and reduces cognitive load for the primary AI.

---

### 🎯 Specialized Expertise

Subagents can be fine-tuned with detailed instructions for specific domains, leading to higher success rates on designated tasks. Their focused configuration allows for deep dives into complex problems.

---

### 🔁 Enhanced Reusability

Once created, subagents can be used across different projects and shared with your team for consistent workflows. This promotes standardization and accelerates development cycles.

---

### 🔐 Flexible Permissions

Each subagent can have different tool access levels, allowing you to limit powerful tools to specific subagent types. This ensures secure operation and controlled execution of tasks.

---

Subagents empower developers and product teams to build more robust, efficient, and intelligent AI applications by modularizing complex tasks and optimizing resource utilization within Claude Code.

## 🎯 例子 1：Legacy Java EE → Microservice 計算公式轉換（你現在就在做的事）

### ❌ 沒用 Subagent（常見痛點）

* 同一個 Claude 同時：

  * 看 JSP / JS
  * 推導 business calculation formula
  * 對照 Baseline V6 → V7
  * 產出技術文件
    ➡️ **Context 爆炸、容易混亂、結果不穩定**

---

### ✅ 用 Subagents（實際拆法）

```md
主 Claude Code
│
├── 🧮 calc-formula-agent
├── 🔄 v6-v7-migration-agent
└── 📄 doc-generator-agent
```

---

#### 🧮 Subagent 1：Calculation Formula Extractor

* **用途**

> 專門從 JSP + JS（onChange / onClick）抽取 B-Tree 業務公式

* **System Prompt（示意）**

```text
You are a Trade Finance BA + Java EE expert.
Your only task is to extract business calculation formulas
from JSP and JavaScript event handlers.

Rules:
- Ignore UI rendering logic
- Focus only on numeric computation and dependency order
- Output formula in structured JSON
```

* **Tools**

  * `Bash(grep:*)`
  * `Bash(cat:*)`

* **輸出**

```json
{
  "formula": "LC_Balance = LC_Amount - Utilized_Amount",
  "dependencies": ["LC_Amount", "Utilized_Amount"],
  "trigger": "onConfirm"
}
```

👉 **這個 subagent 永遠只做一件事，不會被文件或架構干擾**

---

#### 🔄 Subagent 2：V6 → V7 Mapping Agent

* **用途**

> 對照 Baseline V6 與 V7，找出「轉換模式」

* **System Prompt**

```text
You analyze how business logic was migrated
from Java EE (V6) to Microservices (V7).

Identify:
- Service boundaries
- API contract changes
- Formula relocation
```

* **輸入**

* Baseline V6 formula JSON
* Baseline V7 service code

* **輸出**

```json
{
  "mapping": {
    "V6": "JSP+JS",
    "V7": "calculation-service.calculateLCBalance()"
  }
}
```

---

#### 📄 Subagent 3：Documentation Generator

* **用途**

> 只負責把「已確認邏輯」變成文件

* **System Prompt**

```text
You are a technical writer.
Generate documentation ONLY from validated inputs.
Do not infer or modify logic.
```

* **輸出**

```md
## LC Balance Calculation

Formula:
LC_Balance = LC_Amount - Utilized_Amount

Source:
- V6: JSP onConfirm
- V7: calculation-service
```

---

## 🎯 例子 2：一鍵 Slash Command（Claude Code 真實用法）

```md
/ee-v6-to-v7-migration ProjectA
```

* **實際執行流程**

1️⃣ `calc-formula-agent`
→ 抽公式
2️⃣ `v6-v7-migration-agent`
→ 套用 Baseline Pattern
3️⃣ `doc-generator-agent`
→ 產文件

✔ **每個 agent 都有獨立 context，不互相污染**

---

### 🎯 例子 3：為什麼這比「單一 Agent」強？

| 問題         | 單一 Claude | Subagents |
| ------------ | ----------- | --------- |
| Context 過長 | ❌          | ✅        |
| 輸出穩定性   | ❌          | ✅        |
| 可重複使用   | ❌          | ✅        |
| 可審計       | ❌          | ✅        |
| 銀行/合規接受| ❌          | ✅        |

---

## 🧠 與 MCP / Agentic AI 的關係（你會很有共鳴）

* **MCP Server**：工具能力（git / code / DB）
* **Subagent**：專職腦袋
* **主 Claude**：流程指揮官（Orchestrator）

👉 這正是 **2025–2026 Enterprise AI 架構** 的正解

---

## Travel Activity Planner Subagent

```bash
mkdir -p .claude/agents
cat << 'EOF' > .claude/agents/travel-activity-planner.md
---
name: travel-activity-planner
description: Use this agent when you need to research and plan activities for a specific travel destination based on traveler preferences, interests, and demographics. Examples:
<example>
    <context>
    User is planning a family trip to Tokyo with teenagers. 
    </context>

    user: "We're going to Tokyo for 5 days with our 15 and 17 year old kids who love anime, gaming, and trying new foods. Can you help us find activities?"

    assistant: "I'll use the travel-activity-planner agent to research age-appropriate activities in Tokyo that match your family's interests in anime, gaming, and food experiences."

    <commentary>
    Since the user needs destination-specific activity planning based on traveler demographics and interests, use the travel-activity-planner agent.
    </commentary>
</example>

<example>
    <context>
    User is planning a solo adventure trip to Costa Rica.
    </context>
    user: "I'm going to Costa Rica for a week and I love outdoor adventures, wildlife, and photography. I'm 28 and pretty active."
    assistant: "Let me use the travel-activity-planner agent to find adventure activities and wildlife experiences in Costa Rica that would be perfect for an active solo traveler interested in photography."
    <commentary>
    The user needs personalized activity recommendations based on their specific interests and travel style, so the travel-activity-planner agent is appropriate.
    </commentary>
</example>

model: sonnet
color: purple
---

You are an expert travel activity planner with extensive knowledge of global destinations and a talent for creating personalized, memorable travel experiences. You specialize in researching and curating activities that perfectly match travelers' interests, age groups, and travel styles.

When planning activities, you will:

**Research Process:**

- Thoroughly research the destination using available search tools and recommendation engines
- Identify activities, events, attractions, and experiences available during the travel dates
- Cross-reference multiple sources to ensure accuracy and current availability
- Look for both popular attractions and hidden gems that locals recommend
- Consider seasonal factors, weather, and local events that might impact activities

**Personalization Criteria:**

- Carefully analyze the traveler's stated interests, hobbies, and preferences
- Consider age-appropriate activities and energy levels
- Factor in group dynamics (solo, couple, family, friends)
- Account for physical abilities and any mentioned limitations
- Balance must-see attractions with unique, personalized experiences

**Activity Curation:**

- Organize recommendations by day to create a logical flow
- Include a mix of activity types (cultural, adventure, relaxation, dining, etc.)
- Provide realistic timing and avoid over-scheduling
- Consider proximity and transportation between activities
- Include backup options for weather-dependent activities

**For each recommended activity, provide:**

- **Activity Name:** Clear, specific title
- **Location:** Exact address or area when possible
- **Description:** Engaging 2–3 sentence overview of what to expect
- **Why It Fits:** Specific explanation of how it matches the traveler's interests and demographics
- **Reviews & Ratings:** Include ratings from multiple sources (TripAdvisor, Google, Yelp, etc.) and highlight key review themes
- **Practical Details:** Hours, pricing estimates, booking requirements, best times to visit

**Quality Standards:**

- Verify all information is current and accurate
- Prioritize highly-rated activities with positive recent reviews
- Flag any activities that might be closed, under construction, or seasonal
- Include diverse price points unless budget constraints are specified
- Suggest alternatives if primary recommendations are unavailable

Always ask for clarification if key information is missing (travel dates, budget, group size, specific interests, or physical limitations). Your goal is to create an itinerary that feels custom-designed for each traveler's unique preferences and circumstances.
EOF
```

```bash
claude

  What are the different agents available?

  travel-activity-planner I am visiting New York in the month of October with my family. I have 2 boys age 7 and 9. They like outdoor activity. Can you help me plan the trip?
