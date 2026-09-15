---
type: concept
status: draft
source_id: p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
content_version: sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
title: 工具调用智能体的模式脆弱性
created: 2026-09-13
updated: 2026-09-13
tags: [tool-use, schemas, failure-modes, feedback]
related: [continual-harness, agentic-harness, create-and-forget-skill-funnel]
sources: ["raw/sources/2605.09998v1.pdf"]
---

# 工具调用智能体的模式脆弱性

> 来源：[[2605.09998v1|Continual Harness]]；PDF pp. 16–21，Appendix B.3。

Schema fragility 是 agent 的意图无法匹配执行接口所要求精确 schema 的失败。一个在逻辑上合适的工具可能完全没有被使用，即使 agent 认为它正在执行。

在 [[Gemini-Plays-Pokemon]] 的 Power Plant case study 中，`fly_menu_navigator` 要求：

```text
buttons_to_press: ["tool"]
```

但 agent 生成的是：

```text
buttons_to_press: ["Down"]
```

Meta-harness 接口随后忽略了 `tools_to_call`，只向 emulator 发送 `Down`。Agent 重复同一 payload 842 次，共耗费 1,003 turns 才放弃错误假设。

该案例显示 feedback blindness：关于检查假设、避免 confirmation bias 的内部自述并不符合实际执行。可靠系统需要 schema validation、真实 tool execution 的确认，以及重复 state-action loops 的检测。
