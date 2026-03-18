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

**If one class is found:** use it automatically and tell the teacher which class is being used.

**If multiple classes are found:** use AskUserQuestion to ask which class to generate resources for. List each class name as an option, plus an "All classes" option.

**If no student profiles are found:** inform the teacher that no classes have been set up yet, suggest they run `/init-class` first, and stop.

For each profile in the selected class(es), read it. Only include students where the frontmatter contains `active: true`.

Extract from each:

- **Student name**: The student's folder name, replacing hyphens with spaces and title-casing (e.g., `barry-crump` → "Barry Crump")
- **Student folder path**: Full path to the student's folder
- **Profile content**: The full content of `student-profile.md`

If no active students are found, inform the user and stop.

### Step 3: Derive Filename

Generate a filename from the resource prompt:

- Extract the key topic words (drop filler words like "create", "a", "the", "word", numbers)
- Convert to Title-Case-With-Hyphens format
- Append `.md`
- Example: "Create a 500 word fantasy story about teamwork" → `Fantasy-Story-Teamwork.md`

Tell the user the filename that will be used and list the students who will receive the resource.

### Step 4: Generate Resources in Parallel

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
- Write the resource in Markdown format
- Do NOT include YAML frontmatter

Write the completed resource to: {student folder path}/{filename}
```

### Step 5: Report

After all agents complete, summarise:

- How many students received the resource
- The filename used
- List each student name and confirm their file was created
- Note any issues or agents that failed
