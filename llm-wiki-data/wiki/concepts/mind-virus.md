---
type: concept
title: mind virus
created: 2026-09-15
updated: 2026-09-15
tags: [llm, multi-agent-systems, security, propagation]
related: [virus-chain, SOUL-md, 防御提示, 连续性叙事操纵]
source_id: p-377e957a7fd25aefc56f62e702d6bf257d236814276e074e8e49cefd95121be0
content_version: sha256:377e957a7fd25aefc56f62e702d6bf257d236814276e074e8e49cefd95121be0
sources: ["raw/sources/2608.10218v1.pdf"]
---
# mind virus

mind virus 指被宿主智能体采纳后，会改变其行为以向其他智能体传播某种目标、意识形态或行动指令的思想模式；作者将随之出现的行为改变称为其 content。（PDF p.1–3，§1）

> **英文对应表述（非逐字原文）：** A mind virus is a pattern of goals or ideas that changes an agent’s behavior so that it attempts to propagate itself to other agents.

论文区分意识形态型与行动型载荷：前者主要试图改变价值判断或目标，后者试图诱导特定操作。二者都不应仅以表面文件感染或单次工具调用判定成功，而应分别考察内容保真、下游传播与实际行为后果。（PDF p.3–15）

> **英文对应表述（非逐字原文）：** Ideological and action payloads have distinct effects and require separate measurements of retention, propagation, and behavior.

## 图谱关系

- 来源：[[2608.10218v1|Mind Viruses]]
- 传播机制：[[virus-chain|virus chain]]、[[SOUL-md|SOUL.md]]
- 防御：[[防御提示]]
