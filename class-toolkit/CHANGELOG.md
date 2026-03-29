# Changelog

All notable changes to the class-toolkit plugin are documented in this file.

## [0.10.0] — 2026-03-29

### Added

- File structure migration step in update-plugin skill
- Detects and fixes outdated layouts from previous plugin versions
- Migrations: unwrap class-agent nesting, wrap in ClassResources, provision templates, clean up old template copies, add missing year-level to profiles, install Andika font, nest flat progression files

## [0.9.0] — 2026-03-29

### Added

- Generate-progression skill for importing educational progressions, scope and sequences, or curriculum frameworks
- Analyses resources (files or URLs) and creates structured progression files
- Recommends and applies tracking frontmatter fields to student profiles
- Supports applying values uniformly or individually per student

## [0.8.2] — 2026-03-28

### Changed

- Set A4 page size in reference docx templates
- Refined Step 10 student input to use structured options

## [0.8.1] — 2026-03-26

### Added

- Markdown explanation link in README for teachers unfamiliar with .md files
- Optional Prettier formatter setup step in Teacher Setup Guide

## [0.8.0] — 2026-03-26

### Added

- Year-level moved from class-wide setting to individual student profiles
- Init-class output now wrapped in a ClassResources folder
- Andika fonts installed system-wide instead of embedded in each .docx
- Windows launcher script (class-toolkit.bat) integrated into admin setup
- NZ/British English specified for resource generation

## [0.5.1] — 2026-03-24

### Added

- Update-plugin skill for updating from the marketplace
- Andika font embedded in DOCX for cross-platform rendering
- Windows support for pandoc and template copying
- .docx templates provisioned during class setup
- Templates tracked directly in the repository

## [0.1.1] — 2026-03-18

### Added

- Pandoc dependency check via SessionStart hook
- Template generation and year-level formatting for resources
- CLAUDE.md creation during init-class setup

### Changed

- Removed class-agent folder nesting
- Restructured plugin marketplace to match Claude Code spec

## [0.1.0] — 2026-03-16

### Added

- Initial release
- Init-class skill for setting up a class with student profiles
- Generate-resource skill for creating personalised resources per student
