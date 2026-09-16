---
type: concept
title: 非穷举 3D 标注下的 ignore-region suppression
created: 2026-09-16
updated: 2026-09-16
tags: [partial-annotation, ignore-region, federated-evaluation, loss-suppression]
related: [2604.08626v2 (1), WildDet3D, WildDet3D-Bench, 开放词汇单目-3D-目标检测]
sources: ["2604.08626v2 (1).pdf"]
---
# 非穷举 3D 标注下的 ignore-region suppression

在非穷举 3D 数据中，一些可见对象拥有 2D annotation，却因 depth 无效、严重遮挡、截断或位于相机后方而没有可靠 3D ground truth。若直接把这些区域视为背景，模型会因检测真实对象而受到负分类惩罚。（PDF pp. 8–9，§2.4）

> **英文对应表述（非逐字原文）：** Missing valid 3D boxes do not imply that the corresponding visible objects are background.

训练时，[[WildDet3D]]对与 ignore-annotated box 的 2D IoU 超过 `0.5` 的 prediction 抑制 negative classification loss。使用 2D IoU 是因为 ignore objects 本身缺少有效的 3D geometry。（PDF pp. 8–9，§2.4）

> **英文对应表述（非逐字原文）：** Negative loss is suppressed using 2D overlap because ignored objects cannot support reliable 3D matching.

评估时，与 ignore object 匹配的 prediction 既不计 true positive，也不计 false positive；ignore ground truth 也不产生 false negative。[[WildDet3D-Bench]]的 text-prompt protocol 进一步采用 federated evaluation。（PDF pp. 9、14、30，§2.4，§4.1，Appendix C）

> **英文对应表述（非逐字原文）：** Neutral matching keeps known annotation gaps from inflating either false positives or false negatives.

Omni3D ablation 中移除该机制仅降低 `0.2 AP`。论文推测在部分 3D 标注更常见的 WildDet3D-Bench 上作用可能更大，但没有提供对应消融，因此这一外推尚未被直接验证。（PDF pp. 17–18，§4.6，Table 8）

> **英文对应表述（非逐字原文）：** The measured Omni3D effect is small, and a larger benefit under heavier annotation incompleteness remains a hypothesis.

来源：[[2604.08626v2 (1)|WildDet3D 论文来源]]。