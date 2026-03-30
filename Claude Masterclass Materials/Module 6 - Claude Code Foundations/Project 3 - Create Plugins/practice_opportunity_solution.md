# Prompt 4: Practice — Run a Competitive Analysis for a Different Industry

Now it's your turn. For the industry below (or use your own!), run a full competitive analysis using Playwright + the marketing plugin.


## Coffee / Food & Beverage — You're opening an artisan coffee roastery

Analyze these competitors:
- Competitor 1: https://bluebottlecoffee.com
- Competitor 2: https://www.stumptowncoffee.com
- Competitor 3: https://counterculturecoffee.com

Your business: **Ember & Origin** — "Single-origin, small-batch, roasted with intention"
Target audience: Coffee enthusiasts who care about origin, process, and sustainability.

---

## The Challenge

1. **Screenshot competitors** — Use Playwright to visit all three sites, take screenshots of their homepage and one other key page (pricing, products, or about)
2. **Analyze** — Have Claude compare what each does well and what they miss
3. **Build a strategy** — Use the marketing plugin to create a 4-week content calendar and 5 differentiation strategies for your chosen business

Write your own Claude Code prompts following the CIIO format. Then check the reference below.

---

## Solution:

### Part 1: Competitive Screenshots

```
Context: I have the Playwright plugin installed. I'm launching an artisan coffee roastery called "Ember & Origin" and want to analyze what the top specialty coffee brands are doing online.

Instruction: Using the Playwright browser, visit the following coffee brand websites one by one. For each site:
1. Navigate to their homepage and take a full-page screenshot
2. Visit their shop/products page and take a screenshot
3. Note their hero message, color scheme, photography style, and overall brand vibe
4. Check how they present their sourcing/origin story

Then create a competitive analysis comparing all three — what each does well, what's missing, and 5 things Ember & Origin should do differently.

Input:
- Competitor 1: https://bluebottlecoffee.com
- Competitor 2: https://www.stumptowncoffee.com
- Competitor 3: https://counterculturecoffee.com

Output: A competitive analysis with screenshots saved locally and a written summary with actionable recommendations.
```

### Part 2: Marketing Strategy

```
Context: I just completed a competitive analysis of three specialty coffee brands using Playwright. I have the Anthropic marketing plugin installed.

Instruction: Based on the competitive research, create a marketing action plan for Ember & Origin including: brand positioning, a 4-week Instagram + LinkedIn content calendar, 5 customer acquisition strategies the competitors aren't using, and 3 quick wins for this week.

Input:
- Business: Ember & Origin
- Tagline: "Single-origin, small-batch, roasted with intention"
- Target audience: Coffee enthusiasts who care about origin, process, and sustainability
- Differentiator: Every bag comes with a story card about the farmer, the region, and the roast profile
- Budget: Small business (favor organic/free strategies)

Output: A complete marketing plan formatted as an HTML page.
```
