---
name: init-class
description: "Set up a new class with student profiles. Use when the teacher wants to initialise a class, add students, set up the class structure, or get started with the class toolkit. Also use when the user says things like 'create a class', 'add my students', 'set up my class', or 'get started'."
argument-hint: "[class name]"
---

# Initialise Class

Create a new class folder under `class-agent/` and generate a student profile for each student.

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

Use Glob to check if `class-agent/{folder-name}/` already exists.

- If it exists, tell the teacher: "A class called '{class name}' already exists. Would you like to add more students to it?"
- Use AskUserQuestion to confirm. If no, stop. If yes, skip to Step 5.

### Step 4: Create Class Folder

1. Read the template file at `class-agent/guides/student-profile-template.md`
2. Create `class-agent/{folder-name}/student-profile-template.md` as a copy of the template — this gives the teacher a local reference for the profile format

### Step 5: Ask for Student Names

Use AskUserQuestion to ask:

"Please list the student names, one per line. For example:

Arie Norton
Mia Chen
Liam O'Brien"

### Step 6: Create Student Profiles

For each name the teacher provided:
- Trim whitespace and skip blank lines
- Convert the name to a folder-safe format (lowercase, spaces to hyphens, strip apostrophes and special characters)
  - Example: "Arie Norton" → `arie-norton`, "Liam O'Brien" → `liam-obrien`
- If the student folder already exists within this class, skip it and note it in the report
- Read `class-agent/guides/student-profile-template.md`
- Create `class-agent/{folder-name}/{student-folder-name}/student-profile.md` with the template content

### Step 7: Report and Next Steps

Summarise what was created:
- Class name and folder path
- Number of students added
- List each student name
- Note any students that were skipped (already existed)

Then tell the teacher:

"Your class is set up! Each student has a profile at:

  class-agent/{folder-name}/{student-name}/student-profile.md

To personalise resources for your students, open each profile and fill in their:
- **Reading Level** — e.g., below grade level, at grade level, above grade level
- **Interests** — e.g., dinosaurs, soccer, space, art
- **Learning Needs** — e.g., needs visual aids, extended time, gifted enrichment

Once the profiles are filled in, use /generate-resource to create personalised resources for the whole class."
