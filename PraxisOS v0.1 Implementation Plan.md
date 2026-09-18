# PraxisOS v0.1 — Implementation Plan

**Document Type:** Implementation Plan  
**Target Version:** v0.1  
**Execution Model:** Phase-by-Phase  
**Primary Runtime:** Python 3.12+  
**Core Storage:** Markdown + YAML Frontmatter + JSON Schema  
**Primary Goal:** Deliver a usable, validated, local-first Personal Philosophy & Decision OS

---

# 0. Implementation Strategy

整个 v0.1 拆成 7 个 Phase：

```text
Phase 1  Repository Foundation
Phase 2  Data Model & Schemas
Phase 3  Parser & Repository Index
Phase 4  Validation & Privacy Guard
Phase 5  CLI & Authoring Workflow
Phase 6  Skills & Demo Persona
Phase 7  CI, Hardening & Release
```

依赖关系：

```text
Phase 1
   ↓
Phase 2
   ↓
Phase 3
   ↓
Phase 4
   ↓
Phase 5
   ↓
Phase 6
   ↓
Phase 7
```

原则：

> 前一个 Phase 没有通过验收，不进入下一个 Phase。

---

# Phase 1 — Repository Foundation

## 1.1 Goal

建立可运行、可安装、可测试的仓库骨架。

此阶段不实现业务逻辑。

---

## 1.2 Files to Create

```text
README.md
LICENSE
CONTRIBUTING.md
SECURITY.md
AGENTS.md
ARCHITECTURE.md
pyproject.toml
praxis.yaml
.gitignore

docs/
    philosophy.md
    methodology.md
    privacy.md
    data-model.md
    skill-spec.md
    roadmap.md

src/praxis/
    __init__.py
    cli.py
    config.py

tests/
    __init__.py

.github/
    workflows/

private/
    .gitkeep
```

同时创建目录：

```text
constitution/
values/
models/
principles/
decisions/
experiments/
reviews/
schemas/
templates/
skills/
examples/
```

---

## 1.3 pyproject.toml

至少定义：

```text
project metadata
Python >= 3.12
CLI entry point
pytest
PyYAML
python-frontmatter
jsonschema
```

CLI：

```text
praxis = praxis.cli:main
```

---

## 1.4 praxis.yaml

第一版：

```yaml
version: 1

paths:
  constitution: constitution
  values: values
  models: models
  principles: principles
  decisions: decisions
  experiments: experiments
  reviews: reviews

privacy:
  ignored:
    - private/**
    - data/private/**
    - journals/private/**

validation:
  require_counter_evidence: true
  require_principle_boundary: true
  require_decision_next_action: true
```

---

## 1.5 AGENTS.md

必须先定义最小安全规则：

```text
Human is final authority.

Do not modify constitution without explicit approval.

Do not promote principles to validated/core.

Do not overwrite history.

Do not expose private files.

Prefer reversible experiments under uncertainty.
```

---

## 1.6 Acceptance Criteria

- `pip install -e .` 成功；
- `praxis --help` 可以执行；
- pytest 能启动；
- README 能解释项目目的；
- `.gitignore` 正确忽略 `/private/**`；
- 所有核心目录存在；
- `praxis.yaml` 可被读取。

---

## 1.7 Test Cases

### TC-1.1 Package Import

```python
import praxis
```

Expected:

```text
PASS
```

---

### TC-1.2 CLI Entry

```bash
praxis --help
```

Expected：

```text
exit code = 0
```

---

### TC-1.3 Config Load

读取：

```text
praxis.yaml
```

Expected：

```text
version == 1
```

---

### TC-1.4 Private Ignore

创建：

```text
private/test.md
```

执行：

```bash
git status
```

Expected：

```text
private/test.md not tracked
```

---

## 1.8 Exit Condition

仓库已经具备：

```text
installable
testable
configurable
```

但尚未处理任何 PraxisOS 实体。

---

# Phase 2 — Data Model & Schemas

## 2.1 Goal

定义 PraxisOS 的六种核心实体，并通过 JSON Schema 固化。

---

## 2.2 Files to Create

