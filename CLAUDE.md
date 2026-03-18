# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Claude Code plugin repository. Each top-level directory is a standalone plugin that can be installed via the Claude Code plugin marketplace. Currently contains one plugin: **class-toolkit**.

## Repository Structure

Plugins follow the Claude Code plugin convention:
- `.claude-plugin/plugin.json` — plugin metadata, version, and hooks
- `skills/` — each subdirectory contains a `SKILL.md` defining a slash command
- `guides/` — reusable resource prompt templates
- `templates/` — pandoc reference `.docx` files for year-level formatting

## class-toolkit Plugin

An educational tool for teachers to generate personalised resources for students. Two skills:
- **init-class** — creates class folders with student profile scaffolding
- **generate-resource** — launches parallel agents to create personalised `.md` and `.docx` resources per student, using pandoc with year-level reference templates

The generate-resource skill discovers students via `**/student-profile.md` glob, extracts year level from the class folder name (e.g. `year-5-blue` → year 5), and uses the corresponding `templates/year-{N}-ref.docx` for pandoc conversion.

## Key Commands

Regenerate the pandoc reference templates (requires pandoc installed):
```
python3 class-toolkit/generate-templates.py
```

## Commit Convention

Use conventional commits scoped to the plugin name:
```
type(class-toolkit): description
```
Types: `feat`, `fix`, `refactor`, `chore`, `docs`

## Versioning

When making changes to a plugin, bump the version in its `.claude-plugin/plugin.json`. Use semver: patch for fixes, minor for new features, major for breaking changes.
