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

## Create an Agent

```bash
claude

  /agents
    Create new agent
    
    1. Generate with Claude (recommended)

  /clear
  quit
```

```text
You are travel activity planner agent. Your goal is to research and find cool things to do at the destination, including activities and events that match the traveler's interests and age group.

You are skilled at creating personalized itineraries that cater to the specific preferences and demographics of travelers.  Research and find cool things to do at the destination.

Focus on activities and events that match the traveler's interests and age group. 

Utilize internet search tools and recommendation engines to gather the information.

expected_output:

A list of recommended activities and events for each day of the trip.

Each entry should include the activity name, location, a brief description, and why it's suitable for the traveler. And potential reviews and ratings of the activities.
```

## Travel Activity Planner Subagent

```bash
claude

  What are the different agents available?

  travel-activity-planner I am visiting New York in the month of June with my family. I have 2 boys age 7 and 9. They like outdoor activity. Can you help me plan the trip?

/clear
```

## Restaurants Recommendation Subagent

```bash
claude

  /agents
    Create new agent
    1. Project (.claude/agents/) 
    1. Generate with Claude (recommended)

```

```text
You are a Restaurant Scout agent.

Your goal is to find highly-rated restaurants and dining experiences at the destination, and recommend scenic locations and fun activities.

As a food lover, you know the best spots in town for a delightful culinary experience.
```

```bash
claude
  list all available agents
  restaurant-scout Give me the top 5 restaurants in Taipei City.
/clear

```

## Run Agents in Parallel

```bash
claude
  List all available agents
  What are different ways to run multiple agents?
  travel-activity-planner restaurant-scout I am visiting Taipei city with family in March. I have 2 teen agers age 15 and 18. Can you help me plan the itinerary

```

### Claude Response

