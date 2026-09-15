---
type: entity
title: MetaGPT
created: 2026-09-15
updated: 2026-09-15
tags: [多智能体系统, framework, MetaGPT, Data-Interpreter, 安全实验]
related: [多智能体系统控制流劫持, 智能体间元数据的信任边界]
source_id: p-5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11
content_version: sha256:5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11
sources: ["raw/sources/2503.12188v2.pdf"]
---
# MetaGPT

MetaGPT 是本文评估的开源多智能体 framework 之一；作者使用 Data Interpreter agent system，并在 Jupyter notebook 中运行代码。（PDF p. 6，§5；PDF p. 20，附录 E）

> **英文原文：** “For MetaGPT, we use the Data Interpreter agent system, which runs code in a Jupyter notebook.”（PDF p. 20，附录 E）

在 Web Redirect 攻击中，MetaGPT Data Interpreter 的 ASR 随模型差异很大：GPT-4o 为 90%，GPT-4o-mini 为 88%，Gemini 1.5 Pro 为 14%，Gemini 1.5 Flash 为 2%。（PDF p. 7，表 2）

> **英文原文：** “MGPT DI 90% 88% 14% 2%.”（PDF p. 7，表 2）

这些结果与本文的 [[多智能体系统控制流劫持|多智能体系统控制流劫持]] 主张一致：风险取决于 framework、协调结构、模型和输入方式的组合，而不宜把某一数值概括为 MetaGPT 在全部部署中的风险率。（PDF p. 6–8，§5–6）

> **英文对应表述（非逐字原文）：** The measured vulnerability varies across tested model-and-system configurations and is not a deployment-wide risk estimate.

## 图谱关系

- 来源：[[2503.12188v2|Multi-Agent Systems Execute Arbitrary Malicious Code]]
- 攻击机制：[[多智能体系统控制流劫持]]
- 信任边界：[[智能体间元数据的信任边界]]
