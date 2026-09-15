---
type: entity
title: OpenClaw
created: 2026-09-15
updated: 2026-09-15
tags: [agent-system, multi-agent-systems, experiment]
related: [SOUL-md, mind-virus, 防御提示]
source_id: p-377e957a7fd25aefc56f62e702d6bf257d236814276e074e8e49cefd95121be0
content_version: sha256:377e957a7fd25aefc56f62e702d6bf257d236814276e074e8e49cefd95121be0
sources: ["raw/sources/2608.10218v1.pdf"]
---
# OpenClaw

OpenClaw 是论文用于部分编码智能体与防御提示实验的智能体环境。作者在其默认 soul 末尾附加 mind virus warning，并以此测试显式自传播载荷在 Claude Haiku 4.5 上的跨 hop 传播。（PDF p.33，§C）

> **英文对应表述（非逐字原文）：** OpenClaw provides the default soul context to which the evaluated mind-virus warning was appended.

论文中的 OpenClaw 结果属于特定模型、工具与实验协议下的测量，不应直接外推为其他智能体框架的普遍传播率或防护效果。（PDF p.31–34，§B–C）

> **英文对应表述（非逐字原文）：** The reported OpenClaw results are specific to the evaluated models, tools, and experimental protocol.

## 图谱关系

- 来源：[[2608.10218v1|Mind Viruses]]
- 配置与风险：[[SOUL-md|SOUL.md]]、[[mind-virus|mind virus]]
- 防御实验：[[防御提示]]
