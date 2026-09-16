---
type: concept
title: language-guided query selection
created: 2026-09-16
updated: 2026-09-16
tags: [transformer, object-query, vision-language, detection]
related: [2303.05499v5 (1), Grounding-DINO, tight-modality-fusion]
sources: ["2303.05499v5 (1).pdf"]
---

# Language-guided query selection

Language-guided query selection 是 [[Grounding-DINO]] 在 decoder 前选择图像 tokens 的机制。它计算图像 token 与文本 token 的相似度，对每个图像 token 取最大文本相似度，再选出 top-$N_q$ 索引。（PDF p. 7，Equation 1，§3.2）

$$
\mathcal{I}_{N_q}
=
\operatorname{Top}_{N_q}
\left(
\operatorname{Max}^{(-1)}
\left(X_I X_T^\top\right)
\right).
$$

> **英文原文：** “We design a language-guided query selection module to select features that are more relevant to the input text as decoder queries.”

论文默认 `d = 256`、`N_q = 900`，典型图像 token 数超过 `10,000`，文本 token 数低于 `256`。（PDF p. 7，§3.2）

> **英文原文：** “In alignment with the DINO method, we set $N_q$ to be 900.”

选出的 encoder 索引用于初始化 query 的位置部分，即 dynamic anchor boxes；content query 仍为可学习参数。因此，该机制更准确地说是语言引导的位置候选选择。（PDF p. 7，§3.2）

> **英文原文：** “We formulate the positional part as dynamic anchor boxes, which are initialized with encoder outputs.”

## 证据与歧义

在 Table 7 中，full model 的 LVIS zero-shot AP 为 `16.1`，static query selection 为 `13.6`，实际差值是 `2.5 AP`；正文却报告 `+3.0 AP`。（PDF pp. 13–14，Table 7）

> **英文原文：** “Language-guided query selection [...] contribute[s] positively to the LVIS performance, yielding significant gains of +3.0 AP.”

Algorithm 1 还存在变量名不一致：先定义 `logits_per_img_feat`，随后却把 `logits_per_img_feature` 传入 `torch.topk`。复现时需要把论文伪代码与发布实现对照。（PDF p. 20，Algorithm 1）

> **英文对应表述（非逐字原文）：** Algorithm 1 defines `logits_per_img_feat` but calls `torch.topk` with `logits_per_img_feature`, creating a literal undefined-variable error.