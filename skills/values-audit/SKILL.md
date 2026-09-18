# Name

values-audit

# Purpose

Compare what the user **claims** to value with what their **observed decisions
and behaviour** reveal. Use it periodically (e.g. before the quarterly review)
or when the user senses a mismatch between their words and their life.

The skill only reports *possible conflicts* — it never diagnoses the user's
psychology and never rewrites their values.

# Inputs

- optionally the quarter or date range to audit;
- optionally a specific claimed value to focus on.

# Required Context

Read:

- `constitution/values.md` and `constitution/anti-values.md`;
- `values/*.md` (claimed values, with behavioral evidence sections);
- `decisions/*.md` from the period (statuses decided/executing/reviewed);
- `experiments/*.md` and `reviews/*.md` from the period.

# Procedure

1. **Collect claimed values.** From `values/` and the constitution, list the
   values the user says matter most (priority high).
2. **Collect observed behaviour.** From decisions, experiments and reviews,
   list what the user actually did — especially where decisions contradict a
   claimed value.
3. **Compare.**

   ```text
   Claimed:    Autonomy
   Observed:   3 major decisions favored familiarity/security
   Possible tension: Autonomy ↔ Security
   ```

4. **Count, don't judge.** Present discrepancies as patterns with numbers
   ("2 of 3 job decisions prioritized stability"), never as character
   verdicts.
5. **Ask, don't conclude.** End each finding with a question:
   "这是价值观的冲突，还是环境限制导致的权宜之计？" Let the user interpret.
6. **Never modify values.** Report only.

# Output Contract

```text
Claimed Values:
- <value> (priority)

Observed Behaviors:
- <behaviour with decision/experiment ID>

Possible Value Conflicts:
- <value A> ↔ <value B> (evidence: <ID>)
- <possible behavior mismatch: claimed X vs observed Y>

Open Questions:
- <question for the user>
```

Only tentative language is allowed:

```text
possible value conflict
possible behavior mismatch
```

# Write Permissions

- **Read:** `values/`, `decisions/`, `experiments/`, `reviews/`, `constitution/`.
- **Write:** none by default. The audit is a report. If the user asks for a
  summary file, write it under `reviews/` (Level A) as a review-type entry —
  never into `values/` or `constitution/`.

# Forbidden Actions

- never state "你其实不重视 X" as a conclusion — only "possible conflict";
- never make definitive psychological claims;
- never modify values or the constitution;
- never use a single decision as proof of a pattern;
- never ignore contradictory evidence that supports the claimed value.

# Examples

- `examples/input-01.md` — a period's decisions mentioning autonomy vs stability.
- `examples/output-01.md` — the audit report with `possible value conflicts`.