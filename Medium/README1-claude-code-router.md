# 我沒花一分錢就用了 Claude Code——以下是具體方法

**作者：Ayesha Mughal** · *2026 年 2 月 21 日* · 閱讀時間：6 分鐘

大家都以為使用 Claude Code 需要訂閱 Anthropic 的服務。並非如此。

我花了二十分鐘說服自己接受每月 20 美元的套餐，結果發現根本不需要。後來我深入研究，在 [Panaversity AI Agent Factory](https://panaversity.org) 的文件中找到了實際的設定方法，不到十分鐘就免費跑起來了。

有一個沒人事先告訴你的事實：**Claude Code 並不在乎 API 背後實際運行的是哪個模型。** 它只會與你指向的任何 URL 通訊。所以，如果你指向的是免費模型——比如 Gemini、DeepSeek，或 OpenRouter 上 30 多個模型中的任何一個——它的運作方式完全一樣。相同的技能、相同的 MCP 伺服器、相同的子代理，一切都相同。

讓我來詳細示範一下。

---

## ⚡ 首先——選擇你的武器

你有三個選項，它們並不相同。選擇前請先了解：

| | OpenRouter | Gemini | DeepSeek |
|---|---|---|---|
| **費用** | 免費（每日限額） | 免費（每日限額） | ~$0.028/M 代幣 |
| **模型** | 30+（Qwen、Llama、Gemini） | Gemini 2.5 Flash | DeepSeek 聊天 + 推理器 |
| **最適合** | 靈活性、實驗性 | 設置最簡單 | 質量穩定 |

> ⚠️ **很多人不知道的是：** Google 在 2025 年 12 月悄悄削減了 Gemini 的免費套餐——大多數模型的每日請求限制降低了 50% 到 80%。它仍然可用，但如果你要編寫大量程式碼，你會遇到瓶頸。OpenRouter 提供了更大的緩衝空間，因為當一個模型的配額用完時，你可以切換到另一個。

我將詳細介紹 OpenRouter——它最靈活，也是我每天都在使用的。Gemini 和 DeepSeek 的設定流程完全相同，只是設定檔不同。

---

## 🧱 幕後究竟發生了什麼

在操作終端之前，先了解它的架構，這能避免你之後遇到困惑。

```
你 → ccr code → Claude Code Router（本地）→ OpenRouter API → 免費模型
```

Claude Code 與運行在 3456 連接埠的本機路由器通訊。路由器會將 Claude 的請求轉換成後端模型所需的格式。就是這樣。無需任何破解或越獄——這完全是 Anthropic 生態系統官方文件中記錄的設定。

這個工具叫做 **claude-code-router**（`ccr`），它是開源的。

---

## 🛠️ 設定：OpenRouter + Claude Code

### 步驟 1：取得你的免費 OpenRouter 金鑰

1. 前往 [openrouter.ai/keys](https://openrouter.ai/keys)
2. 點選 **「建立金鑰」**——給它取任意名稱。
3. 複製它（以 `sk-or-v1-...` 開頭）

免費帳戶可存取 30 多款模型，每日有配額限制。無需信用卡。

### 步驟 2：安裝這兩個工具

```bash
npm install -g @anthropic-ai/claude-code @musistudio/claude-code-router
```

> **剛才發生了什麼：** 你安裝了 Claude Code（代理）和路由器（翻譯器）。兩者缺一不可。如果沒有路由器，Claude Code 會嘗試直接呼叫 Anthropic 的付費 API。

確認兩者都已安裝：

```bash
claude --version   # Claude Code v2.xx
ccr version        # 顯示版本號
```

### 步驟 3：建立設定檔

**Mac/Linux**——請貼上以下整個程式碼區塊：

```bash
mkdir -p ~/.claude-code-router ~/.claude
cat > ~/.claude-code-router/config.json <<"EOF"
{
  "log": true,
  "logLevel": "info",
  "host": "127.0.0.1",
  "port": 3456,
  "API_TIMEOUT_MS": 600000,
  "providers": [
    {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1",
      "api_key": "$OPENROUTER_API_KEY",
      "models": [
        "qwen/qwen-coder-32b-vision",
        "google/gemini-2.0-flash-exp:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "qwen/qwen3-14b:free"
      ],
      "transformer": {
        "use": ["openrouter"]
      }
    }
  ],
  "router": {
    "default": "openrouter,qwen/qwen-coder-32b-vision",
    "background": "openrouter,qwen/qwen-coder-32b-vision",
    "thinking": "openrouter,meta-llama/llama-3.3-70b-instruct:free",
    "longContext": "openrouter,qwen/qwen-coder-32b-vision",
    "longContextThreshold": 60000
  }
}
EOF
```

**Windows**——開啟記事本，將相同的 JSON 內容儲存到：
`%USERPROFILE%\.claude-code-router\config.json`

> **剛才發生了什麼：** 你告訴路由器使用哪些模型以及各自的用途。`default` 是日常編碼模型，`thinking` 是複雜推理任務模型，`longContext` 是處理大型文件的模型。路由器會自動在它們之間切換，你完全不用操心。

> 🚨 **請勿在設定檔中替換 `$OPENROUTER_API_KEY`**，保持原樣 `$OPENROUTER_API_KEY`。路由器會從你的環境變數中讀取該值（下一步）。如果你直接將金鑰貼到文件中，它無法正常運作，你會浪費 30 分鐘感到困惑。

### 步驟 4：永久設定你的 API 金鑰

**Mac（zsh）：**
```bash
echo 'export OPENROUTER_API_KEY="YOUR_KEY_HERE"' >> ~/.zshrc
source ~/.zshrc
```

**Mac（bash）：**
```bash
echo 'export OPENROUTER_API_KEY="YOUR_KEY_HERE"' >> ~/.bashrc
source ~/.bashrc
```

**Windows（PowerShell——以管理員身分執行）：**
```powershell
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'YOUR_KEY_HERE', 'User')
```
然後關閉所有 PowerShell 視窗，再開啟一個新的。

驗證是否有效：
```bash
echo $OPENROUTER_API_KEY  # 應該會印出你的金鑰
```

> **剛才發生了什麼：** 你把金鑰儲存在 shell 裡，這樣每次會話都會自動載入。如果沒有這樣做，每次打開終端都需要手動匯出金鑰——很容易忘記，然後納悶為什麼什麼都用不了。

### 步驟 5：日常工作流程（雙終端）

這是容易出錯的地方。**你需要兩個終端。**

**終端 1——啟動路由器：**
```bash
ccr start
```
稍等片刻，看到 ✅ `Service started successfully`。**請保持此視窗開啟。**

**終端 2——開始編碼：**
```bash
cd your-project-folder
ccr code
```

> **為什麼需要兩個終端？** 路由器是本機伺服器，必須保持運作。`ccr code` 指向的就是這個伺服器。如果終端 1 關閉，你的編碼會話也會終止。可以把終端 1 想像成引擎，終端 2 想像成駕駛座。

> ⏳ 首次啟動需要 10–20 秒。如果 `ccr code` 看起來卡住了，請不要驚慌，路由器正在初始化，耐心等待即可。

---

## ✅ 驗證是否正常運作

進入 Claude Code 後，輸入：

```
你好
```

如果有回應，則表示已連線。若要更深入地檢查：

```
請解釋此目錄中包含哪些檔案以及此專案的功能。
```

Claude 應該會讀取你的實際文件並做出回應。如果能做到——那麼你就擁有了一個基於免費模型且功能齊全的智能體編碼環境。

---

## 🔄 如果我想用 Gemini 或 DeepSeek 呢？

步驟完全相同，只需替換設定檔內容即可。

**Gemini**——從 [aistudio.google.com/api-keys](https://aistudio.google.com/api-keys) 取得金鑰，使用：

```json
"providers": [{
  "name": "gemini",
  "api_base_url": "https://generativelanguage.googleapis.com/v1beta/models/",
  "api_key": "$GOOGLE_API_KEY",
  "models": ["gemini-2.5-flash"],
  "transformer": { "use": ["gemini"] }
}]
```

環境變數：`GOOGLE_API_KEY`

**DeepSeek**——從 [platform.deepseek.com](https://platform.deepseek.com) 取得金鑰，使用：

```json
"providers": [{
  "name": "deepseek",
  "api_base_url": "https://api.deepseek.com/v1",
  "api_key": "$DEEPSEEK_API_KEY",
  "models": ["deepseek-chat", "deepseek-reasoner"],
  "transformer": { "use": ["openai"] }
}]
```

環境變數：`DEEPSEEK_API_KEY`

---

## 🚨 疑難排解（你實際上會遇到的錯誤）

**「command not found: ccr」**
npm 全域 bin 目錄不在你的 PATH 中。執行：

```bash
npm config get prefix
# 將輸出結果 + /bin 加入 ~/.zshrc 或 ~/.bashrc 的 PATH 中
```

**路由器啟動了，但 Claude 卡住不動**
你在 `ccr start` 完成之前就執行了 `ccr code`。關閉兩者，先重啟終端 1，等待成功訊息後，再啟動終端 2。

**「API key not found」**
你在某個終端會話中設定了變數，但沒有持久化。按照步驟 4 所示，將 `export` 加入你的 `~/.zshrc` 或 `~/.bashrc` 並執行 source。

**會話中途遇到速率限制**
在設定檔中將 `default` 模型切換為 OpenRouter 上另一個免費模型。你有 30 多個選項——輪流使用即可。

---

## 💡 誠實的評價

免費是否意味著與 Claude Sonnet 或 Opus 相同的質量？不。對於複雜的多步驟推理，付費的 Claude 模型更好。

但以下是我的實際發現：對於大多數真實的開發工作——閱讀程式碼庫、生成樣板程式碼、解釋錯誤、編寫測試——OpenRouter 上的免費模型已經足夠好用。Qwen-Coder-32B 在程式碼任務方面尤其出色，令人驚喜。

那些每月花 20 美元訂閱 Claude Pro 來使用 Claude Code 的人，主要是在為便利性和頂峰性能付費。如果你是在學習、實驗或建立個人專案——免費方案能帶你走完 90% 的路程。

**先從免費開始。等真正遇到瓶頸時再升級。**

---

## 📌 快速摘要

| 操作 | 方法 |
|---|---|
| 安裝兩個工具 | `npm install -g @anthropic-ai/claude-code @musistudio/claude-code-router` |
| 設定檔位置 | `~/.claude-code-router/config.json` |
| 設定 API 金鑰 | 匯出至 `~/.zshrc` 或 `~/.bashrc` |
| 啟動路由器 | `ccr start`（終端 1） |
| 開始編碼 | `ccr code`（終端 2） |
| 最佳免費選項 | OpenRouter——模型最多，最靈活 |

本設定基於 Panaversity AI Agent Factory 的官方免費設定指南——與 AI 代理黑客松中使用的課程相同。所有 Claude Code 功能（技能、MCP 伺服器、子代理、鉤子）在免費後端上的運作方式完全相同。

---

**最後的忠告：** 不要被「免費」這個詞嚇到。是的，這些模型有配額限制，但對於大多數開發者來說，這些限制非常寬鬆。你完全可以在不花一分錢的情況下體驗到 Claude Code 的強大功能。只要按照上述步驟操作，你就能輕鬆上手，開始你的 AI 編碼之旅！
