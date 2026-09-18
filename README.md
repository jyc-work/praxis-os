# PraxisOS

> **An open-source personal philosophy & decision operating system that turns values, ideas and lived experience into principles, decisions, experiments and feedback.**

> **PraxisOS 是一个开源个人思想与决策操作系统，将价值观、思想和真实经历转化为原则、决策、行动实验与现实反馈。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](pyproject.toml)

---

## What is PraxisOS?

Most personal systems (Second Brain, LifeOS, productivity stacks) answer one question:

> "What do I need to manage?"

PraxisOS answers a different, higher one:

> **"Why do I choose this — and is my reasoning any good?"**

It is a **local-first, file-based repository** (Markdown + YAML frontmatter + Git) plus a small deterministic toolchain that helps you:

1. discover what you actually value;
2. build explicit models of how the world works;
3. turn outside ideas and lived experience into **personal principles**;
4. use those principles to make structured decisions;
5. convert decisions into small, reversible experiments;
6. record outcomes and compare them against predictions;
7. revise or retire principles that reality disconfirms.

The closed loop:

```text
Reality → Observation → Reflection → World Model → Principle
   → Decision → Action / Experiment → Outcome → Review → Update Principle ──┐
        ↑                                                                    │
        └────────────────────────────────────────────────────────────────────┘
```

## Why it exists

Common failure modes this project targets:

| Failure | What PraxisOS does about it |
| --- | --- |
| Reading a lot, changing nothing | Every input must pass through *My Interpretation* → *Derived Principles* |
| Knowing better, deciding emotionally | Decisions record facts, unknowns, emotion, interests, options, lenses |
| Repeating the same mistake months later | Prediction vs. Actual reviews, with explicit prediction error |
| Goals drifting with mood | A Personal Constitution with a *Definition of Enough* |
| AI advice that ignores your value system | Principles and values live in files the AI must read first |
| Rationalising the past after the fact | Frozen predictions and Git history make hindsight auditable |

## Core concepts

| Entity | Directory | Question it answers |
| --- | --- | --- |
| **Constitution** | `constitution/` | Who do I want to become? |
| **Value** | `values/` | What do I actually care about? |
| **Model** | `models/` | How do I understand the world? |
| **Principle** | `principles/` | What action rule have I earned the right to trust? |
| **Decision** | `decisions/` | Why did I choose this, given what I knew then? |
| **Experiment** | `experiments/` | What cheap test would resolve this uncertainty? |
| **Review** | `reviews/` | Was my judgment any good, independent of the outcome? |

Principles move through a strict state machine:

```text
candidate → testing → validated → core
                ↘         ↘        ↘
                 revised ←─────────┘ → retired
```

Agents may **never** promote a principle to `validated` or `core`. Only the human can.

## Quick Start

```bash
git clone https://github.com/nomiga-ww/praxis-os.git
cd praxis-os

python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -e ".[dev]"

praxis --help
praxis validate
praxis doctor
praxis new principle
```

Target: **clone → first principle in under 10 minutes.**

All of `praxis validate`, `praxis search`, `praxis doctor` and `praxis new` run **without any AI API key**. PraxisOS has no LLM dependency in its core.

## Repository structure

```text
praxis-os/
├── constitution/       # personal constitution, values narrative, guardrails
├── values/             # VALUE-* entities (claimed vs. revealed)
├── models/             # thinkers, philosophies, mental models, world models
├── principles/         # PRINCIPLE-* — the core database
├── decisions/          # DECISION-* — the decision journal
├── experiments/        # EXPERIMENT-* — small reversible tests
├── reviews/            # weekly / monthly / quarterly / annual / decision reviews
├── schemas/            # JSON Schema contracts for all six entities
├── templates/          # Markdown templates used by `praxis new`
├── skills/             # AI-native instruction contracts (4 skills)
├── examples/demo-persona/   # fully fictional end-to-end example
├── docs/               # philosophy, methodology, privacy, data model, ADRs
├── src/praxis/         # deterministic Python core (parser, validator, CLI)
├── tests/              # unit + integration + fixtures
└── private/            # gitignored — never committed
```

## Example workflow

```text
1. Write constitution/constitution.md            (who am I becoming?)
2. Add values/VALUE-LIFE-001-autonomy.md          (what do I value?)
3. Add models/philosophies/MODEL-STOICISM-001.md  (how do I read the world?)
4. praxis new principle --domain career           (earn a principle)
5. praxis new decision  --domain career           (decide deliberately)
6. praxis new experiment                          (test the uncertainty)
7. praxis new review --type decision              (compare prediction vs. actual)
8. praxis validate                                (machine-check the whole repo)
```

See `examples/demo-persona/` for a fictional persona (Alex, 32, software engineer) that demonstrates the full loop — including one principle that gets **revised** by disconfirming evidence.

## Privacy warning

```text
Framework  →  PUBLIC
Your data  →  PRIVATE
```

`/private/**`, `/data/private/**` and `/journals/private/**` are gitignored by default, and `praxis validate` runs a heuristic privacy scan (API keys, private keys, tokens, credentials, emails, phone numbers) that fails CI on obvious secrets.

**Never commit:** real journals, real positions, identity documents, employer-confidential material, colleague names, private relationships.

Sample data in `examples/` must be entirely fictional and de-identified.

See [docs/privacy.md](docs/privacy.md).

## Agent safety

PraxisOS is designed to be operated by AI agents **without letting them play life coach**. The rules live in [AGENTS.md](AGENTS.md), enforced by three permission levels:

| Level | Paths | Agent permission |
| --- | --- | --- |
| A | `reviews/`, `experiments/` | read/write |
| B | `principles/`, `values/`, `models/` | suggest a patch, human confirms |
| C | `constitution/`, `guardrails.md` | read-only without explicit approval |

Hard constraints: the human owns `Final Judgment`; the agent never upgrades a principle's status; history is never silently overwritten; non-obvious claims must separate fact, inference, emotion, value and prediction.

## Documentation

| Document | Contents |
| --- | --- |
| [ARCHITECTURE.md](ARCHITECTURE.md) | repository layout, core pipeline, design decisions |
| [docs/philosophy.md](docs/philosophy.md) | the thinking behind PraxisOS |
| [docs/methodology.md](docs/methodology.md) | day-to-day practice: reviews and loops |
| [docs/data-model.md](docs/data-model.md) | entity schemas, IDs, relations |
| [docs/skill-spec.md](docs/skill-spec.md) | the SKILL.md contract format |
| [docs/privacy.md](docs/privacy.md) | privacy and data-handling model |
| [docs/roadmap.md](docs/roadmap.md) | v0.1 → v1.0 |
| [docs/adr/](docs/adr/) | architecture decision records |

## Roadmap

- **v0.1 (current)** — Foundation: schemas, templates, parser, validator, CLI, 4 skills, demo persona, CI.
- **v0.2** — Local intelligence: full-text + metadata search, relation graph, review reminders, stats.
- **v0.3** — AI layer: provider-agnostic LLM adapter, extraction and analysis helpers.
- **v0.4** — Personal retrieval: hybrid search, embeddings, reranking.
- **v0.5** — Integrations: Notion/Obsidian views, calendar, career KB.
- **v1.0** — A dependable personal decision OS.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). One problem per PR. Never include real personal data.

## License

[MIT](LICENSE).

---

*Thought is not for worship, but for testing.*
