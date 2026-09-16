---
type: concept
title: tight modality fusion
created: 2026-09-16
updated: 2026-09-16
tags: [multimodal-learning, vision-language, feature-fusion]
related: [2303.05499v5 (1), Grounding-DINO, language-guided-query-selection]
sources: ["2303.05499v5 (1).pdf"]
---

# Tight modality fusion

Tight modality fusion 是 [[Grounding-DINO]] 的核心设计原则：把封闭集检测器划分为 neck、query initialization 和 head 三个阶段，并在三处都融合视觉与语言信息。（PDF pp. 2–3，Figure 2，§1）

> **英文原文：** “We conceptually divide a closed-set detector into three phases and propose a tight fusion solution.”

三个阶段分别对应 feature enhancer、[[language-guided-query-selection|language-guided query selection]] 和 cross-modality decoder。（PDF pp. 3、5–7，Figure 3，§3.1–§3.3）

> **英文原文：** “We design three feature fusion approaches in the neck, query initialization, and head phases.”

## 实验证据

在 O365、Swin-T 的消融设置中，移除 encoder fusion 使 LVIS zero-shot AP 从 `16.1` 降至 `13.1`；使用 static query selection 时为 `13.6`；移除 text cross-attention 时为 `14.3`。（PDF pp. 13–14，Table 7）

> **英文对应表述（非逐字原文）：** Under the O365 and Swin-T ablation setting, removing encoder fusion, replacing language-guided selection with static selection, or removing text cross-attention reduces LVIS zero-shot AP.

这些结果支持各融合位置在该配置中的贡献，但消融不是逐步累加设计，也没有重复试验或方差，因而不能完全分离模块交互或确认较小增益的稳定性。

> **英文对应表述（非逐字原文）：** The ablation supports the usefulness of the fusion locations in one configuration, but it does not isolate all interaction effects or establish the stability of small gains across repeated runs.