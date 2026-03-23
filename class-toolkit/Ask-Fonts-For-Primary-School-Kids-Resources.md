---
tags: 
model: sonnet
status: idle
session-id: bc7325c1-9999-4a22-bac9-f3d73342f734
---

When producing resources for primary school kids what font and font settings provide an easily readable resource?


## Claude

For primary school resources, readability research and educational publisher standards point to these recommendations:

## Font Choice

**Best options:**
- **Andika** (free, Google Fonts) — designed specifically for new readers, clear letterforms
- **OpenDyslexic** — good for inclusivity, though polarizing among teachers
- **Comic Sans** — genuinely good for early readers despite its reputation; clear `a` and `g` letterforms
- **URW Gothic** — free alternative with good legibility (similar to URW Gothic)

**Avoid:** Serif fonts (Times, Georgia), condensed fonts, or any with ambiguous `a`/`g` letterforms.

## Font Settings

| Setting | Recommended |
|---|---|
| **Size** | 14–16pt for body text, 18–24pt for younger year groups (Y1–2) |
| **Line spacing** | 1.5× minimum, 2× ideal for early readers |
| **Letter spacing** | Slightly increased (0.5–1pt) helps decoding |
| **Line length** | 45–60 characters max (~12–15 words) |
| **Alignment** | **Left-aligned only** — never justified (creates uneven word gaps) |
| **Contrast** | Black on white or dark on cream/pastel; avoid grey text |

## Key Principles

- **Distinguish easily confused letters**: `b/d/p/q` — fonts with clear serifs on `l` or differentiated forms help
- **Use a consistent `a`** — the single-story `a` (like handwriting) is preferred for early readers
- **Avoid ALL CAPS** — harder to decode than mixed case
- **Cream/off-white backgrounds** reduce glare and help dyslexic readers

For NZ primary context, **Andika** (free) or **Comic Sans** at 14–16pt with 1.5× line spacing is a solid, accessible default.

---
Create front settings to use for each year level from year 1 to 8.

## Claude



Here are recommended font settings for each NZ primary school year level:

## Year 1 (Age 5–6) — Beginning Readers

| Setting | Value |
|---|---|
| **Font** | Andika or Comic Sans |
| **Size** | 22–24pt |
| **Line spacing** | 2.0× |
| **Letter spacing** | +1pt |
| **Words per line** | 6–8 |
| **Alignment** | Left |

## Year 2 (Age 6–7) — Emerging Readers

| Setting | Value |
|---|---|
| **Font** | Andika or Comic Sans |
| **Size** | 20–22pt |
| **Line spacing** | 2.0× |
| **Letter spacing** | +1pt |
| **Words per line** | 8–10 |
| **Alignment** | Left |

## Year 3 (Age 7–8) — Early Fluency

| Setting | Value |
|---|---|
| **Font** | Andika or URW Gothic |
| **Size** | 18–20pt |
| **Line spacing** | 1.75× |
| **Letter spacing** | +0.75pt |
| **Words per line** | 10–12 |
| **Alignment** | Left |

## Year 4 (Age 8–9) — Developing Fluency

| Setting | Value |
|---|---|
| **Font** | Andika or URW Gothic |
| **Size** | 16–18pt |
| **Line spacing** | 1.75× |
| **Letter spacing** | +0.5pt |
| **Words per line** | 10–13 |
| **Alignment** | Left |

## Year 5 (Age 9–10) — Fluent Readers

| Setting | Value |
|---|---|
| **Font** | URW Gothic or Andika |
| **Size** | 14–16pt |
| **Line spacing** | 1.5× |
| **Letter spacing** | +0.5pt |
| **Words per line** | 12–15 |
| **Alignment** | Left |

## Year 6 (Age 10–11) — Confident Readers

| Setting | Value |
|---|---|
| **Font** | URW Gothic or Verdana |
| **Size** | 13–14pt |
| **Line spacing** | 1.5× |
| **Letter spacing** | Normal |
| **Words per line** | 12–15 |
| **Alignment** | Left |

## Year 7 (Age 11–12) — Transitioning

| Setting | Value |
|---|---|
| **Font** | URW Gothic, Verdana, or Carlito |
| **Size** | 12–13pt |
| **Line spacing** | 1.5× |
| **Letter spacing** | Normal |
| **Words per line** | 13–16 |
| **Alignment** | Left |

## Year 8 (Age 12–13) — Independent Readers

| Setting | Value |
|---|---|
| **Font** | Carlito, Verdana, or URW Gothic |
| **Size** | 11–12pt |
| **Line spacing** | 1.5× |
| **Letter spacing** | Normal |
| **Words per line** | 14–17 |
| **Alignment** | Left |

---

**General rules across all levels:**
- **Headings**: 4–6pt larger than body text, bold
- **Background**: White or cream — never coloured text on coloured backgrounds
- **Bold** for emphasis — avoid italics for young readers (Y1–4), use sparingly from Y5+
- **Always left-aligned** — never justified at any year level
- **Minimum contrast ratio**: 4.5:1 (WCAG AA)

---
I've got the command "/generate resources" and at the moment it generates it as markdown. What are my options to have the output as a .docx? Should it write straight to a word doc or should I update the "/md-to-docx" command?
Actually it would be good to have both. The key problem is how do I apply the font setting to the document?

## Claude

Good question. Here's how I'd approach this:

## The Core Problem

Markdown has no font/size/spacing information — those settings need to be applied during conversion to .docx.

## Recommended Approach: Pandoc Reference Templates

Pandoc supports `--reference-doc=template.docx` which applies all styles (font, size, spacing, margins) from a template document. Create one reference template per year level.

**How it works:**
1. Create 8 reference .docx files (one per year level) with the correct heading/body styles pre-configured
2. When converting, pick the right template based on the student's year level
3. Run: `pandoc input.md --reference-doc=year-3-ref.docx -o output.docx`

The markdown content stays clean — all formatting comes from the template.

## What Needs to Change

### 1. Add `year-level` to student profiles

The profiles currently have age but not year level. Adding it makes template selection automatic:

```yaml
---
active: true
year-level: 3
---
```

### 2. Create reference templates

Store them in `01_Projects/Teacher-AI-Resources/class-agent/templates/year-1-ref.docx` through `year-8-ref.docx`, each with the font settings we defined earlier baked into the Word styles (Heading 1, Heading 2, Body Text, etc.).

### 3. Update `/generate-resource`

Add a post-generation step: after each agent writes the .md file, convert it to .docx using the student's year-level template. Output both files side by side.

### 4. Keep `/md-to-docx` as a standalone tool

For one-off conversions where you want to pick a year level manually.

## Creating the Reference Templates

This is the one manual step — you need to create a .docx in Word/Google Docs with the right styles configured. I can generate them programmatically using the docx skill if you'd prefer, with all the font settings we defined earlier baked in.

**Want me to:**
1. Generate the 8 reference templates using the docx skill?
2. Add `year-level` to the student profiles?
3. Update `/generate-resource` to produce both .md and .docx?

---
