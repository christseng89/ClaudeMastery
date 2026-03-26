# 貿易融資文件審核技能 (Trade Finance Document Checking Skill)

## 技能概述 (Skill Overview)

本技能指導 Claude 執行專業的國際貿易融資文件審核,包括信用狀(L/C)檢查、單據不符點分析、UCP 600 合規驗證,以及 SWIFT 訊息格式驗證。

## 核心規範 (Core Standards)

### 1. UCP 600 (跟單信用狀統一慣例)
- **Article 14**: 單據審核標準工作天(5 個銀行工作日)
- **Article 18**: 商業發票要求
- **Article 20-25**: 運輸單據規定
- **Article 38**: 可轉讓單據

### 2. ISBP 745 (國際標準銀行實務)
- 拼字錯誤容忍度標準
- 單據一致性檢查
- 日期邏輯驗證

### 3. SWIFT 訊息標準
- **MT700**: 信用狀開狀
- **MT710**: 信用狀修改
- **MT740**: 信用狀授權
- **MT799**: 銀行間自由格式訊息

## 文件審核工作流程 (Document Checking Workflow)

### Step 1: 信用狀基本資訊驗證

```yaml
檢查項目:
  - 信用狀編號 (L/C Number)
  - 開狀日期 (Issue Date)  
  - 有效期限 (Expiry Date)
  - 開狀銀行 (Issuing Bank)
  - 受益人 (Beneficiary)
  - 申請人 (Applicant)
  - 信用狀金額 (L/C Amount)
  - 幣別 (Currency)
```

**範例檢查程式碼:**
```python
def validate_lc_basics(lc_data):
    required_fields = [
        'lc_number', 'issue_date', 'expiry_date',
        'issuing_bank', 'beneficiary', 'applicant',
        'lc_amount', 'currency'
    ]
    
    discrepancies = []
    for field in required_fields:
        if field not in lc_data or not lc_data[field]:
            discrepancies.append(f"缺少必要欄位: {field}")
    
    # 日期邏輯檢查
    if lc_data['issue_date'] >= lc_data['expiry_date']:
        discrepancies.append("開狀日期不得晚於或等於有效期限")
    
    return discrepancies
```

### Step 2: 單據一致性檢查 (Document Consistency Check)

**必須檢查的關鍵欄位:**

| 檢查項目 | 商業發票 | 裝箱單 | 提單 | 保險單 |
|---------|---------|--------|------|--------|
| 受益人名稱 | ✓ | ✓ | ✓ | ✓ |
| 申請人名稱 | ✓ | ✓ | ✓ | ✓ |
| 貨物描述 | ✓ | ✓ | ✓ | ✓ |
| 數量/重量 | ✓ | ✓ | ✓ | - |
| 發票金額 | ✓ | - | - | - |
| 保險金額 | - | - | - | ✓ |
| 起運港 | ✓ | - | ✓ | ✓ |
| 目的港 | ✓ | - | ✓ | ✓ |

**不符點範例 (Common Discrepancies):**

```markdown
❌ 嚴重不符 (Major Discrepancy):
- 商業發票金額 USD 50,000 超過信用狀金額 USD 48,000
- 提單顯示 "Freight Collect" 但 L/C 要求 "Freight Prepaid"
- 保險金額不足(應為發票金額 110%)

⚠️ 輕微不符 (Minor Discrepancy):
- 受益人名稱拼字差異: "TAIWAN TEXTILE CO LTD" vs "TAIWAN TEXTILE CO., LTD"
- 貨物描述略有差異但不影響實質內容
- 單據日期順序合理但未完全一致
```

### Step 3: 運輸單據審核 (Transport Document Review)

**提單 (Bill of Lading) 檢查清單:**

```markdown
1. 提單類型確認:
   □ 已裝船提單 (On Board B/L)
   □ 收貨待運提單 (Received for Shipment B/L)
   □ 清潔提單 (Clean B/L)
   
2. 必要批註 (Required Notations):
   □ "Shipped on Board" 日期戳記
   □ "Freight Prepaid" 或 "Freight Collect"
   □ "Notify Party" 資訊完整
   
3. 簽署要求 (Signature Requirements):
   □ 船公司或其代理人簽署
   □ 簽署日期在 L/C 有效期內
   □ 簽署者身份清楚標示
   
4. 份數要求 (Number of Originals):
   □ 通常要求全套正本 (Full Set of Originals)
   □ 例: "3/3" 表示三份正本全部提示
```

### Step 4: SWIFT MT700 格式驗證

**MT700 必要欄位檢查:**

