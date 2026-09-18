# PraxisOS v0.1 — Technical Design

**Document Type:** Technical Design  
**Status:** Proposed  
**Scope:** v0.1 Foundation  
**Architecture Style:** Local-first / File-based / Schema-driven / Agent-friendly  
**Core Storage:** Markdown + YAML Frontmatter + Git  
**Primary Runtime:** Python  
**License:** MIT

---

# 1. 技术目标

PraxisOS v0.1 需要解决五个工程问题：

1. 如何用稳定的数据结构表达 Values、Principles、Decisions 等实体；
2. 如何让人和 AI 都可以直接阅读、修改这些数据；
3. 如何保证 AI 不会随意破坏用户核心价值观和历史记录；
4. 如何通过 Git 保留长期演化历史；
5. 如何让未来数据库、RAG、Web UI 可以接入，而不用推翻 v0.1。

核心原则：

```text
Human-readable
+
Machine-validatable
+
Git-versioned
+
Agent-operable
+
Migration-friendly
```

---

# 2. 总体架构

```text
┌──────────────────────────────────────┐
│              Human                   │
│      Markdown / Git / Editor         │
└─────────────────┬────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────┐
│          PraxisOS Repository         │
│                                      │
│ Constitution                         │
│ Values                               │
│ Models                               │
│ Principles                           │
│ Decisions                            │
│ Experiments                          │
│ Reviews                              │
└─────────────────┬────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────┐
│           Praxis Core               │
│                                      │
│ Parser                               │
│ Schema Validator                     │
│ Relation Resolver                    │
│ Repository Index                     │
│ Privacy Guard                        │
└───────────┬──────────────────────────┘
            │
      ┌─────┴─────────────┐
      ▼                   ▼
┌──────────────┐   ┌─────────────────┐
│     CLI      │   │  Agent Skills   │
│              │   │                 │
│ validate     │   │ principle       │
│ search       │   │ decision        │
│ new          │   │ values audit    │
│ review       │   │ review          │
└──────────────┘   └─────────────────┘
            │
            ▼
┌──────────────────────────────────────┐
│           Future Adapters           │
│                                     │
│ Notion / Obsidian / RAG / Web UI   │
└──────────────────────────────────────┘
```

---

# 3. 关键架构决策

## ADR-001：Markdown 是 v0.1 的 Source of Truth

不使用：

- PostgreSQL
- SQLite
- Vector DB
- Notion Database

核心数据全部存储为：

```text
Markdown
+
YAML Frontmatter
```

原因：

- 用户直接可读；
- Git 友好；
- LLM 友好；
- diff 清晰；
- 易迁移；
- 无厂商绑定。

---

# 4. ADR-002：Schema 驱动，而不是自由 Markdown

虽然存储格式是 Markdown，但 Frontmatter 必须遵循 JSON Schema。

例如：

```yaml
---
id: PRINCIPLE-CAREER-001
type: principle
title: 职业前途不能用于偿还一般人情
status: testing
confidence: medium
domains:
  - career
sources:
  - EXP-CAREER-001
created_at: 2026-09-17
updated_at: 2026-09-17
---
```

正文用于：

```text
Why
Evidence
Counter Evidence
Boundary
Action Rule
```

即：

> Metadata 用于机器理解。

> Markdown Body 用于人类表达复杂思想。

---

# 5. ADR-003：Python 负责工具层

建议第一版使用：

```text
Python
```

承担：

- 文件扫描；
- Frontmatter 解析；
- JSON Schema Validation；
- Relation 检查；
- 搜索；
- CLI；
- Privacy Scan；
- Test。

暂时不要实现：

```text
Python backend server
```

系统本身仍然是静态文件仓库。

---

# 6. Repository Structure

