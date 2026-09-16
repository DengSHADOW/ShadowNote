---
type: concept
title: modal–amodal 标注错位
created: 2026-09-16
updated: 2026-09-16
tags: [annotation, evaluation-bias, instance-segmentation]
related: [2304.02643v1 (1), SAM, 自动指标与人工感知质量错位]
sources: ["2304.02643v1 (1).pdf"]
---
# modal–amodal 标注错位

modal–amodal 标注错位指模型输出可见区域的 modal mask，而 benchmark ground truth 按不可见部分补全或禁止内部孔洞，形成 amodal 标注时产生的评价差异。两者可以分别符合不同对象定义，低 IoU 不必然意味着模型边界在视觉上无效。（PDF p. 22，§D.4）

> **英文对应表述（非逐字原文）：** A visually valid modal mask can disagree with an amodal benchmark annotation that completes occluded regions or disallows holes.

论文以 LVIS 中的 plate 为例：[[SAM]] 输出其可见区域，而 LVIS 的标注规则产生无孔洞的 amodal ground truth。该差异可以降低自动 AP，却未必降低人对对象有效性和边界质量的判断。（PDF p. 22，§D.4）

> **英文对应表述（非逐字原文）：** In the LVIS plate example, SAM segments the visible region while the dataset annotation follows an amodal convention, creating a benchmark mismatch.

这一现象是[[自动指标与人工感知质量错位]]的具体来源之一，但不能解释所有性能差异；类别覆盖、候选框质量、排序和边界误差仍可能独立影响 AP。（PDF pp. 9–10、22–26，§5.4、§D.4、§E）

> **英文对应表述（非逐字原文）：** Modal–amodal mismatch explains part, but not all, of the disagreement between benchmark AP and human judgments.