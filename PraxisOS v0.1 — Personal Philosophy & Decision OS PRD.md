# PraxisOS v0.1
## Personal Philosophy & Decision Operating System

**版本：** v0.1  
**状态：** Draft / MVP Design  
**项目形态：** Open Source / Local First / AI Native  
**默认许可证：** MIT  
**核心载体：** Markdown + YAML Frontmatter + Git  
**核心理念：** Thought → Principle → Decision → Action → Feedback

---

# 1. 项目背景

现有多数 Personal OS、Second Brain、LifeOS 系统主要围绕：

- Goals
- Projects
- Tasks
- Habits
- Notes
- Journals

它们主要解决：

> “我要管理什么事情？”

但 PraxisOS 试图解决更上层的问题：

> **我为什么这样选择？**

以及：

> **什么样的人生值得我去构建？**

人的价值观、人生目标、现实经历、思想体系和具体行动之间经常是割裂的。

常见问题包括：

1. 阅读大量哲学、心理学、历史和人物传记，但无法转化成个人行为；
2. 知道很多道理，遇到真实问题依然凭情绪决策；
3. 某次经历产生重要认识，但几个月后重新犯同样错误；
4. 人生目标随着情绪不断变化；
5. 对某些人物或思想高度认同，却不知道具体认同什么；
6. 大量日记、聊天记录、读书笔记无法形成稳定原则；
7. AI 能给建议，却不了解用户长期形成的价值体系；
8. 人容易根据当下情绪重新解释过去，无法检验自己的判断质量。

PraxisOS 的目标是建立：

> **一个可以持续演化、接受现实验证的个人思想与决策系统。**

---

# 2. 产品愿景

PraxisOS 不替用户决定人生。

PraxisOS 应帮助用户：

1. 认识自己的价值观；
2. 建立对世界的模型；
3. 将外部思想转化为个人原则；
4. 用原则辅助现实决策；
5. 将决策转化为行动；
6. 记录行动结果；
7. 检验过去判断；
8. 修正错误原则；
9. 最终逐渐形成属于自己的思想体系。

最终形成闭环：

```text
Reality
   ↓
Observation
   ↓
Reflection
   ↓
World Model
   ↓
Principle
   ↓
Decision
   ↓
Action / Experiment
   ↓
Outcome
   ↓
Review
   ↓
Update Principle
   └──────────────────→
```

---

# 3. 产品原则

## 3.1 用户拥有最终裁决权

AI 是：

- 分析者；
- 反方；
- 检索者；
- 结构化助手；
- 复盘助手。

AI 不是：

- 人生导师；
- 道德裁判；
- 最终决策者。

所有重要 Decision 必须包含：

```text
Final Judgment: Human
```

---

## 3.2 Reality > Ideology

任何思想体系都不得因为其理论权威而自动被接受。

原则必须允许：

- 被现实证伪；
- 被修改；
- 被降级；
- 被废弃。

---

## 3.3 Principle > Quote

PraxisOS 不鼓励建立“名人语录库”。

系统重点保存：

> **用户自己认可并经过思考的原则。**

引用思想家的观点，只作为：

```text
Source / Inspiration
```

而不是系统最终结论。

---

## 3.4 Action > Consumption

阅读、收藏、视频、文章本身不算完成学习。

理想转化路径：

```text
Input
↓
Reflection
↓
Principle Candidate
↓
Action Rule
↓
Experiment
↓
Outcome
```

没有进入现实验证的思想默认属于：

```text
UNVALIDATED
```

---

## 3.5 Framework Public, Personal Data Private

GitHub 开源：

- Schema
- Templates
- Skills
- Prompt
- Methodology
- Sample data

默认禁止公开：

- 私人日记
- 真实资产
- 身份信息
- 公司机密
- 同事姓名
- 真实投资仓位
- 私人关系信息

---

# 4. 核心目标

PraxisOS v0.1 必须实现以下六个核心能力。

## G1 — Value Discovery

帮助用户逐渐发现：

> 我真正重视什么？

不是做一次价值观测试后永久固定，而是通过：

- 行为；
- 决策；
- 冲突；
- 后悔；
- 长期投入；

反推真实价值观。

---

## G2 — Principle Formation

能够把：

