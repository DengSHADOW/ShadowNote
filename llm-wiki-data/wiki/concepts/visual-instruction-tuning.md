---
type: concept
title: visual instruction tuning
created: 2026-09-16
updated: 2026-09-16
tags: [instruction-tuning, 多模态学习, 视觉语言, 指令遵循]
related: [2304.08485v2, LLaVA, LLaVA-Instruct-158K, GPT-assisted-visual-instruction-data-generation, 多模态-feature-alignment]
sources: ["2304.08485v2.pdf"]
---
# visual instruction tuning

visual instruction tuning 是把 instruction tuning 扩展到图像—语言空间的方法：训练样本同时包含视觉输入、自然语言 instruction 和目标回答，使用户以语言显式指定视觉任务。（PDF pp. 1–2，§1）

> **英文原文：** “We present visual instruction-tuning … to extend instruction-tuning to the language-image multimodal space.”

与把任务固化在模型结构或接口中的专用视觉模型相比，这一方法把语言用作通用任务接口，目标是让单个视觉助手根据 instruction 切换任务。（PDF p. 1，§1）

> **英文原文：** “Various task instructions can be explicitly represented in language and guide the end-to-end trained neural assistant to switch to the task of interest.”

## 与 visual prompt tuning 的区别

visual instruction tuning 旨在提升模型理解并遵循自然语言指令的能力；visual prompt tuning 则主要追求参数高效的模型适配。论文明确区分这两个概念。（PDF p. 2，§2）

> **英文原文：** “The former aims to improve the model’s instruction-following abilities, while the latter aims to improve the parameter-efficiency in model adaptation.”

## 在 LLaVA 中的实现

[[LLaVA]] 先通过 [[多模态-feature-alignment]] 建立视觉 token 与语言 embedding 的兼容性，再用 [[LLaVA-Instruct-158K]] 更新投影层和 Vicuna。视觉编码器在两个阶段均被冻结。（PDF p. 5，§4.2）

> **英文对应表述（非逐字原文）：** LLaVA implements visual instruction tuning through a frozen visual encoder, an aligned projection layer, and instruction fine-tuning of the projection and language model.

LLaVA-Bench (COCO) 中，无 instruction tuning 版本整体相对分数为 21.5，完整数据版本为 85.1。这是该方法对 LLaVA 指令遵循能力贡献的直接消融证据，但不是跨模型的普遍结论。（PDF p. 7，Table 4）

> **英文原文：** “With instruction tuning, the model’s ability of following user instructions improves significantly by over 50 points.”

## Wiki 连接

本概念可与 [[可提示分割]]、[[开放集目标检测]] 和 [[可提示-3D-目标检测]] 对照理解：这些页面中的 promptable perception 通常围绕特定输出结构，而 visual instruction tuning 试图以自然语言覆盖更广泛的视觉任务。[[2304.08485v2|本来源]]没有直接比较 SAM、Grounding DINO 或 WildDet3D，因而这种联系属于接口层级的知识组织，而非实验胜负关系。