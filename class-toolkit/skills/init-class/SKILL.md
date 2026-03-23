---
name: init-class
description: "Set up a new class with student profiles. Use when the teacher wants to initialise a class, add students, set up the class structure, or get started with the class toolkit. Also use when the user says things like 'create a class', 'add my students', 'set up my class', or 'get started'."
argument-hint: "[class name]"
---

# Initialise Class

Create a new class folder and generate a student profile for each student.

## Arguments

`$ARGUMENTS` is either:

- A **class name** (e.g., "Year 5 Blue")
- **Empty** — ask the teacher to provide one

## Instructions

### Step 1: Determine Class Name

**If `$ARGUMENTS` is empty:**

1. Use AskUserQuestion to ask: "What is the name of your class? (e.g., Year 5 Blue, Room 12, Period 3 English)"
2. Use the response as the class name

**If `$ARGUMENTS` is provided:**

1. Use `$ARGUMENTS` as the class name

### Step 2: Format the Folder Name

Convert the class name to a folder-safe format:

- Convert to lowercase
- Replace spaces with hyphens
- Remove any characters that are not letters, numbers, or hyphens
- Collapse multiple hyphens into one

Example: "Year 5 Blue" → `year-5-blue`

### Step 3: Check for Existing Class

Use Glob to check if `{folder-name}/` already exists.

- If it exists, tell the teacher: "A class called '{class name}' already exists. Would you like to add more students to it?"
- Use AskUserQuestion to confirm. If no, stop. If yes, continue to Step 4, then skip to Step 6.

### Step 4: Create CLAUDE.md

Check if a `CLAUDE.md` file exists in the working directory root.

**If it already exists:** skip this step — do not overwrite it.

**If it does not exist:** create `CLAUDE.md` with the following content:

```
You are a master expert teacher.

Use the class-toolkit skills to manage classes and generate resources:

- `/init-class` — set up a class and add students
- `/generate-resource` — create personalised resources for each student
```

### Step 5: Copy Formatting Templates

Check if `templates/year-1-ref.docx` already exists in the working directory.

**If it exists:** skip this step — templates are already in place.

**If it does not exist:**

1. Use Glob to find `**/templates/year-1-ref.docx` under `~/.claude/` to locate the plugin's installed templates directory
2. Derive the source directory from the matched path (strip the filename)
3. Create a `templates/` directory in the working directory
4. Use Bash to copy all year-level reference templates using the platform-appropriate command:
   - **Linux/macOS:** `cp {source-directory}/year-*-ref.docx templates/`
   - **Windows:** `Copy-Item -Path "{source-directory}\year-*-ref.docx" -Destination "templates\"`
5. Tell the teacher: "Formatting templates have been copied to `templates/`. These are used by pandoc to apply age-appropriate fonts and spacing when generating Word documents."

If the templates cannot be found, warn the teacher and continue — resources will still generate as Markdown, but .docx formatting will use pandoc defaults.

### Step 6: Create Class Folder

1. Read the template file at `guides/student-profile-template.md`
2. Create `{folder-name}/student-profile-template.md` as a copy of the template — this gives the teacher a local reference for the profile format

### Step 7: Ask for Student Names

Use AskUserQuestion to ask:

"Please list the student names, one per line. For example:

Pat Dagg
Barry Crump
Sarah Uma
Liam 0'Brien"

### Step 8: Create Student Profiles

For each name the teacher provided:

- Trim whitespace and skip blank lines
- Convert the name to a folder-safe format (lowercase, spaces to hyphens, strip apostrophes and special characters)
  - Example: "Barry Crump" → `barry-crump`, "Liam O'Brien" → `liam-obrien`
- If the student folder already exists within this class, skip it and note it in the report
- Read `guides/student-profile-template.md`
- Create `{folder-name}/{student-folder-name}/student-profile.md` with the template content

### Step 9: Report and Next Steps

Summarise what was created:

- Class name and folder path
- Number of students added
- List each student name
- Note any students that were skipped (already existed)
- If a CLAUDE.md was created, mention it

Then tell the teacher:

"Your class is set up! Each student has a profile at:

{folder-name}/{student-name}/student-profile.md

To personalise resources for your students, open each profile and fill in their:

- **Reading Level** — e.g., below grade level, at grade level, above grade level
- **Interests** — e.g., dinosaurs, soccer, space, art
- **Learning Needs** — e.g., needs visual aids, extended time, gifted enrichment

Once the profiles are filled in, use /generate-resource to create personalised resources for the whole class."
