# Release Checklist — v0.1.0

Use this list before tagging any release.

> **原则：如果 v0.1 的思想闭环本身不好用，任何 AI 和 RAG 都只是放大一个不好用的系统。**

## v0.1-rc（当前，engineering complete）

已完成：打 tag `v0.1-rc` 并 push（**不打 GitHub Release**）；进入 Personal Dogfooding。

## Code & quality

- [ ] All tests pass: `pytest`
- [ ] Coverage of core modules: `pytest --cov=praxis --cov-fail-under=70`
- [ ] `praxis validate --root examples/demo-persona` passes (exit 0)
- [ ] Demo persona is complete: 3 values, 2 models, 5 principles, 2 decisions,
      1 experiment, 2 reviews — including one principle revision and one
      prediction-vs-actual review
- [ ] Negative control still fails: `praxis validate --root tests/fixtures/invalid_repo` → exit 1
- [ ] Repository privacy self-scan passes: `python -m praxis.validate_repo_self`
- [ ] Skill contracts intact: every `skills/*/SKILL.md` has all required headings;
      no example promotes a principle beyond `candidate`

## Compliance & hygiene

- [ ] No real private data anywhere in the repository (demo is fictional)
- [ ] No secrets in history — run self-scan before and after commit
- [ ] `LICENSE` present (MIT)
- [ ] `README.md` complete (What / Why / Concepts / Quick Start / Structure /
      Workflow / Privacy / Agent Safety / Roadmap / License)
- [ ] `SECURITY.md` complete
- [ ] `AGENTS.md` complete (authority, permission levels, forbidden actions)
- [ ] `CHANGELOG.md` updated

## Release mechanics

- [ ] `CHANGELOG.md` entry for this version
- [ ] Version bumped in `pyproject.toml` and `src/praxis/__init__.py`
- [ ] Tag: `git tag v0.1.0`
- [ ] Push tag; GitHub Actions `test` and `validate` both green on the tag
- [ ] Release notes drafted from CHANGELOG

## Post-release

- [ ] Update `docs/roadmap.md` (mark v0.1.0 tag item done)
- [ ] Announce / document v0.2 candidates in a new GitHub Milestone