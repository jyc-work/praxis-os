---
id: EXPERIMENT-CAREER-001
type: experiment
title: 外部市场竞争力测试（demo persona）
status: completed
hypothesis: 当前市场竞争力不足
start_date: 2026-06-01
end_date: 2026-08-01
related_decision:
  - DECISION-CAREER-001
related_principles:
  - PRINCIPLE-LIFE-001
  - PRINCIPLE-CAREER-003
metrics:
  - resume_pass_rate
  - first_round_rate
  - second_round_rate
  - offer_rate
created_at: 2026-06-01
updated_at: 2026-08-01
---

# Problem

"我的市场竞争力是不是不足"是一个无法直接回答的问题，需要转化为可测量的实验。

# Hypothesis

如果投递 20 个目标岗位，简历通过率将低于 30%。

# Experiment

向 20 个目标岗位投递简历（同一版本），记录每个阶段的转化率；
不接最终 offer，仅采集市场信号，历时 8 周。

# Minimum Action

第一周完成简历更新并投递首批 5 个岗位。

# Metric

- resume_pass_rate：简历筛选通过数 / 投递数
- first_round_rate：一面通过数 / 面试数
- second_round_rate：二面通过数 / 一面数
- offer_rate：offer 数 / 投递数

# Expected Result

简历通过率 < 30%，offer 率 < 10%，支撑"竞争力不足"假设。

# Actual Result

- 投递 20；简历通过 14（70%）
- 一面 10/14 通过（71%）
- 二面 4/4 通过（100%）
- offer 5/20（25%）
→ 假设被证伪：市场竞争力高于预期。

# What I Learned

"市场竞争力不足"的假设不成立；持续积累在市场中是可检验的。
市场校准本身成本低、信息价值高，值得作为年度例行实验。

# Principle Impact

- PRINCIPLE-LIFE-001 因本实验被修订（补充"市场校准"条款，validate → revise）。
- PRINCIPLE-CAREER-003 获得支持证据（将问题转化为可测量实验有效）。