> 外部思想 / 人生经历 / 失败 / 成功

转化成：

> Personal Principle

---

## G3 — Structured Decision

重大决策不能只记录结果，还应记录：

- 当时掌握的信息；
- 情绪；
- 利益；
- 可选方案；
- 所用原则；
- 判断理由；
- 预测结果。

---

## G4 — Action Translation

所有重要原则均可以进一步转换为：

```text
IF condition
THEN action
```

例如：

```text
IF
职业连续 6 个月没有有效成长

THEN
启动外部市场测试
```

---

## G5 — Outcome Feedback

系统必须支持：

```text
Decision
↓
Prediction
↓
Actual Outcome
↓
Prediction Error
↓
Review
```

解决：

> “当时我觉得自己判断得很正确，但后来到底正确没有？”

---

## G6 — Personal Constitution

随着长期使用，逐渐形成用户自己的：

```text
Personal Constitution
```

它不是一次填写完成，而应该持续演化。

---

# 5. 非目标

v0.1 **明确不做**：

- 社交网络；
- Todo App；
- 日历系统；
- 全功能知识管理工具；
- 财务记账；
- 自动股票交易；
- 心理诊断；
- AI 自动替用户做人生决定；
- 复杂 Multi-Agent；
- Vector Database；
- GraphRAG；
- SaaS；
- 移动 App；
- 微服务；
- 大型 Web Dashboard。

原则：

> **MVP 首先证明思想闭环，而不是技术复杂度。**

---

# 6. 核心信息架构

PraxisOS 第一版包含六类核心实体。

```text
                    Constitution
                         │
                         ↓
Values ←──────────── Principles
  ↑                       │
  │                       ↓
World Models ───────── Decisions
                          │
                          ↓
                     Experiments
                          │
                          ↓
                       Reviews
                          │
                          └────→ Principles
```

---

# 7. Module 01 — Personal Constitution

路径：

```text
/constitution/
```

核心文件：

```text
constitution.md
values.md
anti-values.md
direction.md
guardrails.md
```

---

## 7.1 Constitution

回答：

> 我希望成为怎样的人？

> 我希望建立怎样的生活？

> 我最终希望获得什么？

推荐结构：

```yaml
version: 0.1
last_reviewed:
status: evolving
```

正文包含：

### Life Direction

长期人生方向。

### Core Values

核心价值。

### Anti-Values

拒绝成为怎样的人。

### Non-Negotiables

不可交换原则。

### Desired Life Structure

理想生活结构。

### Definition of Enough

什么叫：

> “已经足够。”

防止目标无限膨胀。

---

# 8. Module 02 — Values

路径：

```text
/values/
```

Value 数据结构：

```yaml
id: VALUE-AUTONOMY
name: Autonomy
name_zh: 自主
status: active

priority: high

definition:
evidence:
conflicts_with:
related_values:

created_at:
updated_at:
```

Value 必须区分：

```text
Claimed Value
vs
Revealed Value
```

### Claimed Value

用户嘴上认为重要。

### Revealed Value

通过长期行为表现出的真实偏好。

AI 可以指出差距，但不得自行修改 Value。

---

# 9. Module 03 — World Models

路径：

```text
/models/
```

用于记录：

> 我如何理解世界。

例如：

```text
/models/machiavelli/
/models/legalism/
/models/stoicism/
/models/adler/
/models/taoism/
```

以及：

```text
/models/organization/
/models/career/
/models/markets/
/models/human-behavior/
```

Thinker / Model 模板：

```yaml
id:
name:
type: thinker | philosophy | mental-model

status: studying

confidence:

tags:
```

正文：

```text
## Core Claim

## Human Nature

## Power

## Wealth

## Action

## Failure

## Relationships

## Emotion

## Career

## Investing

## What I Agree With

## What I Reject

## Where It Works

## Where It Fails

## My Interpretation

## Derived Principles
```

重点：

> 最后必须进入 Derived Principles。

否则只是知识收藏。

---

# 10. Module 04 — Principles

路径：

```text
/principles/
```

这是 PraxisOS 的核心数据库。

Principle Schema：

