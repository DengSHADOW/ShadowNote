---
type: concept
status: draft
source_id: p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
content_version: sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
title: Agentic Harness
created: 2026-09-13
updated: 2026-09-13
tags: [agents, scaffolding, tools, memory]
related: [continual-harness, reset-free-adaptation, model-harness-co-learning]
sources: ["raw/sources/2605.09998v1.pdf"]
---

# Agentic Harness

> 来源：[[sources/2605.09998v1|Continual Harness]]；PDF pp. 3–4，Sections 2.2–3.1。

Agentic harness 是 foundation model 与环境之间的脚手架层。该来源将其分解为：

```text
H = (p, G, K, M)
```

- `p`：system prompt 与策略指令。
- `G`：专门化 sub-agents。
- `K`：可复用的文本级或可执行 skills。
- `M`：保存事实、策略与观察的 persistent memory。

Minimalist harness 只提供画面、局部 ASCII 地图、按键动作和通用 prompt；expert harness 还提供人工编写的 sub-agents、A* pathfinding、type chart、damage calculator 与 curated objectives。[[continual-harness]] 从前一类条件开始，在线构建额外 components。

这种分解把优化对象扩展到 prompt optimization 之外：agent 的行为取决于所有 components 的交互，以及它们是否真的在执行时被检索或调用。
