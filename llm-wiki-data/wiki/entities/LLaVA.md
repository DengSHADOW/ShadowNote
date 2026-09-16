---
type: entity
title: LLaVA
created: 2026-09-16
updated: 2026-09-16
tags: [多模态模型, 视觉助手, Vicuna, CLIP]
related: [2304.08485v2, visual-instruction-tuning, 多模态-feature-alignment, LLaVA-Instruct-158K, LLaVA-Bench]
sources: ["2304.08485v2.pdf"]
---
# LLaVA

LLaVA（Large Language and Vision Assistant）是 [[2304.08485v2|Visual Instruction Tuning]] 提出的 large multimodal model。它将冻结的 CLIP ViT-L/14 vision encoder 与 Vicuna language decoder 相连，以视觉 token 和语言 instruction 生成开放式语言回答。（PDF pp. 1、4，摘要与 §4.1）

> **英文原文：** “LLaVA: Large Language and Vision Assistant, an end-to-end trained large multimodal model that connects a vision encoder and an LLM.”

## 架构边界

LLaVA 的连接层是线性投影矩阵 $W$：

$$
Z_v=g(X_v),\qquad H_v=W\cdot Z_v
$$

$W$ 将 CLIP 视觉特征转换为与 Vicuna 词嵌入维度相同的视觉 token。（PDF p. 4，§4.1，Equation 1）

> **英文原文：** “We apply a trainable projection matrix $W$ to convert $Z_v$ into language embedding tokens $H_v$.”

训练过程中 CLIP 始终冻结。Stage 1 只更新 $W$；Stage 2 更新 $W$ 和 Vicuna 参数。因此 LLaVA 是统一的图像到文本系统，但不是所有组件共同微调的模型。（PDF p. 5，§4.2）

> **英文原文：** “We always keep the visual encoder weights frozen.”

## 证据范围

在 [[LLaVA-Bench]] (COCO) 中，完整 [[visual-instruction-tuning]] 版本得到 85.1 的相对分数，无 instruction tuning 版本为 21.5。85.1 是相对于读取 ground-truth 文本描述的 GPT-4 reference 的评分，而不是准确率。（PDF p. 7，Table 4）

> **英文原文：** “We report relative scores w.r.t. a text-only GPT-4 model that uses ground truth image captions and bounding boxes as visual input.”

在 [[ScienceQA]] 上，LLaVA 单模型的 accuracy 为 90.92%；加入 GPT-4 judge 后为 92.53%。后者是 ensemble 结果，不应归因于 LLaVA 单独模型。（PDF pp. 8–9，Table 7）

> **英文对应表述（非逐字原文）：** LLaVA alone scores 90.92% on ScienceQA, while the 92.53% result belongs to an ensemble using text-only GPT-4 as a judge.

## 已知限制

论文报告 LLaVA 可能产生视觉或事实幻觉，并继承 CLIP、LLaMA 和 Vicuna 的 bias。它还会出现 [[bag-of-patches-组合语义失败]]：识别出局部对象，却错误组合对象之间的语义关系。（PDF pp. 7、14，§5.1 与 Appendix A）

> **英文原文：** “LLaVA might generate outputs that aren’t grounded in facts or input data.”

附录中的 OCR、人物识别、meme 解释和代码生成属于定性案例。论文自身要求后续对这些 emergent behaviors 做更系统的机制与稳健性研究。（PDF pp. 14–19，Appendix B）

> **英文原文：** “It is important to investigate these emergent behaviors more thoroughly.”