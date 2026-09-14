---
type: query
status: draft
source_id: p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
content_version: sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e
sources: ["raw/sources/2605.09998v1.pdf"]
title: "Red bootstrap-updating 的表现"
created: 2026-09-14
tags: [bootstrap-transfer, regression, evidence-check]
related: [continual-harness, reset-free-adaptation, create-and-forget-skill-funnel]
---

# Red bootstrap-updating 的表现

**结论：这是同一 Red 轨迹在不同时间段的表现，不是两个实验条件互相冲突。**

- 主文 Section 4.3（PDF p. 7，Figure 5）报告的里程碑—button-press 曲线中，bootstrap-updating 在所比较的里程碑上比 from-scratch 更省按键；该段据此说明先前运行形成的 harness 可以加速下一次运行。
- 附录 C.2（PDF p. 24）补充了同一设置的后段失效：约在 step 213 后，新建 sub-agents 取代了继承的 sub-agents，却没有经过 from-scratch 技能经历的修复循环。随后 Red 的 milestone staircase 回退，低于 from-scratch，最后也低于 `Hmin`。
- 因而更精确的表述是：**继承并持续实际调用已有 harness 组件时，bootstrap 有迁移价值；当 agent 放弃这些继承组件时，bootstrap-updating 会退化。** 不能把主文的“每个 milestone”扩展为完整运行期间始终占优的结论。

关联：[[sources/2605.09998v1|Continual Harness]]、[[concepts/reset-free-adaptation|Reset-Free Adaptation]]、[[concepts/create-and-forget-skill-funnel|Create-and-Forget Skill Funnel]]。
