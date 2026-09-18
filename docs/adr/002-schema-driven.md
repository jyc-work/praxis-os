# ADR-002: Schema-driven data

- **Status:** Accepted
- **Date:** v0.1

## Context

Free-form Markdown makes *machines* unable to trust the repository. Agents need
stable fields to reason over; CI needs to reject broken files; relations need a
predictable shape.

## Decision

The YAML frontmatter of every entity **must validate against a JSON Schema**
(`schemas/*.schema.json`). The Markdown body carries human expression.

```text
Metadata → machine understanding
Body     → human expression
```

## Consequences

- Illegal statuses, missing IDs and bad dates are caught by `praxis validate`.
- New entities follow the same contract, so tooling stays uniform.
- Humans can still write freely in the body — only metadata is constrained.