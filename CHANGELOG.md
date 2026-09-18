# Changelog

All notable changes to PraxisOS are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

- **Personal Dogfooding (Phase 8)** — 用真实人生数据连续使用几周，不增加大功能；
  重点观察：记录成本、Principle/Value 混淆、Decision 模板轻重、Relation 实用性、
  Review 是否真正修订原则、Skill 是否减少思考负担。
- **v0.1.0 Release Gate** — Clean clone 安装、Windows/Linux 各跑一次、README Quick
  Start 照做、validate 零 error、secret/privacy scan、Git 历史隐私检查（含已删除
  提交）、license/attribution 检查、覆盖率口径统一、打 v0.1.0 tag 后生成 Release。
- Planned (v0.2+): full-text + metadata search hardening, relation graph, review reminders.

## [0.1-rc] - 2026-09-18

### Status

**v0.1 Engineering Complete — Architecture Review Passed**
（独立代码审查修复：decision 模板 Final Judgment、schemas 打包、semantic 配置开关、
MISSING_REVIEW_TARGET、new 冲突报错、review 模板 status=planned）

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

[0.1-rc]: https://github.com/jyc-work/praxis-os/releases/tag/v0.1-rc