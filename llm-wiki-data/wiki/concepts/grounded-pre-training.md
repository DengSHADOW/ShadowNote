---
type: concept
title: grounded pre-training
created: 2026-09-16
updated: 2026-09-16
tags: [vision-language, grounding, pre-training, object-detection]
related: [2303.05499v5 (1), Grounding-DINO, 开放集目标检测]
sources: ["2303.05499v5 (1).pdf"]
---

# Grounded pre-training

Grounded pre-training 通过 region–phrase 对齐统一使用 detection、grounding 和 caption 数据，使检测区域能够进入语言语义空间。[[Grounding-DINO]] 沿用并修改了 GLIP 的训练方式，以支持开放集概念迁移。（PDF pp. 3、8、19–20，§1、§3.5、Appendix B）

> **英文原文：** “GLIP presents a different way by reformulating object detection as a phrase grounding task and introducing contrastive training between object regions and language phrases on large-scale data.”

## 数据类型

检测数据通过把类别名称拼接成文本 prompt 转换为 phrase grounding；grounding 数据直接提供区域与短语对应；caption 数据则使用 GLIP 生成的伪标注。（PDF p. 20，Appendix B）

> **英文原文：** “Following GLIP, we use the pseudo-labeled caption data for model training.”

Grounding DINO T 的主要训练数据包括 O365v1、GoldG 和 Cap4M；Grounding DINO L 使用更大的 O365v2，并在部分配置中加入 OpenImages、COCO 和 RefC。（PDF pp. 8–13、20，Tables 2–6，Appendix B）

> **英文对应表述（非逐字原文）：** Grounding DINO configurations combine different subsets of O365, GoldG, Cap4M, OpenImages, COCO, and RefC, with the large variant using the larger O365v2 dataset.

## 泛化并非单调增长

加入 Cap4M 后，Grounding DINO T 的 LVIS AP 从 `25.6` 增至 `27.4`；但加入 RefC 后，LVIS 从 `25.6` 降至 `21.9`，ODinW 从 `20.0` 降至 `17.7`。这说明 grounded pre-training 的效果取决于数据分布与任务对齐，而不只是样本数量。（PDF pp. 10、13，Tables 3、6）

> **英文原文：** “RefC helps improve the COCO zero-shot and fine-tuning performance but hurts the LVIS and ODinW results.”

作者以一次 Cap4M 增量推断 Grounding DINO 可能比 GLIP 更具 scalability，但没有提供多规模训练曲线、计算量控制或不确定性估计，因此该结论仍属有限证据。（PDF p. 10，§4.2）

> **英文原文：** “We believe that Grounding DINO has better scalability compared with GLIP.”