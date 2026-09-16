---
type: entity
title: Molmo2
created: 2026-09-16
updated: 2026-09-16
tags: [VLM, video-understanding, grounding, open-model]
related: [2601.10611v4, 统一-point-based-grounding, point-then-count, Molmo2-Track]
sources: ["2601.10611v4.pdf"]
---
# Molmo2

Molmo2 是由 Allen Institute for AI 与 University of Washington 提出的 VLM 家族，包括 Molmo2-4B、Molmo2-8B 和基于 OLMo 3 的 Molmo2-O-7B。它统一支持单图、多图和视频 QA、captioning、counting、pointing 与 tracking。（PDF pp. 1–3，摘要与 §1）

> **英文对应表述（非逐字原文）：** Molmo2 is a VLM family comprising 4B, 8B, and OLMo 3-based 7B variants for image, multi-image, and video tasks.

模型以 ViT—connector—LLM 为基本架构，并通过[[统一-point-based-grounding|统一 point-based grounding]]输出时间、对象 ID 和二维坐标。三阶段训练依次为 image-only pre-training、联合 SFT 与 long-context SFT。（PDF pp. 6–8，§3）

> **英文对应表述（非逐字原文）：** Its ViT–connector–LLM architecture uses a shared grounding representation and a three-stage training procedure.

Molmo2-8B 的 overall preference Elo 为 `1057`；Molmo2-4B 与 Molmo2-8B 的 video-pointing F1 分别为 `39.9` 和 `38.4`。这些结果需结合 baseline prompt、输入方式及 SAM 2 后处理差异解释。（PDF pp. 9、33–37，Tables 3、15）

> **英文对应表述（非逐字原文）：** Molmo2 reports competitive preference and video-pointing results, although evaluation conditions differ across model families.

来源：[[2601.10611v4|Molmo2 论文来源页]]。相关任务与评测见 [[Molmo2-Track]]、[[point-based-HOTA]] 和 [[query-conditioned-SlowFast-encoding]]。