```text
schemas/
    value.schema.json
    model.schema.json
    principle.schema.json
    decision.schema.json
    experiment.schema.json
    review.schema.json

templates/
    value.md
    thinker.md
    principle.md
    decision.md
    experiment.md
    weekly-review.md
    quarterly-review.md

docs/data-model.md
```

---

# 2.3 Value Schema

Required：

```text
id
type
name
status
priority
domains
confidence
created_at
updated_at
```

Constraints：

```text
type == value

status ∈
active
inactive
retired
```

---

# 2.4 Model Schema

Required：

```text
id
type
model_type
name
status
domains
created_at
updated_at
```

`model_type`：

```text
thinker
philosophy
mental-model
world-model
```

---

# 2.5 Principle Schema

Required：

```text
id
type
title
status
confidence
domains
created_at
updated_at
```

status：

```text
candidate
testing
validated
core
revised
retired
```

---

# 2.6 Decision Schema

Required：

```text
id
type
title
status
domain
confidence
created_at
updated_at
```

status：

```text
considering
decided
executing
reviewed
abandoned
```

---

# 2.7 Experiment Schema

Required：

```text
id
type
title
status
hypothesis
created_at
updated_at
```

status：

```text
planned
running
completed
abandoned
```

---

# 2.8 Review Schema

Required：

```text
id
type
review_type
status
review_date
created_at
updated_at
```

---

# 2.9 Template Requirements

每个 Template 必须同时满足：

```text
valid YAML frontmatter
+
required markdown sections
```

Principle：

```text
Statement
Why
Evidence
Counter Evidence
Boundary
Trigger
Action Rule
Revision History
```

Decision：

```text
Situation
Facts
Unknowns
Emotion
Interests
Objectives
Options
Trade-offs
Relevant Principles
Lens Analysis
Decision
Next Action
Prediction
Final Judgment
```

---

# 2.10 Acceptance Criteria

- 六个 Schema 均为合法 JSON Schema；
- 六类合法样例均可通过 Schema；
- 非法 enum 能被拒绝；
- 缺少 required field 时验证失败；
- Template 本身与 Schema 兼容；
- 文档描述与 Schema 一致。

---

# 2.11 Test Cases

### TC-2.1 Valid Principle

合法 Principle。

Expected：

```text
PASS
```

---

### TC-2.2 Invalid Principle Status

```yaml
status: approved
```

Expected：

```text
FAIL
```

---

### TC-2.3 Missing ID

删除：

```yaml
id:
```

Expected：

```text
FAIL
```

---

### TC-2.4 Invalid Model Type

```yaml
model_type: ideology-engine
```

Expected：

```text
FAIL
```

---

### TC-2.5 Valid Decision

完整 Decision Template。

Expected：

```text
PASS
```

---

## 2.12 Exit Condition

PraxisOS 已有稳定：

```text
Data Contract
```

后续代码必须遵循 Schema，不允许绕过。

---

# Phase 3 — Parser & Repository Index

## 3.1 Goal

实现：

```text
Markdown
→ Entity
→ Repository Index
```

这是整个 Core 的基础。

---

# 3.2 Files to Create

```text
src/praxis/core/
    __init__.py
    entity.py
    parser.py
    loader.py
    index.py
    ids.py
    relations.py

tests/unit/
    test_parser.py
    test_loader.py
    test_index.py
    test_ids.py

tests/fixtures/
    valid_repo/
    invalid_repo/
```

---

# 3.3 Entity Object

建议：

```python
@dataclass
class Entity:
    id: str
    type: str
    metadata: dict
    body: str
    path: Path
```

不得在 Entity 内塞入业务逻辑。

---

# 3.4 Parser

输入：

```text
Markdown file
```

输出：

```text
Entity
```

职责：

```text
read file
parse YAML
extract body
normalize metadata
```

不负责：

```text
schema validation
semantic validation
relation validation
```

---

# 3.5 Loader

扫描配置目录：

```text
values/
models/
principles/
decisions/
experiments/
reviews/
```

排除：

```text
private/
.git/
tests/
examples/
```

---

# 3.6 ID Utility

负责：

```text
validate prefix
generate next numeric ID
parse entity type
```

例如：

```text
PRINCIPLE-CAREER-001
```

---

# 3.7 Repository Index

内存结构：