```yaml
id: PRINCIPLE-CAREER-001

title:

domain:
  - career

status:
  - candidate
  - testing
  - validated
  - revised
  - retired

confidence:
  - low
  - medium
  - high

source_type:
  - experience
  - thinker
  - book
  - decision
  - review

sources:

created_at:
updated_at:
last_tested:
```

正文模板：

```text
# Principle

## Statement

一句话原则。

## Why

为什么相信它？

## Evidence

什么现实经历支持它？

## Counter Evidence

什么证据反对它？

## Boundary

什么时候不适用？

## Trigger

什么时候应该调用？

## Action Rule

IF ...

THEN ...

## Related Principles

## History

这个原则经历了哪些修订？
```

---

# 11. Principle 生命周期

```text
Candidate
   ↓
Testing
   ↓
Validated
   ↓
Repeated Validation
   ↓
Core Principle
```

也可能：

```text
Validated
   ↓
Contradictory Evidence
   ↓
Revised
```

或者：

```text
Testing
   ↓
Failed
   ↓
Retired
```

系统必须允许：

> **自己过去的思想是错的。**

这是 PraxisOS 与普通“人生信条”最大的区别之一。

---

# 12. Module 05 — Decision Journal

路径：

```text
/decisions/
```

每个重要决策建立独立记录。

Schema：

```yaml
id: DECISION-2026-001

title:

domain:
  - career

status:
  - considering
  - decided
  - executing
  - reviewed

decision_date:

review_dates:
  - 30d
  - 90d
  - 365d

confidence:

related_values:
related_principles:
related_models:
```

模板：

```text
# Situation

发生了什么？

# Facts

确定事实是什么？

# Unknowns

不知道什么？

# Emotion

当前情绪是什么？

# Interests

我的利益是什么？

# Objectives

我希望实现什么？

# Options

## Option A

## Option B

## Option C

# Trade-offs

每个方案失去什么？

# Relevant Principles

哪些 Personal Principles 适用？

# Lens Analysis

## Machiavelli Lens

利益、资源、权力结构是什么？

## Legalist Lens

规则、激励、制度是什么？

## Stoic Lens

什么可控？
什么不可控？

## Adler Lens

我是否在逃避？
当前行为满足什么目的？

## Taoist Lens

这个问题值得解决吗？
是否存在过度行动？

# Final Judgment

我的判断。

# Decision

最终行动。

# Prediction

30天后：
90天后：
365天后：

# Confidence

0–100%

# Review
```

---

# 13. Lens 不是答案生成器

五种思想模型只能提供：

> Perspectives

而不是：

> Final Answers

系统必须防止：

```text
Stoicism says X
→ therefore user must X
```

正确方式：

```text
Stoicism suggests:
X

Potential limitation:
Y

User judgment:
Z
```

---

# 14. Module 06 — Experiments

路径：

```text
/experiments/
```

很多人生问题没有足够信息直接决策。

此时系统应建议：

> Small Experiment

而不是继续空想。

Schema：

```yaml
id:

hypothesis:

status:
  - planned
  - running
  - completed
  - abandoned

start_date:
end_date:

success_metric:

related_decision:
related_principle:
```

模板：

```text
# Problem

# Hypothesis

# Experiment

# Minimum Action

# Metric

# Expected Result

# Actual Result

# What I Learned

# Principle Impact
```

例如：

```text
Hypothesis:
我的市场竞争力较弱。

Experiment:
投递20个目标岗位。

Metric:
简历通过率
一面率
二面率
Offer率
```

将：

> “就业市场是不是很差？”

转化为：

> 可测量的问题。

---

# 15. Module 07 — Reviews

路径：

```text
/reviews/
```

包含：

```text
weekly/
monthly/
quarterly/
annual/
decision/
```

---

# 16. Weekly Review

只回答：

```text
1. 本周最重要的事件是什么？

2. 我做了什么重要判断？

3. 有没有违背自己的原则？

4. 有没有发现一个新的原则候选？

5. 下周只改变什么？
```

目标：

**10–20 分钟完成。**

---

# 17. Monthly Review

重点评估：

```text
Ability
能力

Assets
资产

Optionality
选择权

Dependency
依赖程度

Energy
精力

Attention
注意力
```

---

# 18. Quarterly Direction Review

核心问题：

> **过去三个月，我是在变得更加自由，还是更加依赖？**

