---
type: entity
title: Magentic-One
created: 2026-09-15
updated: 2026-09-15
tags: [多智能体系统, orchestrator, AutoGen, task-ledger, 安全实验]
related: [AutoGen, 多智能体系统控制流劫持, agentic-harness]
source_id: p-5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11
content_version: sha256:5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11
sources: ["raw/sources/2503.12188v2.pdf"]
---
# Magentic-One

Magentic-One 是本文在 AutoGen 中测试的 orchestrator 之一，属于“central orchestrator with external data structures”拓扑：其通过外部 task ledger 循环配合动态中央协调，以保持系统任务对齐。（PDF p. 20–22，附录 E–F）

> **英文原文：** “combine dynamic central orchestration with an external task ledger loop to ensure that the MAS is on-task.”（PDF p. 22，附录 F）

在作者的 Web Redirect 实验中，Magentic-One 的 ASR 为 GPT-4o 58%、GPT-4o-mini 88%、Gemini 1.5 Pro 88%、Gemini 1.5 Flash 33%；本地文件攻击中，GPT-4o 与 Gemini 1.5 Pro 均为 97%。（PDF p. 7，表 2–3）

> **英文原文：** “MO 58% 88% 88% 33%.”（PDF p. 7，表 2）

task ledger 旨在增强任务完成能力，但本文结果表明，外部任务结构本身不等于可信来源或安全执行策略；对来自不可信输入派生的 metadata 仍需建立独立的权限和验证机制。（PDF p. 4–5，§2–4；PDF p. 21–22，附录 F）

> **英文对应表述（非逐字原文）：** A task ledger can support task tracking, but it does not by itself establish provenance or authorization for metadata-driven actions.

## 图谱关系

- 来源：[[2503.12188v2|Multi-Agent Systems Execute Arbitrary Malicious Code]]
- 所属框架：[[AutoGen]]
- 安全机制：[[多智能体系统控制流劫持]]、[[agentic-harness|Agentic Harness]]
