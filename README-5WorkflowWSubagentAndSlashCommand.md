# Advanced Workflow with Subagent and Slash Command

RESOURCES:

<https://github.com/firstlink/claude-code/blob/main/slash-commands-and-agents/.claude/commands/api-review-and-commit-workflow.md>

```bash
cat << 'EOF' > .claude/commands/api-review-and-commit-workflow.md
# API Review and Commit Workflow

You are tasked with orchestrating a complete API review and git commit workflow.

## Workflow Steps

### Step 1: Launch API Reviewer Agent

- Use the Task tool with the following parameters:
  - `subagent_type`: "api-reviewer"
  - `description`: "Review expense tracker API"
  - `prompt`: "Review all API endpoints, request/response schemas, and API documentation in the expense-tracker application. Analysis for best practices, security vulnerabilities, usability issues, and design patterns. Provide specific, actionable recommendations for improvements with code examples where applicable."

### Step 2: Process and Present Findings

- Wait for the api-reviewer agent to complete
- Analysis the findings and categories them:
  - Critical security issues
  - Design/architecture concerns
  - Best practice violations
  - Usability improvements
- Present a clear summary to the user with:
  - Number of issues found by category
  - Specific file locations affected
  - Priority recommendations

### Step 3: User Confirmation

- Ask the user if they want to proceed with the git commit workflow
- If critical issues are found, recommend addressing them first
- Wait for user approval before proceeding

### Step 4: Execute Git Commit

- Once approved, use the SlashCommand tool to execute: `/auto-commit`
- Allow the git commit workflow to complete
- Confirm final status to the user

## Important Guidelines

- Always wait for each step to fully complete before proceeding
- Never skip the user confirmation step
- If the api-reviewer agent fails, do not proceed to git commit
- Provide clear, actionable feedback at each stage
EOF

claude
  /clear
  /api-review-and-commit-workflow
```

```cmd
pytest test_api.py -v
python api_main.py
```

```bash
claude

The api-review-and-commit-workflow Slash Command is not working after commit, both
  - pytest test_api.py -v and
  - python api_main.py  are no longer working.

  Update this slash command to do the test for the two test in advance, if it is working then update the README.md as      
  well to compliance with changes.  After all the above mentioned, then do the /auto-commit slash command.

/clear
```

## **Claude Code 的 Slash Commands 與 Subagents** 的Summary

---

## 1 Slash Commands 是什麼？（用來「快速捷徑」）

* **本質**：寫在專案裡的「預先寫好的提示模板（prompt template）」Markdown 檔。
* **放哪裡**：`.claude/commands/` 目錄，檔案格式 `.md`。
* **怎麼跑**：輸入 `/command-name`，模板內容會**直接送到同一個主 Claude instance**，並共享同一份對話 context；可用 `$ARGUMENTS` 帶參數。

適合：你每天都會重複做的固定流程（例如 `/test`、`/format`、`/deploy` 這種）。

---

## 2 Subagents 是什麼？（用來「獨立分工 / 深度調查」）

* **本質**：啟動一個**獨立的 Claude instance**，和主對話分開跑，擁有**隔離的 context**。
* **核心目的**：把「研究、查證、深度分析」丟給 subagent 做，避免污染主對話的 context 與 token。
* **強項**：可平行處理、隔離上下文、適合深度研究/驗證。
* **代價**：會有額外 API 呼叫、成本更高（因為多開 instance）。

適合：你想「一邊主線開發，一邊讓 subagent 去查文件、驗證安全性、確認 best practices」。

---

## 3 直接對照：Slash Commands vs Subagents

| 面向       | Slash Commands          | Subagents                        |
| -------- | ----------------------- | -------------------------------- |
| 執行方式     | 同一個主 Claude instance    | 另外開一個 Claude instance            |
| Context  | 共享主對話                   | 隔離 context                       |
| 平行處理     | 不行                      | 可以                               |
| Token/成本 | 用主對話 token；無額外呼叫        | 自己的 token 預算；額外 API calls        |
| 最適用      | 重複性、模板化任務               | 深度研究、查證、避免污染主線                   |
| 設定方式     | `.claude/commands/*.md` | 內建機制（你請 Claude “use a subagent”） |

---

## 4 什麼時候用 Slash Commands？

用在：

* **重複工作流**：你開發流程中常常要跑的事情（測試、格式化、部署）。
* **簡單明確任務**：不需要深入調查的操作。
* **節省打字**：把常用 prompt 固定化。

典型例：

* `/test` 跑測試
* `/format` 修格式
* `/deploy` 部署

---

## 5 什麼時候用 Subagents？

用在：

* **深度調查 / 研究**：例如「查官方文件是否推薦這種 API pattern」。
* **需要驗證（verification）**：例如「請 subagent 檢查安全性影響、OWASP API 風險」。
* **平行研究**：你主線在改 code，同時讓 subagent 去查資料。
* **主對話快到 token 極限**：把研究丟出去，主線保持乾淨。

/test
/deploy
/format

---

## 6 最實用的建議（官方風格總結）

* **Slash Commands：重在效率與重複**（每天用的 90% 任務）。
* **Subagents：重在 context 管理與平行工作**（深度研究/驗證、或接近 token 上限時用）。

---
