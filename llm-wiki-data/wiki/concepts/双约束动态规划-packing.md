---
type: concept
title: 双约束动态规划 packing
created: 2026-09-16
updated: 2026-09-16
tags: [training, packing, optimization, efficiency]
related: [2601.10611v4, Molmo2, message-tree-encoding]
sources: ["2601.10611v4.pdf"]
---
# 双约束动态规划 packing

双约束动态规划 packing 同时优化文本 token 与视觉 crop 的填充率。常规 SFT 的约束是 `T ≤ 16384`、`I ≤ 128`，目标为最大化 `T + I × wi`，论文设置候选池 `M=48`、`wi=30`，并把 token 数量量化到最接近的 `32` 的倍数。（PDF pp. 28、31，Appendix B）

> **英文对应表述（非逐字原文）：** The packing problem maximizes a weighted combination of text tokens and image crops under separate capacity constraints.

long-context training 把容量扩展到最多 `36,864` tokens 和 `384` images。作者称候选池超过 `48` 后收益迅速递减，但未提供独立的端到端吞吐复现。（PDF p. 31，Appendix B）

> **英文对应表述（非逐字原文）：** Long-context training increases both capacities, while the authors report diminishing returns from candidate pools larger than 48.

该 packing 与 [[message-tree-encoding]]共同复用视觉输入；视频加载与抽帧仍是 DataLoader 的主要瓶颈。（PDF p. 31，Appendix B）

> **英文对应表述（非逐字原文）：** Packing works with message trees to reuse visual inputs, although video loading and frame extraction remain primary data-loading bottlenecks.

来源：[[2601.10611v4|Molmo2 论文来源页]]。