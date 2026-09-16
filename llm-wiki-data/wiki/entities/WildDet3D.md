---
type: entity
title: WildDet3D
created: 2026-09-16
updated: 2026-09-16
tags: [model, 3D-detection, open-vocabulary, promptable, depth]
related: [2604.08626v2 (1), WildDet3D-Data, WildDet3D-Bench, 可提示-3D-目标检测, 可选深度的双编码器融合]
sources: ["2604.08626v2 (1).pdf"]
---
# WildDet3D

WildDet3D 是面向开放词汇单目 3D 目标检测的模型，接受 RGB image、可选 camera intrinsics、可选 partial/full depth，以及 text、point、box 或 exemplar prompt。输出为 metric 3D center、dimensions、orientation 和 confidence。（PDF pp. 4–7，§2）

> **英文对应表述（非逐字原文）：** WildDet3D predicts metric 3D boxes from one RGB image under several prompt modalities and can additionally consume camera calibration or depth.

## 架构

模型以独立的 semantic image encoder 和 RGBD geometry encoder 形成 dual-backbone，再通过 zero-initialized residual module 融合 depth latents。promptable detector 统一编码不同 prompt，3D head 则依次聚合 camera-ray、depth、2D spatial 与 semantic information。（PDF pp. 4–7，Figures 2–3，§2.1–2.3）

> **英文对应表述（非逐字原文）：** Separate semantic and geometric backbones are reunited before prompt-conditioned decoding and metric 3D regression.

该设计对应 [[可选深度的双编码器融合]]与[[可提示-3D-目标检测]]。它借鉴 SAM 3 的 image encoder 与 prompt encoding，但不应与现有 [[SAM]] 页面所描述的早期 Segment Anything Model 合并。

> **英文对应表述（非逐字原文）：** SAM 3 supplies initialization and prompt-design components, but WildDet3D remains a distinct 3D detection system.

## 证据

在 Omni3D-only 的同数据比较中，WildDet3D 的 text-prompt AP 为 `34.2`，高于 3D-MOOD Swin-B 的 `30.0`；box-prompt AP 为 `36.4`，高于 DetAny3D 的 `34.4`。加入 depth 后分别达到 `41.6` 和 `45.8`。（PDF pp. 15–16，§4.3，Table 4）

> **英文对应表述（非逐字原文）：** WildDet3D leads the reported Omni3D comparisons in both prompt modes, with further gains when depth is supplied.

在 Stereo4D 的小规模 zero-shot box-prompt 测试中，无 depth 的 WildDet3D 为 `7.5 AP`，低于 OVMono3D-LIFT 的 `9.9 AP`；接入真实 stereo depth 后为 `27.7 AP`。（PDF pp. 16–17，§4.5，Table 6）

> **英文对应表述（非逐字原文）：** The model is not the strongest monocular baseline on Stereo4D, but it benefits markedly from real stereo depth.

## 限制

模型仍受 camera intrinsics 误差、单图尺度歧义、遮挡、近对称物体旋转歧义和 dual-backbone 计算成本影响。作者明确表示完整模型不适合未经 distillation 或 quantization 的实时端侧运行，也不面向 safety-critical use。（PDF p. 22，§7）

> **英文对应表述（非逐字原文）：** Calibration, monocular ambiguity, rotation, and computation remain unresolved deployment constraints.

来源：[[2604.08626v2 (1)|WildDet3D 论文来源]]。