```python
entities_by_id: dict[str, Entity]

entities_by_type: dict[str, list[Entity]]
```

附加：

```text
duplicates
paths
relations
```

---

# 3.8 Acceptance Criteria

- 能解析合法 Markdown；
- 无 Frontmatter 文件产生明确错误；
- Repository Scan 能找到所有实体；
- 重复 ID 能被 Index 标记；
- 可通过 ID 查找 Entity；
- 可通过 type 获取实体集合；
- 私有目录不会被加载。

---

# 3.9 Test Cases

### TC-3.1 Parse Valid Markdown

Expected：

```text
Entity.id correctly parsed
Entity.body preserved
```

---

### TC-3.2 Invalid YAML

Expected：

```text
controlled parse error
```

不能直接 stack trace 崩溃。

---

### TC-3.3 Duplicate ID

两个文件：

```text
PRINCIPLE-CAREER-001
```

Expected：

```text
duplicate detected
```

---

### TC-3.4 Private Folder Exclusion

```text
private/secret.md
```

Expected：

```text
not indexed
```

---

### TC-3.5 Type Index

Expected：

```python
repo.by_type("principle")
```

返回全部 Principle。

---

## 3.10 Exit Condition

系统已经具备稳定：

```text
Repository Read Model
```

---

# Phase 4 — Validation & Privacy Guard

## 4.1 Goal

实现完整：

```text
praxis validate
```

这是 v0.1 最关键的工程能力。

---

# 4.2 Files to Create

```text
src/praxis/validation/
    __init__.py
    issue.py
    schema.py
    repository.py
    semantic.py
    privacy.py

src/praxis/commands/
    validate.py

tests/unit/
    test_schema_validation.py
    test_repository_validation.py
    test_semantic_validation.py
    test_privacy.py

tests/integration/
    test_validate_command.py
```

---

# 4.3 Validation Issue Model

```python
@dataclass
class ValidationIssue:
    severity: Severity
    code: str
    message: str
    path: Path | None
    entity_id: str | None
```

Severity：

```text
INFO
WARNING
ERROR
FATAL
```

---

# 4.4 Schema Validation

每种 entity.type 映射：

```text
value
→ value.schema.json
```

以此类推。

---

# 4.5 Repository Validation

检查：

```text
duplicate ID
broken relation
wrong ID prefix
unknown entity type
wrong directory
missing review target
```

---

# 4.6 Semantic Validation

Principle：

```text
Statement exists
Counter Evidence exists
Boundary exists
Action Rule exists
```

Decision：

```text
Facts exists
Unknowns exists
Next Action exists
Final Judgment section exists
```

Experiment：

```text
Hypothesis exists
Metric exists
```

Review：

```text
Actual Outcome exists
Lessons exists
```

---

# 4.7 Privacy Guard

第一版只做启发式检测。

检测：

```text
API keys
private keys
tokens
password-like assignments
email addresses
phone numbers
credential filenames
```

不做：

```text
full PII classification
OCR
ML-based detection
```

---

# 4.8 Validation Result

命令：

```bash
praxis validate
```

输出示例：

```text
Schema        PASS
IDs           PASS
Relations     FAIL
Semantic      WARN
Privacy       PASS

Errors: 1
Warnings: 2
```

Exit code：

```text
0 = no ERROR/FATAL
1 = validation failure
```

---

# 4.9 Acceptance Criteria

- Broken Relation 可检测；
- Duplicate ID 导致失败；
- Invalid Schema 导致失败；
- Missing Principle Boundary 至少 Warning；
- Private key pattern 导致 Error；
- `praxis validate` 有稳定 exit code；
- 输出具备 entity id 和 file path。

---

# 4.10 Test Cases

### TC-4.1 Broken Relation

```yaml
related_principles:
  - PRINCIPLE-404
```

Expected：

```text
ERROR BROKEN_RELATION
```

---

### TC-4.2 Duplicate ID

Expected：

```text
FATAL DUPLICATE_ID
```

---

### TC-4.3 Empty Boundary

Expected：

```text
WARNING PRINCIPLE_BOUNDARY_EMPTY
```

---

### TC-4.4 Invalid API Key Pattern

Fixture 中放置测试假 key。

Expected：

```text
ERROR POSSIBLE_SECRET
```

