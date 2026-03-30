# Prompt 4: Practice — Create a Brand Command for a Different Business

Now it's your turn. Pick ONE of the businesses below (or use your own!) and create a complete `/my-brand` slash command for it.

\---

## Verde Kitchen — Plant-Based Meal Prep

Create a brand command with:

* **Business:** Verde Kitchen
* **Tagline:** "Eat well. Live well. No effort required."
* **Colors:** Forest Green (#2D5A27), Cream (#FAF3E0), Terracotta (#C4704F)
* **Fonts:** Josefin Sans for headings, Source Sans Pro for body
* **Tone:** Friendly, encouraging, health-conscious — like a supportive friend who also happens to be a chef
* **Words to use:** nourish, fresh, plant-powered, simple, wholesome, vibrant
* **Words to avoid:** diet, restrict, guilty, cheat meal, processed, artificial


## In ChatGPT or Gemini, you can create an image using this:
Create a hero photo for my website that sells fresh meals. I want to showcase healthy green food that beautifully captures the moment of eating wholesome food. Image dimensions are 16:9. 



## Solution:

```
Context: I want to create a custom Claude Code command /my-brand-verde-k that stores the Verde Kitchen brand identity.

Instruction: Create a file at \\\~/.claude/commands/my-brand-verde-k.md with the following brand kit. Use the exact YAML frontmatter format that Claude Code require.

Input:
- Description: "Apply my brand identity to all outputs — emails, documents, social posts, web pages, and reports. Use when creating any content."
- Business name: Verde Kitchen
- Tagline: "Eat well. Live well. No effort required."
- Primary color: #2D5A27 (Forest Green) — for headings, buttons, accents
- Secondary color: #FAF3E0 (Cream) — for backgrounds, cards
- Accent color: #C4704F (Terracotta) — for CTAs, highlights, links
- Heading font: Josefin Sans (fallback: Arial)
- Body font: Source Sans Pro (fallback: Helvetica)
- Tone of voice: Friendly, encouraging, health-conscious — like a supportive friend who also happens to be a chef
- Words we use: nourish, fresh, plant-powered, simple, wholesome, vibrant
- Words we avoid: diet, restrict, guilty, cheat meal, processed, artificial
- Closing phrases: "Nourish yourself.", "Fresh starts here.", "Eat well, effortlessly."

Output: A complete my-brand-verde-k.md file with proper YAML frontmatter (name, description) and markdown body covering brand colors, fonts, tone, vocabulary, and formatting rules.
```

