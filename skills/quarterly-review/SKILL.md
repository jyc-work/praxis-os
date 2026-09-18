# Name

quarterly-review

# Purpose

Synthesise the past quarter from the repository's own record — decisions,
experiments, principles and reviews — into one honest report with a next-quarter
focus. Run it at the end of each quarter, before writing the quarterly review
file.

The master question:

> 过去三个月，我是在变得更加自由，还是更加依赖？

# Inputs

- the quarter to review (e.g. `2026-Q3`); default: the quarter that just ended.

# Required Context

Read (filter to the quarter):

- `decisions/*.md` — decisions made, statuses, review dates;
- `experiments/*.md` — hypotheses, outcomes;
- `reviews/*.md` — weekly/monthly/quarterly reviews, decision reviews;
- `principles/*.md` — status changes, revisions, last_tested;
- `constitution/*.md` — to compare behaviour against stated values.

# Procedure

1. **Collect the record.** List decisions, experiments, reviews by ID with
   dates, and principle status changes (created / revised / promoted / retired).
2. **Find repeated patterns.** What themes appear across episodes?
3. **Mark successful vs failed assumptions.** For each experiment and each
   decision review: did the prediction hold?
4. **Detect value conflicts.** Cross-reference the values-audit: did behaviour
   contradict claimed values?
5. **List principle candidates.** What new principles should be extracted?
6. **Assess direction drift.** Compare behaviour with the constitution's
   direction: closer or further?
7. **Write the next-quarter focus.** At most 3 concrete areas, each with a
   small measurable experiment.
8. **Stop before judgment.** Present findings; the direction change, if any,
   is the user's call.

# Output Contract

```text
Quarter: <2026-Q3>

Repeated Patterns:
- <pattern with evidence IDs>

Successful Assumptions:
- <assumption → evidence it held>

Failed Assumptions:
- <assumption → counter evidence>

Value Conflicts:
- <possible conflict>

Principle Candidates:
- <candidate principle with trigger>

Direction Drift:
- <toward / away from constitution direction, with evidence>

Next Quarter Focus:
- <area 1> → <small experiment>
- <area 2> → <small experiment>
```

# Write Permissions

- **Level A (read/write):** `reviews/`. You may create
  `reviews/quarterly/<REVIEW-QUARTERLY-NNN>.md` using the quarterly template
  **after the user confirms** the content.
- Everything else in the repository is read-only for this skill.

# Forbidden Actions

- never decide direction changes for the user;
- never promote principles (that is `principle-extractor`'s domain, and even
  there only to `candidate`);
- never rewrite history or silently edit past review files;
- never ignore failed assumptions to make the quarter look better;
- never edit `constitution/`.

# Examples

- `examples/input-01.md` — a fictional quarter's decision/experiment/review IDs.
- `examples/output-01.md` — the synthesized report in the Output Contract.