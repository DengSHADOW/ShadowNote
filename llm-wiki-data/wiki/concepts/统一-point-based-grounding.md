---
type: concept
title: 统一 point-based grounding
created: 2026-09-16
updated: 2026-09-16
tags: [grounding, pointing, tracking, multimodal]
related: [2601.10611v4, Molmo2, point-then-count, 身份保持的-point-tracking]
sources: ["2601.10611v4.pdf"]
---
# 统一 point-based grounding

统一 point-based grounding 是 Molmo2 用于单图、多图和视频任务的共享输出表示。其基础字段是 object index 与归一化二维坐标；视频任务增加时间戳，多图任务增加 image index。（PDF pp. 2–3、27–28、53–55，Figures 1、29–33）

> **英文对应表述（非逐字原文）：** Molmo2 uses a shared point representation whose fields can include object index, normalized coordinates, timestamp, and image index.

顺序 object indices 使同一表示同时支持 counting 与 tracking：最后一个顺序编号可反映对象总数，同一编号跨时间重复则表示对象身份延续。这分别连接 [[point-then-count]] 与[[身份保持的-point-tracking|身份保持的 point tracking]]。（PDF pp. 27–28，Appendix A）

> **英文对应表述（非逐字原文）：** Sequential object indices connect counting and tracking by representing total instances and preserving identity across time.

该格式扩大了统一接口的任务覆盖，但格式合法不保证语义正确。论文的定性失败包括假阳性、漏检、repeated points 与可能的[[跨样例答案复制]]。（PDF pp. 46–48、58，Appendix H，Figure 36）

> **英文对应表述（非逐字原文）：** A valid structured output does not ensure semantic correctness; observed failures include false positives, missed objects, repeated points, and possible response copying.

来源：[[2601.10611v4|Molmo2 论文来源页]]。