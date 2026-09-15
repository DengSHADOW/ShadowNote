---
type: concept
status: draft
source_id: p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
content_version: sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
title: Model–Harness Co-Learning
created: 2026-09-13
updated: 2026-09-13
tags: [online-learning, imitation-learning, process-reward, self-improvement]
related: [continual-harness, reset-free-adaptation, agentic-harness, Gemma-4, capability-floor]
sources: ["raw/sources/2605.09998v1.pdf"]
---

# Model–Harness Co-Learning

> 来源：[[2605.09998v1|Continual Harness]]；PDF pp. 4–5，7–8，26–28；Figures 2、7、19。

Model–harness co-learning 在两个时间尺度上同时更新 model weights 和 [[agentic-harness]]。每次 rollout 内，Refiner 改变 (H_t)；不同 iterations 之间，soft SFT 更新参数 (	heta_k)。

该来源的每个 online iteration 会在 Pokémon Red 中执行 256-step DAgger rollout。Pairwise PRM 对 trajectory progress、action correctness、reasoning quality 与 format compliance 打分；Gemini-3.1-pro 对低奖励 windows 重新标注，再用于三个 epochs 的 soft SFT，learning rate 为 (5	imes10^{-6})。

Figure 7 展示了五个有净进步的 runs，分别增加 2–6 个 milestones。这说明 [[Gemma-4]] student 能沿其自身 persistent trajectory 进步，但不能证明完全自主的 self-improvement，因为该循环使用 frontier teacher、外部 PRM 和人工设计的 training pipeline。

来源没有报告总 training jobs 数量或未进步 runs 的比例；PRM reward 也并非单调，且不总与 milestone signal 一致。
