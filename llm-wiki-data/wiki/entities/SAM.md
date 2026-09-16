---
type: entity
title: Segment Anything Model（SAM）
created: 2026-09-16
updated: 2026-09-16
tags: [image-segmentation, foundation-model, promptable-model]
related: [2304.02643v1 (1), SA-1B, 可提示分割, 歧义感知多掩码预测]
sources: ["2304.02643v1 (1).pdf"]
---
# Segment Anything Model（SAM）

SAM 是 [[2304.02643v1 (1)|Segment Anything]] 提出的可提示图像分割模型，由 MAE-pretrained ViT-H/16 image encoder、prompt encoder 和轻量 mask decoder 组成。它接受点、框、mask 及初步文本提示，并把通用分割能力暴露为可组合接口。（PDF pp. 3–5，§3）

> **英文对应表述（非逐字原文）：** SAM is a promptable segmentation model with an image encoder, prompt encoder, and lightweight mask decoder that supports point, box, mask, and preliminary text prompts.

输入图像被缩放至 `1024×1024`，image encoder 输出 `256×64×64` embedding。两层 decoder 使用 [[双向-prompt-image-cross-attention]] 融合提示与图像信息；其计算量不足 image encoder 的 1%，适合在同一 image embedding 上重复处理提示。（PDF pp. 16–17，§A）

> **英文对应表述（非逐字原文）：** The image encoder produces a 256-by-64-by-64 embedding, while the two-layer decoder uses two-way cross-attention and is computationally much smaller than the encoder.

SAM 通过 [[歧义感知多掩码预测]]处理单提示的多种合理解释：默认输出 3 个 masks，以最低损失规则训练，并用 predicted IoU 排序。3-mask 机制主要针对 whole、part、subpart 等嵌套歧义，不保证覆盖所有歧义形式。（PDF p. 17，§A）

> **英文对应表述（非逐字原文）：** For ambiguous single prompts, SAM produces three masks, applies minimum-loss training, and predicts a quality score for ranking the candidates.

模型的零样本评估涵盖单点分割、edge detection、object proposals、instance segmentation 和 text-to-mask。其优势是通用性与组合性；主要局限是细结构、断开小分量、候选排序、text-to-mask 鲁棒性，以及重量级 image encoder 带来的端到端成本。（PDF pp. 7–12，§5–7）

> **英文对应表述（非逐字原文）：** SAM transfers to several downstream segmentation tasks through prompting, but it is not uniformly optimal for fine structures, candidate ranking, text prompts, or full end-to-end latency.

相关数据资产见 [[SA-1B]]，核心任务定义见 [[可提示分割]]。