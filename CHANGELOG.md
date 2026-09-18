# Changelog

All notable changes to PraxisOS are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

- Planned: full-text + metadata search hardening, relation graph, review reminders.

## [0.1.0] - 2026-09-18

### Added

- **Repository foundation** — README, LICENSE (MIT), CONTRIBUTING, SECURITY,
  AGENTS.md, ARCHITECTURE.md, `docs/` (philosophy, methodology, privacy,
  data-model, skill-spec, roadmap, three ADRs), `praxis.yaml` config.
- **Data model** — six JSON Schemas (`value`, `model`, `principle`, `decision`,
  `experiment`, `review`) and seven Markdown templates.
- **Core engine** — entity model, frontmatter parser (with YAML date
  normalisation), repository loader (private/ignored paths excluded), in-memory
  index, stable ID utilities (`TYPE-DOMAIN-NNN`), ID-based relation resolution.
- **Validation** — `praxis validate` with four layers: JSON Schema conformance,
  repository integrity (duplicate IDs, broken relations, wrong prefixes,
  placement), semantic checks (boundary, counter evidence, next action, final
  judgment, hypothesis, metrics), and a heuristic privacy scan
  (API keys, private keys, tokens, passwords, emails, phones, credential
  filenames). Stable exit codes (0 = clean, 1 = ERROR/FATAL).
- **CLI** — `praxis new` (value/model/principle/decision/experiment/review),
  `praxis search` (full-text + metadata filters), `praxis doctor` (health
  report: orphans, untested principles, overdue reviews, stale constitution…).
- **Agent skills** — four instruction contracts with example input/output:
  `principle-extractor`, `decision-review`, `values-audit`, `quarterly-review`.
- **Demo persona** — fully fictional end-to-end example (Alex) demonstrating
  Value → Principle → Decision → Experiment → Review → Principle Revision.
- **CI & hardening** — GitHub Actions (`test.yml`, `validate.yml`),
  pre-commit hooks, repository privacy self-scan, 113 tests.

### Fixed

- none (initial release)

### Notes

- Core (`validate`, `search`, `new`, `doctor`) is fully deterministic and
  requires no LLM or network access by design.

[0.1.0]: https://github.com/nomiga-ww/praxis-os/releases/tag/v0.1.0