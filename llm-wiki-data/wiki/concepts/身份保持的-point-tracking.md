---
type: concept
title: 身份保持的 point tracking
created: 2026-09-16
updated: 2026-09-16
tags: [tracking, identity, grounding, video]
related: [2601.10611v4, Molmo2-VideoTrack, Molmo2-Track, point-based-HOTA]
sources: ["2601.10611v4.pdf"]
---
# 身份保持的 point tracking

身份保持的 point tracking 通过在多个时间戳重复使用同一 object index，把离散空间点关联为对象轨迹。它不要求模型直接输出完整 segmentation mask，而是以带身份的 points 作为后续处理提示。（PDF pp. 27–28、37、54，Appendix A、C，Figure 30）

> **英文对应表述（非逐字原文）：** Identity-preserving point tracking links points across timestamps by reusing an object index, without requiring direct mask generation.

在 Molmo2 的评测链条中，带 ID points 会交给 SAM 2 生成 masks；因此 mask-based J&F 会受到 SAM 2 影响，而 [[point-based-HOTA]] 更直接评估检测与身份关联。（PDF pp. 37–38，Appendix C）

> **英文对应表述（非逐字原文）：** SAM 2 converts identity-tagged points into masks, so point-based HOTA more directly evaluates point detection and association than mask J&F.

长序列仍可能出现 point 漂移、identity switch、假阳性与漏检。Figure 36 的 penguin 样例漏掉多个目标，说明保持格式与编号不等于完整覆盖对象集合。（PDF p. 58，Figure 36）

> **英文对应表述（非逐字原文）：** Long tracks remain vulnerable to drift, identity errors, false positives, and missed objects.

来源：[[2601.10611v4|Molmo2 论文来源页]]。相关数据与 benchmark 为 [[Molmo2-VideoTrack]] 和 [[Molmo2-Track]]。