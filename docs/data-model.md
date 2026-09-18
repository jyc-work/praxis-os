# Data Model

> **v0.1 contract.** Machines read the YAML frontmatter (validated against JSON
> Schema); humans read and write the Markdown body.

## Entities

Six and only six core entity types:

```text
VALUE · MODEL · PRINCIPLE · DECISION · EXPERIMENT · REVIEW
```

## IDs

Stable, human-readable, file-path-independent:

```text
TYPE-DOMAIN-NNN
```

Examples:

```text
VALUE-LIFE-001
MODEL-STOICISM-001
PRINCIPLE-CAREER-001
DECISION-CAREER-003
EXPERIMENT-CAREER-002
REVIEW-DECISION-003
```

**An ID never changes because a title changed.** Relations reference IDs only —
never `../principles/foo.md`. If an ID is retired, it is retired for good;
no new file reuses it.

## Schemas (summary — full contracts in `schemas/*.json`)

### value (`schemas/value.schema.json`)

```text
id, type=value, name, name_zh, status, priority, domains, confidence,
created_at, updated_at
```

`status ∈ active | inactive | retired`; `priority ∈ low | medium | high` (schema
also accepts `core`-style narratives outside the contract — see schema file).

Body sections: `Definition`, `Why It Matters`, `Behavioral Evidence`,
`Contradictory Evidence`, `Conflicts`, `Revision History`.

### model (`schemas/model.schema.json`)

```text
id, type=model, model_type, name, status, confidence?, domains, derived_principles?,
created_at, updated_at
```

`model_type ∈ thinker | philosophy | mental-model | world-model`.
Body ends with `My Interpretation` and `Derived Principles` — anything else is
knowledge hoarding.

### principle (`schemas/principle.schema.json`)

```text
id, type=principle, title, status, confidence, domains, sources?, evidence?,
related_values?, related_principles?, related_models?, created_at, updated_at,
last_tested?
```

`status ∈ candidate | testing | validated | core | revised | retired`.

Body sections (required by semantic validation): `Statement`, `Why`, `Evidence`,
`Counter Evidence`, `Boundary`, `Trigger`, `Action Rule`, `Revision History`.

### decision (`schemas/decision.schema.json`)

```text
id, type=decision, title, status, domain, confidence?, decision_date?,
related_values?, related_principles?, related_models?, experiments?,
review_dates?, created_at, updated_at
```

`status ∈ considering | decided | executing | reviewed | abandoned`.

Body sections: `Situation`, `Facts`, `Unknowns`, `Emotion`, `Interests`,
`Objectives`, `Options`, `Trade-offs`, `Relevant Principles`, `Lens Analysis`
(with the five lenses), `Decision`, `Next Action`, `Prediction`, and
`Final Judgment` (human-owned).

### experiment (`schemas/experiment.schema.json`)

```text
id, type=experiment, title, status, hypothesis, start_date?, end_date?,
related_decision?, related_principles?, metrics?,
created_at, updated_at
```

`status ∈ planned | running | completed | abandoned`.
Small, reversible, measurable, time-boxed.

### review (`schemas/review.schema.json`)

```text
id, type=review, review_type, target, status, review_date?,
principles_changed?, created_at, updated_at
```

`review_type ∈ weekly | monthly | quarterly | annual | decision`;
`status ∈ planned | completed | abandoned`.

Body keeps: `Prediction`, `Actual Outcome`, `Difference`, `Decision Quality`,
`Outcome Quality`, `Lessons`, `Principle Impact`.

## Relations

All relations are ID lists inside the frontmatter, resolved at load time via a
repository-wide ID index:

```text
Repository Scan → Build ID Index → Resolve Relations → Report Missing IDs
```

Relation fields by entity:

| Entity | Relation fields |
| --- | --- |
| value | `conflicts_with`, `related_values` (narrative bodies) |
| model | `derived_principles` |
| principle | `sources`, `evidence`, `related_values`, `related_principles`, `related_models` |
| decision | `related_values`, `related_principles`, `related_models`, `experiments`, `review_dates` |
| experiment | `related_decision`, `related_principles` |
| review | `target`, `principles_changed` |

## Placement

Files must live in the directory matching their type (per `praxis.yaml`
`paths`), e.g. principles under `principles/`. Sub-directories by domain
(`principles/career/…`) are allowed; the loader scans recursively.

## Date format

`YYYY-MM-DD`. `null` is allowed where a date has not happened yet
(`last_tested`, `decision_date`, `review_date`).

## Validation levels (what `praxis validate` checks)

1. **Schema** — YAML parses, JSON Schema passes, required fields, enums, dates.
2. **Repository** — no duplicate IDs, every relation target exists, ID prefix
   matches type, entity type matches directory, review targets exist.
3. **Semantic** — principles have `Boundary` + `Counter Evidence`; decisions have
   `Next Action` + `Final Judgment`; experiments have `Hypothesis` + `Metric`;
   reviews have `Actual Outcome` + `Lessons`.
4. **Privacy** — heuristic secret scan (see `docs/privacy.md`).