---
type: concept
status: draft
source_id: p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
content_version: sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
title: Reset-Free Adaptation
created: 2026-09-13
updated: 2026-09-13
tags: [continual-learning, online-adaptation, embodied-agents]
related: [continual-harness, agentic-harness, model-harness-co-learning]
sources: ["raw/sources/2605.09998v1.pdf"]
---

# Reset-Free Adaptation

> 来源：[[sources/2605.09998v1|Continual Harness]]；PDF pp. 4–5，8，26–28。

Reset-free adaptation 指在不把环境返回初始状态的情况下更新 agent 或 harness。在 [[continual-harness]] 中，对 prompt、sub-agents、skills 与 memory 的更改会在同一 trajectory 的下一次决策中生效。

在 outer training loop 中，iteration (k) 结束时的 emulator state 成为 iteration (k+1) 的初始状态。因此游戏内位置与积累的经验得以保留，同时更新 model weights。

这种做法可处理只会在长动作序列后出现的 late-game failures。不过，该来源没有在相同 compute、数据和 teacher 使用条件下比较 reset-free 与 reset-based training。因此它支持可行性和进步，并不支持相对于 resets 的因果优越性。
