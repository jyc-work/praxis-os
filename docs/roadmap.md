# Roadmap

> 路线原则：思想闭环的价值先于技术复杂度；真实使用先于功能堆叠。

## v0.1-rc — Engineering Complete (当前)

- [x] Repository foundation: LICENSE (MIT), AGENTS.md, docs, ADRs, config
- [x] Six entity schemas (value / model / principle / decision / experiment / review)
- [x] Markdown templates (含 constitution 五模板、review status=planned)
- [x] Parser & repository index (SafeLoader、date 规范化、private 排除)
- [x] `praxis validate` 四层：schema / IDs / relations / semantic / privacy（稳定 exit code）
- [x] CLI: `validate`、`new`、`search`、`doctor`
- [x] 四个 agent skills (principle-extractor / decision-review / values-audit / quarterly-review)
- [x] Demo persona（虚构 Alex 完整闭环：Value→Principle→Decision→Experiment→Review→Revision）
- [x] CI（test.yml / validate.yml / pre-commit / privacy self-scan）+ 打包 schemas（data-files）
- [x] 独立代码审查修复（Final Judgment 模板、死分支、config 开关、new 冲突报错）
- [ ] v0.1.0 Release Gate（见下；打 tag 前执行）

**状态：v0.1 Engineering Complete → Personal Dogfooding Begins**

## Phase 8 — Personal Dogfooding

> 拿自己来真正使用 PraxisOS，连续使用几周，不增加大功能。
> 真实私有数据不提交公共仓库（放 private/ 或独立的私有 PraxisOS-data repo）。

首批导入内容（来自真实讨论）：
- Constitution v0.1；Values（Autonomy/Rationality/Independence/Optionality/Competence）
- World Models（Machiavelli / Legalism / Stoicism / Adler / Taoism）
- Principles（感情与去留、人情不抵职业、能力/资产/选择权、真实 vs 虚假问题、焦虑→24h 可控动作）
- Decisions（是否继续当前岗位；Java/大数据/Agent 职业定位）
- Experiments（外部市场竞争力测试）
- Reviews（因 PL/熟悉感推迟离职的事后复盘）

**重点观察 6 个问题**（它们决定真正的 v0.2）：
1. 记录成本是否太高（一个原则 15 字段是否劝退）
2. Principle 与 Value 是否混淆（"自主"是 Value；"不把职业安全寄托于单一组织"才是 Principle）
3. Decision 模板是否太重（未来可能 light / full 两种）
4. Relation 是否真的有用（用不上就是结构噪声）
5. Review 能否真正修改原则（只增不改 = 价值观确认机器）
6. AI Skill 是否减少思考负担（聊天自然转结构化，而非逼人填库）

## v0.1.0 — 首个稳定开源版本

Release Gate（打 v0.1.0 tag 前逐项通过）：
- [ ] Clean clone 从零安装（README Quick Start 完全照做）
- [ ] Windows / Linux 至少各跑一次测试与 validate
- [ ] `praxis validate` 对根仓库与 demo 均为 0 error
- [ ] secret/privacy scan（含全仓自扫描）
- [ ] **Git 历史隐私检查**：搜索本机用户名、绝对路径、公司名、个人姓名——
      **不要只查当前工作树，历史里删过的提交也要查**（公开后可从历史找回）
- [ ] 第三方项目借鉴部分的许可证与 attribution 检查
- [ ] 统一测试覆盖率口径
- [ ] CHANGELOG.md 固化
- [ ] 打 v0.1.0 tag 后再生成 GitHub Release

## v0.1.x — 体验修复期

只修 Dogfooding 暴露的体验 / Schema / Validator 问题，不加功能。

## v0.2 — Local Intelligence

- Full-text + metadata search 加固（CLI 已有，精化）
- Relation graph / navigation
- Review reminders（decision review dates）
- Statistics（repeated mistakes、principle health）

## v0.3 — AI Layer

- Provider-agnostic LLM adapter（OpenAI / Anthropic / Gemini / DeepSeek / local）
- Principle extraction（对话式）
- Decision analysis（多镜头辅助）
- Value-conflict detection
- Review summarisation
- Core 保持确定性；AI 只是可选层

## v0.4 — Personal Retrieval（进一步后置）

- Hybrid search + embeddings + reranking
- **前置条件**：真实积累足够长期个人数据（Principles/Decisions/Reviews > 阈值），
  而不是为了 Retrieval 而 Retrieval
- Personal RAG：提问 → 检索 constitution/values/principles/过去决策/遗憾/实验 → 上下文 → 人决定

## v0.5 — Integrations

- Notion / Obsidian 仅作 view adapter（不引入同步冲突）
- Calendar、GitHub、Career KB（与个人价值观数据隔离）

## v1.0 — Personal Decision OS

可靠完成闭环：Experience → Knowledge → Principle → Decision → Experiment → Feedback → Growth

## 触发条件

| 阶段 | Gate |
| --- | --- |
| Phase 8 Dogfooding | v0.1-rc 已发布并实际使用 |
| v0.1.0 | Release Gate 全绿 |
| v0.3 AI layer | 真实使用确认有需求 |
| v0.4 Retrieval | 长期数据积累达标（而非功能冲动） |