# 10 Must-Have Skills for Claude (and Any Coding Agent) in 2026》

對軟件公司 **SDLC 各階段**推薦使用的最佳實踐技能

---

## 📋 SDLC 各階段 × 文章推薦技能

---

### 1️⃣ 需求分析 & 系統設計階段

**🔧 `@brainstorming`（來自 Antigravity Awesome Skills）**
在編寫任何代碼之前，進行結構化規劃，幫助團隊釐清需求與設計思路。

**🔧 `@architecture`（來自 Antigravity Awesome Skills）**
負責系統設計與組件結構規劃，確保架構合理、可擴展。

**🔧 Excalidraw Diagram Generator**
將架構決策、系統設計、數據流以視覺化圖表呈現，自動生成可發布的架構圖，方便團隊溝通與文件存檔。

---

### 2️⃣ 開發階段

**🔧 Frontend Design**
生成生產級 UI，避免 AI 產出「千篇一律」的設計，確保用戶介面具備高質感與獨特風格。

**🔧 Code Reviewer / `simplify` Skill**
對 AI 或開發人員撰寫的代碼進行自動化審查，檢查：

- 可抽取的重複邏輯
- 違反單一職責的函數
- 性能低效問題（N+1 查詢、不必要的重渲染）
- 命名不清、死碼、未處理的 async 錯誤

**🔧 `@api-design-principles`（來自 Antigravity Awesome Skills）**
確保 REST API 的設計一致性、版本控制與良好的端點結構。

**🔧 PlanetScale Database Skills**
在資料庫設計時自動生成具備索引意識的 Schema，支持分支工作流（如 Git 般管理資料庫變更），避免日後難以回滾的架構錯誤。

**🔧 Valyu（真實數據接入）**
當開發需要接入 SEC 文件、PubMed、經濟指標等專業數據時，提供即時、權威的數據來源，而非依賴過期的訓練數據。

---

### 3️⃣ 測試階段

**🔧 Browser Use**
讓 AI Agent 直接控制瀏覽器，執行端對端測試（E2E Testing），例如自動化測試登入流程、表單填寫、截圖錯誤頁面，取代人工點擊測試。

**🔧 Shannon（自主 AI 滲透測試）**
對本地或 Staging 環境執行真實安全攻擊測試，涵蓋 50+ 種漏洞類型（SQL 注入、XSS、SSRF、身份驗證漏洞、IDOR 等），**96.15% 漏洞成功率**，且只報告已成功利用的漏洞（零誤報）。

**🔧 `@security-auditor`（來自 Antigravity Awesome Skills）**
在代碼審查階段進行安全焦點的代碼檢查。

**🔧 `@lint-and-validate`（來自 Antigravity Awesome Skills）**
輕量級的代碼質量檢查，確保代碼符合規範。

---

### 4️⃣ 部署 & 發布階段

**🔧 `@create-pr`（來自 Antigravity Awesome Skills）**
將開發工作自動打包成乾淨的 Pull Request，規範化代碼提交流程。

**🔧 PlanetScale Database Skills（持續整合）**
透過 `pscale` CLI 建立資料庫分支、創建 Deploy Request，確保每次 Schema 變更都可審查、可回滾，不直接接觸生產環境。

---

### 5️⃣ 維運 & 協作階段

**🔧 Google Workspace (GWS) Skills**
自動化 Google 生態系工作流程，包括：Gmail 草稿回覆、Calendar 會議管理、Sheets 任務追蹤、Docs 會議記錄，讓 AI Agent 真正融入日常運營。

**🔧 Remotion（視頻自動生成）**
用程式碼生成產品演示視頻、版本發布公告、說明影片，無需額外的影片製作工具，直接在代碼編輯器中完成。

**🔧 `@doc-coauthoring`（來自 Antigravity Awesome Skills）**
結構化生成技術文件，讓文件撰寫成為開發流程的一部分，而非事後補充。

**🔧 `@debugging-strategies`（來自 Antigravity Awesome Skills）**
系統化的除錯 Playbook，協助團隊在維運時快速定位與解決問題。

---

## 🗂️ 文章技能 × SDLC 對照總表

| 文章技能 | SDLC 適用階段 |
|---|---|
| Excalidraw Diagram Generator | 需求分析、系統設計 |
| `@brainstorming` / `@architecture` | 需求分析、系統設計 |
| Frontend Design | 開發 |
| Code Reviewer / `simplify` | 開發、測試 |
| `@api-design-principles` | 開發 |
| PlanetScale Database Skills | 開發、部署 |
| Valyu | 開發（數據驅動應用） |
| Browser Use | 測試（E2E） |
| Shannon | 測試（安全測試） |
| `@security-auditor` / `@lint-and-validate` | 測試 |
| `@create-pr` | 部署、發布 |
| Google Workspace (GWS) | 維運、協作 |
| Remotion | 發布、維運（文件與推廣） |
| `@doc-coauthoring` / `@debugging-strategies` | 維運 |
| Antigravity Awesome Skills（整體庫） | 貫穿全 SDLC |

---

## 📌 文章核心建議

文章強調：**「技能的價值在於改變 Agent 的預設行為，而非只是增加一個指令。」** 對於軟件公司 SDLC 而言，最值得優先安裝的是：

1. **Antigravity Awesome Skills**（一次安裝涵蓋 1,234+ 技能，貫穿全流程）
2. **Code Reviewer / simplify**（每個項目都應安裝，提升代碼質量）
3. **Browser Use**（自動化 E2E 測試）
4. **Shannon**（每次部署前的安全驗證）
5. **Excalidraw Diagram Generator**（架構文件的視覺化）

## 📊 完整交叉對照速查表

| SDLC 階段 | 對應文章技能 |
|---|---|
| **1. 需求分析** | `@brainstorming`、`Valyu`、`Browser Use` |
| **2. 系統設計** | `@architecture`、`Excalidraw`、`@api-design-principles`、`PlanetScale` |
| **3. 開發** | `Frontend Design`、`Code Reviewer`、`PlanetScale`、`Valyu`、`Remotion`、`GWS` |
| **4. 測試** | `Browser Use`、`Shannon`、`@security-auditor`、`@lint-and-validate`、`Code Reviewer` |
| **5. 部署發布** | `@create-pr`、`PlanetScale`、`Shannon`、`Remotion` |
| **6. 維運監控** | `@debugging-strategies`、`Browser Use`、`GWS` |
| **7. 文件協作** | `@doc-coauthoring`、`Excalidraw`、`Remotion`、`GWS` |
| **全 SDLC** | `Antigravity Awesome Skills`（涵蓋所有階段） |
