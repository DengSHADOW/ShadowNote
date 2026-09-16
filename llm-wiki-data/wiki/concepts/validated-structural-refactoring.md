---
type: concept
status: draft
title: 可验证的结构重构
created: 2026-09-13
updated: 2026-09-15
tags: [agents, skills, refactoring, rollback]
related: [programmatic-skill-network, trace-guided-skill-repair]
source_id: p-3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
content_version: sha256:3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
sources: ["zotero://users/0/items/5RKUKLBV"]
---

# 可验证的结构重构

> 来源：[[zotero-users-0-5RKUKLBV|Evolving Programmatic Skill Networks]]；PDF pp. 4–5，20–24，Figures 10–14。

在一次成功执行后，PSN 只考察当前技能的父/子节点和 embedding 最近的五个技能，识别参数覆盖、子图覆盖、兄弟特化、公共子技能与完全重复等固定关系。候选重写包括 wrapper、调用替换、抽象技能合成、公共子程序抽取和 canonical merge。

**英文对应表述（非逐字原文）**：After success, the refactor searches parents, children, and five nearest semantic neighbors for five canonical structural relations and applies their prescribed rewrites.（PDF pp. 4–5, 20–24；Table 2；Figures 10–14）

变更先经过语法、类型和语义保持检查；应用后在涉及该技能的最近三个任务上比较成功率，下降超过 20% 则通过逆操作回滚。该流程是经验性安全检查，不是形式化验证。

**英文对应表述（非逐字原文）**：Pre-application checks cover syntax, type safety, and semantic preservation; applied changes are tested on three recent affected tasks and rolled back after a success-rate drop exceeding 20%.（PDF pp. 42–43，Tables 12–13）

统计口径修正：139 个 proposal 中 96 个通过预检查，43 个被拒绝。3.1%（4/131）和 6.7%（12/180）的回滚率以训练 iterations 为分母，而不是以 96 个已应用 proposal 为分母。

**英文对应表述（非逐字原文）**：The paper reports 96/139 proposals passing pre-checks, while post-application rollback rates are calculated over model-specific training iterations: 4/131 and 12/180.（PDF p. 43，Tables 12–13）

关联：[[programmatic-skill-network|程序化技能网络（PSN）]]、[[trace-guided-skill-repair|执行轨迹引导的技能修复]]。
