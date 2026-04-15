---
name: generate-progression
description: "Import an educational progression, scope and sequence, or curriculum framework and apply it to student profiles. Use when the teacher wants to add a progression, import a scope and sequence, set up learning levels, add curriculum tracking, import BSLA, import a framework, or track student progress against a resource. Also use when the user says things like 'add a progression', 'import this resource', 'set up tracking', 'add this to student profiles', 'import scope and sequence', or 'create progressions from this'."
argument-hint: "[file path or URL to resource]"
---

# Generate Progression

Import an educational resource (progression, scope and sequence, or curriculum framework), create structured progression files, and add tracking fields to student profiles.

## Arguments

`$ARGUMENTS` is either:

- A **file path** to a resource (PDF, docx, image, etc.)
- A **URL** linking to an online resource
- **Empty** — ask the teacher to provide one

## Instructions

### Step 1: Obtain the Resource

**If `$ARGUMENTS` is empty:**

1. Use AskUserQuestion to ask: "What resource would you like to import as a progression? Provide a file path (PDF, docx, etc.) or a URL."
2. Use the response as the resource reference

**If `$ARGUMENTS` is provided:**

1. Use `$ARGUMENTS` as the resource reference

### Step 2: Determine Base Directory

Check if the current working directory's basename is `ClassResources`.

- **If yes:** use the current directory as the base — all paths below are relative to `.`
- **If no:** set the base directory to `ClassResources/`. Create this folder if it does not exist.

All subsequent steps use `{base}` to mean either `.` or `ClassResources/` depending on the result above.

### Step 3: Read and Analyse the Resource

**If the resource reference is a file path:**

1. Read the file using the appropriate tool (Read for text/PDF/images, or Bash for other formats)
2. If the file cannot be read directly (e.g., a .docx), attempt conversion using pandoc: `pandoc "{file-path}" -t markdown`

**If the resource reference is a URL:**

1. Use WebFetch to retrieve the content at the URL
2. If the page contains links to sub-pages, sections, or downloadable documents that form part of the progression, follow those links to gather additional context. Use judgement — only follow links that appear to contain progression content (e.g., level descriptions, scope details, weekly sequences). Do not follow unrelated navigation links.

Store the full gathered content as the **resource content**.

### Step 4: Identify Progression Structure

Analyse the resource content to identify:

- **The name of the framework/progression** (e.g., "BSLA", "NZ Maths Stages", "Reading Recovery Levels")
- **The levels/stages/steps** — how many there are, what they are called, and what numbering or naming system they use
- **The content at each level** — scope, sequence, descriptions, learning outcomes, weekly plans, or whatever structure the resource provides

Present a brief summary to the teacher:

"I've analysed this resource. Here's what I found:

- **Framework:** {name}
- **Levels:** {count} levels ({naming scheme, e.g., "Taumata 1–9", "Stages 1–8", "Levels A–Z"})
- **Content per level:** {brief description of what each level contains}

I'll now create progression files for each level."

### Step 5: Create Progressions Folder

1. Derive a **framework slug** from the framework name identified in Step 4 (lowercase, hyphens, e.g., "BSLA" → `bsla`, "NZ Maths Stages" → `nz-maths-stages`)
2. Check if `{base}/progressions/{framework-slug}/` exists
3. If it does not exist, create it (including the parent `progressions/` directory if needed)

### Step 6: Copy or Link the Source Resource

**If the resource reference is a file path:**

1. Copy the file to `{base}/progressions/{framework-slug}/` using the platform-appropriate copy command
2. Tell the teacher the source file has been copied

**If the resource reference is a URL:**

1. Create a file `{base}/progressions/{framework-slug}/source-{framework-slug}.md` containing:
   ```
   # Source

   [{framework name}]({URL})

   Imported on {today's date}.
   ```
3. Tell the teacher the source link has been saved

### Step 7: Generate Progression Files

For each level/stage identified in Step 4, create a Markdown file in `{base}/progressions/{framework-slug}/`:

- **Filename format:** derive from the framework slug and level identifier, using lowercase-hyphenated format
  - Examples: `bsla-taumata-1.md`, `nz-maths-stage-2.md`, `reading-recovery-level-a.md`

- **File content:** structure the level's content in a clear, teacher-friendly Markdown format. Include:
  - A heading with the level name and any subtitle (e.g., `# Taumata 1 — Kākano (Seed)`)
  - All relevant content from the resource for that level — scope, sequence, learning outcomes, descriptions, weekly breakdowns, etc.
  - Organise the content with appropriate subheadings
  - Use NZ/British English spelling throughout

Do not invent content. Only include information present in the source resource.

After creating all files, tell the teacher how many progression files were created and list them.

### Step 8: Recommend Frontmatter Field

Based on the progression structure, recommend a new frontmatter key-value pair for student profiles:

