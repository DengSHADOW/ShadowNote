---
type: entity
title: WildDet3D-Bench
created: 2026-09-16
updated: 2026-09-16
tags: [benchmark, 3D-detection, open-vocabulary, long-tail, federated-evaluation]
related: [2604.08626v2 (1), WildDet3D, WildDet3D-Data, 开放词汇单目-3D-目标检测, 非穷举-3D-标注下的-ignore-region-suppression]
sources: ["2604.08626v2 (1).pdf"]
---
# WildDet3D-Bench

WildDet3D-Bench 是从 [[WildDet3D-Data]] validation set 构建的 in-the-wild 3D detection benchmark，覆盖来自 COCO、LVIS 和 Objects365 的开放词汇类别，并提供人工验证的 3D annotations。（PDF pp. 13–14，§4.1）

> **英文对应表述（非逐字原文）：** WildDet3D-Bench uses human-verified validation annotations to evaluate open-vocabulary 3D detection in varied real-world imagery.

## 协议

benchmark 使用按图像频次划分的 rare、common 和 frequent groups，并通过对象 half-diagonal 归一化的 center-distance thresholds `[0.50:1.00:0.05]` 计算 AP。text-prompt evaluation 采用 federated protocol，使与缺少有效 3D box 的已标注 2D object 重叠的 prediction 保持 neutral。（PDF p. 14，§4.1）

> **英文对应表述（非逐字原文）：** Evaluation combines frequency-stratified center-distance AP with neutral handling of predictions over known but non-3D-annotated objects.

这一 neutral 规则与训练中的[[非穷举-3D-标注下的-ignore-region-suppression]]相对应，避免因 3D annotations 不完整而系统性惩罚合理检测。

> **英文对应表述（非逐字原文）：** Training and evaluation both attempt to avoid treating missing 3D labels as confirmed background.

## 报告结果

在完整训练组合下，[[WildDet3D]]取得 `22.6 AP` 的 text-prompt result 和 `24.8 AP` 的 box-prompt result；加入 ground-truth depth 后分别为 `41.6` 和 `47.2 AP`。（PDF pp. 14–15，§4.2，Table 3）

> **英文对应表述（非逐字原文）：** The full training mixture yields higher AP in both prompt modes, and ground-truth depth produces additional large gains.

## 解释注意事项

论文称 benchmark 覆盖 “700+ categories”，但 frequency groups 的数量为 `464 + 283 + 63 = 810`；Table 1 又列出 `785` 个 val categories，而正文另称 `881` 个 validation categories。当前文本没有说明过滤、去重与评估集合之间的对应关系。（PDF pp. 12、14，§3.4、§4.1，Table 1）

> **英文对应表述（非逐字原文）：** Several category totals appear to refer to different subsets, but their exact mapping is not documented.

rare 是按评价样本频次定义，不代表类别在训练中从未出现。因此 APrare 不能直接作为 novel-category generalization 的证据。（PDF pp. 12、14–15，§3.4、§4.1–4.2）

> **英文对应表述（非逐字原文）：** Evaluation rarity does not establish absence from the training vocabulary or training images.

来源：[[2604.08626v2 (1)|WildDet3D 论文来源]]。