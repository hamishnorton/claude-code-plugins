# Class Toolkit

Generate personalised educational resources for each student in your class from a single prompt.

## Getting Started

Follow the setup guide for your role:

- **Teachers** — [Teacher Setup Guide](Teacher-Setup-Guide.md) — subscribe to Claude Pro, install the plugin, and create your first class
- **School IT / Admins** — [Admin Setup Guide](Admin-Setup-Guide.md) — install the required software on teacher machines (Windows)

## Prerequisites

- [Pandoc](https://pandoc.org/installing.html) — required by `generate-resource` to create Word documents

## How it works

1. **Set up your class** — run `/init-class` to create a class and add student names
2. **Fill in student profiles** — open each student's `student-profile.md` and add their reading level, interests, and learning needs
3. **Generate resources** — run `/generate-resource` with a prompt or guide name, and every student receives a personalised version

## Installation

Add the `hamishnorton/claude-code-plugins` marketplace, then install the plugin:

```
/plugin marketplace add <owner>/claude-code-plugins
/plugin install class-toolkit@hamishnorton
```

Replace `<owner>` with the GitHub username or organisation that hosts this repository.

## Skills

### `/init-class [class name]`

Creates a class folder and a student profile for each student you list.

- Prompts for a class name and student names
- Creates `{class-name}/{student-name}/student-profile.md` for each student
- Can add students to an existing class

### `/generate-resource [prompt or guide name]`

Generates a personalised resource for every active student in a class.

- Accepts a free-text prompt (e.g. "Create a 500 word fantasy story about teamwork") or the name of a saved guide
- If no argument is given, lists available guides to choose from
- New prompts are automatically saved as reusable guides
- Launches one agent per student in parallel for fast generation

## Guides

Resource prompts are saved as reusable guides in `guides/`. The plugin includes three examples:

- **Fantasy Story Perseverance** — a 300 word fantasy story about perseverance
- **Find Adjectives** — a word find looking for 10 adjectives
- **Maths Questions** — a maths word question set

Create your own by passing any prompt to `/generate-resource` — it will be saved automatically for next time.

## Student profiles

Each student has a `student-profile.md` with three fields to fill in:

- **Reading Level** — e.g. below grade level, at grade level, above grade level
- **Interests** — e.g. dinosaurs, soccer, space, art
- **Learning Needs** — e.g. needs visual aids, extended time, gifted enrichment

Students must have `active: true` in their profile frontmatter to receive generated resources.
