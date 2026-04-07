# Cowork

## Resources

Refer to Claude Masterclass Materials\Claude Masterclass - Prompt Library.docx for more examples and templates.

```cowork prompt
Select folder to C:\Users\samfi\OneDrive\Documents\Claude Masterclass Materials

Organize the folder into categories: receipts, invoices, and agreements. Then I want you to add the total receipts and export them in an Excel sheet. 

Remove the original files out of the root folder after you have completed the task.

Draft an email with the summary of all receipts amount that you just calculated and then send the summary of receipts amount to my email samfire5200@gmail.com

Use today's USD/CAD exchange rate to convert the CAD amount to its USD equivalent, then calculate the total.

Update the Receipt Summary – Small Business Expenses as well with Exchange Rate conversion.
```

## Skills

<https://skills.sh>

npx skills add <owner/repo>

```cmd
npx skills add https://github.com/anthropics/skills --skill pdf
npx skills add https://github.com/anthropics/skills --skill pptx
npx skills add https://github.com/anthropics/skills --skill docx
npx skills add https://github.com/anthropics/skills --skill xlsx
npx skills add https://github.com/anthropics/skills --skill frontend-design
```

<https://github.com/anthropics/skills>

## Skills Live Demos - LinkedIn

### Installing Skills from SkillHub

<https://www.skillhub.club/skills/different-ai-zero-finance-linkedin-post>

```powershell
irm "https://www.skillhub.club/api/v1/skills/different-ai-zero-finance-linkedin-post/install?agents=claude&format=ps1" | iex
```

### CoWorking with Skills

Customize -> Skills -> `+` -> Upload a Skill -> Click to Upload -> Select the `SKILL.md` from SkillHub

### Working project folder

C:\Users\samfi\OneDrive\Documents\Claude Masterclass Materials\Module 2 - Claude Cowork\Claude Skills - LinkedIn Post Writer

```cowork prompt
Draft a LinkedIn post about the recent state of AI that starts with a strong hook. Read the state-of-the-art report and make it personal in Dr. Ryan Ahmed's voice. 
```

```md result
88% of organizations say they're using AI.

Only 7% have actually scaled it.

That gap is the story of AI in 2025.

I've been teaching AI and machine learning for years now, and this new McKinsey State of AI report confirms something I keep telling my students:

We're past the hype phase. We're in the "now what?" phase.

The biggest shift? AI agents. 62% of organizations are already experimenting with agentic AI — systems that don't just generate text, but plan, act, and execute across workflows.

But here's the part most people are missing: the companies seeing real EBIT impact aren't just automating tasks. They're 3.6x more likely to be pursuing transformative change. They're redesigning entire workflows, not just bolting AI onto old ones.

Efficiency gets you in the door. Innovation is what keeps you in the room.

If you're leading an AI initiative right now, the data is clear — think bigger.

#AI #ArtificialIntelligence #AIAgents #McKinsey #FutureOfWork

```

## Plugins

Plugins bundle skills, connectors, slash commands & sub-agents into one package for a specific job function. No technical knowledge required to create them.

### Add Plugins

CoWork -> Customize -> `+` -> Browse Plugins -> Click to `Install`

List of **“Manage” plugins** shown in your screenshots (grouped clearly):

#### 🧠 Core Business / Knowledge

* Productivity
* Design
* Marketing
* Data
* Engineering
* Finance

#### 🏢 Business Functions

* Product Management
* Legal
* Operations
* Sales
* Human Resources

#### 🔍 Search & Support

* Enterprise Search
* Customer Support

### Demo - Data Analysis Plugin

C:\Users\samfi\OneDrive\Documents\Claude Masterclass Materials\Module 2 - Claude Cowork\Data Analysis\Sales_Data.xlsx

