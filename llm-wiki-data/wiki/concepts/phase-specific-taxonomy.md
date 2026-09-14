---
type: concept
status: draft
title: 阶段特定分类体系
created: 2026-09-14
updated: 2026-09-14
tags: [single-agent, phases, runtime-feedback]
related: [2607.16387v2, AdaMAST, adaptive-failure-taxonomy, reliable-resolution-conversion]
source_id: p-72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
content_version: sha256:72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
sources: ["raw/sources/2607.16387v2.pdf"]
---

# 阶段特定分类体系

阶段特定分类体系将 `B` 轴适配到单智能体 harness 的不同阶段，例如 `Edit`、`Plan` 和 `Verify`。

论文将这种形式与 TheoremQA 等扁平架构进行对比；后者不会产生 `B` 类代码。在 Claude Code 中，`B.7 Verify partial run misreported as success` 出现在 `40.7%` 的已评判会话中，但只是较弱的失败预测指标；`B.3 Edit overbroad patch footprint` 仅出现于 `8.0%` 的会话，却在 `11/12` 次触发中与未解决结果相关（PDF p. 37）。
