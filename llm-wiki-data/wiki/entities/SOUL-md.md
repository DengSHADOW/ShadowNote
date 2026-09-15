---
type: entity
title: SOUL.md
created: 2026-09-15
updated: 2026-09-15
tags: [persistent-memory, system-prompt, agent-configuration, security]
related: [mind-virus, virus-chain, 防御提示, 连续性叙事操纵]
source_id: p-377e957a7fd25aefc56f62e702d6bf257d236814276e074e8e49cefd95121be0
content_version: sha256:377e957a7fd25aefc56f62e702d6bf257d236814276e074e8e49cefd95121be0
sources: ["raw/sources/2608.10218v1.pdf"]
---
# SOUL.md

`SOUL.md` 是论文实验中可被智能体修改、并会进入后续系统提示或行为上下文的持久化文件。其同时具备跨上下文保留和高优先级行为影响两种属性，因此构成比普通文件更强的传播面。（PDF p.14–15）

> **英文对应表述（非逐字原文）：** `SOUL.md` is a modifiable persistent file incorporated into later agent context, making it a stronger propagation surface than ordinary files.

实验中，`SOUL.md` 感染者的后续感染成功率为 55%，仅其他文件感染者为 17%。这是该论文特定受控环境中的相关结果，不足以单独证明所有系统中该文件类型的因果效应。（PDF p.15，Table 3）

> **英文对应表述（非逐字原文）：** In the reported controlled experiment, soul-infected agents had 55% subsequent infection success, compared with 17% for file-only infection.

## 图谱关系

- 来源：[[2608.10218v1|Mind Viruses]]
- 传播机制：[[mind-virus|mind virus]]、[[virus-chain|virus chain]]
- 防御配置：[[防御提示]]