```cowork prompt
/explore-data using the Sales_Data.xlsx

/validate-data

Clean up the data and save the results in a new file v1. Don’t overwrite the original file

/build-dashboard 

# data visualization
/create-viz 

# The `statistical-analysis` skill currently has user-invocable: false, meaning only Claude can invoke it. To change it to "User & Claude", I need to set user-invocable: true so both you and Claude can trigger it.

/data:statistical-analysis 

Summarize everything you generated in a PowerPoint slides to present to my manager 

Turn this task into a skill for the `` related instructions, since it could be reused.

```

## Financial Forecasting Skill

<https://skills.sh/jeremylongshore/claude-code-plugins-plus-skills/forecasting-time-series-data>
<https://github.com/jeremylongshore/claude-code-plugins-plus-skills/blob/main/plugins/ai-ml/time-series-forecaster/skills/forecasting-time-series-data/SKILL.md>

Customize -> Skills -> `+` Create skill -> Upload a Skill -> Click to Upload -> Select the `SKILL.md` file (Copy and Paste from GitHub)

Select folder `C:\Users\samfi\development\ClaudeCodeLearning\ClaudeMastery\Claude Masterclass Materials\Module 2 - Claude Cowork\Financial Forecasting`

```cowork prompt
using the financial forecasting skill, train an ARIMA model and SARIMA models using the `sales_forecasting.xlsx` to forecast the revenue. Test the model using the `future_calendar.xlsx`
```

✅ 一句話總結

👉 這張圖的核心結論是： `ARIMA` 提供**穩定**可用的**預測**，而 `SARIMA` 在這組數據上設定不佳，導致**預測失真**。

## Custom Financial Plugin

Resources

* Folder `C:\Users\samfi\OneDrive\Documents\Claude Masterclass Materials\Module 2 - Claude Cowork\Finance - Custom Plugin`
* Plugin Instructions file: `Claude Plugin Creation - Finance Variance Analysis and Statements creationV3.docx`
* Data file: `Variance analysis and statements financial dataset.xlsx`

```cowork prompt
- What is your role / position title? => Senior Financial Analyst
- What is your primary accounting software? => Excel / Google Sheets
- What output format do you prefer for reports? => Both Excel & Word
- Who is the primary audience for your financial reports? => Board of Directors
```

Output

* Plugin: `my-finance.plugin` -> Save Plugin
* To install: open the .plugin file in Cowork and press the install button.

```cowork prompt
/my-finance:my-variance-analysis Monthly budget vs. actual expenses
/my-financials-statements

generate powerpoint slides to summarize the financial statements
```

## Practice Opportunity Question: Analyze data plugin

Folder: `C:\Users\samfi\OneDrive\Documents\Claude Masterclass Materials\Module 2 - Claude Cowork\Data Analysis - Practice Opportunity`
Data file: `reviews.xlsx`

### 字段详情

| 字段名 | 类型 | 分类 | 空值 | 唯一值数 | 备注 |
|---|---|---|---|---|---|
| `Rating` | 整数 | 指标 | 0 | 5个（1–5星） | 严重偏向5星 |
| `Date` | 日期 | 时间 | 0 | 75 | 92%的数据来自2025年7月 |
| `Variation` | 文本 | 维度 | 0 | 16 | 产品型号/颜色变体 |
| `Verified_Reviews` | 文本 | 自由文本 | 1 | 2,300 | 用户评论正文 |
| `Feedback` | 整数 | 布尔标志 | 0 | 2（0或1） | 1=正面，0=负面 |

```cowork prompt
/explore-data using the reviews.xlsx
/validate-data
/clean-data save as reviews_cleaned.xlsx
/clean-data those duplicate records to one record in reviews_cleaned.xlsx

/dashboard Create a single-page dashboard showing review volume and average sentiment.

Using data-visualization skill to plot a Word Cloud to identify the most frequent customer by using reviews_cleaned.xlsx

Generate a 3-slide PowerPoint summary

/create-viz plot a bar chart showing the distribution of ratings (1–5 stars) in reviews_cleaned.xlsx

```
