---
type: entity
status: draft
source_id: p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
content_version: sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
title: Gemma-4
created: 2026-09-13
updated: 2026-09-13
tags: [foundation-model, open-source-model, training]
related: [model-harness-co-learning, continual-harness, capability-floor]
sources: ["raw/sources/2605.09998v1.pdf"]
---

# Gemma-4

> 来源：[[sources/2605.09998v1|Continual Harness]]；PDF pp. 7–8，25–28；Figure 19。

Gemma-4 是 [[model-harness-co-learning]] 中作为 student 使用的 open-source model family。该来源评估了 E2B、E4B、26B MoE 和 31B dense 版本。

Supervised fine-tuning 使用 Gemini-3.1-pro trajectories、`r=256` 与 `α=256` 的 LoRA、bf16 precision、8K-token context、Unsloth 和 H200 GPUs；随后进行 offline GRPO，再在 Pokémon Red 中进行 reset-free online training。

Warm-up checkpoints 主要改善 tool formatting 与 action-quality metrics，并未单独带来 milestone progression。在线过程使用 Gemini-3.1-pro 作为 teacher，因为所评估的 Gemma-4 models 不足以同时担任 agent 与 Refiner/teacher。

该来源对 Red initial policy 存在不一致：Section D.2 指定 31B SFT，Section D.4 则写为 26B SFT，尽管相应的 26B adapter 之前被描述为 degenerate。