```text
praxis-os/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── AGENTS.md
├── ARCHITECTURE.md
├── pyproject.toml
│
├── docs/
│   ├── philosophy.md
│   ├── methodology.md
│   ├── privacy.md
│   ├── data-model.md
│   ├── skill-spec.md
│   ├── adr/
│   │   ├── 001-markdown-storage.md
│   │   ├── 002-schema-driven.md
│   │   └── 003-human-final-authority.md
│   └── roadmap.md
│
├── constitution/
│   ├── constitution.md
│   ├── values.md
│   ├── anti-values.md
│   ├── direction.md
│   └── guardrails.md
│
├── values/
│
├── models/
│   ├── thinkers/
│   ├── philosophies/
│   └── mental-models/
│
├── principles/
│   ├── career/
│   ├── life/
│   ├── finance/
│   ├── relationships/
│   └── decision-making/
│
├── decisions/
│   ├── career/
│   ├── finance/
│   ├── life/
│   └── other/
│
├── experiments/
│
├── reviews/
│   ├── weekly/
│   ├── monthly/
│   ├── quarterly/
│   ├── annual/
│   └── decisions/
│
├── schemas/
│   ├── value.schema.json
│   ├── model.schema.json
│   ├── principle.schema.json
│   ├── decision.schema.json
│   ├── experiment.schema.json
│   └── review.schema.json
│
├── templates/
│   ├── value.md
│   ├── thinker.md
│   ├── principle.md
│   ├── decision.md
│   ├── experiment.md
│   ├── weekly-review.md
│   └── quarterly-review.md
│
├── skills/
│   ├── principle-extractor/
│   │   ├── SKILL.md
│   │   └── examples/
│   │
│   ├── decision-review/
│   │   ├── SKILL.md
│   │   └── examples/
│   │
│   ├── values-audit/
│   │   ├── SKILL.md
│   │   └── examples/
│   │
│   └── quarterly-review/
│       ├── SKILL.md
│       └── examples/
│
├── src/
│   └── praxis/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       │
│       ├── core/
│       │   ├── parser.py
│       │   ├── loader.py
│       │   ├── index.py
│       │   ├── relations.py
│       │   └── ids.py
│       │
│       ├── validation/
│       │   ├── schema.py
│       │   ├── semantic.py
│       │   └── privacy.py
│       │
│       └── commands/
│           ├── validate.py
│           ├── search.py
│           ├── new.py
│           └── doctor.py
│
├── tests/
│   ├── unit/
│   ├── fixtures/
│   └── integration/
│
├── examples/
│   └── demo-persona/
│
├── private/
│   └── .gitkeep
│
└── .github/
    └── workflows/
        ├── validate.yml
        └── test.yml
```

---

# 7. Entity Model

v0.1 只允许六种核心实体：

```text
VALUE
MODEL
PRINCIPLE
DECISION
EXPERIMENT
REVIEW
```

未来新增实体不得破坏这六个核心概念。

---

# 8. ID 规范

所有实体使用稳定 ID。

格式：

```text
TYPE-DOMAIN-NNN
```

例如：

```text
VALUE-LIFE-001

MODEL-STOICISM-001

PRINCIPLE-CAREER-001

DECISION-CAREER-003

EXPERIMENT-CAREER-002

REVIEW-DECISION-003
```

ID 一旦创建：

> 不得因为标题修改而改变。

因此 Relation 不依赖文件路径和文件名。

---

# 9. Value Schema

示例：

```yaml
---
id: VALUE-LIFE-001
type: value

name: Autonomy
name_zh: 自主

status: active

priority: high

domains:
  - life
  - career
  - finance

confidence: high

created_at: 2026-09-17
updated_at: 2026-09-17
---
```

正文：

```markdown
# 自主

## Definition

自主意味着能够决定自己的时间、职业和生活方向。

## Why It Matters

...

## Behavioral Evidence

...

## Contradictory Evidence

...

## Conflicts

...

## Revision History
```

---

# 10. Model Schema

Model 可以表达：

```text
Thinker
Philosophy
Mental Model
World Model
```

示例：

```yaml
---
id: MODEL-STOICISM-001
type: model

model_type: philosophy

name: Stoicism

status: studying

confidence: medium

domains:
  - emotion
  - action
  - decision-making

derived_principles:
  - PRINCIPLE-LIFE-003

created_at: 2026-09-17
updated_at: 2026-09-17
---
```

---

# 11. Principle Schema

Principle 是整个 PraxisOS 中最重要的数据结构。

```yaml
---
id: PRINCIPLE-CAREER-001
type: principle

title: 感情影响离开的方式，但不能单独决定职业去留

status: testing

confidence: medium

domains:
  - career
  - relationships

sources:
  - MODEL-STOICISM-001

evidence:
  - EXPERIMENT-CAREER-001

related_values:
  - VALUE-LIFE-001

related_principles: []

created_at: 2026-09-17
updated_at: 2026-09-17
last_tested: null
---
```

正文必须包含：

