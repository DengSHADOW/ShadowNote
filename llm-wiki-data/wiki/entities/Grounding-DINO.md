---
type: entity
title: Grounding DINO
created: 2026-09-16
updated: 2026-09-16
tags: [model, object-detection, vision-language, transformer]
related: [2303.05499v5 (1), tight-modality-fusion, language-guided-query-selection, grounded-pre-training]
sources: ["2303.05499v5 (1).pdf"]
---

# Grounding DINO

Grounding DINO 是以 DINO 为基础的文本条件化开放集目标检测模型。它接收图像和类别名称或 referring expression，输出物体框及其对应短语；其论文证据汇总见 [[2303.05499v5 (1)|来源论文]]。（PDF pp. 1、5–6，Abstract，§3）

> **英文原文：** “Grounding DINO outputs multiple pairs of object boxes and noun phrases for a given (Image, Text) pair.”

## 组成

Grounding DINO 采用 dual-encoder-single-decoder 架构，由图像 backbone、文本 backbone、feature enhancer、[[language-guided-query-selection|language-guided query selection]] 和 cross-modality decoder 构成。（PDF p. 6，§3）

> **英文原文：** “It contains an image backbone for image feature extraction, a text backbone for text feature extraction, a feature enhancer for image and text feature fusion, a language-guided query selection module for query initialization, and a cross-modality decoder for box refinement.”

模型通过 [[tight-modality-fusion|tight modality fusion]] 在 encoder、query 初始化和 decoder 三处注入语言信息。分类分支使用 query 与文本 token 的相似度，而框回归继续采用 L1 和 GIOU loss。（PDF pp. 5–8，Figure 3，§3.1–§3.5）

> **英文对应表述（非逐字原文）：** Grounding DINO injects language at the feature-enhancement, query-initialization, and decoder stages, while using token-level contrastive classification together with L1 and GIOU box-regression losses.

## 能力边界

论文中的“zero-shot”只表示没有使用目标 benchmark 的训练 split，不保证训练类别与测试类别互斥。尤其 O365 几乎覆盖 COCO 类别，因此 COCO `52.5 AP` 不应被解释为严格 novel-category 泛化。（PDF pp. 2、9–10，§1、§4.2）

> **英文原文：** “It is not an exact mapping between O365 and COCO categories. We made some approximations during evaluation.”

Grounding DINO 在 LVIS rare categories 上弱于若干对照配置，并在 ODinW 的不同领域间呈现很大差异。这说明“detect arbitrary objects”是研究目标和宣传性概括，而不是已被无限制验证的能力。（PDF pp. 10、29–33，Tables 3、12–18）

> **英文对应表述（非逐字原文）：** Performance on LVIS rare categories and individual ODinW datasets varies substantially, so the reported evidence does not support an unrestricted interpretation of “detect arbitrary objects.”

模型本身不执行图像生成。论文中的编辑应用由 Grounding DINO 提供检测框或 mask，再由 Stable Diffusion 或 GLIGEN 生成内容。（PDF pp. 26–28，Figures 9–10）

> **英文原文：** “We first detect objects with Grounding DINO and then perform image inpainting with Stable Diffusion.”

Grounding DINO 也不支持 segmentation，并可能产生 false positives 或 hallucination。（PDF p. 14，Limitations）

> **英文原文：** “Our model will produce false positive results in some cases, which may need more techniques or data to reduce the hallucination.”