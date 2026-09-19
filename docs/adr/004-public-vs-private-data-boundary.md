# ADR-004: Public vs private data boundary

- **Status:** Accepted
- **Date:** 2026-09-19 (Dogfooding #1)

## Context

During Dogfooding #1 the first real principle (`PRINCIPLE-CAREER-001`, full
version with real autobiographical evidence) was mistakenly committed to the
public repository in `ba49ffa`. The real version was then moved to the local
private repository and `ba49ffa` was removed from public history via
`push --force-with-lease`. This ADR fixes the boundary so it cannot drift again.

## Decision

Data in this project lives at exactly one of three levels:

| Level | Content | Allowed home |
| --- | --- | --- |
| `PUBLIC_FRAMEWORK` | schemas, skills, templates, docs, CLI, methodology | public repo |
| `ANONYMIZED_EXAMPLE` | real-derived content stripped of identifiable details (names, employers, departments, events) | public repo |
| `PRIVATE_PERSONAL` | raw real experiences, emotions, evidence, decisions, reviews, assets, workplace details | local `PraxisOS-data` only |

Rules:

1. The public repository may only contain `PUBLIC_FRAMEWORK` and
   `ANONYMIZED_EXAMPLE` content.
2. Real autobiographical evidence must never be committed to the public
   repository.
3. The private data repository must have no remote by default; it stays
   local-only.
4. When public content is derived from real experience, it must be generalized
   beyond recognition before commit: anonymize → review → commit.

## Consequences

- Public examples must be synthetic or explicitly anonymized.
- Agents must never copy private evidence into public files.
- A public history leak is handled by history rewrite (`--force-with-lease`,
  never a bare `--force`), with the understanding that existing clones, forks
  and caches cannot be guaranteed to disappear.
- The privacy scan is a credential tripwire, not a PII classifier — reviewers
  remain responsible for the boundary above.