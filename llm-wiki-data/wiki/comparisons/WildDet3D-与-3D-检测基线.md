---
type: comparison
title: WildDet3D 与 3D 检测基线
created: 2026-09-16
updated: 2026-09-16
tags: [comparison, 3D-detection, benchmark, baseline]
related: [2604.08626v2 (1), WildDet3D, WildDet3D-Bench, 开放词汇单目-3D-目标检测]
sources: ["2604.08626v2 (1).pdf"]
---
# WildDet3D 与 3D 检测基线

## 同训练数据比较

在 [[WildDet3D-Bench]] 的 Omni3D-only text setting 中，[[WildDet3D]]为 `6.8 AP`，3D-MOOD 为 `2.3 AP`；Omni3D-only box setting 中，WildDet3D 为 `8.4 AP`，OVMono3D-LIFT 为 `7.7 AP`。（PDF pp. 14–15，§4.2，Table 3）

> **英文对应表述（非逐字原文）：** Under the reported Omni3D-only settings, WildDet3D outperforms the text and box baselines on the in-the-wild benchmark.

在 Omni3D 主 benchmark 上，text-prompt WildDet3D 为 `34.2 AP3D`，3D-MOOD Swin-B 为 `30.0`；box-prompt WildDet3D 为 `36.4`，DetAny3D 为 `34.4`，OVMono3D-LIFT 为 `29.6`。（PDF pp. 15–16，§4.3，Table 4）

> **英文对应表述（非逐字原文）：** WildDet3D reports the highest aggregate Omni3D AP among the listed methods in both prompt modes.

## 不同训练数据比较

WildDet3D 在加入 `Others + WildDet3D-Data` 后，从 `6.8` 提升至 `22.6 AP`（text），从 `8.4` 提升至 `24.8 AP`（box）。由于两组数据同时加入，该增益不能只归因于 [[WildDet3D-Data]]。（PDF pp. 14–15，§4.1–4.2，Table 3）

> **英文对应表述（非逐字原文）：** The expanded mixture improves performance, but the experiment does not isolate WildDet3D-Data from the supplementary datasets.

## 训练效率表述

论文将 WildDet3D 的 12 epochs 与基线的 80–120 epochs 对比；然而 WildDet3D 使用 SAM 3 与 LingBot-Depth initialization，epoch 样本量和训练计算也未归一化。可支持的结论是训练日程更短，而非总成本必然低 `6–10×`。（PDF pp. 15、29，§4.3，Appendix B）

> **英文对应表述（非逐字原文）：** Epoch counts favor WildDet3D, but they are not a compute-normalized comparison.

## 结论边界

这些结果均为作者报告，未提供显著性区间、多随机种子统计或独立复现。不同 prompt mode、training mixture、depth condition 和 matching metric 应分别解释，不能只按 AP 数值横向合并。

> **英文对应表述（非逐字原文）：** Comparisons remain conditional on the reported training data, prompt interface, depth input, and evaluation protocol.

来源：[[2604.08626v2 (1)|WildDet3D 论文来源]]。