```markdown
# Principle

## Statement

## Why

## Evidence

## Counter Evidence

## Boundary

## Trigger

## Action Rule

## Revision History
```

---

# 12. Principle 状态机

严格限制状态：

```text
candidate
    ↓
testing
    ↓
validated
    ↓
core
```

任何状态都可以进入：

```text
revised
```

最终：

```text
retired
```

允许流转：

```text
candidate → testing

testing → validated

testing → retired

validated → core

validated → revised

core → revised

revised → testing

revised → retired
```

禁止 Agent 自动执行：

```text
testing → validated

validated → core
```

必须由用户确认。

---

# 13. Decision Schema

```yaml
---
id: DECISION-CAREER-001
type: decision

title: 是否离开当前岗位

status: considering

domain: career

decision_date: null

confidence: 60

related_values:
  - VALUE-LIFE-001

related_principles:
  - PRINCIPLE-CAREER-001

related_models:
  - MODEL-STOICISM-001

experiments: []

review_dates:
  - 2026-10-17
  - 2026-12-17

created_at: 2026-09-17
updated_at: 2026-09-17
---
```

正文：

```markdown
# Situation

# Facts

# Unknowns

# Emotion

# Interests

# Objectives

# Options

# Trade-offs

# Relevant Principles

# Lens Analysis

## Machiavelli

## Legalism

## Stoicism

## Adler

## Taoism

# Decision

# Next Action

# Prediction

# Final Judgment
```

---

# 14. Experiment Schema

```yaml
---
id: EXPERIMENT-CAREER-001
type: experiment

title: 外部市场竞争力测试

status: planned

hypothesis: 当前市场竞争力不足

start_date: null
end_date: null

related_decision:
  - DECISION-CAREER-001

related_principles:
  - PRINCIPLE-CAREER-001

metrics:
  - resume_pass_rate
  - interview_rate
  - second_round_rate
  - offer_rate
---
```

Experiment 强调：

> 小成本、可逆、可测量。

---

# 15. Review Schema

```yaml
---
id: REVIEW-DECISION-001
type: review

review_type: decision

target:
  - DECISION-CAREER-001

status: completed

review_date: 2026-12-17

principles_changed: []

created_at: 2026-12-17
updated_at: 2026-12-17
---
```

必须记录：

```text
Prediction
Actual Outcome
Difference
Decision Quality
Outcome Quality
Lessons
Principle Impact
```

---

# 16. Relation Model

Relation 全部通过 ID。

禁止：

```text
../principles/foo.md
```

推荐：

```yaml
related_principles:
  - PRINCIPLE-CAREER-001
```

解析流程：

```text
Repository Scan
    ↓
Build ID Index
    ↓
Resolve Relations
    ↓
Report Missing IDs
```

内存索引：

```python
{
    "PRINCIPLE-CAREER-001": Entity(...),
    "VALUE-LIFE-001": Entity(...),
    ...
}
```

v0.1 不需要 Graph DB。

---

# 17. Parser

Parser 负责：

```text
Markdown File
    ↓
Frontmatter
    +
Markdown Body
```

内部对象：

```python
Entity(
    id,
    type,
    metadata,
    body,
    path
)
```

Parser 不负责业务逻辑。

---

# 18. Validation Architecture

分成三层。

## Level 1 — Syntax Validation

检查：

- YAML 能否解析；
- JSON Schema 合法；
- required fields；
- enum；
- 日期格式。

---

## Level 2 — Repository Validation

检查：

- ID 是否重复；
- Relation 是否存在；
- 文件类型和目录是否匹配；
- ID prefix 是否正确；
- review target 是否存在。

---

## Level 3 — Semantic Validation

例如：

Principle：

```text
Boundary 是否存在？
Counter Evidence 是否为空？
```

Decision：

```text
Final Judgment 是否存在？
Next Action 是否存在？
```

Experiment：

```text
Hypothesis 是否存在？
Metric 是否存在？
```

这里是 PraxisOS 区别于普通 Schema Validator 的地方。

---

# 19. CLI Design

统一入口：

```bash
praxis
```

第一阶段实现：

```bash
praxis validate
praxis search
praxis new
praxis doctor
```

---

# 20. praxis validate

执行完整仓库检查：

```bash
praxis validate
```

输出：

