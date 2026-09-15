---
type: entity
status: draft
source_id: p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
content_version: sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
title: Gemini Plays Pokémon
created: 2026-09-13
updated: 2026-09-13
tags: [research-project, embodied-agents, pokemon, Gemini]
related: [continual-harness, agentic-harness, schema-fragility, PokeAgent-Challenge]
sources: ["raw/sources/2605.09998v1.pdf"]
---

# Gemini Plays Pokémon

> 来源：[[2605.09998v1|Continual Harness]]；PDF pp. 1–2，6，14–21。

Gemini Plays Pokémon（GPP）是一个研究项目：Gemini models 通过不断演化的 harness 玩长程 Pokémon RPGs。

按作者说法，GPP 于 2025 年 5 月完成 Pokémon Blue、于 2025 年 8 月在 Yellow Legacy hard mode 中击败 Elite Four，并于 2025 年 11 月在 Pokémon Crystal 中完成全程且未输掉 end-game battle。它是否为首个完成多款 Pokémon RPG 的 AI system，并未在该来源内得到独立验证。

早期版本使用 human-authored specialists。自 Yellow Legacy 起，`define_agent`、`run_code` 和 notepad edits 等通用 meta-tools 允许模型构建 sub-agents 与 executable skills；该过程的人工 refinement 成为自动化 [[continual-harness]] 的经验先例。

GPP 还提供了 [[schema-fragility]] 的 Power Plant case study：一次错误 tool invocation 在相反环境反馈下重复了 842 次。
