# 如何使用 Trade Finance Skill

## ✅ 安裝成功！

你的 **trade-finance** skill 已經正確安裝在：
```
/mnt/skills/user/trade-finance/
```

## 🎯 使用方式

### **方法 1: 自動觸發（推薦）**

當你的任務涉及貿易融資相關內容時，Claude Code 會自動讀取這個 skill：

```bash
# Claude 會自動使用 trade-finance skill
claude "審核這份信用狀單據是否符合 UCP 600"
claude "檢查這個 MT700 SWIFT 訊息格式"
claude "分析提單的不符點"
```

### **方法 2: 明確指定 Skill**

你也可以明確告訴 Claude 使用這個 skill：

```bash
claude "使用 trade-finance skill 來審核這些文件"
```

### **方法 3: 在對話中使用**

```
User: 我有一份信用狀需要審核
Claude: [自動讀取 /mnt/skills/user/trade-finance/SKILL.md]
        好的，我會按照 UCP 600 標準進行審核...
```

## 📋 Skill 包含的功能

根據 SKILL.md，這個 skill 會指導 Claude：

1. ✅ **信用狀基本資訊驗證**
   - L/C 編號、日期、金額、當事人等

2. ✅ **單據一致性檢查**
   - 商業發票、提單、裝箱單、保險單的交叉比對

3. ✅ **運輸單據審核**
   - 提單類型、批註、簽署、份數確認

4. ✅ **SWIFT 訊息驗證**
   - MT700/MT710 格式檢查

5. ✅ **不符點分類**
   - 致命性 → 重大 → 輕微
   - 自動產生處理建議

6. ✅ **審核報告生成**
   - 符合銀行標準的正式報告格式

## 🔧 客製化 Skill

如果你想修改或擴充這個 skill：

```bash
# 編輯主要技能文件
nano /mnt/skills/user/trade-finance/SKILL.md

# 或使用 Claude Code
claude "幫我在 trade-finance skill 中加入 MT710 修改電文的檢查規則"
```

## 📊 測試 Skill

使用提供的範例資料測試：

```bash
# 查看範例資料
view /mnt/skills/user/trade-finance/examples.md

# 測試審核功能
claude "用 examples.md 中的 TEST-001 案例測試 skill"
```

## 🚀 進階整合

### 與 Git Hooks 整合

建立 `.claudecodehooks/pre-commit`：

```yaml
name: Trade Finance Document Check
on: commit
skill: trade-finance

steps:
  - validate_lc_documents
  - check_ucp600_compliance
  - generate_report
```

### 與 Python 程式整合

```python
# 直接使用工具函式
import sys
sys.path.append('/mnt/skills/user/trade-finance')
from utils import UCP600Validator

validator = UCP600Validator()
# ... 你的程式碼
```

## 📝 Skill 文件結構

```
/mnt/skills/user/trade-finance/
├── SKILL.md       # 核心技能指導（Claude 會讀這個）
├── examples.md    # 測試資料範例
└── utils.py       # Python 輔助工具
```

## ⚠️ 重要提醒

1. **只有 SKILL.md 是必需的**
   - Claude Code 主要讀取 SKILL.md
   - examples.md 和 utils.py 是輔助檔案

2. **Skill 不會自動更新**
   - 修改後需要重新啟動 Claude Code session（如果適用）
   - 或明確告訴 Claude 重新讀取 skill

3. **多個 Skills 可以同時使用**
   - 例如同時使用 docx skill + trade-finance skill
   - Claude 會根據任務需求選擇合適的 skill

## 🎓 學習資源

- **UCP 600**: 國際商會跟單信用狀統一慣例
- **ISBP 745**: 國際標準銀行實務
- **SWIFT Standards**: MT700/MT710 訊息格式規範

---

**Skill 版本**: 1.0  
**建立日期**: 2025-01-19  
**維護者**: Chris Tseng  
**下次檢視**: 2025-07-19