```text
Scanning 42 entities...

Schema
✓ 42 passed

IDs
✓ no duplicates

Relations
✓ 73 valid
✗ 1 missing relation

Semantic
⚠ PRINCIPLE-CAREER-004:
  Counter Evidence section is empty

Privacy
✓ no obvious secrets detected

RESULT: FAILED
```

返回非零 exit code。

用于 CI。

---

# 21. praxis new

例如：

```bash
praxis new principle
```

交互式生成：

```text
Title:
Domain:
Source:
```

然后：

```text
Generate ID
↓
Copy Template
↓
Fill Frontmatter
↓
Create File
```

---

# 22. praxis search

v0.1 只做 metadata + text search。

例如：

```bash
praxis search "离职"

praxis search --type principle career

praxis search --status testing

praxis search --value VALUE-LIFE-001
```

不做 embedding。

---

# 23. praxis doctor

用于检查仓库健康度：

```text
Orphan Principles

Decisions Without Reviews

Validated Principles Never Retested

Stale Constitution

Unused Values

Broken Relations

Private Files Accidentally Tracked
```

这是一个非常重要的长期维护工具。

---

# 24. Skill Contract

Skill 不直接等于代码。

Skill 是：

```text
Instruction Contract
```

目录：

```text
skills/<skill-name>/SKILL.md
```

统一格式：

```markdown
# Name

# Purpose

# Inputs

# Required Context

# Procedure

# Output Contract

# Write Permissions

# Forbidden Actions

# Examples
```

---

# 25. principle-extractor Skill

## Input

可以接受：

```text
Conversation
Book Note
Experience
Failure
Success
Observation
```

## Output

必须输出：

```yaml
candidate_principle:

statement:

source:

reasoning_summary:

evidence:

counter_evidence:

boundary:

trigger:

action_rule:
```

注意：

不能直接保存为：

```text
validated
```

最多：

```text
candidate
```

---

# 26. decision-review Skill

Input：

```text
Decision Context
```

处理：

```text
Facts
↓
Unknowns
↓
Emotion
↓
Interests
↓
Objectives
↓
Options
↓
Relevant Principles
↓
Five Lenses
↓
Trade-offs
↓
Small Experiment
```

输出必须明确：

```text
Human Decision Required
```

Agent 不能把自己的建议写入：

```text
Final Judgment
```

除非用户明确确认。

---

# 27. values-audit Skill

核心不是问用户：

> “你最重视什么？”

而是比较：

```text
Claimed Values
vs
Observed Decisions
```

例如：

```text
Claimed:
Autonomy

Observed:
3 major decisions favored familiarity/security

Possible tension:
Autonomy ↔ Security
```

输出必须使用：

```text
Possible conflict
```

不得直接宣称：

> 你其实不重视自由。

---

# 28. quarterly-review Skill

输入：

过去季度：

```text
Decisions
Experiments
Reviews
Principles
```

输出：

```text
Repeated Patterns

Validated Assumptions

Failed Assumptions

New Principle Candidates

Value Conflicts

Direction Drift

Next Quarter Experiments
```

---

# 29. Agent Permission Model

这是 PraxisOS 非常重要的一层。

文件分为：

## Level A — Read/Write

Agent 可直接修改：

```text
reviews/
experiments/
drafts/
```

---

## Level B — Suggest Only

```text
principles/
values/
models/
```

Agent 可以：

```text
Propose Patch
```

但需要用户确认。

---

## Level C — Human Controlled

```text
constitution/
guardrails.md
```

Agent 默认：

```text
READ ONLY
```

任何修改必须显式请求用户批准。

---

# 30. AGENTS.md 核心规范

```text
# Authority

The human user is the final authority.

# Constitution

Never modify files under /constitution
without explicit user approval.

# Principles

Never promote a principle to validated or core.

# History

Never silently overwrite historical reasoning.

# Facts

Always distinguish:
facts
inferences
emotions
values
predictions

# Counter Evidence

Whenever creating a principle,
seek disconfirming evidence.

# Decisions

Do not write AI recommendations
as Final Judgment.

# Uncertainty

When uncertainty is high,
prefer reversible experiments.

# Privacy

Never read or expose ignored private data
unless explicitly provided by the user.

# Minimalism

Do not add infrastructure
without demonstrated need.
```

---

# 31. Privacy Architecture

必须使用多层防护。

第一层：

```text
.gitignore
```

```gitignore
/private/**
/data/private/**
/journals/private/**
.env
*.secret.*
credentials.*
```

