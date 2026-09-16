---
type: concept
title: Referring Expression Comprehension（REC）
created: 2026-09-16
updated: 2026-09-16
tags: [visual-grounding, referring-expression, object-localization]
related: [2303.05499v5 (1), Grounding-DINO, 开放集目标检测]
sources: ["2303.05499v5 (1).pdf"]
---

# Referring Expression Comprehension（REC）

Referring Expression Comprehension（REC）要求模型依据包含属性、位置或关系的自然语言表达定位特定对象。来源论文把 REC 与 referring object detection 作为可互换术语使用。（PDF p. 3，脚注 3）

> **英文原文：** “We use the term Referring Expression Comprehension (REC) and Referring (Object) Detection exchangeable in this paper.”

在 [[Grounding-DINO]] 中，REC 推理选择得分最高的输出对象作为表达式对应框。（PDF pp. 5–6，§3）

> **英文原文：** “We use the output object with the largest scores as the output for the REC task.”

## 与类别检测的任务错配

常规 grounded detection 可能让一个文本 prompt 对应多个框，而 RefCOCO 通常要求一个表达式唯一指向一个对象。这一差异使 REC 比类别名称检测更依赖属性和关系层面的判别。（PDF pp. 25–26，Figure 8，Appendix D.3）

> **英文原文：** “Each RefCOCO text prompt corresponds to only one box, while our model tends to predict multiple objects.”

未使用 RefC 时，Grounding DINO T 的 RefCOCO val 为 `50.41`、RefCOCO+ val 为 `51.40`；加入 RefC 后分别升至 `73.98` 和 `66.81`，再 fine-tune 后升至 `89.19` 和 `81.09`。（PDF p. 12，Table 5）

> **英文对应表述（非逐字原文）：** Adding RefC raises Grounding DINO T from 50.41 to 73.98 on RefCOCO val and from 51.40 to 66.81 on RefCOCO+ val; fine-tuning raises them further to 89.19 and 81.09.

这些差值表明，开放词汇类别检测不会自然转化为强 REC 能力，任务匹配数据是主要因素。（PDF p. 12，§4.3）

> **英文原文：** “After injecting RefCOCO/+/g data into training, Grounding DINO obtains significant gains.”

Grounding DINO L 的 REC 结果可能受到图像重叠影响，因为其训练数据含 COCO，而 COCO 包含 RefC validation images。虽然标注不同，比较时仍应显式记录这一条件。（PDF p. 12，Table 5）

> **英文原文：** “There might be a data leak since COCO includes validation images in RefC.”