进一步检查：

```text
Career
Money
Skills
Relationships
Health
Time
Projects
Learning
```

然后检查：

```text
我的行为
vs
我的价值观
```

是否一致。

---

# 19. Decision Review

任何重要 Decision 到期后必须支持 Review：

```text
What did I predict?

What actually happened?

Where was I wrong?

What information did I ignore?

Was the decision wrong,
or was the outcome merely unlucky?

Which principle needs updating?
```

必须明确区分：

```text
Decision Quality
≠
Outcome Quality
```

不能因为坏结果自动认定决策错误。

---

# 20. 核心 Skills

v0.1 只设计 4 个。

---

## Skill 01 — principle-extractor

用途：

将：

- 聊天
- 书籍笔记
- 视频
- 经历
- 失败
- 成功

转成 Principle Candidate。

流程：

```text
Input
↓
Core Claim
↓
User Interpretation
↓
Evidence
↓
Counter Evidence
↓
Boundary
↓
Principle Candidate
↓
IF / THEN
```

---

## Skill 02 — decision-review

输入：

一个现实决策。

输出：

```text
Facts
Unknowns
Emotion
Interest
Objectives
Options
Trade-offs
Principles
Five Lenses
Experiment
Final Human Decision
```

---

## Skill 03 — values-audit

分析：

```text
Claimed Values
vs
Actual Behavior
```

例如：

用户声称：

> 自由最重要。

但过去一年：

> 大量时间用于维护一个没有成长的工作关系。

系统可以提出：

```text
Possible value conflict detected:

Autonomy
vs
Security / Familiarity
```

不能自行下结论。

---

## Skill 04 — quarterly-review

聚合：

```text
Decisions
Experiments
Principles
Reviews
```

输出：

```text
What changed?

Repeated mistakes

Validated principles

Questionable principles

Emerging values

Direction drift

Next-quarter focus
```

---

# 21. 数据存储

v0.1 使用：

```text
Markdown
+
YAML Frontmatter
+
Git
```

不引入数据库。

原因：

1. 可读；
2. 可搜索；
3. 可版本控制；
4. AI 友好；
5. 不绑定平台；
6. 可轻松迁移；
7. 后期容易 ETL。

---

# 22. 推荐 Repository Structure

```text
praxis-os/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── ARCHITECTURE.md
├── AGENTS.md
│
├── docs/
│   ├── philosophy.md
│   ├── methodology.md
│   ├── privacy.md
│   └── roadmap.md
│
├── constitution/
│   ├── constitution.template.md
│   ├── values.template.md
│   ├── anti-values.template.md
│   ├── direction.template.md
│   └── guardrails.template.md
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
│   ├── thinker.md
│   ├── principle.md
│   ├── decision.md
│   ├── experiment.md
│   ├── weekly-review.md
│   └── quarterly-review.md
│
├── skills/
│   ├── principle-extractor/
│   ├── decision-review/
│   ├── values-audit/
│   └── quarterly-review/
│
├── examples/
│   └── demo-persona/
│
├── tests/
│
└── private/
    ├── README.md
    └── .gitignore
```

---

# 23. Privacy Model

默认采用：

```text
Framework
PUBLIC

Personal Data
PRIVATE
```

`.gitignore`：

```text
/private/**
/data/private/**
/journals/private/**
.env
*.secret.*
```

Sample Data 必须：

- 完全虚构；
- 去身份化；
- 不包含用户真实经历。

---

# 24. Notion Integration

Notion 属于：

> Optional Adapter

而不是 Source of Truth。

推荐逻辑：

```text
Markdown / Git
       ↓
Core Knowledge
       ↓
Notion Adapter
       ↓
Human-friendly UI
```

原因：

PraxisOS 不应绑定某个平台。

未来可支持：

```text
Notion
Obsidian
Logseq
Plain Markdown
Web UI
```

---

# 25. AI Provider Design

不得绑定单一模型。

统一抽象：

```text
LLM Provider
```

允许：

- OpenAI
- Anthropic
- Gemini
- DeepSeek
- Local Models

Skill 主要依赖：

```text
Markdown Contracts
+
Prompt
+
Structured Output
```

---

# 26. RAG Roadmap

## v0.1

不使用 RAG。