第二层：

```text
praxis validate
```

检测：

- API Key Pattern
- Private Key
- Email
- Phone
- Access Token
- Credential file

只做启发式检测。

---

# 32. Git Pre-commit

未来可增加：

```text
pre-commit
```

执行：

```text
schema validation
privacy scan
format validation
```

目的：

> 在 `git commit` 之前阻止隐私泄露。

---

# 33. GitHub Actions

PR / Push 自动执行：

```text
Install
↓
Unit Tests
↓
praxis validate
↓
Privacy Check
↓
Repository Integrity Check
```

CI 不读取：

```text
private/
```

---

# 34. Demo Persona

开源项目不能使用开发者本人真实人生数据。

建立：

```text
examples/demo-persona/
```

例如虚构人物：

```text
Alex
32
software engineer
considering management vs IC path
```

Example 数据至少包含：

```text
3 Values
5 Principles
2 Decisions
1 Experiment
2 Reviews
```

这样别人 clone 后立即能理解系统。

---

# 35. Configuration

根目录增加：

```text
praxis.yaml
```

例如：

```yaml
version: 1

paths:
  values: values
  principles: principles
  decisions: decisions
  experiments: experiments
  reviews: reviews

privacy:
  ignored:
    - private/**
    - journals/private/**

validation:
  require_counter_evidence: true
  require_principle_boundary: true
  require_decision_next_action: true
```

避免未来把路径写死在代码里。

---

# 36. Core Python Domain Objects

第一版无需 ORM。

只需要：

```python
Entity
Repository
ValidationResult
Relation
Issue
```

概念结构：

```text
Repository
│
├── entities_by_id
├── entities_by_type
└── relations
```

---

# 37. Error Severity

Validation Issue 分为：

```text
INFO
WARNING
ERROR
FATAL
```

例如：

### FATAL

```text
Duplicate ID
Invalid YAML
```

### ERROR

```text
Broken Relation
Invalid Status
```

### WARNING

```text
Missing Counter Evidence
Decision overdue for review
```

### INFO

```text
Principle not tested for 365 days
```

---

# 38. Testing Strategy

## Unit Tests

测试：

```text
Parser
ID Generator
Schema Validation
Relation Resolver
Privacy Scanner
```

---

## Integration Tests

测试完整仓库：

```text
Fixture Repository
↓
Load
↓
Validate
↓
Check Result
```

---

## Golden Tests

对于 Skills，使用固定案例。

例如：

```text
input:
"I wanted to leave but stayed because my manager was kind."

expected output:
Principle Candidate
+
Boundary
+
Counter Evidence
```

不要求文本完全一致。

只验证：

```text
required sections exist
```

未来引入 LLM Evaluation 再做语义测试。

---

# 39. No LLM Dependency in Core

非常重要：

```text
praxis validate
praxis search
praxis doctor
```

都必须：

> **在没有 AI API 的情况下运行。**

AI 属于：

```text
Optional Intelligence Layer
```

不是基础设施依赖。

---

# 40. Future AI Architecture

以后可以加：

```text
Agent
  ↓
Context Builder
  ↓
Retriever
  ↓
Relevant Values
Relevant Principles
Relevant Decisions
Relevant Reviews
  ↓
LLM
  ↓
Structured Proposal
  ↓
Human Approval
  ↓
Write
```

注意：

最后仍然是：

```text
Human Approval
```

---

# 41. RAG 预留设计

虽然 v0.1 没有 RAG，但数据结构必须方便以后 Chunk。

未来一个 Principle 可以天然转换：

```json
{
  "id": "PRINCIPLE-CAREER-001",
  "type": "principle",
  "domain": "career",
  "status": "validated",
  "text": "...",
  "related_values": ["VALUE-LIFE-001"]
}
```

Embedding metadata 可以直接使用现有 Frontmatter。

因此 v0.1 不需要专门为 RAG 设计第二套数据结构。

---

# 42. Future Event Model

未来如果需要分析长期变化，可以从 Git History + Review 推导。

暂时不要增加 Event Sourcing。

未来可考虑：

```text
PrincipleCreated
PrincipleRevised
DecisionMade
ExperimentCompleted
ReviewCompleted
```

v0.1 不实现。

---

# 43. Notion Adapter 设计原则

未来 Notion 只能是：

```text
View / Editing Adapter
```

不能成为系统唯一真源。

推荐：

