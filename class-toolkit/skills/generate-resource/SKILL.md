---
name: generate-resource
description: "Generate a personalised resource for each student in the class. Use when the user wants to create educational resources, stories, worksheets, or quizzes for students."
argument-hint: "[prompt or guide name]"
---

# Generate Resource

Generate a personalised educational resource for every active student.

## Arguments

`$ARGUMENTS` is either:

- A **guide name** matching an existing file in `guides/` (with or without `.md`)
- A **new resource prompt** describing what to create (e.g., "Create a 500 word fantasy story about teamwork")
- **Empty** — prompt the user to select from available guides

## Instructions

### Step 1: Resolve the Resource Prompt

The guides directory is `guides/`.

**If `$ARGUMENTS` is empty:**

1. Glob `guides/*.md` to list available guide files (exclude `student-profile-template.md`)
2. If no guides exist, tell the user there are no saved guides and ask them to provide a resource prompt instead, then stop
3. Present the guides as a numbered list (display the filename without `.md`, replacing hyphens with spaces)
4. Use AskUserQuestion to ask the user which guide to use
5. Read the selected guide file — its full content becomes the resource prompt

**If `$ARGUMENTS` matches a guide file:**

1. Check if a file named `$ARGUMENTS` or `$ARGUMENTS.md` exists in the guides directory
2. If found, read the file — its full content becomes the resource prompt
3. Tell the user which guide is being used

**If `$ARGUMENTS` is a new prompt (no matching guide file):**

1. Use `$ARGUMENTS` directly as the resource prompt
2. Save the prompt to a new guide file in the guides directory:
   - Derive the filename using the same logic as Step 3 below (Title-Case-With-Hyphens.md)
   - Write the prompt text as the file content
   - Tell the user the guide has been saved for reuse

### Step 2: Discover Students

Use Glob to find all `**/student-profile.md` files in the working directory. This will find profiles inside class folders (e.g., `year-5-blue/barry-crump/student-profile.md`).

Group the results by **class folder** — the top-level folder that contains the student (not `guides/`). Derive the class display name by replacing hyphens with spaces and title-casing (e.g., `year-5-blue` → "Year 5 Blue").

**Extract the year level** from the class folder name by looking for a pattern like `year-5` or `y5` (a number 1–8). This determines which .docx reference template to use for formatting. If no year level is found in the folder name, default to **2**.

**If one class is found:** use it automatically and tell the teacher which class is being used.

**If multiple classes are found:** use AskUserQuestion to ask which class to generate resources for. List each class name as an option, plus an "All classes" option.

**If no student profiles are found:** inform the teacher that no classes have been set up yet, suggest they run `/init-class` first, and stop.

For each profile in the selected class(es), read it. Only include students where the frontmatter contains `active: true`.

Extract from each:

- **Student name**: The student's folder name, replacing hyphens with spaces and title-casing (e.g., `barry-crump` → "Barry Crump")
- **Student folder path**: Full path to the student's folder
- **Profile content**: The full content of `student-profile.md`
- **Year level**: The year level extracted from the class folder (1–8, default 2)

If no active students are found, inform the user and stop.

### Step 3: Derive Filename

Generate a base filename from the resource prompt:

- Extract the key topic words (drop filler words like "create", "a", "the", "word", numbers)
- Convert to Title-Case-With-Hyphens format
- Example: "Create a 500 word fantasy story about teamwork" → `Fantasy-Story-Teamwork`

Each student will receive two files: `{base-filename}.md` and `{base-filename}.docx`.

Tell the user the filename that will be used and list the students who will receive the resource.

### Step 4: Determine Templates Directory

Derive the **templates directory** from where the student profiles were found in Step 2. The templates directory is a sibling of the class folder:

- If student profiles are at `ClassResources/{class}/{student}/student-profile.md`, templates are at `ClassResources/templates/`
- If student profiles are at `{class}/{student}/student-profile.md` (working directory is already ClassResources), templates are at `templates/`

In short: take the parent directory of the class folder and append `templates/`. Call this `{templates-dir}`.

### Step 5: Ensure Templates Are Available

Check if `{templates-dir}/year-1-ref.docx` exists.

**If it exists:** continue to Step 6.

**If it does not exist:**

1. Use Glob to find `**/class-toolkit/templates/year-1-ref.docx` under `~/.claude/` to locate the plugin's installed directory
2. Derive the **plugin directory** from the matched path (two levels up from `templates/year-1-ref.docx`)
3. Create the `{templates-dir}` directory
4. Use Bash to copy templates using the platform-appropriate commands:
   - **Linux/macOS:**
     ```
     cp {plugin-dir}/templates/year-*-ref.docx {templates-dir}/
     ```
   - **Windows:**
     ```
     Copy-Item -Path "{plugin-dir}\templates\year-*-ref.docx" -Destination "{templates-dir}\"
     ```
5. Tell the teacher that formatting templates have been copied

If the templates cannot be found, warn the teacher that .docx files will use pandoc's default formatting instead of year-appropriate styles, then continue.

### Step 6: Generate Resources in Parallel

Launch one Agent per student **in a single message** (parallel execution). Each agent should be `general-purpose` type.

For each agent, use this prompt template:

```
You are creating a personalised educational resource for a student.

## Student Profile
{paste the full student-profile.md content here}

## Resource Request
{paste the resolved resource prompt here}

## Instructions
- Personalise the content to match this student's reading level, interests, and learning needs from their profile
- If their interests are listed, weave references to those interests naturally into the content
- Match vocabulary and complexity to their reading level
- If learning needs are specified, adapt the resource accordingly
- Use New Zealand/British English spelling throughout (e.g., colour, organised, behaviour, programme, centre)
- Write the resource in Markdown format
- Do NOT include YAML frontmatter

## Step 1: Write the Markdown file

Write the completed resource to: {student folder path}/{base-filename}.md

## Step 2: Convert to Word document

Run this command to convert the Markdown to a formatted .docx using the year-level reference template:

pandoc "{student folder path}/{base-filename}.md" --reference-doc="{templates-dir}/year-{year-level}-ref.docx" -o "{student folder path}/{base-filename}.docx"

The reference template applies age-appropriate font, size, and spacing automatically. Do not skip this step.
```

### Step 7: Report

After all agents complete, summarise:

- How many students received the resource
- The filenames used (both `.md` and `.docx`)
- The year level and reference template used for formatting
- List each student name and confirm both files were created
- Note any issues or agents that failed (including pandoc conversion failures)