```
:20:  Sender's Reference           (發送行參考號)
:31C: Date of Issue                (開狀日期)
:31D: Date and Place of Expiry     (有效期與地點)
:50:  Applicant                    (申請人)
:59:  Beneficiary                  (受益人)
:32B: Currency Code, Amount        (幣別與金額)
:41D: Available With... By...      (付款方式)
:42C: Drafts at...                 (匯票期限)
:43P: Partial Shipments            (分批裝運)
:43T: Transshipment               (轉運)
:44A: Loading on Board/Dispatch    (裝運港)
:44B: For Transportation to...     (目的港)
:44C: Latest Date of Shipment      (最遲裝運日)
:45A: Description of Goods         (貨物描述)
:46A: Documents Required           (所需單據)
:47A: Additional Conditions        (附加條款)
:71B: Charges                      (費用負擔)
```

**格式驗證範例:**

```python
def validate_mt700_format(mt700_message):
    """驗證 MT700 SWIFT 訊息格式"""
    
    mandatory_fields = {
        ':20:': '發送行參考號',
        ':31C:': '開狀日期',
        ':31D:': '有效期限',
        ':50:': '申請人',
        ':59:': '受益人',
        ':32B:': '金額',
        ':45A:': '貨物描述',
        ':46A:': '所需單據'
    }
    
    errors = []
    for tag, description in mandatory_fields.items():
        if tag not in mt700_message:
            errors.append(f"缺少必要欄位 {tag} ({description})")
    
    # 日期格式檢查 (YYMMDD)
    import re
    date_pattern = r':31[CD]:(\d{6})'
    dates = re.findall(date_pattern, mt700_message)
    for date in dates:
        if not validate_date_format(date):
            errors.append(f"日期格式錯誤: {date}")
    
    return errors

def validate_date_format(date_str):
    """檢查 YYMMDD 格式"""
    if len(date_str) != 6:
        return False
    year, month, day = int(date_str[:2]), int(date_str[2:4]), int(date_str[4:6])
    return 1 <= month <= 12 and 1 <= day <= 31
```

## 不符點分類與處理 (Discrepancy Classification)

### 分類標準 (Classification Criteria)

```yaml
第一級 - 致命性不符 (Fatal Discrepancies):
  - 金額超出信用狀限額
  - 單據偽造或造假
  - 裝運日期逾期
  - 缺少必要單據
  處理: 必須拒付 (Must Refuse Payment)

第二級 - 重大不符 (Major Discrepancies):  
  - 貨物描述實質不符
  - 運輸條款不符 (如 Freight Terms)
  - 保險金額不足
  - 提單非清潔提單
  處理: 通知申請人決定是否接受 (Notify Applicant)

第三級 - 輕微不符 (Minor Discrepancies):
  - 拼字錯誤但不影響辨識
  - 地址格式差異
  - 單據日期順序問題
  處理: 視銀行政策決定 (Bank Discretion)
```

## 自動化審核輸出格式 (Automated Review Output)

### 審核報告模板

```markdown
# 信用狀單據審核報告
## Document Review Report

**信用狀編號:** [L/C Number]  
**審核日期:** [Review Date]  
**審核人員:** Claude AI Trade Finance System  

---

## 一、基本資訊核對 (Basic Information Verification)

| 項目 | 信用狀要求 | 實際單據 | 狀態 |
|------|-----------|---------|------|
| 受益人 | [Required] | [Actual] | ✓/✗ |
| 申請人 | [Required] | [Actual] | ✓/✗ |
| 金額 | [Required] | [Actual] | ✓/✗ |
| 裝運期限 | [Required] | [Actual] | ✓/✗ |

---

## 二、單據檢查結果 (Document Check Results)

### 商業發票 (Commercial Invoice)
- ✓ 發票金額符合信用狀限額
- ✓ 貨物描述與信用狀一致
- ⚠️ 受益人地址格式略有差異

### 提單 (Bill of Lading)
- ✓ 清潔已裝船提單
- ✓ 運費預付 (Freight Prepaid)
- ✗ 裝運日期 2024-12-20 超過信用狀要求的 2024-12-15

### 保險單 (Insurance Policy)
- ✓ 保險金額為發票金額 110%
- ✓ 投保險別符合要求 (CIF)

---

## 三、不符點彙總 (Discrepancy Summary)

### 🔴 致命性不符 (Fatal - 1項)
1. **裝運逾期**: 提單日期 2024-12-20 超過信用狀最遲裝運日 2024-12-15  
   **建議處理**: 拒付並通知申請人

### 🟡 輕微不符 (Minor - 1項)  
1. **地址格式**: 受益人地址 "NO.100" vs "NO. 100" (空格差異)  
   **建議處理**: 可接受範圍內的文書差異

---

## 四、審核結論 (Conclusion)

**整體評估**: ❌ 不建議付款 (Payment NOT Recommended)  
**主要原因**: 裝運逾期為致命性不符點

**後續行動建議**:
1. 立即通知申請人單據存在不符點
2. 等待申請人指示是否接受不符點
3. 若申請人拒絕接受,退回單據予受益人
4. 若申請人同意接受,可酌收不符點手續費後付款

---

**審核完成時間**: [Timestamp]  
**系統版本**: Trade Finance AI v1.0  
**合規依據**: UCP 600, ISBP 745
```

