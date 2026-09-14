---
type: entity
status: draft
title: AdaMAST
created: 2026-09-14
updated: 2026-09-14
tags: [agents, failure-taxonomy, feedback]
related: [2607.16387v2, AdaMAST-Judge, adaptive-failure-taxonomy, taxonomy-conditioned-consumer, online-failure-code-refinement]
source_id: p-72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
content_version: sha256:72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
sources: ["raw/sources/2607.16387v2.pdf"]
---
# AdaMAST

AdaMAST 是一个从执行轨迹中归纳目标特定失败分类体系的流程。它将同一分类体系作为反馈接口，用于 AdaEvolve 搜索、Claude Code 与 SWE-agent 的运行时监控，以及通过 [[entities/AdaMAST-Judge|AdaMAST-Judge]] 进行的轨迹选择。

该分类体系以 `A` 表示系统级失败、`B` 表示角色或阶段特定失败、`C` 表示领域推理失败。当架构或轨迹分布变化时，具体代码也会更新。

论文报告称，AdaMAST 在 Frontier-CS、OlympiadBench、MMLU-Pro、TheoremQA 和 DROP 上优于 LLM Guidance；但这些测量不能证明每个触发的代码都会导致特定改进（PDF pp. 1、17、37）。
