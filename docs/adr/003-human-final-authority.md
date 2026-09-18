# ADR-003: Human final authority

- **Status:** Accepted
- **Date:** v0.1

## Context

The value of PraxisOS collapses if the AI becomes the judge of the user's own
life. The system exists to make *human* reasoning better, not replaceable.

## Decision

The human is the final authority. Agents:

- never modify `/constitution` without explicit approval;
- never promote a principle to `validated`/`core`;
- never fill in `Final Judgment` with their own recommendation;
- always separate facts, inferences, emotions, values and predictions.

Enforced in `AGENTS.md`, in the skill contracts, and structurally (Level A/B/C
permission model).

## Consequences

- The system is safe to hand to an AI assistant.
- Some automation is intentionally sacrificed for authority and trust.
- The "final judgment" sections in decision files are visibly human-owned.