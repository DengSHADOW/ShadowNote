---
type: entity
title: LLaVA-Instruct-158K
created: 2026-09-16
updated: 2026-09-16
tags: [数据集, 多模态指令, GPT-4, COCO]
related: [2304.08485v2, LLaVA, GPT-assisted-visual-instruction-data-generation, visual-instruction-tuning]
sources: ["2304.08485v2.pdf"]
---
# LLaVA-Instruct-158K

LLaVA-Instruct-158K 是 [[2304.08485v2|Visual Instruction Tuning]] 构建的语言—图像 instruction-following 数据集，用于 [[LLaVA]] 的第二阶段训练。它包含 158K 个样本：58K conversation、23K detailed description 和 77K complex reasoning。（PDF p. 4，§3）

> **英文原文：** “We collect 158K unique language-image instruction-following samples in total, including 58K in conversations, 23K in detailed description, and 77k in complex reasoning.”

## 构建方式

数据以 COCO 图像为基础，但 text-only GPT-4 不读取像素。生成器接收多条 captions 与带对象类别、归一化位置的 bounding boxes，并通过 few-shot seed examples 生成三类回答。（PDF pp. 3–4，§3；PDF pp. 22–25，Tables 13–16）

> **英文原文：** “We use two types of symbolic representations: (i) Captions … (ii) Bounding boxes.”

conversation 数据覆盖对象类型、数量、动作、位置和相对关系；detailed description 要求完整描述图像；complex reasoning 在可见内容上加入背景知识和逐步推理。（PDF pp. 3–4，§3）

> **英文对应表述（非逐字原文）：** The dataset separates conversational visual questions, comprehensive descriptions, and reasoning-oriented questions into three response types.

## 数据作用

在 LLaVA-Bench (COCO) 上，仅使用 conversation 数据的整体相对分数为 73.8；加入少量 detailed description 与 complex reasoning 后为 80.5；使用完整数据后为 85.1。（PDF p. 7，Table 4）

> **英文原文：** “Having all three types of data yields the best performance at 85.1%.”

这一结果只直接支持三种数据类型对该 LLaVA 配置和该 benchmark 的互补作用，不能外推为所有 large multimodal model 的普遍规律。benchmark 规模为 30 张图和 90 个问题，且生成与评测均依赖 GPT-4。（PDF pp. 6–7，§5.1）

> **英文对应表述（非逐字原文）：** The ablation supports the value of data diversity within this LLaVA experiment, under a small GPT-4-mediated benchmark.

## 数据风险

由于 GPT-4 看到的是 captions 与 boxes，生成样本可能继承代理中的遗漏、错误或歧义。论文只报告 GPT-4 在早期实验中比 ChatGPT 生成质量更高，没有提供系统人工质量评估。（PDF pp. 3–4，§3）

> **英文原文：** “The visual image is not used to prompt GPT.”