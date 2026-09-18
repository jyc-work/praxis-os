# Name

decision-review

# Purpose

Help the user think through a real decision in front of them — deliberately,
not impulsively. Use it whenever there is a significant choice (job, money,
relationship, relocation, project) and the user wants structure.

The skill produces analysis. **The human produces the judgment.**

# Inputs

- a description of the decision (situation, what is being chosen);
- how urgent it is, and by when a decision is needed (if known).

# Required Context

Read (if present):

- `constitution/constitution.md` and `constitution/values.md`;
- relevant `principles/<domain>/*.md`;
- relevant past `decisions/` in the same domain (especially with reviews);
- relevant `models/` the user has studied (for the Lens Analysis).

# Procedure

1. **Facts.** List only verifiable facts. Label them `fact:`.
2. **Unknowns.** List what is not known, and how it could be learned cheaply.
3. **Emotion.** Name the current emotion and how it might bias the judgment.
4. **Interests.** What is at stake for the user (and for whom else)?
5. **Objectives.** What does the user want to achieve, concretely?
6. **Options.** Enumerate at least two real options (including "do nothing").
7. **Relevant principles.** Which existing principles apply? Quote their
   action rules.
8. **Lens Analysis.** For each lens the user has studied, give a
   *perspective*, never a verdict:
   ```text
   Stoicism suggests:   <one insight>
   Potential limitation: <one weakness of that lens here>
   ```
   Five default lenses: Machiavelli (interests/power), Legalism (rules and
   incentives), Stoicism (what is controllable), Adler (what purpose does the
   current behaviour serve — am I avoiding?), Taoism (is this problem worth
   solving, is there over-action?).
9. **Trade-offs.** For each option, state what is lost. A choice with no named
   cost is incomplete.
10. **Small experiment.** If uncertainty is high, propose the smallest
    reversible test that produces information (24–72h).
11. **Stop.** Write:
    ```
    Final Judgment: Human Required
    ```
    Do not fill in the Decision or the Final Judgment.

# Output Contract

```text
Facts
Unknowns
Emotion
Interests
Objectives
Options
Trade-offs
Relevant Principles
Lens Analysis
Reversible Experiment
Final Judgment: Human Required
```

# Write Permissions

- **Level B (suggest only):** `decisions/`. You may draft the full decision
  file with the template's analytic sections filled.
- The sections `# Decision`, `# Next Action` and anything under `# Final
  Judgment` stay empty unless the user writes them.
- You may create a draft in `decisions/` only after the user asks; otherwise
  keep the analysis in the chat.

# Forbidden Actions

- never write an AI recommendation as `Final Judgment`;
- never present a lens as an answer: "Stoicism says X → therefore you must X"
  is forbidden;
- never decide for the user, never push one option;
- never modify `constitution/`;
- never skip the emotion or the unknowns sections;
- never claim an outcome in advance as a fact.

# Examples

- `examples/input-01.md` — a job choice (IC vs management) with context.
- `examples/output-01.md` — the analytic output ending in
  `Final Judgment: Human Required`.