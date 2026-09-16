---
type: concept
title: ground-truth-independent mask quality evaluation
created: 2026-09-16
updated: 2026-09-16
tags: [human-evaluation, mask-quality, segmentation]
related: [2304.02643v1 (1), SAM, 歧义感知多掩码预测, 自动指标与人工感知质量错位]
sources: ["2304.02643v1 (1).pdf"]
---
# ground-truth-independent mask quality evaluation

ground-truth-independent mask quality evaluation 是不以数据集 ground truth 的 IoU 为直接评分依据、而由人判断 mask 质量的评估方法。论文要求标注员检查三个方面：是否构成有效对象、边界是否干净、是否与 point 或 box 提示一致。（PDF pp. 23–24，§E）

> **英文对应表述（非逐字原文）：** Raters judge whether a mask depicts a valid object, has clean boundaries, and agrees with the supplied point or box prompt without directly comparing it to dataset IoU.

point prompt 可合理对应包含该点的 whole、part 或 subpart；box prompt 则应对应与框尺度最匹配的对象。遮挡前景可以统一包含或排除，但同一边界中不一致地混合处理会被视为错误。（PDF pp. 23–24，§E）

> **英文对应表述（非逐字原文）：** Point prompts permit whole, part, or subpart interpretations, while box prompts favor the object matching the box scale; occlusion handling should remain internally consistent.

七个单点数据集各包含 1000 个输入和 4000 个评分任务；LVIS v1 box-input 实验包含 1000 个输入和 3000 个任务。前期五人重复评分的平均标准差为 `0.83`，正式实验每个任务由一人评分，平均耗时 `90 seconds`。（PDF pp. 24–25，§E）

> **英文对应表述（非逐字原文）：** The study scales to thousands of rating tasks after a five-rater pilot, but each production task is scored by only one rater.

Table 8 显示 [[SAM]] 相对 RITM、single-output SAM 和 ViTDet-H 的评分优势均达到统计显著。该结果支持[[歧义感知多掩码预测]]，但单标注员设计和有限数据集覆盖限制了结论的外推范围。（PDF pp. 25–26，Table 8）

> **英文对应表述（非逐字原文）：** Statistical comparisons favor SAM over the evaluated baselines, although single-rater production scoring and limited dataset coverage constrain generalization.