---

### TC-4.5 Clean Repo

Expected：

```text
exit code 0
```

---

## 4.11 Exit Condition

任何提交到主仓库的数据都可以经过机器检查。

---

# Phase 5 — CLI & Authoring Workflow

## 5.1 Goal

让用户可以不用手工复制模板完成基本操作。

---

# 5.2 Files to Create

```text
src/praxis/commands/
    new.py
    search.py
    doctor.py

src/praxis/search/
    __init__.py
    text.py
    metadata.py

tests/unit/
    test_new_command.py
    test_search.py
    test_doctor.py
```

---

# 5.3 praxis new

支持：

```bash
praxis new value
praxis new principle
praxis new decision
praxis new experiment
praxis new review
```

执行：

```text
determine domain
generate ID
copy template
populate metadata
create file
```

---

# 5.4 File Naming

建议：

```text
<id>-<slug>.md
```

例如：

```text
PRINCIPLE-CAREER-001-emotion-vs-career.md
```

ID 仍是唯一真实标识。

---

# 5.5 praxis search

支持：

```bash
praxis search "离职"

praxis search "autonomy" --type value

praxis search --status testing

praxis search --domain career

praxis search --related VALUE-LIFE-001
```

搜索范围：

```text
metadata
+
markdown body
```

---

# 5.6 praxis doctor

输出仓库健康报告。

检查：

```text
orphan principles
decisions without review date
overdue decision reviews
unused values
principles never tested
retired principle still referenced
stale constitution
```

---

# 5.7 Acceptance Criteria

- `praxis new principle` 可创建合法文件；
- 新文件 ID 唯一；
- 新文件立即通过 Schema；
- Search 支持全文；
- Search 支持 metadata filter；
- Doctor 输出结构稳定；
- CLI 错误输入不会产生半成品文件。

---

# 5.8 Test Cases

### TC-5.1 Create Principle

执行：

```bash
praxis new principle --domain career --title "Test Principle"
```

Expected：

```text
file created
schema valid
ID unique
```

---

### TC-5.2 Search by Text

Expected：

```text
matching principle returned
```

---

### TC-5.3 Search by Status

```bash
praxis search --status testing
```

Expected：

只返回 testing。

---

### TC-5.4 Doctor Finds Orphan

无 Relation 的 principle。

Expected：

```text
reported as orphan/info
```

---

### TC-5.5 Invalid Domain

Expected：

```text
controlled error
no file created
```

---

## 5.9 Exit Condition

PraxisOS 已经能够作为本地 CLI 产品被使用。

---

# Phase 6 — Skills & Demo Persona

## 6.1 Goal

完成 PraxisOS 的 AI-native 合同层，同时用虚构数据验证完整闭环。

---

# 6.2 Files to Create

```text
skills/
    principle-extractor/
        SKILL.md
        examples/
            input-01.md
            output-01.md

    decision-review/
        SKILL.md
        examples/

    values-audit/
        SKILL.md
        examples/

    quarterly-review/
        SKILL.md
        examples/
```

以及：

```text
examples/demo-persona/
    constitution/
    values/
    models/
    principles/
    decisions/
    experiments/
    reviews/
```

---

# 6.3 Skill Contract

每个 SKILL.md 必须包含：

```text
Purpose
Inputs
Required Context
Procedure
Output Contract
Write Permissions
Forbidden Actions
Examples
```

---

# 6.4 principle-extractor

Output Contract：

```text
statement
source
why
evidence
counter_evidence
boundary
trigger
action_rule
status=candidate
```

禁止：

```text
validated
core
```

---

# 6.5 decision-review

