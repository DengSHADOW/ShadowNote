---
type: entity
title: WildDet3D-Data
created: 2026-09-16
updated: 2026-09-16
tags: [dataset, 3D-annotation, open-vocabulary, VLM, human-annotation]
related: [2604.08626v2 (1), WildDet3D, WildDet3D-Bench, 多模型候选-人工-VLM-混合-3D-标注]
sources: ["2604.08626v2 (1).pdf"]
---
# WildDet3D-Data

WildDet3D-Data 是从 COCO、LVIS、Objects365 和 V3Det 的既有 2D annotations 扩展而来的开放词汇 3D detection dataset。论文报告总计 `1,003,886 images`、`3,728,078 annotations` 和 `13,499 categories`。（PDF pp. 9–12，§3，Table 1）

> **英文对应表述（非逐字原文）：** WildDet3D-Data lifts large-vocabulary 2D annotations into metric 3D boxes across more than one million in-the-wild images.

## 数据组成

训练数据并非全部逐项经过人工验证：human train 包含 `102,979 images / 229,934 annotations`，VLM-filtered train 包含 `896,004 images / 3,483,292 annotations`；val 与 test 由人工标注。（PDF pp. 11–12，§3.3–3.4，Table 1）

> **英文对应表述（非逐字原文）：** The training set combines a smaller human-selected portion with a much larger automatically selected portion.

因此，“约一百万张人工验证图像”超过 Table 1 能直接支持的范围。更准确的表述是约 103K 张 human-annotated training images，加上约 896K 张 VLM-filtered training images。

> **英文对应表述（非逐字原文）：** Describing all one million images as human-verified obscures the distinction between manual and automatic selection.

## 标注方式

[[多模型候选-人工-VLM-混合-3D-标注]]先由 3D-MOOD、DetAny3D、SAM-3D、RANSAC-PCA 和 LabelAny3D 生成候选，再进行 translation/rotation optimization、规则过滤和人工或 VLM selection。（PDF pp. 9–12，§3.1–3.3，Figure 4）

> **英文对应表述（非逐字原文）：** Candidate diversity is obtained from five lifting methods, followed by geometric refinement and two alternative selection paths.

人工分支使用 Prolific，并设置 screening、gold tasks 与 candidate-quality ratings。自动分支使用 fine-tuned Molmo2 评价 category、scale、translation、shape、rotation 和 vertical tilt，保留总分大于 `10` 的最高分候选。（PDF pp. 11、30–31，§3.3，Appendix D）

> **英文对应表述（非逐字原文）：** Human workers inspect multi-view candidates, whereas Molmo2 assigns structured perceptual scores for automatic selection.

## 质量边界

人工 train subset 中，总体 rejection rate 为 `22.0%`；不同生成器差异显著。VLM score 与聚合 rejection bins 单调对应，但 `AUC=0.66`、point-biserial `r=0.30`，且 score `10` 仍有 `16.7%` rejection。（PDF pp. 12–13，§3.5，Table 2）

> **英文对应表述（非逐字原文）：** VLM scoring is useful for narrowing candidates but does not match the reliability of human verification.

GPT-4.1-mini 生成的物理尺寸范围、Qwen3.5-9B filters 和 Molmo2 selection 都可能继承模型偏差。标注者又主要来自英语西方国家，论文因此提示文化特定物体与非典型场景可能受到系统性筛选影响。（PDF pp. 31–32，Appendix D）

> **英文对应表述（非逐字原文）：** Model-derived priors and a demographically concentrated annotator pool may introduce category- and culture-dependent retention bias.

来源：[[2604.08626v2 (1)|WildDet3D 论文来源]]；该数据集用于训练 [[WildDet3D]]，其人工 validation subset 构成 [[WildDet3D-Bench]]。