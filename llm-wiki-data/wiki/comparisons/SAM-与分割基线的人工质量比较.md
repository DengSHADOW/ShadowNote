---
type: comparison
title: SAM 与分割基线的人工质量比较
created: 2026-09-16
updated: 2026-09-16
tags: [human-evaluation, segmentation, benchmark-comparison]
related: [2304.02643v1 (1), SAM, ground-truth-independent-mask-quality-evaluation, 自动指标与人工感知质量错位]
sources: ["2304.02643v1 (1).pdf"]
---
# SAM 与分割基线的人工质量比较

## 单点分割

论文在 LVIS v0.5、VISOR、DRAM、IBD、NDD20、OVIS 和 iShape 上比较 RITM、single-output SAM、[[SAM]] 与 ground truth。每个数据集抽取 1000 个输入，并由专业标注员按有效对象、边界质量和提示一致性评分。（PDF pp. 23–25，§E）

> **英文对应表述（非逐字原文）：** The point-prompt study compares RITM, a single-output SAM variant, full SAM, and ground truth across seven segmentation datasets using human mask-quality ratings.

Table 8 中，SAM 相对 RITM 的 paired t-test p-values 均显著，10k-sample paired bootstrap 得到的 `99% CI` 均为正。SAM 相对 single-output SAM 的差值也均被报告为显著，为多输出歧义机制提供支持。（PDF pp. 25–26，Table 8）

> **英文对应表述（非逐字原文）：** Table 8 reports statistically significant advantages for SAM over RITM and the single-output variant across all seven point-prompt datasets.

OVIS 的 Figure 18 抽取数值与 Table 8 的方向冲突，因此该数据集的具体均值需要直接核对 PDF 图像；在核验前，只保留 Table 8 所报告的正差值区间 `CI99(∆µ)=(0.27, 0.63)`，不把抽取均值视为可靠定论。（PDF pp. 25–26，Figure 18 与Table 8）

> **英文对应表述（非逐字原文）：** The extracted OVIS means conflict with the positive difference reported in Table 8, so the figure labels require direct visual verification.

## Box-input instance segmentation

LVIS v1 实验使用 ground-truth boxes 比较 cascade ViTDet-H、SAM 和 ground truth。自动 AP 中 ViTDet-H 高于 SAM，但人工质量均值中 SAM 为 `8.1±0.07`，ViTDet-H 为 `7.9±0.08`；Table 8 给出的差值 `99% CI` 为 `(0.11, 0.42)`。（PDF p. 10，Table 5；PDF pp. 24–26，Figure 18 与Table 8）

> **英文对应表述（非逐字原文）：** ViTDet-H scores higher under LVIS AP, while SAM receives a higher mean human rating and a positive 99% confidence interval for the paired difference.

这一比较支持[[自动指标与人工感知质量错位]]，但不证明人工评分是无偏金标准。正式任务每个 mask 仅由一名标注员评分，且研究只覆盖七个单点数据集与一个 box-input 数据集。（PDF pp. 23–26，§E）

> **英文对应表述（非逐字原文）：** The study demonstrates a disagreement between benchmark and human rankings, but its single-rater production design and dataset coverage limit broader conclusions.

评估方法详见 [[ground-truth-independent-mask-quality-evaluation]]。