---
type: concept
title: point-then-count
created: 2026-09-16
updated: 2026-09-16
tags: [counting, pointing, grounding, decoding]
related: [2601.10611v4, Molmo2-VideoPoint, 统一-point-based-grounding]
sources: ["2601.10611v4.pdf"]
---
# point-then-count

point-then-count 是先为每个目标生成空间或时空 point，再从 point 数量得到计数结果的方法。Molmo2 使用顺序 object index，使最后一个编号可以直接表达已定位对象的总数。（PDF pp. 5、27–28，§2，Appendix A）

> **英文对应表述（非逐字原文）：** Point-then-count first localizes target instances and then derives the count from the generated point sequence.

在 specialized 4B 消融中，direct count 在 BVC/MVC 上为 `61.3/28.1`，point-then-count 为 `61.5/34.5`；主要增益出现在更困难的视频计数设置。（PDF p. 13，Table 9）

> **英文对应表述（非逐字原文）：** A specialized 4B ablation reports similar image-counting performance but a substantial video-counting gain from point-then-count.

该方法提供可检查的中间定位结果，但仍可能因重复点、假阳性或漏检产生错误计数，因此不能把结构化输出本身视为计数正确性的保证。（PDF pp. 46–48、58，Appendix H，Figure 36）

> **英文对应表述（非逐字原文）：** The intermediate points improve inspectability, but duplicates, false positives, and missed instances can still produce incorrect counts.

来源：[[2601.10611v4|Molmo2 论文来源页]]。数据表示见 [[Molmo2-VideoPoint]] 与 [[统一-point-based-grounding]]。