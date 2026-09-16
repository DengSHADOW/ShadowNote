---
type: concept
title: GPT-assisted visual instruction data generation
created: 2026-09-16
updated: 2026-09-16
tags: [GPT-4, 数据生成, 多模态指令, 符号化图像代理]
related: [2304.08485v2, LLaVA-Instruct-158K, visual-instruction-tuning, GPT-4-as-judge-多模态评估]
sources: ["2304.08485v2.pdf"]
---
# GPT-assisted visual instruction data generation

GPT-assisted visual instruction data generation 是 [[2304.08485v2|Visual Instruction Tuning]] 提出的数据重构流程：利用 text-only GPT-4，把现有 image-text 数据转换为适合多模态 instruction following 的问答与描述。（PDF pp. 2–4，§§1、3）

> **英文原文：** “We present a data reformation perspective and pipeline to convert image-text pairs into an appropriate instruction-following format, using ChatGPT/GPT-4.”

## 符号化图像代理

GPT-4 不接收原始像素。流程用多条 captions 表示场景语义，用 bounding boxes 表示对象概念与空间位置，再把二者编码成 LLM 可读的文本序列。（PDF p. 3，§3）

> **英文原文：** “This symbolic representation allows us to encode the image as an LLM-recognizable sequence.”

这种设计使纯文本模型能够生成视觉 instruction data，但其认知边界由 captions 与 boxes 决定：未被代理记录的细节无法可靠进入生成数据，错误信息也可能沿生成链传播。（PDF pp. 3、23，§3 与 Table 14）

> **英文对应表述（非逐字原文）：** Because GPT-4 receives only symbolic descriptions, the generated supervision is limited by the coverage and correctness of captions and boxes.

## 生成类别

流程生成 conversation、detailed description 和 complex reasoning 三类数据。conversation 强调对象、数量、动作和位置；detailed description 强调全面描述；complex reasoning 在图像内容之上加入逻辑推理或背景知识。（PDF pp. 3–4，§3）

> **英文原文：** “We use COCO images and generate three types of instruction-following data.”

每类数据由人工设计少量 seed examples，再通过 few-shot in-context learning 扩展。论文将这些 seed examples 描述为数据收集阶段唯一的人工标注。（PDF p. 3，§3）

> **英文原文：** “They are the only human annotations we have during data collection.”

## 方法学风险

同一研究又使用 GPT-4 生成 reference answers、进行 LLaVA-Bench 评分并参与 ScienceQA ensemble。数据 teacher 与 evaluator 的角色重叠可能偏好 GPT-4 自身的表达风格，需要通过独立人工评价或异构 judge 校准。