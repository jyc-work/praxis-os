# Security

## Scope

PraxisOS is a local-first personal decision system. Its security properties are
designed around one threat: **accidentally publishing private life data** through
the public repository, CI artifacts, or exported copies.

## Reporting vulnerabilities

Please report security issues privately rather than in public issues:
open a GitHub Security Advisory or email the maintainers directly. Do not include
personal data in the report.

## Privacy controls

1. **gitignore** — `/private/**`, `/data/private/**`, `/journals/private/**`,
   `.env`, `*.secret.*`, `credentials.*` are ignored by default.
2. **`praxis validate`** — runs a heuristic privacy scan over tracked content:
   - API key patterns (e.g. `sk-...`, `AIza...`, AWS access key shape)
   - private key blocks (`-----BEGIN ... PRIVATE KEY-----`)
   - access tokens and `password = ...` style assignments
   - email addresses and phone numbers
   - credential-looking filenames (`*.pem`, `*.key`, `id_rsa`, `credentials.*`)
3. **CI** — `validate.yml` runs `praxis validate`; `ERROR`-severity findings
   fail the build, so secrets cannot silently merge.

The scan is heuristic by design: it is a tripwire, not a classification system.
It never attempts OCR or ML-based PII detection in v0.1.

## Commit hygiene

- Never add personal data to the repository, even temporarily.
- If you must test a feature, use synthetic data under `tests/fixtures/` or
  `examples/demo-persona/`.
- Before pushing, run `praxis validate` and inspect the diff for accidental files.
- If a real secret ever lands in history, treat it as compromised: rotate it and
  rewrite history, do not merely delete the file.

## Agent behaviour

AI agents operating in this repository are bound by [AGENTS.md](AGENTS.md):
they must not read `private/`, must not upload personal data to third parties,
and must not auto-execute irreversible actions (resignation, transactions,
messages) on the user's behalf.

## Supported versions

Only the current `main` release (v0.1.x) receives security fixes. Security issues
in pre-release branches should be reported as normal bugs.