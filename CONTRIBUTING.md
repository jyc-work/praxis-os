# Contributing

Thanks for considering a contribution to PraxisOS. This is a small, opinionated
project — please read this before opening an issue or PR.

## Ground rules

- **One problem per PR.** Split unrelated changes.
- **No real personal data, ever.** Fixtures, examples, and tests must use fully
  fictional, de-identified data (see `examples/demo-persona/`).
- **Target `dev` branch**, not `main`.
- **All PRs must complete the PR template** — no blank sections, no placeholders.
- **No LLM dependency in the core.** Everything under `src/praxis` must run
  deterministically without any AI API.
- **Tests and `praxis validate` must pass** before a PR is reviewable.

## Workflow

1. Fork and clone.
2. `python -m venv .venv && pip install -e ".[dev]"`
3. Create a branch: `feat/<short-name>` or `fix/<short-name>`.
4. Make the change; add or update tests alongside it.
5. Run:
   ```bash
   pytest
   praxis validate
   praxis doctor
   ```
6. Commit with a clear message (e.g. `feat(validation): detect orphan principles`).
7. Open the PR against `dev` and fill in the template completely.

## What we are looking for

- New tests / fixtures that catch real gaps in the validator, parser, or privacy scan.
- Documentation corrections (schema drift, outdated examples).
- Schema improvements that stay backwards-compatible.

## What will be rejected

- Bulk or spray-and-pray PRs (multiple unrelated changes in one PR).
- Speculative features with no real problem statement behind them.
- Adding third-party dependencies without demonstrated need.
- Changes that weaken the human-authority or privacy guarantees documented in
  [AGENTS.md](AGENTS.md).
- PRs that include real personal data, even as "example" data.

## Questions

Open an issue with the `question` label. Keep it concrete and attach the files or
commands involved.

---

*Thought is not for worship, but for testing.*