# Name

principle-extractor

# Purpose

Turn raw material — a conversation, a book note, a video, an experience, a
failure or a success — into a **principle candidate** with an explicit
`IF / THEN` action rule. Use it whenever the user says something like "我觉得我
应该…" or "我从这件事里学到…" and it relates to how they act.

The skill exists to close the gap between *input* and *action*. It never
produces a validated principle: every output starts at `candidate`.

# Inputs

One of:

- a conversation excerpt about an experience or belief;
- a book / video note containing a claim about how the world works;
- a description of a success or failure and what the user concludes from it;
- an observation about their own repeated behaviour.

Optionally a target `domain` (career / life / finance / relationships / …).

# Required Context

Before drafting, read (if present in the repository):

- `constitution/constitution.md` and `constitution/values.md` — so the
  candidate is checked against existing values;
- existing principles for the same domain (`principles/<domain>/*.md`) —
  to avoid duplicates and to reference related principles.

If these files are absent (no repository yet), note that the candidate is
unreferenced and proceed.

# Procedure

1. **Extract the core claim.** Ask: what is the single behavioural claim behind
   this material? Write it in one sentence.
2. **Separate layers.** Explicitly label, for the user:
   ```text
   fact:        …
   inference:   …
   emotion:     …
   value:       …
   prediction:  …
   ```
3. **Ask for the user's interpretation.** Do not accept the source's wording as
   the conclusion. The candidate must be in the user's own terms. If they cannot
   paraphrase it, the idea is not ready to become a principle.
4. **Elicit evidence.** What real experience supports it? Ask for a concrete
   episode, not a general impression.
5. **Elicit counter evidence.** Ask explicitly: "什么情况会推翻这个想法？" and
   "what evidence would change this belief?" If none is offered, say the
   candidate is a slogan until a boundary exists.
6. **Elicit the boundary.** When does this principle NOT apply?
7. **Elicit the trigger.** When should it be invoked?
8. **Build the action rule.** `IF <condition> THEN <action>`.
9. **Write the candidate.** Fill the Output Contract below, `status: candidate`.
   Do not promote it.
10. **Ask before writing.** Do not create the principle file without the user's
    confirmation. Decide together whether it becomes a new file or a revision
    of an existing principle.

# Output Contract

Produce exactly this structure:

```yaml
candidate_principle: <short title>
statement: <one sentence, user's own words>
source: <conversation | book | video | experience | review | ...>
reasoning_summary: <2-3 sentences of the logic>
evidence: <real episode the user names>
counter_evidence: <what would falsify it, or "none found — slogan risk">
boundary: <when it does not apply>
trigger: <when to invoke it>
action_rule: <IF ... THEN ...>

status: candidate
```

The final line `status` must be `candidate`. Never `testing`, `validated` or
`core`.

# Write Permissions

- **Level B (suggest only):** `principles/`, `values/`, `models/`. You may
  propose the full file content, but the user must confirm before it is written.
- You may draft the markdown body with the standard principle template
  (`templates/principle.md`).

# Forbidden Actions

- never write `status: validated` or `core` — only the human promotes;
- never modify the user's wording: paraphrase back and get their approval;
- never skip counter evidence or boundary; a principle without them is a slogan;
- never modify `constitution/` (Level C, read-only);
- never silently overwrite an existing principle — propose a revision with a
  `## Revision History` entry instead;
- never present inference as fact.

# Examples

- `examples/input-01.md` — a conversation excerpt where the user almost left a
  job for emotional reasons.
- `examples/output-01.md` — the principle candidate extracted from it
  (`status: candidate`, with counter evidence and boundary).