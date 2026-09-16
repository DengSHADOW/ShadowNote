---
type: entity
title: Molmo2-VideoTrack
created: 2026-09-16
updated: 2026-09-16
tags: [dataset, video-tracking, grounding, open-vocabulary]
related: [2601.10611v4, Molmo2, Molmo2-Track, 身份保持的-point-tracking]
sources: ["2601.10611v4.pdf"]
---
# Molmo2-VideoTrack

Molmo2-VideoTrack 是 Molmo2 的开放词汇视频 tracking 训练数据集。Table 21 将其统计为 `6,624` clips、`25,437` tracks 和 `29,704` queries，数据来源覆盖通用场景、体育、自动驾驶、动物、UAV、人物与舞蹈。（PDF pp. 42–45，Table 21）

> **英文对应表述（非逐字原文）：** Molmo2-VideoTrack contains 6,624 clips, 25,437 tracks, and 29,704 queries drawn from diverse tracking domains.

部分原始 bounding-box tracks 通过 SAM 2 转为 masks；若 mask 与 box 的 IoU 过低或超过 `20%` 的 mask 位于 box 外，流程会重新 prompt，平均 IoU 低于 `0.5` 的 track 会被过滤。人工 query 验证后平均保留约 `70%`。（PDF p. 44，Appendix F）

> **英文对应表述（非逐字原文）：** Bounding-box tracks are converted with SAM 2 and filtered using box–mask consistency checks, followed by human query validation.

训练表示在不同时间戳复用同一 object index，以支持[[身份保持的-point-tracking|身份保持的 point tracking]]。tracking 与 pointing 联合训练的 specialized 消融优于仅 tracking 设置，但结论限于作者的 4B 配方。（PDF pp. 13、27–28，Table 10，Appendix A）

> **英文对应表述（非逐字原文）：** Reused object indices preserve identity across timestamps, and a specialized ablation reports gains from combining tracking with pointing data.

来源：[[2601.10611v4|Molmo2 论文来源页]]。评测集见 [[Molmo2-Track]]。