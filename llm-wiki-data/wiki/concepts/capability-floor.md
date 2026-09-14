---
type: concept
status: draft
source_id: p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
content_version: sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
title: 自我改进智能体的能力下限
created: 2026-09-13
updated: 2026-09-13
tags: [model-capability, self-improvement, negative-results]
related: [continual-harness, model-harness-co-learning, agentic-harness]
sources: ["raw/sources/2605.09998v1.pdf"]
---

# 自我改进智能体的能力下限

> 来源：[[sources/2605.09998v1|Continual Harness]]；PDF p. 7 Figure 6，p. 10 Section 6。

能力下限指模型能够有效使用不断演化的 harness 所需的最低能力。低于该阈值时，添加 prompts、sub-agents、skills 和 memory 可能增加成本或认知负担，却不能改善执行。

在 Pokémon Emerald 中，[[continual-harness]] 对 Gemini 3.1 Pro 相比 minimalist baseline 呈 Pareto 优势；对 Flash 则存在较大波动。使用 Flash-Lite 时，minimalist harness 达到 20% completion，而 Continual Harness 的各变体仅为 3–13%。

这一发现反驳了“更多脚手架必然有益于所有模型”的简单假设。Harness 的价值取决于 format compliance、tool selection、component reuse，以及把环境反馈连接到真实行为改变的能力。
