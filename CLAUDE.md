# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Claude Code plugin repository. Each top-level directory is a standalone plugin that can be installed via the Claude Code plugin marketplace. Currently contains one plugin: **class-toolkit**.

See the [Claude Code plugin docs](https://docs.anthropic.com/en/docs/claude-code/plugins) for the plugin convention reference.

## Repository Structure

Plugins follow the Claude Code plugin convention:
- `.claude-plugin/plugin.json` — plugin metadata, version, and hooks
- `skills/` — each subdirectory contains a `SKILL.md` defining a slash command
- `guides/` — reusable resource prompt templates
- `templates/` — pandoc reference `.docx` files for year-level formatting

## Commit Convention

Use conventional commits scoped to the plugin name:
```
type(class-toolkit): description
```
Types: `feat`, `fix`, `refactor`, `chore`, `docs`

## Versioning

When making changes to a plugin, bump the version in its `.claude-plugin/plugin.json`. Use semver: patch for fixes, minor for new features, major for breaking changes. When bumping the version, also update `CHANGELOG.md` with a summary of changes since the last release.

Only bump once per push — if `plugin.json` already has an unpushed version bump, update the existing changelog entry instead of bumping again.

## Structural Changes

When moving files, renaming directories, adding top-level folders, or changing frontmatter fields, also update the migration step (Step 3) in `skills/class-toolkit-update/SKILL.md`. Add a new sub-step that detects the old layout and migrates to the new one. This is the only mechanism for existing users to transition after updating.

## Update Plugin

Use the `/class-toolkit:class-toolkit-update` skill to update the class-toolkit plugin to the latest version. The underlying commands are:

```bash
claude plugin marketplace update hamishnorton
claude plugin update class-toolkit@hamishnorton --scope user
```
