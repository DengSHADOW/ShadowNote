---
type: concept
title: 多模型候选—人工/VLM 混合 3D 标注
created: 2026-09-16
updated: 2026-09-16
tags: [3D-annotation, data-engine, VLM, human-in-the-loop, candidate-selection]
related: [2604.08626v2 (1), WildDet3D-Data, WildDet3D, 分割数据引擎]
sources: ["2604.08626v2 (1).pdf"]
---
# 多模型候选—人工/VLM 混合 3D 标注

该方法先让多个具有不同误差模式的 3D lifting 方法为同一个 2D annotation 生成候选，再以几何规则、VLM 和人工判断筛选。它与[[分割数据引擎]]共享“模型辅助标注—质量筛选—迭代扩展”的思路，但目标是 metric 3D box，而非 segmentation mask。（PDF pp. 9–13，§3，Figure 4）

> **英文对应表述（非逐字原文）：** Multiple candidate generators expose complementary hypotheses, after which automated and human filters decide whether any proposal is usable.

## 候选生成

WildDet3D-Data 使用 3D-MOOD、DetAny3D、SAM-3D、RANSAC-PCA 和 LabelAny3D。候选经过 translation 和 rotation optimization 后，被统一为包含 center、dimensions 与 quaternion 的 10D format。（PDF p. 10，§3.1）

> **英文对应表述（非逐字原文）：** Learned detection, reconstruction, and geometric fitting methods contribute candidates that are refined and converted into one shared box format.

## 两条筛选路径

人工路径展示透视 overlay 和三个正交 point-cloud views，由标注者选择最佳候选并评为 `good_fit`、`acceptable` 或 `unacceptable`。自动路径使用 fine-tuned Molmo2 对六个感知维度评分，并保留达到阈值的最高分候选。（PDF p. 11，§3.3）

> **英文对应表述（非逐字原文）：** Human selection uses multi-view inspection, while automatic selection uses structured perceptual scoring over projected boxes.

## 可靠性

不同候选生成器的 rejection rate 相差超过三倍，说明多模型候选具有互补性，但也说明 source-model identity 会影响标注质量。VLM score 的聚合单调性不能替代逐样本 calibration；`AUC=0.66` 与 score `10` 下 `16.7%` rejection 均表明残余噪声明显。（PDF pp. 12–13，§3.5，Table 2）

> **英文对应表述（非逐字原文）：** Candidate diversity improves coverage, but automatic ranking remains only moderately predictive of human acceptance.

类别尺寸由 GPT-4.1-mini 生成、depicted/composite filters 由 Qwen3.5-9B 提供，最终候选又由 Molmo2 排序，因此多个模型的共同偏差可能集中影响罕见尺度、文化特定物体和非典型形状。（PDF pp. 11、31–32，§3.2，Appendix D）

> **英文对应表述（非逐字原文）：** Stacked model-based filters may compound systematic errors for underrepresented categories and unusual geometries.

来源：[[2604.08626v2 (1)|WildDet3D 论文来源]]；实例数据集见 [[WildDet3D-Data]]。