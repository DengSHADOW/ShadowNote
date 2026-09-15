---
type: entity
title: AutoGen
created: 2026-09-15
updated: 2026-09-15
tags: [多智能体系统, framework, AutoGen, 安全实验]
related: [Magentic-One, 多智能体系统控制流劫持, 智能体间元数据的信任边界]
source_id: p-5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11
content_version: sha256:5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11
sources: ["raw/sources/2503.12188v2.pdf"]
---
# AutoGen

AutoGen 是本文评估的开源多智能体 framework 之一。作者在接近默认配置下测试 Magentic-One、Selector 与 Round-Robin 三种 orchestration，并使用 orchestrator、file surfer、web surfer、coder 与 code executor 等 agent 配置。（PDF p. 6，§5；PDF p. 20，附录 E）

> **英文原文：** “For AutoGen, we tested three orchestrators: Magentic-One (MO), Selector (Sel.), and Round-Robin (RR).”（PDF p. 6，§5）

在 Web Redirect 场景中，AutoGen 多个组合报告较高 ASR，例如 Round-Robin 配合 GPT-4o-mini 为 100%。这些结果证明受测配置存在攻击路径，但每个组合为 10 次受控试验，不能直接代表所有 AutoGen 部署。（PDF p. 7，表 2；PDF p. 20–21，附录 E）

> **英文原文：** “Each (orchestrator-model-query-error) tuple is measured over 10 trials.”（PDF p. 7，表 2）

本文把 AutoGen 案例用于说明 [[多智能体系统控制流劫持|多智能体系统控制流劫持]]：不可信内容经 file 或 web agent 的输出影响后续协调和代码执行，而非表明 AutoGen 的所有配置必然不安全。（PDF p. 2–7，§1–6）

> **英文对应表述（非逐字原文）：** AutoGen is used as an experimental framework demonstrating a possible metadata-mediated control-flow attack path.

## 图谱关系

- 来源：[[2503.12188v2|Multi-Agent Systems Execute Arbitrary Malicious Code]]
- 协调器：[[Magentic-One]]
- 安全机制：[[多智能体系统控制流劫持]]、[[智能体间元数据的信任边界]]
