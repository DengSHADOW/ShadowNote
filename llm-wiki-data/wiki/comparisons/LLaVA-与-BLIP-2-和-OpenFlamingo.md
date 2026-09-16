---
type: comparison
title: LLaVA 与 BLIP-2、OpenFlamingo
created: 2026-09-16
updated: 2026-09-16
tags: [模型比较, LLaVA-Bench, 多模态模型, 指令遵循]
related: [2304.08485v2, LLaVA, LLaVA-Bench, visual-instruction-tuning]
sources: ["2304.08485v2.pdf"]
---
# LLaVA 与 BLIP-2、OpenFlamingo

[[2304.08485v2|Visual Instruction Tuning]] 在 [[LLaVA-Bench]] (In-the-Wild) 上比较 [[LLaVA]]、BLIP-2 与 OpenFlamingo。三者都接收图像和问题，但只有 LLaVA 使用论文生成的 visual instruction data 进行显式 instruction tuning。（PDF pp. 2、7，§§2、5.1）

> **英文原文：** “They are not explicitly tuned with vision-language instruction data.”

| 模型 | Conversation | Detail description | Complex reasoning | All |
|---|---:|---:|---:|---:|
| OpenFlamingo | $19.3\pm0.5$ | $19.0\pm0.5$ | $19.1\pm0.7$ | $19.1\pm0.4$ |
| BLIP-2 | $54.6\pm1.4$ | $29.1\pm1.2$ | $32.9\pm0.7$ | $38.1\pm1.0$ |
| LLaVA | $57.3\pm1.9$ | $52.5\pm6.3$ | $81.7\pm1.8$ | $67.3\pm2.0$ |

*来源：PDF p. 7，Table 5；数值为三次 inference run 的 relative score mean ± std。*

LLaVA 的整体分数比 BLIP-2 高 29.2 个分数点，比 OpenFlamingo 高 48.2 个分数点。原文使用 “+29%” 与 “+48%”，但由于这些值来自同一相对评分量表的直接相减，称为“分数点”更准确。（PDF p. 7，§5.1，Table 5）

> **英文原文：** “LLaVA achieves significantly better performance compared with BLIP-2 (+29%) and OpenFlamingo (+48%).”

论文的定性示例显示 BLIP-2 与 OpenFlamingo 常退化为场景描述，而 LLaVA 更直接地遵循“解释异常之处”或“解释 meme”等 instruction。（PDF pp. 6、15，Tables 3、9）

> **英文原文：** “BLIP-2 and OpenFlamingo focus on describing the image, instead of following the user instruction.”

该比较的证据边界是 24 张图和 60 个问题，并使用 GPT-4 reference 与 judge。它支持 LLaVA 在该小型 benchmark 上的优势，不足以建立所有领域、分辨率或任务上的全面排名。