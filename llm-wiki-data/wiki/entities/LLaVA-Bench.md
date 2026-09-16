---
type: entity
title: LLaVA-Bench
created: 2026-09-16
updated: 2026-09-16
tags: [benchmark, 多模态评估, GPT-4-as-judge, 指令遵循]
related: [2304.08485v2, LLaVA, GPT-4-as-judge-多模态评估, LLaVA-与-BLIP-2-和-OpenFlamingo]
sources: ["2304.08485v2.pdf"]
---
# LLaVA-Bench

LLaVA-Bench 是 [[2304.08485v2|Visual Instruction Tuning]] 为多模态 instruction following 构建的评测套件，包括 COCO 与 In-the-Wild 两个子集。（PDF pp. 2、6–7，§§1、5.1）

> **英文原文：** “We present LLaVA-Bench with two challenging benchmarks, with a diverse selection of paired images, instructions and detailed annotations.”

## COCO 子集

LLaVA-Bench (COCO) 从 COCO-Val-2014 随机选取 30 张图，并为每张图生成 conversation、detailed description 和 complex reasoning 三类问题，共 90 个问题。论文用它研究不同训练数据对 [[LLaVA]] alignment behavior 的影响。（PDF p. 7，§5.1）

> **英文原文：** “We randomly select 30 images from COCO-Val-2014 … totaling 90 questions.”

## In-the-Wild 子集

LLaVA-Bench (In-the-Wild) 包含 24 张图和 60 个问题，图像涵盖室内外场景、meme、绘画和草图。每张图配有人工整理的详细描述与问题。（PDF p. 7，§5.1）

> **英文原文：** “We collect a diverse set of 24 images with 60 questions in total, including indoor and outdoor scenes, memes, paintings, sketches, etc.”

## 评分机制

候选模型读取图像并回答问题；text-only GPT-4 根据 ground-truth textual descriptions 生成 reference answer。随后另一次 GPT-4 调用读取问题、文本化视觉信息和两个回答，按 helpfulness、relevance、accuracy 与 detail 评分。（PDF p. 6，§5.1）

> **英文原文：** “It evaluates the helpfulness, relevance, accuracy, and level of detail of the responses from the assistants.”

报告值是候选模型相对于 GPT-4 reference 的 relative score，不是常规任务准确率。所谓 “approximate theoretical upper bound” 也不是真正的视觉上界，因为 reference 模型读取的是人工文本描述而非原始图像。（PDF pp. 6–7，§5.1）

> **英文原文：** “To provide an approximate theoretical upper bound, we create a reference prediction … using the text-only GPT-4.”

## 方法学限制

[[GPT-4-as-judge-多模态评估]] 在这里形成角色重叠：相近的 GPT-4 管线参与问题或 reference 的产生，同时担任裁判。论文报告重复查询下评分较一致，但没有与独立人工评价做系统校准。（PDF p. 7，Table 5）

> **英文原文：** “For a given set of LLaVA decoding sequences, we evaluate by querying GPT-4 three times; GPT-4 gives a consistent evaluation.”

两个子集规模都较小，因此其大幅分差适合视为候选模型在特定问题集上的证据，不宜直接解释为开放世界多模态能力的总体排名。