直接文件搜索。

---

## v0.2

加入：

```text
Metadata Search
Full-text Search
```

---

## v0.3

当满足以下条件：

```text
Principles > 100

Decisions > 100

Reviews > 100

Notes > 500
```

再评估：

```text
Embedding
Hybrid Search
Reranking
```

---

## v0.4+

可考虑：

```text
Personal RAG
```

例如用户询问：

> 我要不要接受这个 Offer？

系统检索：

```text
Personal Constitution
Relevant Values
Career Principles
Previous Job Decisions
Past Regrets
Related Experiments
```

然后形成分析上下文。

---

# 27. Resume / Career RAG

Career Knowledge Base 与 PraxisOS 关联，但不属于其核心库。

未来结构：

```text
PraxisOS
│
├── Life KB
│
├── Career KB
│     ↓
│  Resume RAG
│
├── Finance KB
│
└── Learning KB
```

Resume RAG 专门处理：

```text
JD
↓
Relevant Experience
↓
Project Evidence
↓
STAR Story
↓
Resume Variant
```

不与私人价值观数据直接混用。

---

# 28. 第一批 Seed Data

PraxisOS Demo 可以包含匿名示例原则：

### Principle 001

> 感情可以影响离开的方式，但不能单独决定职业去留。

---

### Principle 002

> 职业前途不用来偿还普通人情。

---

### Principle 003

> 优先增加能力、资产和选择权。

---

### Principle 004

> 不回避真实问题，也不过度解决虚假问题。

---

### Principle 005

> 对不可控结果产生持续焦虑时，把注意力转向24小时内可执行的可控动作。

---

### Principle 006

> 关键问题建立规则，非关键问题减少管理。

---

# 29. 示例价值模型

Demo Constitution：

```text
Core Goal:
Increase autonomy.

Primary Drivers:
Ability
Assets
Optionality

Avoid:
Excessive dependency
Status games
Lifestyle inflation
Unnecessary conflict
```

强调：

> 这是 Demo Persona，不代表所有用户。

---

# 30. MVP 用户流程

第一次使用：

```text
Clone Repo
↓
Run Init
↓
Create Constitution
↓
Define 3–7 Values
↓
Create First Principle
↓
Create First Decision
↓
Create First Experiment
↓
Weekly Review
```

---

# 31. CLI（可选）

未来可支持：

```bash
praxis init

praxis principle new

praxis decision new

praxis experiment new

praxis review weekly

praxis review quarterly

praxis search

praxis validate
```

v0.1 CLI 不是强制需求。

---

# 32. Schema Validation

开发一个轻量验证脚本：

```bash
praxis validate
```

检查：

- ID 唯一；
- YAML 合法；
- status 合法；
- Relation 是否存在；
- Principle 是否包含 Boundary；
- Decision 是否包含 Final Judgment；
- Review Relation 是否完整。

---

# 33. AGENTS.md

仓库必须包含 Agent 操作规范。

核心规则：

```text
1. Never modify Personal Constitution without explicit approval.

2. Never promote a Principle from candidate to validated automatically.

3. Never make final life decisions for the user.

4. Always distinguish facts, inference, emotions and values.

5. Preserve historical versions of Principles.

6. Never expose files under /private.

7. Prefer asking:
"What evidence would change this belief?"

8. When recommending action, prefer reversible experiments when uncertainty is high.
```

---

# 34. Success Metrics

MVP 成功不以：

```text
GitHub Stars
Downloads
AI Tokens
Number of Notes
```

衡量。

而看：

### M1

用户能否在 5 分钟内找到：

> “我为什么会这样做？”

### M2

重大决策是否能够追溯到：

```text
Value
→ Principle
→ Decision
```

### M3

Decision 是否存在后续 Review。

### M4

是否发生过：

```text
Principle Revision
```

如果从来没有修改过原则，说明系统可能只是确认偏见。

### M5

长期是否逐渐减少：

> 重复犯同一类错误。

---

# 35. 风险

## R1 — AI Echo Chamber

AI 不断强化用户已有看法。

解决：

每个重要 Principle 必须包含：

```text
Counter Evidence
Boundary
Disconfirming Evidence
```

---

## R2 — Overthinking

用户不断分析，不行动。

