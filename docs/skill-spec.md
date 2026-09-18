# Skill Specification

> **Agent skills are instruction contracts, not code.**

A skill is a folder:

```text
skills/<skill-name>/
├── SKILL.md
└── examples/
    ├── input-01.md
    └── output-01.md
```

`SKILL.md` is a Markdown contract with a **fixed set of headings**. Every skill
must contain all of them.

## Required headings

```markdown
# Name

# Purpose

one paragraph: when to use this skill, and why it exists

# Inputs

what the user/context provides

# Required Context

which files the agent must read first
(constitution, values, principles, decisions…)

# Procedure

numbered steps the agent must follow in order

# Output Contract

the exact structure the skill must produce

# Write Permissions

what the skill may create/modify, and under which permission level (A/B/C)

# Forbidden Actions

what the skill must never do — aligned with AGENTS.md

# Examples

links into examples/ with input/output pairs
```

## Cross-cutting rules (all skills)

1. **Human authority.** Never write a `Final Judgment`, never decide for the user.
   End analytic output with `Final Judgment: Human Required`.
2. **No automatic promotion.** A principle may only be created/recorded as
   `candidate`; `testing`, `validated`, `core` require human decision.
3. **Counter evidence always.** Wherever a principle is proposed, the skill must
   elicit `counter_evidence` and `boundary`; otherwise the output is a slogan.
4. **Fact / inference / emotion / value / prediction** must be explicitly
   labelled; never blur them.
5. **Permission levels** from AGENTS.md apply: A (reviews, experiments) may
   write; B (principles, values, models) propose patches; C (constitution) read-only.
6. **Defence against echo chamber.** Lenses (in decision-review) are
   *perspectives*, never verdicts:

   ```text
   Stoicism suggests:   X
   Potential limitation: Y
   User judgment:       Z
   ```

   never:

   ```text
   Stoicism says X → therefore you must X
   ```

## The four v0.1 skills

| Skill | Folder | Output |
| --- | --- | --- |
| principle-extractor | `skills/principle-extractor/` | principle candidate + action rule |
| decision-review | `skills/decision-review/` | structured analysis + human-required judgment |
| values-audit | `skills/values-audit/` | possible value conflicts (never verdicts) |
| quarterly-review | `skills/quarterly-review/` | quarterly synthesis with next-quarter focus |

## Golden output formats

### principle-extractor

```yaml
candidate_principle: present
statement:
source:
reasoning_summary:
evidence:
counter_evidence:
boundary:
trigger:
action_rule:
status: candidate
```

### decision-review

```text
Facts → Unknowns → Emotion → Interests → Objectives → Options → Trade-offs
→ Relevant Principles → Lens Analysis → Reversible Experiment
→ Final Judgment: Human Required
```

### values-audit

Only tentative findings are allowed:

```text
possible value conflict:  Autonomy ↔ Security
possible behavior mismatch: claimed X vs observed Y
```

### quarterly-review

```text
Repeated Patterns
Successful Assumptions
Failed Assumptions
Value Conflicts
Principle Candidates
Direction Drift
Next Quarter Focus
```

## Testing golden examples

Fixture inputs in `examples/` have expected outputs that only check **required
sections exist** (structure), not exact wording. Semantic quality testing of
skills arrives with real AI evaluation in v0.3.