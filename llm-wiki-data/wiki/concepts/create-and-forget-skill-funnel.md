---
type: concept
status: draft
source_id: p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
content_version: sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
title: Create-and-Forget Skill Funnel
created: 2026-09-13
updated: 2026-09-13
tags: [skills, tool-use, lifecycle, continual-learning]
related: [continual-harness, agentic-harness, capability-floor, schema-fragility]
sources: ["raw/sources/2605.09998v1.pdf"]
---

# Create-and-Forget Skill Funnel

> 来源：[[sources/2605.09998v1|Continual Harness]]；PDF pp. 22–24，Figure 16，Appendix C.1。

Create-and-forget skill funnel 描述 skill 从创建、被调用、重复调用到最终成功之间的大幅流失。

该来源的不同条件每次创建 99–335 个 skills，但只有 16–53 个至少被调用一次，只有 3–14 个至少成功一次。尽管存在很长的未使用尾部，少量 working set 聚集了数百次 invocations 和大多数成功执行。

因此 [[continual-harness]] 更像选择性的 triage 与 debugging 机制，而不是持续维护均匀高质量 skill library 的过程。评估应衡量真实 invocations、复用与成功，而不只是生成 components 的数量。

自然的下一步是引入 reuse prior 或 pruning policy，以减少未使用 skills，同时保留有价值的探索。
