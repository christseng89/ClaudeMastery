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

Customize -> Skills -> `+` Create skill -> Upload a Skill -> Click to Upload -> Select the `SKILL.md` from the forecasting-time-series-data skill