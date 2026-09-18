# ADR-001: Markdown is the source of truth

- **Status:** Accepted
- **Date:** v0.1

## Context

PraxisOS data must be human-readable, durable, portable, and AI-friendly.
Databases add migration, lock-in and a barrier between people and their own
thinking.

## Decision

All core data lives in **Markdown files with YAML frontmatter**, versioned in
Git. No PostgreSQL, SQLite, vector DB or Notion database in v0.1.

## Consequences

- Users can read, diff and edit their system with any text editor.
- Git provides history, backup and collaboration.
- Migration to any future backend is a parsing exercise.
- The validator must accept responsibility for data quality instead of a DB.