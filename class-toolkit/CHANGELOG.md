# Changelog

All notable changes to the class-toolkit plugin are documented in this file.

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