```text
Markdown
    ↓
Exporter
    ↓
Notion
```

如果未来支持双向同步，需要单独设计：

```text
Conflict Resolution
```

v0.1 不实现。

---

# 44. 安全边界

PraxisOS 不应自动：

- 替用户辞职；
- 自动进行金融交易；
- 自动发送私人消息；
- 修改 Personal Constitution；
- 删除历史 Principle；
- 把 Personal Data 上传第三方；
- 根据价值观自动替用户作最终决定。

---

# 45. v0.1 Package Boundary

推荐：

```text
praxis.core

praxis.validation

praxis.commands
```

不要出现：

```text
services/
repositories/
controllers/
usecases/
domain/
infrastructure/
```

六七层 Clean Architecture。

当前规模不需要。

原则：

> Architecture should follow complexity,
> not precede it.

---

# 46. 第一阶段开发顺序

## Phase A — Repository Skeleton

完成：

```text
README
LICENSE
AGENTS.md
directories
templates
```

---

## Phase B — Data Schema

完成：

```text
6 JSON Schemas
```

然后创建：

```text
demo-persona
```

验证 Schema 是否真实可用。

---

## Phase C — Core Parser

完成：

```text
Markdown loader
Frontmatter parser
Entity abstraction
Repository index
```

---

## Phase D — Validator

实现：

```text
schema
ID
relations
semantic
privacy
```

交付：

```bash
praxis validate
```

这是 v0.1 最重要的可执行能力。

---

## Phase E — CLI

增加：

```text
new
search
doctor
```

---

## Phase F — Skills

实现：

```text
principle-extractor
decision-review
values-audit
quarterly-review
```

---

## Phase G — GitHub CI

完成：

```text
test
validate
privacy
```

---

# 47. MVP Acceptance Criteria

### AC-01

Clone 项目后：

```bash
praxis validate
```

成功运行。

---

### AC-02

非法 Principle：

```text
invalid status
```

能够被检测。

---

### AC-03

引用不存在的 Principle ID：

```text
DECISION → PRINCIPLE-404
```

能够被检测。

---

### AC-04

重复 ID 能阻止 CI。

---

### AC-05

Decision 没有：

```text
Next Action
```

产生 Warning 或 Error。

---

### AC-06

Principle 没有：

```text
Counter Evidence
Boundary
```

能够被检测。

---

### AC-07

Agent 不得自动修改：

```text
constitution/
```

---

### AC-08

Demo Persona 能完整演示：

```text
Value
→ Principle
→ Decision
→ Experiment
→ Review
```

---

# 48. v0.1 最终系统形态

```text
                 PraxisOS
                    │
             Personal Constitution
                    │
       ┌────────────┼────────────┐
       │            │            │
     Values       Models     Principles
                                  │
                                  ▼
                              Decisions
                                  │
                                  ▼
                             Experiments
                                  │
                                  ▼
                               Reviews
                                  │
                                  └──────→ Principles

                    ▲
                    │
              Praxis Core
                    │
        ┌───────────┼────────────┐
        │           │            │
      Parser     Validator      Search
                    │
                    ▼
                Agent Skills
```

---

# 49. 技术哲学

PraxisOS 的技术架构本身也应该符合 PraxisOS 的思想：

> **不要为了未来可能出现的问题提前制造今天的复杂性。**

所以 v0.1：

不需要数据库。

不需要 Kubernetes。

不需要微服务。

不需要消息队列。

不需要 Vector DB。

不需要复杂 Agent Framework。

只需要：

```text
Files
Schemas
Validation
Git
Skills
```

如果这五样东西不能产生价值，

增加 RAG 也不会产生价值。

---

# 50. Definition of Done

PraxisOS v0.1 技术基础完成的定义：

```text
Repository
✓

Data Model
✓

Schemas
✓

Templates
✓

Parser
✓

Validator
✓

Relations
✓

Privacy Guard
✓

CLI
✓

4 Skills
✓

Demo Persona
✓

Tests
✓

GitHub Actions
✓
```

此时项目已经是：

> **一个真正可以使用和开源的 Personal Philosophy & Decision OS。**

之后才进入：

```text
v0.2 Local Intelligence
```

包括：

```text
更强搜索
统计
Decision Review Scheduler
Principle Health
Relation Graph
```

之后再考虑：

```text
v0.3 AI Layer
v0.4 Personal RAG
```