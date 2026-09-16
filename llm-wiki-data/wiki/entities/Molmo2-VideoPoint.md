---
type: entity
title: Molmo2-VideoPoint
created: 2026-09-16
updated: 2026-09-16
tags: [dataset, video-pointing, grounding, counting]
related: [2601.10611v4, Molmo2, 统一-point-based-grounding, point-then-count]
sources: ["2601.10611v4.pdf"]
---
# Molmo2-VideoPoint

Molmo2-VideoPoint 是为开放词汇视频 pointing 构建的数据集。正文称其覆盖约 `280k` 个视频、`650k+` queries，并以 `2 fps` 提供标注帧；Table 13 则给出 `250k visual`、`450k anno.` 和 `330k ex.`，不同单位之间尚无完整映射。（PDF p. 5、p. 30，§2，Table 13）

> **英文对应表述（非逐字原文）：** Molmo2-VideoPoint provides open-vocabulary video-pointing supervision, but the reported counts use several units whose relationship is not fully explained.

标注把时间戳、顺序 object index 和归一化二维坐标编码在 point 序列中。顺序编号还支持[[point-then-count]]：输出点的数量可以转换为计数答案。（PDF pp. 27–28、53，Appendix A，Figure 29）

> **英文对应表述（非逐字原文）：** Each point combines a timestamp, sequential object index, and normalized coordinates; the indices also support point-derived counting.

该数据集连接 [[Molmo2]]、[[统一-point-based-grounding]] 与视频计数任务。来源：[[2601.10611v4|Molmo2 论文来源页]]。