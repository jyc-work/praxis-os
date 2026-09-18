# Architecture

> **Scope:** PraxisOS v0.1 — local-first, file-based, schema-driven, agent-friendly.

## Principles

```text
Human-readable
+ Machine-validatable
+ Git-versioned
+ Agent-operable
+ Migration-friendly
```

Priority order for v0.1:

```text
Portability > Transparency > Simplicity > AI Compatibility > Automation > UI
```

## System overview

```text
┌──────────────────────────────────────┐
│              Human                   │
│      Markdown / Git / Editor         │
└─────────────────┬────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────┐
│          PraxisOS Repository         │
│  constitution/ values/ models/       │
│  principles/ decisions/ experiments/ │
│  reviews/                            │
└─────────────────┬────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────┐
│           Praxis Core                │
│  Parser → Index → Validator          │
│  (schema / repository / semantic /   │
│   privacy)                           │
└───────────┬──────────────────────────┘
            │
      ┌─────┴─────────────┐
      ▼                   ▼
┌──────────────┐   ┌─────────────────┐
│     CLI      │   │   Agent Skills  │
│  validate    │   │   principle     │
│  search      │   │   decision      │
│  new         │   │   values audit  │
│  doctor      │   │   review        │
└──────────────┘   └─────────────────┘
            │
            ▼
┌──────────────────────────────────────┐
│        Future Adapters              │
│  Notion / Obsidian / RAG / Web UI   │
└──────────────────────────────────────┘
```

## Key decisions (see `docs/adr/`)

| ADR | Decision |
| --- | --- |
| 001 | Markdown + YAML frontmatter is the source of truth. No DB in v0.1. |
| 002 | Schemas drive data. Frontmatter = machine; body = human. |
| 003 | The human holds final authority over judgments and status promotions. |

## Directory-to-entity mapping

The loader scans only the configured paths in `praxis.yaml`; every other
directory (`.git`, `tests/`, `examples/`, `private/`) is excluded.

```yaml
paths:
  values:      values        # VALUE-*
  models:      models        # MODEL-*
  principles:  principles    # PRINCIPLE-*
  decisions:   decisions     # DECISION-*
  experiments: experiments   # EXPERIMENT-*
  reviews:     reviews       # REVIEW-*
```

## Entity model

```python
@dataclass
class Entity:
    id: str
    type: str          # value | model | principle | decision | experiment | review
    metadata: dict     # parsed YAML frontmatter
    body: str          # markdown body after the frontmatter
    path: Path         # source file path
```

IDs are stable: `TYPE-DOMAIN-NNN` (e.g. `PRINCIPLE-CAREER-001`). IDs never
change because a title changed; relations reference IDs, never file paths.

## Core pipeline

```text
Repository scan
   → parse frontmatter + body        (parser.py)
   → build entities_by_id / by_type  (index.py)
   → resolve relations by ID         (relations.py)
   → validate:
       Level 1: schema               (JSON Schema per type)
       Level 2: repository           (IDs, relations, placement, prefixes)
       Level 3: semantic             (boundary, counter evidence, next action…)
       Privacy scan                  (heuristic secrets detection)
   → report issues (INFO/WARNING/ERROR/FATAL), exit code 0/1
```

## Determinism rule

```text
parse, validate, search, relations, doctor  →  fully deterministic
```

No LLM call, no network, no randomness in the core. AI lives only in `skills/`
as instruction contracts; it is an optional intelligence layer, not a dependency.

## Privacy architecture

Three layers:

1. `.gitignore` — `/private/**`, `/data/private/**`, `/journals/private/**`, `.env`, `*.secret.*`
2. `praxis validate` — heuristic privacy scan (API keys, private key blocks, tokens,
   password-like assignments, emails, phones, credential filenames)
3. CI (`validate.yml`) — fails the build on `ERROR`-severity findings

## Testing strategy

- **Unit** — parser, ID generator, schema validation, relation resolver, privacy scanner, CLI commands
- **Integration** — load a fixture repository → validate → assert result
- **Golden** — fixture repositories (`tests/fixtures/valid_repo`, `invalid_repo`) with expected outcomes

## Non-goals for v0.1

Database, vector store, web services, SaaS, mobile app, Notion sync, microservices,
GraphDB, event sourcing, complex multi-agent orchestration. See
[docs/roadmap.md](docs/roadmap.md) for when these arrive.