解决：

Decision 模板必须包含：

```text
Next Action
```

不确定性高时：

```text
Small Experiment
```

---

## R3 — Philosophy Cosplay

用户只是模仿哲学家的语言。

解决：

所有思想必须经过：

```text
My Interpretation
```

以及：

```text
Real-world Evidence
```

---

## R4 — System Building Addiction

用户沉迷完善 Personal OS 而不生活。

解决：

明确：

> PraxisOS 服务现实，不是现实服务 PraxisOS。

系统复杂度必须服从实际收益。

---

## R5 — Personal Data Leakage

通过 GitHub 意外公开隐私。

解决：

默认：

```text
/private
```

完全 gitignore。

提供：

```text
privacy-check
```

防止提交敏感数据。

---

# 36. 技术原则

优先级：

```text
Portability
>
Transparency
>
Simplicity
>
AI Compatibility
>
Automation
>
UI
```

第一版：

> **宁可丑，也不要复杂。**

---

# 37. Roadmap

## v0.1 — Foundation

实现：

- Repository structure
- Schemas
- Templates
- 4 Skills
- Sample Persona
- Validation
- Documentation

---

## v0.2 — Local Tooling

加入：

- CLI
- Full-text Search
- Relation Graph
- Review reminders
- Statistics

---

## v0.3 — AI Layer

加入：

- LLM Adapter
- Principle Extraction
- Decision Analysis
- Value Conflict Detection
- Review Summarization

---

## v0.4 — Personal Retrieval

加入：

- Hybrid Search
- Embedding
- Reranker
- Personal RAG

---

## v0.5 — Integrations

加入：

- Notion
- Obsidian
- Calendar
- GitHub
- Career KB

---

## v1.0 — Personal Decision OS

目标：

能够可靠完成：

```text
Experience
↓
Knowledge
↓
Principle
↓
Decision
↓
Experiment
↓
Feedback
↓
Growth
```

---

# 38. 项目的一句话定义

> **PraxisOS is an open-source personal philosophy and decision operating system that turns values, ideas and lived experience into principles, decisions, experiments and feedback.**

中文：

> **PraxisOS 是一个开源个人思想与决策操作系统，将价值观、思想和真实经历转化为原则、决策、行动实验与现实反馈。**

---

# 39. 核心差异化

传统 Second Brain：

```text
Remember better.
```

传统 Productivity System：

```text
Do more.
```

PraxisOS：

```text
Think better.
Decide deliberately.
Act.
Learn from reality.
```

即：

> **不是帮助一个人保存更多知识，而是帮助一个人逐渐形成自己的思想，并检验这些思想是否真的能够指导人生。**

---

# 40. MVP Definition of Done

只有满足以下条件才能认为 v0.1 完成：

- [ ] README 完成
- [ ] Architecture 完成
- [ ] Philosophy 完成
- [ ] Privacy Model 完成
- [ ] Constitution Template
- [ ] Value Schema
- [ ] World Model Schema
- [ ] Principle Schema
- [ ] Decision Schema
- [ ] Experiment Schema
- [ ] Review Schema
- [ ] Principle Extractor Skill
- [ ] Decision Review Skill
- [ ] Values Audit Skill
- [ ] Quarterly Review Skill
- [ ] Sample Persona
- [ ] 至少 5 个 Demo Principles
- [ ] 至少 2 个 Demo Decisions
- [ ] 至少 1 个 Demo Experiment
- [ ] Schema Validation
- [ ] GitHub Actions 基础检查
- [ ] LICENSE
- [ ] CONTRIBUTING
- [ ] Privacy / Security Guide

v0.1 完成之后，才讨论是否加入：

> Web UI / Database / RAG / Multi-Agent。

---

# 41. 最终设计原则

PraxisOS 应始终遵守：

> **思想不是用来崇拜的，而是用来检验的。**

> **价值观不是写在纸上的，而是通过长期选择体现的。**

> **原则不是永恒真理，而是当前最可靠的行为假设。**

> **决策不是为了保证正确，而是为了在不确定环境中提高判断质量。**

> **复盘不是为了后悔，而是为了修正模型。**

> **最终目标不是构建完美系统，而是形成一个越来越独立、清醒、有行动能力的人。**