## 最佳實踐建議 (Best Practices)

### 1. 審核時效管理
```python
# 5個銀行工作日規則 (UCP 600 Article 14)
from datetime import datetime, timedelta

def calculate_review_deadline(presentation_date):
    """計算審核截止日"""
    banking_days = 0
    current_date = presentation_date
    
    while banking_days < 5:
        current_date += timedelta(days=1)
        # 排除週末和國定假日
        if current_date.weekday() < 5 and not is_bank_holiday(current_date):
            banking_days += 1
    
    return current_date
```

### 2. 常見錯誤預防清單

```markdown
✓ 檢查清單 (Checklist):

□ 所有單據日期邏輯正確 (發票→裝船→提單)
□ 金額計算正確 (總金額 = 單價 × 數量)
□ 幣別一致性 (所有單據使用同一幣別)
□ 受益人/申請人名稱完全一致
□ 起運港/目的港與信用狀一致
□ 裝運日期在有效期限內
□ 單據份數符合要求 (如 3/3 提單正本)
□ 所有簽章與蓋章完整
□ 沒有未經授權的修改或塗改
□ 保險金額至少為 CIF 價格 110%
```

### 3. 風險旗標 (Risk Flags)

```yaml
高風險指標:
  - 首次往來客戶
  - 高風險國家/地區
  - 金額異常龐大
  - 貨物描述模糊
  - 受益人頻繁更換銀行
  - 第三方單據過多
  
處理原則:
  - 加強盡職調查 (Enhanced Due Diligence)
  - 要求額外擔保文件
  - 上報高階主管審核
  - 考慮是否通報 AML 單位
```

## 進階功能 (Advanced Features)

### 1. AI 輔助貨物描述比對

```python
from difflib import SequenceMatcher

def compare_goods_description(lc_description, invoice_description):
    """使用 AI 比對貨物描述相似度"""
    
    # 移除標點符號和統一大小寫
    lc_clean = lc_description.upper().replace(',', '').replace('.', '')
    inv_clean = invoice_description.upper().replace(',', '').replace('.', '')
    
    # 計算相似度
    similarity = SequenceMatcher(None, lc_clean, inv_clean).ratio()
    
    if similarity >= 0.95:
        return "完全一致", similarity
    elif similarity >= 0.85:
        return "實質一致(輕微差異)", similarity
    elif similarity >= 0.70:
        return "部分一致(需人工確認)", similarity
    else:
        return "不符", similarity
```

### 2. SWIFT 訊息自動生成

```python
def generate_mt730_acknowledgement(mt700_data):
    """自動生成 MT730 信用狀確認電文"""
    
    mt730 = f"""
{{1:F01TPBKTWTP0XXX0000000000}}
{{2:I730HSBCHKHHXXXXN}}
{{4:
:20:{mt700_data['reference']}
:21:{mt700_data['related_reference']}
:30:{datetime.now().strftime('%y%m%d')}
:58A:{mt700_data['beneficiary_bank']}
:72:/ACC/WE ACKNOWLEDGE RECEIPT OF YOUR
//MT700 DATED {mt700_data['issue_date']}
//AND CONFIRM THAT THE CREDIT IS AVAILABLE
//AT OUR COUNTERS
-}}
"""
    return mt730
```

## 合規注意事項 (Compliance Notes)

### 制裁篩選 (Sanctions Screening)
- 所有交易對手必須通過 OFAC/UN/EU 制裁名單篩選
- 貨物不得涉及軍民兩用品項 (Dual-Use Goods)
- 注意特定國家禁運規定

### 洗錢防制 (AML/CFT)
- 可疑交易指標識別
- KYC 文件完整性檢查
- 最終受益人 (UBO) 確認

### 資料隱私 (Data Privacy)
- 遵守 GDPR/個資法規定
- 客戶資料加密儲存
- 存取權限管理

---

## 使用此技能的指令範例

```bash
# 1. 基本文件審核
claude "請使用貿易融資技能審核這份信用狀單據組合"

# 2. 生成不符點報告
claude "根據 UCP 600 標準,分析這些單據並產生完整的不符點報告"

# 3. SWIFT 訊息驗證
claude "檢查這個 MT700 訊息格式是否符合 SWIFT 標準"

# 4. 批次審核
claude "批次審核資料夾中所有 L/C 案件並輸出 CSV 報表"
```

## 技能維護與更新

**版本**: 1.0  
**最後更新**: 2025-01-19  
**維護者**: Trade Finance Department  
**下次檢視日期**: 2025-07-19

**變更記錄**:
- 2025-01-19: 初始版本建立,包含 UCP 600 和 ISBP 745 標準