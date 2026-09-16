---
type: concept
title: 双向 prompt–image cross-attention
created: 2026-09-16
updated: 2026-09-16
tags: [cross-attention, multimodal-fusion, mask-decoder]
related: [2304.02643v1 (1), SAM, 可提示分割]
sources: ["2304.02643v1 (1).pdf"]
---
# 双向 prompt–image cross-attention

双向 prompt–image cross-attention 是 [[SAM]] mask decoder 融合提示与图像表示的核心机制。decoder 先让 prompt/output tokens 查询 image embedding，再让 image embedding 查询 tokens，使提示信息能够写回空间图像表示。（PDF pp. 4、16–17，§3 与§A）

> **英文对应表述（非逐字原文）：** The decoder alternates token-to-image and image-to-token cross-attention so that prompt information can influence both output tokens and spatial image features.

SAM 的 decoder 仅有 2 层，prompt embedding 维度为 `256`，cross-attention Q/K/V 维度为 `128`，使用 8 个 attention heads。轻量设计使 decoder 计算量不足 image encoder 的 1%，从而支持在预计算图像表示上反复进行[[可提示分割]]。（PDF pp. 16–17，§A）

> **英文对应表述（非逐字原文）：** The two-layer decoder uses 256-dimensional prompt embeddings, 128-dimensional cross-attention projections, and eight heads, making repeated prompting comparatively inexpensive.

这一机制支撑的是摊销后的快速提示响应，而不是完整图像处理流程的实时性；ViT-H/16 image encoder 仍是端到端计算的主要成本。（PDF pp. 16–17，§A）

> **英文对应表述（非逐字原文）：** Fast repeated prompting is achieved by amortizing the image encoding cost, not by making the full ViT-H image pipeline real-time.