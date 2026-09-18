# Roadmap

## v0.1 — Foundation (current)

- [x] Repository structure, LICENSE, AGENTS.md, docs
- [x] Six entity schemas (value / model / principle / decision / experiment / review)
- [x] Markdown templates
- [x] Parser & repository index
- [x] `praxis validate` (schema + IDs + relations + semantic + privacy)
- [x] CLI: `validate`, `new`, `search`, `doctor`
- [x] Four agent skills (principle-extractor, decision-review, values-audit, quarterly-review)
- [x] Demo persona (fictional end-to-end example)
- [x] GitHub Actions: tests + validation
- [ ] v0.1.0 tag & release

**Not in v0.1:** RAG, embeddings, vector DB, web UI, Notion sync, LLM provider
API, multi-agent, graph DB, mobile app, cloud sync, reminders, resume RAG,
finance integration.

> 如果 v0.1 的思想闭环本身不好用，任何 AI 和 RAG 都只是放大一个不好用的系统。

## v0.2 — Local Intelligence

- Full-text + metadata search (already present in v0.1 CLI, harden it)
- Relation graph / navigation
- Review reminders (decision review dates)
- Statistics (repeated mistakes, principle health)
- `pre-commit` integration

## v0.3 — AI Layer

- Provider-agnostic LLM adapter (OpenAI / Anthropic / Gemini / DeepSeek / local)
- Principle extraction from conversation & notes (dialog-driven)
- Decision analysis with lens perspectives
- Value-conflict detection
- Review summarisation

Core stays deterministic; AI is an optional layer over it.

## v0.4 — Personal Retrieval

- Hybrid search (metadata + full-text + embeddings)
- Reranking
- Personal RAG:
  "Should I take this offer?" → retrieves constitution, values, career principles,
  past job decisions, regrets, related experiments → forms an analysis context
  → human decides.

## v0.5 — Integrations

- Notion / Obsidian as *view adapters* (never source of truth)
- Calendar sync
- GitHub publishing
- Career KB / resume RAG (kept separate from personal values data)

## v1.0 — Personal Decision OS

Reliably complete the loop at scale:

```text
Experience → Knowledge → Principle → Decision → Experiment → Feedback → Growth
```

## Trigger conditions for each stage

| Stage | Gate |
| --- | --- |
| v0.3 AI layer | v0.1 released and actually used |
| v0.4 retrieval | Principles > 100, Decisions > 100, Reviews > 100, Notes > 500 |
| v0.5 integrations | real, demonstrated need; adapters stay optional |