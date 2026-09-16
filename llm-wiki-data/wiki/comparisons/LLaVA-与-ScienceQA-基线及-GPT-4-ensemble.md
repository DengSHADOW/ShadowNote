---
type: comparison
title: LLaVA 与 ScienceQA 基线及 GPT-4 ensemble
created: 2026-09-16
updated: 2026-09-16
tags: [ScienceQA, 模型比较, GPT-4, ensemble, 多模态推理]
related: [2304.08485v2, LLaVA, ScienceQA, GPT-4-as-judge-多模态评估]
sources: ["2304.08485v2.pdf"]
---
# LLaVA 与 ScienceQA 基线及 GPT-4 ensemble

[[2304.08485v2|Visual Instruction Tuning]] 在 [[ScienceQA]] 上比较 GPT-3.5、LLaMA-Adapter、MM-CoT、text-only GPT-4、[[LLaVA]] 及两种 LLaVA–GPT-4 组合策略。（PDF pp. 8–9，§5.2，Table 7）

> **英文原文：** “We consider two schemes to combine the outcomes from our model and GPT-4.”

| 方法 | Average accuracy |
|---|---:|
| GPT-3.5 | 73.97 |
| GPT-3.5 w/ CoT | 75.17 |
| LLaMA-Adapter | 85.19 |
| MM-CoT Base | 84.91 |
| MM-CoT Large | 91.68 |
| GPT-4† | 82.69 |
| LLaVA | 90.92 |
| LLaVA+GPT-4† (complement) | 90.97 |
| LLaVA+GPT-4† (judge) | 92.53 |

*来源：PDF p. 9，Table 7。† 表示 text-only GPT-4。*

LLaVA 单模型比 MM-CoT Large 低 0.76 个百分点。complement 策略只比 LLaVA 高 0.05 个百分点；[[GPT-4-as-judge-多模态评估|judge ensemble]] 则高 1.61 个百分点，并比表中此前最高结果高 0.85 个百分点。（PDF pp. 8–9，Table 7）

> **英文原文：** “This scheme is able to provide consistent improvement over all question classes, and achieves a new SoTA accuracy of 92.53%.”

92.53% 必须归属于 LLaVA+GPT-4 judge 系统，而不能写作 LLaVA 单模型准确率。GPT-4 在 IMG 类别中的作用也不能解释为视觉能力，因为部分题目无需图像即可回答。（PDF p. 8，§5.2）

> **英文原文：** “Some of these questions do not actually require the image context for a correct answer.”

论文把这一结果描述为首次使用 GPT-4 进行 model ensembling，但这是作者的优先权声明，本文没有提供系统文献核验。closed GPT-4 的版本依赖和非确定性也使 ensemble 结果的可复现性弱于单模型结果。