- **Key:** derive from the framework name, using lowercase-hyphenated format (e.g., `bsla-taumata`, `maths-stage`, `reading-level`)
- **Default value:** recommend the lowest or most common starting level as the default (e.g., `1`, `a`, `beginning`)

Present the recommendation to the teacher:

"To track each student's position in this progression, I recommend adding this field to student profiles:

`{recommended-key}: {recommended-default-value}`

This would go in the YAML frontmatter of each student's `student-profile.md`."

Use AskUserQuestion to ask: "Would you like to use this field name and default value? You can suggest a different key or default if you prefer."

Provide options:

1. **Label:** "Yes, use this" — **Description:** "Add `{recommended-key}: {recommended-default-value}` to student profiles"
2. **Label:** "Change the field name" — **Description:** "Suggest a different frontmatter key name"
3. **Label:** "Change the default value" — **Description:** "Use the same key but a different starting value"

If the teacher suggests changes, use their preferred key and/or default value instead.

Store the confirmed **field key** and **default value**.

### Step 9: Select Classes

Use Glob to find all `**/student-profile.md` files under `{base}`.

Group the results by **class folder** — the folder directly under `{base}` that contains student subfolders. Derive the class display name by replacing hyphens with spaces and title-casing (e.g., `year-5-blue` → "Year 5 Blue").

Exclude any profiles found under `progressions/`, `templates/`, or `guides/`.

**If no student profiles are found:** tell the teacher: "No classes have been set up yet. Run `/init-class` to create a class first, then run `/generate-progression` again to apply the tracking field." Then stop.

**If one class is found:** use AskUserQuestion to ask: "I found one class: {class name} ({count} students). Would you like to add `{field-key}` to all students in this class?"

**If multiple classes are found:** use AskUserQuestion with options listing each class name, plus an "All classes" option. Ask: "Which classes should have `{field-key}` added to their student profiles?"

### Step 10: Choose Application Mode

Use AskUserQuestion to ask: "How would you like to set the initial value for `{field-key}`?"

Provide options:

1. **Label:** "Same value for all students" — **Description:** "Set `{field-key}: {default-value}` for every student in the selected class(es)"
2. **Label:** "Set individually per student" — **Description:** "I'll ask you to set a value for each student one at a time"

### Step 11: Apply Frontmatter to Student Profiles

Read each student's `student-profile.md` in the selected class(es). Only include students where the frontmatter contains `active: true`.

**If "Same value for all students" was chosen:**

For each student profile:

1. Check if the frontmatter already contains the `{field-key}` field
2. If it already exists, skip it and note it in the report
3. If it does not exist, add `{field-key}: {default-value}` as a new line in the YAML frontmatter (after the last existing field, before the closing `---`)
4. Write the updated content back to the file

**If "Set individually per student" was chosen:**

For each student profile:

1. Extract the student's display name from the folder name (replace hyphens with spaces, title-case)
2. Check if the frontmatter already contains the `{field-key}` field
3. If it already exists, tell the teacher the current value and ask if they want to change it
4. If it does not exist, use AskUserQuestion to ask: "What `{field-key}` value should {student name} have? (default: {default-value})"
5. Use the teacher's response, or the default if they confirm or leave blank
6. Add the field to the frontmatter and write the updated file

### Step 12: Update Student Profile Template

So that students added in future (via `/init-class` or manually) also include this tracking field, update the template file.

1. Check if `{base}/templates/student-profile-template.md` exists
2. If it does not exist, skip this step
3. Read the template
4. Check if the YAML frontmatter already contains the `{field-key}` field
   - If it already exists, skip — do not overwrite
5. If it does not exist, add `{field-key}: {default-value}` as a new line in the YAML frontmatter (after the last existing field, before the closing `---`)
6. Write the updated content back

Use the **default value** from Step 8 — not any per-student value chosen in Step 10 — because the template is a starting point for new students.

Tell the teacher: "Updated the student profile template so any new students will automatically include `{field-key}`."

### Step 13: Update CLAUDE.md

Check if `{base}/CLAUDE.md` exists.

**If it exists:** read it. If it does not already mention `/generate-progression`, append the following line to the skills list section:

```
- `/generate-progression` — import a progression or curriculum framework and track student levels
```

**If it does not exist:** skip this step.

### Step 14: Report and Next Steps

Summarise what was done:

- Framework name and source (file or URL)
- Number of progression files created in `{base}/progressions/{framework-slug}/`
- The frontmatter field added: `{field-key}: {value}`
- Number of student profiles updated, grouped by class
- Any profiles that were skipped (field already existed)
- Whether the student profile template was updated

Then tell the teacher:

"The progression has been imported and student profiles updated.

You can view the progression files in `{base}/progressions/{framework-slug}/` to see the content at each level.

To change a student's level later, edit the `{field-key}` value in their `student-profile.md` frontmatter.

When generating resources with `/generate-resource`, you can reference the student's `{field-key}` in your prompt to create level-appropriate content."
