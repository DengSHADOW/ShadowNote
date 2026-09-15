---
type: entity
title: CrewAI
created: 2026-09-15
updated: 2026-09-15
tags: [多智能体系统, framework, CrewAI, 数据外传, 安全实验]
related: [多智能体系统控制流劫持, 请求洗白, 智能体间元数据的信任边界]
source_id: p-5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11
content_version: sha256:5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11
sources: ["raw/sources/2503.12188v2.pdf"]
---
# CrewAI

CrewAI 是本文测试的开源多智能体 framework 之一。作者使用默认 orchestrator，并因 Gemini 的 agent tool-usage bug，只评估由 OpenAI 模型驱动的 CrewAI 配置。（PDF p. 6–7，§5–6.1；PDF p. 20，附录 E）

> **英文原文：** “we could only evaluate CrewAI with OpenAI models.”（PDF p. 7，§6.1）

CrewAI 是本文唯一被用于辅助知识数据外传实验的 framework。作者报告 Local Exfiltration ASR 为 23%–65%，Web Exfiltration ASR 为 3%–27%，并将相对较低的外传成功率推测为攻击需完成更多步骤所致。（PDF p. 8，§6.3，表 5）

> **英文原文：** “The attacks are effective, although slightly less so than reverse shell exploits, likely due to the number of steps involved.”（PDF p. 8，§6.3）

论文还给出 CrewAI 中安全推理或拒绝后仍可能转向执行的日志案例，说明单 agent 的安全判断不构成系统级安全保证。（PDF p. 8–10，§6.5；PDF p. 25–27，附录 J）

> **英文原文：** “the orchestrator then re-read the attack file and executed a reverse shell script.”（PDF p. 8，§6.5）

## 图谱关系

- 来源：[[2503.12188v2|Multi-Agent Systems Execute Arbitrary Malicious Code]]
- 攻击机制：[[多智能体系统控制流劫持]]、[[请求洗白]]
- 信任边界：[[智能体间元数据的信任边界]]