输出：

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
```

必须标记：

```text
Final Judgment: Human Required
```

---

# 6.6 values-audit

只允许：

```text
possible value conflict
possible behavior mismatch
```

禁止：

```text
definitive psychological conclusion
```

---

# 6.7 quarterly-review

聚合：

```text
Decisions
Experiments
Principles
Reviews
```

输出：

```text
Repeated Patterns
Successful Assumptions
Failed Assumptions
Value Conflicts
Principle Candidates
Direction Drift
Next Quarter Focus
```

---

# 6.8 Demo Persona

使用完全虚构角色，例如：

```text
Alex
32
software engineer
considering IC vs management
```

至少包含：

```text
3 Values
2 Models
5 Principles
2 Decisions
1 Experiment
2 Reviews
```

必须演示：

```text
Value
↓
Principle
↓
Decision
↓
Experiment
↓
Review
↓
Principle Revision
```

---

# 6.9 Acceptance Criteria

- 四个 Skill 结构一致；
- Skills 权限规则与 AGENTS.md 一致；
- Demo Persona 可通过全部 validation；
- Demo 至少存在一次 Principle Revision；
- Demo 至少存在一次 Prediction vs Actual Review；
- Demo 不含真实用户数据。

---

# 6.10 Test Cases

### TC-6.1 Skill Structure

检查所有 `SKILL.md` 是否包含 required headings。

Expected：

```text
PASS
```

---

### TC-6.2 No Illegal Promotion

检查 `principle-extractor` 示例。

Expected：

```text
status != validated/core
```

---

### TC-6.3 Demo Validation

```bash
praxis validate examples/demo-persona
```

Expected：

```text
PASS
```

---

### TC-6.4 Demo Relation Integrity

所有：

```text
Value
Principle
Decision
Experiment
Review
```

Relation 均存在。

Expected：

```text
PASS
```

---

### TC-6.5 Revision Demonstration

至少一个 Principle：

```text
validated
→ revised
```

有 Revision History。

Expected：

```text
PASS
```

---

## 6.11 Exit Condition

项目已经具备：

```text
Framework
+
Executable Core
+
AI Contract Layer
+
Demonstrable Example
```

---

# Phase 7 — CI, Hardening & v0.1 Release

## 7.1 Goal

把项目从“能运行”提升到“可公开开源”。

---

# 7.2 Files to Create

```text
.github/workflows/
    test.yml
    validate.yml

.pre-commit-config.yaml

CHANGELOG.md
RELEASE_CHECKLIST.md
```

可选：

```text
Makefile
```

---

# 7.3 GitHub Actions

## test.yml

执行：

```text
checkout
setup python
install
pytest
```

---

## validate.yml

执行：

```text
praxis validate
```

并执行：

```text
privacy scan
repository integrity
```

---

# 7.4 Pre-commit

建议：

```text
trailing whitespace
EOF fix
JSON validation
YAML validation
praxis validate
```

Privacy Scan 可以先只放 CI。

---

# 7.5 Test Coverage

建议：

```text
core modules >= 80%
```

重点不是总覆盖率，而是：

```text
parser
validator
relations
privacy
```

必须充分覆盖。

---

# 7.6 README 完善

README 至少包含：

```text
What is PraxisOS?
Why it exists
Core Concepts
Quick Start
Repository Structure
Example Workflow
Privacy Warning
Agent Safety
Roadmap
License
```

---

# 7.7 Quick Start

目标：

新用户从 clone 到第一条 Principle：

```text
< 10 minutes
```

流程：

```bash
git clone ...
cd praxis-os
pip install -e .
praxis validate
praxis new principle
```

---

# 7.8 Release Checklist

```text
[ ] All tests pass
[ ] praxis validate passes
[ ] Demo persona passes
[ ] No real private data
[ ] No secrets
[ ] LICENSE present
[ ] README complete
[ ] SECURITY.md complete
[ ] AGENTS.md complete
[ ] CHANGELOG updated
[ ] Tag v0.1.0
```

---

# 7.9 Acceptance Criteria

- GitHub Actions 全绿；
- Clean clone 可安装；
- CLI 可执行；
- `praxis validate` 通过；
- Demo Persona 完整；
- 无隐私数据；
- README Quick Start 可复现；
- v0.1.0 Tag 可以发布。

---

# 7.10 Test Cases

### TC-7.1 Clean Clone

新环境：

```bash
git clone
pip install -e .
praxis validate
pytest
```

Expected：

```text
all pass
```

---

### TC-7.2 CI Broken Relation

故意提交 broken relation。

Expected：

```text
CI FAIL
```

---

### TC-7.3 CI Secret Leak

fixture 外故意放测试 secret。

Expected：

```text
CI FAIL
```

---

### TC-7.4 README Quick Start

按文档执行。

Expected：

```text
works without undocumented step
```

---

## 7.11 Exit Condition

PraxisOS v0.1 达到：

```text
PUBLIC OSS READY
```

---

# 8. Cross-Phase Quality Gates

每个 Phase 都必须满足以下规则。

## QG-01 No Hidden Coupling

不得为了未来功能提前写：

```text
database abstraction
RAG adapter
LLM orchestration
web service
```

除非当前 Phase 明确需要。

---

## QG-02 No Private Data

开发 fixture 只能使用：

```text
synthetic data
```

---

## QG-03 Deterministic Core

以下功能必须完全 deterministic：

```text
parse
validate
search
relations
doctor
```

不得依赖 LLM。

---

## QG-04 Human Authority

任何 Skill：

```text
不得自动修改 constitution
不得自动验证 principle
不得写 Final Judgment
```

---

## QG-05 Historical Integrity

原则被修改时不得静默删除过去内容。

必须：

```text
Revision History
```

或者通过 Git History 保留。

---

# 9. Suggested Commit Strategy

建议每个 Phase 单独形成稳定 commit/PR。

例如：

```text
feat/foundation
feat/schemas
feat/repository-core
feat/validation
feat/cli
feat/skills-demo
chore/release-v0.1
```

不要把整个 v0.1 放进一个巨大 PR。

---

# 10. Suggested Coding Agent Execution Rule

每个 Phase 给 Agent 的执行要求：

```text
1. Read PRD.
2. Read Technical Design.
3. Execute only the current Phase.
4. Do not implement future phases.
5. Add tests with every implementation.
6. Run full test suite.
7. Run praxis validate where applicable.
8. Report:
   - files changed
   - tests added
   - acceptance criteria
   - known limitations
