---
type: concept
title: 多模态 feature alignment
created: 2026-09-16
updated: 2026-09-16
tags: [feature-alignment, CLIP, Vicuna, 多模态训练]
related: [2304.08485v2, LLaVA, visual-instruction-tuning, LLaVA-Instruct-158K]
sources: ["2304.08485v2.pdf"]
---
# 多模态 feature alignment

多模态 feature alignment 是 [[LLaVA]] 两阶段训练的第一阶段：冻结 CLIP vision encoder 与 Vicuna，只训练线性投影矩阵 $W$，使视觉特征进入语言模型的 embedding 空间。（PDF pp. 4–5，§§4.1–4.2）

> **英文原文：** “The image features $H_v$ can be aligned with the pre-trained LLM word embedding.”

$$
Z_v=g(X_v),\qquad H_v=W\cdot Z_v
$$

论文也把这一阶段解释为为冻结的 LLM 训练兼容的 visual tokenizer。（PDF p. 5，§4.2）

> **英文原文：** “This stage can be understood as training a compatible visual tokenizer for the frozen LLM.”

## 训练数据

该阶段使用从 CC3M 筛选得到的 CC-595K。每个 image-text pair 被改造成单轮指令数据：问题要求简要描述图像，原始 caption 作为目标回答。（PDF p. 5，§4.2）

> **英文原文：** “The ground-truth prediction answer $X_a$ is the original caption.”

CC3M 的筛选过程先用 Spacy 抽取 noun phrases，去除频率低于 3 的短语，并对频率超过 100 的短语最多随机采样 100 条 caption，最终得到约 595K 对。（PDF pp. 20–21，Appendix E）

> **英文原文：** “This results in around 595K image-text pairs.”

## 实验证据

在 ScienceQA 消融中，跳过 alignment 预训练并直接训练的 accuracy 为 85.81%，最佳配置为 90.92%，相差 5.11 个百分点。（PDF p. 9，Table 8）

> **英文原文：** “The 5.11% absolute degradation indicates the importance of our pre-training stage.”

该结果支持 feature alignment 对本论文 LLaVA 配置的重要性，但没有隔离“表示对齐”“额外训练数据”和“优化初始化”各自的贡献。