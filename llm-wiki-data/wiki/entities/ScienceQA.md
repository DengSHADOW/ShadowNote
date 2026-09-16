---
type: entity
title: ScienceQA
created: 2026-09-16
updated: 2026-09-16
tags: [数据集, benchmark, 多模态推理, 科学问答]
related: [2304.08485v2, LLaVA, GPT-4-as-judge-多模态评估, LLaVA-与-ScienceQA-基线及-GPT-4-ensemble]
sources: ["2304.08485v2.pdf"]
---
# ScienceQA

ScienceQA 是一个包含约 21K 道多模态科学选择题的 benchmark，覆盖 3 个学科、26 个主题、127 个类别和 379 项技能。论文使用的划分包含 12,726 个训练样本、4,241 个验证样本和 4,241 个测试样本。（PDF p. 8，§5.2）

> **英文原文：** “ScienceQA contains 21k multimodal multiple choice questions with rich domain diversity across 3 subjects, 26 topics, 127 categories, and 379 skills.”

每道题的上下文可能是自然语言或图像，并带有 lecture 与 explanation。[[LLaVA]] 的训练目标是先生成自然语言 reasoning，再从多个选项中选择答案。（PDF pp. 5、8，§§4.2、5.2）

> **英文原文：** “The assistant provides the reasoning process in natural language and selects the answer among multiple choices.”

## 本文结果

LLaVA 单模型取得 90.92% accuracy，MM-CoT Large 为 91.68%，text-only GPT-4 为 82.69%。GPT-4 complement 组合为 90.97%，相较 LLaVA 只提高 0.05 个百分点。（PDF pp. 8–9，Table 7）

> **英文对应表述（非逐字原文）：** The complement scheme provides almost no gain over LLaVA alone: 90.97% versus 90.92%.

当 LLaVA 与 GPT-4 答案不一致时，让 GPT-4 比较两者并给出最终答案，accuracy 达到 92.53%。这是 [[GPT-4-as-judge-多模态评估|judge ensemble]] 的结果，而不是 LLaVA 单模型结果。（PDF pp. 8–9，§5.2，Table 7）

> **英文原文：** “Whenever GPT-4 and LLaVA produce different answers, we prompt GPT-4 again.”

text-only GPT-4 在带图题目中的帮助不证明其具有视觉能力。作者指出，一部分 IMG 问题可以不依赖图像，使用题干、选项和常识得到正确答案。（PDF p. 8，§5.2）

> **英文原文：** “Some of these questions do not actually require the image context for a correct answer.”

## 可复现性边界

92.53% 依赖 closed GPT-4 的输出与 judge 决策。论文没有报告固定模型快照、重复运行方差或独立 judge，因此该 ensemble 的长期复现性弱于只使用公开权重模型的单模型结果。