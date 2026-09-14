---
type: concept
status: draft
title: 自适应失败分类体系
created: 2026-09-14
updated: 2026-09-14
tags: [failure-taxonomy, execution-traces, agents]
related: [2607.16387v2, AdaMAST, taxonomy-conditioned-consumer, online-failure-code-refinement, failure-compression]
source_id: p-72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
content_version: sha256:72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
sources: ["raw/sources/2607.16387v2.pdf"]
---
# 自适应失败分类体系

自适应失败分类体系，是针对特定智能体系统，从执行轨迹中归纳出来的一组紧凑、有证据依据且具名的失败代码词表。

在 AdaMAST 中，框架保留三个轴：`A` 表示系统级失败，`B` 表示角色或阶段特定失败，`C` 表示领域推理失败；具体代码、定义和证据模式则保持系统特定性。六个领域分类体系之间的平均两两 Jaccard 重叠率仅为 `0.14`，支持这种特定性（PDF p. 1）。