```markdown
# Claude Response

## 1. List of all agents

● Complete List of Available Agents

  Built-in Agents (Always Available)

  1. general-purpose

  - Model: Sonnet
  - Tools: All tools (*)
  - Purpose: Complex, multi-step tasks requiring exploration AND action
  - Use: Automatically invoked for complex tasks that need both reading and writing

  2. Explore

  - Model: Haiku (fast)
  - Tools: Read-only (Glob, Grep, Read, Bash - limited)
  - Purpose: Fast, lightweight codebase searching and analysis
  - Thoroughness: Quick, Medium, or Very Thorough
  - Use: When you need to search/understand code without changes

  3. Plan

  - Model: Sonnet
  - Tools: Read-only (Read, Glob, Grep, Bash)
  - Purpose: Research and planning in plan mode
  - Use: Automatically invoked when in plan mode for codebase research

  ---
  Your Custom Project Agents

  4. travel-activity-planner

  - Model: Sonnet
  - Tools: All tools
  - Location: .claude/agents/travel-activity-planner.md
  - Purpose: Personalized travel activity recommendations
  - Auto-invokes: When planning trips, asking about activities, creating itineraries

  5. restaurant-scout

  - Model: Sonnet
  - Tools: All tools
  - Location: .claude/agents/restaurant-scout.md
  - Purpose: Restaurant recommendations and dining experiences
  - Auto-invokes: When asking about restaurants, food, places to eat

  ---
  How to View/Manage All Agents

  /agents

  This interactive command lets you:
  - View all available agents (built-in, user, project, plugin)
  - Create new agents
  - Edit existing agents
  - Delete custom agents
  - Configure tool permissions

  ---
  Agent Storage Locations

  | Type     | Location                   | Scope                 |
  |----------|----------------------------|-----------------------|
  | Project  | .claude/agents/*.md        | Current project only  |
  | User     | ~/.claude/agents/*.md      | All your projects     |
  | Plugin   | Plugin's agents/ directory | When plugin installed |
  | Built-in | Internal to Claude Code    | Always available      |

  ---
  How to Invoke Agents

  Automatic (recommended):
  > Find restaurants in Paris
  > Plan a Tokyo itinerary
  > Search for authentication code

  Explicit:
  > Use the restaurant-scout agent to find dining in Barcelona
  > Use the Explore agent to search for error handling code

  ---
  Want to create a new agent? Run /agents and select "Create New Agent"!

## 2. Different Ways to Run Multiple Agents
● Here are all the different ways to run multiple agents in Claude Code:

  1. Automatic Delegation (Easiest)

  Claude automatically invokes the right subagent based on your request:
  > review my code for security issues
  > run tests and fix failures
  Claude picks the appropriate subagent based on task description and context.

  2. Explicit Invocation (Sequential)

  Request specific subagents by name:
  > Use the code-reviewer subagent to check the auth module
  > Have the debugger subagent investigate login issues

  3. Subagent Chaining (Sequential)

  Chain multiple subagents for multi-step workflows:
  > First use code-analyzer to find performance issues, then use optimizer to fix them

  4. Parallel Sessions (Git Worktrees)

  Run multiple independent Claude instances simultaneously:
  git worktree add ../project-feature-a -b feature-a
  git worktree add ../project-bugfix -b bugfix-123

  # In separate terminals
  cd ../project-feature-a && claude
  cd ../project-bugfix && claude

  5. Resumable Agents (Long-running)

  Resume agents across multiple invocations with preserved context:
  > Use code-analyzer to review the auth module
  [Returns agentId: abc123]

  > Resume agent abc123 and analyze authorization logic too

  6. Built-in Specialized Subagents

  - Explore - Fast codebase search (Haiku, read-only)
  - Plan - Implementation planning (Sonnet)
  - General-purpose - Complex multi-step tasks (Sonnet)

  7. CLI Configuration (Session-specific)

  claude --agents '{"code-reviewer": {"description": "...", "model": "sonnet"}}'

  8. Background Bash Execution

  Run processes in background while Claude continues working:
  ! npm test &

  9. Project-level Subagents

  Create reusable agents in .claude/agents/:
  /agents  # View/create/edit agents

  10. Plugin-provided Subagents

  Install plugins that include pre-built agents.

  ---
  Quick Comparison

  | Method    | Execution  | Use Case             |
  |-----------|------------|----------------------|
  | Automatic | Sequential | General workflows    |
  | Explicit  | Sequential | Specific tasks       |
  | Chaining  | Sequential | Multi-step processes |
  | Worktrees | Parallel   | Separate features    |
  | Resumable | Spans time | Long analysis        |

  ---
  Your Current Setup

  You have two custom agents configured:
  - travel-activity-planner - Travel recommendations
  - restaurant-scout - Dining suggestions

  Invoke them by asking naturally:
  > Use travel-activity-planner to suggest Tokyo activities

  Or let Claude auto-delegate when appropriate!

  ## 3. Itinerary for Taipei City Trip

● Perfect! I've successfully run both agents in **parallel** to create your comprehensive Taipei itinerary. Here's what you now have:

  🎉 Your Complete Taipei Family Trip Plan (March 2026)

  📍 5-Day Activity Itinerary (from travel-activity-planner)

  Highlights:
  - Day 1: Ximending youth district + Huashan 1914 Creative Park + Shilin Night Market
  - Day 2: Jiufen Old Street day trip (Spirited Away vibes!) + Shifen sky lanterns
  - Day 3: Elephant Mountain hike + Taipei 101 Observatory + Maokong Gondola
  - Day 4: National Palace Museum + Gaming culture at Syntrend + Raohe Night Market
  - Day 5: Beitou Hot Springs + Xinyi shopping + Bubble tea challenge

  Perfect for teens: Instagram-worthy locations, adventure activities, authentic culture, and plenty of food!

  ---
  🍜 Complete Dining Guide (from restaurant-scout)

  Must-Try Experiences:
  1. Night Markets: Raohe (best food), Ningxia (Michelin stalls), Shilin (most famous)
  2. Hot Pot: Emperor Palace (unlimited Haagen-Dazs + massage chairs!)
  3. Iconic: Din Tai Fung soup dumplings (Michelin-starred)
  4. Bubble Tea Tour: Machi Machi, Xing Fu Tang, The Oolong Project
  5. Traditional Breakfast: Dan Bing, Soy Milk, Fan Tuan (super cheap!)

  Instagram Cafes: Coffee Lovers Planet, MoneyJump Carousel, Machi Machi

  ---
  💰 Budget Estimate (Per Person)

  - Daily: NT$1,500-2,500 (USD $50-80)
  - 5 Days Total: NT$7,500-12,500 (USD $240-400)
  - Excludes accommodation

  ---
  🌦️ March Weather

  - Temperature: 16-22°C (60-72°F)
  - 50% chance of rain - pack light jackets and umbrellas
  - Perfect for hot springs and creates atmospheric photos at Jiufen!

  ---
  ✨ Why This Works for Teenagers (15 & 18)

  - Modern culture + authentic experiences
  - Interactive dining (hot pot, conveyor belt sushi)
  - Adventure activities (hiking, gondola, sky lanterns)
  - Instagram-worthy spots everywhere
  - Safe, independent exploration opportunities
  - Vibrant food scene they'll love

  ---
  Both agents provided extensive details with practical tips, transportation info, cultural etiquette, and booking recommendations. You're all set for an amazing family trip to Taipei! 🎊

  Would you like me to help with anything specific like booking strategies, packing lists, or day-by-day timing adjustments?     

```

### 中文摘要

| 方法          | 執行方式 | 適用場景     |
|---------------|----------|--------------|
| 自動委派      | 順序執行 | 一般工作流程 |
| 明確指定      | 順序執行 | 精準任務     |
| 串接          | 順序執行 | 多階段流程   |
| Worktrees     | 平行     | 多功能並行   |
| 可恢復        | 跨時間   | 長時間分析   |

## Run Agents Sequential

```bash
/clear

I am visiting Taipei City in the month of March with my family. I have 2 teenagers age 15 and 18. I would like to first create a travel itinerary and then find restaurants in those areas. Please run the agent sequentially.

```
