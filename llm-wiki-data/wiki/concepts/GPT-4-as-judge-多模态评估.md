---
type: concept
title: GPT-4-as-judge 多模态评估
created: 2026-09-16
updated: 2026-09-16
tags: [GPT-4-as-judge, 多模态评估, model-ensembling, 方法学风险]
related: [2304.08485v2, LLaVA-Bench, ScienceQA, LLaVA, GPT-assisted-visual-instruction-data-generation]
sources: ["2304.08485v2.pdf"]
---
# GPT-4-as-judge 多模态评估

GPT-4-as-judge 多模态评估是让 text-only GPT-4 依据问题、文本化视觉信息和候选回答进行比较或选择。在 [[2304.08485v2|Visual Instruction Tuning]] 中，它被用于 [[LLaVA-Bench]] 评分和 [[ScienceQA]] model ensembling。（PDF pp. 6–9，§5）

> **英文对应表述（非逐字原文）：** Text-only GPT-4 is used both to score multimodal responses and to resolve disagreements between model predictions.

## LLaVA-Bench 评分

裁判接收问题、ground-truth textual descriptions 和两个 assistant 回答，依据 helpfulness、relevance、accuracy 与 detail 给出 1–10 分及解释。（PDF p. 6，§5.1）

> **英文原文：** “It evaluates the helpfulness, relevance, accuracy, and level of detail … and gives an overall score on a scale of 1 to 10.”

最终指标是候选模型分数相对于 GPT-4 reference 分数的比例。它不等同于客观任务准确率，reference 也只读取文本描述，而非原始图像。（PDF pp. 6–7，§5.1）

> **英文原文：** “We report relative scores w.r.t. the text-only GPT-4 model.”

## ScienceQA judge ensemble

当 LLaVA 与 GPT-4 给出不同答案时，GPT-4 judge 读取题目和双方结果并选择最终答案。该机制把 ScienceQA accuracy 从 LLaVA 的 90.92% 提升到 92.53%。（PDF pp. 8–9，§5.2，Table 7）

> **英文原文：** “The GPT-4 judge can identify such cases and correct some of the errors that LLaVA makes.”

论文中的 complement 策略只达到 90.97%，说明性能提升主要来自 judge 的重新裁决，而不是在 GPT-4 拒答时简单回退到 LLaVA。（PDF p. 9，Table 7）

> **英文对应表述（非逐字原文）：** The judge strategy adds 1.61 percentage points over LLaVA, whereas the complement strategy adds only 0.05.

## 有效性威胁

GPT-4 同时参与训练数据生成、reference generation、评分和 ensemble，可能形成风格偏好与评价闭环。论文虽报告三次 judge 查询具有一致性，却没有给出与人工判断的系统相关性，也没有固定 GPT-4 版本与随机性条件。（PDF pp. 7、14，Table 5 与 Appendix A）

> **英文原文：** “Its robustness in different situations and capability to evaluate other unexplored aspects are subjects for future work.”

Table 10 还出现 assistant 编号与实际答案不一致的文本错误，说明单个 judge 示例需要逐条核对，不能只凭自然语言解释认定其过程记录正确。（PDF p. 19，Table 10）