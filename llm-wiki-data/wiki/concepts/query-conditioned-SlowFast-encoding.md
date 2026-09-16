---
type: concept
title: query-conditioned SlowFast encoding
created: 2026-09-16
updated: 2026-09-16
tags: [video, frame-selection, test-time-scaling, efficiency]
related: [2601.10611v4, Molmo2, 统一-point-based-grounding]
sources: ["2601.10611v4.pdf"]
---
# query-conditioned SlowFast encoding

query-conditioned SlowFast encoding（`SF-query`）保留常规 slow-path 视频表示，并依据用户 query 选择额外的 fast-path 帧，以在视觉 token 预算内增加时间覆盖。（PDF pp. 39–40，Figure 7，Table 20）

> **英文对应表述（非逐字原文）：** SF-query combines a slow representation with query-selected fast frames to expand temporal coverage under a limited visual-token budget.

在未经 long-context training 的 Molmo2-8B 上，`SF-query` 使用 `10.7k` visual tokens 得到 `65.7` long-QA average；`224 frames` 使用 `18.6k` tokens 得到 `65.6`，前者减少约 `42.5%` 的视觉 token。（PDF pp. 39–40，Table 20）

> **英文对应表述（非逐字原文）：** SF-query reaches 65.7 long-QA average with 10.7k visual tokens, compared with 65.6 using 18.6k tokens for 224 frames.

该结果只表明论文评测集上的效率—性能平衡。query embedding 相似度较低但对因果或时序推理关键的帧是否会被遗漏，仍未得到系统评估。（PDF pp. 39–40，Table 20）

> **英文对应表述（非逐字原文）：** The evaluation does not establish whether query-based selection can miss temporally crucial frames with low surface-level query similarity.

来源：[[2601.10611v4|Molmo2 论文来源页]]，模型见 [[Molmo2]]。