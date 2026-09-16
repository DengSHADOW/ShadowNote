---
type: entity
title: Molmo2-Track
created: 2026-09-16
updated: 2026-09-16
tags: [benchmark, video-tracking, segmentation, grounding]
related: [2601.10611v4, Molmo2, Molmo2-VideoTrack, point-based-HOTA]
sources: ["2601.10611v4.pdf"]
---
# Molmo2-Track

Molmo2-Track 是开放词汇视频 tracking benchmark，包含 `1,386` clips、`3,062` tracks 和 `3,147` queries，来源包括 APTv2、PersonPath、SportsMOT、DanceTrack 与 SAM-V。（PDF p. 45，Table 21）

> **英文对应表述（非逐字原文）：** Molmo2-Track is an open-vocabulary video-tracking benchmark with 1,386 clips, 3,062 tracks, and 3,147 queries.

Molmo2-4B、Molmo2-8B 与 Molmo2-O-7B 的 overall J&F 分别为 `56.7`、`56.2` 和 `53.7`。API 与 generic VLM 的 boxes、Molmo2 的带 ID points 都会通过 SAM 2 转为 masks，因此 J&F 同时测量模型输出与后处理链条。（PDF pp. 10、37，Table 5，Appendix C）

> **英文对应表述（非逐字原文）：** Molmo2 variants lead the reported overall J&F scores, but the metric also reflects SAM 2 conversion from model-produced boxes or points.

该 benchmark 同时报告 point F1 与 [[point-based-HOTA]]，分别侧重定位检测与身份关联。粗粒度大 mask 可能获得较高 J&F，却不一定表示 point 定位精确或 object identity 稳定。（PDF pp. 37–38，Appendix C）

> **英文对应表述（非逐字原文）：** Point F1 and point-based HOTA complement J&F by testing localization and identity consistency more directly.

来源：[[2601.10611v4|Molmo2 论文来源页]]。训练数据见 [[Molmo2-VideoTrack]]。