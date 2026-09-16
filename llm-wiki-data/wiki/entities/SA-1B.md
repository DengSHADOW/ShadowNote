---
type: entity
title: Segment Anything 1B（SA-1B）
created: 2026-09-16
updated: 2026-09-16
tags: [segmentation-dataset, automatic-annotation, data-governance]
related: [2304.02643v1 (1), SAM, 分割数据引擎, 隐私保护型数据发布]
sources: ["2304.02643v1 (1).pdf"]
---
# Segment Anything 1B（SA-1B）

SA-1B 是 [[2304.02643v1 (1)|Segment Anything]] 发布的大规模分割数据集，包含 11M 张获许可照片和约 1.1B 个由 [[SAM]] 自动生成的无类别 masks，平均每图约 100 个 masks。公开版本不包含模型辅助人工阶段产生的 masks、文本类别、caption 或未模糊原图。（PDF pp. 5–7，§4；PDF pp. 27–29，Dataset Card）

> **英文对应表述（非逐字原文）：** SA-1B contains 11 million licensed images and roughly 1.1 billion automatically generated, class-agnostic masks; manually produced masks, captions, and original unblurred images are not part of the release.

数据通过三阶段[[分割数据引擎]]构建。最终自动流程使用 `32×32` 全图点网格、20 个多尺度 crops、两阶段 `0.7` NMS、predicted-IoU 与 stability filters，并移除小于 `100 pixels` 的连通分量、填充同等面积阈值以下的小孔洞。（PDF p. 18，§B）

> **英文对应表述（非逐字原文）：** The final automatic pipeline uses dense point grids, multi-scale crops, two-stage non-maximum suppression, quality and stability filtering, and small-component cleanup.

抽样约 50k 个 masks 的修订实验中，94% 与专业修订结果的 IoU 超过 90%，97% 超过 75%。这些结果支持自动 masks 的总体质量，但不能证明数据不存在类别特定、地域特定或长尾遗漏。（PDF pp. 6–7，§4）

> **英文对应表述（非逐字原文）：** In a sampled professional-correction study, 94% of masks exceeded 90% IoU and 97% exceeded 75% IoU, providing aggregate rather than exhaustive quality evidence.

数据地域分布依赖 caption-based geolocation inference。Europe 占 `49.8%`，Asia & Oceania 占 `36.2%`，low income countries 仅占 `0.9%`；地点抽取存在元数据缺失、样本选择偏差和实体消歧问题。（PDF pp. 6–7，Table 1；PDF p. 18，§C）

> **英文对应表述（非逐字原文）：** Caption-derived geographic estimates show broad but uneven coverage, with low-income countries substantially underrepresented and location inference subject to ambiguity.

发布采用[[隐私保护型数据发布]]措施，包括人脸和车牌模糊及不公开未处理原图。内容报告可能导致图像被删除，且问题内容的旧版本不保留；该政策降低持续暴露风险，却与严格版本复现之间存在张力。（PDF pp. 27–29，Dataset Card）

> **英文对应表述（非逐字原文）：** The release blurs detected faces and license plates and may remove reported content without retaining the problematic prior version, creating a tradeoff between risk mitigation and exact version reproducibility.