9. Stop after current Phase passes.
```

---

# 11. Phase Completion Report Template

Agent 每阶段完成后必须输出：

```text
Phase:
Status:

Implemented:
- ...

Files Added:
- ...

Files Modified:
- ...

Tests:
- ...

Acceptance Criteria:
AC-01 PASS
AC-02 PASS
...

Known Limitations:
- ...

Deferred:
- ...

Ready for Next Phase:
YES / NO
```

---

# 12. Recommended Execution Order

## Phase 1

重点：

> 骨架正确。

不要写业务逻辑。

## Phase 2

重点：

> Schema 正确。

不要写 CLI。

## Phase 3

重点：

> 能稳定读取数据。

不要做验证策略。

## Phase 4

重点：

> 能发现错误。

这是第一个关键里程碑。

## Phase 5

重点：

> 真正开始可用。

## Phase 6

重点：

> 展示 PraxisOS 的思想价值。

## Phase 7

重点：

> 开源发布质量。

---

# 13. Major Milestones

## Milestone A

Phase 1–2 完成：

```text
Specification Complete
```

---

## Milestone B

Phase 3–4 完成：

```text
Core Engine Complete
```

此时：

```bash
praxis validate
```

应成为稳定能力。

---

## Milestone C

Phase 5 完成：

```text
Usable Local Product
```

---

## Milestone D

Phase 6 完成：

```text
PraxisOS Concept Demonstrated
```

---

## Milestone E

Phase 7 完成：

```text
v0.1 Public Release
```

---

# 14. What v0.1 Explicitly Defers

以下内容进入 v0.2+：

```text
RAG
Embeddings
Vector Database
Web UI
Notion Sync
Obsidian Plugin
LLM Provider API
Multi-Agent
Graph Database
Mobile App
Cloud Sync
Automatic Reminders
Resume RAG
Finance Integration
```

原则：

> 如果 v0.1 的思想闭环本身不好用，任何 AI 和 RAG 都只是放大一个不好用的系统。

---

# 15. Final v0.1 Acceptance Flow

最终必须能完整演示：

```text
Create Value
      ↓
Create Model
      ↓
Extract Principle
      ↓
Create Decision
      ↓
Attach Relevant Principle
      ↓
Create Experiment
      ↓
Record Outcome
      ↓
Create Review
      ↓
Revise Principle
      ↓
Run praxis validate
      ↓
PASS
```

这个流程完整跑通，才能宣布：

```text
PraxisOS v0.1 = DONE
```