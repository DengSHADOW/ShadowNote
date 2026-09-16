---
type: concept
title: message-tree encoding
created: 2026-09-16
updated: 2026-09-16
tags: [training, packing, efficiency, multimodal]
related: [2601.10611v4, Molmo2, 双约束动态规划-packing]
sources: ["2601.10611v4.pdf"]
---
# message-tree encoding

message-tree encoding 把共享视觉输入作为根消息，并把针对同一视觉输入的多条 QA 标注编码为互不 cross-attend 的分支。这样可以复用视觉计算，同时避免不同答案分支相互泄漏。（PDF pp. 7–8、28–31，§3.2，Appendix B）

> **英文对应表述（非逐字原文）：** Message-tree encoding places shared visual content at the root and represents multiple QA annotations as branches that do not cross-attend.

论文把该机制与[[双约束动态规划-packing|双约束动态规划 packing]]结合使用，以提高异构多模态样本的训练吞吐。Table 13 区分 `visual`、`anno.` 与格式化后的 `ex.`，表明原始视觉项、标注数和训练 example 数不能互换。（PDF pp. 30–31，Table 13）

> **英文对应表述（非逐字原文）：** Message trees are combined with packing, and the paper distinguishes visual items, annotations, and formatted training examples as separate counting units.

来源：[[2601.10611v4|Molmo2 论文来源页]]，模型见 [[Molmo2]]。