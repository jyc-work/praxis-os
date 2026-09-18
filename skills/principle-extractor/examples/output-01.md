# Output 01 — principle candidate (principle-extractor)

```yaml
candidate_principle: 感情影响离开的方式，但不能单独决定职业去留
statement: 同事的情分和领导的好意可以影响如何离开（时机、方式、善后），但不足以单独决定是否留下。
source: conversation
reasoning_summary: Alex 因团队氛围和领导照顾而犹豫离职，但长期成长数据（一年无有效产出）显示留下会继续消耗。人际善意应计入离开的"方式"，而不应单独决定"去留"。
evidence: 2026-08 与对话者复盘时确认：过去一年技术产出近乎为零、成长曲线平坦；同时领导在 release 中提供支持（事实）。
counter_evidence: 若善意是长期可兑现的投资（例如领导明确承诺并实际安排成长机会），情分可能与去留相关。
boundary: 当团队善意代表了实在的发展机会（明确的晋升通道、核心技术项目）时，此原则不适用；紧急利益冲突（欠债、违约）时不适用。
trigger: 因为同事/领导的人情而犹豫职业去留时。
action_rule: IF 因人情犹豫职业去留 THEN 分别评估“成长证据”与“情分分量”，并让成长证据决定去留、情分决定离开的方式。
status: candidate
```

Note: does **not** say `validated` or `core`. The file may only be written to
`principles/` after human confirmation.