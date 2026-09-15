---
type: concept
title: 病毒方向 steering
created: 2026-09-15
updated: 2026-09-15
tags: [mechanistic-interpretability, steering, SAE, llm]
related: [mind-virus]
source_id: p-377e957a7fd25aefc56f62e702d6bf257d236814276e074e8e49cefd95121be0
content_version: sha256:377e957a7fd25aefc56f62e702d6bf257d236814276e074e8e49cefd95121be0
sources: ["raw/sources/2608.10218v1.pdf"]
---
# 病毒方向 steering

病毒方向 steering 是论文附录中的探索性设置：作者从 viral vector extraction 的问题集与行为表示中构造 `viral direction`，并在 Layer 16 注入该方向以影响智能体回答。（PDF p.72–73，§L.3–L.4）

> **英文对应表述（非逐字原文）：** The setup extracts a viral direction and injects it at Layer 16 to steer agent behavior.

作者称 Layer 16 的注入在两种模型中产生最一致的行为；其列出的 forward 与 reverse SAE feature 仅具有一般语义关联，不能据此将这些 feature 解释为传播行为的机制性原因或可靠防御指标。（PDF p.73，§L.4）

> **英文对应表述（非逐字原文）：** The SAE feature associations are exploratory and do not support a strong mechanistic conclusion.

## 图谱关系

- 来源：[[2608.10218v1|Mind Viruses]]
- 行为目标：[[mind-virus|mind virus]]
