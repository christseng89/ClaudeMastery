# Token 使用

**Skills（技能）—— 漸進式載入（progressive disclosure）**
Skills 是程序性知識，每個 skill 在未被調用前僅佔約 **30–50 tokens**，只有被**呼叫時才會完整載入。也就是說，session 開始時 Claude 只看得到每個 skill 的 `name` + `description`（metadata），真正的 SKILL.md 內容、腳本、參考文件是等到 Claude 判斷需要用時才載入。官方文件也確認：Skills 僅在被調用時載入，所以把專業指令搬進 skill 能讓基礎 context 變小。

**MCP —— 預設是一開始就全部載入**
MCP 工具定義會在對話開始前就全部載入。以 Anthropic 官方的例子，5 個 MCP server、58 個工具，在對話開始前就消耗約 55K tokens；再加上 Jira（單獨約 17K）很快就破 100K。Anthropic 內部甚至看過 134K tokens 的工具定義。這就是 MCP 被詬病「token 肥大」的原因。

**不過有個新轉折：Tool Search Tool**
Anthropic 推出的 Tool Search Tool 允許把 MCP 工具標記為 `defer_loading: true`，變成「按需發現」。Claude 一開始只看得到 Tool Search 本身和你標為關鍵的工具，其他要用時才展開定義，token 用量可**降低約 85%**。啟用後 MCP 就比較接近 Skills 的行為模式了。

**Subagents / Agents**
Subagent 是被主 agent 呼叫時才 spawn 出來，每個 teammate（subagent）有自己的 context window，token 用量與團隊規模大致成正比；但 spawn prompt、CLAUDE.md、MCP server、skills 都會從一開始就載入該 subagent 的 context。所以 subagent 本身是「**調用時才啟動**」，但它一旦啟動，就會背負它自己那份 MCP 的開銷。

---

**一句話總結給你：**

| 機制 | Session 開始時 | 調用時 |
|---|---|---|
| **Skills** | 只載入 metadata（~30–50 tokens/個） | 載入完整內容 |
| **MCP（預設）** | 全部工具定義載入（動輒幾萬～十幾萬 tokens） | 無額外載入成本 |
| **MCP + Tool Search** | 只載入搜尋工具本身 | 找到才展開工具定義 |
| **Subagents** | 不佔主 context | spawn 後有自己的 context（含 MCP 全開銷） |

所以你的理解 **「Skills 調用時才算，MCP 一開始就算」** 方向正確，只要記住兩個例外：

1. Skills 有 metadata 小額開銷（但極小）
2. MCP 可透過 Tool Search 改成 on-demand

以你目前工作在處理參數系統 bugs + 學 AI Agent 的情境，如果你要設計 agent 架構，通用原則是：**優先用 Skills 封裝程序性知識（怎麼做），MCP 只用於真的需要外部連線的地方（GitHub、DB、API）**，然後開 Tool Search 把不常用的工具 defer 掉。這樣就能在保持靈活性的同時，最大程度減少 token 開銷，讓 agent 更高效地運作。
