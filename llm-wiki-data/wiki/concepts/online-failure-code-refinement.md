---
type: concept
status: draft
title: 在线失败代码优化
created: 2026-09-14
updated: 2026-09-14
tags: [online-refinement, failure-codes, adaptation]
related: [2607.16387v2, AdaMAST, adaptive-failure-taxonomy]
source_id: p-72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
content_version: sha256:72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
sources: ["raw/sources/2607.16387v2.pdf"]
---

# 在线失败代码优化

在线优化会在架构或轨迹分布发生变化后，合并、增加、停用或重命名失败代码。

在 OlympiadBench 中，初始分类体系包含 36 个代码（`16A/6B/14C`），并在第 29、78 和 92 次迭代中出现新代码。该结果表明失败描述会自适应变化，但没有从因果上分离每次优化对分数跃升的影响（PDF p. 17）。
