---
type: concept
title: point-based HOTA
created: 2026-09-16
updated: 2026-09-16
tags: [tracking, evaluation, HOTA, grounding]
related: [2601.10611v4, Molmo2-Track, 身份保持的-point-tracking]
sources: ["2601.10611v4.pdf"]
---
# point-based HOTA

point-based HOTA 是 Molmo2 tracking 评测中的身份感知指标。它把预测点是否落在对应 segmentation mask 内作为二值相似度，再用 HOTA 框架衡量检测与关联质量。（PDF pp. 37–38，Appendix C）

> **英文对应表述（非逐字原文）：** Point-based HOTA uses whether a predicted point lies inside a segmentation mask as a binary similarity for detection and association evaluation.

与 J&F 相比，该指标不容易因粗粒度大 mask 获得高分，更直接对应 point 定位与跨帧身份一致性；它与 point F1、J&F 测量的性质不同，不能相互替代。（PDF pp. 37–38，Appendix C）

> **英文对应表述（非逐字原文）：** Point-based HOTA complements point F1 and J&F by emphasizing identity-aware association rather than mask overlap alone.

论文未充分说明重复点、多个预测点落入同一 mask、身份冲突等边界条件，因而复现时仍需核对正式评测实现。（PDF pp. 37–38，Appendix C）

> **英文对应表述（非逐字原文）：** The paper leaves some matching edge cases underspecified, including duplicate points and identity conflicts.

来源：[[2601.10611v4|Molmo2 论文来源页]]。应用 benchmark 为 [[Molmo2-Track]]，表示机制见[[身份保持的-point-tracking|身份保持的 point tracking]]。