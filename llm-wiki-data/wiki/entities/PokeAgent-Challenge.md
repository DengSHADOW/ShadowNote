---
type: entity
status: draft
source_id: p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
content_version: sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
title: PokeAgent Challenge
created: 2026-09-13
updated: 2026-09-13
tags: [benchmark, embodied-agents, pokemon, evaluation]
related: [continual-harness, agentic-harness, Gemini-Plays-Pokemon]
sources: ["raw/sources/2605.09998v1.pdf"]
---

# PokeAgent Challenge

> 来源：[[sources/2605.09998v1|Continual Harness]]；PDF pp. 3，9。

PokeAgent Challenge 是 embodied RPG agents 的 benchmark，也是该来源所用 canonical milestone ordering 的出处。

评测计算达到每个 milestone 前的累计 button presses。一次输出 `[A, A, DOWN]` 的调用记为三次 presses，使批量发出动作的 harness 能与 minimalist harness 在同一单位下比较。

该 benchmark 的 expert harness 包含人工编写的 sub-agents、A* pathfinding、type chart、damage calculator 和 curated objectives。[[continual-harness]] 将其视为人工设计 scaffolding 的上界，但并未获得相同的 domain-specific components。
