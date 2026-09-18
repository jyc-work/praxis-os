# Privacy & Data Handling

## The model

```text
Framework  →  PUBLIC
Your data  →  PRIVATE
```

The *framework* — schemas, templates, skills, prompts, methodology, sample data —
is open source. The *content* — journals, decisions about your life, real
positions, identities, relationships — is private by construction.

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

## Agent obligations

Agents operating in this repository (see `AGENTS.md`) must:

- never read `private/` unless the user explicitly hands them a file;
- never echo private content into other files;
- never upload personal data to third parties;
- never commit secrets, even temporarily — treat a committed secret as compromised.

## If a secret leaks anyway

1. Rotate/revoke the credential immediately — deletion alone is not enough.
2. Remove the file from history (history rewrite) if the repo is public.
3. Update the privacy scan if the pattern was not caught.
4. Treat the leak as a security incident, not a lint error.

## CI behaviour

`validate.yml` never checks out or reads `private/`. TODO-style comments are
fine; real data is not.