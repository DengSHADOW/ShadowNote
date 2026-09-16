---
type: concept
title: “bag of patches”组合语义失败
created: 2026-09-16
updated: 2026-09-16
tags: [视觉推理, 组合语义, failure-mode, LLaVA]
related: [2304.08485v2, LLaVA, LLaVA-Bench, GPT-4-as-judge-多模态评估]
sources: ["2304.08485v2.pdf"]
---
# “bag of patches”组合语义失败

“bag of patches”组合语义失败指模型识别到多个局部视觉元素，却没有正确建模它们之间的关系，因而把共现对象错误组合为不存在的复合概念。（PDF p. 7，§5.1）

> **英文原文：** “LLaVA perceives the image as a ‘bag of patches’, failing to grasp the complex semantics within the image.”

## 论文案例

在 [[LLaVA-Bench]] (In-the-Wild) 的冰箱图像中，画面同时含有草莓、普通酸奶和蓝莓味酸奶。[[LLaVA]] 在被问及是否存在草莓味酸奶时回答“是”，把独立出现的草莓和酸奶组合成了一个错误属性关系。（PDF pp. 7–8，§5.1，Table 6）

> **英文原文：** “It responds with yes when asked if strawberry-flavored yogurt is present, even though the fridge contains only yogurt and strawberries.”

## 解释边界

该案例表明局部对象识别成功不等于关系理解成功，但单个示例不能确定错误源自 CLIP 表征、线性 projection、Vicuna 解码，还是训练数据中的共现偏差。论文没有通过组件消融隔离这些原因。

> **英文对应表述（非逐字原文）：** The example demonstrates a compositional error, but the paper does not isolate which model component causes it.

这种失败与普通视觉幻觉有交集，但更具体：问题不一定是凭空生成对象，而是把真实可见对象之间的属性、归属或空间关系组合错误。