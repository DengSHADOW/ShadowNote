---
type: concept
title: sub-sentence level text representation
created: 2026-09-16
updated: 2026-09-16
tags: [text-representation, attention-mask, vision-language]
related: [2303.05499v5 (1), Grounding-DINO, grounded-pre-training]
sources: ["2303.05499v5 (1).pdf"]
---

# Sub-sentence level text representation

Sub-sentence level text representation 是 Grounding DINO 用于处理类别名称 prompt 的文本表示方式。它通过 attention mask 阻断互不相关类别名称之间的注意力，同时保留 per-word feature。（PDF pp. 6–8，Figure 4，§3.4）

> **英文原文：** “We introduce attention masks to block attentions among unrelated category names, named ‘sub-sentence’ level representation.”

该方法位于 sentence-level 与 word-level 表示之间：它避免把整个句子压缩成单个特征，也避免随机拼接的类别名称在 self-attention 中形成无意义依赖。（PDF pp. 7–8，§3.4）

> **英文原文：** “Word level representation enables encoding multiple category names with one forward but introduces unnecessary dependencies among categories.”

在 O365、Swin-T 的消融中，full model 的 LVIS zero-shot AP 为 `16.1`，改用 word-level text prompt 后为 `15.6`，对应 `0.5 AP` 差值；COCO zero-shot 与 fine-tune 的差值均为 `0.3 AP`。（PDF pp. 13–14，Table 7）

> **英文对应表述（非逐字原文）：** Replacing the sub-sentence prompt with a word-level prompt reduces LVIS zero-shot AP by 0.5 and both COCO metrics by 0.3 in the reported ablation.

该结果与方法有效相符，但只有单一训练配置和单点指标，尚不足以判断其对不同 prompt 顺序、长度或语言表达的稳健性。

> **英文对应表述（非逐字原文）：** The single-configuration ablation is consistent with a benefit, but it does not establish robustness across prompt ordering, length, or linguistic variation.