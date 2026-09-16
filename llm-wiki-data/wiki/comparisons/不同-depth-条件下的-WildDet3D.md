---
type: comparison
title: 不同 depth 条件下的 WildDet3D
created: 2026-09-16
updated: 2026-09-16
tags: [comparison, depth, monocular, stereo, RGBD]
related: [2604.08626v2 (1), WildDet3D, 可选深度的双编码器融合, WildDet3D-Bench]
sources: ["2604.08626v2 (1).pdf"]
---
# 不同 depth 条件下的 WildDet3D

[[WildDet3D]]使用同一[[可选深度的双编码器融合]]架构处理无 depth、partial/sparse depth、ground-truth depth 和 real stereo depth，但这些条件的传感器误差、覆盖率与现实可获得性不同。（PDF pp. 3–6、14–18，Figures 2–3，§4.2–4.6）

> **英文对应表述（非逐字原文）：** A shared architecture accepts several depth regimes, but each regime represents a different level of geometric information and deployment realism.

| Evaluation | Prompt | 无 depth | 有 depth | depth 条件 |
|---|---|---:|---:|---|
| WildDet3D-Bench，Omni3D training | Text | 6.8 AP | 20.7 AP | Ground-truth depth |
| WildDet3D-Bench，full training | Text | 22.6 AP | 41.6 AP | Ground-truth depth |
| WildDet3D-Bench，Omni3D training | Box | 8.4 AP | 23.9 AP | Ground-truth depth |
| WildDet3D-Bench，full training | Box | 24.8 AP | 47.2 AP | Ground-truth depth |
| Omni3D | Text | 34.2 AP | 41.6 AP | Sparse depth |
| Omni3D | Box | 36.4 AP | 45.8 AP | Sparse depth |
| Argoverse 2 zero-shot | Text | 40.3 ODS | 40.4 ODS | Ground-truth depth |
| ScanNet zero-shot | Text | 48.9 ODS | 50.2 ODS | Ground-truth depth |
| Stereo4D zero-shot | Box | 7.5 AP | 27.7 AP | Real stereo depth |

数据来自 PDF pp. 15–17 的 Tables 3–6。

WildDet3D-Bench 上的 ground-truth depth 增益较大；ScanNet 的 ODS 增益为 `1.3`，Argoverse 2 仅为 `0.1`；Stereo4D 的真实 stereo depth 则带来 `20.2 AP` 增益。效果随数据域、指标与 depth source 明显变化。（PDF pp. 14–17，§4.2–4.5）

> **英文对应表述（非逐字原文）：** Depth gains range from marginal to very large across datasets, metrics, prompt modes, and depth sources.

因此，摘要所称“平均 `+20.7 AP`”需要给出纳入的 settings、指标与权重后才能复算。ODS 与 AP 也不应直接混合求平均。（PDF p. 1，Abstract；pp. 15–17，Tables 3–6）

> **英文对应表述（非逐字原文）：** The stated average improvement cannot be reconstructed unambiguously without a defined set of conditions and aggregation rule.

真实 stereo 测试更接近部署，但仅有 383 张图像、78 个类别，并限于 box prompt；ground-truth depth 结果则主要说明模型利用理想 geometry signal 的能力。

> **英文对应表述（非逐字原文）：** Real-stereo evidence is deployment-relevant but small, whereas ground-truth-depth results primarily measure an upper-bound conditioning capability.

来源：[[2604.08626v2 (1)|WildDet3D 论文来源]]。