---
type: concept
title: 无歧义 3D box rotation normalization
created: 2026-09-16
updated: 2026-09-16
tags: [3D-box, rotation, normalization, 6D-representation]
related: [2604.08626v2 (1), WildDet3D, 开放词汇单目-3D-目标检测]
sources: ["2604.08626v2 (1).pdf"]
---
# 无歧义 3D box rotation normalization

有向 3D box 存在等价参数化：交换 width 与 length 并旋转 `90°`，或对对称对象执行 `180°` yaw flip，可能描述相同几何 box。这会使一个物体对应多个 regression targets。（PDF p. 7，§2.3）

> **英文对应表述（非逐字原文）：** Equivalent dimension and yaw combinations can represent the same oriented cuboid, creating ambiguous regression labels.

[[WildDet3D]]先在 `w > l` 时交换 `(w,l)` 并旋转 `90°`，从而保证 `w ≤ l`；再通过 `180°` rotation 将 yaw 折叠到 `[0,\pi)`。作者称这会把四重 rotation–dimension ambiguity 收敛为唯一形式。（PDF p. 7，§2.3）

> **英文对应表述（非逐字原文）：** Dimension ordering followed by yaw folding maps equivalent boxes to one normalized representation.

模型另以 rotation matrix 前两行组成连续 6D representation，并用 Gram–Schmidt orthogonalization 恢复完整 rotation matrix。（PDF p. 7，§2.3，Eq. 5）

> **英文对应表述（非逐字原文）：** A continuous six-dimensional representation is converted back to a valid rotation matrix through orthogonalization.

该规范化减少标签层面的离散歧义，但不能消除圆桌、方盒等近对称对象在视觉证据上的 orientation ambiguity。论文仍将 rotation estimation 列为薄弱环节。（PDF p. 22，§7）

> **英文对应表述（非逐字原文）：** Canonical labels do not resolve orientation when object appearance itself provides insufficient directional evidence.

来源：[[2604.08626v2 (1)|WildDet3D 论文来源]]。