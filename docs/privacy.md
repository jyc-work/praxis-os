# Privacy & Data Handling

## The model

```text
Framework  →  PUBLIC
Your data  →  PRIVATE
```

The *framework* — schemas, templates, skills, prompts, methodology, sample data —
is open source. The *content* — journals, decisions about your life, real
positions, identities, relationships — is private by construction.

Data is classified at exactly one of three levels (ADR-004):

```text
PUBLIC_FRAMEWORK
    ↓ (anonymize beyond recognition)
ANONYMIZED_EXAMPLE
    ↓ (only in the local private repo)
PRIVATE_PERSONAL
```

| Level | Examples | Home |
| --- | --- | --- |
| `PUBLIC_FRAMEWORK` | schemas, skills, templates, docs, CLI, methodology | public repo |
| `ANONYMIZED_EXAMPLE` | principles/decisions stripped of real names, employers, departments, events | public repo |
| `PRIVATE_PERSONAL` | raw real evidence, decisions, reviews, assets, workplace details | local `PraxisOS-data` only |

## Default gitignore

```gitignore
/private/**
/data/private/**
/journals/private/**
.env
*.secret.*
credentials.*
```

Anything that should never be versioned goes under `private/`, which the
repository tooling never scans and Git never tracks.

## Heuristic scan (`praxis validate`)

The validator's privacy check looks for obvious tripwires in tracked files:

- API key patterns (`sk-…`, `AIza…`, AWS `AKIA…` shape)
- private key blocks (`-----BEGIN … PRIVATE KEY-----`)
- access tokens (e.g. `ghp_…`, `xoxb-…`)
- password-like assignments (`password = …`, `passwd: …`)
- email addresses and phone numbers
- credential-looking filenames (`*.pem`, `*.key`, `id_rsa`, `.env`, `credentials.*`)

Severity: `ERROR` → CI fails. The scan is heuristic: it is a tripwire, not a
classifier. It does not do OCR, ML, or full PII taxonomy in v0.1.

## Rules for sample data

All sample and fixture data must be:

- entirely fictional;
- de-identified;
- free of any user's real experiences.

The demo persona (Alex) is a fictional construct. If a real experience is needed
for illustration, generalise it beyond recognition.

## Public repository boundary

Hard rule:

```text
PUBLIC REPOSITORY RULE

Never write real autobiographical evidence,
real workplace events,
real financial data,
real relationship details,
or identifiable personal context
into the public PraxisOS repository.

Public examples must be:
1. synthetic, or
2. explicitly anonymized/generalized.

Real evidence belongs only in the private data repository.
```

Data matrix (see ADR-004 for the full decision):

| Data | Public PraxisOS | Private PraxisOS-data |
| --- | --- | --- |
| Schema / Template | ✓ | |
| Skill | ✓ | |
| Methodology | ✓ | |
| Synthetic Demo | ✓ | |
| Generalized Principle | ✓ | ✓ |
| Real Evidence | ✗ | ✓ |
| Real Decision | ✗ | ✓ |
| Real Review | ✗ | ✓ |
| Names / company / department | ✗ | ✓ |
| Income / assets / positions | ✗ | ✓ |

If real-life detail has already been committed publicly, remove it from history
with `git push --force-with-lease` and treat earlier clones/forks/caches as
out of your control.

## Agent obligations

Agents operating in this repository (see `AGENTS.md`) must:

- never read `private/` unless the user explicitly hands them a file;
- never echo private content into other files;
- never upload personal data to third parties;
- never commit secrets, even temporarily — treat a committed secret as compromised;
- never write real autobiographical evidence into the public repository
  (PUBLIC_FRAMEWORK / ANONYMIZED_EXAMPLE only — see ADR-004).

## If a secret leaks anyway

1. Rotate/revoke the credential immediately — deletion alone is not enough.
2. Remove the file from history (history rewrite) if the repo is public.
3. Update the privacy scan if the pattern was not caught.
4. Treat the leak as a security incident, not a lint error.

## CI behaviour

`validate.yml` never checks out or reads `private/`. TODO-style comments are
fine; real data is not.