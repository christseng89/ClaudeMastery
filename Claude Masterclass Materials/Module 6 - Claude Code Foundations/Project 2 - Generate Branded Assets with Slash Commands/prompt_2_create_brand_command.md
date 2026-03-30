# Prompt 2: Create Your Own `/my-brand` Command

Copy and paste the following into Claude Code:

```
Context: I'm a freelance photographer running a studio called "Kai Lens Studio." I want to create a reusable slash command called /my-brand so that every time I use Claude, it already knows my brand identity and applies it to everything it creates for me.

Instruction: Create a /my-brand command that stores my full brand identity. Whenever I or Claude use this command, it should apply my brand colors, fonts, tone of voice, and vocabulary rules to any content — emails, social posts, web pages, documents, anything.

Input:
- Business name: Kai Lens Studio
- Tagline: "Your story, beautifully told"
- Brand colors: Deep Navy #1A1A2E (headings, backgrounds), Warm Sand #E8D5B7 (accents, highlights), Antique Gold #C9A96E (buttons, links)
- Fonts: Cormorant Garamond for headings, Nunito Sans for body text
- Tone of voice: Calm, artistic, confident — like a photographer who sees beauty in everything and speaks with quiet authority
- Words we use: timeless, craft, story, light, moment, authentic, intentional
- Words we avoid: cheap, package, deal, basic, quick, selfie, snap
- Closing phrases: "Let's tell your story.", "See you through the lens.", "Your moment, preserved."

Output: A working /my-brand command that I can use in any project going forward.
```

---

## After Claude creates it

Exit and relaunch Claude Code so it picks up the new command:

```
/exit
```

```bash
claude
```

Then verify by typing:

```
/my-brand
```

You should see `my-brand` listed. Now it's available in every project you open.

