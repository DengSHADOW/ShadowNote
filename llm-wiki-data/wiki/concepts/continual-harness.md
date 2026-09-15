---
type: concept
status: draft
source_id: p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
content_version: sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
title: Continual Harness
created: 2026-09-13
updated: 2026-09-13
tags: [agents, continual-learning, harness-refinement, embodied-agents]
related: [agentic-harness, reset-free-adaptation, model-harness-co-learning, capability-floor, create-and-forget-skill-funnel, schema-fragility]
sources: ["raw/sources/2605.09998v1.pdf"]
---

# Continual Harness

> 来源：[[2605.09998v1|Continual Harness]]；PDF pp. 1–10，Figures 1–8。

Continual Harness 是一种在线适应框架，会在连续 trajectory 中修改整个 [[agentic-harness]]。其状态为 (H=(p,G,K,M))，分别表示 system prompt、sub-agents、skills 与 persistent memory。

在 warm-up (W) 后，每隔 (F) 步，Refiner 会检查最近的 trajectory window，寻找 navigation loops、tool failures、stalled objectives 与 missed exploration；随后对四类 components 做 CRUD 修改，而不重置环境。

在 Pokémon Red 和 Emerald 上，效果依赖模型能力。使用 Gemini 3.1 Pro 时，它相对 minimalist harness 显著降低成本；使用 Flash-Lite 时，所有变体都劣于 baseline。因此 refinement 基础设施本身不保证性能提升。

其机制证据对 navigation skills 较强：演化出的 pathfinders 在同一 run 内接近 Dijkstra oracle。与此同时，[[create-and-forget-skill-funnel]] 表明整个过程仍然浪费资源，且只选择性修复一个很小的 working set。

该方法来自 *Continual Harness: Online Adaptation for Self-Improving Foundation Agents* 的 Sections 3–4 与 Appendices C–D。
